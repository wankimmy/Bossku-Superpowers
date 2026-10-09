"""Pick up a Codex task in Claude Code after Codex stopped on its usage limit (phase 1 of cross-host resume).

Claude Code reads Codex's own files, read-only: the newest ~/.codex/state_*.sqlite lists the threads and their rollout
files. Nothing is installed in Codex and nothing is saved. A limit stop is a last `task_complete` record whose
`error.codex_error_info` is `usage_limit_exceeded`; a later `task_started` or a `turn_aborted` means it is not a stop.

Two small hooks use it. SessionStart adds one line when a stop is waiting in this folder. When the user then says
"continue", UserPromptSubmit hands Claude a brief of at most 2,000 characters (the request, the plan, the files and
commands, Codex's last message), kept in the chat only. The one file written is ~/.bosskuai/resume-state.json: thread ids
and times, so the same stop is not offered twice. Every public function swallows its errors, because a convenience must
never break a session. `BOSSKU_RESUME=off` switches both hooks off (`bossku resume` still works by hand). The rollout
format is undocumented, so each field is read defensively, and `bossku resume --debug` shows the structure (never any
text) to check the stop signature against a real limit.
"""

from __future__ import annotations

import json
import ntpath
import os
import posixpath
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from bossku.paths import user_config_dir
from bossku.redact import redact, redact_command

WINDOW = 12 * 3600                 # a stop older than this is not offered
TAIL_BYTES = 2 * 1024 * 1024       # only the end of a rollout is read; the stop is always at the end
BRIEF_CHARS = 2000
MARKER_DAYS = 7
MARKER_FILE = "resume-state.json"
LIMIT_SIGNATURE = "usage_limit_exceeded"
_STATE_EVENTS = ("task_started", "task_complete", "turn_aborted")
_SHELLS = ("powershell", "pwsh", "bash", "sh", "zsh", "cmd")
_LABEL = re.compile(r"[A-Za-z0-9_.:-]{1,40}")
_NEXT = "Next: ask the user what to do first. Do not redo finished steps."


@dataclass(frozen=True)
class Stop:
    thread: str
    rollout: Path
    cwd: str
    at: float                      # when Codex stopped, epoch seconds
    reset_at: float | None = None  # when the limit resets, when the rollout says so


# --- finding the stop ---------------------------------------------------------

def _norm(path) -> str:
    """One spelling for comparing folders: no \\\\?\\ prefix, one separator, and Windows paths without case."""
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    if re.match(r"[A-Za-z]:[\\/]", text) or text.startswith("\\\\"):
        return ntpath.normcase(ntpath.normpath(text))
    return posixpath.normpath(text)


def _under(child: str, parent: str) -> bool:
    prefix = parent.rstrip("\\/")
    return child == parent or child.startswith((prefix + "\\", prefix + "/"))


def _database(home: Path) -> Path | None:
    best, found = -1, None
    for path in (home / ".codex").glob("state_*.sqlite"):
        match = re.fullmatch(r"state_(\d+)\.sqlite", path.name)
        if match and int(match.group(1)) > best:
            best, found = int(match.group(1)), path
    return found


def _threads(cwd, home: Path, now: float, window: float) -> list[tuple[str, str]]:
    """(thread id, rollout path) of the user's recent threads in exactly this folder, newest first."""
    db = _database(home)
    if db is None:
        return []
    import sqlite3   # not at the top: every prompt hook imports this module, and most never need a database

    con = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=0.2)
    try:
        rows = con.execute(
            "SELECT id, rollout_path, cwd FROM threads WHERE archived=0 AND thread_source='user' AND updated_at_ms >= ? "
            "ORDER BY updated_at_ms DESC LIMIT 50", (int((now - window) * 1000),)).fetchall()
    finally:
        con.close()
    want = _norm(cwd)
    return [(str(tid), path) for tid, path, folder in rows
            if isinstance(path, str) and isinstance(folder, str) and _norm(folder) == want]


def _read_tail(path) -> bytes:
    with open(path, "rb") as handle:
        size = handle.seek(0, 2)
        start = max(0, size - TAIL_BYTES)
        handle.seek(start)
        data = handle.read(TAIL_BYTES)
    if start:                       # the cut usually lands inside a line: drop that partial line
        cut = data.find(b"\n")
        data = data[cut + 1:] if cut >= 0 else b""
    return data


