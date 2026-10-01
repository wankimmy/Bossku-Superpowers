"""Small reporting tool built on top of legacy_format."""

import legacy_format


def _clean_line(line):
    parts = [p.strip() for p in line.split("|")]
    if len(parts) == 4 and parts[-1] == "":
        parts = parts[:3]
    return "|".join(parts)


def _parsed_rows(lines):
    rows = []
    for line in lines:
        cleaned = _clean_line(line)
        try:
            rows.append(legacy_format.parse_line(cleaned))
        except ValueError:
            continue
    return rows


def summarize(lines):
    totals = {}
    for row in _parsed_rows(lines):
        totals[row["name"]] = totals.get(row["name"], 0) + row["qty"]
    return totals


def top_sellers(lines, n):
    totals = summarize(lines)
    ordered = sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))
    return [name for name, _ in ordered[:n]]
