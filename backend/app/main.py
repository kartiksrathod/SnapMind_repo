from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .documents.models import DocumentListResponse, DocumentRecord
from .documents.service import DocumentService, DocumentValidationError, DuplicateDocumentError
from .documents.storage import DocumentStorage
from .knowledge.service import KnowledgeService
from .knowledge.vector_store import SQLiteVectorStore
from .knowledge.models import KnowledgeSearchRequest, KnowledgeSearchResponse, KnowledgeStatus
from .ai.models import ChatRequest, ChatResponse, StudyRequest
from .ai.orchestrator import ChatOrchestrator
from .ai.providers import ModelUnavailableError, OllamaProvider
from .ai.productivity import ProductivityGenerationError, ProductivityService
from .ai.catalog import catalog
from .hardware.capabilities import detect_hardware
from .multimodal.capabilities import detect_multimodal_capabilities
from .dashboard import DashboardSnapshot, snapshot
from .benchmark import RetrievalBenchmarkRequest, RetrievalBenchmarkResult, run_retrieval
from .demo import prepare

app = FastAPI(title="SnapMind API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
data_root = Path(__file__).resolve().parents[2] / 'data'
document_storage = DocumentStorage(data_root / 'documents')
knowledge_service = KnowledgeService(SQLiteVectorStore(data_root / 'knowledge.sqlite3', dimensions=512))
document_service = DocumentService(document_storage, indexer=knowledge_service)
llm_provider = OllamaProvider()
chat_orchestrator = ChatOrchestrator(knowledge_service, llm_provider)
productivity_service = ProductivityService(knowledge_service, llm_provider, chat_orchestrator.backend)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "snapmind-api", "phase": "8"}


@app.get("/api/models")
def models() -> dict[str, object]:
    available = llm_provider.is_available()
    return {
        "status": "ready" if available else "unavailable",
        "message": f"Development candidate: {llm_provider.model_name}." if available else f"Local model {llm_provider.model_name} is unavailable. Start Ollama to enable chat.",
        "models": [llm_provider.model_name] if available else [],
        "candidates": catalog(),
    }


@app.get("/api/hardware")
def hardware() -> dict[str, object]:
    capabilities = detect_hardware()
    return {"status": "available", "message": "Only operating-system and runtime evidence is reported.", "device": capabilities.as_dict()}


@app.get("/api/config")
def config() -> dict[str, object]:
    return {"status": "ok", "processing_mode": "local", "cloud_features": False}


@app.get('/api/multimodal/capabilities')
def multimodal_capabilities() -> dict[str, object]:
    return detect_multimodal_capabilities().as_dict()


@app.get('/api/dashboard', response_model=DashboardSnapshot)
def dashboard() -> DashboardSnapshot:
    return snapshot(document_storage, knowledge_service, llm_provider)


@app.post('/api/demo/prepare', response_model=list[DocumentRecord])
def prepare_demo() -> list[DocumentRecord]:
    return prepare(document_service)


@app.post('/api/benchmark/retrieval', response_model=RetrievalBenchmarkResult)
def benchmark_retrieval(request: RetrievalBenchmarkRequest) -> RetrievalBenchmarkResult:
    try:
        return run_retrieval(request, knowledge_service, chat_orchestrator.backend, llm_provider)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get('/api/runtime')
def runtime() -> dict[str, object]:
    report = chat_orchestrator.backend.report
    return {"backend": report.backend, "runtime": report.runtime, "status": report.status, "evidence": report.evidence, "limitation": report.limitation, "model": llm_provider.model_name}


@app.get('/api/documents', response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    return DocumentListResponse(documents=document_service.storage.list_documents())


@app.post('/api/documents', response_model=DocumentRecord, status_code=201)
async def upload_document(file: UploadFile = File(...)) -> DocumentRecord:
    try:
        return await document_service.import_document(file)
    except (DocumentValidationError, DuplicateDocumentError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post('/api/documents/{document_id}/retry', response_model=DocumentRecord)
def retry_document(document_id: str) -> DocumentRecord:
    try:
        return document_service.retry(document_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail='Document not found.') from exc


@app.delete('/api/documents/{document_id}', status_code=204)
def delete_document(document_id: str) -> None:
    try:
        document_service.delete(document_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail='Document not found.') from exc


@app.post('/api/knowledge/search')
def search_knowledge(request: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
    try:
        return knowledge_service.search(request.query, request.top_k, request.document_ids)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get('/api/knowledge/status/{document_id}', response_model=KnowledgeStatus)
def knowledge_status(document_id: str) -> KnowledgeStatus:
    return knowledge_service.status(document_id)


@app.post('/api/chat', response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        return chat_orchestrator.answer(request.query, request.session_id, request.top_k, request.document_ids)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail='Local retrieval or generation failed.') from exc


def _study(request: StudyRequest, task: str) -> dict[str, object]:
    try:
        context = productivity_service.context(request.document_ids)
        result = productivity_service.generate(task, context, request.detail)
        return {'model': llm_provider.model_name, 'status': 'generated', 'citations': context.citations, 'data': result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ProductivityGenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post('/api/study/summary')
def study_summary(request: StudyRequest) -> dict[str, object]:
    return _study(request, 'Create a summary. Return JSON with keys short_summary, detailed_summary, and section_summaries. section_summaries must be an array of objects with title, summary, and source_ids.')


@app.post('/api/study/key-points')
def study_key_points(request: StudyRequest) -> dict[str, object]:
    return _study(request, 'Extract important concepts, facts, definitions, and takeaways. Return JSON with key_points as an array of objects with type, text, and source_ids.')


@app.post('/api/study/quiz')
def study_quiz(request: StudyRequest) -> dict[str, object]:
    return _study(request, 'Create up to 5 multiple-choice questions. Return JSON with questions as an array of objects with question, options, correct_answer, explanation, and source_ids.')


@app.post('/api/study/flashcards')
def study_flashcards(request: StudyRequest) -> dict[str, object]:
    return _study(request, 'Create up to 8 flashcards. Return JSON with flashcards as an array of objects with question, answer, and source_ids.')
