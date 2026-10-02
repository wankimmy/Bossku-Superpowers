"""Drop any key whose value is an empty string."""


def apply(row):
    return {key: value for key, value in row.items() if value != ""}
