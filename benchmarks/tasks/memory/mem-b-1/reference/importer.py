"""Order row importer for the warehouse CSV export."""

from report import report


def import_rows(rows):
    """Split `rows` into (accepted, rejected) based on order_id/amount."""
    accepted = []
    rejected = []
    for row in rows:
        if row.get("order_id") is not None and row.get("amount") is not None:
            accepted.append(row)
        else:
            rejected.append(row)
    return accepted, rejected


def dedupe_rows(rows):
    """Split `rows` into (unique_rows, duplicate_rows) by order_id."""
    seen_ids = set()
    unique_rows = []
    duplicate_rows = []
    for row in rows:
        order_id = row.get("order_id")
        if order_id in seen_ids:
            duplicate_rows.append(row)
        else:
            seen_ids.add(order_id)
            unique_rows.append(row)
    return unique_rows, duplicate_rows


def summarize_import(all_rows):
    """Run import + dedupe over `all_rows` and report/return a summary."""
    accepted, rejected = import_rows(all_rows)
    unique_rows, duplicate_rows = dedupe_rows(accepted)
    summary = {
        "total": len(all_rows),
        "accepted": len(unique_rows),
        "duplicates": len(duplicate_rows),
        "rejected": len(rejected),
    }
    report("import_summary", **summary)
    return summary
