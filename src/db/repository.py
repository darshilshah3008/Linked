"""Repository layer for CRUD operations on all entities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from src.db.models import (
    ActivityLogModel,
    ApprovalRecordModel,
    ApplicationModel,
    CompanyModel,
    ContactModel,
    ContentItemModel,
    DashboardSnapshotModel,
    LeadModel,
    OutreachMessageModel,
)
from src.schemas.actions import ApplicationInput
from src.schemas.approval import ApprovalDecision
from src.schemas.company import CompanyInput
from src.schemas.content import ContentInput
from src.schemas.lead import LeadInput, LeadScoreResult
from src.schemas.outreach import ContactInput, OutreachInput


class Repository:
    """Unified repository for all CRM entities."""

    def __init__(self, session: Session) -> None:
        self.session = session

    # ── Leads ──────────────────────────────────────────────

    def create_lead(self, lead: LeadInput, score: LeadScoreResult | None = None) -> LeadModel:
        """Create a new lead record."""
        model = LeadModel(
            title=lead.title,
            company=lead.company,
            location=lead.location,
            source=lead.source,
            url=lead.url,
            description_snippet=lead.description_snippet,
            relevance_score=score.score if score else 0.0,
            match_reasons_json=json.dumps(score.inferred_match_reasons if score else []),
            missing_requirements_json=json.dumps(score.missing_requirements if score else []),
            confidence=score.confidence if score else "medium",
            status="new",
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_lead(self, lead_id: int) -> LeadModel | None:
        return self.session.query(LeadModel).filter(LeadModel.id == lead_id).first()

    def list_leads(self, status: str | None = None, limit: int = 50) -> list[LeadModel]:
        q = self.session.query(LeadModel)
        if status:
            q = q.filter(LeadModel.status == status)
        return q.order_by(LeadModel.relevance_score.desc()).limit(limit).all()

    def update_lead_status(self, lead_id: int, status: str) -> LeadModel | None:
        lead = self.get_lead(lead_id)
        if lead:
            lead.status = status
            self.session.commit()
        return lead

    # ── Companies ──────────────────────────────────────────

    def create_company(self, company: CompanyInput) -> CompanyModel:
        model = CompanyModel(
            name=company.name,
            website=company.website,
            careers_url=company.careers_url,
            industry=company.industry,
            summary=company.summary,
            embedded_relevance=company.embedded_relevance,
            research_notes=company.research_notes,
            source_url=company.source_url,
            suggested_next_step=company.suggested_next_step,
            last_researched=datetime.now(timezone.utc),
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_company_by_name(self, name: str) -> CompanyModel | None:
        return self.session.query(CompanyModel).filter(CompanyModel.name == name).first()

    def list_companies(self, limit: int = 200) -> list[CompanyModel]:
        return self.session.query(CompanyModel).limit(limit).all()

    def update_company(self, company_id: int, **kwargs) -> CompanyModel | None:
        company = self.session.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if company:
            for key, value in kwargs.items():
                if hasattr(company, key):
                    setattr(company, key, value)
            company.last_researched = datetime.now(timezone.utc)
            self.session.commit()
        return company

    # ── Contacts ───────────────────────────────────────────

    def create_contact(self, contact: ContactInput) -> ContactModel:
        model = ContactModel(
            name=contact.name,
            role=contact.role,
            company=contact.company,
            linkedin_url=contact.linkedin_url,
            profile_url=contact.profile_url,
            source=contact.source,
            notes=contact.notes,
            relevance_reason=contact.relevance_reason,
            contact_priority=contact.contact_priority,
            suggested_outreach_type=contact.suggested_outreach_type,
            relationship_stage=contact.relationship_stage,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_contact_by_name_company(self, name: str, company: str) -> ContactModel | None:
        return (
            self.session.query(ContactModel)
            .filter(ContactModel.name == name, ContactModel.company == company)
            .first()
        )

    def list_contacts(self, limit: int = 50) -> list[ContactModel]:
        return self.session.query(ContactModel).limit(limit).all()

    def list_contacts_by_priority(self, limit: int = 20) -> list[ContactModel]:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        contacts = self.session.query(ContactModel).all()
        contacts.sort(key=lambda c: priority_order.get(c.contact_priority or "medium", 1))
        return contacts[:limit]

    # ── Applications ───────────────────────────────────────

    def create_application(self, app: ApplicationInput) -> ApplicationModel:
        model = ApplicationModel(
            lead_id=app.lead_id,
            applied_date=app.applied_date or datetime.now(timezone.utc),
            resume_version=app.resume_version,
            status=app.status,
            notes=app.notes,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def list_applications(self, limit: int = 50) -> list[ApplicationModel]:
        return self.session.query(ApplicationModel).limit(limit).all()

    # ── Outreach ───────────────────────────────────────────

    def create_outreach(self, outreach: OutreachInput, confidence: float = 0.0) -> OutreachMessageModel:
        model = OutreachMessageModel(
            contact_id=outreach.contact_id,
            company_id=outreach.company_id,
            lead_id=outreach.lead_id,
            message_type=outreach.message_type,
            draft_text=outreach.draft_text,
            confidence_score=confidence,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def update_outreach_approval(self, outreach_id: int, status: str) -> OutreachMessageModel | None:
        msg = (
            self.session.query(OutreachMessageModel)
            .filter(OutreachMessageModel.id == outreach_id)
            .first()
        )
        if msg:
            msg.approval_status = status
            self.session.commit()
        return msg

    def list_outreach(self, status: str | None = None, limit: int = 50) -> list[OutreachMessageModel]:
        q = self.session.query(OutreachMessageModel)
        if status:
            q = q.filter(OutreachMessageModel.approval_status == status)
        return q.order_by(OutreachMessageModel.created_at.desc()).limit(limit).all()

    # ── Content ────────────────────────────────────────────

    def create_content(self, content: ContentInput) -> ContentItemModel:
        model = ContentItemModel(
            theme=content.theme,
            content_type=content.content_type,
            hook=content.hook,
            outline=content.outline,
            full_text=content.full_text,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def list_content(self, status: str | None = None, limit: int = 50) -> list[ContentItemModel]:
        q = self.session.query(ContentItemModel)
        if status:
            q = q.filter(ContentItemModel.status == status)
        return q.order_by(ContentItemModel.created_at.desc()).limit(limit).all()

    def update_content_status(self, content_id: int, status: str) -> ContentItemModel | None:
        item = (
            self.session.query(ContentItemModel)
            .filter(ContentItemModel.id == content_id)
            .first()
        )
        if item:
            item.status = status
            self.session.commit()
        return item

    # ── Approvals ──────────────────────────────────────────

    def create_approval(
        self, item_type: str, item_id: int | None, decision: ApprovalDecision
    ) -> ApprovalRecordModel:
        model = ApprovalRecordModel(
            item_type=item_type,
            item_id=item_id,
            decision=decision.decision,
            reasons_json=json.dumps(decision.reasons),
            confidence_score=decision.confidence_score,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def list_approvals(self, limit: int = 50) -> list[ApprovalRecordModel]:
        return (
            self.session.query(ApprovalRecordModel)
            .order_by(ApprovalRecordModel.reviewed_at.desc())
            .limit(limit)
            .all()
        )

    # ── Dashboard Snapshots ────────────────────────────────

    def save_dashboard_snapshot(self, snapshot_json: str) -> DashboardSnapshotModel:
        model = DashboardSnapshotModel(snapshot_json=snapshot_json)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_latest_dashboard(self) -> DashboardSnapshotModel | None:
        return (
            self.session.query(DashboardSnapshotModel)
            .order_by(DashboardSnapshotModel.created_at.desc())
            .first()
        )

    # ── Activity Logs ─────────────────────────────────────

    def log_activity(self, agent_name: str, action_type: str, summary: str) -> ActivityLogModel:
        model = ActivityLogModel(
            agent_name=agent_name,
            action_type=action_type,
            summary=summary,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def list_activity_logs(self, limit: int = 50) -> list[ActivityLogModel]:
        return (
            self.session.query(ActivityLogModel)
            .order_by(ActivityLogModel.created_at.desc())
            .limit(limit)
            .all()
        )

    # ── Utility ────────────────────────────────────────────

    def count_leads(self, status: str | None = None) -> int:
        q = self.session.query(LeadModel)
        if status:
            q = q.filter(LeadModel.status == status)
        return q.count()

    def count_content(self, status: str | None = None) -> int:
        q = self.session.query(ContentItemModel)
        if status:
            q = q.filter(ContentItemModel.status == status)
        return q.count()

    def count_outreach(self, status: str | None = None) -> int:
        q = self.session.query(OutreachMessageModel)
        if status:
            q = q.filter(OutreachMessageModel.approval_status == status)
        return q.count()

    def count_contacts(self) -> int:
        return self.session.query(ContactModel).count()
