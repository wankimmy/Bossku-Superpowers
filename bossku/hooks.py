from __future__ import annotations

import codecs
import contextlib
import json
import os
import re
import shutil
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

from bossku.memory import sync_project
from bossku.paths import user_config_dir

HOOK_MARKER = "sync-hook"
ALL_TOOLS = ("claude_code", "cursor", "codex", "opencode")

# Denser defaults (additive). Marker-checked per event so upgrades fill gaps.
CURSOR_EVENTS = ("stop", "sessionEnd", "afterAgentResponse")
CLAUDE_EVENTS = ("Stop", "SessionEnd")
HINT_MARKER = "skill-hint"
HINT_EVENT = "UserPromptSubmit"
GATE_MARKER = "verify-gate"
GATE_EVENT = "Stop"
BRIEF_MARKER = "session-brief"
BRIEF_EVENT = "SessionStart"
CODEX_EVENTS = ("Stop", "SessionEnd")
# Kept out of CODEX_EVENTS on purpose: every event in that tuple gets the Stop sync wrapper.
CODEX_HINT_EVENT = "UserPromptSubmit"
CODEX_HINT_TIMEOUT = 10

# The Node harness in hooks/hooks.json, wired into ~/.claude/settings.json: (event, matcher, script, timeout).
# tests/test_harness_extra.py fails when this drifts from hooks.json.
HARNESS_MARKER = "--bossku-harness"
HARNESS_EVENTS = (
    ("SessionStart", "startup|resume|clear|compact", "session-start.mjs", 10),
    ("PreToolUse", "Bash|PowerShell", "guard.mjs", 10),
    ("PostToolUse", "Write|Edit|MultiEdit|NotebookEdit", "post-edit.mjs", 30),
    ("Stop", None, "stop-gate.mjs", 15),
)
# The unambiguous destructive commands, kept even when the hooks are off. Each one is a `perm` of a rule in
# hooks/guard.mjs, and tests/hooks.test.mjs fails when an entry has no matching guard rule.
DENY_RULES = (
    "Bash(git reset --hard:*)",
    "Bash(git clean -f:*)",
    "Bash(git push -f:*)",
    "Bash(php artisan migrate:fresh:*)",
    "Bash(php artisan db:wipe:*)",
    "Bash(docker compose down:*)",
    "Bash(docker-compose down:*)",
    "Bash(docker system prune:*)",
)
PLUGIN_NAMES = ("bossku-superpower", "bossku-ai")   # the current plugin name and the one it had before


def resolve_bossku_argv() -> list[str]:
    exe = shutil.which("bossku")
    return [exe] if exe else [sys.executable, "-m", "bossku"]


def resolve_bossku_command() -> str:
    return " ".join(resolve_bossku_argv())


def _backup(path: Path) -> None:
    if not path.is_file():
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    backup = path.with_name(f"{path.name}.bak-{stamp}")
    if backup.exists():   # never replace an earlier snapshot: it may be the only copy of the original
        return
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def _read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _remove_scratch(scratch: Path) -> None:
    """Delete the .tmp sibling, never raising: a failed cleanup must not hide the error that came first. Windows will
    not delete a read-only file (the .tmp inherits a read-only settings.json's mode), so make it writable first."""
    with contextlib.suppress(OSError):
        if not scratch.is_symlink():      # chmod would follow a link and change the file it points at
            os.chmod(scratch, stat.S_IWRITE)
    with contextlib.suppress(OSError):
        scratch.unlink(missing_ok=True)


def _write_json_atomic(path: Path, data: dict) -> None:
    """Like _write_json, but a crash mid-write never leaves half a settings.json (write a sibling, then swap it in).
    A symlinked file is written through, so a dotfile-managed settings.json stays a link; its mode is kept."""
    target = path.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    scratch = target.with_name(target.name + ".tmp")
    _remove_scratch(scratch)              # one leftover from a crash or an earlier failed run must not block this run
    try:
        scratch.write_text(json.dumps(data, indent=2), encoding="utf-8")
        if target.exists():
            shutil.copymode(target, scratch)
        os.replace(scratch, target)
    except OSError:
        _remove_scratch(scratch)          # a failed swap (a locked or read-only file on Windows) leaves no .tmp behind
        raise


def _commands(node) -> list[str]:
    """Every `command` string inside one hook entry, however deeply it is nested."""
    if isinstance(node, dict):
        own = [node["command"]] if isinstance(node.get("command"), str) else []
        return own + [c for v in node.values() for c in _commands(v)]
    if isinstance(node, list):
        return [c for v in node for c in _commands(v)]
    return []


