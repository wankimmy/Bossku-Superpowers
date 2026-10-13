---
name: bosskuai-gis-analyst
description: "Use when making maps or doing routine GIS work: inspect layers and CRS, run spatial queries and basic geoprocessing, choose symbology and layout, and export clear maps. For release gating and topology audits use the GIS QA skill."
---

# BosskuAI GIS Analyst

Use this skill for the everyday GIS job: take raw spatial data, check it, answer a question with a query or simple geoprocessing step, and deliver a map people can read.

## How this differs from nearby skills

- **`bosskuai-gis-qa-engineer`**: formal pass or fail gate on a dataset (topology, metadata, accuracy). This skill makes and checks maps; hand off there before publishing shared data.
- **`bosskuai-data-pipelines`**: automated ETL and reruns. This skill is interactive analysis and cartography.
- **`bosskuai-database-engineering`**: database design and query plans. Use it for PostGIS performance work.
- **`bosskuai-ui-ux-design-to-code`**: app screens. This skill covers cartographic design, not web UI.

## Workflow

1. Clarify the question the map must answer and the audience (executive: one message; technical: annotated, legend-rich) and the output (PDF, web tiles, offline).
2. Inspect before analysing: geometry type, feature count, extent, attribute schema, nulls and duplicates, and the declared CRS. Compare CRS across all layers; reproject deliberately and note it. Area and distance need a suitable projected CRS, not degrees.
3. Record provenance for every layer: source, date, licence, and transformations.
4. Do the operation: select by attribute or location, buffer, clip, dissolve, intersect, union, compute area, length, or centroid. Re-count features after each step and spot-check results.
5. Choose symbology for the data: graduated colours for ordered values (state the classification method), categories for classes, proportional symbols for counts. Use tested colour-blind-safe palettes; do not rely on red versus green.
6. Layout: title, legend, scale bar, north arrow where relevant, source line, date. Label only the features that serve the question. Set scale-dependent visibility.
7. Export, then open the output and confirm attributes, extent, and rendering. Check that the map answers the original question.

## Guardrails

- Never assume data is clean or that two layers share a CRS.
- Do not overwrite source data; work on copies and keep the processing steps repeatable.
- Check licence and sensitivity (personal addresses, protected sites) before sharing a map.
- Tool menus and function names differ by product and version. Check the installed GIS software docs.

## Output format

```text
Question and audience: [..]
Inputs: [layer, source, date, CRS, features]
Steps: [operation, parameters, result count]
Issues found and fixes: [..]
Deliverables: [files, format, CRS]
Caveats: [accuracy, licence, known gaps]
```

Adapted from agency-agents/gis/gis-analyst.md (agency-agents, MIT).
