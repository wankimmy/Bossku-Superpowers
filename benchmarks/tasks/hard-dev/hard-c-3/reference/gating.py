"""Run code conditionally based on a feature flag."""

import flags


def run_if_enabled(name, func, *args, registry=None, **kwargs):
    """If the flag `name` is enabled in `registry` (default: the shared
    global registry, `flags.default_registry`), call `func(*args, **kwargs)`
    and return `(True, result)`. Otherwise return `(False, None)` without
    calling `func`."""
    reg = registry if registry is not None else flags.default_registry
    if reg.is_enabled(name):
        return True, func(*args, **kwargs)
    return False, None
