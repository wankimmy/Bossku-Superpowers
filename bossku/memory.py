from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from bossku.paths import ensure_inside, project_memory_dir, user_config_path, vault_export_dir
from bossku.redact import redact

ALLOWED_KINDS = frozenset({"decision", "plan", "learning", "project"})
KIND_TO_FILE = {
    "decision": "decisions.md",
    "plan": "plans.md",
    "learning": "learnings.md",
    "project": "project.md",
}


def load_user_config(home: Path | None = None) -> dict:
    path = user_config_path(home)
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_user_config(data: dict, home: Path | None = None) -> None:
    path = user_config_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def memory_project_root(project: Path, *, home: Path | None = None) -> Path:
    return _memory_project_root(project, load_user_config(home))


def _memory_project_root(project: Path, cfg: dict) -> Path:
    resolved = project.resolve()
    roots = cfg.get("memory_project_roots", [])
    if not isinstance(roots, list) or any(not isinstance(root, str) for root in roots):
        raise ValueError("memory_project_roots must be a list of project paths")
    matches = [Path(root).resolve() for root in roots
               if resolved == Path(root).resolve() or Path(root).resolve() in resolved.parents]
    return max(matches, key=lambda root: len(root.parts)) if matches else resolved


def memory_directory(project: Path, *, home: Path | None = None) -> Path:
    return _memory_location(project, home=home)[2]


def _memory_location(project: Path, *, home: Path | None = None) -> tuple[str, Path, Path]:
    cfg = load_user_config(home)
    storage = cfg.get("memory_storage", "repo")
    if storage == "repo":
        return storage, project.resolve(), project_memory_dir(project)
    if storage != "obsidian":
        raise ValueError(f"unknown memory_storage: {storage!r}")
    vault_path = cfg.get("obsidian_vault")
    if not vault_path:
        raise ValueError("Obsidian memory requires a configured obsidian_vault")
    vault = Path(vault_path).resolve()
    if not vault.is_dir():
        raise ValueError("Obsidian vault unavailable; memory was not saved")
    project_root = _memory_project_root(project, cfg)
    namespaces = cfg.get("memory_project_namespaces", {})
    if not isinstance(namespaces, dict) or any(
        not isinstance(root, str) or not root.strip()
        or not isinstance(name, str) or not name.strip()
        for root, name in namespaces.items()
    ):
        raise ValueError("memory_project_namespaces must map project paths to nonempty names")
    names = {name.strip() for root, name in namespaces.items()
             if Path(root).resolve() == project_root}
    if len(names) > 1:
        raise ValueError("memory_project_namespaces has conflicting names for this project")
    namespace = next(iter(names), project_root.name)
    target = vault_export_dir(vault, namespace)
    target = ensure_inside(target, vault)
    project_roots = (project.resolve(), project_root)
    if any(target == root or root in target.parents for root in project_roots):
        raise ValueError("Obsidian memory must be outside the code repository")
    _check_memory_owner(project_root, target, home=home)
    return storage, project_root, target


def _memory_claim_path(memory_dir: Path, *, home: Path | None = None) -> Path:
    identity = os.path.normcase(str(memory_dir.resolve()))
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return user_config_path(home).parent / "memory-project-registry" / f"{digest}.json"


def _check_memory_owner(project_root: Path, memory_dir: Path, *, home: Path | None = None) -> bool:
    claim = _memory_claim_path(memory_dir, home=home)
    try:
        data = json.loads(claim.read_text(encoding="utf-8"))
        if (not isinstance(data, dict)
                or not isinstance(data.get("project_root"), str)
                or not data["project_root"].strip()
                or not Path(data["project_root"]).is_absolute()
                or not isinstance(data.get("memory_dir"), str)
                or not Path(data["memory_dir"]).is_absolute()
                or Path(data["memory_dir"]).resolve() != memory_dir):
            raise ValueError("invalid claim fields")
        owner = Path(data["project_root"]).resolve()
    except FileNotFoundError as exc:
        if claim.is_symlink():
            raise ValueError(f"Invalid memory ownership claim: {claim}") from exc
        return False
    except (OSError, ValueError) as exc:
        raise ValueError(f"Invalid memory ownership claim: {claim}") from exc
    if owner != project_root:
        raise ValueError(
            f"Memory directory already belongs to another project: {memory_dir}. "
            "Configure a distinct memory_project_namespaces entry; existing notes were not moved."
        )
    return True


def _claim_memory_owner(project_root: Path, memory_dir: Path, *, home: Path | None = None) -> None:
    claim = _memory_claim_path(memory_dir, home=home)
    claim.parent.mkdir(parents=True, exist_ok=True)
    try:
        with claim.open("x", encoding="utf-8") as stream:
            json.dump({"project_root": str(project_root), "memory_dir": str(memory_dir)}, stream)
    except FileExistsError:
        if not _check_memory_owner(project_root, memory_dir, home=home):
            raise ValueError(f"Memory ownership claim disappeared: {claim}")


