from __future__ import annotations

import json
import shutil
from pathlib import Path

from bossku.index import index_path, skill_index_signature
from bossku.paths import (
    agents_skills_dir,
    claude_skills_dir,
    library_dir,
    repo_root,
    routing_index_copy,
    routing_signature_path,
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
)

# The subagent contracts copied to ~/.claude/agents. A copy carries the signature; a file without it is the user's own.
AGENT_FILES = ("orchestrator.md", "planner.md", "designer.md", "executor.md", "auditor.md", "final-reviewer.md")
AGENT_SIGNATURE = "<!-- runtime-core:start -->"
# Shared files the repo no longer ships. remove_skill_support only deletes copies of files the repo still has,
# so a retired file is cleaned up by its exact path.
RETIRED_SUPPORT_FILES = ("references/always-on-model-router.md",)


def claude_agents_dir(home: Path) -> Path:
    return home / ".claude" / "agents"


def _is_managed_agent(path: Path) -> bool:
    try:
        return AGENT_SIGNATURE in path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def copy_agents_to(dest_dir: Path, root: Path | None = None) -> tuple[list[str], list[str]]:
    """Copy the contracts. Returns (installed, kept): a file that exists without our signature is the user's own and stays."""
    source = repo_root(root) / "agents"
    installed: list[str] = []
    kept: list[str] = []
    for name in AGENT_FILES:
        if not (source / name).is_file():
            continue
        target = dest_dir / name
        if target.is_file() and not _is_managed_agent(target):
            kept.append(name)
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        if target.exists():
            make_path_writable(target)
        shutil.copyfile(source / name, target)
        make_path_writable(target)
        installed.append(name)
    return installed, kept


def remove_managed_agents(dest_dir: Path) -> list[str]:
    """Delete only the contracts that carry the signature; a user-owned file of the same name stays."""
    removed: list[str] = []
    for name in AGENT_FILES:
        target = dest_dir / name
        if target.is_file() and _is_managed_agent(target):
            make_path_writable(target)
            target.unlink()
            removed.append(name)
    return removed


def remove_managed_skills(dest_dir: Path, root: Path | None = None) -> list[str]:
    removed: list[str] = []
    for child in sorted(dest_dir.iterdir()) if dest_dir.is_dir() else []:
        if child.is_dir() and is_managed_skill_name(child.name, root):
            remove_tree(child)
            removed.append(child.name)
    return removed


def retire_support_files(destination: Path) -> None:
    for rel in RETIRED_SUPPORT_FILES:
        target = destination / rel
        if target.is_file():
            make_path_writable(target)
            target.unlink()


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
    retire_support_files(destination)
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


