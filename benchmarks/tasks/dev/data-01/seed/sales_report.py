"""Turn a raw sales export into a per-category summary report."""


def generate_report(csv_text):
    lines = [line for line in csv_text.splitlines() if line.strip()]
    header, *data_rows = lines
    totals = {}
    counts = {}
    for line in data_rows:
        order_id, category, amount = line.split(",")
        totals[category] = totals.get(category, 0.0) + float(amount)
        counts[category] = counts.get(category, 0) + 1

    out = [f"{'CATEGORY':<20}{'COUNT':>8}{'TOTAL':>12}"]
    for category in sorted(totals):
        out.append(f"{category:<20}{counts[category]:>8}{totals[category]:>12.2f}")
    out.append(f"{'TOTAL':<20}{sum(counts.values()):>8}{sum(totals.values()):>12.2f}")
    return "\n".join(out)
