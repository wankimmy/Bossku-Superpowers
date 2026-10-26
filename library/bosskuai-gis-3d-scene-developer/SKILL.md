---
name: bosskuai-gis-3d-scene-developer
description: "Use when building web 3D geospatial scenes: terrain, 3D Tiles or I3S buildings, LiDAR point clouds, lighting and camera paths in CesiumJS, ArcGIS JS or MapLibre, with streaming, tiling and access control."
---

# BosskuAI GIS 3D Scene Developer

Use this skill to turn 2D GIS data into a 3D web scene that communicates more than the 2D map would, and still loads on the target device.

## How this differs from nearby skills

- **`bosskuai-gis-web-gis-developer`**: standard 2D web maps and dashboards. Use that when 3D is not needed.
- **`bosskuai-3d-web-development`**: general Three.js, WebGL and scroll-driven 3D, not georeferenced data or GIS tile formats.
- **`bosskuai-gis-geoprocessing-specialist`**: preparing and analysing the data in ArcGIS Pro before it reaches the scene.
- **`bosskuai-web-performance`**: general page speed; here only scene streaming and LOD.

## Workflow

1. Inventory data: terrain, imagery, buildings, 3D models, point clouds. Confirm each has a coordinate system and vertical datum.
2. Align the horizontal and vertical datums before composing anything.
3. Compose in layers: terrain base, imagery drape, 3D features, labels, interactions.
4. Choose the engine to fit: CesiumJS for globe-scale and 3D Tiles, ArcGIS JS for the Esri ecosystem, MapLibre for lighter terrain and extrusion, deck.gl for large data layers. Check current docs for supported formats.
5. Prepare data for the web: simplify CAD-level geometry, tile at suitable levels of detail, stream rather than load whole datasets, convert point clouds to a web-ready streaming format.
6. Style: sun position, shadows, atmosphere, vertical exaggeration, default camera that frames the main feature.
7. Access: scenes start private. Gate with the identity provider the organisation uses; show a clear "sign in to view" state, and test redirect loops and CORS.
8. Test on target hardware and on a slow connection: load time, frame rate, memory.

## Guardrails

- Do not use 3D where 2D communicates better; offer a 2D overview beside the scene when users may get lost.
- Keep standard orbit, zoom and pan controls.
- Never publish a scene publicly unless that is the stated intent.
- Verify format names and API versions against current vendor docs.

## Output format

```text
Scene goal: [what 3D must show]
Data: [layers, formats, CRS and datum]
Pipeline: [tiling, LOD, streaming]
Camera and style: [default view, lighting]
Access: [public / authenticated, provider]
Test results: [device, load time, frame rate]
```

Adapted from agency-agents/gis/gis-3d-scene-developer.md (agency-agents, MIT).
