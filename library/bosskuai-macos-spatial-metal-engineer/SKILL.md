---
name: bosskuai-macos-spatial-metal-engineer
description: "Use when building Metal rendering on macOS or streaming to Apple Vision Pro: instanced drawing, GPU buffers and compute layout, frame budgets, Compositor Services, gaze and pinch input, comfort, and profiling with Instruments."
---

# BosskuAI macOS Spatial and Metal Engineer

Use this skill for GPU-heavy Swift and Metal work: rendering large node graphs or scenes on a Mac, and presenting them in an immersive space on visionOS.

## How this differs from nearby skills

- **`bosskuai-swiftui-patterns`**: app UI, state, and navigation. This skill is GPU rendering and spatial input.
- **`bosskuai-swift-concurrency-6-2`**: Swift concurrency rules; use it for the async parts of frame submission.
- **`write-swift`**: general Swift and SwiftUI code writing. This skill covers Metal, compositor, and performance.
- **`bosskuai-3d-web-development`**: 3D in the browser (three.js, WebGL). This skill is native Apple platforms.
- **`bosskuai-performance-profiling`**: general profiling method; here the tools are Instruments and the Metal System Trace.

## Workflow

1. Set the budget before building: target frame rate per platform (immersive stereo is demanding), the largest data size to support, and a memory limit. Check Apple's current guidance for the visionOS and Compositor Services versions you target.
2. Pipeline: use instanced drawing for repeated geometry, per-instance data in buffers, a uniform buffer for view and projection, and triple buffering so the CPU does not stall on the GPU. Use private storage for data the CPU rarely writes and shared storage for frequent CPU updates.
3. Layout: for graph or force-directed layouts prefer a compute kernel; an all-pairs force loop is quadratic, so switch to a spatial grid or approximation when counts grow.
4. Culling and level of detail: frustum cull, reduce detail with distance, and keep draw calls few by batching.
5. Vision Pro path: configure the compositor layer for stereo, colour and depth formats, and pass depth for correct occlusion. Check API names and signatures in the current SDK, because these frameworks change between releases.
6. Input: gaze and pinch hit-testing against your scene, with a fallback when hand tracking drops. Support accessibility features (VoiceOver, Switch Control) and follow current Human Interface Guidelines for spatial comfort, including focus distance and avoiding forced camera motion.
7. Profile on real hardware with Instruments and Metal System Trace: frame time, GPU utilisation, memory, and dropped frames. Change one variable per iteration and record the number.
8. Keep ARC clean (no retain cycles) and reuse resources through pools or heaps.

## Guardrails

- Targets such as frame rate, node counts, and memory limits are project decisions; measure them rather than assuming.
- Device and OS capabilities (mesh shaders, variable rate shading, ray tracing) vary. Check feature support at runtime: use `supportsFamily(_:)` for the GPU family and per-feature properties such as `supportsRaytracing`, and test on the oldest GPU you support.
- Do not ship settings that run the GPU at sustained maximum without testing thermals.
- Do not change signing, entitlements, or bundle identifiers without telling the user.
- Read the macOS, Xcode and SDK versions with `sw_vers`, `xcodebuild -version` and `xcodebuild -showsdks`, and the deployment target in the Xcode project. Log the OS version at launch with `ProcessInfo.processInfo.operatingSystemVersion`.
- Test an empty graph, one node, the largest graph, a layout that returns NaN or infinite positions, and a window resize during a frame.
- Triple buffering with a semaphore stops the CPU from writing a buffer the GPU still reads.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Target: [platform, frame budget, data scale, memory limit]
Pipeline design: [passes, buffers, storage modes]
Measurements: [scenario, frame time, GPU %, memory]
Bottleneck and change: [..]
Comfort and accessibility checks: [..]
Open API questions to verify in current docs: [..]
```

Adapted from agency-agents/spatial-computing/macos-spatial-metal-engineer.md (agency-agents, MIT).
