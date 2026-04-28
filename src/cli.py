"""CLI entrypoint for Job Search Copilot.

Provides action-oriented commands that produce visible,
structured outputs in the terminal:
- seed: Initialize database with sample data
- find-leads: Find, score, and display top job leads
- find-people: Discover contacts at target companies
- research-companies: Research and rank target companies
- draft-content: Generate content drafts
- draft-outreach: Create outreach message drafts
- daily-plan: Generate complete action dashboard
"""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from src.db.init_db import init_db
from src.logging_config import setup_logging

app = typer.Typer(
    name="copilot",
    help="Job Search Copilot — Multi-agent assistant for embedded software job search.",
    add_completion=False,
)
console = Console()


@app.callback()
def startup():
    """Initialize logging and database on every command."""
    setup_logging()
    init_db()


@app.command()
def seed():
    """Seed the database with sample leads and companies."""
    from src.db.seed import seed_database

    console.print("[bold green]Seeding database...[/bold green]")
    seed_database()
    console.print("[bold green]Done.[/bold green]")


@app.command(name="find-leads")
def find_leads(
    limit: int = typer.Option(20, help="Maximum number of leads to return"),
):
    """Find job leads, score them (0-100), and display with full explainability."""
    from src.agents.lead_finder import LeadFinderAgent
    from src.formatters.dashboard import print_leads_table

    console.print("[bold blue]Finding and scoring job leads...[/bold blue]\n")
    agent = LeadFinderAgent()
    leads = agent.run(limit=limit)

    if not leads:
        console.print("[yellow]No leads found.[/yellow]")
        return

    leads_data = []
    for lead in leads:
        leads_data.append({
            "title": lead.title,
            "company": lead.company,
            "location": lead.location,
            "source": lead.source,
            "url": lead.url,
            "fit_score": lead.relevance_score,
            "confidence": lead.confidence,
            "match_reasons": lead.match_reasons,
            "missing_requirements": lead.missing_requirements,
        })

    print_leads_table(leads_data, title=f"Top {len(leads)} Job Leads")

    # Print detailed breakdown for top 3
    console.print("\n[bold underline]Detailed Breakdown — Top 3[/bold underline]\n")
    for i, lead in enumerate(leads[:3], 1):
        console.print(f"  [bold cyan]{i}. {lead.title}[/bold cyan] at [bold]{lead.company}[/bold]")
        console.print(f"     Fit Score: {lead.relevance_score:.0f}/100 | Confidence: {lead.confidence}")
        console.print(f"     Apply URL: {lead.url or 'N/A'}")
        if lead.match_reasons:
            console.print(f"     Match Reasons:")
            for reason in lead.match_reasons:
                console.print(f"       • {reason}")
        if lead.missing_requirements:
            console.print(f"     Missing Requirements:")
            for req in lead.missing_requirements:
                console.print(f"       [!] {req}")
        console.print()

    console.print(f"[green]OK: {len(leads)} leads saved to database.[/green]")


@app.command(name="find-people")
def find_people(
    limit: int = typer.Option(20, help="Maximum number of contacts to return"),
):
    """Discover contacts at target companies for outreach."""
    from src.agents.people_finder import PeopleFinderAgent
    from src.formatters.dashboard import print_people_table

    console.print("[bold blue]Discovering people at target companies...[/bold blue]\n")
    agent = PeopleFinderAgent()
    contacts = agent.run(limit=limit)

    if not contacts:
        console.print("[yellow]No contacts found.[/yellow]")
        return

    people_data = []
    for c in contacts:
        people_data.append({
            "name": c.name,
            "role": c.role,
            "company": c.company,
            "profile_url": c.profile_url or c.linkedin_url,
            "linkedin_url": c.linkedin_url,
            "relevance_reason": c.relevance_reason,
            "contact_priority": c.contact_priority,
            "suggested_outreach_type": c.suggested_outreach_type,
        })

    print_people_table(people_data, title=f"Top {len(contacts)} People To Contact")
    console.print(f"\n[green]OK: {len(contacts)} contacts saved to database.[/green]")


