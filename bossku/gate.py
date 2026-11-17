"""A stop gate: an agent that changed code must run it, and an agent that was asked for a change must make one.

Instructions that say "verify before you finish" work on strong models and are ignored by small ones, which
write a file in one shot and stop, or paste the code into the chat and never touch a file. This `Stop` hook
reads the session transcript and, once per turn for each case, sends the agent back to work when it
  - edited source files and ran nothing afterwards, or
  - was asked to change something, edited no file, and ended with code in its reply, or
  - changed code, a dependency manifest or infra config and ended without a `Security gate:` verdict line
    (the security gate is a must rule, see bossku/security.py).
Each reminder is counted from the transcript itself, so the agent can never be held in a loop. The hook only
reads; it never runs code, and it stays silent for questions, reviews, documentation edits and runs that did
their job.
"""

from __future__ import annotations

import bisect
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from bossku.rules import states_rule, stop_reminder
from bossku.security import VERDICT, is_security_relevant
from bossku.security import is_off as security_off

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
    r"|(?:bash|sh|zsh)\s+[^\s|;&]+\.sh\b"   # as hooks/stop-gate.mjs: a shell script counts
    r"|npx\s+\S+|go\s+(?:test|run|build|vet)\b|cargo\s+(?:test|run|build|check|clippy)\b"
    r"|dotnet\s+(?:test|run|build)\b|(?:mvn|mvnw|gradle|gradlew)\b.{0,400}?\b(?:test|verify|build|check)\b"
    r"|make\s+(?:-\S+\s+)*(?:test|tests|check|build|all|run|lint|verify)\b|swift\s+(?:test|run|build)\b|flutter\s+test\b|bundle\s+exec\b|deno\s+test\b"
    r")", re.I)
# A path-qualified or quoted interpreter, only as the command word (`git add src/python docs` runs nothing).
RUNS_PATH = re.compile(
    r"""^\s*(?:\w+=\S*\s+)*(?:timeout\s+\S+\s+)?(?:"[^"]*[\\/]|'[^']*[\\/]|[^\s=]*[\\/])(?:python3?|py|node|deno|bun|ruby|php|perl|lua|Rscript|julia)(?:\.exe)?["']?\s+"""
    r"(?!--version|-V\b|-h\b|--help)\S", re.I)
# A ./script.sh or ./script.py, only as the command word (`chmod +x ./run.sh` and `git add ./check.py` run nothing):
# after shell keywords and plain wrappers (`if ./check.sh`, `sudo ./x.sh`), NAME=value assignments and `timeout N`.
RUNS_SCRIPT = re.compile(r"^\s*(?:(?:then|do|else|elif|if|while|until|!|\{|sudo|time|env|exec|nohup|command)\s+)*"
                         r"(?:\w+=\S*\s+)*(?:timeout\s+\S+\s+)?\./[\w./-]+\.(?:sh|py)\b", re.I)
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
LIMITS = {"verify": 1, "paste": 1, "security": 1, "rule": 1}
MARKERS = {"verify": "BosskuAI verify gate: you ", "paste": "BosskuAI verify gate: the request",
           "security": "BosskuAI security gate: ", "rule": "BosskuAI memory gate: "}
STYLE_SUFFIXES = {".css", ".scss", ".sass", ".less"}   # no trust boundary in a stylesheet

