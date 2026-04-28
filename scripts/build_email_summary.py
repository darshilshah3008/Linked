"""Build a plain-text email body summarizing today's tracker + dashboard.

Reads application_tracker.csv (source of truth for what's still actionable)
and dashboard.json (for outreach drafts, contacts, companies).

Only rows with Status="New" appear in the TOP JOBS section. Applied/Rejected/
Interview rows are summarized as counts at the top.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path


def read_tracker(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def render(dashboard: dict, tracker_rows: list[dict]) -> str:
    lines: list[str] = []
    date = dashboard.get("date") or datetime.utcnow().strftime("%Y-%m-%d")

    lines.append(f"Job Search Copilot - Daily Dashboard for {date}")
    lines.append("=" * 60)
    lines.append("")

    # Tracker summary
    if tracker_rows:
        counts: dict[str, int] = {}
        for r in tracker_rows:
            s = (r.get("Status") or "New").strip() or "New"
            counts[s] = counts.get(s, 0) + 1
        parts = [f"{k}: {v}" for k, v in counts.items()]
        lines.append("Tracker status: " + " | ".join(parts))
        lines.append("Tip: edit application_tracker.csv on GitHub and set Status=Applied")
        lines.append("     to remove a job from tomorrow's email.")
        lines.append("")

    summary = dashboard.get("summary") or ""
    if summary:
        lines.append(summary)
        lines.append("")

    # Active jobs (Status=New)
    active = [r for r in tracker_rows if (r.get("Status") or "New").strip() == "New"]
    if active:
        # Sort by score desc
        def s(r: dict) -> float:
            try:
                return -float(r.get("Score") or 0)
            except (TypeError, ValueError):
                return 0.0
        active.sort(key=s)

        lines.append(f"TOP {min(len(active), 10)} ACTIVE JOBS (Status=New)")
        lines.append("-" * 60)
        for i, j in enumerate(active[:10], start=1):
            h1b = j.get("H1B Sponsor?") or "?"
            h1b_tag = " [H1B Sponsor]" if h1b.lower() == "yes" else ""
            lines.append(
                f"{i:>2}. [{j.get('Score', '?')}/100, {j.get('Confidence', '?')}]{h1b_tag} "
                f"{j.get('Title') or '?'} @ {j.get('Company') or '?'}"
            )
            loc = j.get("Location") or "?"
            lines.append(f"     Location: {loc}")
            url = j.get("Apply Link") or "(no URL)"
            lines.append(f"     Apply: {url}")
        lines.append("")
    else:
        # Fallback to dashboard.json's top_jobs (e.g. before tracker exists)
        top_jobs = dashboard.get("top_jobs") or []
        if top_jobs:
            lines.append(f"TOP {min(len(top_jobs), 10)} JOBS (no tracker yet)")
            lines.append("-" * 60)
            for i, job in enumerate(top_jobs[:10], start=1):
                lines.append(
                    f"{i:>2}. [{job.get('fit_score','?')}/100, {job.get('confidence','?')}] "
                    f"{job.get('title','?')} @ {job.get('company','?')}"
                )
                lines.append(f"     Location: {job.get('location','?')}")
                lines.append(f"     Apply: {job.get('url') or '(no URL)'}")
            lines.append("")

    # Top contacts
    top_people = dashboard.get("top_people") or []
    if top_people:
        lines.append(f"TOP {min(len(top_people), 5)} CONTACTS")
        lines.append("-" * 60)
        for i, p in enumerate(top_people[:5], start=1):
            role = p.get("role") or p.get("title") or "?"
            priority = p.get("contact_priority") or ""
            tail = f" (priority: {priority})" if priority else ""
            lines.append(
                f"{i:>2}. {p.get('name','?')} - {role} @ {p.get('company','?')}{tail}"
            )
        lines.append("")

    # Outreach drafts
    outreach = dashboard.get("outreach_drafts") or []
    if outreach:
        # Filter outreach to active companies if possible
        active_companies = {(r.get("Company") or "").strip().lower() for r in active}
        filtered = [
            m for m in outreach
            if not active_companies or (m.get("company") or "").strip().lower() in active_companies
        ] or outreach
        lines.append(f"OUTREACH DRAFTS READY: {len(filtered)}")
        lines.append("-" * 60)
        for i, m in enumerate(filtered[:3], start=1):
            lt = m.get("lead_title") or ""
            tail = f" - re: {lt}" if lt else ""
            lines.append(
                f"{i:>2}. [{m.get('message_type','outreach')}] "
                f"{m.get('company','?')}{tail}"
            )
        if len(filtered) > 3:
            lines.append(f"  ...and {len(filtered) - 3} more in dashboard_report.docx")
        lines.append("")

    lines.append("-" * 60)
    lines.append("Attachments:")
    lines.append("  application_tracker.xlsx - your full tracker (clickable Apply links)")
    lines.append("  dashboard_report.docx    - full daily report")
    lines.append("  dashboard.json           - raw data")
    lines.append("")
    lines.append("- Job Search Copilot (automated daily run via GitHub Actions)")
    return "\n".join(lines)


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dashboard.json")
    if not src.exists():
        print(f"ERROR: {src} not found", file=sys.stderr)
        return 1
    dashboard = json.loads(src.read_text(encoding="utf-8"))
    tracker_rows = read_tracker(Path("application_tracker.csv"))
    print(render(dashboard, tracker_rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
