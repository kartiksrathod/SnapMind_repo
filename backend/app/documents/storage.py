import hashlib
import json
from pathlib import Path

from .models import DocumentRecord


class DocumentStorage:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.index_path = root / 'documents.json'

    def list_documents(self) -> list[DocumentRecord]:
        if not self.index_path.exists():
            return []
        try:
            data = json.loads(self.index_path.read_text(encoding='utf-8'))
            return [DocumentRecord.model_validate(item) for item in data]
        except (OSError, ValueError):
            return []

    def save_index(self, documents: list[DocumentRecord]) -> None:
        temporary_path = self.index_path.with_suffix('.tmp')
        temporary_path.write_text(json.dumps([document.model_dump(mode='json') for document in documents], indent=2), encoding='utf-8')
        temporary_path.replace(self.index_path)

    def get(self, document_id: str) -> DocumentRecord | None:
        return next((document for document in self.list_documents() if document.document_id == document_id), None)

    def add(self, document: DocumentRecord) -> None:
        documents = self.list_documents()
        documents.append(document)
        self.save_index(documents)

    def update(self, document: DocumentRecord) -> None:
        documents = self.list_documents()
        self.save_index([document if item.document_id == document.document_id else item for item in documents])

    def delete(self, document_id: str) -> None:
        documents = [item for item in self.list_documents() if item.document_id != document_id]
        self.save_index(documents)
        document_dir = self.root / document_id
        if document_dir.exists():
            for path in document_dir.iterdir():
                path.unlink()
            document_dir.rmdir()

    def content_path(self, document_id: str, filename: str) -> Path:
        directory = self.root / document_id
        directory.mkdir(parents=True, exist_ok=True)
        return directory / filename

    @staticmethod
    def content_hash(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()