VERIFY_REASON = (
    "BosskuAI verify gate: you changed code but have not run anything yet. Do not describe a test or its result: "
    "call the Bash tool now and run the project's tests, or one short script that checks each requirement in the "
    "request and its edge cases (only what is safe to run locally). Read the real output, fix what fails, then "
    "say what you ran and what you could not verify."
)
FAILED_REASON = (
    "BosskuAI verify gate: you ran `{command}` after your last change and it failed. Read the error it printed, fix "
    "the cause, run it again until it passes, then say what you ran. If it cannot pass here, say exactly why."
)
SECURITY_REASON = (
    "BosskuAI security gate: you changed code, dependencies or infra config and the reply has no security verdict "
    "(a must rule). Load bosskuai-security-gate and run its pass on this change: each layer it touches, deep pass for "
    "auth, payments, tenant data, secrets, uploads, public endpoints, infra/CI or agent tools. If a dependency file "
    "changed, check the changed packages against live feeds (OSV.dev, GitHub Advisories, CISA KEV). Then end the "
    "reply with `Security gate: PASS | BLOCK | PROVISIONAL`, listing only High and Critical findings."
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
    errors: dict = field(default_factory=dict)
    reply: str = ""
    cwd: str = ""   # the session folder, as the last main-thread line records it
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
_NOT_TYPED = ("<ci-monitor-event>", "<task-notification>", "<agent-message", "<local-command", "<system-reminder>")


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


class _Call(tuple):
    """(tool name, arguments), as the rest of this module unpacks it, that also knows its tool_use id and timestamp."""

    def __new__(cls, name: str, args: dict, id: str = "", timestamp: str = ""):
        call = super().__new__(cls, (name, args))
        call.id, call.timestamp = id, timestamp
        return call


# An error result that says the command never ran (denied by the auto-mode classifier, a permission rule, a hook or the
# user, or aborted or interrupted first) is not a failed check. Same list as NOT_RUN_RE in hooks/stop-gate.mjs; any other
# error text stays a failure.
NOT_RUN = re.compile(
    r"^\s*(?:<error>)?(?:Permission (?:for this (?:action|command) (?:was|has been) denied|to use )"
    r"|The user doesn't want to proceed with this tool use|Command was aborted before completion"
    r"|\[Request interrupted by user|\[Tool call interrupted: |PreToolUse:\S+ hook error: [^\n]{0,60}? denied"
    r"|The server-side auto mode classifier gave no verdict|<tool_use_error>Blocked: |This agent is isolated in the worktree)")


def _result_state(block: dict):
    """False for a result that came back fine, True for an error, "not_run" for an error that says the command never ran."""
    if block.get("is_error") is not True:
        return False
    content = block.get("content")
    text = content if isinstance(content, str) else "\n".join(
        str(b.get("text", "")) for b in content if isinstance(b, dict)) if isinstance(content, list) else ""
    return "not_run" if NOT_RUN.search(text[:500]) else True


def _results(event: dict) -> dict:
    """{tool_use id: False (ok), True (error) or "not_run"} for the tool_result blocks of one user line."""
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) and event.get("type") == "user" else None
    if not isinstance(content, list):
        return {}
    return {str(b["tool_use_id"]): _result_state(b) for b in content
            if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id")}


def _tool_calls(lines):
    """(calls, errors): every tool call of the main thread, and {tool_use id: errored} for the results that came back."""
    calls, errors = [], {}
    for event in _events(lines):
        errors.update(_results(event))
        message = event.get("message")
        if not isinstance(message, dict) or event.get("type") != "assistant" or event.get("isSidechain"):
            continue
        content = message.get("content")
        for block in content if isinstance(content, list) else []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                calls.append(_call_of(block, event))
    return calls, errors


def _call_of(block: dict, event: dict | None = None) -> _Call:
    """The call with name and arguments forced to the expected types, whatever the transcript holds."""
    args = block.get("input")
    return _Call(str(block.get("name") or ""), args if isinstance(args, dict) else {},
                 str(block.get("id") or ""), str((event or {}).get("timestamp") or ""))


def _spellings(path: str) -> set[str]:
    """The plain and the link-resolved spelling of a path (a temp folder is often an 8.3 short name), case-folded on Windows."""
    plain = os.path.abspath(path)
    return {os.path.normcase(plain), os.path.normcase(os.path.realpath(plain))}


def _within(path: str, folder: str) -> bool:
    """True when `path` is `folder` or inside it, under any spelling of either."""
    return any(here == there or here.startswith(there.rstrip(os.sep) + os.sep)
               for here in _spellings(path) for there in _spellings(folder))


def _outside_project(target: str, project: str = "") -> bool:
    """True for an absolute path in ~/.claude (hooks, settings) or the OS temp folder (scratch files): not source
    edits. The same rule as `isScratch` in hooks/_lib.mjs, which the Node stop gate uses: a root is skipped unless the
    session's project folder is that root or inside it, so a benchmark workspace in the temp folder is still gated
    (including its sibling folders), and a session started in the home folder skips both roots. A relative path is
    taken to be in the project."""
    if not os.path.isabs(target):
        return False
    import tempfile   # not at module scope: bossku.cli imports this module on every hook run
    roots = [tempfile.gettempdir()]
    try:
        roots.append(str(Path.home() / ".claude"))
    except RuntimeError:   # no home directory can be found: only the temp folder is skipped
        pass
    here = project if project and os.path.isabs(project) else ""
    return any(_within(target, root) and not (here and _within(here, root)) for root in roots)


def _is_code_edit(name: str, args: dict, project: str = "") -> bool:
    if name not in EDIT_TOOLS:
        return False
    target = str(args.get("file_path") or args.get("path") or args.get("notebook_path") or "")
    if not target:
        return True   # an unnamed patch: assume it touched code
    return Path(target).suffix.lower() not in NON_CODE_SUFFIXES and not _outside_project(target, project)


def _is_check(name: str, args: dict) -> bool:
    """A shell command with a segment that runs code or a test runner; `cat pytest.ini` and `echo pytest` run nothing."""
    return name in SHELL_TOOLS and any((RUNS_CODE.search(part) or RUNS_PATH.search(part) or RUNS_SCRIPT.search(part))
                                       and not READS_ONLY.search(part)
                                       for part in _command_segments(str(args.get("command", "")), name == "PowerShell"))


def _verification(calls, project: str = "", errors: dict | None = None) -> tuple[str, str]:
    """(state, command): `no_code_change`, `unverified` (nothing ran after the last code edit), `failed_verification`
    (the last check after it came back as an error; the command is named) or `verified`. A check with no result in the
    transcript counts as passed, so a transcript shape this code does not know can never trap a session."""
    last_edit, checks = None, []
    for index, call in enumerate(calls):
        name, args = call
        if _is_code_edit(name, args, project):
            last_edit, checks = index, []
        elif last_edit is not None and _is_check(name, args):
            checks.append(call)
    if last_edit is None:
        return "no_code_change", ""
    errors = errors or {}
    # A denied or aborted check did not run: the last one that did decides.
    ran = [call for call in checks if errors.get(getattr(call, "id", "")) != "not_run"]
    if not ran:
        return "unverified", ""
    if errors.get(getattr(ran[-1], "id", "")):
        return "failed_verification", " ".join(str(ran[-1][1].get("command", "")).split())
    return "verified", ""


def _unverified(calls, project: str = "", errors: dict | None = None) -> bool:
    """True when code was edited and no command that runs code followed the last edit, or the last one failed."""
    return _verification(calls, project, errors)[0] in ("unverified", "failed_verification")


def _needs_security(calls, project: str = "") -> bool:
    """True when a code file (not a stylesheet), a dependency manifest or an infra/CI/agent config file was edited."""
    for name, args in calls:
        if name not in EDIT_TOOLS:
            continue
        target = str(args.get("file_path") or args.get("path") or args.get("notebook_path") or "")
        if not target or _outside_project(target, project):
            continue
        if is_security_relevant(target) or (_is_code_edit(name, args, project)
                                            and Path(target).suffix.lower() not in STYLE_SUFFIXES):
            return True
    return False


def _pasted(request: str, calls, reply: str) -> bool:
    """True when the request asks for a change, no file was edited, and the reply ends with a code block."""
    if not CHANGE_REQUEST.search(request) or "```" not in reply:
        return False
    if any(name in EDIT_TOOLS for name, _ in calls):
        return False
    return not any(name in SHELL_TOOLS and WRITES_FILES.search(str(args.get("command", ""))) for name, args in calls)


def _scan(lines) -> Turn:
    """Read a transcript once: the latest prompt, what the agent did since, and which reminders it already got."""
    turn, cwd = Turn(), ""
    for event in _events(lines):
        turn.errors.update(_results(event))
        if isinstance(event.get("cwd"), str) and event["cwd"] and not event.get("isSidechain"):
            cwd = event["cwd"]
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
                turn.calls.append(_call_of(block, event))
            elif block.get("type") == "text" and str(block.get("text", "")).strip():
                turn.reply = str(block["text"])
    turn.cwd = cwd
    return turn


def needs_verification(transcript_lines, project: str = "") -> bool:
    """True when code was edited anywhere in the session and no command that runs code followed the last edit."""
    calls, errors = _tool_calls(transcript_lines)
    return _unverified(calls, project, errors)


def shows_code_without_editing(transcript_lines) -> bool:
    """True when this turn's request asks for a change, no file was edited, and the reply ends with a code block."""
    turn = _scan(transcript_lines)
    return _pasted(turn.request, turn.calls, turn.reply)


# A real save: `bossku remember ...` (also bossku.exe or a path to it), not a search for the text and not the placeholder.
SAVES_A_NOTE = re.compile(r"(?:^|[\s;&|(`'\"/\\])bossku(?:\.exe)?['\"]?\s+remember\b", re.IGNORECASE)
READS_ONLY = re.compile(r"^\s*(?:(?:sudo|command)\s+)?(?:\S*[\\/])?(?:(?:git\s+grep|grep|egrep|rg|cat|echo|printf|head|tail"
                        r"|less|more|type|findstr|ls|dir|wc|stat|which|where|gc|gci|sls|write-output|write-host"
                        r"|get-content|get-childitem|select-string)(?:\.exe)?(?![\w.-])|sed\s+-n\b)", re.IGNORECASE)
PLACEHOLDER = "<the rule as the user stated it"


def _segments(command: str) -> list[str]:
    """The simple commands of a shell line, split on && || ; | and parentheses. Quotes keep their contents together,
    and posix=False leaves Windows backslashes alone. A line shlex cannot read is judged whole."""
    import shlex   # not at module scope: bossku.cli imports this module, so every hook run would pay for it
    lexer = shlex.shlex(command, posix=False, punctuation_chars=True)
    lexer.whitespace_split, lexer.commenters = True, ""
    try:
        tokens = list(lexer)
    except ValueError:
        return [command]
    segments, current = [], []
    for token in tokens:
        if set(token) <= set(";&|()"):
            segments.append(" ".join(current))
            current = []
        else:
            current.append(token)
    return segments + [" ".join(current)]


def _command_segments(command: str, powershell: bool = False) -> list[str]:
    """The simple commands of a shell command, cut in one pass so quotes decide what a line break means: a newline,
    ; & | and parentheses end a command only outside quotes (a backslash escapes the next character outside single
    quotes; in a PowerShell command a backtick does and a backslash is plain), `$(...)` inside double quotes is a
    command of its own, a # at the start of a word outside quotes starts a comment, and heredoc body lines are skipped
    (the line that opens one decides, so `python - <<EOF` counts and `cat > f <<EOF` does not)."""
    esc = "`" if powershell else "\\"
    out, cur, stack, pending, i = [], [], [], [], 0
    escaped = False   # the last character in `cur` was escaped, so an escaped space does not end a word
    lines = None      # trimmed line -> start offsets, built once on the first heredoc
    while i < len(command):
        ch, top = command[i], stack[-1] if stack else ""
        if ch == esc and top != "'":
            # A line continuation after a word break leaves the next line at a word start, so its # is a comment.
            at_word_start = not cur or (cur[-1][-1].isspace() and not escaped)
            cur.append(command[i:i + 2])
            escaped = not (command[i + 1:i + 2] == "\n" and at_word_start)
            i += 2
            continue
        if top == "'":
            if ch == "'":
                stack.pop()
        elif top == '"':
            if ch == '"':
                stack.pop()
            elif command.startswith("$(", i):
                out.append("".join(cur))
                cur, i = [], i + 2
                stack.append("$(")
                continue
        elif ch == "#" and (not cur or (cur[-1][-1].isspace() and not escaped)):
            end = command.find("\n", i)
            i = len(command) if end < 0 else end
            continue
        elif ch in "'\"":
            stack.append(ch)
        elif ch == ")" and top == "$(":
            stack.pop()
            out.append("".join(cur))
            cur = []
            i += 1
            continue
        elif command.startswith("<<", i) and not command.startswith("<<<", i):
            found = re.compile(r"<<-?\s*(['\"]?)([\w.-]+)\1").match(command, i)
            if found:
                pending.append(found.group(2))
        elif ch in ";&|()\n":
            out.append("".join(cur))
            cur = []
            i += 1
            if ch == "\n" and pending:   # skip the body, and the line with the delimiter
                delim = pending.pop(0)
                if lines is None:
                    lines, pos = {}, 0
                    while pos <= len(command):
                        end = command.find("\n", pos)
                        end = len(command) if end < 0 else end
                        lines.setdefault(command[pos:end].strip(), []).append(pos)
                        pos = end + 1
                # No delimiter line means it was no heredoc (`$((1<<2))`): nothing is skipped.
                starts = lines.get(delim, [])
                at = bisect.bisect_left(starts, i)
                if at < len(starts):
                    end = command.find("\n", starts[at])
                    i = len(command) if end < 0 else end + 1
            continue
        escaped = False
        cur.append(ch)
        i += 1
    return out + ["".join(cur)]


def _saved_a_note(calls) -> bool:
    for name, args in calls:
        command = str(args.get("command", ""))
        if name in SHELL_TOOLS and SAVES_A_NOTE.search(command) and PLACEHOLDER not in command:
            # `grep x && bossku remember ...` still saves: read-only is judged per command, not per line.
            if any(SAVES_A_NOTE.search(part) and not READS_ONLY.search(part) for part in _segments(command)):
                return True
    return False


def decide(transcript_lines, project: str = "") -> tuple[str, str] | None:
    """The reminder to send now as (kind, reason), or None to let the agent finish."""
    turn = _scan(transcript_lines)
    state, failed = _verification(turn.calls, project, turn.errors)
    unverified = state in ("unverified", "failed_verification")
    if unverified and turn.blocks["verify"] < LIMITS["verify"]:
        if state == "failed_verification":
            from bossku.redact import redact_command   # not at module scope: only a failed check needs it
            return "verify", FAILED_REASON.format(command=redact_command(failed[:2000])[:200])   # cut first: masking a huge command is slow
        return "verify", VERIFY_REASON
    if not unverified and turn.blocks["paste"] < LIMITS["paste"] and _pasted(turn.request, turn.calls, turn.reply):
        return "paste", PASTE_REASON
    # A verify reminder that was sent but could not be met (a stylesheet has nothing to run) must not hide the rule one.
    verify_settled = not unverified or turn.blocks["verify"] >= LIMITS["verify"]
    if (verify_settled and turn.blocks["security"] < LIMITS["security"] and not security_off()
            and not VERDICT.search(turn.reply) and _needs_security(turn.calls, project)):
        return "security", SECURITY_REASON
    if (verify_settled and turn.blocks["rule"] < LIMITS["rule"] and states_rule(turn.request)
            and not _saved_a_note(turn.calls)):
        return "rule", stop_reminder(project)
    return None


def _is_prompt_line(line: str) -> bool:
    return any(_prompt_text(event).strip() for event in _events([line]))


def _lines_of(data: bytes) -> list[str]:
    """Split on LF only, as hooks/stop-gate.mjs does: JSON.stringify leaves a raw U+2028 inside a line."""
    text = data.decode("utf-8", errors="replace")
    return [line.removesuffix("\r") for line in text.split("\n")] if text else []


def _turn_lines(path: str, block: int = 1 << 19) -> list[str]:
    """The transcript lines, cut at the user's latest prompt when that prompt is in the last `block` bytes (`_scan` drops
    everything before it). A turn longer than one block gains nothing from searching on, since each pass would parse the
    same lines again, so then the whole file is read, as before."""
    with open(path, "rb") as fh:
        size = fh.seek(0, os.SEEK_END)
        if size > block:
            fh.seek(size - block)
            tail = fh.read()
            cut = tail.find(b"\n")   # begin on a line start, so no line is cut in two
            lines = _lines_of(tail[cut + 1:]) if cut >= 0 else []
            for i in range(len(lines) - 1, -1, -1):
                if _is_prompt_line(lines[i]):
                    return lines[i:]
        fh.seek(0)
        return _lines_of(fh.read())


def gate_output(payload_text: str) -> dict:
    """What a Claude Code `Stop` hook prints: nothing to let the agent finish, or a block with the reason."""
    if os.environ.get("BOSSKU_VERIFY_GATE", "1") == "0":
        return {}
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
        if not isinstance(payload, dict):
            return {}
        path = payload.get("transcript_path")
        lines = _turn_lines(path) if isinstance(path, str) and path else []
        if payload.get("stop_hook_active") and sum(_scan(lines).blocks.values()) == 0:
            return {}   # a reminder was already sent but the transcript does not show it: never risk a loop
        cwd = payload.get("cwd")
        project = os.environ.get("CLAUDE_PROJECT_DIR") or (cwd if isinstance(cwd, str) else "")
        decision = decide(lines, project)
    except Exception:  # noqa: BLE001 - a reminder is a convenience: whatever goes wrong, let the agent finish
        return {}
    return {"decision": "block", "reason": decision[1]} if decision else {}
