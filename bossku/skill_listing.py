"""How big the skill list is that Claude Code shows the model, and the setting that limits it.

Facts, checked against Claude Code 2.1.293 on 2026-10-10:
- The list holds name + description + when_to_use per skill. It is capped at skillListingBudgetFraction x the context
  window (settings.json, default 0.01), which is about 3 characters per token. Over budget, Claude Code keeps every
  name and drops descriptions, least-used skills first, and logs to --debug:
  "Skill listing over budget: <N> skills, <C> chars > <B> budget".
  https://code.claude.com/docs/en/skills.md#skill-descriptions-are-cut-short
  https://code.claude.com/docs/en/settings-reference.md#skilllistingbudgetfraction
- Measured at 0.01: 30,000 characters on a 1M-context model, 6,000 on a 200K-context model.
- description + when_to_use of one skill is cut at skillListingMaxDescChars (default 1536). A skill with
  disable-model-invocation is not listed.
- The SKILL.md files are not the whole list. On the same machine Claude Code logged 98,037 characters for 267 skills,
  while the 238 SKILL.md files in ~/.claude/skills estimate to 81,157 (no plugin enabled, no ~/.claude/commands, no
  project skills). The difference, 98,037 - 81,157 = 16,880 characters, is entries bossku cannot see (most likely
  Claude Code's bundled skills) plus format overhead. 0.035 (105,000 characters on 1M) cleared the warning there;
  sizing from the files alone gives 0.03 (90,000), which still cuts descriptions. UNSEEN_CHARS adds that difference
  to the 1M check and to the fit.

No skill is shortened, hidden or removed here to fit. The fix is the budget setting, and it costs context (the whole
list goes into every session), so `bossku install --fit-skill-list` is opt-in.
"""
from __future__ import annotations

import math
import os
from pathlib import Path

from bossku.hooks import _backup, _read_json, _write_json_atomic
from bossku.paths import claude_skills_dir
from bossku.skills import _parse_frontmatter

BUDGET_KEY = "skillListingBudgetFraction"
MAX_DESC_KEY = "skillListingMaxDescChars"
USER_FILE = "~/.claude/settings.json"
DEFAULT_FRACTION = 0.01
DEFAULT_MAX_DESC = 1536
CHARS_PER_TOKEN = 3
FIT_TOKENS = 1_000_000                              # the context window --fit-skill-list sizes the budget for
CONTEXTS = (("1M", FIT_TOKENS), ("200K", 200_000))  # label, context window in tokens
STEP = 0.005                                        # the fraction a fit is rounded up to
# ponytail: Claude Code does not document how it formats one entry; "- name: " plus a newline is five characters
# around the name. The total is an estimate for the SKILL.md files only (plugin and bundled skills also count).
ENTRY_OVERHEAD = 5
# ponytail: one measurement (Claude Code 2.1.293, no plugins), see the docstring. It is a flat number; a machine with
# plugin skills needs more, and the doctor line says so. It is applied to the 1M check only, because that is the one
# --fit-skill-list acts on; the 200K line counts just the SKILL.md files, so a small profile is not flagged for
# entries nobody can see.
UNSEEN_CHARS = 16_880


def _number(value) -> float | None:
    """A positive number from settings.json, or None (a bool or a string is not one)."""
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0 else None


def _fraction(value) -> float | None:
    """skillListingBudgetFraction as the settings reference allows it: above 0 and at most 1, or None."""
    number = _number(value)
    return number if number is not None and number <= 1 else None


def _cap(value) -> int | None:
    """skillListingMaxDescChars as the settings reference allows it: a whole number of 1 or more, or None."""
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 1 else None


def budget_chars(fraction: float, context_tokens: int) -> int:
    return round(fraction * context_tokens * CHARS_PER_TOKEN)


def fraction_that_fits(chars: int, context_tokens: int = FIT_TOKENS) -> float:
    """The smallest multiple of 0.005 whose budget on that context window holds `chars`."""
    step_chars = round(STEP * context_tokens * CHARS_PER_TOKEN)
    return round(max(1, math.ceil(chars / step_chars)) * STEP, 3)


def _read_file(path: Path) -> dict:
    try:
        data = _read_json(path)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def read_settings(home: Path) -> dict:
    return _read_file(home / ".claude" / "settings.json")


def _layers(home: Path, project: Path | None) -> list[tuple[str, dict]]:
    """(name, settings) for the files that can hold the two keys, highest precedence first. Both keys are scope "Any
    file" (https://code.claude.com/docs/en/settings-reference.md#skilllistingbudgetfraction) and project local beats
    project beats user (https://code.claude.com/docs/en/settings.md#settings-precedence). Managed settings and
    --settings rank higher still; bossku cannot see them."""
    layers = []
    if project is not None:
        folder = project.resolve() / ".claude"
        layers = [(f"the project's .claude/{name}", _read_file(folder / name))
                  for name in ("settings.local.json", "settings.json")]
    return layers + [(USER_FILE, read_settings(home))]


