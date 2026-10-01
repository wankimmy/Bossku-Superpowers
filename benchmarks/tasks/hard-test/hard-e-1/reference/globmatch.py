"""globmatch.py - path pattern matching with ** (globstar) semantics.

See README.md for the full specification.
"""

import re


class GlobPatternError(ValueError):
    """Raised when a glob pattern is malformed."""


_GLOBSTAR = object()  # sentinel token for a "**" segment


def _translate_class_body(body):
    result = []
    n = len(body)
    i = 0
    while i < n:
        c = body[i]
        if c == "-" and 0 < i < n - 1:
            result.append("-")
        elif c == "-":
            result.append("\\-")
        elif c in "\\^]":
            result.append("\\" + c)
        else:
            result.append(c)
        i += 1
    return "".join(result)


def _compile_segment(segment):
    if segment == "":
        raise GlobPatternError("pattern segment must not be empty")
    out = ["^"]
    i = 0
    n = len(segment)
    while i < n:
        ch = segment[i]
        if ch == "\\":
            if i + 1 >= n:
                raise GlobPatternError("trailing backslash in pattern segment")
            out.append(re.escape(segment[i + 1]))
            i += 2
        elif ch == "*":
            out.append(".*")
            i += 1
        elif ch == "?":
            out.append(".")
            i += 1
        elif ch == "[":
            j = i + 1
            negate = False
            if j < n and segment[j] in "!^":
                negate = True
                j += 1
            body_chars = []
            first = True
            while True:
                if j >= n:
                    raise GlobPatternError("unterminated character class in pattern")
                c = segment[j]
                if c == "]" and not first:
                    break
                body_chars.append(c)
                first = False
                j += 1
            class_body = "".join(body_chars)
            if class_body == "":
                raise GlobPatternError("empty character class in pattern")
            translated = _translate_class_body(class_body)
            out.append("[" + ("^" if negate else "") + translated + "]")
            i = j + 1
        else:
            out.append(re.escape(ch))
            i += 1
    out.append("$")
    try:
        return re.compile("".join(out), re.DOTALL)
    except re.error as exc:
        raise GlobPatternError(f"invalid character class: {exc}")


def _compile_pattern(pattern):
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a str")
    if pattern == "":
        raise GlobPatternError("pattern must not be empty")
    raw_segments = pattern.split("/")
    if any(s == "" for s in raw_segments):
        raise GlobPatternError(
            "pattern must not contain an empty segment (leading, trailing, or doubled '/')"
        )
    tokens = []
    for seg in raw_segments:
        if seg == "**":
            tokens.append(_GLOBSTAR)
        else:
            tokens.append(_compile_segment(seg))
    return tokens


def _segments_match(tokens, path_segments):
    n = len(tokens)
    m = len(path_segments)
    memo = {}

    def rec(i, j):
        key = (i, j)
        if key in memo:
            return memo[key]
        if i == n:
            result = j == m
        elif tokens[i] is _GLOBSTAR:
            result = False
            k = j
            while True:
                if rec(i + 1, k):
                    result = True
                    break
                if k >= m:
                    break
                k += 1
        else:
            if j < m and tokens[i].match(path_segments[j]):
                result = rec(i + 1, j + 1)
            else:
                result = False
        memo[key] = result
        return result

    return rec(0, 0)


def match(pattern, path):
    tokens = _compile_pattern(pattern)
    if not isinstance(path, str):
        raise TypeError("path must be a str")
    path_segments = path.split("/")
    return _segments_match(tokens, path_segments)


def filter_paths(pattern, paths):
    tokens = _compile_pattern(pattern)
    if not isinstance(paths, (list, tuple)):
        raise TypeError("paths must be a list or tuple")
    result = []
    for p in paths:
        if not isinstance(p, str):
            raise TypeError("each path must be a str")
        if _segments_match(tokens, p.split("/")):
            result.append(p)
    return result
