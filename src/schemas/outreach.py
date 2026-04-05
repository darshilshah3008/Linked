"""Outreach schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OutreachInput(BaseModel):
    """Input for creating an outreach message draft."""

    contact_id: Optional[int] = None
    company_id: Optional[int] = None
    lead_id: Optional[int] = None
    message_type: str = Field(
        ...,
        description="recruiter_intro | hiring_manager_intro | connection_note | follow_up | post_engagement_comment",
    )
    draft_text: str


class OutreachRecord(BaseModel):
    """Full outreach message record."""

    id: int
    contact_id: Optional[int] = None
    company_id: Optional[int] = None
    lead_id: Optional[int] = None
    message_type: str
    draft_text: str
    approval_status: str = Field(
        default="pending", description="pending | approved | rejected | revision_needed"
    )
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    created_at: datetime

    model_config = {"from_attributes": True}


class ContactInput(BaseModel):
    """Input for creating a contact."""

    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    linkedin_url: Optional[str] = None
    profile_url: Optional[str] = Field(default=None, description="Public profile or team page URL")
    source: Optional[str] = None
    notes: Optional[str] = None
    relevance_reason: Optional[str] = Field(default=None, description="Why this person is relevant")
    contact_priority: str = Field(default="medium", description="high | medium | low")
    suggested_outreach_type: Optional[str] = Field(
        default=None,
        description="connection | recruiter_intro | hiring_manager_intro | warm_engagement_first",
    )
    relationship_stage: str = Field(
        default="identified",
        description="identified | connected | engaged | replied | inactive",
    )


class ContactRecord(BaseModel):
    """Full contact record."""

    id: int
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    linkedin_url: Optional[str] = None
    profile_url: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None
    relevance_reason: Optional[str] = None
    contact_priority: str = "medium"
    suggested_outreach_type: Optional[str] = None
    relationship_stage: str

    model_config = {"from_attributes": True}