def _records(path) -> list[dict]:
    records = []
    for line in _read_tail(path).splitlines():
        try:
            record = json.loads(line)
        except ValueError:          # a half-written last line, or anything that is not JSON
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def _payload(record: dict, kind: str = "event_msg") -> dict | None:
    payload = record.get("payload") if record.get("type") == kind else None
    return payload if isinstance(payload, dict) else None


def _last_state(records: list[dict]) -> tuple[int, dict] | None:
    for index in range(len(records) - 1, -1, -1):
        payload = _payload(records[index])
        if payload and payload.get("type") in _STATE_EVENTS:
            return index, payload
    return None


def _number(value) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _time_of(record: dict, payload: dict) -> float | None:
    stamp = record.get("timestamp")
    if isinstance(stamp, str):
        try:
            moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            return (moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)).timestamp()
        except ValueError:
            pass
    return _number(payload.get("completed_at"))


def _reset_after(records: list[dict], stop_at: float) -> float | None:
    """The reset time of the last token_count that has one, if it lies after the stop (else it is an older window's)."""
    for record in reversed(records):
        payload = _payload(record)
        limits = payload.get("rate_limits") if payload and payload.get("type") == "token_count" else None
        primary = limits.get("primary") if isinstance(limits, dict) else None
        value = _number(primary.get("resets_at")) if isinstance(primary, dict) else None
        if value is not None:
            value = value / 1000 if value > 1e11 else value      # seconds; milliseconds are accepted just in case
            return value if value > stop_at else None
    return None


def _stop_in(records: list[dict], now: float, window: float) -> tuple[float, float | None] | None:
    """(stopped at, reset at) when the rollout ends in a usage-limit stop inside the window."""
    last = _last_state(records)
    if last is None:
        return None
    index, payload = last
    error = payload.get("error")
    if payload.get("type") != "task_complete" or not isinstance(error, dict) \
            or error.get("codex_error_info") != LIMIT_SIGNATURE:
        return None
    at = _time_of(records[index], payload)
    if at is None or now - at > window:
        return None
    return at, _reset_after(records, at)


def _marker_path(home) -> Path:
    return user_config_dir(home) / MARKER_FILE


def _read_marker(home) -> dict[str, float]:
    try:
        raw = json.loads(_marker_path(home).read_text(encoding="utf-8")).get("continued")
        return {str(k): float(v) for k, v in raw.items() if _number(v) is not None} if isinstance(raw, dict) else {}
    except (OSError, ValueError, AttributeError):
        return {}


def mark_continued(stop: Stop, *, home: Path | None = None, now: float | None = None) -> bool:
    """Remember that this thread's stop was handed to Claude (thread id and time only). False when it cannot be saved."""
    now = time.time() if now is None else now
    try:
        seen = {k: t for k, t in _read_marker(home).items() if now - t < MARKER_DAYS * 86400}
        seen[stop.thread] = now
        path = _marker_path(home)
        path.parent.mkdir(parents=True, exist_ok=True)
        scratch = path.with_name(path.name + ".tmp")
        scratch.write_text(json.dumps({"continued": seen}), encoding="utf-8")
        os.replace(scratch, path)
        return True
    except Exception:  # noqa: BLE001 - the brief is still worth delivering without its marker
        return False


def find_codex_stop(cwd, home: Path | None = None, now: float | None = None, window: float = WINDOW, *,
                    ignore_continued: bool = True) -> Stop | None:
    """The usage-limit stop of the newest Codex thread in exactly this folder, or None. Never raises.

    Only the newest thread that has a task record decides: if the user went on in a newer thread, or that thread
    ended cleanly or was already continued, an older stop is not offered. That also keeps it to one tail read."""
    try:
        home = Path.home() if home is None else Path(home)
        now = time.time() if now is None else now
        threads = _threads(cwd, home, now, window)
        done = _read_marker(home) if ignore_continued and threads else {}
        for thread, rollout in threads:
            records = _records(rollout)
            if _last_state(records) is None:        # nothing of a task in the tail: this thread says nothing either way
                continue
            found = _stop_in(records, now, window)
            if found and done.get(thread, 0.0) < found[0]:
                return Stop(thread, Path(rollout), str(cwd), found[0], found[1])
            return None
    except Exception:  # noqa: BLE001 - no stop is the safe answer to any trouble
        pass
    return None


# --- what the user and the hooks see ------------------------------------------

