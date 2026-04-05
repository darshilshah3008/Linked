"""Company schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CompanyInput(BaseModel):
    """Input for creating a company record."""

    name: str
    website: Optional[str] = None
    careers_url: Optional[str] = None
    industry: Optional[str] = None
    summary: Optional[str] = None
    embedded_relevance: Optional[str] = Field(
        default=None, description="high | medium | low | unknown"
    )
    research_notes: Optional[str] = None
    source_url: Optional[str] = None
    suggested_next_step: Optional[str] = Field(
        default=None, description="apply_now | follow_company | engage_employees | monitor_weekly"
    )


class CompanyRecord(BaseModel):
    """Full company record."""

    id: int
    name: str
    website: Optional[str] = None
    careers_url: Optional[str] = None
    industry: Optional[str] = None
    summary: Optional[str] = None
    embedded_relevance: Optional[str] = None
    research_notes: Optional[str] = None
    source_url: Optional[str] = None
    suggested_next_step: Optional[str] = None
    last_researched: Optional[datetime] = None

    model_config = {"from_attributes": True}
