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
import stat
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from bossku.memory import INBOX, KIND_TO_FILE, _claims, auto_namespace, load_user_config, memory_project_root
from bossku.paths import user_config_dir, vault_export_dir
from bossku.redact import redact

NOTE_FILES = tuple(KIND_TO_FILE.values()) + ("handoff.md",)
THROTTLE_SECONDS = 60
ARCHIVE = "_archive"
GLOBAL_RULES = "_global-rules"          # copies of the rules every agent reads, for all projects
AGENT_RULES = "agent-rules"             # in a project: copies of its CLAUDE.md, AGENTS.md and .claude/rules
CLAUDE_MEMORY = "claude-memory"         # in a project: copies of Claude Code's own memory notes
# _archive sub-folders: old copies kept for safety, never read by an agent
EDIT_CONFLICTS = "edit-conflicts"       # your vault edit, kept when the original changed underneath it
MERGED_ORIGINALS = "merged-originals"   # a notes file as it was before tidy merged it into another folder
DELETED_FOLDER_COPIES = "deleted-folder-copies"   # copies of files from a folder that no longer exists
OLD_FORMAT_NOTES = "old-format-notes"   # notes in the layout of older versions
TEST_LEFTOVERS = "test-leftovers"       # notes a test run wrote to the real vault
# the global rules copies, named after the tool that reads them
GLOBAL_RULE_FILES = (((".claude", "CLAUDE.md"), "claude-code-CLAUDE.md"),
                     ((".codex", "AGENTS.md"), "codex-AGENTS.md"),
                     ((".config", "opencode", "AGENTS.md"), "opencode-AGENTS.md"))
FILE_RENAMES = {"claude-CLAUDE.md": "claude-code-CLAUDE.md"}
# old name -> new name, applied by tidy: (path relative to BosskuAI, or to a project folder when it starts with "*/")
OLD_LAYOUT = (
    ("_inbox", INBOX),
    ("_unsorted", INBOX),
    ("_global/notes", INBOX),
    ("_global/rules", GLOBAL_RULES),
    ("_archive/conflicts", f"{ARCHIVE}/{EDIT_CONFLICTS}"),
    ("_archive/merged", f"{ARCHIVE}/{MERGED_ORIGINALS}"),
    ("_archive/old-folders", f"{ARCHIVE}/{DELETED_FOLDER_COPIES}"),
    ("_archive/legacy", f"{ARCHIVE}/{OLD_FORMAT_NOTES}"),
    ("_archive/unsorted", f"{ARCHIVE}/{TEST_LEFTOVERS}"),
    ("*/rules", AGENT_RULES),
    ("*/claude-memory/root", CLAUDE_MEMORY),
    ("*/_legacy", f"{ARCHIVE}/{OLD_FORMAT_NOTES}"),
)
CONFLICT = re.compile(r"\.md\.conflict(\.\d+)?\.md$")


