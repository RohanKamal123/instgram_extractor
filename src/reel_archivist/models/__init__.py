"""Pydantic data models mirroring DATA_MODEL.md tables.

Models are used for in-memory shape validation and serialization at the
boundaries of the DB layer. The SQLite tables themselves are the source of
truth; these models are just typed transport objects.
"""
from .reel import Reel, ReelProcessingStatus, Transcript, TranscriptSource, OCR, Evidence
from .session import (
    ProcessingSession,
    ProcessingSessionStatus,
    ProcessingJob,
    ProcessingJobStatus,
    JobType,
)
from .question import (
    QuestionType,
    QuestionStatus,
    UserQuestion,
    QuestionOption,
    UserAnswer,
    UserCorrection,
)
from .analysis import Analysis, Report, Visualization, Embedding

__all__ = [
    "Reel",
    "ReelProcessingStatus",
    "Transcript",
    "TranscriptSource",
    "OCR",
    "Evidence",
    "Analysis",
    "Embedding",
    "Report",
    "Visualization",
    "ProcessingSession",
    "ProcessingSessionStatus",
    "ProcessingJob",
    "ProcessingJobStatus",
    "JobType",
    "QuestionType",
    "QuestionStatus",
    "UserQuestion",
    "QuestionOption",
    "UserAnswer",
    "UserCorrection",
]
