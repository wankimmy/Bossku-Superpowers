"""The agents/*.md contracts rendered for the other coding tools' subagent formats.

Claude Code reads agents/*.md as they are (bossku.install copies them to ~/.claude/agents). Codex, OpenCode, Cursor
and Devin each have their own subagent file format, so the same contract (frontmatter description, the body as the
instructions) is rendered once per tool, with a model chosen for that tool's providers (ROLE_MODELS). A tool gets
its files only when its user config folder exists, which means the user runs that tool.

Every rendered file carries the contract body, so it carries AGENT_SIGNATURE: a file without it is the user's own and
is never overwritten or removed.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from bossku.install import AGENT_FILES, AGENT_SIGNATURE, claude_agents_dir
from bossku.paths import repo_root
from bossku.skills import _parse_frontmatter, make_path_writable

HOSTS = ("codex", "opencode", "cursor", "devin")

# Model per role and tool, checked against each tool's docs on 2026-10-20. Tiers: the researcher maps code (small and
# fast), the executor and designer build (the main coding model), the planner reasons deeply (the top model), and the
# auditor and final reviewer check the work on a strong model from a different family than the executor wherever the
# tool offers one, so the checker is not the same model that wrote the code. The orchestrator is usually the main
# session itself, so it follows the session. None means no pinned model: the tool's own default for subagents (the
# parent's model in Codex, OpenCode and Cursor; Devin's router).
# - Codex runs OpenAI models only: gpt-6-luna (efficient), gpt-6.1-sol (coding), gpt-6-astra (most capable), from
#   learn.chatgpt.com/docs/models; effort values from its subagents page.
# - OpenCode ids are models.dev's (the registry OpenCode uses), per provider. A role gets the model of the provider
#   the user has set up (opencode_provider); with none of them, the subagent inherits, so nobody gets a model they
#   cannot run. Ollama Cloud picks follow models.dev's metadata (context, price, a code-tuned model), not benchmarks.
# - Cursor: `composer-2.5` and `gpt-5.6-sol` appear in its subagent docs; the Claude 5.5 ids follow the documented
#   `claude-opus-5-5-fast` (cursor.com/docs/models). Cursor falls back to a compatible model when a plan lacks one.
# - Devin takes family names that resolve to the latest version (docs.devin.ai/cli/models): opus, sonnet, swe, codex,
#   gemini. `haiku` is not one, so the researcher uses `swe`, Devin's own fast family.
ROLE_MODELS: dict[str, dict[str, dict[str, str | None]]] = {
    "orchestrator": {"codex": {"model": None, "effort": None},
                     "opencode": {"anthropic": None, "ollama-cloud": None},
                     "cursor": {"model": "inherit"}, "devin": {"model": None}},
    "researcher": {"codex": {"model": "gpt-6-luna", "effort": "low"},
                   "opencode": {"anthropic": "claude-haiku-5-5", "ollama-cloud": "deepseek-v4.1-flash"},
                   "cursor": {"model": "composer-2.5"}, "devin": {"model": "swe"}},
    "planner": {"codex": {"model": "gpt-6-astra", "effort": "high"},
                "opencode": {"anthropic": "claude-opus-5-5", "ollama-cloud": "kimi-k3"},
                "cursor": {"model": "claude-opus-5-5[effort=high]"}, "devin": {"model": "opus"}},
    "designer": {"codex": {"model": "gpt-6.1-sol", "effort": "medium"},
                 "opencode": {"anthropic": "claude-sonnet-5-5", "ollama-cloud": "kimi-k2.7-code"},
                 "cursor": {"model": "claude-sonnet-5-5"}, "devin": {"model": "sonnet"}},
    "executor": {"codex": {"model": "gpt-6.1-sol", "effort": "medium"},
                 "opencode": {"anthropic": "claude-sonnet-5-5", "ollama-cloud": "kimi-k2.7-code"},
                 "cursor": {"model": "claude-sonnet-5-5"}, "devin": {"model": "sonnet"}},
    "auditor": {"codex": {"model": "gpt-6-astra", "effort": "high"},
                "opencode": {"anthropic": "claude-opus-5-5", "ollama-cloud": "glm-5.3"},
                "cursor": {"model": "gpt-5.6-sol"}, "devin": {"model": "codex"}},
    "final-reviewer": {"codex": {"model": "gpt-6-astra", "effort": "high"},
                       "opencode": {"anthropic": "claude-opus-5-5", "ollama-cloud": "glm-5.3"},
                       "cursor": {"model": "gpt-5.6-sol"}, "devin": {"model": "opus"}},
}
OPENCODE_PROVIDERS = ("ollama-cloud", "anthropic")   # checked in this order when the config names no default model

WRITE_TOOLS = frozenset({"Edit", "Write", "MultiEdit", "NotebookEdit"})
# Roles whose shell use is inspection only (git log, ls), so a tool's read-only mode fits them. The auditor and final
# reviewer run test suites, which write caches and reports, and the orchestrator writes the handoff and runs
# `bossku remember`, so read-only mode would block the jobs they exist to do.
INSPECT_ONLY = frozenset({"researcher", "planner"})


def host_dirs(home: Path) -> dict[str, tuple[Path, Path]]:
    """Per tool: (the config folder that shows the tool is used, the folder its user-level subagents live in)."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA") if home == Path.home() else None
        devin_root = Path(appdata) / "devin" if appdata else home / "AppData" / "Roaming" / "devin"
    else:
        devin_root = home / ".config" / "devin"
    return {
        "codex": (home / ".codex", home / ".codex" / "agents"),
        "opencode": (home / ".config" / "opencode", home / ".config" / "opencode" / "agents"),
        "cursor": (home / ".cursor", home / ".cursor" / "agents"),
        "devin": (devin_root, devin_root / "agents"),
    }


