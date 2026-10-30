---
name: bosskuai-gis-spatial-data-engineer
description: "Use when messy geospatial data must become clean, standard datasets: convert Shapefile/GeoJSON/KML/CSV/GPKG, fix CRS and geometry, normalise attributes, and build repeatable GDAL or GeoPandas pipelines."
---

# BosskuAI GIS Spatial Data Engineer

Use this skill for geospatial ETL: ingest data from any source, repair it, standardise it, validate it, and deliver it through a reproducible pipeline. Most GIS project time is data preparation.

## How this differs from nearby skills

- **`bosskuai-gis-cartography-designer`**: styling and map layout once the data is clean.
- **`bosskuai-database-engineering`** and **`bosskuai-postgres-patterns`**: schema, index, and query design; use them for PostGIS tables and performance.
- **`odl-pdf`** and **`markitdown`**: extraction from documents, not spatial formats.
- **`bosskuai-data-throughput-accelerator`**: raising throughput of a data job once it works correctly.

## Workflow

1. Source assessment. Inspect format, CRS metadata, encoding, schema, geometry validity, null patterns, and row counts (for example with `ogrinfo`). Do not trust declared CRS; check coordinates against the expected area.
2. Target schema. Define field names, types, domain values, units, date format, null representation, and the output CRS.
3. Pipeline: read, clean, transform, validate, write to a new location. Never edit the original files.
4. Cleaning. Fix missing or wrong CRS (assign only when you know the true one; reproject otherwise), self-intersections, slivers, duplicate vertices, encoding (UTF-8 versus legacy), coordinate notation, and column names.
5. Validate after each transform: geometry validity, attribute completeness, row-count reconciliation, extent sanity.
6. Make it repeatable. Config-driven paths, CRS codes, and field maps. Idempotent runs. Fail early and loudly on missing or malformed input. Log each step, parameter, and output count.
7. Change detection and scheduling: process only what changed; monitor completion and unexpected volume changes.
8. Document lineage: source, date, steps, known issues, licence.
9. Deliver as files, a database table, or an API as agreed.

## Common patterns

| Job | Typical tools |
|---|---|
| CSV with coordinates to GeoJSON | pandas, shapely |
| Shapefile to GeoPackage | GDAL/OGR, Fiona |
| CAD to GIS | FME or ArcPy (licensed) |
| API to PostGIS | requests, SQLAlchemy |

Check the installed GDAL, GeoPandas, and pyproj versions and their docs for option names.

## Guardrails

- Axis order and datum shifts cause silent errors; test with known control points.
- Respect data licences and personal location data. Location traces can identify people, so check privacy before publishing.
- Do not overwrite production tables or publish to a live service without explicit user approval; run on a copy first.

## Output format

```text
Source audit: [format, CRS, encoding, issues, counts]
Target schema: [fields, types, CRS]
Pipeline steps: [ordered, with tool]
Validation results: [checks, counts in and out]
Lineage and known issues: [text]
Run instructions: [command, config]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/gis/gis-spatial-data-engineer.md (agency-agents, MIT).
