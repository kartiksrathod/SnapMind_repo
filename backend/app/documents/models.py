from datetime import datetime
from typing import Literal

from pydantic import BaseModel

ProcessingStatus = Literal['processing', 'indexed', 'failed']


class DocumentRecord(BaseModel):
    document_id: str
    filename: str
    file_type: str
    file_size: int
    created_at: datetime
    page_count: int | None = None
    processing_status: ProcessingStatus
    error_message: str | None = None
    text_length: int = 0
    content_hash: str = ''


class DocumentListResponse(BaseModel):
    documents: list[DocumentRecord]
