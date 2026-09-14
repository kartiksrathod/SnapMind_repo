from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main
from app.ai.providers import LLMProvider, ModelUnavailableError
from app.documents.service import DocumentService
from app.documents.storage import DocumentStorage
from app.knowledge.service import KnowledgeService
from app.knowledge.vector_store import SQLiteVectorStore


class FakeProvider(LLMProvider):
    @property
    def model_name(self) -> str:
        return 'test-local-model'

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, history=None) -> str:
        assert 'Quantum computing uses qubits' in prompt
        return 'Quantum computing uses qubits for information processing. [1]'


class UnavailableProvider(FakeProvider):
    def is_available(self) -> bool:
        return False

    def generate(self, prompt: str, history=None) -> str:
        raise ModelUnavailableError('test model unavailable')


def configured_client(tmp_path: Path, provider: LLMProvider = FakeProvider()) -> TestClient:
    storage = DocumentStorage(tmp_path / 'documents')
    knowledge = KnowledgeService(SQLiteVectorStore(tmp_path / 'knowledge.sqlite3', dimensions=512))
    main.knowledge_service = knowledge
    main.document_service = DocumentService(storage, indexer=knowledge)
    main.chat_orchestrator = main.ChatOrchestrator(knowledge, provider)
    return TestClient(main.app)


def test_grounded_answer_contains_real_citation_and_history(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    upload = client.post('/api/documents', files={'file': ('quantum.txt', b'Quantum computing uses qubits for information processing.')})
    response = client.post('/api/chat', json={'query': 'What uses qubits?', 'session_id': 'session-1'})
    payload = response.json()
    assert response.status_code == 200
    assert payload['status'] == 'grounded'
    assert payload['model'] == 'test-local-model'
    assert payload['citations'][0]['document_name'] == 'quantum.txt'
    assert payload['citations'][0]['page'] is None
    assert len(payload['history']) == 2
    assert upload.status_code == 201


def test_no_evidence_returns_uncertainty_without_model_call(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    response = client.post('/api/chat', json={'query': 'What is the weather?', 'session_id': 'empty'})
    payload = response.json()
    assert response.status_code == 200
    assert payload['status'] == 'insufficient_context'
    assert payload['citations'] == []
    assert 'couldn\'t find enough information' in payload['answer']


def test_empty_query_and_unavailable_model(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    assert client.post('/api/chat', json={'query': '  '}).status_code == 400
    client = configured_client(tmp_path / 'unavailable', UnavailableProvider())
    client.post('/api/documents', files={'file': ('quantum.txt', b'Quantum computing uses qubits.')})
    response = client.post('/api/chat', json={'query': 'What uses qubits?'})
    assert response.status_code == 503
    assert 'unavailable' in response.json()['detail']


def test_multi_document_chat_preserves_source_identity(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    first = client.post('/api/documents', files={'file': ('first.txt', b'Quantum computing uses qubits.')}).json()
    client.post('/api/documents', files={'file': ('second.txt', b'Bread recipes use flour.')})
    response = client.post('/api/chat', json={'query': 'What uses qubits?', 'document_ids': [first['document_id']]})
    assert response.status_code == 200
    assert {chunk['document_id'] for chunk in response.json()['retrieved_chunks']} == {first['document_id']}
    assert response.json()['citations'][0]['document_name'] == 'first.txt'
