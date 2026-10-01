"""A small RFC-3986-style query-string codec (not form-urlencoding)."""

_UNRESERVED = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "abcdefghijklmnopqrstuvwxyz" "0123456789" "-._~"
)
_HEX_DIGITS = set("0123456789ABCDEFabcdef")


class QueryStringError(ValueError):
    """Raised when query-string text passed to decode_query is malformed."""


def _encode_part(value):
    if not isinstance(value, str):
        raise TypeError(f"expected str, got {type(value).__name__}")
    out = []
    for byte in value.encode("utf-8"):
        ch = chr(byte)
        if byte < 128 and ch in _UNRESERVED:
            out.append(ch)
        else:
            out.append(f"%{byte:02X}")
    return "".join(out)


def encode_query(params):
    if not isinstance(params, (list, tuple)):
        raise TypeError(f"params must be a list or tuple, got {type(params).__name__}")

    pairs = []
    for entry in params:
        if not isinstance(entry, (list, tuple)) or len(entry) != 2:
            raise TypeError("each entry must be a 2-item (key, value) sequence")
        key, value = entry
        pairs.append(f"{_encode_part(key)}={_encode_part(value)}")

    return "&".join(pairs)


def _decode_part(text):
    out = bytearray()
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "%":
            if i + 2 >= n or text[i + 1] not in _HEX_DIGITS or text[i + 2] not in _HEX_DIGITS:
                raise QueryStringError(f"malformed percent-escape at position {i}")
            out.append(int(text[i + 1 : i + 3], 16))
            i += 3
        else:
            out.extend(ch.encode("utf-8"))
            i += 1

    try:
        return out.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise QueryStringError(f"percent-decoded bytes are not valid UTF-8: {exc}")


def decode_query(text):
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")

    if text == "":
        return []

    result = []
    for segment in text.split("&"):
        key_text, sep, value_text = segment.partition("=")
        if not sep:
            value_text = ""
        result.append((_decode_part(key_text), _decode_part(value_text)))

    return result