def _owner_pattern(marker: str) -> re.Pattern:
    """A command bossku wrote for this marker: `bossku <marker>`, `python -m bossku <marker>`, the Codex wrapper
    script, or the old `... # <marker>` tail. A user's own `my-sync-hook-notes.sh` is none of these."""
    m = re.escape(marker)
    lead = r"""(?:^|[\s"'/\\])"""
    return re.compile(
        rf"""{lead}bossku(?:\.exe)?["']?\s+{m}(?![\w.-])|-m\s+bossku\s+{m}(?![\w.-])"""
        rf"""|{lead}codex-{m}\.(?:sh|ps1)\b|#\s*{m}\s*$""", re.IGNORECASE)


def _owned(entry, marker: str) -> bool:
    pattern = _owner_pattern(marker)
    return any(pattern.search(command) for command in _commands(entry))


def _has_marker(entries: list, marker: str) -> bool:
    return any(_owned(entry, marker) for entry in entries)


def _strip_marker(entries: list, marker: str) -> list:
    return [entry for entry in entries if not _owned(entry, marker)]


def _ensure_event(hooks: dict, event: str, entry: dict) -> bool:
    """Add marked entry for event if missing. Returns True when something was added."""
    bucket = hooks.get(event)
    if not isinstance(bucket, list):
        bucket = []
        hooks[event] = bucket
    if _has_marker(bucket, HOOK_MARKER):
        return False
    bucket.append(entry)
    return True


def _strip_events(hooks: dict, events: tuple[str, ...], marker: str = HOOK_MARKER) -> bool:
    changed = False
    for event in events:
        entries = hooks.get(event)
        if not isinstance(entries, list):
            continue
        remaining = _strip_marker(entries, marker)
        if len(remaining) == len(entries):
            continue
        changed = True
        if remaining:
            hooks[event] = remaining
        else:
            del hooks[event]
    return changed


def _events_complete(hooks: dict, events: tuple[str, ...]) -> bool:
    return all(
        isinstance(hooks.get(ev), list) and _has_marker(hooks[ev], HOOK_MARKER) for ev in events
    )


def _sync_cmd() -> str:
    return f"{resolve_bossku_command()} sync-hook"


def _claude_sync_cmd() -> str:
    """Quoted forward-slash path: Claude Code runs hooks through Git Bash on Windows,
    where an unquoted `C:\\Users\\...\\bossku.EXE` loses its backslashes."""
    exe = shutil.which("bossku")
    if exe:
        return f'"{Path(exe).as_posix()}" sync-hook'
    return f'"{Path(sys.executable).as_posix()}" -m bossku sync-hook'


def _claude_cmd(subcommand: str) -> str:
    exe = shutil.which("bossku")
    if exe:
        return f'"{Path(exe).as_posix()}" {subcommand}'
    return f'"{Path(sys.executable).as_posix()}" -m bossku {subcommand}'


def _codex_hint_cmd() -> str:
    """`skill-hint --host codex` with a forward-slash path, quoted only when it has a space. Codex may run the
    command in cmd, PowerShell or bash (not verified); an unquoted path works in all three, a quoted one not in PowerShell."""
    exe = shutil.which("bossku")
    argv = [Path(exe).as_posix()] if exe else [Path(sys.executable).as_posix(), "-m", "bossku"]
    if " " in argv[0]:
        argv[0] = f'"{argv[0]}"'
    return " ".join([*argv, "skill-hint", "--host", "codex"])


def apply_marked_hook(hooks: dict, event: str, marker: str, command: str, timeout: int = 10) -> bool:
    """Add one marked command hook to a hooks dict in memory. Returns True when it changed."""
    bucket = hooks.get(event)
    if isinstance(bucket, list) and _has_marker(bucket, marker):
        if _has_command(bucket, command):
            return False
        hooks[event] = _strip_marker(bucket, marker)   # an older command this shell cannot run
    hooks.setdefault(event, []).append({"hooks": [{"type": "command", "command": command, "timeout": timeout}]})
    return True


def ensure_marked_hook(settings: Path, event: str, marker: str, command: str, timeout: int = 10) -> bool:
    """Add one marked command hook to a Claude Code settings.json. Returns True when the file changed."""
    data = _read_json(settings)
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = data["hooks"] = {}
    if not apply_marked_hook(hooks, event, marker, command, timeout):
        return False
    if settings.is_file():
        _backup(settings)
    _write_json(settings, data)
    return True


def remove_marked_hook(settings: Path, event: str, marker: str) -> bool:
    data = _read_json(settings)
    hooks = data.get("hooks", {})
    bucket = hooks.get(event) if isinstance(hooks, dict) else None
    if not isinstance(bucket, list) or not _has_marker(bucket, marker):
        return False
    remaining = _strip_marker(bucket, marker)
    if remaining:
        hooks[event] = remaining
    else:
        del hooks[event]
    _backup(settings)
    _write_json(settings, data)
    return True


def ensure_skill_hint_hook(settings: Path, command: str | None = None) -> bool:
    return ensure_marked_hook(settings, HINT_EVENT, HINT_MARKER, command or _claude_cmd("skill-hint"))


