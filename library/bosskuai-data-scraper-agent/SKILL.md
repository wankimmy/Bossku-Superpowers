---
name: bosskuai-data-scraper-agent
description: "Use when the task explicitly concerns data scraper agent. Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Runs on a schedule, enriches data with a free LLM (Gemini Flash), stores results in Notion/Sheets/Supabase, and learns from user feedback. Runs 100% free on GitHub Actions. Use when the user wants to monitor, collect, or track any public data automatically."
metadata:
  origin: ECC-adaptation
---

# Data Scraper Agent — portable workflow

Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Runs on a schedule, enriches data with a free LLM (Gemini Flash), stores results in Notion/Sheets/Supabase, and learns from user feedback. Runs 100% free on GitHub Actions. Use when the user wants to monitor, collect, or track any public data automatically.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-lead-intelligence`, `bosskuai-autonomous-loops`, `bosskuai-brand-voice`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Concepts.
2. The Three Layers.
3. Free Stack.
4. AI Model Fallback Chain.
5. Batch API Calls for Efficiency.
6. BAD: 33 API calls for 33 items.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the runtime and HTTP and parser library versions in the lockfile, the free model's name and limits in the provider's current docs, and the runner image in the workflow (pin it, not `ubuntu-latest`), each checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Complete the source “Workflow”, “Step 9: GitHub Actions Workflow” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Read the site's `robots.txt` and terms before the first run. On a 403 or a CAPTCHA page, stop that source, and do not work around it.
- Retry a 429 or 5xx with backoff and jitter, honour `Retry-After`, and cap the attempts. A retried write needs a key (source URL plus content hash), so it cannot save the same item twice.
- Validate each item's fields and types before storage, and fail the run when a page yields no items, so a changed page never writes blank rows. GitHub schedules can run late or drop some queued jobs under high load, and a public repo's schedule is disabled after 60 days without activity. Alert when a scheduled run is missing, and make each run safe to repeat, because a late run can overlap the next one.
- In the Step 9 YAML in `references/upstream/SKILL.md`, replace `runs-on: ubuntu-latest` with a pinned Ubuntu label from the [GitHub runner image list](https://github.com/actions/runner-images), checked at work time.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
