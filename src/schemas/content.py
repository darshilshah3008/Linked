"""Content schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContentInput(BaseModel):
    """Input for creating a content item."""

    theme: str = Field(..., description="Topic theme")
    content_type: str = Field(
        default="linkedin_post", description="linkedin_post | comment_draft | article_idea"
    )
    hook: Optional[str] = Field(default=None, description="Opening hook line")
    outline: Optional[str] = Field(default=None, description="Bullet-point outline")
    full_text: Optional[str] = Field(default=None, description="Full draft text")


class ContentRecord(BaseModel):
    """Full content item record."""

    id: int
    theme: str
    content_type: str
    hook: Optional[str] = None
    outline: Optional[str] = None
    full_text: Optional[str] = None
    status: str = Field(default="draft", description="draft | approved | posted | archived")
    created_at: datetime

    model_config = {"from_attributes": True}


class ContentPlan(BaseModel):
    """Weekly/monthly content plan."""

    week_number: int
    items: list[ContentInput]
    notes: Optional[str] = None
