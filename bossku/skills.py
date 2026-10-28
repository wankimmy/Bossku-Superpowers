from __future__ import annotations

import json
import math
import os
import re
import shutil
import stat
import sys
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote

from bossku.paths import (
    COFOUNDER_SKILL,
    MANAGED_SKILL_PREFIX,
    agents_skills_dir,
    claude_skills_dir,
    library_dir,
    repo_root,
)


@dataclass
class SkillMeta:
    skill_id: str
    name: str
    description: str
    triggers: list[str]
    keywords: list[str]
    path: Path


def aliases_path(root: Path | None = None) -> Path:
    return repo_root(root) / "skills" / "aliases.json"


def vendored_path(root: Path | None = None) -> Path:
    return repo_root(root) / "skills" / "vendored.json"


def load_vendored(root: Path | None = None) -> dict[str, str]:
    path = vendored_path(root)
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    skills = data.get("skills", {})
    return {str(k): str(v) for k, v in skills.items()}


def load_vendored_ids(root: Path | None = None) -> set[str]:
    return set(load_vendored(root).keys())


def load_excluded_vendored(root: Path | None = None) -> set[str]:
    """Upstream skills deliberately not vendored; recorded so a re-vendor leaves them out."""
    path = vendored_path(root)
    if not path.is_file():
        return set()
    return set(json.loads(path.read_text(encoding="utf-8")).get("excluded", {}))


# Never installed or hinted, even if a re-vendor brings it back: x402 prints generated wallet keys and spends
# from a crypto wallet. It is listed under `excluded` in skills/vendored.json, so the repo no longer ships it.
NOT_INSTALLED = frozenset({"x402"})


DEFAULT_REVIEW_DAYS = 180


def load_provenance(root: Path | None = None) -> tuple[dict[str, dict], int]:
    path = vendored_path(root)
    if not path.is_file():
        return {}, DEFAULT_REVIEW_DAYS
    data = json.loads(path.read_text(encoding="utf-8"))
    review_days = int(data.get("review_days", DEFAULT_REVIEW_DAYS))
    return data.get("provenance", {}), review_days


def pack_stocktake(root: Path | None = None, today: date | None = None) -> list[dict]:
    """Age each vendored pack against the review window.

    `last_synced` is a recorded date, not an upstream check: this reports that a pack
    is due for review, never that upstream actually changed.
    """
    path = vendored_path(root)
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    provenance, review_days = load_provenance(root)
    now = today or date.today()

    rows: list[dict] = []
    for pack, ids in data.get("packs", {}).items():
        meta = provenance.get(pack, {})
        synced_raw = meta.get("last_synced")
        try:
            synced = date.fromisoformat(synced_raw) if synced_raw else None
        except ValueError:
            synced = None
        age = (now - synced).days if synced else None
        rows.append(
            {
                "pack": pack,
                "kind": "vendored",
                "skills": len(ids),
                "upstream": meta.get("upstream", ""),
                "last_synced": synced_raw or "",
                "age_days": age,
                "review_days": review_days,
                # An unrecorded sync date is treated as due: silence should not read as fresh.
                "overdue": age is None or age > review_days,
            }
        )
    for group, meta in data.get("adapted", {}).items():
        synced_raw = meta.get("last_synced")
        try:
            synced = date.fromisoformat(synced_raw) if synced_raw else None
        except ValueError:
            synced = None
        age = (now - synced).days if synced else None
        rows.append(
            {
                "pack": group,
                "kind": "adapted",
                "skills": len(adapted_skill_ids(meta, root)),
                "upstream": meta.get("upstream", ""),
                "last_synced": synced_raw or "",
                "age_days": age,
                "review_days": review_days,
                "overdue": age is None or age > review_days,
            }
        )
    rows.sort(key=lambda r: (-1 if r["age_days"] is None else -r["age_days"]))
    return rows


def adapted_skill_ids(meta: dict, root: Path | None = None) -> list[str]:
    """Skills that hold text adapted from one upstream: a fixed list, the SOURCE.json files that name the upstream
    (a wrapper's own, or one under a skill's references/), or the skills whose SKILL.md carries the attribution marker.

    These are first-party skills, so a re-vendor never refreshes them; the stocktake ages them like a pack.
    """
    if "skills" in meta:
        return [sid for sid in meta["skills"] if (skill_folder(sid, root) / "SKILL.md").is_file()]
    found: set[str] = set()
    folders = skill_folders(root)
    if meta.get("source_json"):
        upstream = meta.get("upstream", "")
        for base in folders:
            for source in [*base.glob("*/SOURCE.json"), *base.glob("*/references/*/SOURCE.json")]:
                try:
                    if json.loads(source.read_text(encoding="utf-8")).get("upstream") == upstream:
                        found.add(source.relative_to(base).parts[0])
                except (OSError, ValueError):
                    continue
    marker = meta.get("marker")
    if marker:
        for skill_md in (md for base in folders for md in base.glob("*/SKILL.md")):
            try:
                if marker in skill_md.read_text(encoding="utf-8"):
                    found.add(skill_md.parent.name)
            except OSError:
                continue
    return sorted(found)


def overdue_packs(root: Path | None = None, today: date | None = None) -> list[str]:
    return [r["pack"] for r in pack_stocktake(root, today) if r["overdue"]]


def load_pack_skill_ids(pack_name: str, root: Path | None = None) -> list[str]:
    path = vendored_path(root)
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    packs = data.get("packs", {})
    raw = packs.get(pack_name, [])
    return [str(sid) for sid in raw]


def load_aliases(root: Path | None = None) -> dict[str, str]:
    path = aliases_path(root)
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in data.get("aliases", {}).items()}


def skills_dir(root: Path | None = None) -> Path:
    r = repo_root(root)
    if (r / "skills").is_dir():
        return r / "skills"
    legacy = r / "ai-assistant" / "skills"
    if legacy.is_dir():
        return legacy
    raise FileNotFoundError("skills directory not found")


# Library-only skills live in library/, next to skills/. Plugin manifests (Claude Code, Cursor, Codex) list every
# folder in skills/, so the niche long tail stays out of their skill lists; profiles, the hint, `bossku skills find`
# and `show` reach both folders through skill_folder().
LIBRARY_SKILLS_DIR = "library"


def skill_folders(root: Path | None = None) -> list[Path]:
    """The repo folders that hold skill folders: skills/ (what plugins and profiles list), then library/."""
    base = skills_dir(root)
    library = base.parent / LIBRARY_SKILLS_DIR
    return [base, library] if library.is_dir() else [base]


def skill_folder(sid: str, root: Path | None = None) -> Path:
    """A skill's folder in the repo: skills/<id>, or library/<id> for a library-only skill (skills/<id> if neither)."""
    base = skills_dir(root)
    listed = base / sid
    if listed.is_dir():
        return listed
    library = base.parent / LIBRARY_SKILLS_DIR / sid
    return library if library.is_dir() else listed


def list_skill_ids(root: Path | None = None) -> list[str]:
    aliases = set(load_aliases(root).keys())
    ids: set[str] = set()
    for base in skill_folders(root):
        for child in base.iterdir():
            if not child.is_dir():
                continue
            if not (child / "SKILL.md").is_file():
                continue
            if child.name in aliases:
                continue
            ids.add(child.name)
    return sorted(ids)


