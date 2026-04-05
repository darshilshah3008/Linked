"""SQLAlchemy ORM models for the CRM/memory layer."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base for all models."""

    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class LeadModel(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    company = Column(String(256), nullable=False)
    location = Column(String(256), nullable=True)
    source = Column(String(256), nullable=False)
    url = Column(Text, nullable=True)
    date_seen = Column(DateTime, default=_utcnow, nullable=False)
    description_snippet = Column(Text, nullable=True)
    relevance_score = Column(Float, default=0.0)
    match_reasons_json = Column(Text, default="[]")
    missing_requirements_json = Column(Text, default="[]")
    confidence = Column(String(20), default="medium")
    status = Column(String(50), default="new")

    @property
    def match_reasons(self) -> list[str]:
        return json.loads(self.match_reasons_json) if self.match_reasons_json else []

    @match_reasons.setter
    def match_reasons(self, value: list[str]) -> None:
        self.match_reasons_json = json.dumps(value)

    @property
    def missing_requirements(self) -> list[str]:
        return json.loads(self.missing_requirements_json) if self.missing_requirements_json else []

    @missing_requirements.setter
    def missing_requirements(self, value: list[str]) -> None:
        self.missing_requirements_json = json.dumps(value)


class CompanyModel(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True)
    website = Column(Text, nullable=True)
    careers_url = Column(Text, nullable=True)
    industry = Column(String(256), nullable=True)
    summary = Column(Text, nullable=True)
    embedded_relevance = Column(String(50), nullable=True)
    research_notes = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    suggested_next_step = Column(String(100), nullable=True)
    last_researched = Column(DateTime, nullable=True)


class ContactModel(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    role = Column(String(256), nullable=True)
    company = Column(String(256), nullable=True)
    linkedin_url = Column(Text, nullable=True)
    profile_url = Column(Text, nullable=True)
    source = Column(String(256), nullable=True)
    notes = Column(Text, nullable=True)
    relevance_reason = Column(Text, nullable=True)
    contact_priority = Column(String(20), default="medium")
    suggested_outreach_type = Column(String(100), nullable=True)
    relationship_stage = Column(String(50), default="identified")


class ApplicationModel(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    applied_date = Column(DateTime, nullable=True)
    resume_version = Column(String(100), nullable=True)
    status = Column(String(50), default="applied")
    notes = Column(Text, nullable=True)


class OutreachMessageModel(Base):
    __tablename__ = "outreach_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    message_type = Column(String(100), nullable=False)
    draft_text = Column(Text, nullable=False)
    approval_status = Column(String(50), default="pending")
    confidence_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=_utcnow, nullable=False)


class ContentItemModel(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    theme = Column(String(256), nullable=False)
    content_type = Column(String(100), default="linkedin_post")
    hook = Column(Text, nullable=True)
    outline = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime, default=_utcnow, nullable=False)


class ApprovalRecordModel(Base):
    __tablename__ = "approval_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_type = Column(String(100), nullable=False)
    item_id = Column(Integer, nullable=True)
    decision = Column(String(50), nullable=False)
    reasons_json = Column(Text, default="[]")
    confidence_score = Column(Float, default=0.0)
    reviewed_at = Column(DateTime, default=_utcnow, nullable=False)

    @property
    def reasons(self) -> list[str]:
        return json.loads(self.reasons_json) if self.reasons_json else []

    @reasons.setter
    def reasons(self, value: list[str]) -> None:
        self.reasons_json = json.dumps(value)


class ActivityLogModel(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_name = Column(String(100), nullable=False)
    action_type = Column(String(100), nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_utcnow, nullable=False)


class DashboardSnapshotModel(Base):
    __tablename__ = "dashboard_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_date = Column(DateTime, default=_utcnow, nullable=False)
    snapshot_json = Column(Text, nullable=False, default="{}")
    created_at = Column(DateTime, default=_utcnow, nullable=False)
