from pathlib import Path

from .documents.models import DocumentRecord
from .documents.service import DuplicateDocumentError, DocumentService

DEMO_ROOT = Path(__file__).resolve().parents[2] / 'demo' / 'documents'
DEMO_FILES = ('quantum-notes.md', 'local-ai-principles.md')


def prepare(service: DocumentService) -> list[DocumentRecord]:
    records = []
    for filename in DEMO_FILES:
        path = DEMO_ROOT / filename
        if not path.exists():
            raise FileNotFoundError(f'Demo document is missing: {filename}')
        try:
            records.append(service.import_bytes(filename, path.read_bytes()))
        except DuplicateDocumentError:
            existing = next((item for item in service.storage.list_documents() if item.filename == filename), None)
            if existing:
                records.append(existing)
    return records
