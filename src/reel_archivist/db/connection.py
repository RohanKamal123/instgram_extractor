"""SQLite database connection and initialization."""
from __future__ import annotations

import sqlite3
import threading
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from ..config import Settings
from ..logging_config import get_logger
from .schema import SCHEMA_SQL, SCHEMA_VERSION

log = get_logger(__name__)

_local = threading.local()


def _sqlite_id() -> str:
    return uuid.uuid4().hex


def _connect(settings: Settings) -> sqlite3.Connection:
    path = settings.database_path_abs
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(
        str(path),
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False,
        isolation_level=None,  # use explicit transactions
        timeout=30,
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_database(settings: Settings) -> None:
    """Create the schema if missing. Idempotent.

    This must be called before ``get_conn``/``tx`` are usable.
    """
    conn = _connect(settings)
    try:
        with conn:
            conn.executescript(SCHEMA_SQL)
            row = conn.execute(
                "SELECT 1 FROM schema_version WHERE version = ?",
                (SCHEMA_VERSION,),
            ).fetchone()
            if row is None:
                conn.execute(
                    "INSERT OR IGNORE INTO schema_version(version) VALUES(?)",
                    (SCHEMA_VERSION,),
                )
                log.info("Initialized database schema v%s at %s", SCHEMA_VERSION, settings.database_path_abs.name)
    finally:
        conn.close()


def get_conn(settings: Settings) -> sqlite3.Connection:
    """Return a thread-local persistent SQLite connection.

    The caller must not close it; the connection is reused across calls
    in the same thread and closed implicitly on thread exit.

    The cache is invalidated when the requested ``settings change (important for
    test fixtures that use a throwaway DB per test).
    """
    target_path = str(settings.database_path_abs)
    existing_conn = getattr(_local, "conn", None)
    existing_path = getattr(_local, "conn_db_path", None)
    if existing_conn is None or existing_path != target_path:
        if existing_conn is not None:
            try:
                existing_conn.close()
            except sqlite3.Error:
                pass
        _local.conn = _connect(settings)
        _local.conn_db_path = target_path
    return _local.conn


@contextmanager
def tx(settings: Settings) -> Iterator[sqlite3.Connection]:
    """Context manager wrapping a single explicit transaction.

    Usage::

        with tx(settings) as conn:
            conn.execute(...)
            conn.execute(...)
    """
    conn = get_conn(settings)
    try:
        conn.execute("BEGIN")
        yield conn
    except Exception:
        try:
            conn.execute("ROLLBACK")
        except sqlite3.Error:
            pass
        raise
    else:
        conn.execute("COMMIT")


def new_id(prefix: str = "") -> str:
    """Return a new opaque ID, optionally prefixed for readability.

    Prefixes (e.g. ``"reel_"``) make raw DB rows easier to reason about.
    """
    return f"{prefix}{_sqlite_id()}"
