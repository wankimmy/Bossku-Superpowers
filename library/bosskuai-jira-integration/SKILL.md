---
name: bosskuai-jira-integration
description: "Use when the task explicitly concerns jira integration. Use this skill when retrieving Jira tickets, analyzing requirements, updating ticket status, adding comments, or transitioning issues. Provides Jira API patterns via MCP or direct REST calls."
metadata:
  origin: ECC-adaptation
---

# Jira Integration Skill — portable workflow

Use this skill when retrieving Jira tickets, analyzing requirements, updating ticket status, adding comments, or transitioning issues. Provides Jira API patterns via MCP or direct REST calls.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-cybersecurity-risk`, `bosskuai-product-strategy`, `bosskuai-api-design`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Option A: MCP Server (Recommended).
2. Option B: Direct REST API.
3. MCP Tools Reference.
4. Direct REST API Reference.
5. Fetch a Ticket.
6. Fetch Comments.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. Then check these live at work time: whether the site is Jira Cloud or Data Center, which REST API version the code calls, and Atlassian's developer changelog for deprecated endpoints. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “4. Structured Analysis Output” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Read each issue's valid transitions from `/rest/api/3/issue/{key}/transitions` on Jira Cloud, or from `/rest/api/2/issue/{key}/transitions` on Jira Data Center, and send the transition ID it returns. Never hardcode a status name or ID: each project's workflow differs, and a transition can need required fields.
- Page through every result to the last page. Set explicit timeouts, and on a 429 wait for `Retry-After` before you retry. Mask the API token in logs.
- Test writes on a sandbox Jira site first. Look up custom field IDs (`customfield_...`) on each site, because they differ between sites. Fail loudly when a field comes back with another type.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
