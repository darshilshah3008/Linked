"""Candidate profile — the single source of truth for who the copilot works for.

Every service that writes about the candidate (resume tailoring, cover letters,
outreach, LLM prompts) and every service that judges fit (scoring) reads from
here. Only put facts here that appear on the candidate's own resume; the
approval agent and the "no fabrication" rule depend on it.

Edit this file when the resume changes. Nothing else should hard-code
years of experience, employers, or skills.
"""

from __future__ import annotations

import re

NAME = "Darshil Shah"
CURRENT_TITLE = "Embedded Software Engineer II"
CURRENT_EMPLOYER = "CNH Industrial"
CURRENT_LOCATION = "Sioux Falls, SD"

# Honest framing of experience: 6+ years engineering in total, of which
# 3+ years are production ECU software (Jun 2023 onward at CNH).
YEARS_TOTAL = "6+"
YEARS_PRODUCTION_SW = "3+"
EXPERIENCE_LINE = (
    f"{YEARS_TOTAL} years of engineering experience, including "
    f"{YEARS_PRODUCTION_SW} years developing production ECU software"
)

# Domains, strongest first.
DOMAINS = [
    "precision agriculture",
    "agricultural machinery",
    "off-highway / commercial vehicles",
    "industrial controls",
    "IoT",
]

EXPERIENCE = [
    {
        "company": "CNH Industrial",
        "role": "Embedded Software Engineer II – Precision Technology",
        "location": "Sioux Falls, SD",
        "dates": "Aug 2026 – Present",
        "domain": "Universal Control Module (UCM) and Auto Boom Module (ABM) precision electronics ECUs",
    },
    {
        "company": "CNH Industrial",
        "role": "Embedded Software Engineer – Sprayers",
        "location": "Manitowoc, WI",
        "dates": "Jun 2023 – Aug 2026",
        "domain": "Sprayer suspension and axle control software",
    },
    {
        "company": "The Coats Company (Hennessy Industries)",
        "role": "Embedded Software Intern",
        "dates": "Jan 2023 – May 2023",
        "domain": "FreeRTOS encoder/stepper control, inter-MCU protocol",
    },
    {
        "company": "Sloan Valve Company",
        "role": "R&D Embedded Software Intern",
        "dates": "Jun 2022 – Aug 2022",
        "domain": "BLE OTA firmware update, PCB bring-up",
    },
    {
        "company": "Deepak Phenolics",
        "role": "Project Engineer (Instrumentation & Controls)",
        "dates": "2018 – 2021",
        "domain": "I&C for a greenfield chemical plant",
    },
]

EDUCATION = [
    "M.S. Electrical and Computer Engineering, University of Texas at Arlington, 2023",
    "B.E. Instrumentation and Control Engineering, L.D. College of Engineering, 2018",
]

# Skills the candidate can defend in an interview. Lower-case match terms.
# Scoring treats anything here as "owned"; gap detection never flags these.
OWNED_SKILLS: dict[str, list[str]] = {
    "Embedded C": ["embedded c", "c/c++", "ansi c", "c99", "c11"],
    "C++": ["c++"],
    "Python": ["python"],
    "C#": ["c#"],
    "CAPL": ["capl"],
    "MATLAB": ["matlab"],
    "Simulink": ["simulink"],
    "Stateflow": ["stateflow"],
    "Embedded Coder": ["embedded coder", "auto-code", "autocode", "code generation", "model-based"],
    "FreeRTOS": ["freertos"],
    "RTOS": ["rtos", "real-time operating system"],
    "Embedded Linux": ["embedded linux"],
    "CAN": ["can", "can bus", "controller area network"],
    "CAN FD": ["can fd", "can-fd", "canfd"],
    "SAE J1939": ["j1939"],
    "ISOBUS (ISO 11783)": ["isobus", "iso 11783", "iso11783"],
    "SPI": ["spi"],
    "I2C": ["i2c", "i²c"],
    "UART": ["uart", "serial"],
    "RS-485": ["rs-485", "rs485"],
    "Ethernet": ["ethernet", "udp"],
    "BLE": ["ble", "bluetooth low energy", "bluetooth"],
    "OTA updates": ["ota", "over-the-air", "firmware update"],
    "STM32": ["stm32"],
    "NXP": ["nxp"],
    "TI MCUs": ["tiva", "texas instruments"],
    "Renesas": ["renesas"],
    "ARM Cortex-M": ["arm", "cortex-m", "cortex"],
    "Vector CANalyzer / CANoe": ["canalyzer", "canoe", "vector tools"],
    "Unit testing (Unity)": ["unit test", "unit testing", "unity", "ceedling"],
    "HIL validation": ["hil", "hardware-in-the-loop", "hardware in the loop"],
    "GitLab CI/CD": ["ci/cd", "gitlab", "continuous integration"],
    "Jenkins": ["jenkins"],
    "Git": ["git"],
    "Polarion": ["polarion"],
    "JIRA": ["jira"],
    "Docker": ["docker"],
    "ISO 26262": ["iso 26262", "iso26262", "functional safety"],
    "MISRA C": ["misra"],
    "JTAG / debugger": ["jtag", "debugger", "swd"],
    "Logic analyzer / oscilloscope": ["logic analyzer", "oscilloscope"],
    "DM1 diagnostics": ["dm1", "dtc", "diagnostic trouble code", "diagnostics"],
    "PWM / closed-loop control": ["pwm", "closed-loop", "closed loop", "pid"],
    "Requirements traceability": ["traceability", "requirements"],
}

