---
name: bosskuai-agent-runtime-gateway-smoke-test
description: "Use when the task explicitly concerns agent runtime gateway smoke test. Verify a local agent API, temporary gateway tunnel, and remote sandbox callback with a tool-free task, then restore the original app connection."
metadata:
  origin: ECC-adaptation
---

# Agent Runtime Gateway Smoke Test — portable workflow

Verify a local agent API, temporary gateway tunnel, and remote sandbox callback with a tool-free task, then restore the original app connection.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-autonomous-loops`, `bosskuai-prompt-injection-defense`, `bosskuai-agent-introspection`, `verification-before-completion`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Required Inputs.
2. Authorization and Cleanup.
3. Smoke Test.
4. Connected Tool Follow-up.
5. Failure Handling.
6. Output Contract.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions (from its manifest, lockfile or runtime), the local agent API version, the tunnel tool's version and the sandbox provider's current docs, all checked live at work time. Do the source prerequisites first. Record the versions in the output. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Output Contract” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Use a tool-free task. The sandbox gets no real credentials, customer data or production systems.
- Test the callback path with a slow response and with a tunnel that drops mid-task. Say whether a retry can repeat a side effect.
- Mask tokens in logs, and after the restore, check that the original app connection works again.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
