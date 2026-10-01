"""Money helpers: all amounts are Decimal, rounded to the cent."""

from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def round_half_up(value):
    """Round a Decimal to the nearest cent, ties rounding away from zero."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)
