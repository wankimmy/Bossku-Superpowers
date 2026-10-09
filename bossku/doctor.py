from __future__ import annotations

import json
import os
import re
from pathlib import Path

from bossku.hooks import (
    BRIEF_EVENT, BRIEF_MARKER, GATE_EVENT, GATE_MARKER, HARNESS_MARKER, HINT_EVENT, HINT_MARKER, HOOK_MARKER,
    _commands, _owned, codex_hint_commands, harness_status, hooks_status, plugin_double_load,
)
from bossku.hint import hint_mode
from bossku.index import skill_index_signature
from bossku.init_project import PROJECT_BLOCK, upsert_managed_block
from bossku.install import AGENT_FILES, AGENT_SIGNATURE, claude_agents_dir
from bossku.memory import load_user_config
from bossku.paths import (
    MARKER_END, MARKER_START, agents_skills_dir, claude_skills_dir, library_dir, repo_root, routing_signature_path,
)
from bossku.skills import NOT_INSTALLED, count_managed_skills, is_managed_skill_name, load_lean, skills_dir, validate_skills
from bossku.validate import claude_imports_agents_md, omp_imports_agents_md

# What `bossku hooks install` puts in ~/.claude/settings.json: (label, event, marker).
CLAUDE_HOOK_PIECES = (
    ("sync (Stop)", "Stop", HOOK_MARKER),
    ("sync (SessionEnd)", "SessionEnd", HOOK_MARKER),
    ("skill-hint", HINT_EVENT, HINT_MARKER),
    ("verify-gate", GATE_EVENT, GATE_MARKER),
    ("session-brief", BRIEF_EVENT, BRIEF_MARKER),
)
GATE_SWITCHES = ("BOSSKU_VERIFY_GATE", "BOSSKU_STOP_GATE", "BOSSKU_GUARD", "BOSSKU_POST_EDIT", "BOSSKU_SLOP_LINT")


def _missing_program(command: str) -> str | None:
    """The absolute program a hook command starts with, when that file is gone."""
    match = re.match(r'\s*(?:"([^"]+)"|(\S+))', command)
    exe = (match.group(1) or match.group(2)) if match else ""
    return exe if exe and Path(exe).is_absolute() and not Path(exe).exists() else None