def _ago(seconds: float) -> str:
    minutes = int(max(seconds, 0) // 60)
    if minutes < 1:
        return "under a minute"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h" + (f" {minutes}m" if minutes else "") if hours else f"{minutes} min"


def resume_off() -> bool:
    """BOSSKU_RESUME=off (or 0 or false) switches the two hooks off, so they never open Codex's files.
    `bossku resume` still works when you run it yourself."""
    return os.environ.get("BOSSKU_RESUME", "").strip().lower() in ("off", "0", "false")


def session_pointer(cwd, *, home: Path | None = None, now: float | None = None) -> str | None:
    """The one line SessionStart adds when a Codex stop is waiting in this folder; costs about 40 tokens."""
    if resume_off():
        return None
    now = time.time() if now is None else now
    stop = find_codex_stop(cwd, home, now)
    if stop is None:
        return None
    return (f'Codex hit its usage limit {_ago(now - stop.at)} ago in this folder. Say "continue" to pick up its task. '
            "Nothing loaded yet.")


def resume_context(cwd, *, home: Path | None = None, now: float | None = None) -> str | None:
    """The brief for "continue", marking the stop as handed over; None when there is nothing to resume."""
    if resume_off():
        return None
    now = time.time() if now is None else now
    stop = find_codex_stop(cwd, home, now)
    if stop is None:
        return None
    text = build_brief(stop, cwd, now=now)
    if not text:
        return None
    mark_continued(stop, home=home, now=now)
    return text


# --- the brief ----------------------------------------------------------------

def _clean(text, limit: int, keep_end: bool = False, command: bool = False) -> str:
    """Redact first, then flatten and cut, so a secret is never cut in half and left behind. A path keeps its end.
    A shell command also gets the command-line secret forms (`--password x`, `curl -u a:b`, `mysql -pX`, `DB_PASS=`)."""
    flat = " ".join((redact_command if command else redact)(text[:20000]).split()) if isinstance(text, str) else ""
    if len(flat) <= limit:
        return flat
    return "..." + flat[len(flat) - limit + 3:] if keep_end else flat[:max(limit - 3, 0)].rstrip() + "..."


def _message_text(item: dict) -> str:
    content = item.get("content")
    if isinstance(content, list):
        return " ".join(t for t in (part.get("text") if isinstance(part, dict) else part for part in content)
                        if isinstance(t, str))
    if isinstance(content, str):
        return content
    text = item.get("text")
    return text if isinstance(text, str) else ""


def _command_text(command) -> str:
    if isinstance(command, list):
        parts = [str(p) for p in command]
        if len(parts) >= 3 and re.sub(r"\.exe$", "", ntpath.basename(parts[0]).lower()) in _SHELLS:
            return parts[-1]
        return " ".join(parts)
    return command if isinstance(command, str) else ""


def _plan_steps(arguments) -> list[tuple[str, str]]:
    try:
        data = json.loads(arguments) if isinstance(arguments, str) else arguments
    except ValueError:
        return []
    steps = data.get("plan") if isinstance(data, dict) else None
    return [(s["step"], str(s.get("status"))) for s in steps if isinstance(s, dict) and isinstance(s.get("step"), str)] \
        if isinstance(steps, list) else []


@dataclass
class _Digest:
    goal: str = ""
    plan: object = None                                  # [(step, status)] from update_plan or str from a Plan item; the later wins
    files: dict = field(default_factory=dict)            # path -> None, oldest first
    commands: list = field(default_factory=list)         # [(command, exit code)]
    message: str = ""
    later: str = ""                                      # what the user typed in Codex after the stop


def _item(record: dict) -> dict | None:
    """The finished item of an item_completed record, or None."""
    payload = record.get("payload")
    if record.get("type") != "event_msg" or not isinstance(payload, dict) or payload.get("type") != "item_completed":
        return None
    found = payload.get("item")
    return found if isinstance(found, dict) else None


def _digest(records: list[dict], upto: int) -> _Digest:
    digest = _Digest()
    for record in records[upto + 1:]:
        found = _item(record)
        if found and found.get("type") == "UserMessage":
            digest.later = _message_text(found) or digest.later
    for record in records[:upto + 1]:
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        if record.get("type") == "response_item":
            if payload.get("type") == "function_call" and payload.get("name") == "update_plan":
                steps = _plan_steps(payload.get("arguments"))
                if steps:
                    digest.plan = steps
            continue
        found = _item(record)
        if found is None:
            continue
        kind = found.get("type")
        if kind == "UserMessage":
            digest.goal = _message_text(found) or digest.goal
        elif kind == "AgentMessage":
            digest.message = _message_text(found) or digest.message
        elif kind == "Plan" and isinstance(found.get("text"), str):
            digest.plan = found["text"]
        elif kind == "FileChange" and isinstance(found.get("changes"), dict):
            for path in found["changes"]:
                if isinstance(path, str):
                    digest.files.pop(path, None)
                    digest.files[path] = None
        elif kind == "CommandExecution":
            code = found.get("exit_code")
            digest.commands.append((_command_text(found.get("command")), code if isinstance(code, int) else None))
    return digest


def _git(cwd: str, *args: str) -> bytes | None:
    import subprocess   # only a brief needs it; the prompt hooks that import this module do not

    try:
        run = subprocess.run(["git", "-C", cwd, *args], capture_output=True, timeout=2,
                             env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})   # looking must not touch the index
    except (OSError, subprocess.SubprocessError):
        return None
    return run.stdout if run.returncode == 0 else None


