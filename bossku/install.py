from __future__ import annotations

import json
import shutil
from pathlib import Path

from bossku.paths import (
    agents_skills_dir,
    claude_skills_dir,
    library_dir,
    repo_root,
    user_config_dir,
)
from bossku.hooks import install_hooks, uninstall_hooks
from bossku.skills import (
    copy_library_to,
    copy_skills_to,
    is_managed_skill_name,
    make_path_writable,
    prune_stale_skills,
    remove_tree,
    write_routing_cache,
)


def copy_support_files(source_dir: Path, dest_dir: Path) -> list[str]:
    """Merge shared support files without deleting unrelated destination files."""
    if not source_dir.is_dir():
        return []
    copied: list[str] = []
    for source in sorted(source_dir.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(source_dir)
        target = dest_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            make_path_writable(target)
        shutil.copyfile(source, target)
        make_path_writable(target)
        copied.append(relative.as_posix())
    return copied


def copy_skill_support(root: Path, destination: Path) -> dict[str, list[str]]:
    """Install shared sidecars at the relative paths used by installed skills."""
    references = copy_support_files(root / "references", destination / "references")
    copy_support_files(root / "site", destination / "site")
    docs = []
    for name in ("memory.md",):
        source = root / "docs" / name
        if source.is_file():
            target = destination / "docs" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                make_path_writable(target)
            shutil.copyfile(source, target)
            make_path_writable(target)
            docs.append(name)
    return {"references": references, "docs": docs}


def tools_coverage_map(agents_dest: Path, claude_dest: Path) -> dict:
    agents_s = str(agents_dest)
    claude_s = str(claude_dest)
    init_hint = "project AGENTS.md (bossku init)"
    claude_hint = "project CLAUDE.md @AGENTS.md (bossku init)"
    return {
        "cursor": {"skills": agents_s, "instructions": init_hint},
        "codex": {"skills": agents_s, "instructions": init_hint},
        "opencode": {"skills": [agents_s, claude_s], "instructions": init_hint},
        "claude_code": {"skills": claude_s, "instructions": claude_hint},
        "omp": {
            "skills": [agents_s, claude_s],
            "instructions": "project .omp/AGENTS.md @../AGENTS.md (bossku init)",
        },
    }


AUTO_MEMORY_BLOCK = """<!-- bosskuai:memory:start -->
## Automatic BosskuAI memory

Get the project notes with `bossku memory-brief --project <project-root>` unless they are already in your
context (`bossku memory-path` names the folder; handoff.md lives there). Automatically save, before the final
reply, only what the code and git history cannot tell a future session: a rule or decision someone stated (with
its reason), a plan for later, or a gotcha that cost you time; never a summary of what you built or changed. Use
`bossku remember --project <project-root> --kind decision|plan|learning|project "<note>"`; one call is enough.
Skip routine work, duplicates, secrets, raw prompts and transcripts. With Obsidian storage
(~/.bosskuai/config.json) never write .bossku/memory or repo sync files; if the vault is unavailable, report
that the note was not saved.
<!-- bosskuai:memory:end -->"""


def install_auto_memory_instructions(home: Path) -> list[str]:
    paths = (home / ".codex" / "AGENTS.md", home / ".claude" / "CLAUDE.md",
             home / ".config" / "opencode" / "AGENTS.md")
    installed = []
    start_marker, end_marker = "<!-- bosskuai:memory:start -->", "<!-- bosskuai:memory:end -->"
    for path in paths:
        if not path.parent.is_dir():
            continue
        existing = path.read_text(encoding="utf-8") if path.is_file() else ""
        if start_marker in existing and end_marker in existing:
            start = existing.index(start_marker)
            end = existing.index(end_marker, start) + len(end_marker)
            text = existing[:start] + AUTO_MEMORY_BLOCK + existing[end:]
        else:
            text = existing.rstrip() + ("\n\n" if existing.strip() else "") + AUTO_MEMORY_BLOCK + "\n"
        if text != existing:
            if path.exists():
                make_path_writable(path)
            path.write_text(text, encoding="utf-8")
        installed.append(str(path))
    return installed


def install_user(
    *,
    root: Path | None = None,
    home: Path | None = None,
    profile: str = "full",
    vault: str | None = None,
    memory_storage: str | None = None,
) -> dict:
    r = repo_root(root)
    h = home if home is not None else Path.home()
    agents_dest = agents_skills_dir(h)
    claude_dest = claude_skills_dir(h)
    installed_agents = copy_skills_to(agents_dest, r, profile)
    installed_claude = copy_skills_to(claude_dest, r, profile)
    pruned = prune_stale_skills((agents_dest, claude_dest), set(installed_agents), r)
    agents_support = copy_skill_support(r, agents_dest.parent)
    claude_support = copy_skill_support(r, claude_dest.parent)
    installed_agents_references = agents_support["references"]
    installed_claude_references = claude_support["references"]
    agents_n = len(installed_agents)
    claude_n = len(installed_claude)
    if agents_n == 0 or claude_n == 0:
        raise RuntimeError("install copied zero skills to one or both skill destinations")
    if agents_n != claude_n:
        raise RuntimeError(
            f"skill mirror mismatch: agents={agents_n} claude={claude_n}; re-run `bossku install`"
        )
    library = library_dir(h)
    if profile == "lean":
        # Skills the hosts do not list stay installed whole, one `bossku skills show <id>` away.
        library_ids = copy_library_to(library, r, set(installed_agents))
        copy_skill_support(r, library.parent)
    else:
        library_ids = []
        remove_tree(library)
    # The router can pick anything it can reach: listed skills plus the library.
    cache_path = user_config_dir(h) / "routing-cache.json"
    write_routing_cache(cache_path, r, available=set(installed_agents) | set(library_ids))
    cfg_path = user_config_dir(h) / "config.json"
    cfg: dict = {}
    if cfg_path.is_file():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["installed_from"] = str(r)
    cfg["profile"] = profile
    if vault:
        cfg["obsidian_vault"] = vault
    if memory_storage is not None:
        if memory_storage not in {"repo", "obsidian"}:
            raise ValueError("memory_storage must be repo or obsidian")
        if memory_storage == "obsidian" and not cfg.get("obsidian_vault"):
            raise ValueError("obsidian memory requires --vault or a configured obsidian_vault")
        cfg["memory_storage"] = memory_storage
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    # Default denser Obsidian auto-sync hooks (clone → pip install -e . → bossku install).
    hooks_result = install_hooks(home=h)
    memory_instructions = install_auto_memory_instructions(h)
    return {
        "agents_skills": str(agents_dest),
        "claude_skills": str(claude_dest),
        "agents_count": agents_n,
        "claude_count": claude_n,
        "installed_count": agents_n,
        "library_dir": str(library) if library_ids else None,
        "library_count": len(library_ids),
        "pruned_skills": pruned,
        "agents_reference_count": len(installed_agents_references),
        "claude_reference_count": len(installed_claude_references),
        "agents_doc_count": len(agents_support["docs"]),
        "claude_doc_count": len(claude_support["docs"]),
        "tools": tools_coverage_map(agents_dest, claude_dest),
        "routing_cache": str(cache_path),
        "hooks": hooks_result,
        "auto_memory_instructions": memory_instructions,
    }


def update_user(*, root: Path | None = None, home: Path | None = None) -> dict:
    cfg_path = user_config_dir(home) / "config.json"
    profile = "full"
    vault = None
    effective_root = root
    if cfg_path.is_file():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        profile = cfg.get("profile", "full")
        vault = cfg.get("obsidian_vault")
        if effective_root is None and cfg.get("installed_from"):
            effective_root = Path(cfg["installed_from"])
    return install_user(root=effective_root, home=home, profile=profile, vault=vault)


def uninstall_user(*, root: Path | None = None, home: Path | None = None, purge: bool = False) -> dict:
    h = home if home is not None else Path.home()
    cfg_path = user_config_dir(h) / "config.json"
    effective_root = root
    if effective_root is None and cfg_path.is_file():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        installed_from = cfg.get("installed_from")
        if installed_from:
            effective_root = Path(installed_from)
    removed: list[str] = []
    for dest in (agents_skills_dir(h), claude_skills_dir(h)):
        if not dest.is_dir():
            continue
        for child in list(dest.iterdir()):
            if child.is_dir() and is_managed_skill_name(child.name, effective_root):
                remove_tree(child)
                removed.append(child.name)
    remove_tree(library_dir(h))
    for name in ("references", "site", "docs"):   # shared files the lean library links to
        remove_tree(user_config_dir(h) / name)
    hooks_removed = uninstall_hooks(home=h) if purge else None
    if purge and cfg_path.is_file():
        cfg_path.unlink()
    cache = user_config_dir(h) / "routing-cache.json"
    if purge and cache.is_file():
        cache.unlink()
    return {"removed_skills": removed, "purged_config": purge, "hooks_removed": hooks_removed}
