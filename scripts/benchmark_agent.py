#!/usr/bin/env python3
"""Real-agent coding benchmark: Claude Code (headless) with and without BosskuAI.

Every run is a real model call. Pass/fail comes from tests the agent never sees; tokens, cost,
turns and time come from Claude Code's own result report. Nothing here touches your Claude
config, your BosskuAI install or your Obsidian vault: each run gets a throwaway project
directory, and the `bossku` command inside it is a shim bound to a throwaway home.

    python scripts/benchmark_agent.py validate --suite benchmarks/tasks/test
    python scripts/benchmark_agent.py run --suite benchmarks/tasks/test --model claude-haiku-4-5-20251001 \\
        --arm baseline --arm after=.@lean+hint+gate+brief --out /tmp/pilot
    python scripts/benchmark_agent.py overhead --model claude-haiku-4-5-20251001 --arm baseline --arm after=.@lean+hint+gate+brief
    python scripts/benchmark_agent.py report /tmp/pilot/runs.jsonl

Suites: `benchmarks/tasks/{dev,test}` (coding), `hard-{dev,test}` (longer projects), `memory` (two sessions each) and
`humaneval:N`. See docs/benchmarks/README.md.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import gzip
import hashlib
import json
import math
import os
import queue
import random
import re
import shutil
import stat
import statistics
import subprocess
import sys
import threading
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Paths the agent's own tooling creates; they are not part of "what the agent changed".
SCAFFOLD_PARTS = {'.bossku', '.claude', '.omp', '__pycache__', '.pytest_cache', '.git'}
# Variables that tie a child process to the desktop session that launched this script.
SESSION_ENV = {
    'CLAUDECODE', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_CODE_HOST_SESSION_ID', 'CLAUDE_CODE_CHILD_SESSION',
    'CLAUDE_CODE_MESSAGING_SOCKET', 'CLAUDE_CODE_MESSAGING_TOKEN', 'CLAUDE_CODE_SESSION_ATTENDED',
}
NON_INTERACTIVE = (
    '\n\nThis is a non-interactive run: nobody can answer questions, so make reasonable assumptions '
    'and finish the work in this directory.'
)
OVERHEAD_PROMPT = 'Reply with exactly the single word: OK'
# A project that has been used before has notes. These are deliberately unrelated to every task, so reading them
# can only cost tokens, never help: BosskuAI's memory feature gets a fair price tag.
SEED_NOTES = (
    ('project', 'Internal helper scripts for the shop team. Owner: operations. Release notes live in docs/changes.md.'),
    ('decision', '2026-08-14: Release notes are written by the on-call engineer on Fridays and reviewed on Mondays.'),
    ('learning', '2026-09-02: The nightly export job times out on files larger than 200 MB; split them first.'),
)


# --------------------------------------------------------------------------- arms and environment

@dataclass(frozen=True)
class Arm:
    name: str
    root: Path | None  # None means "no BosskuAI"
    profile: str = 'full'
    hint: bool = False   # install the UserPromptSubmit skill-hint hook (BosskuAI releases that have it)
    gate: bool = False   # install the Stop verify-gate hook
    brief: bool = False  # install the SessionStart project-notes hook
    lines: tuple = ()    # extra instruction lines (experiments only), named by VARIANT_LINES
    inline: tuple = ()   # skills whose text is placed in the instructions from the start (`+skill:ID`, experiments only)


# One-line instruction experiments: an arm flag such as `+tdd` appends the line to the project instructions of that
# arm's template only, so wording can be compared without copying the whole repository.
VARIANT_LINES = {
    'tdd': ('Test first: before you implement, write a test for every requirement and each edge case, run them to '
            'see them fail, then implement until they all pass.'),
    'batch': ('Work in few turns: make independent tool calls together in one step, do not re-read files you just '
              'wrote, and put code and its check in one edit-and-run step.'),
    'review': ('When the checks pass, reread the request once more, line by line, and look for anything it asks for '
               'that no test or run covered.'),
    'quiet': ('These instructions are already in your context: do not open CLAUDE.md or AGENTS.md, and ignore the '
              '.bossku, .omp and .claude folders.'),
}


@dataclass(frozen=True)
class Prepared:
    template: Path
    shim: Path
    instructions: Path | None
    info: dict
    home: Path   # throwaway home: what `~` means to every process the agent starts


def parse_arm(spec: str) -> Arm:
    if spec == 'baseline':
        return Arm('baseline', None)
    name, _, rest = spec.partition('=')
    if not rest:
        raise SystemExit(f'bad --arm {spec!r}; use "baseline" or NAME=ROOT[@lean|core|full][+hint][+gate][+brief]')
    root, _, profile = rest.partition('@')
    profile, *flags = profile.split('+')
    return Arm(name, Path(root).resolve(), profile or 'full', hint='hint' in flags, gate='gate' in flags,
               brief='brief' in flags,
               lines=tuple(VARIANT_LINES[f] for f in flags if f in VARIANT_LINES),
               inline=tuple(f.split(':', 1)[1] for f in flags if f.startswith('skill:')))


def find_claude(explicit: str | None) -> str:
    if explicit:
        return explicit
    found = shutil.which('claude')
    if found:
        return found
    base = Path(os.environ.get('APPDATA', '')) / 'Claude' / 'claude-code'
    # The desktop app keeps each version as <version>/claude.exe, or <version>/<hash>/claude.exe in newer builds.
    versions = sorted({*base.glob('*/claude.exe'), *base.glob('*/*/claude.exe')},
                      key=lambda p: [int(n) for n in re.findall(r'\d+', p.relative_to(base).parts[0])])
    if versions:
        return str(versions[-1])
    raise SystemExit('claude CLI not found; pass --claude PATH')


def rmtree_force(path: Path, attempts: int = 8) -> None:
    """Remove a tree even when it holds read-only files (git objects are read-only on Windows) or files a
    just-killed process has not released yet. Cleanup never fails a run: a leftover temp folder is harmless."""
    def make_writable_and_retry(func, target, _info):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    for attempt in range(attempts):
        if not path.exists():
            return
        try:
            shutil.rmtree(path, onerror=make_writable_and_retry)
            return
        except OSError:
            time.sleep(1.5)


def write_shim(directory: Path, arm: Arm, home: Path) -> None:
    """A `bossku` on PATH that is isolated: real for BosskuAI arms, "not installed" for the baseline."""
    directory.mkdir(parents=True, exist_ok=True)
    py = sys.executable.replace('\\', '/')
    if arm.root is None:
        sh_text = '#!/bin/sh\necho "bossku: command not found" >&2\nexit 127\n'
        cmd_text = '@echo off\r\necho bossku: command not found 1>&2\r\nexit /b 127\r\n'
    else:
        root = str(arm.root).replace('\\', '/')
        home_s = str(home).replace('\\', '/')
        sh_text = f'#!/bin/sh\nPYTHONPATH="{root}" exec "{py}" -m bossku --home "{home_s}" "$@"\n'
        cmd_text = f'@echo off\r\nset "PYTHONPATH={arm.root}"\r\n"{sys.executable}" -m bossku --home "{home}" %*\r\n'
    (directory / 'bossku').write_text(sh_text, encoding='utf-8', newline='\n')
    (directory / 'bossku.cmd').write_text(cmd_text, encoding='utf-8', newline='')
    try:
        (directory / 'bossku').chmod(0o755)
    except OSError:
        pass


# Credentials the child must not inherit from the launching session; each provider sets its own.
AUTH_ENV = {'ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'CLAUDE_CODE_OAUTH_TOKEN', 'CLAUDE_CODE_OAUTH_SCOPES',
            'CLAUDE_CODE_ACCOUNT_UUID', 'CLAUDE_CODE_ORGANIZATION_UUID', 'CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH'}
OLLAMA_URL = 'https://ollama.com'


def provider_env(args, model: str, config_dir: Path) -> dict[str, str]:
    """How a run reaches its model, and how the user's own Claude setup is kept out of the baseline."""
    if args.provider == 'ollama':
        # A throwaway config dir means no login, no ~/.claude/CLAUDE.md, no user skills: a clean harness.
        key = Path(args.ollama_key_file).read_text(encoding='utf-8').strip()
        return {
            'CLAUDE_CONFIG_DIR': str(config_dir), 'ANTHROPIC_BASE_URL': OLLAMA_URL, 'ANTHROPIC_AUTH_TOKEN': key,
            'ANTHROPIC_MODEL': model, 'ANTHROPIC_DEFAULT_HAIKU_MODEL': model, 'ANTHROPIC_DEFAULT_SONNET_MODEL': model,
            'ANTHROPIC_DEFAULT_OPUS_MODEL': model, 'CLAUDE_CODE_SUBAGENT_MODEL': model,
            'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC': '1',
            # Claude Code finds ~/.claude/CLAUDE.md through the OS account, whatever CLAUDE_CONFIG_DIR or HOME say,
            # so the real BosskuAI memory block leaked into the baseline until every CLAUDE.md was switched off.
            'CLAUDE_CODE_DISABLE_CLAUDE_MDS': '1',
        }
    # Claude Code always reads ~/.claude/CLAUDE.md, which for a BosskuAI user holds BosskuAI's own memory
    # block. Switching every CLAUDE.md off keeps the baseline clean; BosskuAI arms get their instructions
    # through --append-system-prompt-file instead (see build_template).
    return {'CLAUDE_CODE_DISABLE_CLAUDE_MDS': '1'}


