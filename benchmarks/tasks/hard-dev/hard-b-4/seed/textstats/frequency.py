"""Word frequency counting over free text."""

from .tokenize import tokenize

SINGLE_LETTER_EXTRAS = {"a", "i"}


def word_frequencies(text, stopwords=None):
    """Count words in `text`, excluding any in `stopwords` (case-folded).

    `stopwords` may be None (no exclusions besides the built-in short
    words) or a set of words to exclude. 1-letter words ('a', 'i') are
    always excluded in addition to whatever `stopwords` contains.
    """
    if stopwords is None:
        stopwords = set()
    stopwords.update(SINGLE_LETTER_EXTRAS)

    counts = {}
    for word in tokenize(text):
        if word in stopwords:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts


def most_common(counts, n):
    """Top `n` (word, count) pairs, highest count first, ties broken
    alphabetically by the word."""
    ranked = sorted(counts.items(), key=lambda item: -item[1])
    return ranked[1:n + 1]
