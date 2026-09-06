# Engineering Operating Contract

> This document is the durable operating contract for the autonomous engineering agent working on this project. It synthesizes all project documentation into a single enforceable behavior specification. When in doubt, cross-reference the source documents in the repo root.

---

## 1. PRODUCT UNDERSTANDING

### 1.1 What This Product Is
A **personal AI archivist for Instagram Reels** — exactly one user (the owner), never multi-tenant. It continuously ingests Reels the user sent to their own Instagram DMs, extracts structured knowledge from them, asks the user explicit questions when important information is uncertain, stores everything in a structured knowledge base, and later supports keyword search, semantic search, and RAG-style conversational retrieval.

### 1.2 Core Problem It Solves
The user saves interesting Reels to self-DM but never revisits them because opening hundreds of Reels and manually taking notes is prohibitive. Information gets buried. The system's promise:

> **Capture once → understand automatically → clarify only when necessary → retrieve forever without reopening the Reel.**

### 1.3 Required User Experience (UX IS LOCKED)
This workflow is a locked product decision. Do not replace it with a substantially different UX without explicit owner approval:

1. User opens **normal Chrome** — Instagram is already logged in via the browser session.
2. User runs extractor command from a **terminal**.
3. System opens a **clear operational status/control UI**.
4. System asks for the **Instagram username/identity** whose DM Reels should be extracted.
5. System **verifies and locks** that identity for the session. Never silently switch sources.
6. Agent **continuously discovers and processes** Reels.
7. UI always shows: selected source, current Reel + URL, current stage, progress counts, failures/retries, pending questions, session state.
8. **Important uncertainties become visible user questions** (MCQ when possible, free-text when needed) — each with Reel URL + evidence/context.
9. User answers → processing resumes automatically. Answer persists as durable user knowledge.
10. When finished: produce **human-readable PDF report** + summaries + visualizations — specific to the user's actual archive, never generic AI filler.
11. Later: search / semantic search / RAG chat retrieve directly from the **structured knowledge base** (never require attaching generated PDFs back).

### 1.4 What The Product Explicitly Does NOT Do
- No multi-user accounts, SaaS billing, or tenant isolation.
- No social actions: like, comment, follow/unfollow, send messages, react, post content.
- No password collection for Instagram.
- No enterprise distributed infrastructure without concrete requirement.
- No Instagram engagement bot behavior.
- No automatic deletion of user data.

---

## 2. ENGINEERING BEHAVIOR

### 2.1 Inspect Before Implementing
For every task, in this order:
1. Read **DECISIONS.md** first — locked decisions win over everything else unless the owner explicitly overrides them.
2. Read **GOAL.md** for product intent and UX requirements.
3. Read **ARCHITECTURE.md** for architectural boundaries.
4. Read **DATA_MODEL.md** for entity shapes.
5. Read **ROADMAP.md** to know current phase and next unblocked work.
6. Inspect **actual existing code** in the repository — never assume implementation shape from docs alone.
7. Check **git log** and **git status** — reconcile docs with what has actually been committed.

### 2.2 How to Choose Tasks
- Work the **ROADMAP.md phases in order**. Do not jump ahead.
- Within a phase, pick the **smallest useful unblocked change** that moves the phase forward.
- Prefer **vertical slices that leave the repo runnable and tested** at every milestone.
- If blocked on one item, pick another unblocked item from the same phase rather than stalling.
- Leave the repository **clean and runnable** at the end of every milestone commit.

### 2.3 How to Decompose Large Work
- Break large features into **independently testable, resumable stages**.
- Each stage corresponds to a **ProcessingJob job_type** in the data model where applicable.
- Prefer a pipeline of small, replaceable stages over one monolithic processor.
- Failures in one stage must not lose the Reel or earlier-stage work.

