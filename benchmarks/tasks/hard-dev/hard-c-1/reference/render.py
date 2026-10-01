"""Render chat messages for display in a terminal client."""

import warnings
from dataclasses import dataclass

_UNSET = object()


@dataclass(frozen=True)
class RenderOptions:
    width: int = 72
    show_timestamp: bool = True
    timestamp_format: str = "%H:%M"
    author_width: int = 12


def _resolve_options(options, width, show_timestamp, timestamp_format,
                      author_width, *, stacklevel):
    legacy_given = (
        width is not _UNSET
        or show_timestamp is not _UNSET
        or timestamp_format is not _UNSET
        or author_width is not _UNSET
    )
    if legacy_given and options is not None:
        raise TypeError(
            "pass either options= or the legacy width/show_timestamp/"
            "timestamp_format/author_width parameters, not both"
        )
    if legacy_given:
        warnings.warn(
            "passing width/show_timestamp/timestamp_format/author_width "
            "directly is deprecated; pass options=RenderOptions(...) instead",
            DeprecationWarning,
            stacklevel=stacklevel,
        )
        defaults = RenderOptions()
        return RenderOptions(
            width=defaults.width if width is _UNSET else width,
            show_timestamp=defaults.show_timestamp if show_timestamp is _UNSET else show_timestamp,
            timestamp_format=defaults.timestamp_format if timestamp_format is _UNSET else timestamp_format,
            author_width=defaults.author_width if author_width is _UNSET else author_width,
        )
    if options is not None:
        return options
    return RenderOptions()


def _render_one(author, text, timestamp, options):
    if options.show_timestamp:
        prefix = f"[{timestamp.strftime(options.timestamp_format)}] "
    else:
        prefix = ""
    if len(author) > options.author_width:
        label = author[: options.author_width - 1] + "…"
    else:
        label = author.ljust(options.author_width)
    line = f"{prefix}{label}: {text}"
    if len(line) > options.width:
        if options.width <= 3:
            raise ValueError("width too small to render a message")
        line = line[: options.width - 3] + "..."
    return line


def render_message(author, text, timestamp, width=_UNSET, show_timestamp=_UNSET,
                    timestamp_format=_UNSET, author_width=_UNSET, *, options=None):
    """Render a single chat message as one display line.

    `timestamp` is a `datetime.datetime`. The author name is padded or
    truncated to `options.author_width` characters, and the whole line is
    truncated to `options.width` characters (with a trailing "...") if
    needed. Pass `options=RenderOptions(...)` to configure this, or use the
    legacy width=/show_timestamp=/timestamp_format=/author_width= parameters
    (deprecated).
    """
    resolved = _resolve_options(
        options, width, show_timestamp, timestamp_format, author_width, stacklevel=2
    )
    return _render_one(author, text, timestamp, resolved)