def _dirty_files(cwd: str) -> tuple[str, set[str]] | None:
    """(repository root, normalised dirty paths) from git, or None when git cannot say."""
    top = _git(cwd, "rev-parse", "--show-toplevel")
    status = _git(cwd, "status", "--porcelain", "-z", "--untracked-files=all") if top else None
    if not top or status is None:
        return None
    root = top.decode("utf-8", "replace").strip()
    dirty, entries, i = set(), status.decode("utf-8", "replace").split("\0"), 0
    while i < len(entries):
        entry, i = entries[i], i + 1
        if len(entry) < 4:
            continue
        dirty.add(_norm(root + "/" + entry[3:]))
        if entry[0] in "RC" or entry[1] in "RC":
            i += 1                  # a rename or copy is followed by its source path
    return _norm(root), dirty


def _short_path(path: str, cwd: str) -> str:
    text = path[4:] if path.startswith("\\\\?\\") else path
    module = ntpath if re.match(r"[A-Za-z]:[\\/]", text) else posixpath
    try:
        rel = module.relpath(text, cwd) if module.isabs(text) else text
    except ValueError:              # another drive
        return text
    return text if rel.startswith("..") else rel


def _files_line(files: list[str], cwd: str, shown: int, git_view) -> str:
    """"Files Codex changed", newest first, each marked against git when git could be asked."""
    resolved = [p if re.match(r"[A-Za-z]:[\\/]|[\\/]", p) else cwd.rstrip("\\/") + "/" + p for p in files]
    normal = [_norm(p) for p in resolved]
    known = bool(git_view) and any(_under(n, git_view[0]) for n in normal)
    names = []
    for path, norm in list(zip(files, normal))[:shown]:
        mark = ""
        if known and _under(norm, git_view[0]):
            mark = " (still dirty)" if norm in git_view[1] else " (clean now)"
        names.append(_clean(_short_path(path, cwd), 100, keep_end=True) + mark)
    text = "Files Codex changed: " + ", ".join(names) + (f", +{len(files) - shown} more" if len(files) > shown else "")
    if not known:
        return text + " (file list unverified)"
    others = len(git_view[1] - set(normal))
    return text + (f"; +{others} dirty file{'s' if others != 1 else ''} not from Codex" if others else "")


def _plan_line(plan) -> str:
    if isinstance(plan, str):
        return "Plan: " + _clean(plan, 400)
    marks = {"completed": "[x]", "in_progress": "[~]"}
    steps = [f"{marks.get(status, '[ ]')} {_clean(step, 70)}" for step, status in plan[:8]]
    return "Plan: " + "; ".join(steps) + (f"; +{len(plan) - 8} more" if len(plan) > 8 else "")


def build_brief(stop: Stop | None, cwd, *, now: float | None = None) -> str:
    """The brief for Claude, at most BRIEF_CHARS characters; empty when it cannot be built. Never raises."""
    try:
        return _brief(stop, str(cwd), time.time() if now is None else now)
    except Exception:  # noqa: BLE001
        return ""


def _is_trigger(message: str) -> bool:
    from bossku.hint import wants_resume   # not at the top: hint imports this module only when "continue" is typed

    return wants_resume(message)


