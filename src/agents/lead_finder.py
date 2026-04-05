"""Lead Finder Agent.

Finds embedded software job leads from configured sources,
scores them for relevance (0-100), and persists them to the CRM layer.
Returns structured results with explainability.
"""

from __future__ import annotations

from loguru import logger

from src.config import get_settings
from src.db.init_db import get_session
from src.db.repository import Repository
from src.schemas.lead import LeadRecord
from src.services.lead_sources import get_lead_sources
from src.services.scoring import score_lead


class LeadFinderAgent:
    """Agent responsible for finding and scoring job leads."""

    AGENT_NAME = "lead_finder"

    def __init__(self) -> None:
        self.settings = get_settings()
        self.sources = get_lead_sources()

    def run(self, limit: int = 20) -> list[LeadRecord]:
        """Find leads from all configured sources, score and persist them.

        Returns the top leads sorted by fit score (0-100).
        """
        session = get_session()
        repo = Repository(session)

        keywords = self.settings.lead_keywords_list
        all_leads: list[LeadRecord] = []

        for source in self.sources:
            logger.info(f"Fetching leads from source: {source.source_name}")
            try:
                raw_leads = source.fetch_leads(keywords)
            except Exception as e:
                logger.error(f"Error fetching from {source.source_name}: {e}")
                continue

            for lead_input in raw_leads:
                score_result = score_lead(lead_input)
                logger.debug(
                    f"Scored lead: {lead_input.title} at {lead_input.company} "
                    f"-> {score_result.score}/100 ({score_result.confidence})"
                )

                model = repo.create_lead(lead_input, score_result)

                all_leads.append(
                    LeadRecord(
                        id=model.id,
                        title=model.title,
                        company=model.company,
                        location=model.location,
                        source=model.source,
                        url=model.url,
                        date_seen=model.date_seen,
                        description_snippet=model.description_snippet,
                        relevance_score=model.relevance_score,
                        match_reasons=model.match_reasons,
                        missing_requirements=model.missing_requirements,
                        confidence=model.confidence or "medium",
                        status=model.status,
                    )
                )

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="find_leads",
            summary=f"Found {len(all_leads)} leads from {len(self.sources)} sources.",
        )

        session.close()

        all_leads.sort(key=lambda x: x.relevance_score, reverse=True)
        return all_leads[:limit]
