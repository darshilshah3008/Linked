"""Generate a detailed dashboard report from dashboard.json."""

import json
import sys

def main():
    with open("dashboard.json", "r", encoding="utf-8") as f:
        d = json.load(f)

    lines = []
    L = lines.append

    L("=" * 80)
    L("  DAILY ACTION DASHBOARD - DETAILED REPORT")
    L("=" * 80)
    L(f"  Generated: {d['date']}")
    L(f"  Summary:   {d['summary']}")
    L("=" * 80)
    L("")

    # ── SECTION 1: TOP JOBS ──────────────────────────────────────────────
    L("")
    L("#" * 80)
    L("  SECTION 1: TOP 10 JOB LEADS (Ranked by Fit Score)")
    L("#" * 80)
    L("")

    for i, job in enumerate(d["top_jobs"], 1):
        L(f"  [{i}] {job['title']}")
        L(f"  {'=' * (len(job['title']) + 4)}")
        L(f"  Company:      {job['company']}")
        L(f"  Location:     {job['location']}")
        L(f"  Fit Score:    {job['fit_score']:.0f}/100")
        L(f"  Confidence:   {job['confidence']}")
        L(f"  Apply URL:    {job['url']}")
        L(f"  Description:  {job['description']}")
        L(f"  Source:       {job['source']}")
        L("")
        L("  Match Reasons:")
        for r in job.get("match_reasons", []):
            L(f"    + {r}")
        missing = job.get("missing_requirements", [])
        if missing:
            L("  Missing Requirements:")
            for m in missing:
                L(f"    ! {m}")
        else:
            L("  Missing Requirements: None")
        L("")
        L("-" * 80)
        L("")

    # ── SECTION 2: TOP PEOPLE ────────────────────────────────────────────
    L("")
    L("#" * 80)
    L("  SECTION 2: TOP 10 PEOPLE TO CONTACT")
    L("#" * 80)
    L("")

    for i, p in enumerate(d["top_people"], 1):
        L(f"  [{i}] {p['name']}")
        L(f"  {'=' * (len(p['name']) + 4)}")
        L(f"  Role:               {p['role']}")
        L(f"  Company:            {p['company']}")
        priority = (p.get("contact_priority") or "medium").upper()
        L(f"  Priority:           {priority}")
        outreach = (p.get("suggested_outreach_type") or "connection").replace("_", " ").title()
        L(f"  Outreach Type:      {outreach}")
        L(f"  Profile URL:        {p.get('profile_url') or 'N/A'}")
        L(f"  LinkedIn:           {p.get('linkedin_url') or 'N/A'}")
        L(f"  Relevance Reason:   {p.get('relevance_reason', 'N/A')}")
        L("")
        L("-" * 80)
        L("")

    # ── SECTION 3: TARGET COMPANIES ──────────────────────────────────────
    L("")
    L("#" * 80)
    L("  SECTION 3: TOP 5 TARGET COMPANIES")
    L("#" * 80)
    L("")

    for i, co in enumerate(d["top_companies"], 1):
        L(f"  [{i}] {co['name']}")
        L(f"  {'=' * (len(co['name']) + 4)}")
        L(f"  Industry:           {co.get('industry', 'N/A')}")
        relevance = (co.get("embedded_relevance") or "unknown").upper()
        L(f"  Embedded Relevance: {relevance}")
        L(f"  Careers URL:        {co.get('careers_url', 'N/A')}")
        L(f"  Summary:            {co.get('summary', 'N/A')}")
        L(f"  Research Notes:     {co.get('research_notes', 'N/A')}")
        step = (co.get("suggested_next_step") or "monitor_weekly").replace("_", " ").title()
        L(f"  Recommended Action: {step}")
        L("")
        L("-" * 80)
        L("")

    # ── SECTION 4: OUTREACH DRAFTS ───────────────────────────────────────
    L("")
    L("#" * 80)
    L("  SECTION 4: OUTREACH DRAFTS (9 Total)")
    L("#" * 80)
    L("")

    for i, msg in enumerate(d["outreach_drafts"], 1):
        mtype = msg["message_type"].replace("_", " ").title()
        L(f"  [{i}] {mtype} - {msg['company']}")
        L(f"  {'=' * (len(mtype) + len(msg['company']) + 5)}")
        L(f"  Target Role:    {msg['lead_title']}")
        L(f"  Message Type:   {mtype}")
        L(f"  Company:        {msg['company']}")
        L("")
        L("  --- Message Draft ---")
        for line in msg["draft_text"].split("\n"):
            L(f"  | {line}")
        L("")
        L("-" * 80)
        L("")

    # ── SECTION 5: COMMENTS TO WRITE ─────────────────────────────────────
    L("")
    L("#" * 80)
    L("  SECTION 5: LINKEDIN COMMENTS TO WRITE (5 Total)")
    L("#" * 80)
    L("")

    for i, c in enumerate(d["comments_to_write"], 1):
        L(f"  [{i}] Theme: {c['theme']}")
        L(f"      Hook: {c['hook']}")
        if c.get("full_text"):
            L("")
            L("      --- Full Draft ---")
            for line in c["full_text"].split("\n"):
                L(f"      | {line}")
        L("")
        L("-" * 80)
        L("")

    # ── SECTION 6: LINKEDIN POST ─────────────────────────────────────────
    L("")
    L("#" * 80)
    L("  SECTION 6: LINKEDIN POST DRAFT")
    L("#" * 80)
    L("")

    lp = d.get("linkedin_post_draft")
    if lp:
        L(f"  Theme:   {lp['theme']}")
        L(f"  Hook:    {lp['hook']}")
        L(f"  Outline: {lp.get('outline', 'N/A')}")
        L("")
        L("  --- Full Post ---")
        if lp.get("full_text"):
            for line in lp["full_text"].split("\n"):
                L(f"  | {line}")
        L("")

    L("")
    L("=" * 80)
    L("  END OF REPORT")
    L(f"  {d['summary']}")
    L("=" * 80)

    report = "\n".join(lines)
    with open("dashboard_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report written: {len(lines)} lines, {len(report)} chars")


if __name__ == "__main__":
    main()
