---
name: bosskuai-gis-solution-engineer
description: "Use when you need a working GIS proof of concept or feasibility check: demo planning, Esri or open-source tool choice (QGIS, PostGIS, MapLibre), offline-safe demo, and a clear line between PoC and production."
---

# BosskuAI GIS Solution Engineer

Use this skill to turn a GIS architecture idea into a small, honest, working prototype and to test technical assumptions before engineering commits.

## How this differs from nearby skills

- **`bosskuai-gis-bim-specialist`**: the building-model and indoor mapping specialisation. This skill is the general GIS prototype.
- **`bosskuai-rapid-prototype`**: MVP scaffolds for apps in general. This skill is GIS-specific stack choice and demo hardening.
- **`bosskuai-throwaway-prototype`**: disposable UI/logic experiments. A GIS PoC may need data and service validation too.
- **`bosskuai-postgres-patterns`**: database design. Use it when PostGIS becomes production data.
- **`bosskuai-3d-web-development`**: 3D scenes in the browser.

## Workflow

1. Translate the brief: pick the 3-5 interactions the demo must show and write success criteria for the PoC.
2. Choose the simplest tool path that shows value (desktop GIS for analysis, hosted web maps for sharing, Python for automation, a JS mapping library for web apps, PostGIS for spatial SQL, GDAL for format conversion).
3. Check feasibility early: data format and cleanup effort, whether the service API supports the needed operation, performance with realistic feature counts, and licensing limits. Read the current vendor docs; APIs and licence terms change.
4. Time-box research on an unknown API (set a limit, then pivot or report it as a risk).
5. Build the critical path first: the one workflow the audience cares about. Clean the data before styling it.
6. Harden the demo: no live calls unless cached, trap 404/timeouts/permission errors, keep it able to run offline, and prepare a fallback (screenshots, recorded video, local copy).
7. Test on the actual device the demo will run on.
8. Hand off: label what is production-ready and what is PoC only, write build steps others can reproduce, and list every assumption and shortcut.

## Guardrails

- Never present a mock as a working feature. If something is not working, say so and show progress.
- Do not use real client data in a public demo without permission; check data-sharing and licence terms.
- A demo that works at 80% scope beats one that breaks at 100%.

## Output format

```text
Goal: [3-5 interactions, success criteria]
Stack: [tools + why, versions checked]
Feasibility: [data, API, scale, licence findings]
Demo: [path, fallback, offline status]
Handoff: [production-ready vs PoC-only, assumptions, build steps]
```

Adapted from agency-agents/gis/gis-solution-engineer.md (agency-agents, MIT).
