"""Optional tools that go with the skills: see which are installed, and install the safe ones when asked.

Skills such as `markitdown`, `bosskuai-headroom` or `moli-webfetch` document a separate program. This module knows
how to find each program and what installing it takes. Nothing is installed by default and nothing is installed
without `--yes`. Programs whose official installer is a script piped into a shell (or an unsigned binary) are never
run by this module: it prints the official instructions for the user to follow.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# How a tool is installed. Only the first four are ever run by `install --yes`.
PIP, NPM_GLOBAL, NPM_PROJECT, AGENT_SKILL, MANUAL = "pip", "npm-global", "npm-project", "agent-skill", "manual"
RUNNABLE = (PIP, NPM_GLOBAL, NPM_PROJECT, AGENT_SKILL)


@dataclass(frozen=True)
class Tool:
    id: str
    title: str
    kind: str
    skills: tuple[str, ...]
    purpose: str
    spec: str = ""                       # pip requirement, npm package or skill source
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
         spec="@nanonets/graft", commands=("graft",),
         note="Builds a native module while installing, which can need a C++ toolchain (it failed on a Windows machine without Visual Studio). "
              "After installing, run `graft build` once in each repository."),
    Tool("e2e", "e2e", NPM_PROJECT, ("bosskuai-agentic-e2e",), "agentic end-to-end tests for web and mobile apps",
         spec="e2e", note="Per project: it edits that project's package.json and writes e2e.config.ts, an example test and "
                          ".gitignore lines. Needs Node 24.8+ (or 22.22.3+) and a terminal, because `npx e2e init` asks questions. "
                          "Sends usage telemetry unless `npx e2e telemetry disable` or E2E_TELEMETRY_DISABLED=1. "
                          "@e2e-dev/web and ai@7 are installed with it.",
         follow_up=(("npx", "e2e", "init"),)),
    Tool("archify", "Archify", AGENT_SKILL, ("bosskuai-archify-diagrams",), "interactive architecture and workflow diagrams as HTML",
         spec="tt-a1i/archify",
         note="Downloads the skill from github.com/tt-a1i/archify (its latest version, not pinned) with `npx skills add` "
              "and installs it for your agents globally; the installer may ask which agents. Its update check contacts a "
              "GitHub Pages URL unless the user declines."),
    Tool("moli", "Moli", MANUAL, ("moli-webfetch", "moli-cdp-server"), "fetch JavaScript-rendered pages as Markdown without Chrome",
         commands=("moli",), manual="https://github.com/lexmount/moli/releases/latest",
         note="An unsigned prebuilt binary; the official installer is a script piped into a shell, so it is never run for you."),
    Tool("hindsight", "Hindsight", MANUAL, ("bosskuai-hindsight-memory",), "an optional agent memory service",
         commands=("hindsight",), manual="https://github.com/vectorize-io/hindsight",
         note="Set up by hand: Bossku Superpower has no installer for it. Its coding-agent plugins keep transcripts by "
              "default; do not enable them."),
    Tool("dcg", "Destructive Command Guard", MANUAL, ("dcg",), "block destructive shell and git commands",
         commands=("dcg",), manual="https://github.com/Dicklesworthstone/destructive_command_guard",
         note="Its official installer is a script piped into a shell, so it is never run for you. "
              "Read the upstream license rider before use."),
)
BY_ID = {tool.id: tool for tool in TOOLS}


def _which(name: str) -> str | None:
    """Find an executable on PATH, never in the current directory (Windows looks there first, so a planted npm.cmd would win)."""
    here = os.path.normcase(os.path.abspath(os.getcwd()))
    windows = os.name == "nt"
    exts = [e.lower() for e in os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD").split(";") if e] if windows else [""]
    names = [name] if windows and Path(name).suffix.lower() in exts else [name + e for e in exts]
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry or os.path.normcase(os.path.abspath(entry)) == here:
            continue
        for candidate in names:
            path = Path(entry) / candidate
            if path.is_file() and (windows or os.access(path, os.X_OK)):
                return str(path)
    return None


def installed(tool: Tool, project: Path | None = None, home: Path | None = None) -> bool:
    if any(_which(cmd) for cmd in tool.commands):
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
        base = home or Path.home()
        return any((base / folder / "skills" / "archify").is_dir() for folder in (".claude", ".agents", ".codex", ".cursor"))
    return False


def plan(tool: Tool) -> list[list[str]]:
    """The exact commands `install --yes` would run, in order; empty when the tool cannot be installed automatically."""
    if tool.kind == PIP:
        # -P keeps the folder bossku runs in off sys.path, so a pip.py lying there is not run instead of pip
        return [[sys.executable, "-P", "-m", "pip", "install", tool.spec]]
    if tool.kind == AGENT_SKILL:
        return [["npx", "skills", "add", tool.spec, "-g"]]
    if tool.kind == NPM_GLOBAL:
        return [["npm", "install", "-g", tool.spec]]
    if tool.kind == NPM_PROJECT:
        return [["npm", "install", "--save-dev", tool.spec, "@e2e-dev/web", "ai@7"], *[list(c) for c in tool.follow_up]]
    return []


def describe(tool: Tool, project: Path | None = None, home: Path | None = None) -> dict:
    return {"id": tool.id, "title": tool.title, "installed": installed(tool, project, home), "kind": tool.kind,
            "skills": list(tool.skills), "purpose": tool.purpose, "note": tool.note,
            "install": [" ".join(c) for c in plan(tool)] or ([tool.manual] if tool.manual else []),
            "automatic": tool.kind in RUNNABLE}


def _run(argv: list[str], *, cwd: str | None = None, check: bool = False, timeout: int = 900):
    """subprocess.run, except that a timeout stops the whole process tree (on Windows npm.cmd starts node as a child)."""
    process = subprocess.Popen(argv, cwd=cwd)
    try:
        return subprocess.CompletedProcess(argv, process.wait(timeout=timeout))
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(process.pid)], capture_output=True, check=False)
        else:
            process.kill()
        process.wait()
        raise
    except BaseException:
        process.kill()
        raise


def _node_problem() -> str:
    """Why e2e cannot run here, or an empty string. It needs Node 24.8+ or 22.22.3+."""
    node = _which("node")
    if not node:
        return "Node.js was not found on PATH"
    try:
        out = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=30, check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return "`node --version` did not run"
    found = re.match(r"v(\d+)\.(\d+)\.(\d+)", out.strip())
    if not found:
        return f"could not read the Node version from {out.strip()!r}"
    version = tuple(int(n) for n in found.groups())
    if version >= (25, 0, 0) or (version[0] == 24 and version >= (24, 8, 0)) or (version[0] == 22 and version >= (22, 22, 3)):
        return ""
    return f"Node {'.'.join(map(str, version))} is too old (needs 24.8+ or 22.22.3+)"


def run_install(tool: Tool, *, project: Path | None = None, runner=None, node_problem=None) -> dict:
    """Run the plan for a pip or npm tool. Manual tools are refused: their installers are not ours to run."""
    runner = runner or _run
    if tool.kind not in RUNNABLE:
        return {"id": tool.id, "ok": False, "ran": [],
                "message": f"{tool.title} is installed by hand: {tool.manual}. {tool.note}".strip()}
    cwd = None
    if tool.kind == NPM_PROJECT:
        cwd = (project or Path.cwd())
        if not (cwd / "package.json").is_file():
            return {"id": tool.id, "ok": False, "ran": [], "message": f"{cwd} has no package.json; pass --project <folder>."}
        follow = " && ".join(" ".join(c) for c in tool.follow_up)
        if installed(tool, cwd):
            return {"id": tool.id, "ok": True, "ran": [], "message": f"{tool.title} is already in {cwd / 'package.json'}; "
                    + (f"if it is not set up yet, run `{follow}` in that folder." if follow else "nothing to do.")}
        if tool.follow_up and not sys.stdin.isatty():
            return {"id": tool.id, "ok": False, "ran": [], "message": f"nothing was changed: `{follow}` asks questions, so "
                    f"run `bossku tools install {tool.id} --yes` in a terminal."}
        problem = (node_problem or _node_problem)()
        if problem:
            return {"id": tool.id, "ok": False, "ran": [], "message": f"nothing was changed: {problem}."}
    ran = []
    for command in plan(tool):
        exe = _which(command[0]) or command[0]
        argv = [exe, *command[1:]]
        try:
            result = runner(argv, cwd=str(cwd) if cwd else None, check=False, timeout=900)
        except (OSError, subprocess.SubprocessError) as exc:
            return {"id": tool.id, "ok": False, "ran": ran, "message": f"could not run {' '.join(command)}: {exc}"}
        ran.append(" ".join(command))
        if getattr(result, "returncode", 1) != 0:
            return {"id": tool.id, "ok": False, "ran": ran, "message": f"{' '.join(command)} exited with {result.returncode}"}
    return {"id": tool.id, "ok": True, "ran": ran, "message": f"{tool.title} installed."}


def status_table(project: Path | None = None, home: Path | None = None) -> list[dict]:
    return [describe(tool, project, home) for tool in TOOLS]
