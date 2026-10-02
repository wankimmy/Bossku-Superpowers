"""Helpers for scaling and converting recipe measurements.

Any function here that can fail on bad input returns a ``(result, error)``
tuple instead of raising: ``error`` is ``None`` on success, ``result`` is
``None`` on failure.
"""

UNITS_TO_ML = {
    "cup": 240.0,
    "tbsp": 15.0,
    "tsp": 5.0,
    "ml": 1.0,
}


def scale_recipe(ingredients, factor):
    return [(name, amount * factor) for name, amount in ingredients]


def convert_unit(amount, from_unit, to_unit):
    if from_unit not in UNITS_TO_ML:
        return None, f"unknown unit: {from_unit!r}"
    if to_unit not in UNITS_TO_ML:
        return None, f"unknown unit: {to_unit!r}"
    milliliters = amount * UNITS_TO_ML[from_unit]
    return milliliters / UNITS_TO_ML[to_unit], None


def total_volume_ml(ingredients_with_units):
    total = 0.0
    for name, amount, unit in ingredients_with_units:
        milliliters, error = convert_unit(amount, unit, "ml")
        if error is not None:
            return None, f"{name}: {error}"
        total += milliliters
    return total, None
