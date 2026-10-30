---
name: bosskuai-browser-automation
description: Use when doing browser-level testing, UI verification, automated user flow testing, visual regression, or scraping JavaScript-rendered pages. Covers QA smoke tests through full user journey automation.
---

# BosskuAI Browser Automation

## When to use

- Smoke-testing a web app after a deploy (console errors, network failures, CWV)
- Automated user flow testing (signup, checkout, onboarding)
- Visual regression checks at multiple breakpoints
- Verifying UI behavior that cannot be caught by unit or integration tests
- Scraping JS-rendered competitor or third-party pages
- Monitoring a live site for uptime or content changes

## How this differs from nearby skills

- **`bosskuai-integration-testing`**: covers API contracts, service-to-service calls, and backend integration correctness. Browser automation covers the browser layer — rendered UI, DOM interactions, network from the client perspective, visual output.
- **`bosskuai-rigorous-code-review`**: static analysis of code. Browser automation executes the running application.
- **`bosskuai-competitor-intelligence`**: strategic tracking of competitor changes. Browser automation is the execution layer that can serve that skill but has its own engineering focus (test stability, selectors, retries).
- **`e2e-testing`** (ecc): Playwright suites committed to the repo (page objects, config, CI); this skill runs ad-hoc QA passes, visual diffs, and scraping against a live URL.
- **`browser-use`** / **`remote-browser`**: an agent driving a browser interactively through the browser-use CLI; this skill produces repeatable scripts and a QA report.

## MCP requirements

| Tool | Role | Degradation |
|------|------|-------------|
| Playwright MCP | Browser automation (required) | Without Playwright MCP, provide script templates for manual execution |
| Chrome DevTools MCP (Google) | Runtime inspection, performance profiling, network analysis, accessibility audits (optional) | Without DevTools MCP, use Playwright's built-in tracing and Lighthouse CLI as alternatives |

Note: For headless scripting and CI, Playwright is required. Read its version from `package.json` and the lockfile (`npm ls @playwright/test` prints the installed one). Browser builds belong to that version, so run `npx playwright install` after an upgrade, and check the latest with `npm view @playwright/test version`.

## Workflow

Choose one or more modes based on the task:

### Mode 1 — QA Smoke Test
1. Navigate to the target URL and capture a full-page screenshot.
2. Check browser console for errors (level: error, warn).
3. Intercept network requests — flag any 4xx/5xx responses.
4. Measure Core Web Vitals (LCP, CLS; INP needs field data or a scripted interaction; hand CWV work to `bosskuai-web-performance`) if performance is in scope.
5. Verify critical above-the-fold elements are visible.
6. Output: pass/fail per check, screenshots, console log excerpt.

### Mode 2 — Interaction Testing
1. Map the user flow to test (e.g., signup → verify email → first use).
2. Write Playwright steps: fill inputs, click, assert DOM state.
3. Wait with locator assertions (`await expect(page.getByRole(...)).toBeVisible()`) or `waitForResponse`; never fixed sleeps or `networkidle`.
4. Test happy path first, then at least one error path (bad input, network failure).
5. Output: step-by-step pass/fail, failure screenshots.

### Mode 3 — Visual Regression
1. Define breakpoints (mobile 375px, tablet 768px, desktop 1440px minimum).
2. Take baseline screenshots if none exist; otherwise compare to stored baselines.
3. Flag pixel diffs above threshold (default: 0.1% of pixels changed).
4. Output: diff images, percentage change per breakpoint.

### Mode 4 — Competitor / Third-Party Monitoring
1. Confirm robots.txt allows crawling the target pages.
2. Set a respectful request rate (minimum 2s between requests).
3. Navigate and extract target data (pricing table, feature list, CTA copy).
4. Store a timestamped snapshot for delta comparison.
5. Output: extracted data, timestamp, diff from previous snapshot if available.

### Mode 5 — DevTools Profiling (requires Chrome DevTools MCP)
1. Open the target page in Chrome via DevTools MCP.
2. Record a performance trace during the critical user action (page load, scroll, interaction).
3. Capture memory snapshots to identify leaks or excessive allocations.
4. Run Lighthouse audits (performance, accessibility, best practices, SEO).
5. Inspect network waterfall for blocking resources, slow responses, or redundant requests.
6. Check console for errors and warnings with source-mapped stack traces.
7. Take responsive screenshots at mobile/tablet/desktop viewports.
8. Output: performance metrics, Lighthouse scores, network waterfall summary, console errors, accessibility findings.

## Output format

```
## QA Report — [Site/Flow] — [Date]

### Summary
PASS / FAIL / PARTIAL — one-line verdict.

### Results by section
| Check | Status | Notes |
|-------|--------|-------|
| Console errors | PASS | 0 errors |
| Network failures | FAIL | 2× 500 on /api/cart |
...

### Screenshots
[Attached / saved to path]

### Recommended actions
Numbered list of issues requiring fix, ordered by severity.
```

## Guardrails

- Never automate login to third-party services (GitHub, Stripe, Google) without explicit user confirmation — credential exposure risk.
- Rate-limit all competitor or external scraping (minimum 2s between requests).
- Respect robots.txt — check before scraping any external domain.
- Do not commit credentials, session tokens, or cookies to any file or log.
- Prefer `data-testid` or semantic selectors over CSS class chains; document selector rationale.
- All Playwright scripts must handle timeouts gracefully — no infinite waits.
- Visual regression baselines must be stored and versioned; never auto-approve large diffs without human review.
- Mocks (`page.route`) return production's types and shapes, including string money values and nulls. A cleaner mock hides the bug.

## Further reading

- `../../references/playbooks/browser-automation-detailed-playbook.md` — extended step-by-step workflow and detailed templates that complement this playbook.
- `../../references/checklists/engineering-quality-bar.md` — the shared bar: versions, data, deploy and proof.

## Post-deploy QA additions

- **Read-only by default.** Never run a mutating journey (checkout, payment, delete, mass update) against a production URL. It needs explicit user opt-in and a staging or preview URL. Use seeded test credentials, and redact credentials, tokens, and PII from screenshots before saving.
- **Smoke filters**: ignore analytics and third-party console noise when counting errors; report it separately as warnings.
- **Interaction sweep**: click every nav link (no dead links), submit forms with valid and invalid data (check both success and error states), and run login to protected page to logout with test accounts only.
- **Visual**: check dark mode if the app has it; flag layout shifts over about 5px, missing elements, and horizontal overflow. No stored baseline means INCONCLUSIVE, never a silent PASS.
- **Accessibility**: run axe-core (or equivalent) for WCAG 2.2 AA, plus keyboard navigation end to end, focus order, and landmarks. Automated runs cover only roughly 30-40% of WCAG, so a clean run is necessary, not sufficient; do not report "accessible" from it alone.
- **Rolling deploys**: old and new instances can serve the same users during a deploy. Run the smoke pass once the rollout has finished, and again after a short wait.
- **Locale and time zone**: run the money and date journeys with Playwright's `locale` and `timezoneId` options (for example `ms-MY` with `Asia/Kuala_Lumpur`), and once in a comma-decimal locale.
- **Data size**: run the journeys against a staging copy of anonymized production data with the same row counts, field lengths and data types. Traces, HAR files and screenshots then hold no real personal data. A flow that passes with three products can fail on the real catalog (pagination, long names).
- **Verdict line** at the end of the report: SHIP, SHIP WITH FIXES, DO NOT SHIP, or INCONCLUSIVE (with issue and blocker counts).

Adapted in part from ECC skills/browser-qa (affaan-m/ECC, MIT).
