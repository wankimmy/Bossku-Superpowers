"""Run code conditionally based on a feature flag.

This is the pattern most call sites should use instead of sprinkling
`if flags.is_enabled(...):` checks everywhere - it keeps the "don't call
the function at all when the flag is off" behavior in one place.
"""

from flags import is_enabled


def run_if_enabled(name, func, *args, **kwargs):
    """If the flag `name` is enabled, call `func(*args, **kwargs)` and
    return `(True, result)`. Otherwise return `(False, None)` without
    calling `func`."""
    if is_enabled(name):
        return True, func(*args, **kwargs)
    return False, None
