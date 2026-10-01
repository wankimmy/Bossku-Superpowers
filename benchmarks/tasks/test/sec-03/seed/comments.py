"""Render visitor comments as a small HTML snippet."""


def render_comment(author, text, link=None):
    safe_author = author.replace("<", "&lt;").replace(">", "&gt;")
    safe_text = text.replace("<", "&lt;").replace(">", "&gt;")
    if link:
        return f'<div class="comment"><a class="author" href="{link}">{safe_author}</a><p>{safe_text}</p></div>'
    return f'<div class="comment"><span class="author">{safe_author}</span><p>{safe_text}</p></div>'
