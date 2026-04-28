"""Build a plain-text email body summarizing today's dashboard.json."""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path


def render(dashboard: dict) -> str:
    lines = []
    date = dashboard.get("date") or datetime.utcnow().strftime("%Y-%m-%d")
    summary = dashboard.get("summary") or ""

    lines.append(f"Job Search Copilot - Daily Dashboard for {date}")
    lines.append("=" * 60)
    lines.append("")
    if summary:
        lines.append(summary)
        lines.append("")

    top_jobs = dashboard.get("top_jobs") or []
    if top_jobs:
        lines.append(f"TOP {min(len(top_jobs), 10)} JOBS")
        lines.append("-" * 60)
        for i, job in enumerate(top_jobs[:10], start=1):
            lines.append(
                f"{i:>2}. [{job.get('fit_score','?')}/100, {job.get('confidence','?')}] "
                f"{job.get('title','?')} @ {job.get('company','?')}"
            )
            lines.append(f"     Location: {job.get('location','?')}")
            lines.append(f"     Apply: {job.get('url') or '(no URL)'}")
            reasons = job.get("match_reasons") or []
            if reasons:
                lines.append(f"     Why: {reasons[0]}")
        lines.append("")

    top_people = dashboard.get("top_people") or []
    if top_people:
        lines.append(f"TOP {min(len(top_people), 5)} CONTACTS")
        lines.append("-" * 60)
        for i, p in enumerate(top_people[:5], start=1):
            role = p.get("role") or p.get("title") or "?"
            priority = p.get("contact_priority", "")
            tail = f" (priority: {priority})" if priority else ""
            lines.append(f"{i:>2}. {p.get('name','?')} - {role} @ {p.get('company','?')}{tail}")
        lines.append("")

    top_companies = dashboard.get("top_companies") or []
    if top_companies:
        lines.append(f"TOP {min(len(top_companies), 5)} COMPANIES")
        lines.append("-" * 60)
        for i, c in enumerate(top_companies[:5], start=1):
            lines.append(f"{i:>2}. {c.get('name','?')} ({c.get('industry','?')})")
        lines.append("")

    outreach = dashboard.get("outreach_drafts") or []
    if outreach:
        lines.append(f"OUTREACH DRAFTS READY: {len(outreach)}")
        lines.append("-" * 60)
        for i, m in enumerate(outreach[:3], start=1):
            lead_title = m.get("lead_title") or ""
            tail = f" - re: {lead_title}" if lead_title else ""
            lines.append(
                f"{i:>2}. [{m.get('message_type','outreach')}] "
                f"{m.get('company','?')}{tail}"
            )
        if len(outreach) > 3:
            lines.append(f"  ...and {len(outreach) - 3} more in dashboard_report.docx")
        lines.append("")

    lines.append("-" * 60)
    lines.append("Full report attached: dashboard_report.docx")
    lines.append("Raw data attached:    dashboard.json")
    lines.append("")
    lines.append("- Job Search Copilot (automated daily run via GitHub Actions)")
    return "\n".join(lines)


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dashboard.json")
    if not src.exists():
        print(f"ERROR: {src} not found", file=sys.stderr)
        return 1
    with src.open("r", encoding="utf-8") as f:
        dashboard = json.load(f)
    print(render(dashboard))
    return 0


if __name__ == "__main__":
    sys.exit(main())
