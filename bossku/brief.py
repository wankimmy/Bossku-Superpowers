"""A short brief of what project memory already says, in one call instead of reading five files.

Reading notes the usual way costs an agent one call to find the folder and one per file, and every call
re-reads the whole conversation. `bossku memory-brief` prints the newest entries of every note file, trimmed
to a fixed budget; the `SessionStart` hook puts the same brief in the agent's context before it starts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from bossku.memory import memory_directory

# Template text written by `bossku init`; a file that only holds this has nothing to say.
TEMPLATE_LINES = {
    "Durable decisions only.", "Active and recent plans.", "Verified lessons worth repeating.",
    "One-paragraph summary of what this repo is and who it serves.", "Ephemeral continuation state. Clear when done.",
}
FILES = (("handoff.md", "handoff"), ("decisions.md", "decision"), ("plans.md", "plan"),
         ("learnings.md", "learning"), ("project.md", "project"))
_HEADING = re.compile(r"^## (.+)$", re.M)


def _entries(text: str) -> list[tuple[str, str]]:
    """(stamp, body) pairs in the file's order; text before the first stamp counts as an unstamped entry."""
    parts = _HEADING.split(text)
    entries = []
    head = " ".join(line.strip() for line in parts[0].splitlines() if line.strip() and not line.startswith("#")
                    and line.strip() not in TEMPLATE_LINES)
    if head:
        entries.append(("", head))
    for stamp, body in zip(parts[1::2], parts[2::2]):
        body = " ".join(body.split())
        if body and body not in TEMPLATE_LINES:
            entries.append((stamp.strip(), body))
    return entries


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."


def memory_brief(project: Path, *, home: Path | None = None, limit: int = 1400, per_entry: int = 260) -> str:
    """Newest entries first, at most `limit` characters; empty when there is nothing worth saying."""
    try:
        folder = memory_directory(project, home=home)
    except (ValueError, OSError):
        return ""   # no vault or no project memory: stay quiet instead of failing a session
    lines: list[str] = []
    used = 0
    for filename, label in FILES:
        path = folder / filename
        try:
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
        except OSError:
            continue
        for stamp, body in reversed(_entries(text)):
            line = f"- [{label}{' ' + stamp if stamp else ''}] {_clip(body, per_entry)}"
            if used + len(line) > limit:
                break
            lines.append(line)
            used += len(line)
            if label == "project":
                break   # the project summary is one paragraph; older stamps are history
    if not lines:
        return ""
    return ("BosskuAI project notes (newest first, trimmed; these are already in your context, "
            "so do not read the memory files again):\n" + "\n".join(lines))


def session_output(payload_text: str, *, home: Path | None = None) -> dict:
    """What a Claude Code `SessionStart` hook prints: the brief for the session's folder, or nothing."""
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
    except json.JSONDecodeError:
        return {}
    cwd = payload.get("cwd") if isinstance(payload, dict) else None
    if not cwd:
        return {}
    try:
        brief = memory_brief(Path(cwd), home=home)
    except Exception:  # noqa: BLE001 - a convenience must never break a session
        return {}
    if not brief:
        return {}
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": brief}}
