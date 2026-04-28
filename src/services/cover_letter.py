"""Cover letter generation service.

Generates targeted cover letters using job lead data,
match reasons, and company research.
"""

from __future__ import annotations

from src.services.resume_tailor import CANDIDATE_EXPERIENCE


def generate_cover_letter(
    lead_title: str,
    company_name: str,
    description_snippet: str | None = None,
    match_reasons: list[str] | None = None,
    missing_requirements: list[str] | None = None,
    company_summary: str | None = None,
    company_industry: str | None = None,
) -> dict:
    """Generate a targeted cover letter for a specific job lead.

    Returns a dict with:
      - subject_line: email subject line
      - cover_letter: full cover letter text
      - key_points: bullet list of selling points used
      - customization_notes: suggestions for further personalization
    """
    match_reasons = match_reasons or []
    missing_requirements = missing_requirements or []

    # Build selling points from match reasons
    key_points = _build_key_points(match_reasons, description_snippet)

    # Generate the letter
    letter = _build_cover_letter(
        lead_title=lead_title,
        company_name=company_name,
        company_summary=company_summary,
        company_industry=company_industry,
        key_points=key_points,
        missing_requirements=missing_requirements,
    )

    subject_line = f"Application: {lead_title} — Darshil Shah"

    customization_notes = _build_customization_notes(
        company_name, missing_requirements, company_summary
    )

    return {
        "job_title": lead_title,
        "company": company_name,
        "subject_line": subject_line,
        "cover_letter": letter,
        "key_points": key_points,
        "customization_notes": customization_notes,
    }


def _build_key_points(match_reasons: list[str], description_snippet: str | None) -> list[str]:
    """Extract key selling points from match reasons and job description."""
    points = []

    # Parse match reasons for specific tech/domain mentions
    keyword_point_map = {
        "can": "CAN/J1939 protocol implementation across multi-ECU agricultural and automotive systems",
        "j1939": "SAE J1939 stack development including diagnostics and transport protocol",
        "embedded": "6+ years of production embedded software development in C/C++",
        "firmware": "Full-lifecycle firmware development from requirements to field deployment",
        "freertos": "FreeRTOS-based real-time system design with deterministic task scheduling",
        "rtos": "RTOS architecture design for safety-critical control applications",
        "matlab": "MATLAB/Simulink model-based design with auto-code generation to embedded C",
        "simulink": "Simulink control algorithm development with production code generation",
        "ci/cd": "CI/CD pipeline automation reducing build times by ~40%",
        "automotive": "Production embedded systems in automotive domain",
        "agriculture": "Embedded control systems for precision agriculture equipment",
        "industrial": "Industrial embedded systems including sensor networks and actuator control",
        "controls": "Closed-loop control algorithm design for real-time systems",
        "ble": "BLE wireless integration for IoT sensor platforms",
        "iot": "IoT-enabled embedded systems with wireless connectivity",
    }

    reasons_text = " ".join(match_reasons).lower()
    for keyword, point in keyword_point_map.items():
        if keyword in reasons_text and point not in points:
            points.append(point)

    # Add core points if we don't have enough
    if len(points) < 3:
        core = [
            "6+ years of embedded software experience across automotive, agricultural, and industrial domains",
            "Track record of resolving 100+ field issues across multiple embedded platforms",
            "CI/CD pipeline automation reducing firmware build and test cycle times by ~40%",
        ]
        for p in core:
            if p not in points:
                points.append(p)
            if len(points) >= 5:
                break

    return points[:5]


def _build_cover_letter(
    lead_title: str,
    company_name: str,
    company_summary: str | None,
    company_industry: str | None,
    key_points: list[str],
    missing_requirements: list[str],
) -> str:
    """Build the full cover letter text."""
    # Opening paragraph — why this company/role
    company_hook = ""
    if company_summary:
        company_hook = f" {company_name}'s work in {company_summary.rstrip('.')} aligns closely with my background."
    elif company_industry:
        company_hook = f" {company_name}'s position in the {company_industry} industry resonates with my professional experience."

    opening = (
        f"Dear Hiring Manager,\n\n"
        f"I am writing to express my strong interest in the {lead_title} position "
        f"at {company_name}.{company_hook} With over six years of hands-on embedded "
        f"software engineering experience spanning automotive, agricultural machinery, "
        f"and industrial IoT systems, I am confident I can make a meaningful contribution "
        f"to your team."
    )

    # Body — key qualifications
    bullets_text = "\n".join(f"  • {point}" for point in key_points)
    body = (
        f"\n\nKey qualifications I bring to this role:\n\n"
        f"{bullets_text}"
    )

    # Experience highlights
    experience = (
        f"\n\nAt CNH Industrial, I develop embedded control software for agricultural "
        f"sprayer systems, working extensively with CAN/J1939 protocols, MATLAB/Simulink "
        f"code generation, and real-time control algorithms. I have contributed to "
        f"reducing firmware build times by approximately 40% through CI/CD automation "
        f"and have resolved over 100 tracked field issues across our embedded platforms."
    )

    # Address gaps proactively if any
    gap_text = ""
    if missing_requirements:
        gap_items = ", ".join(missing_requirements[:2])
        gap_text = (
            f"\n\nWhile my primary focus has been on embedded C/C++ and RTOS development, "
            f"I am eager to expand my expertise in areas such as {gap_items}, and I am a "
            f"fast learner with a strong foundation in systems-level programming."
        )

    # Closing
    closing = (
        f"\n\nI would welcome the opportunity to discuss how my embedded systems "
        f"experience can contribute to {company_name}'s engineering goals. I am "
        f"available for a conversation at your convenience.\n\n"
        f"Thank you for your time and consideration.\n\n"
        f"Sincerely,\nDarshil Shah\n"
        f"Embedded Software Engineer"
    )

    return opening + body + experience + gap_text + closing


def _build_customization_notes(
    company_name: str,
    missing_requirements: list[str],
    company_summary: str | None,
) -> list[str]:
    """Generate notes for further personalizing the cover letter."""
    notes = []

    if not company_summary:
        notes.append(
            f"Research {company_name}'s recent projects or products to add a specific "
            f"reference in the opening paragraph."
        )

    notes.append(
        "Replace generic experience references with specific project names or "
        "metrics relevant to this role."
    )

    if missing_requirements:
        gap_list = ", ".join(missing_requirements[:3])
        notes.append(
            f"Consider adding a sentence about transferable skills related to: {gap_list}."
        )

    notes.append(
        "If you know the hiring manager's name, address the letter to them directly."
    )

    return notes