def _slug(path: Path | str) -> str:
    """The folder name Claude Code gives a working directory: every non-alphanumeric character becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def base_dir(cfg: dict) -> Path | None:
    vault = cfg.get("obsidian_vault")
    if not vault or not Path(vault).is_dir():
        return None
    return Path(vault) / "BosskuAI"


def _namespace(cfg: dict, root: Path, base: Path, home: Path | None = None) -> str:
    """The vault folder name for a project root: the same name `bossku remember` writes to."""
    names = cfg.get("memory_project_namespaces") or {}
    chosen = next((n.strip() for r, n in names.items()
                   if isinstance(n, str) and n.strip() and Path(r).resolve() == root.resolve()), None)
    return vault_export_dir(base.parent, chosen or auto_namespace(root.resolve(), cfg, base.parent, home=home)).name


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
    wanted = {_slug(root).lower(): ""}        # the root's own notes sit directly in claude-memory/
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
                  if entry.is_dir() and (label := wanted.get(entry.name.lower())) is not None)


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
    ns = _namespace(cfg, root, base, home)
    if ns == INBOX:      # not a project: nothing of it is mirrored, so no folder is made for it
        return {"status": "skipped", "reason": "not a project (no git repo, not in memory_project_roots)"}
    changed: list[str] = []

    def mirror(src: Path, dest: Path, label: str) -> None:
        if src.is_file() and _mirror(src, dest, state, label):
            changed.append(str(dest.relative_to(base)))

    home_dir = home or Path.home()
    for suffix, folder in _claude_project_dirs(root, home_dir):
        memory = folder / "memory"
        if memory.is_dir():
            for note in sorted(memory.glob("*.md")):
                mirror(note, base / ns / CLAUDE_MEMORY / suffix / note.name, "Claude Code auto-memory")
    for parts, name in GLOBAL_RULE_FILES:
        mirror(home_dir.joinpath(*parts), base / GLOBAL_RULES / name, "global rules")
    for name in ("CLAUDE.md", "AGENTS.md"):
        mirror(root / name, base / ns / AGENT_RULES / name, "project rules")
    rules_dir = root / ".claude" / "rules"
    if rules_dir.is_dir():
        for rule in sorted(rules_dir.glob("*.md")):
            mirror(rule, base / ns / AGENT_RULES / "claude-rules" / rule.name, "project rules")
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


NOTE_ABOUT = {
    "project.md": "what the project is: stack, setup, facts",
    "decisions.md": "choices made and why",
    "plans.md": "work planned for later",
    "learnings.md": "lessons and gotchas",
    "handoff.md": "unfinished work to pick up next",
}
GUIDE = """# Start here: BosskuAI memory

What your agents remembered, one folder per project. This page is rewritten automatically.

## What is where

| Folder | What it holds |
|---|---|
| `<project>/` | one folder per project (a git repo, or a folder in `memory_project_roots`) |
| `<project>/repos/<repo>/` | notes about one repo inside that project |
| `<project>/agent-rules/` | copies of the project's CLAUDE.md and AGENTS.md (edit the originals in the repo) |
| `<project>/claude-memory/` | copies of Claude Code's own memory for that project (MEMORY.md lists them) |
| `_other-notes/` | notes saved from folders that are not projects; each note says where it came from |
| `_global-rules/` | copies of the rules every agent reads, for all projects |
| `_archive/` | old copies kept for safety; agents never read them |

