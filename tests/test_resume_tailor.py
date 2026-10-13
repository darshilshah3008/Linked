"""Tests that resume tailoring only uses verified profile bullets."""

from src import profile
from src.services.resume_tailor import tailor_resume_bullets


def test_bullets_come_only_from_profile():
    out = tailor_resume_bullets(
        "Embedded Software Engineer", "Deere",
        "CAN FD, J1939, CAPL, Simulink, GitLab CI/CD, FreeRTOS on STM32",
    )
    assert out["tailored_bullets"]
    for b in out["tailored_bullets"]:
        assert b in profile.ACHIEVEMENTS.values()


def test_relevant_bullet_ranks_first():
    out = tailor_resume_bullets("Controls Engineer", "AGCO", "Simulink and Stateflow model-based design")
    assert "Simulink" in out["tailored_bullets"][0]
    assert "Simulink" in out["skills_to_highlight"]


def test_summary_uses_honest_experience_line():
    out = tailor_resume_bullets("Senior Firmware Engineer", "Bosch", "embedded C")
    assert profile.EXPERIENCE_LINE in out["tailored_summary"]
