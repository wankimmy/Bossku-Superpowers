"""Optional tools that go with the skills: see which are installed, and install the safe ones when asked.

Skills such as `markitdown`, `bosskuai-headroom` or `moli-webfetch` document a separate program. This module knows
how to find each program and what installing it takes. Nothing is installed by default and nothing is installed
without `--yes`. Programs whose official installer is a script piped into a shell (or an unsigned binary) are never
run by this module: it prints the official instructions for the user to follow.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# How a tool is installed. Only the first three are ever run by `install --yes`.
PIP, NPM_GLOBAL, NPM_PROJECT, MANUAL = "pip", "npm-global", "npm-project", "manual"
RUNNABLE = (PIP, NPM_GLOBAL, NPM_PROJECT)


@dataclass(frozen=True)
class Tool:
    id: str
    title: str
    kind: str
    skills: tuple[str, ...]
    purpose: str
    spec: str = ""                       # pip requirement or npm package
    commands: tuple[str, ...] = ()       # executables that mean "installed" when found on PATH
    module: str = ""                     # python module that means "installed"
    note: str = ""                       # what the user should know before installing (telemetry, binaries...)
    manual: str = ""                     # where to get it when it cannot be installed automatically
    follow_up: tuple[tuple[str, ...], ...] = field(default=())   # commands to run after the install, in order


TOOLS: tuple[Tool, ...] = (
    Tool("headroom", "Headroom", PIP, ("bosskuai-headroom",), "compress bulky tool output before it reaches the model",
         spec="headroom-ai[mcp]", commands=("headroom",), module="headroom",
         note="Apache-2.0. Sends an anonymous usage beacon unless HEADROOM_BEACON=off or DO_NOT_TRACK=1 is set. "
              "Do not run its wrap, deploy or init commands unless the user asks."),
    Tool("markitdown", "MarkItDown", PIP, ("markitdown",), "convert Office files, PDFs and HTML to Markdown",
         spec="markitdown[all]>=0.1.0", commands=("markitdown",), module="markitdown"),
    Tool("graphify", "Graphify", PIP, ("graphify",), "build a knowledge graph from mixed documents and code",
         spec="graphifyy>=0.8.0", commands=("graphify",), module="graphify"),
    Tool("browser-use", "browser-use", PIP, ("browser-use", "remote-browser", "cloud", "open-source"),
         "an agent that drives a live browser", spec="browser-use>=0.11.0", commands=("browser-use",), module="browser_use"),
    Tool("opendataloader-pdf", "OpenDataLoader PDF", PIP, ("odl-pdf",), "extract structured data, tables and bounding boxes from PDFs",
         spec="opendataloader-pdf", commands=("opendataloader-pdf",), module="opendataloader_pdf",
         note="Needs Java 11 or newer. Bind its hybrid server to 127.0.0.1 only."),
    Tool("graft", "Graft", NPM_GLOBAL, ("graft",), "a map of a code base: callers, skeletons, one targeted question",
         spec="@nanonets/graft", commands=("graft",), note="After installing, run `graft build` once in each repository."),
    Tool("e2e", "e2e", NPM_PROJECT, ("bosskuai-agentic-e2e",), "agentic end-to-end tests for web and mobile apps",
         spec="e2e", note="Per project: it edits that project's package.json and writes e2e.config.ts, an example test and "
                          ".gitignore lines. Needs Node 24.8+ (or 22.22.3+). Sends usage telemetry unless "
                          "`npx e2e telemetry disable` or E2E_TELEMETRY_DISABLED=1. Add @e2e-dev/web and ai@^7 as well.",
         follow_up=(("npx", "e2e", "init"),)),
    Tool("archify", "Archify", NPM_GLOBAL, ("bosskuai-archify-diagrams",), "interactive architecture and workflow diagrams as HTML",
         spec="", note="Installed as an agent skill with `npx skills add tt-a1i/archify -g`. Its update check contacts a "
                       "GitHub Pages URL unless the user declines.",
         follow_up=()),
    Tool("moli", "Moli", MANUAL, ("moli-webfetch", "moli-cdp-server"), "fetch JavaScript-rendered pages as Markdown without Chrome",
         commands=("moli",), manual="https://github.com/lexmount/moli/releases/latest",
         note="An unsigned prebuilt binary; the official installer is a script piped into a shell, so it is never run for you."),
    Tool("hindsight", "Hindsight", MANUAL, ("bosskuai-hindsight-memory",), "an optional agent memory service",
         commands=("hindsight",), manual="https://github.com/vectorize-io/hindsight",
         note="Build or download the CLI yourself. Its coding-agent plugins keep transcripts by default; do not enable them."),
    Tool("dcg", "Destructive Command Guard", MANUAL, ("dcg",), "block destructive shell and git commands",
         commands=("dcg",), manual="https://github.com/Dicklesworthstone/destructive_command_guard",
         note="Read the upstream license rider before use."),
)
BY_ID = {tool.id: tool for tool in TOOLS}

# The archify "package" is really a skills install; it has its own fixed command.
ARCHIFY_COMMAND = ("npx", "skills", "add", "tt-a1i/archify", "-g")


def installed(tool: Tool, project: Path | None = None) -> bool:
    if any(shutil.which(cmd) for cmd in tool.commands):
        return True
    if tool.module and importlib.util.find_spec(tool.module) is not None:
        return True
    if tool.id == "e2e":
        package = (project or Path.cwd()) / "package.json"
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        return isinstance(data, dict) and any(
            "e2e" in (data.get(section) or {}) for section in ("dependencies", "devDependencies"))
    if tool.id == "archify":
        home = Path.home()
        return any((home / base / "skills" / "archify").is_dir() for base in (".claude", ".agents", ".codex", ".cursor"))
    return False


def plan(tool: Tool) -> list[list[str]]:
    """The exact commands `install --yes` would run, in order; empty when the tool cannot be installed automatically."""
    if tool.kind == PIP:
        return [[sys.executable, "-m", "pip", "install", tool.spec]]
    if tool.kind == NPM_GLOBAL and tool.id == "archify":
        return [list(ARCHIFY_COMMAND)]
    if tool.kind == NPM_GLOBAL:
        return [["npm", "install", "-g", tool.spec]]
    if tool.kind == NPM_PROJECT:
        return [["npm", "install", "--save-dev", tool.spec, "@e2e-dev/web", "ai@^7"], *[list(c) for c in tool.follow_up]]
    return []


def describe(tool: Tool, project: Path | None = None) -> dict:
    return {"id": tool.id, "title": tool.title, "installed": installed(tool, project), "kind": tool.kind,
            "skills": list(tool.skills), "purpose": tool.purpose, "note": tool.note,
            "install": [" ".join(c) for c in plan(tool)] or ([tool.manual] if tool.manual else []),
            "automatic": tool.kind in RUNNABLE}


def run_install(tool: Tool, *, project: Path | None = None, runner=subprocess.run) -> dict:
    """Run the plan for a pip or npm tool. Manual tools are refused: their installers are not ours to run."""
    if tool.kind not in RUNNABLE and tool.id != "archify":
        return {"id": tool.id, "ok": False, "ran": [],
                "message": f"{tool.title} is installed by hand: {tool.manual}. {tool.note}".strip()}
    cwd = None
    if tool.kind == NPM_PROJECT:
        cwd = (project or Path.cwd())
        if not (cwd / "package.json").is_file():
            return {"id": tool.id, "ok": False, "ran": [], "message": f"{cwd} has no package.json; pass --project <folder>."}
    ran = []
    for command in plan(tool):
        exe = shutil.which(command[0]) or command[0]
        argv = [exe, *command[1:]]
        try:
            result = runner(argv, cwd=str(cwd) if cwd else None, check=False, timeout=900)
        except (OSError, subprocess.SubprocessError) as exc:
            return {"id": tool.id, "ok": False, "ran": ran, "message": f"could not run {' '.join(command)}: {exc}"}
        ran.append(" ".join(command))
        if getattr(result, "returncode", 1) != 0:
            return {"id": tool.id, "ok": False, "ran": ran, "message": f"{' '.join(command)} exited with {result.returncode}"}
    return {"id": tool.id, "ok": True, "ran": ran, "message": f"{tool.title} installed."}


def status_table(project: Path | None = None) -> list[dict]:
    return [describe(tool, project) for tool in TOOLS]
