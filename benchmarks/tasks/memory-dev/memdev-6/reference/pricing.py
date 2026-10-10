"""Pricing helpers."""


def _percent_of(cents, percent):
    """cents * percent / 100, rounded half up, in integers only."""
    return (cents * percent * 2 + 100) // 200


def apply_discount(cents, percent):
    if cents < 0 or not 0 <= percent <= 100:
        raise ValueError("bad price or percent")
    return cents - _percent_of(cents, percent)


def add_tax(cents, rate_percent):
    if cents < 0 or rate_percent < 0:
        raise ValueError("bad price or rate")
    return cents + _percent_of(cents, rate_percent)
