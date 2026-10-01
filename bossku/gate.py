"""A stop gate: an agent that changed code must run it, and an agent that was asked for a change must make one.

Instructions that say "verify before you finish" work on strong models and are ignored by small ones, which
write a file in one shot and stop, or paste the code into the chat and never touch a file. This `Stop` hook
reads the session transcript and, once per turn, sends the agent back to work when it
  - edited source files and ran nothing afterwards, or
  - was asked to change something, edited no file, and ended with code in its reply.
It only reads; it never runs code itself, and it stays silent for questions, reviews, documentation edits and
runs that did their job.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

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

BLOCK_REASON = (
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


def _events(lines):
    for line in lines:
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(event, dict):
            yield event


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


def needs_verification(transcript_lines) -> bool:
    """True when code was edited and no command that runs code followed the last edit."""
    last_edit = None
    verified_after = False
    for index, (name, args) in enumerate(_tool_calls(transcript_lines)):
        if _is_code_edit(name, args):
            last_edit, verified_after = index, False
        elif name in SHELL_TOOLS and last_edit is not None and RUNS_CODE.search(str(args.get("command", ""))):
            verified_after = True
    return last_edit is not None and not verified_after


def _prompt_text(event: dict) -> str:
    """The text of a prompt the user typed; empty for tool results and for context the hooks added."""
    if event.get("type") != "user" or event.get("isMeta") or event.get("isSidechain"):
        return ""
    content = (event.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(str(b.get("text", "")) for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def shows_code_without_editing(transcript_lines) -> bool:
    """True when this turn's request asks for a change, no file was edited, and the reply ends with a code block."""
    request, calls, reply = "", [], ""
    for event in _events(transcript_lines):
        text = _prompt_text(event)
        if text.strip():
            request, calls, reply = text, [], ""   # a new turn: only what follows it counts
            continue
        message = event.get("message")
        if event.get("type") != "assistant" or event.get("isSidechain") or not isinstance(message, dict):
            continue
        for block in message.get("content") if isinstance(message.get("content"), list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                calls.append((block.get("name", ""), block.get("input") or {}))
            elif block.get("type") == "text" and str(block.get("text", "")).strip():
                reply = str(block["text"])
    if not CHANGE_REQUEST.search(request) or "```" not in reply:
        return False
    if any(name in EDIT_TOOLS for name, _ in calls):
        return False
    return not any(name in SHELL_TOOLS and WRITES_FILES.search(str(args.get("command", ""))) for name, args in calls)


def gate_output(payload_text: str) -> dict:
    """What a Claude Code `Stop` hook prints: nothing to let the agent finish, or a block with the reason."""
    if os.environ.get("BOSSKU_VERIFY_GATE", "1") == "0":
        return {}
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict) or payload.get("stop_hook_active"):
        return {}   # already sent back once this turn: never loop
    path = payload.get("transcript_path")
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines() if path else []
    except OSError:
        return {}   # no transcript to judge by: fail open
    if needs_verification(lines):
        return {"decision": "block", "reason": BLOCK_REASON}
    if shows_code_without_editing(lines):
        return {"decision": "block", "reason": PASTE_REASON}
    return {}
