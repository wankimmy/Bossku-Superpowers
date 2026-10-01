"""Scale recipes and build combined shopping lists."""

from parsing import Ingredient


def scale_recipe(ingredients, factor):
    """Return a new list with every ingredient's quantity multiplied by
    `factor`. Does not modify `ingredients` or its contents."""
    if factor <= 0:
        raise ValueError("scale factor must be positive")
    return [Ingredient(ing.quantity * factor, ing.unit, ing.name) for ing in ingredients]


def build_shopping_list(recipes):
    """Combine ingredients from several recipes (a list of ingredient
    lists) into one shopping list.

    Ingredients are combined when their name (case-insensitive) and unit
    both match exactly - quantities are summed, never converted between
    units. The name used in the output is the casing of the first
    occurrence seen. The result is sorted by (name.lower(), unit).
    """
    totals = {}
    display_names = {}
    for recipe in recipes:
        for ing in recipe:
            key = (ing.name.lower(), ing.unit)
            totals[key] = totals.get(key, 0.0) + ing.quantity
            display_names.setdefault(key, ing.name)
    return [
        Ingredient(totals[key], key[1], display_names[key])
        for key in sorted(totals.keys())
    ]
