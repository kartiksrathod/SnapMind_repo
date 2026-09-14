# ARCHITECTURE.md

# SnapMind

## System Architecture & Technical Design

**Project:** SnapMind
**Purpose:** Private On-Device AI Knowledge Assistant
**Target Platform:** Snapdragon-powered HP PCs
**Primary OS Target:** Windows
**Architecture Style:** Modular Local-First AI Architecture
**Primary AI Pattern:** Retrieval-Augmented Generation (RAG)
**Deployment Principle:** Local-first, hardware-accelerated where supported

---

# 1. Architecture Objective

The SnapMind architecture must support a privacy-first AI knowledge assistant that can process user content locally and use Snapdragon AI acceleration wherever technically supported.

The architecture must:

- Keep core knowledge processing local.
- Support offline operation.
- Separate UI, backend, AI, retrieval, and storage responsibilities.
- Allow AI models to be replaced without rewriting the application.
- Support Snapdragon CPU/GPU/NPU execution paths.
- Allow Qualcomm AI Hub models and supported runtimes to be integrated.
- Provide CPU/GPU fallback where appropriate.
- Make performance measurable.
- Remain simple enough to deploy reliably on a Windows AI PC.

---

# 2. High-Level Architecture

```text
                         SNAPMIND
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Frontend/UI                 Local Backend
              │                           │
              │                    ┌──────┴──────┐
              │                    │             │
              │               Document       AI Orchestrator
              │               Service             │
              │                    │         ┌────┼────┐
              │                    │         │    │    │
              │                    │        LLM  VLM  STT
              │                    │
              │               RAG Engine
              │                    │
              │              ┌─────┴─────┐
              │              │           │
              │          Embeddings   Retriever
              │              │           │
              │              └─────┬─────┘
              │                    │
              │              Local Vector DB
              │
              └─────────────── Local API
```

All major components communicate through defined interfaces rather than directly depending on implementation details.

---

# 3. Architectural Principles

## 3.1 Local First

The default execution path should remain on the user's device.

Cloud services must not be required for core functionality.

---

## 3.2 Privacy First

User documents, extracted text, embeddings, and knowledge indexes should remain local by default.

External network communication should only occur when explicitly required and clearly communicated.

---

## 3.3 Hardware-Aware AI

AI workloads should be mapped to the most appropriate available Snapdragon execution target.

Conceptually:

```text
AI Workload
     │
     ↓
Hardware Capability Detection
     │
     ├── NPU available → NPU execution
     │
     ├── GPU suitable → GPU execution
     │
     └── CPU fallback → CPU execution
```

The exact execution hierarchy will depend on model/runtime support.

### Phase 5 Verified Runtime Boundary

The current development machine is Windows 11 on an Intel Core i5-12450H with Intel UHD Graphics. No Qualcomm/NPU device, Qualcomm AI Hub resource, Qualcomm AI Runtime, ONNX Runtime, or ONNX GenAI package was available during Phase 5 inspection. Therefore the verified inference path is the local Ollama candidate through the CPU fallback only. The application reports `NPU execution not verified` and does not claim Snapdragon, Qualcomm, NPU, or GPU acceleration.

The Phase 5 runtime evidence endpoint reports: backend `CPU`, runtime `Ollama local runtime`, model `llama3.2:latest`, status `active`. A direct generation probe returned `local inference verified.` This verifies local CPU-backed generation only; it does not verify the underlying Ollama process's use of any GPU and does not establish Qualcomm compatibility.

### Phase 8 Multimodal Boundary

Phase 8 capability evaluation found no local OCR engine, verified vision model/runtime, or speech-to-text package/toolchain in the current environment. The backend exposes capability evidence and keeps OCR, image understanding, and voice disabled until an end-to-end local test is possible. These optional paths do not alter the document, RAG, or local LLM pipelines until independently verified.

---

## 3.4 Model Abstraction

Application code must not be tightly coupled to one AI model.

Instead:

```text
Application
     ↓
AI Interface
     ↓
Model Adapter
     ↓
Selected Runtime
     ↓
Model
```

This allows different models to be evaluated and replaced.

---

## 3.5 Evidence-Based Optimization

The system must not claim:

- NPU acceleration
- Snapdragon optimization
- faster inference
- lower resource consumption

without measurable evidence or reliable platform information.

---

# 4. Major Components

SnapMind will consist of the following logical components:

