"""A stop gate: an agent that changed code must run it, and an agent that was asked for a change must make one.

Instructions that say "verify before you finish" work on strong models and are ignored by small ones, which
write a file in one shot and stop, or paste the code into the chat and never touch a file. This `Stop` hook
reads the session transcript and sends the agent back to work when it
  - edited source files and ran nothing afterwards (once),
  - was asked to change something, edited no file, and ended with code in its reply (once), or
  - changed and ran its code but never checked the result against each requirement of a long request (once,
    only when asked to: `--audit`).
Each kind of reminder is limited and counted from the transcript itself, so the agent can never be held in a
loop. The hook only reads; it never runs code, and it stays silent for questions, reviews, documentation edits
and runs that did their job.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from bossku.spec import audit_reason, extract_requirements

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "apply_patch", "str_replace_editor", "create_file"}
SHELL_TOOLS = {"Bash", "PowerShell", "shell", "run_terminal_cmd"}
# Prose and config are not behavior: editing only these does not call for running anything.
NON_CODE_SUFFIXES = {".md", ".markdown", ".txt", ".rst", ".adoc", ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg",
                     ".lock", ".gitignore", ".csv", ".svg", ".png", ".jpg"}
# A command that executes code or a test runner, as opposed to one that only reads files.
RUNS_CODE = re.compile(
    r"(?:^|[\s;&|(`])(?:"
    r"(?:python3?|py|node|deno|bun|ruby|php|perl|lua|Rscript|julia)(?:\.exe)?\s+(?!--version|-V\b|-h\b|--help)\S"
    r"|(?:pytest|py\.test|tox|nox|jest|vitest|mocha|phpunit|pest|rspec|ctest|behave)\b"
    r"|(?:npm|yarn|pnpm)\s+(?:run\s+)?(?:test|t|start|build|lint|check|dev)\b"
    r"|npx\s+\S+|go\s+(?:test|run|build|vet)\b|cargo\s+(?:test|run|build|check|clippy)\b"
    r"|dotnet\s+(?:test|run|build)\b|(?:mvn|mvnw|gradle|gradlew)\b.*\b(?:test|verify|build|check)\b"
    r"|make\s+(?:-\S+\s+)*(?:test|tests|check|build|all|run|lint|verify)\b|swift\s+(?:test|run|build)\b|flutter\s+test\b|bundle\s+exec\b|deno\s+test\b"
    r")", re.I)
# The request asks for something to be changed or made (as opposed to explained or reviewed).
CHANGE_REQUEST = re.compile(
    r"\b(?:fix|implement|add|write|create|build|refactor|update|change|modify|patch|rename|remove|convert|migrate|extend|make)\b",
    re.I)
# A shell command that can write a file: redirection, tee, in-place edits, patches, moves and copies.
WRITES_FILES = re.compile(r"(?<![<>=!\-])>>?\s*[^\s&|>]|\btee\b|\bsed\s+-\w*i|\bperl\s+-\w*i|\bgit\s+apply\b|\bpatch\b|\b(?:mv|cp|touch)\s",
                          re.I)

# How often each reminder may be sent in one turn, and the text that marks it in the transcript. A second
# "run it now" reminder was tried on a small model: it answered with invented tool names, looped for 30+ turns and
# passed no more often, so each kind is sent once.
LIMITS = {"verify": 1, "paste": 1, "audit": 1}
MARKERS = {"verify": "BosskuAI verify gate: you ", "paste": "BosskuAI verify gate: the request",
           "audit": "BosskuAI requirement audit:"}
AUDIT_MIN_ITEMS = 5

VERIFY_REASON = (
    "BosskuAI verify gate: you changed code but ran nothing afterwards. Before you finish, run the project's "
    "tests, or write and run a quick check that covers each requirement in the request and its edge cases "
    "(run only what is safe to run locally). Fix whatever fails, then finish by saying what you ran and what "
    "you could not verify."
)
PASTE_REASON = (
    "BosskuAI verify gate: the request asks for a change, but you edited no file and your reply only shows code. "
    "Write the change into the project files with your edit tools, run it (or the project's tests), fix what "
    "fails, then say what you ran. If the request was only a question, say so and finish."
)


@dataclass
class Turn:
    """What happened since the user's latest prompt."""
    request: str = ""
    calls: list = field(default_factory=list)
    reply: str = ""
    blocks: dict = field(default_factory=lambda: {kind: 0 for kind in MARKERS})


def _events(lines):
    for line in lines:
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(event, dict):
            yield event


