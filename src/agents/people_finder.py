"""People Finder Agent.

Discovers relevant contacts at target companies and persists
them to the contacts table. Returns ranked contacts for outreach.
"""

from __future__ import annotations

from loguru import logger

from src.db.init_db import get_session
from src.db.repository import Repository
from src.schemas.outreach import ContactRecord
from src.services.people_sources import get_people_source


# Target companies for people discovery
# Includes original core targets + H1B sponsor companies from CSV
TARGET_COMPANIES = [
    # Core ag/industrial/vehicle targets
    "Deere & Company",
    "CNH Industrial",
    "Caterpillar",
    "Bosch",
    "Continental",
    "AGCO Corporation",
    "Rockwell Automation",
    "Siemens",
    "Parker Hannifin",
    "Honeywell",
    "Oshkosh Corporation",
    # Semiconductor / Chip
    "Qualcomm",
    "Intel",
    "Texas Instruments",
    "Analog Devices",
    "Infineon",
    "Broadcom",
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
    "DJI",
    "ABB",
    # Networking
    "Cisco Systems",
    "Arista Networks",
    # Big Tech (embedded teams)
    "Apple",
    "Google",
    "Meta",
    "Amazon",
]


class PeopleFinderAgent:
    """Agent responsible for discovering and ranking contacts."""

    AGENT_NAME = "people_finder"

    def __init__(self) -> None:
        self.source = get_people_source()

    def run(self, limit: int = 20) -> list[ContactRecord]:
        """Find people at target companies, persist, and return ranked list."""
        session = get_session()
        repo = Repository(session)

        all_contacts: list[ContactRecord] = []

        for company in TARGET_COMPANIES:
            logger.info(f"Finding people at: {company}")
            try:
                people = self.source.find_people(company)
            except Exception as e:
                logger.error(f"Error finding people at {company}: {e}")
                continue

            for contact_input in people:
                # Check if already exists
                existing = repo.get_contact_by_name_company(
                    contact_input.name, contact_input.company or ""
                )
                if existing:
                    logger.debug(f"Contact already exists: {contact_input.name} at {contact_input.company}")
                    all_contacts.append(
                        ContactRecord(
                            id=existing.id,
                            name=existing.name,
                            role=existing.role,
                            company=existing.company,
                            linkedin_url=existing.linkedin_url,
                            profile_url=existing.profile_url,
                            source=existing.source,
                            notes=existing.notes,
                            relevance_reason=existing.relevance_reason,
                            contact_priority=existing.contact_priority or "medium",
                            suggested_outreach_type=existing.suggested_outreach_type,
                            relationship_stage=existing.relationship_stage,
                        )
                    )
                    continue

                model = repo.create_contact(contact_input)
                all_contacts.append(
                    ContactRecord(
                        id=model.id,
                        name=model.name,
                        role=model.role,
                        company=model.company,
                        linkedin_url=model.linkedin_url,
                        profile_url=model.profile_url,
                        source=model.source,
                        notes=model.notes,
                        relevance_reason=model.relevance_reason,
                        contact_priority=model.contact_priority or "medium",
                        suggested_outreach_type=model.suggested_outreach_type,
                        relationship_stage=model.relationship_stage,
                    )
                )

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="find_people",
            summary=f"Discovered {len(all_contacts)} contacts across {len(TARGET_COMPANIES)} companies.",
        )

        session.close()

        # Sort by priority: high > medium > low
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_contacts.sort(key=lambda c: priority_order.get(c.contact_priority, 1))

        return all_contacts[:limit]
