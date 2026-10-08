"""Keep everything an agent learns in one tidy place: the Obsidian vault.

`sync` mirrors what lives elsewhere into <vault>/BosskuAI/ without ever touching the originals:
  - Claude Code's own auto-memory for the project (and its sub-repos and worktrees),
  - the rules files that steer the agents (global CLAUDE.md, a project's CLAUDE.md and AGENTS.md, .claude/rules),
  - notes in legacy .bossku/memory folders,
and writes an Index.md that links it all. `tidy` plans (and with apply=True performs) a clean-up of the folders that
earlier versions scattered. Nothing is ever deleted: notes are merged or moved to _archive, and a zip of the whole
BosskuAI folder is taken first. The only thing removed is a folder with no file anywhere inside it.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from bossku.memory import KIND_TO_FILE, load_user_config, memory_project_root
from bossku.paths import user_config_dir
from bossku.redact import redact

NOTE_FILES = tuple(KIND_TO_FILE.values()) + ("handoff.md",)
THROTTLE_SECONDS = 60
ARCHIVE = "_archive"


def _slug(path: Path | str) -> str:
    """The folder name Claude Code gives a working directory: every non-alphanumeric character becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def base_dir(cfg: dict) -> Path | None:
    vault = cfg.get("obsidian_vault")
    if not vault or not Path(vault).is_dir():
        return None
    return Path(vault) / "BosskuAI"


def _state_path(home: Path | None) -> Path:
    return user_config_dir(home) / "vault-sync-state.json"


def _load_state(home: Path | None) -> dict:
    try:
        return json.loads(_state_path(home).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_state(state: dict, home: Path | None) -> None:
    path = _state_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=1), encoding="utf-8")


def _mirror(src: Path, dest: Path, state: dict, label: str) -> bool:
    """Copy src to dest with a header that says where it came from. True when the vault copy changed."""
    try:
        body = src.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    body = redact(body)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    key = str(dest)
    if state.get(key) == digest and dest.is_file():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    header = (f"---\nmirror_of: {src}\nsource: {label}\nsynced: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}\n"
              "note: automatic copy, edit the original; changes here are overwritten\n---\n\n")
    dest.write_text(header + body, encoding="utf-8")
    state[key] = digest
    return True


def _claude_project_dirs(root: Path, home_dir: Path) -> list[tuple[str, Path]]:
    """Claude Code project folders for this root and the sub-repos and worktrees under it: (suffix, folder)."""
    projects = home_dir / ".claude" / "projects"
    if not projects.is_dir():
        return []
    prefix = _slug(root).lower()
    found = []
    for entry in projects.iterdir():
        name = entry.name.lower()
        if entry.is_dir() and (name == prefix or name.startswith(prefix + "-")):
            found.append((entry.name[len(prefix):].lstrip("-") or "root", entry))
    return sorted(found)


def sync(project: Path, *, home: Path | None = None, force: bool = False) -> dict:
    """Mirror auto-memory, rules and legacy notes for this project into the vault, then refresh the index."""
    cfg = load_user_config(home)
    base = base_dir(cfg)
    if base is None:
        return {"status": "skipped", "reason": "no vault configured or vault unavailable"}
    state = _load_state(home)
    now = time.time()
    if not force and now - state.get("_last_run", 0) < THROTTLE_SECONDS:
        return {"status": "throttled"}
    root = memory_project_root(project, home=home)
    namespaces = cfg.get("memory_project_namespaces") or {}
    ns = next((n for r, n in namespaces.items() if Path(r).resolve() == root), root.name)
    changed: list[str] = []

    def mirror(src: Path, dest: Path, label: str) -> None:
        if src.is_file() and _mirror(src, dest, state, label):
            changed.append(str(dest.relative_to(base)))

    home_dir = home or Path.home()
    for suffix, folder in _claude_project_dirs(root, home_dir):
        memory = folder / "memory"
        if memory.is_dir():
            for note in sorted(memory.glob("*.md")):
                mirror(note, base / ns / "claude-memory" / suffix / note.name, "Claude Code auto-memory")
    for src, name in ((home_dir / ".claude" / "CLAUDE.md", "claude-CLAUDE.md"),
                      (home_dir / ".codex" / "AGENTS.md", "codex-AGENTS.md"),
                      (home_dir / ".config" / "opencode" / "AGENTS.md", "opencode-AGENTS.md")):
        mirror(src, base / "_global" / "rules" / name, "global rules")
    for name in ("CLAUDE.md", "AGENTS.md"):
        mirror(root / name, base / ns / "rules" / name, "project rules")
    rules_dir = root / ".claude" / "rules"
    if rules_dir.is_dir():
        for rule in sorted(rules_dir.glob("*.md")):
            mirror(rule, base / ns / "rules" / "claude-rules" / rule.name, "project rules")
    legacy = root / ".bossku" / "memory"
    if legacy.is_dir():
        for name in NOTE_FILES:
            mirror(legacy / name, base / ns / "imported" / "repo-memory" / name, "legacy .bossku/memory")
    if write_index(base):
        changed.append("Index.md")
    state["_last_run"] = now
    _save_state(state, home)
    return {"status": "ok", "namespace": ns, "changed": changed}


