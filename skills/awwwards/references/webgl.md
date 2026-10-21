<!-- Generated from tests/nexttest by tests/_gen/build.py; edit there, not here. -->
# WebGL

WebGL is standard on award-winning sites (6 of 7 recent Site of the Day portfolios). It is
worth adding only when it expresses the concept and holds 60 fps on a mid-range phone. The
engine's optional GL module (code at the end of this file, in `src/engine/gl/`) gives you one
shared OGL canvas with two primitives. Extend them rather than adding a second renderer.
Install: `npm i ogl`.

## Primitives

1. **DOM-synced planes** (`data-gl`): every `<figure data-gl>` gets a plane drawn exactly over
   its rect each frame. The `<img>` stays in the DOM (SEO, a11y, LCP, fallback) at opacity 0.
   Built-in look: in-shader object-fit cover, hover zoom and pointer push, chromatic split from
   scroll velocity, organic bottom-up reveal, bend with scroll velocity.
   Procedural variant (`data-gl="procedural"`): seeded fbm field in three palette colors with grain.

   | Attribute | Effect |
   |---|---|
   | `data-gl` | Image plane for the `<img>` inside. Remote images need `crossorigin="anonymous"` |
   | `data-gl="procedural" data-seed="2.4" data-colors="#a,#b,#c"` | Generative cover in the palette (for projects without imagery). Put a `.gl-fallback` div with `role="img"` + `aria-label` inside |
   | `data-gl-instant` | Visible immediately (hero media, the target of a shared-element transition) |
   | `data-gl-scrub` | Reveal follows scroll position (0 as it enters, 1 at 25% from the top) |
   | `data-gl-duration="2.4"` | Length of the timed reveal in seconds (default 1.6) |

2. **Fullscreen layer** (`setBackground(fragment, uniforms)`): a shader under the planes for skies,
   fields, gradients, noise, light. Built-in uniforms: `uTime, uResolution, uScroll (0..1),
   uScrollY, uVelocity, uMouse (smoothed 0..1)`; varying `vUv`.

Customize the plane shaders in `src/engine/gl/shaders.ts` per concept (that is expected):
change the hover, the reveal shape and the velocity response. Keep the uniform names so the
engine can drive them.
Tested example: a photographer's "darkroom" replaced `imageFragment` so prints develop out of
paper white (dark tones first, uneven like tray agitation) under a red safelight cast, and hover
turns the room lights on (true color); `data-gl-scrub` tied development to scroll position.

**Layering rules (the canvas is UNDER the content):**
- No background on a `[data-gl]` element or its ancestors inside `<main>` (the engine forces
  `background: none` on GL elements; `shoot.mjs` reports `glHidden` for covered planes).
- Text over a GL image: put a gradient scrim as a pseudo-element on the container in the DOM.
- Fixed UI over GL imagery: `mix-blend-mode: difference` or a scrim.

## Recipes

### Scroll-driven sky / time of day (fullscreen)
```ts
import { onPage, setBackground } from '../engine';
const frag = /* glsl */ `
precision highp float;
varying vec2 vUv;
uniform float uTime, uScroll;
uniform vec2 uMouse, uResolution;
uniform vec3 uA, uB, uC;           // palette stops (dawn, noon, dusk)
float hash(vec2 p){ return fract(sin(dot(p, vec2(12.9898,78.233))) * 43758.5453); }
void main() {
  float t = uScroll;
  vec3 top = mix(mix(uA, uB, smoothstep(0.0, 0.5, t)), uC, smoothstep(0.5, 1.0, t));
  vec3 bottom = mix(top, vec3(1.0), 0.35 - 0.25 * t);
  vec2 sun = vec2(0.2 + 0.6 * t, 0.85 - 0.6 * abs(t - 0.5) * 2.0) + (uMouse - 0.5) * 0.03;
  float glow = smoothstep(0.35, 0.0, distance(vUv * vec2(uResolution.x / uResolution.y, 1.0), sun * vec2(uResolution.x / uResolution.y, 1.0)));
  vec3 col = mix(bottom, top, vUv.y) + glow * 0.25;
  col += (hash(vUv * uResolution + fract(uTime)) - 0.5) * 0.03; // grain
  gl_FragColor = vec4(col, 1.0);
}`;
// Register once, in setupMotion (src/motion/setup.ts); it persists across pages:
setBackground(frag, { uA: { value: [0.62, 0.72, 0.86] }, uB: { value: [0.97, 0.96, 0.92] }, uC: { value: [0.93, 0.47, 0.25] } });
```
Text over a moving background must keep AA contrast at every scroll position: pick ink colors
that work on all stops, or tween the ink color with the same progress.
`setBackground` returns `null` when GL is off (reduced motion, no WebGL): style `html` with a
static gradient as the fallback.

