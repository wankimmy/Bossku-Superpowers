---
name: bosskuai-gis-geoprocessing-specialist
description: "Use when automating repeated ArcGIS Pro work: Python toolboxes (.pyt), ArcPy scripts, Model Builder models and batch clip, reproject or export jobs, with parameter validation, logging, licensing and cleanup."
---

# BosskuAI GIS Geoprocessing Automation

Use this skill when a manual GIS workflow has been done more than a couple of times and should become a repeatable, validated tool.

## How this differs from nearby skills

- **`bosskuai-gis-web-gis-developer`**: web maps and services for end users, not desktop geoprocessing.
- **`bosskuai-gis-3d-scene-developer`**: displaying prepared data in 3D on the web.
- **`python-patterns`** and **`python-testing`**: general Python style and pytest. This skill adds ArcPy and toolbox conventions on top.
- **`bosskuai-performance-profiling`**: use it if a script is slow for non-GIS reasons.

## Workflow

1. Write down the manual workflow step by step: inputs, parameters, outputs, failure cases.
2. Decide the surface: Model Builder for visual workflows non-programmers maintain, ArcPy script for batch jobs, Python toolbox (.pyt) for a shareable tool with a dialog.
3. Prototype the core logic in ArcPy on a small dataset.
4. Set environments explicitly (workspace, output coordinate system, extent). Never rely on whatever the session had.
5. Licensing: check out required extensions at the start, check them in at the end, and fail with a clear message if unavailable.
6. For a .pyt tool: define parameters, add validation in `updateParameters` and `updateMessages`, report progress for long jobs, write helper text and dependencies between parameters.
7. Use data-access cursors (`arcpy.da`) in `with` blocks; delete scratch data, release locks.
8. Batch jobs: loop over inputs with logging and per-item error handling so one bad input does not stop the run unnoticed; consider parallelism only when profiling shows it helps.
9. Test with realistic and awkward data (empty inputs, NoData, schema locks, wrong projection), not only the happy path.
10. Document purpose, parameters, limitations and an example.

## Guardrails

- Tool, function and parameter behaviour changes between ArcGIS Pro versions; check the installed version and the current Esri docs.
- Work on copies or a scratch workspace; never overwrite source data without explicit user approval.
- Error messages should say what is wrong ("Input has no features"), not a bare error code.
- Do not run destructive deletes on enterprise geodatabases without approval.

## Output format

```text
Workflow replaced: [manual steps]
Surface: [model / script / .pyt]
Parameters and validation: [list]
Environment and license: [settings, extensions]
Error handling and logging: [approach]
Tests: [datasets and edge cases]
```

Adapted from agency-agents/gis/gis-geoprocessing-specialist.md (agency-agents, MIT).
