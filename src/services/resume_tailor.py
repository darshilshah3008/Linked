"""Resume tailoring service.

Picks and orders the candidate's real resume bullets for a specific job lead.
Every bullet comes from ``src.profile.ACHIEVEMENTS``; nothing is invented.
"""

from __future__ import annotations

from src import profile

# Job-posting term -> label shown as a target keyword.
KEYWORD_BANK: dict[str, str] = {
    "can fd": "CAN FD", "can": "CAN bus", "j1939": "SAE J1939", "isobus": "ISOBUS",
    "iso 11783": "ISOBUS", "uds": "UDS", "xcp": "XCP", "lin": "LIN",
    "freertos": "FreeRTOS", "rtos": "RTOS", "bare-metal": "Bare-metal", "bare metal": "Bare-metal",
    "embedded c": "Embedded C", "c/c++": "C/C++", "c++": "C++", "python": "Python", "c#": "C#",
    "capl": "CAPL", "canalyzer": "CANalyzer", "canoe": "CANoe",
    "stm32": "STM32", "nxp": "NXP", "arm": "ARM Cortex-M", "cortex": "ARM Cortex-M",
    "renesas": "Renesas", "spi": "SPI", "i2c": "I2C", "uart": "UART", "rs-485": "RS-485",
    "ble": "BLE", "bluetooth": "Bluetooth", "ethernet": "Ethernet", "ota": "OTA updates",
    "matlab": "MATLAB", "simulink": "Simulink", "stateflow": "Stateflow",
    "embedded coder": "Embedded Coder", "model-based": "Model-based design",
    "ci/cd": "CI/CD", "gitlab": "GitLab CI/CD", "jenkins": "Jenkins", "git": "Git",
    "unit test": "Unit testing", "hil": "HIL testing", "hardware-in-the-loop": "HIL testing",
    "iso 26262": "ISO 26262", "iso 25119": "ISO 25119", "functional safety": "Functional safety",
    "misra": "MISRA C", "autosar": "AUTOSAR", "polarion": "Polarion",
    "diagnostics": "Diagnostics", "dm1": "DM1 diagnostics", "bootloader": "Bootloader",
    "device driver": "Device drivers", "driver": "Device drivers",
    "embedded linux": "Embedded Linux", "firmware": "Firmware", "embedded": "Embedded systems",
    "ecu": "ECU software", "precision ag": "Precision agriculture", "sprayer": "Sprayers",
    "agricultur": "Agriculture", "off-highway": "Off-highway", "automotive": "Automotive",
    "industrial": "Industrial", "iot": "IoT", "controls": "Controls", "pwm": "PWM control",
    "debug": "Debugging", "root cause": "Root-cause analysis", "requirements": "Requirements traceability",
}

# Job-posting term -> which real achievement(s) it should pull forward, in priority order.
KEYWORD_TO_ACHIEVEMENTS: dict[str, list[str]] = {
    "j1939": ["j1939", "capl"], "can": ["j1939", "diagnostics"], "can fd": ["j1939"],
    "isobus": ["precision_ag", "j1939"], "dm1": ["j1939", "capl"], "diagnostics": ["capl", "diagnostics"],
    "capl": ["capl"], "canalyzer": ["capl", "j1939"], "canoe": ["capl"],
    "simulink": ["simulink"], "matlab": ["simulink"], "stateflow": ["simulink"],
    "embedded coder": ["simulink"], "model-based": ["simulink"],
    "ci/cd": ["ci/cd"], "gitlab": ["ci/cd"], "jenkins": ["ci/cd"], "unit test": ["ci/cd", "rtos"],
    "hil": ["ci/cd"], "git": ["git"], "freertos": ["freertos", "rtos"], "rtos": ["rtos", "freertos"],
    "spi": ["freertos"], "arm": ["rtos"], "cortex": ["rtos"], "renesas": ["inter-mcu"], "uart": ["inter-mcu"],
    "ble": ["ble"], "bluetooth": ["ble"], "ota": ["ble"], "c#": ["diagnostics"],
    "debug": ["defects"], "root cause": ["defects"], "requirements": ["defects"], "polarion": ["defects"],
    "precision ag": ["precision_ag"], "sprayer": ["precision_ag", "simulink"],
    "agricultur": ["precision_ag", "simulink"], "controls": ["simulink", "precision_ag"],
    "pwm": ["precision_ag"], "ecu": ["j1939", "precision_ag"], "functional safety": ["precision_ag"],
    "iso 26262": ["precision_ag"], "embedded": ["j1939", "simulink"], "firmware": ["freertos", "ble"],
}

