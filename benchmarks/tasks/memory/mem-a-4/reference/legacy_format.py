"""Legacy row parser. Owned by the data-platform team."""


def parse_line(line):
    parts = line.split("|")
    if len(parts) != 3:
        raise ValueError("expected 3 fields, got {}".format(len(parts)))
    name, qty, price = parts
    return {"name": name, "qty": int(qty), "price_cents": int(price)}
