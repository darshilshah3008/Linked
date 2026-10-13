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
        lead_us = _make_lead(title="Embedded Software Engineer", location="Peoria, IL")
        lead_abroad = _make_lead(title="Embedded Software Engineer", location="Munich, Germany")
        assert score_lead(lead_us).score > score_lead(lead_abroad).score

    def test_any_us_location_is_full_marks(self):
        a = score_lead(_make_lead(title="Embedded Software Engineer", location="Sioux Falls, SD")).score
        b = score_lead(_make_lead(title="Embedded Software Engineer", location="San Jose, CA")).score
        c = score_lead(_make_lead(title="Embedded Software Engineer", location="Detroit, Michigan")).score
        d = score_lead(_make_lead(title="Embedded Software Engineer", location="Remote, USA")).score
        assert a == b == c == d

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


class TestEmbeddedSpecificScoring:
    """Embedded-engineer specific behaviour: no substring false positives, blockers, gaps."""

    def test_no_substring_false_positives(self):
        # "candidates", "Canada", "responsible", "able", "laws", "robust", "digital"
        # used to match CAN, BLE, AWS, Rust and Git.
        lead = _make_lead(
            title="Salesforce Developer",
            description_snippet="Responsible for scalable digital apps; candidates able to "
            "work with our Canada team. Robust knowledge of privacy laws.",
        )
        result = score_lead(lead)
        assert not any("stack" in r.lower() for r in result.inferred_match_reasons)
        assert result.missing_requirements == []
        assert result.score < 30

    def test_can_matches_as_protocol(self):
        lead = _make_lead(title="Embedded Software Engineer", description_snippet="CAN/J1939 and CAN FD networks.")
        reasons = " ".join(score_lead(lead).inferred_match_reasons).lower()
        assert "j1939" in reasons and "can fd" in reasons

    def test_more_stack_overlap_scores_higher(self):
        thin = _make_lead(title="Embedded Software Engineer", description_snippet="Experience with C++.")
        deep = _make_lead(
            title="Embedded Software Engineer",
            description_snippet="Embedded C, FreeRTOS, CAN FD, J1939, Simulink, CAPL, HIL.",
        )
        assert score_lead(deep).score > score_lead(thin).score

    def test_us_citizen_itar_is_blocker_and_capped(self):
        lead = _make_lead(
            title="Senior Embedded Software Engineer",
            location="Sioux Falls, SD",
            description_snippet="CAN, J1939, FreeRTOS, embedded C for military vehicles. "
            "Must be a U.S. citizen due to ITAR.",
        )
        result = score_lead(lead)
        assert result.score <= 30
        assert any(m.startswith("BLOCKER") for m in result.missing_requirements)

    def test_no_sponsorship_is_blocker(self):
        lead = _make_lead(
            title="Firmware Engineer",
            description_snippet="Embedded C on STM32. We will not sponsor work visas.",
        )
        assert any("sponsorship" in m.lower() for m in score_lead(lead).missing_requirements)

    def test_owned_skills_not_flagged_as_gaps(self):
        lead = _make_lead(
            title="Embedded Software Engineer",
            description_snippet="Python, CAN FD, ISO 26262, Simulink, MISRA. AUTOSAR and UDS a plus.",
        )
        gaps = score_lead(lead).missing_requirements
        assert "Python programming" not in gaps and not any("Python" in g for g in gaps)
        assert any("AUTOSAR" in g for g in gaps)
        assert any("UDS" in g for g in gaps)

    def test_non_embedded_title_gets_no_title_credit(self):
        web = _make_lead(title="Full Stack Developer", description_snippet="Embedded analytics dashboards in React.")
        result = score_lead(web)
        assert result.score < 40

    def test_engineer_ii_beats_staff_and_intern(self):
        ii = score_lead(_make_lead(title="Embedded Software Engineer II")).score
        staff = score_lead(_make_lead(title="Staff Embedded Software Engineer")).score
        intern = score_lead(_make_lead(title="Embedded Software Intern")).score
        assert ii > staff > intern

    def test_ag_domain_beats_adjacent_domain(self):
        ag = _make_lead(title="Embedded Software Engineer", description_snippet="Precision agriculture sprayer ECUs.")
        med = _make_lead(title="Embedded Software Engineer", description_snippet="Medical device firmware.")
        assert score_lead(ag).score > score_lead(med).score
