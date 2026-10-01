"""Parse and format compact duration strings like "1d2h3m4s"."""

import re

_COMPONENT_RE = re.compile(r"([0-9]+)([dhms])")
_UNIT_SECONDS = {"d": 86400, "h": 3600, "m": 60, "s": 1}
_UNIT_ORDER = "dhms"


class DurationError(ValueError):
    """Raised when a duration string is malformed."""


def parse_duration(text):
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")

    body = text
    negative = False
    if body.startswith("-"):
        negative = True
        body = body[1:]

    if body == "":
        raise DurationError("duration has no components")

    pos = 0
    last_unit_index = -1
    total = 0
    seen = set()

    while pos < len(body):
        match = _COMPONENT_RE.match(body, pos)
        if not match or match.start() != pos:
            raise DurationError(f"invalid duration syntax at position {pos}")
        digits, unit = match.group(1), match.group(2)
        unit_index = _UNIT_ORDER.index(unit)
        if unit in seen:
            raise DurationError(f"unit {unit!r} repeated")
        if unit_index <= last_unit_index:
            raise DurationError(f"unit {unit!r} out of order")
        seen.add(unit)
        last_unit_index = unit_index
        total += int(digits) * _UNIT_SECONDS[unit]
        pos = match.end()

    if pos != len(body):
        raise DurationError("trailing characters in duration")

    return -total if negative else total


def format_duration(total_seconds):
    if isinstance(total_seconds, bool) or not isinstance(total_seconds, int):
        raise TypeError(
            f"total_seconds must be an int, got {type(total_seconds).__name__}"
        )

    if total_seconds == 0:
        return "0s"

    negative = total_seconds < 0
    remaining = abs(total_seconds)

    parts = []
    for unit in _UNIT_ORDER:
        size = _UNIT_SECONDS[unit]
        value, remaining = divmod(remaining, size)
        if value:
            parts.append(f"{value}{unit}")

    return ("-" if negative else "") + "".join(parts)
