_NUMERALS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def to_roman(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an int")
    if n < 1 or n > 3999:
        raise ValueError("n must be between 1 and 3999")
    result = []
    remaining = n
    for value, numeral in _NUMERALS:
        if remaining <= 0:
            break
        count, remaining = divmod(remaining, value)
        if count:
            result.append(numeral * count)
    return "".join(result)


def from_roman(s):
    if not isinstance(s, str) or not s:
        raise ValueError("s must be a non-empty string")
    for ch in s:
        if ch not in _VALUES:
            raise ValueError(f"invalid roman numeral character: {ch!r}")
    total = 0
    i = 0
    while i < len(s):
        value = _VALUES[s[i]]
        if i + 1 < len(s) and _VALUES[s[i + 1]] >= value:
            total += _VALUES[s[i + 1]] - value
            i += 2
        else:
            total += value
            i += 1
    if total < 1 or total > 3999 or to_roman(total) != s:
        raise ValueError(f"not a canonical roman numeral: {s!r}")
    return total


def is_valid(s):
    try:
        from_roman(s)
    except ValueError:
        return False
    return True


def add(a, b):
    total = from_roman(a) + from_roman(b)
    return to_roman(total)
