# Task Breakdown

## MVP Tasks (Completed)

### Infrastructure
- [x] Python project setup (pyproject.toml, requirements.txt)
- [x] Environment configuration (.env.example, Pydantic settings)
- [x] Logging configuration (loguru)
- [x] SQLite database initialization

### Data Layer
- [x] Pydantic schemas for all 8 entities (lead, company, contact, application, outreach, content, approval, activity log)
- [x] SQLAlchemy ORM models
- [x] Repository with CRUD operations for all entities
- [x] Seed data (8 leads, 5 companies)

### Agents
- [x] Lead Finder Agent — fetches from sources, scores, persists
- [x] Company Research Agent — enriches with mock data, persists
- [x] Content Agent — generates ideas, weekly plans, 30-day calendar
- [x] Outreach Agent — drafts personalized messages, submits for approval
- [x] Approval Agent — pattern-based safety checks (spam, claims, automation)
- [x] Orchestrator Agent — daily plan generation from CRM state

### Services
- [x] Deterministic lead scoring (5 weighted factors)
- [x] Lead source adapter pattern (mock + interface for real sources)
- [x] Company research adapter pattern
- [x] Content planner with 8 topic buckets and templates
- [x] Outreach personalizer with 5 message types
- [x] Prompt templates for all agents (Jinja2)
- [x] Swappable LLM client (mock + OpenAI stub)

### CLI
- [x] `seed` command
- [x] `find-leads` command with limit option
- [x] `research-company` command
- [x] `draft-content` command with theme and count options
- [x] `draft-outreach` command with lead-id and type options
- [x] `daily-plan` command

### Tests
- [x] Scoring tests (10 tests — keyword matching, seniority, location, determinism)
- [x] Approval tests (8 tests — spam, safety, claims, placeholders)
- [x] Repository tests (13 tests — CRUD for all entities)
- [x] Content tests (6 tests — generation, plans, themes)

### Documentation
- [x] README.md
- [x] PROJECT_PLAN.md
- [x] TASK_BREAKDOWN.md
- [x] KNOWN_LIMITATIONS.md
- [x] FUTURE_INTEGRATIONS.md

---

## Next Tasks (Prioritized)

### High Priority
- [ ] Add `PublicCareerPageAdapter` for fetching real job postings
- [ ] Connect OpenAI client with structured output parsing
- [ ] Add People Discovery Agent for identifying relevant contacts
- [ ] Add Job Scoring Agent as a separate agent (currently scoring is inline)

### Medium Priority
- [ ] Add `apply` CLI command to track applications
- [ ] Add `contacts` CLI command to manage contacts
- [ ] Add content calendar export (markdown or CSV)
- [ ] Add outreach history per contact
- [ ] Implement comment draft generation for LinkedIn engagement

### Lower Priority
- [ ] FastAPI web interface
- [ ] Daily email digest
- [ ] Resume version tracking
- [ ] Interview prep generation
