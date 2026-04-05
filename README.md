# Job Search Copilot

A **multi-agent CLI tool** for Embedded Software Engineers to find jobs, research companies, discover hiring contacts, draft LinkedIn content, and create personalized outreach messages. Built as a **local-first** Python application with a SQLite CRM, deterministic scoring engine, and a human-in-the-loop approval workflow.

> **This is a copilot, not an automation bot.** It drafts, recommends, scores, and organizes. You decide what to send, post, or apply to.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [CLI Commands](#cli-commands)
  - [seed](#seed--initialize-database-with-sample-data)
  - [find-leads](#find-leads--discover-and-score-job-leads)
  - [find-people](#find-people--discover-contacts-at-target-companies)
  - [research-companies](#research-companies--batch-research-all-target-companies)
  - [research-company](#research-company--research-a-single-company)
  - [draft-content](#draft-content--generate-linkedin-post-drafts)
  - [draft-outreach](#draft-outreach--create-personalized-outreach-messages)
  - [daily-plan](#daily-plan--generate-the-full-daily-dashboard)
- [Lead Scoring Engine](#lead-scoring-engine)
- [Generating Reports](#generating-reports)
  - [JSON Export](#json-export)
  - [Word Document Report](#word-document-report)
- [Database Schema](#database-schema)
- [Agents and Workflow](#agents-and-workflow)
- [Safety Boundaries](#safety-boundaries)
- [Running Tests](#running-tests)
- [Configuration Reference](#configuration-reference)
- [LLM Integration](#llm-integration)
- [Extension Roadmap](#extension-roadmap)
- [License](#license)

---

## Features

| Capability | Description |
|---|---|
| **Find Leads** | Discover embedded software job opportunities from configured sources, scored 0-100 by profile fit |
| **Find People** | Discover hiring managers, recruiters, and engineering leads at 96+ target companies |
| **Research Companies** | Build structured intelligence on target companies (industry, embedded relevance, careers URLs, notes) |
| **Draft Content** | Generate LinkedIn post ideas and drafts across 8 embedded engineering themes |
| **Draft Outreach** | Create personalized recruiter/hiring manager messages grounded in real context |
| **Daily Dashboard** | Get a prioritized action plan with ranked jobs, contacts, companies, outreach drafts, and content ideas |
| **Export Reports** | Export the full dashboard to JSON or generate a comprehensive Word document (.docx) report |
| **Approval Workflow** | All outreach and content pass through a safety/quality review before being marked ready |
| **Track Everything** | SQLite-backed CRM for leads, companies, contacts, applications, outreach, content, and approvals |

### What It Does NOT Do

- Auto-apply to jobs
- Auto-send LinkedIn messages or connection requests
- Auto-post or auto-comment on LinkedIn
- Scrape restricted platforms or bypass authentication
- Simulate browser clicks or impersonate users
- Fabricate job listings, companies, or people

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLI (Typer + Rich)                   │
│   seed | find-leads | find-people | research-companies  │
│   research-company | draft-content | draft-outreach     │
│   daily-plan [--export dashboard.json]                  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                 Orchestrator Agent                       │
│   Routes requests, coordinates agents, builds dashboard │
└──┬──────┬──────┬──────┬──────┬──────┬───────────────────┘
   │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│Lead  ││People││Comp. ││Comp. ││Cont. ││Out-  │
│Finder││Finder││Target││Rsrch ││Agent ││reach │
└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘
   │       │       │       │       │       │
   │       │       │       │       │       ▼
   │       │       │       │       │   ┌──────┐
   │       │       │       │       │   │Apprvl│  ← Reviews all external-facing
   │       │       │       │       │   │Agent │    drafts for safety & quality
   │       │       │       │       │   └──┬───┘
   ▼       ▼       ▼       ▼       ▼      ▼
┌─────────────────────────────────────────────────────────┐
│             SQLite CRM / Memory Layer                   │
│  leads | companies | contacts | content | outreach      │
│  applications | approvals | activity_logs | snapshots   │
└─────────────────────────────────────────────────────────┘
         │                               │
         ▼                               ▼
   dashboard.json              dashboard_report.docx
   (JSON export)               (Word document report)
```

### Agents

| Agent | Responsibility |
|---|---|
| **Orchestrator** | Coordinates all agents, generates daily plans, builds the full dashboard snapshot |
| **Lead Finder** | Fetches job leads from configured sources, scores each for relevance (0-100) |
| **People Finder** | Discovers hiring contacts (managers, recruiters, engineers) at 42+ target companies |
| **Company Targeting** | Batch-researches 96+ predetermined target companies for relevance |
| **Company Research** | Researches a single company in detail (industry, embedded relevance, notes) |
| **Content Agent** | Generates LinkedIn post drafts, weekly plans, and 30-day content calendars |
| **Outreach Agent** | Drafts personalized outreach messages with 5 message types |
| **Approval Agent** | Reviews all externally visible content for safety, spam, and factuality |

### Key Design Decisions

| Decision | Rationale |
|---|---|
| **Adapter pattern** for lead/research/people sources | Swap mock data for real APIs without changing agents |
| **Swappable LLM client** | Runs with mock client by default; plug in OpenAI when ready |
| **Deterministic scoring (0-100)** | Transparent, testable, tunable scoring with no black box |
| **Anti-hallucination rules** | `null` for unknowns, `source_url` for facts, confidence markers |
| **Approval gating** | All outreach and content reviewed before being marked ready |
| **Mock-first design** | Works out of the box with no API keys or external services |
| **SQLite + SQLAlchemy** | Portable, local, no server needed — easily upgradeable to PostgreSQL |

---

## Project Structure

```
job-search-copilot/
├── README.md                          # This file
├── pyproject.toml                     # Project metadata, dependencies, entry points
├── requirements.txt                   # Pinned dependencies
├── inspect_db.py                      # Database inspection utility
├── generate_report_docx.py            # Word document report generator
│
├── data/
│   ├── app.db                         # SQLite database (auto-created)
│   ├── copilot.log                    # Application log file (auto-created)
│   └── seeds/
│       ├── sample_leads.json          # 8 sample embedded job leads
│       └── sample_companies.json      # 5 sample companies
│
├── docs/
│   ├── PROJECT_PLAN.md                # Original project plan
│   ├── TASK_BREAKDOWN.md              # Development task breakdown
│   ├── KNOWN_LIMITATIONS.md           # Current limitations
│   └── FUTURE_INTEGRATIONS.md         # Planned future features
│
├── src/
│   ├── __init__.py
│   ├── __main__.py                    # Entry point: `python -m src`
│   ├── main.py                        # App initialization
│   ├── cli.py                         # Typer CLI — all 8 commands defined here
│   ├── config.py                      # Pydantic Settings from .env
│   ├── logging_config.py              # Loguru config (console + file)
│   │
│   ├── agents/                        # Multi-agent system
│   │   ├── __init__.py
│   │   ├── orchestrator.py            # Central coordinator, daily dashboard builder
│   │   ├── lead_finder.py             # Job lead discovery & scoring
│   │   ├── people_finder.py           # Contact discovery at target companies
│   │   ├── company_targeting.py       # Batch company research (96+ companies)
│   │   ├── company_research.py        # Single company research
│   │   ├── content_agent.py           # LinkedIn content drafting
│   │   ├── outreach_agent.py          # Outreach message drafting
│   │   └── approval.py               # Safety & quality review
│   │
│   ├── db/                            # Database layer
│   │   ├── __init__.py
│   │   ├── models.py                  # SQLAlchemy ORM models (9 tables)
│   │   ├── repository.py             # Repository pattern — CRUD for all entities
│   │   ├── init_db.py                 # Engine, session factory, table creation
│   │   └── seed.py                    # Seed data loader from JSON files
│   │
│   ├── schemas/                       # Pydantic data models
│   │   ├── __init__.py
│   │   ├── lead.py                    # LeadInput, LeadRecord, LeadScoreResult
│   │   ├── company.py                 # CompanyInput, CompanyRecord
│   │   ├── content.py                 # ContentInput, ContentRecord, ContentPlan
│   │   ├── outreach.py               # OutreachInput, OutreachRecord, ContactInput
│   │   ├── approval.py               # ApprovalRequest, ApprovalDecision
│   │   └── actions.py                # ActionItem, DailyPlan, DashboardSnapshot
│   │
│   ├── services/                      # Business logic & adapters
│   │   ├── __init__.py
│   │   ├── scoring.py                 # Deterministic lead scoring (0-100)
│   │   ├── lead_sources.py           # Lead source adapter pattern (mock + stubs)
│   │   ├── research_sources.py       # Company research adapter (mock, 96+ companies)
│   │   ├── content_planner.py        # Content calendar & template-based drafts
│   │   ├── outreach_personalizer.py  # 5 outreach message templates
│   │   ├── prompt_templates.py        # Jinja2 prompt templates for LLM agents
│   │   └── llm_client.py            # Swappable LLM interface (mock + OpenAI)
│   │
│   └── utils/                         # Shared utilities
│       ├── __init__.py
│       ├── text_utils.py              # truncate(), clean_whitespace()
│       ├── time_utils.py              # utcnow(), format_datetime(), days_ago()
│       └── validators.py             # Message type & status validators
│
└── tests/                             # Test suite (38 tests)
    ├── __init__.py
    ├── test_scoring.py                # 10 tests — lead relevance scoring
    ├── test_approval.py               # 9 tests — approval safety checks
    ├── test_repository.py             # 13 tests — CRUD operations
    └── test_content.py                # 6 tests — content generation
```

---

## Getting Started

### Prerequisites

- **Python 3.11+** (tested with 3.12)
- **pip** (Python package manager)
- **Git** (to clone the repo)

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd job-search-copilot

# 2. Create a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 3. Install in development mode
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt
```

After installation, you can run commands in two ways:
```bash
# Option A: Module mode (always works)
python -m src <command>

# Option B: Installed entry point (if pip install -e . was used)
copilot <command>
```

### Configuration

Create a `.env` file in the project root (optional — sensible defaults are provided):

```bash
# Database
DATABASE_URL=sqlite:///data/app.db

# LLM Provider (mock = no API key needed)
LLM_PROVIDER=mock
# OPENAI_API_KEY=sk-...          # Uncomment if using OpenAI
# OPENAI_MODEL=gpt-4o-mini       # OpenAI model to use

# Job Search Profile
LEAD_KEYWORDS=embedded software engineer,firmware engineer,embedded systems,controls engineer
PREFERRED_LOCATIONS=Manitowoc,Wisconsin,Remote,USA

# Content Strategy
POSTS_PER_WEEK=3
CONTENT_TONE=professional

# Logging
LOG_LEVEL=INFO
LOG_FILE=data/copilot.log
```

### First Run

```bash
# Seed sample data into the database
python -m src seed

# Find and score job leads
python -m src find-leads

# Discover contacts at target companies
python -m src find-people

# Research all target companies
python -m src research-companies

# Generate the full daily dashboard and export to JSON
python -m src daily-plan --export dashboard.json

# Generate a Word document report
python generate_report_docx.py
```

---

## CLI Commands

All commands are run with `python -m src <command>` or `copilot <command>`.

### `seed` — Initialize database with sample data

```bash
python -m src seed
```

Seeds the database with 8 sample embedded job leads and 5 sample companies from `data/seeds/`. Safe to run multiple times — leads append, companies skip duplicates. Creates `data/app.db` if it doesn't exist.

---

### `find-leads` — Discover and score job leads

```bash
python -m src find-leads
python -m src find-leads --limit 10
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--limit` | int | 20 | Maximum number of leads to fetch |

Fetches leads from configured sources (currently 61 mock leads across 96+ companies), scores each on a 0-100 scale, and saves to the database. Displays a ranked table with fit scores, confidence levels, match reasons, and gaps.

**Example output:**
```
                            Top 10 Leads
┌────┬──────────────────────┬──────────────┬──────────┬───────┬────────────┐
│ #  │ Title                │ Company      │ Location │ Fit   │ Confidence │
├────┼──────────────────────┼──────────────┼──────────┼───────┼────────────┤
│ 1  │ Senior Firmware Eng  │ Honeywell    │ Remote   │ 100   │ high       │
│ 2  │ Controls Engineer    │ Siemens      │ Remote   │ 94    │ high       │
│ 3  │ Sr Embedded SW Eng   │ Deere & Co   │ Moline   │ 93    │ high       │
│ 4  │ Firmware Engineer    │ Rockwell     │ Milwaukee│ 87    │ high       │
│ 5  │ Embedded Controls    │ Cummins      │ Columbus │ 93    │ high       │
└────┴──────────────────────┴──────────────┴──────────┴───────┴────────────┘
```

---

### `find-people` — Discover contacts at target companies

```bash
python -m src find-people
python -m src find-people --limit 30
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--limit` | int | 20 | Maximum number of contacts to discover |

Discovers hiring managers, embedded engineering leads, and recruiters at 42+ target companies. Contacts are ranked by priority (HIGH > MEDIUM > LOW) and deduplicated.

---

### `research-companies` — Batch research all target companies

```bash
python -m src research-companies
```

Researches all 96+ target companies in the system and displays a summary table with industry, embedded relevance rating (HIGH / MEDIUM / LOW / UNKNOWN), careers URLs, and recommended next steps.

**Company coverage includes:**
- **Agricultural/Industrial:** Deere & Company, CNH Industrial, AGCO, Caterpillar, Rockwell Automation, etc.
- **Semiconductor:** Qualcomm, Intel, Texas Instruments, Analog Devices, Infineon, Broadcom, etc.
- **Automotive:** Ford, GM, Tesla, Aptiv, Magna, Cummins, Lucid Motors, ZF Group, etc.
- **Aerospace/Defense:** Boeing, Lockheed Martin, Raytheon, Northrop Grumman, GE Aerospace
- **Robotics/Consumer HW:** Boston Dynamics, iRobot, DJI, Sony, Panasonic, ABB
- **Big Tech:** Apple, Google, Meta, Microsoft, Amazon
- **Networking:** Cisco, Arista Networks, Juniper Networks
- **Software/Consulting (H1B sponsors):** Accenture, Adobe, Anthropic, Databricks, Deloitte, TikTok, Uber, and 30+ more

---

### `research-company` — Research a single company

```bash
python -m src research-company --company "CNH Industrial"
python -m src research-company --company "Qualcomm"
```

**Options:**
| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--company` | str | Yes | Company name to research |

Outputs structured intelligence: industry, website, careers URL, embedded relevance, summary, research notes, and recommended next action.

---

### `draft-content` — Generate LinkedIn post drafts

```bash
python -m src draft-content --theme "embedded cicd"
python -m src draft-content --theme "rtos design" --count 2
python -m src draft-content --theme "can j1939"
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--theme` | str | Required | Content theme to generate ideas for |
| `--count` | int | 3 | Number of ideas to generate |

**Available themes (8 topics):**

| Theme | Topics Covered |
|---|---|
| `embedded debugging` | Production debug strategies, JTAG, logic analyzers, printf debugging |
| `rtos design` | FreeRTOS patterns, task priorities, memory management |
| `can j1939` | CAN bus in practice, J1939 protocol, vehicle networking |
| `embedded cicd` | CI/CD pipelines for firmware teams, HIL testing, automated builds |
| `system integration` | Firmware integration challenges, hardware-software handoffs |
| `industrial embedded` | Architecture patterns for industrial control systems |
| `field reliability` | Reducing field failures, watchdog timers, error handling |
| `model based development` | MATLAB/Simulink code generation, model-in-loop testing |

Each theme includes ideas with hooks, outlines, and full draft text — grounded in real embedded engineering experience, with no fabricated achievements.

---

### `draft-outreach` — Create personalized outreach messages

```bash
python -m src draft-outreach --lead-id 1 --type recruiter_intro
python -m src draft-outreach --lead-id 3 --type hiring_manager_intro
python -m src draft-outreach --lead-id 5 --type connection_note
python -m src draft-outreach --lead-id 1 --type follow_up
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--lead-id` | int | Required | Database ID of the lead to draft outreach for |
| `--type` | str | `recruiter_intro` | Message type (see below) |

**Message types:**

| Type | Purpose | Approx. Length |
|---|---|---|
| `recruiter_intro` | First message to recruiter about a specific role | ~300 words |
| `hiring_manager_intro` | Personalized note to a hiring manager | ~300 words |
| `connection_note` | Short LinkedIn connection request | ~50 words |
| `follow_up` | Follow-up on a previous conversation | ~150 words |
| `post_engagement_comment` | Comment on someone's LinkedIn post | ~100 words |

Each draft automatically goes through the **Approval Agent** which checks for unsupported claims, spam language, and unsafe automation indicators. Uses `[PLACEHOLDER]` markers where data is missing instead of fabricating details.

---

### `daily-plan` — Generate the full daily dashboard

```bash
python -m src daily-plan
python -m src daily-plan --export dashboard.json
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--export` | str | None | File path to export dashboard as JSON |

The **core command**. The orchestrator:
1. Finds and scores all job leads
2. Discovers contacts at target companies
3. Researches all target companies
4. Generates outreach drafts (recruiter, hiring manager, connection notes)
5. Creates LinkedIn content ideas and a post draft
6. Assembles everything into a `DashboardSnapshot`

Displays a Rich-formatted terminal dashboard and optionally exports the full data to JSON for report generation.

---

## Lead Scoring Engine

Every job lead is scored on a **deterministic 0-100 scale** (no ML or opaque models). The scoring is fully documented, testable, and tunable.

### Scoring Formula

| Factor | Max Points | What It Checks |
|--------|------------|----------------|
| **Title Keyword Match** | 35 | Scans title & description for: `embedded software`, `firmware`, `embedded systems`, `rtos`, `controls engineer` |
| **Industry Match** | 20 | Company industry or description keywords: `automotive`, `agriculture`, `industrial`, `iot`, `machinery`, `defense`, `aerospace`, `robotics` |
| **Protocol/Stack Match** | 20 | Technical stack mentions: `can`, `j1939`, `freertos`, `c/c++`, `stm32`, `spi`, `i2c`, `uart`, `matlab`, `simulink` |
| **Seniority Fit** | 15 | `senior` = full points, `mid-level` = 60%, `junior`/`intern` = 10% |
| **Location Match** | 10 | Preferred locations = full points, `remote` = 90%, other = 30% |

### Score Output

Each scored lead includes:
- **`score`** (0-100, float)
- **`confidence`** — `high` (score >= 70), `medium` (40-69), `low` (< 40)
- **`match_reasons`** — Exact keywords and factors that matched
- **`missing_requirements`** — Gaps identified in the listing
- **`observed_facts`** — Raw facts extracted from the listing

### Example

A "Senior Embedded Software Engineer" at Deere & Company mentioning CAN, J1939, and FreeRTOS in Moline, IL would score approximately **93/100** (high confidence):
- Title: 35/35 (direct "embedded software" match)
- Industry: 20/20 (agriculture)
- Protocol: 20/20 (CAN + J1939 + FreeRTOS)
- Seniority: 15/15 (senior)
- Location: 3/10 (Moline, not preferred location)

---

## Generating Reports

### JSON Export

The `daily-plan` command with `--export` produces a `dashboard.json` file containing:
- All scored job leads (ranked by fit score)
- All discovered contacts (ranked by priority)
- All researched companies (sorted by embedded relevance)
- Outreach message drafts
- LinkedIn comment ideas and post draft

```bash
python -m src daily-plan --export dashboard.json
```

### Word Document Report

A comprehensive Word document report can be generated from `dashboard.json`:

```bash
python generate_report_docx.py
```

**Dependencies:** Requires `python-docx` and `lxml`:
```bash
pip install python-docx lxml
```

The generated `.docx` report includes 6 sections:

| Section | Contents |
|---------|----------|
| **1. All Job Leads** | Master table + detailed breakdown for every lead (fit score, match reasons, gaps, apply URLs) |
| **2. All Contacts** | Master table + individual profiles with role, company, priority, and outreach strategy |
| **3. All Companies** | Master table of all 96+ companies, then grouped by relevance (HIGH / MEDIUM / LOW / UNKNOWN) with full details, careers URLs, research notes, and recommended actions |
| **4. Outreach Drafts** | Formatted outreach messages ready for review and sending |
| **5. LinkedIn Comments** | Comment drafts with themes and hooks |
| **6. LinkedIn Post** | Full post draft with theme, hook, outline, and body text |

The report automatically handles file locks (saves with timestamp suffix if the file is open).

---

## Database Schema

SQLite database at `data/app.db` with 9 tables managed by SQLAlchemy ORM:

| Table | Key Columns | Purpose |
|-------|------------|---------|
| **leads** | id, title, company, location, source, url, relevance_score, match_reasons_json, confidence, status | Job opportunities with scoring |
| **companies** | id, name, website, careers_url, industry, embedded_relevance, research_notes, suggested_next_step | Company intelligence |
| **contacts** | id, name, role, company, linkedin_url, relevance_reason, contact_priority, suggested_outreach_type | People at target companies |
| **applications** | id, lead_id (FK), applied_date, status, resume_version | Application tracking |
| **outreach_messages** | id, contact_id, company_id, lead_id (FK), message_type, draft_text, approval_status, confidence_score | Message drafts under review |
| **content_items** | id, theme, content_type, hook, outline, full_text, status | Content drafts (posts, comments, articles) |
| **approval_records** | id, item_type, item_id, decision, reasons_json, confidence_score | Approval decision history |
| **activity_logs** | id, agent_name, action_type, summary, created_at | Full audit trail |
| **dashboard_snapshots** | id, snapshot_date, snapshot_json | Daily dashboard snapshots |

### Inspecting the Database

A utility script is included to quickly view database contents:

```bash
python inspect_db.py
```

Outputs table row counts, sample leads, all companies with relevance, outreach messages, and recent activity logs.

---

## Agents and Workflow

### How the Agents Interact

```
User runs CLI command
        │
        ▼
   ┌──────────┐
   │   CLI    │  Parses args, calls the appropriate agent
   └────┬─────┘
        │
        ▼
  ┌───────────────┐
  │ Orchestrator  │  For `daily-plan`: coordinates all agents below
  └──┬──┬──┬──┬──┘
     │  │  │  │
     │  │  │  └──► Outreach Agent ──► Approval Agent ──► DB
     │  │  └─────► Content Agent ──────────────────────► DB
     │  └────────► Company Targeting ──────────────────► DB
     │           ► People Finder ──────────────────────► DB
     └───────────► Lead Finder ── Scoring Engine ──────► DB
                                                         │
                                                         ▼
                                               DashboardSnapshot
                                                    (JSON)
```

### Agent Details

**Lead Finder** (`src/agents/lead_finder.py`):
1. Fetches raw leads from `LeadSource` adapters
2. Scores each lead via `score_lead()` (0-100)
3. Attaches match reasons, missing requirements, confidence level
4. Persists scored leads to the `leads` table
5. Returns top N leads sorted by score

**People Finder** (`src/agents/people_finder.py`):
1. Iterates through 42+ target companies
2. Calls `PeopleSource.find_people(company)` for each
3. Deduplicates contacts by (name, company)
4. Ranks by priority (HIGH > MEDIUM > LOW)
5. Persists to the `contacts` table

**Company Targeting** (`src/agents/company_targeting.py`):
1. Has a built-in list of 96+ target companies spanning all sectors
2. Calls `ResearchSource.research(company)` for each
3. Creates/updates `companies` table records
4. Returns companies sorted by embedded relevance

**Outreach Agent** (`src/agents/outreach_agent.py`):
1. Loads lead and company context from DB
2. Generates personalized message via `draft_outreach_message()`
3. Submits to `ApprovalAgent` for safety/quality review
4. Persists with approval status and confidence score

**Content Agent** (`src/agents/content_agent.py`):
1. Generates content ideas from 8 theme buckets
2. Each idea includes hook, outline, and full draft text
3. Supports weekly plans and 30-day content calendars

**Approval Agent** (`src/agents/approval.py`):
1. Scans text for unsupported claims, spam, and automation indicators
2. Cross-references against verified claims list
3. Checks minimum length and placeholder completeness
4. Returns decision: `approved`, `revision_needed`, or `rejected`

---

## Safety Boundaries

### What the Approval Agent Checks

| Check | Examples Flagged |
|-------|-----------------|
| **Unsupported claims** | Unverified percentages, "best in class", "guaranteed results", "top 1%" |
| **Spam language** | "Act now", "limited time", "!!!", urgency pressure |
| **Unsafe automation** | "auto-send", "auto-post", "auto-apply" |
| **Content length** | Drafts shorter than 20 characters |
| **Placeholders** | `[PLACEHOLDER]` tokens that need human completion |

### Verified Claims (Auto-Approved)

The system maintains a list of verified professional claims that won't be flagged:
- "40% build time reduction"
- "CAN/J1939 protocol implementation"
- "FreeRTOS task management"

### Anti-Hallucination Rules

1. Never infer a fact that was not observed — use `null` for unknown fields
2. Attach `source_url` for externally gathered facts
3. Distinguish: observed facts vs. inferred relevance vs. generated draft language
4. Include uncertainty markers: `confidence: high | medium | low`
5. Include `missing_fields` and `missing_requirements` for transparency
6. Approval layer rejects unsupported claims, invented metrics, and unverifiable personalization

---

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src

# Run a specific test file
python -m pytest tests/test_scoring.py -v
```

**Test breakdown (38 tests):**

| File | Tests | Coverage |
|------|-------|----------|
| `test_scoring.py` | 10 | Lead scoring formula, edge cases, confidence levels |
| `test_approval.py` | 9 | Spam detection, claim verification, safety checks |
| `test_repository.py` | 13 | CRUD for leads, companies, contacts, outreach, content, approvals |
| `test_content.py` | 6 | Content idea generation, weekly plans, theme validation |

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///data/app.db` | SQLAlchemy-compatible database URL |
| `LLM_PROVIDER` | `mock` | LLM provider: `mock` (no API needed) or `openai` |
| `OPENAI_API_KEY` | — | Required when `LLM_PROVIDER=openai` |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `LEAD_KEYWORDS` | `embedded software engineer,...` | Comma-separated job search keywords |
| `PREFERRED_LOCATIONS` | `Manitowoc,Wisconsin,Remote,USA` | Comma-separated preferred locations |
| `POSTS_PER_WEEK` | `3` | Target LinkedIn posts per week |
| `CONTENT_TONE` | `professional` | Tone for generated content |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | `data/copilot.log` | Log file path |

### Logging

Loguru-based logging with dual output:
- **Console** (stderr) — colored, human-readable
- **File** (`data/copilot.log`) — with rotation at 10 MB, 7-day retention

---

## LLM Integration

The system defaults to a **mock LLM client** that returns template-based, placeholder responses. No API key is required for the default experience.

### Connecting OpenAI

```bash
# In your .env file:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

```bash
# Install the OpenAI dependency:
pip install openai
# or
pip install -e ".[llm]"
```

### Adding Custom LLM Providers

The LLM interface is abstract (`src/services/llm_client.py`). To add a new provider:

1. Implement the `LLMClient` abstract class with `chat()` and `generate()` methods
2. Register it in `get_llm_client()` factory function
3. Set `LLM_PROVIDER=your_provider` in `.env`

Compatible with local LLMs (Ollama, llama.cpp), Anthropic, or any OpenAI-compatible API.

---

## Extension Roadmap

| Priority | Integration | Status |
|---|---|---|
| 1 | Real job board adapters (company careers pages, RSS) | Adapter interface ready |
| 2 | OpenAI/local LLM for richer content generation | Stub ready, needs API key |
| 3 | People discovery from LinkedIn public profiles | Adapter ready |
| 4 | FastAPI web dashboard | Optional dependency in pyproject.toml |
| 5 | Resume tailoring per lead | Not started |
| 6 | Interview prep agent | Not started |
| 7 | Email integration for application tracking | Not started |

---

## Typical Workflow

```bash
# ┌─────────────────────────────────────────────────┐
# │               SETUP (once)                       │
# └─────────────────────────────────────────────────┘
pip install -e .
python -m src seed

# ┌─────────────────────────────────────────────────┐
# │           DAILY ROUTINE                          │
# └─────────────────────────────────────────────────┘

# 1. Generate the full dashboard (finds leads, people, companies)
python -m src daily-plan --export dashboard.json

# 2. Generate a Word report for review
python generate_report_docx.py

# 3. Optionally explore specific areas
python -m src find-leads --limit 30
python -m src find-people --limit 50
python -m src research-company --company "Qualcomm"
python -m src draft-content --theme "can j1939"
python -m src draft-outreach --lead-id 1 --type recruiter_intro

# ┌─────────────────────────────────────────────────┐
# │           MAINTENANCE                            │
# └─────────────────────────────────────────────────┘
python inspect_db.py                  # View database contents
python -m pytest tests/ -v           # Run test suite
```

---

## License

MIT