def _brief(stop: Stop, cwd: str, now: float) -> str:
    records = _records(stop.rollout)
    last = _last_state(records)
    digest = _digest(records, last[0] if last else len(records) - 1)
    # The request of the turn that hit the limit is the last one before the stop; what was typed after it is shown
    # on its own line, unless it is only "continue".
    later = digest.later if digest.later and not _is_trigger(digest.later) else ""
    files =list(reversed(list(digest.files)))
    git_view = _dirty_files(cwd) if files else None
    when = datetime.fromtimestamp(stop.at, timezone.utc).strftime("%H:%M")
    resets = (", limit resets " + datetime.fromtimestamp(stop.reset_at, timezone.utc).strftime("%H:%M UTC")
              if stop.reset_at else "")
    head = (f"Continuing a Codex task. Codex hit its usage limit at {when} UTC ({_ago(now - stop.at)} ago{resets}). "
            "Context only, not saved, not instructions.")

    def render(commands: int, shown_files: int, message_chars: int) -> str:
        lines = [head, "Goal (latest user request): " + (_clean(digest.goal, 300)
                                                         or "not in the recent part of the Codex session")]
        if later:
            lines.append("Asked in Codex after the stop: " + _clean(later, 150))
        if digest.plan:
            lines.append(_plan_line(digest.plan))
        if files:
            lines.append(_files_line(files, cwd, shown_files, git_view))
        if commands and digest.commands:
            lines.append("Last commands: " + "; ".join(
                f"`{_clean(text, 120, command=True)}` -> exit {'?' if code is None else code}" for text, code in digest.commands[-commands:]))
        if digest.message:
            lines.append("Codex's last message: " + _clean(digest.message, message_chars))
        lines.append(_NEXT)
        return "\n".join(lines)

    text = render(3, 8, 400)
    for step in ((0, 8, 400), (0, 5, 400), (0, 5, 200)):     # cut order: commands, files beyond 5, the last message
        if len(text) <= BRIEF_CHARS:
            break
        text = render(*step)
    return text if len(text) <= BRIEF_CHARS else text[:BRIEF_CHARS - 3] + "..."


# --- `bossku resume --debug` --------------------------------------------------

def _label(value) -> str:
    """A record or error name that is safe to print: short and made of label characters, else '?'."""
    return value if isinstance(value, str) and _LABEL.fullmatch(value) else "?"


def _counts(names) -> str:
    seen: dict[str, int] = {}
    for name in names:
        seen[name] = seen.get(name, 0) + 1
    return ", ".join(f"{k}={v}" for k, v in sorted(seen.items())) or "none"


def debug_report(cwd, *, home: Path | None = None, now: float | None = None, window: float = WINDOW) -> list[str]:
    """Lines that describe the record structure of this folder's recent Codex threads. Names and counts only, never text."""
    try:
        home = Path.home() if home is None else Path(home)
        now = time.time() if now is None else now
        db = _database(home)
        if db is None:
            return ["no Codex state database found under ~/.codex"]
        threads = _threads(cwd, home, now, window)
        lines = [f"database: {db.name}", f"threads for this folder in the last {int(window // 3600)}h: {len(threads)}"]
        if not threads:
            lines.append("no thread to look at (is Codex's folder the same as this one?)")
        for number, (_thread, rollout) in enumerate(threads[:3], 1):
            records = _records(rollout)
            lines.append(f"thread {number}: {len(records)} records read from the end of the rollout")
            lines.append("  record types: " + _counts(_label(r.get("type")) for r in records))
            events = [_label(p.get("type")) for r in records if (p := _payload(r))]
            lines.append("  event types: " + _counts(events))
            lines.append("  last 3 records: " + ", ".join(
                f"{_label(r.get('type'))}/{_label(r['payload'].get('type')) if isinstance(r.get('payload'), dict) else '-'}"
                for r in records[-3:]))
            last = _last_state(records)
            if last is None:
                lines.append("  not a stop: no task_started, task_complete or turn_aborted record")
                continue
            payload = last[1]
            error = payload.get("error")
            lines.append(f"  last state record: {_label(payload.get('type'))}; keys: "
                         + ", ".join(sorted(_label(k) for k in payload)))
            if isinstance(error, dict):
                info = error.get("codex_error_info")
                lines.append("  error keys: " + ", ".join(sorted(_label(k) for k in error))
                             + (f"; codex_error_info={info}" if _label(info) != "?" else ""))
            found = _stop_in(records, now, window)
            lines.append("  verdict: a usage-limit stop" if found else "  verdict: not a stop (no usage-limit error "
                         "on the last state record, or it is older than the window)")
        return lines
    except Exception as exc:  # noqa: BLE001
        return [f"debug failed: {type(exc).__name__}"]
