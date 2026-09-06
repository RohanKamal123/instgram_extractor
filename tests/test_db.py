"""Tests for the SQLite schema and basic persistence (Phase 0)."""
from __future__ import annotations

import sqlite3

from reel_archivist.config import Settings
from reel_archivist.db.connection import get_conn, init_database, new_id, tx
from reel_archivist.db.schema import SCHEMA_VERSION


def test_init_creates_schema_version(test_settings: Settings) -> None:
    init_database(test_settings)  # should be idempotent
    conn = get_conn(test_settings)
    row = conn.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
    assert row["v"] == SCHEMA_VERSION


def test_expected_tables_exist(test_settings: Settings) -> None:
    expected = {
        "reels", "transcripts", "ocr", "evidence",
        "analyses", "embeddings", "reports", "visualizations",
        "user_questions", "question_options", "user_answers", "user_corrections",
        "processing_sessions", "processing_jobs", "schema_version",
    }
    conn = get_conn(test_settings)
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    tables = {r["name"] for r in rows}
    missing = expected - tables
    assert not missing, f"Missing tables: {sorted(missing)}"


def test_session_and_job_roundtrip(test_settings: Settings) -> None:
    conn = get_conn(test_settings)
    session_id = new_id("sess_")
    reel_id = new_id("reel_")
    job_id = new_id("job_")

    with tx(test_settings):
        conn.execute(
            """INSERT INTO processing_sessions
               (id, selected_source_identity, status) VALUES (?, ?, ?)""",
            (session_id, "@myself", "running"),
        )
        conn.execute(
            """INSERT INTO reels
               (id, reel_url, source_identity, processing_status) VALUES (?,?,?,?)""",
            (reel_id, "https://instagram.com/reel/X/", "@myself", "queued"),
        )
        conn.execute(
            """INSERT INTO processing_jobs
               (id, session_id, reel_id, job_type, status, attempts) VALUES (?,?,?,?,?,?)""",
            (job_id, session_id, reel_id, "transcript", "pending", 0),
        )

    job = conn.execute("SELECT * FROM processing_jobs WHERE id=?", (job_id,)).fetchone()
    assert job["reel_id"] == reel_id
    assert job["job_type"] == "transcript"
    assert job["session_id"] == session_id
    reel = conn.execute("SELECT reel_url FROM reels WHERE id=?", (reel_id,)).fetchone()
    assert reel["reel_url"].endswith("/X/")


def test_user_question_and_answer_roundtrip(test_settings: Settings) -> None:
    conn = get_conn(test_settings)
    qid = new_id("q_")
    aid = new_id("a_")
    oid = new_id("opt_")
    rid = new_id("reel_q_")
    sid = new_id("sess_q_")

    with tx(test_settings):
        conn.execute(
            "INSERT INTO processing_sessions(id,status) VALUES (?,?)",
            (sid, "waiting_for_user"),
        )
        conn.execute(
            "INSERT INTO reels(id,reel_url,processing_status) VALUES (?,?,?)",
            (rid, "https://instagram.com/reel/Q/", "waiting_for_user"),
        )
        conn.execute(
            """INSERT INTO user_questions
               (id, reel_id, session_id, question, question_type, status)
               VALUES (?,?,?,?,?,?)""",
            (qid, rid, sid, "Why did you save this?", "mcq", "pending"),
        )
        conn.execute(
            "INSERT INTO question_options(id,question_id,label,value,position) VALUES (?,?,?,?,?)",
            (oid, qid, "Learning", "learning", 0),
        )
        conn.execute(
            """INSERT INTO user_answers
               (id, question_id, reel_id, selected_option_id, free_text)
               VALUES (?,?,?,?,?)""",
            (aid, qid, rid, oid, None),
        )
        conn.execute(
            "UPDATE user_questions SET status='answered', answered_at=CURRENT_TIMESTAMP WHERE id=?",
            (qid,),
        )

    q = conn.execute("SELECT status, answered_at FROM user_questions WHERE id=?", (qid,)).fetchone()
    assert q["status"] == "answered"
    assert q["answered_at"] is not None
    ans = conn.execute(
        "SELECT selected_option_id, free_text FROM user_answers WHERE id=?", (aid,)
    ).fetchone()
    assert ans["selected_option_id"] == oid
    assert ans["free_text"] is None


def test_tx_rollback_on_error(test_settings: Settings) -> None:
    conn = get_conn(test_settings)
    sid = new_id("fail_")

    try:
        with tx(test_settings):
            conn.execute(
                "INSERT INTO processing_sessions(id,status) VALUES (?,?)", (sid, "running")
            )
            raise RuntimeError("boom")  # trigger rollback
    except RuntimeError:
        pass

    row = conn.execute(
        "SELECT 1 FROM processing_sessions WHERE id=?", (sid,)
    ).fetchone()
    assert row is None, "Transaction was not rolled back"


def test_new_id_prefixes_are_unique() -> None:
    ids = {new_id("reel_") for _ in range(50)}
    assert len(ids) == 50
    assert all(i.startswith("reel_") for i in ids)


def test_foreign_keys_enforced(test_settings: Settings) -> None:
    conn = get_conn(test_settings)
    # Referencing a reel_id that does not exist should fail (FKs ON).
    with pytest.raises(sqlite3.IntegrityError):  # type: ignore[name-defined]
        with tx(test_settings):
            conn.execute(
                "INSERT INTO transcripts(id,reel_id,source) VALUES (?,?,?)",
                (new_id("t_"), "reel_does_not_exist", "whisper"),
            )


import pytest  # noqa: E402  (used inline above for raises block)