1. Frontend
2. Backend API
3. Document Processing Service
4. RAG Engine
5. Embedding Service
6. Vector Storage
7. AI Orchestrator
8. Local LLM Runtime
9. Vision/Multimodal Runtime
10. Speech Runtime
11. Hardware Capability Layer
12. Local Data Storage
13. Benchmarking System
14. Configuration System

Not every component needs to run as a separate process.

The architecture should remain modular logically while minimizing unnecessary deployment complexity.

---

# 5. Frontend Architecture

The frontend provides the user-facing application.

## Responsibilities

- Document upload
- Knowledge library
- Chat interface
- Source/citation display
- Summaries
- Quiz generation
- Flashcards
- Settings
- AI status
- Hardware status
- Benchmark visualization

The frontend should not directly execute AI models.

Instead:

```text
Frontend
    ↓
Backend API
    ↓
AI Services
```

---

# 6. Backend Architecture

The backend acts as the central application coordinator.

Responsibilities include:

- API routing
- File validation
- Document processing orchestration
- RAG orchestration
- AI request handling
- Session management
- Local storage management
- Model management
- Hardware capability reporting
- Error handling
- Benchmark execution

Conceptual API:

```text
/api
 ├── /documents
 ├── /knowledge
 ├── /chat
 ├── /summarize
 ├── /quiz
 ├── /flashcards
 ├── /models
 ├── /hardware
 └── /benchmark
```

Exact API contracts will be finalized during implementation.

---

# 7. Document Processing Pipeline

The document pipeline converts user files into searchable knowledge.

```text
User File
    ↓
File Validation
    ↓
Parser
    ↓
Content Extraction
    ↓
Cleaning
    ↓
Metadata Extraction
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Index
```

---

# 8. File Validation

Before processing:

- Verify file type.
- Verify file size.
- Reject unsupported formats.
- Prevent unsafe paths.
- Generate a local document identifier.

Example:

```text
Document ID
File Name
File Type
File Size
Import Time
Processing Status
```

---

# 9. Document Parsing

The parser extracts usable content from supported formats.

Initial target:

```text
PDF
TXT
Markdown
DOCX
```

The parser layer must be replaceable.

Example:

```text
DocumentParser
      │
      ├── PDFParser
      ├── TXTParser
      ├── MarkdownParser
      └── DOCXParser
```

---

# 10. Text Cleaning

Extracted content may contain:

- Excess whitespace
- Broken line breaks
- Repeated headers
- Page artifacts
- Encoding problems

The cleaning stage normalizes content before chunking.

The original source metadata must remain available.

---

# 11. Chunking Architecture

Documents are divided into smaller pieces for retrieval.

```text
Document
    ↓
Sections
    ↓
Chunks
    ↓
Metadata
```

Each chunk should retain:

- Document ID
- Chunk ID
- Page number where available
- Section information where available
- Text
- Position/order

Chunking parameters should be configurable.

The final values will be selected through testing.

---

# 12. Embedding Architecture

Each chunk is converted into an embedding vector.

```text
Chunk
  ↓
Embedding Model
  ↓
Vector
  ↓
Local Vector Database
```

The embedding model should preferably support local execution.

Model selection will depend on:

- Quality
- Latency
- Memory
- Snapdragon compatibility
- Runtime support
- License

---

# 13. Vector Storage

Vector representations will be stored locally.

Logical structure:

```text
Knowledge Base
    │
    ├── Documents
    │
    ├── Chunks
    │
    └── Embeddings
```

The vector database should support:

- Similarity search
- Metadata filtering
- Local persistence
- Fast retrieval

The specific vector database will be finalized after evaluating deployment simplicity and performance.

---

# 14. RAG Architecture

The core question-answering architecture is:

```text
User Question
      ↓
Query Processing
      ↓
Query Embedding
      ↓
Vector Search
      ↓
Top-K Relevant Chunks
      ↓
Context Filtering
      ↓
Prompt Construction
      ↓
Local LLM
      ↓
Grounded Response
      ↓
Citation Mapping
      ↓
Frontend
```

---

# 15. Retrieval Strategy

Initial retrieval will use semantic similarity.

Potential improvements:

- Metadata filtering
- Keyword + semantic hybrid retrieval
- Reranking
- Context deduplication
- Relevance thresholds

These improvements will be added only if testing demonstrates meaningful benefits.

