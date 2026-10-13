---
name: bosskuai-video-streaming
description: "Use when delivering video over HLS or DASH: ffmpeg bitrate ladders, CMAF packaging, segment and latency choices, DRM in the startup path, CDN caching and egress cost, and QoE metrics like rebuffer ratio."
---

# BosskuAI Video Streaming

Use this skill to design and debug adaptive-bitrate video delivery, judged by what viewers experience (start time, stalls, failures) and what delivery costs.

## How this differs from nearby skills

- **`bosskuai-video-editing`**: cutting and assembling footage. This skill starts once there is a master file to deliver.
- **`bosskuai-videodb`**: indexing, searching, and editing video through an SDK, not building a delivery pipeline.
- **`bosskuai-web-performance`**: page speed and Core Web Vitals; use it for the player page, and this skill for the stream.
- **`bosskuai-cost-optimization`**: general cloud spend. Egress for video is covered here at the ladder and cache level.
- **`bosskuai-observability-sre`**: general telemetry and alerting; this skill defines which player metrics to collect.

## Workflow

1. Profile the use: VOD, standard live, low-latency live, or real-time interactive. Profile content complexity, target devices, and the network mix of real viewers.
2. Design the bitrate ladder to the content: a fast, low-bitrate startup rung, rungs spaced far enough apart to matter, and only rungs your devices and networks can use. Prefer per-title or per-scene analysis when volume justifies it. Judge quality with an objective metric such as VMAF plus viewing checks.
3. Encode with aligned keyframes and closed GOPs so all rungs switch cleanly at segment boundaries. Choose codecs by device reach; add newer codecs as extra rungs with fallback, not replacements.
4. Package once in CMAF and emit both HLS and DASH manifests, avoiding duplicate encodes. Validate both manifests and test playback on the real device matrix (Safari and iOS especially).
5. Pick segment and chunk durations deliberately: longer for VOD cache efficiency, shorter for live, chunked low-latency only where the latency is worth the request cost.
6. DRM: use the systems your device matrix requires, fetch licenses in parallel with startup, and test key rotation on protected real devices.
7. CDN: long caching for immutable segments, short for live manifests, clean cache keys, origin shield, byte-range support. Measure hit ratio and egress per hour delivered.
8. QoE: instrument time to first frame, rebuffer ratio, play-failure rate, average bitrate and switch rate, and exit before start. Segment by device and network, and alert on the worst cohort.
9. Test on throttled and lossy networks, not only on office broadband. Change one variable at a time (startup rung, segment size, ABR config) and compare against the metrics.

## Guardrails

- Check the installed ffmpeg and packager versions and their current documentation; flags and defaults change.
- Targets (latency, rebuffer ratio, bitrates) come from your audience data and business needs, not from fixed numbers in any guide.
- Respect content licensing, DRM terms, and regional rules. Do not remove or bypass protection.
- Do not change production encoding, DRM keys, or CDN config without explicit approval and a rollback.

## Output format

```text
Use case and audience: [VOD/live/LL/real-time, devices, networks]
Ladder: [rung - resolution - bitrate - role]
Packaging: [container, manifests, segment/chunk duration]
DRM and CDN: [systems, cache rules, hit ratio]
QoE baseline and target: [startup, rebuffer, failures]
Experiments: [variable - result]
```

Adapted from agency-agents/engineering/engineering-video-streaming-engineer.md (agency-agents, MIT).
