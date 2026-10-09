from __future__ import annotations

import json
import re
from pathlib import Path

from bossku.index import index_is_stale, index_path
from bossku.install import AGENT_FILES, AGENT_SIGNATURE, DEFAULT_VOICE_RULE
from bossku.paths import repo_root
from bossku.skills import (
    _parse_frontmatter,
    is_managed_skill_name,
    list_skill_ids,
    load_provenance,
    load_vendored_ids,
    pack_stocktake,
    skills_dir,
    validate_lean,
    validate_skills,
)


REQUIRED_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    ".omp/AGENTS.md",
    ".omp/config.yml",
    "README.md",
    "pyproject.toml",
    "skills/aliases.json",
    "skills/vendored.json",
)

REQUIRED_AGENTS = (
    "orchestrator.md",
    "planner.md",
    "executor.md",
    "auditor.md",
    "final-reviewer.md",
)

# What a Claude Code subagent may list in `tools`, and take as `model` (a full `claude-...` id is also fine).
KNOWN_AGENT_TOOLS = frozenset({
    "Agent", "Bash", "Edit", "Glob", "Grep", "LSP", "MultiEdit", "NotebookEdit", "PowerShell", "Read", "Skill", "Task",
    "TodoWrite", "WebFetch", "WebSearch", "Write",
})
KNOWN_AGENT_MODELS = frozenset({"sonnet", "opus", "haiku", "inherit"})
RUNTIME_CORE_END = "<!-- runtime-core:end -->"
# These run commands to check work, so a contract without Bash cannot do its job.
VERIFYING_AGENTS = ("executor.md", "auditor.md", "final-reviewer.md", "designer.md")

CLAUDE_AGENTS_IMPORT = "@AGENTS.md"
OMP_AGENTS_IMPORT = "@../AGENTS.md"
# Always loaded in every session, so growth is a cost: raise this on purpose, not by accident.
AGENTS_MD_MAX_CHARS = 16000
# Files that repeat the voice rule word for word.
VOICE_RULE_COPIES = ("AGENTS.md", ".cursor/rules/bosskuai.mdc", *(f"agents/{name}" for name in REQUIRED_AGENTS))
PLUGIN_NAME = "bossku-superpower"
MARKETPLACE_NAME = "bossku-superpower-marketplace"
CODEX_MARKETPLACE_NAME = "bossku-superpower"


