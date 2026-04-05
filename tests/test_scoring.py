"""Tests for the lead relevance scoring module."""

from src.schemas.lead import LeadInput
from src.services.scoring import score_lead


def _make_lead(**overrides) -> LeadInput:
    defaults = {
        "title": "Software Engineer",
        "company": "Acme Corp",
        "location": None,
        "source": "test",
        "url": None,
        "description_snippet": None,
    }
    defaults.update(overrides)
    return LeadInput(**defaults)


class TestScoreLead:
    """Test suite for score_lead function."""

    def test_high_relevance_lead(self):
        lead = _make_lead(
            title="Senior Embedded Software Engineer",
            company="Deere & Company",
            location="Moline, IL",
            description_snippet="CAN/J1939, FreeRTOS, C/C++ required. Agricultural equipment.",
        )
        result = score_lead(lead)
        assert result.score >= 70
        assert result.confidence == "high"
        assert len(result.inferred_match_reasons) > 0

    def test_low_relevance_lead(self):
        lead = _make_lead(
            title="Frontend Web Developer",
            company="Google",
            location="Mountain View, CA",
            description_snippet="React, TypeScript, CSS. Building web applications.",
        )
        result = score_lead(lead)
        assert result.score < 40
        assert result.confidence == "low"

    def test_title_keyword_matching(self):
        lead = _make_lead(title="Firmware Engineer")
        result = score_lead(lead)
        assert any("match" in r.lower() for r in result.inferred_match_reasons)

    def test_seniority_positive(self):
        lead_senior = _make_lead(title="Senior Embedded Software Engineer")
        lead_intern = _make_lead(title="Embedded Software Intern")

        score_senior = score_lead(lead_senior).score
        score_intern = score_lead(lead_intern).score
        assert score_senior > score_intern

    def test_location_match(self):
        lead_wi = _make_lead(
            title="Embedded Software Engineer",
            location="Manitowoc, Wisconsin",
            description_snippet="CAN bus, embedded controls",
        )
        lead_ca = _make_lead(
            title="Embedded Software Engineer",
            location="San Francisco, CA",
        )
        score_wi = score_lead(lead_wi).score
        score_ca = score_lead(lead_ca).score
        assert score_wi > score_ca

    def test_remote_location_scores_well(self):
        lead = _make_lead(
            title="Embedded Software Engineer",
            location="Remote, USA",
        )
        result = score_lead(lead)
        assert any("Location" in r or "location" in r for r in result.inferred_match_reasons)

    def test_observed_facts_present(self):
        lead = _make_lead(
            title="Firmware Engineer",
            location=None,
            url=None,
            description_snippet=None,
        )
        result = score_lead(lead)
        assert len(result.observed_facts) > 0
        assert any("Title" in f for f in result.observed_facts)

    def test_score_bounded_0_to_100(self):
        lead = _make_lead(
            title="Senior Embedded Software Engineer",
            company="Deere & Company",
            location="Remote, USA",
            description_snippet="CAN J1939 FreeRTOS STM32 automotive industrial RTOS embedded C",
        )
        result = score_lead(lead)
        assert 0.0 <= result.score <= 100.0

    def test_deterministic_scoring(self):
        lead = _make_lead(
            title="Embedded Systems Engineer",
            company="Caterpillar",
            description_snippet="CAN/J1939, STM32, RTOS",
        )
        score1 = score_lead(lead)
        score2 = score_lead(lead)
        assert score1.score == score2.score
        assert score1.inferred_match_reasons == score2.inferred_match_reasons

    def test_protocol_keyword_matching(self):
        lead = _make_lead(
            title="Software Engineer",
            description_snippet="Experience with CAN bus, J1939. FreeRTOS preferred.",
        )
        result = score_lead(lead)
        assert any("stack" in r.lower() for r in result.inferred_match_reasons)

    def test_missing_requirements_detected(self):
        lead = _make_lead(
            title="Embedded Software Engineer",
            description_snippet="Must have Python, AWS, and machine learning experience.",
        )
        result = score_lead(lead)
        assert len(result.missing_requirements) > 0
