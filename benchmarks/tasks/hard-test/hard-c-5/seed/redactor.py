"""Redact sensitive substrings (emails, phone numbers) from text.

This module only knows how to redact a single piece of content; `pipeline.py`
builds on it to process a whole batch of documents at once and keep running
totals of how often each rule fired.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RedactionRule:
    """One find-and-mask rule: every substring matching `pattern` (a
    regular expression) is replaced with `mask`. `name` identifies the
    rule in the counts dict `redact` returns."""

    name: str
    pattern: str
    mask: str


DEFAULT_RULES = (
    RedactionRule("email", r"[\w.+-]+@[\w-]+\.[\w.-]+", "[REDACTED-EMAIL]"),
    RedactionRule("phone", r"\b\d{3}[-.]\d{3}[-.]\d{4}\b", "[REDACTED-PHONE]"),
)


def redact(content, rules=DEFAULT_RULES):
    """Redact `content` (a `str`) according to `rules`, applied in order:
    each rule's substitution is applied to the result of the previous
    rule's substitution.

    Returns `(result, counts)` where `result` is the redacted text and
    `counts` is a dict mapping every rule's name to how many times it
    matched (0 if it didn't match at all).
    """
    text = content
    counts = {}
    for rule in rules:
        text, n = re.subn(rule.pattern, rule.mask, text)
        counts[rule.name] = n
    return text, counts
