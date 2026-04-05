"""Tests for the approval agent."""

from src.agents.approval import ApprovalAgent
from src.schemas.approval import ApprovalRequest


def _make_request(content: str, item_type: str = "outreach") -> ApprovalRequest:
    return ApprovalRequest(
        item_type=item_type,
        content_text=content,
        metadata={},
    )


class TestApprovalAgent:
    """Test suite for the approval layer."""

    def setup_method(self):
        self.agent = ApprovalAgent()

    def test_clean_content_approved(self):
        request = _make_request(
            "Hi John, I noticed the Embedded Software Engineer role at Deere and "
            "wanted to connect. My background in CAN/J1939 and FreeRTOS aligns well."
        )
        decision = self.agent.review(request)
        assert decision.decision == "approved"
        assert decision.confidence_score > 0.5

    def test_spam_content_flagged(self):
        request = _make_request(
            "Act now!!! Don't miss this exclusive opportunity! Reply urgently!"
        )
        decision = self.agent.review(request)
        assert decision.decision in ("rejected", "revision_needed")
        assert len(decision.flagged_issues) > 0

    def test_unsafe_automation_rejected(self):
        request = _make_request(
            "This message will auto-send to all recruiters in the database."
        )
        decision = self.agent.review(request)
        assert decision.decision == "rejected"
        assert any("unsafe" in issue.lower() or "auto" in issue.lower() for issue in decision.flagged_issues)

    def test_too_short_content_flagged(self):
        request = _make_request("Hi")
        decision = self.agent.review(request)
        assert decision.decision in ("rejected", "revision_needed")

    def test_verified_claim_not_flagged(self):
        request = _make_request(
            "In my current role, I helped reduce build and deployment time by 40% "
            "using GitLab CI automation."
        )
        decision = self.agent.review(request)
        # 40% is a verified claim from the profile
        assert decision.decision == "approved"

    def test_placeholder_noted(self):
        request = _make_request(
            "Hi [RECIPIENT_NAME], I'm interested in the role at [COMPANY_NAME]. "
            "My experience with [SPECIFIC_PROJECT] is relevant."
        )
        decision = self.agent.review(request)
        assert any("placeholder" in r.lower() for r in decision.reasons)

    def test_unsupported_superlatives_flagged(self):
        request = _make_request(
            "I am the best in class embedded engineer with a guaranteed track record."
        )
        decision = self.agent.review(request)
        assert decision.decision in ("rejected", "revision_needed")
        assert len(decision.flagged_issues) > 0

    def test_confidence_score_bounded(self):
        request = _make_request("Normal professional outreach message about embedded roles.")
        decision = self.agent.review(request)
        assert 0.0 <= decision.confidence_score <= 1.0