def _split(text: str) -> tuple[dict, str]:
    """(frontmatter, body) of a contract; the body is everything after the closing `---`."""
    front = _parse_frontmatter(text)
    match = re.match(r"---[^\n]*\n.*?^---[ \t]*$\n?", text, re.MULTILINE | re.DOTALL)
    return front, (text[match.end():] if match else text).strip() + "\n"


def _tools(front: dict) -> set[str]:
    raw = front.get("tools", "")
    items = raw if isinstance(raw, list) else re.split(r"[,\s]+", str(raw).strip("[] "))
    return {str(t).strip(" \"'") for t in items if str(t).strip(" \"'")}


def _yaml_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)   # a JSON string is a valid YAML double-quoted scalar


def _toml_multiline(value: str) -> str:
    if "'''" not in value:
        return "'''\n" + value + "'''"            # a literal string: no escapes at all
    escaped = value.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return '"""\n' + escaped + '"""'


def opencode_provider(home: Path) -> str | None:
    """The OpenCode provider whose models the subagents should use, or None to let them inherit the session model.

    The user's default `model` in the OpenCode config wins when it names a provider in OPENCODE_PROVIDERS. Otherwise
    the first of those providers that is set up: a stored login (`/connect` writes auth.json) or a provider block in
    the config. Only files count, not the shell's environment: the shell that runs bossku is not the one OpenCode runs
    in, and doctor would flip between stale and current with it. Nothing from the files is kept."""
    data_home = Path(os.environ["XDG_DATA_HOME"]) if home == Path.home() and os.environ.get("XDG_DATA_HOME") else home / ".local" / "share"
    found: set[str] = set()
    try:
        logins = json.loads((data_home / "opencode" / "auth.json").read_text(encoding="utf-8"))
        found |= {p for p in OPENCODE_PROVIDERS if p in logins}
    except (OSError, ValueError, TypeError):
        pass
    preferred = None
    for name in ("opencode.json", "opencode.jsonc"):
        try:
            text = (home / ".config" / "opencode" / name).read_text(encoding="utf-8")
        except OSError:
            continue
        # A key, not a value: `"model": "anthropic/claude-..."` under another provider (OpenRouter) does not count.
        found |= {p for p in OPENCODE_PROVIDERS if re.search(rf'"{re.escape(p)}"\s*:', text)}
        default = re.search(r'"model"\s*:\s*"([\w.-]+)/', text)
        if default and default.group(1) in OPENCODE_PROVIDERS and preferred is None:
            preferred = default.group(1)
    if preferred:
        return preferred
    return next((p for p in OPENCODE_PROVIDERS if p in found), None)


def render(host: str, role: str, text: str, *, provider: str | None = None) -> str:
    """One contract rendered as `host`'s subagent file."""
    front, body = _split(text)
    description = str(front.get("description", "")).strip()
    tools = _tools(front)
    read_only = not (tools & WRITE_TOOLS)
    runs_commands = "Bash" in tools
    choice = ROLE_MODELS[role][host]
    model = choice.get("model")
    if host == "codex":
        lines = [f"name = {_yaml_str(role.replace('-', '_'))}", f"description = {_yaml_str(description)}"]
        if model:
            lines.append(f"model = {_yaml_str(model)}")
        if choice.get("effort"):
            lines.append(f"model_reasoning_effort = {_yaml_str(choice['effort'])}")
        # No [features] shell_tool = false, even for the researcher: Codex reads files through the shell, so turning
        # it off leaves the agent unable to read at all, and Codex has no per-agent edit lock. The contract's own
        # rules keep the researcher read-only there.
        lines.append(f"developer_instructions = {_toml_multiline(body)}")
        return "\n".join(lines) + "\n"
    head = []
    if host == "opencode":
        head += [f"description: {_yaml_str(description)}", "mode: subagent"]
        picked = choice.get(provider) if provider else None
        if picked:
            head.append(f"model: {provider}/{picked}")
        if read_only:
            # No bash and no task for the researcher: a subagent it starts could edit for it.
            head += ["permission:", "  edit: deny"] + ([] if runs_commands else ["  bash: deny", "  task: deny"])
    elif host == "cursor":
        head += [f"name: {role}", f"description: {_yaml_str(description)}", f"model: {model or 'inherit'}"]
        if read_only and role in INSPECT_ONLY:
            head.append("readonly: true")   # readonly also blocks state-changing shell commands, so not for test runners
    elif host == "devin":
        head += [f"name: {role}", f"description: {_yaml_str(description)}"]
        if model:
            head.append(f"model: {model}")
        if read_only and not runs_commands:
            head += ["allowed-tools:", "  - read", "  - grep", "  - glob"]
    else:
        raise ValueError(f"unknown host {host}")
    return "---\n" + "\n".join(head) + "\n---\n\n" + body


