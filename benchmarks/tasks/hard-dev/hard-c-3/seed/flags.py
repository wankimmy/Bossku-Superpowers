"""A tiny feature-flag registry.

A flag is just a name mapped to True/False. There's no concept of a flag
that "doesn't exist" versus one that's off - asking about an unknown name
just reports False, same as an explicitly disabled one. The only thing
that distinguishes them is `all_flags()`, which only lists names that
have actually been touched at least once.
"""


class FeatureFlags:
    """A single, independent set of feature flags.

    Most code doesn't construct this directly - it uses the module-level
    `enable`/`disable`/`is_enabled`/`all_flags` functions below, which all
    operate on one shared instance for the whole process. Constructing
    your own `FeatureFlags()` is only useful when you need flags that are
    isolated from that shared state, e.g. in a test.
    """

    def __init__(self):
        self._flags = {}

    def enable(self, name):
        if not isinstance(name, str):
            raise TypeError("flag name must be a string")
        self._flags[name] = True

    def disable(self, name):
        if not isinstance(name, str):
            raise TypeError("flag name must be a string")
        self._flags[name] = False

    def is_enabled(self, name):
        if not isinstance(name, str):
            raise TypeError("flag name must be a string")
        return self._flags.get(name, False)

    def all_flags(self):
        """A snapshot dict of every flag that's ever been explicitly set,
        mapped to its current state. Safe to mutate - it's a copy."""
        return dict(self._flags)


_default = FeatureFlags()


def enable(name):
    _default.enable(name)


def disable(name):
    _default.disable(name)


def is_enabled(name):
    return _default.is_enabled(name)


def all_flags():
    return _default.all_flags()
