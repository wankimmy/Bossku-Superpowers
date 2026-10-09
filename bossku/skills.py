from __future__ import annotations

import json
import math
import os
import re
import shutil
import stat
from dataclasses import dataclass
from datetime import date
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


# Kept in the repo but never installed: x402 prints generated wallet keys and auto-tops-up spend.
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
                "skills": len(ids),
                "upstream": meta.get("upstream", ""),
                "last_synced": synced_raw or "",
                "age_days": age,
                "review_days": review_days,
                # An unrecorded sync date is treated as due: silence should not read as fresh.
                "overdue": age is None or age > review_days,
            }
        )
    rows.sort(key=lambda r: (-1 if r["age_days"] is None else -r["age_days"]))
    return rows


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


def list_skill_ids(root: Path | None = None) -> list[str]:
    base = skills_dir(root)
    aliases = set(load_aliases(root).keys())
    ids: list[str] = []
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "SKILL.md").is_file():
            continue
        sid = child.name
        if sid in aliases:
            continue
        ids.append(sid)
    return ids


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


def resolve_skill_id(skill_id: str, root: Path | None = None) -> str:
    aliases = load_aliases(root)
    seen: set[str] = set()
    current = skill_id
    while current in aliases:
        if current in seen:
            break
        seen.add(current)
        current = aliases[current]
    return current


def rank_skills(task: str, root: Path | None = None, limit: int = 5) -> list[tuple[str, float]]:
    """Rank skills for a task, best first. Uses skills/skill-index.json when present."""
    from bossku.index import compute_idf, tokenize, variants

    data = _routing_index(root)
    entries: dict[str, dict] = data.get("skills", {})
    if not entries:
        return []

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
        scored.append((sid, _score_entry(sid, entry, task_l, q_terms, q_mass) + REQUEST_FIT_WEIGHT * request_fit.get(sid, 0.0)))
    scored.sort(key=lambda pair: (-pair[1], pair[0]))
    return scored[:limit]


# How strongly the vocabulary of real requests counts next to the skill's own words (tuned on the dev halves of two
# prompt sets, reported on the test halves).
REQUEST_FIT_WEIGHT = 5.0
_BM25_K1, _BM25_B = 1.2, 0.75
_request_models: dict[str, tuple] = {}


def _request_model(entries: dict[str, dict], key: str) -> tuple:
    """(counts per skill, length per skill, average length, idf) from the 'word:count' text in the index."""
    if key and key in _request_models:
        return _request_models[key]
    counts = {sid: {w: int(c) for w, _, c in (item.partition(":") for item in entry["qterms"].split())}
              for sid, entry in entries.items() if entry.get("qterms")}
    lengths = {sid: sum(c.values()) for sid, c in counts.items()}
    average = sum(lengths.values()) / max(len(lengths), 1)
    n = len(counts)
    df: dict[str, int] = {}
    for c in counts.values():
        for w in c:
            df[w] = df.get(w, 0) + 1
    idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}
    model = (counts, lengths, average, idf)
    if key:
        _request_models[key] = model
    return model


def _request_fit(task: str, entries: dict[str, dict], key: str) -> dict[str, float]:
    """0..1 per skill: how well the words of the request match the words people use when they need that skill (BM25)."""
    from bossku.index import singular, tokenize

    counts, lengths, average, idf = _request_model(entries, key)
    if not counts:
        return {}
    words = list(dict.fromkeys(singular(t) for t in tokenize(task)))
    norm = sum(idf.get(w, 0.0) for w in words) * (_BM25_K1 + 1) or 1.0
    fit: dict[str, float] = {}
    for sid, tf in counts.items():
        total = 0.0
        for w in words:
            f = tf.get(w)
            if f:
                total += idf[w] * f * (_BM25_K1 + 1) / (f + _BM25_K1 * (1 - _BM25_B + _BM25_B * lengths[sid] / average))
        if total:
            fit[sid] = total / norm
    best = max(fit.values(), default=0.0)
    # Relative to the best-fitting skill: a request that fits nothing well gets no push, so the curated phrases and
    # the skill's own words keep deciding short or odd requests.
    return {sid: value / best for sid, value in fit.items()} if best else fit


def find_skill(task: str, root: Path | None = None) -> tuple[str, float]:
    aliases = load_aliases(root)
    task_l = task.lower()
    data = _routing_index(root)
    known = set((data or {}).get("skills", {})) or set(list_skill_ids(root))

    for alias, target in aliases.items():
        if alias.replace("bosskuai-", "").replace("-", " ") in task_l and target in known:
            return target, 1.5

    ranked = rank_skills(task, root, limit=1)
    fallback = COFOUNDER_SKILL
    if not ranked or ranked[0][1] <= 0:
        return fallback, 0.0
    return resolve_skill_id(ranked[0][0], root), round(ranked[0][1], 3)


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
)


