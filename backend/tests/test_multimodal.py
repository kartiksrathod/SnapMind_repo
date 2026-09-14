from fastapi.testclient import TestClient

from app.main import app


def test_multimodal_capabilities_are_honest() -> None:
    payload = TestClient(app).get('/api/multimodal/capabilities').json()
    assert set(payload) == {'ocr', 'image_understanding', 'speech_to_text'}
    assert payload['image_understanding']['status'] == 'unavailable'
    assert 'not enabled' in payload['image_understanding']['limitation'].lower()