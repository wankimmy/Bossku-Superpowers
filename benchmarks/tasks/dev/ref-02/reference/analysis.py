"""Text statistics helpers."""
from cleaning import clean_text, normalize


def word_count(text):
    return len(normalize(text).split())


def sentence_count(text):
    cleaned = clean_text(text)
    return sum(1 for ch in cleaned if ch in ".!?")


def average_word_length(text):
    words = normalize(text).split()
    if not words:
        return 0.0
    return round(sum(len(w) for w in words) / len(words), 2)


def longest_word(text):
    words = normalize(text).split()
    if not words:
        return ""
    return max(words, key=len)
