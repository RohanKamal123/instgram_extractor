"""Question / Answer / Correction models (Tier 3 — durable user knowledge)."""
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

QuestionType = Literal["mcq", "free_text", "confirmation"]
QuestionStatus = Literal["pending", "answered", "dismissed", "superseded"]


class UserQuestion(BaseModel):
    """An ambiguity that must be resolved by the user (Category 3 / HITL).

    See DATA_MODEL.md § User Question and SYSTEM_PROMPT §4.
    """

    id: str
    reel_id: str
    session_id: Optional[str] = None
    question: str
    reason: Optional[str] = None
    evidence_context: Optional[str] = None  # JSON snapshot
    question_type: QuestionType = "mcq"
    status: QuestionStatus = "pending"
    created_at: str = Field(default_factory=utcnow_iso)
    answered_at: Optional[str] = None


class QuestionOption(BaseModel):
    """One option for an MCQ-type UserQuestion."""

    id: str
    question_id: str
    label: str
    value: str
    position: int = 0


class UserAnswer(BaseModel):
    """The user's response to a UserQuestion. This is Tier 3 durable knowledge."""

    id: str
    question_id: str
    reel_id: str
    selected_option_id: Optional[str] = None
    free_text: Optional[str] = None
    answered_at: str = Field(default_factory=utcnow_iso)


class UserCorrection(BaseModel):
    """An explicit user correction to an AI-derived field. Tier 3, durable."""

    id: str
    reel_id: str
    field_name: str
    original_value: Optional[str] = None
    corrected_value: Optional[str] = None
    reason: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)
