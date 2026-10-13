"""Lead relevance scoring for an embedded software engineer.

Scoring is deterministic and explainable. A lead earns up to 100 points:

- title_match      (35)  Is this actually an embedded / firmware / ECU role?
- stack_match      (20)  How much of the posting's embedded stack the candidate has,
                         scaled by the number of distinct hits (4+ hits = full marks).
- industry_match   (20)  Domain closeness: ag / off-highway / vehicle = full,
                         other embedded-heavy industries = partial.
- seniority_fit    (15)  Fit for an Engineer II.
- location_fit     (10)  Preferred locations > remote > elsewhere (open to relocation).

Then two adjustments:

- Non-embedded titles (web, data, sales, ...) get no title credit even if the
  description mentions "embedded".
- Eligibility blockers (U.S. citizens only, ITAR, clearance, no sponsorship)
  cap the score at 30 when the profile needs visa sponsorship, and are listed
  first in missing_requirements as "BLOCKER: ...".

All keyword matching is whole-token: "can" matches "CAN bus" and "CAN/J1939"
but not "candidate", "scan" or "Canada"; "ble" does not match "responsible".
"""

from __future__ import annotations

from src import profile
from src.config import get_settings
from src.profile import find_terms, has_term
from src.schemas.lead import LeadInput, LeadScoreResult

# ── Keyword banks ──────────────────────────────────────────

TITLE_KEYWORDS = [
    "embedded", "firmware", "rtos", "ecu", "microcontroller", "mcu",
    "controls software", "control software", "controls engineer",
    "vehicle software", "device driver", "bsp", "bootloader",
    "electronics software", "machine controls", "autonomy software",
]

# Titles that are clearly not embedded software roles.
NON_EMBEDDED_TITLES = [
    "frontend", "front-end", "front end", "web developer", "web engineer", "full stack",
    "full-stack", "fullstack", "data scientist", "data engineer", "data analyst",
    "machine learning engineer", "salesforce", "sales", "marketing", "recruiter",
    "ui designer", "ux", "ios", "android developer", "cloud engineer", "site reliability",
    "business analyst", "account manager", "technician", "mechanical engineer",
    "manufacturing engineer", "quality engineer", "plc programmer",
]

# Stack terms. Matched as whole tokens against title + description.
STACK_KEYWORDS = [
    # Vehicle networks & diagnostics
    "can", "can fd", "j1939", "isobus", "iso 11783", "canopen", "lin", "uds", "xcp",
    "obd", "dm1", "diagnostics", "capl", "canalyzer", "canoe", "vector",
    # Languages & RTOS
    "embedded c", "c/c++", "c++", "freertos", "rtos", "bare-metal", "bare metal",
    "embedded linux", "zephyr", "autosar",
    # MCUs
    "stm32", "nxp", "arm", "cortex-m", "renesas", "tiva", "microcontroller",
    # Peripherals & buses
    "spi", "i2c", "uart", "rs-485", "rs485", "adc", "pwm", "dma", "ethernet", "ble",
    # Model-based & test
    "matlab", "simulink", "stateflow", "embedded coder", "model-based", "hil",
    "hardware-in-the-loop", "unit test", "unity", "ceedling", "misra",
    # Process / safety
    "iso 26262", "iso 25119", "functional safety", "aspice", "ci/cd", "gitlab", "jenkins",
    "jtag", "oscilloscope", "logic analyzer", "bootloader", "device driver",
]

# Domain tiers. Tier 1 = the candidate's own domain; tier 2 = embedded-heavy neighbours.
INDUSTRY_TIER1 = [
    "precision ag", "precision agriculture", "agriculture", "agricultural", "ag equipment",
    "sprayer", "sprayers", "tractor", "tractors", "combine", "off-highway", "heavy equipment",
    "construction equipment", "hydraulic", "hydraulics", "commercial vehicle", "commercial vehicles", "truck", "trucks",
    "vehicle", "vehicles", "automotive", "powertrain", "machinery", "mobile hydraulics",
]
INDUSTRY_TIER2 = [
    "industrial", "industrial automation", "automation", "controls", "iot", "robotics",
    "aerospace", "defense", "medical device", "medical devices", "semiconductor",
    "ev", "electric vehicle", "battery management", "bms", "energy", "hvac", "manufacturing",
]

SENIORITY_STRONG = ["ii", "iii", "2", "3", "senior", "sr", "sr."]
SENIORITY_STRETCH = ["staff", "principal", "lead", "architect", "manager", "director", "iv"]
SENIORITY_JUNIOR = ["junior", "jr", "jr.", "entry level", "entry-level", "new grad", "associate", "i", "1"]
SENIORITY_INTERN = ["intern", "internship", "co-op", "coop", "student"]

