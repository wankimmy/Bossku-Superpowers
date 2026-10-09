from __future__ import annotations

import json
import shutil
from pathlib import Path

from bossku import __version__
from bossku.memory import init_memory_templates
from bossku.install import DEFAULT_VOICE_RULE, copy_skill_support
from bossku.paths import MARKER_END, MARKER_START, project_meta_dir, repo_root
from bossku.skills import copy_skills_to, skills_dir
from bossku.validate import claude_imports_agents_md, omp_imports_agents_md


# Always loaded, so every word is paid for in every session: concrete steps beat general advice.
PROJECT_BLOCK = (
    "BosskuAI is active.\n"
    + DEFAULT_VOICE_RULE + "\n"
    + "Code changes: list every requirement in the request, make exactly that change, and leave other behavior "
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
    "enough and most tasks save nothing. Use the commands, not the files: never open or edit .bossku/memory, "
    ".bossku/project.json or ~/.bosskuai/ by hand (.bossku/DESIGN.md and .bossku/shots/ are yours to read and "
    "write), never save secrets, and never write .bossku/memory when memory_storage is obsidian.\n"
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
    start = existing.find(MARKER_START)
    if start >= 0:
        end = existing.find(MARKER_END, start)
        if end < 0:   # appending a second block would later swallow the text between the two; the user must close it
            raise ValueError(f"the start marker {MARKER_START} has no end marker {MARKER_END} after it: "
                             "add the end marker where the block ends, or remove the start marker")
        return existing[:start] + wrapped + existing[end + len(MARKER_END):]
    if existing.strip():
        return existing.rstrip() + "\n\n" + wrapped + "\n"
    return wrapped + "\n"


DESIGN_STUB = """# DESIGN.md - design source of truth

Status: STUB. Filled in by the BosskuAI designer contract before the first real UI work
(`agents/designer.md`, skill `bosskuai-design-systems`). Delete this file if the project has no UI.
Every UI change reads this file first; every value here is a decision, not a default.

## 1. Visual Theme & Atmosphere
Design Read (one line: who it is for, the mood, the closest real reference):
Direction (named theme / real design system / labelled aesthetic) and why:

## 2. Color Palette & Roles
Primitive palette (5-8 hex) and semantic roles (primary, accent, surface, text, success, warning, error). One accent.

## 3. Typography Rules
Display / body / mono families (a deliberate choice, not Inter by default) and the hierarchy table (size, weight, line-height, tracking).

## 4. Component Stylings
Buttons, inputs, cards, navigation, feedback: every state (default, hover, focus, active, disabled, loading, empty, error).

## 5. Layout Principles
Spacing base unit and scale, grid, content max-width, one radius system.

## 6. Depth & Elevation
Shadow / surface tokens. Glass and gradients only with a stated reason.

## 7. Do's and Don'ts
Brand-specific guardrails. Always: no placeholder people or companies, no filler verbs, no fake-perfect numbers, no em-dash decoration, real images and real SVG marks.

## 8. Responsive Behavior
Breakpoints 390 / 768 / 1440, touch targets 44px, what collapses where. Screenshots at 390 and 1440 before any UI is called done.

## 9. Agent Prompt Guide
Paste-ready component prompt using the tokens above.
"""


DESIGN_FILES = ("DESIGN.md", "design/DESIGN.md")


def init_design_stub(project: Path) -> str | None:
    """Scaffold .bossku/DESIGN.md unless the project already keeps a design source of truth. Returns its path, or None.

    The places to look are the ones hooks/session-start.mjs reads: .bossku/DESIGN.md, DESIGN.md, design/DESIGN.md."""
    dest = project_meta_dir(project) / "DESIGN.md"
    if dest.is_file() or any((project / rel).is_file() for rel in DESIGN_FILES):
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(DESIGN_STUB, encoding="utf-8")
    return str(dest)


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
    design_md = init_design_stub(project)
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
        "design_md": design_md,
        "omp": str(omp_dir),
        "portable_skills": portable_info,
    }