### Image hover variants (edit `imageFragment`)
- **Liquid:** offset `uv` by `fbm(uv * 3.0 + uTime * 0.2) * 0.03 * uHover`.
- **Pixel sort / mosaic:** `uv = floor(uv * mix(400.0, 24.0, uHover)) / mix(400.0, 24.0, uHover)`.
- **Lens:** inside `distance(vUv, uMouse) < 0.2`, scale uv toward uMouse by `1.0 - 0.3 * uHover`.
- **Duotone to color:** mix luminance-mapped duotone (palette) with the true color by `uHover`.

### Reveal variants (edit `revealMask`)
- Horizontal wipe: use `uv.x`. Circle from center: `distance(uv, vec2(0.5))`.
- Blinds: `fract(uv.y * 8.0)` compared to `uReveal`.

### Text in WebGL
Prefer real DOM text. If a concept truly needs GL text (displacing a giant word), render the word
into a 2D canvas (`ctx.font` with the loaded webfont after `document.fonts.ready`), use it as a
texture on a `data-gl`-like plane, and keep the DOM word visually hidden but present.

### 3D models
Only when the concept is spatial. Use Three.js + `GLTFLoader` with Draco/Meshopt-compressed GLB
under 1.5 MB, lazy-import it (`await import('three')`) after the hero paints, and render in its
own canvas only while visible. Never block the loader on a model.

## Performance rules

- One canvas, DPR capped at 2 (engine), `antialias: false`, geometry segments ≤ 32.
- Fragment work: ≤ 5 fbm octaves per fullscreen pixel; avoid loops over textures; no
  `discard`-heavy shaders on large areas.
- Pause when the tab is hidden (engine) and skip planes off-screen (engine).
- Textures: images ≤ 2000 px on the long edge, compressed (AVIF/WebP for DOM, the GL reads the
  decoded `<img>`). Remote images need CORS (`crossorigin="anonymous"`).
- Test: the `shoot.mjs` FPS sample must stay at 55 or above on desktop. For heavy scenes,
  throttle the CPU 4x in DevTools and reduce octaves or DPR when it drops.
- Reduced motion, Save-Data, or no WebGL: the engine never starts GL; DOM images and the static
  fallback must look finished, not broken.

## Module code

Add these two files only when the site uses GL. The core (`engine.md`) imports `./gl`; without
GL, delete the lines marked `// GL` there instead.

### `src/engine/gl/index.ts`

