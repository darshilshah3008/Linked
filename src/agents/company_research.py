"""Company Research Agent.

Researches companies using configured sources and persists
structured summaries to the CRM layer.
"""

from __future__ import annotations

from loguru import logger

from src.db.init_db import get_session
from src.db.repository import Repository
from src.schemas.company import CompanyRecord
from src.services.research_sources import get_research_source


class CompanyResearchAgent:
    """Agent responsible for researching companies."""

    AGENT_NAME = "company_research"

    def __init__(self) -> None:
        self.source = get_research_source()

    def research(self, company_name: str) -> CompanyRecord | None:
        """Research a company and persist the results.

        Returns the company record, or None if research failed.
        """
        session = get_session()
        repo = Repository(session)

        # Check if already researched
        existing = repo.get_company_by_name(company_name)
        if existing:
            logger.info(f"Company already researched: {company_name}. Updating.")

        logger.info(f"Researching company: {company_name}")
        company_input = self.source.research(company_name)

        if company_input is None:
            logger.warning(f"No research data found for: {company_name}")
            repo.log_activity(
                agent_name=self.AGENT_NAME,
                action_type="research_company",
                summary=f"No data found for {company_name}.",
            )
            session.close()
            return None

        if existing:
            repo.update_company(
                existing.id,
                website=company_input.website,
                careers_url=company_input.careers_url,
                industry=company_input.industry,
                summary=company_input.summary,
                embedded_relevance=company_input.embedded_relevance,
                research_notes=company_input.research_notes,
                source_url=company_input.source_url,
                suggested_next_step=company_input.suggested_next_step,
            )
            model = repo.get_company_by_name(company_name)
        else:
            model = repo.create_company(company_input)

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="research_company",
            summary=f"Researched {company_name}: relevance={company_input.embedded_relevance}.",
        )

        result = CompanyRecord(
            id=model.id,
            name=model.name,
            website=model.website,
            careers_url=model.careers_url,
            industry=model.industry,
            summary=model.summary,
            embedded_relevance=model.embedded_relevance,
            research_notes=model.research_notes,
            source_url=model.source_url,
            suggested_next_step=model.suggested_next_step,
            last_researched=model.last_researched,
        )

        session.close()
        return result
