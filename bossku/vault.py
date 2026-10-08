"""Keep everything an agent learns in one tidy place: the Obsidian vault.

`sync` mirrors what lives elsewhere into <vault>/BosskuAI/ without ever touching the originals:
  - Claude Code's own auto-memory for the project (and its sub-repos and worktrees),
  - the rules files that steer the agents (global CLAUDE.md, a project's CLAUDE.md and AGENTS.md, .claude/rules),
  - notes in legacy .bossku/memory folders,
and writes an Index.md that links it all. `tidy` plans (and with apply=True performs) a clean-up of the folders that
earlier versions scattered. Nothing is ever deleted: notes are merged or moved to _archive (a name already taken gets a
number), and a zip of the whole BosskuAI folder is taken first. The only thing removed is a folder with no file anywhere
inside it. A folder is only ever treated as part of a project when its name is exactly the name of a folder inside that
project's configured root; everything else is left where it is.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from bossku.memory import KIND_TO_FILE, load_user_config, memory_project_root
from bossku.paths import user_config_dir, vault_export_dir
from bossku.redact import redact

NOTE_FILES = tuple(KIND_TO_FILE.values()) + ("handoff.md",)
THROTTLE_SECONDS = 60
ARCHIVE = "_archive"
CONFLICT = re.compile(r"\.md\.conflict(\.\d+)?\.md$")


def _slug(path: Path | str) -> str:
    """The folder name Claude Code gives a working directory: every non-alphanumeric character becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def base_dir(cfg: dict) -> Path | None:
    vault = cfg.get("obsidian_vault")
    if not vault or not Path(vault).is_dir():
        return None
    return Path(vault) / "BosskuAI"


def _namespace(cfg: dict, root: Path, base: Path) -> str:
    """The vault folder name for a project root: the same name `bossku remember` writes to."""
    names = cfg.get("memory_project_namespaces") or {}
    chosen = next((n.strip() for r, n in names.items()
                   if isinstance(n, str) and n.strip() and Path(r).resolve() == root.resolve()), root.name)
    return vault_export_dir(base.parent, chosen).name


def _read(path: Path) -> str:
    """Read a text file whatever editor wrote it: UTF-8 (with or without BOM), UTF-16 with BOM, or Windows-1252."""
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="replace").replace("\r\n", "\n")
    try:
        return raw.decode("utf-8-sig").replace("\r\n", "\n")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace").replace("\r\n", "\n")


