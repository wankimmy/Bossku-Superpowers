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
        if key in overrides:
            result[key] = overrides[key] or default
        else:
            result[key] = default
    return result