# Short skills line for prompts and letters.
CORE_SKILLS = [
    "Embedded C/C++",
    "FreeRTOS",
    "CAN FD / SAE J1939 / ISOBUS",
    "MATLAB/Simulink/Stateflow with Embedded Coder",
    "CAPL and Python test automation",
    "GitLab CI/CD",
    "HIL validation",
]

# Results that appear on the resume. The approval agent's VERIFIED_CLAIMS
# should stay consistent with these numbers.
ACHIEVEMENTS = {
    "j1939": "Implemented CAN and SAE J1939 messaging and DM1 diagnostics for precision electronics ECUs (UCM, ABM), validated in Vector CANalyzer.",
    "capl": "Wrote CAPL scripts in Vector CANalyzer for bus-off recovery, DM1/DTC fault injection, and J1939 address-claim validation.",
    "simulink": "Developed suspension and axle control software in MATLAB/Simulink/Stateflow with Embedded Coder, cutting integration issues by 40% and improving vehicle stability by 30%.",
    "ci/cd": "Built Python-driven GitLab CI/CD pipelines running Simulink Test harnesses and Unity unit tests on every merge request, cutting build/deploy time by 40%.",
    "git": "Led the SVN-to-Git migration and defined branching and code-review workflows, reducing merge conflicts by 50%.",
    "diagnostics": "Integrated a C# diagnostic GUI with embedded firmware over CAN, reducing system response latency by 25%.",
    "defects": "Resolved 100+ defects in Polarion with root-cause analysis and requirements-to-test traceability, contributing to a 30% reduction in field failures.",
    "freertos": "Developed an SPI driver linking FreeRTOS firmware to an AMT203 absolute encoder and implemented stepper-motor stall detection.",
    "inter-mcu": "Established a TI Tiva to Renesas inter-MCU communication protocol with unit tests.",
    "ble": "Developed BLE-based OTA firmware update for IoT fixtures; performed PCB bring-up and failure analysis on prototype boards.",
    "rtos": "Built a custom preemptive RTOS on ARM Cortex-M4F with a priority scheduler and semaphores, validated with Unity unit tests in CI.",
    "precision_ag": "Developing Auto Boom height control and Universal Control Module features for CNH precision-ag sprayers.",
}

# Fit settings used by scoring.
SENIORITY_LEVEL = "II"  # Engineer II; strong for II/III/Senior, a stretch for Staff/Principal.
NEEDS_VISA_SPONSORSHIP = True  # Flags U.S.-citizen-only / ITAR / clearance / no-sponsorship roles.


def headline() -> str:
    """One-line summary used in letters, outreach and prompts."""
    return (
        f"{CURRENT_TITLE} at {CURRENT_EMPLOYER} with {EXPERIENCE_LINE} "
        f"for agricultural and off-highway vehicle platforms"
    )


def prompt_background() -> str:
    """Bulleted background block for LLM prompts."""
    lines = [
        f"- {CURRENT_TITLE} at {CURRENT_EMPLOYER} ({CURRENT_LOCATION})",
        f"- {EXPERIENCE_LINE}",
        "- Current work: Universal Control Module (UCM) and Auto Boom Module (ABM) precision-ag ECUs",
        f"- Skills: {', '.join(CORE_SKILLS)}",
        f"- Domains: {', '.join(DOMAINS)}",
        "- Prior: CNH Industrial Sprayers (Manitowoc, WI); internships at The Coats Company and Sloan Valve",
    ]
    return "\n".join(lines)


# ── Keyword matching shared by scoring and tailoring ──────────

def _pattern(term: str) -> re.Pattern[str]:
    # Boundaries are "not a letter or digit", so "c++", "rs-485" and
    # "can/j1939" match, while "can" does not match "candidate" or "scan".
    return re.compile(r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])")


_PATTERN_CACHE: dict[str, re.Pattern[str]] = {}


def has_term(text: str, term: str) -> bool:
    """True if ``term`` appears in ``text`` as a whole token (case-insensitive)."""
    pat = _PATTERN_CACHE.get(term)
    if pat is None:
        pat = _PATTERN_CACHE[term] = _pattern(term)
    return pat.search(text.lower()) is not None


def find_terms(text: str, terms: list[str]) -> list[str]:
    """Return the terms from ``terms`` that appear in ``text``, in list order."""
    return [t for t in terms if has_term(text, t)]


def owns_skill(term: str) -> bool:
    """True if ``term`` is one of the candidate's owned skill aliases."""
    term = term.lower()
    return any(term in aliases for aliases in OWNED_SKILLS.values())
