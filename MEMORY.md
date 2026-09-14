# SnapMind Memory

## Phase 1 Implementation

- Frontend: React + TypeScript + Vite + Tailwind CSS configuration in `frontend/`.
- Frontend entry point: `frontend/src/main.tsx`; shared visual system: `frontend/src/styles.css`.
- Routes implemented: Dashboard, Documents, Knowledge, Chat, Study, Hardware, Benchmark, Settings.
- Backend: FastAPI app at `backend/app/main.py`; run with `python -m app` from `backend/`.
- API endpoints: `/api/health`, `/api/models`, `/api/hardware`, `/api/config`.
- Vite proxies `/api` requests to `http://127.0.0.1:8000` during development.
- Models and hardware report honest unavailable/unknown states until their later phases are implemented.
- Frontend build command: `npm run build` from `frontend/`.
- Backend validation: `python -m pytest` from `backend/`.
- Phase 1 validation completed: frontend production build passes; backend API tests pass.

## Phase 2 Implementation

- Documents API lives in `backend/app/documents/` with separate models, storage, parsers, and service layers.
- Local files and metadata are stored under `backend/data/documents/`; extracted text is saved locally beside each source.
- Supported extensions: PDF, TXT, MD/Markdown, and DOCX. Maximum upload size is 50 MB.
- Document API: `GET /api/documents`, `POST /api/documents`, `POST /api/documents/{id}/retry`, `DELETE /api/documents/{id}`.
- Frontend Documents route now supports file selection, drag-and-drop, search, status filtering, metadata cards, retry, deletion, and error states.
- Phase 2 deliberately excludes embeddings, vector search, RAG, and LLM inference.
- Phase 2 validation completed: 6 backend tests pass, frontend production build passes, and live `/documents` UI smoke test passes.

## Phase 3 Implementation

- Local vector storage choice: SQLite with JSON-serialized normalized vectors. It is built into Python, persistent, Windows-compatible, low-complexity, and maintainable without a separate database process.
- Embedding abstraction lives in `backend/app/knowledge/embeddings.py`; Phase 3 uses a deterministic offline hashing embedder as a replaceable baseline, with stable SHA-256 buckets across restarts.
- Cleaning and configurable chunking live in `backend/app/knowledge/chunking.py`; the default is 700-character chunks with 100-character overlap.
- Chunk records preserve document ID, chunk ID, page, section, text, and position, plus source filename/type and relevance score.
- Knowledge API: `POST /api/knowledge/search` and `GET /api/knowledge/status/{document_id}`.
- Successful document processing indexes chunks; retry replaces the document index; deletion removes its chunks.
- Phase 3 validation completed: 9 backend tests pass, frontend production build passes, and a 73-chunk local retrieval benchmark returned 5 results in 19.444 ms.
- Phase 3 deliberately excludes LLM answer generation.

## Phase 4 Implementation

- AI abstraction lives in `backend/app/ai/providers.py`; `LLMProvider` supports replaceable model adapters and a `stream()` extension point.
- The development candidate is `OllamaProvider` using the local Ollama service at `127.0.0.1:11434`; the installed candidate is `llama3.2:latest`.
- `ChatOrchestrator` performs retrieval, context building, grounded local generation, citation mapping, and current-session history.
- Chat endpoint: `POST /api/chat`; empty queries return 400, unavailable local models return 503, and local retrieval/generation failures return 502.
- No retrieved chunks bypass model generation and return an uncertainty response without fabricated citations.
- Citations are copied only from retrieved chunk metadata and preserve document, page, section, and chunk IDs.
- Phase 4 validation completed: 12 backend tests pass, frontend production build passes, and a live local Ollama smoke test completed upload -> retrieval -> generation -> citation -> cleanup.
- Phase 4 deliberately excludes streaming transport implementation and Snapdragon runtime selection; the provider interface leaves streaming extensible for later runtime work.

## Phase 7 Implementation

- Shared productivity generation lives in `backend/app/ai/productivity.py`; it reuses the existing `KnowledgeService`, `InferenceBackend`, and `LLMProvider` rather than duplicating AI implementations.
- Study endpoints: `POST /api/study/summary`, `/api/study/key-points`, `/api/study/quiz`, and `/api/study/flashcards`.
- Study generation uses full indexed source context, optional document filters, structured JSON output, and source-ID validation against actual citations.
- Multi-document Chat now accepts `document_ids` and preserves document identity through retrieval and citations.
- Study UI is implemented in the `/study` route with Summary, Key points, Quiz, and Flashcards tabs, loading/error/empty states, and traceable source references.
- Phase 7 validation completed: 17 backend tests pass, frontend production build passes, and the live Study UI renders correctly.
- Real local-model summary smoke test generated structured output with one citation using `llama3.2:latest`; invalid source IDs from the model are rejected safely rather than turned into fake citations.

## Phase 5 Implementation

