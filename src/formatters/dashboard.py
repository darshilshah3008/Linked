"""Rich CLI output formatters for the daily action dashboard.

Provides structured, human-readable terminal output for all
major workflows: leads, people, companies, outreach, and the
unified daily dashboard.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def print_leads_table(leads: list[dict], title: str = "Job Leads To Apply") -> None:
    """Print a rich table of job leads with fit scores and match reasons."""
    table = Table(title=title, show_lines=True, expand=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="bold cyan", max_width=35)
    table.add_column("Company", style="bold")
    table.add_column("Location", max_width=18)
    table.add_column("Fit", justify="right", style="bold")
    table.add_column("Confidence")
    table.add_column("Apply URL", max_width=40)
    table.add_column("Match Reasons", max_width=45)
    table.add_column("Missing", max_width=25)

    for i, lead in enumerate(leads, 1):
        score = lead.get("fit_score", 0)
        score_style = "bold green" if score >= 70 else ("yellow" if score >= 40 else "red")
        conf = lead.get("confidence", "medium")
        url = lead.get("url") or "[dim]no URL[/dim]"
        reasons = "; ".join(lead.get("match_reasons", [])[:3]) or "-"
        missing = "; ".join(lead.get("missing_requirements", [])[:2]) or "-"

        table.add_row(
            str(i),
            lead.get("title", ""),
            lead.get("company", ""),
            lead.get("location") or "N/A",
            Text(f"{score:.0f}", style=score_style),
            conf,
            url,
            reasons,
            missing,
        )

    console.print(table)


def print_people_table(people: list[dict], title: str = "People To Contact") -> None:
    """Print a rich table of contacts with priority and outreach type."""
    table = Table(title=title, show_lines=True, expand=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Name", style="bold cyan", max_width=30)
    table.add_column("Title/Role", max_width=30)
    table.add_column("Company", style="bold")
    table.add_column("Priority", justify="center")
    table.add_column("Outreach Type", max_width=22)
    table.add_column("Profile/URL", max_width=40)
    table.add_column("Why Relevant", max_width=50)

    for i, person in enumerate(people, 1):
        prio = person.get("contact_priority", "medium")
        prio_style = "bold green" if prio == "high" else ("yellow" if prio == "medium" else "dim")
        url = person.get("profile_url") or person.get("linkedin_url") or "[dim]no URL[/dim]"
        outreach = (person.get("suggested_outreach_type") or "connection").replace("_", " ")

        table.add_row(
            str(i),
            person.get("name", ""),
            person.get("role") or "N/A",
            person.get("company") or "N/A",
            Text(prio.upper(), style=prio_style),
            outreach,
            url,
            person.get("relevance_reason") or "-",
        )

    console.print(table)


def print_companies_table(companies: list[dict], title: str = "Company Targets") -> None:
    """Print a rich table of target companies."""
    table = Table(title=title, show_lines=True, expand=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Company", style="bold cyan", max_width=25)
    table.add_column("Relevance", justify="center")
    table.add_column("Industry", max_width=30)
    table.add_column("Careers URL", max_width=45)
    table.add_column("Why It Fits", max_width=50)
    table.add_column("Next Step", max_width=20)

    for i, company in enumerate(companies, 1):
        rel = company.get("embedded_relevance") or "unknown"
        rel_style = "bold green" if rel == "high" else ("yellow" if rel == "medium" else "dim")
        careers = company.get("careers_url") or "[dim]no URL[/dim]"
        next_step = (company.get("suggested_next_step") or "monitor_weekly").replace("_", " ")

        table.add_row(
            str(i),
            company.get("name", ""),
            Text(rel.upper(), style=rel_style),
            company.get("industry") or "N/A",
            careers,
            company.get("research_notes") or company.get("summary") or "-",
            next_step,
        )

    console.print(table)


def print_outreach_drafts(drafts: list[dict], title: str = "Outreach Drafts") -> None:
    """Print outreach message drafts in panels."""
    console.print(f"\n[bold underline]{title}[/bold underline]\n")
    for i, draft in enumerate(drafts, 1):
        msg_type = draft.get("message_type", "unknown").replace("_", " ").title()
        company = draft.get("company") or ""
        header = f"[{i}] {msg_type}"
        if company:
            header += f" - {company}"

        console.print(Panel(
            draft.get("draft_text", ""),
            title=header,
            border_style="blue",
            expand=True,
        ))


def print_content_suggestions(items: list[dict], title: str = "Content Suggestions") -> None:
    """Print content/comment suggestions."""
    console.print(f"\n[bold underline]{title}[/bold underline]\n")
    for i, item in enumerate(items, 1):
        ctype = item.get("content_type", "linkedin_post").replace("_", " ").title()
        console.print(f"  [bold]{i}. {ctype}[/bold]: [dim]{item.get('theme', '')}[/dim]")
        if item.get("hook"):
            console.print(f"     Hook: {item['hook']}")
        if item.get("full_text"):
            console.print(Panel(
                item["full_text"],
                title=f"Draft #{i}",
                border_style="green",
                expand=True,
            ))
        console.print()


def print_daily_dashboard(dashboard: dict) -> None:
    """Print the complete daily action dashboard."""
    console.print()
    console.print(Panel(
        "[bold]DAILY ACTION DASHBOARD[/bold]",
        style="bold white on blue",
        expand=True,
    ))
    console.print(f"  [dim]{dashboard.get('summary', '')}[/dim]\n")

    # Top Jobs
    jobs = dashboard.get("top_jobs", [])
    if jobs:
        print_leads_table(jobs[:10], title="TOP 10 JOBS TO APPLY")
    else:
        console.print("[yellow]  No job leads found. Run: python -m src.main find-leads[/yellow]\n")

    # Top People
    people = dashboard.get("top_people", [])
    if people:
        print_people_table(people[:10], title="TOP 10 PEOPLE TO ENGAGE")
    else:
        console.print("[yellow]  No contacts found. Run: python -m src.main find-people[/yellow]\n")

    # Top Companies
    companies = dashboard.get("top_companies", [])
    if companies:
        print_companies_table(companies[:5], title="TOP 5 COMPANIES TO TRACK")
    else:
        console.print("[yellow]  No companies found. Run: python -m src.main research-companies[/yellow]\n")

    # Outreach Drafts
    drafts = dashboard.get("outreach_drafts", [])
    if drafts:
        print_outreach_drafts(drafts[:3], title="TOP 3 OUTREACH DRAFTS TO REVIEW")

    # Comments
    comments = dashboard.get("comments_to_write", [])
    if comments:
        print_content_suggestions(comments[:5], title="TOP 5 COMMENTS TO WRITE")

    # LinkedIn Post
    post = dashboard.get("linkedin_post_draft")
    if post:
        console.print("\n[bold underline]LINKEDIN POST DRAFT[/bold underline]\n")
        console.print(Panel(
            post.get("full_text") or post.get("hook", ""),
            title=post.get("theme", "LinkedIn Post"),
            border_style="magenta",
            expand=True,
        ))

    console.print()
