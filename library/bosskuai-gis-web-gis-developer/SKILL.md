---
name: bosskuai-gis-web-gis-developer
description: "Use when building interactive web maps: choosing MapLibre, Leaflet, OpenLayers, deck.gl or ArcGIS JS, serving vector tiles and OGC or REST services, real-time layers, clustering, and responsive, touch-friendly map UX."
---

# BosskuAI Web GIS Developer

Use this skill to build or fix interactive web mapping applications that stay fast with real data volumes and work on phones.

## How this differs from nearby skills

- **`bosskuai-gis-3d-scene-developer`**: 3D terrain, point clouds and scenes. Stay here for 2D maps.
- **`bosskuai-gis-geoprocessing-specialist`**: desktop analysis and ArcPy automation that produce the data.
- **`bosskuai-dashboard-builder`**: Grafana-style operational dashboards, not map apps.
- **`bosskuai-ui-ux-design-to-code`**: turning mockups into UI; use it for the surrounding app screens.
- **`bosskuai-web-performance`**: general web speed; here the focus is map data volume.

## Workflow

1. Requirements: which data, which interactions (identify, search, measure, print), which devices, how fresh the data must be.
2. Pick the library to fit: MapLibre GL JS for vector tiles and custom styling, ArcGIS JS API for the Esri ecosystem, Leaflet for simple maps, OpenLayers for broad OGC support, deck.gl for large data. Confirm current versions and licences in official docs.
3. Publish data as a service: vector tiles (for example from PostGIS with a tile server, or tiles built offline), OGC API Features, WMS, WFS, WMTS, or ArcGIS REST.
4. Build in order: base map, data layers, interactions, UI. Set a default viewport on the area of interest, not the whole world.
5. Scale: never load every feature. Use tiles, clustering, viewport filtering and geometry simplification. Plain GeoJSON is fine for small sets, not for large ones.
6. Real-time: pick WebSocket, server-sent events or polling to suit the source; update features in place; add auto-refresh and a time control if the data is temporal.
7. UX: loading state, legend, touch gestures, readable labels, accessible controls.
8. Auth: use the identity method the services require (OAuth, tokens, API keys). Keep keys and secrets out of client bundles; restrict keys by referrer where the provider supports it.
9. Test on a phone, on a throttled connection, and with the largest real dataset.

## Guardrails

- Check tile and service licences and terms before using a public basemap or geocoder in production.
- Do not expose private layers through a public tile or API endpoint.
- Large imagery on mobile can crash the tab; test memory.

## Output format

```text
Requirement: [data, interactions, devices]
Library and why: [choice, version checked]
Data serving: [tiles / OGC / REST, caching]
Scale strategy: [cluster, filter, simplify]
UX and auth: [loading, legend, touch, auth method]
Test results: [device, network, dataset size]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/gis/gis-web-gis-developer.md (agency-agents, MIT).
