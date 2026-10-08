# Agentic end-to-end tests: detail

The short checklist is in SKILL.md. This file holds what a job may need beyond it. It was written from a read of the open-source e2e project (tester-army/e2e, Apache-2.0, checked at commit f1a1ac24 on 2026-10-07; see `docs/third-party.md`); no text is copied. The CLI prints its own current guides, so prefer them when they differ.

## What e2e is

A TypeScript test runner. `agent.act` pursues one goal on the screen; `agent.assert`, `agent.waitFor` and `agent.extract` judge the screen; `screen`, `app`, `browser` and `expect` make exact interactions and checks. A replay cache reruns verified actions and compares their recorded end state without a model call, while agent judgments still run live. Engines: `@e2e-dev/web` (Playwright, browsers) and `@e2e-dev/mobile` (iOS simulators, Android emulators, connected phones). A test that takes only `app` can check an API with `fetch` and `expect`.

## Install and first run (ask the user first)

- Needs Node.js 24.8+, or 22.22.3+ on Node 22.
- `npx e2e init` scaffolds the config, an example test, `.gitignore` lines and agent skill/MCP entries. Manual route: `npm install --save-dev e2e @e2e-dev/web ai@^7`.
- Agent steps need a model in the config and that provider's sign-in or API key. Tests without agent steps need no model.
- Telemetry is on by default; `npx e2e telemetry disable` or `E2E_TELEMETRY_DISABLED=1` turns it off.

## Config shape

`e2e.config.ts` exports `{ targets, agents } satisfies E2EConfig` (type import from `e2e`). A UI target names an engine and the app beside it: `{ engine: web(), app: { url, command } }` where `command` starts the app and may name a log file. `agents.default` holds the model (an AI SDK instance), a `system` prompt for how the app works, and optional `context` for the vocabulary on screen. Config and tests are ES modules whatever `package.json` says.

## Topics (`npx e2e guide <topic>`)

| Topic | Read it when |
|---|---|
| `setup` | adding e2e, writing the config, starting the app, mobile targets |
| `writing-tests` | fixtures, locators, actions, matchers, sign-in sessions |
| `agent` | agent steps, model choice, cost and budgets, the replay cache |
| `running` | CLI flags, reporters, trace pages, `report.json`, exit codes, CI |
| `explore` | exploring toward a goal without a test file |
| `debugging` | a run failed: error codes, `--headed`, `--debug`, `--ai-trace` |
| `mcp` | driving the live app from a coding agent: `e2e mcp` and its tools |
| `bug-bash` | parallel `e2e explore` charters, merging findings, repro tests |

## Writing rules that prevent flaky tests

- Locators resolve when used; actions wait for readiness and `expect` retries. Plain reads such as `textContent()` fail at once on zero matches, and `count()` answers from the current screen, so use a matcher when a value has to settle.
- A locator matching two nodes fails with `LOCATOR_AMBIGUOUS`; narrow it by role and name.
- One goal per `act`, worded as the screen words it, with real values passed as params. When a step fails, tighten the goal first, then the context, then the agent.
- Secrets live under `credentials` and `secrets` in the config and are resolved with `credentials.user(name).password` and `secrets.get(name)`. They are separate namespaces. Hand the result only to `fill()` or `act` params.

## Bug bash loop

1. Pick charters (areas and goals), one per `npx e2e explore` run, and run them in parallel within the model budget.
2. Merge the findings and drop duplicates and anything caused by the test setup.
3. For each real finding write a repro test; run it and confirm it fails on the reported assertion. Only then change the app.
4. Report findings with the repro file, the command and the trace page.

## Cost and CI

Agent steps cost model calls the first time; the replay cache avoids them on reruns when the screen state matches. Set budgets before a bug bash. In CI run `npx e2e run` with the model key as a secret and keep `.e2e/results` as an artifact. Do not commit `.e2e/`.
