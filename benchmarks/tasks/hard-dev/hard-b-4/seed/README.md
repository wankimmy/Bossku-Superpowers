# Text Stats

Word-frequency analytics over free text.

Run tests: `python -m unittest discover -s tests`

## Tokenizing

`tokenize(text)` (in `textstats/tokenize.py`) splits text into words: a
word is a maximal run of Unicode alphabetic characters. Digits,
punctuation, and whitespace are all separators and are never part of a
word. Words are matched **case-insensitively using full Unicode case
folding** (Python's `str.casefold()`), not simple lowercasing - for
example `"Straße"` and `"STRASSE"` are the same word. `tokenize`
returns the words in the order they appear, case-folded.

## Counting

`word_frequencies(text, stopwords=None)` (in `textstats/frequency.py`)
counts case-folded words in `text`:

- `stopwords`, if given, is a set of (already case-folded) words to
  exclude from the count. **The caller's `stopwords` set is never
  modified by this call**, no matter what.
- The single-letter words `"a"` and `"i"` are always excluded too,
  whether or not they were in `stopwords` - but that's only for this
  call's own counting; it must never leak into the caller's
  `stopwords` set either.
- Returns a `dict` mapping each remaining word to how many times it
  appears. A word that doesn't appear (after exclusions) is not a key
  at all - no zero entries.

## Ranking

`most_common(counts, n)` (in `textstats/frequency.py`) takes the dict
`word_frequencies` returns and returns the top `n` as a list of
`(word, count)` tuples, highest count first. **Ties in count are
broken by alphabetical order of the word** (not by which word happened
to appear first in the text). If fewer than `n` distinct words exist,
it returns all of them, still correctly ordered. `n=0` returns `[]`.

## Summary report

`summarize(text, stopwords=None, top_n=5)` (in `textstats/report.py`)
returns:

```
{
  "total_words": int,       # sum of all counted word occurrences
  "distinct_words": int,    # number of distinct counted words
  "top_words": [...],       # most_common(counts, top_n)
}
```
