---
name: bosskuai-embedded-firmware
description: "Use when writing or reviewing firmware for microcontrollers (ESP32/ESP-IDF, STM32, Nordic nRF/Zephyr, Arduino, PlatformIO, FreeRTOS): task design, ISRs, drivers with timeouts, memory budgets, OTA, power, and debugging."
---

# BosskuAI Embedded Firmware

Use this skill for bare-metal and RTOS firmware where RAM, flash, and timing are limited and a crash means a dead device in the field. What works on a dev board often fails in production.

## How this differs from nearby skills

- **`bosskuai-rust-patterns`**: Rust language idioms; use it alongside if the firmware is Rust.
- **`bosskuai-performance-profiling`**: server and app profiling, not MCU timing.
- **`bosskuai-cybersecurity-risk`**: general app security; this skill covers only firmware-level checks such as OTA integrity.
- **`bosskuai-network-interface-health`**: host network diagnostics, not device protocol stacks.

## Workflow

1. Hardware analysis. Record the MCU family and part, peripherals in use, RAM and flash budget, clock and power constraints, and the SDK version. Use the datasheet, reference manual, and errata as the source of truth.
2. Architecture. Define tasks, priorities, stack sizes, and the queues, semaphores, or event groups between them. Keep ISRs short and defer work to tasks.
3. Drivers. Write each bottom-up and test it alone. Every wait has a timeout. Every SDK or HAL return value is checked. Define what happens after a failed transfer (recover per the reference manual and errata; do not blindly resend).
4. Memory. Allocate statically or from pools after init. Measure stack high-water marks instead of guessing sizes. Keep shared mutable state behind a primitive.
5. Integration and timing. Verify real deadlines with a logic analyser or oscilloscope, not only logs.
6. Fault handling. Test error paths with fault injection, watchdog resets, brown-out, and cold boot.
7. Release. Pin toolchain and library versions (no floating `latest`), record flash/RAM use with headroom, and test OTA update and rollback.
8. Debug aids. Use SWD/JTAG, UART logs, core dumps, and RTOS runtime stats or trace tools your SDK offers.

## Rules of thumb

- Use the `FromISR` variants of RTOS calls inside interrupts; never block there.
- On Zephyr use devicetree and Kconfig rather than hard-coded peripheral addresses.
- STM32 timing-critical paths may suit LL drivers over HAL; check the part's documentation.
- Sleep modes: define wake sources and which RAM is retained; test current draw.
- Bootloaders and OTA: verify image integrity (and authenticity where required) before swapping, and keep a rollback path.

## Guardrails

- Check the current vendor SDK docs for API names and defaults before copying code; they change between versions.
- Do not flash or erase a real device, change fuses or readout protection, or alter bootloader settings without explicit user approval; some of these are irreversible.
- Medical, automotive, aviation, or other safety-critical devices need the applicable standard, independent review, and qualified engineers. This skill organises the work; it is not a safety case.

## Output format

```text
Target: [MCU, SDK version, memory budget]
Task map: [task, priority, stack, communication]
Driver risks: [timeouts, error paths, shared state]
Timing evidence: [measurement method, result]
Release checks: [pinned versions, OTA, watchdog, power]
Open issues: [list]
```

Adapted from agency-agents/engineering/engineering-embedded-firmware-engineer.md (agency-agents, MIT).
