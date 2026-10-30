---
name: bosskuai-diagnose-loop
description: "Use when diagnosing hard bugs or perf regressions: reproduce, minimise, hypothesise, instrument, fix, regression-test. Triggers: 'diagnose/debug this', bug reports, broken/throwing/failing, perf regressions."
---

# Diagnose

For a bug, a regression or a slow path. Do not guess at fixes before you can reproduce the problem.

Cover the whole surface before you conclude. People name a problem loosely: "the tenant page is slow" can be the list, the detail page, the edit form or one tab. List every screen, endpoint and job under the reported path from the routing config and check each one; time each call on a masked copy of production data and read what it loads. Re-read the output you already have before running more. Keep a coverage table (part, call, time, what it loads, checked yes or no), never conclude "not the cause" while a row is unchecked, and name the unchecked parts and why. With no masked copy, ask the user to prepare one and keep that check open (shared bar section 9).

1. **Get a fast, deterministic signal.** A failing test at the right seam, a command or script with a fixture input, a replayed payload, a bisect harness. If the bug is intermittent, raise its reproduction rate first (loop it, pin time and random seeds). For a race, run two callers at once with a forced delay between the check and the write. One passing run proves nothing.
2. **Reproduce the exact symptom the user described**, not a nearby one. Capture the error text or wrong output. Shrink the input until removing anything more hides the bug. If the bug needs real data, reproduce it on a masked copy of production data with the same types (the string "0.01" is not the number 0.01). Never reproduce it on production.
3. **Write 3-5 ranked hypotheses**, each with a prediction ("if X is the cause, changing Y fixes it"). Test them one at a time, changing one thing per probe. Prefer a debugger or a targeted, tagged log line (`[DEBUG-x]`) to printing everything. For slowness, measure before you change anything.
4. **Fix the cause and lock it in.** Turn the minimal repro into a failing test, watch it fail, fix the cause rather than the symptom, watch it pass, then re-run the original scenario. After three failed fixes, stop and rethink the diagnosis.
4a. **Repair the data.** If the bug already wrote bad rows, find them on a masked copy of production data first. Rehearse the repair on that copy, with production data types, and check the counts against what the fixed code should give. Then take a backup, check that it restores, write down how to undo the repair, and repair production in chunks.
5. **Look sideways.** Search for the same defect pattern in sibling code and fix every instance the request covers.
6. **Clean up** every debug line and throwaway file, and say what the real cause was.

The full loop, ways to build a feedback loop, and the post-mortem questions: read `reference.md` in this folder.

Shared bar: `../../references/checklists/engineering-quality-bar.md`.
