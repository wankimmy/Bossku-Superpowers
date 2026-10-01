#!/usr/bin/env python3
"""Draw the README benchmark charts from the saved result files; no number is typed by hand.

    python scripts/make_charts.py            # reads benchmarks/results/*.json, writes docs/assets/benchmark-*.svg

One rulebook for every chart: bars grow from a single baseline, thin marks with a 4 px rounded data end, a 2 px
gap between touching bars, hairline grid, the value at the bar tip, text in text colours (never the series
colour), a legend for two or more series, and a card background of its own so the chart reads on GitHub's light
and dark themes. Archify draws the architecture and flow diagrams; it has no bar-chart type, so these follow
the same palette and typography instead.
"""

from __future__ import annotations

import argparse
import html
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / 'benchmarks' / 'results'
ASSETS = REPO / 'docs' / 'assets'

LIGHT = {'surface': '#fcfcfb', 'ink': '#0b0b0b', 'ink2': '#52514e', 'muted': '#898781', 'grid': '#e1e0d9', 'base': '#c3c2b7'}
DARK = {'surface': '#1a1a19', 'ink': '#ffffff', 'ink2': '#c3c2b7', 'muted': '#898781', 'grid': '#2c2c2a', 'base': '#383835'}
# Categorical slots 1-3 in their fixed order: one colour per entity, never re-ranked. (light, dark)
SERIES = {
    'baseline': ('Without BosskuAI', '#2a78d6', '#3987e5'),
    'keyword': ('Keyword search only', '#2a78d6', '#3987e5'),
    'before': ('BosskuAI before', '#eb6834', '#d95926'),
    'after': ('BosskuAI after', '#1baf7a', '#199e70'),
}
FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
MODELS = {
    'claude-haiku-4-5-20251001': 'Claude Haiku 4.5', 'claude-sonnet-5-5': 'Claude Sonnet 5.5',
    'nemotron-3-nano:30b': 'Nemotron 3 Nano 30B', 'deepseek-v4.1-flash': 'DeepSeek V4.1 Flash',
    'glm-5.3-flash': 'GLM 5.3 Flash', 'gpt-oss:20b': 'gpt-oss 20B',
}


def model_name(raw: str) -> str:
    return MODELS.get(raw, raw)


def text_width(text: str, size: float) -> float:
    return len(text) * size * 0.56


def nice_ticks(maximum: float, target: int = 5) -> list[float]:
    if maximum <= 0:
        return [0.0, 1.0]
    raw = maximum / target
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next((m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw), magnitude * 10)
    ticks, value = [], 0.0
    while value <= maximum + step * 0.01:
        ticks.append(round(value, 10))
        value += step
    return ticks


@dataclass
class Group:
    label: str
    values: list[float | None]
    sublabel: str = ''
    ci: list[tuple[float, float] | None] | None = None
    tips: list[str] | None = None


@dataclass
class Panel:
    title: str
    groups: list[Group]
    fmt: object = staticmethod(lambda v: f'{v:,.0f}')
    unit: str = ''
    axis_max: float | None = None
    ticks: list[float] | None = None
    note: str = ''


