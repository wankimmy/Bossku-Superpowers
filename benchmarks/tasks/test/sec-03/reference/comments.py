"""Render visitor comments as a small, safe HTML snippet."""
from urllib.parse import urlsplit

_ALLOWED_SCHEMES = {"http", "https", "mailto"}


def _escape(value, quotes=False):
    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if quotes:
        value = value.replace('"', "&quot;")
    return value


def _is_allowed_link(link):
    if not link:
        return False
    return urlsplit(link).scheme.lower() in _ALLOWED_SCHEMES


def render_comment(author, text, link=None):
    safe_author = _escape(author)
    safe_text = _escape(text)
    if _is_allowed_link(link):
        safe_link = _escape(link, quotes=True)
        return (f'<div class="comment"><a class="author" href="{safe_link}">'
                f'{safe_author}</a><p>{safe_text}</p></div>')
    return f'<div class="comment"><span class="author">{safe_author}</span><p>{safe_text}</p></div>'
