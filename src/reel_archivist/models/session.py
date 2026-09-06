"""Session and ProcessingJob operational state models (DATA_MODEL.md)."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .._utils import utcnow_iso

ProcessingSessionStatus = Literal[
    "starting",
    "running",
    "waiting_for_user",
    "paused",
    "completed",
    "failed",
    "stopped",
]

ProcessingJobStatus = Literal[
    "pending",
    "processing",
    "waiting_for_user",
    "completed",
    "failed",
    "cancelled",
]

# Pipeline stages. This list will grow through Phase 1/2/3, but the Phase 0
# skeleton uses the full vocabulary so the UI can render the stage names.
JobType = Literal[
    "ingest",          # Phase 1 — discover + create Reel row
    "metadata",        # Phase 1 — extract metadata/caption/creator
    "media_retrieve",  # Phase 2 — download media if permitted
    "transcript",      # Phase 2 — transcript generation
    "ocr",             # Phase 3 — OCR extraction
    "analyze",         # Phase 3 — AI structured analysis
    "question_review", # Phase 4 — block pending user answer
    "embed",           # Phase 5 — semantic embedding
    "complete",        # Finalize processing_status on the Reel
]


class ProcessingSession(BaseModel):
    """A user-initiated extraction run. See DATA_MODEL.md § ProcessingSession."""

    id: str
    selected_source_identity: Optional[str] = None
    status: ProcessingSessionStatus = "starting"
    started_at: str = Field(default_factory=utcnow_iso)
    paused_at: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)
    updated_at: str = Field(default_factory=utcnow_iso)


class ProcessingJob(BaseModel):
    """One asynchronous stage in a Reel's processing pipeline."""

    id: str
    session_id: Optional[str] = None
    reel_id: str
    job_type: JobType
    status: ProcessingJobStatus = "pending"
    attempts: int = 0
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)
