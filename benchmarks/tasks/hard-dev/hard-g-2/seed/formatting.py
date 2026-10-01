"""Shared percentage rounding/formatting helpers.

Every percentage in this package is a :class:`decimal.Decimal`; never a
``float``. Round with :func:`round_percent` (ROUND_HALF_UP -- round half
away from zero) and display with :func:`format_percent`; don't call
``.quantize()`` or format a percentage anywhere else, so every rounding
decision in this package goes through one place.
"""
from decimal import Decimal, ROUND_HALF_UP


def round_percent(value, places=1):
    """Round a ``Decimal`` percent to ``places`` decimal digits using ROUND_HALF_UP.

    ROUND_HALF_UP rounds an exact halfway value away from zero, e.g.
    ``Decimal("30.25")`` rounds (at 1 place) to ``Decimal("30.3")`` -- not
    the ``Decimal("30.2")`` Python's default ``Decimal`` rounding
    (ROUND_HALF_EVEN) would give.
    """
    quantum = Decimal(1).scaleb(-places)
    return value.quantize(quantum, rounding=ROUND_HALF_UP)


def format_percent(value):
    """Format a ``Decimal`` percent as a string like ``"87.5%"`` (always 1dp)."""
    return f"{round_percent(value, 1):.1f}%"
