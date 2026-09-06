"""Tests for configuration loading."""
from __future__ import annotations

from pathlib import Path

from reel_archivist.config import Settings


def test_defaults_resolve_to_project_root() -> None:
    s = Settings()
    assert s.PROJECT_ROOT.name == "instgram_extractor"
    assert s.DATABASE_URL.startswith("sqlite:///")
    assert s.LOG_LEVEL == "INFO"
    assert s.MEDIA_RETENTION_POLICY == "temporary"


def test_ensure_directories_creates_folders(tmp_project: Path) -> None:
    s = Settings(
        DATA_DIR=tmp_project / "d",
        LOG_DIR=tmp_project / "l",
        TEMP_MEDIA_DIR=tmp_project / "t",
    )
    s.ensure_directories()
    for p in (s.data_dir_abs, s.log_dir_abs, s.temp_media_dir_abs):
        assert p.exists() and p.is_dir()


def test_database_path_abs_resolves_relative(tmp_project: Path) -> None:
    s = Settings(DATABASE_URL=f"sqlite:///./x/y.db")
    s.PROJECT_ROOT = tmp_project
    expected = (tmp_project / "x" / "y.db").resolve()
    assert s.database_path_abs == expected
