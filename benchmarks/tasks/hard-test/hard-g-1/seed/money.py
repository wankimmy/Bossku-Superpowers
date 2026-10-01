"""Shared money helpers.

Every money value in this package is a :class:`decimal.Decimal`; never a
``float``. Round with :func:`round_money` (ROUND_HALF_UP -- round half
away from zero) and display with :func:`format_money`; don't call
``.quantize()`` or do ad-hoc string formatting on money anywhere else, so
that every rounding decision in this package goes through one place.
"""
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def round_money(value):
    """Round a ``Decimal`` to 2 decimal places using ROUND_HALF_UP.

    ROUND_HALF_UP rounds an exact halfway value away from zero, e.g.
    ``Decimal("20.125")`` rounds to ``Decimal("20.13")`` -- this is *not*
    the same as Python's default ``Decimal`` rounding (ROUND_HALF_EVEN),
    which would round that same value to ``Decimal("20.12")``.
    """
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def format_money(value):
    """Format a ``Decimal`` as a string like ``"$12.34"`` (always 2dp, with a ``$``)."""
    return f"${round_money(value):.2f}"