def count_managed_agents(dest: Path) -> int:
    """Subagent contracts in a folder that carry our signature; a user's own file of the same name is not counted."""
    total = 0
    for name in AGENT_FILES:
        try:
            total += AGENT_SIGNATURE in (dest / name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    return total


def claude_hook_state(home: Path) -> tuple[list[str], list[str], list[str]]:
    """(installed pieces, missing pieces, problems) of the BosskuAI hooks in ~/.claude/settings.json. Read-only."""
    path = home / ".claude" / "settings.json"
    hooks: object = {}
    problems: list[str] = []
    if path.is_file():
        try:
            hooks = json.loads(path.read_text(encoding="utf-8")).get("hooks", {})
        except (OSError, ValueError, AttributeError):
            problems.append("~/.claude/settings.json is not valid JSON; fix it by hand")
    for entries in hooks.values() if isinstance(hooks, dict) else ():
        for command in _commands(entries) if isinstance(entries, list) else ():
            script = re.search(r'"([^"]+\.mjs)"', command)
            if HARNESS_MARKER in command and script and not Path(script.group(1)).is_file():
                problems.append(
                    f"claude_code harness hook runs {script.group(1)}, which no longer exists; run `bossku install` "
                    "from your BosskuAI checkout to rewrite it"
                )
    present: list[str] = []
    missing: list[str] = []
    for label, event, marker in CLAUDE_HOOK_PIECES:
        bucket = hooks.get(event) if isinstance(hooks, dict) else None
        entries = [e for e in bucket if _owned(e, marker)] if isinstance(bucket, list) else []
        (present if entries else missing).append(label)
        for command in _commands(entries):
            gone = _missing_program(command)
            if gone:
                problems.append(
                    f"claude_code {label} hook runs {gone}, which no longer exists; fix the path in ~/.claude/settings.json "
                    "(`bossku hooks install` rewrites it but also re-adds any hook you removed)"
                )
    return present, missing, sorted(set(problems))


def _body(text: str) -> str:
    """A skill without its frontmatter: the lean profile rewrites only the description there."""
    if text.startswith("---"):
        close = re.search(r"^---[ \t]*$", text[3:], re.MULTILINE)
        if close:
            return text[3 + close.end():]
    return text


def stale_skills(source: Path, home: Path, profile: str | None) -> list[str]:
    """Installed skill copies whose text no longer matches the repo. Absent copies are not drift."""
    base = skills_dir(source)
    listed = set(load_lean(source)["descriptions"]) if profile == "lean" else set()
    folders = [agents_skills_dir(home), claude_skills_dir(home)] + ([library_dir(home)] if profile == "lean" else [])
    stale: set[str] = set()
    for folder in folders:
        if not folder.is_dir():
            continue
        for child in folder.iterdir():
            installed, original = child / "SKILL.md", base / child.name / "SKILL.md"
            if child.name in NOT_INSTALLED or not installed.is_file() or not original.is_file():
                continue
            if not is_managed_skill_name(child.name, source):
                continue
            try:
                a, b = installed.read_text(encoding="utf-8"), original.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                stale.add(child.name)
                continue
            if (_body(a) != _body(b)) if child.name in listed else (a != b):
                stale.add(child.name)
    return sorted(stale)


def routing_copy_issue(source: Path, home: Path) -> str | None:
    """Words for the index copy in ~/.bosskuai when it no longer matches the skills in `source`. A missing copy is
    not an issue: an older install has none, and the prompt hook then reads the repo's own index."""
    try:
        stored = routing_signature_path(home).read_text(encoding="utf-8").strip()
        current = skill_index_signature(source)
    except OSError:                                  # no copy, or no skills folder (validate_skills reports that)
        return None
    if stored == current:
        return None
    return ("the skill index copy in ~/.bosskuai is older than the skills in the repo, so the prompt hook reads the "
            "repo's index instead; run `bossku skills index` if you edited a skill, then `bossku update`")


def gather_doctor_issues(
    root: Path | None = None,
    home: Path | None = None,
    *,
    project: Path | None = None,
) -> list[str]:
    issues: list[str] = []
    try:
        r = repo_root(root)
    except FileNotFoundError as exc:
        issues.append(str(exc))
        r = None
    else:
        issues.extend(validate_skills(r))

    cfg = load_user_config(home)
    h = home if home is not None else Path.home()
    claude_skills_on = cfg.get("claude_skills", True) is not False   # `bossku install --no-claude` turns it off
    if not cfg.get("installed_from"):
        issues.append("user install not detected; run `bossku install`")
    else:
        installed_from = Path(cfg["installed_from"])
        if not installed_from.is_dir():
            issues.append(
                f"install source {installed_from} is missing, so `bossku update` fails; "
                "run `bossku install` from your BosskuAI checkout"
            )
        agents_path = agents_skills_dir(h)
        claude_path = claude_skills_dir(h)
        for label, path in (
            ("~/.agents/skills", agents_path),
            ("~/.claude/skills", claude_path),
        ):
            if not path.is_dir() and (claude_skills_on or path is agents_path):
                issues.append(f"missing skill directory {label}; run `bossku install`")
        if r is not None and agents_path.is_dir() and (claude_path.is_dir() or not claude_skills_on):
            agents_n = count_managed_skills(agents_path, r)
            claude_n = count_managed_skills(claude_path, r) if claude_skills_on else 0
            if agents_n == 0:
                issues.append("no managed skills in ~/.agents/skills; run `bossku install`")
            if claude_skills_on and claude_n == 0:
                issues.append("no managed skills in ~/.claude/skills; run `bossku install`")
            if agents_n > 0 and claude_n > 0 and agents_n != claude_n:
                issues.append(
                    f"skill mirror mismatch: agents={agents_n} claude={claude_n}; run `bossku update`"
                )
        # Compare with the repo `bossku update` would copy from, not with the one doctor happens to run in.
        source = root.resolve() if root is not None else installed_from
        if source.is_dir():
            try:
                stale = stale_skills(source, h, cfg.get("profile"))
            except FileNotFoundError:
                stale = []                    # no skills directory there; validate_skills reports it
            if stale:
                shown = ", ".join(stale[:5]) + (f" and {len(stale) - 5} more" if len(stale) > 5 else "")
                issues.append(f"installed skills differ from the repo: {shown}; run `bossku update`")
            copy_issue = routing_copy_issue(source, h)
            if copy_issue:
                issues.append(copy_issue)
        if cfg.get("profile") == "lean":
            library = library_dir(h)
            if not library.is_dir() or not any((c / "SKILL.md").is_file() for c in library.iterdir() if c.is_dir()):
                issues.append("lean profile has no skill library; run `bossku update`")
        # A missing piece (say the verify-gate) can be a deliberate choice, so only broken hooks are issues.
        issues.extend(claude_hook_state(h)[2])
        for command in codex_hint_commands(h):
            gone = _missing_program(command)
            if gone:
                issues.append(f"codex skill-hint hook runs {gone}, which no longer exists; "
                              "`bossku hooks install` rewrites it")

    # A plugin next to a local install loads everything twice.
    plugin = plugin_double_load(h)
    if plugin["plugin_enabled"]:
        if r is not None and count_managed_skills(claude_skills_dir(h), r) > 0:
            issues.append(
                f"the BosskuAI plugin is enabled AND ~/.claude/skills holds managed copies: every skill loads twice "
                "per session. Run `bossku install --no-claude` (the plugin serves Claude Code) or disable the plugin "
                f"(`/plugin disable {plugin['plugin']}`) and keep the local install"
            )
        if plugin["plugin_has_hooks"] and harness_status(h)["hooks"]:
            issues.append(
                "the BosskuAI plugin ships hooks AND the harness gates are in ~/.claude/settings.json: the gates fire "
                f"twice. Disable the plugin (`/plugin disable {plugin['plugin']}`); the local install keeps working without it"
            )

    if project is not None:
        proj = project.resolve()
        agents_file = proj / "AGENTS.md"
        claude_file = proj / "CLAUDE.md"
        omp_agents_file = proj / ".omp" / "AGENTS.md"
        omp_config_file = proj / ".omp" / "config.yml"
        if not agents_file.is_file():
            issues.append(f"missing project AGENTS.md at {proj}; run `bossku init`")
        else:
            text = agents_file.read_text(encoding="utf-8")
            start = text.find(MARKER_START)
            if start < 0:
                issues.append(f"project AGENTS.md missing BosskuAI managed block; run `bossku init {proj}`")
            elif text.find(MARKER_END, start) < 0:
                issues.append("project AGENTS.md managed block has no end marker; add it or remove the start marker")
            # This repo's own AGENTS.md is the rule source, so its block is a short stub on purpose.
            elif proj != r and upsert_managed_block(text, PROJECT_BLOCK) != text:
                issues.append(f"project AGENTS.md managed block is out of date; run `bossku init {proj}`")
        if not claude_file.is_file():
            issues.append(f"missing project CLAUDE.md at {proj}; run `bossku init`")
        elif not claude_imports_agents_md(claude_file.read_text(encoding="utf-8")):
            issues.append(
                f"project CLAUDE.md must include bare @AGENTS.md; run `bossku init {proj}`"
            )
        if not omp_agents_file.is_file():
            issues.append(f"missing project .omp/AGENTS.md at {proj}; run `bossku init`")
        elif not omp_imports_agents_md(omp_agents_file.read_text(encoding="utf-8")):
            issues.append(
                f"project .omp/AGENTS.md must include bare @../AGENTS.md; run `bossku init {proj}`"
            )
        if not omp_config_file.is_file():
            issues.append(f"missing project .omp/config.yml at {proj}; run `bossku init`")

    return issues


def format_doctor_success(
    root: Path | None,
    home: Path | None,
    *,
    version: str,
    project: Path | None = None,
) -> list[str]:
    h = home if home is not None else Path.home()
    r = repo_root(root)
    agents_path = agents_skills_dir(h)
    claude_path = claude_skills_dir(h)
    n = count_managed_skills(agents_path, r)
    lines = [f"doctor: ok (bossku {version})"]
    lines.append(
        f"  cursor, codex, opencode, omp: {agents_path} ({n} managed skills)"
    )
    saved = load_user_config(home)
    if saved.get("claude_skills", True) is False:
        lines.append("  claude_code: skills off (`bossku install --no-claude`); a plugin or project copy serves it")
    else:
        lines.append(f"  claude_code: {claude_path} ({n} managed skills)")
    contracts = count_managed_agents(claude_agents_dir(h))
    if contracts:
        lines.append(f"  claude_code agents: {contracts} of {len(AGENT_FILES)} contracts")
    elif saved.get("agents", True) is False:   # a plain `bossku install` keeps this choice, so it is not the fix
        lines.append("  claude_code agents: off (`bossku install --no-agents`)")
    else:
        lines.append("  claude_code agents: none installed; run `bossku install`")
    if project is not None:
        lines.append(f"  project instructions: ready at {project.resolve()}")
    else:
        lines.append(
            "  project instructions: run `bossku init <project>` for AGENTS.md, "
            "CLAUDE.md, and .omp/"
        )
    present, missing, _ = claude_hook_state(h)
    gates = harness_status(h)
    if gates["hooks"]:
        missing = [piece for piece in missing if piece != "verify-gate"]   # the Node stop gate does that job
    if not present:
        hooks = "none installed (opted out)"
    else:
        hooks = ", ".join(present) + (f" (not installed: {', '.join(missing)})" if missing else "")
    lines.append(f"  claude_code hooks: {hooks}")
    if (h / ".codex").is_dir():
        lines.append("  codex skill-hint: " + ("wired" if codex_hint_commands(h) else "not installed; run `bossku hooks install`"))
    lines.append(f"  skill hint mode: {hint_mode(home)}")
    if gates["hooks"]:
        lines.append("  harness gates: guard, post-edit lint, stop gate, session contract"
                     + (" + deny rules" if gates["deny_rules"] else " (deny rules missing)"))
    elif gates["events"]:
        lines.append(f"  harness gates: partial ({', '.join(gates['events'])}); run `bossku install`")
    elif saved.get("harness", True) is False:
        lines.append("  harness gates: off (`bossku install --no-harness`)")
    else:
        lines.append("  harness gates: not installed; run `bossku install`")
    plugin = plugin_double_load(h)
    if plugin["plugin_enabled"]:
        lines.append(f"  plugin: {plugin['plugin']} enabled (cached version {plugin['version'] or 'unknown'})")
    switches = [f"{name}={os.environ[name]}" for name in GATE_SWITCHES if name in os.environ]
    lines.append(f"  gate switches set in this shell: {', '.join(switches) if switches else 'none'}")
    status = hooks_status(h)
    installed = [tool for tool, on in status.items() if on]
    if installed:
        lines.append(f"  denser Obsidian auto-sync hooks: {', '.join(sorted(installed))}")
    else:
        lines.append(
            "  denser Obsidian auto-sync hooks: none installed; run `bossku hooks install` "
            "for denser Obsidian auto-sync (per-turn / session-end / after-response)"
        )
    return lines