# Selection policy. Scores are lexical evidence on a scale that shrinks as a prompt gets longer, so the
# floors are low and the shortlist is judged relative to the best match instead of against a fixed bar.
MIN_EVIDENCE = 1.5          # below this the router has nothing to go on and falls back to the cofounder skill
RELATIVE_FLOOR = 0.65       # a follow-up skill needs at least this share of the best score (or a phrase match)
CONCERN_WINNER_MIN = 6.0    # a clause of a multi-part request nominates its best skill above this score
CONFIDENT_MIN = 6.0         # a confident pick needs this much evidence and a lead over the runner-up
CONFIDENT_LEAD = 1.25


def select_skill_stack(
    task: str,
    root: Path | None = None,
    limit: int = 5,
    available: set[str] | None = None,
) -> dict:
    """Compose skills from prompt evidence, without executing or installing them.

    Scores are lexical evidence, not probabilities. Availability is an explicit
    host/profile inventory; None means the full installable repository inventory.
    """
    from bossku.index import tokenize, variants

    entries = _routing_index(root).get("skills", {})
    allowed = (set(entries) if available is None else set(available)) - NOT_INSTALLED
    ranked = rank_skills(task, root, limit=len(entries))
    scores = dict(ranked)
    # Score separate asks independently so a strong first domain cannot drown out
    # a second one. These are candidate hints; novelty and alternatives still gate loading.
    concern_winners: set[str] = set()
    concerns = re.split(r"[;,\n]|\b(?:and|then|also)\b", task.lower())
    if len(concerns) > 1:
        for concern in concerns:
            matches = rank_skills(concern, root, limit=1)
            if matches and matches[0][1] >= CONCERN_WINNER_MIN:
                concern_winners.add(matches[0][0])
    aliases = load_aliases(root)
    task_l = task.lower()
    requested: list[str] = []
    mentions = []
    for name in [*entries, *aliases]:
        for match in re.finditer(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", task_l):
            before = task_l[:match.start()]
            named = ("-" in name or "_" in name or task_l.strip() == name
                     or before.endswith(("/", "$"))
                     or re.search(r"\b(?:use|load|invoke|run|apply|select|skill)\s+"
                                  r"(?:[\w$/-]+\s*(?:,|and)\s*)*$", before))
            if not named:
                continue
            mentions.append((match.start(), resolve_skill_id(name, root)))
    for _, sid in sorted(mentions):
        if sid not in requested:
            requested.append(sid)

    selected: list[dict] = []
    deferred: list[dict] = []
    unavailable = []
    excluded: set[str] = set()
    covered: set[str] = set()
    query = {token: variants(token) for token in tokenize(task)}
    order = requested + [sid for sid, _ in ranked if sid not in requested]
    top = max((score for sid, score in ranked if sid in allowed), default=0.0)

    for sid in order:
        entry = entries[sid]
        score = scores.get(sid, 0.0)
        explicit = sid in requested
        words = set(tokenize(" ".join([sid.replace("bosskuai-", "").replace("-", " "),
                                       *entry.get("triggers", [])])))
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
                 *(alias for alias, target in aliases.items() if resolve_skill_id(target, root) == sid)]
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
        elif selected and not explicit and not (terms - covered):
            reason = "does not cover another prompt concern"

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


def _routing_index(root: Path | None = None) -> dict:
    from bossku.index import build_index, index_is_stale, load_index

    return build_index(root) if index_is_stale(root) else load_index(root)


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
    from bossku.index import singular, tokenize

    ident = sid.replace("bosskuai-", "").replace("-", " ")
    id_tokens = {singular(t) for t in sid.replace("bosskuai-", "").split("-") if len(t) >= 2}
    triggers = entry.get("triggers", [])
    trigger_words = {w for t in triggers for w in tokenize(t)}
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


