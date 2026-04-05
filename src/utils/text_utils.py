"""Text utility functions."""

from __future__ import annotations


def truncate(text: str, max_length: int = 200) -> str:
    """Truncate text to max_length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def clean_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    return " ".join(text.split())
