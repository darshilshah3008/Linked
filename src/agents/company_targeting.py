"""Company Targeting Agent.

Researches a set of target companies, stores structured data
with careers URLs and recommendations, and returns ranked results.
"""

from __future__ import annotations

from loguru import logger

from src.db.init_db import get_session
from src.db.repository import Repository
from src.schemas.company import CompanyRecord
from src.services.research_sources import get_research_source


# Default target companies for embedded software job search
# Includes original core targets + H1B sponsor companies from CSV
TARGET_COMPANIES = [
    # Core ag/industrial/vehicle targets
    "Deere & Company",
    "CNH Industrial",
    "Bosch",
    "Continental",
    "AGCO Corporation",
    "Caterpillar",
    "Siemens",
    "Rockwell Automation",
    "Parker Hannifin",
    "Honeywell",
    "Oshkosh Corporation",
    "Medtronic",
    # Semiconductor / Chip
    "Qualcomm",
    "Intel",
    "Texas Instruments",
    "Analog Devices",
    "Infineon",
    "Micron Technology",
    "Western Digital",
    "Seagate Technology",
    "Broadcom",
    "Synaptics",
    "Synopsys",
    "Samsung Semiconductor",
    "ARM",
    # Automotive
    "Aptiv",
    "Ford Motor Company",
    "General Motors",
    "Magna International",
    "Cummins",
    "Tesla",
    "Lucid Motors",
    "ZF Group",
    # Aerospace & Defense
    "Boeing",
    "Lockheed Martin",
    "Raytheon Technologies",
    "Northrop Grumman",
    "GE Aerospace",
    # Robotics & Consumer HW
    "Boston Dynamics",
    "iRobot",
    "DJI",
    "Sony",
    "Panasonic",
    "Hitachi",
    "ABB",
    "Ericsson",
    # Networking
    "Cisco Systems",
    "Arista Networks",
    "Juniper Networks",
    # Big Tech (embedded teams)
    "Apple",
    "Google",
    "Meta",
    "Microsoft",
    "Amazon",
    # Cloud / Infra
    "IBM",
    "Oracle",
    "VMware",
    "Red Hat",
    "Lumen Technologies",
    # ── H1B CSV companies (software/consulting/other) ──
    "Accenture",
    "Adobe",
    "Airbnb",
    "Anthropic",
    "Atlassian",
    "Bloomberg",
    "Canva",
    "Capgemini",
    "Cognizant Technology Solutions",
    "Databricks",
    "Deloitte",
    "Dropbox",
    "Elastic",
    "Electronic Arts",
    "Epic Games",
    "Ernst & Young (EY)",
    "Figma",
    "Gusto",
    "HCL Technologies",
    "Infosys",
    "John Deere",
    "LinkedIn",
    "Lyft",
    "MongoDB",
    "PayPal",
    "QVC",
    "SanDisk",
    "Savant",
    "SoftBank",
    "Symantec",
    "TikTok",
    "Twilio",
    "Uber",
    "Unity Technologies",
    "Wayfair",
    "Wipro",
    "Zillow",
]

RELEVANCE_ORDER = {"high": 0, "medium": 1, "low": 2, "unknown": 3}


class CompanyTargetingAgent:
    """Agent that researches and ranks target companies."""

    AGENT_NAME = "company_targeting"

    def __init__(self) -> None:
        self.source = get_research_source()

    def research_all(self) -> list[CompanyRecord]:
        """Research all target companies and return ranked results."""
        session = get_session()
        repo = Repository(session)

        results: list[CompanyRecord] = []

        for company_name in TARGET_COMPANIES:
            logger.info(f"Researching target company: {company_name}")
            company_input = self.source.research(company_name)
            if company_input is None:
                continue

            existing = repo.get_company_by_name(company_name)
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

            results.append(
                CompanyRecord(
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
            )

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="research_companies",
            summary=f"Researched {len(results)} target companies.",
        )

        session.close()

        # Sort by relevance: high > medium > low > unknown
        results.sort(key=lambda c: RELEVANCE_ORDER.get(c.embedded_relevance or "unknown", 3))

        return results
