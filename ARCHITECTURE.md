# Architecture

## System Principles

The system is a personal, continuously running, human-in-the-loop Reel archivist.

The key principle is:

**Capture once → understand automatically → ask when important information is uncertain → store structured knowledge → retrieve without reopening the Reel.**

The generated PDF and summaries are reports, not the system's memory. The knowledge base is the canonical source for later retrieval and RAG.

## Development / Runtime Separation

### Development

Windows
    ↓
Trae
    ↓
Local project
    ├── application
    ├── Playwright/Chromium
    ├── local processing
    └── tests
    ↓
Git
    ↓
GitHub (canonical source)

### Runtime / Deployment

The VPS is used for persistent runtime/infrastructure workloads when needed. It is not the primary development workstation.

Do not distribute components to the VPS prematurely. Build the simplest working local system first, then move workloads that have a concrete reason to run remotely.

## High-Level Application Architecture

User
  ↓
Chrome with Instagram already authenticated
  ↓
Extractor command
  ↓
Interactive control/status UI
  ↓
Authenticated Playwright browser agent
  ↓
Source account selection + lock
  ↓
DM/Reel discovery
  ↓
Persistent processing queue
  ↓
Reel archive
  ↓
Media/content extraction
  ↓
Transcript + OCR + metadata + visual understanding
  ↓
AI analysis
  ↓
Uncertainty / evidence check
  ├── sufficiently known → store analysis
  └── important ambiguity → Human Question Queue
                                  ↓
                              User answer
                                  ↓
                              Resume processing
  ↓
Structured Personal Knowledge Base
  ├── keyword retrieval
  ├── semantic retrieval
  └── RAG/conversational retrieval
  ↓
Reports / PDF / summaries / visualizations

## Browser Agent

Responsible for:

- connecting to the user's already-authenticated Chrome/Chromium session or an appropriate persistent browser profile
- opening/navigating Instagram
- verifying the requested source identity
- locking the selected source for the session
- navigating accessible DMs
- identifying Reel messages
- extracting metadata and URLs
- opening Reel pages when necessary
- retrieving accessible media/content
- reporting progress to the UI

The browser agent must be resumable and defensive against Instagram UI changes.

It must not perform social actions.

## Interactive Control and Status UI

The user should always have a clear view of what the system is doing.

At minimum, expose:

- session state
- selected Instagram identity/conversation
- current Reel and URL
- current processing stage
- progress counts
- failures/retries
- pending questions
- whether the worker is running, paused, waiting for input, or complete

The UI is operational, not merely decorative. A user should be able to understand why the system is waiting and what will happen next.

## Ingestion Layer

Converts browser observations into normalized Reel records.

Responsibilities:

- deduplication
- source identity association
- Reel URL normalization
- metadata extraction
- persistence
- resumable discovery

The ingestion layer should not perform AI analysis directly.

## Processing Queue / Worker

Processing is asynchronous and continuous.

Each Reel moves through independent stages so failures can be retried without losing the Reel.

The system must persist job state and avoid unnecessarily reprocessing completed work.

A session may continue processing while some items wait for human answers.

## Media Processor

Handles:

- media retrieval where technically possible
- temporary storage
- audio extraction
- frame extraction when needed

Media retention follows the configured policy.

## Transcription Layer

Priority:

1. Instagram-provided transcript/captions
2. accessible subtitles
3. extracted audio + local Whisper
4. another appropriate fallback when explicitly supported

The interface abstracts the transcription backend.

Transcript provenance and confidence should be retained.

## OCR / Visual Understanding

OCR extracts useful text from frames when necessary.

Visual analysis captures information that speech/transcript alone cannot represent.

The final content representation may combine:

- transcript
- subtitles
- OCR
- caption
- metadata
- selected visual observations

## AI Layer

Responsible for converting raw Reel information into structured knowledge.

DeepSeek is the initial general-purpose provider.

The provider/model must remain replaceable.

The AI should produce structured outputs rather than only prose.

The AI must distinguish facts from inference.

## Uncertainty / Human Question Layer

This layer is a core part of the architecture, not an optional UI feature.

When important information is missing, contradictory, or materially ambiguous, the system should create a question instead of silently guessing.

Each question should retain:

- Reel reference/URL
- question text
- evidence/context
- options when suitable
- free-text fallback when suitable
- reason the question was generated
- confidence/uncertainty information when useful
- status
- user's answer
- timestamp

The system should prefer MCQ when the ambiguity naturally has discrete choices because this minimizes user effort.

User answers become durable knowledge and must survive AI-analysis regeneration.

## Knowledge Base

Store raw/archive information separately from derived AI information and user-provided corrections.

SQLite is sufficient for the initial personal version.

Avoid PostgreSQL, vector databases, or distributed infrastructure without a concrete need.

The knowledge base should contain enough structured information for future RAG retrieval without requiring the user to attach generated reports.

## Retrieval Layer

### Keyword

Use SQLite full-text search or an equivalent simple local mechanism initially.

### Semantic

Add embeddings when needed for semantic retrieval.

### Conversational / RAG

The conversational interface retrieves relevant Reel records, transcripts, analyses, user answers, and relationships from the knowledge base before generating an answer.

Generated PDFs are not the primary retrieval source.

## Reporting Layer

After a processing run or when requested, generate a polished human-readable report from the actual knowledge base.

Outputs may include:

- detailed PDF
- executive summary
- collection statistics
- topic/category distributions
- important Reel rankings
- recurring themes
- entities/tools/products
- resources
- action items
- related-content clusters
- forgotten/unacted-on content
- unresolved questions
- visualizations

The report should be deliberately designed, specific to the user's data, concise where possible, and free from generic AI filler.

## Processing Pipeline

For each Reel:

1. Detect Reel.
2. Create/resolve Reel record.
3. Extract metadata.
4. Retrieve media/content where technically possible.
5. Obtain transcript.
6. Run OCR when useful.
7. Build unified content representation.
8. Run structured AI analysis.
9. Evaluate important uncertainty.
10. If clarification is required, create a human question and pause that dependent stage.
11. Store analysis and user-provided answers/corrections.
12. Generate embedding when enabled.
13. Mark processing complete.
14. Make the Reel searchable.

Failures should not lose the Reel.

## Privacy

The system handles private Instagram content.

Therefore:

- never log passwords
- never expose browser cookies/session tokens
- never commit secrets
- minimize external API transmission
- make AI provider usage explicit
- retain raw media only according to configured policy
- keep reports and local databases protected

## Design Principle

The system should optimize for:

**Capture once → understand automatically → clarify only when necessary → retrieve forever.**