```ts
// DOM-synced WebGL planes on ONE shared canvas (the standard award-site technique).
//   <figure data-gl>                         image plane: uses the <img> inside (keep the img: SEO, a11y, fallback)
//   <figure data-gl="procedural" data-seed="3" data-colors="#0d0d0d,#e9e4da,#ff4d00">  generative cover
//   data-gl-scrub (reveal tied to scroll position)  data-gl-duration="2.4" (timed reveal length)  data-gl-instant
// The DOM element stays in layout; the canvas draws on top of its rect each frame.
// Disabled under reduced motion, without WebGL, or with Save-Data; DOM images then show as-is.
import { Renderer, Camera, Transform, Plane, Program, Mesh, Texture, Vec2, Triangle } from 'ogl';
import { gsap } from 'gsap';
import { vertex, imageFragment, proceduralFragment } from './shaders';
import { scrollState } from '../scroll';
import { prefersReducedMotion } from '../env';

type Item = { el: HTMLElement; mesh: Mesh; program: Program; hover: { v: number }; revealed: boolean; scrub: boolean; io?: IntersectionObserver; off: () => void };

let renderer: Renderer | null = null;
let camera: Camera;
let scene: Transform;
let geometry: Plane;
const items: Item[] = [];
const textures = new Map<string, Texture>();
let vw = 0, vh = 0, time = 0, velocity = 0;
let bg: { scene: Transform; program: Program } | null = null;
const mouse = { x: 0.5, y: 0.5, tx: 0.5, ty: 0.5 };

const hex = (h: string) => {
  const n = parseInt(h.replace('#', ''), 16);
  return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
};

export function glSupported() {
  if (prefersReducedMotion()) return false;
  if ((navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData) return false;
  try { return !!document.createElement('canvas').getContext('webgl'); } catch { return false; }
}

export function initGL() {
  if (renderer || !glSupported()) return;
  renderer = new Renderer({ dpr: Math.min(devicePixelRatio, 2), alpha: true, antialias: false, premultipliedAlpha: true });
  const gl = renderer.gl;
  gl.canvas.classList.add('gl-canvas');
  gl.canvas.setAttribute('aria-hidden', 'true');
  // Lives in a host element that persists across navigations (#gl in the layout).
  (document.getElementById('gl') || document.body).appendChild(gl.canvas);
  camera = new Camera(gl, { near: -10, far: 10 });
  camera.position.z = 1;
  scene = new Transform();
  geometry = new Plane(gl, { widthSegments: 24, heightSegments: 24 });
  document.documentElement.classList.add('gl-on');
  resize();
  addEventListener('resize', resize);
  addEventListener('pointermove', (e) => { mouse.tx = e.clientX / vw; mouse.ty = 1 - e.clientY / vh; }, { passive: true });
  gsap.ticker.add(render);
}

/**
 * Fullscreen shader layer drawn under the DOM planes (skies, fields, gradients, noise).
 * Built-in uniforms: uTime (s), uResolution (px), uScroll (0..1 page progress), uScrollY (px),
 * uVelocity (smoothed scroll velocity), uMouse (0..1, smoothed). Varying: vUv.
 * Persists across navigations until clearBackground(). Returns the Program (tween its uniforms).
 */
export function setBackground(fragment: string, uniforms: Record<string, { value: unknown }> = {}) {
  if (!renderer) return null;
  clearBackground();
  const gl = renderer.gl;
  const program = new Program(gl, {
    vertex: `attribute vec2 uv; attribute vec2 position; varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position, 0.0, 1.0); }`,
    fragment,
    uniforms: {
      uTime: { value: 0 }, uResolution: { value: new Vec2(vw, vh) }, uScroll: { value: 0 }, uScrollY: { value: 0 },
      uVelocity: { value: 0 }, uMouse: { value: new Vec2(0.5, 0.5) }, ...uniforms,
    },
    depthTest: false,
    depthWrite: false,
  });
  const scene = new Transform();
  new Mesh(gl, { geometry: new Triangle(gl), program }).setParent(scene);
  bg = { scene, program };
  return program;
}
export function clearBackground() { bg = null; }

function resize() {
  if (!renderer) return;
  vw = innerWidth; vh = innerHeight;
  renderer.setSize(vw, vh);
  camera.orthographic({ left: -vw / 2, right: vw / 2, top: vh / 2, bottom: -vh / 2, near: -10, far: 10 });
}

function loadTexture(img: HTMLImageElement, program: Program) {
  const src = img.currentSrc || img.src;
  const gl = renderer!.gl;
  let tex = textures.get(src);
  const apply = (t: Texture) => {
    program.uniforms.tMap.value = t;
    const im = t.image as HTMLImageElement;
    program.uniforms.uImage.value.set(im.naturalWidth || 1, im.naturalHeight || 1);
  };
  if (tex) return apply(tex);
  tex = new Texture(gl, { generateMipmaps: false, minFilter: gl.LINEAR });
  textures.set(src, tex);
  const im = new Image();
  im.crossOrigin = 'anonymous';
  im.decoding = 'async';
  im.onload = () => { tex!.image = im; apply(tex!); };
  im.src = src;
}

function add(el: HTMLElement) {
  if (!renderer) return;
  const gl = renderer.gl;
  const procedural = el.dataset.gl === 'procedural';
  const uniforms: Record<string, { value: unknown }> = {
    uPlane: { value: new Vec2(1, 1) },
    uTime: { value: 0 },
    uHover: { value: 0 },
    uVelocity: { value: 0 },
    uReveal: { value: el.hasAttribute('data-gl-instant') ? 1 : 0 },
    uMouse: { value: new Vec2(0.5, 0.5) },
  };
  if (procedural) {
    const [c1, c2, c3] = (el.dataset.colors || '#111111,#888888,#eeeeee').split(',').map(hex);
    Object.assign(uniforms, { uC1: { value: c1 }, uC2: { value: c2 }, uC3: { value: c3 }, uSeed: { value: parseFloat(el.dataset.seed || '1') } });
  } else {
    const blank = new Texture(gl, { image: new Uint8Array([0, 0, 0, 0]), width: 1, height: 1 });
    Object.assign(uniforms, { tMap: { value: blank }, uImage: { value: new Vec2(1, 1) } });
  }
  const program = new Program(gl, { vertex, fragment: procedural ? proceduralFragment : imageFragment, uniforms, transparent: true });
  const mesh = new Mesh(gl, { geometry, program });
  mesh.setParent(scene);
  const img = el.querySelector('img');
  if (img && !procedural) {
    if (img.complete && img.naturalWidth) loadTexture(img, program);
    else img.addEventListener('load', () => loadTexture(img, program), { once: true });
  }
  const hover = { v: 0 };
  const enter = () => gsap.to(hover, { v: 1, duration: 0.9, ease: 'expo.out' });
  const leave = () => gsap.to(hover, { v: 0, duration: 0.9, ease: 'expo.out' });
  const move = (e: PointerEvent) => {
    const r = el.getBoundingClientRect();
    program.uniforms.uMouse.value.set((e.clientX - r.left) / r.width, 1 - (e.clientY - r.top) / r.height);
  };
  el.addEventListener('pointerenter', enter);
  el.addEventListener('pointerleave', leave);
  el.addEventListener('pointermove', move);
  const scrub = el.hasAttribute('data-gl-scrub');
  const item: Item = {
    el, mesh, program, hover, revealed: false, scrub,
    off: () => {
      el.removeEventListener('pointerenter', enter);
      el.removeEventListener('pointerleave', leave);
      el.removeEventListener('pointermove', move);
    },
  };
  if (!el.hasAttribute('data-gl-instant') && !scrub) {
    item.io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting && !item.revealed) {
        item.revealed = true;
        gsap.to(program.uniforms.uReveal, { value: 1, duration: parseFloat(el.dataset.glDuration || '1.6'), ease: 'expo.out', delay: parseFloat(el.dataset.delay || '0') });
        item.io?.disconnect();
      }
    }, { rootMargin: '0px 0px -10% 0px' });
    item.io.observe(el);
  }
  items.push(item);
}

/** Scan a page for [data-gl] elements. Call on every page load. */
export function mountGL(root: ParentNode = document) {
  if (!renderer) return;
  root.querySelectorAll<HTMLElement>('[data-gl]').forEach(add);
}

/** Remove all planes (before a page swap). Textures stay cached for back-navigation. */
export function unmountGL() {
  while (items.length) {
    const it = items.pop()!;
    it.off();
    it.io?.disconnect();
    it.mesh.setParent(null);
    it.program.remove?.();
  }
}

/** Fade every plane out, e.g. as part of a page-leave animation. */
export function hideGL(duration = 0.6) {
  return gsap.to(items.map((i) => i.program.uniforms.uReveal), { value: 0, duration, ease: 'expo.in' });
}

function render(t: number) {
  if (!renderer || document.hidden) return;
  time = t;
  const target = Math.max(-40, Math.min(40, scrollState().velocity));
  velocity += (target - velocity) * 0.12;
  let visible = 0;
  for (const it of items) {
    const r = it.el.getBoundingClientRect();
    const onScreen = r.bottom > -100 && r.top < vh + 100 && r.width > 0;
    it.mesh.visible = onScreen;
    if (!onScreen) continue;
    visible++;
    it.mesh.scale.set(r.width, r.height, 1);
    it.mesh.position.set(r.left + r.width / 2 - vw / 2, vh / 2 - (r.top + r.height / 2), 0);
    const u = it.program.uniforms;
    u.uPlane.value.set(r.width, r.height);
    u.uTime.value = time;
    u.uHover.value = it.hover.v;
    u.uVelocity.value = velocity * 0.05;
    // data-gl-scrub: reveal follows position: 0 when the top enters the viewport, 1 at 25% from the top.
    if (it.scrub) u.uReveal.value = Math.min(1, Math.max(0, (vh - r.top) / (vh * 0.75)));
  }
  mouse.x += (mouse.tx - mouse.x) * 0.08;
  mouse.y += (mouse.ty - mouse.y) * 0.08;
  if (bg) {
    const u = bg.program.uniforms;
    const s = scrollState();
    u.uTime.value = time; u.uResolution.value.set(vw, vh); u.uScroll.value = s.progress; u.uScrollY.value = s.y;
    u.uVelocity.value = velocity; u.uMouse.value.set(mouse.x, mouse.y);
    renderer.render({ scene: bg.scene, camera });
    renderer.render({ scene, camera, clear: false });
  } else if (visible || renderer.gl.canvas.dataset.dirty !== '0') {
    renderer.render({ scene, camera });
    renderer.gl.canvas.dataset.dirty = visible ? '1' : '0';
  }
}
```