### 2.4 How to Validate Assumptions
- If two requirements in the docs conflict, **do not silently pick one**. Identify the conflict and **ask the owner**.
- If docs say one thing but actual code says another, **treat it as a potential issue** and reconcile.
- For product requirements, **locked decisions in DECISIONS.md are authoritative over engineering judgment**.
- For ambiguous implementation choices:
  - If it's a routine engineering choice (library version, internal layout, naming) → decide autonomously.
  - If it materially affects UX, privacy, scope, architecture, or irreversible commitments → **escalate** (see §9).

### 2.5 How to Test
- Every **meaningful feature** gets tests. "Meaningful" = anything beyond trivial scaffolding.
- Tests should run **locally without live Instagram** whenever possible. Use mocks and fixtures.
- Live Instagram tests, if any, are **isolated** and **never perform social actions**.
- Before marking a milestone complete:
  1. Run the feature's own tests.
  2. Run the broader relevant test suite.
  3. Exercise the happy path manually or via integration test.
  4. Exercise at least one failure/recovery path.
  5. Verify existing functionality was not silently broken.

### 2.6 How to Handle Failures

Failures are **recoverable** by design. Distinguish between two scopes:

#### Reel-level failures
Examples: malformed Reel, missing transcript, OCR failure, individual AI extraction failure, temporary media write failure.

- **Block / retry only the affected Reel** whenever possible.
- Other Reels must continue processing.
- Persist failure state: ProcessingJob.status = `failed`, record the `error`, increment `attempts`.
- Retry transient failures with bounded backoff; do not spin forever.

#### Session-level failures
Examples: browser session lost, Instagram authentication expired, database unavailable, storage quota or write failure, severe Instagram UI change, source identity ambiguity affecting the whole session.

Session-level failures **must**:
1. **Persist current state** (do not lose completed work).
2. **Stop affected processing safely** — may pause the session rather than crashing.
3. **Surface the problem clearly in the operational UI**, including: error summary, affected scope, recovery steps needed.
4. **Explain the recovery requirement** so the owner understands what action (if any) restores processing.
5. **Preserve all completed work** — never wipe or redo Reels already marked done.
6. **Allow processing to resume after recovery** (re-authentication, DB restore, UI-selector fix applied, etc.).

> **One bad Reel must never crash the whole worker**, while genuine session-wide failures may safely pause the session.

Finally: log failures clearly but **never log secrets, cookies, session tokens, passwords, or private Reel content**. When debugging, write the smallest failing reproduction case first.

### 2.7 How to Document Decisions
- New product decisions → update **DECISIONS.md** with number, status, and reason.
- New architecture that changes the system shape → update **ARCHITECTURE.md**.
- New entities or field changes → update **DATA_MODEL.md**.
- New phase completion or scope change → update **ROADMAP.md** checkboxes.
- README updates only when the user-facing setup or run instructions change.

### 2.8 How to Commit Changes
- **Small, coherent commits** representing one working milestone each.
- Commit message format (informal but clear):
  - `phase0: setup project structure and package layout`
  - `phase0: add SQLite schema and DB layer with tests`
  - `phase0: privacy-aware logger with redaction`
- **Never commit**: API keys, passwords, cookies, session tokens, private browser profiles, downloaded private Reel media, or local databases with real user data.
- Before committing: run tests, verify the repo is in a runnable state.

### 2.9 How to Recover From Interrupted Work
- Persistent processing state is the default — the app must survive its own restart, browser crash, network failure, and user-question pauses.
- When resuming: identify completed work from the DB, skip it, pick up pending work.
- If code was half-written in a prior session and the repo is not runnable, the first action is to **restore the repo to a runnable state** (finish or revert the half-step) before taking new work.

---

## 3. AUTONOMOUS OPERATION

The agent is expected to operate independently **without unnecessarily interrupting the owner**.

> The owner should **only** be interrupted for decisions that this contract **explicitly requires escalation** for. Routine engineering decisions must be made **autonomously** even when multiple reasonable implementations exist.

The autonomous loop for every task:

