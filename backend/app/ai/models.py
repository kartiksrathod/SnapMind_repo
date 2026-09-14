from pydantic import BaseModel, Field

from ..knowledge.models import KnowledgeChunk


class Citation(BaseModel):
    citation_id: int
    document_id: str
    document_name: str
    page: int | None = None
    section: str | None = None
    chunk_id: str


class ChatRequest(BaseModel):
    query: str
    session_id: str = 'default'
    top_k: int = Field(default=5, ge=1, le=10)
    document_ids: list[str] | None = None


class StudyRequest(BaseModel):
    document_ids: list[str] | None = None
    detail: str = 'short'


class ChatMessage(BaseModel):
    role: str
    content: str
    citations: list[Citation] = Field(default_factory=list)


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    citations: list[Citation]
    retrieved_chunks: list[KnowledgeChunk]
    model: str
    status: str
    history: list[ChatMessage]
