"""Cover letter generation service.

Generates targeted cover letters using job lead data,
match reasons, and company research.
"""

from __future__ import annotations

from src import profile


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
        "j1939": "CAN / SAE J1939 messaging and DM1 diagnostics on production precision-ag ECUs (UCM, ABM)",
        "can": "CAN and CAN FD networking on multi-ECU agricultural vehicle platforms, validated in Vector CANalyzer",
        "isobus": "ISOBUS (ISO 11783) precision-ag control modules at CNH Industrial",
        "capl": "CAPL test scripts for bus-off recovery, DM1/DTC fault injection and J1939 address claim",
        "firmware": "Firmware from driver level (SPI, inter-MCU protocols) up to application control logic",
        "freertos": "FreeRTOS firmware, plus a custom preemptive RTOS built on ARM Cortex-M4F",
        "rtos": "RTOS internals: built a preemptive scheduler with semaphores on ARM Cortex-M4F",
        "matlab": "MATLAB/Simulink/Stateflow model-based development with Embedded Coder",
        "simulink": "Simulink/Stateflow control software with production code generation (40% fewer integration issues)",
        "ci/cd": "Python + GitLab CI/CD running Simulink Test and Unity unit tests on every merge request (40% faster builds)",
        "agricultur": "Embedded control software for CNH precision-ag sprayers (Auto Boom, suspension, axle control)",
        "controls": "Closed-loop vehicle control software (suspension and axle control, boom height control)",
        "ble": "BLE OTA firmware update for IoT fixtures (Sloan Valve)",
        "iot": "BLE OTA firmware update for IoT fixtures (Sloan Valve)",
        "safety": "ECU feature work following ISO 26262 functional-safety practices",
    }

    search_text = " ".join(match_reasons + [description_snippet or ""])
    for keyword, point in keyword_point_map.items():
        hit = keyword in search_text.lower() if keyword in ("agricultur", "safety") else profile.has_term(search_text, keyword)
        if hit and point not in points:
            points.append(point)

    # Add core points if we don't have enough
    if len(points) < 3:
        core = [
            profile.EXPERIENCE_LINE,
            "Resolved 100+ Polarion defects with root-cause analysis, contributing to 30% fewer field failures",
            "GitLab CI/CD automation cutting firmware build and deploy time by 40%",
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
        f"at {company_name}.{company_hook} I am an {profile.CURRENT_TITLE} at "
        f"{profile.CURRENT_EMPLOYER} with {profile.EXPERIENCE_LINE} for agricultural "
        f"and off-highway vehicle platforms, and I am confident I can make a meaningful "
        f"contribution to your team."
    )

    # Body — key qualifications
    bullets_text = "\n".join(f"  • {point}" for point in key_points)
    body = (
        f"\n\nKey qualifications I bring to this role:\n\n"
        f"{bullets_text}"
    )

    # Experience highlights
    experience = (
        f"\n\nAt CNH Industrial in Sioux Falls I develop software for the Universal Control "
        f"Module and Auto Boom Module, precision-electronics ECUs that communicate over "
        f"CAN / SAE J1939. Before that, on the Sprayers program, I built suspension and axle "
        f"control software in MATLAB/Simulink/Stateflow with Embedded Coder, wrote CAPL "
        f"tests in Vector CANalyzer, cut build and deploy time by 40% with Python and "
        f"GitLab CI/CD, and resolved 100+ defects in Polarion with root-cause analysis."
    )

    # Address gaps proactively if any
    gap_text = ""
    skill_gaps = [g for g in missing_requirements if not g.startswith("BLOCKER")]
    if skill_gaps:
        gap_items = ", ".join(skill_gaps[:2])
        gap_text = (
            f"\n\nMy core is embedded C/C++, RTOS and vehicle networking; I am eager to expand my expertise in areas such as {gap_items}, and I am a "
            f"fast learner with a strong foundation in systems-level programming."
        )

    # Closing
    closing = (
        f"\n\nI would welcome the opportunity to discuss how my embedded systems "
        f"experience can contribute to {company_name}'s engineering goals. I am "
        f"available for a conversation at your convenience.\n\n"
        f"Thank you for your time and consideration.\n\n"
        f"Sincerely,\n{profile.NAME}\n"
        f"{profile.CURRENT_TITLE}"
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

    blockers = [g for g in missing_requirements if g.startswith("BLOCKER")]
    if blockers:
        notes.insert(0, "Check eligibility before applying: " + "; ".join(blockers))
    skill_gaps = [g for g in missing_requirements if not g.startswith("BLOCKER")]
    if skill_gaps:
        gap_list = ", ".join(skill_gaps[:3])
        notes.append(
            f"Consider adding a sentence about transferable skills related to: {gap_list}."
        )

    notes.append(
        "If you know the hiring manager's name, address the letter to them directly."
    )

    return notes
