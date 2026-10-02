"""Strip leading/trailing whitespace from every string value in a row."""


def apply(row):
    return {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in row.items()
    }