def child_env(shim_dir: Path, extra: dict[str, str], home: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in SESSION_ENV and k not in AUTH_ENV}
    if extra.get('ANTHROPIC_AUTH_TOKEN') is None:   # Anthropic provider: keep the user's own login
        env.update({k: v for k, v in os.environ.items() if k in AUTH_ENV})
        # Claude Code finds its login under ~/.claude; keep that, but let everything else see the throwaway home.
        env['CLAUDE_CONFIG_DIR'] = os.environ.get('CLAUDE_CONFIG_DIR') or str(Path.home() / '.claude')
    # Anything the agent runs that resolves `~` (bossku, git, python) lands in the throwaway home, never
    # in the real one: a benchmark must not write notes into your Obsidian vault.
    env.update({'HOME': str(home), 'USERPROFILE': str(home)})
    env.update({
        'CLAUDE_CODE_DISABLE_AUTO_MEMORY': '1',   # no per-project memory files, same for every arm
        'CLAUDE_CODE_DISABLE_CRON': '1',
        'PYTHONDONTWRITEBYTECODE': '1',
        'PYTHONIOENCODING': 'utf-8',
        'GIT_TERMINAL_PROMPT': '0',
        'PATH': str(shim_dir) + os.pathsep + env.get('PATH', ''),
    })
    env.update(extra)
    return env


def sh(cmd: list[str], cwd: Path | None = None, timeout: int | None = 120, env: dict | None = None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                          timeout=timeout, env=env)


def kill_tree(pid: int) -> None:
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'], capture_output=True)
    else:
        try:
            os.killpg(pid, 9)
        except OSError:
            pass


# --------------------------------------------------------------------------- project templates

TEMPLATE_BUILDER = r'''
import json, sys
from pathlib import Path
root = Path(sys.argv[1]); proj = Path(sys.argv[2]); profile = sys.argv[3]; want_hint = sys.argv[4] == "1"; want_gate = sys.argv[5] == "1"
want_brief = sys.argv[6] == "1"; notes = json.loads(sys.argv[7])
extra_lines = json.loads(sys.argv[8]); inline_skills = json.loads(sys.argv[9])
sys.path.insert(0, str(root))
import bossku
assert Path(bossku.__file__).resolve().parent.parent == root, bossku.__file__
from bossku.skills import copy_skills_to
from bossku.install import copy_skill_support, install_user, AUTO_MEMORY_BLOCK
from bossku.init_project import init_project
home = proj.parent / (proj.name + "_home")
home.mkdir(parents=True, exist_ok=True)
# A real user-level install, but into a throwaway home: config, routing cache and (for lean) the library,
# so `bossku skills find/show` behave as they would for a user. Nothing touches the real home.
install_user(root=root, home=home, profile=profile)
init_project(proj, root=root, home=home, portable=False, profile=profile)
for sid in inline_skills:   # a skill the agent starts with, as if it had already been loaded
    body = (root / "skills" / sid / "SKILL.md").read_text(encoding="utf-8")
    if body.startswith("---"):
        body = body.split("---", 2)[2]
    extra_lines.append("## Skill loaded: " + sid + "\n" + body.strip())
if extra_lines:
    from bossku.paths import MARKER_END
    agents_file = proj / "AGENTS.md"
    agents_text = agents_file.read_text(encoding="utf-8")
    assert MARKER_END in agents_text
    agents_file.write_text(agents_text.replace(MARKER_END, "\n".join(extra_lines) + "\n" + MARKER_END, 1), encoding="utf-8")
claude = proj / ".claude"
ids = copy_skills_to(claude / "skills", root, profile)
copy_skill_support(root, claude)
if want_hint:
    from bossku.hooks import ensure_skill_hint_hook
    ensure_skill_hint_hook(proj / ".claude" / "settings.json", command="bossku skill-hint")
if want_gate:
    from bossku.hooks import ensure_verify_gate_hook
    ensure_verify_gate_hook(proj / ".claude" / "settings.json", command="bossku verify-gate")
if want_brief:
    from bossku.hooks import ensure_session_brief_hook
    ensure_session_brief_hook(proj / ".claude" / "settings.json", command="bossku session-brief")
from bossku.memory import remember
for kind, note in notes:
    remember(proj, kind, note, home=home)
for stale in (proj / ".claude").glob("settings.json.bak-*"):   # installer backups are not part of a project
    stale.unlink()
# `bossku install` appends the memory block to the user-level ~/.claude/CLAUDE.md; a throwaway config
# dir has none, so the project CLAUDE.md carries it (used by providers that load CLAUDE.md natively).
cm = proj / "CLAUDE.md"
cm.write_text(cm.read_text(encoding="utf-8").rstrip() + "\n\n" + AUTO_MEMORY_BLOCK + "\n", encoding="utf-8")
# Providers that must switch CLAUDE.md off get the same text through one instructions file instead.
agents = (proj / "AGENTS.md").read_text(encoding="utf-8").strip()
text = "Project instructions (AGENTS.md, checked into the codebase):\n\n" + agents + "\n\n" + AUTO_MEMORY_BLOCK + "\n"
instructions = proj.parent / (proj.name + ".instructions.md")
instructions.write_text(text, encoding="utf-8")
print(json.dumps({"version": bossku.__version__, "skills_installed": len(ids),
                  "instructions": str(instructions), "instruction_chars": len(text)}))
'''


def build_template(arm: Arm, dest: Path) -> dict:
    """Mimic `bossku install` + `bossku init` for one BosskuAI source tree, in an isolated directory."""
    if dest.exists():
        rmtree_force(dest)
    dest.mkdir(parents=True)
    if arm.root is None:
        return {'skills_installed': 0}
    out = sh([sys.executable, '-c', TEMPLATE_BUILDER, str(arm.root), str(dest), arm.profile, '1' if arm.hint else '0',
                      '1' if arm.gate else '0', '1' if arm.brief else '0', json.dumps(SEED_NOTES),
                      json.dumps(list(arm.lines)), json.dumps(list(arm.inline))],
              timeout=300)
    if out.returncode:
        raise SystemExit(f'template build failed for {arm.name}: {out.stderr or out.stdout}')
    return json.loads(out.stdout.strip().splitlines()[-1])


def prepare_arms(arms: list[Arm], work: Path) -> dict[str, Prepared]:
    prepared = {}
    for arm in arms:
        template = work / 'tpl' / arm.name
        info = build_template(arm, template)
        shim = work / 'shim' / arm.name
        home = work / 'tpl' / f'{arm.name}_home'
        home.mkdir(parents=True, exist_ok=True)
        write_shim(shim, arm, home)
        instructions = Path(info['instructions']) if info.get('instructions') else None
        prepared[arm.name] = Prepared(template, shim, instructions, info, home)
        print(f'arm {arm.name}: {info}', flush=True)
    return prepared