@dataclass
class Figure:
    title: str
    subtitle: str
    series: list[str]
    panels: list[Panel]
    footnote: str = ''
    width: int = 880
    label_width: int = 176
    _out: list[str] = field(default_factory=list)

    def render(self) -> str:
        bar_h, gap, group_gap, panel_gap = 18, 2, 22, 40
        left, right_pad = 28 + self.label_width, 150
        plot_w = self.width - left - right_pad
        y = 112
        body: list[str] = []
        for panel in self.panels:
            highest = max((v for g in panel.groups for v in g.values if v is not None), default=1.0)
            highs = [c[1] for g in panel.groups for c in (g.ci or []) if c]
            axis_max = panel.axis_max or max([highest, *highs]) * 1.04
            ticks = panel.ticks or nice_ticks(axis_max)
            axis_max = max(axis_max, ticks[-1])
            block = len(self.series) * bar_h + (len(self.series) - 1) * gap
            rows_h = len(panel.groups) * block + (len(panel.groups) - 1) * group_gap

            def x_of(value: float) -> float:
                return left + plot_w * value / axis_max

            if panel.title:
                body.append(f'<text class="ink" x="28" y="{y}" font-size="15" font-weight="650">{html.escape(panel.title)}</text>')
                if panel.note:
                    body.append(f'<text class="muted" x="{28 + text_width(panel.title, 15) + 12:.0f}" y="{y}" font-size="12">'
                                f'{html.escape(panel.note)}</text>')
                y += 22
            top = y
            for tick in ticks:
                x = x_of(tick)
                body.append(f'<line class="grid" x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{top + rows_h + 6}" stroke-width="1"/>')
                body.append(f'<text class="muted" x="{x:.1f}" y="{top + rows_h + 22}" font-size="12" text-anchor="middle">'
                            f'{html.escape(panel.fmt(tick))}{html.escape(panel.unit)}</text>')
            body.append(f'<line class="base" x1="{left}" y1="{top - 8}" x2="{left}" y2="{top + rows_h + 6}" stroke-width="1.5"/>')
            gy = top
            for group in panel.groups:
                multiline = bool(group.sublabel)
                body.append(f'<text class="ink" x="28" y="{gy + block / 2 + (-2 if multiline else 5):.1f}" font-size="14" '
                            f'font-weight="600">{html.escape(group.label)}</text>')
                if multiline:
                    body.append(f'<text class="muted" x="28" y="{gy + block / 2 + 15:.1f}" font-size="12">{html.escape(group.sublabel)}</text>')
                for index, value in enumerate(group.values):
                    by = gy + index * (bar_h + gap)
                    if value is None:
                        continue
                    width = max(x_of(max(value, 0)) - left, 1.0)
                    r = min(4, width / 2, bar_h / 2)
                    path = (f'M{left},{by} H{left + width - r:.1f} Q{left + width:.1f},{by} {left + width:.1f},{by + r:.1f} '
                            f'V{by + bar_h - r:.1f} Q{left + width:.1f},{by + bar_h} {left + width - r:.1f},{by + bar_h} H{left} Z')
                    body.append(f'<path class="s{index}" d="{path}"/>')
                    tip = group.tips[index] if group.tips else f'{panel.fmt(value)}{panel.unit}'
                    label_x = left + width + 8
                    ci = group.ci[index] if group.ci else None
                    if ci:
                        lo, hi, cy = x_of(ci[0]), x_of(ci[1]), by + bar_h / 2
                        body.append(f'<line class="whisker" x1="{lo:.1f}" y1="{cy}" x2="{hi:.1f}" y2="{cy}" stroke-width="1.5"/>')
                        for edge in (lo, hi):
                            body.append(f'<line class="whisker" x1="{edge:.1f}" y1="{cy - 4}" x2="{edge:.1f}" y2="{cy + 4}" stroke-width="1.5"/>')
                        label_x = max(label_x, hi + 8)
                    body.append(f'<text class="ink" x="{label_x:.1f}" y="{by + bar_h / 2 + 4.5:.1f}" font-size="13" font-weight="600">'
                                f'{html.escape(tip)}</text>')
                gy += block + group_gap
            y = top + rows_h + 22 + panel_gap
        height = int(y - panel_gap + 30 + (22 * (self.footnote.count('\n') + 1) if self.footnote else 0))

        css = [f'text{{font-family:{FONT}}}']
        for mode, palette, key in (('', LIGHT, 1), ('dark', DARK, 2)):
            rules = (f'.card{{fill:{palette["surface"]}}}.ink{{fill:{palette["ink"]}}}.ink2{{fill:{palette["ink2"]}}}'
                     f'.muted{{fill:{palette["muted"]}}}.grid{{stroke:{palette["grid"]}}}.base{{stroke:{palette["base"]}}}'
                     f'.whisker{{stroke:{palette["ink2"]}}}')
            for index, name in enumerate(self.series):
                rules += f'.s{index}{{fill:{SERIES[name][key]}}}'
            css.append(rules if not mode else f'@media (prefers-color-scheme:dark){{{rules}}}')
        desc = [self.title + '.', self.subtitle]
        for panel in self.panels:
            for g in panel.groups:
                desc.append(f'{panel.title} {g.label}: ' + ', '.join(
                    f'{SERIES[s][0]} {g.tips[i] if g.tips else panel.fmt(v) + panel.unit}'
                    for i, (s, v) in enumerate(zip(self.series, g.values)) if v is not None) + '.')
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {height}" width="{self.width}" '
               f'height="{height}" role="img" aria-labelledby="t d">',
               f'<title id="t">{html.escape(self.title)}</title>',
               f'<desc id="d">{html.escape(" ".join(desc))}</desc>',
               '<style>' + ''.join(css) + '</style>',
               f'<rect class="card" width="{self.width}" height="{height}" rx="14"/>',
               f'<text class="ink" x="28" y="42" font-size="22" font-weight="650">{html.escape(self.title)}</text>',
               f'<text class="ink2" x="28" y="66" font-size="14">{html.escape(self.subtitle)}</text>']
        lx = 28
        for index, name in enumerate(self.series):
            label = SERIES[name][0]
            out.append(f'<rect class="s{index}" x="{lx}" y="78" width="12" height="12" rx="3"/>')
            out.append(f'<text class="ink2" x="{lx + 18}" y="89" font-size="13">{html.escape(label)}</text>')
            lx += 18 + int(text_width(label, 13)) + 26
        out.extend(body)
        for line_no, line in enumerate(self.footnote.split('\n') if self.footnote else []):
            out.append(f'<text class="muted" x="28" y="{height - 16 - 16 * (self.footnote.count(chr(10)) - line_no)}" font-size="12">'
                       f'{html.escape(line)}</text>')
        out.append('</svg>')
        return '\n'.join(out)


