from io import BytesIO
from pathlib import Path

from docx import Document
from fastapi.testclient import TestClient
from reportlab.pdfgen.canvas import Canvas

from app import main
from app.documents.service import DocumentService
from app.documents.storage import DocumentStorage


def client_with_tmp_storage(tmp_path: Path) -> TestClient:
    main.document_service = DocumentService(DocumentStorage(tmp_path / 'documents'))
    return TestClient(main.app)


def test_supported_text_formats_and_metadata(tmp_path: Path) -> None:
    client = client_with_tmp_storage(tmp_path)
    for filename, content in [('notes.txt', b'Local notes'), ('readme.md', b'# Local readme')]:
        response = client.post('/api/documents', files={'file': (filename, BytesIO(content), 'text/plain')})
        assert response.status_code == 201
        assert response.json()['processing_status'] == 'indexed'
        assert response.json()['text_length'] > 0


def test_valid_pdf_and_docx_are_processed(tmp_path: Path) -> None:
    client = client_with_tmp_storage(tmp_path)
    pdf_buffer = BytesIO()
    canvas = Canvas(pdf_buffer)
    canvas.drawString(72, 72, 'A local PDF document')
    canvas.save()
    pdf = client.post('/api/documents', files={'file': ('one-page.pdf', BytesIO(pdf_buffer.getvalue()))})
    assert pdf.status_code == 201
    assert pdf.json()['processing_status'] == 'indexed'
    assert pdf.json()['page_count'] == 1

    docx_buffer = BytesIO()
    document = Document()
    document.add_paragraph('A local DOCX document')
    document.save(docx_buffer)
    docx = client.post('/api/documents', files={'file': ('notes.docx', BytesIO(docx_buffer.getvalue()))})
    assert docx.status_code == 201
    assert docx.json()['processing_status'] == 'indexed'
    assert docx.json()['text_length'] > 0


def test_empty_unsupported_duplicate_and_delete(tmp_path: Path) -> None:
    client = client_with_tmp_storage(tmp_path)
    assert client.post('/api/documents', files={'file': ('empty.txt', BytesIO(b''))}).status_code == 400
    assert client.post('/api/documents', files={'file': ('image.png', BytesIO(b'png'))}).status_code == 400
    first = client.post('/api/documents', files={'file': ('notes.txt', BytesIO(b'Unique'))})
    assert client.post('/api/documents', files={'file': ('copy.txt', BytesIO(b'Unique'))}).status_code == 400
    document_id = first.json()['document_id']
    assert client.delete(f'/api/documents/{document_id}').status_code == 204
    assert client.get('/api/documents').json()['documents'] == []


def test_corrupt_pdf_and_docx_are_reported(tmp_path: Path) -> None:
    client = client_with_tmp_storage(tmp_path)
    pdf = client.post('/api/documents', files={'file': ('broken.pdf', BytesIO(b'not a pdf'))})
    assert pdf.status_code == 201
    assert pdf.json()['processing_status'] == 'failed'
    docx = client.post('/api/documents', files={'file': ('broken.docx', BytesIO(b'not a docx'))})
    assert docx.status_code == 201
    assert docx.json()['processing_status'] == 'failed'
