"""A stop gate: an agent that changed code must run it, and an agent that was asked for a change must make one.

Instructions that say "verify before you finish" work on strong models and are ignored by small ones, which
write a file in one shot and stop, or paste the code into the chat and never touch a file. This `Stop` hook
reads the session transcript and, once per turn for each case, sends the agent back to work when it
  - edited source files and ran nothing afterwards, or
  - was asked to change something, edited no file, and ended with code in its reply.
Each reminder is counted from the transcript itself, so the agent can never be held in a loop. The hook only
reads; it never runs code, and it stays silent for questions, reviews, documentation edits and runs that did
their job.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from bossku.rules import states_rule, stop_reminder

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
LIMITS = {"verify": 1, "paste": 1, "rule": 1}
MARKERS = {"verify": "BosskuAI verify gate: you ", "paste": "BosskuAI verify gate: the request",
           "rule": "BosskuAI memory gate: "}

VERIFY_REASON = (
    "BosskuAI verify gate: you changed code but have not run anything yet. Do not describe a test or its result: "
    "call the Bash tool now and run the project's tests, or one short script that checks each requirement in the "
    "request and its edge cases (only what is safe to run locally). Read the real output, fix what fails, then "
    "say what you ran and what you could not verify."
)
PASTE_REASON = (
    "BosskuAI verify gate: the request asks for a change, but you edited no file and your reply only shows code. "
    "Do not paste code: call your edit tool now to write the change into the project files, then run it (or the "
    "project's tests), fix what fails, and say what you ran. If the request was only a question, say so and finish."
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
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(str(b.get("text", "")) for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


# Lines the app writes as "user" turns that no person typed: they must not replace the request being judged.
_NOT_TYPED = ("<ci-monitor-event>", "<task-notification>", "<local-command", "<system-reminder>")


def _typed_by_a_person(event: dict) -> bool:
    origin = event.get("origin")
    if isinstance(origin, dict) and origin.get("kind") not in (None, "human"):
        return False
    return not event.get("isCompactSummary")


def _prompt_text(event: dict) -> str:
    """The text of a prompt the user typed; empty for tool results, for context the hooks added and for app events."""
    if event.get("type") != "user" or event.get("isMeta") or event.get("isSidechain") or not _typed_by_a_person(event):
        return ""
    text = _text_of(event)
    return "" if text.lstrip().startswith(_NOT_TYPED) else text


def _typed_while_working(event: dict) -> str:
    """A message the user sent while the agent was busy is stored as a queued command, not as a user turn."""
    attachment = event.get("attachment")
    origin = event.get("origin")
    if (isinstance(attachment, dict) and attachment.get("type") == "queued_command"
            and isinstance(origin, dict) and origin.get("kind") == "human"
            and not event.get("isSidechain") and isinstance(attachment.get("prompt"), str)):
        return "" if attachment["prompt"].lstrip().startswith(_NOT_TYPED) else attachment["prompt"]
    return ""


def _tool_calls(lines):
    for event in _events(lines):
        message = event.get("message")
        if not isinstance(message, dict) or event.get("type") != "assistant" or event.get("isSidechain"):
            continue
        content = message.get("content")
        for block in content if isinstance(content, list) else []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield _call_of(block)


def _call_of(block: dict) -> tuple[str, dict]:
    """(tool name, arguments) with both forced to the expected types, whatever the transcript holds."""
    args = block.get("input")
    return str(block.get("name") or ""), args if isinstance(args, dict) else {}


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
        queued = _typed_while_working(event)
        if queued.strip():
            turn.request += "\n" + queued   # said mid-turn: it belongs to the turn that is running
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
                turn.calls.append(_call_of(block))
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


# A real save: `bossku remember ...` (also bossku.exe or a path to it), not a search for the text and not the placeholder.
SAVES_A_NOTE = re.compile(r"(?:^|[\s;&|(`'\"/\\])bossku(?:\.exe)?['\"]?\s+remember\b", re.IGNORECASE)
READS_ONLY = re.compile(r"^\s*(?:grep|egrep|rg|cat|echo|printf|head|tail|less|more|type|findstr|ls|dir)\b", re.IGNORECASE)
PLACEHOLDER = "<the rule as the user stated it"


def _saved_a_note(calls) -> bool:
    for name, args in calls:
        command = str(args.get("command", ""))
        if (name in SHELL_TOOLS and SAVES_A_NOTE.search(command) and PLACEHOLDER not in command
                and not READS_ONLY.search(command)):
            return True
    return False


def decide(transcript_lines, project: str = "") -> tuple[str, str] | None:
    """The reminder to send now as (kind, reason), or None to let the agent finish."""
    turn = _scan(transcript_lines)
    unverified = _unverified(turn.calls)
    if unverified and turn.blocks["verify"] < LIMITS["verify"]:
        return "verify", VERIFY_REASON
    if not unverified and turn.blocks["paste"] < LIMITS["paste"] and _pasted(turn.request, turn.calls, turn.reply):
        return "paste", PASTE_REASON
    # A verify reminder that was sent but could not be met (a stylesheet has nothing to run) must not hide the rule one.
    verify_settled = not unverified or turn.blocks["verify"] >= LIMITS["verify"]
    if (verify_settled and turn.blocks["rule"] < LIMITS["rule"] and states_rule(turn.request)
            and not _saved_a_note(turn.calls)):
        return "rule", stop_reminder(project)
    return None


def gate_output(payload_text: str) -> dict:
    """What a Claude Code `Stop` hook prints: nothing to let the agent finish, or a block with the reason."""
    if os.environ.get("BOSSKU_VERIFY_GATE", "1") == "0":
        return {}
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
        if not isinstance(payload, dict):
            return {}
        path = payload.get("transcript_path")
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines() if isinstance(path, str) and path else []
        if payload.get("stop_hook_active") and sum(_scan(lines).blocks.values()) == 0:
            return {}   # a reminder was already sent but the transcript does not show it: never risk a loop
        cwd = payload.get("cwd")
        project = os.environ.get("CLAUDE_PROJECT_DIR") or (cwd if isinstance(cwd, str) else "")
        decision = decide(lines, project)
    except Exception:  # noqa: BLE001 - a reminder is a convenience: whatever goes wrong, let the agent finish
        return {}
    return {"decision": "block", "reason": decision[1]} if decision else {}
