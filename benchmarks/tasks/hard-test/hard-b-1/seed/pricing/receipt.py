"""Build a priced receipt for a cart, applying coupon codes."""

from decimal import Decimal

from .discounts import (
    SHIPPING_FEE,
    discount_amount,
    qualifies_for_free_shipping,
    select_codes,
)
from .money import round_half_up


def build_receipt(cart, codes):
    subtotal = cart.subtotal()
    percent_entry, fixed_entry, free_ship_entry = select_codes(codes)

    discount = discount_amount(subtotal, percent_entry, fixed_entry)
    discount = min(discount, subtotal)

    if not cart.lines:
        shipping = Decimal("0.00")
    elif free_ship_entry is not None or qualifies_for_free_shipping(subtotal):
        shipping = Decimal("0.00")
    else:
        shipping = SHIPPING_FEE

    total = round_half_up(subtotal - discount + shipping)

    applied = []
    if percent_entry is not None:
        applied.append(percent_entry[0].strip().upper())
    if fixed_entry is not None:
        applied.append(fixed_entry[0].strip().upper())
    if free_ship_entry is not None:
        applied.append(free_ship_entry[0].strip().upper())

    cart.applied_codes.extend(applied)

    return {
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "total": total,
        "applied_codes": list(cart.applied_codes),
    }
