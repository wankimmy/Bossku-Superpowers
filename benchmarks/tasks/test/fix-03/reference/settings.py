"""Default settings for generated reports."""

DEFAULTS = {
    "indent": 4,
    "prefix": ">> ",
    "show_header": True,
    "tags": ("general",),
}


def resolve_settings(overrides=None):
    overrides = overrides or {}
    result = {}
    for key, default in DEFAULTS.items():
        value = overrides.get(key)
        result[key] = default if value is None else value
    return result
