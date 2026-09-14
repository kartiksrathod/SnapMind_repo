from ..knowledge.models import KnowledgeChunk
from ..knowledge.service import KnowledgeService
from .models import ChatMessage, ChatResponse, Citation
from .backends import InferenceBackend, select_backend
from .providers import LLMProvider, ModelUnavailableError

UNCERTAINTY = "I couldn't find enough information in your knowledge base to answer this reliably."


class ContextBuilder:
    def build(self, query: str, chunks: list[KnowledgeChunk]) -> str:
        sources = '\n\n'.join(f'[{index}] {chunk.filename} | page={chunk.page or "unknown"} | section={chunk.section or "unknown"}\n{chunk.text}' for index, chunk in enumerate(chunks, 1))
        return f"""You are SnapMind, a local document-grounded assistant. Answer the user's question using only the provided source context. Do not use outside knowledge, invent facts, or invent citations. If the context does not support an answer, say that you could not find enough information. Keep the response concise and cite supporting source numbers like [1].\n\nUser question:\n{query}\n\nSource context:\n{sources}"""


class ChatOrchestrator:
    def __init__(self, knowledge: KnowledgeService, provider: LLMProvider, context_builder: ContextBuilder | None = None, backend: InferenceBackend | None = None) -> None:
        self.knowledge = knowledge
        self.provider = provider
        self.context_builder = context_builder or ContextBuilder()
        self.backend = backend or select_backend()
        self.sessions: dict[str, list[ChatMessage]] = {}

    def answer(self, query: str, session_id: str, top_k: int, document_ids: list[str] | None = None) -> ChatResponse:
        clean_query = query.strip()
        if not clean_query:
            raise ValueError('Question cannot be empty.')
        retrieval = self.knowledge.search(clean_query, top_k, document_ids)
        chunks = retrieval.results
        citations = [Citation(citation_id=index, document_id=chunk.document_id, document_name=chunk.filename, page=chunk.page, section=chunk.section, chunk_id=chunk.chunk_id) for index, chunk in enumerate(chunks, 1)]
        history = self.sessions.setdefault(session_id, [])
        user_message = ChatMessage(role='user', content=clean_query)
        if not chunks:
            answer = UNCERTAINTY
            status = 'insufficient_context'
        else:
            prompt = self.context_builder.build(clean_query, chunks)
            try:
                answer = self.backend.generate(self.provider, prompt, [{'role': message.role, 'content': message.content} for message in history[-6:]])
            except ModelUnavailableError:
                raise
            status = 'grounded'
        assistant_message = ChatMessage(role='assistant', content=answer, citations=citations)
        history.extend([user_message, assistant_message])
        return ChatResponse(session_id=session_id, answer=answer, citations=citations, retrieved_chunks=chunks, model=self.provider.model_name, status=status, history=history)
