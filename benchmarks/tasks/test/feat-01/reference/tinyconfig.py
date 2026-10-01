"""Tiny parser for key = value config text (durations, sizes, bools, numbers, strings)."""
import re

_DURATION_UNITS = {"ms": 0.001, "s": 1.0, "m": 60.0, "h": 3600.0, "d": 86400.0}
_SIZE_UNITS = {
    "B": 1,
    "KB": 1000, "MB": 1000 ** 2, "GB": 1000 ** 3,
    "KiB": 1024, "MiB": 1024 ** 2, "GiB": 1024 ** 3,
}

_DURATION_RE = re.compile(r"^(\d+(?:\.\d+)?)(ms|s|m|h|d)$")
_SIZE_RE = re.compile(r"^(\d+)(B|KiB|MiB|GiB|KB|MB|GB)$")
_INT_RE = re.compile(r"^-?\d+$")
_FLOAT_RE = re.compile(r"^-?\d+\.\d+$")


class ConfigError(Exception):
    """Raised for a malformed config line. `.line` is the 1-based line number."""

    def __init__(self, message, line):
        super().__init__(f"line {line}: {message}")
        self.line = line


def _decode_quoted(inner, line):
    out = []
    i = 0
    while i < len(inner):
        ch = inner[i]
        if ch == "\\" and i + 1 < len(inner) and inner[i + 1] in ('"', "\\"):
            out.append(inner[i + 1])
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _convert(value, line):
    if value.startswith('"'):
        if len(value) < 2 or not value.endswith('"'):
            raise ConfigError("unterminated quoted string", line)
        return _decode_quoted(value[1:-1], line)
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    match = _DURATION_RE.match(value)
    if match:
        return float(match.group(1)) * _DURATION_UNITS[match.group(2)]
    match = _SIZE_RE.match(value)
    if match:
        return int(match.group(1)) * _SIZE_UNITS[match.group(2)]
    if _INT_RE.match(value):
        return int(value)
    if _FLOAT_RE.match(value):
        return float(value)
    if re.search(r"\s", value):
        raise ConfigError("unquoted value cannot contain whitespace", line)
    return value


def parse(text):
    result = {}
    for lineno, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in raw:
            raise ConfigError("expected 'key = value'", lineno)
        key, _, value = raw.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            raise ConfigError("empty key", lineno)
        if not value:
            raise ConfigError("empty value", lineno)
        result[key] = _convert(value, lineno)
    return result
