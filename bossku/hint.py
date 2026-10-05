"""Put a skill suggestion in front of the agent when the user sends a prompt.

Agents rarely open a skill nobody pointed them to. A `UserPromptSubmit` hook runs this router over the
prompt and adds one short, honest hint (the best one or two matches, with their own descriptions), so the
choice is made on the request itself instead of on a skill list the agent has already stopped reading.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import bossku.skills as skills
from bossku.index import load_index
from bossku.rules import prompt_reminder, states_rule
from bossku.skills import NOT_INSTALLED, locate_skill, select_skill_stack

MIN_WORDS = 5            # a short ping ("thanks", "run the tests") needs no skill
MIN_SCORE = 2.0          # below this the lexical evidence is a guess; say nothing
MAX_HINTS = 2
_BOILERPLATE = re.compile(
    r"^(?:use this (?:skill )?(?:for|when|to)|use when|use for|use to|"
    r"when the user (?:wants|needs|asks)(?: help)?(?: with| to| for)?)\s+", re.I)


def _short(description: str, limit: int = 110) -> str:
    """The first sentence of a description without its 'Use when...' lead-in, cut to a short line."""
    text = " ".join(description.split())
    text = re.split(r"(?<=[a-z0-9)])\.\s", text, maxsplit=1)[0]
    text = _BOILERPLATE.sub("", text).rstrip(".")
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."


def build_hint(prompt: str, *, root: Path | None = None, home: Path | None = None) -> str | None:
    """A two-line suggestion for this prompt, or None when there is nothing worth saying."""
    prompt = prompt.strip()
    if len(prompt.split()) < MIN_WORDS or prompt.startswith(("/", "!")):
        return None
    selection = select_skill_stack(prompt, root, limit=MAX_HINTS + 1)
    picks = []
    for row in selection["selected"]:
        if row["skill_id"] in NOT_INSTALLED or row["score"] < MIN_SCORE:
            continue
        if row["reason"].startswith("insufficient eligible evidence"):
            continue
        picks.append(row)
    if not picks:
        return None
    lines = []
    for row in picks[:MAX_HINTS]:
        kind, _ = locate_skill(row["skill_id"], root, home)
        how = "Skill tool" if kind == "listed" else f"`bossku skills show {row['skill_id']}`"
        lines.append(f"- {row['skill_id']}: {_short(row['description'])} (load with {how})")
    return ("BosskuAI skill hint: these skills match this request. Load the best fit before you start "
            "(both only if they cover different parts):\n"
            + "\n".join(lines)
            + "\nSkip only if the task is trivial or neither fits.")


def hook_output(payload_text: str, *, root: Path | None = None, home: Path | None = None) -> dict:
    """The JSON a Claude Code `UserPromptSubmit` hook prints; empty when there is no hint."""
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
    except json.JSONDecodeError:
        return {}
    prompt = payload.get("prompt") if isinstance(payload, dict) else None
    if not isinstance(prompt, str):
        return {}
    # Every prompt pays for this hook, so read the saved index instead of re-hashing all skills per lookup.
    original, saved = skills._routing_index, {}

    def saved_index(index_root=None):
        if "data" not in saved:
            saved["data"] = load_index(index_root) or original(index_root)
        return saved["data"]

    skills._routing_index = saved_index
    try:
        hint = build_hint(prompt, root=root, home=home)
    except Exception:  # noqa: BLE001 - a hint is a convenience; it must never break the user's prompt
        hint = None
    finally:
        skills._routing_index = original
    parts = [hint] if hint else []
    cwd = payload.get("cwd")
    project = os.environ.get("CLAUDE_PROJECT_DIR") or (cwd if isinstance(cwd, str) else "")
    if states_rule(prompt):
        parts.append(prompt_reminder(project))
    if not parts:
        return {}
    return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "\n".join(parts)}}