Every notes folder uses the same files: `project.md` (what the project is), `decisions.md` (choices and why), `plans.md` (work for later), `learnings.md` (lessons and gotchas) and `handoff.md` (unfinished work). Newest entries are at the bottom.
"""
ARCHIVE_ABOUT = {
    EDIT_CONFLICTS: "your vault edit, kept when the original changed underneath it",
    MERGED_ORIGINALS: "notes files as they were before tidy merged them into another folder",
    DELETED_FOLDER_COPIES: "copies of files from folders that no longer exist",
    OLD_FORMAT_NOTES: "notes in the layout of older versions",
    TEST_LEFTOVERS: "notes a test run wrote to the real vault",
}


def _link(base: Path, p: Path, label: str) -> str:
    return f"[[{p.relative_to(base).with_suffix('').as_posix()}|{label}]]"


OTHER_ABOUT = {
    "project.md": "facts and reviews",
    "decisions.md": "choices made and why",
    "plans.md": "work planned for later",
    "learnings.md": "lessons and gotchas",
    "handoff.md": "unfinished work to pick up next",
}
RULE_LABELS = {
    "claude-code-CLAUDE.md": "Claude Code: CLAUDE.md",
    "codex-AGENTS.md": "Codex: AGENTS.md",
    "opencode-AGENTS.md": "OpenCode: AGENTS.md",
}


def _notes_lines(base: Path, folder: Path, about: dict[str, str] = NOTE_ABOUT) -> list[str]:
    return [f"- {_link(base, folder / name, name[:-3])}: {text}"
            for name, text in about.items() if (folder / name).is_file()]


def write_index(base: Path) -> bool:
    """The vault's start page: what each folder is for, then every project with links. True when it changed."""
    if not base.is_dir():
        return False
    sections = [GUIDE.rstrip()]
    for folder in sorted((p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))),
                         key=lambda p: p.name.lower()):
        md = sorted(p for p in folder.rglob("*.md") if not CONFLICT.search(p.name))
        if not md:
            continue
        part = [f"## {folder.name}", ""] + _notes_lines(base, folder)
        repos = folder / "repos"
        for repo in sorted(p for p in repos.iterdir() if p.is_dir()) if repos.is_dir() else []:
            links = ", ".join(_link(base, repo / n, n[:-3]) for n in NOTE_ABOUT if (repo / n).is_file())
            if links:
                part.append(f"- repo `{repo.name}`: {links}")
        rules = sorted((folder / AGENT_RULES).rglob("*.md")) if (folder / AGENT_RULES).is_dir() else []
        if rules:
            part.append("- agent rules (copies): " + ", ".join(
                _link(base, p, p.relative_to(folder / AGENT_RULES).as_posix()) for p in rules))
        memory = folder / CLAUDE_MEMORY
        if memory.is_dir():
            count = sum(1 for p in memory.rglob("*.md") if p.name != "MEMORY.md")
            start = memory / "MEMORY.md"
            label = _link(base, start, "MEMORY") if start.is_file() else f"`{CLAUDE_MEMORY}/`"
            part.append(f"- Claude Code memory (copies): {label}, {count} note{'' if count == 1 else 's'}")
        shown = {folder / n for n in NOTE_ABOUT} | set(rules)
        rest = [p for p in md if p not in shown and repos not in p.parents and memory not in p.parents]
        if rest:
            part.append("- other files: " + ", ".join(_link(base, p, p.relative_to(folder).as_posix()) for p in rest))
        sections.append("\n".join(part))
    other = base / INBOX
    if other.is_dir() and any(other.glob("*.md")):
        sections.append("\n".join(["## Other notes (not from a project)", "",
                                   "Each entry starts with `From:` and the folder it was saved in.", ""]
                                  + _notes_lines(base, other, OTHER_ABOUT)))
    glob = sorted((base / GLOBAL_RULES).glob("*.md")) if (base / GLOBAL_RULES).is_dir() else []
    if glob:
        sections.append("## Rules for all projects (copies)\n\n" + "\n".join(
            f"- {_link(base, p, RULE_LABELS.get(p.name, p.stem))}" for p in glob))
    archive = base / ARCHIVE
    kept = [f"- `{ARCHIVE}/{p.name}/`: {ARCHIVE_ABOUT.get(p.name, 'old files kept for safety')}"
            for p in sorted(archive.iterdir()) if p.is_dir()] if archive.is_dir() else []
    if kept:
        sections.append("## Archive (old copies, safe to ignore)\n\n" + "\n".join(kept))
    text = "---\ngenerated: true\n---\n\n" + "\n\n".join(sections) + "\n"
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


def _same_file(a: Path, b: Path) -> bool:
    try:
        return a.read_bytes() == b.read_bytes()
    except OSError:
        return False


def _already_in(src: Path, target: Path) -> bool:
    """True when every entry of `src` is already in `target`, so importing it again would change nothing."""
    try:
        current = _read(target)
        return merge_notes(current, _read(src)) == merge_notes(current, "")
    except OSError:
        return False


