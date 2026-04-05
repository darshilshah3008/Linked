"""Orchestrator Agent.

Routes user requests to task agents, combines outputs,
generates the daily action dashboard with ranked jobs,
contacts, companies, outreach drafts, and content suggestions.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from loguru import logger

from src.agents.company_targeting import CompanyTargetingAgent
from src.agents.content_agent import ContentAgent
from src.agents.lead_finder import LeadFinderAgent
from src.agents.outreach_agent import OutreachAgent
from src.agents.people_finder import PeopleFinderAgent
from src.db.init_db import get_session
from src.db.repository import Repository
from src.schemas.actions import ActionItem, DailyPlan, DashboardSnapshot
from src.services.content_planner import generate_content_ideas
from src.services.outreach_personalizer import draft_outreach_message


class OrchestratorAgent:
    """Central orchestrator that coordinates all task agents and builds the dashboard."""

    AGENT_NAME = "orchestrator"

    def __init__(self) -> None:
        self.lead_finder = LeadFinderAgent()
        self.people_finder = PeopleFinderAgent()
        self.company_targeting = CompanyTargetingAgent()
        self.content_agent = ContentAgent()
        self.outreach_agent = OutreachAgent()

    def daily_plan(self) -> DailyPlan:
        """Generate today's recommended action plan based on current CRM state."""
        session = get_session()
        repo = Repository(session)

        new_leads_count = repo.count_leads(status="new")
        reviewed_leads_count = repo.count_leads(status="reviewed")
        draft_content_count = repo.count_content(status="draft")
        pending_outreach_count = repo.count_outreach(status="pending")

        actions: list[ActionItem] = []

        if new_leads_count < 5:
            actions.append(
                ActionItem(
                    action_type="find_leads",
                    description="Find new job leads — current pipeline has fewer than 5 new leads.",
                    priority=2,
                    requires_approval=False,
                )
            )

        if new_leads_count > 0:
            leads = repo.list_leads(status="new", limit=5)
            for lead in leads:
                actions.append(
                    ActionItem(
                        action_type="review_lead",
                        description=f"Review lead: {lead.title} at {lead.company} (score: {lead.relevance_score:.0f})",
                        priority=3,
                        target_id=lead.id,
                        target_type="lead",
                        requires_approval=False,
                    )
                )

        leads_with_companies = repo.list_leads(limit=20)
        researched_names = {c.name for c in repo.list_companies()}
        unresearched = {
            lead.company
            for lead in leads_with_companies
            if lead.company not in researched_names
        }
        for company_name in list(unresearched)[:3]:
            actions.append(
                ActionItem(
                    action_type="research_company",
                    description=f"Research company: {company_name}",
                    priority=4,
                    requires_approval=False,
                )
            )

        if draft_content_count < 3:
            actions.append(
                ActionItem(
                    action_type="draft_content",
                    description="Create new content drafts — fewer than 3 drafts in queue.",
                    priority=5,
                    requires_approval=True,
                )
            )

        if reviewed_leads_count > 0 and pending_outreach_count < 3:
            actions.append(
                ActionItem(
                    action_type="draft_outreach",
                    description="Draft outreach messages for top reviewed leads.",
                    priority=4,
                    requires_approval=True,
                )
            )

        actions.sort(key=lambda x: x.priority)

        plan = DailyPlan(
            date=datetime.now(timezone.utc),
            actions=actions,
            summary=self._build_summary(
                new_leads_count, len(unresearched), draft_content_count, pending_outreach_count
            ),
            leads_to_review=new_leads_count,
            companies_to_research=len(unresearched),
            content_to_create=max(0, 3 - draft_content_count),
            outreach_to_send=pending_outreach_count,
        )

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="daily_plan",
            summary=f"Generated daily plan with {len(actions)} actions.",
        )

        session.close()
        return plan

    def build_dashboard(self) -> DashboardSnapshot:
        """Build the complete daily action dashboard.

        Gathers data from DB (runs agents if DB is empty),
        then assembles the full dashboard snapshot.
        """
        session = get_session()
        repo = Repository(session)

        # ── Gather leads ──────────────────────────────────
        leads = repo.list_leads(limit=200)
        if not leads:
            session.close()
            logger.info("No leads in DB. Running lead finder...")
            self.lead_finder.run(limit=200)
            session = get_session()
            repo = Repository(session)
            leads = repo.list_leads(limit=200)

        top_jobs = []
        for lead in leads:
            top_jobs.append({
                "title": lead.title,
                "company": lead.company,
                "location": lead.location or "N/A",
                "source": lead.source,
                "url": lead.url,
                "fit_score": lead.relevance_score,
                "confidence": lead.confidence or "medium",
                "match_reasons": lead.match_reasons,
                "missing_requirements": lead.missing_requirements,
                "description": lead.description_snippet,
            })

        # ── Gather contacts ───────────────────────────────
        contacts = repo.list_contacts_by_priority(limit=200)
        if not contacts:
            session.close()
            logger.info("No contacts in DB. Running people finder...")
            self.people_finder.run(limit=200)
            session = get_session()
            repo = Repository(session)
            contacts = repo.list_contacts_by_priority(limit=200)

        top_people = []
        for c in contacts:
            top_people.append({
                "name": c.name,
                "role": c.role,
                "company": c.company,
                "profile_url": c.profile_url or c.linkedin_url,
                "linkedin_url": c.linkedin_url,
                "relevance_reason": c.relevance_reason,
                "contact_priority": c.contact_priority or "medium",
                "suggested_outreach_type": c.suggested_outreach_type,
            })

        # ── Gather companies ──────────────────────────────
        companies = repo.list_companies(limit=200)
        if not companies:
            session.close()
            logger.info("No companies in DB. Running company targeting...")
            self.company_targeting.research_all()
            session = get_session()
            repo = Repository(session)
            companies = repo.list_companies(limit=200)

        relevance_order = {"high": 0, "medium": 1, "low": 2, "unknown": 3}
        companies_sorted = sorted(
            companies,
            key=lambda c: relevance_order.get(c.embedded_relevance or "unknown", 3),
        )

        top_companies = []
        for co in companies_sorted:
            top_companies.append({
                "name": co.name,
                "careers_url": co.careers_url,
                "industry": co.industry,
                "embedded_relevance": co.embedded_relevance,
                "summary": co.summary,
                "research_notes": co.research_notes,
                "suggested_next_step": co.suggested_next_step,
            })

        # ── Generate outreach drafts ──────────────────────
        outreach_drafts = []
        # 3 recruiter messages
        for i, lead in enumerate(leads[:3]):
            msg = draft_outreach_message(
                message_type="recruiter_intro",
                lead_title=lead.title,
                company_name=lead.company,
                company_summary=None,
                lead_id=lead.id,
            )
            outreach_drafts.append({
                "message_type": "recruiter_intro",
                "company": lead.company,
                "lead_title": lead.title,
                "draft_text": msg.draft_text,
            })

        # 3 hiring manager messages
        for i, lead in enumerate(leads[:3]):
            msg = draft_outreach_message(
                message_type="hiring_manager_intro",
                lead_title=lead.title,
                company_name=lead.company,
                company_summary=None,
                lead_id=lead.id,
            )
            outreach_drafts.append({
                "message_type": "hiring_manager_intro",
                "company": lead.company,
                "lead_title": lead.title,
                "draft_text": msg.draft_text,
            })

        # 3 connection notes
        for i, lead in enumerate(leads[:3]):
            msg = draft_outreach_message(
                message_type="connection_note",
                lead_title=lead.title,
                company_name=lead.company,
                company_summary=None,
                lead_id=lead.id,
            )
            outreach_drafts.append({
                "message_type": "connection_note",
                "company": lead.company,
                "lead_title": lead.title,
                "draft_text": msg.draft_text,
            })

        # ── Content suggestions (comments + post) ────────
        comment_ideas = generate_content_ideas("embedded debugging", count=3)
        comment_ideas += generate_content_ideas("can j1939", count=2)
        comments_to_write = []
        for idea in comment_ideas[:5]:
            comments_to_write.append({
                "theme": idea.theme,
                "content_type": "comment_draft",
                "hook": idea.hook,
                "full_text": idea.full_text,
            })

        post_ideas = generate_content_ideas("embedded cicd", count=1)
        linkedin_post_draft = None
        if post_ideas:
            p = post_ideas[0]
            linkedin_post_draft = {
                "theme": p.theme,
                "content_type": "linkedin_post",
                "hook": p.hook,
                "outline": p.outline,
                "full_text": p.full_text,
            }

        # ── Build snapshot ────────────────────────────────
        summary_parts = []
        summary_parts.append(f"{len(top_jobs)} jobs ranked")
        summary_parts.append(f"{len(top_people)} contacts identified")
        summary_parts.append(f"{len(top_companies)} companies tracked")
        summary_parts.append(f"{len(outreach_drafts)} outreach drafts ready")
        summary = "Dashboard: " + ", ".join(summary_parts) + "."

        snapshot = DashboardSnapshot(
            date=datetime.now(timezone.utc),
            top_jobs=top_jobs,
            top_people=top_people,
            top_companies=top_companies,
            outreach_drafts=outreach_drafts,
            comments_to_write=comments_to_write,
            linkedin_post_draft=linkedin_post_draft,
            summary=summary,
        )

        # Save snapshot to DB
        repo.save_dashboard_snapshot(snapshot.model_dump_json())

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="build_dashboard",
            summary=summary,
        )

        session.close()
        return snapshot

    def _build_summary(
        self,
        new_leads: int,
        unresearched: int,
        draft_content: int,
        pending_outreach: int,
    ) -> str:
        parts = []
        if new_leads > 0:
            parts.append(f"{new_leads} new leads to review")
        if unresearched > 0:
            parts.append(f"{unresearched} companies to research")
        if draft_content < 3:
            parts.append("content queue needs replenishing")
        if pending_outreach > 0:
            parts.append(f"{pending_outreach} outreach messages pending approval")

        if not parts:
            return "All caught up. Consider finding new leads or creating content."

        return "Today's priorities: " + "; ".join(parts) + "."
