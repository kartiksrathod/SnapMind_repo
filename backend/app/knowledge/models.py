from pydantic import BaseModel, Field


class KnowledgeChunk(BaseModel):
    document_id: str
    chunk_id: str
    page: int | None = None
    section: str | None = None
    text: str
    position: int
    relevance: float = Field(ge=0, le=1)
    filename: str
    file_type: str


class KnowledgeSearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    document_ids: list[str] | None = None


class KnowledgeSearchResponse(BaseModel):
    query: str
    indexed_chunks: int
    results: list[KnowledgeChunk]


class KnowledgeStatus(BaseModel):
    document_id: str
    chunk_count: int
    status: str
