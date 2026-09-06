"""Tests for privacy-aware logging."""
from __future__ import annotations

import io
import logging

from reel_archivist.logging_config import PrivacyFilter, configure_logging


def _make_logger_with_buffer() -> tuple[logging.Logger, io.StringIO]:
    logger = logging.getLogger("privacy_test_" + __name__)
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    buf = io.StringIO()
    h = logging.StreamHandler(buf)
    h.addFilter(PrivacyFilter())
    logger.addHandler(h)
    return logger, buf


def test_api_key_pattern_is_redacted() -> None:
    logger, buf = _make_logger_with_buffer()
    logger.info("Got token sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcd calling API")
    out = buf.getvalue()
    assert "sk-proj-" not in out
    assert "[REDACTED]" in out


def test_bearer_token_is_redacted() -> None:
    logger, buf = _make_logger_with_buffer()
    logger.info("Header Authorization=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    out = buf.getvalue()
    assert "Bearer eyJhbGci" not in out
    assert "[REDACTED]" in out


def test_password_assignment_is_redacted() -> None:
    logger, buf = _make_logger_with_buffer()
    logger.info("Config password=SuperSecret123 loaded")
    out = buf.getvalue()
    assert "SuperSecret123" not in out
    assert "[REDACTED]" in out


def test_long_messages_are_truncated() -> None:
    logger, buf = _make_logger_with_buffer()
    long_txt = "x" * 1000
    logger.info("Captured reel caption: %s", long_txt)
    out = buf.getvalue()
    assert "[truncated 1000 chars]" in out
    assert len(out) < 800  # well below the 1000+ message


def test_harmless_log_lines_are_unchanged() -> None:
    logger, buf = _make_logger_with_buffer()
    logger.info("Initialized 12 tables in schema v1 in 0.03s")
    out = buf.getvalue()
    assert "Initialized 12 tables in schema v1 in 0.03s" in out
    assert "[REDACTED]" not in out


def test_configure_logging_is_idempotent() -> None:
    # Calling twice should not stack handlers
    from reel_archivist.config import Settings

    configure_logging(Settings(LOG_TO_FILE=False))
    before = len(logging.getLogger().handlers)
    configure_logging(Settings(LOG_TO_FILE=False))
    after = len(logging.getLogger().handlers)
    assert before == after
