# RULES.md

# SnapMind

## Development, AI, Privacy, Competition & Engineering Rules

**Project:** SnapMind  
**Purpose:** Private On-Device AI Knowledge Assistant for Snapdragon-powered HP PCs  
**Target Platform:** Windows on Snapdragon  
**Document Type:** Project Rules / Engineering Rules  
**Status:** Active  
**Last Updated:** September 2026

---

# 1. Purpose of This Document

This document defines the rules that must be followed while designing, developing, testing, optimizing, documenting, and presenting SnapMind.

The purpose is to keep the project:

- technically credible
- privacy-first
- locally executable
- Snapdragon-focused
- maintainable
- measurable
- competition-ready
- honest about performance and capabilities

These rules apply throughout the complete development lifecycle.

---

# 2. Core Project Principles

SnapMind must follow these principles in priority order.

1. Local-first
2. Privacy-first
3. Evidence-based engineering
4. Snapdragon-aware optimization
5. Reliable AI responses
6. Clear source attribution
7. Measurable performance
8. Simple and maintainable architecture
9. Good user experience
10. Competition-ready presentation

If two decisions conflict, the higher-priority principle should generally win unless a documented engineering reason justifies an exception.

---

# 3. Local-First Rule

## 3.1 Default Behavior

SnapMind should process user data locally whenever technically possible.

The following should preferably execute locally:

- document parsing
- text extraction
- chunking
- embeddings
- vector search
- RAG retrieval
- LLM inference
- summarization
- quiz generation
- flashcard generation
- image processing
- OCR
- speech processing

## 3.2 No Mandatory Cloud Dependency

The core application must not require a cloud API to perform its primary knowledge-assistant workflow.

The application should remain usable without an internet connection after required models and dependencies have been installed.

## 3.3 Optional Online Features

If an online feature is introduced later, it must:

- be clearly marked as optional
- not silently upload user documents
- explain what data leaves the device
- fail safely when the network is unavailable

---

# 4. Privacy Rules

User documents are considered private data.

## 4.1 No Silent Uploads

The application must never silently upload:

- PDFs
- documents
- images
- extracted text
- embeddings
- chat history
- personal notes
- generated answers

to external services.

## 4.2 Local Storage

User data should be stored locally unless the user explicitly chooses otherwise.

## 4.3 Logs

Logs must not unnecessarily contain:

- full document contents
- private user questions
- complete AI responses
- personal information
- sensitive extracted text

Debug logs should use IDs, metadata, and controlled diagnostic information whenever possible.

## 4.4 Privacy Messaging

The UI must clearly communicate the application's local/private nature.

However, privacy claims must accurately reflect actual implementation.

Do not claim:

> "Your data never leaves your device"

unless the complete implementation has been verified to satisfy that claim.

---

# 5. AI Model Rules

## 5.1 Model Selection

Models must not be selected only because they are popular.

Model selection should consider:

- Snapdragon compatibility
- Windows compatibility
- Qualcomm AI Hub availability
- inference performance
- model size
- memory requirements
- quantization support
- accuracy
- context length
- licensing
- offline capability
- integration complexity

## 5.2 Model Abstraction

The application must avoid tightly coupling business logic to one specific model.

Example:

Bad:

