"""Content Agent.

Generates LinkedIn content drafts, weekly plans, and engagement
suggestions based on the user's embedded engineering background.
"""

from __future__ import annotations

from loguru import logger

from src.db.init_db import get_session
from src.db.repository import Repository
from src.schemas.content import ContentPlan, ContentRecord
from src.services.content_planner import (
    generate_content_ideas,
    generate_weekly_plan,
)


class ContentAgent:
    """Agent responsible for generating content drafts and plans."""

    AGENT_NAME = "content_agent"

    def draft_content(self, theme: str, count: int = 3) -> list[ContentRecord]:
        """Generate content ideas for a theme and persist them.

        Returns created content records.
        """
        session = get_session()
        repo = Repository(session)

        ideas = generate_content_ideas(theme, count=count)
        records: list[ContentRecord] = []

        for idea in ideas:
            model = repo.create_content(idea)
            records.append(
                ContentRecord(
                    id=model.id,
                    theme=model.theme,
                    content_type=model.content_type,
                    hook=model.hook,
                    outline=model.outline,
                    full_text=model.full_text,
                    status=model.status,
                    created_at=model.created_at,
                )
            )
            logger.debug(f"Created content draft: {idea.theme} - {idea.hook[:50] if idea.hook else 'no hook'}")

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="draft_content",
            summary=f"Generated {len(records)} content ideas for theme: {theme}.",
        )

        session.close()
        return records

    def create_weekly_plan(self, week_number: int) -> ContentPlan:
        """Generate a weekly content plan."""
        plan = generate_weekly_plan(week_number)

        session = get_session()
        repo = Repository(session)

        # Persist plan items
        for item in plan.items:
            repo.create_content(item)

        repo.log_activity(
            agent_name=self.AGENT_NAME,
            action_type="weekly_plan",
            summary=f"Created week {week_number} content plan with {len(plan.items)} items.",
        )

        session.close()
        logger.info(f"Weekly plan generated for week {week_number}.")
        return plan

    def create_30_day_calendar(self) -> list[ContentPlan]:
        """Generate a 30-day (4-week) content calendar."""
        plans: list[ContentPlan] = []
        for week in range(1, 5):
            plan = self.create_weekly_plan(week)
            plans.append(plan)
        logger.info("30-day content calendar generated.")
        return plans