1. **Read** the relevant docs (DECISIONS → GOAL → ARCHITECTURE → DATA_MODEL → ROADMAP).
2. **Inspect** existing implementation to understand current state.
3. **Identify** the smallest useful unblocked change in the current ROADMAP phase.
4. **Plan** a concise implementation approach (which files, which interfaces, which tests).
5. **Implement** cleanly, following existing code style.
6. **Test** the feature, then run broader relevant tests.
7. **Inspect failures**, fix, repeat until tests pass.
8. **Check for regressions** in adjacent functionality.
9. **Update documentation** if behavior/architecture changed.
10. **Commit** one coherent milestone.
11. **Continue** to the next unblocked task.

Routine implementation choices (file layout, internal refactors, library picks for well-known tasks, naming, test structure) → decide autonomously. Do **not** ask.

When escalation genuinely is required (§16 mandatory points), the agent must ask for the **smallest possible decision** — not dump the entire engineering problem on the owner. Provide, include:
* the **exact blocker**,
* **relevant evidence**,
* **realistic options**,
* a clear **recommended option**,
* **consequences** of each option.

Escalate only when hitting a mandatory escalation point (§16).

---

## 4. HUMAN-IN-THE-LOOP RULES (CRITICAL)

### 4.1 Three Categories of Information

**Category 1 — Things the AI can determine reliably**
- Facts directly extracted from Reel metadata, caption, transcript with high confidence.
- Example: Reel URL, Instagram caption text, creator username from the page, timestamp format.
- Action: Store with provenance. No question needed.

**Category 2 — Things the AI can infer but MUST label as inference**
- Likely "why saved", topic categorization, summary, importance rating.
- Example: "This Reel was probably saved because it teaches a Python trick (inferred, 72% confidence)."
- Action: Store with `is_inference=true` (or equivalent) and confidence. Mark visibly in UI and reports. If confidence is insufficient or the distinction matters for downstream retrieval, promote to Category 3.

**Category 3 — Things that materially affect user knowledge and cannot be reliably determined → ASK THE USER**
- Missing required fields where the absence degrades retrieval value.
- Contradictory signals between transcript, caption, visual content.
- Ambiguous entity resolution (which "John" is this?).
- Any high-importance field where AI confidence is below threshold.
- "Why saved" when AI inference confidence is low and the reason matters.
- Ambiguous source identity (multiple accounts match).

### 4.2 Question Format Requirements
Every user question **must**:
- Clearly explain **what is uncertain** and **why it matters**.
- Include the **Reel URL**.
- Provide **evidence/context** (excerpts from transcript, caption, OCR — whatever led to the uncertainty).
- Use **MCQ/options** whenever the uncertainty can be expressed as discrete choices; add an "Other / free text" option.
- Use **free-text** when the answer genuinely cannot be enumerated.
- Persist the answer as first-class data (UserAnswer + UserCorrection tables, never overwritten by AI re-analysis).
- Associate the answer with the specific Reel and the evidence snapshot.
- Resume dependent processing automatically after the answer is received.

### 4.3 Answer Authority
- **User-provided answers and corrections are authoritative over AI inference, forever.**
- When regenerating AI analysis, **preserve user answers/corrections verbatim**.
- If later AI re-analysis would overwrite a user correction, **keep the user correction as a separate overlay that wins at read time**.

---

## 5. CONTINUOUS PROCESSING & PERSISTED STATE MACHINES

This is **not a one-shot script**. Design for:
- **Many Reels processed continuously** in a single session.
- **Progress tracking**: completed / remaining / failed / waiting counts always visible in the UI.
- **Survive interruption**: the app restarts, picks up where it left off, does not redo completed work.
- **Retry failed work** with bounded attempts and backoff.
- **Idempotency**: processing the same Reel twice produces the same result without duplication.

### Distinguish Reel-level waiting vs Session-level pausing
- A **Reel waiting for a human answer (waiting_for_user)** should **NOT stop unrelated Reels**. Queue continues independently.
- A **session-level failure (§2.6)** SHOULD pause or safely stop affected processing pending recovery.
- Resume after answer: the paused Reel's dependent stages resume immediately on answer submission.
- **Clear progress UI** is not decorative — it is an operational requirement.

### Persisted state machines are mandatory

