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

The user logs into Instagram manually in the browser profile used by the agent.

---

## D004 — Self-DM is the primary source

Status: Accepted

The main workflow is Reels sent to the user's own account.

The system should also support Reels sent to other accessible DM conversations.

---

## D005 — Transcript is first-class data

Status: Accepted

Transcript generation is not optional when technically possible.

Fallback:

Instagram transcript/captions → subtitles → audio → Whisper.

Timestamped segments should be retained when possible.

---

## D006 — Multimodal processing

Status: Accepted

Speech alone is insufficient.

The system should eventually combine:

- audio/transcript
- captions
- OCR
- visual information
- metadata

---

## D007 — DeepSeek initially

Status: Accepted

DeepSeek API is available and should be the initial general-purpose LLM provider.

The AI layer must remain provider-independent.

---

## D008 — Local Whisper

Status: Accepted

Speech transcription can run locally.

This reduces API costs and keeps processing under the user's control.

---

## D009 — Preserve raw data separately

Status: Accepted

Original extracted information must remain separate from AI-generated analysis.

AI analysis can be regenerated.

---

## D010 — Configurable media retention

Status: Accepted

Media retention should be configurable.

Temporary processing is preferable for large files unless the user chooses to preserve a Reel.

---

## D011 — Three retrieval modes

Status: Accepted

The system should eventually provide:

- keyword search
- semantic search
- conversational querying

---

## D012 — AI-inferred "why saved"

Status: Accepted

The system cannot know the user's actual reason for saving a Reel.

Therefore, it should infer a likely reason and clearly label it as an inference.

The user should be able to correct it.