---

# 16. Citation Architecture

Each retrieved chunk maintains its source metadata.

Example:

```text
Retrieved Chunk
      │
      ├── document_id
      ├── page_number
      ├── section
      └── chunk_id
```

The generated answer can then map claims/context back to the relevant source.

The application must never generate fake source references.

---

# 17. AI Orchestrator

The AI Orchestrator is responsible for selecting and coordinating AI workloads.

```text
                  AI ORCHESTRATOR
                         │
        ┌────────────────┼────────────────┐
        │                │                │
       LLM              VLM              STT
        │                │                │
     Text AI         Vision AI       Speech AI
```

The orchestrator should hide runtime-specific implementation details from the rest of the application.

---

# 18. Local LLM Architecture

The LLM is responsible for tasks such as:

- Question answering
- Summarization
- Key point extraction
- Quiz generation
- Flashcard generation

Logical interface:

```text
LLMService

generate()
stream()
summarize()
extract()
generate_quiz()
generate_flashcards()
```

The actual model will be selected after Snapdragon compatibility and performance testing.

---

# 19. Qualcomm AI Hub Integration

Qualcomm AI Hub will be evaluated as a primary source for Snapdragon-compatible and optimized AI models.

Potential workflow:

```text
Model Candidates
      ↓
Qualcomm AI Hub
      ↓
Compatibility Check
      ↓
Snapdragon Target
      ↓
Runtime Integration
      ↓
Benchmark
      ↓
Final Model Selection
```

The project will not assume that every AI Hub model automatically provides NPU execution.

Each chosen model/runtime combination must be verified.

---

# 20. Snapdragon Hardware Layer

The hardware layer provides information about available compute capabilities.

Conceptually:

```text
Hardware Detection
       │
       ├── Snapdragon Platform
       ├── NPU
       ├── GPU
       ├── CPU
       └── Memory
```

This information can be displayed in the application.

Example:

```text
AI Hardware

Platform: Snapdragon
AI Accelerator: Available
Execution: NPU
Model: [Selected Model]
```

The exact hardware-detection implementation will depend on supported Windows/Qualcomm APIs.

---

# 21. Execution Backend Abstraction

The application should use a common interface:

```text
InferenceBackend
       │
       ├── NPUBackend
       ├── GPUBackend
       └── CPUBackend
```

This prevents the application from being tightly coupled to a single accelerator.

---

# 22. Fallback Strategy

If the preferred execution backend is unavailable:

```text
Preferred Backend
       ↓
Supported Alternative
       ↓
CPU Fallback
```

Example:

```text
NPU
 ↓ unavailable
GPU
 ↓ unavailable
CPU
```

The actual order will be determined by model/runtime compatibility.

The system must not attempt to execute a model on hardware that the runtime does not support.

---

# 23. Multimodal Architecture

For image-supported workflows:

```text
Image
  ↓
Image Validation
  ↓
Vision Model
  ↓
Visual Representation
  ↓
AI Orchestrator
  ↓
Response
```

For image + document reasoning:

```text
Image
   │
   ├── Vision Processing
   │
   ↓
Visual Context
   │
   ├── Document Retrieval
   │
   ↓
Combined Context
   ↓
Multimodal Model
   ↓
Response
```

Multimodal functionality will be implemented after the core RAG system is stable.

---

# 24. Voice Architecture

Optional voice workflow:

```text
Microphone
    ↓
Speech-to-Text
    ↓
User Query
    ↓
RAG
    ↓
Local LLM
    ↓
Response
    ↓
Text-to-Speech
```

Voice is secondary to the core document/RAG workflow.

---

# 25. Local Storage Architecture

The system should separate:

```text
Application Data
       │
       ├── Documents
       ├── Extracted Content
       ├── Vector Index
       ├── Metadata
       ├── Conversations
       ├── Generated Content
       └── Benchmarks
```

Storage locations should be configurable.

Sensitive user data should not be stored unnecessarily.

---

# 26. Configuration Architecture

Configuration should be centralized.

Potential settings:

```text
Model
Embedding Model
Vector Database
Chunk Size
Chunk Overlap
Top-K
Temperature
Max Tokens
Execution Backend
Storage Path
Privacy Mode
```

Configuration must not require modifying source code for normal usage.

---

# 27. Privacy Architecture

Default data flow:

