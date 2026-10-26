---
name: bosskuai-issue-tracker-setup
description: "Use when configuring a repo's agent setup once: record where issues live (GitHub, GitLab, local markdown or other), the triage label vocabulary, and the domain-doc layout, then add an Agent skills block to CLAUDE.md or AGENTS.md."
---

# BosskuAI Issue Tracker Setup

Use this skill once per repo, before skills that read or write issues, so they know where issues live, which labels to use, and where glossary and decision docs sit. It is a guided conversation, not a script: explore, present findings, confirm, then write.

## How this differs from nearby skills

- **`issue-triage`**: scans an existing issue queue, dedupes and proposes labels. This skill sets up where the queue is and what the labels are called.
- **`bosskuai-github-workflow`**: day-to-day GitHub issues, PRs and Actions.
- **`bosskuai-jira-integration`**: working with Jira tickets through an API or MCP once Jira is chosen.
- **`bosskuai-project-flow-ops`**: execution flow across GitHub and Linear after setup.

## Workflow

1. Explore without assuming: git remotes, existing `CLAUDE.md` / `AGENTS.md` and any existing "Agent skills" section, `GLOSSARY.md`, `docs/adr/`, `docs/agents/`, a `.scratch/` folder, whether a triage skill is installed, and monorepo signals (workspace config, several packages with their own source).
2. Present what exists and what is missing. Take one section at a time, lead with the recommended answer, and skip sections the exploration already settled.
3. Issue tracker: propose GitHub or GitLab if the remote points there; otherwise local markdown files under a scratch folder, or "other" described in one paragraph (Jira, Linear and similar). Record in `docs/agents/issue-tracker.md`.
4. Triage labels (only if a triage skill is installed): offer the default role names (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix) and collect overrides only if the tracker already uses other names.
5. Domain docs: default to a single glossary and ADR folder at the repo root; offer a multi-context layout only when monorepo signals exist.
6. Draft the "Agent skills" block and each docs file, show them, and let the user edit.
7. Write after confirmation: edit the existing `CLAUDE.md` or `AGENTS.md` (never create the second one when one exists; ask which to create if neither does). Update an existing block in place instead of appending a duplicate.
8. If labels are configured on GitHub or GitLab, create the missing ones with the platform CLI only after the user agrees.
9. Tell the user what was written and that they can edit `docs/agents/*.md` directly later.

## Guardrails

- Creating labels or editing agent instruction files changes shared repo state: show the draft and get approval first.
- Do not overwrite the user's edits to surrounding sections.
- Check the installed CLI versions and flags (`gh`, `glab`) before running them.
- Leave pull-request-as-request-surface style flags at their defaults unless the user asks.

## Output format

```text
Found: [remote, instruction files, docs, triage skill, monorepo?]
Decisions: [tracker, labels, domain layout]
Files to write: [path, one-line purpose]
Agent skills block: [draft]
Next step: [approval or edits needed]
```

Adapted from mattpocock/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md (mattpocock/skills, MIT).