def prepare_workdir(arm: Arm, template: Path, seed: Path | None, workdir: Path) -> str:
    """Create the project the agent will work in; returns the seed commit its changes are measured against."""
    if workdir.exists():
        rmtree_force(workdir)
    if arm.root is not None:
        shutil.copytree(template, workdir)
    else:
        workdir.mkdir(parents=True)
    if seed is not None and seed.is_dir():
        shutil.copytree(seed, workdir, dirs_exist_ok=True)
    if not any(p.name != '.git' for p in workdir.iterdir()):
        (workdir / '.keep').write_text('', encoding='utf-8')
    for cmd in (['git', 'init', '-q'], ['git', 'config', 'user.email', 'bench@example.invalid'],
                ['git', 'config', 'user.name', 'bench'], ['git', 'config', 'core.autocrlf', 'false'],
                ['git', 'add', '-A'], ['git', 'commit', '-q', '--no-gpg-sign', '-m', 'seed']):
        result = sh(cmd, cwd=workdir)
        if result.returncode:
            raise RuntimeError(f'{cmd}: {result.stderr}')
    return sh(['git', 'rev-parse', 'HEAD'], cwd=workdir).stdout.strip()


# --------------------------------------------------------------------------- transcript parsing

def read_events(path: Path):
    with path.open(encoding='utf-8-sig', errors='replace') as stream:
        for line in stream:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


SKILL_PATH = re.compile(r'[/\\]([A-Za-z0-9._-]+)[/\\]SKILL\.md$')
SHOW_CALL = re.compile(r'\bbossku(?:\.cmd|\.exe)?\s+(?:--\S+\s+\S+\s+)*skills\s+show\s+([A-Za-z0-9._-]+)')


def tool_uses(events: list[dict]):
    for event in events:
        if event.get('type') == 'assistant' and event.get('parent_tool_use_id') is None:
            for block in (event.get('message') or {}).get('content') or []:
                if block.get('type') == 'tool_use':
                    yield block


def loaded_from_blocks(blocks) -> list[str]:
    """Skills the agent actually opened, in order: the Skill tool, a SKILL.md read, or `bossku skills show`."""
    loaded: list[str] = []
    for block in blocks:
        name, args = block.get('name'), block.get('input') or {}
        sid = None
        if name == 'Skill':
            sid = args.get('skill') or args.get('name')
        elif name == 'Read':
            found = SKILL_PATH.search(str(args.get('file_path', '')))
            sid = found.group(1) if found else None
        elif name in {'Bash', 'PowerShell'}:
            found = SHOW_CALL.search(str(args.get('command', '')))
            sid = found.group(1) if found else None
        if sid:
            sid = str(sid).split(':')[-1]   # plugin skills are namespaced plugin:skill
            if sid not in loaded:
                loaded.append(sid)
    return loaded


def skills_loaded(events: list[dict]) -> list[str]:
    return loaded_from_blocks(tool_uses(events))


BOSSKU_CALL = re.compile(r'(^|[\s;&|`(])bossku(\.cmd|\.exe)?(\s|$)|-m bossku')

EDIT_TOOLS = {'Write', 'Edit', 'MultiEdit', 'NotebookEdit'}
NOT_CODE = re.compile(r'\.(md|txt|rst|json|ya?ml|toml|ini|cfg|lock|csv)$', re.I)
# A command word, not a file name: "app.py" and "node_modules" must not count as running python or node.
RUNS_SOMETHING = re.compile(r'(?<![\w./-])(python3?|py|pytest|unittest|node|npm|npx|yarn|pnpm|deno|bun|tsc|go|cargo|make|mvn|gradle|dotnet|ruby|php|bash|sh)(?![\w.-])|(?<![\w.])\./\S+')


def checked_after_last_edit(sequence: list[tuple[str, dict]]) -> dict:
    """Did the agent run anything after its last code edit? Judged from the tool calls alone, the same for every arm."""
    last_edit = last_run = -1
    for index, (name, args) in enumerate(sequence):
        if name in EDIT_TOOLS and not NOT_CODE.search(str(args.get('file_path') or args.get('notebook_path') or '')):
            last_edit = index
        elif name in {'Bash', 'PowerShell'} and RUNS_SOMETHING.search(str(args.get('command', ''))):
            last_run = index
    return {'edited_code': last_edit >= 0, 'ran_after_last_edit': last_run > last_edit >= 0}


