from pathlib import Path

from fastapi.testclient import TestClient

from app import main
from app.ai.backends import CPUBackend, select_backend


def test_hardware_report_is_explicit_about_unknown_npu() -> None:
    response = TestClient(main.app).get('/api/hardware')
    assert response.status_code == 200
    payload = response.json()
    assert payload['device']['cpu']['status'] == 'available'
    assert payload['device']['npu']['evidence'] == 'NPU execution not verified'


def test_backend_selection_uses_safe_verified_fallback() -> None:
    backend = select_backend()
    assert isinstance(backend, CPUBackend)
    assert backend.report.backend == 'CPU'
    assert backend.report.status == 'active'
    assert 'not verified' in backend.report.limitation
