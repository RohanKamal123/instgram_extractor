"""Tests for the status UI scaffold (Phase 0)."""
from __future__ import annotations

from fastapi.testclient import TestClient

from reel_archivist.config import Settings
from reel_archivist.db.connection import get_conn, new_id, tx
from reel_archivist.ui.app import create_app


def test_health_endpoint(test_settings: Settings) -> None:
    app = create_app(test_settings)
    with TestClient(app) as client:
        r = client.get("/api/health")
        assert r.status_code == 200
        body = r.json()
        assert body["ok"] is True
        assert body["phase"] == 0
        assert "db_path" in body


def test_status_json_contains_all_required_fields(test_settings: Settings) -> None:
    app = create_app(test_settings)
    with TestClient(app) as client:
        r = client.get("/api/status")
        assert r.status_code == 200
        s = r.json()
        for top in ("session", "progress", "current_reel", "pending_questions", "phase", "generated_at"):
            assert top in s, f"Missing /api/status field: {top}"
        prog = s["progress"]
        for k in (
            "reels_total", "reels_processed", "reels_processing", "reels_failed",
            "jobs_total", "jobs_completed", "jobs_remaining", "jobs_failed", "retry_attempts",
        ):
            assert k in prog, f"Missing progress field: {k}"


def test_status_html_renders(test_settings: Settings) -> None:
    app = create_app(test_settings)
    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        html = r.text
        assert "Reel Archivist" in html
        assert "Current Reel" in html
        assert "Pending Questions" in html
        assert "Human-in-the-Loop" in html


def test_pending_questions_shown_in_status(test_settings: Settings) -> None:
    app = create_app(test_settings)
    conn = get_conn(test_settings)
    # Seed a session + reel + question that looks like a real one
    sid = new_id("sess_1_")
    rid = new_id("reel_1_")
    qid = new_id("q_1_")

    with tx(test_settings):
        conn.execute(
            "INSERT INTO processing_sessions(id, status, selected_source_identity) VALUES (?,?,?)",
            (sid, "waiting_for_user", "@demo"),
        )
        conn.execute(
            "INSERT INTO reels(id, reel_url, source_identity, processing_status) VALUES (?,?,?,?)",
            (rid, "https://instagram.com/reel/STATUS_CHECK/", "@demo", "waiting_for_user"),
        )
        conn.execute(
            """INSERT INTO user_questions
               (id, reel_id, session_id, question, question_type, status)
               VALUES (?,?,?,?,?,?)""",
            (qid, rid, sid, "Confirm: is this a tutorial on async Python?", "confirmation", "pending"),
        )

    with TestClient(app) as client:
        s = client.get("/api/status").json()
        pending = [q for q in s["pending_questions"] if q["id"] == qid]
        assert len(pending) == 1
        assert pending[0]["reel_url"] == "https://instagram.com/reel/STATUS_CHECK/"
        assert "async Python" in pending[0]["question"]