def parse_stream(path: Path) -> dict:
    init = result = None
    tools: Counter = Counter()
    skills: list[str] = []
    skill_reads: list[str] = []
    bash: list[str] = []
    message_usage: dict[str, dict] = {}
    final_text = ''
    assistant_events: list[dict] = []
    sequence: list[tuple[str, dict]] = []
    for event in read_events(path):
        kind = event.get('type')
        if kind == 'system' and event.get('subtype') == 'init':
            init = event
        elif kind == 'result':
            result = event
        elif kind == 'assistant':
            assistant_events.append(event)
            message = event.get('message') or {}
            if message.get('id'):
                message_usage[message['id']] = message.get('usage') or {}
            for block in message.get('content') or []:
                if block.get('type') == 'text' and event.get('parent_tool_use_id') is None:
                    final_text = block.get('text', final_text)
                if block.get('type') != 'tool_use':
                    continue
                name, args = block.get('name', '?'), block.get('input') or {}
                tools[name] += 1
                if event.get('parent_tool_use_id') is None:
                    sequence.append((name, args))
                if name == 'Skill':
                    skills.append(str(args.get('skill') or args.get('name') or '?'))
                elif name in {'Bash', 'PowerShell'}:   # on Windows the agent picks either shell
                    bash.append(str(args.get('command', '')))
                elif name == 'Read' and 'SKILL.md' in str(args.get('file_path', '')):
                    skill_reads.append(str(args.get('file_path')))
    usage = (result or {}).get('usage') or {}
    if not usage and message_usage:  # timed-out or crashed run: rebuild from per-message usage
        usage = {key: sum(u.get(key, 0) or 0 for u in message_usage.values())
                 for key in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')}
    model_usage = (result or {}).get('modelUsage') or {}
    return {
        'has_result': result is not None,
        'is_error': bool((result or {}).get('is_error')),
        'subtype': (result or {}).get('subtype'),
        'terminal_reason': (result or {}).get('terminal_reason'),
        'turns': (result or {}).get('num_turns'),
        'duration_ms': (result or {}).get('duration_ms'),
        'api_ms': (result or {}).get('duration_api_ms'),
        'cost_usd': (result or {}).get('total_cost_usd'),
        'denials': len((result or {}).get('permission_denials') or []),
        'tokens': {
            'input_uncached': usage.get('input_tokens', 0) or 0,
            'cache_write': usage.get('cache_creation_input_tokens', 0) or 0,
            'cache_read': usage.get('cache_read_input_tokens', 0) or 0,
            'output': usage.get('output_tokens', 0) or 0,
        },
        'models': sorted(model_usage),
        'context_window': next((v.get('contextWindow') for v in model_usage.values()), None),
        'claude_code_version': (init or {}).get('claude_code_version'),
        'init': {k: len((init or {}).get(k) or []) for k in
                 ('tools', 'skills', 'slash_commands', 'plugins', 'mcp_servers', 'agents')},
        'tool_calls': dict(tools),
        'skills_invoked': skills,
        'skill_files_read': skill_reads,
        'skills_loaded': skills_loaded(assistant_events),
        'bossku_calls': [c for c in bash if BOSSKU_CALL.search(c)],
        'bash_calls': len(bash),
        **checked_after_last_edit(sequence),
        'final_text': final_text[:4000],
    }


def total_input(tokens: dict) -> int:
    """Every input token the model processed across all turns, cached or not."""
    return tokens['input_uncached'] + tokens['cache_write'] + tokens['cache_read']


# --------------------------------------------------------------------------- grading

UNITTEST_TOTAL = re.compile(r'^Ran (\d+) tests? in ', re.M)
UNITTEST_FAIL = re.compile(r'FAILED \((.*?)\)')


def parse_unittest(output: str, returncode: int) -> dict:
    ran = UNITTEST_TOTAL.search(output)
    total = int(ran.group(1)) if ran else 0
    failed = 0
    fail = UNITTEST_FAIL.search(output)
    if fail:
        failed = sum(int(n) for n in re.findall(r'=(\d+)', fail.group(1)))
    passed = max(total - failed, 0)
    return {'passed': returncode == 0 and total > 0, 'tests_total': total, 'tests_passed': passed}


def diff_stats(workdir: Path, base: str = 'HEAD') -> dict:
    """What the agent changed, relative to the seed commit (agents that commit their work still count)."""
    sh(['git', 'add', '-A'], cwd=workdir)
    numstat = sh(['git', 'diff', '--cached', '--numstat', base], cwd=workdir).stdout
    files = added = removed = 0
    for row in numstat.splitlines():
        parts = row.split('\t')
        if len(parts) != 3 or SCAFFOLD_PARTS & set(Path(parts[2]).parts) or parts[2].endswith('.pyc'):
            continue
        files += 1
        added += int(parts[0]) if parts[0].isdigit() else 0
        removed += int(parts[1]) if parts[1].isdigit() else 0
    return {'files_changed': files, 'lines_added': added, 'lines_removed': removed}


def grade(task_dir: Path, task: dict, workdir: Path) -> dict:
    hidden = task_dir / 'hidden'
    if hidden.is_dir():
        shutil.copytree(hidden, workdir, dirs_exist_ok=True)
    grader = task['grader']
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'}
    try:
        out = sh(grader['cmd'], cwd=workdir, timeout=grader.get('timeout', 120), env=env)
        return parse_unittest(out.stdout + '\n' + out.stderr, out.returncode)
    except subprocess.TimeoutExpired:
        return {'passed': False, 'tests_total': 0, 'tests_passed': 0, 'grader_timeout': True}


# --------------------------------------------------------------------------- running

HUMANEVAL_DATA = REPO / 'benchmarks' / 'datasets' / 'HumanEval.jsonl.gz'
HUMANEVAL_PROMPT = (
    'Implement the function `{entry}` in `solution.py`, following its docstring. The file already has the '
    'signature and docstring with a placeholder body. Keep the function name and signature; helper functions are fine.'
)
HUMANEVAL_TEST = """import unittest

from solution import *  # noqa: F401,F403  (helpers defined in the prompt are used by some checks)
import solution

{test}


class HumanEvalHidden(unittest.TestCase):
    def test_{entry}(self):
        check(solution.{entry})


if __name__ == "__main__":
    unittest.main()
"""


def materialize_humaneval(dest: Path, count: int, seed: int = 20261001) -> Path:
    """Turn the public HumanEval problems into benchmark tasks: a stub to complete, hidden `check` tests."""
    rows = [json.loads(line) for line in gzip.decompress(HUMANEVAL_DATA.read_bytes()).decode('utf-8').splitlines()
            if line.strip()]
    chosen = random.Random(seed).sample(rows, count) if count < len(rows) else rows
    chosen.sort(key=lambda row: int(row['task_id'].split('/')[1]))
    if dest.exists():
        rmtree_force(dest)
    for row in chosen:
        task_id = f"he-{int(row['task_id'].split('/')[1]):03d}"
        base, entry = dest / task_id, row['entry_point']
        for sub in ('seed', 'hidden', 'reference'):
            (base / sub).mkdir(parents=True)
        (base / 'seed' / 'solution.py').write_text(row['prompt'].rstrip() + '\n    pass\n', encoding='utf-8')
        (base / 'reference' / 'solution.py').write_text(row['prompt'] + row['canonical_solution'], encoding='utf-8')
        (base / 'hidden' / 'test_humaneval_hidden.py').write_text(
            HUMANEVAL_TEST.format(test=row['test'].strip('\n'), entry=entry), encoding='utf-8')
        (base / 'task.json').write_text(json.dumps({
            'id': task_id, 'category': 'humaneval', 'prompt': HUMANEVAL_PROMPT.format(entry=entry),
            'source': row['task_id'],
            'grader': {'cmd': ['python', '-m', 'unittest', '-v', 'test_humaneval_hidden'], 'timeout': 120},
        }, indent=2), encoding='utf-8')
    return dest


def resolve_suite(spec: str, work: Path) -> Path:
    """A suite is a directory of tasks, or `humaneval[:N]` for a seeded sample of the public HumanEval set."""
    if spec.startswith('humaneval'):
        _, _, count = spec.partition(':')
        return materialize_humaneval(work / 'suites' / f'humaneval-{count or "all"}', int(count) if count else 164)
    return Path(spec)


def load_suite(suite: Path, only: set[str] | None = None) -> list[tuple[Path, dict]]:
    tasks = []
    for task_json in sorted(suite.glob('*/task.json')):
        task = json.loads(task_json.read_text(encoding='utf-8'))
        if only is None or task['id'] in only:
            tasks.append((task_json.parent, task))
    if not tasks:
        raise SystemExit(f'no tasks found in {suite}')
    return tasks


def agent_command(claude: str, model: str, args, instructions: Path | None) -> list[str]:
    cmd = [claude, '-p', '--model', model, '--output-format', 'stream-json', '--verbose',
           '--setting-sources', 'project', '--permission-mode', 'bypassPermissions',
           '--strict-mcp-config', '--exclude-dynamic-system-prompt-sections', '--include-hook-events',
           '--disallowedTools', 'WebFetch', 'WebSearch']
    # A dollar cap protects your own Claude account. Claude Code prices other models with a made-up rate, so a cap
    # there ends runs at an arbitrary token count and punishes whichever version uses more tokens: no cap by default.
    budget = args.budget if args.budget is not None else (1.0 if args.provider == 'anthropic' else None)
    if budget is not None:
        cmd += ['--max-budget-usd', str(budget)]
    effort = args.effort
    # Sessions are kept for every provider: the stop gate reads the session transcript, and with
    # --no-session-persistence the file does not exist, so the gate would silently do nothing for Claude models.
    # Runs on your own login write them under your real ~/.claude/projects; _execute deletes those folders afterwards.
    if instructions is not None:
        cmd += ['--append-system-prompt-file', str(instructions)]
    if effort:
        cmd += ['--effort', effort]
    return cmd


def claude_session_dir(workdir: Path) -> Path:
    """Where Claude Code keeps the sessions it ran in `workdir`: every non-alphanumeric character becomes '-'."""
    config = Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude')
    return config / 'projects' / re.sub(r'[^A-Za-z0-9]', '-', str(workdir.resolve()))


def invoke(cmd: list[str], prompt: str, workdir: Path, env: dict, transcript: Path, timeout: int,
           stop_when=None) -> tuple[bool, bool, float]:
    """Run the agent, saving its event stream. `stop_when(events)` may end the run early (routing probes)."""
    started = time.monotonic()
    timed_out = stopped = False
    proc = subprocess.Popen(cmd, cwd=workdir, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    lines: queue.Queue = queue.Queue()

    def pump() -> None:
        for raw in iter(proc.stdout.readline, b''):
            lines.put(raw)
        lines.put(None)

    threading.Thread(target=pump, daemon=True).start()
    try:
        proc.stdin.write(prompt.encode('utf-8'))
        proc.stdin.close()
    except OSError:
        pass
    events: list[dict] = []
    with transcript.open('wb') as stream:
        while True:
            remaining = timeout - (time.monotonic() - started)
            if remaining <= 0:
                timed_out = True
                break
            try:
                raw = lines.get(timeout=min(remaining, 1.0))
            except queue.Empty:
                continue
            if raw is None:
                break
            stream.write(raw)
            if stop_when is not None:
                try:
                    events.append(json.loads(raw.decode('utf-8-sig')))
                except ValueError:
                    continue
                if stop_when(events):
                    stopped = True
                    break
    if timed_out or stopped:
        kill_tree(proc.pid)
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        kill_tree(proc.pid)
    return timed_out, stopped, time.monotonic() - started


def is_infrastructure_failure(parsed: dict) -> bool:
    """The model service, not the model, ended the run: no answer at all, no model work done, or an API error part-way.

    A rate limit (HTTP 429) that cuts a run short leaves partial work that fails the hidden tests; counting that as a
    failed task would blame the setup for a limit on the account.
    """
    return (not parsed['has_result'] or parsed.get('terminal_reason') == 'api_error'
            or (parsed['is_error'] and parsed['subtype'] != 'error_max_budget_usd' and parsed['tokens']['output'] == 0))


def excluded(row: dict) -> bool:
    return bool(row.get('infrastructure_failure') or row.get('harness_error'))


def vault_projects() -> set[str]:
    """Project folders in the real Obsidian vault: the first place a stray `bossku remember` would leave a mark."""
    try:
        vault = json.loads((Path.home() / '.bosskuai' / 'config.json').read_text(encoding='utf-8')).get('obsidian_vault')
        base = Path(vault) / 'BosskuAI'
        return {p.name for p in base.iterdir() if p.is_dir()} if base.is_dir() else set()
    except (OSError, ValueError, TypeError):
        return set()


class Runner:
    def __init__(self, args, claude: str, work: Path, out: Path):
        self.args, self.claude, self.work, self.out = args, claude, work, out
        self.lock = threading.Lock()
        self.abort = threading.Event()
        self.consecutive_infra = 0
        self.digests: set[str] = set()   # names of this run's throwaway projects; none may appear in the real vault
        self.vault_before = vault_projects()   # folders that already existed are not ours
        (out / 'transcripts').mkdir(parents=True, exist_ok=True)

    def append(self, row: dict) -> None:
        with self.lock, (self.out / 'runs.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')

    def one(self, arm: Arm, prep: Prepared, task_dir: Path | None, task: dict | None,
            trial: int, model: str, prompt: str, kind: str, stop_when=None, label: str | None = None,
            extra: dict | None = None) -> dict | None:
        if self.abort.is_set():
            return None
        task_id = label or (task['id'] if task else 'overhead')
        run_id = f'{kind}.{arm.name}.{model}.{task_id}.t{trial}'.replace('/', '_')
        base = {'run_id': run_id, 'kind': kind, 'arm': arm.name, 'profile': arm.profile if arm.root else None,
                'model': model, 'task': task_id, 'category': (task or {}).get('category'), 'trial': trial}
        try:
            row = {**base, **(extra or {}), **self._execute(arm, prep, task_dir, task, model, prompt, run_id, stop_when)}
        except Exception as exc:  # noqa: BLE001 - recorded and reported, never silently dropped
            row = {**base, 'harness_error': f'{type(exc).__name__}: {exc}'[:500], 'tokens': {
                'input_uncached': 0, 'cache_write': 0, 'cache_read': 0, 'output': 0}}
        row['timestamp'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
        leaked = sorted((self.digests & vault_projects()) - self.vault_before)
        if leaked:   # attributable to us: stop before more notes land in the user's vault
            row['real_vault_touched'] = leaked
            self.abort.set()
            print(f'[POLLUTION] benchmark project(s) {leaked} appeared in the real Obsidian vault; stopping', flush=True)
        self.append(row)
        if row.get('harness_error'):
            print(f'[HARNESS-ERROR] {run_id}: {row["harness_error"]}', flush=True)
            return row
        verdict = 'PASS' if row.get('passed') else ('INFRA' if row['infrastructure_failure'] else 'FAIL')
        verdict = 'OK' if row['kind'] != 'task' and verdict == 'FAIL' else verdict
        print(f'[{verdict}] {run_id} turns={row.get("turns")} cost=${row.get("cost_usd") or 0:.3f} '
              f'in={total_input(row["tokens"])} out={row["tokens"]["output"]} wall={row["wall_s"]}s', flush=True)
        return row

    def _run_setup_sessions(self, cmd: list[str], task: dict | None, workdir: Path, env: dict, transcript: Path) -> dict:
        """Earlier sessions of a memory task: the same project and home, a fresh conversation each time.

        What the agent learns in them can reach the graded session only through what it saved (BosskuAI notes) or
        left in the files. Their usage is reported apart from the graded session's.
        """
        prompts = list((task or {}).get('setup') or [])
        if not prompts:
            return {}
        tokens = {'input_uncached': 0, 'cache_write': 0, 'cache_read': 0, 'output': 0}
        turns, saved = [], 0
        for index, text in enumerate(prompts, 1):
            side = transcript.with_name(f'{transcript.stem}.setup{index}.jsonl')
            invoke(cmd, text + NON_INTERACTIVE, workdir, env, side, self.args.timeout)
            parsed = parse_stream(side)
            for key in tokens:
                tokens[key] += parsed['tokens'][key]
            turns.append(parsed['turns'])
            saved += sum('remember' in call for call in parsed['bossku_calls'])
            if self.args.keep_transcripts:
                safe = re.sub(r'[^A-Za-z0-9._-]', '_', f'{transcript.stem}.setup{index}')
                with side.open('rb') as src, gzip.open(self.out / 'transcripts' / f'{safe}.jsonl.gz', 'wb') as dst:
                    shutil.copyfileobj(src, dst)
        return {'sessions': len(prompts), 'tokens': tokens, 'turns': turns, 'remember_calls': saved}

    def _execute(self, arm: Arm, prep: Prepared, task_dir: Path | None, task: dict | None,
                 model: str, prompt: str, run_id: str, stop_when=None) -> dict:
        digest = hashlib.sha1(run_id.encode()).hexdigest()[:10]   # short paths: Windows MAX_PATH is real
        self.digests.add(digest)
        workdir = self.work / 'r' / digest
        transcript = self.work / 't' / f'{digest}.jsonl'
        transcript.parent.mkdir(parents=True, exist_ok=True)
        config_dir = self.work / 'cfg' / digest
        cmd = agent_command(self.claude, model, self.args, prep.instructions)
        for attempt in range(self.args.retries + 1):
            seed_commit = prepare_workdir(arm, prep.template, (task_dir / 'seed') if task_dir else None, workdir)
            if config_dir.exists():
                rmtree_force(config_dir)
            config_dir.mkdir(parents=True, exist_ok=True)
            env = child_env(prep.shim, provider_env(self.args, model, config_dir), prep.home)
            setup = self._run_setup_sessions(cmd, task, workdir, env, transcript)
            timed_out, stopped, wall = invoke(cmd, prompt, workdir, env, transcript, self.args.timeout, stop_when)
            parsed = parse_stream(transcript)
            infra = is_infrastructure_failure(parsed) and not (timed_out or stopped)
            if infra and attempt < self.args.retries:
                time.sleep(20 * (attempt + 1))
                continue
            break
        with self.lock:
            self.consecutive_infra = self.consecutive_infra + 1 if infra else 0
            if self.consecutive_infra >= self.args.abort_after:
                self.abort.set()
        stats = diff_stats(workdir, seed_commit) if task else {}
        grading = grade(task_dir, task, workdir) if task else {}
        if self.args.keep_transcripts and transcript.exists():
            safe_name = re.sub(r'[^A-Za-z0-9._-]', '_', run_id)   # a ':' in a model id would become an NTFS stream
            with transcript.open('rb') as src, gzip.open(self.out / 'transcripts' / f'{safe_name}.jsonl.gz', 'wb') as dst:
                shutil.copyfileobj(src, dst)
        if self.args.provider == 'anthropic':   # the sessions of this throwaway folder, left in your real ~/.claude
            sessions = claude_session_dir(workdir)
            if sessions.is_dir() and sessions.name.endswith(re.sub(r'[^A-Za-z0-9]', '-', str(Path('r') / digest))):
                rmtree_force(sessions)
        if not self.args.keep_workdirs:
            rmtree_force(workdir)
        rmtree_force(config_dir)
        row = {'wall_s': round(wall, 1), 'timed_out': timed_out, 'stopped_early': stopped, 'infrastructure_failure': infra,
               'attempts': attempt + 1, 'provider': self.args.provider, **grading, **stats, **parsed}
        if setup:
            row['setup'] = setup
        if self.args.provider != 'anthropic':   # Claude Code prices unknown models with a fallback table
            row['cost_usd_reported_unreliable'] = row.pop('cost_usd')
            row['cost_usd'] = None
        return row


def done_ids(out: Path) -> set[str]:
    path = out / 'runs.jsonl'
    if not path.exists():
        return set()
    ids = set()
    for line in path.read_text(encoding='utf-8').splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not excluded(row):
            ids.add(row['run_id'])
    return ids


LEAK_PROMPT = (
    'Without using any tools: quote word for word every instruction in your context that came from a memory file or '
    'a project instructions file (CLAUDE.md, AGENTS.md or similar). If there are none, reply with the single word NONE.'
)


def isolation_check(runner: 'Runner', arms: list[Arm], prepared: dict[str, Prepared], model: str) -> None:
    """Canary: the baseline must start with no BosskuAI text in its context, or every comparison is void."""
    for arm in arms:
        if arm.root is not None:
            continue
        row = runner.one(arm, prepared[arm.name], None, None, 0, model, LEAK_PROMPT, 'selftest')
        text = (row or {}).get('final_text', '')
        says_none = re.fullmatch(r'\W*NONE\W*', text.strip(), re.I) is not None
        if not says_none and re.search(r'bossku|memory-path|Contents of', text, re.I):
            raise SystemExit('ISOLATION FAILED: the baseline sees instruction text it should not:\n' + text[:600])
        print(f'isolation ok: baseline context is clean ({model})', flush=True)


def cmd_run(args) -> int:
    claude = find_claude(args.claude)
    arms = [parse_arm(spec) for spec in args.arm]
    out, work = Path(args.out).resolve(), Path(args.work).resolve()
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    tasks = load_suite(resolve_suite(args.suite, work), set(args.tasks.split(',')) if args.tasks else None)
    prepared = prepare_arms(arms, work)
    runner = Runner(args, claude, work, out)
    if not args.dry_run:
        for model in args.model:
            isolation_check(runner, arms, prepared, model)
    finished = done_ids(out)
    jobs = []
    for model in args.model:
        for task_dir, task in tasks:
            for trial in range(1, args.trials + 1):
                for arm in arms:
                    run_id = f'task.{arm.name}.{model}.{task["id"]}.t{trial}'
                    if run_id not in finished:
                        jobs.append((arm, prepared[arm.name], task_dir, task, trial, model, task['prompt'] + NON_INTERACTIVE))
    random.Random(args.seed).shuffle(jobs)
    print(f'{len(jobs)} runs to do ({len(finished)} already finished), parallel={args.parallel}', flush=True)
    if args.dry_run:
        return 0
    if jobs and not args.no_warmup:
        # One throwaway call per arm and model so the prompt cache is warm; otherwise whichever arm
        # happens to run first pays for cache writes and looks more expensive than it is.
        for model in args.model:
            for arm in arms:
                runner.one(arm, prepared[arm.name], None, None, 0, model, OVERHEAD_PROMPT, 'warmup')
    with cf.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = [pool.submit(runner.one, arm, prep, task_dir, task, trial, model, prompt, 'task')
                   for arm, prep, task_dir, task, trial, model, prompt in jobs]
        for future in futures:
            future.result()
    if runner.abort.is_set():
        print('ABORTED: stopped early (repeated infrastructure failures such as rate limits, or a vault write). '
              'Fix the cause, then rerun the same command to resume.', flush=True)
        return 3
    return 0


def routing_split(prompt_id: str) -> str:
    return 'dev' if int(hashlib.sha1(prompt_id.encode()).hexdigest()[:8], 16) % 2 == 0 else 'test'


def routing_stop(events: list[dict]) -> bool:
    """End a routing probe once the agent has had its say about skills: three steps after it first opens one,
    ten steps in total, or the end of the run."""
    if any(event.get('type') == 'result' for event in events):
        return True
    calls = list(tool_uses(events))
    if len(calls) >= 10:
        return True
    for index in range(1, len(calls) + 1):
        if loaded_from_blocks(calls[:index]):
            return len(calls) - index >= 3
    return False


def cmd_routing(args) -> int:
    """Live skill selection: does the agent open an acceptable skill for a held-out user request?"""
    claude = find_claude(args.claude)
    arms = [parse_arm(spec) for spec in args.arm]
    out, work = Path(args.out).resolve(), Path(args.work).resolve()
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    prompts = [row for row in json.loads(Path(args.prompts).read_text(encoding='utf-8'))
               if args.split == 'all' or routing_split(row['id']) == args.split]
    if args.limit:
        prompts = random.Random(args.seed).sample(prompts, min(args.limit, len(prompts)))
    prepared = prepare_arms(arms, work)
    runner = Runner(args, claude, work, out)
    if not args.dry_run:
        for model in args.model:
            isolation_check(runner, arms, prepared, model)
    finished = done_ids(out)
    jobs = [(arm, prepared[arm.name], model, row) for model in args.model for row in prompts for arm in arms
            if f'routing.{arm.name}.{model}.{row["id"]}.t1' not in finished]
    random.Random(args.seed).shuffle(jobs)
    print(f'{len(jobs)} probes to do, parallel={args.parallel}', flush=True)
    if args.dry_run:
        return 0
    if jobs and not args.no_warmup:
        for model in args.model:
            for arm in arms:
                runner.one(arm, prepared[arm.name], None, None, 0, model, OVERHEAD_PROMPT, 'warmup')
    with cf.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = [pool.submit(runner.one, arm, prep, None, None, 1, model, row['prompt'] + NON_INTERACTIVE, 'routing',
                               routing_stop, row['id'],
                               {'prompt_id': row['id'], 'domain': row.get('domain'), 'concerns': row['concerns'],
                                'split': routing_split(row['id'])})
                   for arm, prep, model, row in jobs]
        for future in futures:
            future.result()
    return 3 if runner.abort.is_set() else 0


def routing_summary(paths: list[str]) -> dict:
    rows = load_runs(paths, 'routing')
    result: dict = {}
    for model in sorted({r['model'] for r in rows}):
        for arm in sorted({r['arm'] for r in rows if r['model'] == model}):
            group = [r for r in rows if r['model'] == model and r['arm'] == arm]
            n = len(group)
            union = lambda r: set().union(*[set(c) for c in r['concerns']])  # noqa: E731
            any_ok = sum(bool(set(r['skills_loaded']) & union(r)) for r in group)
            first_ok = sum(bool(r['skills_loaded']) and r['skills_loaded'][0] in union(r) for r in group)
            none = sum(not r['skills_loaded'] for r in group)
            coverage = statistics.mean(
                sum(bool(set(r['skills_loaded']) & set(c)) for c in r['concerns']) / len(r['concerns']) for r in group)
            lo, hi = wilson(any_ok, n)
            result.setdefault(model, {})[arm] = {
                'prompts': n, 'acceptable_skill_loaded': any_ok, 'rate': any_ok / n, 'ci': [lo, hi],
                'first_skill_acceptable': first_ok, 'no_skill_loaded': none, 'concern_coverage': coverage,
                'skills_loaded_mean': statistics.mean(len(r['skills_loaded']) for r in group),
                'input_tokens_mean': statistics.mean(total_input(r['tokens']) for r in group),
            }
    return result


def cmd_routing_report(args) -> int:
    result = routing_summary(args.runs)
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2), encoding='utf-8')
    for model, arms in result.items():
        print(f'\n== {model}')
        print(f'{"arm":<12}{"prompts":>8}{"acceptable":>12}{"first ok":>10}{"no skill":>10}{"concerns":>10}{"skills":>8}{"in tok":>10}')
        for arm, s in arms.items():
            print(f'{arm:<12}{s["prompts"]:>8}{100 * s["rate"]:>11.0f}%{s["first_skill_acceptable"]:>10}{s["no_skill_loaded"]:>10}'
                  f'{100 * s["concern_coverage"]:>9.0f}%{s["skills_loaded_mean"]:>8.1f}{s["input_tokens_mean"]:>10.0f}')
    return 0


def cmd_overhead(args) -> int:
    """Fixed cost of a session: the same one-word prompt in every arm, repeated, after a warm-up."""
    claude = find_claude(args.claude)
    arms = [parse_arm(spec) for spec in args.arm]
    out, work = Path(args.out).resolve(), Path(args.work).resolve()
    out.mkdir(parents=True, exist_ok=True)
    prepared = prepare_arms(arms, work)
    runner = Runner(args, claude, work, out)
    for model in args.model:
        for arm in arms:
            for trial in range(0, args.trials + 1):  # trial 0 is the cache warm-up, excluded in the report
                runner.one(arm, prepared[arm.name], None, None, trial, model, OVERHEAD_PROMPT, 'overhead')
    return 0


def cmd_validate(args) -> int:
    """Each task must be fair: hidden tests fail on the seed and pass on the reference solution."""
    bad = 0
    suite = resolve_suite(args.suite, Path(args.work).resolve())
    for task_dir, task in load_suite(suite, set(args.tasks.split(',')) if args.tasks else None):
        tmp = Path(args.work).resolve() / 'validate' / task['id']
        if tmp.exists():
            rmtree_force(tmp)
        tmp.mkdir(parents=True)
        shutil.copytree(task_dir / 'seed', tmp, dirs_exist_ok=True)
        before = grade(task_dir, task, tmp)
        shutil.copytree(task_dir / 'reference', tmp, dirs_exist_ok=True)
        after = grade(task_dir, task, tmp)
        ok = (not before['passed']) and after['passed']
        bad += not ok
        print(f'{"ok " if ok else "BAD"} {task["id"]}: seed passes={before["passed"]} '
              f'({before["tests_passed"]}/{before["tests_total"]}), reference passes={after["passed"]} '
              f'({after["tests_passed"]}/{after["tests_total"]})')
    return 1 if bad else 0


# --------------------------------------------------------------------------- statistics

def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def bootstrap_ci(values: list[float], stat=statistics.mean, reps: int = 4000, seed: int = 7) -> tuple[float, float]:
    if len(values) < 2:
        return (float('nan'), float('nan'))
    rng = random.Random(seed)
    draws = sorted(stat([rng.choice(values) for _ in values]) for _ in range(reps))
    return (draws[int(0.025 * reps)], draws[int(0.975 * reps) - 1])


def load_runs(paths: list[str], kind: str) -> list[dict]:
    rows = []
    for path in paths:
        for line in Path(path).read_text(encoding='utf-8').splitlines():
            if line.strip():
                row = json.loads(line)
                if row.get('kind') == kind and not excluded(row):
                    rows.append(row)
    return rows


def count_excluded(paths: list[str]) -> dict[str, int]:
    counts: Counter = Counter()
    for path in paths:
        for line in Path(path).read_text(encoding='utf-8').splitlines():
            if line.strip():
                row = json.loads(line)
                if row.get('kind') == 'task' and excluded(row):
                    counts[f"{row['arm']}: {'harness error' if row.get('harness_error') else 'infrastructure failure'}"] += 1
    return dict(counts)


def summarize_arm(rows: list[dict]) -> dict:
    n = len(rows)
    passed = sum(bool(r.get('passed')) for r in rows)
    lo, hi = wilson(passed, n)
    costs = [r['cost_usd'] for r in rows if r.get('cost_usd') is not None]
    mean = lambda values: statistics.mean(values) if values else 0.0  # noqa: E731
    edited = [r for r in rows if r.get('edited_code')]
    unchecked = sum(not r.get('ran_after_last_edit') for r in edited)
    earlier = [r for r in rows if r.get('setup')]   # memory tasks: an earlier session came first
    return {
        'runs': n, 'passed': passed, 'pass_rate': passed / n if n else 0.0, 'pass_ci': [lo, hi],
        'saved_a_note_rate': (sum(r['setup']['remember_calls'] > 0 for r in earlier) / len(earlier)) if earlier else None,
        'edited_runs': len(edited), 'unchecked_finishes': unchecked,
        'unchecked_rate': unchecked / len(edited) if edited else None,
        'cost_mean': mean(costs) if costs else None, 'cost_total': sum(costs) if costs else None,
        'cost_per_solved': sum(costs) / passed if costs and passed else None,
        'input_tokens_mean': mean([total_input(r['tokens']) for r in rows]),
        'output_tokens_mean': mean([r['tokens']['output'] for r in rows]),
        'cache_read_mean': mean([r['tokens']['cache_read'] for r in rows]),
        'cache_write_mean': mean([r['tokens']['cache_write'] for r in rows]),
        'turns_mean': mean([(r['turns'] or 0) for r in rows]),
        'wall_s_mean': mean([r['wall_s'] for r in rows]),
        'skills_loaded_per_run': mean([len(r['skills_invoked']) + len(r['skill_files_read']) for r in rows]),
        'bossku_calls_per_run': mean([len(r['bossku_calls']) for r in rows]),
        'shell_calls_mean': mean([(r.get('bash_calls') or 0) for r in rows]),
        'lines_changed_mean': mean([(r.get('lines_added', 0) + r.get('lines_removed', 0)) for r in rows]),
        'timeouts': sum(bool(r['timed_out']) for r in rows),
        'budget_stops': sum(r.get('subtype') == 'error_max_budget_usd' for r in rows),
    }


def paired(rows: list[dict], arm: str, base: str, metric) -> dict:
    """Per-task mean difference (arm - base) over tasks that both arms ran, with a bootstrap interval."""
    by: dict[tuple, dict[str, list[float]]] = {}
    for r in rows:
        by.setdefault((r['model'], r['task']), {}).setdefault(r['arm'], []).append(metric(r))
    diffs, ratios = [], []
    for cell in by.values():
        if arm in cell and base in cell:
            a, b = statistics.mean(cell[arm]), statistics.mean(cell[base])
            diffs.append(a - b)
            if b:
                ratios.append(a / b)
    if not diffs:
        return {'tasks': 0}
    lo, hi = bootstrap_ci(diffs)
    return {'tasks': len(diffs), 'mean_diff': statistics.mean(diffs), 'ci': [lo, hi],
            'mean_ratio': statistics.mean(ratios) if ratios else float('nan')}


def build_report(rows: list[dict], baseline: str) -> dict:
    report: dict = {'models': {}}
    for model in sorted({r['model'] for r in rows}):
        mrows = [r for r in rows if r['model'] == model]
        arms = sorted({r['arm'] for r in mrows}, key=lambda a: (a != baseline, a))
        block: dict = {'arms': {a: summarize_arm([r for r in mrows if r['arm'] == a]) for a in arms}, 'paired': {},
                       'by_category': {}}
        for a in arms:
            if a != baseline and baseline in arms:
                block['paired'][a] = {
                    'cost': (paired(mrows, a, baseline, lambda r: r['cost_usd'])
                             if all(r.get('cost_usd') is not None for r in mrows) else {'tasks': 0}),
                    'input_tokens': paired(mrows, a, baseline, lambda r: total_input(r['tokens'])),
                    'output_tokens': paired(mrows, a, baseline, lambda r: r['tokens']['output']),
                    'turns': paired(mrows, a, baseline, lambda r: r['turns'] or 0),
                    'passed': paired(mrows, a, baseline, lambda r: 1.0 if r.get('passed') else 0.0),
                }
        for category in sorted({r['category'] for r in mrows if r.get('category')}):
            block['by_category'][category] = {
                a: summarize_arm([r for r in mrows if r['arm'] == a and r.get('category') == category]) for a in arms}
        report['models'][model] = block
    return report


def coding_report(paths: list[str], baseline: str = 'baseline') -> dict:
    report = build_report(load_runs(paths, 'task'), baseline)
    report['excluded_runs'] = count_excluded(paths)
    return report


def cmd_report(args) -> int:
    report = coding_report(args.runs, args.baseline)
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2), encoding='utf-8')
    for model, block in report['models'].items():
        print(f'\n== {model}')
        print(f'{"arm":<14}{"runs":>5}{"pass":>6}{"pass% (95% CI)":>20}{"$/run":>9}{"$/solved":>10}'
              f'{"in tok":>10}{"out tok":>9}{"turns":>7}{"skills":>7}{"wall s":>8}')
        for arm, s in block['arms'].items():
            ci = f'{100 * s["pass_rate"]:.0f}% ({100 * s["pass_ci"][0]:.0f}-{100 * s["pass_ci"][1]:.0f})'
            money = lambda v: f'{v:>9.3f}' if v is not None else f'{"n/a":>9}'  # noqa: E731
            print(f'{arm:<14}{s["runs"]:>5}{s["passed"]:>6}{ci:>20}{money(s["cost_mean"])}{money(s["cost_per_solved"]):>10}'
                  f'{s["input_tokens_mean"]:>10.0f}{s["output_tokens_mean"]:>9.0f}{s["turns_mean"]:>7.1f}'
                  f'{s["skills_loaded_per_run"]:>7.1f}{s["wall_s_mean"]:>8.0f}')
        for arm, metrics in block['paired'].items():
            print(f'  paired {arm} - {args.baseline}: ' + '; '.join(
                f'{name} {m["mean_diff"]:+.3f} [{m["ci"][0]:+.3f},{m["ci"][1]:+.3f}] (n={m["tasks"]})'
                for name, m in metrics.items() if m.get('tasks')))
    if report['excluded_runs']:
        print(f'\nexcluded runs: {report["excluded_runs"]}')
    capped = {f'{model}/{arm}': s['budget_stops'] for model, block in report['models'].items()
              for arm, s in block['arms'].items() if s['budget_stops']}
    if capped:
        print(f'\nWARNING: these runs were ended by the dollar cap, so they were cut short and count as failures: {capped}')
    return 0


