---
name: job-search-copilot
description: 'Specialized workflow for the Job Search Copilot project. Use when: adding new companies, adding job leads, changing scoring weights, running the pipeline, generating reports, adding CLI commands, writing tests, extending agents, or debugging the mock data sources. Covers: lead scoring, mock data sources, agent architecture, SQLite CRM, CLI commands, Word report generation, approval workflow, and H1B company research.'
argument-hint: 'What do you want to do? (e.g. add company, change scoring, run pipeline, generate report, add agent)'
---

# Job Search Copilot — Developer Skill

## Project Identity

**Job Search Copilot** — A standalone Python CLI for embedded software engineers to find jobs, research companies, discover hiring contacts, and draft outreach. No external services required. Mock data by default, OpenAI optional.

- **Entry point:** `python -m src <command>` or `copilot <command>` (after `pip install -e .`)
- **Database:** SQLite at `data/app.db` (auto-created, never committed to git)
- **Tests:** `python -m pytest tests/ -v` (38 tests)
- **Report:** `python generate_report_docx.py` (reads `dashboard.json`)

---

## Project Structure Map

```
src/
  cli.py                    ← All CLI commands (Typer)
  config.py                 ← Env vars via Pydantic Settings
  agents/
    orchestrator.py         ← build_dashboard() — main pipeline
    lead_finder.py          ← Scores leads 0-100, writes to DB
    people_finder.py        ← Contacts at TARGET_COMPANIES list
    company_targeting.py    ← TARGET_COMPANIES list (96 entries)
    company_research.py     ← Single company research
    content_agent.py        ← LinkedIn content drafts
    outreach_agent.py       ← Personalized message drafts
    approval.py             ← Safety/spam/hallucination checks
  db/
    models.py               ← SQLAlchemy ORM (9 tables)
    repository.py           ← CRUD for all entities
    init_db.py              ← Engine + session factory
    seed.py                 ← Loads data/seeds/*.json
  services/
    scoring.py              ← 0-100 scoring formula
    lead_sources.py         ← MockLeadSource (61 leads)
    research_sources.py     ← MockResearchSource (96 companies)
    people_sources.py       ← MockPeopleSource (44 contacts)
    content_planner.py      ← 8 topic templates
    outreach_personalizer.py← 5 message type templates
    llm_client.py           ← MockLLMClient / OpenAIClient
  schemas/                  ← Pydantic models (lead, company, contact, etc.)
  utils/                    ← text_utils, time_utils, validators
generate_report_docx.py     ← Word document report from dashboard.json
inspect_db.py               ← Quick DB row count + sample viewer
```

---

## Key Workflows

### Run the Full Pipeline

```bash
# Fresh run (clears old DB)
Remove-Item -Force data\app.db -ErrorAction SilentlyContinue
python -m src daily-plan --export dashboard.json
python generate_report_docx.py
python inspect_db.py   # verify counts
```

### Run Individual Commands

```bash
python -m src seed                                      # Load 8 sample leads + 5 companies
python -m src find-leads --limit 30                     # Find & score job leads
python -m src find-people --limit 50                    # Discover contacts
python -m src research-companies                        # Batch research 96 companies
python -m src research-company --company "Qualcomm"     # Single company
python -m src draft-content --theme "can j1939"         # LinkedIn content
python -m src draft-outreach --lead-id 1 --type recruiter_intro
python -m src daily-plan --export dashboard.json        # Full dashboard
```

---

## How to Add a New Company

1. **Add to `src/services/research_sources.py`** — append to `MockResearchSource._DATA` dict:
   ```python
   "Company Name": {
       "name": "Company Name",
       "website": "https://www.example.com",
       "careers_url": "https://www.example.com/careers",
       "industry": "Industry Type",
       "summary": "One sentence description.",
       "embedded_relevance": "high|medium|low",
       "research_notes": "Details about embedded roles, tech stack, etc.",
       "source_url": "https://www.example.com/about",
       "suggested_next_step": "apply_now|follow_company|monitor_weekly",
   },
   ```

