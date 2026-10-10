"""A tiny route registry."""
ROUTES = {}


def route(method, path):
    def decorator(fn):
        ROUTES[(method, path)] = fn
        return fn
    return decorator
