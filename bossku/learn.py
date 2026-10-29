"""Learned skills: lessons an agent distils from real sessions, kept with the project notes (the Obsidian vault).

The agent only proposes. `bossku learn apply <intent.json>` is the one writer: it lints the intent, and on pass writes
the skill under `<memory_dir>/skills/<name>/` with temp files and `os.replace`. It changes only skills that carry
`learned: true`, never deletes (an archive moves the folder to `skills/.archive/`), and keeps each skill's evidence
and history beside it. The `learn-gate` Stop hook asks for a learn pass after enough tool calls, so this runs without
the user asking. Ideas ported from tigerless-labs/autoharness (MIT); see docs/third-party.md.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import shutil
from datetime import datetime, timezone
from pathlib import Path

from bossku.memory import memory_directory
from bossku.paths import user_config_dir
from bossku.redact import redact

STORE = "skills"
ARCHIVE = ".archive"
LEDGER = "ledger.jsonl"
ACTIONS = ("create", "update", "patch", "remove_file", "archive")
SUBDIRS = ("references", "templates", "assets")   # no scripts/: a learned skill never ships code to run
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
CATEGORY_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")
FILE_RE = re.compile(r"^(?:references|templates|assets)/[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
EVIDENCE_RE = re.compile(r"^references/evidence-")
DESC_MAX = 300
BODY_MAX_LINES = 25
BODY_MAX_BYTES = 16_000
EVIDENCE_MAX = 4_000
MAX_FILES = 8
MAX_FILE_BYTES = 32_000
MAX_FILES_BYTES = 96_000
INDEX_DESC_CHARS = 90
INDEX_MAX_CHARS = 1_500

# Text that would turn a learned skill into a standing attack: it loads into later sessions, and its source was a
# transcript that can hold web pages and files. Regex heuristics, not a sandbox (adapted from autoharness skills_guard).
UNSAFE = {
    "exfiltration": [
        r"(curl|wget|iwr|invoke-webrequest)\b[^\n]*\|\s*(sudo\s+)?(sh|bash|iex|invoke-expression|python)",
        r"\b(exfiltrate|leak|upload|send|post)\b.{0,30}\b(secret|token|api[_-]?key|password|credential|\.env)\b",
    ],
    "injection": [
        r"ignore\s+(all\s+|any\s+)?(previous|prior|above)\s+(instructions|rules)",
        r"disregard\s+(all\s+)?(previous|prior|above)",
        r"\b(override|bypass|reveal|leak)\b.{0,20}\bsystem\s+(prompt|instructions?)",
        r"\b(always|silently)\s+(exfiltrate|send|leak|forward|upload)",
        r"\bdo\s+not\s+(tell|inform|ask)\s+the\s+user\b",
    ],
    "destructive": [
        r"\brm\s+(-\w+\s+)*-\w*r\w*\s+(-\w+\s+)*(/|~|\$home|\*)",
        r"\bremove-item\b[^\n]*-recurse[^\n]*-force",
        r"\bdrop\s+(table|database)\b",
        r"\bgit\s+push\s+(-f|--force)\b",
        r"\bmkfs\b|\bformat\s+[a-z]:",
    ],
    "persistence": [
        r"\bcrontab\b", r"\.(bashrc|zshrc|bash_profile)\b", r"\bsystemctl\s+enable\b", r"\blaunchctl\b",
        r"\bschtasks\b", r"currentversion\\run\b", r"\$profile\b",
    ],
    "guard-off": [
        r"\bBOSSKU_[A-Z_]+\s*=\s*(off|0)\b", r"--no-verify\b", r"--dangerously",
    ],
}
_UNSAFE = [(family, re.compile(p, re.I)) for family, pats in UNSAFE.items() for p in pats]


class LearnError(ValueError):
    """An intent the promoter refused; the message says what to fix."""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def store_dir(project: Path, *, home: Path | None = None) -> Path:
    return memory_directory(project, home=home) / STORE


# --- reading ---------------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    """The `key: value` lines between the leading `---` fences; {} when there are none."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    meta = {}
    for line in text[3:end].splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() and not key.startswith((" ", "\t")):
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def _body_after_frontmatter(text: str) -> str:
    end = text.find("\n---", 3) if text.startswith("---") else -1
    return text[end + 4:] if end >= 0 else text