# Requirements the candidate does not (yet) have. Term -> label.
GAP_KEYWORDS: dict[str, str] = {
    "fpga": "FPGA", "vhdl": "VHDL", "verilog": "Verilog", "rust": "Rust",
    "autosar": "AUTOSAR (classic stack)", "yocto": "Yocto", "zephyr": "Zephyr RTOS",
    "linux kernel": "Linux kernel development", "device tree": "Linux device tree",
    "qnx": "QNX", "do-178": "DO-178C", "do-178c": "DO-178C", "iec 62304": "IEC 62304",
    "aspice": "Automotive SPICE", "cybersecurity": "Embedded cybersecurity", "iso 21434": "ISO/SAE 21434",
    "secoc": "SecOC", "machine learning": "Machine learning", "computer vision": "Computer vision",
    "aws": "AWS cloud", "azure": "Azure cloud", "kubernetes": "Kubernetes",
    "phd": "PhD", "ros": "ROS", "ros2": "ROS 2", "dsp": "DSP algorithms",
    "uds": "UDS (ISO 14229)", "xcp": "XCP calibration", "lin": "LIN", "canopen": "CANopen",
}

# Eligibility blockers for a candidate who needs visa sponsorship. Term -> label.
BLOCKER_KEYWORDS: dict[str, str] = {
    "u.s. citizen": "U.S. citizenship required",
    "us citizen": "U.S. citizenship required",
    "u.s. citizenship": "U.S. citizenship required",
    "us citizenship": "U.S. citizenship required",
    "citizenship is required": "U.S. citizenship required",
    "itar": "ITAR (U.S. person) restriction",
    "export control": "Export-control (U.S. person) restriction",
    "security clearance": "Security clearance required",
    "secret clearance": "Security clearance required",
    "active clearance": "Security clearance required",
    "ts/sci": "Security clearance required",
    "no sponsorship": "No visa sponsorship",
    "not sponsor": "No visa sponsorship",
    "unable to sponsor": "No visa sponsorship",
    "will not sponsor": "No visa sponsorship",
    "without sponsorship": "No visa sponsorship",
    "without visa sponsorship": "No visa sponsorship",
    "green card": "Green card / permanent residency required",
    "permanent resident": "Green card / permanent residency required",
}
BLOCKER_SCORE_CAP = 30.0

# ── Max points per factor ─────────────────────────────────

PTS_TITLE = 35
PTS_STACK = 20
PTS_INDUSTRY = 20
PTS_SENIORITY = 15
PTS_LOCATION = 10
STACK_HITS_FOR_FULL = 4

# Backwards-compatible aliases (older code and docs refer to these names).
PROTOCOL_KEYWORDS = STACK_KEYWORDS
INDUSTRY_KEYWORDS = INDUSTRY_TIER1 + INDUSTRY_TIER2
PTS_PROTOCOL = PTS_STACK


