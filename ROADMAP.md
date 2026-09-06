# Roadmap

## Phase 0 — Project Foundation & Local UX

- [ ] Establish project structure
- [ ] Configuration management
- [ ] Local database
- [ ] Logging with privacy safeguards
- [ ] Basic interactive web/status interface
- [ ] Processing state model
- [ ] Persistent session model
- [ ] Basic question/answer state model
- [ ] Tests
- [ ] Local runnable developer workflow on Windows

## Phase 1 — Instagram Browser Ingestion

- [ ] Persistent Chrome/Chromium browser profile/session strategy
- [ ] Manual Instagram login flow
- [ ] Detect authenticated session
- [ ] Ask for source Instagram username/identity
- [ ] Verify source identity
- [ ] Lock selected source for the session
- [ ] Navigate Instagram DMs
- [ ] Identify Reel messages
- [ ] Extract Reel URLs
- [ ] Extract captions
- [ ] Extract creator information
- [ ] Extract timestamps where available
- [ ] Track processed Reel IDs/messages
- [ ] Make ingestion resumable and idempotent
- [ ] Live ingestion progress UI

## Phase 2 — Media & Transcript

- [ ] Retrieve Reel media where technically possible
- [ ] Temporary media storage
- [ ] Configurable media preservation
- [ ] Audio extraction
- [ ] Transcript detection
- [ ] Subtitle extraction
- [ ] Local Whisper fallback
- [ ] Timestamped transcript
- [ ] Transcript provenance
- [ ] Failed-processing recovery

## Phase 3 — Content Understanding

- [ ] LLM abstraction
- [ ] DeepSeek integration
- [ ] Structured Reel analysis
- [ ] Title generation
- [ ] Summary
- [ ] Key points
- [ ] Topics/categories
- [ ] Likely reason saved
- [ ] Tools/products
- [ ] People/companies
- [ ] Claims
- [ ] Resources
- [ ] Action items
- [ ] Importance
- [ ] Confidence
- [ ] OCR integration
- [ ] Visual/multimodal analysis
- [ ] Fact vs inference distinction

## Phase 4 — Human-in-the-Loop

- [ ] Uncertainty detection
- [ ] Evidence/context collection for questions
- [ ] User question queue
- [ ] MCQ question format
- [ ] Free-text/Other answer support
- [ ] Reel URL attached to questions
- [ ] User answers persisted as first-class data
- [ ] User corrections persisted across AI regeneration
- [ ] Pause/resume dependent processing
- [ ] Live pending-question UI

## Phase 5 — Knowledge Base & Retrieval

- [ ] Reel archive
- [ ] Transcript storage
- [ ] OCR storage
- [ ] Analysis storage
- [ ] User answer/correction storage
- [ ] Full-text search
- [ ] Embeddings
- [ ] Semantic search
- [ ] Related Reels
- [ ] Topic aggregation
- [ ] Cross-Reel relationships
- [ ] Retrieval layer for RAG

## Phase 6 — Personal AI Interface

- [ ] Chat with Reel archive
- [ ] Retrieval-augmented answers
- [ ] Search + chat combination
- [ ] "Find the Reel I remember..."
- [ ] "What have I saved about..."
- [ ] "What haven't I tried?"
- [ ] Cross-Reel synthesis
- [ ] Use knowledge-base records directly without requiring PDF attachments

## Phase 7 — Reporting & Visualization

- [ ] Detailed human-readable PDF generation
- [ ] Deliberately designed report layout
- [ ] Executive summary
- [ ] Collection statistics
- [ ] Topic/category visualizations
- [ ] Important Reel rankings
- [ ] Recurring themes
- [ ] Tools/products/people/companies summaries
- [ ] Resources and URLs
- [ ] Action-item summaries
- [ ] Related-content clusters
- [ ] Forgotten/unacted-on content
- [ ] Unresolved questions
- [ ] User corrections/answers where useful
- [ ] Other meaningful data visualizations
- [ ] Verify reports are specific to actual archive and not generic AI filler

## Phase 8 — Intelligence

- [ ] Detect repeated interests
- [ ] Detect related Reels
- [ ] Detect recurring tools/topics
- [ ] Forgotten-content resurfacing
- [ ] Action tracking
- [ ] Personalized ranking
- [ ] Learn from user corrections
- [ ] Long-term interest evolution

## Explicitly Deferred

- [ ] Multi-user support
- [ ] SaaS billing
- [ ] Social actions
- [ ] Automated messaging
- [ ] Instagram engagement automation
- [ ] Unnecessary distributed infrastructure