def package_version(root: Path) -> str:
    text = (root / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise ValueError("pyproject.toml missing version")
    return match.group(1)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _path_exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def _validate_manifest_version(
    errors: list[str],
    label: str,
    manifest_version: str | None,
    expected: str,
) -> None:
    if manifest_version is None:
        errors.append(f"{label}: missing version")
        return
    if manifest_version != expected:
        errors.append(
            f"{label}: version {manifest_version!r} does not match pyproject.toml {expected!r}"
        )


def _validate_component_paths(
    errors: list[str],
    root: Path,
    label: str,
    manifest: dict,
    fields: tuple[str, ...],
) -> None:
    for field in fields:
        value = manifest.get(field)
        if value is None:
            continue
        paths = value if isinstance(value, list) else [value]
        for rel in paths:
            if not _path_exists(root, rel):
                errors.append(f"{label}: missing {field} path: {rel}")


def validate_plugin_manifests(root: Path) -> list[str]:
    errors: list[str] = []
    expected_version = package_version(root)

    claude_plugin = root / ".claude-plugin" / "plugin.json"
    claude_marketplace = root / ".claude-plugin" / "marketplace.json"
    cursor_plugin = root / ".cursor-plugin" / "plugin.json"
    cursor_marketplace = root / ".cursor-plugin" / "marketplace.json"
    codex_plugin = root / ".codex-plugin" / "plugin.json"
    codex_marketplace = root / ".agents" / "plugins" / "marketplace.json"
    opencode_config = root / ".opencode" / "opencode.jsonc"

    required = {
        "claude plugin manifest": claude_plugin,
        "claude marketplace manifest": claude_marketplace,
        "cursor plugin manifest": cursor_plugin,
        "cursor marketplace manifest": cursor_marketplace,
        "codex plugin manifest": codex_plugin,
        "codex marketplace manifest": codex_marketplace,
        "opencode config": opencode_config,
    }
    for label, path in required.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(root).as_posix()}")

    if errors:
        return errors

    try:
        claude_plugin_data = _load_json(claude_plugin)
        claude_marketplace_data = _load_json(claude_marketplace)
        cursor_plugin_data = _load_json(cursor_plugin)
        cursor_marketplace_data = _load_json(cursor_marketplace)
        codex_plugin_data = _load_json(codex_plugin)
        codex_marketplace_data = _load_json(codex_marketplace)
        opencode_data = _load_json(opencode_config)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid plugin JSON: {exc}")
        return errors

    if claude_plugin_data.get("name") != PLUGIN_NAME:
        errors.append("claude plugin manifest: name must be bossku-superpower")
    if claude_marketplace_data.get("name") != MARKETPLACE_NAME:
        errors.append("claude marketplace manifest: name must be bossku-superpower-marketplace")
    if cursor_plugin_data.get("name") != PLUGIN_NAME:
        errors.append("cursor plugin manifest: name must be bossku-superpower")
    if codex_plugin_data.get("name") != PLUGIN_NAME:
        errors.append("codex plugin manifest: name must be bossku-superpower")
    if codex_marketplace_data.get("name") != CODEX_MARKETPLACE_NAME:
        errors.append("codex marketplace manifest: name must be bossku-superpower")

    _validate_manifest_version(
        errors,
        "claude plugin manifest",
        claude_plugin_data.get("version"),
        expected_version,
    )
    _validate_manifest_version(
        errors,
        "cursor plugin manifest",
        cursor_plugin_data.get("version"),
        expected_version,
    )
    _validate_manifest_version(
        errors,
        "codex plugin manifest",
        codex_plugin_data.get("version"),
        expected_version,
    )

    for label, data in (
        ("claude marketplace manifest", claude_marketplace_data),
        ("cursor marketplace manifest", cursor_marketplace_data),
    ):
        _validate_manifest_version(
            errors, f"{label} metadata", (data.get("metadata") or {}).get("version"), expected_version
        )
    for label, data in (
        ("claude marketplace manifest", claude_marketplace_data),
        ("cursor marketplace manifest", cursor_marketplace_data),
        ("codex marketplace manifest", codex_marketplace_data),
    ):
        for entry in data.get("plugins", []):
            if entry.get("name") == PLUGIN_NAME:
                _validate_manifest_version(errors, f"{label} plugin", entry.get("version"), expected_version)

    init_file = root / "bossku" / "__init__.py"
    found = (
        re.search(r'^__version__\s*=\s*"([^"]+)"', init_file.read_text(encoding="utf-8"), re.MULTILINE)
        if init_file.is_file()
        else None
    )
    _validate_manifest_version(errors, "bossku/__init__.py", found.group(1) if found else None, expected_version)

    _validate_component_paths(
        errors,
        root,
        "claude plugin manifest",
        claude_plugin_data,
        ("skills", "agents"),
    )
    _validate_component_paths(
        errors,
        root,
        "cursor plugin manifest",
        cursor_plugin_data,
        ("skills", "agents", "rules"),
    )
    _validate_component_paths(
        errors,
        root,
        "codex plugin manifest",
        codex_plugin_data,
        ("skills",),
    )

    claude_plugins = claude_marketplace_data.get("plugins", [])
    if not any(
        entry.get("name") == PLUGIN_NAME and entry.get("source") == "./"
        for entry in claude_plugins
    ):
        errors.append(
            "claude marketplace manifest: must list bossku-superpower with source ./"
        )

    cursor_plugins = cursor_marketplace_data.get("plugins", [])
    if not any(
        entry.get("name") == PLUGIN_NAME and entry.get("source") == "./"
        for entry in cursor_plugins
    ):
        errors.append(
            "cursor marketplace manifest: must list bossku-superpower with source ./"
        )

    codex_plugins = codex_marketplace_data.get("plugins", [])
    codex_entry = next(
        (entry for entry in codex_plugins if entry.get("name") == PLUGIN_NAME),
        None,
    )
    if codex_entry is None:
        errors.append("codex marketplace manifest: missing bossku-superpower plugin entry")
    else:
        source = codex_entry.get("source", {})
        # Codex resolves a local source from the marketplace root (the repo), not from .agents/plugins.
        if source.get("source") != "local" or source.get("path") != "./":
            errors.append(
                "codex marketplace manifest: bossku-superpower source must be local ./"
            )
        policy = codex_entry.get("policy", {})
        if policy.get("installation") != "AVAILABLE":
            errors.append(
                "codex marketplace manifest: bossku-superpower policy.installation must be AVAILABLE"
            )
        if policy.get("authentication") != "ON_INSTALL":
            errors.append(
                "codex marketplace manifest: bossku-superpower policy.authentication must be ON_INSTALL"
            )

    # opencode_data is parsed above only to prove the file is valid JSON: OpenCode reads the root AGENTS.md
    # and ~/.agents/skills on its own, and a `references` block resolved against the wrong folder.
    return errors


