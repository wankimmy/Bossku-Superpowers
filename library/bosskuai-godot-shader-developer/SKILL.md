---
name: bosskuai-godot-shader-developer
description: "Use when writing or reviewing Godot 4 shaders: canvas_item and spatial shaders, VisualShader graphs, CompositorEffect post-processing, renderer limits (Forward+, Mobile, Compatibility), and shader performance audits."
---

# BosskuAI Godot Shader Developer

Use this skill for visual effects in Godot 4 written in the Godot shading language or VisualShader. It is GLSL-like but not raw GLSL, and renderer choice limits what is allowed.

## How this differs from nearby skills

- **`bosskuai-technical-artist`**: asset pipeline, budgets, and cross-engine art tooling; this skill is Godot shader code and review.
- **`bosskuai-game-designer`**: what an effect should do for the player, not how it renders.
- **`bosskuai-unity-multiplayer-engineer`**: another engine and a networking topic.
- **`animate`**: UI motion on the web, not GPU shaders.

## Workflow

1. Define the visual target (reference image or video) and the platform. Pick the renderer first: Forward+, Mobile, or Compatibility. Use of depth or screen textures can lock the choice.
2. Pick the shader type: `canvas_item` for 2D and UI, `spatial` for 3D surfaces, `particles`, or `sky`. Declare `shader_type` first in every file.
3. Prototype in VisualShader when artists will tweak it; port to a code shader when logic is complex or performance-critical.
4. Use Godot built-ins (`TEXTURE`, `UV`, `COLOR`, `FRAGCOORD`, `TIME`). Do not use Godot 3 or raw GLSL names such as `texture2D`. In spatial shaders, `ALBEDO`, `ROUGHNESS` and similar are outputs.
5. Expose every artist-facing value as a `uniform` with a hint (`source_color`, `hint_range`, `hint_normal`). No magic numbers in the body.
6. Mobile pass: count texture samples, avoid `discard` in opaque materials (prefer alpha scissor), avoid variable-length loops in fragment code, and avoid screen-texture reads that force a framebuffer copy unless justified.
7. Compatibility check if broad device support matters, since this renderer has the most restrictions.
8. Profile with the engine's rendering profiler and compare GPU frame time before and after.
9. Put the renderer requirement and any built-in quirks in a header comment.
10. For full-screen effects, use `CompositorEffect` with the rendering device; chain passes and offer tiered presets per renderer.

## Review checklist

```text
Shader type / renderer target:
Texture samples in fragment:
Uniforms all hinted:
discard or alpha clip handling:
SCREEN_TEXTURE / DEPTH_TEXTURE use and justification:
Dynamic loops:
Compatibility renderer safe: yes/no
```

## Guardrails

- Godot's shading language, renderer features, and `CompositorEffect` APIs change between 4.x releases. Check the installed Godot version and its docs before relying on a built-in or render mode.
- Treat any sample budget as a starting point; measure on target hardware.
- Do not ship an effect validated only on a desktop GPU if mobile is a target.
- Get the installed editor version with `godot --version`. Do not use the version in `project.godot` as the engine version, because it can differ from the installed editor. Before you rely on a renderer feature, check the latest stable release notes at https://github.com/godotengine/godot/releases.
- Compile and check the shader on every renderer you ship. A shader that works on Forward+ can fail on Compatibility.
- Test zero and maximum uniform values, a missing texture, and very large and very small screen sizes. Before you rename a uniform, search the project for the old name.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Effect and target: [description, renderer, platform]
Approach: [VisualShader / code / compositor]
Uniforms: [name, type, hint, default]
Performance notes: [samples, loops, measured frame time]
Compatibility: [renderers tested]
Risks: [list]
```

Adapted from agency-agents/game-development/godot/godot-shader-developer.md (agency-agents, MIT).