def score_lead(lead: LeadInput) -> LeadScoreResult:
    """Score a lead for relevance. Returns a deterministic score in [0, 100]."""
    observed_facts: list[str] = []
    match_reasons: list[str] = []
    missing_reqs: list[str] = []
    total = 0.0

    text_blob = _build_text_blob(lead)
    title = lead.title or ""

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

    # ── Title (35) ─────────────────────────────────────────
    title_hits = find_terms(title, TITLE_KEYWORDS)
    non_embedded = find_terms(title, NON_EMBEDDED_TITLES)
    if title_hits and not non_embedded:
        total += PTS_TITLE
        match_reasons.append(f"Title directly matches embedded profile: {', '.join(title_hits)}")
        observed_facts.append(f"Title keywords found: {', '.join(title_hits)}")
    elif non_embedded:
        observed_facts.append(f"Non-embedded title: {', '.join(non_embedded)}")
        match_reasons.append("Title is not an embedded software role")
    else:
        desc_hits = find_terms(text_blob, TITLE_KEYWORDS)
        if desc_hits:
            total += PTS_TITLE * 0.5
            match_reasons.append(f"Description mentions embedded work: {', '.join(desc_hits[:3])}")
            observed_facts.append(f"Description keywords found: {', '.join(desc_hits[:3])}")
        else:
            observed_facts.append("No embedded/firmware title keywords found")

    # ── Stack (20, scaled by number of hits) ──────────────
    stack_hits = _dedupe_stack(find_terms(text_blob, STACK_KEYWORDS))
    owned_hits = [t for t in stack_hits if profile.owns_skill(t)]
    if owned_hits:
        frac = min(len(owned_hits), STACK_HITS_FOR_FULL) / STACK_HITS_FOR_FULL
        total += PTS_STACK * frac
        match_reasons.append(f"Tech stack overlap ({len(owned_hits)}): {', '.join(owned_hits[:6])}")
        observed_facts.append(f"Stack keywords: {', '.join(stack_hits[:8])}")
    else:
        observed_facts.append("No specific protocol/stack keywords found")

    # ── Industry (20, tiered) ─────────────────────────────
    tier1 = find_terms(text_blob, INDUSTRY_TIER1)
    tier2 = find_terms(text_blob, INDUSTRY_TIER2)
    if tier1:
        total += PTS_INDUSTRY
        match_reasons.append(f"Industry matches your domain (ag / vehicle): {', '.join(tier1[:3])}")
        observed_facts.append(f"Industry keywords: {', '.join((tier1 + tier2)[:4])}")
    elif tier2:
        total += PTS_INDUSTRY * 0.6
        match_reasons.append(f"Adjacent embedded industry: {', '.join(tier2[:3])}")
        observed_facts.append(f"Industry keywords: {', '.join(tier2[:4])}")
    else:
        observed_facts.append("No target industry keywords found")

    # ── Seniority (15) ────────────────────────────────────
    seniority_score, seniority_note = _score_seniority(title)
    total += PTS_SENIORITY * seniority_score
    if seniority_score >= 0.8:
        match_reasons.append(f"Seniority fits an Engineer II ({seniority_note})")
    elif seniority_score <= 0.4:
        match_reasons.append(f"Seniority mismatch — {seniority_note}")
    else:
        match_reasons.append(f"Seniority is a stretch — {seniority_note}")
    observed_facts.append(f"Seniority fit: {seniority_score:.1f} ({seniority_note})")

    # ── Location (10) ─────────────────────────────────────
    loc_score = _score_location(lead.location)
    total += PTS_LOCATION * loc_score
    if lead.location and loc_score >= 0.9:
        match_reasons.append(f"Location is viable: {lead.location}")
    elif lead.location is None:
        observed_facts.append("Location not specified")

    # ── Eligibility blockers & skill gaps ─────────────────
    if lead.description_snippet:
        blockers = _unique(BLOCKER_KEYWORDS[k] for k in BLOCKER_KEYWORDS if has_term(text_blob, k))
        if profile.NEEDS_VISA_SPONSORSHIP:
            missing_reqs.extend(f"BLOCKER: {b}" for b in blockers)
        gaps = _unique(
            label for term, label in GAP_KEYWORDS.items()
            if has_term(lead.description_snippet, term) and not profile.owns_skill(term)
        )
        missing_reqs.extend(gaps)
    else:
        blockers = []
        observed_facts.append("No description available for requirements analysis")

    if not lead.url:
        observed_facts.append("Missing: direct apply URL")

    score = round(min(total, 100.0), 1)
    if blockers and profile.NEEDS_VISA_SPONSORSHIP and score > BLOCKER_SCORE_CAP:
        observed_facts.append(f"Score capped at {BLOCKER_SCORE_CAP:.0f} due to eligibility blocker")
        score = BLOCKER_SCORE_CAP
    confidence = "high" if score >= 70 else ("medium" if score >= 40 else "low")

    return LeadScoreResult(
        score=score,
        observed_facts=observed_facts,
        inferred_match_reasons=match_reasons,
        missing_requirements=missing_reqs,
        confidence=confidence,
    )


def _build_text_blob(lead: LeadInput) -> str:
    parts = [lead.title, lead.company]
    if lead.location:
        parts.append(lead.location)
    if lead.description_snippet:
        parts.append(lead.description_snippet)
    return " ".join(p for p in parts if p).lower()


def _dedupe_stack(hits: list[str]) -> list[str]:
    """Collapse aliases so 'c++' and 'c/c++' or 'rtos' and 'freertos' don't double count."""
    out = list(hits)
    pairs = [("c/c++", "c++"), ("freertos", "rtos"), ("can fd", "can"), ("rs485", "rs-485"),
             ("bare metal", "bare-metal"), ("hardware-in-the-loop", "hil"), ("iso 11783", "isobus")]
    for keep, drop in pairs:
        if keep in out and drop in out:
            out.remove(drop)
    return out


def _unique(items) -> list[str]:
    seen: list[str] = []
    for i in items:
        if i not in seen:
            seen.append(i)
    return seen


def _score_seniority(title: str) -> tuple[float, str]:
    """Return (0-1 fit, note) for an Engineer II candidate."""
    if find_terms(title, SENIORITY_INTERN):
        return 0.1, "internship / co-op"
    if find_terms(title, SENIORITY_STRETCH):
        return 0.5, "staff / lead level, likely 8+ years"
    if find_terms(title, SENIORITY_STRONG):
        return 1.0, "II / III / Senior"
    if find_terms(title, SENIORITY_JUNIOR):
        return 0.4, "entry level, below your experience"
    return 0.8, "level not stated"


def _score_location(location: str | None) -> float:
    """Return 0-1 location fit. Preferred > remote > elsewhere in the U.S. (open to relocating)."""
    if location is None:
        return 0.3

    settings = get_settings()
    loc_lower = location.lower()
    for pref in settings.preferred_locations_list:
        if pref.lower() in ("remote",):
            continue
        if has_term(loc_lower, pref):
            return 1.0
    if "remote" in loc_lower:
        return 0.9
    if "hybrid" in loc_lower:
        return 0.6
    return 0.5
