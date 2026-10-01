"""Redact sensitive substrings (emails, phone numbers) from text."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RedactionRule:
    name: str
    pattern: str
    mask: str


DEFAULT_RULES = (
    RedactionRule("email", r"[\w.+-]+@[\w-]+\.[\w.-]+", "[REDACTED-EMAIL]"),
    RedactionRule("phone", r"\b\d{3}[-.]\d{3}[-.]\d{4}\b", "[REDACTED-PHONE]"),
)


def redact(content, rules=DEFAULT_RULES):
    """Redact `content` according to `rules`, applied in order: each
    rule's substitution is applied to the result of the previous rule's
    substitution.

    `content` may be `str` or `bytes`. Bytes are treated as UTF-8; decoding
    errors are not caught here. The return type mirrors the input type.

    Returns `(result, counts)` where `counts` maps every rule's name to how
    many times it matched (0 if it didn't match at all).
    """
    if isinstance(content, bytes):
        text = content.decode("utf-8")
        was_bytes = True
    elif isinstance(content, str):
        text = content
        was_bytes = False
    else:
        raise TypeError("content must be str or bytes")

    counts = {}
    for rule in rules:
        text, n = re.subn(rule.pattern, rule.mask, text)
        counts[rule.name] = n

    if was_bytes:
        return text.encode("utf-8"), counts
    return text, counts
