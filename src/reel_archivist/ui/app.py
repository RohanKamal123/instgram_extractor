"""Status/control UI application (Phase 0 skeleton).

Phase 0 scope: renders a live operational view of the processing pipeline
state. The data shown is currently DB-backed scaffolding (real tables, real
models) but the actual ingestion/processing workers come online in Phase 1.

Required UI elements per AGENTS.md and ROADMAP Phase 0:
  * current session (id, status, started)
  * selected account / conversation
  * current Reel + URL + current stage
  * progress counts: completed / remaining / failed / retries
  * pending questions (Human-in-the-Loop queue preview)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .._utils import utcnow_iso
from ..config import Settings
from ..db.connection import get_conn, new_id, tx
from ..logging_config import get_logger

log = get_logger(__name__)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _ensure_seed_session(settings: Settings) -> str:
    """Create a dummy Phase 0 session + jobs if DB has no rows yet.

    This provides the Phase 0 status UI with something meaningful to render.
    In later phases the worker creates sessions itself.
    """
    conn = get_conn(settings)
    row = conn.execute("SELECT id FROM processing_sessions LIMIT 1").fetchone()
    if row is not None:
        return row["id"]

    session_id = new_id("sess_")
    reel_id_1 = new_id("reel_")
    reel_id_2 = new_id("reel_")
    reel_id_3 = new_id("reel_")
    question_id = new_id("q_")

    with tx(settings):
        now = utcnow_iso()
        conn.execute(
            """INSERT INTO processing_sessions
               (id, selected_source_identity, status, started_at, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (session_id, None, "starting", now, now, now),
        )
        for rid, status, url in (
            (reel_id_1, "processed", "https://www.instagram.com/reel/Cx1ExampleA/"),
            (reel_id_2, "processing", "https://www.instagram.com/reel/Cx2ExampleB/"),
            (reel_id_3, "queued", "https://www.instagram.com/reel/Cx3ExampleC/"),
        ):
            conn.execute(
                """INSERT INTO reels
                   (id, reel_url, source_identity, processing_status, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (rid, url, None, status, now, now),
            )
        # Seed some jobs with different stages to give the UI real counts
        jobs = [
            (new_id("job_"), session_id, reel_id_1, "ingest", "completed", 1),
            (new_id("job_"), session_id, reel_id_1, "transcript", "completed", 1),
            (new_id("job_"), session_id, reel_id_1, "analyze", "completed", 1),
            (new_id("job_"), session_id, reel_id_2, "ingest", "completed", 1),
            (new_id("job_"), session_id, reel_id_2, "transcript", "processing", 1),
            (new_id("job_"), session_id, reel_id_3, "ingest", "pending", 0),
            (new_id("job_"), session_id, reel_id_3, "transcript", "pending", 0),
            (new_id("job_"), session_id, reel_id_3, "analyze", "failed", 2),
        ]
        for jid, sid, rid, jtype, jstatus, att in jobs:
            conn.execute(
                """INSERT INTO processing_jobs
                   (id, session_id, reel_id, job_type, status, attempts, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (jid, sid, rid, jtype, jstatus, att, now),
            )
        # Seed a pending question to exercise the HITL queue UI
        conn.execute(
            """INSERT INTO user_questions
               (id, reel_id, session_id, question, reason, evidence_context,
                question_type, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                question_id,
                reel_id_2,
                session_id,
                "What is the most likely reason you saved this Reel?",
                "AI inference confidence was below threshold for 'why saved'.",
                '{"caption_excerpt":"how I built my startup in 3 days","transcript_excerpt":"..."}',
                "mcq",
                "pending",
                now,
            ),
        )
        for pos, (label, value) in enumerate(
            [
                ("Learn a tool / technique", "learning"),
                ("Reference / tutorial later", "reference"),
                ("Inspiration / idea", "inspiration"),
                ("Action item / todo", "todo"),
                ("Other (free text)", "other"),
            ]
        ):
            conn.execute(
                """INSERT INTO question_options
                   (id, question_id, label, value, position)
                   VALUES (?, ?, ?, ?, ?)""",
                (new_id("opt_"), question_id, label, value, pos),
            )
    log.info("Seeded Phase 0 demonstration session=%s", session_id)
    return session_id


def _collect_status_payload(settings: Settings) -> dict[str, Any]:
    session_id = _ensure_seed_session(settings)
    conn = get_conn(settings)
    session = conn.execute(
        "SELECT * FROM processing_sessions WHERE id = ?", (session_id,)
    ).fetchone()

    reels_total = conn.execute("SELECT COUNT(*) AS c FROM reels").fetchone()["c"]
    reels_processed = conn.execute(
        "SELECT COUNT(*) AS c FROM reels WHERE processing_status='processed'"
    ).fetchone()["c"]
    reels_processing = conn.execute(
        "SELECT COUNT(*) AS c FROM reels WHERE processing_status IN ('processing','queued')"
    ).fetchone()["c"]
    reels_failed = conn.execute(
        "SELECT COUNT(*) AS c FROM reels WHERE processing_status='failed'"
    ).fetchone()["c"]

    jobs_total = conn.execute("SELECT COUNT(*) AS c FROM processing_jobs").fetchone()["c"]
    jobs_completed = conn.execute(
        "SELECT COUNT(*) AS c FROM processing_jobs WHERE status='completed'"
    ).fetchone()["c"]
    jobs_failed = conn.execute(
        "SELECT COUNT(*) AS c FROM processing_jobs WHERE status='failed'"
    ).fetchone()["c"]
    retry_attempts = conn.execute(
        "SELECT COALESCE(SUM(attempts),0) AS s FROM processing_jobs WHERE attempts > 1"
    ).fetchone()["s"]

    current = conn.execute(
        """SELECT r.id, r.reel_url, r.processing_status, j.job_type AS current_stage
           FROM reels r
           LEFT JOIN processing_jobs j ON j.reel_id = r.id AND j.status = 'processing'
           ORDER BY CASE r.processing_status
               WHEN 'processing' THEN 0 WHEN 'queued' THEN 1 WHEN 'failed' THEN 2 ELSE 3 END,
             r.created_at ASC
           LIMIT 1"""
    ).fetchone()

    questions = conn.execute(
        """SELECT q.id, q.reel_id, q.question, q.question_type, q.reason, q.created_at,
                  r.reel_url
           FROM user_questions q
           JOIN reels r ON r.id = q.reel_id
           WHERE q.status='pending'
           ORDER BY q.created_at ASC"""
    ).fetchall()

    return {
        "session": dict(session) if session else None,
        "progress": {
            "reels_total": reels_total,
            "reels_processed": reels_processed,
            "reels_processing": reels_processing,
            "reels_failed": reels_failed,
            "jobs_total": jobs_total,
            "jobs_completed": jobs_completed,
            "jobs_remaining": max(jobs_total - jobs_completed - jobs_failed, 0),
            "jobs_failed": jobs_failed,
            "retry_attempts": retry_attempts,
        },
        "current_reel": dict(current) if current else None,
        "pending_questions": [dict(q) for q in questions],
        "phase": 0,
        "phase_note": "Phase 0 skeleton — infrastructure only. Instagram ingestion starts in Phase 1.",
        "generated_at": utcnow_iso(),
    }


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title="Reel Archivist Status UI",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )
    app.state.settings = settings

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index(request: Request) -> HTMLResponse:
        payload = _collect_status_payload(settings)
        return templates.TemplateResponse(
            request,
            "status.html",
            {"s": payload},
        )

    @app.get("/api/status")
    async def api_status() -> JSONResponse:
        return JSONResponse(_collect_status_payload(settings))

    @app.get("/api/health")
    async def api_health() -> JSONResponse:
        return JSONResponse(
            {
                "ok": True,
                "phase": 0,
                "app": "reel-archivist",
                "db_path": str(settings.database_path_abs),
            }
        )

    return app