# ----------------------------------------------------------------------------------------------- charts

def load(results: Path, name: str) -> dict:
    path = results / name
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}


def chart_session_overhead(data: dict) -> str | None:
    """What BosskuAI adds to the first call of every session, per Claude model."""
    if not data:
        return None
    tokens, dollars = [], []
    for model, arms in data.items():
        base = arms['baseline']
        window = base.get('context_window')
        sub = (f'{window // 1_000_000}M-token window' if window >= 1_000_000 else f'{window // 1000}k-token window') if window else ''
        extra_t = [arms[a]['input_tokens_median'] - base['input_tokens_median'] for a in ('before', 'after')]
        extra_c = [arms[a]['cost_median'] - base['cost_median'] for a in ('before', 'after')]
        tokens.append(Group(model_name(model), extra_t, sub,
                            tips=[f'+{extra_t[0]:,.0f}', f'+{extra_t[1]:,.0f}  ({extra_t[0] / max(extra_t[1], 1):.1f}x less)']))
        dollars.append(Group(model_name(model), extra_c, sub,
                             tips=[f'+${extra_c[0]:.4f}', f'+${extra_c[1]:.4f}  ({extra_c[0] / max(extra_c[1], 1e-9):.1f}x less)']))
    figure = Figure('What BosskuAI adds to every session',
                    'First call of a Claude Code session, compared with no BosskuAI (median of 3 runs)',
                    ['before', 'after'],
                    [Panel('Extra input tokens', tokens, fmt=lambda v: f'{v:,.0f}'),
                     Panel('Extra cost of that first call', dollars, fmt=lambda v: f'${v:.3f}')],
                    footnote='A one-word prompt after a cache warm-up. Cost is Claude Code\'s own list-price figure.')
    return figure.render()


def chart_routing(data: dict) -> str | None:
    """Held-out skill search: prompts the router was never tuned on."""
    split = (data.get('splits') or {}).get('test')
    names = ('description-only', 'before', 'after')
    if not split or not all(name in split for name in names):
        return None
    rows = [('Right skill ranked first', 'top1'), ('Right skill in the top three', 'top3')]
    groups = []
    for label, key in rows:
        groups.append(Group(label, [split[a][key]['rate'] * 100 for a in names],
                            ci=[tuple(100 * c for c in split[a][key]['ci']) for a in names]))
    coverage = [Group('Parts of a request covered', [None, split['before']['concern_coverage'] * 100, split['after']['concern_coverage'] * 100]),
                Group('Whole request covered', [None, split['before']['all_concerns_covered']['rate'] * 100,
                                                split['after']['all_concerns_covered']['rate'] * 100])]
    n = split['after']['prompts']
    figure = Figure('Finding the right skill on new prompts',
                    f'{n} held-out requests written without seeing the router (never used for tuning)',
                    ['keyword', 'before', 'after'],
                    [Panel('Ranking', groups, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100]),
                     Panel('Requests with several jobs', coverage, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100])],
                    footnote='Whiskers show a 95% interval. The keyword baseline only ranks, so it has no coverage bars.')
    return figure.render()


ARMS = ('baseline', 'before', 'after')


