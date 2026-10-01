"""Sales report generator."""


def _valid_amounts(entries):
    return [(category, amount) for category, amount in entries if amount > 0]


def generate_report(entries):
    entries = _valid_amounts(entries)
    if not entries:
        raise ValueError("entries must not be empty")

    # --- overall stats ---
    total_count = len(entries)
    total_sum = 0.0
    for _, amount in entries:
        total_sum += amount
    total_average = total_sum / total_count
    total_min = entries[0][1]
    for _, amount in entries:
        if amount < total_min:
            total_min = amount
    total_max = entries[0][1]
    for _, amount in entries:
        if amount > total_max:
            total_max = amount

    overall = {
        "count": total_count,
        "total": round(total_sum, 2),
        "average": round(total_average, 2),
        "min": round(total_min, 2),
        "max": round(total_max, 2),
    }

    # --- group by category ---
    grouped = {}
    for category, amount in entries:
        grouped.setdefault(category, []).append(amount)

    by_category = {}
    for category, amounts in grouped.items():
        # --- the same stats logic, written out again ---
        cat_count = len(amounts)
        cat_sum = 0.0
        for amount in amounts:
            cat_sum += amount
        cat_average = cat_sum / cat_count
        cat_min = amounts[0]
        for amount in amounts:
            if amount < cat_min:
                cat_min = amount
        cat_max = amounts[0]
        for amount in amounts:
            if amount > cat_max:
                cat_max = amount
        by_category[category] = {
            "count": cat_count,
            "total": round(cat_sum, 2),
            "average": round(cat_average, 2),
            "min": round(cat_min, 2),
            "max": round(cat_max, 2),
        }

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
        # --- and again, just to get a total ---
        cat_sum = 0.0
        for amount in grouped[category]:
            cat_sum += amount
        if best_total is None or cat_sum > best_total:
            best_total = cat_sum
            best_category = category

    return best_category
