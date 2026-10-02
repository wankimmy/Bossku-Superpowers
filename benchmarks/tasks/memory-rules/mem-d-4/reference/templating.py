"""Tiny placeholder-substitution template renderer, with filters."""

import re

PLACEHOLDER_PATTERN = r"\{\{\s*(.+?)\s*\}\}"

_MISSING = object()


def _apply_filter(value, filter_expr):
    if ":" in filter_expr:
        name, arg = filter_expr.split(":", 1)
    else:
        name, arg = filter_expr, None
    if name == "upper":
        return str(value).upper()
    if name == "lower":
        return str(value).lower()
    if name == "default":
        if value is _MISSING or value == "":
            return arg
        return value
    raise ValueError(f"unknown filter: {name}")


def render(template, context):
    def replace(match):
        expr = match.group(1)
        parts = [p.strip() for p in expr.split("|")]
        key = parts[0]
        value = context.get(key, _MISSING)
        for filter_expr in parts[1:]:
            value = _apply_filter(value, filter_expr)
        if value is _MISSING:
            raise KeyError(key)
        return str(value)

    return re.sub(PLACEHOLDER_PATTERN, replace, template)


def render_many(template, contexts):
    """Render `template` once per context in `contexts`, stamping `_index`."""
    rendered = []
    for index, context in enumerate(contexts):
        stamped = dict(context)
        stamped["_index"] = index
        rendered.append(render(template, stamped))
    return rendered
