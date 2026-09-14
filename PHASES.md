PHASES.md

# SnapMind

## Development Phases and Execution Roadmap

**Project:** SnapMind  
**Competition:** Snapdragon® AI Lab Build & Present Challenge  
**Target:** Snapdragon-powered HP PCs  
**Platform:** Windows  
**Development Approach:** Incremental, measurable, hardware-aware  
**Status:** Phase 10 complete; Phase 11 pending
**Last Updated:** September 2026

---

# 1. Purpose

This document defines the development roadmap for SnapMind.

The project will be developed in controlled phases so that:

- the core product works early
- architecture remains stable
- AI features are added incrementally
- Snapdragon optimization is evidence-based
- performance can be measured
- UI is polished after functionality is stable
- final competition submission is reliable

The project must not attempt to build every feature simultaneously.

---

# 2. Overall Development Strategy

The development sequence is:

```text
Phase 0
Project Foundation
        ↓
Phase 1
Application Skeleton
        ↓
Phase 2
Document Management
        ↓
Phase 3
RAG Knowledge Engine
        ↓
Phase 4
Local AI Inference
        ↓
Phase 5
Snapdragon / Qualcomm AI Hub Integration
        ↓
Phase 6
Performance & Benchmarking
        ↓
Phase 7
AI Productivity Features
        ↓
Phase 8
Multimodal Features
        ↓
Phase 9
UI/UX Polish
        ↓
Phase 10
Testing & Reliability
        ↓
Phase 11
Competition Demo
        ↓
Phase 12
Final Submission

Not every optional feature must reach the final build.

3. Priority System

Each feature will have a priority.

P0 - Critical

Must work for the competition.

Examples:

local document ingestion
RAG
local AI inference
citations
Snapdragon-compatible AI path
benchmarking
polished core workflow
P1 - Important

Should be implemented if time allows.

Examples:

summarization
quiz generation
flashcards
hardware dashboard
multiple model support
P2 - Optional

Only implement after P0/P1 stability.

Examples:

OCR
image understanding
voice
advanced personalization
4. Phase 0 - Project Foundation
Objective

Create the project foundation before writing major application code.

Tasks
Repository

Create Git repository.

Suggested repository:

snapmind
Initial files
PRD.md
ARCHITECTURE.md
RULES.md
PHASES.md
DESIGN.md
MEMORY.md
README.md
.gitignore
.env.example
Folder structure

Initial structure:

snapmind/
│
├── frontend/
│
├── backend/
│
├── ai/
│
├── models/
│
├── data/
│
├── benchmarks/
│
├── docs/
│
├── scripts/
│
├── tests/
│
├── PRD.md
├── ARCHITECTURE.md
├── RULES.md
├── PHASES.md
├── DESIGN.md
├── MEMORY.md
├── README.md
├── .gitignore
└── .env.example
Environment

Verify:

Python
Node.js
npm
Git
required compiler/runtime dependencies
Completion Criteria
repository created
project structure created
application can be started
documentation files committed
.gitignore configured
first Git commit completed
5. Phase 1 - Application Skeleton
Objective

Build the basic application shell.

Frontend

Use:

React
TypeScript
Tailwind CSS

Create:

Dashboard
Documents
Knowledge
Chat
Settings
Benchmark
Backend

Use:

Python
FastAPI

Create basic endpoints:

GET /api/health
GET /api/models
GET /api/hardware
GET /api/config
Frontend ↔ Backend

Verify:

React
   ↓
FastAPI
   ↓
Response
   ↓
React
Completion Criteria

The application should:

launch successfully
show dashboard
communicate with backend
display backend status
handle basic errors

No AI is required yet.

### Phase 1 Completion Record

Completed:

- React, TypeScript, Vite, and Tailwind CSS frontend shell
- FastAPI backend with health, model, hardware, and config endpoints
- Responsive sidebar, topbar, page container, and dashboard
- Routes for Dashboard, Documents, Knowledge, Chat, Study, Hardware, Benchmark, and Settings
- Frontend API client with loading, connection, and error states
- Honest unavailable/setup states for unimplemented AI and hardware capabilities
- Frontend production build and backend API tests

Phase 2 is now the next active implementation phase. No document processing, RAG, inference, benchmarking, or Snapdragon acceleration was implemented in Phase 1.

6. Phase 2 - Document Management
Objective

Allow users to build a local knowledge library.

Supported Formats

Initial formats:

PDF
TXT
Markdown
DOCX

Additional formats may be added later.

Workflow
Select File
    ↓
Validate
    ↓
Copy to Local Storage
    ↓
Parse
    ↓
Extract Text
    ↓
Create Metadata
    ↓
Store
Document Metadata

Store:

document_id
filename
file_type
file_size
created_at
page_count
processing_status
UI

Document screen should support:

upload
document list
processing status
delete
view metadata
search/filter
Edge Cases

Test:

empty document
corrupted PDF
unsupported file
duplicate file
large file
scanned PDF
missing text
Completion Criteria

A user can:

Upload PDF
    ↓
See document
    ↓
Process document
    ↓
View extracted text/metadata

### Phase 2 Completion Record

Completed:

- Local upload and storage for PDF, TXT, Markdown, and DOCX
- File validation for supported format, empty files, duplicates, unsafe filenames, and 50 MB size limit
- Separate parser interfaces for text, PDF, and DOCX extraction
- Persistent document metadata and processing status
- Document listing, search, status filtering, retry, deletion, and clear error states
- Responsive document management UI with drag-and-drop import
- Tests for valid text/PDF/DOCX, corrupted files, empty files, unsupported files, duplicates, and deletion

Phase 3 is now the next active implementation phase. Embeddings, vector search, RAG, and LLM inference were intentionally excluded from Phase 2.
7. Phase 3 - RAG Knowledge Engine
Objective

Convert documents into a searchable local knowledge base.

Pipeline
Document
    ↓
Text Extraction
    ↓
Cleaning
    ↓
Chunking
    ↓
Metadata
    ↓
Embeddings
    ↓
Vector Storage
Chunk Metadata

Every chunk should preserve:

document_id
chunk_id
page
section
text
position
Retrieval

Query flow:

User Question
      ↓
Query Embedding
      ↓
Vector Search
      ↓
Top-K Results
      ↓
Relevant Context
Testing

Create a fixed evaluation set.

Example:

Question 1
Question 2
Question 3
...
Question N

Each question should have an expected source/document.

Completion Criteria

The system can:

index documents
generate embeddings
search relevant chunks
return source metadata
handle multiple documents

At this stage, the system does not need a sophisticated LLM.

### Phase 3 Completion Record

Completed:

- Local text cleaning and configurable overlap-based chunking
- Replaceable embedding service interface with deterministic offline baseline
- Persistent SQLite vector store selected for local Windows simplicity
- Document indexing on import and retry, with index cleanup on deletion
- Query embedding, cosine-style similarity ranking, top-K retrieval, and relevance thresholding
- Chunk metadata preservation for document, chunk, page, section, text, and position
- Knowledge screen with search, indexed chunk status, source details, and relevance information
- Retrieval tests for relevant, irrelevant, multi-document, missing-index, filtered, deleted, and re-indexed content
- Basic local retrieval benchmark documented in `MEMORY.md`

Phase 4 is now the next active implementation phase. LLM answer generation was intentionally excluded from Phase 3.

8. Phase 4 - Local AI Inference
Objective

Connect the RAG engine to a local language model.

Architecture
Question
   ↓
Retriever
   ↓
Relevant Context
   ↓
AI Orchestrator
   ↓
Local LLM
   ↓
Grounded Answer
   ↓
Citation Mapping
Model Selection

Do not permanently select a model before testing.

Evaluate candidates based on:

Snapdragon compatibility
Windows compatibility
model size
quantization
latency
memory
response quality
licensing
Required Interface

The AI layer should expose a model-independent interface.

Conceptually:

generate()
stream()
summarize()
extract()
generate_quiz()
generate_flashcards()
Grounding

The prompt must prioritize retrieved document context for document-based questions.

Citation

Answer should map back to:

Document
Page
Section
Chunk
Completion Criteria

The user can:

Upload document
     ↓
Ask question
     ↓
Retrieve context
     ↓
Run local LLM
     ↓
Receive grounded answer
     ↓
See citation

This is the first major MVP milestone.

### Phase 4 Completion Record

Completed:

- Model-independent local LLM provider interface
- Ollama development candidate with model availability and generation errors
- AI orchestrator connecting retrieval, context building, local generation, and citations
- Grounding instructions that restrict answers to retrieved source context
- Uncertainty response when retrieval provides insufficient evidence
- Current local session chat history
- Chat API with validation, model-unavailable, and generation failure handling
- Complete Chat UI with empty state, input, staged loading, assistant messages, citations, source cards, and retry
- Tests for factual grounded questions, unsupported questions, multiple document retrieval, no-document behavior, empty queries, and unavailable models
- Live local Ollama verification with cleanup

Phase 5 is now the next active implementation phase. Snapdragon/Qualcomm runtime selection and acceleration verification were intentionally excluded from Phase 4.

### Phase 5 Completion Record

Completed:

- Local hardware capability abstraction with OS-backed CPU/GPU evidence
- Explicit unknown NPU state and `NPU execution not verified` limitation
- Model candidate catalog with format, size, quantization, runtime, workload, licensing, compatibility, and evidence fields
- Replaceable inference backend interface with safe CPU fallback selection
- Runtime evidence endpoint and Hardware UI showing device, processor, accelerators, model, runtime, backend, status, and limitations
- Environment evaluation: Intel Windows development machine; no Qualcomm AI Hub or Qualcomm runtime available
- Actual local Ollama inference path tested successfully through the CPU fallback

Phase 6 is now the next active implementation phase. No Snapdragon or Qualcomm acceleration claim is made because NPU execution and AI Hub deployment were not verifiable in this environment.

### Phase 7 Completion Record

Completed:

- Shared local AI productivity service for summaries, key points, quizzes, and flashcards
- Short and detailed summary generation with optional section summaries
- Source-aware concepts, facts, definitions, and takeaways
- Structured multiple-choice quiz generation with answers, explanations, and sources
- Source-aware flashcard generation
- Multi-document chat filtering with document identity preserved through retrieval and citations
- Empty knowledge, missing context, model failure, invalid structured output, and generation error handling
- Complete Study UI with four workflows, loading states, errors, retry, and traceable source references
- 17 backend tests covering all productivity workflows and core regression behavior
- Real local summary generation verified with `llama3.2:latest`; invalid model source IDs are rejected to prevent fake citations

Phase 8 is now pending. Phase 7 did not add cloud AI, duplicate model implementations, or untraceable study content.

### Phase 8 Completion Record

Evaluated but not enabled:

- OCR: unavailable because no local OCR package and Tesseract executable were detected
- Image understanding: unavailable because no verified local vision model/runtime was detected
- Speech-to-text: unavailable because no local STT package and ffmpeg toolchain were detected

Implemented:

- Honest `/api/multimodal/capabilities` capability report
- Hardware UI panel showing optional multimodal readiness, evidence, and limitations
- Automated capability-state test and live endpoint smoke test

No multimodal feature appears enabled in the application. Document processing, RAG, local LLM inference, and verified hardware reporting were left unchanged.

### Phase 9 Completion Record

Completed:

- Live dashboard snapshot with real document/index counts, AI status, hardware evidence, and recent documents
- Coherent spacing, typography, hierarchy, card, navigation, empty, loading, and error treatments across the application
- Accessible keyboard focus states and clearer disabled/error presentation
- Restrained transitions with reduced-motion support
- Responsive dashboard, document, knowledge, chat, study, and hardware layouts
- Honest, screen-specific not-configured states for Benchmark and Settings
- Browser route sweep for Dashboard, Documents, Knowledge, Chat, Study, Hardware, Benchmark, and Settings
- 19 backend tests and frontend production build passing

Phase 10 is now pending. Core architecture and benchmark values were not changed during UI polish.

9. MVP CHECKPOINT

At this point SnapMind should already be a usable product.

MVP Must Include
local document upload
document processing
local indexing
RAG retrieval
local LLM
grounded answers
citations
basic UI
local storage
MVP Demo
Open SnapMind
      ↓
Upload PDF
      ↓
Processing
      ↓
Ask question
      ↓
AI answer
      ↓
Citation

If later phases fail, this MVP must remain functional.

10. Phase 5 - Snapdragon / Qualcomm AI Hub Integration
Objective

Transform the generic local AI application into a Snapdragon-focused AI-PC application.

This is one of the most important competition phases.

Step 1 - Identify Target Hardware

Determine the target Snapdragon configuration.

Record:

Device
Processor
Snapdragon platform
RAM
NPU capability
GPU capability
Windows version
Step 2 - Explore Qualcomm AI Hub

Evaluate available models and deployment options.

Candidate workloads:

LLM
Embedding
Vision
OCR
Speech

Not every workload must use the same runtime.

Step 3 - Model Compatibility

For each candidate model record:

Model
Version
Model size
Runtime
Supported hardware
Quantization
Expected workload
Step 4 - Runtime Testing

Test appropriate runtime paths.

Potential runtime categories include:

Qualcomm AI Runtime
ONNX Runtime
TFLite
GenieX
Other Qualcomm-supported runtime

The final runtime must be selected through testing.

Step 5 - Hardware Backend

Implement hardware abstraction:

InferenceBackend
       |
       +---- NPU
       |
       +---- GPU
       |
       +---- CPU

The application should know which backend is being used.

Step 6 - Capability Detection

Conceptually:

Application
     ↓
Hardware Detection
     ↓
Available Accelerators
     ↓
Runtime Compatibility
     ↓
Backend Selection
Step 7 - Verify NPU Execution

If a workload is claimed to use the NPU, verify it through appropriate tools or runtime evidence.

Do not infer NPU usage merely because the device contains an NPU.

Completion Criteria

At least one meaningful AI workload should have a verified Snapdragon-compatible acceleration path.

The project documentation must record:

model
runtime
hardware
backend
benchmark result
limitations
11. Phase 6 - Performance & Benchmarking
Objective

Measure whether Snapdragon optimization actually improves the application.

Benchmark Categories
Model Loading

Measure:

Cold load
Warm load
Inference

Measure:

Time to first token
Total response time
Tokens per second
RAG

Measure:

Embedding time
Retrieval time
Context construction time
Document Processing

Measure:

Text extraction
Chunking
Embedding
Indexing
System

Measure where practical:

RAM
CPU utilization
GPU utilization
NPU utilization
12. Benchmark Design

Use repeatable workloads.

Example:

Benchmark Document:
50-page PDF

Question Set:
20 fixed questions

Runs:
5 runs per configuration

Potential comparison:

CPU
vs
GPU
vs
NPU

Only include configurations that are actually supported.

Results

Store benchmark results locally.

Example:

benchmarks/
│
├── results/
├── datasets/
├── scripts/
└── reports/
Output

The application may display:

Backend: NPU
Average Latency: XXX ms
Memory: XXX MB

The exact values must come from actual measurements.

13. Phase 7 - AI Productivity Features
Objective

Turn the knowledge engine into a broader productivity assistant.

Feature 1 - Summarization

Flow:

Document
   ↓
Relevant content / full document
   ↓
Local LLM
   ↓
Summary

Support:

short summary
detailed summary
section summary
Feature 2 - Key Points

Generate:

Key Concepts
Important Facts
Definitions
Takeaways
Feature 3 - Quiz

Generate:

Question
Options
Correct Answer
Explanation
Source
Feature 4 - Flashcards

Generate:

Question
Answer
Source
Feature 5 - Multi-Document Q&A

Allow questions such as:

Compare the concepts discussed in these documents.

The retrieval layer must preserve document identity.

14. Phase 8 - Multimodal Features
Objective

Extend SnapMind beyond text when sufficient time and hardware support exist.

Image Understanding

Potential flow:

Image
  ↓
Vision Model
  ↓
Extract Information
  ↓
AI Reasoning

Possible use cases:

diagrams
charts
screenshots
lecture slides
technical figures
OCR

Potential flow:

Image
  ↓
OCR
  ↓
Text
  ↓
Knowledge Pipeline

OCR should remain local where possible.

Voice

Optional architecture:

Microphone
   ↓
Local Speech-to-Text
   ↓
Question
   ↓
RAG
   ↓
Local LLM
   ↓
Answer

Voice must not delay the completion of the core competition workflow.

15. Phase 9 - UI/UX Polish
Objective

Make SnapMind competition-ready.

Dashboard

Show:

documents
recent activity
AI status
hardware status
model
backend
performance snapshot
Knowledge Library

Improve:

search
filtering
sorting
document cards
processing indicators
Chat

Improve:

message layout
streaming
citations
source previews
loading state
error state
Hardware Panel

Potential information:

AI Backend
Model
Runtime
Accelerator
Memory
Latency
Benchmark Panel

Show:

Workload
Backend
Latency
Memory
Throughput

The UI must present technical information without overwhelming normal users.

16. Phase 10 - Testing & Reliability
Objective

Stabilize the complete application.

Functional Testing

Test:

Upload
Parse
Index
Search
Chat
Citation
Summary
Quiz
Flashcards
Delete
Settings
Benchmark
Failure Testing

Test:

Model unavailable
Runtime unavailable
Invalid document
Corrupted index
Insufficient memory
No accelerator
Network disabled
Backend crash
Large document
Empty query
Offline Test

Disable internet and verify the core workflow.

Expected:

Open app
   ↓
Load local knowledge
   ↓
Ask question
   ↓
Local retrieval
   ↓
Local inference
   ↓
Answer
Performance Regression Test

After major optimization, rerun benchmark suite.

Do not assume optimization improved performance.

17. Phase 11 - Competition Demo Preparation
Objective

Create a short, technically strong demonstration.

Recommended Demo Story
Part 1 - Problem

Explain:

Modern AI assistants often send information to cloud servers. This creates privacy, latency, and connectivity concerns.

Part 2 - Solution

Introduce:

SnapMind is a private, local-first AI knowledge assistant designed for Snapdragon-powered AI PCs.

Part 3 - Live Workflow
Import PDF
      ↓
Local Processing
      ↓
Ask Question
      ↓
RAG Retrieval
      ↓
Local AI
      ↓
Grounded Answer
      ↓
Citation
Part 4 - Snapdragon

Show:

Model
Runtime
Hardware
Accelerator

Explain the actual verified acceleration path.

Part 5 - Benchmark

Show actual measurements.

Example structure:

                 CPU     GPU     NPU
Latency           X       Y       Z
Memory            X       Y       Z
Throughput        X       Y       Z

Only show measured values.

Part 6 - Productivity

Demonstrate one or two:

Summary
Quiz
Flashcards

Do not demonstrate ten features badly.

18. Phase 12 - Final Submission
Objective

Prepare the final competition package.

Final Checklist
Product
 Application starts reliably
 Core workflow works
 Documents process correctly
 RAG works
 Citations work
 Local AI works
 Snapdragon path verified
 Benchmark works
UI
 No broken screens
 No obvious visual bugs
 Loading states work
 Errors are understandable
 Demo path is simple
Technical
 No secrets committed
 Dependencies documented
 Model information documented
 Runtime documented
 Hardware information documented
 Benchmark results verified
Documentation
 PRD updated
 ARCHITECTURE updated
 RULES updated if needed
 PHASES updated
 DESIGN updated
 MEMORY updated
 README completed
Presentation
 Problem explained
 Solution explained
 Architecture explained
 Snapdragon relevance explained
 Live demo prepared
 Benchmark evidence prepared
 Limitations acknowledged
19. Time Management Strategy

The competition submission deadline is:

30 September 2026
11:59 PM IST

Development should therefore follow a risk-first strategy.

Risk Priority

Highest risk:

Snapdragon compatibility
        ↓
Local model inference
        ↓
Performance
        ↓
RAG reliability
        ↓
UI polish
        ↓
Optional features

Do not spend most of the project time polishing UI before proving the AI workload can run correctly on the target environment.

20. Recommended Milestones
Milestone 1
Project boots
Milestone 2
Documents work
Milestone 3
RAG works
Milestone 4
Local LLM works
Milestone 5
Snapdragon-compatible inference works
Milestone 6
Benchmarks available
Milestone 7
Product features complete
Milestone 8
UI polished
Milestone 9
Final demo stable
Milestone 10
Submission ready
21. Development Stop Rules

Stop adding new features when any of the following occurs:

core demo becomes unstable
benchmark results are not reproducible
model/runtime compatibility becomes uncertain
major bugs remain unresolved
deployment becomes unreliable
documentation falls behind
submission deadline becomes the primary risk

At that point:

New Features
     ↓
STOP

Testing
Documentation
Optimization
Demo
     ↓
CONTINUE
22. Final Product Definition

The final SnapMind product should ideally provide:

                    SNAPMIND
                       |
        +--------------+--------------+
        |              |              |
    Knowledge       Local AI       Hardware
        |              |              |
   Documents         RAG           Snapdragon
   Retrieval         LLM             NPU
   Citations       Summary           GPU
                                  Benchmark
        |
   Productivity
        |
   Quiz
   Flashcards
   Key Points

The exact final feature set depends on time, hardware compatibility, and measured reliability.

23. Definition of Done

SnapMind is considered competition-ready when:

Product
 Core workflow works end-to-end
 Local document knowledge base works
 RAG answers are grounded
 Citations are accurate
 Local inference works
Snapdragon
 Target hardware identified
 Compatible model selected
 Runtime selected
 Acceleration path verified
 Performance measured
Engineering
 Code is modular
 Errors handled
 Security checks implemented
 No secrets committed
 Git history is reasonable
UX
 Main workflow is intuitive
 UI is polished
 Loading/error states exist
 Hardware information is understandable
Competition
 Demo is reproducible
 Claims are evidence-based
 Benchmarks are real
 Documentation is complete
 Final submission materials are ready
24. Current Status
Phase 0   Project Foundation       PLANNED
Phase 1   Application Skeleton     PLANNED
Phase 2   Document Management      PLANNED
Phase 3   RAG Engine               PLANNED
Phase 4   Local AI                 PLANNED
Phase 5   Snapdragon Integration   PLANNED
Phase 6   Benchmarking             PLANNED
Phase 7   Productivity Features   PLANNED
Phase 8   Multimodal               OPTIONAL
Phase 9   UI/UX Polish             PLANNED
Phase 10  Testing                  COMPLETE
Phase 11  Competition Demo         PLANNED
Phase 12  Final Submission         PLANNED

Status must be updated as development progresses.

25. Change Management

Whenever a phase changes significantly, update:

PHASES.md
MEMORY.md

If the change affects requirements:

PRD.md

If the change affects architecture:

ARCHITECTURE.md

If the change affects visual/UI decisions:

DESIGN.md

If the change introduces or modifies a project rule:

RULES.md
26. Golden Execution Principle

The project should always follow:

Build
  ↓
Test
  ↓
Measure
  ↓
Document
  ↓
Improve

Not:

Build everything
  ↓
Hope it works
  ↓
Demo
END OF PHASES.md
```



