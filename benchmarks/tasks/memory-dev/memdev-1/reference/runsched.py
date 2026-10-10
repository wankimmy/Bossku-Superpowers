"""Scheduling helpers."""
from datetime import datetime, timedelta, timezone


def _now():
    return datetime.now(timezone.utc)


def _utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_iso(text):
    return _utc(datetime.fromisoformat(text))


def format_iso(dt):
    return _utc(dt).isoformat()


def age_seconds(created, now=None):
    return ((_utc(now) if now else _now()) - _utc(created)).total_seconds()


def start_of_today():
    return _now().replace(hour=0, minute=0, second=0, microsecond=0)


def next_run(last_run, every_hours):
    return _utc(last_run) + timedelta(hours=every_hours)
