"""Turns plain lines of text into a formatted report."""
from settings import resolve_settings


def format_report(lines, overrides=None):
    settings = resolve_settings(overrides)
    out = []
    if settings["show_header"]:
        out.append("REPORT")
    for line in lines:
        out.append(settings["prefix"] + " " * settings["indent"] + line)
    if settings["tags"]:
        out.append("tags: " + ", ".join(settings["tags"]))
    return "\n".join(out)
