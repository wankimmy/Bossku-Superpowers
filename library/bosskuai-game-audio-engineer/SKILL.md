---
name: bosskuai-game-audio-engineer
description: "Use when designing game audio with FMOD, Wwise, or engine-native audio: event structure, adaptive music, spatial audio, mixer buses, voice and memory budgets, and profiling for hitches on target hardware."
---

# BosskuAI Game Audio Engineer

Use this skill when sound has to react to gameplay state and stay inside a performance budget.

## How this differs from nearby skills

- **`bosskuai-audio-prompting`**: generating music with an AI model. This skill is runtime audio implementation in a game.
- **`bosskuai-csharp-testing`** and **`bosskuai-cpp-coding-standards`**: language-level work on the engine code. This skill is audio architecture and budgets.
- **`bosskuai-performance-profiling`**: general profiling method; use it for non-audio hitches.
- **`bosskuai-video-editing`**: linear video audio, not interactive audio.

## Workflow

1. Write a short audio design brief: three words for the sonic identity, the gameplay states that need audio responses, and the target platforms.
2. Set budgets before production: voice count (real and virtual) per platform, memory per category, audio CPU time per frame on the lowest target hardware. Check the middleware docs for how each is configured.
3. Set up the middleware project first: event hierarchy with consistent naming (`event:/Category/Sub/Name`), bus tree, and VCAs, then platform overrides for sample rate and compression.
4. Route all gameplay audio through named events or event references. Avoid hard-coded asset paths in game code. Game code sets parameters; audio logic lives in the middleware.
5. Give every event a voice limit, priority, and steal mode instead of leaving defaults. Pick formats by role: stream music and long ambience, load short effects into memory, keep UI latency-critical sounds uncompressed or low-latency. Verify against the platform's current guidance.
6. Design adaptive music around a small set of parameters (for example a 0-1 tension value) with a defined source, update rate, and smoothing. Quantize transitions to musical boundaries and keep a neutral layer that can play for a long time.
7. Spatial audio: use 3D for diegetic sounds, drive occlusion from a raycast with a per-frame cap, and match reverb zones to the visual space. Test on headphones and speakers.
8. SFX variation: randomized containers (pitch, volume, multi-shot) so repeats do not sound identical.
9. Profile on target hardware: stress the maximum simultaneous voice count, trigger transitions (combat enter and exit, death, scene change), and check streaming hitches on the real storage medium.

## Guardrails

- Loudness targets and certification rules differ by platform; read the current platform requirements before locking the mix.
- Middleware and engine APIs change between versions; check the installed version.
- Treat budget numbers in templates as placeholders until measured.

## Output format

```text
Budget: [voices, memory, CPU per platform]
Events: [path, priority, voice limit, steal mode]
Parameters: [name, range, source, update rate]
Music transitions: [from -> to, sync point]
Profile results: [worst case, hitch list]
```

Adapted from agency-agents/game-development/game-audio-engineer.md (agency-agents, MIT).
