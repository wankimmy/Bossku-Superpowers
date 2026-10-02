from __future__ import annotations

import json
import shutil
from pathlib import Path

from bossku import __version__
from bossku.memory import init_memory_templates
from bossku.install import copy_skill_support
from bossku.paths import MARKER_END, MARKER_START, project_meta_dir, repo_root
from bossku.skills import copy_skills_to, skills_dir
from bossku.validate import claude_imports_agents_md, omp_imports_agents_md


# Always loaded, so every word is paid for in every session: concrete steps beat general advice.
PROJECT_BLOCK = (
    "BosskuAI is active.\n"
    "Code changes: list every requirement in the request, make exactly that change, and leave other behavior "
    "alone. Before you finish, run the project's tests once (if there are none, write and run one short check "
    "of the requirements) and fix the code, not the test, until it passes; do not repeat a check that already "
    "passed. Say what you ran and what you could not verify. Work in few turns: make independent tool calls "
    "together in one step, do not re-read files you just wrote, and put code and its check in one "
    "edit-and-run step.\n"
    "Skills: load a skill from the list first when one fits the job (Skill tool, or `bossku skills show <id>`). "
    "Superpowers skills cover process (plans, debugging, TDD); Anti-Slop covers UI, copy and comment quality. "
    "Add complementary skills only for distinct parts of the request, never two that do the same job. "
    'If none fits a non-trivial job, run `bossku skills find "<task>"` once. Skip skills for one-line tasks.\n'
    "Memory: project notes are in your context at session start (or run `bossku memory-brief --project "
    "<project-root>` once). Automatically save, before the final reply, every rule or decision the user "
    "states (with its reason), plus a plan for later or a gotcha that cost you time; never a summary of what you "
    "built or changed, and not what the code already shows. Save it with "
    '`bossku remember --project <project-root> --kind decision|plan|learning|project "<note>"`; one call is '
    "enough and most tasks save nothing. Use the commands, not the files: never open or edit .bossku/ or "
    "~/.bosskuai/ by hand, never save secrets, and never write .bossku/memory when memory_storage is obsidian.\n"
    "Grounding is always on: say when evidence is insufficient instead of guessing, and cite file:line or "
    "command output."
    # antislop runs an install wizard and a blocking "during or after?" question unless the
    # entry file carries its pointer block; Bossku already installs all six skills.
    "\n<!-- antislop:start -->\n"
    "antislop: Bossku installs all six antislop skills; skip the install wizard. "
    "Mode: during the work for new UI, after it for audits of existing UI, unless the user says otherwise.\n"
    "<!-- antislop:end -->"
)


def _managed_block(content: str) -> str:
    return f"{MARKER_START}\n{content.strip()}\n{MARKER_END}"


def upsert_managed_block(existing: str, block: str) -> str:
    wrapped = _managed_block(block)
    if MARKER_START in existing and MARKER_END in existing:
        start = existing.index(MARKER_START)
        end = existing.index(MARKER_END) + len(MARKER_END)
        return existing[:start] + wrapped + existing[end:]
    if existing.strip():
        return existing.rstrip() + "\n\n" + wrapped + "\n"
    return wrapped + "\n"


def init_project(
    project: Path,
    *,
    root: Path | None = None,
    home: Path | None = None,
    portable: bool = False,
    profile: str = "core",
) -> dict:
    project = project.resolve()
    project.mkdir(parents=True, exist_ok=True)
    meta = project_meta_dir(project)
    meta.mkdir(parents=True, exist_ok=True)
    meta_file = meta / "project.json"
    metadata = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
    metadata["bossku_version"] = __version__
    metadata.setdefault("profile", profile)
    meta_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    memory_dir = init_memory_templates(project, home=home)
    agents_path = project / "AGENTS.md"
    claude_path = project / "CLAUDE.md"
    omp_dir = project / ".omp"
    omp_agents_path = omp_dir / "AGENTS.md"
    omp_config_path = omp_dir / "config.yml"
    block = PROJECT_BLOCK
    if agents_path.exists():
        agents_path.write_text(
            upsert_managed_block(agents_path.read_text(encoding="utf-8"), block),
            encoding="utf-8",
        )
    else:
        agents_path.write_text(
            "# Project Agents\n\n" + _managed_block(block) + "\n",
            encoding="utf-8",
        )
    claude_stub = "@AGENTS.md\n"
    if claude_path.exists():
        text = claude_path.read_text(encoding="utf-8")
        if not claude_imports_agents_md(text):
            claude_path.write_text(claude_stub + "\n" + text, encoding="utf-8")
    else:
        claude_path.write_text(claude_stub, encoding="utf-8")
    omp_dir.mkdir(parents=True, exist_ok=True)
    omp_stub = "@../AGENTS.md\n"
    if omp_agents_path.exists():
        text = omp_agents_path.read_text(encoding="utf-8")
        if not omp_imports_agents_md(text):
            omp_agents_path.write_text(omp_stub + "\n" + text, encoding="utf-8")
    else:
        omp_agents_path.write_text(omp_stub, encoding="utf-8")
    if not omp_config_path.exists():
        omp_config_path.write_text(
            "tools:\n  approvalMode: write\n",
            encoding="utf-8",
        )
    portable_info = None
    if portable:
        dest = project / ".bossku" / "skills"
        copy_skills_to(dest, root, profile)
        copy_skill_support(repo_root(root), dest.parent)
        portable_info = str(dest)
    return {
        "project": str(project),
        "meta": str(meta_file),
        "memory": str(memory_dir),
        "omp": str(omp_dir),
        "portable_skills": portable_info,
    }
