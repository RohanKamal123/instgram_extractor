"""Shared small utilities.

Kept intentionally tiny so we don't import heavy modules here; this module
is safe to import from any layer including data models.
"""
from __future__ import annotations

from datetime import UTC, datetime


def utcnow_iso() -> str:
    """Return current UTC time as a timezone-naive ISO-8601 string.

    The stored format intentionally matches SQLite's ``CURRENT_TIMESTAMP``
    output, which is timezone-naive ISO-8601.

    Uses the Python 3.12+ recommended ``datetime.now(UTC)`` instead of the
    deprecated ``datetime.utcnow()``.
    """
    return datetime.now(UTC).replace(tzinfo=None).isoformat()
