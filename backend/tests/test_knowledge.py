from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from app import main
from app.documents.service import DocumentService
from app.documents.storage import DocumentStorage
from app.knowledge.service import KnowledgeService
from app.knowledge.vector_store import SQLiteVectorStore


def configured_client(tmp_path: Path) -> TestClient:
    storage = DocumentStorage(tmp_path / 'documents')
    knowledge = KnowledgeService(SQLiteVectorStore(tmp_path / 'knowledge.sqlite3', dimensions=512))
    main.knowledge_service = knowledge
    main.document_service = DocumentService(storage, indexer=knowledge)
    return TestClient(main.app)


def upload(client: TestClient, filename: str, text: str) -> dict:
    return client.post('/api/documents', files={'file': (filename, BytesIO(text.encode()), 'text/plain')}).json()


def test_retrieval_returns_relevant_source_metadata(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    first = upload(client, 'alpha.txt', 'Quantum computing uses qubits and quantum gates.')
    second = upload(client, 'beta.txt', 'Bread recipes use flour, water, yeast, and salt.')
    response = client.post('/api/knowledge/search', json={'query': 'What uses qubits?', 'top_k': 2})
    assert response.status_code == 200
    results = response.json()['results']
    assert results[0]['document_id'] == first['document_id']
    assert results[0]['filename'] == 'alpha.txt'
    assert results[0]['position'] == 0
    assert results[0]['relevance'] > 0
    assert {item['document_id'] for item in results} == {first['document_id']}
    second_results = client.post('/api/knowledge/search', json={'query': 'flour yeast', 'top_k': 2}).json()['results']
    assert second_results[0]['document_id'] == second['document_id']


def test_search_validation_filters_and_deleted_index(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    first = upload(client, 'alpha.txt', 'Quantum computing uses qubits.')
    second = upload(client, 'beta.txt', 'Bread recipes use flour.')
    assert client.post('/api/knowledge/search', json={'query': '   '}).status_code == 400
    filtered = client.post('/api/knowledge/search', json={'query': 'flour', 'document_ids': [first['document_id']]}).json()
    assert filtered['results'] == []
    assert client.delete(f"/api/documents/{second['document_id']}").status_code == 204
    remaining = client.post('/api/knowledge/search', json={'query': 'flour'}).json()
    assert remaining['results'] == []
    status = client.get(f"/api/knowledge/status/{first['document_id']}").json()
    assert status['chunk_count'] == 1
    assert status['status'] == 'indexed'


def test_missing_index_returns_empty_results(tmp_path: Path) -> None:
    client = configured_client(tmp_path)
    response = client.post('/api/knowledge/search', json={'query': 'anything'})
    assert response.status_code == 200
    assert response.json()['indexed_chunks'] == 0
    assert response.json()['results'] == []
