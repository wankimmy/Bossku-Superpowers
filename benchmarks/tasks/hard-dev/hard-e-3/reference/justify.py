"""justify.py - full text justification with exact padding rules.

See README.md for the full specification.
"""


class JustifyError(ValueError):
    """Raised when width is not a positive integer."""


def _check_args(text, width):
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an int")
    if width <= 0:
        raise JustifyError("width must be positive")


def justify_paragraph(text, width):
    _check_args(text, width)
    words = text.split()
    if not words:
        return []

    lines = []
    current = []
    current_len = 0
    for word in words:
        if current and (current_len + len(current) + len(word) > width):
            lines.append(current)
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += len(word)
    if current:
        lines.append(current)

    out_lines = []
    last_index = len(lines) - 1
    for i, line_words in enumerate(lines):
        is_last = i == last_index
        total_chars = sum(len(w) for w in line_words)
        if is_last or len(line_words) == 1:
            line = " ".join(line_words)
            if len(line) >= width:
                out_lines.append(line)
            else:
                out_lines.append(line + " " * (width - len(line)))
        else:
            gaps = len(line_words) - 1
            extra = width - total_chars
            base, rem = divmod(extra, gaps)
            parts = [line_words[0]]
            for idx in range(1, len(line_words)):
                spaces = base + (1 if (idx - 1) < rem else 0)
                parts.append(" " * spaces)
                parts.append(line_words[idx])
            out_lines.append("".join(parts))
    return out_lines


def justify_text(text, width):
    _check_args(text, width)
    raw_lines = text.split("\n")
    paragraphs = []
    current_para = []
    for line in raw_lines:
        if line.strip() == "":
            if current_para:
                paragraphs.append(current_para)
                current_para = []
        else:
            current_para.append(line)
    if current_para:
        paragraphs.append(current_para)

    justified = []
    for para_lines in paragraphs:
        para_text = " ".join(para_lines)
        lines = justify_paragraph(para_text, width)
        justified.append("\n".join(lines))
    return "\n\n".join(justified)