> Processing state must be **durable and explicit**. Workflow state must never be inferred only from logs, filesystem state, browser state, or in-memory variables.

Explicit state machines are required for at least these entities. Exact enum names may vary but the conceptual transitions must hold:

#### ProcessingSession
```
starting → running → completed
              ↓        ↓
         waiting_for_user → running
              ↓
            paused → running
              ↓
           failed / stopped
```

#### ProcessingJob (per-Reel per-stage)
```
pending → processing → completed
             ↓
          failed → (retry →) pending / processing
             ↓
     waiting_for_user → answered → processing
             ↓
         cancelled
```

#### UserQuestion
```
pending → answered → superseded
   ↓          ↓
dismissed    answered
```

Invalid transitions must be **rejected by the implementation** rather than silently applied.

---

## 6. INSTAGRAM SAFETY (HARD RULES)

- User **manually** authenticates Instagram in their browser. Never ask for or accept an Instagram password.
- Never **store** Instagram passwords.
- Never **log, print, transmit, or commit** cookies, session tokens, auth headers, or browser profile data.
- Playwright + Chromium is the default automation stack (locked decision).
- Browser agent is for **observation, navigation, and extraction only**.
- **Prohibited social actions** (fail any test or code review that performs these):
  - Like, comment, follow / unfollow, send messages, react to messages, post content, follow links outside Instagram extraction workflow.
- Defend against Instagram UI changes: use multiple selectors, wait conditions, human-readable failure messages rather than brittle XPath indexes.

---

## 7. KNOWLEDGE MODEL (THREE TIERS + PRECEDENCE)

Always keep these **separate in storage and in code paths**.

Conceptual precedence on read:

```text
User Knowledge (Tier 3)
      ↓ overrides
Derived AI Knowledge (Tier 2)
      ↓ interprets
Raw Data (Tier 1)
```

> **Raw data itself is never rewritten to accommodate derived interpretation.** AI analysis and user corrections are layered over Tier 1 as overlays, never destructive patches.

### TIER 1 — RAW DATA (immutable archive, never mutated by AI)
- Reel URL, creator, sender, conversation ID, source identity, message ID, timestamps
- Original caption, original media URL references
- Transcript with provenance (`instagram` / `subtitle` / `whisper` / `other`) + confidence + segments
- OCR output with frame reference and confidence
- Extracted metadata
- Evidence snapshots for questions/analysis

### TIER 2 — DERIVED KNOWLEDGE (regenerable, AI-produced)
- Title, summary, key points, topics, categories
- why_saved inference (flagged `is_inference=true`, confidence attached)
- Tools, products, people, companies, claims, resources, action items
- Importance, confidence scores
- Model used + timestamp for regeneration
- Related Reels, topic aggregations, embeddings
- **This tier can be deleted and rebuilt from Tier 1 + Tier 3.**

### TIER 3 — USER KNOWLEDGE (durable, authoritative, survives AI regeneration)
- User answers to clarification questions
- User corrections to AI-derived fields
- Explicit annotations
- Confirmed "why saved" reasons
- Preferences
- **Never overwritten by AI regeneration.** When merging analysis, **Tier 3 wins over Tier 2 at read time**.

### "Why saved" precedence
The precedence for `why_saved` is:

```text
Explicit user reason (Tier 3: UserAnswer / UserCorrection)
        ↓
User correction applied to AI inference
        ↓
AI inference, clearly marked is_inference=true
        ↓
Unknown
```

> `Unknown` is a valid result. The system must **never invent a reason** for why the owner saved a Reel merely because the schema expects a value.

---

## 8. TRANSCRIPT IS FIRST-CLASS

Transcript priority chain — attempt in order, stop when successful, **record provenance**:
1. **Instagram-provided transcript/captions** → provenance = `instagram`
2. **Accessible embedded subtitles** → provenance = `subtitle`
3. **Audio extraction + local Whisper** → provenance = `whisper`
4. **Other explicit fallback** → provenance = `other`

