# httpheader

A small library for parsing structured HTTP header *values* -- not whole
headers, just the value part you'd get after the `Name:` -- for a proxy
we're writing. Add a new `httpheader.py` at the project root with three
functions and one exception class, following this spec exactly (it is
deliberately more precise than "how browsers usually do it", so please
implement what's written here rather than from memory of HTTP).

`HeaderParseError` (a `ValueError` subclass) is raised by all three
functions for a malformed `value`. All three raise `TypeError` if `value`
is not a `str`.

## Quoted strings, shared by all three functions

Wherever this spec mentions a "quoted string", it means: a `"` character,
followed by any characters, followed by a closing `"`. Inside it, `\"`
means a literal `"` and `\\` means a literal `\`; no other character may
follow a `\` (that's an error). A `"` with no matching closing `"` is an
error ("unterminated"). Nothing outside a quoted string is ever escaped --
a `\` outside quotes is just an ordinary character.

## `split_list(value)`

Splits `value` into a `list` of element strings on top-level commas --
commas *inside* a quoted string don't split. Each element has leading and
trailing spaces/tabs stripped (whitespace *inside* a quoted part of an
element is left alone). An element that is empty after stripping is
dropped entirely -- this means leading commas, trailing commas, and
doubled commas are all fine and simply don't produce an empty entry
(`",a,,b,"` -> `["a", "b"]`). Elements are **not** unescaped or unquoted by
this function -- quotes and backslash-escapes inside an element are left
exactly as written; that's a different function's job. `split_list("")` is
`[]`.

## `parse_params(value)`

Parses a `main-value; key1=value1; key2="quoted value"` style header (like
`Content-Type` or `Content-Disposition`) into `(main_value, params)`, where
`params` is a `list` of `(key, value)` tuples **in the order they appear**
-- duplicates are kept, never collapsed.

- `value` is split on top-level semicolons (quote-aware, same rule as
  `split_list`). The first chunk is `main_value`; each later chunk is one
  parameter.
- `main_value`, after stripping surrounding whitespace, must be a *bare
  token*: non-empty, and containing none of space, tab, `"`, `;`, `=`.
  Unlike `split_list`'s comma elements, **an empty chunk here is always an
  error, never silently dropped** -- so `value=";a=1"` (empty main) and
  `"x;;a=1"` (empty parameter between two semicolons) both raise
  `HeaderParseError`, as does a trailing `;` with nothing after it.
- Each parameter chunk must contain a top-level `=`; split it on the
  *first* `=`. The key, after stripping whitespace, must be a bare token
  (same rule as above) and is **lowercased** before being stored. The
  value, after stripping whitespace, is either a quoted string (quotes
  removed, escapes resolved, and nothing but whitespace allowed between
  the closing quote and the next `;`) or a bare token (same character
  restriction as a key -- so a value containing a space or another `=`
  must be quoted, or it's an error).

## `parse_quality_list(value)`

Parses an `Accept`/`Accept-Language`-style weighted list, e.g.
`"en-US,en;q=0.8,fr;q=0.9,*;q=0.1"`, into a `list` of `(item, q)` tuples
sorted by **descending `q`**, ties broken by keeping the original left-to-
right order (a stable sort on `-q`).

- First apply `split_list` to `value` (so quoting and empty-element-
  dropping behave identically to `split_list`). Then run each resulting
  element through `parse_params`, exactly as above (so an element's own
  `;`-separated parameters are parsed the same way a `Content-Type`'s
  would be).
- Only the `q` parameter matters; any other parameter on an element is
  parsed (so it can still cause an error if *it's* malformed) but
  otherwise ignored. If `q` appears more than once on the same element,
  the **last** occurrence wins. If there's no `q` at all, it defaults to
  `1.0`.
- A q-value's text must match one of exactly these two shapes: `0`
  optionally followed by `.` and zero to three digits, or `1` optionally
  followed by `.` and zero to three `0` digits (so `1`, `1.0`, `1.000`,
  `0`, `0.5`, `0.123`, and even `0.` are all valid; `1.5`, `1.0001`,
  `-0.5`, `01`, and `+1` are all invalid). This means **a value can never
  exceed `1`**, and `1.2` is invalid even though `1.2` would be a
  perfectly normal decimal number elsewhere.

A couple of basic checks are sketched in `tests/test_httpheader.py`.