```text
User File
   ↓
Local Application
   ↓
Local Processing
   ↓
Local Vector Store
   ↓
Local AI Model
   ↓
Local Response
```

There should be no hidden:

```text
User File
   ↓
External Cloud API
```

Core functionality should remain local-first.

---

# 28. Network Dependency Model

The application should distinguish:

### Required for Installation

Possible internet requirements for:

- Installing dependencies
- Downloading models
- Initial setup

### Not Required During Core Usage

After setup:

- Document processing
- RAG
- Local inference
- Retrieval
- Summarization

should work offline where supported.

The exact offline boundary will be documented in the final implementation.

---

# 29. Benchmark Architecture

Benchmarking should be built into the project rather than performed manually only at the end.

```text
Benchmark Runner
       ↓
Workload
       ↓
Execution Backend
       ↓
Metrics Collection
       ↓
Results Store
       ↓
Visualization
```

Potential metrics:

- Latency
- Tokens/second
- Memory
- CPU utilization
- GPU utilization
- NPU utilization
- Model loading time
- Retrieval latency
- Embedding throughput

---

# 30. AI Workload Classification

Different workloads may use different execution paths.

```text
                 AI Workloads
                      │
       ┌──────────────┼──────────────┐
       │              │              │
   Embeddings        LLM            Vision
       │              │              │
   Backend A       Backend B      Backend C
```

There is no requirement that every workload use the same accelerator.

The architecture should choose the most appropriate supported execution path.

---

# 31. Request Lifecycle

For a standard user question:

```text
1. User enters question
          ↓
2. Frontend sends request
          ↓
3. Backend validates request
          ↓
4. Query embedding generated
          ↓
5. Vector database searched
          ↓
6. Relevant chunks selected
          ↓
7. Context constructed
          ↓
8. Local LLM invoked
          ↓
9. Response generated
          ↓
10. Citations mapped
          ↓
11. Response returned
          ↓
12. Frontend renders answer
```

---

# 32. Document Lifecycle

```text
Upload
  ↓
Validate
  ↓
Parse
  ↓
Clean
  ↓
Chunk
  ↓
Embed
  ↓
Index
  ↓
Ready
```

Status examples:

```text
UPLOADED
PROCESSING
INDEXING
READY
FAILED
```

---

# 33. Error Architecture

Errors should be categorized.

```text
Validation Error
Processing Error
Model Error
Retrieval Error
Hardware Error
Storage Error
Configuration Error
```

The backend should return structured errors.

Example:

```text
{
    "error": "MODEL_UNAVAILABLE",
    "message": "The selected local model is unavailable.",
    "recoverable": true
}
```

The frontend converts technical errors into user-friendly messages.

---

# 34. Security Boundaries

The architecture should enforce:

```text
Frontend
   ↓
API Boundary
   ↓
Backend
   ↓
Local Services
   ↓
Local Storage
```

The frontend should not have unrestricted access to arbitrary filesystem locations.

Uploaded files must pass validation before processing.

---

# 35. Deployment Architecture

Target deployment:

```text
Snapdragon HP PC
│
├── SnapMind Application
│
├── Local Backend
│
├── Local AI Runtime
│
├── AI Models
│
├── Vector Database
│
└── Local User Data
```

The application should ideally be deployable without requiring users to manually configure multiple complex services.

The final packaging approach will be decided after the prototype is stable.

---

# 36. Development Environment vs Target Environment

Development may occur on a non-Snapdragon machine.

```text
Development PC
      ↓
Application Development
      ↓
Model/Runtime Testing
      ↓
Qualcomm AI Hub / Compatible Environment
      ↓
Snapdragon Validation
      ↓
Final Target
```

However, final performance claims must be based on the appropriate target hardware.

---

# 37. Model Selection Process

Models will be selected through:

```text
Candidate Models
      ↓
License Check
      ↓
Task Quality Test
      ↓
Snapdragon Compatibility
      ↓
Runtime Compatibility
      ↓
Memory Test
      ↓
Latency Test
      ↓
NPU/GPU/CPU Test
      ↓
Final Selection
```

No model becomes a permanent dependency before this evaluation.

---

# 38. Architecture Evolution

The architecture is intentionally modular.

Possible future additions:

- Additional model providers
- More document formats
- Better retrieval
- Local OCR
- More vision models
- Voice interaction
- Multi-user local workspaces
- Advanced agent workflows

