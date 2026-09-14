from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['phase'] == '8'


def test_unavailable_capabilities_are_honest() -> None:
    assert client.get('/api/models').json()['status'] in {'ready', 'unavailable'}
    assert client.get('/api/hardware').json()['status'] == 'available'


def test_dashboard_snapshot_has_real_counts() -> None:
    response = client.get('/api/dashboard')
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload['document_count'], int)
    assert isinstance(payload['indexed_chunk_count'], int)
    assert 'ai' in payload and 'hardware' in payload
