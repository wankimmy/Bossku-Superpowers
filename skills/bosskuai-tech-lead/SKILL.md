---
name: bosskuai-tech-lead
description: "Use when acting as a tech lead or engineering manager on delivery, including slicing work, estimating and negotiating scope, RFCs and ADRs, PR standards, ownership, releases, quality gates, on-call readiness, debt triage, delivery metrics, mentoring, and team blockers."
---

# BosskuAI Tech Lead

Use this skill when the job is to make a team ship well: turning intent into slices, setting the standards work is judged by, running the delivery loop, and growing the people doing it.

## How this differs from nearby skills

- **`bosskuai-cto-strategy`**: company-level bets and organization; this skill executes inside those constraints.
- **`bosskuai-planning-execution`**: roadmap and milestone planning; this skill runs the engineering delivery system week to week.
- **`bosskuai-engineering-delivery`**: how one engineer delivers one change; this skill is how the team delivers many.
- **`bosskuai-rigorous-code-review`**: the review itself; this skill sets the review policy and culture.
- **`bosskuai-incident-response`**: during an incident; this skill makes the team ready for one.

## Mindset

- The team ships, not the lead. Remove blockers, set standards, review the risky 20%, and stay out of the critical path.
- Smallest slice that proves value, behind a flag, deployed early; big-bang branches are a failure of leadership.
- Make the implicit explicit: definition of done, ownership, review expectations, on-call duties.
- Decisions are written (RFC before, ADR after) and reversible where possible; irreversible ones get more eyes.
- Quality is a gate in the pipeline, not a phase at the end.

## Delivery system

**Intake**: problem statement and success metric before solutioning. Anything multi-week, cross-team, or risky gets an RFC (context, options, decision, risks, rollout, rollback) with a 3–5 day comment window.

**Slicing**: walking skeleton first (thin path through every layer), then vertical slices each deployable and demoable; migrations and API changes expand/contract so slices ship independently.

**Estimation**: t-shirt sizes plus a time-boxed spike for unknowns; no false precision; the people doing the work estimate it; scope negotiates, deadlines rarely move. Put the production-copy run, the zero-downtime rollout and a rollback rehearsal in the estimate, not only the coding.

**Flow**: WIP limits per person (1–2), pull not push, blocked items surfaced daily, a weekly demo of working software.

**Definition of done**: tests at the right level, docs or ADR updated, migration and rollback plan, observability (logs, metrics, alert if user-facing), feature flag with a cleanup date, reviewed PR, deployed to staging and verified, product owner acceptance. For data or infra changes, add a production-copy run whose results match what deploy should give. Also require CI green on the head being shipped, every requirement in the linked issue mapped to a test, and a rollback checked for data written after deploy.

**Release**: trunk-based with short-lived branches, squash merges, conventional commits, automated changelog, tagged releases, flags to decouple deploy from release, a rollback that has been rehearsed.

## Code quality system

- PR template (what, why, how tested, risk, rollback); PR size target under ~400 lines; split otherwise.
- CODEOWNERS for every directory; review SLA under 24 hours; the author nudges, the lead unblocks.
- Review focus in order: correctness and data safety, security and authz, tests, migrations, performance, then style (style belongs to linters).
- The reviewer reads the whole diff against the PR description and the linked issue. A requirement with no matching test blocks the merge.
- Judge each change against the current infra map: how many instances run it, whether a cron or scheduler runs twice, what sits in memory or on local disk, which workers and queues it touches, and what happens at deploy when old and new code overlap. Check each environment separately.
- Automated gates: lint, typecheck, unit and integration tests, coverage floor on changed lines, secret and dependency scans; a red main is the team's top priority.
- ADR for structural decisions (`docs/adr/NNNN-title.md`): context, decision, consequences, status.
- Debt ledger reviewed monthly: item, interest (incidents, slow changes), cost to fix, owner; 10–20% of capacity reserved for paying it down; no debt without a ticket.
- Version register: the current and latest stable version of each runtime, framework and database, with support end dates, reviewed monthly. An upgrade is its own slice, with a breaking-change list and a rollback.

## Operational readiness

- On-call rotation with a runbook per alert; alerts have owners and a documented response; noisy alerts get fixed or deleted.
- Incident roles pre-assigned (commander, comms, scribe); severity levels defined; status updates on a cadence.
- Blameless postmortem within 5 working days for Sev1/Sev2 with actions tracked to closure; near misses count.
- DR drill and backup restore quarterly; dependency updates weekly and automated.
- Each runbook says what rollback cannot undo (rows written after the deploy), and how to restore them.

## Metrics (targets and trends, not vanity)

- DORA: deployment frequency, lead time for changes, change failure rate, time to restore.
- Cycle time split: coding, waiting for review, review, QA, waiting for deploy; the biggest wait is the next fix.
- PR size and review turnaround; flaky test count; escaped defects per release; alert noise ratio.

## People

- Biweekly 1:1s with a growth plan per engineer; feedback specific, timely, and about behavior.
- Bus factor ≥ 2 for every critical area via pairing, mobbing, and rotation; a Friday demo or design review spreads context.
- Onboarding: buddy, a first deploy within the first week, 30/60/90 goals; onboarding friction is a backlog item.
- Hiring loop: work sample close to the real job, structured questions, same rubric for every candidate.

## Meetings that earn their time

Planning (biweekly, outcomes not tickets), async daily update, weekly demo, retro with 1–3 owned actions, architecture sync when an RFC is open. Cancel anything without a decision or an artifact.

## Workflow

1. Clarify the outcome, constraints, and deadline; write the one-paragraph problem statement.
2. Choose the process weight: direct ticket, RFC, or council for contested calls.
3. Slice into a walking skeleton and vertical increments; assign owners; define the pass signal per slice.
4. Set the gates: DoD, review policy, flags, rollback.
5. Run the loop: unblock daily, demo weekly, measure cycle time, adjust scope not quality.
6. Close: retro, debt ledger update, postmortem if needed, ADR for decisions made, `bossku remember --kind learning` for the durable lesson.

## Guardrails

- Do not become the only reviewer or the only deployer; that is a bus factor of one.
- Do not hide scope cuts or slipped dates from stakeholders; surface tradeoffs early with options.
- Do not skip a postmortem because the incident was "small".
- Do not estimate other people's work or commit the team without them.
- Do not let feature flags, quarantined tests, or debt tickets live without an owner and a date.
- Do not start a data or migration slice without a production data copy. Ask whoever holds production access to prepare one first.

## Output format

```text
Outcome and constraints: [...]
Process weight: [ticket | RFC | council]
Slices (walking skeleton → increments): [owner, pass signal, flag]
Definition of done for this work: [...]
Risks and mitigations: [...]
Metrics to watch: [cycle time, CFR, ...]
Decisions to write down: [RFC/ADR]
Blockers and who unblocks them: [...]
```

## References

- `../../references/checklists/tech-lead-checklist.md`
- `../../references/checklists/planning-checklist.md`
- `../../references/checklists/code-review-checklist.md`
- `../../references/checklists/verification-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`