- Actual development environment: Windows 11 Home Single Language build 26200 on a 12th Gen Intel Core i5-12450H, Intel UHD Graphics, 8 cores/12 logical processors.
- No Qualcomm/NPU device was detected through Windows device inspection. Qualcomm AI Hub SDK/resources, Qualcomm AI Runtime, ONNX Runtime, and ONNX GenAI are not installed in this environment.
- Hardware capability layer lives in `backend/app/hardware/capabilities.py`; it reports CPU/GPU evidence from local OS queries and explicitly reports `NPU execution not verified`.
- Inference backend abstraction lives in `backend/app/ai/backends.py`; only the CPU backend is selected because it is the only verified feasible path here. NPU/GPU backends are not claimed active.
- Model catalog lives in `backend/app/ai/catalog.py`; `llama3.2:latest` remains a development candidate via local Ollama, not a Qualcomm AI Hub optimized model.
- Runtime endpoint: `GET /api/runtime`; hardware endpoint now returns device, CPU, GPU, and NPU evidence.
- Verified Phase 5 path: local Ollama generation through the CPU fallback. Snapdragon/Qualcomm accelerated execution remains unverified and is documented as a tested limitation.

Phase 5 evidence capture:

- OS: Windows 11; processor: Intel64 Family 6 Model 154 Stepping 3; 12 logical processors.
- GPU: Intel(R) UHD Graphics, reported by Windows CIM.
- NPU: unknown; exact reported evidence: `NPU execution not verified`.
- Runtime API: backend `CPU`, runtime `Ollama local runtime`, model `llama3.2:latest`, status `active`.
- Direct inference check returned `local inference verified.` through `CPUBackend` and `OllamaProvider`.
- Qualcomm AI Hub / Qualcomm AI Runtime / ONNX Runtime availability: not installed or verified in this environment.

## Phase 8 Evaluation

- No multimodal feature was enabled because this environment lacks a local OCR engine/executable, speech-to-text package/toolchain, and verified vision model/runtime.
- Capability endpoint: `GET /api/multimodal/capabilities` reports OCR, image understanding, and speech-to-text with runtime, evidence, status, and limitations.
- Live report: OCR unavailable, image understanding unavailable, and speech-to-text unavailable. The installed Ollama candidate is text-only for this project.
- Document processing, RAG, local LLM inference, and Snapdragon inference paths were not changed.
- Phase 8 validation completed: 18 backend tests pass, frontend production build passes, diagnostics are clean, and the capability endpoint was smoke-tested live.

## Phase 9 UI/UX Polish

- Added `/api/dashboard` snapshot for real document count, indexed chunk count, AI readiness, hardware evidence, and recent documents.
- Dashboard now renders live loading/error states and navigable recent-document cards; Import Document routes to the Documents workflow.
- Added shared visible keyboard focus states, restrained hover transitions, disabled control states, and `prefers-reduced-motion` support.
- Improved responsive layout for dashboard recents and preserved polished responsive states across Documents, Knowledge, Chat, Study, and Hardware.
- Replaced stale phase-number placeholders on Benchmark and Settings with clear not-configured states.
- Phase 9 validation completed: 19 backend tests pass, frontend production build passes, all eight routes were browser-smoke-tested, and no route rendered an error alert.

## Phase 10 Implementation

- Comprehensive test suite created at `backend/tests/test_phase10.py` with 78 tests across 8 test classes.
- Test classes: TestCompleteSystemWorkflow (8), TestEdgeCases (24), TestOfflineWorkflow (8), TestSecurity (8), TestPerformanceBenchmark (4), TestRegression (13), TestHardwareAndBackend (6), TestErrorHandling (6).
- Edge cases covered: empty file, corrupted PDF/DOCX, unsupported format (.png, .exe), duplicate document, very large document (1MB), oversized file (51MB), scanned PDF, missing model (503), model loading failure (502), runtime failure (502), unavailable NPU, CPU fallback, empty query, irrelevant query, insufficient retrieval context, deleted document, interrupted processing retry, no filename, path traversal, whitespace-only file, unicode content, binary .txt file.
- Security tests: .env not present, no secrets exposed in API responses, safe file paths, file validation enforced (8 dangerous extensions rejected), no arbitrary code execution, safe local storage, SQL injection prevented, XSS in filenames handled.
- Offline workflow verified: local documents accessible, local retrieval works, local AI works, citations work, health/models/hardware/dashboard endpoints all functional offline.
- Performance benchmarks: retrieval (20 searches, avg <1000ms, max <2000ms), indexing (<5000ms), chat (<1000ms), study generation (4 endpoints, each <1000ms).
- Regression tests verify all previous phases: Phase 1 (health/config), Phase 2 (document upload/list), Phase 3 (retrieval/indexing), Phase 4 (chat/citations), Phase 5 (hardware/backend), Phase 7 (study features), Phase 8 (multimodal capabilities), Phase 9 (dashboard).
- Hardware/backend tests: CPU backend selected, CPU backend report valid, unsupported accelerator raises, hardware detection valid, runtime endpoint returns CPU, models endpoint returns candidates.
- Error handling tests: 404/400/503/502 clear messages, empty search query error, no documents clear message.
- Phase 10 validation completed: 97 total backend tests pass (78 from Phase 10 + 19 from previous phases), frontend production build passes, full test suite runs in 23.48s.
- Snapdragon claims verified: NPU evidence remains "NPU execution not verified", CPU fallback is active, no false acceleration claims.
- No critical bugs found, core workflow intact, offline workflow functional, errors are understandable, benchmark remains functional.
