"""Tests for content draft creation."""

from src.schemas.content import ContentInput, ContentPlan
from src.services.content_planner import (
    TOPIC_BUCKETS,
    generate_content_ideas,
    generate_weekly_plan,
)


class TestContentPlanner:
    def test_generate_content_ideas_returns_correct_count(self):
        ideas = generate_content_ideas("embedded debugging", count=3)
        assert len(ideas) == 3

    def test_content_ideas_have_required_fields(self):
        ideas = generate_content_ideas("rtos design", count=1)
        idea = ideas[0]
        assert isinstance(idea, ContentInput)
        assert idea.theme == "rtos design"
        assert idea.content_type == "linkedin_post"
        assert idea.hook is not None

    def test_generate_weekly_plan(self):
        plan = generate_weekly_plan(week_number=1, posts_per_week=3)
        assert isinstance(plan, ContentPlan)
        assert plan.week_number == 1
        assert len(plan.items) == 3

    def test_weekly_plan_rotates_themes(self):
        plan1 = generate_weekly_plan(week_number=1, posts_per_week=3)
        plan2 = generate_weekly_plan(week_number=2, posts_per_week=3)
        themes1 = {item.theme for item in plan1.items}
        themes2 = {item.theme for item in plan2.items}
        # Weeks should have different themes (unless bucket count is very small)
        assert themes1 != themes2 or len(TOPIC_BUCKETS) <= 3

    def test_fallback_for_unknown_theme(self):
        ideas = generate_content_ideas("quantum computing", count=1)
        assert len(ideas) == 1
        assert ideas[0].hook is not None

    def test_embedded_cicd_has_full_text(self):
        ideas = generate_content_ideas("embedded cicd", count=1)
        assert ideas[0].full_text is not None
        assert len(ideas[0].full_text) > 100
