"""Helpers for tracking login sessions."""

from datetime import datetime, timezone


DEFAULT_TIMEOUT_MINUTES = 30


def default_clock():
    return datetime.now(timezone.utc)


def create_session(user_id, clock=default_clock):
    return {"user_id": user_id, "created_at": clock()}


def is_expired(session, timeout_minutes=DEFAULT_TIMEOUT_MINUTES, clock=default_clock):
    elapsed = clock() - session["created_at"]
    return elapsed.total_seconds() >= timeout_minutes * 60


def describe_age(session, clock=default_clock):
    elapsed_seconds = int((clock() - session["created_at"]).total_seconds())

    if elapsed_seconds < 60:
        return "just now"

    minutes = elapsed_seconds // 60
    if minutes < 60:
        return _pluralize(minutes, "minute")

    hours = minutes // 60
    if hours < 24:
        return _pluralize(hours, "hour")

    days = hours // 24
    return _pluralize(days, "day")


def _pluralize(count, unit):
    suffix = "" if count == 1 else "s"
    return "{} {}{} ago".format(count, unit, suffix)
