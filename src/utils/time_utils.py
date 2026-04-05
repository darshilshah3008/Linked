"""Time utility functions."""

from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime) -> str:
    """Format a datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def days_ago(dt: datetime) -> int:
    """Return number of days between dt and now."""
    delta = utcnow() - dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else utcnow() - dt
    return max(0, delta.days)
