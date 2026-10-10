"""Put a skill suggestion in front of the agent when the user sends a prompt.

Agents rarely open a skill nobody pointed them to. A `UserPromptSubmit` hook runs this router over the
prompt and adds one short, honest hint (the best matches, with their own descriptions), so the
choice is made on the request itself instead of on a skill list the agent has already stopped reading.

`hint_mode` in ~/.bosskuai/config.json picks the policy. `v1` (the default) is what Claude Code has had so far and its
text does not change. `v2` can name up to three skills (the best one plus one for each other part of the request),
lets a skill the user named by id through, and keeps the whole hint under 800 characters.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import bossku.index as bossku_index
import bossku.skills as skills
from bossku.index import load_index, skill_index_signature
from bossku.paths import routing_index_copy, routing_signature_path, user_config_path
from bossku.rules import prompt_reminder, states_rule
from bossku.skills import NOT_INSTALLED, locate_skill, select_skill_stack

MIN_WORDS = 5            # a short ping ("thanks", "run the tests") needs no skill
MIN_SCORE = 2.0          # below this the lexical evidence is a guess; say nothing
# The hint costs tokens every time it speaks, so it speaks only when the best match is strong: on the tuning halves
# of two held-out prompt sets a top score of 12 or more picked an acceptable skill 97% of the time (41% of those
# prompts reached it), while the scores of spec-style coding prompts stay around 1-2.
MIN_TOP_SCORE = 12.0
V1_MAX_HINTS = 2         # hint_mode v1 asks for three, shows two: the third pick was always dropped
MAX_HINTS = 3            # hint_mode v2: one number for the select limit and the cap, so a third concern is kept
SECOND_MIN = 4.0         # v2: a later pick needs at least this much; the first one still needs MIN_TOP_SCORE
HINT_CHARS = 800         # v2: the hint without the rule reminder; the lowest pick goes first when it is longer
DESCRIPTION_CHARS = 100  # v2: the cut of each description (v1 keeps 110)
SHORT_DESCRIPTION_CHARS = 60   # v2: tried before a pick is dropped for length
MODES = ("v1", "v2")
HOSTS = ("claude", "codex")
NONCE_ENV = "BOSSKU_HINT_NONCE"     # test only: the delivery canary asks the agent to quote this value back
_NONCE = re.compile(r"[A-Za-z0-9_.-]{1,40}")
EXPLICIT = "explicit skill request"
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
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."


def wants_resume(prompt: str) -> bool:
    """A short prompt that asks to go on ("continue", "lanjut", "bossku resume"); slash commands never do."""
    text = prompt.strip()
    return bool(text) and not text.startswith(("/", "!")) and len(text.split()) <= RESUME_MAX_WORDS \
        and RESUME_TRIGGER.search(text) is not None


def hint_mode(home: Path | None = None) -> str:
    """`hint_mode` from ~/.bosskuai/config.json: v1 (the default) or v2. A missing key or file, or any other value, is v1."""
    try:
        value = json.loads(user_config_path(home).read_text(encoding="utf-8")).get("hint_mode")
    except (OSError, ValueError, AttributeError):
        return "v1"
    return value if value in MODES else "v1"


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


def pick_skills(prompt: str, *, root: Path | None = None, mode: str = "v1", min_words: int = MIN_WORDS,
                data: dict | None = None) -> list[dict]:
    """The rows (skill_id, score, description, reason) the hint would name for this prompt; empty means silence.

    v1: the best match must score MIN_TOP_SCORE; up to V1_MAX_HINTS rows. v2: the same bar for the first pick,
    SECOND_MIN for each later one (they come from select_skill_stack, so each covers another part of the request),
    up to MAX_HINTS rows, and a skill the user names by id is let through below the bar.
    """
    prompt = prompt.strip()
    if len(prompt.split()) < min_words or prompt.startswith(("/", "!")):
        return []
    v2 = mode == "v2"
    data = skills._routing_index(root) if data is None else data
    top = skills.rank_skills(prompt, root, limit=1, data=data)
    gated = bool(top) and round(top[0][1], 3) >= MIN_TOP_SCORE    # no pick can score higher than the best-ranked skill
    if not gated and not (v2 and _mentions_a_skill(prompt.lower(), [*data.get("skills", {}), *data.get("aliases", {})])):
        return []
    rows = select_skill_stack(prompt, root, limit=MAX_HINTS if v2 else V1_MAX_HINTS + 1, data=data)["selected"]
    if not rows or (rows[0]["score"] < MIN_TOP_SCORE and not (v2 and rows[0]["reason"] == EXPLICIT)):
        return []
    picks = []
    for row in rows:
        if row["skill_id"] in NOT_INSTALLED or row["reason"].startswith("insufficient eligible evidence"):
            continue
        if not (v2 and row["reason"] == EXPLICIT):    # a skill the user named is not held to a score
            if v2 and not gated:                      # under the bar only a named skill speaks
                continue
            if row["score"] < (SECOND_MIN if v2 and picks else MIN_SCORE):
                continue
        picks.append(row)
    return picks[:MAX_HINTS if v2 else V1_MAX_HINTS]


def _posix(path) -> str:
    return str(path).replace("\\", "/")


def _bossku_command() -> str:
    """The absolute `bossku` the footer names: forward slashes (Git Bash drops backslashes), quoted only for a space."""
    from bossku.hooks import resolve_bossku_argv

    exe, *rest = resolve_bossku_argv()
    exe = _posix(exe)
    return " ".join([f'"{exe}"' if " " in exe else exe, *rest])


def render_hint(picks: list[dict], *, root: Path | None = None, home: Path | None = None, host: str = "claude",
                mode: str = "v1") -> str:
    """The hint text. Claude on v1 keeps its original wording. Every other case says how to load each skill: the
    Skill tool for a skill Claude lists, otherwise `Read <absolute SKILL.md>` (Codex has no Skill tool), and a
    footer with the absolute `bossku skills show` for a read that is refused."""
    located = [(row, *locate_skill(row["skill_id"], root, home)) for row in picks]
    if mode == "v1" and host == "claude":
        lines = []
        for row, kind, _ in located:
            how = "Skill tool" if kind == "listed" else f"`bossku skills show {row['skill_id']}`"
            lines.append(f"- {row['skill_id']}: {_short(row['description'])} (load with {how})")
        return ("BosskuAI skill hint: these skills match this request. Load the best fit before you start "
                "(both only if they cover different parts):\n"
                + "\n".join(lines)
                + "\nSkip only if the task is trivial or neither fits.")
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
    # ponytail: a single pick is never cut, so a very long home path can still pass HINT_CHARS.
    count, limit = len(located), DESCRIPTION_CHARS
    if len(text(count, limit)) > HINT_CHARS:
        limit = SHORT_DESCRIPTION_CHARS
        while count > 1 and len(text(count, limit)) > HINT_CHARS:
            count -= 1
    return text(count, limit)


def build_hint(prompt: str, *, root: Path | None = None, home: Path | None = None, host: str = "claude",
               mode: str = "v1") -> str | None:
    """The suggestion for this prompt, or None when there is nothing worth saying."""
    picks = pick_skills(prompt, root=root, mode=mode)
    if not picks:
        return None
    text = render_hint(picks, root=root, home=home, host=host, mode=mode)
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
        hint = build_hint(prompt, root=root, home=home, host=host, mode=hint_mode(home))
    except Exception:  # noqa: BLE001 - a hint is a convenience; it must never break the user's prompt
        hint = None
    finally:
        skills._routing_index = original
        bossku_index.compute_idf = idf_original
    parts = [hint] if hint else []
    project = os.environ.get("CLAUDE_PROJECT_DIR") or (cwd if isinstance(cwd, str) else "")
    if states_rule(prompt):
        parts.append(prompt_reminder(project))
    if not parts:
        return {}
    return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "\n".join(parts)}}
