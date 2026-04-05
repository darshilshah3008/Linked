"""Lead schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LeadInput(BaseModel):
    """Input schema for creating/importing a lead."""

    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(default=None, description="Job location")
    source: str = Field(..., description="Where this lead was found")
    url: Optional[str] = Field(default=None, description="Direct apply URL")
    description_snippet: Optional[str] = Field(
        default=None, description="Short description excerpt"
    )


class LeadRecord(BaseModel):
    """Full lead record with computed fields."""

    id: int
    title: str
    company: str
    location: Optional[str] = None
    source: str
    url: Optional[str] = None
    date_seen: datetime
    description_snippet: Optional[str] = None
    relevance_score: float = Field(default=0.0, ge=0.0, le=100.0)
    match_reasons: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    confidence: str = Field(default="medium", description="high | medium | low")
    status: str = Field(default="new", description="new | reviewed | applied | rejected | archived")

    model_config = {"from_attributes": True}


class LeadScoreResult(BaseModel):
    """Output of lead scoring with full explainability."""

    score: float = Field(..., ge=0.0, le=100.0, description="Fit score 0-100")
    observed_facts: list[str] = Field(default_factory=list, description="Raw facts observed from listing")
    inferred_match_reasons: list[str] = Field(default_factory=list, description="Why this matches the profile")
    missing_requirements: list[str] = Field(default_factory=list, description="Requirements the candidate lacks")
    confidence: str = Field(default="medium", description="high | medium | low")
