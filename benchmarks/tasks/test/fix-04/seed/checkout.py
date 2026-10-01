"""Checkout total calculation for the shop."""
from receipts import render_line, render_bulk_discount, render_totals


def checkout_summary(items, tax_rate, bulk_threshold=100.0, bulk_discount=0.1):
    subtotal = 0.0
    receipt_lines = []
    for name, unit_price, qty, discount_percent in items:
        line_total = unit_price * qty
        net = round(line_total * (1 - discount_percent / 100.0), 2)
        receipt_lines.append(render_line(name, unit_price, qty, discount_percent, net))
        subtotal = round(subtotal + net, 2)

    tax = round(subtotal * tax_rate, 2)

    if subtotal > bulk_threshold:
        bulk_off = round(subtotal * bulk_discount, 2)
        subtotal = round(subtotal - bulk_off, 2)
        receipt_lines.append(render_bulk_discount(bulk_off))

    total = round(subtotal + tax, 2)
    receipt_lines.extend(render_totals(tax, total))
    return total, receipt_lines
