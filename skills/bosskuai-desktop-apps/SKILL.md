---
name: bosskuai-desktop-apps
description: "Use when building or reviewing Electron or Tauri desktop apps: IPC and process isolation, code signing and notarization, auto-update and rollback, native OS integration, and startup, memory, and installer-size budgets."
---

# BosskuAI Desktop Apps

Use this skill when a web-technology app is shipped as a desktop app (Electron or Tauri) and the hard parts are security at the process boundary, signing, updates, and footprint.

## How this differs from nearby skills

- **`bosskuai-windows-desktop-e2e`**: UI automation tests for native Windows apps (WPF, WinForms, Qt). This skill is about building and releasing Electron/Tauri apps.
- **`bosskuai-expo-react-native`**: mobile apps and EAS, not desktop.
- **`bosskuai-cybersecurity-risk`**: general threat review. Here the focus is the renderer-to-privileged boundary.
- **`bosskuai-ci-cd-pipelines`**: generic pipeline YAML. Here only the sign, notarize, stage, and rollback steps for desktop releases.
- **`bosskuai-web-performance`**: browser Core Web Vitals, not installer size or idle memory.
- **`bosskuai-swiftui-patterns`**: native Apple UI, not web-in-shell apps.

## Principles

- Treat the renderer or webview as untrusted, even for your own code, because XSS makes it not your code. Electron: context isolation on, node integration off, sandbox on. Tauri: scope capabilities to what the window needs. Check the installed version's current defaults.
- IPC is a public API. Each channel or command validates input on the privileged side, checks authorization for sensitive actions, and does one narrow thing. Prefer `saveUserExport(data)` with a user-picked path over `writeFile(path, data)`.
- Remote content gets no privileges. Load it in a sandboxed view with no IPC, or a deny-by-default allowlist.
- Ship signed. Windows code signing and macOS signing plus notarization (hardened runtime) are release-blocking. Keep signing keys in a vault or HSM, not as files in CI.
- The updater is the most critical code. A broken updater cannot fix itself. Use signed update manifests, staged rollout, a health check, and a tested rollback.
- Follow each platform's conventions separately: menu placement, Cmd vs Ctrl, tray behavior, installer expectations.
- Measure footprint: cold start, idle memory, installer size, idle CPU. Set budgets and fail the build on regressions.
- Plan for offline. Local-first data with a visible sync status beats a spinner.

## Choosing Electron or Tauri

Decide in writing, before the first commit, from: size and memory budget, need for identical rendering everywhere, team skills (Node vs Rust), native module needs, and plugin maturity. Tauri uses the system webview, so rendering varies by OS and must be tested on the matrix. Electron ships its own Chromium, so it is consistent but larger.

## Workflow

1. Choose the runtime and record why.
2. Define the full IPC contract as typed, validated verbs before building UI against it.
3. Stand up signing, an update feed, and a rollback drill with a walking-skeleton release on an internal channel.
4. Add OS integrations (tray, shortcuts, deep links, notifications) with per-platform acceptance criteria.
5. Add footprint checks to CI.
6. Test signed builds on real macOS, Windows, and Linux machines, fresh install and upgrade.
7. Roll out in stages, watching crash-free rate and update success before widening.

## Checklist

- Every IPC channel is listed in one place, validated, and as narrow as possible.
- No generic filesystem, shell, or URL-open passthrough to the renderer.
- Strict CSP; no remote code in privileged windows.
- Builds signed on all shipped platforms; notarized on macOS.
- Update manifest signed; rollback path exercised before release.
- Certificate expiry dates tracked.
- Single-instance and deep-link behavior tested.
- Crash reporting with symbols uploaded.

## Output format

```text
Runtime choice: [Electron / Tauri, reason]
IPC surface: [verbs, validation, authorization]
Release path: [signing, notarization, update channel, rollout steps, rollback]
Platform notes: [per-OS differences]
Budgets: [start, memory, size] and how measured
```

Adapted from agency-agents/engineering/engineering-desktop-app-engineer.md (agency-agents, MIT).
