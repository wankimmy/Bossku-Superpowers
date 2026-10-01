"""Sales report generator."""
from stats import Stats


def _valid_amounts(entries):
    return [(category, amount) for category, amount in entries if amount > 0]


def generate_report(entries):
    entries = _valid_amounts(entries)
    if not entries:
        raise ValueError("entries must not be empty")

    overall = Stats([amount for _, amount in entries]).as_dict()

    grouped = {}
    for category, amount in entries:
        grouped.setdefault(category, []).append(amount)

    by_category = {category: Stats(amounts).as_dict() for category, amounts in grouped.items()}

    return {"overall": overall, "by_category": by_category}


def top_category(entries):
    entries = _valid_amounts(entries)
    if not entries:
        raise ValueError("entries must not be empty")

    grouped = {}
    for category, amount in entries:
        grouped.setdefault(category, []).append(amount)

    best_category = None
    best_total = None
    for category in sorted(grouped):
        total = Stats(grouped[category]).total
        if best_total is None or total > best_total:
            best_total = total
            best_category = category

    return best_category