def _text_of(event: dict) -> str:
    content = (event.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(str(b.get("text", "")) for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _prompt_text(event: dict) -> str:
    """The text of a prompt the user typed; empty for tool results and for context the hooks added."""
    if event.get("type") != "user" or event.get("isMeta") or event.get("isSidechain"):
        return ""
    return _text_of(event)


def _tool_calls(lines):
    for event in _events(lines):
        message = event.get("message")
        if not isinstance(message, dict) or event.get("type") != "assistant" or event.get("isSidechain"):
            continue
        content = message.get("content")
        for block in content if isinstance(content, list) else []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name", ""), block.get("input") or {}


def _is_code_edit(name: str, args: dict) -> bool:
    if name not in EDIT_TOOLS:
        return False
    target = str(args.get("file_path") or args.get("path") or args.get("notebook_path") or "")
    if not target:
        return True   # an unnamed patch: assume it touched code
    return Path(target).suffix.lower() not in NON_CODE_SUFFIXES


def _unverified(calls) -> bool:
    """True when code was edited and no command that runs code followed the last edit."""
    last_edit = None
    verified_after = False
    for index, (name, args) in enumerate(calls):
        if _is_code_edit(name, args):
            last_edit, verified_after = index, False
        elif name in SHELL_TOOLS and last_edit is not None and RUNS_CODE.search(str(args.get("command", ""))):
            verified_after = True
    return last_edit is not None and not verified_after


def _pasted(request: str, calls, reply: str) -> bool:
    """True when the request asks for a change, no file was edited, and the reply ends with a code block."""
    if not CHANGE_REQUEST.search(request) or "```" not in reply:
        return False
    if any(name in EDIT_TOOLS for name, _ in calls):
        return False
    return not any(name in SHELL_TOOLS and WRITES_FILES.search(str(args.get("command", ""))) for name, args in calls)


def _scan(lines) -> Turn:
    """Read a transcript once: the latest prompt, what the agent did since, and which reminders it already got."""
    turn = Turn()
    for event in _events(lines):
        text = _prompt_text(event)
        if text.strip():
            turn = Turn(request=text)   # a new turn: only what follows it counts
            continue
        if event.get("type") == "user" and event.get("isMeta"):
            feedback = _text_of(event)
            for kind, marker in MARKERS.items():
                if marker in feedback:
                    turn.blocks[kind] += 1
            continue
        message = event.get("message")
        if event.get("type") != "assistant" or event.get("isSidechain") or not isinstance(message, dict):
            continue
        for block in message.get("content") if isinstance(message.get("content"), list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                turn.calls.append((block.get("name", ""), block.get("input") or {}))
            elif block.get("type") == "text" and str(block.get("text", "")).strip():
                turn.reply = str(block["text"])
    return turn


def needs_verification(transcript_lines) -> bool:
    """True when code was edited anywhere in the session and no command that runs code followed the last edit."""
    return _unverified(list(_tool_calls(transcript_lines)))


def shows_code_without_editing(transcript_lines) -> bool:
    """True when this turn's request asks for a change, no file was edited, and the reply ends with a code block."""
    turn = _scan(transcript_lines)
    return _pasted(turn.request, turn.calls, turn.reply)


def decide(transcript_lines, *, audit: bool = False) -> tuple[str, str] | None:
    """The reminder to send now as (kind, reason), or None to let the agent finish."""
    turn = _scan(transcript_lines)
    unverified = _unverified(turn.calls)
    if unverified and turn.blocks["verify"] < LIMITS["verify"]:
        return "verify", VERIFY_REASON
    if not unverified and turn.blocks["paste"] < LIMITS["paste"] and _pasted(turn.request, turn.calls, turn.reply):
        return "paste", PASTE_REASON
    if (audit and os.environ.get("BOSSKU_AUDIT", "1") != "0" and not unverified and turn.blocks["audit"] < LIMITS["audit"]
            and any(_is_code_edit(name, args) for name, args in turn.calls)):
        items = extract_requirements(turn.request)
        if len(items) >= AUDIT_MIN_ITEMS:
            return "audit", audit_reason(items)
    return None


def gate_output(payload_text: str, *, audit: bool = False) -> dict:
    """What a Claude Code `Stop` hook prints: nothing to let the agent finish, or a block with the reason."""
    if os.environ.get("BOSSKU_VERIFY_GATE", "1") == "0":
        return {}
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict):
        return {}
    path = payload.get("transcript_path")
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines() if path else []
    except OSError:
        return {}   # no transcript to judge by: fail open
    if payload.get("stop_hook_active") and sum(_scan(lines).blocks.values()) == 0:
        return {}   # a reminder was already sent but the transcript does not show it: never risk a loop
    decision = decide(lines, audit=audit)
    return {"decision": "block", "reason": decision[1]} if decision else {}
