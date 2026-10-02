"""Helpers for a tiny in-memory job scheduler."""


def make_job_id(prefix, n):
    """Build a simple deterministic job id, like 'job-3'."""
    return f"{prefix}-{n}"
