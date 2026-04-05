"""Tests for the repository layer."""

from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base
from src.db.repository import Repository
from src.schemas.approval import ApprovalDecision
from src.schemas.company import CompanyInput
from src.schemas.content import ContentInput
from src.schemas.lead import LeadInput, LeadScoreResult
from src.schemas.outreach import OutreachInput


def _get_test_session():
    """Create an in-memory SQLite session for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class TestLeadRepository:
    def setup_method(self):
        self.session = _get_test_session()
        self.repo = Repository(self.session)

    def test_create_and_get_lead(self):
        lead = LeadInput(
            title="Firmware Engineer",
            company="Acme Corp",
            source="test",
        )
        score = LeadScoreResult(score=75.0, inferred_match_reasons=["Title match"], confidence="high")
        model = self.repo.create_lead(lead, score)

        assert model.id is not None
        assert model.title == "Firmware Engineer"
        assert model.relevance_score == 75.0

        fetched = self.repo.get_lead(model.id)
        assert fetched is not None
        assert fetched.company == "Acme Corp"

    def test_list_leads_ordered_by_score(self):
        for title, score in [("Low", 20.0), ("High", 90.0), ("Mid", 50.0)]:
            self.repo.create_lead(
                LeadInput(title=title, company="Co", source="test"),
                LeadScoreResult(score=score, inferred_match_reasons=[], confidence="medium"),
            )
        leads = self.repo.list_leads()
        scores = [l.relevance_score for l in leads]
        assert scores == sorted(scores, reverse=True)

    def test_update_lead_status(self):
        model = self.repo.create_lead(
            LeadInput(title="Test", company="Co", source="test"),
        )
        assert model.status == "new"
        self.repo.update_lead_status(model.id, "reviewed")
        updated = self.repo.get_lead(model.id)
        assert updated.status == "reviewed"

    def test_count_leads_with_filter(self):
        self.repo.create_lead(LeadInput(title="A", company="Co", source="test"))
        self.repo.create_lead(LeadInput(title="B", company="Co", source="test"))
        model = self.repo.create_lead(LeadInput(title="C", company="Co", source="test"))
        self.repo.update_lead_status(model.id, "reviewed")

        assert self.repo.count_leads() == 3
        assert self.repo.count_leads(status="new") == 2
        assert self.repo.count_leads(status="reviewed") == 1


class TestCompanyRepository:
    def setup_method(self):
        self.session = _get_test_session()
        self.repo = Repository(self.session)

    def test_create_and_get_company(self):
        company = CompanyInput(
            name="Deere & Company",
            industry="Agriculture",
            embedded_relevance="high",
        )
        model = self.repo.create_company(company)
        assert model.id is not None

        fetched = self.repo.get_company_by_name("Deere & Company")
        assert fetched is not None
        assert fetched.industry == "Agriculture"

    def test_update_company(self):
        model = self.repo.create_company(CompanyInput(name="TestCo"))
        self.repo.update_company(model.id, industry="Automotive", embedded_relevance="high")
        updated = self.repo.get_company_by_name("TestCo")
        assert updated.industry == "Automotive"
        assert updated.embedded_relevance == "high"


class TestContentRepository:
    def setup_method(self):
        self.session = _get_test_session()
        self.repo = Repository(self.session)

    def test_create_content(self):
        content = ContentInput(
            theme="embedded cicd",
            content_type="linkedin_post",
            hook="CI/CD for firmware teams",
            outline="- Point 1\n- Point 2",
        )
        model = self.repo.create_content(content)
        assert model.id is not None
        assert model.status == "draft"

    def test_update_content_status(self):
        model = self.repo.create_content(ContentInput(theme="test", content_type="linkedin_post"))
        self.repo.update_content_status(model.id, "approved")
        items = self.repo.list_content(status="approved")
        assert len(items) == 1


class TestOutreachRepository:
    def setup_method(self):
        self.session = _get_test_session()
        self.repo = Repository(self.session)

    def test_create_outreach(self):
        outreach = OutreachInput(
            message_type="recruiter_intro",
            draft_text="Hi, I'm interested in the role.",
            lead_id=None,
        )
        model = self.repo.create_outreach(outreach, confidence=0.8)
        assert model.id is not None
        assert model.approval_status == "pending"
        assert model.confidence_score == 0.8


class TestApprovalRepository:
    def setup_method(self):
        self.session = _get_test_session()
        self.repo = Repository(self.session)

    def test_create_approval_record(self):
        decision = ApprovalDecision(
            decision="approved",
            reasons=["Looks good"],
            confidence_score=0.85,
            flagged_issues=[],
        )
        model = self.repo.create_approval("outreach", 1, decision)
        assert model.id is not None
        assert model.decision == "approved"

    def test_list_approvals(self):
        for d in ["approved", "rejected", "approved"]:
            self.repo.create_approval(
                "content",
                None,
                ApprovalDecision(decision=d, reasons=[], confidence_score=0.5),
            )
        approvals = self.repo.list_approvals()
        assert len(approvals) == 3


class TestActivityLog:
    def setup_method(self):
        self.session = _get_test_session()
        self.repo = Repository(self.session)

    def test_log_activity(self):
        model = self.repo.log_activity("orchestrator", "daily_plan", "Test summary")
        assert model.id is not None
        assert model.agent_name == "orchestrator"

    def test_list_logs(self):
        self.repo.log_activity("agent_a", "action_1", "Summary A")
        self.repo.log_activity("agent_b", "action_2", "Summary B")
        logs = self.repo.list_activity_logs()
        assert len(logs) == 2
