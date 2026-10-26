---
name: bosskuai-gis-drone-reality-mapping
description: "Use when turning drone imagery into GIS products: flight and GCP planning, photogrammetry processing, orthomosaic, DTM/DSM, point cloud classification, accuracy (RMSE) reporting, and export for GIS."
---

# BosskuAI GIS Drone Reality Mapping

Use this skill to plan a drone mapping job and process the images into orthomosaics, elevation models, point clouds, or meshes whose accuracy is measured and reported honestly.

## How this differs from nearby skills

- **`bosskuai-gis-spatial-data-scientist`**: statistics and modeling on geospatial data after it exists. This skill produces the data from imagery.
- **`bosskuai-3d-web-development`**: showing 3D scenes in a browser. Use it to publish a mesh once this skill has produced it.
- **`bosskuai-data-pipelines`**: general ETL; use it to automate batch processing.
- **`bosskuai-postgres-patterns`**: storing spatial data in a database.

## Workflow

1. Brief: purpose, area, required product (ortho, DTM, DSM, mesh, point cloud), required accuracy, deadline, and the local rules for flying (permits, airspace, privacy).
2. Mission plan: ground sample distance target, altitude, forward and side overlap, speed, camera settings, terrain-following needs, lighting and weather window, sensor type (RGB, multispectral, thermal, LiDAR).
3. Ground control: decide the number and spread of control points, how they are marked and surveyed, and which checkpoints are held back for independent accuracy testing. RTK or PPK on the drone helps but should be validated with checkpoints.
4. Capture: monitor image quality in the field and re-fly gaps.
5. Cull blurred, under-exposed, or poorly geotagged images before processing.
6. Process: align, optimise cameras, add control points, build dense cloud, then mesh, DEM, and ortho as needed. Record software and settings.
7. Classify point cloud if required (ground, vegetation, buildings), derive a bare-earth DTM, and avoid over-smoothing real terrain.
8. Quality control: report RMSE on control and on independent checkpoints, horizontal and vertical separately. State GSD as resolution, not positional accuracy. Inspect seams, blur, holes, and artifacts, and check density.
9. Export in formats the consumer needs (for example GeoTIFF, LAS/LAZ, mesh or 3D tile formats) with the coordinate reference system and vertical datum recorded. Load results into a GIS to confirm they register correctly.

## Guardrails

- Check aviation, privacy, and land-access rules in the area before flying. This skill does not give legal advice.
- Survey-grade deliverables used for legal boundaries or engineering sign-off need review by a qualified surveyor.
- Overlap thresholds, accuracy targets, and altitude limits depend on the software, terrain, and regulations; take them from the project spec and software documentation.
- Do not claim accuracy that was not measured against independent checkpoints.
- Do not fly, publish, or share imagery of private land or people without authorization.

## Output format

```text
Brief: [purpose, area, products, accuracy need]
Flight plan: [GSD, altitude, overlap, weather window, control points]
Processing log: [software, key settings, image count, culled]
Accuracy: [control RMSE, checkpoint RMSE, horizontal/vertical]
Products: [file - format - CRS/datum - resolution]
Known issues: [holes, artifacts, limits]
```

Adapted from agency-agents/gis/gis-drone-reality-mapping.md (agency-agents, MIT).
