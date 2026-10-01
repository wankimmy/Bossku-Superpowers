"""Password strength scoring."""

import warnings
from dataclasses import dataclass

SYMBOLS = "!@#$%^&*()-_=+"


@dataclass(frozen=True)
class PasswordReport:
    score: int
    reasons: tuple


def evaluate_password(password):
    """Score a password's strength and explain what's missing.

    Returns a `PasswordReport(score, reasons)`:
    - `score` is an int from 0 to 5, one point per satisfied criterion below.
    - `reasons` is a tuple of strings describing each UNsatisfied criterion,
      in this fixed order: length, lowercase, uppercase, digit, symbol.

    If the password contains any whitespace character, scoring
    short-circuits: the result is always
    `PasswordReport(0, ("passwords may not contain whitespace",))`,
    regardless of anything else about the password.

    Raises `TypeError` if `password` is not a `str`.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    if any(c.isspace() for c in password):
        return PasswordReport(0, ("passwords may not contain whitespace",))

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

    return PasswordReport(score, tuple(reasons))


def check_strength(password):
    """Deprecated alias for `evaluate_password`.

    Returns the old `(score, reasons)` shape, with `reasons` as a `list`.
    """
    warnings.warn(
        "check_strength is deprecated; use evaluate_password instead",
        DeprecationWarning,
        stacklevel=2,
    )
    report = evaluate_password(password)
    return report.score, list(report.reasons)
