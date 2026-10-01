"""Coupon code catalog and stacking rules."""

from decimal import Decimal

from .money import round_half_up

SHIPPING_FEE = Decimal("6.99")
FREE_SHIPPING_THRESHOLD = Decimal("50.00")

CATALOG = {
    "SAVE10": {"type": "percent", "value": Decimal("0.10")},
    "WELCOME10": {"type": "percent", "value": Decimal("0.10")},
    "SAVE15": {"type": "percent", "value": Decimal("0.15")},
    "SAVE20": {"type": "percent", "value": Decimal("0.20")},
    "5OFF": {"type": "fixed", "value": Decimal("5.00")},
    "10OFF": {"type": "fixed", "value": Decimal("10.00")},
    "FREESHIP": {"type": "free_shipping", "value": Decimal("0")},
}


def _lookup(code):
    return CATALOG.get(code)


def select_codes(codes):
    """Pick which entered codes actually apply, per the stacking rules.

    Returns (percent_entry, fixed_entry, free_ship_entry) where each is
    either None or (code, catalog_entry).
    """
    percent_candidates = []
    fixed_candidates = []
    free_ship = None

    for raw in codes:
        entry = _lookup(raw)
        if entry is None:
            continue
        if entry["type"] == "percent":
            percent_candidates.append((raw, entry))
        elif entry["type"] == "fixed":
            fixed_candidates.append((raw, entry))
        elif entry["type"] == "free_shipping":
            free_ship = (raw, entry)

    best_percent = percent_candidates[0] if percent_candidates else None
    best_fixed = fixed_candidates[0] if fixed_candidates else None
    return best_percent, best_fixed, free_ship


def discount_amount(subtotal, percent_entry, fixed_entry):
    """Compute total discount in dollars for the chosen codes."""
    remaining = subtotal
    discount = Decimal("0")

    if percent_entry is not None:
        _, entry = percent_entry
        pct_amount = (subtotal * entry["value"]).quantize(Decimal("0.01"))
        discount += pct_amount
        remaining -= pct_amount

    if fixed_entry is not None:
        _, entry = fixed_entry
        fixed_amount = min(entry["value"], remaining)
        discount += fixed_amount

    return round_half_up(discount)


def qualifies_for_free_shipping(subtotal):
    return subtotal > FREE_SHIPPING_THRESHOLD
