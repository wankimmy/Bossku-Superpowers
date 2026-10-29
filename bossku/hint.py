"""Put a skill suggestion in front of the agent when the user sends a prompt.

Agents rarely open a skill nobody pointed them to. A `UserPromptSubmit` hook runs this router over the
prompt and adds one short, honest hint (the best matches, with their own descriptions), so the
choice is made on the request itself instead of on a skill list the agent has already stopped reading.

The hint uses task evidence, names up to three complementary skills, accepts eligible explicit requests, and stays
under 800 characters. The old `hint_mode` setting (v1/v2) is gone; a leftover key in ~/.bosskuai/config.json is ignored.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import bossku.index as bossku_index
import bossku.skills as skills
from bossku.index import load_index, skill_index_signature
from bossku.paths import routing_index_copy, routing_signature_path
from bossku.rules import prompt_reminder, states_rule
from bossku.skills import NOT_INSTALLED, locate_skill, select_skill_stack, skill_has_task_evidence

MIN_WORDS = 5            # retained for callers; evidence, not word count, decides eligibility
MIN_TOP_SCORE = 12.0     # legacy benchmark/caller compatibility; not an eligibility gate
MAX_HINTS = 3            # one primary and at most two distinct prompt concerns
HINT_CHARS = 800         # the hint without the separate rule reminder
DESCRIPTION_CHARS = 100
SHORT_DESCRIPTION_CHARS = 60
HOSTS = ("claude", "codex")
NONCE_ENV = "BOSSKU_HINT_NONCE"     # test only: the delivery canary asks the agent to quote this value back
_NONCE = re.compile(r"[A-Za-z0-9_.-]{1,40}")
EXPLICIT = "explicit skill request"
# Prompts the app submits that no person typed (a finished background task, a CI event). Same list as
# bossku.gate._NOT_TYPED, kept here so the per-prompt hook does not import the gate.
NOT_TYPED = ("<ci-monitor-event>", "<task-notification>", "<agent-message", "<local-command", "<system-reminder>")
RESUME_MAX_WORDS = 8     # a longer prompt is a real request that merely contains the word
# Kept here, not in bossku.resume, so a prompt that is not "continue" never pays for importing that module.
RESUME_TRIGGER = re.compile(
    r"\b(?:continue|carry\s+on|keep\s+going|pick\s+up|lanjut(?:kan)?|sambung|teruskan|bossku\s+resume)\b", re.I)
_BOILERPLATE = re.compile(
    r"^(?:use this (?:skill )?(?:for|when|to)|use when|use for|use to|"
    r"when the user (?:wants|needs|asks)(?: help)?(?: with| to| for)?)\s+", re.I)
_ID_CHAR = re.compile(r"[\w-]")


def _short(description: str, limit: int = 110) -> str:
    """The first sentence of a description without its 'Use when...' lead-in, cut to a short line."""
    text = " ".join(description.split())
    text = re.split(r"(?<=[a-z0-9)])\.\s", text, maxsplit=1)[0]
    text = _BOILERPLATE.sub("", text).rstrip(".")
    if limit == 0:
        return "See skill instructions"
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."


def wants_resume(prompt: str) -> bool:
    """A short prompt that asks to go on ("continue", "lanjut", "bossku resume"); slash commands never do."""
    text = prompt.strip()
    # "continue what codex was doing, ask me if unsure" names the task it means, so it may run longer.
    limit = RESUME_MAX_WORDS * 2 if re.search(r"\bcodex\b", text, re.I) else RESUME_MAX_WORDS
    return bool(text) and not text.startswith(("/", "!")) and len(text.split()) <= limit \
        and RESUME_TRIGGER.search(text) is not None


def _copied_index(root: Path | None, home: Path | None) -> dict | None:
    """The index copy `bossku install` keeps in ~/.bosskuai, when its signature still matches the skills in `root`.
    None means: read the repo's own saved index, as the hook always did."""
    try:
        stored = routing_signature_path(home).read_text(encoding="utf-8").strip()
        if not stored or stored != skill_index_signature(root):
            return None
        data = json.loads(routing_index_copy(home).read_text(encoding="utf-8"))
    except (OSError, ValueError):   # no copy (an older install), or a skills folder that moved
        return None
    return data if isinstance(data, dict) else None


def _mentions_a_skill(text: str, names) -> bool:
    """True when a skill id or alias stands in the text as a whole word (a cheap look; select_skill_stack decides)."""
    for name in names:
        at = text.find(name)
        while at >= 0:
            end = at + len(name)
            if not (at and _ID_CHAR.match(text[at - 1])) and not (end < len(text) and _ID_CHAR.match(text[end])):
                return True
            at = text.find(name, at + 1)
    return False


def pick_skills(prompt: str, *, root: Path | None = None, min_words: int = MIN_WORDS,
                data: dict | None = None) -> list[dict]:
    """Name eligible selected skills with task evidence; short requests get hints too.

    `min_words` remains accepted for caller compatibility. The host handles slash
    commands directly; greetings, fallback selections and lexical coincidences stay silent.
    """
    prompt = prompt.strip()
    if not prompt or prompt.startswith(("/", "!")) or any(tag in prompt[:200] for tag in NOT_TYPED):
        return []
    data = skills._routing_index(root) if data is None else data
    rows = select_skill_stack(prompt, root, limit=MAX_HINTS, data=data)["selected"]
    return [row for row in rows
            if row["skill_id"] not in NOT_INSTALLED
            and not row["reason"].startswith("insufficient eligible evidence")
            and skill_has_task_evidence(row, prompt, data)][:MAX_HINTS]


