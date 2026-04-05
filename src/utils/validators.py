"""Input validators."""

from __future__ import annotations

VALID_MESSAGE_TYPES = {
    "recruiter_intro",
    "hiring_manager_intro",
    "connection_note",
    "follow_up",
    "post_engagement_comment",
}

VALID_LEAD_STATUSES = {"new", "reviewed", "applied", "rejected", "archived"}
VALID_CONTENT_STATUSES = {"draft", "approved", "posted", "archived"}
VALID_OUTREACH_STATUSES = {"pending", "approved", "rejected", "revision_needed"}


def validate_message_type(message_type: str) -> bool:
    """Check if message type is valid."""
    return message_type in VALID_MESSAGE_TYPES


def validate_lead_status(status: str) -> bool:
    """Check if lead status is valid."""
    return status in VALID_LEAD_STATUSES
