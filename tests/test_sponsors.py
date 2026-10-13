"""Green card sponsor targeting and the no-disclosure guard."""

from src import profile
from src.agents.approval import ApprovalAgent
from src.schemas.approval import ApprovalRequest
from src.services import sponsors
from src.services.cover_letter import generate_cover_letter
from src.services.resume_tailor import tailor_resume_bullets


def test_known_sponsors_match_name_variants():
    for name in ["Deere & Company", "John Deere", "Robert Bosch LLC", "Caterpillar Inc.",
                 "Honeywell Aerospace", "Texas Instruments Incorporated", "Daimler Truck North America LLC"]:
        assert sponsors.is_recommended(name), name


def test_non_sponsors_are_not_recommended():
    # Few or no recent green card filings, or never checked.
    for name in ["General Motors", "Google", "Lockheed Martin", "Boston Dynamics", "Oshkosh Corporation", "Acme Robotics"]:
        assert not sponsors.is_recommended(name), name


def test_filter_is_on_by_default():
    assert profile.REQUIRE_GREEN_CARD_SPONSOR
    assert not sponsors.allowed("Google")
    assert sponsors.allowed("Cummins")


def test_every_recommended_sponsor_has_a_source():
    recs = sponsors.recommended_companies()
    assert len(recs) > 50
    for c in recs:
        assert c["perm_url"].startswith("https://")
        assert c["perm_recent_2024_2025"] >= 3


def test_approval_rejects_visa_mentions():
    req = ApprovalRequest(
        item_type="outreach_message", item_id=1,
        content_text="Hi Sam, I'd love to join your team. I will need H-1B sponsorship and a green card.",
    )
    decision = ApprovalAgent().review(req)
    assert decision.decision == "rejected"
    assert any("immigration" in i.lower() for i in decision.flagged_issues)


def test_cover_letter_never_mentions_visa():
    out = generate_cover_letter(
        lead_title="Firmware Engineer", company_name="Acme",
        description_snippet="Embedded C on STM32. We will not sponsor visas. Must be a U.S. citizen.",
        match_reasons=["Tech stack overlap: embedded c"],
        missing_requirements=["BLOCKER: No visa sponsorship", "BLOCKER: U.S. citizenship required", "Yocto"],
    )
    assert profile.immigration_mentions(out["cover_letter"]) == []


def test_resume_tailoring_never_mentions_visa():
    out = tailor_resume_bullets(
        "Embedded Software Engineer", "Acme", "CAN, J1939. Visa sponsorship not available.",
        missing_requirements=["BLOCKER: No visa sponsorship", "AUTOSAR"],
    )
    text = " ".join([out["tailored_summary"], *out["tailored_bullets"], *out["gaps_to_address"]])
    assert profile.immigration_mentions(text) == []
    assert out["gaps_to_address"] == ["AUTOSAR"]


def test_strip_removes_only_offending_sentences():
    text = "I build CAN stacks. I require H-1B transfer. I love controls."
    assert profile.strip_immigration_mentions(text) == "I build CAN stacks. I love controls."


def test_serper_adapter_parses_jobs_and_records_errors(monkeypatch):
    """The live search must actually call the API (it once crashed on a missing import)."""
    from src.services import lead_sources

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"jobs": [{"title": "Embedded Software Engineer", "company_name": "John Deere",
                              "location": "Moline, IL", "link": "https://example.com/job/1",
                              "description": "CAN, J1939, embedded C"}]}

    monkeypatch.setenv("SERPER_API_KEY", "test")
    monkeypatch.setenv("SERPER_MAX_QUERIES", "1")
    monkeypatch.setattr(lead_sources.httpx, "post", lambda *a, **k: Resp())
    adapter = lead_sources.SerperJobSearchAdapter()
    leads = adapter.fetch_leads(["embedded software engineer"])
    assert adapter.errors == []
    assert leads and leads[0].url == "https://example.com/job/1"


def test_tracker_fallback_link_is_careers_page():
    assert sponsors.careers_url("John Deere").startswith("https://")
    assert sponsors.careers_url("Acme Robotics") is None
