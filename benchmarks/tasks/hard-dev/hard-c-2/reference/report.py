"""Build human-readable password strength reports."""

from checker import evaluate_password


def summarize_one(password):
    report = evaluate_password(password)
    if report.reasons:
        return f"{password}: {report.score}/5 (missing: {'; '.join(report.reasons)})"
    return f"{password}: {report.score}/5"


def summarize_many(passwords):
    return "\n".join(summarize_one(p) for p in passwords)


def rank_by_strength(passwords):
    """Return `passwords` sorted strongest-first. Ties keep their original
    relative order."""
    return sorted(passwords, key=lambda p: evaluate_password(p).score, reverse=True)
