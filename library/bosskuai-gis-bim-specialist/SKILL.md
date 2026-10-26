---
name: bosskuai-gis-bim-specialist
description: "Use when bringing Revit or IFC building models into GIS: georeferencing, attribute mapping, indoor routing networks, floor-aware maps, and digital twin data models that combine BIM, IoT, and work orders."
---

# BosskuAI BIM/GIS Specialist

Use this skill to connect building-scale BIM data with geographic-scale GIS without losing the attributes people need or placing the building in the wrong spot.

## How this differs from nearby skills

- **`bosskuai-gis-solution-engineer`**: builds a PoC across a GIS stack. This skill is specifically the BIM-to-GIS conversion and indoor/digital twin design.
- **`bosskuai-3d-web-development`**: rendering 3D scenes in the browser. This skill decides what data goes into those scenes and how it is georeferenced.
- **`bosskuai-data-architecture`**: general data modelling. This skill supplies the building-to-feature mapping.
- **`bosskuai-logistics-exception-management`**: shipments and routing exceptions, not building networks.

## Workflow

1. State the purpose in one sentence ("track room utilisation across 50 buildings"). Purpose sets the level of detail: campus context needs far less than facility operations.
2. Assess the source: Revit version, IFC export settings and schema version, available parameters, units, and model quality.
3. Georeference first. Map the Revit Survey Point and Project Base Point to a real coordinate reference system and confirm the transformation with a known landmark. Wrong georeferencing is the most common BIM-GIS failure.
4. Convert by use case (IFC or RVT to a mesh format or scene layer, plus 2D feature classes). Simplify geometry; do not import every fixture.
5. Map attributes to a GIS schema: building, floor/level, room, corridor, door, window, utility point, with keys that link them (building ID, level ID, room number). Keep the attributes needed for the purpose, not every Revit parameter.
6. Validate: visual overlay on a basemap, attribute completeness, spatial accuracy, and lost texture or position after solid-to-mesh conversion.
7. For indoor mapping: build floor plans, a floor-aware data model, a routing network of rooms, corridors, stairs, lifts, and doors, then a map with a floor selector and accessible-route option.
8. For a digital twin: separate static (BIM), dynamic (sensors), and operational (work orders) data, and name the owner and refresh schedule for each. Start with geometry and room names, add sensors, then work orders.

## Guardrails

- Check current vendor docs for tool versions (ArcGIS, Revit, Cesium, ifcopenshell) before quoting menus, tools, or APIs.
- Building plans can be sensitive (security, critical infrastructure); confirm sharing rules before publishing data outside the owner.
- If the task is only a 2D footprint, point cloud classification, or terrain scene, a simpler workflow fits better.

## Output format

```text
Purpose: [one sentence]
Source: [format, version, quality notes]
CRS: [source -> target, check landmark]
Schema map: [BIM element -> GIS layer -> kept attributes]
Validation: [visual, attribute, spatial results]
Twin plan: [static / dynamic / operational data, owners, refresh]
```

Adapted from agency-agents/gis/gis-bim-specialist.md (agency-agents, MIT).
