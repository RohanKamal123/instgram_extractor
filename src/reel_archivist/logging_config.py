"""Privacy-aware logging.

Applies a ``PrivacyFilter`` that redacts known-sensitive patterns so even if
a developer accidentally logs a cookie, session token, auth header, or a
Reel URL / private content string, it does not appear in logs verbatim.

Redaction is conservative: anything that looks like a secret, token, or
credential pattern is replaced with ``[REDACTED]``.
"""
from __future__ import annotations

import logging
import logging.handlers
import re
import sys
from pathlib import Path
from typing import Optional

from .config import Settings

_LOGGERS_INITIALIZED = False

# Regex patterns for things we never want to appear in logs verbatim.
# Each non-capturing group is matched case-insensitively.
_SECRET_PATTERNS: list[re.Pattern[str]] = [
    # Bearer tokens, session cookies, Authorization headers
    re.compile(r"(?i)(bearer\s+[A-Za-z0-9_\-\.=]{10,})"),
    re.compile(r"(?i)(session(?:id)?\s*[=:]\s*[\"']?[A-Za-z0-9_\-]{16,}[\"']?)"),
    re.compile(r"(?i)(cookie\s*[=:]\s*[\"']?[^\s\"']{16,}[\"']?)"),
    re.compile(r"(?i)(authorization\s*[:=]\s*[\"']?[^\s\"']{10,}[\"']?)"),
    # API keys / access tokens / sk-/pk- prefixed
    re.compile(r"(?i)(api[_-]?key\s*[=:]\s*[\"']?[A-Za-z0-9_\-]{10,}[\"']?)"),
    re.compile(r"(?i)(access[_-]?token\s*[=:]\s*[\"']?[A-Za-z0-9_\-]{10,}[\"']?)"),
    re.compile(r"(?i)((?:sk|pk|ds)-[A-Za-z0-9_\-]{16,})"),
    # Password= assignments
    re.compile(r"(?i)(password\s*[=:]\s*[\"']?[^\s\"']{3,}[\"']?)"),
    # mid-length hex strings that look like session IDs or CSRF tokens
    re.compile(r"\b[0-9a-fA-F]{32,}\b"),
]

# Characters of private Reel content that are frequently captured via
# accidentally-logged blobs. Truncate long free-text messages to avoid
# spilling Reel captions into logs.
_MAX_TEXT_LEN = 240


class PrivacyFilter(logging.Filter):
    """Logging filter that redacts secrets and truncates long messages."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        record.msg = self._sanitize(str(record.msg))
        if record.args:
            if isinstance(record.args, tuple):
                record.args = tuple(self._sanitize(str(a)) for a in record.args)
            else:
                record.args = {k: self._sanitize(str(v)) for k, v in record.args.items()}
        if record.exc_info:
            record.exc_text = self._sanitize(record.exc_text or "")
        return True

    # ------------------------------------------------------------------ utils

    @staticmethod
    def _truncate(text: str) -> str:
        if len(text) <= _MAX_TEXT_LEN:
            return text
        return f"{text[:_MAX_TEXT_LEN]}... [truncated {len(text)} chars]"

    @classmethod
    def _sanitize(cls, text: str) -> str:
        if not text:
            return text
        for pattern in _SECRET_PATTERNS:
            text = pattern.sub("[REDACTED]", text)
        return cls._truncate(text)


def _level_from_string(level: str) -> int:
    mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return mapping.get(level.upper(), logging.INFO)


def configure_logging(settings: Optional[Settings] = None) -> None:
    """Configure the root logger with the privacy filter and handlers.

    Idempotent; repeated calls are no-ops. This is called automatically on
    first ``get_logger`` invocation with default settings if never called.
    """
    global _LOGGERS_INITIALIZED
    if _LOGGERS_INITIALIZED:
        return
    settings = settings or Settings()

    root = logging.getLogger()
    root.setLevel(_level_from_string(settings.LOG_LEVEL))
    root.handlers.clear()

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    filt = PrivacyFilter()

    stream = logging.StreamHandler(stream=sys.stdout)
    stream.setFormatter(fmt)
    stream.addFilter(filt)
    root.addHandler(stream)

    if settings.LOG_TO_FILE:
        settings.log_dir_abs.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            settings.log_dir_abs / "reel_archivist.log",
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(fmt)
        file_handler.addFilter(filt)
        root.addHandler(file_handler)

    # Mute overly-verbose library logs by default
    for noisy in ("urllib3", "httpx", "httpcore", "uvicorn", "playwright"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _LOGGERS_INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    """Return a logger, configuring the logging subsystem on first use."""
    if not _LOGGERS_INITIALIZED:
        configure_logging()
    return logging.getLogger(name)
