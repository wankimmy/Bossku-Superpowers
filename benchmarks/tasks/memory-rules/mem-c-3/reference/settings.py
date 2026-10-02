"""Helpers for loading admin feature-flag settings.

Internal dicts stay snake_case. Anything serialized as JSON for the
frontend (an API response body) is converted to camelCase keys right at
the boundary, via ``_to_camel_case``.
"""


def load_settings(path):
    result = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            key, _, value = stripped.partition("=")
            result[key.strip()] = value.strip()
    return result


def _to_camel_case(key):
    parts = key.split("_")
    first, rest = parts[0], parts[1:]
    return first + "".join(part.capitalize() for part in rest)


def settings_api_response(settings):
    response = {_to_camel_case(key): value for key, value in settings.items()}
    response["source"] = "file"
    return response