These should be added without breaking the core RAG architecture.

---

# 39. Initial Recommended Stack

The initial implementation can use:

### Frontend

React + TypeScript + Tailwind CSS

### Backend

Python + FastAPI

### AI/RAG

Python-based modular AI services

### Vector Storage

Local vector database selected during implementation

### Local Storage

Filesystem + local metadata database

### AI Models

Qualcomm AI Hub / compatible open-source models

### Target Runtime

Snapdragon-compatible Windows AI runtime selected after testing

These are initial recommendations, not permanent requirements.

---

# 40. Architecture Decision Rules

When choosing between two technical solutions, prioritize:

1. Snapdragon compatibility
2. Local execution
3. Privacy
4. Performance
5. Reliability
6. Simplicity
7. Maintainability
8. Deployment ease
9. Licensing
10. Feature richness

A technically impressive feature should not be selected if it makes the core demo unreliable.

---

# 41. Final Target Architecture

The intended final architecture is:

```text
┌───────────────────────────────────────────────────────┐
│                    SNAPMIND APP                       │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │                 React Frontend                 │  │
│  │                                                 │  │
│  │ Dashboard │ Library │ Chat │ Insights │ Stats │  │
│  └───────────────────────┬─────────────────────────┘  │
│                          │                            │
│                     Local API                        │
│                          │                            │
│  ┌───────────────────────▼─────────────────────────┐  │
│  │                 FastAPI Backend                 │  │
│  │                                                 │  │
│  │ Document │ RAG │ AI │ Model │ Hardware │ Data │  │
│  └──────┬─────────┬───────────┬────────────────────┘  │
│         │         │           │                       │
│         ↓         ↓           ↓                       │
│    Document     RAG       AI Orchestrator             │
│    Pipeline     Engine          │                     │
│         │         │       ┌────┼────┐                │
│         │         │       ↓    ↓    ↓                │
│         │         │      LLM  VLM  STT               │
│         │         │       │    │    │                │
│         └─────────┴───────┴────┴────┘                │
│                           │                           │
│                  Snapdragon Runtime                  │
│                           │                           │
│                    ┌──────┼──────┐                    │
│                    ↓      ↓      ↓                    │
│                   NPU    GPU    CPU                   │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │                 Local Storage                  │  │
│  │ Documents │ Metadata │ Vector DB │ Benchmarks │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

---

# 42. Architecture Success Criteria

The architecture is considered successful when:

- Frontend and backend are clearly separated.
- AI models can be replaced without major application changes.
- Documents can be processed locally.
- RAG operates locally.
- AI inference can use a Snapdragon-supported execution path.
- CPU fallback is available where appropriate.
- Hardware execution can be identified.
- Performance can be measured.
- User data remains local by default.
- Core functionality can operate offline after setup.
- The system can be packaged for a Windows Snapdragon AI PC.
- The architecture remains simple enough for reliable competition demonstration.

---

# 43. Relationship With Other Project Documents

`PRD.md`
→ Defines what the product must achieve.

`ARCHITECTURE.md`
→ Defines how the product is technically structured.

`RULES.md`
→ Defines development and implementation constraints.

`PHASES.md`
→ Defines the implementation sequence.

`DESIGN.md`
→ Defines UI/UX and visual product requirements.

`MEMORY.md`
→ Records changes, decisions, reasons, experiments, and project history.

`README.md`
→ Public-facing project documentation and setup instructions.

---

# 44. Current Architecture Status

**Status:** Initial Architecture Defined

**Model:** Not permanently selected

**Runtime:** Not permanently selected

**Vector Database:** Not permanently selected

**Snapdragon Hardware:** Target platform

**NPU Strategy:** To be validated

**GPU Strategy:** To be validated

**CPU Fallback:** Required where technically feasible

**Multimodal:** Planned

**Voice:** Optional

**Benchmarking:** Required

**Offline Core:** Required

**Privacy:** Required

All technology choices marked as "to be validated" must be tested before being treated as final project decisions.

```

**`ARCHITECTURE.md` complete.**

Ab next **`RULES.md`** hoga. Ye bahut important hai because yahin hum lock karenge ki development ke time **kya allowed hai, kya avoid karna hai, privacy rules, AI/model rules, Snapdragon claims, coding rules, testing rules, Git rules, and especially "shortcut leke competition demo fake nahi karna"** type constraints.
```
