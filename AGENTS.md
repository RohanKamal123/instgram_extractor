# Agent Context

## Role

You are the primary engineering agent for this project.

Build, maintain, test, and improve a personal AI system that automatically processes Instagram Reels from the user's accessible Instagram DMs and turns them into structured, searchable personal knowledge.

## Product Scope

This is a personal-only system for one owner. Do not build multi-user SaaS functionality unless explicitly requested.

The core workflow is:

1. The user normally uses Instagram and sends interesting Reels to their own Instagram account/self-DM.
2. The user opens their normal Chrome/Instagram session and starts the extractor from a terminal.
3. The system asks which Instagram account/identity should be used as the Reel source.
4. It finds and locks onto that account/conversation when found.
5. The agent continuously discovers and processes relevant Reels.
6. The user sees clear live progress and what the agent is doing.
7. When important information is missing or ambiguous and cannot be reliably determined, the system asks the user instead of guessing.
8. Questions appear in a clear human-in-the-loop queue, preferably as MCQ when appropriate, with the relevant Reel URL and evidence/context.
9. After the user answers, processing resumes automatically.
10. When extraction is complete, the system generates a detailed, human-readable report PDF plus useful summaries and visualizations.
11. The structured knowledge base remains the source for later search and RAG-based conversational retrieval; reports are output artifacts, not the primary memory store.

The fundamental problem is that manually reopening each Reel and taking notes is difficult and time-consuming.

## Development Environment

The primary development environment is Windows.

The primary coding agent is Trae.

GitHub is the canonical source of truth for the source repository.

The VPS is runtime/deployment infrastructure, not the primary development workstation.

Local development should be preferred when it is sufficient, especially for browser automation, manual Instagram authentication, UI development, and tests.

See DEVELOPMENT.md for the detailed environment model.

## Instagram Access

The user manually logs into Instagram in their normal Chrome browser/session before starting the extractor.

The system may operate the already-authenticated browser session/profile.

Never ask the user for or store their Instagram password.

Do not expose browser cookies, session tokens, or authentication state in logs, UI, commits, or reports.

Use browser automation rather than depending on an Instagram API as the primary ingestion mechanism.

Playwright/Chromium is the preferred automation technology unless a better solution is demonstrated.

The browser agent is for observation, navigation, and extraction only. It must not perform social actions such as:

- liking
- commenting
- following/unfollowing
- sending messages
- reacting to messages
- posting content

## Source Account Selection

At the beginning of an ingestion session, the system should ask the user for the Instagram username/identity from which Reels should be extracted.

The system must verify that the requested identity/conversation is found before proceeding.

Once found, the selected source should be locked for that processing session so the agent does not silently switch to another identity.

If the account cannot be found or the identity is ambiguous, ask the user rather than guessing.

Primary source:

- Reels sent to the user's own Instagram account/self-DM.

Also support:

- Reels sent to other Instagram accounts/conversations accessible through the authenticated browser session.

## Continuous Processing

The extractor is a long-running, resumable worker rather than a one-shot script.

Processing must persist state so interruption, restart, or browser failure does not cause completed Reels to be lost or unnecessarily reprocessed.

The UI must make the current state visible, including at minimum:

- current session
- selected account/conversation
- current Reel
- current processing stage
- completed/remaining counts when known
- failures/retries
- questions waiting for the user

The system should pause only the work that genuinely requires user input and resume after an answer whenever possible.

## Human-in-the-Loop / Uncertainty

This is a critical product principle:

**AI may propose; it must not silently guess when an important answer is uncertain.**

If required information is missing, contradictory, or materially ambiguous, create a user question rather than inventing an answer.

Questions should:

- explain what is uncertain
- show the relevant Reel URL
- provide useful evidence/context
- use MCQ/options when the ambiguity can be expressed as discrete choices
- allow a free-text/other response when appropriate
- record the user's answer as durable knowledge
- resume processing after the answer

Distinguish clearly between:

- information extracted from the Reel
- AI interpretation/inference
- information supplied or corrected by the user

