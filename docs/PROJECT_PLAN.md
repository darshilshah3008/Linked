# Project Plan

## Phase 1: MVP (Current)

**Status: Complete**

Core local-first job search copilot with:
- CLI interface for all workflows
- 6 agents (orchestrator, lead finder, company research, content, outreach, approval)
- SQLite CRM layer with 8 entity types
- Deterministic lead scoring with 37 passing tests
- Mock data sources with adapter pattern for future integrations
- Anti-hallucination safeguards in approval agent

## Phase 2: Real Data Sources

**Status: Not started**

- [ ] Implement `PublicCareerPageAdapter` — fetch job listings from company careers pages via httpx
- [ ] Add RSS/Atom feed adapter for job aggregation
- [ ] Implement `PublicWebResearchSource` — scrape company about/engineering pages
- [ ] Add rate limiting and robots.txt compliance
- [ ] Add caching layer for fetched pages

## Phase 3: LLM-Powered Generation

**Status: Stub ready**

- [ ] Connect OpenAI client for content generation
- [ ] Enhance outreach personalization with LLM context
- [ ] Add LLM-based company research summarization
- [ ] Implement structured JSON output parsing from LLM responses
- [ ] Add local LLM support (Ollama, llama.cpp)

## Phase 4: Web Dashboard

**Status: Not started**

- [ ] FastAPI backend serving CRM data
- [ ] Simple HTML dashboard showing daily plan, leads, content queue
- [ ] Approval workflow in browser (approve/reject/revise buttons)
- [ ] Lead pipeline visualization

## Phase 5: Advanced Features

**Status: Not started**

- [ ] Resume tailoring per lead (highlight relevant experience)
- [ ] Interview prep agent (company-specific question generation)
- [ ] Application timeline tracking with reminders
- [ ] LinkedIn SSI improvement tracking
- [ ] Email integration for application confirmations
