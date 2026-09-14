from pathlib import Path

from ..documents.models import DocumentRecord
from ..documents.parsers import ParsedDocument, parser_for
from .chunking import TextChunker
from .embeddings import EmbeddingService, HashingEmbeddingService
from .models import KnowledgeChunk, KnowledgeSearchResponse, KnowledgeStatus
from .vector_store import SQLiteVectorStore


class KnowledgeService:
    def __init__(self, store: SQLiteVectorStore, embedder: EmbeddingService | None = None, chunker: TextChunker | None = None) -> None:
        self.store = store
        self.embedder = embedder or HashingEmbeddingService(dimensions=store.dimensions)
        self.chunker = chunker or TextChunker()

    def index_document(self, document: DocumentRecord, source_path: Path) -> int:
        parsed = parser_for(source_path.suffix).parse(source_path)
        return self.index_parsed(document, parsed)

    def index_parsed(self, document: DocumentRecord, parsed: ParsedDocument) -> int:
        chunks = self.chunker.chunk(parsed.segments or [])
        knowledge_chunks = [KnowledgeChunk(document_id=document.document_id, chunk_id=f'{document.document_id}:{item.position}', page=item.page, section=item.section, text=item.text, position=item.position, relevance=0, filename=document.filename, file_type=document.file_type) for item in chunks]
        vectors = self.embedder.embed([chunk.text for chunk in knowledge_chunks])
        self.store.replace_document(document.document_id, document.filename, document.file_type, knowledge_chunks, vectors)
        return len(knowledge_chunks)

    def remove_document(self, document_id: str) -> None:
        self.store.delete_document(document_id)

    def search(self, query: str, top_k: int, document_ids: list[str] | None = None) -> KnowledgeSearchResponse:
        clean_query = query.strip()
        if not clean_query:
            raise ValueError('Search query cannot be empty.')
        vector = self.embedder.embed([clean_query])[0]
        scored = self.store.search(vector, top_k, document_ids)
        results = [chunk.model_copy(update={'relevance': score}) for chunk, score in scored]
        return KnowledgeSearchResponse(query=clean_query, indexed_chunks=self.store.count(), results=results)

    def status(self, document_id: str) -> KnowledgeStatus:
        count = self.store.count(document_id)
        return KnowledgeStatus(document_id=document_id, chunk_count=count, status='indexed' if count else 'not_indexed')

    def chunks(self, document_ids: list[str] | None = None) -> list[KnowledgeChunk]:
        return self.store.chunks(document_ids)
