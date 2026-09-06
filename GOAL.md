# Product Goal

## Product

A personal AI archivist for Instagram Reels.

It continuously turns the user's Reel collection into structured, searchable personal knowledge while asking the user for clarification whenever important information cannot be reliably determined.

## Core Problem

The user frequently sends interesting Instagram Reels to themselves because they want to remember or learn from them.

Over time, the collection becomes large. Opening each Reel again, understanding it, and manually taking notes is difficult and time-consuming.

As a result, valuable information gets buried inside Instagram DMs.

## Core Goal

Automatically transform the user's Instagram Reel collection into a structured, searchable, understandable personal knowledge base.

The user should continue using Instagram normally. The system removes the work that happens afterward.

Desired workflow:

    Find interesting Reel
        ↓
    Send/share Reel to self
        ↓
    Forget about it
        ↓
    Open Chrome with Instagram already logged in
        ↓
    Run extractor from terminal
        ↓
    Select source Instagram account/identity
        ↓
    Agent locks the selected source
        ↓
    Continuous Reel discovery + processing
        ↓
    Transcript + OCR + visual understanding + metadata
        ↓
    AI analysis
        ↓
    If important uncertainty exists → ask user
        ↓
    User answers question/MCQ with Reel context
        ↓
    Processing resumes
        ↓
    Structured personal knowledge base
        ↓
    Search / browse / RAG chat
        ↓
    Detailed human-readable PDF + summaries + visualizations

## User Experience

### Startup

The user should be able to:

1. Open their normal Chrome browser.
2. Have Instagram already logged in through the browser session.
3. Open a recent Instagram tab/session.
4. Run the extractor from a terminal command.
5. See a clear UI showing that the agent has started.

The system must not require the user to type their Instagram password into the application.

### Source selection

At the beginning, ask for the username/identity of the Instagram account/conversation from which Reels should be extracted.

If found, lock that selection for the session.

If not found or ambiguous, ask the user. Do not silently choose another account.

### Live operation

The agent works continuously and exposes what it is doing through a clear UI.

The UI should make visible, where applicable:

- selected source
- current Reel
- Reel URL
- current processing stage
- progress counts
- completed/remaining work
- failures/retries
- questions requiring user input
- overall session state

The system should be resumable after interruption.

### Human-in-the-loop questions

The system must not invent answers to important unresolved questions.

If information needed for useful analysis is missing or materially ambiguous, the agent creates a question for the user.

Questions should be presented in a convenient queue. When appropriate, use MCQ/options rather than forcing the user to write a long answer.

Every question should include the relevant Reel URL and enough evidence/context for the user to answer intelligently.

After the user answers, the agent continues processing automatically.

User answers and corrections become part of the durable knowledge base.

## Primary User

One person: the owner of this project.

This is a personal tool, not a SaaS product.

## Core Value Proposition

The system saves the user from repeatedly opening Reels and manually taking notes.

The system should make this promise real:

**Capture once → understand automatically → clarify only when necessary → retrieve later without reopening everything.**

## Required Capabilities

### Instagram ingestion

Use an authenticated browser session.

The user logs into Instagram manually in Chrome.

The system then navigates accessible DMs and identifies Reel content.

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

Clearly distinguish facts, AI inferences, and user-provided information.

### Retrieval

Support:

- keyword search
- semantic search
- conversational/RAG search

The RAG layer should retrieve from the structured knowledge base. Users should not need to attach generated PDFs or manually export data to ask questions.

## Reporting & Outputs

After the extraction/processing run, generate useful artifacts from the actual archive.

The primary report should be a detailed, clear, human-readable PDF that is deliberately designed and specific to the user's data. It must avoid generic AI filler, repetitive boilerplate, and raw AI-chat formatting.

Useful outputs may include:

- executive summary
- collection statistics
- topic/category distributions
- important Reel rankings
- recurring themes
- tools/products/people/companies
- resources and URLs
- action items
- related-content clusters
- forgotten/unacted-on content
- unresolved items
- user corrections/answers where useful
- data visualizations
- other meaningful summaries

These are derived outputs. The structured knowledge base is the canonical memory and remains usable for later retrieval.

## Long-Term Vision

The Reel itself is not the ultimate value.

The valuable asset is the structured knowledge extracted from the Reel, the user's corrections and answers, and its relationship with everything else the user has saved.

Eventually the system should discover connections such as:

- multiple Reels about the same technology
- repeated interests
- related tools
- ideas that appeared repeatedly
- saved content that has not been acted upon
- older content relevant to a current question
- changes in the user's interests over time

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
- unnecessary enterprise/distributed infrastructure

## Success Criteria

The project succeeds when the user can:

1. Open Chrome with Instagram already authenticated.
2. Start the extractor from a terminal.
3. Select the Instagram source identity.
4. See the agent continuously discover and process Reels.
5. Obtain transcripts even when Instagram does not provide them.
6. See what the agent is doing through a clear UI.
7. Receive explicit questions instead of silent guesses when important information is uncertain.
8. Answer those questions/MCQs with Reel context and have processing resume.
9. Read useful structured knowledge instead of reopening every Reel.
10. Search for old Reels using keyword or semantic retrieval.
11. Ask questions about the collection through RAG.
12. Receive a high-quality human-readable PDF and useful summaries/visualizations.
13. Have the knowledge remain available without attaching those generated reports to future questions.

The most important metric is:

**How much time does this save the user compared with manually revisiting and taking notes on their Reels?**
