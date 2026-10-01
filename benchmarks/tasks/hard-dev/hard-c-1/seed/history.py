"""Render a sequence of chat messages as one block of text.

Used by the CLI to replay an entire saved conversation, and by anything
else (a log viewer, a digest e-mail, ...) that wants a whole conversation
rendered consistently rather than calling `render_message` message by
message with its own formatting options.
"""

from render import render_message


def render_history(messages, width=72, show_timestamp=True,
                    timestamp_format="%H:%M", author_width=12):
    """Render `messages` (a list of {"author", "text", "timestamp"} dicts)
    by rendering each one with `render_message` and joining with newlines.

    All of the keyword arguments are forwarded unchanged to every call to
    `render_message` - this function doesn't add any formatting rules of
    its own, it just applies the same ones consistently across a list of
    messages instead of one at a time.
    """
    lines = [
        render_message(
            m["author"], m["text"], m["timestamp"],
            width=width, show_timestamp=show_timestamp,
            timestamp_format=timestamp_format, author_width=author_width,
        )
        for m in messages
    ]
    return "\n".join(lines)