def ensure_verify_gate_hook(settings: Path, command: str | None = None) -> bool:
    return ensure_marked_hook(settings, GATE_EVENT, GATE_MARKER, command or _claude_cmd("verify-gate"), timeout=15)


def ensure_session_brief_hook(settings: Path, command: str | None = None) -> bool:
    return ensure_marked_hook(settings, BRIEF_EVENT, BRIEF_MARKER, command or _claude_cmd("session-brief"))


def remove_session_brief_hook(settings: Path) -> bool:
    return remove_marked_hook(settings, BRIEF_EVENT, BRIEF_MARKER)


def remove_skill_hint_hook(settings: Path) -> bool:
    return remove_marked_hook(settings, HINT_EVENT, HINT_MARKER)


def remove_verify_gate_hook(settings: Path) -> bool:
    return remove_marked_hook(settings, GATE_EVENT, GATE_MARKER)


def _has_command(entries: list, command: str) -> bool:
    return any(
        isinstance(hook, dict) and hook.get("command") == command
        for entry in entries
        if isinstance(entry, dict)
        for hook in entry.get("hooks", [])
    )


# --- the Node harness (hooks/hooks.json) -----------------------------------

def _harness_entry(root: Path, matcher: str | None, script: str, timeout: int) -> dict:
    command = f'node "{root.resolve().as_posix()}/hooks/{script}" {HARNESS_MARKER}'
    entry = {"matcher": matcher} if matcher else {}
    entry["hooks"] = [{"type": "command", "command": command, "timeout": timeout}]
    return entry


def _is_harness(entry) -> bool:
    return any(HARNESS_MARKER in command for command in _commands(entry))


def _harness_problem(root: Path) -> dict | None:
    """Why the harness cannot be wired from this checkout, or None when it can."""
    if shutil.which("node") is None:
        return {"status": "skipped_no_node", "message": "node is not on PATH, and the harness hooks run with Node"}
    for rel in ("hooks/hooks.json", *(f"hooks/{script}" for _e, _m, script, _t in HARNESS_EVENTS)):
        if not (root / rel).is_file():
            return {"status": "error", "message": f"{rel} not found under {root}"}
    return None


def _apply_harness(data: dict, hooks: dict, root: Path) -> bool:
    """Add the harness commands and the deny rules to a settings dict in memory, next to whatever is there.
    Returns True when something changed."""
    changed = False
    for event, matcher, script, timeout in HARNESS_EVENTS:
        want = _harness_entry(root, matcher, script, timeout)
        bucket = hooks.get(event)
        bucket = bucket if isinstance(bucket, list) else []
        if [e for e in bucket if _is_harness(e)] == [want]:
            continue
        hooks[event] = [e for e in bucket if not _is_harness(e)] + [want]   # an older path or matcher is replaced
        changed = True
    perms = data.get("permissions")
    perms = data["permissions"] = perms if isinstance(perms, dict) else {}
    deny = perms.get("deny")
    deny = perms["deny"] = deny if isinstance(deny, list) else []
    missing = [rule for rule in DENY_RULES if rule not in deny]
    deny.extend(missing)
    return changed or bool(missing)


def _strip_harness(data: dict, hooks: dict) -> bool:
    """Take the harness commands and the deny rules out of a settings dict in memory; the user's own stay.
    ponytail: a deny rule the user wrote word for word like ours cannot be told apart, so it goes too."""
    changed = False
    for event in list(hooks):
        entries = hooks[event]
        if not isinstance(entries, list) or not any(_is_harness(e) for e in entries):
            continue
        changed = True
        remaining = [e for e in entries if not _is_harness(e)]
        if remaining:
            hooks[event] = remaining
        else:
            del hooks[event]
    perms = data.get("permissions")
    deny = perms.get("deny") if isinstance(perms, dict) else None
    if isinstance(deny, list) and any(rule in deny for rule in DENY_RULES):
        changed = True
        perms["deny"] = [rule for rule in deny if rule not in DENY_RULES]
        if not perms["deny"]:
            del perms["deny"]
        if not perms:
            del data["permissions"]
    return changed


def harness_status(home: Path | None = None) -> dict:
    """What `bossku hooks install` wired into ~/.claude/settings.json: `hooks` (all gates), `deny_rules`, `events`. Read-only."""
    h = home if home is not None else Path.home()
    status: dict = {"hooks": False, "deny_rules": False, "events": []}
    try:
        data = _read_json(h / ".claude" / "settings.json")
        hooks, perms = data.get("hooks"), data.get("permissions")
    except (OSError, ValueError, AttributeError):
        return status
    hooks = hooks if isinstance(hooks, dict) else {}
    status["events"] = [event for event, *_ in HARNESS_EVENTS
                        if isinstance(hooks.get(event), list) and any(_is_harness(e) for e in hooks[event])]
    status["hooks"] = len(status["events"]) == len(HARNESS_EVENTS)
    deny = perms.get("deny") if isinstance(perms, dict) else None
    status["deny_rules"] = isinstance(deny, list) and all(rule in deny for rule in DENY_RULES)
    return status


