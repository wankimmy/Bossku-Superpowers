#!/usr/bin/env python3
"""Summarise one dated run set (benchmarks/results/raw/<date>/) into <date>.json, the tables of its results page and its charts.

    python scripts/summarize_run_set.py 2026-10-10           # rewrite benchmarks/results/2026-10-10.json, the page tables and the charts
    python scripts/summarize_run_set.py 2026-10-10 --check   # change nothing; exit 1 when any of them differs from the raw rows

The numbers come from the same functions as `benchmark_agent.py report`. A file is named <suite>-<model>.jsonl, where the
suite is `test` (the 17 hidden-test coding tasks), `humaneval`, `memory` (10 two-session tasks) or `memory-rules` (12 more).
Rows that the harness excluded (a rate limit, a failed folder setup) are counted and never scored.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts.benchmark_agent import build_report, count_excluded, excluded, load_runs  # noqa: E402
from scripts.make_charts import Figure, Group, Panel  # noqa: E402

RESULTS = REPO / 'benchmarks' / 'results'
ASSETS = REPO / 'docs' / 'assets'
FILE_NAME = re.compile(r'(memory-rules|memory|test|humaneval)-(.+)\.jsonl')
SUITES = ('test', 'humaneval', 'memory', 'memory-rules')
BOTH = 'memory-both'   # the two memory sets pooled, for a model that has scored runs in both
SUITE_TITLE = {'test': 'Hidden-test coding tasks', 'humaneval': 'HumanEval problems',
               'memory': 'Remembering a rule: the 10 original two-session tasks',
               'memory-rules': 'Remembering a rule: the 12 added two-session tasks',
               BOTH: 'Remembering a rule: all 22 two-session tasks'}
# Where the 1-8 October run kept the same suite: a model that ran only one arm here borrows its baseline from there.
OLD_RAW = {'test': 'coding', 'humaneval': 'humaneval', 'memory': 'memory', 'memory-rules': 'memory'}
ARM_NAME = {'baseline': 'Without', 'ship': 'v2.2.0', 'ship2': 'Improved build'}
MODEL_NAME = {'claude-haiku-5-5': 'Claude Haiku 5.5', 'claude-opus-5-5': 'Claude Opus 5.5',
              'deepseek-v4.1-flash': 'DeepSeek V4.1 Flash', 'glm-5.3-flash': 'GLM 5.3 Flash', 'glm-5.3': 'GLM 5.3',
              'kimi-k3': 'Kimi K3'}


def split_name(path: Path) -> tuple[str, str]:
    match = FILE_NAME.fullmatch(path.name)
    if not match:
        raise SystemExit(f'{path} is not named <suite>-<model>.jsonl')
    return match.group(1), match.group(2)


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def reused_baseline(suite: str, model: str, tasks: set[str], raw: Path) -> tuple[list[dict], dict]:
    """The 1-8 October `baseline` runs of the same model on the same tasks, for a model that ran no baseline here."""
    path = raw.parent / f'{OLD_RAW[suite]}-{model}.jsonl'
    rows = [r for r in load_runs([str(path)], 'task') if r['arm'] == 'baseline' and r['task'] in tasks] if path.exists() else []
    versions = Counter(r['claude_code_version'] for r in rows)
    source = {'file': f'raw/{path.name}', 'arm': 'baseline', 'tasks': len({r['task'] for r in rows}), 'runs': len(rows),
              'claude_code_versions': dict(sorted(versions.items())),
              'first_row': min((r['timestamp'] for r in rows), default=None),
              'last_row': max((r['timestamp'] for r in rows), default=None)}
    return rows, source


def one_cell(paths: list[Path], suite: str, model: str) -> dict:
    scored = load_runs([str(p) for p in paths], 'task')
    rate_limited = sum(1 for p in paths for r in read_rows(p)
                       if r.get('kind') == 'task' and r.get('infrastructure_failure') and '(429)' in (r.get('final_text') or ''))
    canary = [('answered NONE' if re.fullmatch(r'\W*NONE\W*', (r.get('final_text') or '').strip(), re.I) else
               'no answer (excluded)' if excluded(r) else 'other answer')
              for p in paths for r in read_rows(p) if r.get('kind') == 'selftest']   # the baseline must say it was given nothing
    cell: dict = {'arms': {}, 'paired': {}, 'excluded_runs': count_excluded([str(p) for p in paths]),
                  'excluded_rate_limited': rate_limited, 'baseline_canary': canary, 'baseline_source': 'same run'}
    if not scored:
        return cell
    others = {r['task'] for r in scored if r['arm'] != 'baseline'}
    if others and not any(r['arm'] == 'baseline' for r in scored):
        old, source = reused_baseline(suite, model, others, paths[0].parent)
        scored, cell['baseline_source'] = scored + old, source
    block = build_report(scored, 'baseline')['models'][model]
    cell['arms'] = block['arms']
    cell['paired'] = block['paired']
    if 'ship' in block['arms'] and 'ship2' in block['arms']:   # the improved build against v2.2.0 (rows of two sessions of work)
        cell['paired_ship2_vs_ship'] = build_report(scored, 'ship')['models'][model]['paired']['ship2']
    return cell


def windows(files: list[Path]) -> dict:
    """First and last row time and Claude Code version per model and arm, from the raw rows."""
    out: dict = {}
    for path in files:
        for row in read_rows(path):
            if row.get('kind') != 'task':
                continue
            cell = out.setdefault(row['model'], {}).setdefault(row['arm'], {'rows': 0, 'first': row['timestamp'],
                                                                              'last': row['timestamp'], 'versions': Counter()})
            cell['rows'] += 1
            cell['first'], cell['last'] = min(cell['first'], row['timestamp']), max(cell['last'], row['timestamp'])
            if row.get('claude_code_version'):
                cell['versions'][row['claude_code_version']] += 1
    return {m: {a: {**c, 'versions': dict(sorted(c['versions'].items()))} for a, c in sorted(arms.items())}
            for m, arms in sorted(out.items())}


def limit_timeline(files: list[Path]) -> dict:
    """When the Ollama runs stopped being scored: the newest scored row, and the first and last rate-limited one."""
    rows = [r for path in files for r in read_rows(path) if r.get('kind') == 'task' and r.get('provider') == 'ollama']
    scored = [r['timestamp'] for r in rows if not excluded(r)]
    limited = [r['timestamp'] for r in rows if r.get('infrastructure_failure') and '(429)' in (r.get('final_text') or '')]
    return {'last_scored_row': max(scored, default=None), 'first_rate_limited_row': min(limited, default=None),
            'last_rate_limited_row': max(limited, default=None),
            'scored_rows_after_first_rate_limit': sum(1 for ts in scored if limited and ts > min(limited))}


def summarize(raw: Path) -> dict:
    files = sorted(raw.glob('*.jsonl'))
    paths = {split_name(path): path for path in files}
    suites: dict = {s: {} for s in SUITES + (BOTH,)}
    for (suite, model), path in sorted(paths.items(), key=lambda item: item[0][::-1]):
        suites[suite][model] = one_cell([path], suite, model)
    for model in sorted({model for _, model in paths}):
        both = [paths.get((suite, model)) for suite in ('memory', 'memory-rules')]
        if all(both) and suites['memory'][model]['arms'] and suites['memory-rules'][model]['arms']:
            suites[BOTH][model] = one_cell(both, 'memory', model)
    return {'set': raw.name, 'suites': suites, 'rows': windows(files), 'ollama_limit': limit_timeline(files)}


# --------------------------------------------------------------------------- the tables of the results page

def pct(value: float) -> str:
    return f'{100 * value:.0f}%'


def signed(value: float) -> str:
    return '0' if round(value) == 0 else f'{round(value):+d}'


def interval_points(m: dict) -> str:
    """A paired difference in points with its 95% interval, from a `paired.passed` block."""
    if not m.get('tasks') or m['ci'][0] != m['ci'][0]:   # no tasks in common, or too few for an interval (NaN)
        return '-'
    return f'{signed(100 * m["mean_diff"])} ({signed(100 * m["ci"][0])} to {signed(100 * m["ci"][1])})'


def tokens(arm: dict) -> float:
    return arm['input_tokens_mean'] + arm['output_tokens_mean']


def model_label(model: str) -> str:
    return MODEL_NAME.get(model, model)


def suite_table(suite: str, cells: dict) -> str:
    lines = ['| Model | Setup | Runs | Passed | Pass rate (95% interval) | Change against without, points (95% interval) | '
             'Tokens per run | Tokens against without | Turns per run | Cost per run |',
             '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for model, cell in cells.items():
        if not cell['arms']:
            lines.append(f'| {model_label(model)} | none scored | 0 | - | - | - | - | - | - | - |')
            continue
        base = cell['arms'].get('baseline')
        for arm, s in cell['arms'].items():
            ci = f'{pct(s["pass_ci"][0])} to {pct(s["pass_ci"][1])}'
            change = '-' if arm == 'baseline' else interval_points(cell['paired'].get(arm, {}).get('passed', {}))
            ratio = f'{tokens(s) / tokens(base):.1f}×' if base and arm != 'baseline' else '-'
            cost = f'${s["cost_mean"]:.3f}' if s['cost_mean'] is not None else '-'
            label = ARM_NAME.get(arm, arm) + (' (reused 1-8 October runs)' if arm == 'baseline' and cell['baseline_source'] != 'same run' else '')
            lines.append(f'| {model_label(model)} | {label} | {s["runs"]} | {s["passed"]} | {pct(s["pass_rate"])} ({ci}) | '
                         f'{change} | {tokens(s) / 1000:,.0f}k | {ratio} | {s["turns_mean"]:.1f} | {cost} |')
    return '\n'.join(lines)


def improved_table(suites: dict) -> str:
    lines = ['| Suite | Model | Pass rate v2.2.0 | Pass rate improved | Change, points (95% interval) | '
             'Tokens per run v2.2.0 | Tokens per run improved | Turns per run v2.2.0 | Turns per run improved |',
             '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for suite in SUITES + (BOTH,):
        for model, cell in suites[suite].items():
            if 'paired_ship2_vs_ship' not in cell:
                continue
            a, b = cell['arms']['ship'], cell['arms']['ship2']
            lines.append(f'| {SUITE_TITLE[suite]} | {model_label(model)} | {pct(a["pass_rate"])} ({a["passed"]}/{a["runs"]}) | '
                         f'{pct(b["pass_rate"])} ({b["passed"]}/{b["runs"]}) | '
                         f'{interval_points(cell["paired_ship2_vs_ship"]["passed"])} | {tokens(a) / 1000:,.0f}k | '
                         f'{tokens(b) / 1000:,.0f}k | {a["turns_mean"]:.1f} | {b["turns_mean"]:.1f} |')
    return '\n'.join(lines)


def checking_table(suites: dict) -> str:
    lines = ['| Suite | Model | Without | v2.2.0 | Improved build |', '|---|---|---:|---:|---:|']
    for suite in SUITES:
        for model, cell in suites[suite].items():
            if cell['arms']:
                shown = [f'{s["unchecked_finishes"]} of {s["edited_runs"]}' if (s := cell['arms'].get(arm)) else '-' for arm in ARM_NAME]
                lines.append(f'| {SUITE_TITLE[suite]} | {model_label(model)} | ' + ' | '.join(shown) + ' |')
    return '\n'.join(lines)


def when_table(rows: dict) -> str:
    lines = ['| Model | Setup | Task rows (scored or excluded) | First row (UTC) | Last row (UTC) | Claude Code version |', '|---|---|---:|---|---|---|']
    for model, arms in rows.items():
        for arm, w in arms.items():
            lines.append(f'| {model_label(model)} | {ARM_NAME[arm]} | {w["rows"]} | {w["first"][:16].replace("T", " ")} | '
                         f'{w["last"][:16].replace("T", " ")} | {", ".join(w["versions"]) or "none recorded"} |')
    return '\n'.join(lines)


def reused_table(suites: dict) -> str:
    lines = ['| Suite | Model | Taken from | Tasks | Runs | First row (UTC) | Last row (UTC) | Claude Code version |',
             '|---|---|---|---:|---:|---|---|---|']
    for suite in SUITES + (BOTH,):
        for model, cell in suites[suite].items():
            if cell['baseline_source'] != 'same run':
                src = cell['baseline_source']
                lines.append(f'| {SUITE_TITLE[suite]} | {model_label(model)} | `{src["file"]}` | {src["tasks"]} | {src["runs"]} | '
                             f'{src["first_row"][:16].replace("T", " ")} | {src["last_row"][:16].replace("T", " ")} | '
                             f'{", ".join(src["claude_code_versions"])} |')
    return '\n'.join(lines)


def excluded_table(suites: dict) -> str:
    lines = ['| Suite | Model | Excluded runs (setup, reason: count) | Of those, "Request rejected (429)" |', '|---|---|---|---:|']
    for suite in SUITES:
        for model, cell in suites[suite].items():
            if cell['excluded_runs']:
                what = '; '.join(f'{ARM_NAME[key.split(": ")[0]]}, {key.split(": ")[1]}: {n}' for key, n in sorted(cell['excluded_runs'].items()))
                lines.append(f'| {SUITE_TITLE[suite]} | {model_label(model)} | {what} | {cell["excluded_rate_limited"]} |')
    total = Counter()
    for suite in SUITES:
        for cell in suites[suite].values():
            for key, n in cell['excluded_runs'].items():
                total[key.split(": ")[1]] += n
            total['429'] += cell['excluded_rate_limited']
    lines.append(f'| All | All | infrastructure failure: {total["infrastructure failure"]}; harness error: {total["harness error"]} | {total["429"]} |')
    return '\n'.join(lines)


def render(summary: dict) -> dict[str, str]:
    """Block name -> markdown, for the <!-- name:start --> ... <!-- name:end --> markers of the results page."""
    blocks = {f'set-{suite}': suite_table(suite, summary['suites'][suite]) for suite in SUITES + (BOTH,)}
    blocks['set-improved'] = improved_table(summary['suites'])
    blocks['set-when'] = when_table(summary['rows'])
    blocks['set-reused'] = reused_table(summary['suites'])
    blocks['set-checking'] = checking_table(summary['suites'])
    blocks['set-excluded'] = excluded_table(summary['suites'])
    return blocks


# ------------------------------------------------------------------------------ the charts of the results page
# Three setups in a fixed order, one colour each (SERIES in make_charts.py), so a reader learns the colours once.
# Drawn from the summary alone, as static SVG: GitHub shows no hover, so the tables of the page are the data view.

CHART_ARMS = ('baseline', 'ship', 'ship2')
# ponytail: the charts are specific to the 2026-10-10 set (both Claude models and the ship2 arm).
CHART_MODELS = ('claude-haiku-5-5', 'claude-opus-5-5')
FOOT_PASS = ('Whiskers: 95% interval, the range the real pass rate most likely sits in. Labels: tasks passed.\n'
             'One trial per task. The improved build ran about three hours after v2.2.0, so read gaps as hints.')


def pass_groups(cells: dict, noun: str = '') -> list[Group]:
    """One group per model: pass rate with its 95% whiskers for the three setups, labelled with the pass count."""
    groups = []
    for model in CHART_MODELS:
        arms = cells[model]['arms']
        groups.append(Group(model_label(model), [100 * arms[a]['pass_rate'] for a in CHART_ARMS],
                            f'{arms["baseline"]["runs"]} {noun}' if noun else '',
                            ci=[tuple(100 * c for c in arms[a]['pass_ci']) for a in CHART_ARMS],
                            tips=[f'{pct(arms[a]["pass_rate"])}  ({arms[a]["passed"]}/{arms[a]["runs"]})' for a in CHART_ARMS]))
    return groups


def pass_panel(title: str, groups: list[Group]) -> Panel:
    return Panel(title, groups, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100])


def chart_memory(summary: dict) -> str:
    return Figure('Remembering a rule from an earlier session',
                  'Session 1 states a project rule. Session 2 asks for work that breaks it unless the agent remembers.',
                  list(CHART_ARMS), [pass_panel('', pass_groups(summary['suites'][BOTH], 'tasks'))], footnote=FOOT_PASS).render()


def chart_coding(summary: dict) -> str:
    panels = []
    for title, suite, noun in (('Hidden-test coding tasks', 'test', 'tasks'), ('HumanEval problems', 'humaneval', 'problems')):
        cells = summary['suites'][suite]
        runs = cells[CHART_MODELS[0]]['arms']['baseline']['runs']
        panels.append(pass_panel(f'{title} ({runs} {noun})', pass_groups(cells)))
    return Figure('Coding tasks and HumanEval: hidden tests passed',
                  'Both models already pass almost everything without Bossku Superpower, so there is little room to gain.',
                  list(CHART_ARMS), panels, footnote=FOOT_PASS).render()


def token_change(arms: dict, arm: str) -> float:
    """Percent more tokens per run than the Without setup; below zero is fewer."""
    return 100 * (tokens(arms[arm]) / tokens(arms['baseline']) - 1)


def chart_tokens(summary: dict) -> str:
    suites = (('Hidden-test coding tasks', 'test', 'tasks'), ('HumanEval problems', 'humaneval', 'problems'),
              ('Two-session tasks', BOTH, 'tasks'))
    changes = [token_change(summary['suites'][suite][model]['arms'], arm)
               for _, suite, _ in suites for model in CHART_MODELS for arm in ('ship', 'ship2')]
    low, high = min(-20, 20 * math.floor(min(changes) / 20)), max(20, 20 * math.ceil(max(changes) / 20))   # one scale for every panel
    panels = []
    for title, suite, noun in suites:
        cells = summary['suites'][suite]
        groups = [Group(model_label(model), [token_change(cells[model]['arms'], arm) for arm in ('ship', 'ship2')],
                        f'Without: {tokens(cells[model]["arms"]["baseline"]) / 1000:,.0f}k tokens',
                        tips=[f'{signed(token_change(cells[model]["arms"], arm))}%' for arm in ('ship', 'ship2')])
                  for model in CHART_MODELS]
        runs = cells[CHART_MODELS[0]]['arms']['baseline']['runs']
        panels.append(Panel(f'{title} ({runs} {noun})', groups, fmt=signed, unit='%', axis_min=low, axis_max=high,
                            ticks=list(range(low, high + 1, 20))))
    return Figure('Extra tokens per run compared with no Bossku Superpower',
                  'Zero is the run without Bossku Superpower. Left of zero used fewer tokens, right of zero used more.',
                  ['ship', 'ship2'], panels,
                  footnote='Tokens per run: every input token across all turns (cached or not) plus the output tokens, averaged.\n'
                           'One trial per task. The two builds ran about three hours apart, so read it as a hint.').render()


def charts(summary: dict) -> dict[str, str]:
    """File name -> SVG for the three charts of the results page."""
    prefix = f'benchmark-{summary["set"]}-'
    return {prefix + 'memory.svg': chart_memory(summary), prefix + 'coding.svg': chart_coding(summary),
            prefix + 'tokens.svg': chart_tokens(summary)}


def marker(name: str, edge: str) -> str:
    return f'<!-- {name}:{edge} -->'


def inject(page: str, blocks: dict[str, str]) -> str:
    for name, text in blocks.items():
        start, end = marker(name, 'start'), marker(name, 'end')
        if start not in page or end not in page:
            raise SystemExit(f'the results page has no {start} ... {end} block')
        head, rest = page.split(start, 1)
        page = head + start + '\n' + text + '\n' + end + rest.split(end, 1)[1]
    return page


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('date', help='folder name under benchmarks/results/raw/, for example 2026-10-10')
    parser.add_argument('--check', action='store_true', help='write nothing; exit 1 if the saved files differ')
    args = parser.parse_args(argv)
    summary = summarize(RESULTS / 'raw' / args.date)
    saved, page_path = RESULTS / f'{args.date}.json', REPO / 'docs' / 'benchmarks' / f'results-{args.date}.md'
    text = json.dumps(summary, indent=2) + '\n'
    page = page_path.read_text(encoding='utf-8')   # text mode: a CRLF page reads as LF
    new_page = inject(page, render(summary))
    drawn = charts(json.loads(text))   # from the saved text, so a chart can never show more than the summary does
    if args.check:
        same = (saved.exists() and saved.read_text(encoding='utf-8') == text and new_page == page and
                all((ASSETS / name).exists() and (ASSETS / name).read_text(encoding='utf-8') == svg for name, svg in drawn.items()))
        print('up to date' if same else 'out of date')
        return 0 if same else 1
    saved.write_text(text, encoding='utf-8', newline='\n')
    for name, svg in drawn.items():
        (ASSETS / name).write_text(svg, encoding='utf-8', newline='\n')
    ending = '\r\n' if b'\r\n' in page_path.read_bytes() else '\n'   # keep the page's own line endings
    page_path.write_text(new_page, encoding='utf-8', newline=ending)
    print(f'wrote {saved.relative_to(REPO)}, the tables of {page_path.relative_to(REPO)} and {len(drawn)} charts in {ASSETS.relative_to(REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