def _setting(key: str, layers: list[tuple[str, dict]], valid) -> tuple[float | None, str]:
    """The first valid value for `key` and the file it came from (the user file when none sets it)."""
    for name, settings in layers:
        value = valid(settings.get(key))
        if value is not None:
            return value, name
    return None, USER_FILE


def _entries(folder: Path, cap: int) -> dict[str, tuple[int, int]]:
    """name -> (characters taken by the name, characters of its description + when_to_use), for each listed skill."""
    found: dict[str, tuple[int, int]] = {}
    for child in sorted(folder.iterdir()) if folder.is_dir() else []:
        try:
            front = _parse_frontmatter((child / "SKILL.md").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if str(front.get("disable-model-invocation", "")).lower() == "true":
            continue
        name = str(front.get("name") or child.name)
        text = " ".join(str(front[key]) for key in ("description", "when_to_use") if front.get(key))
        found[name] = (len(name) + ENTRY_OVERHEAD, min(len(text), cap))
    return found


def _cut(entries: dict[str, tuple[int, int]], total: int, budget: int) -> int:
    """About how many descriptions go when the list is over budget. Claude Code drops those of the least-used skills
    first and nothing here knows which skills those are, so this counts at the average description size."""
    sizes = [size for _, size in entries.values() if size]
    if total <= budget or not sizes:
        return 0
    return min(len(sizes), math.ceil((total - budget) / (sum(sizes) / len(sizes))))


def estimate(home: Path | None = None, project: Path | None = None) -> dict:
    """The size of the list from every SKILL.md in ~/.claude/skills (and the project's .claude/skills), against the
    budget saved in ~/.claude/settings.json (or, with a project, the project's settings files that override it).
    Read-only."""
    h = home if home is not None else Path.home()
    layers = _layers(h, project)
    cap = _setting(MAX_DESC_KEY, layers, _cap)[0] or DEFAULT_MAX_DESC
    saved, fraction_file = _setting(BUDGET_KEY, layers, _fraction)
    fraction = saved or DEFAULT_FRACTION
    entries = _entries(claude_skills_dir(h), cap)
    if project is not None:
        entries.update(_entries(project.resolve() / ".claude" / "skills", cap))   # a project skill replaces a same-named one
    total = sum(name + size for name, size in entries.values())
    whole = total + UNSEEN_CHARS                    # the SKILL.md files plus the entries bossku cannot see
    models = {}
    for label, tokens in CONTEXTS:
        budget = budget_chars(fraction, tokens)
        size = whole if tokens == FIT_TOKENS else total
        models[label] = {"budget": budget, "fits": size <= budget, "cut": _cut(entries, size, budget)}
    return {"skills": len(entries), "chars": total, "tokens": total // CHARS_PER_TOKEN, "fraction": fraction,
            "fraction_is_default": saved is None, "fraction_file": fraction_file, "max_desc_chars": cap,
            "whole_tokens": whole // CHARS_PER_TOKEN, "models": models, "fit_fraction": fraction_that_fits(whole)}


def fit_settings(home: Path) -> dict:
    """Set skillListingBudgetFraction in ~/.claude/settings.json to the fraction that holds the whole list on a
    1M-context model. Never lowers a value that is already higher (or the default 0.01); every other key stays."""
    path = home / ".claude" / "settings.json"
    if not path.parent.is_dir():
        return {"status": "skipped_not_found", "path": str(path)}
    try:
        data = _read_json(path)
    except (OSError, ValueError):
        data = None
    if not isinstance(data, dict):
        return {"status": "skipped_invalid_json", "path": str(path)}
    if BUDGET_KEY in data and _fraction(data[BUDGET_KEY]) is None:
        return {"status": "skipped_invalid_value", "path": str(path), "value": data[BUDGET_KEY]}
    found = estimate(home)
    if not found["skills"]:
        return {"status": "skipped_no_skills", "path": str(path)}
    was = data.get(BUDGET_KEY)                 # None: not in the file, so Claude Code uses 0.01
    have = DEFAULT_FRACTION if was is None else was
    if found["fit_fraction"] <= have:
        return {"status": "already_fits", "path": str(path), "fraction": have, "needed": found["fit_fraction"]}
    if path.exists() and not os.access(path, os.W_OK):   # a file the user made read-only stays as it is, with no backup
        return {"status": "failed", "path": str(path), "error": f"{path} is read-only; make it writable and run again"}
    data[BUDGET_KEY] = found["fit_fraction"]
    try:                                       # the install has already finished; a locked file is a status, not a crash
        _backup(path)
        _write_json_atomic(path, data)
    except OSError as exc:
        return {"status": "failed", "path": str(path), "error": str(exc)}
    return {"status": "set", "path": str(path), "fraction": found["fit_fraction"], "was": was}