For "why saved", the AI should infer a likely reason but label it as an inference. If confidence is insufficient or the distinction matters, ask the user. User corrections take precedence over AI inference for future retrieval/reporting while preserving the original inference.

## Transcription

A transcript is a first-class requirement.

Try extraction in this general order:

1. Existing Instagram-provided transcript/captions when accessible.
2. Embedded/generated subtitles when accessible.
3. Audio extraction.
4. Local Whisper transcription.

If no transcript exists, generate one whenever technically possible.

Preserve timestamps when technically possible.

Record how the transcript was obtained and confidence/quality where available.

Never silently present an inferred/generated transcript as an original Instagram transcript.

## Multimodal Extraction

A Reel may contain important information in:

- speech
- subtitles
- on-screen text
- captions
- visual content
- metadata

The pipeline should support:

- speech-to-text
- OCR
- caption extraction
- metadata extraction
- visual/multimodal analysis

## AI Provider

DeepSeek API is available and should be supported as the initial general-purpose LLM provider.

The AI layer must be provider/model independent so providers can be changed without rewriting the application.

Small/local models should be preferred where sufficiently capable, especially for inexpensive preprocessing tasks.

Whisper may run locally.

Do not send private Reel content to external AI providers unnecessarily.

## Reel Analysis

For every processed Reel, attempt to produce:

- title
- summary
- transcript reference
- key points
- topics
- categories
- likely reason saved
- tools mentioned
- products mentioned
- people mentioned
- companies mentioned
- claims
- resources/URLs
- action items
- importance
- confidence
- related concepts
- related Reels

The AI must distinguish extracted facts from interpretation.

## Retrieval

The knowledge base should eventually support all of:

1. Keyword search
2. Semantic search
3. Conversational/RAG querying

The conversational layer should retrieve structured source records from the knowledge base rather than requiring the user to attach PDFs or manually provide exported data.

## Reporting

After extraction, generate a detailed human-readable report that is specific to the user's actual archive, not generic AI filler.

The report should be designed as a proper document and may include:

- executive overview
- collection statistics
- topic/category distributions
- important Reels
- recurring themes
- tools/products/people/companies
- resources and URLs
- action items
- relationships and clusters
- forgotten or unresolved content
- user-provided answers/corrections where useful
- data visualizations

PDF generation is an output layer. The knowledge base remains the canonical structured memory.

## Data Principles

Never destroy original extracted information when generating AI summaries.

Keep raw/archive data separate from derived intelligence.

AI-generated analysis should be regenerable.

A model upgrade should not require re-ingesting Instagram content.

User answers/corrections are first-class data and must not be overwritten by regeneration.

Avoid unnecessary duplication of downloaded media.

## Media Storage

Support three states:

1. Permanent storage
2. Temporary processing storage
3. Configurable preservation

Default behavior should avoid unnecessary permanent storage of large media.

The user should be able to preserve important Reels.

Retain the original Reel URL whenever available.

## Engineering Principles

- Inspect the existing project before changing it.
- Prefer simple solutions.
- Avoid premature abstractions.
- Keep components independently testable.
- Write tests for meaningful functionality.
- Do not silently break existing functionality.
- Keep documentation synchronized with architectural changes.
- Never mark functionality complete without testing it.
- Handle Instagram UI changes defensively.
- Make processing resumable and idempotent.
- Do not process the same Reel repeatedly unless explicitly requested.
- Design long-running tasks to survive interruption.
- Log failures clearly without logging secrets or private authentication state.
- Never delete user data automatically.
- Never hard-code secrets.
- Use environment variables for API keys and sensitive configuration.
- Do not introduce distributed infrastructure merely because it is fashionable.
- Do not ask the user for routine engineering decisions.
- Do ask the user when a product requirement, important ambiguity, privacy/security boundary, or other explicitly protected decision requires human judgment.

## Definition of Done

A feature is not complete merely because code exists.

It is complete when:

- implementation exists
- relevant tests pass
- failure cases are considered
- documentation is updated when necessary
- the application can actually use the feature
- existing functionality still works
- user-facing behavior is clear
- important uncertainty is handled explicitly rather than silently guessed