```text
ChatPDF -> Llama 3.2 specific implementation
Preferred:

ChatPDF/SnapMind
        |
        v
AI Model Interface
        |
        +---- Model A
        +---- Model B
        +---- Model C

This allows models to be replaced after Snapdragon benchmarking.

5.3 No Fake AI

The application must not generate fake AI outputs for the final competition demo.

Mock data may be used during early UI development, but it must be clearly isolated from production AI workflows.

5.4 No Hardcoded AI Answers

Responses must not be hardcoded to make the demo appear intelligent.

6. RAG Rules

RAG is a core feature of SnapMind.

6.1 Grounded Responses

When answering questions about uploaded documents, the AI should use retrieved document context.

The system must not intentionally fabricate information.

6.2 Citation Requirement

Document-based answers should provide source references whenever the relevant source information is available.

Citation metadata should ideally include:

document name
page number
section/chunk
source identifier
6.3 No Fake Citations

A citation must correspond to an actual retrieved source.

Never generate:

Page 17

if the source content did not come from page 17.

6.4 Insufficient Evidence

If retrieved context is insufficient, the system should communicate uncertainty instead of pretending to know the answer.

Preferred behavior:

I couldn't find enough information in your uploaded documents
to answer this confidently.
6.5 Retrieval Quality

RAG performance should be evaluated using:

retrieval relevance
top-K quality
response grounding
citation correctness
latency
7. Snapdragon Optimization Rules

Snapdragon optimization is one of the most important competition requirements.

7.1 No Unsupported Claims

Never claim:

"Runs on the NPU"

unless this has been verified.

Never claim:

"Uses Qualcomm acceleration"

unless the implementation actually uses a compatible Qualcomm-supported path.

Never claim:

"Optimized for Snapdragon"

without measurable or technical evidence.

7.2 Evidence-Based Optimization

Snapdragon optimization must be demonstrated through one or more of:

supported runtime
Qualcomm AI Hub model deployment
NPU execution
GPU execution
CPU/NPU comparison
latency measurements
memory measurements
power/performance observations
benchmark results
target-device testing
7.3 Hardware Capability Detection

The application should detect available hardware capabilities where practical.

Conceptually:

Hardware
   |
   +-- CPU
   +-- GPU
   +-- NPU
   |
   v
Capability Detection
   |
   v
Runtime Selection
7.4 Fallback

If the preferred acceleration path is unavailable, SnapMind should degrade gracefully.

Example:

Preferred:
NPU

Fallback:
GPU

Fallback:
CPU

The actual priority must be determined through compatibility and benchmark testing.

7.5 No Forced NPU Usage

Do not force a workload onto the NPU simply to claim NPU utilization.

The best hardware backend should be selected based on:

compatibility
latency
memory
reliability
workload type
8. Qualcomm AI Hub Rules

Qualcomm AI Hub should be evaluated as a primary source for Snapdragon-compatible models and deployment options.

8.1 Candidate Evaluation

Potential models should be evaluated for:

supported Snapdragon hardware
supported operating system
supported runtime
model format
quantization
performance
accuracy
integration complexity
8.2 Final Model Selection

The final model should be selected based on actual testing rather than assumptions.

8.3 Documentation

The project documentation should record:

selected model
model version
runtime
target hardware
reason for selection
benchmark results
known limitations
9. Performance Rules

Performance must be measured rather than guessed.

9.1 Important Metrics

Where applicable, measure:

application startup time
model loading time
embedding latency
retrieval latency
time to first token
total response latency
tokens per second
document processing time
memory usage
CPU utilization
GPU utilization
NPU utilization
indexing time
9.2 Benchmark Consistency

Benchmark comparisons should use consistent:

input documents
questions
model configuration
hardware
runtime
measurement method
9.3 No Cherry-Picking

Do not present only the best benchmark result while hiding significantly worse results.

If a result is unusually good or bad, investigate and document it.

9.4 Benchmark Transparency

Competition presentation should distinguish between:

Measured

and

Expected / Theoretical

Do not present theoretical performance as measured performance.

10. Development Rules
10.1 Modular Code

The application must be divided into logical modules.

Avoid putting:

UI logic
AI inference
database logic
document processing
RAG logic
configuration

into one large file.

10.2 Separation of Concerns

Preferred structure:

Frontend
   |
Backend/API
   |
Services
   |
AI/RAG
   |
Runtime
   |
Storage

Each layer should have a clear responsibility.

10.3 Configuration

Environment-specific settings must not be hardcoded unnecessarily.

Use configuration files/environment variables for:

model paths
database paths
runtime settings
ports
feature flags
benchmark settings
10.4 Secrets

Never commit:

API keys
passwords
access tokens
private credentials

to Git.

Use .env or equivalent secure configuration mechanisms.

11. Git Rules
11.1 Meaningful Commits

Commit messages should describe actual changes.

Preferred:

feat: add local document indexing
feat: add citation mapping
perf: benchmark embedding runtime
fix: handle empty document extraction

Avoid:

update
changes
final
final2
working
test
11.2 Commit Frequently

Do not wait until the entire project is finished before committing.

Recommended workflow:

Implement
   ↓
Test
   ↓
Commit
   ↓
Continue
11.3 Never Commit Generated Noise

Avoid committing:

.env
cache folders
Python virtual environments
large temporary files
model binaries unless intentionally required
build output
IDE-specific temporary files

Use .gitignore.

12. Testing Rules

Every major feature must be tested independently.

12.1 Functional Testing

Test:

document upload
document parsing
indexing
retrieval
Q&A
citations
summarization
quiz generation
flashcards
image handling
model loading
hardware detection
12.2 Edge Cases

Test:

empty files
corrupted files
unsupported formats
very large documents
scanned PDFs
documents with images
documents with tables
duplicate documents
missing embeddings
unavailable model
insufficient retrieval context
unavailable hardware acceleration
insufficient memory
12.3 Failure Handling

Failures must produce understandable messages.

Bad:

500 Internal Server Error

Preferred:

The selected model could not be loaded.
Try another model or check available system memory.
13. UI/UX Rules

The UI should make the AI-PC value obvious.

13.1 Core UX

The user should be able to understand:

What SnapMind does
Where their documents are stored
Whether processing is local
Which model is being used
Which hardware backend is being used
Where answers came from
13.2 Loading States

Long operations must have visible progress indicators.

Examples:

Processing document...
Generating embeddings...
Searching knowledge...
Generating answer...
13.3 Errors

Do not expose raw stack traces to normal users.

Developer diagnostics may be available separately.

13.4 Accessibility

Where practical:

readable typography
sufficient contrast
keyboard navigation
understandable icons
clear button labels
responsive layout
14. Feature Scope Rules

The project must prioritize quality over feature count.

Priority 1: Must Work
document ingestion
local knowledge library
RAG Q&A
citations
local AI inference
Snapdragon-compatible deployment path
benchmarking
Priority 2: High Value
summarization
key points
quiz generation
flashcards
hardware information
performance dashboard
Priority 3: Optional
image understanding
OCR
voice interaction
advanced personalization
additional model choices

If time becomes limited, Priority 1 features must be completed before Priority 3 features.

15. Competition Rules

The project must be built for genuine technical evaluation.

15.1 No Fake Demo

Do not create a video where:

fake outputs are shown
benchmark numbers are invented
NPU usage is simulated
screenshots are presented as live functionality
unavailable features are represented as completed
15.2 Demo Must Be Reproducible

The core demo should be reproducible by another person following the project documentation.

15.3 Show Technical Depth

The presentation should demonstrate more than UI.

Recommended demo flow:

Problem
   ↓
SnapMind
   ↓
Import document
   ↓
Local processing
   ↓
Ask question
   ↓
Grounded answer
   ↓
Citation
   ↓
Hardware/runtime information
   ↓
Benchmark
   ↓
Snapdragon advantage
15.4 Show Evidence

Where possible, demonstrate:

local execution
hardware backend
inference latency
model information
memory usage
benchmark comparison
16. Documentation Rules

Important technical decisions must be documented.

Documentation should answer:

What changed?
Why was it changed?
What alternatives were considered?
Why was the selected approach chosen?
What was tested?
What was the result?
What remains unresolved?
Required Documents
PRD.md
ARCHITECTURE.md
RULES.md
PHASES.md
DESIGN.md
MEMORY.md
README.md

README.md is intended for public project documentation.

MEMORY.md is intended as the internal project decision/history log.

17. MEMORY.md Update Rule

MEMORY.md must be updated after every meaningful project change.

A meaningful change includes:

architecture changes
model selection
runtime selection
database changes
major UI changes
new features
removed features
rejected approaches
benchmark findings
important bugs
deployment findings
Snapdragon compatibility discoveries

Each entry should explain:

Date
Change
Reason
Impact
Decision
Current Status

Example:

## 2026-09-15

### Change
Changed vector database from Option A to Option B.

### Reason
Option B provided simpler local deployment and lower memory usage.

### Impact
Reduced deployment complexity.

### Decision
Option B selected for MVP.

### Status
Implemented and benchmarked.
18. No Unnecessary Technology Rule

Do not add a technology simply because it is popular.

Every major dependency should answer:

Why is it needed?
What problem does it solve?
Is there a simpler alternative?
Does it support local execution?
Does it work on Windows/Snapdragon?
What is its performance impact?
What is its licensing situation?

If a dependency does not provide meaningful value, do not add it.

19. Model and Dependency Reproducibility

The project should document important versions.

For example:

Python version
Node version
Frontend dependencies
Backend dependencies
Model name/version
Runtime
Vector database
Operating system

This reduces "works on my machine" problems.

20. Security Rules
20.1 File Validation

Uploaded files should be validated before processing.

Validation should consider:

extension
MIME type
file size
parser support
malformed files
20.2 Path Safety

User-controlled filenames must not be allowed to escape the application's storage directory.

20.3 API Safety

Local APIs should validate:

request format
file references
IDs
model selection
configuration values
20.4 No Arbitrary Code Execution

Uploaded documents must never be treated as executable code.

21. AI Safety and Reliability Rules
21.1 Uncertainty

The system should acknowledge uncertainty when evidence is insufficient.

21.2 Source Priority

For document questions:

Retrieved user content
        >
Model's general knowledge

when the question specifically concerns the uploaded material.

21.3 No Misleading Confidence

The system should not make unsupported claims simply because the language model produces a confident response.

21.4 Context Isolation

Documents should remain logically separated where required.

For example, asking about Document A should not accidentally retrieve unrelated content from Document B unless the user explicitly uses a multi-document knowledge query.

22. Offline Mode Rules

The core workflow should function without internet access once required assets are installed.

Offline testing should eventually verify:

Internet
   OFF
    ↓
Open SnapMind
    ↓
Load local documents
    ↓
Retrieve information
    ↓
Generate answer
    ↓
Display citation

If a feature cannot work offline, it must be clearly identified as an optional online feature.

23. Hardware Testing Rules

Hardware-dependent features must be tested separately from ordinary software functionality.

Testing should distinguish:

Software correctness

from:

Hardware acceleration

A feature can be functionally correct while acceleration is still unverified.

Both states must be documented independently.

24. Fallback and Recovery Rules

The application should recover gracefully from:

model loading failures
runtime failures
missing files
corrupted indexes
unavailable acceleration
insufficient memory
unsupported documents
interrupted processing

Preferred recovery:

Detect failure
     ↓
Explain failure
     ↓
Attempt safe fallback
     ↓
Continue if possible

Never silently switch to a completely different behavior.

25. No Premature Optimization

Do not optimize before identifying a measurable bottleneck.

Preferred process:

Build
 ↓
Measure
 ↓
Identify bottleneck
 ↓
Optimize
 ↓
Measure again

Optimization claims must be supported by before/after measurements.

26. Architecture Change Rule

Do not make major architecture changes casually.

Before changing a major component, document:

current approach
problem
proposed approach
reason
expected benefit
migration impact
testing requirement

Then update:

ARCHITECTURE.md
MEMORY.md
PHASES.md

where applicable.

27. Feature Removal Rule

Removing a feature is acceptable if it improves:

reliability
performance
privacy
simplicity
Snapdragon compatibility
development feasibility

A removed feature should be recorded in MEMORY.md if it was previously part of the plan.

28. Demo Stability Rule

Before the final competition submission:

freeze unnecessary feature development
test the complete demo flow
remove obvious bugs
verify benchmark results
verify hardware/runtime claims
verify citations
verify privacy messaging
verify installation instructions

The final days should focus primarily on stability and presentation rather than adding risky features.

29. Presentation Rules

The final presentation should answer five questions:

1. What problem are we solving?

Explain the problem in simple terms.

2. Why local AI?

Explain:

privacy
offline capability
lower dependency on cloud
potentially lower latency
3. Why Snapdragon?

Explain the role of:

NPU
CPU
GPU
Qualcomm AI Hub
optimized inference
4. What makes SnapMind different?

Focus on:

private knowledge base
local RAG
grounded answers
citations
AI-PC hardware awareness
measurable optimization
5. What evidence supports the claims?

Show:

actual demo
actual measurements
actual runtime information
actual hardware information
30. Final Submission Integrity Rule

Every statement in the final submission must fall into one of these categories:

Implemented
Tested
Measured
Documented
Planned

Do not describe a planned feature as implemented.

Do not describe an untested feature as tested.

Do not describe an estimated benchmark as measured.

Do not describe theoretical Snapdragon support as verified deployment.

31. Definition of a Trustworthy Claim

A claim is considered trustworthy only when there is evidence.

Example:

Weak

SnapMind provides extremely fast NPU inference.

Strong

On the tested Snapdragon configuration, the selected model achieved an average inference latency of X ms using the configured acceleration backend, compared with Y ms on CPU.

The second statement is preferred because it is measurable and reproducible.

32. Decision-Making Rule

When uncertain between two technical approaches, evaluate them in this order:

1. Does it work?
2. Is it local?
3. Is it privacy-safe?
4. Does it support Snapdragon?
5. Can we measure it?
6. Is it reliable?
7. Is it maintainable?
8. Is it simple?
9. Does it improve the user experience?
10. Does it strengthen the competition submission?
33. Golden Rule

The most important rule of SnapMind is:

Build what we can prove, measure what we claim, and never fake what we cannot verify.

The project should be impressive because of genuine engineering, not because of exaggerated claims.

34. Current Rule Status

The following rules are currently mandatory:

 Local-first architecture
 Privacy-first design
 Model abstraction
 RAG grounding
 Citation integrity
 No fake AI outputs
 No fake benchmark numbers
 No unsupported Snapdragon/NPU claims
 Evidence-based optimization
 Modular architecture
 Meaningful Git commits
 Security-conscious file handling
 Graceful fallback
 MEMORY.md updates after meaningful changes
 Competition demo integrity
35. Relationship With Other Documents
Document	Responsibility
PRD.md	What and why
ARCHITECTURE.md	How the system works
RULES.md	What must and must not be done
PHASES.md	Development sequence
DESIGN.md	UI/UX and visual system
MEMORY.md	Project history and decisions
README.md	Public project documentation

These documents should remain consistent.

If a major decision changes the project direction, the relevant documents must be updated.

END OF RULES.md
```
