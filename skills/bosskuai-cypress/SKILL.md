---
name: bosskuai-cypress
description: "Use when writing, fixing, running or explaining Cypress tests in a project that uses Cypress (cypress.config files, cy.* commands, cy.intercept, cy.session, a flaky Cypress spec). Playwright suites belong to e2e-testing; agent-driven UI goals belong to bosskuai-agentic-e2e."
---

# Cypress tests

Cypress is MIT-licensed ([repo](https://github.com/cypress-io/cypress)). Ground each step in the docs page it cites; Cypress changes between releases.

1. **Check it is there.** Look for `cypress.config.ts` (or `.js`) and a `cypress` entry in `package.json`. If it is missing, show the user `bossku tools install cypress` and run it only after a clear yes.
2. **Learn the app first.** Read the components or open the page for the real text, roles and test attributes. A selector must match what the app renders.
3. **Select by test attribute.** `cy.get('[data-cy="submit"]')` is the docs' "always best" choice because the attribute does not change with CSS or JS behaviour. Use the project's own attribute if it has one ([best practices](https://docs.cypress.io/app/core-concepts/best-practices)).
4. **No fixed waits.** Wait on an aliased request (`cy.wait('@getOrders')`) or on an assertion that retries ([best practices](https://docs.cypress.io/app/core-concepts/best-practices), [cy.intercept](https://docs.cypress.io/api/commands/intercept)).
5. **Stub the network with `cy.intercept`** when the test should not depend on a live API ([cy.intercept](https://docs.cypress.io/api/commands/intercept)).
6. **Log in with code.** `cy.session` caches cookies, localStorage and sessionStorage. If `validate` fails on a restored session, `setup` runs again; if it fails right after `setup`, the test fails. Sessions are not kept across spec files by default ([cy.session](https://docs.cypress.io/api/commands/session)).
7. **Keep tests independent.** Each test sets up its own state and does not rely on an earlier test ([best practices](https://docs.cypress.io/app/core-concepts/best-practices)).
8. **Keep secrets out of specs.** Read sensitive values with `cy.env()` ([best practices](https://docs.cypress.io/app/core-concepts/best-practices)). Do not pass `--record` or set `CYPRESS_RECORD_KEY` unless the user asks: it sends results to Cypress Cloud and needs a project set up for recording ([command line](https://docs.cypress.io/app/references/command-line)).
9. **Run the spec you changed.** `npx cypress run --spec "cypress/e2e/<file>.cy.ts"`. Add `--component` for component specs and `--browser chrome` (or another installed browser), because Electron is deprecated as a test browser ([command line](https://docs.cypress.io/app/references/command-line), [install](https://docs.cypress.io/app/get-started/install-cypress)). Leave `npx cypress open` to the user: it launches the Cypress App so a person can choose tests ([install](https://docs.cypress.io/app/get-started/install-cypress)).
10. **Say what you ran.** List the commands, what passed, what failed, and what you could not run.

## Windows notes

- `CYPRESS_CACHE_FOLDER` must exist every time Cypress launches ([advanced installation](https://docs.cypress.io/app/references/advanced-installation)).
- In PowerShell, quote comma-separated values: `--env "host=api.dev.local,port=4222"` ([command line](https://docs.cypress.io/app/references/command-line)).
- Cypress sends crash reports (exception data) to `api.cypress.io` by default. `CYPRESS_CRASH_REPORTS=0` in the environment turns that off; set it before installing, and tell the user before an install if they care about privacy ([advanced installation](https://docs.cypress.io/app/references/advanced-installation)).
- The npm install downloads the Cypress binary by default. `CYPRESS_INSTALL_BINARY=0` skips that download, and `npx cypress install` fetches it later ([advanced installation](https://docs.cypress.io/app/references/advanced-installation)).
