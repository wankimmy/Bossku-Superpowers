"""Calculator helpers."""


def _ok(data):
    return {"ok": True, "data": data, "error": None}


def _fail(message):
    return {"ok": False, "data": None, "error": message}


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def add(a, b):
    if not (_is_number(a) and _is_number(b)):
        return _fail("both arguments must be numbers")
    return _ok(a + b)


def multiply(a, b):
    if not (_is_number(a) and _is_number(b)):
        return _fail("both arguments must be numbers")
    return _ok(a * b)


def divide(a, b):
    if not (_is_number(a) and _is_number(b)):
        return _fail("both arguments must be numbers")
    if b == 0:
        return _fail("division by zero")
    return _ok(a / b)


def parse_number(text):
    try:
        value = float(text)
    except (TypeError, ValueError):
        return _fail("not a number: %r" % (text,))
    if value != value or value in (float("inf"), float("-inf")):
        return _fail("not a finite number")
    return _ok(int(value) if value == int(value) and "." not in str(text) else value)
