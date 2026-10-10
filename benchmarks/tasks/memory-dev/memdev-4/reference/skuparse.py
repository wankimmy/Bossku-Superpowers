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


def parse_order_line(line):
    qty_text, sep, sku = line.strip().partition("x ")
    if not sep or not qty_text.isascii() or not qty_text.isdigit() or int(qty_text) < 1:
        raise ValueError("bad order line")
    letters, number = parse_sku(sku)
    return int(qty_text), letters, number
