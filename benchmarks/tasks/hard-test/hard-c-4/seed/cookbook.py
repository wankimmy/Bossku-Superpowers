"""Parse ingredient lines, scale recipes, and build shopping lists.

This module does three different jobs and has grown too big.
"""

from dataclasses import dataclass

UNIT_ALIASES = {
    "tsp": "tsp", "teaspoon": "tsp", "teaspoons": "tsp",
    "tbsp": "tbsp", "tablespoon": "tbsp", "tablespoons": "tbsp",
    "cup": "cup", "cups": "cup",
    "g": "g", "gram": "g", "grams": "g",
    "kg": "kg", "kilogram": "kg", "kilograms": "kg",
}


@dataclass(frozen=True)
class Ingredient:
    quantity: float
    unit: str
    name: str


def _canonical_unit(token):
    return UNIT_ALIASES.get(token.lower())


def parse_ingredient(text):
    """Parse a line like "2 cups flour" or "3 eggs" into an `Ingredient`.

    The first whitespace-separated token is the quantity (a positive
    number). If the second token is a recognized unit (case-insensitively,
    see `UNIT_ALIASES`), it becomes the canonical unit and every token after
    it is the name. Otherwise the unit is "count" and every token from the
    second one onward is the name.
    """
    tokens = text.split()
    if not tokens:
        raise ValueError("missing ingredient name")
    try:
        quantity = float(tokens[0])
    except ValueError:
        raise ValueError(f"invalid quantity: {tokens[0]}")
    if quantity <= 0:
        raise ValueError("quantity must be positive")

    rest = tokens[1:]
    unit = "count"
    if rest:
        canonical = _canonical_unit(rest[0])
        if canonical is not None:
            unit = canonical
            rest = rest[1:]
    name = " ".join(rest).strip()
    if not name:
        raise ValueError("missing ingredient name")
    return Ingredient(quantity, unit, name)


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
    result = [
        Ingredient(totals[key], key[1], display_names[key])
        for key in sorted(totals.keys())
    ]
    return result
