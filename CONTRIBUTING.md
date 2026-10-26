# Contributing

Bossku Superpower is a toolkit-only repo: skills, agents, CLI, and docs.

## Changes

1. Keep `AGENTS.md` tool-neutral and concise. It loads in every session, and `validate` fails above 16,000 bytes (UTF-8), which keeps it inside the 16,384 bytes Devin loads automatically.
2. Add or edit skills under `skills/<id>/SKILL.md` with YAML frontmatter; `name` must equal the folder name. A niche skill that no profile should list goes under `library/<id>/` and into `skills/library-only.json` (plugins list every folder in `skills/`). `allowed-tools` may pre-approve read-only commands only: `bossku validate` rejects a bare `Bash` or a catch-all such as `Bash(git:*)`.
3. Register deprecated names in `skills/aliases.json` instead of duplicating folders.
4. The 27 skills in `skills/lean.json` each have three `claude plugin eval` cases in [`evals/`](evals/README.md). Keep them in step when you rename or replace one; `tests/test_plugin_evals.py` checks it.
5. Run before opening a PR:

```bash
pip install -e .
python -m bossku validate --root .
python -m unittest discover -s tests -v
```

## Archive

Product MVP code lives on `archive/product-mvp-2026-07`. Do not reintroduce Laravel/Nuxt/Docker surfaces on `main` without an explicit decision.

## GitHub repository (About)

Use this on **Settings → General → Description** (max 350 characters). It describes toolkit `main`, not the archived Ollama/dashboard product.

**Description (recommended):**

```text
Skills and tools that make your AI coding agent do better work: it finds the right skill, runs its own code, remembers your project's rules and keeps notes in Obsidian. 670+ skills and optional tools for Claude Code, Cursor, Codex, OpenCode and OMP. MIT.
```

**Shorter alternative:**

```text
Skills and tools for AI coding agents: right skill, tested code, remembered rules, Obsidian notes. 670+ skills. MIT.
```

**Topics:** `ai-agents`, `agent-skills`, `claude-code`, `cursor`, `codex`, `opencode`, `obsidian`, `developer-tools`, `mit-license`

Do not use “approval gates”, “run dashboard”, or “Local-first (Ollama)” on `main` unless the About text targets `archive/product-mvp-2026-07` instead.
