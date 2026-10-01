"""Turn free text into a list of words."""


def tokenize(text):
    """Split text into maximal runs of alphabetic characters, case-folded.

    Digits, punctuation, and whitespace are all separators and never
    part of a word.
    """
    words = []
    current = []
    for ch in text:
        if ch.isalpha():
            current.append(ch)
        else:
            if current:
                words.append("".join(current).lower())
                current = []
    if current:
        words.append("".join(current).lower())
    return words
