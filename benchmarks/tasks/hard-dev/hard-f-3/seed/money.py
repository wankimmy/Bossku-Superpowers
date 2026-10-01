"""This project's one, shared rule for turning a number into money.

``round_money(x)`` rounds to 2 decimal places using *round-half-up*
(0.005 rounds to 0.01, not down), via ``decimal.Decimal`` - **not**
Python's built-in ``round()``, which rounds half-to-even ("banker's
rounding") on the float's actual binary value and silently disagrees
with round-half-up on plenty of ordinary-looking amounts. For example,
``round(2.125, 2) == 2.12`` but ``round_money(2.125) == 2.13``.

Every amount anywhere in this project - when an expense is created, and
whenever amounts are summed for a total - is rounded with this one
function, so a figure never shows one rounding behavior in one place and
a different one somewhere else.
"""
from decimal import Decimal, ROUND_HALF_UP

_CENTS = Decimal("0.01")


def round_money(amount):
    return float(Decimal(str(amount)).quantize(_CENTS, rounding=ROUND_HALF_UP))
