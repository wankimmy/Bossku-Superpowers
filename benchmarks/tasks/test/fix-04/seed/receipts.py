"""Formatting helpers for checkout receipts."""


def render_line(name, unit_price, qty, discount_percent, net):
    return f"{name}: {qty} x {unit_price:.2f} -{discount_percent:.0f}% = {net:.2f}"


def render_bulk_discount(bulk_off):
    return f"Bulk discount: -{bulk_off:.2f}"


def render_totals(tax, total):
    return [f"Tax: {tax:.2f}", f"Total: {total:.2f}"]
