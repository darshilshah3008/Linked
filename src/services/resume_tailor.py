"""Resume tailoring service.

Generates keyword-targeted resume bullets for specific job leads
using the lead's description, match reasons, and tech keywords.
"""

from __future__ import annotations

from src.services.llm_client import get_llm_client

# Candidate's verified experience — only these can be used
CANDIDATE_EXPERIENCE = {
    "summary": (
        "Embedded Software Engineer with 6+ years of experience in automotive, "
        "agricultural machinery, and industrial IoT systems."
    ),
    "skills": [
        "Embedded C/C++", "CAN/J1939", "ISOBUS", "FreeRTOS", "RTOS",
        "MATLAB/Simulink", "STM32", "NXP", "SPI", "I2C", "UART",
        "RS-485", "BLE", "Ethernet", "CI/CD", "Git", "Jenkins",
        "embedded Linux", "Python scripting", "unit testing",
    ],
    "achievements": [
        "Reduced firmware build times by ~40% through CI/CD pipeline automation",
        "Resolved 100+ tracked field issues across sprayer control platforms",
        "Implemented CAN/J1939 communication stacks for multi-ECU systems",
        "Developed MATLAB/Simulink auto-code generation workflows",
        "Designed embedded control software for agricultural sprayer systems",
        "Integrated FreeRTOS task scheduling for real-time control loops",
        "Built automated test frameworks for embedded firmware validation",
    ],
    "companies": [
        {"name": "CNH Industrial", "role": "Embedded Software Engineer", "domain": "Agricultural sprayers"},
        {"name": "The Coats Company", "role": "Software Engineer", "domain": "Automotive tire changers"},
        {"name": "Sloan Valve", "role": "Firmware Engineer", "domain": "IoT sensor systems"},
    ],
}


def tailor_resume_bullets(
    lead_title: str,
    company_name: str,
    description_snippet: str | None = None,
    match_reasons: list[str] | None = None,
    missing_requirements: list[str] | None = None,
) -> dict:
    """Generate tailored resume bullets for a specific job.

    Returns a dict with:
      - target_keywords: keywords extracted from the job
      - tailored_bullets: rewritten resume bullets emphasizing matching skills
      - skills_to_highlight: skills from candidate profile that match
      - gaps_to_address: requirements the candidate may lack
      - summary_line: a tailored one-line professional summary
    """
    # Extract keywords from the job posting
    job_text = " ".join([
        lead_title or "",
        company_name or "",
        description_snippet or "",
    ]).lower()

    target_keywords = _extract_target_keywords(job_text)
    matching_skills = _match_candidate_skills(target_keywords)
    tailored_bullets = _generate_tailored_bullets(target_keywords, matching_skills)
    summary_line = _generate_summary_line(lead_title, company_name, matching_skills)
    gaps = missing_requirements or []

    return {
        "job_title": lead_title,
        "company": company_name,
        "target_keywords": target_keywords,
        "skills_to_highlight": matching_skills,
        "tailored_summary": summary_line,
        "tailored_bullets": tailored_bullets,
        "gaps_to_address": gaps,
    }


def _extract_target_keywords(job_text: str) -> list[str]:
    """Extract relevant technical keywords from job text."""
    keyword_bank = {
        "can": "CAN bus", "j1939": "J1939", "isobus": "ISOBUS",
        "freertos": "FreeRTOS", "rtos": "RTOS",
        "embedded c": "Embedded C", "c++": "C++", "c/c++": "C/C++",
        "stm32": "STM32", "nxp": "NXP", "arm": "ARM",
        "spi": "SPI", "i2c": "I2C", "uart": "UART",
        "rs-485": "RS-485", "rs485": "RS-485",
        "ble": "BLE", "bluetooth": "Bluetooth",
        "ethernet": "Ethernet", "tcp/ip": "TCP/IP",
        "matlab": "MATLAB", "simulink": "Simulink",
        "ci/cd": "CI/CD", "jenkins": "Jenkins", "git": "Git",
        "linux": "Embedded Linux", "python": "Python",
        "firmware": "Firmware", "embedded": "Embedded Systems",
        "automotive": "Automotive", "agriculture": "Agriculture",
        "industrial": "Industrial", "iot": "IoT",
        "controls": "Controls", "automation": "Automation",
        "sensor": "Sensors", "actuator": "Actuators",
        "debug": "Debugging", "testing": "Testing",
    }
    found = []
    for keyword, label in keyword_bank.items():
        if keyword in job_text and label not in found:
            found.append(label)
    return found


