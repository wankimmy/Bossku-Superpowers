"""Shared invoice splitting for the roommates' expense tool."""

from decimal import Decimal, ROUND_HALF_EVEN

CENT = Decimal("0.01")


def round_cents(amount):
    """Round a Decimal amount to the nearest cent, ties to even."""
    return amount.quantize(CENT, rounding=ROUND_HALF_EVEN)


class Invoice:
    def __init__(self):
        self._items = []  # list of (description, unit_price, quantity)

    def add_line_item(self, description, unit_price, quantity):
        self._items.append((description, unit_price, quantity))

    def total(self):
        result = Decimal("0")
        for _description, unit_price, quantity in self._items:
            result += unit_price * quantity
        return result


def split_evenly(invoice, n):
    """Split invoice.total() into n Decimal shares that sum exactly to it,
    handing any leftover cent(s) to the first few shares."""
    if n <= 0:
        raise ValueError("n must be positive")
    total = round_cents(invoice.total())
    whole_cents, extra_units = divmod(total / CENT, n)
    shares = [whole_cents * CENT] * n
    for i in range(int(extra_units)):
        shares[i] = shares[i] + CENT
    return shares