def write_index(base: Path) -> bool:
    """A table of contents of every project folder, with links. True when it changed."""
    lines = ["---", "generated: true", "---", "", "# Bossku Superpower memory", "",
             "Notes, learnings, decisions and rules saved by your agents. This page is rewritten automatically.", ""]
    sections = []
    for folder in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        notes = sorted(p for p in folder.rglob("*.md") if p.name not in ("Index.md",) and ".conflict" not in p.name)
        if not notes:
            continue
        links = [f"- [[{p.relative_to(base).with_suffix('').as_posix()}|{p.relative_to(folder).as_posix()}]]" for p in notes]
        sections.append(f"## {folder.name}\n\n" + "\n".join(links))
    glob = sorted((base / "_global").rglob("*.md")) if (base / "_global").is_dir() else []
    if glob:
        sections.append("## Global\n\n" + "\n".join(
            f"- [[{p.relative_to(base).with_suffix('').as_posix()}|{p.relative_to(base / '_global').as_posix()}]]" for p in glob))
    text = "\n".join(lines) + "\n" + "\n\n".join(sections) + "\n"
    target = base / "Index.md"
    if target.is_file() and target.read_text(encoding="utf-8") == text:
        return False
    target.write_text(text, encoding="utf-8")
    return True


# ---------------------------------------------------------------- tidy

def _files(folder: Path) -> list[Path]:
    return [p for p in folder.rglob("*") if p.is_file()]


def _entries(text: str) -> tuple[str, list[str]]:
    """Split a notes file into its title line and its '## timestamp' entries."""
    head, *parts = re.split(r"(?m)^(?=## )", text)
    return head.rstrip(), [part.rstrip() for part in parts if part.strip()]


def merge_notes(existing: str, incoming: str) -> str:
    """Union of two notes files: every entry of both, none twice, oldest first."""
    title, mine = _entries(existing)
    other_title, theirs = _entries(incoming)
    seen = {re.sub(r"\s+", " ", e.split("\n", 1)[-1]).strip() for e in mine}
    merged = list(mine)
    for entry in theirs:
        body = re.sub(r"\s+", " ", entry.split("\n", 1)[-1]).strip()
        if body not in seen:
            seen.add(body)
            merged.append(entry)
    merged.sort(key=lambda e: e.split("\n", 1)[0])
    return (title or other_title).rstrip() + "\n\n" + "\n\n".join(merged) + "\n"


