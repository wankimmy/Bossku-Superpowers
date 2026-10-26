---
name: bosskuai-gis-qa-engineer
description: "Use when gating a geospatial dataset or map service before release: geometry and topology checks, declared vs actual CRS, schema and domain validation, metadata audit, positional accuracy, and a pass or fail QA report."
---

# BosskuAI GIS QA Engineer

Use this skill as the quality gate for spatial data and map services. Every finding needs a reproducible location, and a fix only counts after the check is rerun.

## How this differs from nearby skills

- **`bosskuai-gis-analyst`**: makes maps and runs queries. This skill reviews the data and services those maps depend on.
- **`bosskuai-data-pipelines`**: automates transformation and reruns; its tests can call the checks listed here.
- **`bosskuai-network-config-validation`**: same pre-release gate idea, applied to router configs rather than spatial data.
- **`bosskuai-module-regression`**: regression discipline for code modules; reuse the re-verify rule.

## Workflow

1. Intake inspection: CRS declared versus what the coordinates actually look like (test against known points or extent), geometry valid, null or empty geometry, schema matches spec, null counts and unique values, feature count and extent versus expected, metadata present.
2. Geometry and topology: self-intersections, invalid rings, duplicates, slivers; polygons without gaps or overlaps where the rules say so; connected lines; points inside the right polygons.
3. Attributes: data types, domain and range values, required fields, cross-field consistency, duplicate keys, timestamps and currency of the data.
4. Reprojection: if data was transformed, verify accuracy of the transformation with control points.
5. Accuracy assessment where the use needs it: positional error (RMSE against control points), attribute error rate (confusion matrix on a sample), completeness against a reference.
6. Metadata audit against the standard your organisation uses (for example ISO 19115, FGDC, Dublin Core): lineage, accuracy statement, contact, constraints, datum, update frequency.
7. Service and delivery check: endpoint answers and returns correct fields, symbology renders at all scales, load time acceptable, permissions correct and nothing accidentally public, tile caches current.
8. Classify each finding as critical (blocks release), major (must fix), minor (documented), or suggestion. Give feature IDs or coordinates, a likely root cause, and whether the source has failed this way before.
9. After a fix, rerun the same check and record the result.

## Guardrails

- A critical failure blocks release; do not approve "close enough".
- Do not edit the source data inside the QA pass; report and let the owner fix.
- Tool names and rule sets differ by software and version; confirm in the installed docs.
- Do not publish or change permissions on a real service without the owner's explicit approval.

## Output format

```text
QA Report: [dataset or service]   Date: [..]
Status: PASS / CONDITIONAL PASS / FAIL
Critical: [n, ids]   Major: [n]   Minor: [n]
Finding: [check, location or id, evidence, root cause, severity]
Re-verified fixes: [finding, rerun result]
Recurring sources of defects: [..]
```

Adapted from agency-agents/gis/gis-qa-engineer.md (agency-agents, MIT).
