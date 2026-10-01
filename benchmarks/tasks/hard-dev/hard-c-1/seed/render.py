"""Render chat messages for display in a terminal client.

This is deliberately just string formatting - no I/O, no knowledge of
where the messages came from. `history.py` builds on top of this to
render a whole conversation, and `cli.py` is the one place that actually
reads anything from disk.
"""


def render_message(author, text, timestamp, width=72, show_timestamp=True,
                    timestamp_format="%H:%M", author_width=12):
    """Render a single chat message as one display line.

    `timestamp` is a `datetime.datetime`. The author name is padded or
    truncated to `author_width` characters, and the whole line is
    truncated to `width` characters (with a trailing "...") if needed.

    Parameters
    ----------
    author : str
        Display name of the message's sender.
    text : str
        The message body, as typed by the sender.
    timestamp : datetime.datetime
        When the message was sent.
    width : int
        Maximum length, in characters, of the rendered line.
    show_timestamp : bool
        Whether to prefix the line with a formatted timestamp.
    timestamp_format : str
        `strftime`-style format used for the timestamp prefix.
    author_width : int
        Fixed column width reserved for the author name.
    """
    if show_timestamp:
        prefix = f"[{timestamp.strftime(timestamp_format)}] "
    else:
        prefix = ""
    if len(author) > author_width:
        label = author[: author_width - 1] + "…"
    else:
        label = author.ljust(author_width)
    line = f"{prefix}{label}: {text}"
    if len(line) > width:
        if width <= 3:
            raise ValueError("width too small to render a message")
        line = line[: width - 3] + "..."
    return line
