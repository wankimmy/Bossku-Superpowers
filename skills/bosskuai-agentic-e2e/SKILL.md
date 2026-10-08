---
name: bosskuai-agentic-e2e
description: "Use when writing or running agentic end-to-end UI tests with the e2e runner (e2e.config.ts, agent.act steps beside exact locators, web or mobile), exploring an app toward a goal, or bug-bashing a branch. Plain Playwright suites belong to e2e-testing."
---

# Agentic end-to-end tests (e2e)

For tests that mix agent goals ("upgrade the workspace to Pro") with exact checks on what the screen shows. e2e is a separate, optional Node tool; learn its current behaviour from `npx e2e guide <topic>` rather than from memory.

1. **Check it is there.** Look for `e2e.config.ts` (or `.mts`), an `e2e` entry in `package.json` and a `tests/**/*.e2e.ts` glob. If it is missing, tell the user what `npx e2e init` writes (config, an example test, `.gitignore` lines, skill and MCP entries; Node 24.8+ or 22.22.3+) and that the CLI reports usage telemetry unless `npx e2e telemetry disable`. Run it only after they say yes.
2. **Learn the screens before writing.** Read the components for roles, labels and button text, or open the page with `--headed`. A locator needs the accessible name the app really renders.
3. **Write one goal per `agent.act`.** Pin every outcome right after it with `expect` or `agent.assert`. Use exact values through `screen` and judge meaning, not phrasing (`toContain('Pro')`, not a sentence a model wrote). Never add a sleep: use a matcher that retries.
4. **Keep secrets out of test code.** Declare accounts under `credentials` and other sensitive values under `secrets` in the config; hand the opaque value only to `fill()` or `agent.act` params.
5. **Run one file, read the trace.** `npx e2e run tests/<feature>.e2e.ts`. On a failure open `.e2e/results/<test>/trace.md`, fix the locator, the expectation or the app, and run again. `.e2e/` is output: read it, never edit it.
6. **Bug bash.** Run `npx e2e explore` charters in parallel, merge the findings, and prove each with a repro test that fails on the reported assertion before any fix.
7. **Say what you ran.** List the commands, what passed, what failed and what you could not run (for example no model key).

Never run `npx e2e feedback`: it sends text to the e2e team, so do it only when the user asks. Topic guides, config shape, cost control and CI: read `reference.md` in this folder.
