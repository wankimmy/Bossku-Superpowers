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
    'keyword': ('Without BosskuAI (keyword search)', '#2a78d6', '#3987e5'),
    'after': ('With BosskuAI', '#1baf7a', '#199e70'),
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
# The README shows two setups only: without BosskuAI and with it. Other versions stay in the raw data for
# maintainers and are never drawn.

ARMS = ('baseline', 'after')


def load(results: Path, name: str) -> dict:
    path = results / name
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}


def table(head: list[str], rows: list[list[str]]) -> str:
    lines = ['| ' + ' | '.join(head) + ' |', '|' + '---|' + '---:|' * (len(head) - 1)]
    lines += ['| ' + ' | '.join(row) + ' |' for row in rows]
    return '\n'.join(lines)


def complete_models(data: dict) -> list[tuple[str, dict]]:
    """(model, arms) for every model that has both setups."""
    return [(model, block['arms']) for model, block in (data.get('models') or {}).items()
            if all(a in block['arms'] for a in ARMS)]


def window_label(window: int | None) -> str:
    if not window:
        return ''
    return f'{window // 1_000_000}M-token window' if window >= 1_000_000 else f'{window // 1000}k-token window'


def chart_session_overhead(data: dict) -> str | None:
    """The first call of a Claude Code session, with and without BosskuAI, per Claude model."""
    models = [(m, arms) for m, arms in (data or {}).items() if all(a in arms for a in ARMS)]
    if not models:
        return None
    tokens, dollars = [], []
    for model, arms in models:
        sub = window_label(arms['baseline'].get('context_window'))
        t = [arms[a]['input_tokens_median'] for a in ARMS]
        c = [arms[a]['cost_median'] for a in ARMS]
        tokens.append(Group(model_name(model), t, sub, tips=[f'{t[0]:,.0f}', f'{t[1]:,.0f}  (+{t[1] - t[0]:,.0f})']))
        dollars.append(Group(model_name(model), c, sub, tips=[f'${c[0]:.4f}', f'${c[1]:.4f}  (+${c[1] - c[0]:.4f})']))
    return Figure('What BosskuAI adds to every session',
                  'First call of a Claude Code session, with and without BosskuAI (median of 3 runs)',
                  list(ARMS),
                  [Panel('Input tokens of the first call', tokens, fmt=lambda v: f'{v:,.0f}'),
                   Panel('Cost of the first call', dollars, fmt=lambda v: f'${v:.3f}')],
                  footnote="A one-word prompt after a cache warm-up. Cost is Claude Code's own list-price figure.").render()


def chart_routing(data: dict) -> str | None:
    """Held-out skill search: prompts the router was never tuned on."""
    split = (data.get('splits') or {}).get('test')
    if not split or 'description-only' not in split or 'after' not in split:
        return None
    groups = []
    for label, key in (('Right skill ranked first', 'top1'), ('Right skill in the top three', 'top3')):
        groups.append(Group(label, [split[a][key]['rate'] * 100 for a in ('description-only', 'after')],
                            ci=[tuple(100 * c for c in split[a][key]['ci']) for a in ('description-only', 'after')]))
    after = split['after']
    coverage = [Group('Parts of a request covered', [None, after['concern_coverage'] * 100]),
                Group('Whole request covered', [None, after['all_concerns_covered']['rate'] * 100])]
    return Figure('Finding the right skill on new prompts',
                  f'{after["prompts"]} held-out requests written without seeing the router (never used for tuning)',
                  ['keyword', 'after'],
                  [Panel('Ranking', groups, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100]),
                   Panel('Requests with several jobs', coverage, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100,
                         ticks=[0, 25, 50, 75, 100])],
                  footnote='Whiskers show a 95% interval. Plain keyword search only ranks, so it has no coverage bars.').render()


