# Human-centred design upgrade: what changed and what is proven

Written on 2026-11-17, before commit. Evidence is a file and line in the working tree, `git show HEAD:<path>`, command output from this session, or a report from the model agents that built and reviewed the work (workflow journal, attributed). Anything else is marked "not verified". Nobody looked at a real product screen as part of this change.

## What was asked

The owner decided on 2026-11-17 to classify the product before choosing a design direction. Creative and marketing sites may use the Awwwards house rule. SaaS, ERP/CRM/HRMS, dashboards, internal tools, e-commerce, mobile and learning apps put familiarity first. Engagement must serve the user's goal: no fake urgency, fabricated social proof, guilt notifications, punitive streaks, hidden cancellation or compulsive loops, and no claim that a mechanism releases dopamine or guarantees retention. A global `overflow-x: hidden` must not hide a layout defect. No visual check or human reaction may be claimed that did not happen.

## What the audit found

Evidence is the text at HEAD. Five model audits found these.

| Conflict or gap | Evidence at HEAD | What answers it now |
| --- | --- | --- |
| Same rule written differently | `antislop/SKILL.md:299-300` "Large text (18px+)" against `bosskuai-design-systems/SKILL.md:80` "24px, or 18.7px bold"; tap target "(44px)" against `accessibility/SKILL.md:41` "24x24 CSS pixel" | `skills/bosskuai-ui-ux-design-to-code/SKILL.md:29-34`: "These win where a vendored design skill gives a different number". The width set is at `:14`; `layout-reliability-checklist.md:37`, `reference.md:78` and `bossku/init_project.py:102` repeat the same seven widths |
| Showcase gates forced on product UI | `hooks/session-start.mjs:40` "Design default is Awwwards style"; `agents/designer.md:48` "Pass needs the `jury` estimate in the Site of the Day band" | `agents/designer.md:48`; `skills/bosskuai-taste/SKILL.md:14-15` |
| One default in the canonical rule file | `AGENTS.md:49` "Design default is Awwwards style" | `AGENTS.md:49` now says "Classify the product before choosing a design direction" |
| No owner for a consumer mobile app | `bossku/design.py:13` word list has no "app" | `bossku/design.py:57` `APP_REMINDER`; `agents/designer.md:15`. The router part is still open |
| Only screenshots were executable | `scripts/shot.mjs:70-73` two viewports | `scripts/layout-check.mjs` (new) |
| ERP and SaaS dashboards routed to a monitoring skill | Routing facts: "Build a modern ERP dashboard" went to `bosskuai-dashboard-builder` | `bossku/index.py:882-890`; see Routing |
| Vendored marketing skills push pressure | `churn-prevention/SKILL.md:131` "Time-limit the offer"; `popups/SKILL.md:405` "Add countdown timers to create urgency"; `marketing-psychology/SKILL.md:169` "Pre-select the plan you want" | Vendored files untouched. `docs/third-party.md:88-97` lists the lines; `engagement-ethics-checklist.md:3` says it wins over any loaded skill |
| No always-on engagement rule | a grep of HEAD `AGENTS.md` found no manipulation, dark pattern, urgency, streak or engagement text | `AGENTS.md:84-86` "Engagement ethics (always on)" |
| "Familiar first" only in a reference file | `ui-ux-design-to-code/reference.md:45`; `SKILL.md:15` "Hold the Awwwards craft bar, the default style" | `SKILL.md:12` "Familiar first"; `bosskuai-taste/SKILL.md:203-215` |

## The rule now, and where it lives

- **Showcase web** (marketing, landing, portfolio, agency): the Awwwards house rule, jury score.
- **Task-first public pages** (storefront, checkout, docs, pricing): familiar patterns, native scroll.
- **Product UI** (SaaS, ERP/CRM/HRMS, dashboards, internal tools): the project's design system first, no jury.
- **Consumer and mobile apps**: platform conventions first, then the product UI rules.

| Place | Quote | Status |
| --- | --- | --- |
| `AGENTS.md:49`; `hooks/session-start.mjs:40`; `agents/designer.md:15` | "Classify the product before choosing a design direction" (AGENTS, session-start); "Classify the product first" (designer) | agrees |
| `skills/bosskuai-taste/SKILL.md:14-15`; `ui-ux-design-to-code/SKILL.md:17-20` | "no concept card, signature moment or jury band"; "Product UI: the project's design system and component library first" | agrees |
| `bossku/design.py:44-63`; `docs/routing.md:11`; playbook line 3 | Five reminder strings; "follows the type of the thing redesigned"; "Operational products put familiarity first." | agrees |
| Jury scope: `taste/SKILL.md:11`, `ui-ux-design-to-code/SKILL.md:17`, `bossku/design.py:45-46`, `docs/routing.md:7`, `agents/designer.md:46`, `session-start.mjs:40` | "on a public URL or a local production build" (the hook says "a public URL or a local build"). `AGENTS.md:49` says only "a `jury` score" | agrees |
| Layout check exit 0: `ui-ux-design-to-code/SKILL.md:14`, `designer.md:46`, `layout-reliability-checklist.md:37`, `layout-check.mjs:8` | "Exit 0 means no errors (read any warnings)"; "exit 0 no errors"; "Exit 0 means no errors (read any warnings it lists)"; "Exit 0: no error". Warnings do not change the exit code (`layout-check.mjs:242-245`) | agrees |
| Concept Card file: `taste/SKILL.md:49`, `taste/SKILL.md:221`, `designer.md:41` | "Concept Card in `DESIGN.md` (in the spec for a one-off page)"; "in the spec for a one-off page"; "for a one-off page, write no file" | agrees |
| Check command path: `layout-reliability-checklist.md:34`, `ui-ux-design-to-code/SKILL.md:14`, `designer.md:46`, `session-start.mjs:48` | `node <BosskuAI install>/scripts/layout-check.mjs <url>` in the three documents; the hook prints the full install path | agrees |