def _layout_steps(base: Path) -> list[dict]:
    """Steps that move folders still using an older name (`_inbox`, `rules`, `claude-memory/root`...) to the
    current one. Notes files are merged; a mirrored copy that sync already wrote again under the new name is dropped
    when it is identical, and archived when it is not."""
    projects = [p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))]
    pairs: list[tuple[Path, Path]] = []
    for old, new in OLD_LAYOUT:
        if old.startswith("*/"):
            for project in projects:
                dest = base / new / project.name if new.startswith("_") else project / new
                pairs.append((project / old[2:], dest))
        else:
            pairs.append((base / old, base / new))
    steps: list[dict] = []
    why = "renamed so the vault is easier to read"
    for src_dir, dest_dir in pairs:
        if not src_dir.is_dir():
            continue
        for f in sorted(_files(src_dir)):
            if dest_dir.name == INBOX and f.name in NOTE_FILES and (dest_dir / f.name).is_file():
                steps.append({"action": "merge", "source": str(f), "target": str(dest_dir / f.name), "why": why})
                continue
            rel = f.relative_to(src_dir)
            dest = dest_dir / rel.parent / FILE_RENAMES.get(rel.name, rel.name)
            if not dest.is_file() or f.relative_to(base).parts[0] == ARCHIVE:   # archived copies are never merged
                steps.append({"action": "move", "source": str(f), "target": str(dest), "why": why})
            elif _same_file(f, dest):
                steps.append({"action": "drop-duplicate", "source": str(f), "target": str(dest), "why": "the same file is already there"})
            elif f.name in NOTE_FILES:
                steps.append({"action": "merge", "source": str(f), "target": str(dest), "why": why})
            else:
                steps.append({"action": "archive", "source": str(f),
                              "target": str(base / ARCHIVE / EDIT_CONFLICTS / f.relative_to(base)), "why": "an older copy of a file that is already there"})
    return steps


