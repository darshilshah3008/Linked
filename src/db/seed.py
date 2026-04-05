"""Seed the database with sample data."""

from __future__ import annotations

import json
from pathlib import Path

from loguru import logger

from src.db.init_db import get_session, init_db
from src.db.repository import Repository
from src.schemas.company import CompanyInput
from src.schemas.lead import LeadInput
from src.services.scoring import score_lead

_SEEDS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "seeds"


def seed_database() -> None:
    """Seed database with sample data from JSON files."""
    init_db()
    session = get_session()
    repo = Repository(session)

    _seed_leads(repo)
    _seed_companies(repo)

    session.close()
    logger.info("Database seeded successfully.")


def _seed_leads(repo: Repository) -> None:
    leads_file = _SEEDS_DIR / "sample_leads.json"
    if not leads_file.exists():
        logger.warning(f"Seed file not found: {leads_file}")
        return

    with open(leads_file, "r", encoding="utf-8") as f:
        leads_data = json.load(f)

    for entry in leads_data:
        lead_input = LeadInput(**entry)
        score_result = score_lead(lead_input)
        repo.create_lead(lead_input, score_result)
        logger.debug(f"Seeded lead: {lead_input.title} at {lead_input.company}")

    logger.info(f"Seeded {len(leads_data)} leads.")


def _seed_companies(repo: Repository) -> None:
    companies_file = _SEEDS_DIR / "sample_companies.json"
    if not companies_file.exists():
        logger.warning(f"Seed file not found: {companies_file}")
        return

    with open(companies_file, "r", encoding="utf-8") as f:
        companies_data = json.load(f)

    for entry in companies_data:
        company_input = CompanyInput(**entry)
        existing = repo.get_company_by_name(company_input.name)
        if not existing:
            repo.create_company(company_input)
            logger.debug(f"Seeded company: {company_input.name}")

    logger.info(f"Seeded {len(companies_data)} companies.")
