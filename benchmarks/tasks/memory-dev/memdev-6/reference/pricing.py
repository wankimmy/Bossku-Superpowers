"""Pricing helpers."""


def to_cents(text):
    whole, dot, frac = text.partition(".")
    if not whole.isascii() or not whole.isdigit() or (dot and (not frac.isascii() or not frac.isdigit())) or len(frac) > 2:
        raise ValueError("bad price")
    return int(whole) * 100 + int((frac + "00")[:2])


def format_cents(cents):
    return str(cents // 100) + "." + str(cents % 100).zfill(2)


def _div_half_up(numerator, denominator):
    return (numerator * 2 + denominator) // (denominator * 2)


def apply_discount(cents, percent):
    if cents < 0 or not 0 <= percent <= 100:
        raise ValueError("bad price or percent")
    return _div_half_up(cents * (100 - percent), 100)


def add_tax(cents, rate_percent):
    if cents < 0 or rate_percent < 0:
        raise ValueError("bad price or rate")
    return _div_half_up(cents * (100 + rate_percent), 100)