@app.command(name="research-companies")
def research_companies():
    """Research target companies and display with careers links and recommendations."""
    from src.agents.company_targeting import CompanyTargetingAgent
    from src.formatters.dashboard import print_companies_table

    console.print("[bold blue]Researching target companies...[/bold blue]\n")
    agent = CompanyTargetingAgent()
    companies = agent.research_all()

    if not companies:
        console.print("[yellow]No company data found.[/yellow]")
        return

    companies_data = []
    for co in companies:
        companies_data.append({
            "name": co.name,
            "careers_url": co.careers_url,
            "industry": co.industry,
            "embedded_relevance": co.embedded_relevance,
            "summary": co.summary,
            "research_notes": co.research_notes,
            "suggested_next_step": co.suggested_next_step,
        })

    print_companies_table(companies_data, title=f"Target Companies ({len(companies)})")
    console.print(f"\n[green]OK: {len(companies)} companies saved to database.[/green]")


@app.command(name="research-company")
def research_company(
    company: str = typer.Option(..., help="Company name to research"),
):
    """Research a single company and save structured notes."""
    from src.agents.company_research import CompanyResearchAgent

    console.print(f"[bold blue]Researching: {company}...[/bold blue]")
    agent = CompanyResearchAgent()
    result = agent.research(company)

    if result is None:
        console.print(f"[yellow]No data found for {company}.[/yellow]")
        return

    console.print(f"\n[bold]{result.name}[/bold]")
    console.print(f"  Industry:    {result.industry or 'Unknown'}")
    console.print(f"  Website:     {result.website or 'Unknown'}")
    console.print(f"  Careers:     {result.careers_url or 'N/A'}")
    console.print(f"  Relevance:   {result.embedded_relevance or 'Unknown'}")
    console.print(f"  Summary:     {result.summary or 'N/A'}")
    console.print(f"  Notes:       {result.research_notes or 'N/A'}")
    console.print(f"  Next Step:   {(result.suggested_next_step or 'monitor_weekly').replace('_', ' ')}")
    console.print(f"  Source:      {result.source_url or 'N/A'}")


@app.command(name="draft-content")
def draft_content(
    theme: str = typer.Option(..., help="Content theme (e.g., 'embedded cicd', 'rtos design')"),
    count: int = typer.Option(3, help="Number of ideas to generate"),
):
    """Generate content drafts for a given theme."""
    from src.agents.content_agent import ContentAgent

    console.print(f"[bold blue]Generating content for theme: {theme}...[/bold blue]")
    agent = ContentAgent()
    records = agent.draft_content(theme=theme, count=count)

    for i, record in enumerate(records, 1):
        console.print(f"\n[bold]--- Idea {i} ---[/bold]")
        console.print(f"  Theme: {record.theme}")
        console.print(f"  Type:  {record.content_type}")
        if record.hook:
            console.print(f"  Hook:  {record.hook}")
        if record.outline:
            console.print(f"  Outline:\n{record.outline}")
        if record.full_text:
            console.print(f"\n  [dim]Full Draft:[/dim]\n{record.full_text}")
        console.print(f"  Status: {record.status}")


@app.command(name="draft-outreach")
def draft_outreach(
    lead_id: int = typer.Option(..., help="Lead ID for outreach context"),
    type: str = typer.Option(
        "recruiter_intro",
        help="Message type: recruiter_intro|hiring_manager_intro|connection_note|follow_up|post_engagement_comment",
    ),
):
    """Draft a personalized outreach message for a lead."""
    from src.agents.outreach_agent import OutreachAgent
    from src.utils.validators import validate_message_type

    if not validate_message_type(type):
        console.print(f"[red]Invalid message type: {type}[/red]")
        raise typer.Exit(1)

    console.print(f"[bold blue]Drafting {type} for lead {lead_id}...[/bold blue]")
    agent = OutreachAgent()
    result = agent.draft_outreach(lead_id=lead_id, message_type=type)

    if result is None:
        console.print("[red]Failed to create outreach draft. Check lead ID.[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Outreach Draft (ID: {result.id})[/bold]")
    console.print(f"  Type:     {result.message_type}")
    console.print(f"  Approval: {result.approval_status}")
    console.print(f"  Confidence: {result.confidence_score:.2f}")
    console.print(f"\n[dim]--- Message ---[/dim]\n{result.draft_text}")


