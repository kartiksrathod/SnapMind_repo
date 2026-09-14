import json
from pathlib import Path

from fastapi.testclient import TestClient

from app import main
from app.ai.providers import LLMProvider
from app.documents.service import DocumentService
from app.documents.storage import DocumentStorage
from app.knowledge.service import KnowledgeService
from app.knowledge.vector_store import SQLiteVectorStore


class StudyProvider(LLMProvider):
    @property
    def model_name(self) -> str:
        return 'test-study-model'

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, history=None) -> str:
        if 'Create a summary' in prompt:
            return json.dumps({'short_summary': 'Quantum computing uses qubits.', 'detailed_summary': 'The source describes qubits as the unit of quantum information.', 'section_summaries': [{'title': 'Basics', 'summary': 'Qubits hold quantum information.', 'source_ids': [1]}]})
        if 'Extract important' in prompt:
            return json.dumps({'key_points': [{'type': 'definition', 'text': 'A qubit is a unit of quantum information.', 'source_ids': [1]}]})
        if 'Create up to 5' in prompt:
            return json.dumps({'questions': [{'question': 'What holds quantum information?', 'options': ['A qubit', 'A folder'], 'correct_answer': 'A qubit', 'explanation': 'The source defines a qubit this way.', 'source_ids': [1]}]})
        return json.dumps({'flashcards': [{'question': 'What is a qubit?', 'answer': 'A unit of quantum information.', 'source_ids': [1]}]})


def configured_client(tmp_path: Path) -> TestClient:
    storage = DocumentStorage(tmp_path / 'documents')
    knowledge = KnowledgeService(SQLiteVectorStore(tmp_path / 'knowledge.sqlite3', dimensions=512))
    main.knowledge_service = knowledge
    main.document_service = DocumentService(storage, indexer=knowledge)
    main.productivity_service = main.ProductivityService(knowledge, StudyProvider(), main.chat_orchestrator.backend)
    return TestClient(main.app)


def test_all_study_features_generate_traceable_local_content(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    uploaded = client.post('/api/documents', files={'file': ('quantum.txt', b'Quantum computing uses qubits. A qubit is a unit of quantum information.')})
    assert uploaded.status_code == 201
    for endpoint, key in [('/api/study/summary', 'short_summary'), ('/api/study/key-points', 'key_points'), ('/api/study/quiz', 'questions'), ('/api/study/flashcards', 'flashcards')]:
        response = client.post(endpoint, json={})
        assert response.status_code == 200
        assert response.json()['data'][key]
        assert response.json()['citations'][0]['document_name'] == 'quantum.txt'


def test_empty_knowledge_and_invalid_source_are_errors(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    assert client.post('/api/study/summary', json={}).status_code == 400
    class InvalidProvider(StudyProvider):
        def generate(self, prompt: str, history=None) -> str:
            return json.dumps({'key_points': [{'type': 'fact', 'text': 'Unknown', 'source_ids': [99]}]})
    main.productivity_service = main.ProductivityService(main.knowledge_service, InvalidProvider(), main.chat_orchestrator.backend)
    client.post('/api/documents', files={'file': ('source.txt', b'Grounded fact')})
    assert client.post('/api/study/key-points', json={}).status_code == 502
