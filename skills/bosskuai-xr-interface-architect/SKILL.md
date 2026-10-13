---
name: bosskuai-xr-interface-architect
description: "Use when designing UI for AR, VR or XR apps: HUDs, floating menus, panel placement, comfort limits, gaze/pinch/controller/hand input with fallbacks, and usability tests focused on comfort and learnability."
---

# BosskuAI XR Interface Architect

Use this skill to design spatial interfaces that are comfortable, discoverable, and accessible in immersive environments. The source material for this skill is brief, so the steps below are a working checklist; confirm platform specifics in current documentation.

## How this differs from nearby skills

- **`bosskuai-gis-cartography-designer`**: map design on screens and paper, not headset UI.
- **`accessibility`**: WCAG for web and mobile; here accessibility means input fallbacks and comfort inside XR.
- **`bosskuai-design-systems`**: component and token systems for 2D products.
- **`bosskuai-ui-ux-design-to-code`**: turns mockups into code for flat screens.
- **`bosskuai-technical-artist`**: rendering and asset budgets that XR frame rates depend on.

## Workflow

1. Context. Define the task, user, environment (seated, standing, moving, shared space), device class (headset, passthrough AR, handheld AR), and session length.
2. Input models. List the supported inputs: direct touch, gaze plus pinch, controller, hand gesture, voice. For each primary action, define a fallback input so users who cannot use one method can still finish the task.
3. Layout zones. Place HUDs, panels, and menus in comfortable viewing and reach zones relative to the head and hands. Use the platform vendor's current comfort guidance for distances, angles, and text size, and write the values you adopt into the spec with the source.
4. Motion comfort. Avoid UI that moves unexpectedly or locks rigidly to the head in ways that cause discomfort. Keep latency low and give stable anchors. Offer comfort options (snap versus smooth turning, vignette) where the platform supports them.
5. Interaction flows. Map search, selection, manipulation, and confirmation flows. Make targets large enough for the least precise input, give clear hover, press, and select feedback (visual, audio, haptic where available), and keep destructive actions confirmable.
6. Discoverability. Show affordances in the space, teach with short in-context hints, and avoid hidden gestures with no prompt.
7. Layout templates. Reuse templates for cockpit, dashboard, or wearable-style interfaces so users learn once.
8. Prototype and test. Test on the real device with people who vary in height, hand size, vision, and experience. Observe comfort, errors, and time to learn, and stop a session early if a participant feels unwell.
9. Hand off to developers with annotated spatial specs (position, size, distance, input, feedback, fallback) and a list of open questions for engine limits.

## Guardrails

- Comfort thresholds, latency tolerances, and target sizes differ by device and change; cite the current vendor guidance rather than assuming numbers.
- Treat motion sickness and fatigue as real safety issues. Include session-length and break guidance for any training or work use.
- Capturing gaze, hand, and room data is sensitive personal data. Decide what is stored and get consent before recording it.
- Do not run user tests with participants, or publish to a headset store, without explicit approval from the project owner.

## Output format

```text
Task and environment: [text]
Input matrix: [action, primary input, fallback]
Layout spec: [element, zone, distance, size, source of guidance]
Comfort measures: [list]
Flow notes: [search / select / manipulate / confirm]
Test plan: [participants, tasks, comfort and learnability measures]
Open risks: [list]
```

Adapted from agency-agents/spatial-computing/xr-interface-architect.md (agency-agents, MIT).
