# Future Integrations

## Tier 1: High Value, Low Risk

### Real Job Board Adapters
- **What:** Fetch actual job listings from public company careers pages
- **How:** Implement `PublicCareerPageAdapter` using httpx to fetch and parse career page HTML
- **Scope:** Start with 3-5 target companies (Deere, Rockwell, Oshkosh, Parker Hannifin, Caterpillar)
- **Safety:** Respect robots.txt, add rate limiting (1 request/second), cache results
- **Effort:** Medium — adapter interface already exists, need HTML parsing per site

### OpenAI / LLM Content Generation
- **What:** Use a real LLM for richer content drafts, outreach personalization, and company summaries
- **How:** Set `LLM_PROVIDER=openai` in `.env`, use existing `OpenAIClient` class
- **Scope:** All agents have Jinja2 prompt templates ready in `prompt_templates.py`
- **Safety:** Validate LLM output against schemas, apply approval checks to all generated text
- **Effort:** Low — client stub exists, need output parsing and validation

### Local LLM Support (Ollama)
- **What:** Run LLM inference locally using Ollama or llama.cpp
- **How:** Add `OllamaClient` implementing `LLMClient` interface, point to local endpoint
- **Scope:** Same prompts as OpenAI, just different HTTP endpoint
- **Safety:** Same validation pipeline, no API keys leave the machine
- **Effort:** Low — just another `LLMClient` implementation

## Tier 2: Medium Value, Medium Effort

### People Discovery Agent
- **What:** Identify relevant engineers, hiring managers, and recruiters at target companies
- **How:** Use public data sources (company team pages, conference speaker lists, published articles)
- **Scope:** Store in `contacts` table with relationship tracking
- **Safety:** Only use publicly available information, never fabricate connections
- **Blocked by:** Need reliable public data sources; LinkedIn API requires partnership

### FastAPI Dashboard
- **What:** Web UI showing daily plan, lead pipeline, content queue, approval workflow
- **How:** FastAPI backend + simple HTML/HTMX frontend
- **Scope:** Read-only dashboard first, then add approve/reject buttons
- **Safety:** Local-only by default, add basic auth if exposed
- **Effort:** Medium — FastAPI is an optional dependency, needs frontend work

### Application Tracking CLI
- **What:** Track job applications with status, dates, resume versions, and notes
- **How:** Add `apply`, `list-applications`, `update-application` CLI commands
- **Scope:** Uses existing `ApplicationModel` — just needs CLI and display logic
- **Effort:** Low — model and repository methods already exist

### Content Calendar Export
- **What:** Export the 30-day content plan as markdown, CSV, or calendar format
- **How:** Add `export-calendar` CLI command
- **Scope:** Generate markdown with weekly sections, post hooks, and scheduled dates
- **Effort:** Low

## Tier 3: High Value, High Effort

### Resume Tailoring
- **What:** Generate role-specific resume highlights per lead
- **How:** New agent that matches lead requirements against user profile and suggests emphasis areas
- **Scope:** Output a "resume notes" section per lead, not a full resume generator
- **Safety:** Only use stated experience, never fabricate
- **Effort:** High — needs LLM + careful prompt engineering

### Interview Prep Agent
- **What:** Generate company-specific interview questions and preparation notes
- **How:** Use company research + role requirements to generate likely technical questions
- **Scope:** CAN/J1939, RTOS, embedded C/C++ focused question banks
- **Safety:** Questions are educational aids, not predictions
- **Effort:** High — needs domain expertise in prompt design

### LinkedIn SSI Tracking
- **What:** Track LinkedIn Social Selling Index improvement over time
- **How:** Manual input of SSI scores with date tracking, trend visualization
- **Scope:** SSI currently at 29 (engagement = 0 is the critical gap)
- **Safety:** No LinkedIn API access needed — manual entry only
- **Effort:** Medium — needs data model extension and simple charting

### Email Integration
- **What:** Track application confirmation emails and recruiter responses
- **How:** IMAP/POP3 reader or Gmail API integration
- **Scope:** Parse application confirmations, link to lead records
- **Safety:** Requires careful credential handling, read-only access
- **Effort:** High — email parsing is complex and error-prone

## Integration Design Principles

1. **Adapter pattern** — all external data sources go through abstract interfaces
2. **Fail safely** — if a source is unavailable, log a warning and continue with cached/mock data
3. **Rate limiting** — no more than 1 request/second to any external source
4. **Respect TOS** — do not scrape sites that prohibit it in robots.txt or terms of service
5. **Cache aggressively** — company data changes slowly, cache for 7 days minimum
6. **Validate everything** — all external data passes through schema validation before storage
