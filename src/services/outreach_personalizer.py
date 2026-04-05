"""Outreach message personalizer.

Generates draft outreach messages based on lead/company context.
Uses templates when no LLM is configured.
"""

from __future__ import annotations

from typing import Optional

from src.schemas.outreach import OutreachInput


def draft_outreach_message(
    message_type: str,
    lead_title: str | None = None,
    company_name: str | None = None,
    company_summary: str | None = None,
    contact_name: str | None = None,
    contact_role: str | None = None,
    lead_id: int | None = None,
    contact_id: int | None = None,
    company_id: int | None = None,
) -> OutreachInput:
    """Generate a draft outreach message using templates.

    When an LLM is connected, this will use prompt_templates.OUTREACH_TEMPLATE
    for richer personalization.
    """
    company_display = company_name or "[Company Name]"
    lead_display = lead_title or "[Job Title]"
    contact_display = contact_name or "[Recipient Name]"
    role_display = contact_role or "[Their Role]"

    drafters = {
        "recruiter_intro": _draft_recruiter_intro,
        "hiring_manager_intro": _draft_hiring_manager_intro,
        "connection_note": _draft_connection_note,
        "follow_up": _draft_follow_up,
        "post_engagement_comment": _draft_post_engagement_comment,
    }

    drafter = drafters.get(message_type, _draft_connection_note)
    text = drafter(
        lead_title=lead_display,
        company_name=company_display,
        company_summary=company_summary,
        contact_name=contact_display,
        contact_role=role_display,
    )

    return OutreachInput(
        contact_id=contact_id,
        company_id=company_id,
        lead_id=lead_id,
        message_type=message_type,
        draft_text=text,
    )


def _draft_recruiter_intro(
    lead_title: str,
    company_name: str,
    company_summary: str | None,
    contact_name: str,
    contact_role: str,
) -> str:
    company_line = ""
    if company_summary:
        company_line = f" I'm particularly interested in {company_name}'s work — {company_summary}"

    return (
        f"Hi {contact_name},\n\n"
        f"I came across the {lead_title} opening at {company_name} and wanted to reach out.{company_line}\n\n"
        f"I'm an Embedded Software Engineer with 6+ years of experience in automotive, "
        f"agricultural, and industrial systems. My background in CAN/J1939, FreeRTOS, and "
        f"CI/CD for firmware teams aligns well with this role.\n\n"
        f"I'd welcome the chance to discuss how my experience could contribute to your team. "
        f"Would you be open to a brief conversation?\n\n"
        f"Best regards,\nDarshil Shah"
    )


def _draft_hiring_manager_intro(
    lead_title: str,
    company_name: str,
    company_summary: str | None,
    contact_name: str,
    contact_role: str,
) -> str:
    relevance = ""
    if company_summary:
        relevance = f"\n\nI noticed {company_name} works in {company_summary} — that's closely aligned with my experience in [SPECIFIC_PROJECT or domain area]."

    return (
        f"Hi {contact_name},\n\n"
        f"I'm reaching out regarding the {lead_title} role at {company_name}.{relevance}\n\n"
        f"In my current role at CNH Industrial, I develop embedded control software for "
        f"agricultural sprayers, working with CAN/J1939, MATLAB/Simulink code generation, "
        f"and CI/CD pipeline automation. I've contributed to reducing build times by ~40% "
        f"and helped resolve 100+ tracked field issues.\n\n"
        f"I'd value the opportunity to learn more about your team's embedded challenges. "
        f"Would a brief call work for you?\n\n"
        f"Best,\nDarshil Shah"
    )


def _draft_connection_note(
    lead_title: str,
    company_name: str,
    company_summary: str | None,
    contact_name: str,
    contact_role: str,
) -> str:
    return (
        f"Hi {contact_name}, I'm an Embedded Software Engineer interested in "
        f"{company_name}'s work in [SPECIFIC_AREA]. I'd like to connect and learn "
        f"more about your embedded engineering team. — Darshil"
    )


def _draft_follow_up(
    lead_title: str,
    company_name: str,
    company_summary: str | None,
    contact_name: str,
    contact_role: str,
) -> str:
    return (
        f"Hi {contact_name},\n\n"
        f"I wanted to follow up on my previous message regarding the {lead_title} "
        f"role at {company_name}. I remain very interested in this opportunity and "
        f"would welcome any updates.\n\n"
        f"Please let me know if there's any additional information I can provide.\n\n"
        f"Best,\nDarshil Shah"
    )


def _draft_post_engagement_comment(
    lead_title: str,
    company_name: str,
    company_summary: str | None,
    contact_name: str,
    contact_role: str,
) -> str:
    return (
        f"Great post, {contact_name}. [REFERENCE_SPECIFIC_POINT from their post]. "
        f"This resonates with my experience working on embedded systems in "
        f"[RELEVANT_DOMAIN]. [ADD_BRIEF_INSIGHT_OR_QUESTION]."
    )