def chart_pass_rates(coding: dict, humaneval: dict) -> str | None:
    panels = []
    for title, data in (('Hidden-test coding tasks', coding), ('HumanEval problems', humaneval)):
        groups = []
        for model, arms in complete_models(data):
            groups.append(Group(model_name(model), [arms[a]['pass_rate'] * 100 for a in ARMS],
                                f'{arms["baseline"]["runs"]} runs per setup',
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
                  footnote='Read from the tool calls alone, the same way for both setups.').render()


def tokens_per_run(summary: dict) -> float:
    return summary['input_tokens_mean'] + summary['output_tokens_mean']


def chart_effort(coding: dict) -> str | None:
    tokens, solved = [], []
    for model, arms in complete_models(coding):
        per_run = [tokens_per_run(arms[a]) / 1000 for a in ARMS]
        tokens.append(Group(model_name(model), per_run, tips=[f'{v:,.0f}k' for v in per_run]))
        per_solved = [tokens_per_run(arms[a]) / 1000 / arms[a]['pass_rate'] if arms[a]['pass_rate'] else None for a in ARMS]
        solved.append(Group(model_name(model), per_solved, tips=[f'{v:,.0f}k' if v else 'none solved' for v in per_solved]))
    if not tokens:
        return None
    return Figure('What a task costs in tokens', 'Input plus output tokens the model processed, all turns (lower is better)',
                  list(ARMS),
                  [Panel('Tokens per run (thousands)', tokens, fmt=lambda v: f'{v:,.0f}', unit='k'),
                   Panel('Tokens per solved task (thousands)', solved, fmt=lambda v: f'{v:,.0f}', unit='k')],
                  footnote='Input counts every turn, cached or not. Ollama Cloud bills by subscription, so tokens are the honest unit.').render()


def chart_memory(memory: dict) -> str | None:
    """Tasks where a rule is stated in one session and matters in the next."""
    groups = []
    for model, arms in complete_models(memory):
        groups.append(Group(model_name(model), [arms[a]['pass_rate'] * 100 for a in ARMS],
                            f'{arms["baseline"]["runs"]} runs per setup',
                            ci=[tuple(100 * c for c in arms[a]['pass_ci']) for a in ARMS]))
    if not groups:
        return None
    return Figure('Remembering a rule from an earlier session',
                  'Session 1 states a project rule. Session 2 asks for something that breaks it unless the agent remembers.',
                  list(ARMS), [Panel('', groups, fmt=lambda v: f'{v:.0f}', unit='%', axis_max=100, ticks=[0, 25, 50, 75, 100])],
                  footnote='A fresh conversation each time: the agent only has the files and whatever notes were saved.').render()


# ---------------------------------------------------------------------------------------- the words
# Every sentence below is built from the saved result files, so the explanation under a chart can never
# disagree with the chart.

def pct(value: float) -> str:
    return f'{100 * value:.0f}%'


def points(value: float) -> str:
    rounded = round(100 * value)
    return '0' if rounded == 0 else f'{rounded:+d}'


def times(value: float) -> str:
    return f'{value:.1f}×' if value < 10 else f'{value:.0f}×'


def pass_bullet(model: str, block: dict, unit: str) -> str:
    arms = block['arms']
    without, with_ = arms['baseline'], arms['after']
    diff = (block.get('paired') or {}).get('after', {}).get('passed') or {}
    name = model_name(model)
    head = f'{pct(with_["pass_rate"])} with BosskuAI against {pct(without["pass_rate"])} without ({without["runs"]} runs each)'
    slow = ''
    if with_.get('timeouts') or without.get('timeouts'):
        slow = (f' {with_.get("timeouts", 0)} of the {with_["runs"]} runs with BosskuAI ({without.get("timeouts", 0)} without) '
                f'ran out of time and count as failures.')
    if not diff.get('tasks'):
        return f'- **{name}:** {head}.{slow}'
    lo, hi = diff['ci']
    interval = f'{points(diff["mean_diff"])} points over the same {unit}, 95% interval {points(lo)} to {points(hi)}'
    if lo > 0:
        return f'- **{name} finished more {unit}.** {head}: {interval}.{slow}'
    if hi < 0:
        return f'- **{name} finished fewer {unit}.** {head}: {interval}.{slow}'
    ceiling = (' Both setups were already near the ceiling, so there was little room to improve.'
               if min(without['pass_rate'], with_['pass_rate']) >= 0.9 else '')
    return f'- **{name}: no clear difference.** {head}: {interval}.{ceiling}{slow}'


def summary_overhead(results: Path) -> str:
    data = load(results, 'overhead.json')
    sentences = []
    for model, arms in data.items():
        if not all(a in arms for a in ARMS):
            continue
        base, new = arms['baseline'], arms['after']
        extra = new['input_tokens_median'] - base['input_tokens_median']
        sentences.append(f'{model_name(model)} +{extra:,.0f} tokens ({extra / base["input_tokens_median"]:.0%} more), '
                         f'+${new["cost_median"] - base["cost_median"]:.4f}')
    if not sentences:
        return ''
    return ('**What this shows:** BosskuAI adds a small, fixed amount to the first call of a session: ' + '; '.join(sentences) +
            '. That is the skill list and the short instructions. The same text is reused on every later call, so it does '
            'not grow with the length of the session.')


def summary_routing(results: Path) -> str:
    split = (load(results, 'routing-heldout.json').get('splits') or {}).get('test') or {}
    if 'after' not in split or 'description-only' not in split:
        return ''
    after, keyword = split['after'], split['description-only']
    text = (f'**What this shows:** on {after["prompts"]} requests it was never tuned on, BosskuAI ranked an acceptable skill first '
            f'{pct(after["top1"]["rate"])} of the time, against {pct(keyword["top1"]["rate"])} for plain keyword search. '
            f'For requests with several jobs it found a fitting skill for every part {pct(after["all_concerns_covered"]["rate"])} '
            f'of the time.')
    for model, arms in load(results, 'routing-live.json').items():
        if 'after' in arms:
            text += (f' With a real agent ({model_name(model)}) on the same requests, an acceptable skill was actually opened '
                     f'for {pct(arms["after"]["rate"])} of them.')
            break
    return text


def summary_pass(results: Path) -> str:
    blocks = []
    for title, name, unit in (('Hidden-test coding tasks', 'coding-test.json', 'tasks'), ('HumanEval problems', 'humaneval.json', 'problems')):
        data = load(results, name)
        bullets = [pass_bullet(model, data['models'][model], unit) for model, _ in complete_models(data)]
        if bullets:
            blocks.append(f'**{title}**\n' + '\n'.join(bullets))
    return '\n\n'.join(blocks)


def summary_checking(results: Path) -> str:
    data = load(results, 'coding-test.json')
    bullets = []
    for model, arms in complete_models(data):
        without, with_ = arms['baseline'], arms['after']
        if without.get('unchecked_rate') is None or with_.get('unchecked_rate') is None:
            continue
        bullets.append(f'- **{model_name(model)}** ended without running its code in {pct(without["unchecked_rate"])} of the runs '
                       f'that changed code on its own, and in {pct(with_["unchecked_rate"])} with BosskuAI.')
    if not bullets:
        return ''
    return ('**What this shows:** the habit that BosskuAI\'s stop check is built to change. A model that never runs what it wrote '
            'cannot find its own mistakes.\n' + '\n'.join(bullets))


def summary_effort(results: Path) -> str:
    data = load(results, 'coding-test.json')
    bullets = []
    for model, arms in complete_models(data):
        without, with_ = arms['baseline'], arms['after']
        line = (f'- **{model_name(model)}** used {times(tokens_per_run(with_) / tokens_per_run(without))} the tokens per run '
                f'({tokens_per_run(without) / 1000:,.0f}k without, {tokens_per_run(with_) / 1000:,.0f}k with)')
        if without['pass_rate'] and with_['pass_rate']:
            per_solved = (tokens_per_run(with_) / with_['pass_rate']) / (tokens_per_run(without) / without['pass_rate'])
            line += f' and {times(per_solved)} the tokens per task it actually solved'
        bullets.append(line + '.')
    if not bullets:
        return ''
    return ('**What this shows:** BosskuAI makes the agent do more work, and work costs tokens. The extra work is running, '
            'checking and fixing. Where that turns failures into passes it is worth it; where the model already passes, it is not.\n'
            + '\n'.join(bullets))


def summary_overall(results: Path) -> str:
    coding = load(results, 'coding-test.json')
    bullets = []
    for model, arms in complete_models(coding):
        diff = (coding['models'][model].get('paired') or {}).get('after', {}).get('passed') or {}
        without, with_ = arms['baseline'], arms['after']
        if diff.get('tasks') and diff['ci'][0] > 0:
            bullets.append(f'- **{model_name(model)} finished more tasks with BosskuAI:** {pct(without["pass_rate"])} without, '
                           f'{pct(with_["pass_rate"])} with.')
        elif diff.get('tasks'):
            bullets.append(f'- **{model_name(model)} gained nothing it could measure:** {pct(without["pass_rate"])} without, '
                           f'{pct(with_["pass_rate"])} with.')
    split = (load(results, 'routing-heldout.json').get('splits') or {}).get('test') or {}
    if 'after' in split and 'description-only' in split:
        bullets.append(f'- **It finds the right skill more often:** {pct(split["after"]["top1"]["rate"])} first-pick accuracy on new '
                       f'requests, against {pct(split["description-only"]["top1"]["rate"])} for keyword search.')
    extras = []
    for model, arms in load(results, 'overhead.json').items():
        if all(a in arms for a in ARMS):
            extra = arms['after']['input_tokens_median'] - arms['baseline']['input_tokens_median']
            extras.append(f'{extra:,.0f} on {model_name(model)}')
    if extras:
        bullets.append('- **Its fixed cost is small:** extra tokens on the first call of a session: ' + ', '.join(extras) + '.')
    return '\n'.join(bullets)


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
            parts.append(table(['First call of a session', 'Without BosskuAI', 'With BosskuAI'], rows))
    split = (data('routing-heldout.json').get('splits') or {}).get('test') or {}
    if 'description-only' in split and 'after' in split:
        rows = [['Right skill ranked first'] + [pct(split[n]['top1']['rate']) for n in ('description-only', 'after')],
                ['Right skill in the top three'] + [pct(split[n]['top3']['rate']) for n in ('description-only', 'after')],
                ['Every part of a multi-part request covered', '-', pct(split['after']['all_concerns_covered']['rate'])]]
        for model, arms in data('routing-live.json').items():
            if 'after' in arms:
                rows.append([f'A real agent ({model_name(model)}) opens an acceptable skill', '-', pct(arms['after']['rate'])])
                break
        parts.append(table([f'Finding a skill ({split["after"]["prompts"]} new requests)', 'Keyword search only', 'With BosskuAI'], rows))
    for title, name in (('Hidden-test coding tasks', 'coding-test.json'), ('HumanEval problems', 'humaneval.json'),
                        ('Remembering a rule from an earlier session', 'memory.json')):
        rows = []
        for model, arms in complete_models(data(name)):
            runs = arms['baseline']['runs']
            rows.append([f'{model_name(model)}: tasks passed ({runs} runs each)'] + [
                f'{pct(arms[a]["pass_rate"])} ({arms[a]["passed"]}/{arms[a]["runs"]})' for a in ARMS])
            rows.append([f'{model_name(model)}: tokens per run'] + [f'{tokens_per_run(arms[a]) / 1000:,.0f}k' for a in ARMS])
            if all(arms[a].get('unchecked_rate') is not None for a in ARMS) and name == 'coding-test.json':
                rows.append([f'{model_name(model)}: ended without running its code'] + [pct(arms[a]['unchecked_rate']) for a in ARMS])
        if rows:
            parts.append(table([title, 'Without BosskuAI', 'With BosskuAI'], rows))
    return '\n\n'.join(parts)


# --------------------------------------------------------------------------------------- the README
# Blocks in the README that are rewritten from the data: <!-- NAME:start --> ... <!-- NAME:end -->

def summary_memory(results: Path) -> str:
    data = load(results, 'memory.json')
    bullets = []
    for model, _ in complete_models(data):
        block = data['models'][model]
        bullets.append(pass_bullet(model, block, 'tasks'))
        saved = block['arms']['after'].get('saved_a_note_rate')
        if saved is not None:
            bullets[-1] += f' In the first session, the agent with BosskuAI saved the rule as a note {pct(saved)} of the time.'
    if not bullets:
        return ''
    return ('**What this shows:** each task states a project rule in a first session (for example "this must run on Python 3.8" '
            'or "never use eval") and asks for related work in a second one that would break the rule if forgotten. The agent '
            'starts the second session fresh: without BosskuAI it has only the files; with BosskuAI it also sees the notes it saved.\n'
            + '\n'.join(bullets))


def block_text(results: Path) -> dict[str, str]:
    return {'results': results_markdown(results), 'summary-overall': summary_overall(results),
            'summary-overhead': summary_overhead(results), 'summary-routing': summary_routing(results),
            'summary-pass': summary_pass(results), 'summary-checking': summary_checking(results),
            'summary-effort': summary_effort(results), 'summary-memory': summary_memory(results)}


def marker(name: str, edge: str) -> str:
    return f'<!-- {name}:{edge} -->'


def inject_block(text: str, name: str, block: str) -> str:
    start, end = marker(name, 'start'), marker(name, 'end')
    if start not in text or end not in text:
        return text
    head, rest = text.split(start, 1)
    tail = rest.split(end, 1)[1]
    return f'{head}{start}\n{block}\n{end}{tail}' if block else f'{head}{start}\n{end}{tail}'


def inject_all(readme: Path, blocks: dict[str, str]) -> bool:
    text = readme.read_text(encoding='utf-8').replace('\r\n', '\n')
    new = text
    for name, block in blocks.items():
        new = inject_block(new, name, block)
    if marker('results', 'start') not in new:
        raise SystemExit(f'{readme} has no {marker("results", "start")} block')
    if new == text:
        return False
    readme.write_text(new, encoding='utf-8', newline='\n')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--results', type=Path, default=RESULTS)
    parser.add_argument('--out', type=Path, default=ASSETS)
    parser.add_argument('--readme', type=Path, help='rewrite the tables and summaries marked with <!-- name:start --> ... <!-- name:end -->')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    data = lambda name: load(args.results, name)  # noqa: E731
    jobs = {
        'benchmark-session-overhead.svg': chart_session_overhead(data('overhead.json')),
        'benchmark-routing.svg': chart_routing(data('routing-heldout.json')),
        'benchmark-pass-rates.svg': chart_pass_rates(data('coding-test.json'), data('humaneval.json')),
        'benchmark-checking.svg': chart_checking(data('coding-test.json')),
        'benchmark-effort.svg': chart_effort(data('coding-test.json')),
        'benchmark-memory.svg': chart_memory(data('memory.json')),
    }
    for name, svg in jobs.items():
        if svg:
            (args.out / name).write_text(svg, encoding='utf-8', newline='\n')
            print('wrote', name)
        else:
            print('skipped', name, '(no data)')
    if args.readme:
        print('README tables and summaries', 'updated' if inject_all(args.readme, block_text(args.results)) else 'unchanged')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
