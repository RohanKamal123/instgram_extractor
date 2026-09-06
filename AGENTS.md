# Agent Context

## Role

You are the primary engineering agent for this project.

Build, maintain, test, and improve a personal AI system that automatically processes Instagram Reels from the user's accessible Instagram DMs and turns them into structured, searchable personal knowledge.

## User

The system is for one person only: the owner of this project.

Do not build multi-user SaaS functionality unless explicitly requested.

The user's primary workflow is:

1. Find an interesting Reel on Instagram.
2. Send/share it to their own Instagram account/self-DM.
3. Forget about it.
4. The system processes it automatically.
5. Later, the user can search, understand, and retrieve what they saved.

The fundamental problem is that manually opening each Reel and taking notes is too difficult and time-consuming.

## Instagram Access

The user will manually log into Instagram in the browser.

The agent may then operate the already-authenticated browser session.

Do not ask the user for their Instagram password.

Do not store Instagram credentials.

Use browser automation rather than depending on an Instagram API as the primary ingestion mechanism.

Playwright/Chromium is the preferred initial approach unless a better technical solution is demonstrated.

The system must not perform social actions such as:

- liking
- commenting
- following/unfollowing
- sending messages
- reacting to messages

The browser agent's job is primarily observation, extraction, and navigation.

## Content Scope

Primary source:

- Reels sent to the user's own Instagram account/self-DM.

Also support:

- Reels sent to other Instagram accounts/conversations accessible through the authenticated browser session.

The system should eventually be able to identify Reel messages regardless of which accessible DM conversation contains them.

## Transcription

A transcript is a first-class requirement.

Try extraction in this general order:

1. Existing Instagram-provided transcript/captions when accessible.
2. Embedded/generated subtitles when accessible.
3. Audio extraction.
4. Local Whisper transcription.

If no transcript exists, generate one.

Preserve timestamps when technically possible.

Record how the transcript was obtained and its confidence/quality where available.

Do not silently pretend an inferred transcript is an original transcript.

## Multimodal Extraction

A Reel may contain important information in:

- speech
- subtitles
- on-screen text
- captions
- visual content
- metadata

Therefore, the processing pipeline should eventually support:

- speech-to-text
- OCR
- caption extraction
- metadata extraction
- multimodal analysis

## AI Provider

DeepSeek API is available and should be supported as the primary LLM provider initially.

Design the AI layer so the provider/model can be changed without rewriting the application.

Small/local models should be preferred where they are sufficiently capable, especially for inexpensive preprocessing tasks.

Whisper may be run locally.

Do not send data to external AI providers unnecessarily.

## Reel Analysis

For every processed Reel, attempt to produce:

- title
- summary
- transcript
- key points
- topics
- categories
- why the user may have saved it
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

The AI must distinguish between facts extracted from the Reel and its own interpretation.

For "why saved", the AI should infer rather than claim certainty.

Example:

"Likely saved because this demonstrates an interesting autonomous coding workflow."

The user must be able to correct the inference.

## Knowledge Retrieval

The system should eventually support all of:

1. Keyword search
2. Semantic search
3. Conversational querying

Examples:

"Find Reels about local LLMs."

"Find the Reel I saved about an AI coding agent that tests its own code."

"What useful AI tools have I saved but never tried?"

"What topics do I repeatedly save?"

"Show me Reels related to autonomous software development."

## Data Principles

Never destroy the original extracted information when generating AI summaries.

Keep raw/archive data separate from the derived intelligence layer.

AI-generated analysis should be regenerable.

A model upgrade should not require re-ingesting Instagram content.

Avoid unnecessary duplication of downloaded media.

## Media Storage

Support three states:

1. Permanent storage
2. Temporary processing storage
3. Configurable preservation

Default behavior should avoid unnecessary permanent storage of large media.

The user should be able to preserve important Reels.

The original Reel URL should be retained whenever available.

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
- Make processing resumable.
- Do not process the same Reel repeatedly unless explicitly requested.
- Design long-running tasks to survive interruption.
- Log failures clearly.
- Never delete user data automatically.
- Never hard-code secrets.
- Use environment variables for API keys and sensitive configuration.

## Definition of Done

A feature is not complete merely because code exists.

It is complete when:

- implementation exists
- relevant tests pass
- failure cases are considered
- documentation is updated when necessary
- the application can actually use the feature
- existing functionality still works
