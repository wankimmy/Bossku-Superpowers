---
name: bosskuai-expo-react-native
description: "Use when building React Native or Expo apps with Expo Router, EAS Build or Update, development builds, config plugins, native modules, navigation, offline storage, notifications, deep links, permissions, device performance, and iOS or Android differences."
---

# BosskuAI Expo / React Native

Use this skill when building, auditing, or debugging a React Native app, with or without Expo, where the answer depends on native platform behavior rather than on React alone.

## How this differs from nearby skills

- **`bosskuai-react-development`**: React on the web; hooks and state advice carry over, DOM and routing advice does not.
- **`bosskuai-mobile-app-release`**: credentials, store review, rollouts, and OTA policy; this skill gets the app correct on device.
- **`bosskuai-api-design`** / backend skills: the API the app calls.
- **`animate-expo`** (emil-skills): motion, gestures, sheets, and haptics, including the Reanimated and Gesture Handler code; this skill owns app structure, native behavior, and builds.

## Mindset

- The device is the truth. Simulators hide permission prompts, memory pressure, slow networks, and real keyboards.
- Two threads: JS and UI. Anything that blocks JS drops frames; anything heavy belongs in worklets, native modules, or off the render path.
- Stay on managed Expo until a real native need appears; then add a config plugin or a development build, not a bare eject.
- Every permission is a product decision with a purpose string and a timing.

## Orient before changing anything

1. `npx expo-doctor` and `npx expo install --check`: SDK version, mismatched native dependencies.
2. `app.json` / `app.config.ts`: bundle id / package, scheme, permissions, plugins, `runtimeVersion` policy, Hermes, and on SDK 54 or older the New Architecture flag.
3. `eas.json`: build profiles (development, preview, production), channels, env per profile.
4. Navigation: Expo Router (file-based, groups, layouts) or React Navigation; auth gating approach.
5. Data and storage: TanStack Query, MMKV, SQLite/expo-sqlite, SecureStore; offline expectations.
6. Expo Go vs development build: any custom native module, notification, or in-app purchase means a development build.

## Rules that catch most React Native bugs

- Long lists: `FlashList` or `FlatList` with stable keys, `getItemLayout` where sizes are fixed, never a `ScrollView` of hundreds of children.
- Inline objects and functions on list items re-render every row; memoize row components and pass primitives.
- Reanimated: animation math in worklets (`useAnimatedStyle`, `useSharedValue`); never read shared values on the JS thread inside render.
- Gesture Handler needs `GestureHandlerRootView` at the root; nested gestures need explicit `simultaneousWithExternalGesture`.
- Safe areas via `react-native-safe-area-context` insets, not hard-coded padding; notch, home indicator, and Android navigation bar differ.
- Keyboard: `KeyboardAvoidingView` `behavior` differs per platform; test with a real keyboard and a small screen.
- Android hardware back: handle it in Expo Router or `BackHandler`; do not trap the user.
- Text must be inside `<Text>`; layout uses flexbox with `flexDirection: 'column'` default.
- Images: `expo-image` with explicit sizes and caching; never decode large images on the JS side.
- Secrets: `SecureStore` for tokens; `AsyncStorage`/MMKV only for non-sensitive data; `EXPO_PUBLIC_*` env is bundled into the app and is public by definition.
- Networking: iOS ATS blocks plain HTTP; Android 9+ blocks cleartext unless configured. Retry with backoff; show offline state.
- Deep links: `scheme` for custom links, Universal Links (AASA) and App Links (assetlinks.json) for HTTPS; test cold start and warm start paths.
- Notifications: request permission in context, not at launch; test on physical devices with production credentials; Android needs a channel.
- OTA (EAS Update): only JS and assets; any native change (new module, permission, SDK upgrade) requires a new build and a new `runtimeVersion`.
- New Architecture: mandatory from React Native 0.82 / Expo SDK 55 (SDK 54 is the last with a legacy option). Before upgrading past SDK 54, confirm every native library supports it; replace legacy-only modules instead of pinning the SDK. Fabric/TurboModules break old bridge-based modules.
- Platform targets: Play requires a recent `targetSdkVersion` each year; Apple requires current Xcode SDK and privacy manifests for listed APIs.

## Architecture that holds up