def overhead_summary(paths: list[str]) -> dict:
    rows = [r for r in load_runs(paths, 'overhead') if r['trial'] > 0]
    table: dict[tuple, list[dict]] = {}
    for r in rows:
        table.setdefault((r['model'], r['arm']), []).append(r)
    result: dict = {}
    for (model, arm), group in sorted(table.items()):
        tokens = [total_input(r['tokens']) for r in group]
        cost = [r['cost_usd'] for r in group if r.get('cost_usd') is not None]
        result.setdefault(model, {})[arm] = {
            'runs': len(group), 'input_tokens_median': statistics.median(tokens),
            'cost_median': statistics.median(cost) if cost else None,
            'skills_listed': group[0]['init']['skills'], 'tools': group[0]['init']['tools'],
            'context_window': group[0]['context_window'],
        }
    return result


def cmd_overhead_report(args) -> int:
    result = overhead_summary(args.runs)
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2), encoding='utf-8')
    for model, arms in result.items():
        print(f'\n== {model}')
        for arm, s in arms.items():
            cost = f'${s["cost_median"]:.4f}' if s['cost_median'] is not None else 'n/a'
            print(f'{arm:<14} input tokens (median of {s["runs"]}): {s["input_tokens_median"]:>8.0f}   '
                  f'cost {cost}   skills in init: {s["skills_listed"]}   window: {s["context_window"]}')
    return 0


