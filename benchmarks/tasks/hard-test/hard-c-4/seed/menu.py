"""Weekly menu planning on top of the cookbook module."""

import cookbook


def plan_week(recipes, servings_factor=1.0):
    """`recipes` is a list of raw ingredient-line lists (one per recipe).
    Parses each, scales it by `servings_factor`, and returns the combined
    shopping list across all of them."""
    scaled_recipes = []
    for lines in recipes:
        parsed = [cookbook.parse_ingredient(line) for line in lines]
        scaled_recipes.append(cookbook.scale_recipe(parsed, servings_factor))
    return cookbook.build_shopping_list(scaled_recipes)
