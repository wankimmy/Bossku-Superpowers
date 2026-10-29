# Brief: auto-learn (ideas ported from autoharness)

Status: draft, waiting for the user's approval. Tier: large (memory, hooks, agent-written instructions).

Source studied: `tigerless-labs/autoharness` @ `697cf5e` (MIT, Copyright (c) 2026 ryan), local copy at
`C:/dev/Tenant-Management-System/skills/autoharness`. Ideas ported, no code copied as-is.

## Goal

On by default after `bossku install`, on Windows, macOS and Linux, for anyone who clones the repo:

1. Every working session is distilled automatically: lessons become **learned skills**; decisions and facts stay
   `bossku remember` notes.
2. Learned skills and their evidence live in the Obsidian vault (the configured memory dir), never in the code repo.
3. The learned library improves itself: patch before create, fix stale rules, fold near-duplicates, archive (never
   delete). It never touches hand-written, first-party or vendored skills.

User decisions (2026-10-28): port the ideas, not the plugin; lessons land as skills; auto by default; Obsidian.

## Design

| Part | What | autoharness idea |
|---|---|---|
| Store | `<memory_dir>/skills/<name>/SKILL.md` + `references/` + `ledger.jsonl`; archive under `skills/.archive/` | skill tree + ledger |
| Promoter | `bossku learn apply <intent.json>`, the only writer; actions `create`, `update`, `patch`, `remove_file`, `archive` (`absorbed_into`) | stage_skill + promoter |
| Lint | frontmatter (`name`, `description`, `category`, `learned: true`); trigger within first 60 chars; description ≤ 1024; body ≤ 25 non-blank lines; subfiles only `references/` `templates/` `assets/` (no `scripts/`), each pointed at from the body; size caps; slug names; no path traversal; safety regex scan; secrets via `bossku/redact.py` reject the intent; only `learned: true` skills can be changed; verbatim `evidence` required, saved as `references/evidence-<stamp>.md` | validate + skills_guard |
| Write | temp dir + `os.replace`, cross-platform | atomic rename |
| Trigger | new Python Stop hook `bossku learn-gate` (marker-owned, installed by default, works with Node or Python stop gate). Counts tool calls since the last `bossku learn` call in the transcript (no state file); at ≥ `BOSSKU_LEARN_EVERY_N` (default 50) it sends the agent back once: "run the learn pass". Every 5th pass asks for a consolidation pass instead. Off: `BOSSKU_AUTO_LEARN=off` | tool-call counter, curator cadence |
| Recall | `bossku session-brief` adds a grouped index of learned skills (one line each); `bossku skill-hint` also matches learned descriptions; `bossku learn show <name>` prints one and records a use in the ledger | session-start index, use counter |
| Rules | new skill `bosskuai-learn` (also `/learn` on demand): compare-first ladder, reconcile old vs new, fold with `absorbed_into`, rule-altitude bodies, consolidation section | reflector + curator contracts |
| Other hosts | Codex, Cursor, OpenCode get the instruction via AGENTS.md and the skill; no Stop hook there (stated in docs) | — |

Not ported (YAGNI): background child `claude -p` sessions, MCP server, transcript capture/redaction pipeline,
usage-rate auto-archive, desktop notifications. The learn pass runs in the user's own session instead.

## Files

New: `bossku/learn.py`, `skills/bosskuai-learn/SKILL.md`, `tests/test_learn.py`.
Edit: `bossku/cli.py`, `bossku/hooks.py`, `bossku/install.py`, `bossku/brief.py`, `bossku/hint.py`, `bossku/index.py`
(triggers), `skills/bosskuai-continuous-learning/SKILL.md` (ladder row), `skills/bosskuai-permanent-memory-orchestration/SKILL.md`
(line 62), `AGENTS.md` (Memory section), `docs/memory.md`, `docs/installation.md`, `docs/third-party.md`, `README.md`,
`CHANGELOG.md`.

## Conflict to resolve

`bosskuai-permanent-memory-orchestration` line 62 says a human reviews before a note becomes a skill. Proposed wording:
learned skills are a separate tier in the vault, marked `learned: true`, shown with their evidence; repo skills, rules and
AGENTS.md still need a human.

## Risks

- Persistent prompt injection: a lesson distilled from a web page or file becomes a standing instruction. Mitigation:
  safety scan, no scripts, evidence required, learned skills labelled as learned, user can read and edit them in Obsidian.
- Extra turn cost: one learn pass per ~50 tool calls in the user's session.
- No vault configured: falls back to the existing memory-dir rule, same as `bossku remember`.

## Acceptance

1. Fresh `bossku install` wires `learn-gate`; `bossku hooks uninstall` removes it; `BOSSKU_AUTO_LEARN=off` silences it.
2. Gate blocks once at the threshold, never twice in a row, never on a tiny session, never crashes a session.
3. Promoter rejects: bad frontmatter, late trigger, long body, unpointed subfile, `scripts/`, traversal, secret, unsafe
   pattern, editing a non-learned skill, archive into a missing umbrella. Accepts and lands the valid cases atomically.
4. Session brief lists learned skills; `learn show` reads one and logs a use.
5. Paths work on Windows (tests use `--home` / temp dirs).
6. `python -m bossku validate --root .` and `python -m unittest discover -s tests -v` pass.
