---
name: bosskuai-rigorous-code-review
description: "Use when doing PR or pre-merge review, adversarial review, or challenging an implementation, a docs or rules change, or a plan: skeptical expert review of correctness, intended outcome and downstream impact that prefers minimal fixes."
---

# Rigorous code review

Assume the change is wrong until the code, tests and callers show otherwise. Review the change, do not rewrite the system. A review request allows analysis only: do not edit files, post comments or submit a review unless asked (a self-review of your own diff asks for fixes, per AGENTS.md Self-review; posting and submitting still need the ask), and keep any reproduction in a scratch copy (no installers or machine-wide changes).

**Size the review first and name the tier in the verdict.** When unsure, pick Full; a Light change that turns out to touch behaviour moves to Full.

- **Light:** a small change with no behaviour change (dead code removal, copy text, comments, config that changes nothing at runtime). Search for leftover references and the same pattern elsewhere, read the CI logs, check the merge with the base, and run the one path it touches. Step 4 still covers every category, briefly.
- **Full:** business logic, data writes, permissions, API contracts, migrations, UI flows or layout. Run every step below, including the checks marked "Full tier", and the methods in `full-tier.md` (requirements ledger, whole-feature trace, fail-first and broken-guard runs).

**Rules that decide the verdict:**

- **Before and after.** For every finding, check the base version of that exact line (`git show <base>:<file>`, or the `-` and `+` lines of the diff) and say whether this change introduced it. A line that was already there is at most an optional nit or a follow-up issue, even when the new code sits next to it. Only lines the change adds or edits, or behaviour it breaks, can be P0 to P2.
- **Small fixes belong in this PR.** A fix on a line the PR adds or changes, or a check the linked issue asks for, is an ask in this PR (P2 at least), however small. Keep "optional" for things outside the PR's lines and scope.
- **CI.** Any failing or pending check, required or not, means no approval, even a known flake fixed elsewhere (step 3).
- **Merge conflicts.** Check mergeability at the start and again before posting (`gh pr view <n> --json mergeable`). A conflicting PR gets Request changes that tags the author and names the conflicting files, even when the code is clean ("code looks good; approve once the conflict is resolved and CI is green on the new head"). Never approve it with a "before merge" line, and never resolve it yourself unless asked.
- **Findings to fix mean Request changes,** posted as a review, never as a plain comment or "approve with comments".
- **Confusing UI is a fix, not a nit** (step 4, UI/UX).
- **Docs and rules changes:** a statement that is right but covers fewer cases than the code (another state, role or precondition), or a catalog row the paired code change makes stale, is an ask with suggested wording, not a nit. Wording taste alone stays a nit or nothing.

**Steps:**

1. **State the intended outcome** from the request, the PR description and the linked issue (Linear, GitHub), and what is deliberately deferred. Check that the description matches the diff, and that each requirement in the issue is met by the code, quoting the requirement. If intent is unclear, label your assumption and carry on. Full tier: write the requirements ledger first (`full-tier.md`).
2. **Read the evidence, not just the diff:**
   - the whole PR diff against its base (a re-review reads all of it, not only the new commits), the callers, the tests, the types or schemas, and the config or infra it touches
   - the project's current infra architecture (instances, workers, queues, data stores, environments, deploy path), so you judge the change against how it really runs
   - the versions it runs on, from the manifest, lockfile or runtime; check the latest stable live (shared bar section 2) and flag any API the change uses that the installed version does not have
   - a vendored or generated file in the diff: review its source or regeneration, since a hand edit gets overwritten
   - pin the round: record every PR's head SHA and its base tip, and read code the PR does not change at the base tip, not the head. Full tier: review every PR of the issue as one change, with a trace and a reverse check (`full-tier.md`)
3. **Check CI and the PR's own proof** on the head you review.
   - Run `gh pr checks <n>` (or read the pipeline) and open each failing log. A failing check is Request changes: name the check, its log line and a file:line. Use the code line the log points to. If the log gives none (for example a job timeout or runner cancel), use the workflow file:line that runs the failing step, and trace that step's command to the code it runs before requesting changes. A pending check is not a verdict yet: say "approve once <check> is green".
   - A green tick alone is not enough: open the lint and test logs and confirm they ran on the changed files (lint scope, test count, the changed spec or test names). A skipped job or zero collected tests proves nothing, so it is not a pass.
   - Open every screenshot or recording in the PR: it shows this change and matches the code, covers the states and screen sizes the repo asks for, and its before and after are like for like.
   - Run the branch yourself on a local setup and walk the path it changes. A UI change with no proof is a finding, unless your own run of the branch verified it; then say what you ran instead.