def _agent_tools(value: object) -> list[str]:
    """The tools a contract lists, whether the frontmatter writes `[Read, Bash]` or `Read, Bash`."""
    items = value if isinstance(value, list) else str(value or "").split(",")
    return [str(item).strip().strip("\"'") for item in items if str(item).strip()]


def validate_agents(root: Path) -> list[str]:
    """Every subagent contract has the frontmatter Claude Code reads (name, description, tools, model) and its core block."""
    agents = root / "agents"
    if not agents.is_dir():
        return ["missing agents/"]
    errors: list[str] = []
    for name in AGENT_FILES:
        path = agents / name
        label = f"agents/{name}"
        if not path.is_file():
            errors.append(f"missing agent contract: {label}")
            continue
        text = path.read_text(encoding="utf-8")
        front = _parse_frontmatter(text)
        if not front:
            errors.append(f"{label}: missing YAML frontmatter (name, description, tools, model)")
            continue
        if str(front.get("name", "")).strip() != path.stem:
            errors.append(f"{label}: frontmatter name must be {path.stem}")
        if not str(front.get("description", "")).strip():
            errors.append(f"{label}: missing description")
        tools = _agent_tools(front.get("tools"))
        if not tools:
            errors.append(f"{label}: tools must list the allowed Claude Code tools explicitly")
        for tool in tools:
            if tool.split("(")[0] not in KNOWN_AGENT_TOOLS and not tool.startswith("mcp__"):
                errors.append(f"{label}: unknown tool {tool} (not a Claude Code tool; it would be dropped)")
        model = str(front.get("model", "")).strip()
        if model and model not in KNOWN_AGENT_MODELS and not model.startswith("claude-"):
            errors.append(f"{label}: model {model!r} is not a Claude Code value (sonnet|opus|haiku|inherit|claude-*)")
        if AGENT_SIGNATURE not in text or RUNTIME_CORE_END not in text:
            errors.append(f"{label}: missing runtime-core block")
        if name in VERIFYING_AGENTS and "Bash" not in tools:
            errors.append(f"{label}: must include Bash, or it cannot run the pass signal it is contracted to check")
    return errors


