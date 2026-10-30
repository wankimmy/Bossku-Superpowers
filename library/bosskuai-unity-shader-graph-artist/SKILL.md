---
name: bosskuai-unity-shader-graph-artist
description: "Use when building Unity shaders: Shader Graph with Sub-Graphs, converting to URP/HDRP-compatible HLSL, custom Renderer Features, per-platform ALU and texture-sample budgets, profiling, and artist handoff."
---

# BosskuAI Unity Shader Graph Artist

Use this skill to author, optimise, and hand off Unity materials and screen effects in Shader Graph or HLSL, with an explicit cost budget per platform.

## How this differs from nearby skills

- **`bosskuai-3d-web-development`**: shaders in Three.js and WebGL/WebGPU. This skill is Unity's pipelines, Shader Graph, and SRP APIs.
- **`bosskuai-blender-motion-state-inspection`**: inspecting Blender motion state, not engine shaders.
- **`bosskuai-web-performance`**: browser performance, not GPU frame cost in a game engine.
- **`write-swift`**: unrelated language; mentioned only because Metal shaders on Apple targets are compiled from Unity's output.

## Workflow

1. Brief: visual reference, target platforms (PC, console, mobile), pipeline (URP, HDRP; built-in is legacy), and the cost budget. Agree these before opening Shader Graph.
2. Check the project's Unity version (`ProjectSettings/ProjectVersion.txt`) and the URP or HDRP package version (`Packages/packages-lock.json`), then read the matching documentation and the latest stable release notes. Custom-pass APIs differ between URP and HDRP and between versions.
3. Plan the logic on paper: texturing, lighting, effects, output. Decide Shader Graph (artist-editable) versus HLSL (when profiling shows a need).
4. Build reusable pieces first as Sub-Graphs (fresnel, dissolve core, triplanar). Group nodes by purpose, expose only artist-facing parameters, and add tooltips on the Blackboard.
5. For HLSL: use SRP-compatible macros and include files, declare per-material constants consistently with the Properties block (mismatches give black or wrong materials), and keep include files separate from shader wrappers.
6. For full-screen or multi-pass effects, use the pipeline's renderer-feature mechanism, and test render-pass ordering and targets.
7. Profile with the Frame Debugger and the GPU profiler on the target device. Compare texture samples, instruction count, overdraw, and transparency mode against the budget. Prefer alpha clipping to blending where quality allows.
8. Provide a fallback variant for low-end targets when needed, and avoid features that are undefined on the target GPU class (for example derivatives on some mobile GPUs; verify per device).
9. Handoff: parameter list with ranges and visual descriptions, a material setup guide, and source assets in version control.

## Guardrails

- Budget numbers (samples, instructions) depend on the device tier and content. Set them from profiling of the target hardware, not from a fixed rule.
- A graph built for one pipeline does not port automatically to another.
- Do not ship only compiled shader variants; keep the source.
- Do not change shared library shaders without checking dependent materials.
- Each new keyword multiplies the shader variant count. Check the count and the build time after each keyword.
- Test zero and maximum parameter values, a missing texture, and a camera with an unusual aspect ratio.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Target: [pipeline, platform, Unity version]
Budget: [samples, instructions, transparency, overdraw]
Design: [Shader Graph / HLSL, Sub-Graphs, exposed parameters]
Profile: [tool, device, measured cost vs budget]
Fallback: [variant or none, reason]
Handoff: [parameter doc, material guide, source location]
```

Adapted from agency-agents/game-development/unity/unity-shader-graph-artist.md (agency-agents, MIT).
