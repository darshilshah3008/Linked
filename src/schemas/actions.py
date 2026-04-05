"""Action schemas used by the orchestrator."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    """A single recommended action."""

    action_type: str = Field(
        ...,
        description="review_lead | research_company | draft_content | draft_outreach | follow_up | post_content",
    )
    description: str
    priority: int = Field(default=5, ge=1, le=10, description="1=highest, 10=lowest")
    target_id: Optional[int] = None
    target_type: Optional[str] = None
    requires_approval: bool = Field(default=False)


class DailyPlan(BaseModel):
    """Daily action plan from the orchestrator."""

    date: datetime
    actions: list[ActionItem]
    summary: str
    leads_to_review: int = 0
    companies_to_research: int = 0
    content_to_create: int = 0
    outreach_to_send: int = 0


class DashboardSnapshot(BaseModel):
    """Complete daily action dashboard."""

    date: datetime
    top_jobs: list[dict] = Field(default_factory=list, description="Top 10 jobs to apply")
    top_people: list[dict] = Field(default_factory=list, description="Top 10 people to engage")
    top_companies: list[dict] = Field(default_factory=list, description="Top 5 companies to track")
    outreach_drafts: list[dict] = Field(default_factory=list, description="Top 3 outreach drafts")
    comments_to_write: list[dict] = Field(default_factory=list, description="Top 5 engagement comments")
    linkedin_post_draft: Optional[dict] = Field(default=None, description="1 LinkedIn post draft")
    summary: str = ""


class ApplicationInput(BaseModel):
    """Input for tracking an application."""

    lead_id: int
    applied_date: Optional[datetime] = None
    resume_version: Optional[str] = None
    status: str = Field(
        default="applied", description="applied | interviewing | offered | rejected | withdrawn"
    )
    notes: Optional[str] = None


class ApplicationRecord(BaseModel):
    """Full application record."""

    id: int
    lead_id: int
    applied_date: Optional[datetime] = None
    resume_version: Optional[str] = None
    status: str
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class ActivityLogEntry(BaseModel):
    """Activity log entry."""

    id: int
    agent_name: str
    action_type: str
    summary: str
    created_at: datetime

    model_config = {"from_attributes": True}