def complete_models(data: dict) -> list[tuple[str, dict]]:
    """(model, arms) for every model that has all three versions."""
    return [(model, block['arms']) for model, block in (data.get('models') or {}).items()
            if all(a in block['arms'] for a in ARMS)]


def chart_pass_rates(coding: dict, humaneval: dict) -> str | None:
    panels = []
    for title, data in (('Hidden-test coding tasks', coding), ('HumanEval problems', humaneval)):
        groups = []
        for model, arms in complete_models(data):
            n = arms['baseline']['runs']
            groups.append(Group(model_name(model), [arms[a]['pass_rate'] * 100 for a in ARMS],
                                f'{n} runs per version',
                                ci=[tuple(100 * c for c in arms[a]['pass_ci']) for a in ARMS]))
        if groups:
            panels.append(Panel(title, groups, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100]))
    if not panels:
        return None
    return Figure('Tasks finished: hidden tests passed', 'Same model, same harness, same tasks; only BosskuAI changes',
                  list(ARMS), panels,
                  footnote='Whiskers show a 95% interval. Small samples: read overlaps as "no clear difference".').render()


def chart_checking(coding: dict) -> str | None:
    """How often an agent that changed code ended without running anything afterwards."""
    groups = []
    for model, arms in complete_models(coding):
        if any(arms[a].get('unchecked_rate') is None for a in ARMS):
            continue
        rates = [arms[a]['unchecked_rate'] * 100 for a in ARMS]
        groups.append(Group(model_name(model), rates, 'of the runs that changed code',
                            tips=[f'{r:.0f}%  ({arms[a]["unchecked_finishes"]} of {arms[a]["edited_runs"]})'
                                  for r, a in zip(rates, ARMS)]))
    if not groups:
        return None
    return Figure('Did the agent run its code before finishing?',
                  'Runs that changed code and then ended without running anything (lower is better)',
                  list(ARMS), [Panel('', groups, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100])],
                  footnote='Read from the tool calls alone, the same way for every version.').render()


def chart_effort(coding: dict) -> str | None:
    tokens, solved = [], []
    for model, arms in complete_models(coding):
        per_run = [(arms[a]['input_tokens_mean'] + arms[a]['output_tokens_mean']) / 1000 for a in ('baseline', 'before', 'after')]
        tokens.append(Group(model_name(model), per_run, tips=[f'{v:,.0f}k' for v in per_run]))
        per_solved = []
        for a in ('baseline', 'before', 'after'):
            rate = arms[a]['pass_rate']
            per_solved.append((arms[a]['input_tokens_mean'] + arms[a]['output_tokens_mean']) / 1000 / rate if rate else None)
        solved.append(Group(model_name(model), per_solved, tips=[f'{v:,.0f}k' if v else 'none solved' for v in per_solved]))
    if not tokens:
        return None
    return Figure('What a task costs in tokens', 'Input plus output tokens the model processed, all turns (lower is better)',
                  ['baseline', 'before', 'after'],
                  [Panel('Tokens per run (thousands)', tokens, fmt=lambda v: f'{v:,.0f}', unit='k'),
                   Panel('Tokens per solved task (thousands)', solved, fmt=lambda v: f'{v:,.0f}', unit='k')],
                  footnote='Input counts every turn, cached or not. Ollama Cloud bills by subscription, so tokens are the honest unit.').render()


def chart_live_routing(data: dict) -> str | None:
    groups = []
    for model, arms in (data or {}).items():
        if 'before' in arms and 'after' in arms:
            groups.append(Group(model_name(model), [arms['before']['rate'] * 100, arms['after']['rate'] * 100],
                                f'{arms["after"]["prompts"]} requests',
                                ci=[tuple(100 * c for c in arms[a]['ci']) for a in ('before', 'after')]))
    if not groups:
        return None
    return Figure('Does the agent open a fitting skill?', 'A real agent, one request at a time, stopped a few steps after its first skill',
                  ['before', 'after'],
                  [Panel('', groups, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100])],
                  footnote='Counted when the agent loads a skill an independent reader accepted for that request.').render()


README_START, README_END = '<!-- results:start -->', '<!-- results:end -->'


def table(head: list[str], rows: list[list[str]]) -> str:
    lines = ['| ' + ' | '.join(head) + ' |', '|' + '---|' + '---:|' * (len(head) - 1)]
    lines += ['| ' + ' | '.join(row) + ' |' for row in rows]
    return '\n'.join(lines)


