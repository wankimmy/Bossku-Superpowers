---
name: bosskuai-terminal-integration-specialist
description: "Use when embedding a terminal emulator in a Swift app with SwiftTerm: SwiftUI hosting, keyboard and paste input, scrollback, rendering performance, SSH stream bridging, accessibility, and iOS/macOS/visionOS differences."
---

# BosskuAI Terminal Integration Specialist

Use this skill to embed a terminal view in an Apple-platform app with SwiftTerm and connect it to a local process or SSH stream without blocking the UI.

## How this differs from nearby skills

- **`bosskuai-swiftui-patterns`**: general SwiftUI state, composition, and navigation. This skill is the terminal-specific layer inside such an app.
- **`write-swift`**: Swift language and framework code style.
- **`bosskuai-terminal-ops`**: an agent running shell commands in a repo, not building a terminal UI.
- **`bosskuai-desktop-apps`**: desktop app packaging and architecture.
- **`bosskuai-web-performance`**: browser performance. Rendering here uses native text drawing.

## Scope

SwiftTerm-based client-side emulation on Apple platforms. Not server-side terminal management, not other emulator libraries, not cross-platform terminals.

## Workflow

1. Confirm the target platforms and minimum OS versions, and the data source (local pty on macOS, SSH or custom stream elsewhere).
2. Check the installed SwiftTerm version and read its current README and API docs. Do not rely on remembered API names.
3. Host the terminal view in SwiftUI through the platform wrapper (UIViewRepresentable or NSViewRepresentable). Define who owns the view, the session, and its lifecycle (create, resize, suspend, teardown).
4. Bridge I/O: remote bytes go to the terminal feed method on a background queue and UI updates stay on the main actor; keyboard input goes to the write side of the stream. Handle backpressure and partial UTF-8 sequences.
5. Input: special keys, modifier combinations, hardware versus on-screen keyboard, paste (including bracketed paste), and focus handling.
6. Appearance: font, color scheme, cursor style, dynamic type, theme switching.
7. State: connection, disconnection, reconnect, and error messages displayed in the terminal or UI. Multiple sessions and restoration of state.
8. Scrollback and search: set a buffer size you can afford in memory and test long sessions.
9. Accessibility and selection: VoiceOver behaviour, text selection, copy to clipboard, and large-text support.
10. Test: run with high-volume output, resize, background and foreground, and network drop. Profile CPU and memory with Instruments.

## Guardrails

- Do not hard-code credentials or private keys for SSH. Use the system keychain and the user's approved auth flow.
- Validate host keys; do not silently accept unknown ones.
- Do not log terminal output that may contain secrets.
- App Store or platform rules about terminals, networking, and background execution change; check the current guidelines.

## Output format

```text
Targets: [platforms, OS versions, SwiftTerm version]
Architecture: [view host, session owner, I/O threading]
Input and accessibility notes: [..]
Failure handling: [disconnect, resize, long output]
Verification: [tests, Instruments traces]
Open risks: [..]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/spatial-computing/terminal-integration-specialist.md (agency-agents, MIT).