@app.command(name="daily-plan")
def daily_plan(
    export: Optional[str] = typer.Option(None, help="Export dashboard to a JSON file (e.g., dashboard.json)"),
):
    """Generate the complete daily action dashboard.

    This is the main command. It produces:
    - Top 10 ranked jobs to apply
    - Top 10 people to engage
    - Top 5 companies to track
    - Top 3 outreach drafts to review
    - Top 5 comments to write
    - 1 LinkedIn post draft
    """
    import json
    from pathlib import Path

    from src.agents.orchestrator import OrchestratorAgent
    from src.formatters.dashboard import print_daily_dashboard

    console.print("[bold blue]Building daily action dashboard...[/bold blue]")
    agent = OrchestratorAgent()
    snapshot = agent.build_dashboard()

    print_daily_dashboard(snapshot.model_dump())

    if export:
        out_path = Path(export)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")
        console.print(f"[green]OK: Dashboard exported to {out_path}[/green]")

    console.print(f"[green]OK: Dashboard snapshot saved to database.[/green]")


@app.command(name="priority-jobs")
def priority_jobs(
    min_score: int = typer.Option(85, help="Minimum fit score to show (0-100)"),
    limit: int = typer.Option(20, help="Maximum number of jobs to display"),
):
    """Show prioritized high-fit jobs with actionable next steps.

    Filters leads by fit score and displays them grouped by priority
    tier (HIGH >= 85, MEDIUM >= 60, LOW < 60) with apply URLs and contacts.
    """
    from src.db.init_db import get_session
    from src.db.repository import Repository

    session = get_session()
    repo = Repository(session)

    leads = repo.list_leads(limit=200)
    contacts = repo.list_contacts_by_priority(limit=200)

    if not leads:
        console.print("[yellow]No leads in database. Run: python -m src find-leads[/yellow]")
        session.close()
        return

    # Filter by minimum score
    priority_leads = [l for l in leads if l.relevance_score >= min_score]

    if not priority_leads:
        console.print(f"[yellow]No leads with fit score >= {min_score}. Try a lower --min-score.[/yellow]")
        session.close()
        return

    # Build contact lookup
    contact_map: dict[str, list] = {}
    for c in contacts:
        if c.company not in contact_map:
            contact_map[c.company] = []
        contact_map[c.company].append(c)

    # Group by priority tier
    tiers = {"HIGH (>= 85)": [], "MEDIUM (60-84)": [], "LOW (< 60)": []}
    for lead in priority_leads[:limit]:
        score = lead.relevance_score
        if score >= 85:
            tiers["HIGH (>= 85)"].append(lead)
        elif score >= 60:
            tiers["MEDIUM (60-84)"].append(lead)
        else:
            tiers["LOW (< 60)"].append(lead)

    console.print(f"\n[bold]PRIORITY JOBS (fit score >= {min_score}): {len(priority_leads)} found[/bold]\n")

    for tier_name, tier_leads in tiers.items():
        if not tier_leads:
            continue
        console.print(f"[bold underline]{tier_name} — {len(tier_leads)} jobs[/bold underline]\n")
        for i, lead in enumerate(tier_leads, 1):
            company_contacts = contact_map.get(lead.company, [])
            contact_info = ""
            if company_contacts:
                best = company_contacts[0]
                contact_info = f" | Contact: {best.name} ({best.role})"

            console.print(
                f"  {i}. [bold cyan]{lead.title}[/bold cyan] at [bold]{lead.company}[/bold]"
            )
            console.print(
                f"     Score: [bold green]{lead.relevance_score:.0f}[/bold green] | "
                f"{lead.location or 'N/A'}{contact_info}"
            )
            console.print(f"     Apply: {lead.url or '[dim]no URL[/dim]'}")
            if lead.match_reasons:
                console.print(f"     Why:   {'; '.join(lead.match_reasons[:2])}")
            console.print()

    console.print(f"[green]Tip: Run 'python -m src tailor-resume --lead-id <ID>' to customize your resume.[/green]")
    session.close()