- Expo Router route groups: `(auth)`, `(app)`; a root layout that redirects on session state; typed routes on.
- Server state in TanStack Query persisted to MMKV for instant cold-start UI; mutations queued offline where the product needs it.
- Feature folders (`features/<name>/{components,hooks,api,schema}`) with zod schemas shared with the backend when possible.
- Theming through a single token module; i18n with `expo-localization` + i18next or Lingui from day one if more than one language is plausible.
- Crash and error reporting (Sentry) with source maps uploaded per build.
- Offline-first: decide the sync and conflict rule (last write wins, server wins, or merge) per data type before building the queue, and show the user pending and failed states.
- Biometric sign-in unlocks a stored credential through `expo-local-authentication` and `SecureStore`; keep a non-biometric fallback and handle enrolment changes.
- Background work and location cost battery: request the lowest accuracy and shortest background window the feature needs, and test on a real device with the battery profiler.

## Performance on device

- Profile release builds on a mid-range Android device, not the iOS simulator.
- Startup: lazy-require heavy screens, avoid top-level work in modules, measure with `expo-atlas` for bundle composition.
- Frames: React Native DevTools / Perf Monitor; move heavy work to worklets or native; avoid bridging in loops.
- Memory: unsubscribe listeners on unmount, cap image cache, page data.

## Testing

- `jest-expo` + Testing Library for React Native for components and hooks.
- Maestro (or Detox) flows on real devices or emulators for critical paths; run on EAS-built binaries in CI.
- Manual matrix: smallest supported iPhone, a mid-range Android, both OS minimum versions, dark mode, large font sizes.

## Verification

```bash
npx expo-doctor && npx expo install --check
tsc --noEmit && eslint .
jest
eas build --profile preview --platform all   # then install on devices
```

## Guardrails

- Do not eject to bare workflow to solve something a config plugin or development build already solves.
- Do not ship native changes through EAS Update.
- Do not store tokens in AsyncStorage or ship secrets in `EXPO_PUBLIC_*`.
- Do not test only on simulators before a release candidate.
- Do not upgrade to Expo SDK 55+ / React Native 0.82+ until every native dependency supports the New Architecture.

## Output format

```text
Expo SDK: [xx] - RN: [x.y] - Workflow: [managed | dev build | bare] - Legacy-arch deps: [none / list]
Router: [Expo Router | React Navigation] - Data: [...] - Storage: [...]

Findings:
  P0/P1/P2 - [file:line or config key] - [issue] - [fix]

Change plan: [smallest correct change]
Device verification: [devices/OS versions tested, results]
```

## References

- `../../references/checklists/expo-react-native-checklist.md`
- `../../references/checklists/react-development-checklist.md`
- `../../references/checklists/mobile-app-release-checklist.md`

Offline, biometric and battery bullets adapted in part from engineering/engineering-mobile-app-builder.md (agency-agents, MIT).

## Screen-level patterns

- **Thin route files**: a route reads and validates params, then hands off to a screen component in `features/` or `components/`. Deep links and dynamic routes deliver untrusted strings, so parse them with a schema (for example `z.string().uuid()`) and `router.replace('/not-found')` on failure.
- **State has one home each**: server data in a query cache (never copied into a client store); UI state in a small store or context (start with local `useState`); route state in router params; forms in a form library plus schema resolver; tokens in SecureStore; non-secret persistence in MMKV or AsyncStorage.
- **Validate at the boundary**: parse API responses, route params, and push payloads with a schema, and infer types from it.
- **Every screen renders loading, error, and empty states** (not just a spinner); errors use an alert accessibility role. Pull-to-refresh via `onRefresh` plus `refreshing`.
- **Lists**: memoized row components and a memoized `renderItem`, stable `keyExtractor`; tune `initialNumToRender` and `windowSize` on `FlatList`; `FlashList` for large or mixed lists.
- **Native APIs live in `use*` hooks**, never in JSX. Track a status (loading, denied, granted) rather than just a value, so the UI can tell "still loading" from "permission denied". Use an `active` flag in effect cleanup to ignore stale results after unmount.
- **Styling**: pick one system (StyleSheet or a utility-class library) and stay with it; no inline style objects on hot paths.
- **Forms**: set `keyboardType`, `autoCapitalize`, and an `accessibilityLabel` on inputs; respect safe areas and Dynamic Type from the start.
- **Never ship a real secret in the bundle**; privileged calls stay server-side and only public keys protected by backend rules go in the app.

Adapted in part from ECC skills/react-native-patterns (affaan-m/ECC, MIT).
