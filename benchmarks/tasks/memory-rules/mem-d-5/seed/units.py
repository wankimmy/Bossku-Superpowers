"""Simple unit conversion helpers."""

UNIT_FACTORS = {
    "m": 1.0,
    "cm": 0.01,
    "km": 1000.0,
    "ft": 0.3048,
    "mi": 1609.34,
}


def convert(value, from_unit, to_unit):
    """Convert `value` from `from_unit` to `to_unit` (length units, for now)."""
    return value * UNIT_FACTORS[from_unit] / UNIT_FACTORS[to_unit]