4. **Go through every category; none is skipped.** If one needs something you do not have (a production data copy, access, the linked issue, screenshots), ask the user to prepare it; until it arrives, the verdict is "Provisional (missing: <input>)" and nothing is approved. A category that cannot apply is marked "not applicable: <reason>", which is not a skip:
   - correctness: edge and boundary values, empty and null, ordering, race conditions (two users or jobs on the same row, double submits, check-then-act, queue retries), idempotency, partial failure, retries; walk every scenario that can reach the change through the code (shared bar section 3) and name any left untested. Hardest axes here: another tenant or role, a double submit or retry, old and new code side by side at deploy
   - business logic: rules and state changes that clash with existing flows, roles or data (detail: `reference.md`)
   - data: run the change against a masked production data copy (personal data and secrets masked), never production, and match production data types and shapes, such as "0.01" text vs 0.01 number (detail: shared bar section 4). A screen or endpoint that lists data is never "not applicable" here. Full tier: start with generated data in the shapes that break things (long text, unicode, null, empty lists, records saved before the change); use a production copy only with the user's OK, and let only counts, errors, plans and timings leave it, never rows with personal data (not in screenshots, page text or prompts)
   - API integration (when the change calls or serves an API): endpoint down or slow, retries, extra, missing or retyped fields, and logging with secrets and personal data masked (full list: shared bar section 5)
   - UI/UX (when the change touches a screen, message or flow): read each screenshot and the template as the user would. A message, warning or label that is wrong for that state, contradicts the result, or leaves the user unsure what happened or what to do next is a finding to fix, not a nit (severity per the UI/UX rule in `reference.md`, step 4). So is a state with no feedback, a disabled control with no reason shown, or wording that differs between two places for the same thing. Full tier: look at it yourself at phone (390 px) and desktop (1440 px) widths, not only the author's shots
   - structure: follows best practice and the repo's existing patterns and code structure
   - scope: every file in the diff belongs to the change. Agent working files (superpowers plans, `docs/work-items` notes, handoffs, scratch scripts, logs, local config) and committed review notes are a finding to remove, unless the repo keeps them on purpose; then check they are current and match the code. Lasting knowledge goes where the next coder looks: the PR description and issue, tests, a code comment for a non-obvious why, an ADR, the README or a runbook
   - security: validation at every trust boundary, injection, authorization on every path, secrets, error leaks. Full tier, when the change touches permissions, menus, buttons, route guards or role-gated data: run it as a limited role that should have access and one that should not, not only as an all-permission admin, and check the control, a direct URL and the API call
   - performance: queries in loops, unbounded growth, blocking calls on hot paths, missing indexes
   - tests: the new behaviour, the failure paths and the bug path are covered, and the tests exercise real behaviour. A test that passes before and after the change shows nothing on its own. Full tier: fail-first and broken-guard runs (`full-tier.md`)
   - compatibility: existing callers, existing users and day-to-day operations, schema and API changes, deprecations
   - operations: logs and metrics that help, migrations (locks on large tables, backfills), deploy order and zero downtime (old code on the new schema, new code on the old), rollback
   - AI-generated code: APIs or library methods that do not exist, catch-all error handling that swallows failures, placeholder validation, boilerplate that does not match the repo
5. **Check the outcome and who is affected** (a short pass, sized to the risk): does the change provide the mechanism for the result it promises, or only describe it? Who or what has to use it: callers, existing data and roles, an agent that must load a rule or doc? How could it pass every check and still miss its purpose? Green CI shows the behaviour the checks cover, not adoption. **Second reviewer** (Full tier, and any change built on your own earlier analysis, spec or issue, where you would partly be checking your own conclusion): start a fresh subagent with only the diff, the linked issue and the repo, never your findings or verdict, and run it while you test. Trace each finding it has that you do not until it is confirmed or ruled out, and say in the verdict that it ran and what it added.
6. **Report only what you can point to.**
   - Every finding has a file:line, the evidence, a severity (P0 blocks, P1 must fix, P2 should fix, P3 nit), how you verified it (ran it, traced it, inferred it) and the smallest fix.
   - Put the effort into P0, P1 and P2. A nit is good to have, never strict: it never changes the verdict, the author may skip it without a reply, and it gets no run or trace effort. Report three nits at most, the ones worth the author's time, and drop anything too minor to matter (taste, a tiny wording or spacing point, what a linter or formatter already handles).
   - When unsure between P2 and P3, ask whether it can confuse a user, hide a failure or slow the next change; if yes, it is P2. Keep confirmed defects and unmet explicit requirements apart from optional improvements.
   - A suspected bug, error or broken path is never dropped for low confidence: run it or trace it until it is confirmed or ruled out. Drop any finding you cannot support after you run or trace it, style or otherwise; do not pad, and do not invent a recommendation quota.
   - When asked to post, follow `posting.md`: short comments, numbered findings kept across rounds, every finding inline on its line, the pins re-checked, and a pending review pinned to the reviewed commit.
7. **Escalate scope** (a larger refactor) only when a small fix cannot work, and say why.

Verdict first: approve, approve with nits (P3 only; still an approval, posted as Approve with the nits marked optional), request changes (any P1 or P2, a failing check or a merge conflict), block (any P0), or provisional (missing: <input>). Approve only when CI is green, the PR merges cleanly and no P0, P1 or P2 is open; nits never hold an approval back, and a known bug or a path that does not work is never a nit. In a self-review `Review:` line, count only P0 to P2; a nit alone does not make it OPEN.

Then the outcome and impact in a line, the findings most severe first, any material recommendation (smallest change, how to check it, this PR or a follow-up), the CI state of the reviewed head (green, or which check fails and why), and the checks you ran, with your local runs kept apart from external CI. If the diff is clean, say so briefly and still say what the evidence does not show.

The full checklists, confidence scoring and optional tool integrations: `reference.md`. The shared quality bar, with version sources per language and the types the same value can arrive as: `../../references/checklists/engineering-quality-bar.md`.

**Review since a fixed point** (a branch, tag or commit the user names): confirm it resolves (`git rev-parse`) and the diff is not empty before reviewing, then use `git diff <ref>...HEAD` so the comparison is against the merge-base. Report two axes separately and do not merge or rerank them: Standards (the repo's documented rules) and Spec (the originating issue or spec: missing or partial requirements, scope creep, requirements that look done but are wrong, each quoting the spec line). Code can pass one axis and fail the other. If no spec exists, mark the Spec axis "not applicable: no spec".

**Smell baseline** for the Standards axis when the repo documents little: possible Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. These are judgement calls, never hard violations: label them "possible", let a documented repo standard override them, and skip anything tooling already enforces. A smell on its own is a nit; it rises to P2 only when it causes a real problem you can point to.

Fixed-point two-axis review and smell baseline adapted in part from engineering/code-review (skills pack by Matt Pocock, MIT).