# Strong default order when a posting gives little to go on.
DEFAULT_ORDER = ["j1939", "simulink", "ci/cd", "capl", "defects", "precision_ag", "git", "diagnostics"]


def tailor_resume_bullets(
    lead_title: str,
    company_name: str,
    description_snippet: str | None = None,
    match_reasons: list[str] | None = None,
    missing_requirements: list[str] | None = None,
) -> dict:
    """Generate tailored resume content for a specific job.

    Returns a dict with:
      - target_keywords: keywords extracted from the job
      - skills_to_highlight: candidate skills that match those keywords
      - tailored_summary: a one-line summary pointed at this role
      - tailored_bullets: real resume bullets, most relevant first
      - gaps_to_address: skill gaps only (eligibility blockers stay out of documents)
    """
    job_text = " ".join([lead_title or "", company_name or "", description_snippet or ""])

    target_keywords = _extract_target_keywords(job_text)
    matching_skills = _match_candidate_skills(job_text)
    tailored_bullets = _select_bullets(job_text)
    summary_line = _generate_summary_line(lead_title, company_name, matching_skills)

    gaps = [g for g in (missing_requirements or []) if not g.startswith("BLOCKER")]
    return {
        "job_title": lead_title,
        "company": company_name,
        "target_keywords": target_keywords,
        "skills_to_highlight": matching_skills,
        "tailored_summary": profile.strip_immigration_mentions(summary_line),
        "tailored_bullets": [profile.strip_immigration_mentions(b) for b in tailored_bullets],
        "gaps_to_address": gaps,
    }


def _extract_target_keywords(job_text: str) -> list[str]:
    found: list[str] = []
    for term, label in KEYWORD_BANK.items():
        if _hit(job_text, term) and label not in found:
            found.append(label)
    return found


def _match_candidate_skills(job_text: str) -> list[str]:
    """Candidate skills (display names) whose aliases appear in the job text."""
    matched = []
    for skill, aliases in profile.OWNED_SKILLS.items():
        if any(profile.has_term(job_text, a) for a in aliases):
            matched.append(skill)
    return matched


def _select_bullets(job_text: str, limit: int = 6) -> list[str]:
    keys: list[str] = []
    for term, ach_keys in KEYWORD_TO_ACHIEVEMENTS.items():
        if _hit(job_text, term):
            for k in ach_keys:
                if k not in keys:
                    keys.append(k)
    for k in DEFAULT_ORDER:  # top up with strongest general bullets
        if len(keys) >= limit:
            break
        if k not in keys:
            keys.append(k)
    return [profile.ACHIEVEMENTS[k] for k in keys[:limit]]


def _hit(text: str, term: str) -> bool:
    # Stems like "agricultur" are meant as prefixes; everything else is a whole token.
    if term in ("agricultur",):
        return term in text.lower()
    return profile.has_term(text, term)


def _generate_summary_line(lead_title: str, company_name: str, matching_skills: list[str]) -> str:
    skills = ", ".join(matching_skills[:5]) if matching_skills else ", ".join(profile.CORE_SKILLS[:3])
    role = (lead_title or "embedded software").lower()
    for prefix in ("senior ", "sr. ", "sr "):
        role = role.replace(prefix, "")
    return (
        f"{profile.CURRENT_TITLE} with {profile.EXPERIENCE_LINE}, specializing in "
        f"{skills} — ready to contribute to {company_name}'s {role} work."
    )
