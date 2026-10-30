# Bug Finding Checklist

> If the request is general, ambiguous, or touches many files — ask clarifying yes/no questions **before acting**. Use numbered bullets with explicit answer format: e.g. `1-yes/no  2-A/B`.

- What is the exact entry point and expected behavior?
- What changed recently or looks suspicious?
- What happens on empty, null, partial, duplicate, and retry paths?
- Are auth, permission, tenant, or role assumptions being violated?
- Are there race conditions, transaction gaps, or stale-state issues?
- Does the frontend/backend or caller/callee contract drift anywhere?
- What tests should exist but do not?
- Which other screens, endpoints or jobs share this path or code, and were all of them checked?
- What did earlier output already show that is still unexplained?