def plugin_double_load(home: Path | None = None) -> dict:
    """Is a BosskuAI plugin enabled in Claude Code, and does its cached copy ship hooks? Read-only.
    Next to a local install, an enabled plugin loads every skill and every hook a second time."""
    h = home if home is not None else Path.home()
    out: dict = {"plugin_enabled": False, "plugin": None, "plugin_has_hooks": False, "version": None}
    try:
        enabled = _read_json(h / ".claude" / "settings.json").get("enabledPlugins")
        installed = _read_json(h / ".claude" / "plugins" / "installed_plugins.json").get("plugins")
    except (OSError, ValueError, AttributeError):
        return out
    ours = [key for key, on in (enabled.items() if isinstance(enabled, dict) else ())
            if on and str(key).split("@")[0] in PLUGIN_NAMES]
    if not ours:
        return out
    out["plugin_enabled"] = True
    out["plugin"] = ours[0]
    copies = installed.get(ours[0]) if isinstance(installed, dict) else None
    copy = copies[0] if isinstance(copies, list) and copies and isinstance(copies[0], dict) else {}
    out["version"] = copy.get("version")
    where = copy.get("installPath")
    out["plugin_has_hooks"] = isinstance(where, str) and (Path(where) / "hooks" / "hooks.json").is_file()
    return out


# --- Codex continue-safe wrappers ----------------------------------------

_CODEX_SH = """#!/usr/bin/env bash
# Managed by BosskuAI (`bossku hooks install`). Codex Stop/SessionEnd wrapper.
# Curated one-way Obsidian export, then continue JSON required by Codex Stop.
set -u
if [ -t 0 ]; then
  INPUT=""
else
  INPUT="$(cat || true)"
fi
run_sync() {
  if command -v bossku >/dev/null 2>&1; then
    if [ -n "$INPUT" ]; then printf '%s' "$INPUT" | bossku sync-hook; else bossku sync-hook </dev/null; fi
  else
    if [ -n "$INPUT" ]; then printf '%s' "$INPUT" | python3 -m bossku sync-hook; else python3 -m bossku sync-hook </dev/null; fi
  fi
}
run_sync >/dev/null 2>&1 || true
printf '%s\n' '{"continue": true}'
"""

_CODEX_PS1 = """# Managed by BosskuAI (`bossku hooks install`). Codex Stop/SessionEnd wrapper.
# Curated one-way Obsidian export, then continue JSON required by Codex Stop.
$ErrorActionPreference = 'Continue'
# Read and pass the payload as UTF-8: the console code page would turn a non-ASCII project path into '?'.
$utf8 = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = $utf8
$inputJson = ''
try {
  $buffer = New-Object System.IO.MemoryStream
  [Console]::OpenStandardInput().CopyTo($buffer)
  $inputJson = $utf8.GetString($buffer.ToArray())
} catch {}
function Invoke-BosskuSyncHook {
  if (Get-Command bossku -ErrorAction SilentlyContinue) {
    if ($inputJson) { $inputJson | & bossku sync-hook | Out-Null }
    else { & bossku sync-hook | Out-Null }
    return
  }
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
  if ($py) {
    if ($inputJson) { $inputJson | & $py.Source -m bossku sync-hook | Out-Null }
    else { & $py.Source -m bossku sync-hook | Out-Null }
  }
}
try { Invoke-BosskuSyncHook } catch {}
Write-Output '{"continue": true}'
"""


def _scripts_dir() -> Path | None:
    candidate = Path(__file__).resolve().parent.parent / "scripts"
    return candidate if candidate.is_dir() else None


def ensure_codex_wrapper(home: Path, *, windows: bool | None = None) -> Path:
    """Materialize ~/.bosskuai/codex-sync-hook.(sh|ps1) from scripts/ templates when present."""
    cfg = user_config_dir(home)
    cfg.mkdir(parents=True, exist_ok=True)
    use_win = os.name == "nt" if windows is None else windows
    scripts = _scripts_dir()
    if use_win:
        dest = cfg / "codex-sync-hook.ps1"
        shipped = scripts / "codex-sync-hook.ps1" if scripts else None
        body = shipped.read_text(encoding="utf-8") if shipped and shipped.is_file() else _CODEX_PS1
    else:
        dest = cfg / "codex-sync-hook.sh"
        shipped = scripts / "codex-sync-hook.sh" if scripts else None
        body = shipped.read_text(encoding="utf-8") if shipped and shipped.is_file() else _CODEX_SH
    dest.write_text(body, encoding="utf-8")
    if not use_win:
        dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return dest


def codex_wrapper_command(wrapper: Path) -> str:
    if wrapper.suffix.lower() == ".ps1":
        quoted = str(wrapper).replace("'", "''")
        return f"powershell -NoProfile -ExecutionPolicy Bypass -File '{quoted}'"
    return str(wrapper)


