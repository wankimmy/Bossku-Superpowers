# cookbook

Parses recipe ingredient lines, scales recipes up or down, and builds
combined shopping lists across one or more recipes.

Modules:
- `cookbook.py` — `Ingredient`, `UNIT_ALIASES`, `parse_ingredient(text)`,
  `scale_recipe(ingredients, factor)`, `build_shopping_list(recipes)`.
- `menu.py` — plans a week of meals on top of `cookbook`: parses each
  recipe's ingredient lines, scales every recipe by the same serving
  factor, and combines them all into one shopping list.
- `scripts/print_shopping_list.py` — CLI that prints a shopping list for
  one or more recipe files, each a plain text file with one ingredient
  per line.

Ingredient lines look like `"2 cups flour"` or `"3 eggs"` (quantity, then
an optional unit, then the ingredient name). Units are matched against
`UNIT_ALIASES`, case-insensitively, so `"2 Cups flour"` and `"2 CUPS flour"`
parse the same way; anything not recognized as a unit is treated as part
of the name instead, so `"3 large eggs"` has no unit at all.

Example:

```python
from cookbook import parse_ingredient, scale_recipe, build_shopping_list

recipe = [parse_ingredient("2 cups flour"), parse_ingredient("1 cup flour")]
doubled = scale_recipe(recipe, 2)
result = build_shopping_list([doubled])
```

`result` is a one-item list containing 6 cups of flour (2 + 1, doubled).

Run tests: `python -m unittest discover -s tests`
