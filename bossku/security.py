"""Make the security gate run without the user asking for it.

The security gate is a must rule (user decision, 2026-10-28): every change gets a security pass, and a project's
dependencies are checked against the latest advisories every day. Text in AGENTS.md alone is skipped by agents that
never open the skill, so the hooks carry it:
  - the prompt hook adds the rule to every change request, and once a day per project asks for a live dependency
    check before other work;
  - the stop gates (hooks/stop-gate.mjs, bossku/gate.py) hold a turn that changed code, dependencies or infra until
    the reply carries the `Security gate:` verdict line.
Off switch: BOSSKU_SECURITY_GATE=off.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path, PurePath

from bossku.paths import user_config_dir

# Dependency manifests and lockfiles. Same list as MANIFESTS in hooks/stop-gate.mjs.
MANIFESTS = frozenset({
    "package.json", "package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock",
    "requirements.txt", "pyproject.toml", "poetry.lock", "pipfile", "pipfile.lock", "uv.lock",
    "composer.json", "composer.lock", "go.mod", "go.sum", "cargo.toml", "cargo.lock", "gemfile", "gemfile.lock",
    "pom.xml", "build.gradle", "build.gradle.kts", "packages.lock.json", "pubspec.lock",
})
# Infra, CI and agent setup. Same pattern as INFRA in hooks/stop-gate.mjs.
INFRA = re.compile(
    r"(?:^|/)(?:dockerfile[^/]*|docker-compose[^/]*\.ya?ml|compose\.ya?ml|[^/]+\.tf|[^/]+\.tfvars|\.gitlab-ci\.yml|"
    r"\.github/workflows/[^/]+\.ya?ml|\.mcp\.json|nginx[^/]*\.conf|serverless\.ya?ml|vercel\.json|netlify\.toml)$",
    re.I)
VERDICT = re.compile(r"\bsecurity gate:", re.I)

_CHANGE = re.compile(
    r"\b(?:fix|implement|add|build|create|write|refactor|update|upgrade|bump|install|change|modify|patch|remove|"
    r"delete|migrate|deploy|integrate|connect|enable|rewrite|replace|make(?! sure)|buat(?:kan)?|tambah(?:kan)?|"
    r"ubah|betulkan|baiki|bina|pasang|naik ?taraf)\b", re.I)

CHANGE_REMINDER = (
    "BosskuAI security gate (must rule): this request changes the project, so load bosskuai-security-gate and run "
    "its pass on the change: quick by default, deep for auth, payments, tenant data, secrets, uploads, public "
    "endpoints, infra/CI or agent tools. Check changed dependencies against live feeds (OSV.dev, GitHub Advisories, "
    "CISA KEV), never memory. Alert only on High and Critical. End the reply with the line `Security gate: PASS | BLOCK`; the stop "
    "gate holds the turn until it is there.")
DAILY_REMINDER = (
    "BosskuAI daily dependency check (must rule, first prompt today in this project): before other work, check "
    "{files} against live feeds: run an installed scanner (osv-scanner, npm audit, pip-audit, composer audit, "
    "govulncheck, cargo audit) or query OSV.dev and GitHub Advisories, then match hits against CISA KEV (see "
    "threat-intel.md in bosskuai-security-gate). Report only High and Critical hits, each with KEV status and the fixed version, in "
    "one short `Live intel:` block; with none, say nothing about it. Then do what the user asked. Do not upgrade anything without the user's go-ahead.")


def is_off() -> bool:
    return os.environ.get("BOSSKU_SECURITY_GATE", "").lower() in {"off", "0", "false"}


def is_security_relevant(path: str) -> bool:
    """A dependency manifest or an infra/CI/agent config file (code files are judged by the stop gate's own list)."""
    posix = str(path).replace("\\", "/")
    return PurePath(posix).name.lower() in MANIFESTS or bool(INFRA.search(posix))


def _manifests_in(project: Path) -> list[str]:
    try:
        return sorted(p.name for p in project.iterdir() if p.is_file() and p.name.lower() in MANIFESTS)
    except OSError:
        return []


def _daily_due(project: str, home: Path | None, today: str) -> list[str]:
    """The manifests to check when this project has not had its check today; records today so it asks once."""
    if not project:
        return []
    root = Path(project)
    files = _manifests_in(root)
    if not files:
        return []
    stamp = user_config_dir(home) / "security-checks.json"
    key = str(root.resolve()).lower() if os.name == "nt" else str(root.resolve())
    try:
        seen = json.loads(stamp.read_text(encoding="utf-8")) if stamp.is_file() else {}
    except (OSError, ValueError):
        seen = {}
    if not isinstance(seen, dict) or seen.get(key) == today:
        return []
    seen[key] = today
    try:
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.write_text(json.dumps(seen, indent=2, sort_keys=True), encoding="utf-8")
    except OSError:
        return []   # cannot record it: stay quiet rather than ask on every prompt
    return files


def security_reminders(prompt: str, project: str = "", *, home: Path | None = None,
                       today: str | None = None) -> list[str]:
    """The security lines for a typed prompt: the daily dependency check when due, and the rule for a change."""
    if is_off():
        return []
    lines = []
    files = _daily_due(project, home, today or date.today().isoformat())
    if files:
        shown = ", ".join(files[:6]) + (f" (+{len(files) - 6} more)" if len(files) > 6 else "")
        lines.append(DAILY_REMINDER.format(files=shown))
    if _CHANGE.search(prompt[:4000]):
        lines.append(CHANGE_REMINDER)
    return lines
