"""Helpers for parsing simple structured log lines."""

LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")


def parse_line(line):
    """Parse a well-formed 'LEVEL TIMESTAMP MESSAGE' log line into a dict."""
    level, timestamp, message = line.split(" ", 2)
    return {"level": level, "timestamp": timestamp, "message": message}


def filter_by_level(records, level):
    """Return only the records whose level matches `level` exactly, in order."""
    return [record for record in records if record["level"] == level]


def _parse_line_safe(line):
    """Parse one possibly-malformed line.

    Returns (record, error): exactly one side is None, never both, never neither.
    """
    parts = line.split(" ", 2)
    if len(parts) < 3 or not parts[0] or not parts[1] or not parts[2]:
        return None, "missing field"
    level, timestamp, message = parts
    if level not in LEVELS:
        return None, "unknown level"
    return {"level": level, "timestamp": timestamp, "message": message}, None


def parse_lines_safely(lines):
    """Parse a batch of possibly-malformed lines without raising.

    Returns a list of (record, error) tuples, one per input line, in order.
    """
    return [_parse_line_safe(line) for line in lines]


def summarize(lines):
    """Tally how many lines in a batch parsed cleanly vs failed."""
    results = parse_lines_safely(lines)
    ok = sum(1 for record, error in results if error is None)
    failed = len(results) - ok
    return {"total": len(results), "ok": ok, "failed": failed}
