"""httpheader.py - structured HTTP header value parsing.

See README.md for the full specification.
"""

import re

_QVALUE_ZERO = re.compile(r"0(\.[0-9]{0,3})?$")
_QVALUE_ONE = re.compile(r"1(\.0{0,3})?$")


class HeaderParseError(ValueError):
    """Raised when a header value is malformed."""


def _split_top_level(s, sep):
    """Split s on sep, except inside a double-quoted span. Quoted spans
    recognize only \\" and \\\\ as escapes; any other backslash escape, or
    an unterminated quote, is an error. Chunks are returned raw (quotes
    and escapes untouched) -- only the split points are determined here.
    """
    chunks = []
    current = []
    in_quotes = False
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if in_quotes:
            if ch == "\\":
                if i + 1 >= n:
                    raise HeaderParseError("trailing backslash inside quoted string")
                nxt = s[i + 1]
                if nxt not in ('"', "\\"):
                    raise HeaderParseError(f"invalid escape \\{nxt} inside quoted string")
                current.append(ch)
                current.append(nxt)
                i += 2
                continue
            if ch == '"':
                in_quotes = False
                current.append(ch)
                i += 1
                continue
            current.append(ch)
            i += 1
            continue
        if ch == '"':
            in_quotes = True
            current.append(ch)
            i += 1
            continue
        if ch == sep:
            chunks.append("".join(current))
            current = []
            i += 1
            continue
        current.append(ch)
        i += 1
    if in_quotes:
        raise HeaderParseError("unterminated quoted string")
    chunks.append("".join(current))
    return chunks


def split_list(value):
    if not isinstance(value, str):
        raise TypeError("value must be a str")
    chunks = _split_top_level(value, ",")
    result = []
    for c in chunks:
        trimmed = c.strip(" \t")
        if trimmed:
            result.append(trimmed)
    return result


def _validate_bare_token(tok, what):
    if not tok:
        raise HeaderParseError(f"{what} must not be empty")
    for c in tok:
        if c in " \t\";=":
            raise HeaderParseError(f"{what} contains an invalid character: {tok!r}")


def _parse_quoted(s):
    # s starts with '"'; returns the unescaped value, and validates that
    # nothing but whitespace follows the closing quote.
    out = []
    i = 1
    n = len(s)
    closed = False
    while i < n:
        ch = s[i]
        if ch == "\\":
            if i + 1 >= n:
                raise HeaderParseError("trailing backslash in quoted value")
            nxt = s[i + 1]
            if nxt not in ('"', "\\"):
                raise HeaderParseError(f"invalid escape \\{nxt} in quoted value")
            out.append(nxt)
            i += 2
            continue
        if ch == '"':
            closed = True
            i += 1
            break
        out.append(ch)
        i += 1
    if not closed:
        raise HeaderParseError("unterminated quoted value")
    trailing = s[i:]
    if trailing.strip(" \t") != "":
        raise HeaderParseError("trailing characters after quoted value")
    return "".join(out)


def parse_params(value):
    if not isinstance(value, str):
        raise TypeError("value must be a str")
    s = value.strip(" \t")
    if not s:
        raise HeaderParseError("empty header value")
    chunks = _split_top_level(s, ";")
    main = chunks[0].strip(" \t")
    _validate_bare_token(main, "main value")
    params = []
    for chunk in chunks[1:]:
        c = chunk.strip(" \t")
        if not c:
            raise HeaderParseError("empty parameter")
        if "=" not in c:
            raise HeaderParseError(f"parameter without '=': {c!r}")
        key_raw, val_raw = c.split("=", 1)
        key = key_raw.strip(" \t")
        _validate_bare_token(key, "parameter name")
        key = key.lower()
        val_stripped = val_raw.strip(" \t")
        if val_stripped.startswith('"'):
            val = _parse_quoted(val_stripped)
        else:
            _validate_bare_token(val_stripped, "parameter value")
            val = val_stripped
        params.append((key, val))
    return main, params


def _validate_qvalue(s):
    if _QVALUE_ZERO.fullmatch(s) or _QVALUE_ONE.fullmatch(s):
        return float(s)
    raise HeaderParseError(f"invalid q value: {s!r}")


def parse_quality_list(value):
    if not isinstance(value, str):
        raise TypeError("value must be a str")
    items = split_list(value)
    staged = []
    for idx, item in enumerate(items):
        main, params = parse_params(item)
        q = 1.0
        for key, val in params:
            if key == "q":
                q = _validate_qvalue(val)
        staged.append((main, q, idx))
    staged.sort(key=lambda t: (-t[1], t[2]))
    return [(m, q) for (m, q, _idx) in staged]