QUOTES_AND_SPACE = '\\s"\''
HOME_PATHS = (re.compile('[A-Za-z]:[\\\\/]+Users[\\\\/]+[^\\\\/' + QUOTES_AND_SPACE + ']+'),   # C:\Users\name, C:/Users/name
              re.compile('(?<![\\w.])/(?:[a-z]|home|Users)/(?:Users/)?[^/' + QUOTES_AND_SPACE + ']+'))   # /c/Users/name, /home/name
VAULT_FOLDER = re.compile('(<home>[\\\\/]+OneDrive[\\\\/]+Documents[\\\\/]+)[^\\\\/' + QUOTES_AND_SPACE + ']+')


def scrub(text: str) -> str:
    """Take the author's account name and folder names out of free text before it is committed."""
    for pattern in HOME_PATHS:
        text = pattern.sub('<home>', text)
    text = VAULT_FOLDER.sub(lambda match: match.group(1) + '<folder>', text)
    name = Path.home().name
    return re.sub('(?<![\\w-])' + re.escape(name) + '(?![\\w-])', '<user>', text) if len(name) >= 3 else text


def cmd_compact(args) -> int:
    """Copy run rows into a file small enough to commit: same numbers, shorter free text, no account or folder names."""
    kept = 0
    seen: set[str] = set()   # two processes started on the same folder can write the same run twice: keep the first
    with Path(args.out).open('w', encoding='utf-8', newline='\n') as out:
        for path in args.runs:
            for line in Path(path).read_text(encoding='utf-8').splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if not excluded(row):
                    if row.get('run_id') in seen:
                        continue
                    seen.add(row.get('run_id'))
                if args.kind and row.get('kind') not in args.kind:
                    continue
                if args.arm and row.get('arm') not in args.arm:
                    continue
                row['final_text'] = (row.get('final_text') or '')[:240]
                row['bossku_calls'] = [call[:120] for call in row.get('bossku_calls', [])]
                out.write(scrub(json.dumps(row, ensure_ascii=False, sort_keys=True)) + '\n')   # every field, not just the free text
                kept += 1
    print(f'wrote {kept} rows to {args.out}')
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    default_work = str(Path(os.environ.get('TEMP', '/tmp')) / 'bb')

    def common(p):
        p.add_argument('--claude', help='path to the claude CLI (default: PATH, then the desktop app copy)')
        p.add_argument('--arm', action='append', default=[], help='baseline | NAME=BOSSKU_ROOT[@lean|core|full][+hint][+gate][+brief] (repeatable)')
        p.add_argument('--model', action='append', default=[], help='model id (repeatable)')
        p.add_argument('--provider', choices=['anthropic', 'ollama'], default='anthropic',
                       help='anthropic = your own Claude login; ollama = Ollama Cloud via its Anthropic-compatible API')
        p.add_argument('--ollama-key-file', help='file holding the Ollama API key (never printed, never saved)')
        p.add_argument('--out', default=str(REPO / 'benchmarks' / 'results' / 'latest'))
        p.add_argument('--work', default=default_work, help='keep this path short; Windows MAX_PATH applies')
        p.add_argument('--timeout', type=int, default=900, help='seconds per agent run')
        p.add_argument('--budget', type=float, default=None,
                       help='hard USD cap per run (default: $1 for Claude models, none for Ollama, whose cost figure is not real)')
        p.add_argument('--effort', default=None)
        p.add_argument('--retries', type=int, default=2, help='retries for infrastructure failures only')
        p.add_argument('--abort-after', type=int, default=4, help='stop after this many consecutive infrastructure failures')
        p.add_argument('--keep-transcripts', action='store_true')
        p.add_argument('--keep-workdirs', action='store_true')
        p.add_argument('--trials', type=int, default=1)

    p_run = sub.add_parser('run', help='run the coding tasks')
    common(p_run)
    p_run.add_argument('--suite', required=True)
    p_run.add_argument('--tasks', help='comma-separated task ids')
    p_run.add_argument('--parallel', type=int, default=3)
    p_run.add_argument('--seed', type=int, default=20261001)
    p_run.add_argument('--dry-run', action='store_true')
    p_run.add_argument('--no-warmup', action='store_true', help='skip the per-arm cache warm-up call')
    p_run.set_defaults(func=cmd_run)

    p_over = sub.add_parser('overhead', help='measure the fixed per-session context cost')
    common(p_over)
    p_over.set_defaults(func=cmd_overhead)

    p_route = sub.add_parser('routing', help='live skill selection on held-out prompts')
    common(p_route)
    p_route.add_argument('--prompts', default=str(REPO / 'benchmarks' / 'routing-heldout' / 'prompts.json'))
    p_route.add_argument('--split', choices=['dev', 'test', 'all'], default='test')
    p_route.add_argument('--limit', type=int, default=0, help='probe a seeded sample of this many prompts')
    p_route.add_argument('--parallel', type=int, default=3)
    p_route.add_argument('--seed', type=int, default=20261001)
    p_route.add_argument('--dry-run', action='store_true')
    p_route.add_argument('--no-warmup', action='store_true')
    p_route.set_defaults(func=cmd_routing)

    p_rrep = sub.add_parser('routing-report', help='summarize routing probes')
    p_rrep.add_argument('runs', nargs='+')
    p_rrep.add_argument('--json')
    p_rrep.set_defaults(func=cmd_routing_report)

    p_val = sub.add_parser('validate', help='check that tasks are fair (hidden tests fail on seed, pass on reference)')
    p_val.add_argument('--suite', required=True)
    p_val.add_argument('--tasks', help='comma-separated task ids')
    p_val.add_argument('--work', default=default_work)
    p_val.set_defaults(func=cmd_validate)

    p_rep = sub.add_parser('report', help='summarize one or more runs.jsonl files')
    p_rep.add_argument('runs', nargs='+')
    p_rep.add_argument('--baseline', default='baseline')
    p_rep.add_argument('--json')
    p_rep.set_defaults(func=cmd_report)

    p_comp = sub.add_parser('compact', help='write a committable copy of run files')
    p_comp.add_argument('runs', nargs='+')
    p_comp.add_argument('--out', required=True)
    p_comp.add_argument('--kind', action='append', help='keep only these kinds (task, overhead, routing, ...)')
    p_comp.add_argument('--arm', action='append', help='keep only these arms (repeatable)')
    p_comp.set_defaults(func=cmd_compact)

    p_orep = sub.add_parser('overhead-report', help='summarize overhead runs')
    p_orep.add_argument('runs', nargs='+')
    p_orep.add_argument('--json')
    p_orep.set_defaults(func=cmd_overhead_report)

    args = parser.parse_args(argv)
    if args.command in {'run', 'overhead', 'routing'}:
        if not args.arm or not args.model:
            parser.error('--arm and --model are required')
        if args.provider == 'ollama' and not args.ollama_key_file:
            parser.error('--provider ollama needs --ollama-key-file')
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
