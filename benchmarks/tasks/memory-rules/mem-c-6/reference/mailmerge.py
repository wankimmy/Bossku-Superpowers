"""Helpers for rendering newsletter templates.

Placeholders are Mustache-style double curly braces, like ``{{name}}``.
A lone ``{`` or ``}`` in template text is left completely untouched.
"""

import re

PLACEHOLDER_PATTERN = re.compile(r"\{\{(\w+)\}\}")


def load_template(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def render_template(template_text, values):
    def _replace(match):
        name = match.group(1)
        if name in values:
            return str(values[name])
        return match.group(0)

    return PLACEHOLDER_PATTERN.sub(_replace, template_text)
