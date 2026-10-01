"""Read and write the pipe-delimited, backslash-escaped record format.

Records are separated by real newline characters; fields within a record are
separated by real "|" characters. A literal "|", "\\", or newline inside a
field's value is written as the two-character escape sequence "\\|", "\\\\",
or "\\n" respectively.
"""


class PipeFormatError(ValueError):
    """Raised when pipe-delimited text is malformed."""


def _split_records(text):
    if text == "":
        return []
    pieces = text.split("\n")
    if len(pieces) > 1 and pieces[-1] == "":
        pieces = pieces[:-1]
    return pieces


def _parse_record_fields(raw):
    fields = []
    current = []
    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]
        if ch == "\\":
            if i + 1 >= n:
                raise PipeFormatError("trailing escape character at end of record")
            nxt = raw[i + 1]
            if nxt == "|":
                current.append("|")
            elif nxt == "\\":
                current.append("\\")
            elif nxt == "n":
                current.append("\n")
            else:
                raise PipeFormatError(f"invalid escape sequence '\\{nxt}'")
            i += 2
        elif ch == "|":
            fields.append("".join(current))
            current = []
            i += 1
        else:
            current.append(ch)
            i += 1
    fields.append("".join(current))
    return fields


def parse_records(text):
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    return [_parse_record_fields(raw) for raw in _split_records(text)]


def _escape_field(value):
    if not isinstance(value, str):
        raise TypeError(f"field must be a str, got {type(value).__name__}")
    out = []
    for ch in value:
        if ch == "\\":
            out.append("\\\\")
        elif ch == "|":
            out.append("\\|")
        elif ch == "\n":
            out.append("\\n")
        else:
            out.append(ch)
    return "".join(out)


def format_records(records):
    if not isinstance(records, (list, tuple)):
        raise TypeError(f"records must be a list or tuple, got {type(records).__name__}")

    lines = []
    for row in records:
        if not isinstance(row, (list, tuple)):
            raise TypeError(f"each row must be a list or tuple, got {type(row).__name__}")
        if len(row) == 0:
            raise PipeFormatError("a row must have at least one field")
        lines.append("|".join(_escape_field(field) for field in row))

    if not lines:
        return ""
    return "\n".join(lines) + "\n"
