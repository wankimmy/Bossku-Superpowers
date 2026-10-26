---
name: bosskuai-visionos-spatial-engineer
description: "Use when building native visionOS apps with SwiftUI and RealityKit: windows, volumes, ornaments, attachments, glass background effects, spatial widgets, gestures and accessibility in 3D space."
---

# BosskuAI visionOS Spatial Engineer

Use this skill for native visionOS work where SwiftUI scenes, volumetric content and glass materials must fit Apple's spatial design conventions.

The source material for this skill is a short feature list, so treat it as a map of topics. The installed SDK and Apple's current documentation are the authority for every API named here.

## How this differs from nearby skills

- **`bosskuai-swiftui-patterns`**: SwiftUI state, composition and navigation for iOS and macOS. This skill adds spatial scenes and RealityKit.
- **`bosskuai-liquid-glass-design`**: the glass material system across Apple platforms; use it for design detail, then apply it in visionOS windows here.
- **`bosskuai-3d-web-development`**: browser 3D, not native visionOS.
- **`write-swift`** and **`bosskuai-swift-concurrency-6-2`**: Swift language and concurrency rules.

## Workflow

1. Confirm the target visionOS version and Xcode version. Features differ between releases; check release notes before using a new API.
2. Choose the scene types: standard windows, unique single-instance windows, volumetric windows, or immersive spaces. Use the lightest one that serves the task.
3. Structure scenes with `WindowGroup` and clear presentation hierarchies. Decide how window lifecycle and state are shared, using observable models.
4. Build UI with spatial patterns: ornaments for controls attached to a window, attachments for UI anchored to 3D entities, and glass background effects for window materials.
5. Integrate RealityKit content with SwiftUI: observable entities, gesture handling on entities, attachment components for 2D views in 3D.
6. Handle input: gaze and hand gestures, with indirect and direct interaction both considered.
7. Manage depth and layout deliberately: position, distance, scale and relationships between content and windows.
8. Performance: watch GPU cost of many glass windows and heavy 3D content; profile with Xcode instruments on device.
9. Accessibility: VoiceOver labels and navigation that make sense in space, alternatives to gaze- or gesture-only actions.

## Guardrails

- Limit scope to the SwiftUI and RealityKit stack and the targeted OS version. Say so when a request needs another engine or an older OS.
- Do not copy API names from memory; verify in the current documentation.
- Test on a device or simulator before claiming behaviour; some spatial behaviour only shows on hardware.

## Output format

```text
Target: [visionOS version, Xcode version]
Scene plan: [window / volume / immersive space, why]
UI structure: [ornaments, attachments, materials]
State and input: [models, gestures]
Performance and accessibility notes: [risks, checks]
Verification: [simulator or device result]
```

Adapted from agency-agents/spatial-computing/visionos-spatial-engineer.md (agency-agents, MIT).
