from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from .models import DocumentRecord
from .parsers import DocumentParseError, parser_for
from .storage import DocumentStorage

ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.md', '.markdown', '.docx'}
MAX_FILE_SIZE = 50 * 1024 * 1024


class DocumentValidationError(Exception):
    pass


class DuplicateDocumentError(Exception):
    pass


class DocumentService:
    def __init__(self, storage: DocumentStorage, indexer=None) -> None:
        self.storage = storage
        self.indexer = indexer

    async def import_document(self, upload: UploadFile) -> DocumentRecord:
        filename = Path(upload.filename or '').name
        extension = Path(filename).suffix.lower()
        if not filename or extension not in ALLOWED_EXTENSIONS:
            raise DocumentValidationError('Unsupported file format. Use PDF, TXT, Markdown, or DOCX.')
        content = await upload.read()
        if not content:
            raise DocumentValidationError('The selected file is empty.')
        if len(content) > MAX_FILE_SIZE:
            raise DocumentValidationError('The file is too large. Maximum size is 50 MB.')
        content_hash = self.storage.content_hash(content)
        if any(document.content_hash == content_hash for document in self.storage.list_documents()):
            raise DuplicateDocumentError('This document has already been imported.')

        document_id = uuid4().hex
        path = self.storage.content_path(document_id, filename)
        path.write_bytes(content)
        now = datetime.now(timezone.utc)
        record = DocumentRecord(document_id=document_id, filename=filename, file_type=extension.lstrip('.'), file_size=len(content), created_at=now, processing_status='processing', content_hash=content_hash)
        self.storage.add(record)
        return self._process(record, path)

    def import_bytes(self, filename: str, content: bytes) -> DocumentRecord:
        """Import trusted local bytes through the same validation and processing path."""
        upload = UploadFile(filename=filename)
        upload.file.write(content)
        upload.file.seek(0)
        import asyncio
        return asyncio.run(self.import_document(upload))

    def retry(self, document_id: str) -> DocumentRecord:
        record = self.storage.get(document_id)
        if record is None:
            raise KeyError(document_id)
        path = self.storage.content_path(document_id, record.filename)
        return self._process(record.model_copy(update={'processing_status': 'processing', 'error_message': None}), path)

    def delete(self, document_id: str) -> None:
        if self.storage.get(document_id) is None:
            raise KeyError(document_id)
        if self.indexer:
            self.indexer.remove_document(document_id)
        self.storage.delete(document_id)

    def _process(self, record: DocumentRecord, path: Path) -> DocumentRecord:
        try:
            parsed = parser_for(path.suffix).parse(path)
            result = record.model_copy(update={'processing_status': 'indexed', 'page_count': parsed.page_count, 'text_length': len(parsed.text), 'error_message': None})
            text_path = path.parent / 'extracted.txt'
            text_path.write_text(parsed.text, encoding='utf-8')
        except (DocumentParseError, OSError) as exc:
            result = record.model_copy(update={'processing_status': 'failed', 'error_message': str(exc)})
        self.storage.update(result)
        if self.indexer:
            self.indexer.remove_document(record.document_id)
            if result.processing_status == 'indexed':
                try:
                    self.indexer.index_parsed(result, parsed)
                except Exception as exc:
                    result = result.model_copy(update={'processing_status': 'failed', 'error_message': f'Knowledge indexing failed: {exc}'})
                    self.storage.update(result)
        return result

