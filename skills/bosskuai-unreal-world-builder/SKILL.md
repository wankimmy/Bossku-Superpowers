---
name: bosskuai-unreal-world-builder
description: "Use when building a large Unreal Engine 5 open world: World Partition grids and data layers, Landscape materials, HLOD, PCG foliage, streaming tests, and a performance checklist per milestone."
---

# BosskuAI Unreal World Builder

Use this skill to plan and check an open-world UE5 level so it streams without hitches and renders within budget on the target hardware.

## How this differs from nearby skills

- **`bosskuai-3d-web-development`**: browser 3D (Three.js, WebGL). This skill is native UE5 world building.
- **`bosskuai-performance-profiling`**: general profiling method; this skill supplies the open-world checklist.
- **`bosskuai-cpp-coding-standards`**: C++ style for gameplay code, not level and streaming design.
- **`bosskuai-game-audio-engineer`**: audio budgets within the same world.
- **`bosskuai-xr-immersive-developer`**: WebXR in the browser.

## Workflow

1. Define world size, biome layout, points of interest, target platforms, and frame-time budget. Check the engine version first; World Partition, PCG, and Nanite features differ between UE5 releases.
2. Plan World Partition before filling the world: choose the runtime grid cell size per content type (denser areas smaller, sparse areas larger), loading ranges, and data layers. Reconfiguring the grid late can force a full re-save.
3. Put always-loaded content (sky, managers, game systems) in a dedicated always-loaded data layer. Keep gameplay-critical actors away from cell boundaries and test boundary crossings.
4. Landscape: compute resolution from component size with the engine's import tool, plan the master material with a small number of layers per region, use runtime virtual texturing where layer cost is high, and use the visibility layer for holes rather than deleting components.
5. Populate with PCG or the procedural foliage tool for large areas; reserve hand placement for hero assets. Define exclusion zones (roads, paths, water, hand-placed structures), use Nanite-eligible meshes where they fit, and bake large-area output ahead of time rather than generating at runtime.
6. HLOD: build for everything seen at distance, generate (never hand-author) and rebuild after geometry changes, and review visually from the far draw distance each milestone.
7. Streaming test: traverse at the fastest player speed (mounts, sprint, vehicles) and confirm streaming sources and ranges stay ahead; add secondary sources for cinematics and AI directors.
8. Profile with the engine's profiling tools on target hardware at the worst-density spots. Fix the top three frame-time contributors before the next milestone.
9. For worlds with large extents, evaluate Large World Coordinates and one-file-per-actor for team editing; check the docs for current behaviour.

## Guardrails

- Numbers in templates (cell sizes, layer counts, limits) are starting points; set them from measurements on your hardware and the engine version in use.
- Back up and use version control before changing partition settings or regenerating HLOD or PCG on a shared project.
- Do not rely on desktop-only results for console or mobile targets.

## Output format

```text
World: [size, platforms, frame budget, UE version]
Partition: [grid, cell size, range, data layers]
Landscape: [resolution, layers, RVT]
Population: [PCG graphs, exclusions, bake status]
HLOD: [layers, rebuild trigger, visual check]
Perf results: [streaming hitches, GPU time, memory]
```

Adapted from agency-agents/game-development/unreal-engine/unreal-world-builder.md (agency-agents, MIT).
