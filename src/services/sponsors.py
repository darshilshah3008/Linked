"""Green card (PERM) + H-1B sponsor lookup.

Loads ``data/green_card_sponsors.json`` — employers checked against
DOL-derived filing history — and answers "has this company recently filed
green cards for engineers?". The copilot only recommends companies in the
``proven`` or ``smaller`` tiers when ``profile.REQUIRE_GREEN_CARD_SPONSOR``
is on.

This information is for the candidate's targeting only. It must never be
written into a resume, cover letter or outreach message (the approval agent
blocks that).
"""

from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

from src import profile

SPONSOR_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "green_card_sponsors.json"
RECOMMENDED_TIERS = ("proven", "smaller")

_SUFFIXES = (
    "inc", "incorporated", "corp", "corporation", "llc", "lp", "l p", "ltd", "co", "company",
    "the", "plc", "gmbh", "ag", "sa", "us", "usa", "america", "americas", "north america",
)


def normalize(name: str) -> str:
    """Lower-case, strip accents/punctuation and legal suffixes."""
    n = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    n = n.replace("&", " and ")
    n = re.sub(r"\(.*?\)", " ", n)  # "Collins Aerospace (Raytheon)" -> "collins aerospace"
    n = re.sub(r"[^a-z0-9]+", " ", n)
    n = " ".join(n.split())
    if n.startswith("the "):
        n = n[4:]
    # Strip trailing legal suffixes and "(of) (north) america(s)" repeatedly:
    # "Daimler Truck North America LLC" -> "daimler truck".
    tail = re.compile(r"\s+(?:" + "|".join(sorted(map(re.escape, _SUFFIXES), key=len, reverse=True))
                      + r"|of north america|of america|north america)$")
    prev = None
    while prev != n:
        prev = n
        n = tail.sub("", n).strip()
    return n


@lru_cache(maxsize=1)
def _load() -> tuple[list[dict], dict[str, dict]]:
    if not SPONSOR_FILE.exists():
        return [], {}
    data = json.loads(SPONSOR_FILE.read_text(encoding="utf-8"))
    companies = data.get("companies", [])
    index: dict[str, dict] = {}
    for c in companies:
        for alias in [c["company"], c.get("entity", ""), *c.get("aliases", [])]:
            key = normalize(alias)
            if key and key not in index:
                index[key] = c
    return companies, index


def lookup(company: str) -> dict | None:
    """Return the sponsor record for ``company`` or None if it has not been checked.

    Matches exact normalized names, then a whole-word prefix, so
    "Honeywell Aerospace" -> Honeywell and "John Deere - Moline" -> Deere.
    """
    _, index = _load()
    key = normalize(company)
    if not key:
        return None
    if key in index:
        return index[key]
    best = None
    for alias, rec in index.items():
        if len(alias) < 3:
            continue
        if key.startswith(alias + " ") and (best is None or len(alias) > len(best[0])):
            best = (alias, rec)
    return best[1] if best else None


def is_recommended(company: str) -> bool:
    """True if this company has a recent record of filing green cards for engineers."""
    rec = lookup(company)
    return bool(rec and rec["tier"] in RECOMMENDED_TIERS)


def filter_enabled() -> bool:
    return bool(getattr(profile, "REQUIRE_GREEN_CARD_SPONSOR", False))


def allowed(company: str) -> bool:
    """Gate used by agents: everything passes when the filter is off."""
    return is_recommended(company) if filter_enabled() else True


def label(company: str) -> str:
    """Short label for trackers and reports (private to the candidate)."""
    rec = lookup(company)
    if rec is None:
        return "Not checked"
    return {"proven": "Yes - proven", "smaller": "Yes - smaller", "excluded": "No"}.get(rec["tier"], "Not checked")


def recommended_companies() -> list[dict]:
    companies, _ = _load()
    return [c for c in companies if c["tier"] in RECOMMENDED_TIERS]


def careers_url(company: str) -> str | None:
    """Company careers / job-search page from the sponsor list (fallback apply link)."""
    rec = lookup(company)
    return rec.get("careers_url") if rec else None