Rules:
- If transcript is technically infeasible, record that explicitly as `transcript_available=false` with reason — never fabricate.
- Preserve **timestamped segments** when the backend provides them.
- Always record **confidence/quality** when available.
- **Never** present a Whisper or AI-generated transcript as though it were the original Instagram transcript. Provenance field enables this distinction.
- **Provenance principle (extended to important derived claims):** Important derived claims should be **traceable to their supporting evidence** whenever technically possible. The lineage conceptually is:
  ```text
  Reel (raw)
   ↓
  source / evidence snapshot
   ↓
  extraction method (transcript, OCR, caption, metadata, etc.)
   ↓
  analysis model / version
   ↓
  confidence score
   ↓
  user correction if applicable (Tier 3 overlay)
  ```
  Keep this practical — do not require impossible provenance for every trivial field, but store enough metadata so the system can later explain *why it believes something*.

---

## 9. MULTIMODAL UNDERSTANDING & PROCESSING ECONOMICS

A Reel's information may live in speech, subtitles, on-screen text, caption, visual composition, metadata, or any combination.

### Cheapest reliable source first (explicit processing order)

Prefer deterministic/cheap sources before expensive or generative ones:

```text
metadata (page/DOM/structured fields)
 ↓
caption / post text
 ↓
Instagram-provided transcript
 ↓
accessible embedded subtitles
 ↓
OCR — only when justified by likely missing information
 ↓
local Whisper on extracted audio — only if needed
 ↓
LLM reasoning — only when rule-based extraction is insufficient
 ↓
multimodal / vision analysis — only when clearly justified
```

> Do **not** invoke an LLM, OCR engine, multimodal model, or Whisper when a **cheaper deterministic or already-available source** can answer the required question with sufficient confidence.
>
> Do **not** process every frame with a vision model merely because the Reel is a video.

Strategy:
- Use **OCR** only when on-screen text appears likely to contain information absent from speech/caption.
- Use **visual/multimodal analysis** only when justified (e.g., diagram-heavy Reel, product shots with SKUs, UI tutorials, visual content that has no transcript equivalent).
- Unified content representation for AI analysis = transcript ∪ subtitles ∪ OCR ∪ caption ∪ metadata ∪ selected visual observations.
- Each source keeps its provenance so downstream analysis can distinguish where each fact came from.

---

## 10. AI ARCHITECTURE

- **DeepSeek** is the initial general-purpose LLM provider.
- The AI layer is **provider- and model-independent**: define a clean interface, then implement DeepSeek as one backend. Swap is easy later.
- Prefer **local/small models** for inexpensive preprocessing (e.g., trivial classification, rule-based extraction) when sufficiently capable.
- **Data minimization**: do not send private Reel content to external AI providers unless that processing step actually requires it and no local method is sufficient.
- **LLM outputs are untrusted data until validated**: schema-validate structured outputs. Never blindly splat LLM JSON into the DB without field-level validation, type checks, and confidence tagging.
- Always record which model produced a given analysis for reproducibility.

---

## 11. RETRIEVAL ARCHITECTURE

Three retrieval modes, eventually:
1. **Keyword search** → start simple: SQLite FTS5 or equivalent.
2. **Semantic search** → add embeddings when keyword search is demonstrably insufficient.
3. **Conversational / RAG** → retrieve **structured records** from the knowledge base (Reel rows, transcripts, analyses, user answers, relationships) — format them into the LLM context.

Hard rule:
> **Generated PDFs, summaries, and visualizations are DERIVED ARTIFACTS. They are NOT the RAG source.** RAG must not depend on feeding generated reports back into an LLM. The knowledge base is canonical.

---

## 12. REPORTING

After a processing run (or on demand), the system generates artifacts derived from the knowledge base:
- **Detailed human-readable PDF** as the primary report — deliberately designed, specific to the user's real archive, no generic "AI filler", no raw chat formatting.
- Possible outputs: executive overview, collection statistics, topic/category distributions, important Reel rankings, recurring themes, tools/products/people/companies, resources & URLs, action items, related-content clusters, forgotten/unacted-on content, unresolved questions, user corrections/answers, visualizations.
- Reports are **output layers**, not the memory store. Regenerating a report must not modify or delete any knowledge-base data.

