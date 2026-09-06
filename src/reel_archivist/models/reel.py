"""Reel, Transcript, OCR, Evidence models (Tier 1 raw data)."""
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

ReelProcessingStatus = Literal[
    "pending",
    "discovered",
    "queued",
    "processing",
    "waiting_for_user",
    "processed",
    "failed",
    "archived",
]

TranscriptSource = Literal["instagram", "subtitle", "whisper", "other"]


class Reel(BaseModel):
    """Raw Reel record — Tier 1 raw data. See DATA_MODEL.md § Reel."""

    id: str
    instagram_message_id: Optional[str] = None
    reel_url: str
    conversation_id: Optional[str] = None
    source_identity: Optional[str] = None
    sender: Optional[str] = None
    creator: Optional[str] = None
    caption: Optional[str] = None
    captured_at: Optional[str] = None
    original_media_url: Optional[str] = None
    local_media_path: Optional[str] = None
    media_retention_policy: str = "temporary"
    processing_status: ReelProcessingStatus = "pending"
    created_at: str = Field(default_factory=utcnow_iso)
    updated_at: str = Field(default_factory=utcnow_iso)


class Transcript(BaseModel):
    """Transcript of a Reel with provenance. See DATA_MODEL.md § Transcript."""

    id: str
    reel_id: str
    text: Optional[str] = None
    language: Optional[str] = None
    source: TranscriptSource
    confidence: Optional[float] = None
    timestamped_segments: Optional[str] = None  # JSON string or None
    is_preferred: bool = True
    created_at: str = Field(default_factory=utcnow_iso)


class OCR(BaseModel):
    """OCR extraction from a Reel frame. See DATA_MODEL.md § OCR."""

    id: str
    reel_id: str
    text: Optional[str] = None
    frame_timestamp: Optional[float] = None
    confidence: Optional[float] = None
    frame_reference: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)


class Evidence(BaseModel):
    """Evidence snapshot tied to an analysis or user question."""

    id: str
    reel_id: str
    evidence_type: Literal[
        "transcript", "subtitle", "ocr", "visual", "caption", "metadata", "external_resource"
    ]
    content_reference: Optional[str] = None
    evidence_timestamp: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)