def plan_tidy(*, home: Path | None = None) -> list[dict]:
    """What a clean-up would do, as a list of {action, source, target, why}. Changes nothing."""
    cfg = load_user_config(home)
    base = base_dir(cfg)
    if base is None:
        return []
    roots = [Path(r) for r in cfg.get("memory_project_roots") or []]
    plan: list[dict] = []
    # sub-repo names under each configured root, e.g. TMS -> backend, frontend, tms-owner-web
    owners: list[tuple[str, str]] = []
    for root in roots:
        if root.is_dir():
            owners += [(child.name.lower(), root.name) for child in root.iterdir() if child.is_dir() and not child.name.startswith(".")]
    for folder in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        files = _files(folder)
        if not files:
            plan.append({"action": "remove-empty-folder", "source": str(folder), "target": "", "why": "no file inside it"})
            continue
        conflicts = [f for f in files if ".conflict" in f.name]
        for f in conflicts:
            plan.append({"action": "archive", "source": str(f), "target": str(base / ARCHIVE / "conflicts" / folder.name / f.name),
                         "why": "backup the old export made when the vault copy had been edited"})
        real = [f for f in files if f not in conflicts]
        if not real:
            continue
        low = folder.name.lower()
        parent = next((ns for name, ns in sorted(owners, key=lambda o: -len(o[0])) if low == name or low.startswith(name + "-")), None)
        if parent and parent != folder.name and (base / parent).is_dir():
            sub = folder.name
            for f in real:
                if f.name in NOTE_FILES:
                    plan.append({"action": "merge", "source": str(f), "target": str(base / parent / "repos" / sub / f.name),
                                 "why": f"belongs to {parent} (a folder inside its project root)"})
                else:
                    plan.append({"action": "move", "source": str(f), "target": str(base / parent / "repos" / sub / f.relative_to(folder)),
                                 "why": f"belongs to {parent}"})
        elif re.fullmatch(r"[0-9a-f]{10,16}", folder.name):
            for f in real:
                plan.append({"action": "archive", "source": str(f), "target": str(base / ARCHIVE / "unsorted" / folder.name / f.name),
                             "why": "a hash-named folder: leftover from a throwaway or benchmark project"})
        elif re.fullmatch(r"g-p-[0-9a-f]{20,}", folder.name) or len(folder.name) <= 3:
            for f in real:
                plan.append({"action": "move", "source": str(f), "target": str(base / "_unsorted" / folder.name / f.name),
                             "why": "a generated or very short project name: decide which project it belongs to"})
    for root in roots:
        legacy = root / ".bossku" / "memory"
        for sub in [root, *[c for c in root.iterdir() if c.is_dir()]] if root.is_dir() else []:
            memory = sub / ".bossku" / "memory"
            for name in NOTE_FILES:
                if (memory / name).is_file() and (memory / name).stat().st_size > 0:
                    plan.append({"action": "import", "source": str(memory / name),
                                 "target": str(base / root.name / "repos" / (sub.name if sub != root else "_root") / name),
                                 "why": "notes stored outside the vault (the original is left in place)"})
    return plan


def backup(base: Path, home: Path | None = None) -> Path:
    target = user_config_dir(home) / "backups"
    target.mkdir(parents=True, exist_ok=True)
    zip_path = target / f"vault-BosskuAI-{datetime.now():%Y%m%d-%H%M%S}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for f in base.rglob("*"):
            if f.is_file():
                archive.write(f, f.relative_to(base.parent).as_posix())
    return zip_path


def apply_tidy(plan: list[dict], *, home: Path | None = None) -> dict:
    cfg = load_user_config(home)
    base = base_dir(cfg)
    if base is None:
        return {"status": "skipped"}
    zip_path = backup(base, home)
    done = {"merge": 0, "move": 0, "archive": 0, "import": 0, "remove-empty-folder": 0}
    for step in plan:
        src, dest = Path(step["source"]), Path(step["target"]) if step["target"] else None
        action = step["action"]
        if action == "remove-empty-folder":
            if src.is_dir() and not _files(src):
                shutil.rmtree(src)
                done[action] += 1
            continue
        if not src.is_file() or dest is None:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if action in ("merge", "import") and dest.is_file():
            dest.write_text(merge_notes(dest.read_text(encoding="utf-8"), src.read_text(encoding="utf-8")), encoding="utf-8")
        elif action in ("merge", "import"):
            shutil.copyfile(src, dest)
        else:
            if dest.exists():
                dest = dest.with_name(f"{dest.stem}.{int(time.time())}{dest.suffix}")
            shutil.move(str(src), str(dest))
            done[action] += 1
            continue
        if action == "merge":     # keep the original: it moves to the archive once its entries are in the target
            keep = base / ARCHIVE / "merged" / src.parent.name
            keep.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(keep / src.name))
        done[action] += 1
    for folder in sorted((p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))), key=lambda p: p.name):
        if not _files(folder):
            shutil.rmtree(folder)
            done["remove-empty-folder"] += 1
    write_index(base)
    return {"status": "ok", "backup": str(zip_path), "done": done}
