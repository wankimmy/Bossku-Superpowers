"""Simple unit conversion helpers."""

UNIT_FACTORS = {
    "m": 1.0,
    "cm": 0.01,
    "km": 1000.0,
    "ft": 0.3048,
    "mi": 1609.34,
}

WEIGHT_FACTORS = {
    "kg": 1.0,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}

_TABLES = (UNIT_FACTORS, WEIGHT_FACTORS)


def _factor_for(unit):
    for table in _TABLES:
        if unit in table:
            return table[unit]
    raise KeyError(unit)


def convert(value, from_unit, to_unit):
    """Convert `value` from `from_unit` to `to_unit` within the same category."""
    return value * _factor_for(from_unit) / _factor_for(to_unit)


def convert_many(values, from_unit, to_unit):
    """Convert a list of values at once, in order."""
    return [convert(value, from_unit, to_unit) for value in values]


def round_result(value, ndigits=2):
    """Round a converted value for display."""
    return round(value, ndigits)
