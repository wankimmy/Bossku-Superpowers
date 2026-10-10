"""SKU parsing."""


def parse_sku(text):
    if not isinstance(text, str) or len(text) != 7 or text[2] != "-":
        raise ValueError("bad sku")
    letters, digits = text[:2], text[3:]
    if not all("A" <= c <= "Z" for c in letters) or not all("0" <= c <= "9" for c in digits):
        raise ValueError("bad sku")
    return letters, int(digits)


def is_valid_sku(text):
    try:
        parse_sku(text)
    except ValueError:
        return False
    return True


def find_skus(text):
    found = []
    for word in text.translate(str.maketrans({c: " " for c in "(),.;:[]"})).split():
        if is_valid_sku(word):
            found.append(parse_sku(word))
    return found