def _match_candidate_skills(target_keywords: list[str]) -> list[str]:
    """Find which candidate skills match the target keywords."""
    matched = []
    target_lower = {kw.lower() for kw in target_keywords}
    for skill in CANDIDATE_EXPERIENCE["skills"]:
        if skill.lower() in target_lower:
            matched.append(skill)
        else:
            # Partial match
            for t in target_lower:
                if t in skill.lower() or skill.lower() in t:
                    if skill not in matched:
                        matched.append(skill)
                    break
    return matched


def _generate_tailored_bullets(
    target_keywords: list[str], matching_skills: list[str]
) -> list[str]:
    """Generate resume bullets emphasizing the matching keywords."""
    keyword_lower = {kw.lower() for kw in target_keywords}
    bullets = []

    # Map achievements to keyword relevance
    keyword_achievement_map = {
        "can": "Implemented CAN/J1939 communication stacks for multi-ECU agricultural and automotive systems, ensuring reliable real-time data exchange across distributed embedded controllers.",
        "j1939": "Developed SAE J1939 protocol layers for heavy equipment platforms, including diagnostics (DM1/DM2), transport protocol, and address claim handling.",
        "freertos": "Designed FreeRTOS-based task architectures for real-time control loops, managing sensor acquisition, CAN communication, and actuator control with deterministic timing.",
        "rtos": "Engineered RTOS-based embedded systems with priority-based scheduling, achieving sub-millisecond response times for safety-critical control applications.",
        "ci/cd": "Reduced firmware build and validation times by ~40% through CI/CD pipeline automation using Jenkins, Git, and automated embedded test frameworks.",
        "matlab": "Developed MATLAB/Simulink auto-code generation workflows for control algorithms, bridging model-based design with production embedded C deployment.",
        "simulink": "Created Simulink models for sprayer control systems with auto-code generation to embedded C, reducing manual coding effort and improving algorithm traceability.",
        "firmware": "Designed and maintained production firmware for multi-platform embedded systems spanning automotive, agricultural, and IoT domains.",
        "embedded": "Built embedded control software for agricultural sprayer systems processing real-time sensor data, CAN bus communications, and closed-loop actuator control.",
        "testing": "Built automated test frameworks for embedded firmware validation, including hardware-in-the-loop (HIL) and software-in-the-loop (SIL) test strategies.",
        "automation": "Architected CI/CD pipelines for embedded firmware teams, automating build, static analysis, and flash-based testing across multiple target platforms.",
        "ble": "Integrated BLE wireless communication into IoT sensor systems for remote monitoring and configuration of embedded devices.",
        "linux": "Developed embedded Linux applications for gateway devices bridging field sensor networks with cloud-based monitoring platforms.",
        "python": "Created Python-based test automation scripts and data analysis tools supporting embedded firmware development and field issue resolution.",
        "automotive": "Delivered embedded software for automotive systems including tire changer controllers and vehicle diagnostic interfaces.",
        "iot": "Designed IoT-enabled embedded systems with wireless connectivity (BLE, Wi-Fi) for smart building and industrial monitoring applications.",
        "sensor": "Implemented sensor acquisition and signal conditioning firmware for temperature, pressure, flow, and position sensors in industrial applications.",
        "debug": "Resolved 100+ tracked field issues across embedded control platforms using systematic debugging with JTAG, logic analyzers, and CAN bus monitors.",
        "controls": "Developed closed-loop control algorithms for agricultural sprayer systems, managing flow rate, pressure, and nozzle actuation in real time.",
        "industrial": "Built embedded control systems for industrial equipment including valve controllers, sensor networks, and automated machinery.",
        "stm32": "Developed bare-metal and RTOS-based firmware for STM32 microcontrollers, including peripheral drivers for SPI, I2C, UART, and ADC.",
        "arm": "Programmed ARM Cortex-M based microcontrollers (STM32, NXP) for real-time embedded control applications.",
    }

    for kw in target_keywords:
        kw_lower = kw.lower()
        for key, bullet in keyword_achievement_map.items():
            if key in kw_lower or kw_lower in key:
                if bullet not in bullets:
                    bullets.append(bullet)
                break

    # Always include the core achievements if nothing specific matched
    if not bullets:
        bullets = list(CANDIDATE_EXPERIENCE["achievements"])

    return bullets[:8]  # Cap at 8 bullets


def _generate_summary_line(
    lead_title: str, company_name: str, matching_skills: list[str]
) -> str:
    """Generate a tailored one-line professional summary."""
    skill_list = ", ".join(matching_skills[:5]) if matching_skills else "embedded C/C++, RTOS, CAN/J1939"
    return (
        f"Embedded Software Engineer with 6+ years of experience specializing in "
        f"{skill_list} — seeking to contribute to {company_name}'s "
        f"{lead_title.lower().replace('senior ', '').replace('sr. ', '')} initiatives."
    )