@app.command(name="tailor-resume")
def tailor_resume(
    lead_id: int = typer.Option(..., help="Lead ID to tailor resume for"),
):
    """Generate keyword-targeted resume bullets for a specific job lead.

    Analyzes the job description and match reasons to produce tailored
    resume bullets, a custom summary line, and skills to highlight.
    """
    from src.db.init_db import get_session
    from src.db.repository import Repository
    from src.services.resume_tailor import tailor_resume_bullets

    session = get_session()
    repo = Repository(session)

    lead = repo.get_lead(lead_id)
    if not lead:
        console.print(f"[red]Lead not found: {lead_id}[/red]")
        session.close()
        raise typer.Exit(1)

    console.print(f"[bold blue]Tailoring resume for: {lead.title} at {lead.company}...[/bold blue]\n")

    result = tailor_resume_bullets(
        lead_title=lead.title,
        company_name=lead.company,
        description_snippet=lead.description_snippet,
        match_reasons=lead.match_reasons,
        missing_requirements=lead.missing_requirements,
    )

    console.print(f"[bold]Target: {result['job_title']}[/bold] at [bold]{result['company']}[/bold]\n")

    console.print("[bold underline]Tailored Summary Line[/bold underline]")
    console.print(f"  {result['tailored_summary']}\n")

    console.print("[bold underline]Keywords to Emphasize[/bold underline]")
    console.print(f"  {', '.join(result['target_keywords'])}\n")

    console.print("[bold underline]Skills to Highlight[/bold underline]")
    for skill in result["skills_to_highlight"]:
        console.print(f"  • {skill}")

    console.print(f"\n[bold underline]Tailored Resume Bullets[/bold underline]")
    for i, bullet in enumerate(result["tailored_bullets"], 1):
        console.print(f"  {i}. {bullet}")

    if result["gaps_to_address"]:
        console.print(f"\n[bold yellow]Gaps to Address[/bold yellow]")
        for gap in result["gaps_to_address"]:
            console.print(f"  [!] {gap}")

    session.close()
    console.print(f"\n[green]OK: Resume tailored for lead #{lead_id}.[/green]")


@app.command(name="cover-letter")
def cover_letter(
    lead_id: int = typer.Option(..., help="Lead ID to generate cover letter for"),
):
    """Generate a targeted cover letter for a specific job lead.

    Uses match reasons, job description, and company research to
    create a personalized cover letter with customization notes.
    """
    from src.db.init_db import get_session
    from src.db.repository import Repository
    from src.services.cover_letter import generate_cover_letter

    session = get_session()
    repo = Repository(session)

    lead = repo.get_lead(lead_id)
    if not lead:
        console.print(f"[red]Lead not found: {lead_id}[/red]")
        session.close()
        raise typer.Exit(1)

    # Get company context if available
    company = repo.get_company_by_name(lead.company)
    company_summary = company.summary if company else None
    company_industry = company.industry if company else None

    console.print(f"[bold blue]Generating cover letter for: {lead.title} at {lead.company}...[/bold blue]\n")

    result = generate_cover_letter(
        lead_title=lead.title,
        company_name=lead.company,
        description_snippet=lead.description_snippet,
        match_reasons=lead.match_reasons,
        missing_requirements=lead.missing_requirements,
        company_summary=company_summary,
        company_industry=company_industry,
    )

    console.print(f"[bold]Subject: {result['subject_line']}[/bold]\n")

    from rich.panel import Panel
    console.print(Panel(
        result["cover_letter"],
        title=f"Cover Letter — {lead.company}",
        border_style="green",
        expand=True,
    ))

    console.print(f"\n[bold underline]Key Selling Points Used[/bold underline]")
    for point in result["key_points"]:
        console.print(f"  • {point}")

    console.print(f"\n[bold underline]Customization Notes[/bold underline]")
    for note in result["customization_notes"]:
        console.print(f"  → {note}")

    session.close()
    console.print(f"\n[green]OK: Cover letter generated for lead #{lead_id}.[/green]")