def remove_skill_support(root: Path, destination: Path) -> None:
    """Undo copy_skill_support: delete only copies that still match the repo, so a user's own file stays."""
    retire_support_files(destination)
    pairs = [(root / "docs" / "memory.md", destination / "docs" / "memory.md")]
    for name in ("references", "site"):
        pairs += [(s, destination / name / s.relative_to(root / name)) for s in (root / name).rglob("*") if s.is_file()]
    for source, target in pairs:
        if source.is_file() and target.is_file() and source.read_bytes() == target.read_bytes():
            make_path_writable(target)
            target.unlink()
    for name in ("references", "site", "docs"):
        base = destination / name
        folders = sorted((p for p in base.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True)
        for folder in [*folders, base]:
            try:
                folder.rmdir()          # empty folders only
            except OSError:
                pass


def install_routing_copy(root: Path, home: Path) -> str | None:
    """Keep a copy of skills/skill-index.json in ~/.bosskuai with the signature of the skills it sits beside.

    The prompt hook uses the copy only while the signature still matches, and reads the repo's index otherwise, so
    editing a skill never silences a hint. Returns the copy's path, or None when the repo has no saved index."""
    source = index_path(root)
    if not source.is_file():
        return None
    destination, signature = routing_index_copy(home), routing_signature_path(home)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    signature.write_text(skill_index_signature(root) + "\n", encoding="utf-8")
    return str(destination)


def tools_coverage_map(agents_dest: Path, claude_dest: Path, claude_skills: bool = True) -> dict:
    agents_s = str(agents_dest)
    claude_s = str(claude_dest) if claude_skills else "off (no managed copy; a plugin or project copy serves Claude Code)"
    both = [agents_s, claude_s] if claude_skills else [agents_s]
    init_hint = "project AGENTS.md (bossku init)"
    claude_hint = "project CLAUDE.md @AGENTS.md (bossku init)"
    return {
        "cursor": {"skills": agents_s, "instructions": init_hint},
        "codex": {"skills": agents_s, "instructions": init_hint},
        "opencode": {"skills": both, "instructions": init_hint},
        "claude_code": {"skills": claude_s, "instructions": claude_hint},
        "omp": {
            "skills": both,
            "instructions": "project .omp/AGENTS.md @../AGENTS.md (bossku init)",
        },
    }


DEFAULT_VOICE_RULE = (
    'Default voice: use malaysia-localisation for every user-facing response, alongside the primary task skill. '
    'Keep responses short, simple and easy to understand. '
    'Answer first; use everyday words and short sentences; include only the detail needed. '
    "Match the user's English, BM or rojak; when unclear, use clear Malaysian English. "
    'Do not force slang or particles. '
    'Follow explicit language, tone, length and format requests. '
    'Preserve technical accuracy, commands, identifiers and required structured output. '
    'This voice remains the default in normal mode unless the user requests a different voice.'
)

DEFAULT_VOICE_BLOCK = ("<!-- bosskuai:voice:start -->\n## Default response voice\n\n"
                       + DEFAULT_VOICE_RULE + "\n<!-- bosskuai:voice:end -->")


AUTO_MEMORY_BLOCK = """<!-- bosskuai:memory:start -->
## Automatic BosskuAI memory

Get the project notes with `bossku memory-brief --project <project-root>` unless they are already in your
context (`bossku memory-path` names the folder; handoff.md lives there). Automatically save, before the final
reply, every rule or decision the user states (with its reason), plus a plan for later or a gotcha that cost you
time; never a summary of what you built or changed, and not what the code already shows. Use
`bossku remember --project <project-root> --kind decision|plan|learning|project "<note>"`; one call is enough.
Skip routine work, duplicates, secrets, raw prompts and transcripts. With Obsidian storage
(~/.bosskuai/config.json) never write .bossku/memory or repo sync files; if the vault is unavailable, report
that the note was not saved.
<!-- bosskuai:memory:end -->"""


def instruction_files(home: Path) -> tuple[Path, ...]:
    return (home / ".codex" / "AGENTS.md", home / ".claude" / "CLAUDE.md",
            home / ".config" / "opencode" / "AGENTS.md")


def remove_instruction_blocks(home: Path) -> list[str]:
    """Take out the memory and voice blocks install wrote; the user's own text and line endings stay."""
    cleaned = []
    for path in instruction_files(home):
        if not path.is_file():
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            original = text = handle.read()
        for name in ("memory", "voice"):
            start_marker, end_marker = f"<!-- bosskuai:{name}:start -->", f"<!-- bosskuai:{name}:end -->"
            start = text.find(start_marker)
            end = text.find(end_marker, start) if start >= 0 else -1
            if end < 0:
                continue
            before, after = text[:start].rstrip("\r\n"), text[end + len(end_marker):]
            text = before + after if before else after.lstrip("\r\n")
        if text != original:
            make_path_writable(path)
            path.write_text(text, encoding="utf-8", newline="")
            cleaned.append(str(path))
    return cleaned


def install_auto_memory_instructions(home: Path) -> list[str]:
    paths = instruction_files(home)
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
        voice_start, voice_end = "<!-- bosskuai:voice:start -->", "<!-- bosskuai:voice:end -->"
        if voice_start in text and voice_end in text:
            start = text.index(voice_start)
            end = text.index(voice_end, start) + len(voice_end)
            text = text[:start] + DEFAULT_VOICE_BLOCK + text[end:]
        else:
            text = text.rstrip() + "\n\n" + DEFAULT_VOICE_BLOCK + "\n"
        if text != existing:
            if path.exists():
                make_path_writable(path)
            path.write_text(text, encoding="utf-8")
        installed.append(str(path))
    return installed


def _saved_choice(cfg: dict, key: str, flag: bool | None) -> bool:
    return flag if flag is not None else cfg.get(key, True) is not False


def install_user(
    *,
    root: Path | None = None,
    home: Path | None = None,
    profile: str = "full",
    vault: str | None = None,
    memory_storage: str | None = None,
    claude: bool | None = None,
    agents: bool | None = None,
    harness: bool | None = None,
) -> dict:
    """Install skills, agent contracts and hooks at user level.

    `claude=False` skips ~/.claude/skills and removes the managed copies there: use it when a Claude Code plugin
    serves the skills, or every skill loads twice. `agents=False` skips (and removes) the contracts in
    ~/.claude/agents; `harness=False` leaves the Node gates and deny rules out of ~/.claude/settings.json and takes
    ours out when an earlier install put them there (the Python verify-gate becomes the Stop gate).
    A flag left as None keeps the choice saved in config.json (on for a first install), so `bossku update` and
    a plain re-install do not undo it."""
    r = repo_root(root)
    h = home if home is not None else Path.home()
    cfg_path = user_config_dir(h) / "config.json"
    cfg: dict = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    claude, agents, harness = (_saved_choice(cfg, key, flag)
                               for key, flag in (("claude_skills", claude), ("agents", agents), ("harness", harness)))
    agents_dest = agents_skills_dir(h)
    claude_dest = claude_skills_dir(h)
    installed_agents = copy_skills_to(agents_dest, r, profile)
    if claude:
        installed_claude = copy_skills_to(claude_dest, r, profile)
        removed_claude: list[str] = []
    else:
        installed_claude, removed_claude = [], remove_managed_skills(claude_dest, r)
    pruned = prune_stale_skills((agents_dest, claude_dest) if claude else (agents_dest,), set(installed_agents), r)
    agents_support = copy_skill_support(r, agents_dest.parent)
    if claude:
        claude_support = copy_skill_support(r, claude_dest.parent)
    else:
        remove_skill_support(r, claude_dest.parent)
        claude_support = {"references": [], "docs": []}
    installed_agents_references = agents_support["references"]
    installed_claude_references = claude_support["references"]
    agents_n = len(installed_agents)
    claude_n = len(installed_claude)
    if agents_n == 0 or (claude and claude_n == 0):
        raise RuntimeError("install copied zero skills to one or both skill destinations")
    if claude and agents_n != claude_n:
        raise RuntimeError(
            f"skill mirror mismatch: agents={agents_n} claude={claude_n}; re-run `bossku install`"
        )
    contracts_dest = claude_agents_dir(h)
    if agents:
        contracts_installed, contracts_kept = copy_agents_to(contracts_dest, r)
        contracts_removed: list[str] = []
    else:
        contracts_installed, contracts_kept, contracts_removed = [], [], remove_managed_agents(contracts_dest)
    library = library_dir(h)
    if profile == "lean":
        # Skills the hosts do not list stay installed whole, one `bossku skills show <id>` away.
        library_ids = copy_library_to(library, r, set(installed_agents))
        copy_skill_support(r, library.parent)
    else:
        library_ids = []
        remove_tree(library)
        retire_support_files(library.parent)   # the lean profile used to put shared files here
    (user_config_dir(h) / "routing-cache.json").unlink(missing_ok=True)   # older installs wrote it; nothing reads it
    routing_copy = install_routing_copy(r, h)
    cfg["installed_from"] = str(r)
    cfg["profile"] = profile
    cfg["claude_skills"], cfg["agents"], cfg["harness"] = claude, agents, harness
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
    hooks_result = install_hooks(home=h, harness=harness, root=r)
    memory_instructions = install_auto_memory_instructions(h)
    return {
        "agents_skills": str(agents_dest),
        "claude_skills": str(claude_dest),
        "claude_skills_removed": removed_claude,
        "claude_agents": str(contracts_dest),
        "agents_installed": contracts_installed,
        "agents_kept": contracts_kept,
        "agents_removed": contracts_removed,
        "agents_count": agents_n,
        "claude_count": claude_n,
        "installed_count": agents_n,
        "library_dir": str(library) if library_ids else None,
        "library_count": len(library_ids),
        "routing_index": routing_copy,
        "pruned_skills": pruned,
        "agents_reference_count": len(installed_agents_references),
        "claude_reference_count": len(installed_claude_references),
        "agents_doc_count": len(agents_support["docs"]),
        "claude_doc_count": len(claude_support["docs"]),
        "tools": tools_coverage_map(agents_dest, claude_dest, claude),
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
    # install_user keeps the saved --no-claude / --no-agents / --no-harness choices when none is given.
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
                if child.name not in removed:
                    removed.append(child.name)
    removed_agents = remove_managed_agents(claude_agents_dir(h))
    remove_tree(library_dir(h))
    for name in ("references", "site", "docs"):   # shared files the lean library links to
        remove_tree(user_config_dir(h) / name)
    routing_index_copy(h).unlink(missing_ok=True)
    routing_signature_path(h).unlink(missing_ok=True)
    try:
        source = repo_root(effective_root)
    except FileNotFoundError:
        source = None                              # no repo to compare with: delete nothing
    if source is not None:
        for dest in (agents_skills_dir(h), claude_skills_dir(h)):
            remove_skill_support(source, dest.parent)
    hooks_removed = uninstall_hooks(home=h) if purge else None
    cleaned = remove_instruction_blocks(h) if purge else []
    if purge and cfg_path.is_file():
        cfg_path.unlink()
    cache = user_config_dir(h) / "routing-cache.json"
    if purge and cache.is_file():
        cache.unlink()
    return {"removed_skills": removed, "removed_agents": removed_agents, "purged_config": purge,
            "hooks_removed": hooks_removed, "cleaned_instructions": cleaned}
