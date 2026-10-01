"""JSON persistence for the expense list.

The on-disk file is a single JSON object: ``{"next_id": <int>, "expenses":
[...]}``. ``next_id`` is tracked explicitly (rather than recomputed as
``max(existing ids) + 1``) specifically so that deleting the
highest-numbered expense does not free its id for reuse - ids are
assigned once, in increasing order, and never recycled.
"""
import json

from errors import StorageError


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
    except FileNotFoundError:
        return {"next_id": 1, "expenses": []}
    if not raw:
        return {"next_id": 1, "expenses": []}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise StorageError(f"could not parse {path}: {exc}") from exc
    data.setdefault("next_id", 1)
    data.setdefault("expenses", [])
    return data


def save(path, next_id, expenses):
    data = {"next_id": next_id, "expenses": expenses}
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    except OSError as exc:
        raise StorageError(f"could not write {path}: {exc}") from exc
