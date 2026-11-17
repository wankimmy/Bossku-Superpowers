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
from bossku.redact import redact_note

# Template text written by `bossku init`; a file that only holds this has nothing to say.
TEMPLATE_LINES = {
    "Durable decisions only.", "Active and recent plans.", "Verified lessons worth repeating.",
    "One-paragraph summary of what this repo is and who it serves.", "Ephemeral continuation state. Clear when done.",
}
FILES = (("decisions.md", "decision"), ("plans.md", "plan"),
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


def _handoff_block(text: str, budget: int) -> str:
    """handoff.md as its own block: lines kept as written, cut at a line boundary. A longer file keeps its start and
    its FOR_NEXT_MODEL tail, because the next steps are what a new session needs most."""
    lines = [line.rstrip() for line in text.splitlines() if line.strip() and line.strip() not in TEMPLATE_LINES]
    if not any(not line.startswith("#") for line in lines):
        return ""   # a title alone says nothing
    if len("\n".join(lines)) <= budget:
        return "\n".join(lines)
    marker = "[handoff cut]"
    tail_at = next((i for i, line in enumerate(lines) if "FOR_NEXT_MODEL" in line), len(lines))
    tail = lines[tail_at:]
    head_size = len("\n".join(lines[:tail_at]))
    tail_room = max(budget // 2, budget - head_size - 2 * len(marker) - 4)   # the tail takes what the head leaves
    tail_cut = False
    while len(tail) > 1 and len("\n".join(tail)) > tail_room:
        tail.pop()   # an oversized tail keeps its first lines
        tail_cut = True
    if tail and len(tail[0]) > tail_room:
        tail[0] = _clip(tail[0], tail_room - 4)   # _clip may add "..."; one long FOR_NEXT_MODEL line is cut too, never kept whole
        tail_cut = True
    room = budget - len("\n".join(tail)) - 2 * len(marker) - 4
    head, head_cut = [], False
    for line in lines[:tail_at]:
        if len(line) + 1 > room:
            if room > 20:
                head.append(_clip(line, room - 4))   # a one-paragraph handoff still shows its start
            head_cut = True
            break
        head.append(line)
        room -= len(line) + 1
    return "\n".join(head + ([marker] if head_cut else []) + tail + ([marker] if tail_cut else []))


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."


RULE_ENTRY = 480   # decisions are rules: clipping one loses the exact name or value that matters

BRIEF_INTRO = ("BosskuAI project notes, newest first within each group. These rules and decisions apply to this "
               "request even when its own wording differs from them (names, values, formats): apply the rule and say "
               "so in your reply. "
               "Only an explicit instruction to change or drop a rule overrides it "
               "(do not read the memory files again):\n")


def memory_brief(project: Path, *, home: Path | None = None, limit: int = 1300, per_entry: int = 220) -> str:
    """Newest entries first within each file, at most `limit` characters; empty when there is nothing worth saying."""
    try:
        folder = memory_directory(project, home=home)
    except (ValueError, OSError):
        return ""   # no vault or no project memory: stay quiet instead of failing a session
    lines: list[str] = []
    used = 0
    try:
        handoff = _handoff_block((folder / "handoff.md").read_text(encoding="utf-8"), limit * 6 // 10)
    except (OSError, UnicodeDecodeError):
        handoff = ""   # no handoff yet, or one that is not UTF-8: the decisions still go out
    if handoff:
        lines.append("Handoff:\n" + handoff)
        used = len(lines[0])
    for filename, label in FILES:
        path = folder / filename
        try:
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
        except OSError:
            continue
        for stamp, body in reversed(_entries(text)):
            room = max(per_entry, RULE_ENTRY) if label == "decision" else per_entry
            line = f"- [{label}{' ' + stamp if stamp else ''}] {_clip(body, room)}"
            if used + len(line) > limit:
                break
            lines.append(line)
            used += len(line)
            if label == "project":
                break   # the project summary is one paragraph; older stamps are history
    if not lines:
        return ""
    return redact_note(BRIEF_INTRO + "\n".join(lines))


def session_output(payload_text: str, *, home: Path | None = None) -> dict:
    """What a Claude Code `SessionStart` hook prints: the project notes for the session's folder, plus a one-line pointer
    when Codex stopped on its usage limit here (new sessions only), as one context; nothing when there is neither."""
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
    except json.JSONDecodeError:
        return {}
    cwd = payload.get("cwd") if isinstance(payload, dict) else None
    if not cwd:
        return {}
    parts = []
    try:
        parts.append(memory_brief(Path(cwd), home=home))
    except Exception:  # noqa: BLE001 - a convenience must never break a session
        pass
    try:
        from bossku.learn import learned_index

        parts.append(learned_index(Path(cwd), home=home))
    except Exception:  # noqa: BLE001 - no vault, no learned skills: the notes still go out
        pass
    if payload.get("source") in ("startup", "clear"):   # not on resume or compact: the pointer was already seen
        try:
            from bossku.resume import session_pointer   # only a new session needs it

            parts.append(session_pointer(cwd, home=home))
        except Exception:  # noqa: BLE001 - and one failing must not hide the other
            pass
    context = "\n".join(part for part in parts if part)
    if not context:
        return {}
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}