def _free(path: Path) -> Path:
    """`path`, or `name.1.ext`, `name.2.ext`... when it is taken, so nothing is ever overwritten."""
    if not path.exists():
        return path
    n = 1
    while True:
        candidate = path.with_name(f"{path.stem}.{n}{path.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _state_path(home: Path | None) -> Path:
    return user_config_dir(home) / "vault-sync-state.json"


def _load_state(home: Path | None) -> dict:
    try:
        data = json.loads(_state_path(home).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_state(state: dict, home: Path | None) -> None:
    path = _state_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(state, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def _mirror(src: Path, dest: Path, state: dict, label: str) -> bool:
    """Copy src to dest with a header that says where it came from. True when the vault copy changed.

    A copy you edited in the vault is left alone until the original changes; then your version is kept next to it as
    `<name>.conflict.md` before the new copy is written.
    """
    try:
        body = redact(_read(src))
    except OSError:
        return False
    digest = _digest(body)
    key = str(dest)
    entry = state.get(key) if isinstance(state.get(key), dict) else None
    current = None
    if dest.is_file():
        try:
            current = _read(dest)
        except OSError:
            current = None
        if entry and entry.get("src") == digest:
            return False
        if current is not None and current.endswith(body):          # same content, only the header differs
            state[key] = {"src": digest, "out": _digest(current)}
            return False
    header = (f"---\nmirror_of: {src}\nsource: {label}\nsynced: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}\n"
              "note: automatic copy of the original; if you edit it here, your version is kept as a .conflict.md "
              "file when the original changes\n---\n\n")
    out = header + body
    dest.parent.mkdir(parents=True, exist_ok=True)
    if current is not None and not (entry and _digest(current) == entry.get("out")):
        keep = _free(dest.with_name(dest.name + ".conflict.md"))
        keep.write_text(current, encoding="utf-8")
    dest.write_text(out, encoding="utf-8")
    state[key] = {"src": digest, "out": _digest(out)}
    return True


def _claude_project_dirs(root: Path, home_dir: Path) -> list[tuple[str, Path]]:
    """Claude Code project folders of this root and the folders and worktrees inside it: (label, folder).

    Matched against the real directories, so a sibling such as `app-old` next to `app` is not mistaken for part of it.
    """
    projects = home_dir / ".claude" / "projects"
    if not projects.is_dir():
        return []
    wanted = {_slug(root).lower(): "root"}
    try:
        children = [c for c in root.iterdir() if c.is_dir()]
    except OSError:
        children = []
    for child in children:
        wanted.setdefault(_slug(child).lower(), child.name)
    for holder in (root, *children):
        trees = holder / ".claude" / "worktrees"
        if trees.is_dir():
            for tree in trees.iterdir():
                if tree.is_dir():
                    wanted.setdefault(_slug(tree).lower(), f"{holder.name}-worktree-{tree.name}")
    return sorted((label, entry) for entry in projects.iterdir()
                  if entry.is_dir() and (label := wanted.get(entry.name.lower())))


def sync(project: Path, *, home: Path | None = None, force: bool = False) -> dict:
    """Mirror auto-memory, rules and legacy notes for this project into the vault, then refresh the index."""
    cfg = load_user_config(home)
    base = base_dir(cfg)
    if base is None:
        return {"status": "skipped", "reason": "no vault configured or vault unavailable"}
    state = _load_state(home)
    before = json.dumps(state, sort_keys=True)
    now = time.time()
    root = memory_project_root(project, home=home)
    throttle = f"_last_run:{root}"
    if not force and now - state.get(throttle, 0) < THROTTLE_SECONDS:
        return {"status": "throttled"}
    ns = _namespace(cfg, root, base)
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
    if changed or json.dumps(state, sort_keys=True) != before:      # a sync that finds nothing writes nothing
        state[throttle] = now
        _save_state(state, home)
    return {"status": "ok", "namespace": ns, "changed": changed}


def write_index(base: Path) -> bool:
    """A table of contents of every project folder, with links. True when it changed."""
    if not base.is_dir():
        return False
    lines = ["---", "generated: true", "---", "", "# Bossku Superpower memory", "",
             "Notes, learnings, decisions and rules saved by your agents. This page is rewritten automatically.", ""]
    sections = []
    for folder in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        notes = sorted(p for p in folder.rglob("*.md") if p.name != "Index.md" and not CONFLICT.search(p.name))
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
    if target.is_file() and _read(target) == text:
        return False
    target.write_text(text, encoding="utf-8")
    return True


# ---------------------------------------------------------------- tidy

def _files(folder: Path) -> list[Path]:
    return [p for p in folder.rglob("*") if p.is_file()]


def _split(text: str) -> tuple[str, str, list[str]]:
    """A notes file as (title line, text before the first '## ' entry, the '## ' entries)."""
    head, *parts = re.split(r"(?m)^(?=## )", text)
    first, _, rest = head.strip().partition("\n")
    if first.startswith("# "):
        title, preamble = first.strip(), rest.strip()
    else:
        title, preamble = "", head.strip()
    return title, preamble, [part.rstrip() for part in parts if part.strip()]


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def merge_notes(existing: str, incoming: str) -> str:
    """Union of two notes files: every entry of both, none twice, oldest first.

    Text before the first entry of either file (or a whole file with no entries) is kept as an undated entry.
    """
    title, preamble, mine = _split(existing)
    other_title, other_preamble, theirs = _split(incoming)
    seen = {_norm(e.split("\n", 1)[-1]) for e in mine}
    merged = list(mine)
    if other_preamble and _norm(other_preamble) not in _norm(existing):
        seen.add(_norm(other_preamble))
        merged.append("## (undated, merged in)\n\n" + other_preamble)
    for entry in theirs:
        body = _norm(entry.split("\n", 1)[-1])
        if body not in seen:
            seen.add(body)
            merged.append(entry)
    merged.sort(key=lambda e: e.split("\n", 1)[0])
    top = [part for part in ((title or other_title), preamble) if part]
    return "\n\n".join(top + merged).rstrip() + "\n"


def _folder_moves(cfg: dict, base: Path) -> dict[str, Path]:
    """`vault_folder_moves` from the config: {"folder name": "where it goes, relative to BosskuAI"}. Bad entries are ignored."""
    moves = {}
    for name, where in (cfg.get("vault_folder_moves") or {}).items():
        if not isinstance(name, str) or not isinstance(where, str) or not where.strip():
            continue
        rel = Path(where.strip().replace("\\", "/").strip("/"))
        if rel.parts and not rel.is_absolute() and ".." not in rel.parts and (base / rel).resolve().is_relative_to(base.resolve()):
            moves[name.lower()] = rel
    return moves


def plan_tidy(*, home: Path | None = None) -> list[dict]:
    """What a clean-up would do, as a list of {action, source, target, why}. Changes nothing."""
    cfg = load_user_config(home)
    base = base_dir(cfg)
    if base is None or not base.is_dir():
        return []
    roots = [Path(r).resolve() for r in cfg.get("memory_project_roots") or []]
    namespaces = {root: _namespace(cfg, root, base) for root in roots}
    protected = {ns.lower() for ns in namespaces.values()}
    # a folder is a sub-repo only when its name is exactly a folder inside one (and only one) configured root
    owners: dict[str, set[str]] = {}
    for root in roots:
        if root.is_dir():
            for child in root.iterdir():
                if child.is_dir() and not child.name.startswith("."):
                    owners.setdefault(child.name.lower(), set()).add(namespaces[root])
    moves = _folder_moves(cfg, base)
    plan: list[dict] = []
    for folder in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        files = _files(folder)
        if not files:
            plan.append({"action": "remove-empty-folder", "source": str(folder), "target": "", "why": "no file inside it"})
            continue
        conflicts = [f for f in files if CONFLICT.search(f.name)]
        for f in conflicts:
            plan.append({"action": "archive", "source": str(f), "target": str(base / ARCHIVE / "conflicts" / folder.name / f.name),
                         "why": "backup the old export made when the vault copy had been edited"})
        real = [f for f in files if f not in conflicts]
        low = folder.name.lower()
        if not real:
            continue
        if low in moves:                      # you said where this folder belongs
            rel = moves[low]
            kept_apart = rel.parts[0].startswith("_")
            for f in real:
                merges = f.name in NOTE_FILES and not kept_apart
                plan.append({"action": "merge" if merges else "move", "source": str(f),
                             "target": str(base / rel / (f.name if merges else f.relative_to(folder))),
                             "why": f"listed in vault_folder_moves in your config: {rel.as_posix()}"})
            continue
        if low in protected:
            continue
        parents = owners.get(low, set())
        if len(parents) == 1:
            parent = next(iter(parents))
            for f in real:
                if f.name in NOTE_FILES:
                    plan.append({"action": "merge", "source": str(f), "target": str(base / parent / "repos" / folder.name / f.name),
                                 "why": f"belongs to {parent} (a folder inside its project root)"})
                else:
                    plan.append({"action": "move", "source": str(f), "target": str(base / parent / "repos" / folder.name / f.relative_to(folder)),
                                 "why": f"belongs to {parent}"})
        elif re.fullmatch(r"g-p-[0-9a-f]{20,}", folder.name):
            for f in real:
                plan.append({"action": "move", "source": str(f), "target": str(base / "_unsorted" / folder.name / f.relative_to(folder)),
                             "why": "a generated project name: decide which project it belongs to"})
    for root in roots:
        if not root.is_dir():
            continue
        for sub in [root, *[c for c in root.iterdir() if c.is_dir()]]:
            memory = sub / ".bossku" / "memory"
            for name in NOTE_FILES:
                if (memory / name).is_file() and (memory / name).stat().st_size > 0:
                    plan.append({"action": "import", "source": str(memory / name),
                                 "target": str(base / namespaces[root] / "repos" / (sub.name if sub != root else "_root") / name),
                                 "why": "notes stored outside the vault (the original is left in place)"})
    return plan


def backup(base: Path, home: Path | None = None) -> Path:
    target = user_config_dir(home) / "backups"
    target.mkdir(parents=True, exist_ok=True)
    zip_path = _free(target / f"vault-BosskuAI-{datetime.now():%Y%m%d-%H%M%S-%f}.zip")
    with zipfile.ZipFile(zip_path, "x", zipfile.ZIP_DEFLATED) as archive:
        for f in base.rglob("*"):
            if f.is_file():
                archive.write(f, f.relative_to(base.parent).as_posix())
    return zip_path


def _apply_step(step: dict, base: Path) -> str | None:
    """Carry out one planned step. Returns the action that was performed, or None when there was nothing to do."""
    src, dest = Path(step["source"]), Path(step["target"]) if step["target"] else None
    action = step["action"]
    if action == "remove-empty-folder":
        if src.is_dir() and not _files(src):
            shutil.rmtree(src)
            return action
        return None
    if not src.is_file() or dest is None:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    if action in ("merge", "import"):
        if dest.is_file():
            dest.write_text(merge_notes(_read(dest), _read(src)), encoding="utf-8")
        else:
            dest.write_text(_read(src), encoding="utf-8")
        if action == "merge":        # keep the original: it moves to the archive once its entries are in the target
            keep = _free(base / ARCHIVE / "merged" / src.relative_to(base).parent / src.name)
            keep.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(keep))
        return action
    shutil.move(str(src), str(_free(dest)))
    return action


def apply_tidy(plan: list[dict], *, home: Path | None = None) -> dict:
    cfg = load_user_config(home)
    base = base_dir(cfg)
    if base is None or not base.is_dir():
        return {"status": "skipped"}
    zip_path = backup(base, home)
    done = {"merge": 0, "move": 0, "archive": 0, "import": 0, "remove-empty-folder": 0}
    failed: list[dict] = []
    for step in plan:
        try:
            action = _apply_step(step, base)
        except (OSError, ValueError) as error:       # record it and carry on with the rest of the plan
            failed.append({"step": step["action"], "source": step["source"], "error": str(error)})
            continue
        if action:
            done[action] += 1
    for folder in sorted((p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))), key=lambda p: p.name):
        if not _files(folder):
            shutil.rmtree(folder)
            done["remove-empty-folder"] += 1
    try:
        write_index(base)
    except OSError as error:
        failed.append({"step": "index", "source": str(base / "Index.md"), "error": str(error)})
    result = {"status": "ok" if not failed else "partial", "backup": str(zip_path), "done": done}
    if failed:
        result["failed"] = failed
    return result