@app.command(name="batch-outreach")
def batch_outreach(
    limit: int = typer.Option(10, help="Number of top leads to generate outreach for"),
    types: str = typer.Option(
        "recruiter_intro,hiring_manager_intro,connection_note",
        help="Comma-separated message types to generate",
    ),
):
    """Generate outreach messages for top leads in batch.

    Creates recruiter intros, hiring manager intros, and connection
    notes for your highest-scoring leads with matching contacts.
    """
    from src.db.init_db import get_session
    from src.db.repository import Repository
    from src.services.outreach_personalizer import draft_outreach_message

    session = get_session()
    repo = Repository(session)

    leads = repo.list_leads(limit=limit)
    contacts = repo.list_contacts_by_priority(limit=200)

    if not leads:
        console.print("[yellow]No leads in database. Run: python -m src find-leads[/yellow]")
        session.close()
        return

    message_types = [t.strip() for t in types.split(",")]
    contact_map: dict[str, list] = {}
    for c in contacts:
        if c.company not in contact_map:
            contact_map[c.company] = []
        contact_map[c.company].append(c)

    from rich.panel import Panel
    total = 0

    for lead in leads:
        company_contacts = contact_map.get(lead.company, [])
        company = repo.get_company_by_name(lead.company)
        company_summary = company.summary if company else None

        for msg_type in message_types:
            contact_name = None
            contact_role = None
            if company_contacts:
                # Pick appropriate contact for message type
                best = company_contacts[0]
                contact_name = best.name
                contact_role = best.role

            msg = draft_outreach_message(
                message_type=msg_type,
                lead_title=lead.title,
                company_name=lead.company,
                company_summary=company_summary,
                contact_name=contact_name,
                contact_role=contact_role,
                lead_id=lead.id,
            )

            label = msg_type.replace("_", " ").title()
            console.print(Panel(
                msg.draft_text,
                title=f"[{lead.company}] {label} — {lead.title}",
                border_style="blue",
                expand=True,
            ))
            total += 1

    session.close()
    console.print(f"\n[green]OK: {total} outreach messages generated for {len(leads)} leads.[/green]")


@app.command(name="export-tracker")
def export_tracker(
    output: str = typer.Option("application_tracker.csv", help="Output file path (.csv or .xlsx)"),
    min_score: int = typer.Option(0, help="Minimum fit score to include"),
):
    """Export an application tracker spreadsheet.

    Creates a CSV or Excel file with columns:
    Company | Role | Fit Score | Priority | Apply URL |
    Contact Person | Contact Role | Outreach Type | Status | Notes
    """
    from src.db.init_db import get_session
    from src.db.repository import Repository
    from src.services.tracker_export import export_tracker_csv, export_tracker_excel

    session = get_session()
    repo = Repository(session)

    leads = repo.list_leads(limit=200)
    contacts = repo.list_contacts_by_priority(limit=200)

    if not leads:
        console.print("[yellow]No leads in database. Run: python -m src find-leads[/yellow]")
        session.close()
        return

    # Convert to dicts for the export service
    leads_data = []
    for lead in leads:
        if lead.relevance_score < min_score:
            continue
        leads_data.append({
            "title": lead.title,
            "company": lead.company,
            "location": lead.location,
            "url": lead.url,
            "fit_score": lead.relevance_score,
            "match_reasons": lead.match_reasons,
            "missing_requirements": lead.missing_requirements,
        })

    contacts_data = []
    for c in contacts:
        contacts_data.append({
            "name": c.name,
            "role": c.role,
            "company": c.company,
            "contact_priority": c.contact_priority,
            "suggested_outreach_type": c.suggested_outreach_type,
        })

    if output.endswith(".xlsx"):
        out_path = export_tracker_excel(leads_data, contacts_data, output)
    else:
        out_path = export_tracker_csv(leads_data, contacts_data, output)

    session.close()
    console.print(f"[green]OK: Application tracker exported to {out_path} ({len(leads_data)} leads).[/green]")