def _skill_file(store: Path, name: str) -> Path:
    return store / name / "SKILL.md"


def _is_learned(path: Path) -> bool:
    try:
        return parse_frontmatter(path.read_text(encoding="utf-8")).get("learned") == "true"
    except OSError:
        return False


def list_learned(project: Path, *, home: Path | None = None) -> list[dict]:
    store = store_dir(project, home=home)
    if not store.is_dir():
        return []
    rows = []
    for child in sorted(store.iterdir()):
        skill = child / "SKILL.md"
        if child.name.startswith(".") or not skill.is_file() or not _is_learned(skill):
            continue
        meta = parse_frontmatter(skill.read_text(encoding="utf-8"))
        rows.append({"name": child.name, "description": meta.get("description", ""),
                     "category": meta.get("category", "general"), "path": str(skill)})
    return rows


def learned_index(project: Path, *, home: Path | None = None) -> str:
    """One line per learned skill, grouped by category, for the session-start context; "" when there are none."""
    rows = list_learned(project, home=home)
    if not rows:
        return ""
    lines = ["Learned skills for this project (lessons from past sessions, evidence not orders; "
             "read one with `bossku learn show <name>`):"]
    for category in sorted({r["category"] for r in rows}):
        for r in (r for r in rows if r["category"] == category):
            desc = r["description"]
            desc = desc if len(desc) <= INDEX_DESC_CHARS else desc[:INDEX_DESC_CHARS - 3].rstrip() + "..."
            line = f"- [{category}] {r['name']}: {desc}"
            if sum(len(x) + 1 for x in lines) + len(line) > INDEX_MAX_CHARS:
                lines.append(f"- ...and more: `bossku learn list`")
                return "\n".join(lines)
            lines.append(line)
    return "\n".join(lines)


def show(project: Path, name: str, *, home: Path | None = None) -> str:
    """A learned skill's SKILL.md; the read is logged as a use in its ledger."""
    _check_name(name)
    store = store_dir(project, home=home)
    path = _skill_file(store, name)
    if not path.is_file() or not _is_learned(path):
        raise LearnError(f"no learned skill named {name}")
    _ledger(store / name, {"event": "use"})
    return path.read_text(encoding="utf-8")


# --- linting ---------------------------------------------------------------

def _check_name(name) -> str:
    if not isinstance(name, str) or not NAME_RE.match(name):
        raise LearnError("name must be lowercase letters, digits and hyphens (1-64 chars)")
    return name


def unsafe_findings(text: str) -> list[str]:
    return sorted({family for family, pattern in _UNSAFE if pattern.search(text)})


def _scan(label: str, text: str) -> None:
    hits = unsafe_findings(text)
    if hits:
        raise LearnError(f"{label} looks unsafe ({', '.join(hits)}); a learned skill must not carry that")
    if redact(text) != text:
        raise LearnError(f"{label} holds what looks like a secret; remove it")


def _pointed(body: str, rel: str) -> bool:
    return rel in body


def lint_skill(name: str, text: str, files: dict[str, str], kept: dict[str, str] | None = None) -> None:
    """Raise LearnError on the first problem with a full SKILL.md, the subfiles this intent adds (`files`, each must be
    pointed at) and the ones already on disk (`kept`, counted against the size budget; a pointer may be patched out
    first and the file removed by the next intent)."""
    if len(text.encode("utf-8")) > BODY_MAX_BYTES:
        raise LearnError(f"SKILL.md is over {BODY_MAX_BYTES} bytes")
    meta = parse_frontmatter(text)
    if not meta:
        raise LearnError("SKILL.md needs frontmatter: name, description, category, learned: true")
    if meta.get("name") != name:
        raise LearnError(f"frontmatter name must be {name}")
    if meta.get("learned") != "true":
        raise LearnError("frontmatter must say learned: true")
    if not CATEGORY_RE.match(meta.get("category", "")):
        raise LearnError("frontmatter category must be one lowercase word or hyphenated phrase")
    desc = meta.get("description", "")
    if not desc.startswith("Use when") or not desc.endswith("."):
        raise LearnError("description must start with 'Use when' (the trigger) and be one sentence ending in '.'")
    if len(desc) > DESC_MAX:
        raise LearnError(f"description is {len(desc)} chars; keep it to {DESC_MAX}")
    body = _body_after_frontmatter(text)
    lines = [line for line in body.splitlines() if line.strip()]
    if not lines:
        raise LearnError("SKILL.md body is empty")
    if len(lines) > BODY_MAX_LINES:
        raise LearnError(f"body is {len(lines)} non-blank lines (> {BODY_MAX_LINES}); state the rule, "
                         "move detail to references/")
    _scan("SKILL.md", text)
    for rel in files:
        if not _pointed(body, rel):
            raise LearnError(f"{rel} is not referenced from SKILL.md; point to it or drop it")
    merged = {**(kept or {}), **files}
    # evidence files are promoter-owned provenance: never counted against the budget
    total = sum(len(c.encode("utf-8")) for rel, c in merged.items() if not EVIDENCE_RE.match(rel))
    if total > MAX_FILES_BYTES:
        raise LearnError(f"subfiles are over {MAX_FILES_BYTES} bytes in total")


