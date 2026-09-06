"""SQLite DDL schema for the Reel Archivist knowledge base.

Mirror of DATA_MODEL.md. Three tiers are preserved:
  * Tier 1 (raw/archive):         reels, transcripts, ocr, evidence
  * Tier 2 (derived, regenerable): analyses, embeddings, reports, visualizations
  * Tier 3 (user knowledge, durable): user_questions, question_options,
                                      user_answers, user_corrections

Sessions and jobs are operational metadata, not knowledge tiers.
"""
from __future__ import annotations

SCHEMA_VERSION = 1

SCHEMA_SQL = """
-- ---------------------------------------------------------------------------
-- Tier 1 — RAW / ARCHIVE (immutable after ingestion, never regenerated)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS reels (
    id                      TEXT PRIMARY KEY,
    instagram_message_id    TEXT,
    reel_url                TEXT NOT NULL,
    conversation_id         TEXT,
    source_identity         TEXT,
    sender                  TEXT,
    creator                 TEXT,
    caption                 TEXT,
    captured_at             TEXT,
    original_media_url      TEXT,
    local_media_path        TEXT,
    media_retention_policy  TEXT DEFAULT 'temporary',
    processing_status       TEXT DEFAULT 'pending',
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_reels_reel_url       ON reels(reel_url);
CREATE INDEX IF NOT EXISTS idx_reels_source         ON reels(source_identity);
CREATE INDEX IF NOT EXISTS idx_reels_processing     ON reels(processing_status);
CREATE INDEX IF NOT EXISTS idx_reels_message_id     ON reels(instagram_message_id);

CREATE TABLE IF NOT EXISTS transcripts (
    id                      TEXT PRIMARY KEY,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    text                    TEXT,
    language                TEXT,
    source                  TEXT NOT NULL,   -- instagram | subtitle | whisper | other
    confidence              REAL,
    timestamped_segments    TEXT,            -- JSON array, nullable
    is_preferred            INTEGER NOT NULL DEFAULT 1,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_transcripts_reel ON transcripts(reel_id);

CREATE TABLE IF NOT EXISTS ocr (
    id                      TEXT PRIMARY KEY,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    text                    TEXT,
    frame_timestamp         REAL,
    confidence              REAL,
    frame_reference         TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_ocr_reel ON ocr(reel_id);

CREATE TABLE IF NOT EXISTS evidence (
    id                      TEXT PRIMARY KEY,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    evidence_type           TEXT NOT NULL,   -- transcript|subtitle|ocr|visual|caption|metadata|external_resource
    content_reference       TEXT,            -- opaque reference (JSON/text/URL/path)
    evidence_timestamp      TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_evidence_reel ON evidence(reel_id);

-- ---------------------------------------------------------------------------
-- Tier 2 — DERIVED / AI-GENERATED (regenerable; Tier 3 corrections win)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS analyses (
    id                      TEXT PRIMARY KEY,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    title                   TEXT,
    summary                 TEXT,
    why_saved               TEXT,
    why_saved_is_inference  INTEGER NOT NULL DEFAULT 1,
    key_points              TEXT,            -- JSON array
    topics                  TEXT,            -- JSON array
    categories              TEXT,            -- JSON array
    tools                   TEXT,            -- JSON array
    products                TEXT,            -- JSON array
    people                  TEXT,            -- JSON array
    companies               TEXT,            -- JSON array
    claims                  TEXT,            -- JSON array
    resources               TEXT,            -- JSON array
    action_items            TEXT,            -- JSON array
    importance              REAL,
    confidence              REAL,
    model                   TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_analyses_reel ON analyses(reel_id);

CREATE TABLE IF NOT EXISTS embeddings (
    id                      TEXT PRIMARY KEY,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    content_type            TEXT NOT NULL,   -- title|summary|transcript|combined
    vector                  BLOB,            -- raw embedding bytes; Phase 5+
    model                   TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_embeddings_reel ON embeddings(reel_id);

CREATE TABLE IF NOT EXISTS reports (
    id                      TEXT PRIMARY KEY,
    report_type             TEXT NOT NULL,   -- pdf|summary|executive|visualization_set
    title                   TEXT,
    scope                   TEXT,            -- JSON description of scope
    output_path             TEXT,
    source_snapshot_ref     TEXT,
    generated_at            TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS visualizations (
    id                      TEXT PRIMARY KEY,
    report_id               TEXT REFERENCES reports(id) ON DELETE SET NULL,
    visualization_type      TEXT NOT NULL,
    title                   TEXT,
    data_reference          TEXT,
    output_path             TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- Tier 3 — USER KNOWLEDGE (durable; never overwritten by AI regeneration)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS user_questions (
    id                      TEXT PRIMARY KEY,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    session_id              TEXT REFERENCES processing_sessions(id) ON DELETE SET NULL,
    question                TEXT NOT NULL,
    reason                  TEXT,            -- why this question was generated
    evidence_context        TEXT,            -- JSON snapshot of evidence
    question_type           TEXT NOT NULL,   -- mcq | free_text | confirmation
    status                  TEXT NOT NULL DEFAULT 'pending',   -- pending|answered|dismissed|superseded
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    answered_at             TEXT
);
CREATE INDEX IF NOT EXISTS idx_questions_status  ON user_questions(status);
CREATE INDEX IF NOT EXISTS idx_questions_reel    ON user_questions(reel_id);
CREATE INDEX IF NOT EXISTS idx_questions_session ON user_questions(session_id);

CREATE TABLE IF NOT EXISTS question_options (
    id                      TEXT PRIMARY KEY,
    question_id             TEXT NOT NULL REFERENCES user_questions(id) ON DELETE CASCADE,
    label                   TEXT NOT NULL,
    value                   TEXT NOT NULL,
    position                INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_options_question ON question_options(question_id);

CREATE TABLE IF NOT EXISTS user_answers (
    id                      TEXT PRIMARY KEY,
    question_id             TEXT NOT NULL REFERENCES user_questions(id) ON DELETE CASCADE,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    selected_option_id      TEXT REFERENCES question_options(id) ON DELETE SET NULL,
    free_text               TEXT,
    answered_at             TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_answers_question ON user_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_answers_reel     ON user_answers(reel_id);

CREATE TABLE IF NOT EXISTS user_corrections (
    id                      TEXT PRIMARY KEY,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    field_name              TEXT NOT NULL,   -- e.g. 'why_saved', 'categories[2]'
    original_value          TEXT,            -- JSON-encoded original value from AI
    corrected_value         TEXT,            -- JSON-encoded user-provided value
    reason                  TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_corrections_reel ON user_corrections(reel_id);

-- ---------------------------------------------------------------------------
-- Operational metadata
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS processing_sessions (
    id                      TEXT PRIMARY KEY,
    selected_source_identity TEXT,
    status                  TEXT NOT NULL DEFAULT 'starting',  -- starting|running|waiting_for_user|paused|completed|failed|stopped
    started_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paused_at               TEXT,
    completed_at            TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS processing_jobs (
    id                      TEXT PRIMARY KEY,
    session_id              TEXT REFERENCES processing_sessions(id) ON DELETE SET NULL,
    reel_id                 TEXT NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
    job_type                TEXT NOT NULL,   -- e.g. ingest|transcript|ocr|analyze|embed|complete
    status                  TEXT NOT NULL DEFAULT 'pending',   -- pending|processing|waiting_for_user|completed|failed|cancelled
    attempts                INTEGER NOT NULL DEFAULT 0,
    error                   TEXT,
    started_at              TEXT,
    completed_at            TEXT,
    created_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_jobs_session ON processing_jobs(session_id);
CREATE INDEX IF NOT EXISTS idx_jobs_reel    ON processing_jobs(reel_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status  ON processing_jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_type    ON processing_jobs(job_type);

-- ---------------------------------------------------------------------------
-- Internal bookkeeping
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS schema_version (
    version                 INTEGER PRIMARY KEY,
    applied_at              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""
