"""Approval schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ApprovalRequest(BaseModel):
    """Request sent to the approval layer."""

    item_type: str = Field(..., description="outreach | content | action")
    item_id: Optional[int] = None
    content_text: str = Field(..., description="The text to be reviewed")
    metadata: dict = Field(default_factory=dict, description="Additional context for review")


class ApprovalDecision(BaseModel):
    """Decision returned by the approval layer."""

    decision: str = Field(..., description="approved | rejected | revision_needed")
    reasons: list[str] = Field(default_factory=list)
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    flagged_issues: list[str] = Field(default_factory=list)


class ApprovalRecord(BaseModel):
    """Persisted approval record."""

    id: int
    item_type: str
    item_id: Optional[int] = None
    decision: str
    reasons: list[str] = Field(default_factory=list)
    confidence_score: float
    reviewed_at: datetime

    model_config = {"from_attributes": True}