def validate_hooks(root: Path) -> list[str]:
    """The optional hook harness: every script hooks.json runs exists, and none prints an unresolved placeholder."""
    hooks = root / "hooks"
    if not hooks.is_dir():
        return []
    errors: list[str] = []
    manifest = hooks / "hooks.json"
    if manifest.is_file():
        try:
            text = manifest.read_text(encoding="utf-8")
            json.loads(text)
        except ValueError as exc:
            errors.append(f"hooks/hooks.json is not valid JSON: {exc}")
        else:
            for rel in sorted(set(re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)", text))):
                if not (root / rel).is_file():
                    errors.append(f"hooks/hooks.json runs a missing script: {rel}")
    for script in sorted(hooks.glob("*.mjs")):
        if "<plugin-root>" in script.read_text(encoding="utf-8"):
            errors.append(f"hooks/{script.name} prints the unresolved placeholder <plugin-root>")
    return errors


def validate_instructions(root: Path) -> list[str]:
    """Always-on text stays inside its size budget, and the voice rule matches everywhere it is copied."""
    errors: list[str] = []
    agents_md = root / "AGENTS.md"
    if agents_md.is_file():
        size = len(agents_md.read_text(encoding="utf-8"))
        if size > AGENTS_MD_MAX_CHARS:
            errors.append(
                f"AGENTS.md is {size} characters, over the {AGENTS_MD_MAX_CHARS} always-on budget "
                "(trim it, or raise AGENTS_MD_MAX_CHARS in bossku/validate.py on purpose)"
            )
    rule = " ".join(DEFAULT_VOICE_RULE.split())
    for rel in VOICE_RULE_COPIES:
        path = root / rel
        if path.is_file() and rule not in " ".join(path.read_text(encoding="utf-8").split()):
            errors.append(f"{rel}: voice rule differs from DEFAULT_VOICE_RULE in bossku/install.py")
    return errors


def _has_bare_import(text: str, import_line: str) -> bool:
    """Require a live adapter line rather than a Markdown code example."""
    fence_char = ""
    fence_length = 0
    for line in text.splitlines():
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char:
            if (
                fence
                and fence.group(1)[0] == fence_char
                and len(fence.group(1)) >= fence_length
                and not fence.group(2).strip()
            ):
                fence_char = ""
            continue
        if fence:
            # Backtick fences cannot have backticks in their info string.
            if fence.group(1)[0] == "~" or "`" not in fence.group(2):
                fence_char = fence.group(1)[0]
                fence_length = len(fence.group(1))
            continue
        if re.fullmatch(r" {0,3}" + re.escape(import_line) + r"[ \t]*", line):
            return True
    return False


def claude_imports_agents_md(text: str) -> bool:
    """True if CLAUDE.md contains the canonical import outside Markdown code."""
    return _has_bare_import(text, CLAUDE_AGENTS_IMPORT)


def omp_imports_agents_md(text: str) -> bool:
    """True if .omp/AGENTS.md imports the canonical project AGENTS.md."""
    return _has_bare_import(text, OMP_AGENTS_IMPORT)


def validate_repo(root: Path | None = None) -> list[str]:
    errors: list[str] = []
    r = repo_root(root)
    for rel in REQUIRED_FILES:
        if not (r / rel).is_file():
            errors.append(f"missing required file: {rel}")
    claude_path = r / "CLAUDE.md"
    if claude_path.is_file():
        if not claude_imports_agents_md(claude_path.read_text(encoding="utf-8")):
            errors.append(
                "CLAUDE.md must include a bare @AGENTS.md import line for Claude Code"
            )
    omp_agents_path = r / ".omp" / "AGENTS.md"
    if omp_agents_path.is_file():
        if not omp_imports_agents_md(omp_agents_path.read_text(encoding="utf-8")):
            errors.append(
                ".omp/AGENTS.md must include a bare @../AGENTS.md import line for OMP"
            )
    errors.extend(validate_agents(r))
    try:
        skills_dir(r)
    except FileNotFoundError:
        errors.append("missing skills directory")
    errors.extend(validate_skills(r))
    errors.extend(validate_lean(r))
    if not index_path(r).is_file():
        errors.append("missing skills/skill-index.json (run `bossku skills index`)")
    elif index_is_stale(r):
        errors.append(
            "skills/skill-index.json is stale for the current skills "
            "(run `bossku skills index`)"
        )
    vendored = load_vendored_ids(r)
    for sid in vendored:
        if sid not in set(list_skill_ids(r)):
            errors.append(f"vendored skill missing folder: {sid}")
    # Provenance completeness is deterministic, so it is an error. Whether a pack is
    # *due* for review depends on today's date and only ever warns - see `_stocktake`.
    provenance, _ = load_provenance(r)
    for row in pack_stocktake(r):
        meta = provenance.get(row["pack"], {})
        if not meta:
            errors.append(
                f"vendored pack {row['pack']} has no provenance entry in skills/vendored.json"
            )
        elif not row["last_synced"]:
            errors.append(f"vendored pack {row['pack']} is missing last_synced")
        elif not meta.get("upstream"):
            errors.append(f"vendored pack {row['pack']} is missing upstream")
    legacy_product = [
        "app/artisan",
        "web/package.json",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "data/postgres",
    ]
    for rel in legacy_product:
        if (r / rel).exists():
            errors.append(f"legacy product path still present: {rel}")
    errors.extend(validate_plugin_manifests(r))
    errors.extend(validate_instructions(r))
    errors.extend(validate_hooks(r))
    return errors
