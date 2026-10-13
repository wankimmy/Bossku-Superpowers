---
name: bosskuai-xr-immersive-developer
description: "Use when building browser-based AR or VR with WebXR (A-Frame, Three.js, Babylon.js): session setup, hand and controller input, hit testing, performance tuning, device compatibility, and graceful fallbacks."
---

# BosskuAI XR Immersive Developer

Use this skill to scaffold and debug WebXR experiences that run across headsets and mobile AR, with sensible fallbacks.

## How this differs from nearby skills

- **`bosskuai-3d-web-development`**: general Three.js, R3F, and WebGL scenes. This skill adds XR sessions, input, and device support.
- **`bosskuai-unreal-world-builder`**: native UE5 worlds, not the browser.
- **`bosskuai-ui-ux-design-to-code`**: 2D screens. Spatial UI needs separate interaction design.
- **`accessibility`**: 2D WCAG audits; spatial accessibility needs extra planning.
- **`bosskuai-web-performance`**: page performance in general.

## Workflow

1. Define the experience and target devices (for example Meta Quest, Apple Vision Pro, HoloLens, mobile AR) and whether the mode is VR, AR, or both. Browser and device support for WebXR changes often, so check the current support tables and each framework's docs before choosing.
2. Pick the framework (A-Frame for fast component prototypes, Three.js or Babylon.js for control). Note the installed version and the XR APIs it exposes.
3. Scaffold the project: feature detection, a clear "enter XR" button that starts the session from a user gesture, and a non-XR fallback view (desktop or mobile) so the content still works without a headset.
4. Request only the XR features you need (hand tracking, hit test, anchors) as optional features, and handle refusal.
5. Input: support controllers, hand tracking (pinch), and gaze or touch as fallbacks. Use raycasting for selection and hit testing for placing objects in AR.
6. Interaction design: keep UI at a comfortable distance and size, give feedback for hover and select, and avoid motion that causes discomfort (smooth artificial movement, abrupt camera moves). Offer comfort options such as snap turning.
7. Performance: set a frame-rate target for the device, then reduce draw calls and triangles, use level of detail and culling, compress textures, and keep shaders simple. Profile on the headset, not only a desktop.
8. Test across devices and browsers, record input and session bugs with exact device and browser versions, and keep a compatibility table.
9. Verify the privacy side: camera, room scanning, and hand-tracking data should be used only as needed, with the user told why.

## Guardrails

- This skill is thin on source detail; treat specifics (API names, flags, limits) as unverified until confirmed in the current WebXR and framework documentation.
- Do not test on-headset motion for long sessions without breaks; warn users about motion sickness and photosensitivity.
- Do not collect spatial or camera data without consent and a stated purpose.

## Output format

```text
Experience: [VR/AR, devices, framework + version]
Session setup: [entry, required/optional features, fallback]
Input matrix: [controller / hand / gaze / touch]
Performance: [target fps, measured on device, top costs]
Compatibility: [device, browser, result, bugs]
```

Adapted from agency-agents/spatial-computing/xr-immersive-developer.md (agency-agents, MIT).