def write_routing_cache(dest: Path, root: Path | None = None, available: set[str] | None = None) -> None:
    """Mirror the routing index next to the install so hosts get triggers, not just names."""
    data = _routing_index(root)
    entries: dict[str, dict] = data.get("skills", {})
    allowed = (set(entries) if available is None else set(available)) - NOT_INSTALLED
    payload = {
        "version": data.get("version", "2.1.0"),
        "fingerprint": data.get("fingerprint", ""),
        "skills": [
            {
                "id": sid,
                "name": entry.get("name", sid),
                "description": entry.get("description", ""),
                "triggers": entry.get("triggers", []),
                "exclusions": entry.get("exclusions", []),
                "keywords": entry.get("keywords", []),
                "model_role": entry.get("model_role", "coder"),
                "pack": entry.get("pack", "bossku"),
                "user_invoked": bool(entry.get("user_invoked")),
            }
            for sid, entry in sorted(entries.items()) if sid in allowed
        ],
        "aliases": {alias: target for alias, target in load_aliases(root).items()
                    if resolve_skill_id(target, root) in allowed},
        "default_skill_id": COFOUNDER_SKILL,
        "selection_policy": {
            "alternative_groups": [sorted(group) for group in ALTERNATIVE_SKILLS],
            "note": "Choose one primary and complements for distinct concerns. Respect exclusions, "
                    "user-only invocation and runtime availability; read descriptions before loading.",
        },
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def make_path_writable(path: Path) -> None:
    """Add user-write permission without discarding existing mode bits."""
    try:
        os.chmod(path, path.stat().st_mode | stat.S_IWRITE)
    except FileNotFoundError:
        return


def make_tree_writable(path: Path) -> None:
    if not path.exists():
        return
    for child in path.rglob("*"):
        make_path_writable(child)
    make_path_writable(path)


def _remove_read_only(func, path: str, _exc_info) -> None:
    target = Path(path)
    make_path_writable(target)
    func(path)


def remove_tree(path: Path) -> None:
    """Remove a tree even when copied files carry Windows read-only attributes."""
    if path.exists():
        shutil.rmtree(path, onerror=_remove_read_only)


def copy_skills_to(dest_dir: Path, root: Path | None = None, profile: str = "full") -> list[str]:
    base = skills_dir(root)
    dest_dir.mkdir(parents=True, exist_ok=True)
    selected = _profile_skills(profile, root)
    short = load_lean(root)["descriptions"] if profile == "lean" else {}
    installed: list[str] = []
    for sid in selected:
        src = base / sid
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
    base = skills_dir(root)
    dest_dir.mkdir(parents=True, exist_ok=True)
    ids = [sid for sid in list_skill_ids(root) if sid not in exclude and sid not in NOT_INSTALLED]
    for sid in ids:
        target = dest_dir / sid
        if target.exists():
            remove_tree(target)
        shutil.copytree(base / sid, target)
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
        path = skills_dir(root) / sid / "SKILL.md"
    except FileNotFoundError:
        return "missing", None
    return ("repo", path) if path.is_file() else ("missing", None)


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
            parse_skill_md(skills_dir(root) / sid / "SKILL.md").description if sid in ids else "")
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


def _profile_skills(profile: str, root: Path | None) -> list[str]:
    if profile not in {"lean", "core", "full"}:
        raise ValueError("profile must be lean, core or full")
    if profile == "lean":
        base_dir = skills_dir(root)
        return [sid for sid in load_lean(root)["listed"] if (base_dir / sid).is_dir()]
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
        "malaysia-localisation",
        "bosskuai-taste",
    ]
    if profile == "core":
        base_dir = skills_dir(root)
        loop_ids = load_pack_skill_ids("loop-engineering", root)
        combined: list[str] = []
        seen: set[str] = set()
        for sid in [*core, *loop_ids]:
            if sid in seen:
                continue
            seen.add(sid)
            combined.append(sid)
        return [s for s in combined if (base_dir / s).is_dir()]
    return [s for s in list_skill_ids(root) if s not in NOT_INSTALLED]


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


def _broken_relative_links(skill_md: Path) -> list[str]:
    broken: list[str] = []
    for raw in _MARKDOWN_LINK.findall(skill_md.read_text(encoding="utf-8")):
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
    base = skills_dir(root)
    ids = list_skill_ids(root)
    vendored = load_vendored(root)
    custom = [sid for sid in ids if sid not in vendored]
    descriptions: dict[str, str] = {}
    body_words: dict[str, int] = {}
    broken_links: list[dict[str, str]] = []

    by_pack: dict[str, list[str]] = {"all": ids, "bossku": custom}
    for sid in ids:
        skill_md = base / sid / "SKILL.md"
        descriptions[sid] = parse_skill_md(skill_md).description
        body_words[sid] = len(re.findall(r"\b[\w'-]+\b", skill_md.read_text(encoding="utf-8")))
        pack = vendored.get(sid, "bossku")
        if pack != "bossku":
            by_pack.setdefault(pack, []).append(sid)
        for target in _broken_relative_links(skill_md):
            broken_links.append({"skill_id": sid, "pack": pack, "target": target})

    description_chars = sum(len(value) for value in descriptions.values())
    custom_description_chars = sum(len(descriptions[sid]) for sid in custom)
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
        "custom_descriptions_over_300_chars": sorted(
            sid for sid in custom if len(descriptions[sid]) > 300
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
        "user_invocable",
        "allowed-tools",
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


def validate_skills(root: Path | None = None) -> list[str]:
    errors: list[str] = []
    base = skills_dir(root)
    vendored = load_vendored(root)
    aliases = load_aliases(root)
    ids = set(list_skill_ids(root))
    for alias, target in aliases.items():
        if alias in ids:
            errors.append(f"alias {alias} conflicts with real skill folder")
        if target not in ids and target not in aliases.values():
            errors.append(f"alias {alias} points to missing skill {target}")
    for sid in sorted(ids):
        skill_md = base / sid / "SKILL.md"
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
        unknown = sorted(set(front) - KNOWN_FRONTMATTER_KEYS)
        if unknown:
            errors.append(f"{sid}/SKILL.md unknown frontmatter key(s): {', '.join(unknown)}")
        if sid not in vendored:
            for target in _broken_relative_links(skill_md):
                errors.append(f"{sid}/SKILL.md broken relative link: {target}")
    return errors
