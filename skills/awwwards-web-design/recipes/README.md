# Recipes

Last updated: 2026-09-25

This folder holds framework-free ES modules and CSS for award-level motion and WebGL. Everything follows the visible-by-default contract: HTML and CSS render all content at rest, and the modules only layer motion on top. If JS, WebGL or the CDN fails, the page stays fully readable.

Tested against gsap 3.15.0, lenis 1.3.26 and three 0.186.1, loaded from jsDelivr through an import map. There is no build step.

| File | What it gives you | Use it for |
|---|---|---|
| `tokens.css` | Easing curves (`--ease-enter`, `--ease-reveal`, `--ease-exit`, `--ease-move`, and named beziers), durations `--dur-1`…`--dur-6`, staggers, fluid type-scale helpers, and a reduced-motion block. The values come from the 51-site probe. | Every build. Pick faces and palette from `references/typography.md` and `references/color.md`; this file sets neither. |
| `boot.html-snippet.html` | An inline `<head>` capability flag, the CSS deadline for the one above-the-fold intro, and the import map. | Paste it into `<head>` before any motion code. |
| `motion-core.js` + `motion-core.css` | Lenis on the GSAP ticker synced to ScrollTrigger, plus data-attribute effects: `data-reveal="lines|image|settle|items"`, `data-parallax`, `data-marquee` (with a pause control), `data-pin="horizontal"` (vertical fallback), `data-stack`, `data-intro`. Exports `init`, `destroy`, `getLenis`, `registerReveal` and `setMotionPreference`. | Scroll choreography for every direction. See `references/motion.md` for when to use each effect. |
| `magnetic.js` | The label drifts toward the pointer while the box stays still (no hover lift). The hover state itself is a tonal change in your CSS. | Primary CTAs and standalone links on pointer-fine devices. |
| `page-transitions.css` + `.js` | Cross-document View Transitions with shared-element pairing and back direction, and `window.pageTransitions.swap()` for SPAs. Without support it falls back to plain navigation. | Multi-page sites. Use Taxi or Swup only when WebGL, audio or scroll state must persist. |
| `webgl-image-hover.js` | One shared canvas that draws DOM-synced planes over `<img data-gl-hover>`, with velocity-driven distortion. The `<img>` never leaves the DOM. | Editorial, archive and portfolio directions (`references/imagery.md`). |
| `three-hero.js` | `mountHero(container, options)` mounts a poster-first 3D object: a PBR physical material, RoomEnvironment lighting, pointer parallax and an optional scroll-scrubbed camera. It uses a DPR clamp, on-demand frames, pauses offscreen and gives reduced-motion users one still frame. | Object-hero and material-calm directions (`references/webgl-3d.md`). Pass your own `geometry`, or load a glTF instead of the lathe demo object. |
| `demo/` | A neutral test harness (system-ui, black on white), not a design template. `index.html` and `about.html` cover motion and transitions; `webgl.html` covers the WebGL recipes. | Seeing each recipe working in isolation. |
| `test_recipes.py` | Playwright checks of 3 pages × 5 scenarios: normal, JavaScript disabled, `prefers-reduced-motion: reduce`, WebGL unavailable, and CDN blocked. It asserts that there are no console errors and that every word, image and control stays visible. | Run it after changing any recipe, and copy the pattern for your own build's QA. |

## Run the tests

```bash
python3 test_recipes.py
```

The script starts its own static server, needs Python Playwright with Chromium, and writes screenshots to `.qa/` (override with `RECIPES_QA_OUT`). Last run (2026-09-25): 15/15 scenario-page runs passed.

`test_recipes_stress.py` adds five more checks:
- **slow CDN:** every jsDelivr request is delayed 4s
- **390px touch viewport:** no horizontal overflow
- **200% zoom:** simulated as a 720×450 viewport
- **keyboard:** Tab through the page, checking that focus is visible and on screen
- **live reduced-motion toggle:** the setting flips after boot

Last run (2026-09-25): 10/10 passed.

```bash
python3 test_recipes_stress.py
```

## Known limitations

- Chromium was the only engine tested. Safari caps Lenis at 60fps and applies View Transitions differently, so check Safari by hand before shipping.
- `three-hero.js` ships a procedural demo object. Real products need a glTF prepared with the `references/webgl-3d.md` pipeline (Draco or Meshopt, KTX2).
- Back/forward-cache restores are not tested automatically.