### `src/engine/gl/shaders.ts`

```ts
// Shared vertex: bends the plane with scroll velocity, swells on hover.
export const vertex = /* glsl */ `
attribute vec3 position;
attribute vec2 uv;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
uniform float uVelocity;
uniform float uHover;
varying vec2 vUv;
void main() {
  vUv = uv;
  vec3 p = position;
  float bend = sin(uv.x * 3.14159265);
  p.y += bend * uVelocity * 0.06;
  p.z += bend * uHover * 0.05;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
}`;

const common = /* glsl */ `
precision highp float;
varying vec2 vUv;
uniform vec2 uPlane;
uniform float uTime;
uniform float uHover;
uniform float uVelocity;
uniform float uReveal;
uniform vec2 uMouse;
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
float fbm(vec2 p) {
  float v = 0.0, a = 0.5;
  for (int i = 0; i < 5; i++) { v += a * noise(p); p *= 2.02; a *= 0.5; }
  return v;
}
// Reveal mask: rises from the bottom with an organic edge. uReveal 0 → hidden, 1 → shown.
float revealMask(vec2 uv) {
  float edge = uReveal * 1.25 - 0.12 + (noise(uv * vec2(6.0, 2.0) + uTime * 0.2) - 0.5) * 0.12;
  return smoothstep(edge, edge - 0.08, uv.y);
}`;

// Image plane: object-fit: cover in-shader, hover zoom + chromatic split driven by velocity.
export const imageFragment = /* glsl */ `
${common}
uniform sampler2D tMap;
uniform vec2 uImage;
vec2 cover(vec2 uv) {
  vec2 r = vec2(min((uPlane.x / uPlane.y) / (uImage.x / uImage.y), 1.0), min((uPlane.y / uPlane.x) / (uImage.y / uImage.x), 1.0));
  return uv * r + (1.0 - r) * 0.5;
}
void main() {
  vec2 uv = vUv;
  vec2 c = uv - 0.5;
  uv = 0.5 + c * (1.0 - uHover * 0.06);
  vec2 dir = (uv - uMouse) * uHover;
  uv += dir * 0.04 * smoothstep(0.6, 0.0, length(vUv - uMouse));
  float shift = (abs(uVelocity) * 0.004 + uHover * 0.004);
  vec2 t = cover(uv);
  float r = texture2D(tMap, t + vec2(shift, 0.0)).r;
  float g = texture2D(tMap, t).g;
  float b = texture2D(tMap, t - vec2(shift, 0.0)).b;
  gl_FragColor = vec4(r, g, b, 1.0) * revealMask(vUv);
}`;

// Procedural plane: seeded flowing field in the palette. Honest generative cover art for
// projects that do not have imagery yet (never a fake screenshot).
export const proceduralFragment = /* glsl */ `
${common}
uniform vec3 uC1;
uniform vec3 uC2;
uniform vec3 uC3;
uniform float uSeed;
void main() {
  vec2 uv = vUv;
  vec2 p = uv * vec2(uPlane.x / uPlane.y, 1.0) * 1.6 + uSeed * 7.0;
  float t = uTime * 0.05;
  vec2 q = vec2(fbm(p + t), fbm(p + vec2(5.2, 1.3) - t));
  vec2 m = (uMouse - 0.5) * uHover * 0.8;
  float f = fbm(p + 2.5 * q + m + vec2(uVelocity * 0.02, 0.0));
  vec3 col = mix(uC1, uC2, smoothstep(0.2, 0.75, f));
  col = mix(col, uC3, smoothstep(0.55, 0.95, length(q) * f * 1.4));
  col += (hash(uv * uPlane + fract(uTime)) - 0.5) * 0.045; // film grain
  gl_FragColor = vec4(col, 1.0) * revealMask(vUv);
}`;
```
