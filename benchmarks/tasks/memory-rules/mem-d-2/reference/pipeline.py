"""Helpers for turning simple CSV text into JSON-ready rows."""

import importlib
import json

from transforms import TRANSFORM_ORDER

DELIMITER = ","


def _apply_transforms(row):
    for name in TRANSFORM_ORDER:
        module = importlib.import_module(f"transforms.{name}")
        row = module.apply(row)
    return row


def read_csv_rows(text):
    """Parse CSV `text` (header row first) into a list of row dicts, cleaned."""
    lines = [line for line in text.splitlines() if line != ""]
    if not lines:
        return []
    header = lines[0].split(DELIMITER)
    rows = []
    for line in lines[1:]:
        values = line.split(DELIMITER)
        row = dict(zip(header, values))
        rows.append(_apply_transforms(row))
    return rows


def rows_to_json(rows):
    """Return a compact JSON string for a list of row dicts."""
    return json.dumps(rows)
