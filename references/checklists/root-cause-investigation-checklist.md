# Root Cause Investigation Checklist

> If the request is general, ambiguous, or touches many files — ask clarifying yes/no questions **before acting**. Use numbered bullets with explicit answer format: e.g. `1-yes/no  2-A/B`.

- What is the exact expected behavior, actual behavior, scope, environment, and time window?
- What entity IDs, request IDs, job IDs, webhook IDs, or idempotency keys link the evidence together?
- What does the business flow look like from trigger to final side effect?
- What does the database state show before, during, and after the incident?
- What do logs, queue/job traces, webhook histories, or external system records show?
- Which business invariant first breaks, and where?
- Is the root cause code logic, data state, async handoff, race/transaction gap, retry/idempotency failure, or config drift?
- What immediate containment, durable fix, test, and monitor would prevent recurrence?

## Coverage before conclusion

- Is every part under the reported path listed from the routing config, not only the one URL the user named (list, detail, edit, create, each tab, modals, exports, jobs it starts)?
- Was each part checked on a masked production copy (types and formats kept), with each API call timed and what it loads read (query count, eager-loaded relations, rows scanned, payload size)?
- Did you re-read the output you already have? Earlier runs often show the cause (an endpoint loading 16 relations, a query returning 50,000 rows).
- Is there a coverage table (part, call, time, what it loads, checked yes or no), and does every "not the cause" claim rest on a checked row?
- Are the unchecked parts named, with the reason? With any part unchecked, there is no conclusion yet.
- Before asking the user to measure production, was everything you can reach yourself checked (masked production copy, logs, browser), and is the ask exact?