def enable_codex_hooks_feature(home: Path) -> dict:
    """Set [features] hooks = true in ~/.codex/config.toml without wiping other keys.

    An explicit `hooks = false` is the user's choice and stays; so does a file that is not valid TOML."""
    base = home / ".codex"
    if not base.is_dir():
        return {"status": "skipped_not_found", "path": str(base / "config.toml"), "changed": False}
    path = base / "config.toml"
    if not path.is_file():
        path.write_text("[features]\nhooks = true\n", encoding="utf-8")
        return {"status": "installed", "path": str(path), "changed": True}

    raw = path.read_bytes()   # bytes keep CRLF as it was
    bom = codecs.BOM_UTF8 if raw.startswith(codecs.BOM_UTF8) else b""   # PowerShell 5.1 writes one; tomllib rejects it
    updated, status = _enable_hooks_in_toml(raw[len(bom):].decode("utf-8"))
    result = {"status": status, "path": str(path), "changed": status == "installed"}
    if status == "disabled_by_user":
        result["warning"] = "[features] hooks = false in config.toml: left as it is, so Codex will not run the sync hook"
    elif status == "skipped_invalid_toml":
        result["warning"] = "config.toml is not valid TOML or cannot be edited safely: set [features] hooks = true by hand"
    if status == "installed":
        _backup(path)
        path.write_bytes(bom + updated.encode("utf-8"))
    return result


_FEATURES_HEADER = re.compile(r"^\s*\[\s*features\s*\]\s*(?:#.*)?$")


def _enable_hooks_in_toml(text: str) -> tuple[str, str]:
    """(new text, state): installed, already_installed, disabled_by_user or skipped_invalid_toml."""
    import tomllib   # only the Codex installer needs it: keep it off every hook process
    try:
        features = tomllib.loads(text).get("features")
    except tomllib.TOMLDecodeError:
        return text, "skipped_invalid_toml"
    current = features.get("hooks") if isinstance(features, dict) else None
    if current is True:
        return text, "already_installed"
    if current is False:
        return text, "disabled_by_user"
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if _FEATURES_HEADER.match(line.rstrip("\r")):
            lines.insert(i + 1, "hooks = true" + ("\r" if line.endswith("\r") else ""))
            new = "\n".join(lines)
            break
    else:
        gap = "" if not text else (nl if text.endswith("\n") else nl + nl)
        new = f"{text}{gap}[features]{nl}hooks = true{nl}"
    try:   # never write a file Codex could not read back
        ok = tomllib.loads(new).get("features", {}).get("hooks") is True
    except tomllib.TOMLDecodeError:
        ok = False
    return (new, "installed") if ok else (text, "skipped_invalid_toml")


# --- install -----------------------------------------------------------

def install_claude_code_hook(home: Path) -> dict:
    return _install_claude(home)[0]


def _has_harness_gate(hooks: dict) -> bool:
    entries = hooks.get(GATE_EVENT)
    return isinstance(entries, list) and any(_is_harness(e) for e in entries)


def _install_claude(
    home: Path, harness_root: Path | None = None, *, harness_off: bool = False
) -> tuple[dict, dict | None]:
    """The Claude Code hooks, plus the Node harness when `harness_root` (a checkout with hooks/) is given.
    One read, one backup and one write. Returns (claude_code result, claude_harness result or None).

    The harness has its own Stop gate, so a user never gets two: the Python verify-gate is left out, and an old
    one removed, whenever the Node gate is wired by this call or is already in settings.json (no root, no node or a
    broken checkout leave the Node gate that is there alone). `harness_off` is the explicit opt-out: it takes
    our Node gates and deny rules out, and the verify-gate takes over."""
    base = home / ".claude"
    if not base.is_dir():
        gone = {"status": "skipped_not_found", "path": str(base)}
        return gone, (dict(gone) if harness_root is not None else None)
    path = base / "settings.json"
    data = _read_json(path)
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = {}
        data["hooks"] = hooks
    command = _claude_sync_cmd()
    entry = {"hooks": [{"type": "command", "command": command}]}
    for ev in CLAUDE_EVENTS:
        bucket = hooks.get(ev)
        # Our own entry from an older install may hold a command this shell cannot run.
        if isinstance(bucket, list) and _has_marker(bucket, HOOK_MARKER) and not _has_command(bucket, command):
            hooks[ev] = _strip_marker(bucket, HOOK_MARKER)
    added = [ev for ev in CLAUDE_EVENTS if _ensure_event(hooks, ev, json.loads(json.dumps(entry)))]
    if apply_marked_hook(hooks, HINT_EVENT, HINT_MARKER, _claude_cmd("skill-hint")):
        added.append("skill-hint")
    stripped = _strip_harness(data, hooks) if harness_off else False
    blocked = _harness_problem(harness_root) if harness_root is not None else None
    wire_harness = harness_root is not None and blocked is None
    dropped_gate = False
    if wire_harness or _has_harness_gate(hooks):
        dropped_gate = _strip_events(hooks, (GATE_EVENT,), GATE_MARKER)
    elif apply_marked_hook(hooks, GATE_EVENT, GATE_MARKER, _claude_cmd("verify-gate"), timeout=15):
        added.append("verify-gate")
    if apply_marked_hook(hooks, BRIEF_EVENT, BRIEF_MARKER, _claude_cmd("session-brief")):
        added.append("session-brief")
    harness = None
    if wire_harness:
        wired = _apply_harness(data, hooks, harness_root) or dropped_gate
        harness = {"status": "installed" if wired else "already_installed", "path": str(path),
                   "events": [event for event, *_ in HARNESS_EVENTS], "deny_rules": len(DENY_RULES)}
        if dropped_gate:
            harness["removed"] = ["verify-gate"]
    elif blocked is not None:
        harness = {**blocked, "path": str(path)}
    elif stripped:
        harness = {"status": "removed", "path": str(path)}
    events = [*CLAUDE_EVENTS, HINT_EVENT, BRIEF_EVENT]
    if added or stripped or (wire_harness and harness["status"] == "installed") or (dropped_gate and not wire_harness):
        _backup(path)
        _write_json(path, data)
    result = {"status": "installed" if added else "already_installed", "path": str(path), "events": events}
    if added:
        result["added"] = added
    if dropped_gate and not wire_harness:
        result["removed"] = ["verify-gate"]
    return result, harness