2. **Add to `src/agents/company_targeting.py`** — append name to `TARGET_COMPANIES` list.

3. **Optionally add contacts** in `src/services/people_sources.py` — append to `MockPeopleSource._DATA`.

4. **Optionally add leads** in `src/services/lead_sources.py` — append a `LeadInput(...)` in `MockLeadSource.fetch_leads()`.

5. **Reset DB and rerun:** `Remove-Item data\app.db; python -m src daily-plan --export dashboard.json`

### Embedded Relevance Guide

| Value | When to Use |
|-------|-------------|
| `high` | Core embedded: automotive, ag, aerospace, semiconductor, robotics, defense |
| `medium` | Some embedded roles: big tech HW teams, storage, industrial IT |
| `low` | Mostly SW/consulting: SaaS, fintech, social media, IT services |
| `unknown` | Not researched yet |

### Suggested Next Step Guide

| Value | When |
|-------|------|
| `apply_now` | HIGH relevance, active job postings |
| `follow_company` | MEDIUM relevance, worth monitoring |
| `monitor_weekly` | LOW relevance or no embedded roles currently |

---

## How to Add a Job Lead

Add a `LeadInput(...)` entry in `src/services/lead_sources.py` inside `MockLeadSource.fetch_leads()`:

```python
LeadInput(
    title="Senior Embedded Software Engineer",
    company="Company Name",
    location="City, ST",
    source="mock",
    url="https://careers.example.com/job/123",
    description_snippet=(
        "Keywords that matter: embedded, firmware, CAN, J1939, FreeRTOS, C/C++, "
        "RTOS, STM32, MATLAB, automotive, industrial, senior."
    ),
),
```

The scoring engine auto-scores based on `description_snippet` content. Higher scores come from more keyword matches.

---

## Lead Scoring Formula (src/services/scoring.py)

| Factor | Points | Keywords |
|--------|--------|----------|
| Title match | 35 | embedded software, firmware, embedded systems, rtos, controls engineer |
| Industry match | 20 | automotive, agriculture, industrial, iot, machinery, defense, aerospace, robotics |
| Protocol/stack | 20 | can, j1939, freertos, c/c++, stm32, spi, i2c, uart, matlab, simulink |
| Seniority | 15 | senior=1.0, mid-level=0.6, junior/intern=0.1 |
| Location | 10 | Preferred (Manitowoc/WI/Remote)=1.0, Remote=0.9, other=0.3 |

**To change scoring weights:** Edit the multipliers in `src/services/scoring.py`.  
**To add keywords:** Add to the relevant list in `score_lead()`.

---

## Database Schema Quick Reference

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `leads` | Job opportunities | title, company, relevance_score, status, match_reasons_json |
| `companies` | Company research | name, embedded_relevance, research_notes, careers_url |
| `contacts` | Hiring people | name, role, company, contact_priority, linkedin_url |
| `outreach_messages` | Message drafts | message_type, draft_text, approval_status |
| `content_items` | LinkedIn content | theme, hook, full_text, status |
| `approval_records` | Approval history | decision, reasons_json, confidence_score |
| `activity_logs` | Audit trail | agent_name, action_type, summary |
| `dashboard_snapshots` | Daily snapshots | snapshot_json |
| `applications` | Job applications | lead_id, status, applied_date |

**Repository pattern:** All DB access goes through `src/db/repository.py` — `Repository` class with typed methods.

---

## How to Add a New CLI Command

1. In `src/cli.py`, add a new `@app.command()` function using Typer:
   ```python
   @app.command()
   def my-command(
       option: str = typer.Option("default", help="Description"),
   ) -> None:
       """Short description shown in --help."""
       console.print("[bold]Running...[/bold]")
       # Call agent or service here
   ```
