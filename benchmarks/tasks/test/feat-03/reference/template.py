"""Tiny `{{ dotted.name }}` template renderer, plus a greedy text wrapper."""


class TemplateError(Exception):
    pass


def _lookup(context, dotted_name):
    current = context
    for segment in dotted_name.split("."):
        if not isinstance(current, dict) or segment not in current:
            raise TemplateError(f"unknown placeholder {dotted_name!r}")
        current = current[segment]
    return current


def render(template, context):
    out = []
    i = 0
    n = len(template)
    while i < n:
        if template[i:i + 3] == "\\{{":
            out.append("{{")
            i += 3
        elif template[i:i + 2] == "\\\\":
            out.append("\\")
            i += 2
        elif template[i:i + 2] == "{{":
            end = template.find("}}", i + 2)
            if end == -1:
                raise TemplateError("unclosed placeholder")
            name = template[i + 2:end].strip()
            out.append(str(_lookup(context, name)))
            i = end + 2
        else:
            out.append(template[i])
            i += 1
    return "".join(out)


def wrap(text, width):
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        raise ValueError("width must be a positive integer")
    words = text.split()
    if not words:
        return ""
    lines = []
    current = words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return "\n".join(lines)