def install_cursor_hook(home: Path) -> dict:
    base = home / ".cursor"
    if not base.is_dir():
        return {"status": "skipped_not_found", "path": str(base)}
    path = base / "hooks.json"
    data = _read_json(path)
    data.setdefault("version", 1)
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = {}
        data["hooks"] = hooks
    entry = {"command": _sync_cmd()}
    added = [ev for ev in CURSOR_EVENTS if _ensure_event(hooks, ev, dict(entry))]
    if not added:
        return {"status": "already_installed", "path": str(path), "events": list(CURSOR_EVENTS)}
    _backup(path)
    _write_json(path, data)
    return {"status": "installed", "path": str(path), "events": list(CURSOR_EVENTS), "added": added}


def install_codex_hook(home: Path) -> dict:
    base = home / ".codex"
    if not base.is_dir():
        return {"status": "skipped_not_found", "path": str(base)}
    path = base / "hooks.json"
    data = _read_json(path)
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = {}
        data["hooks"] = hooks

    wrapper = ensure_codex_wrapper(home)
    command = codex_wrapper_command(wrapper)
    entry = {"hooks": [{"type": "command", "command": command, "timeout": 20}]}
    added = [ev for ev in CODEX_EVENTS if _ensure_event(hooks, ev, json.loads(json.dumps(entry)))]
    if apply_marked_hook(hooks, CODEX_HINT_EVENT, HINT_MARKER, _codex_hint_cmd(), CODEX_HINT_TIMEOUT):
        added.append("skill-hint")
    feature = enable_codex_hooks_feature(home)
    blocked = feature["status"] if feature.get("warning") else None   # the user's hooks = false, or a config we cannot edit
    events = [*CODEX_EVENTS, CODEX_HINT_EVENT]

    if not added and not feature.get("changed"):
        return {
            "status": blocked or "already_installed",
            "path": str(path),
            "events": events,
            "wrapper": str(wrapper),
            "features": feature,
        }
    if added:
        _backup(path)
        _write_json(path, data)
    return {
        "status": blocked or "installed",
        "path": str(path),
        "events": events,
        "added": added,
        "wrapper": str(wrapper),
        "features": feature,
    }


_OPENCODE_PLUGIN_TEMPLATE = """// Managed by BosskuAI (`bossku hooks install`). Safe to delete; re-run to restore.
// Pushes .bossku/memory to the configured Obsidian vault when an OpenCode session goes idle.
import {{ spawn }} from "node:child_process";

const BOSSKU_ARGV = {argv};

export const BosskuSyncPlugin = async (input) => {{
  return {{
    event: (arg) => {{
      const ev = arg && arg.event;
      if (!ev || ev.type !== "session.idle") return;
      const cwd = input.directory || (input.project && input.project.worktree) || process.cwd();
      try {{
        const [bin, ...rest] = BOSSKU_ARGV;
        const child = spawn(bin, [...rest, "sync-hook", "--project", cwd], {{
          detached: true,
          stdio: "ignore",
        }});
        // A missing binary is reported on the child, not thrown: unhandled, it ends the host process.
        child.on("error", (e) => console.warn(`[bossku-sync] failed to run sync-hook: ${{e.message}}`));
        child.unref();
      }} catch (e) {{
        console.warn(`[bossku-sync] failed to spawn sync-hook: ${{e instanceof Error ? e.message : String(e)}}`);
      }}
    }},
  }};
}};

export default BosskuSyncPlugin;
"""