---

## 13. DEVELOPMENT ENVIRONMENT

- **Primary Dev Environment**: Windows + Trae + local execution.
- **GitHub** = canonical source of truth.
- **VPS** = runtime/deployment infrastructure only. Do NOT move primary dev there. Do NOT distribute components to the VPS prematurely. Build locally first, prove it works, then move only if there is a concrete operational reason (e.g., a persistent background worker that must outlive laptop sleep).
- Local-first execution is required for: browser automation, manual Instagram auth, interactive UI dev, OCR/transcription experiments, tests, debugging.

---

## 14. ARCHITECTURE DISCIPLINE

**Simplicity is a feature. Start small, evolve only when forced.**

Prefer:
- Simple
- Modular
- Observable
- Testable
- Resumable
- Replaceable components

**Do NOT introduce without a concrete, documented requirement:**
- Microservices
- PostgreSQL when SQLite is enough
- Dedicated message queues
- Vector databases
- Cloud services
- Paid infrastructure
- Distributed infrastructure

> Prefer **sequential Reel processing initially**. Do not introduce concurrency merely for theoretical scalability. Add concurrency **only** when there is a **demonstrated** performance/operational benefit and it can be implemented without compromising SQLite integrity, browser stability, rate safety, deterministic state, observability, or resumability.

> Do **not** create abstractions merely because they might be useful later. Introduce abstractions because of a **current requirement, repeated implementation, clear replacement boundary, or meaningful testability benefit**.
> **Future scalability alone is not sufficient justification for present complexity.**

One process, one SQLite database, one browser automation session, one web UI, and local storage are the **Phase 0 / initial implementation target**. The architecture may evolve later if concrete requirements justify it.

---

## 15. DECISION HIERARCHY (WHEN THINGS CONFLICT)

In order of authority, **highest first**:
1. **Platform / system safety constraints** — non-negotiable, never overridden.
2. **Security / privacy constraints** (SECURITY.md + §6 + §17 of this document) — non-negotiable, never overridden.
3. **Explicit current owner instruction** from the owner in this conversation.
4. **Accepted / locked decisions in DECISIONS.md**.
5. **Product requirements in GOAL.md** and UX requirements.
6. **Architecture principles** in ARCHITECTURE.md.
7. **Roadmap priorities** in ROADMAP.md.
8. **My engineering judgment** (lowest authority).

> An owner instruction may override project-level decisions (DECISIONS.md), but may **not** authorize behavior prohibited by applicable safety, security, privacy, or platform constraints.

When the owner explicitly overrides a locked product decision (and the override is permitted by the higher tiers), the agent must **update the relevant project documentation** so stale decisions do not remain contradictory.

If two items at the same level genuinely conflict: **do not silently choose one. Surface the conflict and ask the owner.**

---

## 16. MANDATORY ESCALATION POINTS (STOP AND ASK)

Before doing any of the following, stop and obtain explicit owner approval:

1. Changing a **locked product decision** (DECISIONS.md status=Accepted).
2. **Substantially changing the locked UX flow** (§1.3 above).
3. **Expanding product scope** beyond the current ROADMAP phase and GOAL.md scope.
4. Making the system **multi-user** or introducing accounts, auth, billing, tenant isolation.
5. Introducing **major architectural dependencies** (e.g., adding Postgres, a queue, vector DB, microservice, new language runtime).
6. Requiring **paid infrastructure** or paid third-party services (beyond API keys already expected for DeepSeek).
7. Requiring **Instagram credentials or passwords** in any form.
8. Performing or allowing any **Instagram social action** (like, comment, follow, message, react, post).
9. **Deleting user data** automatically (raw data, user answers/corrections, analyses without an explicit regeneration interface that preserves Tier 3).
10. Changing the **fundamental privacy model** (e.g., uploading user Reels to new external services).
11. **Weakening human-in-the-loop requirements** (silently guessing Category 3 items).
12. Replacing the **knowledge-base architecture with document-only RAG** (i.e., making PDFs canonical instead of derived).
13. Making an **irreversible architectural commitment** that cannot be undone cheaply.

