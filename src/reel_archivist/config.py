"""Application configuration loaded from environment variables."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

MediaRetentionPolicy = Literal["temporary", "permanent", "configurable"]


class Settings(BaseSettings):
    """Typed application configuration.

    All values can be overridden via environment variables or a ``.env`` file
    in the project root. Real secrets are loaded from the environment only;
    ``.env.example`` contains safe placeholders without real credentials.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- AI provider ---------------------------------------------------------
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # --- Paths ---------------------------------------------------------------
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
    DATA_DIR: Path = Field(default=Path("./data"))
    LOG_DIR: Path = Field(default=Path("./logs"))
    TEMP_MEDIA_DIR: Path = Field(default=Path("./temp_media"))

    # --- Database ------------------------------------------------------------
    DATABASE_URL: str = "sqlite:///./data/reel_archivist.db"

    # --- Logging -------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = True

    # --- Media ---------------------------------------------------------------
    MEDIA_RETENTION_POLICY: MediaRetentionPolicy = "temporary"

    # --- Web UI --------------------------------------------------------------
    UI_HOST: str = "127.0.0.1"
    UI_PORT: int = 8765

    # --- Browser / Playwright ------------------------------------------------
    PLAYWRIGHT_USER_DATA_DIR: str = ""
    PLAYWRIGHT_HEADLESS: bool = False

    # ------------------------------------------------------------------ paths

    @property
    def data_dir_abs(self) -> Path:
        return (self.PROJECT_ROOT / self.DATA_DIR).resolve()

    @property
    def log_dir_abs(self) -> Path:
        return (self.PROJECT_ROOT / self.LOG_DIR).resolve()

    @property
    def temp_media_dir_abs(self) -> Path:
        return (self.PROJECT_ROOT / self.TEMP_MEDIA_DIR).resolve()

    @property
    def database_path_abs(self) -> Path:
        """Resolved absolute path for the local SQLite database."""
        prefix = "sqlite:///"
        if self.DATABASE_URL.startswith(prefix):
            rel = self.DATABASE_URL[len(prefix):]
            return (self.PROJECT_ROOT / rel).resolve()
        raise ValueError(
            "Only local SQLite databases are supported in Phase 0 "
            f"(got DATABASE_URL={self.DATABASE_URL!r})"
        )

    def ensure_directories(self) -> None:
        """Create required directories if they don't already exist."""
        for p in (self.data_dir_abs, self.log_dir_abs, self.temp_media_dir_abs):
            p.mkdir(parents=True, exist_ok=True)
