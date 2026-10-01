"""Text cleaning and analysis helpers, all mixed together."""

_PUNCTUATION = ".,!?;:\"'()[]"


def clean_text(text):
    result = []
    previous_was_space = False
    for ch in text.lower():
        if ch.isspace():
            if not previous_was_space:
                result.append(" ")
            previous_was_space = True
        else:
            result.append(ch)
            previous_was_space = False
    return "".join(result).strip()


def strip_punctuation(text):
    return "".join(ch for ch in text if ch not in _PUNCTUATION)


def normalize(text):
    return clean_text(strip_punctuation(text))


def title_case(text):
    return " ".join(w.capitalize() for w in normalize(text).split())


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