def remember(
    project: Path,
    kind: str,
    note: str,
    *,
    home: Path | None = None,
) -> dict:
    if kind not in ALLOWED_KINDS:
        raise ValueError(f"kind must be one of {sorted(ALLOWED_KINDS)}")
    cleaned = redact(note.strip())
    if not cleaned:
        raise ValueError("note cannot be empty after redaction")
    storage, project_root, mem_dir = _memory_location(project, home=home)
    if storage == "obsidian":
        _claim_memory_owner(project_root, mem_dir, home=home)
    mem_dir.mkdir(parents=True, exist_ok=True)
    target = mem_dir / KIND_TO_FILE[kind]
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    entry = f"\n## {stamp}\n\n{cleaned}\n"
    with target.open("a", encoding="utf-8") as stream:
        if target.stat().st_size == 0:
            stream.write(f"# {kind.title()}s\n")
        stream.write(entry)
    if storage == "obsidian":
        vault_result = {"status": "ok", "storage": "obsidian", "vault_dir": str(mem_dir)}
        return _saved(kind, target, vault_result)
    sync_state = _load_sync_state(project)
    sync_state.setdefault("pending", []).append(kind)
    _save_sync_state(project, sync_state)
    return _saved(kind, target, sync_project(project, home=home))


def _saved(kind: str, target: Path, vault: dict) -> dict:
    """The result of a successful save. The first two keys say so plainly: agents that only saw a vault status of
    "skipped" took a saved note for a failure and retried, wrote test notes, and edited the memory files by hand."""
    status = vault.get("status")
    if status == "ok" and vault.get("storage") == "obsidian":
        where = f"in the vault: {target}"
    elif status == "ok":
        where = f"to {target} and copied it to the vault"
    elif status == "pending":
        where = f"to {target}; the vault is unavailable, so the copy waits for the next sync"
    else:
        where = f"to {target}; no vault is configured, so there is no second copy"
    message = f"Saved the {kind} note {where}. Nothing more to do."
    return {"saved": True, "message": message, "kind": kind, "file": str(target), "vault": vault}


def sync_project(project: Path, *, home: Path | None = None) -> dict:
    cfg = load_user_config(home)
    storage = cfg.get("memory_storage", "repo")
    if storage not in {"repo", "obsidian"}:
        raise ValueError(f"unknown memory_storage: {storage!r}")
    vault_path = cfg.get("obsidian_vault")
    if not vault_path:
        return {"status": "skipped", "reason": "no vault configured"}
    vault = Path(vault_path)
    if not vault.is_dir():
        return {"status": "pending", "reason": "vault unavailable"}
    if cfg.get("memory_storage", "repo") == "obsidian":
        mem_dir = memory_directory(project, home=home)
        return {"status": "ok", "storage": "obsidian", "exported": [],
                "conflicts": [], "vault_dir": str(mem_dir)}
    project_name = project.resolve().name
    export_base = vault_export_dir(vault, project_name)
    ensure_inside(export_base, vault)
    export_base.mkdir(parents=True, exist_ok=True)
    mem_dir = project_memory_dir(project)
    exported: list[str] = []
    conflicts: list[str] = []
    state = _load_sync_state(project)
    file_hashes: dict[str, str] = state.get("file_hashes", {})
    for kind, filename in KIND_TO_FILE.items():
        src = mem_dir / filename
        if not src.is_file():
            continue
        content = src.read_text(encoding="utf-8")
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        dest = export_base / filename
        ensure_inside(dest, vault)
        if dest.is_file():
            prev = file_hashes.get(filename)
            current_vault = hashlib.sha256(dest.read_bytes()).hexdigest()
            if prev and current_vault != prev and digest != current_vault:
                conflict = export_base / f"{filename}.conflict.md"
                conflict.write_text(dest.read_text(encoding="utf-8"), encoding="utf-8")
                conflicts.append(str(conflict))
        dest.write_text(content, encoding="utf-8")
        file_hashes[filename] = digest
        exported.append(filename)
    state["file_hashes"] = file_hashes
    state["pending"] = []
    state["last_sync"] = datetime.now(timezone.utc).isoformat()
    _save_sync_state(project, state)
    return {"status": "ok", "exported": exported, "conflicts": conflicts, "vault_dir": str(export_base)}


def _sync_state_path(project: Path) -> Path:
    return project_memory_dir(project) / "sync-state.json"


def _load_sync_state(project: Path) -> dict:
    path = _sync_state_path(project)
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_sync_state(project: Path, state: dict) -> None:
    path = _sync_state_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def init_memory_templates(project: Path, *, home: Path | None = None) -> Path:
    storage, project_root, mem = _memory_location(project, home=home)
    if storage == "obsidian":
        _claim_memory_owner(project_root, mem, home=home)
    mem.mkdir(parents=True, exist_ok=True)
    templates = {
        "project.md": "# Project\n\nOne-paragraph summary of what this repo is and who it serves.\n",
        "decisions.md": "# Decisions\n\nDurable decisions only.\n",
        "plans.md": "# Plans\n\nActive and recent plans.\n",
        "learnings.md": "# Learnings\n\nVerified lessons worth repeating.\n",
        "handoff.md": "# Handoff\n\nEphemeral continuation state. Clear when done.\n",
    }
    for name, body in templates.items():
        path = mem / name
        if not path.exists():
            path.write_text(body, encoding="utf-8")
    return mem
