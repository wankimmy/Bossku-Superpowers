---
name: bosskuai-diagnose-loop
description: "Use when diagnosing hard bugs or perf regressions: reproduce, minimise, hypothesise, instrument, fix, regression-test. Triggers: 'diagnose/debug this', bug reports, broken/throwing/failing, perf regressions."
---

# Diagnose

For a bug, a regression or a slow path. Do not guess at fixes before you can reproduce the problem.

1. **Get a fast, deterministic signal.** A failing test at the right seam, a command or script with a fixture input, a replayed payload, a bisect harness. If the bug is intermittent, raise its reproduction rate first (loop it, pin time and random seeds).
2. **Reproduce the exact symptom the user described**, not a nearby one. Capture the error text or wrong output. Shrink the input until removing anything more hides the bug.
3. **Write 3-5 ranked hypotheses**, each with a prediction ("if X is the cause, changing Y fixes it"). Test them one at a time, changing one thing per probe. Prefer a debugger or a targeted, tagged log line (`[DEBUG-x]`) to printing everything. For slowness, measure before you change anything.
4. **Fix the cause and lock it in.** Turn the minimal repro into a failing test, watch it fail, fix the cause rather than the symptom, watch it pass, then re-run the original scenario. After three failed fixes, stop and rethink the diagnosis.
5. **Look sideways.** Search for the same defect pattern in sibling code and fix every instance the request covers.
6. **Clean up** every debug line and throwaway file, and say what the real cause was.

The full loop, ways to build a feedback loop, and the post-mortem questions: read `reference.md` in this folder.
