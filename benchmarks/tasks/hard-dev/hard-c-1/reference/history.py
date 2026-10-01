"""Render a sequence of chat messages as one block of text."""

from render import _UNSET, _render_one, _resolve_options


def render_history(messages, width=_UNSET, show_timestamp=_UNSET,
                    timestamp_format=_UNSET, author_width=_UNSET, *, options=None):
    """Render `messages` (a list of {"author", "text", "timestamp"} dicts)
    by rendering each one and joining with newlines.

    Accepts `options=RenderOptions(...)` or the legacy width=/show_timestamp=/
    timestamp_format=/author_width= parameters (deprecated). Regardless of
    how many messages are rendered, at most one DeprecationWarning is raised
    per call when the legacy parameters are used.
    """
    resolved = _resolve_options(
        options, width, show_timestamp, timestamp_format, author_width, stacklevel=2
    )
    lines = [
        _render_one(m["author"], m["text"], m["timestamp"], resolved)
        for m in messages
    ]
    return "\n".join(lines)
