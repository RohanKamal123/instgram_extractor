# Architecture

## High-Level System

Instagram
    ↓
Authenticated Chromium
    ↓
Playwright Browser Agent
    ↓
DM/Reel Collector
    ↓
Reel Archive
    ↓
Media Extraction
    ↓
Transcript + OCR + Metadata
    ↓
AI Analysis
    ↓
Personal Knowledge Base
    ↓
Search / Semantic Search / Chat

## Components

### Browser Agent

Responsible for:

- opening Instagram
- navigating accessible DMs
- identifying Reel messages
- extracting metadata
- opening Reel pages when necessary
- retrieving accessible media/content

The browser agent must be resumable.

It must remember what it has already processed.

### Ingestion Layer

Converts browser observations into normalized Reel records.

The ingestion layer should not perform AI analysis directly.

### Media Processor

Handles:

- media retrieval
- temporary storage
- audio extraction
- frame extraction when needed

### Transcription Layer

Priority:

1. Instagram transcript
2. subtitles
3. local Whisper

The interface should abstract the transcription backend.

### OCR Layer

Extracts useful text from Reel frames when necessary.

### AI Layer

Responsible for converting raw Reel information into structured knowledge.

DeepSeek is the initial provider.

The provider should be replaceable.

### Storage Layer

Store raw/archive information separately from derived AI information.

SQLite is sufficient for the initial personal version.

Avoid introducing PostgreSQL or distributed infrastructure without a concrete need.

### Search Layer

Initial:

- SQLite full-text/keyword search

Later:

- vector embeddings
- semantic search
- hybrid retrieval

### Web Application

Mobile-first interface because the user primarily wants to consume and search the archive conveniently.

Primary views:

- Inbox
- Library
- Search
- Reel details
- Actions
- Chat

## Processing Pipeline

For each new Reel:

1. Detect Reel.
2. Create Reel record.
3. Extract metadata.
4. Attempt content/media retrieval.
5. Obtain transcript.
6. Run OCR if useful.
7. Construct unified content representation.
8. Send appropriate content to the LLM.
9. Store structured analysis.
10. Generate embedding.
11. Mark processing complete.
12. Make Reel searchable.

Failures should not lose the Reel.

A failed processing job can be retried independently.

## Privacy

The system handles private Instagram content.

Therefore:

- never log passwords
- never expose browser cookies
- never commit secrets
- minimize external API transmission
- make AI provider usage explicit
- retain raw media only according to configured policy

## Design Principle

The system should optimize for:

**Capture once → understand automatically → retrieve forever.**