## From evidence to guideline

The playbook and the two checklists use these sources. Ids and classes are as the research input gave them; the playbook words some differently (P1 "company-reported A/B test").

| Id | Evidence class | Guideline it supports | Written in | Stated limit |
| --- | --- | --- | --- | --- |
| M1 | professional design guidance | Autonomy, competence, relatedness as user goals | Playbook 3 | Secondary summary; education results |
| M2 | meta-analysis or systematic review | Light gamification only in learning | Playbook 4 | Learners only; no retention outcome |
| M6 | professional design guidance | When behaviour fails, cut effort first | Playbook 3 | A framework, no evidence it works |
| P1 | published industry A/B test | Small daily action separate from a bigger goal | Playbook 4, 6 | One app; no sample size or significance test |
| P2 | observational evidence | Limited streak freeze; flexible streaks; celebration kept for real milestones | Playbook 4, 5, 6; ethics checklist 3 | One company; design not described |
| P3 | company description without data | A shared streak is worth testing, not assuming | Playbook 3, 4 | One 22% relative figure, no baseline |
| P4 | company description without data | Time-boxed challenges with visible rules | Playbook 4 | Rules only; no outcome data |
| U1 | professional design guidance | Exits, undo, plain errors, system status | Playbook 3, 5 | Expert evaluation, no outcome comparison |
| U2 | professional design guidance | Polish raises perceived, not real, usability | Playbook 2 | Forgives minor problems only |
| U3 | observational evidence | About five users per round, repeated rounds | Playbook 7 | Qualitative tests only |
| U5 | professional design guidance | Three to five top destinations on mobile | Playbook 1 | Android Material only |
| U6 | standard or regulation | Reflow at 320px, 200% text, 24px target floor | Layout checklist, Prevention | Thresholds vary by level |
| C2 | observational evidence | Mark required and optional fields | Playbook 1 | Own rubric; no sample sizes |
| C4 | professional design guidance | Layout shift good is below 0.1 (reserving space is the checklist's own advice) | Layout checklist, Prevention | Google targets only |
| C5 | professional design guidance | Pixel baselines catch change, not quality | Layout checklist, The check | Environment-specific |
| E1 | company description without data | Definition of a dark pattern | Ethics checklist, intro | 2022 report not read |
| E2 | company description without data | Named tactics: false countdowns, hard cancellation | Playbook 4; ethics checklist, intro and 5 | Staff report not read |

Sources marked not read, which support no guideline: M3, M4, M5, U4, C3. The playbook lists them in its source table. Playbook line 63 prints the five HEART names under the C3 tag; the research input says they come from outside the source and are unverified. C1 was read but no guideline cites it.

Reading caveat: most sources were read through a fetch-tool summary, not the original text. Figures such as 22% and 0.1 are as that reader reported them.

## Checks an agent can run

`scripts/layout-check.mjs <url>` opens a page in Playwright and runs six checks: `page_overflow_x`, `hidden_overflow_x`, `element_overflow`, `clipped_text`, `overlap` and `small_target` (lines 171-226). A `coverage` warning appears when a page holds more than 5,000 elements and the first 5,000 were measured (`:84`, `:148`, `:229`). Default widths: 320, 375, 390, 768, 1024, 1440, 1920 (`:17`). Exit 0 means no error, 1 means an error, 2 means the check could not run (`:8`); an HTTP status of 400 or more also gives 2 (`:297`). Only http and https URLs are accepted.

I ran `node --test tests/layout-check.test.mjs`: 26 tests, 25 pass, 0 fail, 1 skipped. The skipped one is the end-to-end test; Playwright cannot be resolved here because this repo has no `package.json`.

Reported by the fixer (not re-run by me): with Playwright from another project and local fixture pages, 26 of 26 pass. The real-browser runs used widths 320 and 1024 only (`tests/layout-check.test.mjs:263-272`); the script launches Chromium only (`:282-285`). On `broken.html` at 320px it reports exit 1 with `page_overflow_x` 3, `hidden_overflow_x` 1, `element_overflow` 2, `clipped_text` 1, `overlap` 2 and `small_target` 1. On `clean.html` it reports exit 0. A 404 page gave exit 2. No real-world page and no screenshot was used.

`scripts/shot.mjs <url> --widths 320,768` adds one screenshot for each width the check flagged, beside the fixed 390 and 1440 (`scripts/shot.mjs`, function `viewports`; test in `tests/hooks.test.mjs`). A real run in this session, with Playwright from another project and the clean fixture page, wrote four PNG files (390, 1440, 320, 768).

Stays a human judgement: whether the design is good or familiar, focus order, motion, and whether a screenshot was looked at.

## Routing

Numbers are the orchestrator's own lab runs, as written in its facts file.

| Variant | 18 design prompts right | Result on 1,392 labelled prompts | Decision |
| --- | --- | --- | --- |
| before | 9 | baseline | |
| phrase triggers on the UI skill | fixed 6 product prompts | took over a bug report and a pricing question | rejected |
| exclusions on `bosskuai-dashboard-builder` only | 9 | 0 better, 0 worse | not enough |
| plus "erp", "crm", "hrms" triggers | 10 | 0 better, 0 worse | shipped |
| plus "saas" trigger | 11 | 0 better, 0 worse, 0 changed | shipped |

After shipping: `scripts/benchmark_routing.py` 101 of 101 top-1; held-out benchmark 88% top-1 on 328 prompts, unchanged.

Still wrong, 7 of 18: dr-p03 (to `revops`), dr-p04 (`bosskuai-saas-billing-ops`), dr-p05 (`bosskuai-archify-diagrams`), dr-p06 (`antislop-layoutmobile`), dr-n04 (the UI skill), dr-n05 (`bosskuai-mongodb`), dr-n06 (`free-tools`). "Build a mobile language-learning app" still goes to `bosskuai-mobile-app-release`.

The design reminder is separate from the router. I called `bossku.design.design_reminder` on eight prompts: the ERP, SaaS and CRM dashboard prompts gave the product line, the portfolio the showcase line, the mobile learning app the app line, the checkout page the task-first line. The CRM prompt was the short form "design the CRM dashboard for our sales team". The full dr-p03 prompt, with "they need pipeline and tasks at a glance", first returned no reminder, because a bare "pipeline" was in the not-design word list. The list now holds only build, data, release and ETL pipelines, with a test for the CRM prompt (`tests/test_design_default.py`), and dr-p03 returns the product line. dr-p04, dr-p05 and dr-p06 return the product line.

## Review record

Reviewers and fixers were models, not people.

| Package | Reviewer verdict | Findings | Fix result |
| --- | --- | --- | --- |
| references-and-ethics | changes required | 1 P1, 4 P2, 3 P3 | The fixer reports all 4 P2 and 2 P3 resolved. The P1 was in a file it did not own (`design-systems-detailed-playbook.md:87`); the orchestrating session changed that line to 24px regular or about 18.66px bold, and changed the exit-0 wording at `ui-ux-design-to-code/SKILL.md:14` to "Exit 0 means no errors (read any warnings)". Not re-reviewed by the package reviewer |
| layout-check | changes required | 0 P1, 7 P2, 3 P3 | The fixer reports all 7 P2 and all 3 P3 changed; the third P3 (small links in a nav) has no probe and stays unverified. The orchestrating session changed the check command in `layout-reliability-checklist.md:34` and `ui-ux-design-to-code/SKILL.md:14` to the install path. Not re-reviewed by the package reviewer |
| direction-and-gates | changes required | 3 P1, 5 P2, 3 P3 | The fixer reports all 3 P1 and all 5 P2 fixed, 2 P3 changed and 1 P3 needing no change. Its runs: `tests.test_design_default` 11 tests OK; a wider run of 222 tests had 1 failure, a stale `skills/skill-index.json`, left for the orchestrator. Still open by its report: router triggers for storefront and mobile-app prompts. The orchestrating session then made the jury wording the same in six places, moved `docs/skills.md:72` and `agents/executor.md:92` to the product-type rule, and added `--widths` to `scripts/shot.mjs`. Not re-reviewed by the package reviewer |

## Limits

- No human usability test and no inspection of a real product screen.
- The layout check ran on fixture pages only, per the agents' reports.
- Engagement guidance and retention: a hypothesis. Sources not read support nothing.
- The 18 routing prompts were written by one model.
- `jury` cannot score a page behind a login: `skills/jury/SKILL.md:43`.
- Not verified: the routing numbers (taken as written); that the mobile prompt had no design reminder at HEAD (I ran the HEAD copy of `design.py` on it: None); No package was re-reviewed by its own reviewer after its fix; a separate pre-release review of the whole change ran afterwards.
- The design reminder goes silent on a design prompt that holds a not-design word such as "test", "api" or "database". The "pipeline" case (dr-p03) is fixed.

## Planned design evaluation (not run)

It needs a budget decision. Plan: six briefs (ERP dashboard, storefront checkout, mobile language-learning app, existing SaaS dashboard, agency portfolio, streak feature); the last release against this tree; three trials per brief per arm; observable rubric items (product type named, design system used, states present, layout check result, screenshots named as looked at, no refused tactic, no false claim of a visual check); a second model scores, with a human spot check. A difference counts only if the same direction shows in two of three trials on five of six briefs with a mean gap of two rubric items. Otherwise report "no difference shown".
