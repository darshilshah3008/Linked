"""Content planner for LinkedIn content strategy.

Generates content calendars and drafts based on the user's
embedded engineering background.
"""

from __future__ import annotations

from src.schemas.content import ContentInput, ContentPlan

# ── Topic Buckets ──────────────────────────────────────────
# These are grounded in the user's actual background and skills.

TOPIC_BUCKETS: list[dict[str, str]] = [
    {
        "theme": "embedded debugging",
        "description": "Lessons from debugging embedded systems in production",
    },
    {
        "theme": "rtos design",
        "description": "Real-time operating system design tradeoffs and practical patterns",
    },
    {
        "theme": "can j1939",
        "description": "CAN/J1939 protocol lessons from agricultural and industrial systems",
    },
    {
        "theme": "embedded cicd",
        "description": "CI/CD pipelines for firmware teams: what works and what doesn't",
    },
    {
        "theme": "system integration",
        "description": "Firmware integration challenges and how to prevent them",
    },
    {
        "theme": "industrial embedded",
        "description": "Embedded software architecture for industrial and ag machinery",
    },
    {
        "theme": "field reliability",
        "description": "Reducing field failures through better embedded engineering practices",
    },
    {
        "theme": "model based development",
        "description": "MATLAB/Simulink code generation: practical realities",
    },
]


def generate_content_ideas(theme: str, count: int = 3) -> list[ContentInput]:
    """Generate content ideas for a given theme.

    These are template-based drafts. When an LLM is connected,
    this function will use prompt_templates to generate richer content.
    """
    theme_lower = theme.lower().replace("-", " ").replace("_", " ")

    templates = _get_theme_templates(theme_lower)
    results: list[ContentInput] = []

    for i, tmpl in enumerate(templates[:count]):
        results.append(
            ContentInput(
                theme=theme,
                content_type="linkedin_post",
                hook=tmpl["hook"],
                outline=tmpl["outline"],
                full_text=tmpl.get("full_text"),
            )
        )

    return results


def generate_weekly_plan(week_number: int, posts_per_week: int = 3) -> ContentPlan:
    """Generate a weekly content plan rotating through topic buckets."""
    items: list[ContentInput] = []
    bucket_count = len(TOPIC_BUCKETS)

    for i in range(posts_per_week):
        bucket_idx = ((week_number - 1) * posts_per_week + i) % bucket_count
        bucket = TOPIC_BUCKETS[bucket_idx]
        ideas = generate_content_ideas(bucket["theme"], count=1)
        items.extend(ideas)

    return ContentPlan(
        week_number=week_number,
        items=items,
        notes=f"Week {week_number}: {posts_per_week} posts planned across rotating themes.",
    )


