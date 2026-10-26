---
name: bosskuai-unreal-technical-artist
description: "Use when building or auditing Unreal Engine 5 visuals: Material Functions and instances, shader permutation counts, Niagara budgets and scalability, PCG graphs, Nanite, LOD and culling, and Unreal Insights profiling."
---

# BosskuAI Unreal Technical Artist

Use this skill to keep UE5 visuals consistent and inside per-platform performance budgets. Budgets are set per project and per target hardware; measure them.

## How this differs from nearby skills

- **`bosskuai-level-designer`**: layout, pacing, and encounters. This skill dresses and optimises what the level uses.
- **`bosskuai-performance-profiling`**: general profiling method; Unreal-specific tools appear in step 7.
- **`bosskuai-3d-web-development`**: real-time 3D in browsers, not Unreal.
- **`bosskuai-game-audio-engineer`**: sound; VFX and audio sync is coordinated, not shared.
- **`bosskuai-unity-architect`**: the equivalent data and architecture work in Unity.

## Workflow

1. Visual brief: reference images, quality tiers, and target platforms with their frame budgets. Audit existing Material Functions before creating new ones.
2. Materials: put reusable logic in Material Functions rather than copying node clusters between master materials, and expose variation through Material Instances. Count static switches, since each one multiplies shader permutations, and approve each addition. Use quality-tier switches for mobile, console, and PC where the tiers differ.
3. Material review per asset class: record instruction count from the material stats view, texture samples, static switches, functions used, and whether variation goes through instances. Compare with the budgets your project agreed for each platform.
4. Niagara: choose CPU versus GPU simulation by particle count and platform. Set a maximum particle count on every system, build Low, Medium, and High scalability presets alongside the system, and test at the highest expected simultaneous count. Be careful with per-particle collision on GPU systems.
5. PCG: prototype the graph on primitives, keep results deterministic for the same inputs, use slope, density, and exclusion filters instead of uniform grids, and expose and document the parameters designers may tune (density, scale variation, exclusion zones). Check streaming behaviour with World Partition for hitches.
6. Meshes: use Nanite where the mesh type is eligible; give non-eligible meshes (skeletal, spline, procedural) manual LOD chains with checked transition distances; set cull distances per asset class and configure hierarchical LOD for open-world zones.
7. Profile with Unreal Insights and the GPU profiler on target hardware; list the top rendering costs, change one thing at a time, and record the number.
8. Record sign-off items (permutation counts, scalability presets, LOD checks) before milestone lock.

## Guardrails

- Engine features and menus change across UE5 minor versions (for example material systems and PCG nodes). Verify against the installed version's documentation.
- Treat any budget number as project-specific and confirm it on the lowest target hardware.
- Do not bulk-edit shared master materials or content folders without version control and a note to the team.

## Output format

```text
Targets and budgets: [platform, frame budget, material/VFX limits]
Material review: [asset, instructions, samples, switches, pass/fail]
VFX review: [system, sim type, max particles, presets tested]
PCG graph: [parameters exposed, exclusions, streaming result]
LOD and culling checks: [..]
Profile results: [capture, top costs, change, result]
```

Adapted from agency-agents/game-development/unreal-engine/unreal-technical-artist.md (agency-agents, MIT).