def plan_tidy(*, home: Path | None = None) -> list[dict]:
    """What a clean-up would do, as a list of {action, source, target, why}. Changes nothing."""
    cfg = load_user_config(home)
    base = base_dir(cfg)
    if base is None or not base.is_dir():
        return []
    roots = [Path(r).resolve() for r in cfg.get("memory_project_roots") or []]
    namespaces = {root: _namespace(cfg, root, base, home) for root in roots}
    protected = {ns.lower() for ns in namespaces.values()}
    # a folder is a sub-repo only when its name is exactly a folder inside one (and only one) configured root
    owners: dict[str, set[str]] = {}
    for root in roots:
        if root.is_dir():
            for child in root.iterdir():
                if child.is_dir() and not child.name.startswith("."):
                    owners.setdefault(child.name.lower(), set()).add(namespaces[root])
    moves = _folder_moves(cfg, base)
    plan: list[dict] = _layout_steps(base)
    for folder in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        files = _files(folder)
        if not files:
            plan.append({"action": "remove-empty-folder", "source": str(folder), "target": "", "why": "no file inside it"})
            continue
        conflicts = [f for f in files if CONFLICT.search(f.name)]
        for f in conflicts:
            plan.append({"action": "archive", "source": str(f), "target": str(base / ARCHIVE / EDIT_CONFLICTS / folder.name / f.name),
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
        elif (home_ns := _new_home(folder, base, cfg, home)) or re.fullmatch(r"g-p-[0-9a-f]{20,}", folder.name):
            dest, why = home_ns or (INBOX, "a generated project name, not a project")
            for f in real:
                if f.name in NOTE_FILES and f.parent == folder:
                    plan.append({"action": "merge", "source": str(f), "target": str(base / dest / f.name), "why": why})
                else:            # mirrored rules and other copies: regenerated by sync, so the old copy is archived
                    plan.append({"action": "archive", "source": str(f),
                                 "target": str(base / ARCHIVE / DELETED_FOLDER_COPIES / folder.name / f.relative_to(folder)), "why": why})
        elif all(_stale_mirror(f) for f in real):
            for f in real:
                plan.append({"action": "archive", "source": str(f),
                             "target": str(base / ARCHIVE / DELETED_FOLDER_COPIES / folder.name / f.relative_to(folder)),
                             "why": "copies of files in a folder that no longer exists"})
    for root in roots:
        if not root.is_dir():
            continue
        for sub in [root, *[c for c in root.iterdir() if c.is_dir()]]:
            memory = sub / ".bossku" / "memory"
            for name in NOTE_FILES:
                src = memory / name
                target = base / namespaces[root] / "repos" / (sub.name if sub != root else "_root") / name
                if src.is_file() and src.stat().st_size > 0 and not _already_in(src, target):
                    plan.append({"action": "import", "source": str(src), "target": str(target),
                                 "why": "notes stored outside the vault (the original is left in place)"})
    return plan


def _new_home(folder: Path, base: Path, cfg: dict, home: Path | None) -> tuple[str, str] | None:
    """(vault folder, why) when this folder was made by an older version for a root that now saves somewhere else."""
    for claim in _claims(home):
        root = Path(claim["project_root"])
        if Path(claim["memory_dir"]).name.lower() != folder.name.lower() or not root.is_dir():
            continue
        ns = auto_namespace(root, cfg, base.parent, home=home)
        if ns.lower() != folder.name.lower():
            why = "not a project (no git repo, not in memory_project_roots)" if ns == INBOX else f"same git repo as {ns}"
            return ns, why
    return None


def _stale_mirror(f: Path) -> bool:
    """True when `f` is a mirrored copy (it has a mirror_of header) whose original no longer exists."""
    try:
        head = _read(f)[:600]
    except OSError:
        return False
    match = re.search(r"(?m)^mirror_of: (.+)$", head)
    return bool(match) and not Path(match.group(1).strip()).exists()


def backup(base: Path, home: Path | None = None) -> Path:
    target = user_config_dir(home) / "backups"
    target.mkdir(parents=True, exist_ok=True)
    zip_path = _free(target / f"vault-BosskuAI-{datetime.now():%Y%m%d-%H%M%S-%f}.zip")
    with zipfile.ZipFile(zip_path, "x", zipfile.ZIP_DEFLATED) as archive:
        for f in base.rglob("*"):
            if f.is_file():
                archive.write(f, f.relative_to(base.parent).as_posix())
    return zip_path


def _rmdir(folder: Path) -> None:
    try:
        folder.rmdir()
    except PermissionError:               # a read-only folder (OneDrive makes some): clear the flag and try again
        os.chmod(folder, stat.S_IWRITE)
        folder.rmdir()


def _remove_empty_folder(folder: Path) -> None:
    """Remove a folder that has no file anywhere inside it, sub-folders first."""
    for sub in sorted((p for p in folder.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        _rmdir(sub)
    _rmdir(folder)


def _apply_step(step: dict, base: Path) -> str | None:
    """Carry out one planned step. Returns the action that was performed, or None when there was nothing to do."""
    src, dest = Path(step["source"]), Path(step["target"]) if step["target"] else None
    action = step["action"]
    if action == "remove-empty-folder":
        if src.is_dir() and not _files(src):
            _remove_empty_folder(src)
            return action
        return None
    if not src.is_file() or dest is None:
        return None
    if action == "drop-duplicate":   # only when an identical copy is still there (the zip backup has it as well)
        if dest.is_file() and _same_file(src, dest):
            src.unlink()
            return action
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    if action in ("merge", "import"):
        if dest.is_file():
            dest.write_text(merge_notes(_read(dest), _read(src)), encoding="utf-8")
        else:
            dest.write_text(_read(src), encoding="utf-8")
        if action == "merge":        # keep the original: it moves to the archive once its entries are in the target
            keep = _free(base / ARCHIVE / MERGED_ORIGINALS / src.relative_to(base).parent / src.name)
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
    done = {"merge": 0, "move": 0, "archive": 0, "import": 0, "drop-duplicate": 0, "remove-empty-folder": 0}
    failed: list[dict] = []
    for step in plan:
        try:
            action = _apply_step(step, base)
        except (OSError, ValueError) as error:       # record it and carry on with the rest of the plan
            failed.append({"step": step["action"], "source": step["source"], "error": str(error)})
            continue
        if action:
            done[action] += 1
    folders = (p for p in base.rglob("*") if p.is_dir() and not any(s.startswith(".") for s in p.relative_to(base).parts))
    for folder in sorted(folders, key=lambda p: len(p.parts), reverse=True):     # deepest first, so parents empty out
        if not any(folder.iterdir()):
            try:
                _rmdir(folder)
                done["remove-empty-folder"] += 1
            except OSError as error:
                failed.append({"step": "remove-empty-folder", "source": str(folder), "error": str(error)})
    try:
        write_index(base)
    except OSError as error:
        failed.append({"step": "index", "source": str(base / "Index.md"), "error": str(error)})
    result = {"status": "ok" if not failed else "partial", "backup": str(zip_path), "done": done}
    if failed:
        result["failed"] = failed
    return result
