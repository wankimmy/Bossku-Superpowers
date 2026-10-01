"""Text normalization helpers."""

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