def _check_files(files) -> dict[str, str]:
    if files is None:
        return {}
    if not isinstance(files, dict) or len(files) > MAX_FILES:
        raise LearnError(f"files must be a map of at most {MAX_FILES} relative paths to text")
    clean = {}
    for rel, content in files.items():
        if not isinstance(rel, str) or not FILE_RE.match(rel) or ".." in rel:
            raise LearnError(f"bad subfile path {rel!r}: use references/, templates/ or assets/ plus a plain file name")
        if EVIDENCE_RE.match(rel):
            raise LearnError(f"{rel}: evidence files are written by the promoter only")
        if not isinstance(content, str) or len(content.encode("utf-8")) > MAX_FILE_BYTES:
            raise LearnError(f"{rel} must be text under {MAX_FILE_BYTES} bytes")
        _scan(rel, content)
        clean[rel] = content
    return clean


def _existing_files(skill_dir: Path) -> dict[str, str]:
    found = {}
    for sub in SUBDIRS:
        folder = skill_dir / sub
        if folder.is_dir():
            for f in folder.iterdir():
                if f.is_file():
                    found[f"{sub}/{f.name}"] = f.read_text(encoding="utf-8", errors="replace")
    return found


# --- writing ---------------------------------------------------------------

def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{secrets.token_hex(4)}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _ledger(skill_dir: Path, entry: dict) -> None:
    entry = {"at": _now().strftime("%Y-%m-%dT%H:%M:%SZ"), **entry}
    with open(skill_dir / LEDGER, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _evidence(skill_dir: Path, action: str, reason: str, evidence: str) -> str:
    stamp = _now().strftime("%Y%m%dT%H%M%S") + "-" + secrets.token_hex(2)
    rel = f"references/evidence-{stamp}.md"
    _write_atomic(skill_dir / rel, f"# Evidence ({action})\n\nReason: {redact(reason)}\n\n> "
                  + redact(evidence).replace("\n", "\n> ") + "\n")
    return rel


def _require_text(intent: dict, key: str, limit: int) -> str:
    value = intent.get(key)
    if not isinstance(value, str) or not value.strip():
        raise LearnError(f"{key} is required")
    if len(value) > limit:
        raise LearnError(f"{key} is over {limit} chars")
    return value


def apply_intent(project: Path, intent: dict, *, home: Path | None = None) -> dict:
    """Validate one intent and land it. Raises LearnError (nothing written) when it fails a check."""
    if not isinstance(intent, dict):
        raise LearnError("an intent is a JSON object")
    action = intent.get("action")
    if action not in ACTIONS:
        raise LearnError(f"action must be one of {', '.join(ACTIONS)}")
    name = _check_name(intent.get("name"))
    reason = _require_text(intent, "reason", 500)
    evidence = _require_text(intent, "evidence", EVIDENCE_MAX)
    for label, text in (("reason", reason), ("evidence", evidence)):
        hits = unsafe_findings(text)
        if hits:
            raise LearnError(f"{label} looks unsafe ({', '.join(hits)})")
    store = store_dir(project, home=home)
    skill_dir = store / name
    skill = skill_dir / "SKILL.md"
    exists = skill.is_file()
    if exists and not _is_learned(skill):
        raise LearnError(f"{name} is not a learned skill; the promoter only changes skills it wrote")
    if action != "create" and not exists:
        raise LearnError(f"no learned skill named {name}")
    result = {"action": action, "name": name}

    if action == "create" and (exists or skill_dir.exists()):
        raise LearnError(f"{name} already exists; patch or update it instead")
    if action in ("create", "update"):
        text = _require_text(intent, "body", BODY_MAX_BYTES)
        files = _check_files(intent.get("files"))
        kept = {} if action == "create" else _existing_files(skill_dir)
        lint_skill(name, text, files, kept)
        for rel, content in files.items():
            _write_atomic(skill_dir / rel, content)
        _write_atomic(skill, text)
        result["files"] = sorted(files)
    elif action == "patch":
        old = _require_text(intent, "old_string", BODY_MAX_BYTES)
        new = intent.get("new_string")
        if not isinstance(new, str):
            raise LearnError("new_string is required (it may be empty)")
        live = skill.read_text(encoding="utf-8")
        if live.count(old) != 1:
            raise LearnError("old_string must match the live SKILL.md exactly once")
        text = live.replace(old, new, 1)
        lint_skill(name, text, {}, _existing_files(skill_dir))
        _write_atomic(skill, text)
    elif action == "remove_file":
        rel = intent.get("path")
        if not isinstance(rel, str) or not FILE_RE.match(rel) or ".." in rel or EVIDENCE_RE.match(rel):
            raise LearnError("path must be a references/, templates/ or assets/ file the agent wrote")
        target = skill_dir / rel
        if not target.is_file():
            raise LearnError(f"{rel} does not exist")
        if _pointed(_body_after_frontmatter(skill.read_text(encoding="utf-8")), rel):
            raise LearnError(f"SKILL.md still points to {rel}; patch the pointer out first")
        _archive_path(store, target, f"{name}-{rel.replace('/', '-')}")
    else:   # archive
        absorbed = intent.get("absorbed_into")
        if absorbed:
            _check_name(absorbed)
            umbrella = _skill_file(store, absorbed)
            if absorbed == name or not umbrella.is_file() or not _is_learned(umbrella):
                raise LearnError(f"absorbed_into must name another live learned skill, not {absorbed!r}")
            result["absorbed_into"] = absorbed
        rel_ev = _evidence(skill_dir, action, reason, evidence)
        _ledger(skill_dir, {"event": action, "reason": redact(reason), "evidence": rel_ev,
                            "absorbed_into": absorbed or None})
        result["archived_to"] = str(_archive_path(store, skill_dir, name))
        return result

    rel_ev = _evidence(skill_dir, action, reason, evidence)
    _ledger(skill_dir, {"event": action, "reason": redact(reason), "evidence": rel_ev})
    result["path"] = str(skill)
    return result


def _archive_path(store: Path, source: Path, label: str) -> Path:
    """Move a skill folder or one subfile out of recall. Moving it back revives it; nothing is deleted."""
    dest = store / ARCHIVE / f"{label}-{_now().strftime('%Y%m%dT%H%M%S')}-{secrets.token_hex(2)}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(dest))
    return dest


def apply_file(project: Path, intent_path: Path, *, home: Path | None = None) -> dict:
    """`bossku learn apply`: one intent object, or a list applied in order (stops at the first refusal)."""
    data = json.loads(Path(intent_path).read_text(encoding="utf-8"))
    intents = data if isinstance(data, list) else [data]
    landed = []
    for i, intent in enumerate(intents):
        try:
            landed.append(apply_intent(project, intent, home=home))
        except LearnError as exc:
            return {"ok": False, "landed": landed, "rejected": {"index": i, "error": str(exc)}}
    return {"ok": True, "landed": landed}


# --- the auto-learn Stop hook --------------------------------------------

EVERY_N = 50          # tool calls between learn passes (BOSSKU_LEARN_EVERY_N)
CONSOLIDATE_EVERY = 5  # every 5th pass is a consolidation pass
GATE_STATE = "learn-gate.json"
GATE_KEEP = 200        # sessions remembered in the gate state
MARKER = "[bossku-learn]"
_TOOL_USE = re.compile(rb'"type":\s?"tool_use"')

LEARN_REASON = (
    MARKER + " Auto-learn: this session made {n} tool calls since the last learn pass. Before you finish, run the "
    "`bosskuai-learn` pass (`bossku skills show bosskuai-learn` if it is not listed): turn each durable, reusable "
    "lesson from this session into a learned skill with `bossku learn apply <intent.json>` (check `bossku learn list` "
    "first and patch an existing one before creating), and save decisions or facts with `bossku remember`. A review "
    "finding that keeps coming back (the same kind of fix after more than one `Review:` line) is such a lesson. If nothing "
    "is worth keeping, say so in one line and finish. Off switch for the user: BOSSKU_AUTO_LEARN=off."
)
CONSOLIDATE_REASON = (
    MARKER + " Auto-learn consolidation pass: before you finish, run the consolidation section of `bosskuai-learn` "
    "(`bossku skills show bosskuai-learn` if it is not listed): read `bossku learn list`, fold near-duplicate learned "
    "skills into one class-level skill (patch the umbrella, then archive each sibling with absorbed_into), fix any "
    "rule that a newer one contradicts, then learn from this session as usual. If the library is already clean, say "
    "so in one line and finish. Off switch for the user: BOSSKU_AUTO_LEARN=off."
)


def auto_learn_off() -> bool:
    return os.environ.get("BOSSKU_AUTO_LEARN", "on").strip().lower() in ("off", "0", "false", "no")


def _every_n() -> int:
    try:
        return max(5, int(os.environ.get("BOSSKU_LEARN_EVERY_N", EVERY_N)))
    except ValueError:
        return EVERY_N


def _count_tool_calls(path: str) -> int:
    """Tool calls in a Claude Code transcript, counted on the raw bytes in 1 MiB blocks (no JSON parse, any size).
    A match never spans lines, so each block is cut after its last newline and the rest carried to the next."""
    count, carry = 0, b""
    with open(path, "rb") as fh:
        while True:
            block = fh.read(1 << 20)
            data = carry + block
            if not block:
                return count + len(_TOOL_USE.findall(data))
            cut = data.rfind(b"\n") + 1
            count += len(_TOOL_USE.findall(data, 0, cut))
            carry = data[cut:]


def _load_gate_state(home: Path | None) -> dict:
    try:
        data = json.loads((user_config_dir(home) / GATE_STATE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"passes": 0, "sessions": {}}
    if not isinstance(data, dict) or not isinstance(data.get("sessions"), dict):
        return {"passes": 0, "sessions": {}}
    return data


def _save_gate_state(state: dict, home: Path | None) -> None:
    sessions = state["sessions"]
    if len(sessions) > GATE_KEEP:   # drop the oldest
        for key in sorted(sessions, key=lambda k: str(sessions[k].get("at", "")))[: len(sessions) - GATE_KEEP]:
            del sessions[key]
    _write_atomic(user_config_dir(home) / GATE_STATE, json.dumps(state))


def learn_gate_output(payload_text: str, *, home: Path | None = None) -> dict:
    """What the `learn-gate` Stop hook prints: a block asking for a learn pass once every N tool calls, else nothing.
    Never raises, never blocks a stop that another hook already blocked (no loops), never blocks twice per window."""
    if auto_learn_off():
        return {}
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
        if not isinstance(payload, dict) or payload.get("stop_hook_active"):
            return {}
        path, session = payload.get("transcript_path"), payload.get("session_id")
        if not isinstance(path, str) or not path or not isinstance(session, str) or not session:
            return {}
        calls = _count_tool_calls(path)
        state = _load_gate_state(home)
        seen = state["sessions"].get(session) or {}
        since = calls - int(seen.get("calls", 0))
        if since < _every_n():
            return {}
        passes = int(state.get("passes", 0)) + 1
        state["passes"] = passes
        state["sessions"][session] = {"calls": calls, "at": _now().strftime("%Y-%m-%dT%H:%M:%SZ")}
        _save_gate_state(state, home)
    except Exception:  # noqa: BLE001 - a reminder is a convenience: whatever goes wrong, let the agent finish
        return {}
    reason = CONSOLIDATE_REASON if passes % CONSOLIDATE_EVERY == 0 else LEARN_REASON.format(n=since)
    return {"decision": "block", "reason": reason}
