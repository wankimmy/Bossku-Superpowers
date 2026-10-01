"""Parse ingredient text into `Ingredient` values."""

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
