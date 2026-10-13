---
name: bosskuai-iot-fleets
description: "Use when designing or operating a fleet of IoT or edge devices: per-device identity and provisioning, MQTT telemetry for flaky networks, signed staged OTA firmware updates with rollback, and fleet observability."
---

# BosskuAI IoT Fleets

Use this skill when devices live where you cannot reach them, on networks that drop, running firmware you cannot casually redeploy. A bad update can mean a physical visit per device.

## How this differs from nearby skills

- **`bosskuai-data-pipelines`**: backend ingestion and transformation. This skill covers the device side, the protocol and the update path.
- **`bosskuai-observability-sre`**: server-side logs, metrics and SLOs. Fleet health signals here come from devices that may be offline.
- **`bosskuai-devops-iac`**: release strategy for cloud workloads. OTA firmware needs stricter staging and rollback.
- **`bosskuai-cybersecurity-risk`**: general trust-boundary review; here security means device identity, signed images and revocation.

## Workflow

1. Model the fleet: device count, hardware revisions, connectivity type, duty cycle, power limits, physical reachability.
2. Identity and provisioning: each device gets a unique, revocable identity (X.509 or secure-element keys), never a shared fleet credential. Assume the factory is untrusted; generate keys on the device.
3. Telemetry: define topics scoped per device, QoS, bounded edge buffering, upload with original timestamps on reconnect, and server-side dedupe on device id plus sequence. Commands carry a time-to-live and an idempotency id.
4. Budget cardinality and bandwidth for the full fleet, not a lab. Aggregate at the edge and sample deliberately.
5. OTA design: signed images verified on-device, dual-bank (A/B) partitions, boot-once then confirm health, and bootloader rollback to the last known good image if no healthy check-in arrives in the watchdog window.
6. Rollout: canary on real devices across hardware revisions, then widen in stages, each gated on the post-update healthy check-in rate. Halt automatically when a stage falls below target.
7. Decide what runs on the device versus in the cloud (latency, bandwidth, offline operation) and how edge software updates safely.
8. Observability: firmware version distribution, last-seen gap, post-OTA health, error and reboot telemetry, battery and signal where relevant.
9. Plan for the long tail: old firmware stays in the field, so keep protocols backward compatible and plan migration.

## Guardrails

- Never push firmware to the whole fleet at once.
- An unsigned update path is a remote code execution risk. Verify signatures on the device.
- Check the current docs for your broker, device SDK and cloud IoT service; features and limits differ.
- Do not start a real rollout, revoke certificates or change production device config without the user's explicit approval.

## Output format

```text
Fleet model: [devices, revisions, connectivity]
Identity flow: [keys, registry, revocation]
Telemetry design: [topics, QoS, buffering, dedupe, budget]
OTA plan: [image signing, partitions, stages, health gate, halt rule]
Observability: [signals, alert conditions]
Legacy plan: [old versions, compatibility window]
```

Adapted from agency-agents/engineering/engineering-iot-fleet-engineer.md (agency-agents, MIT).