def parse_skill_md(path: Path) -> SkillMeta:
    text = path.read_text(encoding="utf-8")
    front = _parse_frontmatter(text)
    skill_id = path.parent.name
    triggers = front.get("triggers", [])
    keywords = front.get("keywords", [])
    if isinstance(triggers, str):
        triggers = [triggers]
    if isinstance(keywords, str):
        keywords = [keywords]
    return SkillMeta(
        skill_id=skill_id,
        name=str(front.get("name", skill_id)),
        description=str(front.get("description", "")),
        triggers=[str(t) for t in triggers],
        keywords=[str(k) for k in keywords],
        path=path.parent,
    )


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    # Close on a line that is exactly `---`; a bare find() would stop at any `---`
    # inside a description and silently truncate the frontmatter.
    match = re.search(r"^---[ \t]*$", text[3:], re.MULTILINE)
    if match is None:
        return {}
    block = text[3 : 3 + match.start()].strip()
    out: dict[str, object] = {}
    key: str | None = None
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("- ") and key:
            items = out.setdefault(key, [])
            if isinstance(items, list):
                items.append(stripped[2:].strip())
            i += 1
            continue
        if ":" in line and (not line or not line[0].isspace()):
            key_part, val = line.split(":", 1)
            key = key_part.strip()
            val = val.strip()
            # Block scalars carry optional chomping/indent indicators (`>-`, `|+`, `>2`).
            # Matching only bare `>`/`|` turned `description: >-` into the string ">-".
            if re.fullmatch(r"[>|][-+]?\d?", val):
                folded = val.startswith(">")
                i += 1
                parts: list[str] = []
                while i < len(lines):
                    nxt = lines[i]
                    if nxt.strip() == "":
                        if not folded:
                            parts.append("")
                        i += 1
                        continue
                    if not nxt[0].isspace():
                        head = nxt.split(":", 1)[0].strip()
                        if head and re.match(r"^[A-Za-z0-9_-]+$", head):
                            break
                    parts.append(nxt.strip())
                    i += 1
                out[key] = (" ".join(parts) if folded else "\n".join(parts)).strip()
                continue
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                out[key] = [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
            else:
                out[key] = _unquote_scalar(val)
            i += 1
            continue
        i += 1
    return out


def _unquote_scalar(val: str) -> str:
    """Read a YAML scalar the way hosts do, so the index sees the same description.

    Stripping quote characters left `\\"` escapes behind, which garbled every
    phrase derived from a double-quoted description that quotes its triggers.
    """
    if len(val) >= 2 and val[0] == val[-1] == '"':
        return re.sub(r'\\(["\\])', r"\1", val[1:-1])
    if len(val) >= 2 and val[0] == val[-1] == "'":
        return val[1:-1].replace("''", "'")
    return val


def resolve_skill_id(skill_id: str, root: Path | None = None, aliases: dict[str, str] | None = None) -> str:
    aliases = load_aliases(root) if aliases is None else aliases
    seen: set[str] = set()
    current = skill_id
    while current in aliases:
        if current in seen:
            break
        seen.add(current)
        current = aliases[current]
    return current


def rank_skills(task: str, root: Path | None = None, limit: int = 5, data: dict | None = None) -> list[tuple[str, float]]:
    """Rank skills for a task, best first. Uses skills/skill-index.json when present.

    `data` is a routing index the caller already holds; passing it spares a re-hash of every SKILL.md.
    """
    from bossku.index import compute_idf, routing_context, tokenize, variants

    data = _routing_index(root) if data is None else data
    entries: dict[str, dict] = data.get("skills", {})
    if not entries:
        return []

    task = routing_context(task)
    idf = compute_idf(entries)
    task_l = " " + re.sub(r"\s+", " ", task.lower().strip()) + " "

    # Weight each query term by rarity, and remember its morphological variants once.
    default_idf = max(idf.values(), default=1.0)
    q_terms: dict[str, tuple[float, set[str]]] = {}
    for token in tokenize(task):
        if token not in q_terms:
            q_terms[token] = (idf.get(token, default_idf), variants(token))
    q_mass = sum(w for w, _ in q_terms.values()) or 1.0

    request_fit = _request_fit(task, entries, data.get("fingerprint", ""))
    scored: list[tuple[str, float]] = []
    for sid, entry in entries.items():
        if sid in NOT_INSTALLED:
            continue
        fit = REQUEST_FIT_WEIGHT * request_fit.get(sid, 0.0) * (LIBRARY_FIT_SHARE if entry.get("library") else 1.0)
        scored.append((sid, _score_entry(sid, entry, task_l, q_terms, q_mass) + fit))
    scored.sort(key=lambda pair: (-pair[1], pair[0]))
    return scored[:limit]


# How strongly the vocabulary of real requests counts next to the skill's own words (tuned on the dev halves of two
# prompt sets, reported on the test halves).
REQUEST_FIT_WEIGHT = 5.0
# Library-only skills are many and niche, and their example prompts share everyday words with listed skills. Their fit
# is scored against the listed skills' statistics (see _request_model) and counts three quarters: on the dev halves the
# right library skill was named for 19% of held-back library prompts (4% without examples) while 4 held-out prompts
# went to a library skill (18 at full weight).
LIBRARY_FIT_SHARE = 0.75
_BM25_K1, _BM25_B = 1.2, 0.75
_request_models: dict[str, tuple] = {}
_COUNT = re.compile(r":(\d+)")


def _request_model(entries: dict[str, dict], key: str) -> tuple:
    """(' word:count ...' text per skill, length per skill, average listed length, library ids, postings per word).

    The text stays as the index stores it; a request only looks up its own few words (see _request_fit),
    so a hook process, which runs once per prompt, never parses the other ~8,000.
    """
    if key and key in _request_models:
        return _request_models[key]
    texts = {sid: f" {entry['qterms']} " for sid, entry in entries.items() if entry.get("qterms")}
    lengths = {sid: sum(map(int, _COUNT.findall(text))) for sid, text in texts.items()}
    # Statistics come from the listed skills only, so adding library examples never moves a listed skill's fit.
    library = frozenset(sid for sid in texts if entries[sid].get("library"))
    listed = [length for sid, length in lengths.items() if sid not in library] or list(lengths.values())
    average = sum(listed) / max(len(listed), 1)
    model = (texts, lengths, average, library, {})
    if key:
        _request_models[key] = model
    return model


def _request_fit(task: str, entries: dict[str, dict], key: str) -> dict[str, float]:
    """0..1 per skill: how well the words of the request match the words people use when they need that skill (BM25)."""
    from bossku.index import singular, tokenize

    texts, lengths, average, library, postings = _request_model(entries, key)
    if not texts:
        return {}
    documents = len(texts) - len(library) or len(texts)
    words = list(dict.fromkeys(singular(t) for t in tokenize(task)))
    for w in words:
        if w not in postings:
            needle = f" {w}:"
            hits: dict[str, int] = {}
            for sid, text in texts.items():
                at = text.find(needle)
                if at >= 0:
                    start = at + len(needle)
                    hits[sid] = int(text[start:text.index(" ", start)])
            frequency = sum(1 for sid in hits if sid not in library)
            idf = math.log(1 + (documents - frequency + 0.5) / (frequency + 0.5)) if hits else 0.0
            postings[w] = (hits, idf)
    norm = sum(postings[w][1] for w in words) * (_BM25_K1 + 1) or 1.0
    fit: dict[str, float] = {}
    for w in words:
        hits, idf = postings[w]
        for sid, f in hits.items():
            fit[sid] = fit.get(sid, 0.0) + idf * f * (_BM25_K1 + 1) / (f + _BM25_K1 * (1 - _BM25_B + _BM25_B * lengths[sid] / average))
    fit = {sid: total / norm for sid, total in fit.items() if total}
    best = max((value for sid, value in fit.items() if sid not in library), default=0.0) or max(fit.values(), default=0.0)
    # Scale to the best listed fit (a library skill is capped at it); task evidence still decides eligibility.
    return {sid: min(value / best, 1.0) for sid, value in fit.items()} if best else fit


def find_skill(task: str, root: Path | None = None, data: dict | None = None) -> tuple[str, float]:
    aliases = load_aliases(root)
    task_l = task.lower()
    data = _routing_index(root) if data is None else data
    known = set((data or {}).get("skills", {})) or set(list_skill_ids(root))

    for alias, target in aliases.items():
        if alias.replace("bosskuai-", "").replace("-", " ") in task_l and target in known:
            return target, 1.5

    ranked = rank_skills(task, root, limit=1, data=data)
    fallback = COFOUNDER_SKILL
    if not ranked or ranked[0][1] <= 0:
        return fallback, 0.0
    return resolve_skill_id(ranked[0][0], root, aliases), round(ranked[0][1], 3)


def recommend_skill_stack(
    task: str,
    root: Path | None = None,
    limit: int = 5,
) -> list[tuple[str, float]]:
    """Return a bounded stack; detailed reasons are available from select_skill_stack."""
    result = select_skill_stack(task, root, limit)
    return [(row["skill_id"], row["score"]) for row in result["selected"]]


DIRECTION_SKILLS = frozenset(
    {"bosskuai-taste", "taste-skill", "hallmark", "soft-skill", "minimalist-skill", "brutalist-skill"}
)

# Alternatives for the same job. Domain specialists and process skills can coexist.
ALTERNATIVE_SKILLS = (
    DIRECTION_SKILLS,
    frozenset({"bosskuai-diagnose-loop", "systematic-debugging"}),
    frozenset({"bosskuai-tdd-loop", "test-driven-development"}),
    frozenset({"animate", "emil-design-eng"}),
    frozenset({"awwwards", "awwwards-web-design"}),    # two full Awwwards build loops; bosskuai-taste routes to either
)


# Selection policy. Scores are lexical evidence on a scale that shrinks as a prompt gets longer, so the
# floors are low and the shortlist is judged relative to the best match instead of against a fixed bar.
MIN_EVIDENCE = 1.5          # below this the router has nothing to go on and falls back to the cofounder skill
RELATIVE_FLOOR = 0.65       # a follow-up skill needs at least this share of the best score (or a phrase match)
CONCERN_WINNER_MIN = 6.0    # a clause of a multi-part request nominates its best skill above this score
CONFIDENT_MIN = 6.0         # a confident pick needs this much evidence and a lead over the runner-up
CONFIDENT_LEAD = 1.25

_TASK_ACTION = re.compile(
    r"\b(?:build|run|audit(?:ing|ed|s)?|implement(?:ing|ed|s)?|writ(?:e|ing)|creat(?:e|ing)|"
    r"design(?:ing|ed|s)?|debug(?:ging)?|diagnos(?:e|ing)|fix(?:es|ed|ing)?|repair(?:ing|ed)?|"
    r"investigat(?:e|ing)|review(?:ing|ed|s)?|test(?:ing|ed|s)?|verif(?:y|ying)|configur(?:e|ing)|"
    r"setup|optimiz(?:e|ing)|explain|trace|improve|translate|rewrite|plan|migrate|deploy|connect|"
    r"install|remove|compare|analyse|analyze|check|inspect(?:ing|ed)?|grad(?:e|ing)|"
    r"convert(?:ing)?|extract(?:ing)?|find|search|summari[sz](?:e|ing)|recommend|"
    r"calculate|generate|animate|set up|reduce|increase|grow|retain|launch|market|sell|"
    r"measure|track|protect|secure|integrate|connect|monitor|schedule|publish|refactor|"
    r"harden|redesign|upgrade|bump|profile|cache|validate|scale|expose|prioriti[sz]e|"
    r"speed up|clean up|sort out|figure out|hook up)\b")
_TASK_DEFECT = re.compile(
    r"\b(?:crash(?:es)?|broken|fails?|failing|exception|error|timeouts?|missing|intermittent|"
    r"regression|not working|still happens|bugs?|hang(?:s|ing)?|freez(?:e|es|ing)|leak(?:s|ing)?|"
    r"flaky|outage|hacked|stutter(?:s|ing)?)\b")
# Wording that also fills follow-ups ("can you make that shorter", "yes please", "still wrong"): a task only
# when the request also names the skill's subject twice over (see skill_has_task_evidence).
_TASK_SOFT = re.compile(
    r"\b(?:add(?:ing|ed|s)?|make|version|model(?:ing|ling)?|tighten|decide|choose|pick|handle|rename|"
    r"split|ship|release|document|scope|draft|pitch|wire)\b|"
    r"\b(?:i|we)\s+(?:need|want|have to|must|would like)\b|\b(?:i'd|we'd) like\b|"
    r"\b(?:need|want)s?\s+(?:to|a|an|the|some|our|my|this|it)\b|\bhow (?:do|can|should|would) (?:i|we|you)\b|"
    r"\bwhat(?:'s| is) the (?:best|right|proper|cleanest) way\b|\bshould (?:we|i)\b|"
    r"\b(?:can|could|would) (?:you|u)\b|\b(?:help|pls|please)\b|\btrying to\b|\b(?:i'm|i am|we're|we are) \w+ing\b|"
    r"\b(?:slow(?:er|ness)?|lag(?:s|gy|ging)?|stuck|wrong|incorrect|re-?render(?:s|ing)?|dropp(?:ed|ing)|"
    r"keeps? \w+ing|not \w+ing|(?:doesn't|does not|won't|can't|cannot|isn't|aren't|didn't) \w+)\b")
_GENERIC_CONCERN = frozenset(
    "app apps code task tasks issue issues build write create fix review design test tests run "
    "check use request function implementation button user website plan error go going "
    "change update good morning sentence line output time keep message word dictionary list "
    "one two second double right small format section later next thing read "
    "first last option options short shorter more other same".split())


def skill_has_task_evidence(row: dict, task: str, data: dict) -> bool:
    """Require a task and concrete skill evidence, not just a high lexical score."""
    from bossku.index import CURATED_TRIGGERS, routing_context, tokenize

    if row.get('reason') == 'explicit skill request':
        return True
    text = routing_context(task)
    strong = bool(_TASK_ACTION.search(text) or _TASK_DEFECT.search(text)
                  or re.search(r"(?:^|\bplease\s+|\byou\s+)read\b", text))
    if not (strong or _TASK_SOFT.search(text)):
        return False
    sid = row['skill_id']

    def subject(term: str) -> bool:
        return not (term in _GENERIC_CONCERN or _TASK_ACTION.fullmatch(term)
                    or (not strong and _TASK_SOFT.fullmatch(term)))

    terms = {term for term in row.get('matched_terms', ()) if subject(term)}
    keyword_terms = {term for term in set(tokenize(text)) &
                     set(data.get('skills', {}).get(sid, {}).get('keywords', ())) if subject(term)}
    precise = any(len(p.split()) >= 2 and p in CURATED_TRIGGERS.get(sid, ())
                  for p in row.get('matched_triggers', ()))
    # Meta descriptions are not a request for Meta advertisements.
    if sid == 'ads' and not re.search(r"\b(?:ads|advertising|advertisements?|ppc|campaigns?)\b", text):
        return False
    if sid == 'bosskuai-i18n-l10n' and not re.search(
        r"\b(?:i18n|l10n|locales?|app|website|product|software|frontend|backend|"
        r"translation keys|language switch|rtl|internationalization|localization)\b", text
    ):
        return False
    contexts = {
        'bosskuai-ai-model-selection': r"\b(?:models?|llm|claude|gpt|opus|sonnet|inference|tokens?|context window)\b",
        'graft': r"\b(?:graft|repo|repository|codebase|files?|modules?|call sites|called|callers|blast radius)\b",
        'minimal-fix': r"\b(?:bug|regression|diff|patch|hotfix|code|failing|broken)\b",
        'ci-triage': r"\b(?:ci|pipeline|workflow|github actions|build failure|failing checks|red checks|checks are failing)\b",
        'bosskuai-react-development': r"\b(?:react|jsx|tsx|next.js|nextjs)\b",
        'bosskuai-nuxt-development': r"\b(?:nuxt|nuxtjs|nitro|usefetch|useasyncdata|routerules|runtimeconfig)\b",
        'bosskuai-claude-md-management': r"\b(?:claude\.md|rule files?|instructions?|imports?|instruction scope|session learning)\b",
        'bosskuai-customize-bosskuai': r"\b(?:config|configuration|agents\.md|skill-index|skill definitions?|plugin manifests?|edit|modify|change|update)\b",
        'bosskuai-prompt-optimizer': r"\b(?:optimize|improve|draft|write|rewrite|ready-to-paste)\b",
        'loop-constraints': r"\b(?:loop|constraints?|denylist|safety|sweep|triage|ci|pull requests?)\b",
        'bosskuai-permanent-memory-orchestration': r"\b(?:memory|remember|obsidian|recall|notes?|handoff|durable decisions?|durable plans?)\b",
        'bosskuai-prompt-injection-defense': r"\b(?:injection|security|secure|attacks?|poisoning|untrusted|permissions?|tool abuse)\b",
        'schema': r"\b(?:schema|jsonld|json-ld|structured data|rich results|schema.org|markup|seo)\b",
        'animate-expo': r"\b(?:expo|react native|native|mobile|ios|android)\b",
        'bosskuai-expo-react-native': r"\b(?:expo|react native|eas|ios|android|mobile apps?|testflight|play store|app store)\b",
        'diagnosing-superpowers': r"\b(?:sessions?|superpowers|skills?|agents?|subagents?|transcripts?|claude|codex|tokens?)\b",
        'loop-triage': r"\b(?:issues?|backlog|ci|prs?|pull requests?|sweep|agent loops?|triage)\b",
        'error-handling': r"\b(?:errors?|exceptions?|retries|retry|circuit breaker|failures?|timeouts?|malformed|broken|crash|fallback)\b",
        'emil-design-eng': r"\b(?:motion|animations?|animated|gestures?|hover|transition|easing|drag|spring|interaction)\b",
    }
    if sid in contexts and not re.search(contexts[sid], text):
        return False
    if sid in DIRECTION_SKILLS and not re.search(
        r"\b(?:ui|ux|design|landing|page|frontend|interface|dashboard|website|layout|screen|visual|portfolio|"
        r"homepage|site|hero|laman|halaman|awwwards)\b", text
    ):
        return False
    if not strong:   # description keywords alone match follow-ups; soft wording needs the skill's own words twice
        return bool(precise or len(terms) >= 2)
    return bool(precise or terms or len(keyword_terms) >= 2)


def select_skill_stack(
    task: str,
    root: Path | None = None,
    limit: int = 5,
    available: set[str] | None = None,
    data: dict | None = None,
) -> dict:
    """Compose skills from prompt evidence, without executing or installing them.

    Scores are lexical evidence, not probabilities. Availability is an explicit
    host/profile inventory; None means the full installable repository inventory.
    `data` is a routing index the caller already holds (see rank_skills).
    """
    from bossku.index import normalize_task, routing_context, tokenize, variants

    data = _routing_index(root) if data is None else data
    entries = data.get("skills", {})
    allowed = (set(entries) if available is None else set(available)) - NOT_INSTALLED
    ranked = rank_skills(task, root, limit=len(entries), data=data)
    scores = dict(ranked)
    # Score separate asks independently so a strong first domain cannot drown out
    # a second one. These are candidate hints; novelty and alternatives still gate loading.
    concern_winners: dict[str, str] = {}    # skill -> the clause it won, as evidence for its own task
    normalized = routing_context(task)
    pieces = re.split(r"([;,\n]|\b(?:and|then|also)\b)", normalized)
    concerns, joins = pieces[0::2], [""] + pieces[1::2]
    if len(concerns) > 1:
        for at, concern in enumerate(concerns):
            if not concern.strip():    # the gap between two separators never nominates a skill; ranking it only costs time
                continue
            matches = rank_skills(concern, root, limit=1, data=data)
            if matches and matches[0][1] >= CONCERN_WINNER_MIN:
                # "fix X and Y": Y shares the verb before "and"; a sentence after a comma brings its own.
                shared = joins[at].strip() in ("and", "also") and at > 0
                concern_winners.setdefault(matches[0][0], (concerns[at - 1] + " " if shared else "") + concern)
    aliases = load_aliases(root)
    resolved = {alias: resolve_skill_id(target, root, aliases) for alias, target in aliases.items()}
    task_l = normalize_task(task)
    requested: list[str] = []
    mentions = []
    # A substring test first: a regex per skill name overflows re's 512-pattern cache and recompiles every prompt.
    for name in [*entries, *aliases]:
        spaced = name.removeprefix("bosskuai-").replace("-", " ")
        if name not in task_l and spaced + " skill" not in task_l:
            continue
        for match in re.finditer(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", task_l):
            before = task_l[:match.start()]
            named = ("-" in name or "_" in name or task_l.strip() == name
                     or before.endswith(("/", "$"))
                     or re.search(r"\b(?:use|load|invoke|run|apply|select|skill)\s+"
                                  r"(?:[\w$/-]+\s*(?:,|and)\s*)*$", before))
            if not named:
                continue
            mentions.append((match.start(), resolve_skill_id(name, root, aliases)))
        # "use the mysql patterns skill", "run the four-voice council skill": a spaced id, asked for by a verb.
        for match in re.finditer(r"\b(?:use|load|invoke|run|apply|try)\s+(?:[\w-]+\s+){0,3}?"
                                 + re.escape(spaced) + r"\s+skill\b", task_l):
            mentions.append((match.start(), resolve_skill_id(name, root, aliases)))
    for _, sid in sorted(mentions):
        if sid not in requested:
            requested.append(sid)

    selected: list[dict] = []
    deferred: list[dict] = []
    unavailable = []
    excluded: set[str] = set()
    covered: set[str] = set()
    query = {token: variants(token) for token in tokenize(normalized)}
    order = requested + [sid for sid, _ in ranked if sid not in requested]
    top = max((score for sid, score in ranked if sid in allowed), default=0.0)

    for sid in order:
        entry = entries[sid]
        score = scores.get(sid, 0.0)
        explicit = sid in requested
        words = _words(sid.replace("bosskuai-", "").replace("-", " "), *entry.get("triggers", []))
        terms = {term for term, forms in query.items() if forms & words}
        matched_triggers = [phrase for phrase in entry.get("triggers", [])
                            if _contains(" " + task_l.replace("-", " ") + " ",
                                         phrase.replace("-", " "))]
        phrase_match = any(len(phrase.split()) >= 2 for phrase in matched_triggers)
        if not explicit and sid not in concern_winners and (
            score < MIN_EVIDENCE or (score < top * RELATIVE_FLOOR and not phrase_match)
        ):
            continue

        reason = None
        names = [sid, sid.removeprefix("bosskuai-").replace("-", " "),
                 *(alias for alias, target in resolved.items() if target == sid)]
        if sid == "bosskuai-hindsight-memory":
            names.append("hindsight")
        negated = any(re.search(r"\b(?:do not|don't|without|avoid|no|not)\s+"
                                r"(?:(?:use|using|load|loading|invoke|invoking|run|running|apply|applying|select|selecting)\s+)?[$/]?"
                                + re.escape(name) + r"(?![\w-])", task_l) for name in names)
        if negated:
            reason = "excluded by the user"
            excluded.add(sid)
        elif sid not in allowed:
            reason = "not installed in the selected inventory"
            if explicit:
                unavailable.append(sid)
        elif entry.get("user_invoked"):
            reason = "requires user invocation as /" + sid
        elif sid == "bosskuai-hindsight-memory" and not (
            re.search(r"\bhindsight\b", task_l)
            or (re.search(r"\b(?:retain|recall|reflect)\b", task_l)
                and re.search(r"\b(?:memory bank|bank_id|bank id|mcp)\b", task_l))
        ):
            reason = "optional Hindsight integration was not requested"
        elif any(sid in group and any(row["skill_id"] in group for row in selected)
                 for group in ALTERNATIVE_SKILLS):
            reason = "alternative to an already selected skill"
        elif len(selected) >= max(limit, 0):
            reason = "stack limit reached; use this skill in a later phase"
        elif selected and not explicit and sid not in concern_winners and not ((terms - covered) - _GENERIC_CONCERN):
            reason = "does not cover another prompt concern"
        elif selected and not explicit and not skill_has_task_evidence(
            {'skill_id': sid, 'matched_terms': terms, 'matched_triggers': matched_triggers},
            concern_winners.get(sid, task), data
        ):
            reason = "no concrete task evidence for another concern"
        elif selected and not explicit and sid not in concern_winners and not phrase_match and len(
            {t for t in terms - covered
             if t not in _GENERIC_CONCERN and not _TASK_ACTION.fullmatch(t) and not _TASK_SOFT.fullmatch(t)}
        ) < 2:
            # One shared word ("service", "submit") is how unrelated skills ride along with the real one.
            reason = "one shared word is not a separate concern"

        if reason:
            deferred.append({"skill_id": sid, "reason": reason, "score": round(score, 3)})
            continue
        selected.append({"skill_id": sid, "score": round(score, 3),
                         "description": entry.get("description", ""),
                         "reason": "explicit skill request" if explicit else
                                   ("primary prompt match" if not selected else "additional prompt concern"),
                         "matched_terms": sorted(terms), "matched_triggers": matched_triggers})
        covered.update(terms)

    if not selected and limit > 0 and COFOUNDER_SKILL in allowed and COFOUNDER_SKILL not in excluded:
        selected.append({"skill_id": COFOUNDER_SKILL, "score": 0.0,
                         "description": entries[COFOUNDER_SKILL].get("description", ""),
                         "reason": "insufficient eligible evidence; inspect the task before loading specialists",
                         "matched_terms": [], "matched_triggers": []})
    primary = selected[0]["skill_id"] if selected else None
    primary_score = selected[0]["score"] if selected else 0.0
    runner_up = max((score for sid, score in ranked if sid in allowed and sid != primary), default=0.0)
    confident = bool(selected) and (primary in requested or
                                  (primary_score >= CONFIDENT_MIN and primary_score >= runner_up * CONFIDENT_LEAD))
    unknown = sorted(set(re.findall(r"\bbosskuai-[a-z0-9]+(?:-[a-z0-9]+)*\b", task_l))
                     - set(entries) - set(aliases))
    unavailable.extend(unknown)
    deferred.extend({"skill_id": sid, "reason": "unknown requested skill", "score": 0.0} for sid in unknown)
    return {"primary": primary, "selected": selected, "deferred": deferred,
            "confident": confident, "unavailable_requested": unavailable,
            "note": "Read selected descriptions and verify host capabilities. Scores are lexical evidence; "
                    "re-route when the task changes. Selection does not invoke tools or authorize side effects."}


def _contains(haystack: str, phrase: str) -> bool:
    return f" {phrase} " in haystack


@lru_cache(maxsize=None)   # the default 128 slots never hit: one lookup touches every skill
def _words(*phrases: str) -> frozenset[str]:
    from bossku.index import tokenize

    return frozenset(w for phrase in phrases for w in tokenize(phrase))


_stale_noted: set[Path] = set()


def _routing_index(root: Path | None = None) -> dict:
    from bossku.index import build_index, load_index, skills_fingerprint

    data = load_index(root)
    if data is not None and data.get("fingerprint") == skills_fingerprint(root):
        return data
    # The prompt hook reads the saved index without hashing the skills, so it cannot notice this; say it here, once.
    if data is not None and repo_root(root) not in _stale_noted:
        _stale_noted.add(repo_root(root))
        print("bossku: skills/skill-index.json is stale; routing from a fresh in-memory build. The prompt hook "
              "keeps using the saved index until you run `bossku skills index`.", file=sys.stderr)
    return build_index(root)


def _score_entry(
    sid: str,
    entry: dict,
    task_l: str,
    q_terms: dict[str, tuple[float, set[str]]],
    q_mass: float,
) -> float:
    """Score by how much of the query a skill explains, plus exact phrase evidence.

    Coverage-based rather than additive: an incidental word ("design *tokens*" hitting
    `token-saver`) explains one term out of several, so it cannot outrank a skill that
    accounts for the whole request.
    """
    from bossku.index import singular

    ident = sid.replace("bosskuai-", "").replace("-", " ")
    id_tokens = {singular(t) for t in sid.replace("bosskuai-", "").split("-") if len(t) >= 2}
    triggers = entry.get("triggers", [])
    trigger_words = _words(*triggers)
    keywords = set(entry.get("keywords", []))

    # Users write "founder-led" where a trigger says "founder led": compare both spellings.
    task_flat = task_l.replace("-", " ")

    def says(phrase: str) -> bool:
        return _contains(task_l, phrase) or _contains(task_flat, phrase.replace("-", " "))

    if any(says(phrase) for phrase in entry.get("exclusions", [])):
        return 0.0

    # How much of the query's information mass does this skill account for?
    matched = 0.0
    for weight, forms in q_terms.values():
        if forms & id_tokens:
            matched += weight * 3.0
        elif forms & trigger_words:
            matched += weight * 2.0
        elif forms & keywords:
            matched += weight * 1.0
    coverage = matched / (q_mass * 3.0)
    score = 18.0 * coverage

    # Exact multi-word phrases are precise evidence and survive on their own merit.
    for field, weight in (("triggers", 5.0), ("phrases", 1.8)):
        for phrase in entry.get(field, []):
            words = phrase.replace("-", " ").split()   # "micro-interactions" is two words, like "micro interactions"
            if len(words) >= 2 and says(phrase):
                score += weight + 0.9 * len(words)

    if _contains(task_l, sid) or _contains(task_l, ident):
        score += 3.0 if len(id_tokens) > 1 else 1.5

    return score


def make_path_writable(path: Path) -> None:
    """Add user-write permission without discarding existing mode bits."""
    try:
        os.chmod(path, path.stat().st_mode | stat.S_IWRITE)
    except FileNotFoundError:
        return


def make_tree_writable(path: Path) -> None:
    """Parents first: on POSIX a folder without read and search bits hides its children until it is fixed."""
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink():
        os.chmod(path, path.stat().st_mode | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        for child in path.iterdir():
            make_tree_writable(child)
    else:
        make_path_writable(path)


def _remove_read_only(func, path: str, _exc_info) -> None:
    target = Path(path)
    make_path_writable(target)
    func(path)


def remove_tree(path: Path) -> None:
    """Remove a tree even when copied files carry Windows read-only attributes or POSIX read-only modes."""
    if not path.exists():
        return
    try:
        shutil.rmtree(path, onerror=_remove_read_only)
    except OSError:
        # POSIX: a file in a folder without write permission cannot be unlinked, and the error names the file,
        # not the folder, so the handler above cannot fix it. Open the whole tree, then try once more.
        make_tree_writable(path)
        shutil.rmtree(path, onerror=_remove_read_only)


def copy_skills_to(dest_dir: Path, root: Path | None = None, profile: str = "full") -> list[str]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    selected = [sid for sid in _profile_skills(profile, root) if sid not in NOT_INSTALLED]   # whatever the profile lists
    short = load_lean(root)["descriptions"] if profile == "lean" else {}
    installed: list[str] = []
    for sid in selected:
        src = skill_folder(sid, root)
        if not src.is_dir():
            continue
        target = dest_dir / sid
        if target.exists():
            remove_tree(target)
        shutil.copytree(src, target)
        make_tree_writable(target)
        if sid in short:
            set_description(target / "SKILL.md", short[sid])
        installed.append(sid)
    return installed


LEAN_FILE = "lean.json"


def lean_path(root: Path | None = None) -> Path:
    return skills_dir(root) / LEAN_FILE


def load_lean(root: Path | None = None) -> dict:
    """The skills a host lists in every session, with short descriptions.

    Hosts spend a fixed share of the context window on skill descriptions and cut the rest down to
    bare names, so the long tail is kept out of the list and reached through `bosskuai-skill-finder`.
    """
    path = lean_path(root)
    if not path.is_file():
        return {"listed": [], "descriptions": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "listed": [str(sid) for sid in data.get("listed", [])],
        "descriptions": {str(k): str(v) for k, v in data.get("descriptions", {}).items()},
    }


def set_description(skill_md: Path, description: str) -> None:
    """Replace the frontmatter description of an installed copy; repository sources are never edited."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return
    close = re.search(r"^---[ \t]*$", text[3:], re.MULTILINE)
    if close is None:
        return
    head_end = 3 + close.start()
    lines = text[3:head_end].split("\n")
    out: list[str] = []
    done = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if not done and line.startswith("description:"):
            out.append("description: " + json.dumps(description, ensure_ascii=False))
            i += 1
            while i < len(lines):
                if lines[i][:1] in (" ", "\t"):          # continuation of a folded or block scalar
                    i += 1
                    continue
                if not lines[i].strip():                 # blank line: only a continuation if an indented line follows
                    j = i
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and lines[j][:1] in (" ", "\t"):
                        i = j
                        continue
                break
            done = True
            continue
        out.append(line)
        i += 1
    if done:
        skill_md.write_text("---" + "\n".join(out) + text[head_end:], encoding="utf-8", newline="\n")


def copy_library_to(dest_dir: Path, root: Path | None = None, exclude: set[str] | frozenset[str] = frozenset()) -> list[str]:
    """Install whole skills the host does not list, so `bossku skills show` can read them on demand."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    ids = [sid for sid in list_skill_ids(root) if sid not in exclude and sid not in NOT_INSTALLED]
    for sid in ids:
        target = dest_dir / sid
        if target.exists():
            remove_tree(target)
        shutil.copytree(skill_folder(sid, root), target)
        make_tree_writable(target)
    for child in dest_dir.iterdir():
        if child.is_dir() and child.name not in set(ids):
            remove_tree(child)
    return ids


def locate_skill(sid: str, root: Path | None = None, home: Path | None = None) -> tuple[str, Path | None]:
    """Where a skill can be read: ("listed" | "library" | "repo", SKILL.md) or ("missing", None)."""
    sid = resolve_skill_id(sid, root)
    for kind, folder in (("listed", claude_skills_dir(home)), ("listed", agents_skills_dir(home)),
                         ("library", library_dir(home))):
        path = folder / sid / "SKILL.md"
        if path.is_file():
            return kind, path
    try:
        path = skill_folder(sid, root) / "SKILL.md"
    except FileNotFoundError:
        return "missing", None
    return ("repo", path) if path.is_file() else ("missing", None)


LIBRARY_ONLY_FILE = "library-only.json"


def load_library_only(root: Path | None = None) -> frozenset[str]:
    """Skills no profile lists. The hint and `bossku skills find` still reach them; `show` or a read loads them."""
    path = skills_dir(root) / LIBRARY_ONLY_FILE
    if not path.is_file():
        return frozenset()
    return frozenset(json.loads(path.read_text(encoding="utf-8")).get("skills", []))


def validate_library_only(root: Path | None = None) -> list[str]:
    ids = set(list_skill_ids(root))
    listed = set(load_lean(root)["listed"])
    errors = [f"{LIBRARY_ONLY_FILE}: {sid} has no skill folder" for sid in sorted(load_library_only(root) - ids)]
    errors += [f"{LIBRARY_ONLY_FILE}: {sid} is also in {LEAN_FILE} listed" for sid in sorted(load_library_only(root) & listed)]
    # The folder is the switch plugins see: they list skills/ and never library/.
    base = skills_dir(root)
    library = base.parent / LIBRARY_SKILLS_DIR
    library_only = load_library_only(root)
    for sid in sorted(ids):
        in_skills, in_library = (base / sid / "SKILL.md").is_file(), (library / sid / "SKILL.md").is_file()
        if in_skills and in_library:
            errors.append(f"{sid} has a folder in both skills/ and {LIBRARY_SKILLS_DIR}/")
        elif sid in library_only and in_skills:
            errors.append(f"{LIBRARY_ONLY_FILE}: {sid} must live in {LIBRARY_SKILLS_DIR}/ so plugin installs do not list it")
        elif sid not in library_only and in_library:
            errors.append(f"{LIBRARY_SKILLS_DIR}/{sid} is not in {LIBRARY_ONLY_FILE}: list it there or move it to skills/")
    return errors


MAX_LEAN_SKILLS = 48
MAX_LEAN_DESCRIPTION_CHARS = 150


def validate_lean(root: Path | None = None) -> list[str]:
    """The lean list must stay small, short and complete, or its context saving quietly erodes."""
    path = lean_path(root)
    if not path.is_file():
        return [f"missing skills/{LEAN_FILE}"]
    errors: list[str] = []
    lean = load_lean(root)
    ids = set(list_skill_ids(root))
    listed = lean["listed"]
    if len(set(listed)) != len(listed):
        errors.append(f"{LEAN_FILE}: duplicate ids in listed")
    if len(listed) > MAX_LEAN_SKILLS:
        errors.append(f"{LEAN_FILE}: {len(listed)} listed skills; keep at most {MAX_LEAN_SKILLS}")
    if "bosskuai-skill-finder" not in listed:
        errors.append(f"{LEAN_FILE}: bosskuai-skill-finder must be listed or the long tail is unreachable")
    for sid in listed:
        if sid not in ids:
            errors.append(f"{LEAN_FILE}: listed skill has no folder: {sid}")
        elif sid in NOT_INSTALLED:
            errors.append(f"{LEAN_FILE}: {sid} is never installed")
        shown = lean["descriptions"].get(sid) or (
            parse_skill_md(skill_folder(sid, root) / "SKILL.md").description if sid in ids else "")
        if not MIN_DESCRIPTION_CHARS <= len(shown) <= MAX_LEAN_DESCRIPTION_CHARS:
            errors.append(f"{LEAN_FILE}: {sid} description is {len(shown)} chars; "
                          f"use {MIN_DESCRIPTION_CHARS}-{MAX_LEAN_DESCRIPTION_CHARS}")
    for sid in lean["descriptions"]:
        if sid not in listed:
            errors.append(f"{LEAN_FILE}: description for a skill that is not listed: {sid}")
    return errors


def prune_stale_skills(dests: tuple[Path, ...], keep: set[str], root: Path | None = None) -> list[str]:
    """Remove managed copies this install no longer ships (retired, excluded, or off-profile).

    Without this, a skill deleted from the repo lives on in every host's listing.
    Unmanaged folders (the user's own skills) are never touched.
    """
    pruned: set[str] = set()
    for dest in dests:
        if not dest.is_dir():
            continue
        for child in dest.iterdir():
            if child.is_dir() and child.name not in keep and is_managed_skill_name(child.name, root):
                remove_tree(child)
                pruned.add(child.name)
    return sorted(pruned)


PROFILES = ("lean", "core", "engineering", "full")


def _profile_skills(profile: str, root: Path | None) -> list[str]:
    if profile not in PROFILES:
        raise ValueError("profile must be lean, core, engineering or full")
    if profile == "lean":
        return [sid for sid in load_lean(root)["listed"] if skill_folder(sid, root).is_dir()]
    core = [
        COFOUNDER_SKILL,
        "bosskuai-project-understanding",
        "bosskuai-search-first",
        "antislop",
        "antislop-copywriting",
        "bosskuai-continuous-learning",
        "bosskuai-context-limit-continuation",
        "bosskuai-permanent-memory-orchestration",
        "bosskuai-engineering-delivery",
        "bosskuai-rigorous-code-review",
        "bosskuai-documentation-lookup",
        "bosskuai-ponytail",
        "bosskuai-grounding",
        "bosskuai-security-gate",
        "malaysia-localisation",
        "bosskuai-taste",
    ]
    if profile == "core":
        loop_ids = load_pack_skill_ids("loop-engineering", root)
        combined: list[str] = []
        seen: set[str] = set()
        for sid in [*core, *loop_ids]:
            if sid in seen:
                continue
            seen.add(sid)
            combined.append(sid)
        return [s for s in combined if skill_folder(s, root).is_dir()]
    library_only = load_library_only(root)
    if profile == "engineering":   # everything except the marketing pack; copy_skills_to still refuses NOT_INSTALLED
        marketing = set(load_pack_skill_ids("marketingskills", root))
        return [s for s in list_skill_ids(root) if s not in marketing and s not in library_only]
    return [s for s in list_skill_ids(root) if s not in NOT_INSTALLED and s not in library_only]


def is_managed_skill_name(name: str, root: Path | None = None) -> bool:
    if name in {COFOUNDER_SKILL, "malaysia-localisation"} or name.startswith(MANAGED_SKILL_PREFIX):
        return True
    # Retired ids (aliases) and dropped vendored skills were ours once, so stale copies are ours to prune.
    return (
        name in load_vendored_ids(root)
        or name in load_aliases(root)
        or name in load_excluded_vendored(root)
    )


def count_managed_skills(dest_dir: Path, root: Path | None = None) -> int:
    if not dest_dir.is_dir():
        return 0
    total = 0
    for child in dest_dir.iterdir():
        if not child.is_dir():
            continue
        if not (child / "SKILL.md").is_file():
            continue
        if is_managed_skill_name(child.name, root):
            total += 1
    return total


_MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


_FENCE = re.compile(r"^( {0,3})(`{3,}|~{3,}).*?^\1\2[ \t]*$", re.M | re.S)


def _broken_relative_links(skill_md: Path) -> list[str]:
    broken: list[str] = []
    # A link inside a fenced code block is example text (an ADR index template, say), not a file to open.
    text = _FENCE.sub("", skill_md.read_text(encoding="utf-8"))
    for raw in _MARKDOWN_LINK.findall(text):
        target = raw.strip().strip("<>")
        if not target or target.startswith(("#", "/", "\\")):
            continue
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        # Ignore optional Markdown titles and validate only the path component.
        target = unquote(target.split()[0].split("#", 1)[0])
        if target and not (skill_md.parent / target).resolve().exists():
            broken.append(raw.strip())
    return broken


def audit_skills(root: Path | None = None) -> dict:
    """Measure routing context, skill size, provenance, and local link integrity."""
    ids = list_skill_ids(root)
    vendored = load_vendored(root)
    custom = [sid for sid in ids if sid not in vendored]
    # Library-only skills are listed by no profile, so their descriptions cost no session any context.
    library_only = load_library_only(root)
    listed_custom = [sid for sid in custom if sid not in library_only]
    descriptions: dict[str, str] = {}
    body_words: dict[str, int] = {}
    broken_links: list[dict[str, str]] = []

    by_pack: dict[str, list[str]] = {"all": ids, "bossku": custom}
    for sid in ids:
        skill_md = skill_folder(sid, root) / "SKILL.md"
        descriptions[sid] = parse_skill_md(skill_md).description
        body_words[sid] = len(re.findall(r"\b[\w'-]+\b", skill_md.read_text(encoding="utf-8")))
        pack = vendored.get(sid, "bossku")
        if pack != "bossku":
            by_pack.setdefault(pack, []).append(sid)
        for target in _broken_relative_links(skill_md):
            broken_links.append({"skill_id": sid, "pack": pack, "target": target})

    description_chars = sum(len(value) for value in descriptions.values())
    custom_description_chars = sum(len(descriptions[sid]) for sid in listed_custom)
    broken_by_pack: dict[str, int] = {}
    for item in broken_links:
        broken_by_pack[item["pack"]] = broken_by_pack.get(item["pack"], 0) + 1
    return {
        "skill_count": len(ids),
        "custom_count": len(custom),
        "vendored_count": len(ids) - len(custom),
        "description_chars": description_chars,
        "approx_description_tokens": math.ceil(description_chars / 4),
        "custom_description_chars": custom_description_chars,
        "approx_custom_description_tokens": math.ceil(custom_description_chars / 4),
        "descriptions_over_300_chars": sorted(
            sid for sid, value in descriptions.items() if len(value) > 300
        ),
        "library_only_count": len(library_only & set(ids)),
        "custom_descriptions_over_300_chars": sorted(
            sid for sid in listed_custom if len(descriptions[sid]) > 300
        ),
        "custom_descriptions_without_use_when": sorted(
            sid for sid in custom if not descriptions[sid].lower().startswith("use when")
        ),
        "bodies_over_500_words": sorted(
            sid for sid, words in body_words.items() if words > 500
        ),
        "broken_relative_links": broken_links,
        "broken_relative_links_by_pack": dict(sorted(broken_by_pack.items())),
        "custom_broken_relative_links": [
            item for item in broken_links if item["pack"] == "bossku"
        ],
        "skills_by_pack": {pack: sorted(pack_ids) for pack, pack_ids in sorted(by_pack.items())},
    }


KNOWN_FRONTMATTER_KEYS = frozenset(
    {
        "name",
        "description",
        "metadata",
        "license",
        "user-invocable",
        "allowed-tools",
        "disallowed-tools",
        "when_to_use",
        "arguments",
        "model",
        "effort",
        "context",
        "agent",
        "paths",
        "argument-hint",
        "compatibility",
        "version",
        "triggers",
        "keywords",
        "model_role",
        "disable-model-invocation",
        "origin",  # ECC provenance marker on vendored skills
    }
)

_TOP_LEVEL_SCALAR = re.compile(r"^([A-Za-z0-9_-]+):[ 	]+(.+)$")


def _strict_yaml_problems(text: str) -> list[str]:
    """Top-level plain values that real YAML parsers reject but Bossku's lenient parser accepts.

    An unquoted `description: Use this for x: y` makes Claude Code, Codex, and Cursor drop the
    description and show the file's H1 instead, so the skill routes by name only.
    """
    match = re.search(r"^---[ 	]*$", text[3:], re.MULTILINE)
    if match is None:
        return []
    keys: list[str] = []
    for line in text[3 : 3 + match.start()].splitlines():
        found = _TOP_LEVEL_SCALAR.match(line)
        if not found:
            continue
        value = found.group(2).strip()
        if value[:1] in "\"'[{|>&*!%@`":
            continue
        if ": " in value or " #" in value or value.endswith(":"):
            keys.append(found.group(1))
    return keys


# Hosts read `description` on every session, so it is a shared context budget.
MAX_DESCRIPTION_CHARS = 1200
MIN_DESCRIPTION_CHARS = 40

# `allowed-tools` runs the listed tools with no permission prompt in the turn that loads the skill (Claude Code), so a
# blanket shell grant, or a catch-all for a CLI that can push, merge, publish or deploy, skips the user's Risk pauses.
# Grant the read-only subcommands instead (`Bash(gh pr view:*)`) and let the rest go through the normal prompt.
_GRANT = re.compile(r"[A-Za-z_]+(?:\([^)]*\))?")
_BLANKET_SHELL = frozenset({"bash", "powershell", "bash(*)", "bash(:*)", "powershell(*)", "powershell(:*)"})
_CATCH_ALL_CLIS = frozenset({"git", "gh", "glab", "p4", "npm", "pnpm", "yarn", "npx", "bunx", "docker", "kubectl",
                             "helm", "terraform", "vercel", "eas", "fly", "firebase", "aws", "gcloud", "az"})
# A grant for one of these, with or without more words after it, pre-approves the push, merge, publish or deploy
# itself. `gh api` and `glab api` are raw API access: one call can merge a PR or force-move a branch.
_RISKY_SUBCOMMANDS = ("gh api", "glab api", "git push", "gh pr merge", "gh pr create", "glab mr merge",
                      "glab mr create", "gh repo create", "gh repo delete", "gh repo archive", "gh repo rename",
                      "gh release create", "gh release delete", "gh release upload", "gh workflow run",
                      "npm publish", "pnpm publish", "yarn publish", "yarn npm publish", "bun publish",
                      "cargo publish", "twine upload", "gem push", "docker push", "kubectl delete", "helm uninstall",
                      "terraform apply", "terraform destroy", "pulumi up", "pulumi destroy", "eas submit",
                      "eas update", "fly deploy", "firebase deploy", "wrangler deploy", "netlify deploy",
                      "vercel deploy", "p4 submit", "p4 shelve")


def risky_tool_grants(value: object) -> list[str]:
    """The entries of an `allowed-tools` value that pre-approve a whole shell, a whole consequential CLI, or a push,
    merge, publish or deploy subcommand (raw `gh api` / `glab api` included)."""
    text = " ".join(str(v) for v in value) if isinstance(value, list) else str(value or "")
    risky: list[str] = []
    for grant in _GRANT.findall(text):
        g = grant.strip().lower()
        inner = re.fullmatch(r"(?:bash|powershell)\(\s*([\w.-]+)\s*(?::\s*\*|\s+\*)?\s*\)", g)
        command = re.fullmatch(r"(?:bash|powershell)\((.*)\)", g, re.S)
        words = " ".join(re.sub(r"(?::\s*\*|\s*\*)\s*$", "", command.group(1)).split()) if command else ""
        if (g in _BLANKET_SHELL or (inner and inner.group(1) in _CATCH_ALL_CLIS)
                or any(words == r or words.startswith(r + " ") for r in _RISKY_SUBCOMMANDS)):
            risky.append(grant)
    return risky


def validate_skills(root: Path | None = None) -> list[str]:
    errors: list[str] = []
    vendored = load_vendored(root)
    aliases = load_aliases(root)
    ids = set(list_skill_ids(root))
    for alias, target in aliases.items():
        if alias in ids:
            errors.append(f"alias {alias} conflicts with real skill folder")
        if target not in ids and target not in aliases.values():
            errors.append(f"alias {alias} points to missing skill {target}")
    for sid in sorted(ids):
        skill_md = skill_folder(sid, root) / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"missing SKILL.md for {sid}")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{sid}/SKILL.md missing YAML frontmatter")
            continue
        front = _parse_frontmatter(text)
        if not front:
            errors.append(f"{sid}/SKILL.md frontmatter did not parse")
            continue
        if not str(front.get("name", "")).strip():
            errors.append(f"{sid}/SKILL.md missing name")
        description = str(front.get("description", "")).strip()
        if not description:
            errors.append(f"{sid}/SKILL.md missing description")
        elif len(description) < MIN_DESCRIPTION_CHARS:
            errors.append(
                f"{sid}/SKILL.md description too short ({len(description)} chars); "
                "routing needs enough signal to match on"
            )
        elif len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"{sid}/SKILL.md description too long ({len(description)} chars, "
                f"max {MAX_DESCRIPTION_CHARS}); it loads into every session"
            )
        for key in _strict_yaml_problems(text):
            errors.append(
                f"{sid}/SKILL.md `{key}` needs quotes: hosts' YAML parsers reject ': ' or ' #' "
                "in an unquoted value and drop the field"
            )
        if str(front.get("name", "")).strip() and str(front.get("name", "")).strip() != sid:
            errors.append(
                f"{sid}/SKILL.md name `{front.get('name')}` must match its folder: the Agent Skills spec, Cursor and "
                "OpenCode require it, and Claude Code lists the skill under that name"
            )
        unknown = sorted(set(front) - KNOWN_FRONTMATTER_KEYS)
        if unknown:
            errors.append(f"{sid}/SKILL.md unknown frontmatter key(s): {', '.join(unknown)}")
        # Vendored skills too: a plugin ships their grants as they are.
        for grant in risky_tool_grants(front.get("allowed-tools")):
            errors.append(
                f"{sid}/SKILL.md allowed-tools pre-approves `{grant}` with no prompt; grant the read-only "
                "subcommands it needs instead"
            )
        if sid not in vendored:
            for target in _broken_relative_links(skill_md):
                errors.append(f"{sid}/SKILL.md broken relative link: {target}")
    return errors
