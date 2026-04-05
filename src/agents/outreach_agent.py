"""Outreach Agent.

Creates personalized outreach message drafts based on lead
and company context. All messages are drafts only — human
approval is required before sending.
"""

from __future__ import annotations

from loguru import logger

from src.agents.approval import ApprovalAgent
from src.db.init_db import get_session
from src.db.repository import Repository
from src.schemas.approval import ApprovalRequest
from src.schemas.outreach import OutreachRecord
from src.services.outreach_personalizer import draft_outreach_message


class OutreachAgent:
    """Agent responsible for drafting outreach messages."""

    AGENT_NAME = "outreach_agent"

    def __init__(self) -> None:
        self.approval_agent = ApprovalAgent()

    def draft_outreach(
        self,
        lead_id: int,
        message_type: str = "recruiter_intro",
    ) -> OutreachRecord | None:
        """Draft an outreach message for a lead and submit for approval.

        Returns the outreach record with approval status.
        """
        session = get_session()
        repo = Repository(session)

        # Load lead context
        lead = repo.get_lead(lead_id)
        if not lead:
            logger.error(f"Lead not found: {lead_id}")
            session.close()
            return None

        # Load company context if available
        company = repo.get_company_by_name(lead.company)
        company_summary = company.summary if company else None
        company_id = company.id if company else None

        # Generate draft
        outreach_input = draft_outreach_message(
            message_type=message_type,
            lead_title=lead.title,
            company_name=lead.company,
            company_summary=company_summary,
            lead_id=lead.id,
            company_id=company_id,
        )

        # Submit for approval
        approval_request = ApprovalRequest(
            item_type="outreach",
            content_text=outreach_input.draft_text,
            metadata={
                "message_type": message_type,
                "company": lead.company,
                "lead_title": lead.title,
            },
        )
        approval_decision = self.approval_agent.review(approval_request)

        # Persist outreach
        model = repo.create_outreach(
            outreach_input,
            confidence=approval_decision.confidence_score,
        )

        # Update approval status
        repo.update_outreach_approval(model.id, approval_decision.decision)

        # Save approval record
        repo.create_approval(
            item_type="outreach",
            item_id=model.id,
            decision=approval_decision,
        )

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="draft_outreach",
            summary=(
                f"Drafted {message_type} for {lead.company} — "
                f"approval: {approval_decision.decision} "
                f"(confidence: {approval_decision.confidence_score})"
            ),
        )

        session.close()

        return OutreachRecord(
            id=model.id,
            contact_id=model.contact_id,
            company_id=model.company_id,
            lead_id=model.lead_id,
            message_type=model.message_type,
            draft_text=model.draft_text,
            approval_status=approval_decision.decision,
            confidence_score=approval_decision.confidence_score,
            created_at=model.created_at,
        )
