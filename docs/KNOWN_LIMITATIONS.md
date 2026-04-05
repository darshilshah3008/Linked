# Known Limitations

## Data Sources

- **All lead data is currently mock.** The `MockLeadSource` returns 8 hardcoded sample leads. These are illustrative examples, not real job postings. Real job board integration requires implementing the `LeadSource` adapter interface.

- **Company research uses mock data.** Only CNH Industrial, Deere & Company, Rockwell Automation, and Oshkosh Corporation have pre-populated data. All other companies get a minimal record with `embedded_relevance: unknown`.

- **No live web scraping.** The adapter interfaces exist but no real HTTP-based source is implemented yet. This is intentional — adding scrapers requires careful handling of rate limits, robots.txt, and terms of service.

## LLM Integration

- **Default LLM is a mock.** All agent prompts are defined in `prompt_templates.py` but the mock client only returns placeholder text. Content and outreach drafts use hardcoded templates instead of LLM generation.

- **No chain-of-thought filtering.** When a real LLM is connected, responses are passed through as-is. A production system should parse structured JSON from LLM output and validate before use.

## Agents

- **No People Discovery Agent.** The prompt spec requests identifying relevant professionals (engineers, hiring managers). This is not implemented because it would require data sources that are either restricted (LinkedIn) or unavailable without API access.

- **No separate Job Scoring Agent.** Scoring is currently a service module (`scoring.py`) called by the Lead Finder. The spec describes a separate scoring agent, but a function is more appropriate at this scale.

- **Content Agent uses templates, not LLM.** Post drafts come from a library of pre-written templates organized by theme. Quality will improve significantly when connected to a real LLM.

- **Outreach personalization is limited.** Without company-specific research data or contact details, messages use `[PLACEHOLDER]` markers. These require manual replacement before sending.

## Approval Agent

- **Pattern-based only.** The approval agent uses regex patterns to detect issues. It cannot assess semantic meaning, factual nuance, or writing quality. It's a safety net, not a quality gate.

- **Verified claims are hardcoded.** The list of acceptable percentage claims (e.g., "40% build time reduction") comes from the user's resume. Adding new verified claims requires updating `ApprovalAgent.VERIFIED_CLAIMS`.

## CRM / Memory

- **No contact management CLI.** The `Contact` model exists in the database but there are no CLI commands to add, list, or manage contacts. This requires a simple CRUD extension to the CLI.

- **No application tracking CLI.** The `Application` model exists but has no CLI commands. Applications can only be created programmatically.

- **No data export.** There is no way to export leads, content, or outreach data to CSV, markdown, or any other format from the CLI.

## Infrastructure

- **SQLite only.** The system uses SQLite for simplicity. For multi-device access or larger scale, migration to PostgreSQL would be needed (SQLAlchemy makes this a configuration change).

- **No authentication.** The system is local-only with no user authentication. The planned FastAPI layer would need auth before deployment.

- **Logging goes to stderr.** On Windows PowerShell, loguru's stderr output causes exit code 1 even when commands succeed. This is cosmetic but may confuse users.

## Testing

- **No integration tests.** All tests are unit tests against individual modules. End-to-end workflow testing (seed → find → research → draft → approve) is not automated.

- **No LLM output tests.** Since the mock LLM returns fixed text, there are no tests validating LLM response parsing or structured output handling.