def install_opencode_plugin(home: Path) -> dict:
    base = home / ".config" / "opencode"
    if not base.is_dir():
        return {"status": "skipped_not_found", "path": str(base)}
    path = base / "plugins" / "bossku-sync.js"
    was_present = path.is_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_OPENCODE_PLUGIN_TEMPLATE.format(argv=json.dumps(resolve_bossku_argv())), encoding="utf-8")
    return {"status": "already_installed" if was_present else "installed", "path": str(path)}


_INSTALLERS = {
    "claude_code": install_claude_code_hook,
    "cursor": install_cursor_hook,
    "codex": install_codex_hook,
    "opencode": install_opencode_plugin,
}


def install_hooks(
    *,
    home: Path | None = None,
    tools: tuple[str, ...] | None = None,
    harness: bool = True,
    root: Path | None = None,
) -> dict:
    """Install the sync hooks. For claude_code the Node harness (gates and deny rules) comes with them, under
    the `claude_harness` key, when `harness` is true and `root` names the checkout whose hooks/ folder the
    commands point at. Without a root nothing is guessed: no harness is added, and a harness already in
    settings.json stays (with no Python verify-gate beside its Stop gate). `harness=False` is the opt-out: it also
    takes our Node gates and deny rules out of settings.json."""
    h = home if home is not None else Path.home()
    result: dict = {}
    for tool in tools or ALL_TOOLS:
        installer = _INSTALLERS.get(tool)
        if installer is None:
            result[tool] = {"status": "error", "message": f"unknown tool {tool!r}"}
            continue
        try:
            if tool == "claude_code":
                result[tool], gates = _install_claude(h, root if harness else None, harness_off=not harness)
                if gates is not None:
                    result["claude_harness"] = gates
            else:
                result[tool] = installer(h)
        except Exception as exc:  # noqa: BLE001 - one tool's failure must not abort the rest
            result[tool] = {"status": "error", "message": str(exc)}
    return result


# --- uninstall -----------------------------------------------------------

def uninstall_claude_code_hook(home: Path) -> dict:
    return _uninstall_claude(home)[0]


def _uninstall_claude(home: Path) -> tuple[dict, dict]:
    """(claude_code result, claude_harness result). Every piece is stripped in memory and written once,
    so one backup holds the state from before this run."""
    path = home / ".claude" / "settings.json"
    if not path.is_file():
        gone = {"status": "skipped_not_found", "path": str(path)}
        return gone, dict(gone)
    data = _read_json(path)
    hooks = data.get("hooks", {})
    hooks = hooks if isinstance(hooks, dict) else {}
    changed = _strip_events(hooks, (HINT_EVENT,), HINT_MARKER)
    changed |= _strip_events(hooks, (GATE_EVENT,), GATE_MARKER)
    changed |= _strip_events(hooks, (BRIEF_EVENT,), BRIEF_MARKER)
    changed |= _strip_events(hooks, CLAUDE_EVENTS)
    harness_changed = _strip_harness(data, hooks)
    if changed or harness_changed:
        _backup(path)
        _write_json(path, data)
    return ({"status": "removed" if changed else "not_installed", "path": str(path)},
            {"status": "removed" if harness_changed else "not_installed", "path": str(path)})


def uninstall_cursor_hook(home: Path) -> dict:
    path = home / ".cursor" / "hooks.json"
    if not path.is_file():
        return {"status": "skipped_not_found", "path": str(path)}
    data = _read_json(path)
    hooks = data.get("hooks", {})
    if not isinstance(hooks, dict) or not _strip_events(hooks, CURSOR_EVENTS):
        return {"status": "not_installed", "path": str(path)}
    _backup(path)
    data["hooks"] = hooks
    _write_json(path, data)
    return {"status": "removed", "path": str(path)}


def uninstall_codex_hook(home: Path) -> dict:
    path = home / ".codex" / "hooks.json"
    changed = False
    if path.is_file():
        data = _read_json(path)
        hooks = data.get("hooks", {})
        stripped = isinstance(hooks, dict) and _strip_events(hooks, CODEX_EVENTS)
        if isinstance(hooks, dict) and _strip_events(hooks, (CODEX_HINT_EVENT,), HINT_MARKER):   # only the skill-hint entries
            stripped = True
        if stripped:
            _backup(path)
            data["hooks"] = hooks
            _write_json(path, data)
            changed = True

    removed_wrappers: list[str] = []
    cfg = user_config_dir(home)
    for name in ("codex-sync-hook.sh", "codex-sync-hook.ps1"):
        wrapper = cfg / name
        if wrapper.is_file():
            wrapper.unlink()
            removed_wrappers.append(str(wrapper))
            changed = True

    if not changed:
        return {"status": "not_installed" if path.is_file() else "skipped_not_found", "path": str(path)}
    result: dict = {"status": "removed", "path": str(path)}
    if removed_wrappers:
        result["wrappers_removed"] = removed_wrappers
    return result