def _posix(path) -> str:
    return str(path).replace("\\", "/")


def _bossku_command() -> str:
    """The absolute `bossku` the footer names: forward slashes (Git Bash drops backslashes), quoted only for a space."""
    from bossku.hooks import resolve_bossku_argv

    exe, *rest = resolve_bossku_argv()
    exe = _posix(exe)
    return " ".join([f'"{exe}"' if " " in exe else exe, *rest])


def render_hint(picks: list[dict], *, root: Path | None = None, home: Path | None = None, host: str = "claude") -> str:
    """Bounded host-aware loading instructions."""
    located = [(row, *locate_skill(row["skill_id"], root, home)) for row in picks[:MAX_HINTS]]
    command = _bossku_command()
    ways = [("Skill tool" if kind == "listed" and host == "claude"
             else f"Read {_posix(path)}" if path else f"run `{command} skills show {row['skill_id']}`")
            for row, kind, path in located]
    head = ("BosskuAI skill hint: load the best fit before you start, and the others only if they cover "
            "another part of the request:\n")
    foot = "\nSkip if the task is trivial or none fits."
    if any(way.startswith("Read ") for way in ways):    # only a read can be refused
        foot += f" If a read is refused, run `{command} skills show <id>`."

    def text(count: int, limit: int) -> str:
        lines = [f"- {row['skill_id']}: {_short(row['description'], limit)} ({way})"
                 for (row, _, _), way in zip(located, ways)]
        return head + "\n".join(lines[:count]) + foot

    # Shorter descriptions before fewer skills: a second concern is worth more than the tail of a sentence.
    count, limit = len(located), DESCRIPTION_CHARS
    if len(text(count, limit)) > HINT_CHARS:
        limit = SHORT_DESCRIPTION_CHARS
        while count > 1 and len(text(count, limit)) > HINT_CHARS:
            count -= 1
    result = text(count, limit)
    if len(result) <= HINT_CHARS:
        return result
    # Paths and executable names can be arbitrarily long. Use the installed command name
    # as a last resort rather than truncating a path into an unusable loading instruction.
    head = "BosskuAI skill hint: load the best fit before starting:\n"
    foot = "\nSkip if the task is trivial or none fits."
    ways = ["Skill tool" if kind == "listed" and host == "claude"
            else f"run `bossku skills show {row['skill_id']}`" for row, kind, _ in located]
    while count and len(text(count, 0)) > HINT_CHARS:
        count -= 1
    return text(count, 0)


def build_hint(prompt: str, *, root: Path | None = None, home: Path | None = None, host: str = "claude") -> str | None:
    """The suggestion for this prompt, or None when there is nothing worth saying."""
    picks = pick_skills(prompt, root=root)
    if not picks:
        return None
    text = render_hint(picks, root=root, home=home, host=host)
    nonce = os.environ.get(NONCE_ENV, "")
    return f"{text} [nonce {nonce}]" if _NONCE.fullmatch(nonce) else text


def hook_output(payload_text: str, *, root: Path | None = None, home: Path | None = None, host: str = "claude") -> dict:
    """The JSON a `UserPromptSubmit` hook prints (Claude Code and Codex alike); empty when there is no hint."""
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
    except json.JSONDecodeError:
        return {}
    prompt = payload.get("prompt") if isinstance(payload, dict) else None
    if not isinstance(prompt, str):
        return {}
    cwd = payload.get("cwd")
    # "continue" after Codex hit its limit: hand over its brief. Not inside Codex itself: that would use the brief up.
    if host == "claude" and isinstance(cwd, str) and wants_resume(prompt):
        from bossku.resume import resume_context

        brief = resume_context(cwd, home=home)
        if brief:
            return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": brief}}
    # Every prompt pays for this hook, so read the saved index instead of re-hashing all skills per lookup, and build
    # the idf table once: ranking the prompt and each of its clauses would rebuild it every time (a quarter of the time).
    original, saved = skills._routing_index, {}
    idf_original, idf_saved = bossku_index.compute_idf, {}

    def saved_index(index_root=None):
        if "data" not in saved:
            saved["data"] = _copied_index(index_root, home) or load_index(index_root) or original(index_root)
        return saved["data"]

    def saved_idf(entries):
        if id(entries) not in idf_saved:
            idf_saved[id(entries)] = (entries, idf_original(entries))    # holding entries keeps its id from being reused
        return idf_saved[id(entries)][1]

    skills._routing_index = saved_index
    bossku_index.compute_idf = saved_idf
    try:
        hint = build_hint(prompt, root=root, home=home, host=host)
    except Exception:  # noqa: BLE001 - a hint is a convenience; it must never break the user's prompt
        hint = None
    finally:
        skills._routing_index = original
        bossku_index.compute_idf = idf_original
    parts = [hint] if hint else []
    project = os.environ.get("CLAUDE_PROJECT_DIR") or (cwd if isinstance(cwd, str) else "")
    if not prompt.strip().startswith(("/", "!")) and not any(tag in prompt[:200] for tag in NOT_TYPED):
        from bossku.design import design_reminder
        from bossku.security import security_reminders

        design = design_reminder(prompt)
        if design:
            parts.append(design)
        try:
            parts.extend(security_reminders(prompt, project, home=home))
        except Exception:  # noqa: BLE001 - like the hint, never break the user's prompt
            pass
    if states_rule(prompt):
        parts.append(prompt_reminder(project))
    if not parts:
        return {}
    return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "\n".join(parts)}}
