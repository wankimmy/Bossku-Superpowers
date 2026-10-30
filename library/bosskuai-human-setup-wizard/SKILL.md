---
name: bosskuai-human-setup-wizard
description: "Use when a setup or cutover needs steps only a human can do (dashboards, credentials, CI secrets, one-off migrations): generate an interactive bash wizard that guides each stage and writes values to .env or CI."
---

# BosskuAI Human Setup Wizard

Use this skill to turn a tedious manual procedure into an interactive bash script that walks a person through it one stage at a time: open this page, click here, paste the value, confirm. Do not use it for steps the agent can do itself.

## How this differs from nearby skills

- **`bosskuai-claude-code-setup`**: configures the agent tooling for a repo, not a human walkthrough of third-party dashboards.
- **`bosskuai-ci-cd-pipelines`**: designs the pipeline; the wizard only collects the secrets and values it needs.
- **`bosskuai-homelab-network-setup`**: network design guidance rather than a scripted guided procedure.
- **`bosskuai-flox-environments`**: reproducible dev environments, not credential provisioning.

## Workflow

1. Scope. Read `.env.example`, `.env*`, README, compose files, framework config, and CI workflows. Every `secrets.*` or `vars.*` reference is a value the wizard may have to produce. For a migration, list current state, target state, and the irreversible steps between.
2. Confirm the ordered stage list with the user, including each value it produces: where the human gets it, where it is written (`.env`, a CI secret, both, or nowhere), and whether it is secret.
3. Map each stage as a precise path, such as "Dashboard, Developers, API keys, reveal test key, copy". If you do not know the current UI or command, say so and check the docs or ask. Do not invent steps.
4. Write the script. Define a small helper block once at the top: `stage` (clear screen, show "stage N of M"), `say`, `open_url` (macOS, Linux, WSL, Git Bash), `pause`, `confirm` (y/N), `ask`, `ask_secret` (hidden input), `write_env` (idempotent upsert, file mode 600), and optional `set_secret` / `set_var` via the `gh` CLI with a fallback message. End with a summary of what was configured.
5. One focused task per stage, in dependency order. Open the URL before asking for its value. Use hidden input for secrets. Persist every value that needs persisting. Put a `confirm` before any irreversible action.
6. Verify without running it end to end (it opens browsers and waits for people): `bash -n script`, `shellcheck` if installed, `chmod +x`. Trace statically that each captured value lands where step 2 said and that every CI secret name matches the workflow reference exactly.
7. Hand off: tell the user how to run it. Treat the script as disposable unless they want a repeatable setup path in the repo; then link it from the README.

## Guardrails

- Never print secrets, put them on the command line, or commit a populated `.env`.
- The wizard must not make payments, delete resources, or change production without a clear on-screen confirm and the user's explicit approval of the stage.
- Re-runs must be safe: offer the existing value as default and upsert instead of appending.
- State assumptions about third-party UIs; they change.

## Output format

```text
Stages: [n, name, URL, human action]
Values: [name, source, destination, secret?]
Irreversible steps: [list with confirm gates]
Checks run: [bash -n, shellcheck result]
How to run: [command]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from skills/skills/engineering/wizard/SKILL.md (mattpocock/skills, MIT).