def file_name(host: str, role: str) -> str:
    return f"{role}.toml" if host == "codex" else f"{role}.md"


def _managed(path: Path) -> bool:
    try:
        return AGENT_SIGNATURE in path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def _resolved(path: Path) -> str:
    try:
        return os.path.normcase(str(path.resolve()))
    except OSError:
        return os.path.normcase(str(path.absolute()))


def target_dirs(home: Path) -> tuple[dict[str, Path], dict[str, str]]:
    """(tool -> its subagent folder, tool -> why it is skipped) for the tools in use.

    A folder that is a link to ~/.claude/agents, or to a folder another tool already got, is skipped: writing there
    would replace the Claude Code contract (and its tool lock) with another tool's format, and removing there would
    delete it."""
    taken = {_resolved(claude_agents_dir(home)): "~/.claude/agents"}
    dirs: dict[str, Path] = {}
    skipped: dict[str, str] = {}
    for host, (marker, dest) in host_dirs(home).items():
        if not marker.is_dir():
            continue
        key = _resolved(dest)
        if key in taken:
            skipped[host] = f"{dest} is the same folder as {taken[key]}"
            continue
        taken[key] = str(dest)
        dirs[host] = dest
    return dirs, skipped


def expected_files(root: Path | None, home: Path) -> dict[str, dict[Path, str]]:
    """Per tool that is in use: target path -> the text it should hold."""
    source = repo_root(root) / "agents"
    provider = opencode_provider(home)
    out: dict[str, dict[Path, str]] = {}
    for host, dest in target_dirs(home)[0].items():
        files: dict[Path, str] = {}
        for name in AGENT_FILES:
            role = name[:-3]
            src = source / name
            if role in ROLE_MODELS and src.is_file():
                files[dest / file_name(host, role)] = render(host, role, src.read_text(encoding="utf-8"), provider=provider)
        out[host] = files
    return out


def install_host_agents(root: Path | None, home: Path) -> dict[str, dict[str, list[str]]]:
    """Write every tool's subagents. A same-named file without our signature is the user's own and is kept."""
    result: dict[str, dict[str, list[str]]] = {}
    for host, files in expected_files(root, home).items():
        written, kept = [], []
        for path, text in files.items():
            if path.is_file() and not _managed(path):
                kept.append(path.name)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                make_path_writable(path)
            path.write_bytes(text.encode("utf-8"))
            written.append(path.name)
        result[host] = {"installed": written, "kept": kept}
    for host, why in target_dirs(home)[1].items():
        result[host] = {"installed": [], "kept": [], "skipped": [why]}
    return result


def remove_host_agents(home: Path) -> dict[str, list[str]]:
    """Delete only our files (signature present) from every tool's subagent folder, never through a shared link."""
    removed: dict[str, list[str]] = {}
    linked = target_dirs(home)[1]
    for host, (_, dest) in host_dirs(home).items():
        if host in linked:
            continue
        gone = []
        for name in AGENT_FILES:
            path = dest / file_name(host, name[:-3])
            if path.is_file() and _managed(path):
                make_path_writable(path)
                path.unlink()
                gone.append(path.name)
        if gone:
            removed[host] = gone
    return removed


def outdated_host_agents(root: Path | None, home: Path) -> dict[str, list[str]]:
    """Per tool: our files that are missing or differ from what install would write now (line endings ignored)."""
    stale: dict[str, list[str]] = {}
    for host, files in expected_files(root, home).items():
        names = []
        for path, text in files.items():
            try:
                current = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                names.append(path.name)
                continue
            if _managed(path) and current.replace("\r\n", "\n") != text:
                names.append(path.name)
        if names:
            stale[host] = names
    return stale
