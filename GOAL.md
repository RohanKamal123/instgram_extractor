# Product Goal

## Product

A personal AI archivist for Instagram Reels.

## Core Problem

The user frequently sends interesting Instagram Reels to themselves because they want to remember or learn from them.

Over time, the collection becomes large.

Opening each Reel again, understanding it, and manually taking notes is difficult and time-consuming.

As a result, valuable information gets buried inside Instagram DMs.

## Goal

Automatically transform the user's Instagram Reel collection into a structured, searchable, understandable personal knowledge base.

The user should be able to continue using Instagram exactly as they normally do.

The system should remove the work that happens afterward.

Desired workflow:

    Find interesting Reel
        ↓
    Send/share Reel to self
        ↓
    Forget about it
        ↓
    AI processes it
        ↓
    Transcript + understanding + metadata
        ↓
    Personal knowledge base
        ↓
    Search / browse / ask questions later

## Primary User

One person: the owner of this project.

This is a personal tool, not a SaaS product.

## Core Value Proposition

The system saves the user from repeatedly opening Reels and manually taking notes.

The system should answer:

"Everything I saved is now understandable and retrievable without me having to manually revisit every Reel."

## Required Capabilities

### Instagram ingestion

Use an authenticated browser session.

The user logs into Instagram manually.

The system then navigates accessible Instagram DMs and identifies Reel content.

Primary source:

- self-DM

Secondary supported source:

- other accessible DM conversations where Reels were sent

### Content understanding

Every Reel should be processed as completely as practical.

Extract:

- caption
- creator
- Reel URL
- date/time when available
- transcript
- subtitles
- visible text
- important visual information
- metadata

### Transcript

A transcript should be generated whenever technically possible.

If Instagram does not provide one, generate it from the Reel's audio using Whisper or another appropriate speech-to-text system.

### AI knowledge extraction

Create a structured note containing:

- title
- summary
- key points
- topics
- categories
- likely reason saved
- tools
- products
- people
- companies
- claims
- resources
- action items
- importance
- confidence
- relationships

### Retrieval

Support:

- keyword search
- semantic search
- conversational search

## Long-Term Vision

The Reel itself is not the ultimate value.

The valuable asset is the structured knowledge extracted from the Reel and its relationship with everything else the user has saved.

Eventually the system should be able to discover connections such as:

- multiple Reels about the same technology
- repeated interests
- related tools
- ideas that appeared repeatedly
- saved content that has not been acted upon
- older content relevant to a current question

## Non-Goals

Do not initially build:

- multi-user accounts
- SaaS billing
- social-media engagement automation
- automatic liking
- commenting
- following
- messaging
- a general-purpose Instagram bot
- unnecessary enterprise infrastructure

## Success Criteria

The project succeeds when the user can:

1. Log into Instagram manually.
2. Let the system find their saved Reel messages.
3. Have Reels automatically processed.
4. Obtain transcripts even when Instagram does not provide them.
5. Read a useful structured note instead of reopening every Reel.
6. Search for old Reels using normal or semantic queries.
7. Ask questions about their collection.
8. Find useful content they previously forgot about.

The most important metric is:

**How much time does this save the user compared with manually revisiting and taking notes on their Reels?**
