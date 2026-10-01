"""A tiny feature-flag registry."""


class FeatureFlags:
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
        return dict(self._flags)


default_registry = FeatureFlags()


def enable(name):
    default_registry.enable(name)


def disable(name):
    default_registry.disable(name)


def is_enabled(name):
    return default_registry.is_enabled(name)


def all_flags():
    return default_registry.all_flags()
