"""Password strength scoring.

This module has exactly one job: look at a candidate password and say how
strong it is, with enough detail that a UI can tell the user what to fix.
It doesn't know anything about accounts, hashing, or storage - that all
happens elsewhere, after a password has already passed this check.
"""

SYMBOLS = "!@#$%^&*()-_=+"


def check_strength(password):
    """Score a password's strength and explain what's missing.

    Returns a tuple `(score, reasons)`:
    - `score` is an int from 0 to 5, one point per satisfied criterion below.
    - `reasons` is a list of strings describing each UNsatisfied criterion,
      in this fixed order: length, lowercase, uppercase, digit, symbol.

    If the password contains any whitespace character, scoring
    short-circuits: the result is always
    `(0, ["passwords may not contain whitespace"])`, regardless of
    anything else about the password.

    Raises `TypeError` if `password` is not a `str`.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    if any(c.isspace() for c in password):
        return 0, ["passwords may not contain whitespace"]

    score = 0
    reasons = []

    if len(password) >= 12:
        score += 1
    else:
        reasons.append("too short (needs at least 12 characters)")

    if any('a' <= c <= 'z' for c in password):
        score += 1
    else:
        reasons.append("missing a lowercase letter")

    if any('A' <= c <= 'Z' for c in password):
        score += 1
    else:
        reasons.append("missing an uppercase letter")

    if any('0' <= c <= '9' for c in password):
        score += 1
    else:
        reasons.append("missing a digit")

    if any(c in SYMBOLS for c in password):
        score += 1
    else:
        reasons.append("missing a symbol")

    return score, reasons
