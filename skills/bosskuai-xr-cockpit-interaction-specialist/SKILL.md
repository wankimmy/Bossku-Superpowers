---
name: bosskuai-xr-cockpit-interaction-specialist
description: "Use when prototyping seated XR cockpit or vehicle controls: constrained yokes, levers, and switches, dashboard gauges, gaze, hand, and voice input, comfort anchoring, and feedback cues in A-Frame or Three.js."
---

# BosskuAI XR Cockpit Interaction

Use this skill for fixed-position, seated XR interfaces such as a vehicle cockpit, command console, or trainer, where the user's viewpoint stays anchored and controls are reached by hand, gaze, or voice. The source material is brief, so keep recommendations modest and test them.

## How this differs from nearby skills

- **`bosskuai-3d-web-development`**: general browser 3D (scene setup, assets, performance). This skill covers cockpit-style control and comfort design on top of it.
- **`bosskuai-macos-spatial-metal-engineer`**: native Metal and visionOS rendering, not web XR prototypes.
- **`bosskuai-rapid-prototype`**: time-boxed prototype method; use it to scope a cockpit demo.
- **`bosskuai-ui-ux-design-to-code`**: 2D screens, not spatial controls.

## Workflow

1. Define the task: what the user operates, what the seat and fixed viewpoint are, which inputs must work (hand, controller, gaze, voice, physical prop), and the target device and browser.
2. Anchor the viewpoint to the seat. Do not move the camera freely; moving the user's view without matching body movement is a common cause of discomfort.
3. Lay out controls by ergonomic reach and eye-hand-head flow: primary controls within easy reach, frequently read gauges within the comfortable gaze area, rarely used controls further away. Check against current published ergonomic or platform guidance.
4. Model each control with constraints rather than free movement: a throttle slides on one axis, a yoke rotates within limits, a switch has discrete states. Snap or clamp values, and show the current state visually.
5. Feedback: pair every interaction with a visual change and a sound or haptic cue where hardware allows. Animate gauges from real state and avoid distracting motion.
6. Multi-input: define one clear fallback for each action (for example hand grab with a controller trigger alternative, voice command with a gaze-and-dwell alternative). Handle tracking loss gracefully.
7. Prototype in A-Frame or Three.js with simple shapes first, then refine models. Test seated on the real headset, note any discomfort, and iterate.
8. Accessibility: allow one-handed use, seated and standing setups, and adjustable control height and text size where practical.

## Guardrails

- Comfort thresholds and motion-sickness limits vary by person and device. Test with real users, and check current headset vendor guidance rather than quoting numbers from memory.
- Simulators used for training do not replace certified training or equipment. Do not present a prototype as a safety-qualified training tool.
- Browser XR APIs and device support change; verify in the current documentation.

## Output format

```text
Task and devices: [..]
Control layout: [control, position, reach zone, constraint]
Input map: [action, primary input, fallback]
Feedback cues: [control, visual, audio, haptic]
Comfort test notes: [participant, issue, change]
Open questions: [..]
```

Adapted from agency-agents/spatial-computing/xr-cockpit-interaction-specialist.md (agency-agents, MIT).
