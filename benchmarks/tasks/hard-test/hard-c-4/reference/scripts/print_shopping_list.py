"""CLI: print the combined shopping list for one or more recipe files.

Each recipe file has one ingredient per line, e.g. "2 cups flour".
"""

import sys

from cookbook import build_shopping_list, parse_ingredient


def _load_recipe(path):
    with open(path, encoding="utf-8") as handle:
        lines = [line.strip() for line in handle if line.strip()]
    return [parse_ingredient(line) for line in lines]


def main(argv):
    if not argv:
        print("usage: print_shopping_list.py <recipe_file> [recipe_file ...]")
        return
    recipes = [_load_recipe(path) for path in argv]
    for ing in build_shopping_list(recipes):
        print(f"{ing.quantity:g} {ing.unit} {ing.name}")


if __name__ == "__main__":
    main(sys.argv[1:])
