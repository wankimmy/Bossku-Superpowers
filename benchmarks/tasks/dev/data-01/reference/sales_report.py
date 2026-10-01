"""Turn a raw sales export into a per-category summary report."""
import csv

_CATEGORY_WIDTH = 20
_COUNT_WIDTH = 8
_TOTAL_WIDTH = 12


def _format_row(label, count, total):
    return f"{label:<{_CATEGORY_WIDTH}}{count:>{_COUNT_WIDTH}}{total:>{_TOTAL_WIDTH}.2f}"


def generate_report(csv_text):
    lines = [line for line in csv_text.splitlines() if line.strip()]
    rows = list(csv.reader(lines))
    if not rows:
        raise ValueError("missing header row")
    header, data_rows = rows[0], rows[1:]
    if header != ["order_id", "category", "amount"]:
        raise ValueError("unexpected header: " + ",".join(header))

    by_order = {}
    for order_id, category, amount in data_rows:
        by_order[order_id] = (category, float(amount))

    totals = {}
    counts = {}
    for category, amount in by_order.values():
        totals[category] = totals.get(category, 0.0) + amount
        counts[category] = counts.get(category, 0) + 1

    out = [f"{'CATEGORY':<{_CATEGORY_WIDTH}}{'COUNT':>{_COUNT_WIDTH}}{'TOTAL':>{_TOTAL_WIDTH}}"]
    for category in sorted(totals):
        out.append(_format_row(category, counts[category], totals[category]))
    out.append(_format_row("TOTAL", len(by_order), sum(totals.values())))
    return "\n".join(out)
