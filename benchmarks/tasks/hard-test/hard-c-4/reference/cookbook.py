"""Backward-compatible shim.

The parsing and planning code that used to live here has moved to
`parsing.py` and `planning.py`; this module just re-exports it so existing
imports (`import cookbook`, `from cookbook import ...`) keep working.
"""

from parsing import Ingredient, UNIT_ALIASES, parse_ingredient
from planning import build_shopping_list, scale_recipe

__all__ = [
    "Ingredient",
    "UNIT_ALIASES",
    "parse_ingredient",
    "scale_recipe",
    "build_shopping_list",
]
