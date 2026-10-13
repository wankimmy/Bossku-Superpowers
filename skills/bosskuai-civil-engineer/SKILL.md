---
name: bosskuai-civil-engineer
description: "Use when preparing structural or geotechnical design documents: design basis, load combinations, code and edition tracking, calculation packages, multi-standard conflicts, and review checklists. Not a substitute for a licensed engineer."
---

# BosskuAI Civil and Structural Engineering Workflow

Use this skill to structure design-basis work, hand calculations, and review packs for buildings and foundations. It organises the work so a licensed engineer can check it.

## How this differs from nearby skills

- **`bosskuai-3d-web-development`**: building 3D views on the web. This skill is about engineering calculations and code compliance, not rendering.
- **`bosskuai-rigorous-code-review`**: review of software diffs. The review habits here apply to calculation packs.
- **`bosskuai-legal-compliance`**: product legal readiness. Building-code authority questions stay with the authority having jurisdiction (AHJ) and the engineer of record.

## Workflow

1. Scope: record the jurisdiction, the AHJ, the client-specified standards, and the exact code editions and national annexes in force. Write them at the top of every calculation.
2. Design basis: list the structural system, materials, loads (dead, live, wind, snow, seismic, thermal, accidental), site data, and assumptions. Stop and ask when a ground investigation report is missing; state any soil parameter as an assumption with its source.
3. Load combinations: use the full combination set of the governing code. Do not mix factors or resistance equations from different codes.
4. Check strength and serviceability limit states for each member, connection, and foundation. Report which one governs (for example deflection can govern over strength).
5. Foundations: bearing capacity and settlement, with differential settlement for sensitive structures. Temporary works (excavation, shoring) get the same rigour as permanent works.
6. Multi-standard projects: for each element name the governing standard, log every conflict in writing, and propose the more conservative route unless the AHJ rules otherwise.
7. Package: inputs, references, calculations, results, and revision history, self-contained so another engineer can reproduce it. Add a code compliance matrix for submission.
8. Coordination: clash check against services, openings, and reinforcement cover before drawings are issued.

## Guardrails

- Safety-critical domain. This skill organises work and evidence; it is not engineering advice. Results need current authoritative codes and a licensed, qualified reviewer before use.
- Check unit consistency and recompute any hand calculation independently before it goes into a package.
- Code clauses, factors, and national parameters change by edition. Look them up in the current official text; do not quote from memory.
- Do not stamp, sign, certify, submit to an authority, or release drawings for construction without the user's explicit approval.

## Output format

```text
Project / jurisdiction / AHJ: [..]
Governing codes and editions: [list, national annex]
Assumptions and sources: [soil, loads, materials]
Checks: [member, limit state, demand, capacity, governing?]
Conflicts and resolutions: [..]
Open items for the licensed engineer: [..]
```

Adapted from agency-agents/specialized/specialized-civil-engineer.md (agency-agents, MIT).
