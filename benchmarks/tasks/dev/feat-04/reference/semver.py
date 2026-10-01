"""Parse and compare MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD] version strings."""
import re
from functools import total_ordering

_IDENT_RE = re.compile(r"^[A-Za-z0-9-]+$")
_CORE_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([^+]+))?(?:\+(.+))?$")


@total_ordering
class Version:
    def __init__(self, major, minor, patch, prerelease, build):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.build = build

    def _eq_key(self):
        return (self.major, self.minor, self.patch, self.prerelease)

    def _sort_key(self):
        pre_key = tuple((0, part) if isinstance(part, int) else (1, part) for part in self.prerelease)
        return (self.major, self.minor, self.patch, 0 if self.prerelease else 1, pre_key)

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._eq_key() == other._eq_key()

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._sort_key() < other._sort_key()

    def __hash__(self):
        return hash(self._eq_key())

    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch}, {self.prerelease!r}, {self.build!r})"


def _parse_identifier(text):
    if not _IDENT_RE.match(text):
        raise ValueError(f"invalid identifier {text!r}")
    if text.isdigit() and len(text) > 1 and text[0] == "0":
        raise ValueError(f"numeric identifier has a leading zero: {text!r}")
    return int(text) if text.isdigit() else text


def parse(s):
    match = _CORE_RE.match(s)
    if not match:
        raise ValueError(f"not a valid version string: {s!r}")
    major, minor, patch, prerelease_raw, build_raw = match.groups()

    prerelease = ()
    if prerelease_raw is not None:
        prerelease = tuple(_parse_identifier(part) for part in prerelease_raw.split("."))

    build = ""
    if build_raw is not None:
        for part in build_raw.split("."):
            if not _IDENT_RE.match(part):
                raise ValueError(f"invalid build identifier {part!r}")
        build = build_raw

    return Version(int(major), int(minor), int(patch), prerelease, build)


def sort_versions(strings):
    parsed = [(s, parse(s)) for s in strings]
    parsed.sort(key=lambda pair: pair[1]._sort_key())
    return [s for s, _ in parsed]