2. Import and call the relevant agent from `src/agents/`.
3. Add a test in `tests/` if the command has logic worth testing.

---

## How to Add a New Agent

1. Create `src/agents/my_agent.py`:
   ```python
   class MyAgent:
       AGENT_NAME = "my_agent"
       def run(self) -> list[...]:
           session = get_session()
           repo = Repository(session)
           # ... logic ...
           repo.log_activity(self.AGENT_NAME, "action_type", "summary")
           session.close()
           return results
   ```
2. Import in `src/agents/__init__.py`.
3. Wire into `OrchestratorAgent` in `src/agents/orchestrator.py` if it should run as part of `daily-plan`.

---

## Approval Agent Rules (src/agents/approval.py)

The approval agent rejects or flags drafts that contain:

| Check | Examples |
|-------|---------|
| Unsupported claims | Unverified %, "best in class", "guaranteed", "top 1%" |
| Spam language | "act now", "limited time", "!!!", urgency pressure |
| Unsafe automation | "auto-send", "auto-post", "auto-apply" |
| Too short | Under 20 characters |
| Placeholders | `[PLACEHOLDER]` tokens left unfilled |

**Verified claims** (auto-approved): "40% build time reduction", "CAN/J1939 protocol implementation", "FreeRTOS task management"

To add a new verified claim: edit `VERIFIED_CLAIMS` in `src/agents/approval.py`.

---

## LLM Configuration

| Setting | Value | Effect |
|---------|-------|--------|
| `LLM_PROVIDER=mock` | Default | Template-based content, no API key |
| `LLM_PROVIDER=openai` | Optional | Richer AI-generated content |
| `OPENAI_API_KEY=sk-...` | Required for openai | API authentication |
| `OPENAI_MODEL=gpt-4o-mini` | Default for openai | Model selection |

**To add a new LLM provider:** Subclass `LLMClient` in `src/services/llm_client.py` with `chat()` and `generate()` methods, then register in `get_llm_client()`.

---

## Word Report Generation

The report reads from `dashboard.json` (generated by `daily-plan --export`):

```bash
python -m src daily-plan --export dashboard.json
python generate_report_docx.py
```

**Report sections:**
1. All job leads ranked by fit score (with match reasons + gaps)
2. All contacts by priority (with outreach strategies)
3. All companies grouped by relevance (HIGH/MEDIUM/LOW/UNKNOWN)
4. Outreach drafts (recruiter, hiring manager, connection notes)
5. LinkedIn comment drafts
6. LinkedIn post draft

**Output:** `dashboard_report.docx` (or timestamped if file is open)

---

## Testing

```bash
python -m pytest tests/ -v           # All 38 tests
python -m pytest tests/test_scoring.py -v    # 10 scoring tests
python -m pytest tests/test_approval.py -v   # 9 approval tests
python -m pytest tests/test_repository.py -v # 13 repository tests
python -m pytest tests/test_content.py -v    # 6 content tests
```

**Test patterns:**
- Scoring tests: pass a `LeadInput` with specific keywords, assert score range
- Approval tests: pass draft text, assert `approved` or `revision_needed`
- Repository tests: use in-memory SQLite (`sqlite:///:memory:`), test CRUD
- Content tests: call `generate_content_ideas(theme)`, assert structure

---

## Common Troubleshooting

| Problem | Fix |
|---------|-----|
| DB has stale data | `Remove-Item data\app.db; python -m src daily-plan` |
| Company not in report | Add to `research_sources.py` `_DATA` dict and `company_targeting.py` `TARGET_COMPANIES` |
| Lead score too low | Check `description_snippet` for keyword coverage; edit scoring weights in `scoring.py` |
| Word file permission error | Close Word doc first, or the report auto-saves with timestamp suffix |
| `ModuleNotFoundError` | Run `pip install -e .` from project root |
| Tests failing | Check `data/app.db` is not locked; tests use in-memory DB so shouldn't conflict |
