"""Build human-readable password strength reports.

Everything here is a thin wrapper around `checker.check_strength` - this
module is only responsible for formatting and ordering, not for deciding
what makes a password strong.
"""

from checker import check_strength


def summarize_one(password):
    """Format one password's score and (if any) its missing criteria as a
    single line of text."""
    score, reasons = check_strength(password)
    if reasons:
        return f"{password}: {score}/5 (missing: {'; '.join(reasons)})"
    return f"{password}: {score}/5"


def summarize_many(passwords):
    """Format a whole batch of passwords, one `summarize_one` line each,
    in the same order they were given."""
    return "\n".join(summarize_one(p) for p in passwords)


def rank_by_strength(passwords):
    """Return `passwords` sorted strongest-first. Ties keep their original
    relative order."""
    return sorted(passwords, key=lambda p: check_strength(p)[0], reverse=True)
