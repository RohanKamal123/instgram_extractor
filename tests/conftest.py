"""Shared pytest fixtures for Phase 0 tests.

All tests use a throwaway SQLite database under a temp directory so that
tests never touch the developer's real data folder.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Ensure ``src`` layout is importable without editable install in tests.
_SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from reel_archivist.config import Settings  # noqa: E402
from reel_archivist.db.connection import init_database  # noqa: E402
from reel_archivist.logging_config import configure_logging  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _configure_test_logging_once() -> None:
    configure_logging(Settings(LOG_TO_FILE=False, LOG_LEVEL="WARNING"))


@pytest.fixture()
def tmp_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Move the project root to a temp dir; return the path."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture()
def test_settings(tmp_project: Path) -> Settings:
    """Settings pointing at a throwaway SQLite DB under ``tmp_project``."""
    settings = Settings(
        DATABASE_URL=f"sqlite:///{tmp_project}/test_archivist.db",
        DATA_DIR=tmp_project / "data",
        LOG_DIR=tmp_project / "logs",
        TEMP_MEDIA_DIR=tmp_project / "temp",
        LOG_TO_FILE=False,
        LOG_LEVEL="WARNING",
    )
    settings.ensure_directories()
    init_database(settings)
    return settings
