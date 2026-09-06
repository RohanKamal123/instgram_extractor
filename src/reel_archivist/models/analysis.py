"""Tier 2 derived knowledge: AI analysis, embeddings, reports, visualizations."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .._utils import utcnow_iso


class Analysis(BaseModel):
    """AI-generated structured analysis of a Reel. Tier 2 — regenerable.

    When regenerated, user corrections (Tier 3) are applied as an overlay on
    read; the analysis row itself can be replaced without losing user input.
    """

    id: str
    reel_id: str
    title: Optional[str] = None
    summary: Optional[str] = None
    why_saved: Optional[str] = None
    why_saved_is_inference: bool = True
    key_points: Optional[str] = None       # JSON array
    topics: Optional[str] = None           # JSON array
    categories: Optional[str] = None       # JSON array
    tools: Optional[str] = None            # JSON array
    products: Optional[str] = None         # JSON array
    people: Optional[str] = None           # JSON array
    companies: Optional[str] = None        # JSON array
    claims: Optional[str] = None           # JSON array
    resources: Optional[str] = None        # JSON array
    action_items: Optional[str] = None     # JSON array
    importance: Optional[float] = None     # 0..1
    confidence: Optional[float] = None     # 0..1
    model: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)
    updated_at: str = Field(default_factory=utcnow_iso)


class Embedding(BaseModel):
    id: str
    reel_id: str
    content_type: str
    vector: Optional[bytes] = None
    model: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)


class Report(BaseModel):
    id: str
    report_type: str
    title: Optional[str] = None
    scope: Optional[str] = None
    output_path: Optional[str] = None
    source_snapshot_ref: Optional[str] = None
    generated_at: str = Field(default_factory=utcnow_iso)


class Visualization(BaseModel):
    id: str
    report_id: Optional[str] = None
    visualization_type: str
    title: Optional[str] = None
    data_reference: Optional[str] = None
    output_path: Optional[str] = None
    created_at: str = Field(default_factory=utcnow_iso)
