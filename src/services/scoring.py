"""Lead relevance scoring module.

Scoring is deterministic and based on keyword/attribute matching.
Returns a fit score on 0-100 scale with full explainability.

Each factor contributes a weighted component:
- title_keyword_match (35 pts max)
- industry_match (20 pts max)
- protocol_stack_match (20 pts max)
- seniority_fit (15 pts max)
- location_match (10 pts max)
"""

from __future__ import annotations

from src.config import get_settings
from src.schemas.lead import LeadInput, LeadScoreResult

# ── Keyword banks ──────────────────────────────────────────

TITLE_KEYWORDS = [
    "embedded software",
    "firmware",
    "embedded systems",
    "embedded engineer",
    "rtos",
    "controls engineer",
    "embedded developer",
    "systems software",
]

INDUSTRY_KEYWORDS = [
    "automotive",
    "agriculture",
    "agricultural",
    "industrial",
    "iot",
    "off-highway",
    "machinery",
    "controls",
    "vehicle",
    "automation",
    "manufacturing",
    "defense",
    "aerospace",
    "medical devices",
    "robotics",
]

PROTOCOL_KEYWORDS = [
    "can",
    "j1939",
    "isobus",
    "spi",
    "i2c",
    "uart",
    "freertos",
    "embedded c",
    "c++",
    "stm32",
    "nxp",
    "ti ",
    "matlab",
    "simulink",
    "rs-485",
    "ble",
    "ethernet",
]

SENIORITY_POSITIVE = ["senior", "sr.", "staff", "lead", "principal", "ii", "iii"]
SENIORITY_NEGATIVE = ["intern", "co-op", "junior", "entry level", "entry-level"]

# Profile requirements for missing-requirements detection
PROFILE_SKILLS = {
    "can", "j1939", "freertos", "c", "c++", "embedded", "rtos",
    "matlab", "simulink", "stm32", "spi", "i2c", "ci/cd", "git",
}

# ── Max points per factor ─────────────────────────────────

PTS_TITLE = 35
PTS_INDUSTRY = 20
PTS_PROTOCOL = 20
PTS_SENIORITY = 15
PTS_LOCATION = 10


def score_lead(lead: LeadInput) -> LeadScoreResult:
    """Score a lead for relevance. Returns deterministic score in [0, 100]."""
    observed_facts: list[str] = []
    match_reasons: list[str] = []
    missing_reqs: list[str] = []
    total = 0.0

    text_blob = _build_text_blob(lead)
    title_lower = lead.title.lower()

    # ── Observe raw facts ──────────────────────────────────
    observed_facts.append(f"Title: {lead.title}")
    observed_facts.append(f"Company: {lead.company}")
    if lead.location:
        observed_facts.append(f"Location: {lead.location}")
    if lead.source:
        observed_facts.append(f"Source: {lead.source}")
    if lead.url:
        observed_facts.append(f"Apply URL available: {lead.url}")
    else:
        observed_facts.append("No direct apply URL provided")

    # ── Title keyword match (35 pts) ──────────────────────
    title_matches = [kw for kw in TITLE_KEYWORDS if kw in title_lower]
    if title_matches:
        total += PTS_TITLE
        match_reasons.append(f"Title directly matches profile: {', '.join(title_matches)}")
        observed_facts.append(f"Title keywords found: {', '.join(title_matches)}")
    else:
        desc_matches = [kw for kw in TITLE_KEYWORDS if kw in text_blob]
        if desc_matches:
            total += PTS_TITLE * 0.5
            match_reasons.append(f"Description mentions relevant terms: {', '.join(desc_matches[:3])}")
            observed_facts.append(f"Description keywords found: {', '.join(desc_matches[:3])}")
        else:
            observed_facts.append("No embedded/firmware title keywords found")

    # ── Industry match (20 pts) ───────────────────────────
    industry_matches = [kw for kw in INDUSTRY_KEYWORDS if kw in text_blob]
    if industry_matches:
        total += PTS_INDUSTRY
        match_reasons.append(f"Industry aligns with background: {', '.join(industry_matches[:3])}")
        observed_facts.append(f"Industry keywords: {', '.join(industry_matches[:3])}")
    else:
        observed_facts.append("No target industry keywords found")

    # ── Protocol/stack match (20 pts) ─────────────────────
    protocol_matches = [kw for kw in PROTOCOL_KEYWORDS if kw in text_blob]
    if protocol_matches:
        total += PTS_PROTOCOL
        match_reasons.append(f"Tech stack overlap: {', '.join(protocol_matches[:4])}")
        observed_facts.append(f"Stack keywords: {', '.join(protocol_matches[:4])}")
    else:
        observed_facts.append("No specific protocol/stack keywords found")

    # ── Seniority fit (15 pts) ────────────────────────────
    seniority_score = _score_seniority(title_lower)
    total += PTS_SENIORITY * seniority_score
    if seniority_score > 0.5:
        match_reasons.append("Seniority level appropriate for 6+ years experience")
    elif seniority_score < 0.3:
        match_reasons.append("Seniority mismatch — may be too junior")
    observed_facts.append(f"Seniority fit: {seniority_score:.1f}")

    # ── Location match (10 pts) ───────────────────────────
    loc_score = _score_location(lead.location)
    total += PTS_LOCATION * loc_score
    if lead.location and loc_score > 0.5:
        match_reasons.append(f"Location is viable: {lead.location}")
    elif lead.location is None:
        observed_facts.append("Location not specified")

    # ── Detect missing requirements ───────────────────────
    if lead.description_snippet:
        desc_lower = lead.description_snippet.lower()
        # Check for requirements the candidate may not have
        high_level_reqs = [
            ("python", "Python programming"),
            ("aws", "AWS cloud experience"),
            ("azure", "Azure cloud experience"),
            ("machine learning", "Machine learning"),
            ("security clearance", "Security clearance"),
            ("phd", "PhD required"),
            ("fpga", "FPGA experience"),
            ("vhdl", "VHDL/Verilog"),
            ("rust", "Rust programming"),
        ]
        for keyword, label in high_level_reqs:
            if keyword in desc_lower:
                missing_reqs.append(label)
    else:
        observed_facts.append("No description available for requirements analysis")

    if not lead.url:
        observed_facts.append("Missing: direct apply URL")

    # ── Confidence ────────────────────────────────────────
    score = round(min(total, 100.0), 1)
    confidence = "high" if score >= 70 else ("medium" if score >= 40 else "low")

    return LeadScoreResult(
        score=score,
        observed_facts=observed_facts,
        inferred_match_reasons=match_reasons,
        missing_requirements=missing_reqs,
        confidence=confidence,
    )


def _build_text_blob(lead: LeadInput) -> str:
    """Combine all text fields into a lowercase searchable string."""
    parts = [lead.title, lead.company]
    if lead.location:
        parts.append(lead.location)
    if lead.description_snippet:
        parts.append(lead.description_snippet)
    return " ".join(parts).lower()


def _score_seniority(title_lower: str) -> float:
    """Return 0-1 seniority fit score."""
    for neg in SENIORITY_NEGATIVE:
        if neg in title_lower:
            return 0.1
    for pos in SENIORITY_POSITIVE:
        if pos in title_lower:
            return 1.0
    return 0.6


def _score_location(location: str | None) -> float:
    """Return 0-1 location fit score."""
    if location is None:
        return 0.3

    settings = get_settings()
    loc_lower = location.lower()
    for pref in settings.preferred_locations_list:
        if pref.lower() in loc_lower:
            return 1.0

    if "remote" in loc_lower:
        return 0.9

    return 0.3