def uninstall_opencode_plugin(home: Path) -> dict:
    path = home / ".config" / "opencode" / "plugins" / "bossku-sync.js"
    if not path.is_file():
        return {"status": "skipped_not_found", "path": str(path)}
    path.unlink()
    return {"status": "removed", "path": str(path)}


_UNINSTALLERS = {
    "claude_code": uninstall_claude_code_hook,
    "cursor": uninstall_cursor_hook,
    "codex": uninstall_codex_hook,
    "opencode": uninstall_opencode_plugin,
}


def uninstall_hooks(*, home: Path | None = None, tools: tuple[str, ...] | None = None) -> dict:
    h = home if home is not None else Path.home()
    result: dict = {}
    for tool in tools or ALL_TOOLS:
        uninstaller = _UNINSTALLERS.get(tool)
        if uninstaller is None:
            result[tool] = {"status": "error", "message": f"unknown tool {tool!r}"}
            continue
        try:
            if tool == "claude_code":
                result[tool], result["claude_harness"] = _uninstall_claude(h)
            else:
                result[tool] = uninstaller(h)
        except Exception as exc:  # noqa: BLE001
            result[tool] = {"status": "error", "message": str(exc)}
    return result


# --- status (read-only, used by `bossku doctor`) --------------------------

def hooks_status(home: Path | None = None) -> dict:
    h = home if home is not None else Path.home()
    status: dict[str, bool] = {}

    claude_path = h / ".claude" / "settings.json"
    claude_hooks = _read_json(claude_path).get("hooks", {}) if claude_path.is_file() else {}
    status["claude_code"] = isinstance(claude_hooks, dict) and _events_complete(claude_hooks, CLAUDE_EVENTS)

    cursor_path = h / ".cursor" / "hooks.json"
    cursor_hooks = _read_json(cursor_path).get("hooks", {}) if cursor_path.is_file() else {}
    status["cursor"] = isinstance(cursor_hooks, dict) and _events_complete(cursor_hooks, CURSOR_EVENTS)

    codex_path = h / ".codex" / "hooks.json"
    codex_hooks = _read_json(codex_path).get("hooks", {}) if codex_path.is_file() else {}
    status["codex"] = isinstance(codex_hooks, dict) and _events_complete(codex_hooks, CODEX_EVENTS)

    status["opencode"] = (h / ".config" / "opencode" / "plugins" / "bossku-sync.js").is_file()
    return status


def codex_hint_commands(home: Path | None = None) -> list[str]:
    """The commands of the skill-hint hook in ~/.codex/hooks.json; empty when it is not wired. Read-only."""
    h = home if home is not None else Path.home()
    path = h / ".codex" / "hooks.json"
    try:
        hooks = _read_json(path).get("hooks") if path.is_file() else None
    except (OSError, ValueError, AttributeError):
        return []
    bucket = hooks.get(CODEX_HINT_EVENT) if isinstance(hooks, dict) else None
    return _commands([e for e in bucket if _owned(e, HINT_MARKER)]) if isinstance(bucket, list) else []


# --- the hook entrypoint itself (`bossku sync-hook`) -----------------------

def read_hook_stdin() -> str:
    """The hook payload as UTF-8 text: a Windows pipe would otherwise decode it with the console code page."""
    if sys.stdin.isatty():
        return ""
    raw = getattr(sys.stdin, "buffer", None)
    return raw.read().decode("utf-8", errors="replace") if raw is not None else sys.stdin.read()


def _payload_project(payload) -> tuple[Path | None, bool]:
    """(folder, named): the existing folder a hook payload points at, and whether it named any folder at all.
    Claude and Codex send cwd. Cursor sends workspace_roots, where a root that already has notes wins."""
    if not isinstance(payload, dict):
        return None, False
    cwd, roots = payload.get("cwd"), payload.get("workspace_roots")
    if not cwd and not roots:
        return None, False
    if isinstance(cwd, str) and Path(cwd).is_dir():
        return Path(cwd), True
    dirs = [Path(r) for r in roots if isinstance(r, str) and Path(r).is_dir()] if isinstance(roots, list) else []
    return next((d for d in dirs if (d / ".bossku" / "memory").is_dir()), dirs[0] if dirs else None), True


def run_sync_hook(*, project: Path | None = None, home: Path | None = None) -> dict:
    cwd = project
    if cwd is None:
        try:
            payload = json.loads(read_hook_stdin() or "{}")
        except (json.JSONDecodeError, OSError):
            payload = {}
        cwd, named = _payload_project(payload)
        if cwd is None and named:   # a bad path must not turn into a sync of whatever folder the hook runs in
            return {"status": "skipped", "reason": "the hook payload names no existing folder"}
    if cwd is None:
        cwd = Path.cwd()
    try:
        return sync_project(cwd, home=home)
    except Exception as exc:  # noqa: BLE001 - a safety-net hook must never break the caller's session
        return {"status": "error", "reason": str(exc)}
