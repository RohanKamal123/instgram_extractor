# Architecture & Product Decisions

## D001 — Personal-only system

Status: Accepted

The initial product is for a single user.

Reason:

The problem is personal information overload, not multi-user collaboration.

Avoid authentication, billing, tenant isolation, and SaaS infrastructure unless needed later.

---

## D002 — Browser automation over Instagram API

Status: Accepted

Use an authenticated browser session.

Reason:

The required information exists inside the user's normal Instagram experience, particularly DMs containing shared Reels.

The user manually logs in.

The automation operates the authenticated session.

Preferred technology: Playwright + Chromium.

---

## D003 — User manually authenticates

Status: Accepted

The application must not collect or store the user's Instagram password.

The user logs into Instagram manually in their normal Chrome/appropriate persistent browser session.

Authentication state must never be logged or committed.

---

## D004 — Self-DM is the primary source

Status: Accepted

The main workflow is Reels sent to the user's own account.

The system should also support Reels sent to other accessible DM conversations.

---

## D005 — Source identity is explicitly selected and locked

Status: Accepted

At the beginning of a processing session, ask the user for the Instagram username/identity from which Reels should be extracted.

The system must verify the identity and lock the selected source for that session.

If the identity is missing or ambiguous, ask the user instead of guessing.

---

## D006 — Transcript is first-class data

Status: Accepted

Transcript generation is not optional when technically possible.

Fallback:

Instagram transcript/captions → subtitles → audio → Whisper.

Timestamped segments should be retained when possible.

---

## D007 — Multimodal processing

Status: Accepted

Speech alone is insufficient.

The system should combine, when useful:

- audio/transcript
- captions/subtitles
- OCR
- visual information
- metadata

---

## D008 — DeepSeek initially

Status: Accepted

DeepSeek API is available and should be the initial general-purpose LLM provider.

The AI layer must remain provider-independent.

---

## D009 — Local Whisper

Status: Accepted

Speech transcription can run locally.

This reduces API costs and keeps processing under the user's control.

---

## D010 — Preserve raw data separately

Status: Accepted

Original extracted information must remain separate from AI-generated analysis.

AI analysis can be regenerated.

User answers and corrections must remain durable across analysis regeneration.

---

## D011 — Configurable media retention

Status: Accepted

Media retention should be configurable.

Temporary processing is preferable for large files unless the user chooses to preserve a Reel.

---

## D012 — Three retrieval modes

Status: Accepted

The system should eventually provide:

- keyword search
- semantic search
- conversational/RAG querying

RAG retrieves from the structured knowledge base; users do not need to attach generated PDFs or export data manually.

---

## D013 — AI-inferred "why saved"

Status: Accepted

The system cannot know the user's actual reason for saving a Reel unless the user states it.

Therefore, it should infer a likely reason and clearly label it as an inference.

The user should be able to correct it.

If the distinction is important and confidence is insufficient, ask the user.

---

## D014 — Human-in-the-loop for important uncertainty

Status: Accepted

The system must not silently guess when important information is missing, contradictory, or materially ambiguous.

Create a user question instead.

Questions should include the relevant Reel URL and evidence/context. MCQ/options should be preferred when appropriate to minimize user effort.

User answers are first-class durable knowledge.

---

## D015 — Continuous resumable processing

Status: Accepted

The extractor is a continuous worker, not merely a one-shot script.

It must persist processing state, support retries, avoid unnecessary duplicate processing, survive interruption, and resume after user answers.

---

## D016 — Live operational UI

Status: Accepted

The user must have a clear UI showing what the agent is doing, including selected source, current Reel, current stage, progress, failures, and pending questions.

The UI should make waiting states understandable.

---

## D017 — Reports are outputs, not memory

Status: Accepted

After extraction, the system should generate a detailed human-readable PDF and useful summaries/visualizations based on the actual archive.

The report must avoid generic AI filler and should be deliberately designed for human reading.

The knowledge base remains the canonical source for future search and RAG.

---

## D018 — Windows + Trae as primary development environment

Status: Accepted

The project is primarily developed on Windows using Trae as the coding agent.

GitHub is the canonical source repository.

The VPS is runtime/deployment infrastructure, not the primary development workstation.

Local development is preferred where practical, especially for browser automation and interactive authentication.

---

## D019 — No social actions

Status: Accepted

The browser agent is an observation/extraction system.

It must not like, comment, follow/unfollow, message, react, post, or otherwise engage socially on the user's behalf.