def _get_theme_templates(theme: str) -> list[dict[str, str]]:
    """Return template drafts for a theme. These are starter templates, not final content."""

    _TEMPLATES: dict[str, list[dict[str, str]]] = {
        "embedded debugging": [
            {
                "hook": "The hardest embedded bugs aren't in your code — they're in the assumptions you made about your hardware.",
                "outline": "- Timing issues that only appear in production\n- How JTAG saved a week of debugging\n- Systematic debug approach for intermittent faults",
                "full_text": (
                    "The hardest embedded bugs aren't in your code — they're in the assumptions "
                    "you made about your hardware.\n\n"
                    "After years of debugging embedded systems in production environments, "
                    "I've learned that the most stubborn issues come from:\n\n"
                    "1. Timing assumptions that hold on the bench but fail in the field\n"
                    "2. Signal integrity issues that only manifest under load\n"
                    "3. Peripheral initialization order dependencies\n\n"
                    "The approach that works: instrument first, hypothesize second.\n\n"
                    "What's the most surprising embedded bug you've encountered?\n\n"
                    "(Generalized example based on common embedded engineering patterns)"
                ),
            },
            {
                "hook": "Your embedded CI pipeline is lying to you if it doesn't test on real hardware.",
                "outline": "- Why software-only testing misses hardware bugs\n- Minimal hardware-in-loop setups\n- When simulation is enough vs when it isn't",
            },
            {
                "hook": "Three things I check first on every embedded debug session.",
                "outline": "- Stack overflow indicators\n- Clock configuration verification\n- Peripheral register state dump",
            },
        ],
        "rtos design": [
            {
                "hook": "FreeRTOS task priorities: getting them wrong won't crash your system immediately — it'll crash it at the worst possible time.",
                "outline": "- Priority inversion in practice\n- How to design task hierarchies\n- Testing for timing regressions",
            },
            {
                "hook": "The real cost of dynamic memory allocation in RTOS systems.",
                "outline": "- Heap fragmentation over time\n- Static allocation patterns\n- Memory pool design",
            },
            {
                "hook": "Semaphores vs. queues: when to use which in FreeRTOS.",
                "outline": "- Common misuse patterns\n- Queue-based designs for data flow\n- Binary semaphore gotchas",
            },
        ],
        "can j1939": [
            {
                "hook": "J1939 looks simple until you have 15 ECUs on the same bus arguing about priority.",
                "outline": "- Message priority conflicts in multi-ECU systems\n- DM1 fault handling patterns\n- Bus load optimization",
            },
            {
                "hook": "Debugging CAN bus issues without a protocol analyzer is like debugging C without printf.",
                "outline": "- Essential CAN debug tools\n- Interpreting error frames\n- Common J1939 integration mistakes",
            },
            {
                "hook": "Why every embedded engineer working in vehicles should understand J1939 transport protocol.",
                "outline": "- Multi-packet messages in practice\n- BAM vs connection-mode\n- Edge cases that cause field failures",
            },
        ],
        "embedded cicd": [
            {
                "hook": "We reduced our firmware build and deploy time by 40% with GitLab CI. Here's what actually mattered.",
                "outline": "- Automating the build pipeline\n- Static analysis in CI\n- Binary artifact management",
                "full_text": (
                    "We reduced our firmware build and deploy time by 40% with GitLab CI. "
                    "Here's what actually mattered.\n\n"
                    "Most embedded teams still build firmware manually. "
                    "When I helped set up CI/CD for our firmware pipeline, the biggest wins were:\n\n"
                    "1. Automated builds on every commit — catches integration issues early\n"
                    "2. Static analysis gates — no merge without clean analysis\n"
                    "3. Binary versioning and artifact storage — always know what's deployed\n\n"
                    "The hardest part wasn't the tooling. It was convincing the team that "
                    "the upfront investment would pay off.\n\n"
                    "What's your experience with CI/CD in embedded teams?\n\n"
                    "(Based on real workflow improvements; specific metrics are approximate)"
                ),
            },
            {
                "hook": "The SVN-to-Git migration nobody wanted to do — and why it was worth it.",
                "outline": "- Migration planning for embedded repos\n- Handling binary assets\n- Branch strategies for firmware",
            },
            {
                "hook": "Docker for embedded builds: overkill or essential?",
                "outline": "- Reproducible build environments\n- Cross-compilation containers\n- When it adds unnecessary complexity",
            },
        ],
        "system integration": [
            {
                "hook": "The gap between 'firmware works on my bench' and 'firmware works in the vehicle' is where most integration bugs hide.",
                "outline": "- Environmental factors in integration\n- Interface contract testing\n- Incremental integration strategies",
            },
            {
                "hook": "Integrating a C# GUI with embedded firmware taught me more about system design than any textbook.",
                "outline": "- Communication protocol design\n- Latency requirements\n- Error handling across boundaries",
            },
            {
                "hook": "Three integration failures that changed how I design embedded systems.",
                "outline": "- Timing assumption failures\n- Protocol version mismatches\n- Power sequencing issues",
            },
        ],
        "industrial embedded": [
            {
                "hook": "Industrial embedded systems are unforgiving. There's no 'restart the app' when you're controlling machinery.",
                "outline": "- Safety-critical design mindset\n- Watchdog timer patterns\n- Graceful degradation strategies",
            },
            {
                "hook": "What agricultural machinery taught me about embedded software reliability.",
                "outline": "- Environmental extremes\n- Connectors and vibration\n- Operator expectations vs engineering constraints",
            },
            {
                "hook": "The difference between embedded software for consumer products and industrial equipment.",
                "outline": "- Lifecycle expectations (10+ years)\n- Serviceability requirements\n- Regulatory landscape",
            },
        ],
        "field reliability": [
            {
                "hook": "We reduced field failures by 30% — not by writing better code, but by writing better tests and tracking issues systematically.",
                "outline": "- Issue tracking as a reliability tool\n- Root cause patterns in field failures\n- Feedback loops from field to firmware",
            },
            {
                "hook": "Every field failure is a design review you didn't have.",
                "outline": "- Post-mortem culture for embedded teams\n- Common root causes\n- Building reliability metrics",
            },
            {
                "hook": "The firmware worked perfectly for 11 months. Then winter came.",
                "outline": "- Temperature-related firmware bugs\n- Environmental testing gaps\n- Defensive coding for extreme conditions\n(Generalized example)",
            },
        ],
        "model based development": [
            {
                "hook": "MATLAB/Simulink code generation is powerful — until you need to debug the generated C code.",
                "outline": "- Traceability between model and code\n- Integration with hand-written code\n- Verification strategies",
            },
            {
                "hook": "When model-based development saves time and when it creates more problems than it solves.",
                "outline": "- Suitable vs unsuitable use cases\n- Team skill requirements\n- Toolchain lock-in considerations",
            },
            {
                "hook": "Reducing integration issues by 40% with model-based development: what made the difference.",
                "outline": "- Consistent interface contracts from models\n- Early simulation before hardware\n- Code review of generated code",
            },
        ],
    }

    # Find best matching theme
    for key, templates in _TEMPLATES.items():
        if key in theme or theme in key:
            return templates

    # Fallback: return generic templates
    return [
        {
            "hook": f"Something every embedded engineer should know about {theme}.",
            "outline": f"- Key insight about {theme}\n- Practical application\n- Common mistakes",
        }
    ]
