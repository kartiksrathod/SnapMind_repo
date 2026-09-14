DESIGN.md

# SnapMind

## UI/UX Design System and Product Experience

**Project:** SnapMind  
**Purpose:** Private On-Device AI Knowledge Assistant  
**Target Platform:** Snapdragon-powered HP PCs  
**Platform:** Windows  
**Design Goal:** Premium AI-PC experience with clear privacy, AI, and hardware visibility  
**Status:** Active  
**Last Updated:** September 2026

---

# 1. Design Philosophy

SnapMind should feel like a modern AI-native desktop application rather than a traditional document management tool.

The interface must communicate three things immediately:

```text
PRIVATE
LOCAL AI
SNAPDRAGON-READY

The design should be:

modern
premium
minimal
professional
technically credible
easy to navigate
responsive
information-rich without being overwhelming
2. Primary UX Principle

The user should never have to understand the underlying AI architecture to use SnapMind.

The normal workflow should feel simple:

Import
  ↓
Ask
  ↓
Understand
  ↓
Learn

The technical information should be available when the user wants it.

3. Design Hierarchy

SnapMind has three levels of information.

Level 1 - User Experience

Visible to everyone.

Examples:

documents
chat
summaries
quiz
flashcards
Level 2 - AI Information

Visible during AI interaction.

Examples:

model
source
citations
processing status
Level 3 - Technical Information

Visible through hardware/benchmark screens.

Examples:

runtime
backend
NPU
GPU
CPU
latency
memory

This prevents the main interface from becoming too technical.

4. Application Layout

Primary desktop layout:

┌─────────────────────────────────────────────────────────────┐
│ SnapMind                                      System Status │
├───────────────┬─────────────────────────────────────────────┤
│               │                                             │
│  Logo         │                                             │
│               │                                             │
│  Dashboard    │               Main Content                  │
│  Documents    │                                             │
│  Knowledge    │                                             │
│  Chat         │                                             │
│  Study        │                                             │
│               │                                             │
│  ─────────    │                                             │
│  Hardware     │                                             │
│  Benchmark    │                                             │
│               │                                             │
│  Settings     │                                             │
│               │                                             │
└───────────────┴─────────────────────────────────────────────┘
5. Navigation

Primary navigation:

Dashboard
Documents
Knowledge
Chat
Study
Hardware
Benchmark
Settings
Navigation Responsibilities
Dashboard

Overview of the user's workspace.

Documents

Manage imported files.

Knowledge

Explore indexed knowledge.

Chat

Ask questions.

Study

Quiz and flashcards.

Hardware

View AI/runtime/hardware information.

Benchmark

View performance measurements.

Settings

Application configuration.

6. Dashboard Design

The dashboard is the first screen after opening SnapMind.

Goal

Give the user an immediate overview.

Dashboard Structure
┌─────────────────────────────────────────────────────────────┐
│ Good evening                                               │
│ Your private knowledge workspace                            │
│                                                             │
│ [ Import Document ]                                        │
├──────────────────────┬──────────────────────────────────────┤
│ Documents            │ AI Status                            │
│ 12                   │ Local AI ● Ready                    │
│                      │ Model: Selected Local Model          │
├──────────────────────┼──────────────────────────────────────┤
│ Knowledge            │ Hardware                             │
│ 4,832 chunks         │ Snapdragon / Accelerator             │
├──────────────────────┴──────────────────────────────────────┤
│ Recent Documents                                           │
│                                                            │
│ Document 1                                                │
│ Document 2                                                │
│ Document 3                                                │
└─────────────────────────────────────────────────────────────┘
7. Dashboard Components
Welcome Header

Display:

Good evening
Your private knowledge workspace

The exact greeting can be time-aware.

Primary Action

Large button:

+ Import Document

This should be the most visually prominent action.

Statistics

Display useful metrics:

Documents
Knowledge Chunks
Questions Asked
Study Items

Avoid showing meaningless statistics.

8. AI Status Card

Example:

LOCAL AI

● Ready

Model
Selected Local Model

Runtime
Selected Runtime

Backend
NPU

The actual values must come from the system.

Never hardcode technical status.

9. Hardware Status Card

Example:

HARDWARE

Snapdragon
AI acceleration available

Accelerator
NPU

Status
Ready

If hardware detection is unavailable:

Hardware information unavailable

Do not fabricate hardware information.

10. Documents Screen
Goal

Provide a clean local knowledge library.

Layout:

┌─────────────────────────────────────────────────────────────┐
│ Documents                                      + Import     │
│                                                             │
│ Search documents...                            Filter ▼     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐      │
│ │ PDF           │ │ PDF           │ │ DOCX          │      │
│ │               │ │               │ │               │      │
│ │ ML Notes      │ │ Research      │ │ Project Spec  │      │
│ │ 42 pages      │ │ 18 pages      │ │ 12 pages      │      │
│ │ ● Indexed     │ │ ● Indexed     │ │ Processing... │      │
│ └───────────────┘ └───────────────┘ └───────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
11. Document Card

Each card should show:

file type
document name
page count
size
processing status
date
actions

Example:

PDF

Machine Learning Notes

42 pages
2.8 MB

● Indexed
12. Processing States

Documents should have clear states.

Uploading
    ↓
Processing
    ↓
Extracting
    ↓
Embedding
    ↓
Indexed

Failure:

Processing failed

The UI should allow retry where appropriate.

13. Knowledge Screen

The Knowledge screen represents the indexed knowledge base.

Possible sections:

All Knowledge
Documents
Topics
Recent

Show:

source document
section
page
chunk information
indexed status

The screen should help users understand where AI answers originate.

14. Chat Screen

Chat is the primary AI interaction screen.

Layout:

┌─────────────────────────────────────────────────────────────┐
│ Chat                                     Model: Local AI    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                     AI conversation                         │
│                                                             │
│ User                                                       │
│ Explain the main concept in this document.                 │
│                                                             │
│ SnapMind                                                   │
│ The main concept is...                                    │
│                                                             │
│ Sources                                                    │
│ [1] ML Notes · Page 12                                    │
│ [2] ML Notes · Page 14                                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Ask anything about your knowledge...                 Send │
└─────────────────────────────────────────────────────────────┘
15. Chat Message Design
User Message

Minimal and visually distinct.

AI Message

Should contain:

answer
optional structured information
sources

Example:

The document explains supervised learning as...

Sources
────────────────────────
[1] Machine Learning Notes
Page 12
16. Citation Design

Citations are a major SnapMind differentiator.

They should not look like generic footnotes.

Example:

According to the document, supervised learning
uses labeled examples to learn a mapping. [1]

Sources

┌───────────────────────────────────────────┐
│ [1] Machine Learning Notes                │
│ Page 12 · Supervised Learning             │
│                                           │
│ Open source →                             │
└───────────────────────────────────────────┘

If source preview is supported, clicking the citation can open the relevant document location.

17. Citation Rules

Citation UI must distinguish:

Verified Source

from:

No Supporting Source Found

If no supporting evidence exists, do not display a fake citation.

18. Chat Processing State

When generating a response:

Retrieving knowledge...
       ↓
Preparing context...
       ↓
Generating locally...

If streaming is supported:

Generating...
The model response appears progressively.
19. Chat Empty State

Before the first question:

Ask your knowledge anything.

Try:

"Summarize this document"

"What are the key concepts?"

"Create a quiz from this chapter"

"Compare these two documents"

Suggestions should be based on actual available features.

20. Study Screen

The Study section contains:

Summary
Quiz
Flashcards
Key Points

Layout:

┌─────────────────────────────────────────────────────────────┐
│ Study                                                      │
│ Turn your documents into learning material.                │
│                                                             │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│ │ Summary    │ │ Quiz       │ │ Flashcards │               │
│ └────────────┘ └────────────┘ └────────────┘               │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Key Points                                              │ │
│ │ • Concept 1                                             │ │
│ │ • Concept 2                                             │ │
│ │ • Concept 3                                             │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
21. Quiz Design

Quiz screen:

Question 4 of 10

What is the primary purpose of...?

○ Option A

○ Option B

○ Option C

○ Option D

                    [ Submit ]

After submission:

Correct

Explanation:
...

Source:
Document · Page 8
22. Flashcard Design

Front:

┌───────────────────────────────┐
│                               │
│ What is supervised learning?  │
│                               │
│       Click to reveal         │
│                               │
└───────────────────────────────┘

Back:

┌───────────────────────────────┐
│ Supervised learning is...     │
│                               │
│ Source: Page 12               │
└───────────────────────────────┘
23. Hardware Screen

This screen is important for the competition.

Goal

Make the Snapdragon optimization visible without making unsupported claims.

Layout:

┌─────────────────────────────────────────────────────────────┐
│ Hardware                                                   │
│ AI acceleration and runtime information                    │
├─────────────────────────────────────────────────────────────┤
│ Device                                                     │
│ Snapdragon-powered Windows PC                              │
│                                                             │
│ CPU              GPU              NPU                      │
│ Available        Available        Available                │
├─────────────────────────────────────────────────────────────┤
│ Current AI Backend                                          │
│                                                             │
│ Runtime:       Selected Runtime                             │
│ Model:         Selected Model                               │
│ Accelerator:   NPU                                         │
│ Status:        ● Active                                    │
└─────────────────────────────────────────────────────────────┘

Only show information verified by the actual system.

24. Hardware Capability States

Possible states:

Available
Active
Unavailable
Unsupported
Unknown

Example:

NPU
Available

Status
Active

or:

NPU
Available

Status
Not used for current workload

This distinction is important.

25. Benchmark Screen

The benchmark screen should communicate measurable performance.

Layout:

┌─────────────────────────────────────────────────────────────┐
│ Benchmark                                                  │
│ Measure SnapMind AI performance                            │
├─────────────────────────────────────────────────────────────┤
│ Workload                                                   │
│ [ RAG Question ▼ ]                                        │
│                                                             │
│ Backend                                                   │
│ [ NPU ▼ ]                                                 │
│                                                             │
│                    [ Run Benchmark ]                       │
├─────────────────────────────────────────────────────────────┤
│ Results                                                    │
│                                                             │
│ Average Latency        XXX ms                              │
│ First Token            XXX ms                              │
│ Throughput             XX tokens/s                         │
│ Memory                 XXX MB                              │
└─────────────────────────────────────────────────────────────┘
26. Benchmark Comparison

When multiple backends are available:

Performance

CPU    ███████████████
GPU    █████████
NPU    █████

The chart must be generated from actual benchmark data.

No manually created fake values.

27. Benchmark History

Store previous results.

Example:

Date
Model
Runtime
Backend
Workload
Latency
Memory

Users should be able to compare runs.

28. Settings Screen

Settings should be divided into logical sections.

General
AI Models
Knowledge
Privacy
Performance
Advanced
29. AI Model Settings

Show:

Current Model
Model Path
Runtime
Quantization
Context Length

Advanced settings should not overwhelm normal users.

30. Privacy Settings

Clearly communicate:

Processing Mode

● Local

If online functionality exists:

Online Features
[ Enabled / Disabled ]

Any feature capable of sending data externally must explain what happens.

31. Performance Settings

Potential options:

Preferred Backend
Automatic
NPU
GPU
CPU

Performance Mode
Balanced
Performance
Efficiency

Only expose options actually supported by the implementation.

32. Visual Language

SnapMind should have a dark, premium AI-PC aesthetic.

The interface should use:

dark backgrounds
elevated cards
subtle borders
restrained accent elements
clean typography
clear hierarchy
soft depth
minimal visual noise

The design should feel closer to a professional AI workstation than a gaming dashboard.

33. Color System

Use a restrained palette.

Background

Primary application background:

#0B0D10

Secondary surface:

#11151A

Card surface:

#161B22

Border:

#252C35
Primary Accent

Use a cool technical accent suitable for AI/hardware branding.

Suggested:

#7C8CFF
Success
#35D07F
Warning
#F4B740
Error
#F05D6C

These colors should be used sparingly.

34. Typography

Recommended:

Font:
Inter

Fallback:

system-ui
sans-serif
Hierarchy

Page title:

28-32px

Section title:

20-24px

Body:

14-16px

Secondary text:

12-14px

Avoid excessive font-size variation.

35. Spacing

Use a consistent spacing scale.

Recommended base:

4px
8px
12px
16px
24px
32px
48px

Do not use arbitrary spacing values throughout the application.

36. Border Radius

Use moderate rounding.

Recommended:

Small:
8px

Cards:
12px

Large panels:
16px

Buttons:
8-10px

Avoid excessive pill-shaped UI.

37. Cards

Cards should have:

subtle background difference
thin border
consistent padding
clear title
useful content

Avoid placing every small piece of information inside a separate card.

38. Buttons

Primary button:

+ Import Document

Secondary:

Run Benchmark

Tertiary:

View Source

Destructive:

Delete

Button labels should describe the action clearly.

39. Icons

Use icons consistently.

Suggested icon categories:

Documents
Chat
Search
Settings
Hardware
Benchmark
Quiz
Flashcards
Upload
Delete
Source

Icons should support text rather than replace it.

40. Loading Animation

Loading states should feel technical but subtle.

Avoid distracting animations.

Example:

● Processing document...

or a small progress indicator.

41. AI Activity Indicator

During AI processing:

LOCAL AI
● Processing

Potential detailed state:

Retrieving
Preparing context
Generating
Complete
42. Privacy Indicator

A small persistent indicator can communicate local processing.

Example:

● Local processing

Possible placement:

Top-right

or near the active AI model.

The indicator must reflect actual system behavior.

43. Hardware Indicator

Example:

Snapdragon AI
● Ready

When an accelerator is actively being used:

Snapdragon AI
● NPU Active

Only show NPU Active when verified.

44. Empty States

Every major page should have a useful empty state.

No Documents
Your knowledge library is empty.

Import your first document to get started.

[ Import Document ]
No Chat
Start asking questions about your knowledge.
No Benchmark
No benchmark results yet.

Run your first benchmark to measure AI performance.
45. Error States

Errors should be actionable.

Bad:

Error 500

Preferred:

The document could not be processed.

Try:
• checking the file format
• importing another document
• retrying the operation
46. Responsive Behavior

The primary target is a Windows desktop/laptop.

Minimum design target:

Laptop / Desktop

The application should still behave reasonably at smaller desktop resolutions.

47. Accessibility

The UI should support:

keyboard navigation
visible focus states
readable text
accessible labels
semantic controls
sufficient contrast
understandable error messages
48. Animation Rules

Animations should be:

short
purposeful
subtle

Use animation for:

page transitions
loading
state changes
card interaction

Do not animate everything.

49. Competition Demo Mode

A dedicated demo configuration may be created if useful.

Possible behavior:

Demo Mode
   ↓
Preconfigured documents
   ↓
Known benchmark dataset
   ↓
Stable workflow

However, demo mode must still use real application functionality.

It must not replace real AI with fake outputs.

50. Competition Demo Screen

The demo should make the important story visible.

Suggested flow:

Dashboard
   ↓
Import Document
   ↓
Processing
   ↓
Chat
   ↓
Question
   ↓
Answer + Citation
   ↓
Hardware
   ↓
Benchmark

The user should be able to navigate this flow quickly.

51. Technical Transparency

The UI should distinguish between:

User-facing information

and:

Developer/technical information

Example:

Normal user:

Local AI Ready

Advanced information:

Model: [actual model]
Runtime: [actual runtime]
Backend: [actual backend]
Accelerator: [actual accelerator]
52. Responsive Component Architecture

Recommended React structure:

components/
│
├── layout/
│   ├── Sidebar
│   ├── Topbar
│   └── PageContainer
│
├── dashboard/
│   ├── WelcomeHeader
│   ├── StatsCard
│   ├── AIStatusCard
│   └── HardwareCard
│
├── documents/
│   ├── DocumentCard
│   ├── UploadDialog
│   └── ProcessingStatus
│
├── chat/
│   ├── ChatMessage
│   ├── ChatInput
│   ├── Citation
│   └── SourceCard
│
├── study/
│   ├── Quiz
│   ├── Flashcard
│   └── Summary
│
├── hardware/
│   ├── HardwareCard
│   ├── RuntimeCard
│   └── AcceleratorStatus
│
└── benchmark/
    ├── BenchmarkRunner
    ├── MetricCard
    └── BenchmarkChart
53. Design Tokens

Centralize design values.

Conceptually:

colors
spacing
radius
typography
shadows
transitions

Do not scatter visual constants throughout the codebase.

54. Design Rules
Must
maintain visual consistency
show meaningful loading states
show useful errors
preserve citation visibility
make local processing visible
make hardware status understandable
keep technical claims truthful
Must Not
overload the dashboard
use excessive gradients
use excessive animations
hide important citations
fake hardware status
fake benchmark data
create unnecessary screens
sacrifice usability for visual effects
55. Mobile UI

Mobile is not a primary target for the competition.

A responsive web layout may exist, but desktop Windows experience has priority.

Development time should not be diverted to extensive mobile optimization before the desktop product is stable.

56. Design Priorities

Priority order:

1. Usability
2. Clarity
3. Technical credibility
4. Visual polish
5. Animation

A beautiful interface that is confusing is not considered successful.

57. Final Visual Goal

The final application should communicate:

┌───────────────────────────────────────────┐
│                                           │
│               SNAPMIND                    │
│                                           │
│       Your private AI knowledge space     │
│                                           │
│        Local AI     Private     Fast      │
│                                           │
│       Snapdragon-powered experience       │
│                                           │
└───────────────────────────────────────────┘

The user should understand the product within a few seconds.

58. Definition of Done

The design system is considered complete when:

 Navigation is consistent
 Dashboard is complete
 Document library is complete
 Chat interface is complete
 Citation UI is complete
 Study interface is complete
 Hardware screen is complete
 Benchmark screen is complete
 Settings are complete
 Loading states exist
 Error states exist
 Empty states exist
 Typography is consistent
 Spacing is consistent
 Components are reusable
 Design tokens are centralized
 Competition demo flow is clear
59. Relationship With Other Documents
Document	Responsibility
PRD.md	Product requirements
ARCHITECTURE.md	Technical architecture
RULES.md	Engineering and project rules
PHASES.md	Development roadmap
DESIGN.md	UI/UX design
MEMORY.md	Project decisions and history
README.md	Public documentation
60. Current Status
Design System       PLANNED
Navigation          PLANNED
Dashboard           PLANNED
Documents           PLANNED
Knowledge           PLANNED
Chat                PLANNED
Study               PLANNED
Hardware            PLANNED
Benchmark           PLANNED
Settings            PLANNED
Design Tokens       PLANNED
Competition Demo    PLANNED
END OF DESIGN.md

### Ab last core file hai: **`MEMORY.md`**

Ye normal documentation nahi hai. Ye hamara **project brain / decision history** hoga. Isme har meaningful change ke saath **kya change hua + kyun hua + kya reject kiya + current state** maintain karenge. Iske baad hum **actual Phase 0 coding start** kar sakte hain.
```