def results_markdown(results: Path) -> str:
    """The numbers the README quotes, read from the saved result files so none is typed by hand."""
    data = lambda name: load(results, name)  # noqa: E731
    parts: list[str] = []
    overhead = data('overhead.json')
    if overhead:
        rows = []
        for model, arms in overhead.items():
            if not all(a in arms for a in ARMS):
                continue
            rows.append([f'{model_name(model)}: input tokens'] + [f'{arms[a]["input_tokens_median"]:,.0f}' for a in ARMS])
            rows.append([f'{model_name(model)}: cost'] + [f'${arms[a]["cost_median"]:.4f}' for a in ARMS])
        if rows:
            parts.append(table(['First call of a session', 'Without BosskuAI', 'Before', 'After'], rows))
    split = (data('routing-heldout.json').get('splits') or {}).get('test') or {}
    names = ('description-only', 'before', 'after')
    if all(name in split for name in names):
        pct = lambda value: f'{100 * value:.0f}%'  # noqa: E731
        rows = [['Right skill ranked first'] + [pct(split[n]['top1']['rate']) for n in names],
                ['Right skill in the top three'] + [pct(split[n]['top3']['rate']) for n in names],
                ['Every part of a multi-part request covered', '-'] + [pct(split[n]['all_concerns_covered']['rate']) for n in names[1:]]]
        parts.append(table([f'Finding a skill ({split["after"]["prompts"]} new requests)', 'Keyword search', 'Before', 'After'], rows))
    for title, name in (('Hidden-test coding tasks', 'coding-test.json'), ('HumanEval problems', 'humaneval.json')):
        rows = []
        for model, arms in complete_models(data(name)):
            runs = arms['baseline']['runs']
            rows.append([f'{model_name(model)}: tasks passed ({runs} runs each)'] + [
                f'{100 * arms[a]["pass_rate"]:.0f}% ({arms[a]["passed"]}/{arms[a]["runs"]})' for a in ARMS])
            rows.append([f'{model_name(model)}: tokens per run'] + [
                f'{(arms[a]["input_tokens_mean"] + arms[a]["output_tokens_mean"]) / 1000:,.0f}k' for a in ARMS])
            if all(arms[a].get('unchecked_rate') is not None for a in ARMS) and name == 'coding-test.json':
                rows.append([f'{model_name(model)}: ended without running its code'] + [
                    f'{100 * arms[a]["unchecked_rate"]:.0f}%' for a in ARMS])
        if rows:
            parts.append(table([title, 'Without BosskuAI', 'Before', 'After'], rows))
    return '\n\n'.join(parts)


def inject_results(readme: Path, block: str) -> bool:
    text = readme.read_text(encoding='utf-8')
    if README_START not in text or README_END not in text:
        raise SystemExit(f'{readme} has no {README_START} ... {README_END} block')
    head, rest = text.split(README_START, 1)
    tail = rest.split(README_END, 1)[1]
    new = f'{head}{README_START}\n{block}\n{README_END}{tail}'
    if new == text:
        return False
    readme.write_text(new, encoding='utf-8', newline='\n')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--results', type=Path, default=RESULTS)
    parser.add_argument('--out', type=Path, default=ASSETS)
    parser.add_argument('--readme', type=Path, help=f'rewrite the block between {README_START} and {README_END}')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    data = lambda name: load(args.results, name)  # noqa: E731
    jobs = {
        'benchmark-session-overhead.svg': chart_session_overhead(data('overhead.json')),
        'benchmark-routing.svg': chart_routing(data('routing-heldout.json')),
        'benchmark-live-routing.svg': chart_live_routing(data('routing-live.json')),
        'benchmark-pass-rates.svg': chart_pass_rates(data('coding-test.json'), data('humaneval.json')),
        'benchmark-checking.svg': chart_checking(data('coding-test.json')),
        'benchmark-effort.svg': chart_effort(data('coding-test.json')),
    }
    for name, svg in jobs.items():
        if svg:
            (args.out / name).write_text(svg, encoding='utf-8', newline='\n')
            print('wrote', name)
        else:
            print('skipped', name, '(no data)')
    if args.readme:
        print('README results block', 'updated' if inject_results(args.readme, results_markdown(args.results)) else 'unchanged')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
