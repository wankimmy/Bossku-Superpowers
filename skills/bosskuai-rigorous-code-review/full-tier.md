# Full-tier methods

Read this for a Full-tier review (`SKILL.md`, Size the review first). Each method adds proof the diff alone cannot give. Do them in this order.

## 1. Requirements ledger

Write it before reading the diff in depth.

- **R1...** one testable statement per requirement, with a short quote and link. Split compound criteria.
- **X1...** what must not change. This includes a restriction the issue keeps on purpose. When the PR adds a second path for an existing process (an importer, a job, a calculation), add an X item that the same input gives the same data on every path.
- **D1...** decisions made after the issue was written (its comments, review threads, sibling issues), with who and where.
- **I1...** requirements a team rule implies but the issue does not state. Quote the rule.
- **Q1...** gaps or contradictions in the requirements themselves.

Take requirements from the issue and its comments, never from the PR description: that is the author's claim, which you check. Show the ledger and ask the user once: proceed, add what was agreed verbally, or fix an item.

## 2. Pin the round

Record every PR's head SHA and its base tip. Read everything at those SHAs. Read code the PR does not change at the base tip, not the head: list what landed since the merge base on those files (`git log <merge-base>..origin/<base> -- <paths>`) before calling anything outside the diff a gap. `posting.md` re-checks the pins before anything is posted.

## 3. Whole feature: trace and reverse check

When the issue has PRs in more than one repo, find them all (the issue's links, then a search by issue key) and review them as one change.

- **Trace:** one row per ledger item, one column per repo. Each cell cites `repo:path:line` at the pinned SHA, or "-". Add the test that proves it and a status: Met, Partial (what is missing), Missing, Contradicts (quote both sides), or Can't tell from code (run it).
- **Reverse check:** every meaningful change with no ledger item is scope creep or a business-rule side effect, and is a finding. A repo that applies the rule but has no PR is a finding too.
- Show the trace one block per requirement (asked, how the PR does it, where it shows, proof, status) before any test plan. It becomes the `<details>` block of the lead PR's review.

## 4. Tests that prove something

Run these in scratch clones, never over your own uncommitted edits.

- **Fail first:** check out the merge base, bring in only the PR's new or changed test files, and run them. Each should fail for the reason the PR fixes.
- **Break each guard:** in its own clone of the head, remove one guard, or widen an isolation scope one level, and run the tests. Some test must fail. A guard that survives the PR's own tests is rerun over the wider test folders before it becomes a finding; name the folders and the test count.
- **Compare copies:** when the PR adds the same guard in several places, compare the copies with each other. The one that differs is a finding.
- **Re-check rounds:** a test added to fix an earlier finding must also fail on the code it replaces. Drop any that stays green there.
