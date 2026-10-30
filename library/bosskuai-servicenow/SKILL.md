---
name: bosskuai-servicenow
description: "Use when developing or debugging on ServiceNow: Business Rules, Script Includes with GlideAjax, GlideRecord versus GlideAggregate, Flow Designer, ACLs, and isolating whether a failure is out-of-the-box or custom."
---

# BosskuAI ServiceNow Developer and Debugger

Use this skill to write idiomatic ServiceNow code and to troubleshoot instance problems by evidence first, root cause second, fix third.

## How this differs from nearby skills

- **`bosskuai-diagnose-loop`**: generic bug method (reproduce, minimise, fix, regression-test). This skill adds ServiceNow evidence sources and OOTB-versus-custom isolation.
- **`systematic-debugging`**: general debugging discipline; same idea, no platform specifics.
- **`bosskuai-jira-integration`**: another ticketing platform's API; unrelated code.
- **`bosskuai-performance-profiling`**: general profiling; here only platform query and rule patterns.

## Workflow

1. Reproduce on a sub-production instance with one concrete record and user. Use a clone of production, because a small dev dataset hides real data shapes. If you cannot get one, ask the user to prepare it and say so in the result until it arrives. State expected versus actual and the scope (one form, one flow, all users).
2. Gather evidence before changing anything: session or node logs, `gs.log` or `gs.info` output, Script Debugger, a background script to run a query in isolation, and an ACL check for read/write denials.
3. Check configuration first: system properties, plugin and activation state, recent update sets.
4. Isolate OOTB versus custom: deactivate custom Business Rules, Script Includes, client scripts and ACLs one at a time on the sub-prod instance and retest. Restore anything that made no difference.
5. State the confirmed root cause and its evidence before writing a fix.
6. Pick the right surface. Reusable server logic goes in Script Includes; the client reaches it through GlideAjax (parameters via `getParameter`), never by running server APIs in a client script. Flow Designer for orchestration, Business Rules for record-event side effects, client scripts and UI policies for form behaviour.
7. Keep Business Rules lean: correct condition, `async` or `display` where possible, and a header comment naming table, trigger and intent.
8. Query hygiene: `GlideAggregate` for counts and sums, bounded queries (`setLimit`, indexed fields), no unbounded loops, no hardcoded sys_ids (use properties or reference records). `getValue()` returns "0.01", not 0.01, so cast a value on purpose before you compare or sum it.
9. Verify on the original record and on a second unrelated one; note the previous value of every record changed so the fix can be rolled back.

## Guardrails

- Check the instance release and the current ServiceNow docs for API names and behaviour; they change between releases.
- Do not bypass ACLs or hardcode sys_ids to "make it work".
- Do not run scripts or deactivate rules on a production instance without explicit user approval; promote changes via update sets or source control.
- Disclose a script's side effects: records touched, notifications sent, tables queried.
- Count rows before and after any bulk script on the clone, and compare the result with the expected count before you run it on production.
- Make bulk updates safe to rerun: each run selects only rows not yet changed, processes a bounded batch, and a run after the last batch changes nothing.
- For REST Table API calls, set a timeout, page with `sysparm_limit` and `sysparm_offset` to the last page, and retry a 429 or 5xx only when the call is safe to repeat.
- Mask passwords, tokens and personal data in `gs.log` output and integration logs.

## Output format

```text
Symptom and scope: [expected vs actual, who, where]
Evidence: [log lines, ACL result, query counts]
OOTB vs custom: [artifact that changed the symptom]
Root cause: [statement + evidence]
Fix: [surface, code summary, side effects]
Verification and rollback: [records tested, prior values]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/engineering/engineering-servicenow-developer-mentor.md (agency-agents, MIT).
