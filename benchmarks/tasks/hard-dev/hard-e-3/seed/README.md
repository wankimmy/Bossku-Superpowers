# justify

A fixed-width text justifier for plain-text reports (think of an old
word-processor's "justify" button, not a ragged-right word-wrap). Add a
new `justify.py` module at the project root with two functions and one
exception class, following this spec exactly -- it pins down several
details ("what happens to the last line") that are easy to get wrong by
half-remembering how `textwrap` or a basic word-wrap works.

`JustifyError` (a `ValueError` subclass) is raised when `width` is a valid
`int` but not positive. `TypeError` is raised when `text` is not a `str`,
or `width` is not an `int` (a `bool` counts as the wrong type here, even
though it's technically an `int`).

## `justify_paragraph(text, width)`

Treats `text` as a single paragraph and returns a `list` of line strings.

- Words are found by `text.split()` -- i.e. any run of whitespace
  (spaces, tabs, newlines, ...) separates words, and leading/trailing
  whitespace is ignored. `justify_paragraph("", width)` and an all-
  whitespace `text` both return `[]` (no lines at all).
- **Greedy line-filling**: starting an empty line, add the next word to
  the current line if doing so would keep the line's total length --
  every word's characters, plus exactly one space between each pair of
  words already on the line -- at or under `width`. The first word always
  goes on a line (even if that one word alone is already longer than
  `width` -- see below), no matter what. When a word doesn't fit, it
  starts a new line instead.
- **Full justification of every line except the last**: for a line that
  is *not* the paragraph's last line and has two or more words, compute
  `extra = width - (sum of that line's word lengths)` and
  `gaps = (number of words on the line) - 1`. Distribute `extra` spaces
  across the `gaps` gaps between words as evenly as possible: each gap
  gets `extra // gaps` spaces, and the leftover `extra % gaps` single
  spaces go to the *leftmost* gaps, one each (so earlier gaps may get one
  more space than later ones). The resulting line is always exactly
  `width` characters long.
- **The last line of the paragraph is never stretched**, no matter how
  many words it has: join its words with a single space each, then pad
  the right side with spaces out to `width`. A line with only one word
  (anywhere in the paragraph, last or not) can't be stretched either,
  since there's no gap to distribute into -- it gets the same
  left-justify-and-pad treatment as the last line.
- **A single word longer than `width`** is placed alone on its own line
  and returned exactly as-is, with no padding and no truncation -- that
  line is simply longer than `width`. This module never splits, hyphenates,
  or truncates a word.
- Tabs and newlines inside `text` are just whitespace, like a run of
  spaces -- there's no tab-stop expansion, and a paragraph's own internal
  line breaks are not preserved (words are reflowed from scratch).

## `justify_text(text, width)`

Handles multiple paragraphs and returns a single `str`.

- Split `text` on `\n` into physical lines. A *blank* line (empty, or
  only whitespace) separates paragraphs; one or more consecutive blank
  lines between two paragraphs collapse to a single separator either way.
  Leading and/or trailing blank lines (before the first paragraph, or
  after the last) produce no empty paragraph -- they're simply dropped.
- Each paragraph's physical lines are joined with a single space (so a
  word-break that merely happens to fall at the end of an input line
  doesn't matter -- see the reflow rule above) and run through
  `justify_paragraph` independently, with the same `width`.
- The final result joins each paragraph's justified lines with `\n`
  (within a paragraph) and separates paragraphs from each other with a
  blank line (`\n\n`). `text` with no paragraphs at all (empty, or
  nothing but blank lines) returns `""`.

A couple of basic checks are sketched in `tests/test_justify.py`.
