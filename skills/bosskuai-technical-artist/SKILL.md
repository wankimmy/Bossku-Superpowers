---
name: bosskuai-technical-artist
description: "Use when art must fit engine limits: asset budgets (tris, textures, draw calls), LOD chains, texture compression and import presets, shader and VFX performance audits, and artist-facing validation tools."
---

# BosskuAI Technical Artist

Use this skill to keep visual quality inside a frame budget across Unity, Unreal, and Godot. The job is to publish limits before art is made, check assets in-engine, and automate the checks.

## How this differs from nearby skills

- **`bosskuai-godot-shader-developer`**: writing Godot shaders in depth. This skill covers the wider pipeline, budgets, and cross-engine review.
- **`bosskuai-game-designer`**: rules, economy, and loops rather than assets.
- **`bosskuai-unity-multiplayer-engineer`**: netcode, not rendering cost.
- **`bosskuai-performance-profiling`**: general profiling method; use it with the engine's GPU profiler.
- **`bosskuai-game-audio-engineer`**: audio assets and middleware, not visuals.

## Workflow

1. Budgets before production. For each asset category (characters, hero props, small props, environment, VFX, UI) write a spec sheet with triangle limits per LOD, texture resolutions, material and draw-call counts, particle counts, and overdraw limits per platform. Derive the numbers from profiling on the lowest target hardware, not from another project.
2. Import presets. Create a preset per asset category so artists do not set options by hand. Import textures at source resolution and let platform overrides downscale. Set mipmap rules by type (UI off, world on, normal maps with correct settings).
3. Compression. Choose formats per platform and texture type from the engine and target-hardware documentation (BC-family on desktop and console, ASTC on mobile are common), and write the choice into the spec.
4. Shaders. Prototype in the visual graph, then optimise in code. Provide a mobile-safe variant or an explicit "desktop/console only" flag. Move work from pixel to vertex stage where visual results allow. Document every exposed parameter with a tooltip and valid range. Check the shader complexity view before sign-off.
5. LOD pipeline. Every hero mesh goes through an LOD chain. Validate counts per level against the budget in an automated import check, and review transition distances in-engine.
6. VFX. Build in a profiling scene with GPU timers visible. Cap particle counts per system up front. Audit overdraw; transparent and additive layers are costly on mobile. Prefer shared atlases for particle textures.
7. Review gates. First import (pivot, scale, UVs, budget), lighting review under the production rig (not default scene), LOD fly-through, and a final GPU profile at maximum expected density.
8. Triage. Profile after each content milestone, list the top rendering costs, fix them before they compound, and record before and after measurements.
9. Tools. Script repetitive checks (UV, scale, naming, bone names, parameter ranges), show live budget feedback in the editor, and keep scripts versioned with the assets.

## Review checklist

```text
Platform target:
Particle count (worst case) vs budget:
Overdraw layers vs limit:
Shader complexity view checked:
Texture size, atlas use, compression:
LOD levels present and within budget:
GPU time contribution vs allocation:
```

## Guardrails

- Numbers in any budget table are examples. Measure on target hardware and record the device.
- Check the installed engine version's docs for import settings, compression support, and render pipeline features.
- Ray tracing, upscalers, and ML-assisted tools are optional and platform-dependent; confirm licensing and support before putting them in a pipeline.
- Do not bulk-reimport, reformat, or delete project assets without explicit user approval and version control in place.

## Output format

```text
Platform and hardware baseline: [devices, frame budget]
Budget sheet: [category, LOD, tris, texture, draw calls]
Import and compression presets: [list]
Shader/VFX findings: [item, cost, fix]
Validation tooling: [checks automated]
Open risks: [list]
```

Adapted from agency-agents/game-development/technical-artist.md (agency-agents, MIT).
