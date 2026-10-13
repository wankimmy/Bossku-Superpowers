---
name: bosskuai-react-development
description: "Use when building or auditing React and TypeScript frontends, including components, hooks, state management, data fetching and caching, forms, routing, rendering performance, accessibility, Testing Library, and Playwright; use the Expo skill for React Native."
---

# React development

For React/TypeScript frontend work where the answer depends on React's rendering model and hook rules, not generic UI advice.

1. **Orient first.** Check `package.json` for the React major (19 changes `ref`/`forwardRef`/`use()`), the framework (Vite SPA, Next App/Pages Router, React Router 7), and whether `strict` TypeScript and the React Compiler are on. Use whatever state/data library already exists; don't add another.
2. **Place new state correctly**: URL for shareable UI state, `useState` for local, context for low-frequency globals split by update frequency, Zustand/Jotai for high-frequency shared state, TanStack Query for server data, react-hook-form + zod for forms.
3. **Write effects to synchronize with the outside world** — subscriptions, DOM APIs, timers — never derived state or clicks. A fetch inside `useEffect` needs an abort/ignore flag or it races on navigation; prefer a loader or TanStack Query. Never silence `exhaustive-deps`; fix the dependency.
4. **Catch these bugs**: stable, non-index `key`s on lists; no new object/array/function literals handed down every render; no hooks behind a conditional; never flip an input between controlled and uncontrolled; pair risky regions with an error boundary and Suspense.
5. **Build accessibility in, not after**: native elements before ARIA, focus management on route/modal changes, labeled inputs with errors wired to `aria-describedby`, 4.5:1 contrast, `prefers-reduced-motion` honored.
6. **Measure before optimizing.** Profile with React DevTools; only then add `memo`/virtualization/code-splitting to the slow component.
7. **Test like a user**: queries by role or label, `userEvent`, MSW for network, one Playwright flow per critical path. Never ship `any` at a component or API boundary.
8. **Verify**: `tsc --noEmit`, `eslint . --max-warnings=0`, `vitest run`, then the Playwright flow. A green unit suite alone does not prove the flow works.

If the state or framework choice is open and nobody can answer, use whatever the repo already uses; don't add a second state library where the URL or TanStack Query already does.

The full bug list with Next.js/React-version specifics, the state table, and the output format: `reference.md`.

## Extra checks

- Derive values during render; storing a derived value in state plus an effect adds a render and can desync.
- An error boundary does not catch errors in event handlers or async code; handle those where they happen.
- Never import a Server Component from a Client Component file; pass it in as `children` or a prop.
- Place Suspense close to the data so content reveals progressively, not at the route root.
- A custom data hook that takes an inline fetcher or options object must hold them in refs (or require stable inputs), or its refetch changes every render and the effect loops forever.
- Copy before sorting in `useMemo` (`[...items].sort(...)`); `sort` mutates in place. Extract a custom hook only when the same hook sequence appears in two or more components.
- `React.memo` only when the component re-renders often, props are usually equal, and render is measurably costly; otherwise the equality check is pure overhead. Use `useSyncExternalStore` for external stores so concurrent rendering stays safe.
- Virtualize once visible rows pass roughly 50 non-trivial items.
- Custom widgets (dropdown, combobox, modal): arrow/Enter/Escape keys work, focus moves in on open and returns to the trigger on close.

Adapted in part from ECC skills/react-patterns and skills/frontend-patterns (affaan-m/ECC, MIT).
