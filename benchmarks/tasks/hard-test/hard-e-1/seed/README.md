# globmatch

A standalone path-pattern matcher for our build tool's file-selection rules
(which files to include in a bundle, which to exclude from a watch list,
etc.). It looks like a normal shell glob but there is no filesystem access
anywhere in this module -- `match`/`filter_paths` only ever compare two
strings. Implement it in a new `globmatch.py` at the project root, following
this spec exactly.

## API

- `match(pattern, path)` -> `bool`. Raises `TypeError` if `pattern` or `path`
  is not a `str`. Raises `GlobPatternError` (defined in this module, a
  `ValueError` subclass) if `pattern` is malformed.
- `filter_paths(pattern, paths)` -> the subsequence of `paths` (a `list` or
  `tuple` of `str`) that `match(pattern, p)` is true for, in their original
  order, without mutating `paths`. Raises `TypeError` if `paths` is not a
  `list`/`tuple` or contains a non-`str`, and the same `GlobPatternError` as
  `match` for a malformed `pattern` (validate the pattern once, not once per
  path).

## Paths and segments

Both `pattern` and `path` use `/` as the only separator (never `\`), and are
split into segments on `/`. A `pattern` must not be empty and must not
contain an empty segment -- no leading `/`, no trailing `/`, no doubled `//`
-- any of those raise `GlobPatternError`. `path`, by contrast, is never
validated and never raises: it is just data, split the same way, and an
empty segment in a `path` (from `//`, or a leading/trailing `/`) is matched
by the ordinary segment rules below like any other segment (so a pattern
segment of `*` does match an empty path segment, since `*` matches zero or
more characters; a literal pattern segment does not).

Matching never crosses a `/` boundary except through `**` (below). All
matching is case-sensitive; there is no platform-dependent behavior and no
special treatment of a leading `.` in a path segment -- `*` matches a
dotfile's name exactly like any other name.

## Segment syntax (every segment except a bare `**`)

Within one segment:

- A literal character matches itself.
- `*` matches zero or more characters, but never a `/` (segments are
  already split on `/`, so this is automatic).
- `?` matches exactly one character (not `/`).
- `[...]` matches exactly one character from a set: `[abc]` is `a`, `b`, or
  `c`; `[a-z]` is an inclusive range; ranges and literals can be combined,
  e.g. `[a-zA-Z0-9_]`. A leading `!` or `^` right after `[` negates the set
  (`[!abc]` / `[^abc]` both mean "any one character not in the set").
  A literal `]` can be the set's first member (right after `[`, or right
  after the `!`/`^`), e.g. `[]ab]` is `]`, `a`, or `b`. A literal `-` can be
  the first or last member of the set to mean a hyphen rather than a range.
  The characters `]`, `^`, and `\` cannot themselves be used as a *range
  endpoint* (only as standalone literal members) -- this case is simply not
  supported, don't worry about it. An unterminated `[` (no closing `]`), or
  an empty set (`[]` with nothing in it, or `[!]`/`[^]` with nothing after
  the negation), raises `GlobPatternError`. A backslash has no special
  meaning inside `[...]` -- it is just a literal backslash character to
  match, same as any other ordinary character; escaping (below) does not
  apply inside brackets.
- `\` escapes the next character, making it literal (so `\*`, `\?`, `\[`,
  and `\\` match a literal `*`, `?`, `[`, and `\`). A trailing `\` with
  nothing after it (at the end of the segment) raises `GlobPatternError`.
- Any other character matches itself.

Two or more consecutive `*` inside a segment behave exactly the same as one
`*` (there is nothing special about e.g. `a**b` -- read it as the ordinary
segment `a`, `*`, `*`, `b`, which matches the same strings as `a*b`). This
matters because of the next rule.

## `**` -- the globstar

A segment is a globstar **only** when, after splitting on `/`, its entire
text is exactly the two characters `**` and nothing else. `a**`, `**b`, and
`***` are *not* globstars -- they're ordinary segments under the rule
above, matched within a single path segment only, never crossing a `/`.

A true `**` segment matches **zero or more entire path segments**. This
means:

- `a/**/b` matches `a/b` (zero segments in between), `a/x/b`, `a/x/y/b`, ...
- `a/**` matches `a` itself (zero extra segments), as well as `a/b`,
  `a/b/c`, ...
- `**/b` matches `b` itself (zero segments before it), as well as `x/b`,
  `x/y/b`, ...
- Consecutive globstar segments, e.g. `a/**/**/b`, behave exactly like a
  single `**` -- still zero or more segments overall, not "two or more".

## Errors

`GlobPatternError` (a `ValueError` subclass) covers every malformed-pattern
case above: empty pattern, empty segment, unterminated or empty character
class, trailing backslash, or an invalid range inside `[...]` (such as
`[z-a]`, where the range is backwards). `TypeError` covers wrong argument
types in `match`/`filter_paths`, as described above. Nothing about `path`
or `paths` entries is ever validated beyond their type.

A couple of basic checks are sketched in `tests/test_globmatch.py`.