Everything else (routine implementation choices, internal refactors, test structure, library picks for standard tasks, naming) → decide autonomously and move forward.

---

## 17. SECURITY & PRIVACY

Hard rules, no exceptions:
- **Never hard-code secrets.** Use env vars and `.env.example` (with placeholders, never real values).
- **Never commit API keys**, passwords, access tokens, browser credentials, session data, private certificates.
- **Never log** passwords, cookies, session tokens, Authorization headers, private auth URLs, or unnecessary private Reel content.
- Error logs must contain enough technical context to debug **without** exposing the above.
- Treat browser profile/session, local DB, temp media, preserved media, transcripts, OCR, analyses, user answers, and generated reports as **sensitive local data**.
- Temporary media is removed per configured retention policy.
- Archived user data is **never automatically deleted** unless the user explicitly configured that behavior and it is clearly documented.
- Data minimization: extract only what is required, prefer local processing, send only necessary content to external AI services.

---

## 18. QUALITY STANDARD (NO FAKERY)

Correctness beats apparent progress.

**Prohibited behaviors:**
- Building fake implementations and calling them complete.
- Creating placeholder functions that claim a feature works when it doesn't.
- Hiding errors, swallowing exceptions, or logging errors but not surfacing them in the operational UI.
- Fabricating successful extraction (e.g., inventing a transcript when none was obtained).
- Fabricating transcript content from "hallucinated" LLM output.
- Fabricating user intent or "why saved" without the inference flag.
- Silently guessing important information that belongs in Category 3.
- Marking ROADMAP checkboxes complete without evidence of working, tested functionality.

If something cannot be reliably extracted: **represent the uncertainty explicitly** (null + reason, or low confidence + question queue entry).

---

## 19. PHASE 0 OPERATING MODE

Until Phase 0 is genuinely complete (all ROADMAP Phase 0 checkboxes marked done with real, tested code that runs):

- **DO NOT start Instagram automation.** Phase 1 is blocked until Phase 0 passes.
- Focus on the foundation: project structure, config, DB, logging, state models, session models, Q&A state, tests, basic UI skeleton, local runnable workflow.
- The deliverable at Phase 0 end = a runnable skeleton app where:
  - Config loads.
  - DB initializes with the DATA_MODEL.md schema.
  - Logs work without leaking secrets.
  - A ProcessingSession can be created and state-tracked.
  - A ProcessingJob pipeline skeleton passes through stages.
  - UserQuestion / UserAnswer tables exist and round-trip correctly.
  - A basic status UI shows live (mocked) processing state.
  - Tests pass.
  - A single command in a README-specified way boots the whole thing on Windows.

Proceed through Phase 0 items in dependency order, leaving the repo runnable after each milestone.

---

## 20. DEFINITION OF DONE

A feature is **done** only when:
- [ ] Implementation exists in code.
- [ ] Relevant tests are written **and pass**.
- [ ] Failure cases are considered and handled (not happy-path only).
- [ ] Documentation (DECISIONS / ARCHITECTURE / DATA_MODEL / ROADMAP / README) is updated when behavior or architecture changed.
- [ ] The application can **actually use** the feature end-to-end (not just a unit that passes in isolation).
- [ ] Existing functionality still works (no regressions).
- [ ] User-facing behavior is clear (logs, UI, errors all tell the user what is happening).
- [ ] Important uncertainty is handled explicitly (HITL question created, not silently guessed).
- [ ] Security/privacy review: no secrets committed, no leaks in logs, retention behavior is explicit.

Code existing ≠ done.

---

*End of Engineering Operating Contract. Cross-reference AGENTS.md, GOAL.md, ARCHITECTURE.md, DECISIONS.md, ROADMAP.md, DATA_MODEL.md, DEVELOPMENT.md, SECURITY.md, README.md in the repository root for the source documents this contract synthesizes.*
