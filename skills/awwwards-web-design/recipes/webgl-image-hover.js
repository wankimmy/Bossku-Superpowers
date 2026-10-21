/**
 * webgl-image-hover.js
 * Upgrades <img data-gl-hover> into DOM-synced WebGL planes that distort with the pointer's eased velocity.
 *
 * WHAT IT DOES
 *   One shared, fixed, full-viewport <canvas> (one WebGL context for every image) draws a plane exactly over
 *   each image's box. While the pointer moves over an image, the plane drags the picture along the pointer's
 *   eased velocity, plus a little value noise, inside a soft radius around the pointer. A still pointer produces
 *   no distortion, so nothing warps at rest. The <img> never leaves the DOM, the layout or the accessibility tree.
 *   It is set to opacity 0 only after its plane has drawn a frame at full alpha, and set back before the plane fades.
 *
 * USAGE
 *   <script type="importmap">{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.186.1/+esm" } }</script>
 *   <img data-gl-hover src="/a.avif" width="1200" height="800" alt="…">    data-gl-hover="0.6" sets a per-image strength
 *   <script type="module">
 *     import { initImageHover } from './webgl-image-hover.js';
 *     const hover = initImageHover();          // hover.ready -> Promise<boolean>; hover.refresh() after DOM changes
 *   </script>
 *   With boot.html-snippet.html, add the "three" line to its import map. No CSS is needed: the <img> keeps its own.
 *
 * RETURNS  { ready (getter: the latest boot's Promise<boolean>), refresh(), state(), dispose() }
 *
 * OPTIONS (all optional)
 *   selector    'img[data-gl-hover]'
 *   rest        'dom'   The real <img> shows whenever the effect is idle; GL takes over only while the picture moves.
 *                       Safe with native scrolling, which the compositor runs ahead of rAF. Default.
 *               'gl'    Planes stay on after their first frame and follow scroll in rAF. Use it with a main-thread
 *                       smooth scroller (Lenis) or when you add an effect that shows at rest.
 *   strength    1       Max drag = 5% of the image's short side x strength. 0 disables the drag.
 *   radius      0.55    Influence radius as a fraction of the image's short side.
 *   maxDpr      1.5     Clamp for the shared canvas: min(devicePixelRatio, maxDpr).
 *   zIndex      1       Canvas z-index in the root stacking context (see LIMITS).
 *   fade        0.18    Plane cross-fade in seconds.
 *   rootMargin  '300px' How far ahead of the viewport textures are decoded and uploaded.
 *   failIfMajorPerformanceCaveat  true   false also runs on software renderers (SwiftShader). Keep true in production.
 *   loadThree   () => import('three')   Swap it for a bundler import or another pinned CDN.
 *   onError     (err) => console.warn(…) Called once when the module falls back to plain <img> elements.
 *
 * FALLBACKS (each one leaves the plain <img> untouched and visible)
 *   - No JS: nothing runs.
 *   - prefers-reduced-motion: reduce, or <html data-motion="reduce"> (the in-page toggle of motion-core.js and the
 *     boot snippet). Both are followed live (media `change`, window `motionchange`): switching to reduce disposes
 *     everything and restores the images; switching back boots again.
 *   - No hover-capable fine pointer (touch devices). The effect needs hover, so three is never downloaded there.
 *   - Save-Data.
 *   - No WebGL2, or a context with a major performance caveat (software rendering).
 *   - The three import fails (CDN down, missing import map).
 *   - Any init error.
 *   - A cross-origin image without CORS: that one image stays DOM, the others still upgrade.
 *   - object-fit other than fill/cover/contain: that image stays DOM.
 *   - WebGL context loss: every image is restored at once, and the planes come back on restore.
 *
 * BUDGET
 *   - Boots after window load + idle (requestIdleCallback; setTimeout fallback for Safari). Never on the LCP path.
 *   - DPR <= 1.5. No MSAA: planes are axis-aligned, and the rounded-corner mask anti-aliases itself.
 *   - Renders on demand. It draws only while a plane animates or fades, or (rest 'gl') while scrolling with a plane
 *     on screen. The loop stops when settled, when the tab is hidden, and on context loss.
 *   - Textures are uploaded and the one shared shader program is compiled before the first hover, so there is no hitch.
 *   - dispose() restores every <img>, removes every listener, frees GPU memory and releases the context slot.
 *
 * LIMITS
 *   - The canvas is fixed above the page. Anything drawn over an image (a caption laid on it) needs position plus a
 *     z-index above `zIndex` in the root stacking context, or it is covered while that image's plane is showing.
 *   - Replicated: box position and size (including CSS transform scale), object-fit fill/cover/contain (centred),
 *     and border-radius (one radius for all corners). Planes are snapped to the canvas pixel grid. At DPR 1 a
 *     resting plane matches its <img> to a mean abs difference of 0.2-2.5 / 255 on thin-line test patterns. On a
 *     2x screen the canvas is capped at 1.5x, so a plane is slightly softer than the <img> (MAD 3-5): that is why
 *     rest 'dom' (the real <img> at rest) is the default.
 *   - Not replicated: ancestor overflow or clip-path, rotation, CSS filters, object-position other than centre.
 *   - Cross-origin images need crossorigin="anonymous" and CORS headers.
 *
 * WHY THREE.JS AND NOT OGL
 *   - OGL is lighter on its own: 39.7 KB brotli (ogl@1.0.11/+esm) against 190.3 KB for three@0.186.1/+esm
 *     (jsDelivr, measured 2026-09-25).
 *   - But OGL has been dormant since 2025-04, and no OGL signature turned up in the ~25 probed award winners, where
 *     three was the engine whenever one could be identified (webgl-3d-stack.md sections 1-2).
 *   - When three-hero.js (or any three scene) is on the page, this module adds zero library bytes: both resolve
 *     'three' through the same import map.
 *   - three's texture upload, mipmaps, program cache and context-restore handling come free. The shader passes the
 *     encoded sRGB bytes straight through (NoColorSpace, no output conversion), which is what keeps the plane
 *     visually identical to the <img>.
 *   - It loads after load + idle and only on hover devices.
 *   - If three is not otherwise on the page and bytes matter most, FRAG below ports to an OGL Program nearly
 *     unchanged (VERT needs its attribute declarations and a precision line).
 *
 * TESTED 2026-09-25 with three 0.186.1 (jsDelivr +esm build) in Playwright Chromium 145 (headless, ANGLE Metal GPU).
 *   The SwiftShader fallback, reduced motion (OS and in-page toggle, live), no-JS, CDN-blocked, touch, context loss
 *   and dispose paths were also tested. Not run in Safari or Firefox.
 */

const DEFAULTS = {
  selector: 'img[data-gl-hover]',
  rest: 'dom',
  strength: 1,
  radius: 0.55,
  maxDpr: 1.5,
  zIndex: 1,
  fade: 0.18,
  rootMargin: '300px',
  failIfMajorPerformanceCaveat: true,
  loadThree: () => import('three'),
  onError: (err) => console.warn('[webgl-image-hover] kept plain <img> elements:', err),
};

const VMAX = 1800; // pointer speed in CSS px/s that counts as a full-strength flick
const DRAG = 0.05; // max drag as a fraction of the image's short side, at strength 1
const FITS = new Set(['fill', 'cover', 'contain']);

const VERT = /* glsl */ `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`;

const FRAG = /* glsl */ `
uniform sampler2D uMap;
uniform vec2 uSize;      // plane size, CSS px
uniform vec2 uScale;     // object-fit mapping around the centre
uniform float uContain;  // 1 = transparent outside the picture (object-fit: contain)
uniform float uRadius;   // border-radius, CSS px
uniform vec2 uPointer;   // pointer in plane UV, y up
uniform vec2 uVel;       // eased pointer velocity, |v| <= 1
uniform float uHover;    // eased 0..1
uniform float uTime;
uniform float uDrag;     // max drag, CSS px
uniform float uReach;    // influence radius, CSS px
uniform float uAlpha;    // cross-fade with the <img>
varying vec2 vUv;

float hash(vec2 p) { p = fract(p * vec2(234.34, 435.345)); p += dot(p, p + 34.23); return fract(p.x * p.y); }
float vnoise(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);
}

void main() {
  vec2 p = vUv * uSize;                                        // work in CSS px so the falloff stays round
  float fall = 1.0 - smoothstep(0.0, uReach, distance(p, uPointer * uSize));
  fall *= fall;                                                // soft shoulder, no edge ring
  float speed = length(uVel);
  vec2 q = p / 140.0 + vec2(uTime * 0.35, -uTime * 0.25);
  vec2 n = vec2(vnoise(q), vnoise(q + 19.7)) * 2.0 - 1.0;
  // Uniform velocity term, so there is no singularity or tear at the pointer. It is zero when the pointer is still.
  vec2 disp = (uVel + n * 0.45 * speed) * fall * uHover * uDrag;
  vec2 st = ((p - disp) / uSize - 0.5) * uScale + 0.5;
  // The texture holds encoded sRGB (NoColorSpace) and goes out untouched: mip filtering and canvas blending then
  // happen in the same space the browser uses to scale and composite an <img>, so the plane matches it.
  // LOD bias -0.5: plain trilinear is visibly softer than the browser's own downscale (measured).
  // Sampled before any branch, so the implicit derivatives stay defined.
  vec4 c = texture2D(uMap, clamp(st, 0.0, 1.0), -0.5);
  float inside = uContain > 0.5 && (any(lessThan(st, vec2(0.0))) || any(greaterThan(st, vec2(1.0)))) ? 0.0 : 1.0;
  vec2 h = uSize * 0.5;                                        // rounded-rect mask, 1 CSS px anti-aliased edge
  vec2 d = abs(p - h) - (h - uRadius);
  float sd = length(max(d, 0.0)) + min(max(d.x, d.y), 0.0) - uRadius;
  float mask = clamp(0.5 - sd, 0.0, 1.0);
  gl_FragColor = vec4(c.rgb, c.a * mask * inside * uAlpha);
}`;

export function initImageHover(options = {}) {
  const o = { ...DEFAULTS, ...options };
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  let engine = null;
  let pending = null;
  let stopped = false;
  let ready = Promise.resolve(false); // replaced by each boot attempt; the getter below always returns the latest
  const fail = (err) => { try { o.onError?.(err); } catch { /* never let reporting break the page */ } };

  const eligible = () =>
    !stopped && !reduce.matches && fine.matches &&
    document.documentElement.dataset.motion !== 'reduce' && // in-page toggle (motion-core.js, boot snippet)
    navigator.connection?.saveData !== true &&
    !!document.querySelector(o.selector);

  function boot() {
    if (engine || pending) return;
    if (!eligible()) { ready = Promise.resolve(false); return; }
    ready = pending = (async () => {
      try {
        await afterLoadIdle();
        if (!eligible() || !canRunWebGL2(o.failIfMajorPerformanceCaveat)) return false;
        const THREE = await o.loadThree();
        if (!eligible()) return false;
        engine = createEngine(THREE, o);
        return true;
      } catch (err) {
        engine?.dispose();
        engine = null;
        fail(err);
        return false;
      } finally {
        pending = null;
      }
    })();
  }

  const onPreference = () => {
    if (eligible()) { boot(); return; }
    engine?.dispose();
    engine = null;
    if (!pending) ready = Promise.resolve(false); // a boot in flight re-checks eligible() and resolves false
  };
  reduce.addEventListener('change', onPreference);
  fine.addEventListener('change', onPreference);
  addEventListener('motionchange', onPreference);
  boot();

  return {
    get ready() { return ready; }, // Promise<boolean>: true once planes can run, false = plain <img> fallback
    refresh() { if (engine) engine.refresh(); else boot(); },
    state() { return engine ? engine.state() : { live: false, running: false, renders: 0, planes: 0 }; },
    dispose() {
      stopped = true;
      reduce.removeEventListener('change', onPreference);
      fine.removeEventListener('change', onPreference);
      removeEventListener('motionchange', onPreference);
      engine?.dispose();
      engine = null;
      if (!pending) ready = Promise.resolve(false); // a boot in flight re-checks eligible() and resolves false
    },
  };
}

function createEngine(THREE, o) {
  const canvas = document.createElement('canvas');
  canvas.setAttribute('aria-hidden', 'true');
  canvas.setAttribute('data-gl-hover-canvas', '');
  canvas.style.cssText =
    `position:fixed;inset:0;width:100%;height:100%;display:block;pointer-events:none;z-index:${o.zIndex}`;
  const printCss = document.createElement('style');
  printCss.textContent =
    '@media print{[data-gl-hover-canvas]{display:none!important}[data-gl-hover-hidden]{opacity:1!important}}';

  const renderer = new THREE.WebGLRenderer({
    canvas, alpha: true, antialias: false, powerPreference: 'high-performance',
    failIfMajorPerformanceCaveat: o.failIfMajorPerformanceCaveat,
  });
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(0, 1, 0, -1, -10, 10);
  const geometry = new THREE.PlaneGeometry(1, 1);
  const items = new Map();
  const listeners = [];
  const listen = (target, type, fn, opts) => {
    target.addEventListener(type, fn, opts);
    listeners.push(() => target.removeEventListener(type, fn, opts));
  };

  let vw = 1, vh = 1, dpr = 1, px = 0, py = 0, hasPointer = false, hovered = 0;
  let running = false, last = 0, drawn = false, dead = false, lost = false, renders = 0;
  let compiled = null;
  const fadeTime = o.rest === 'gl' ? Math.max(o.fade, 0.35) : o.fade;
  const snap = (v) => Math.round(v * dpr) / dpr; // CSS px -> nearest canvas pixel edge

  function resize() {
    vw = Math.max(1, canvas.clientWidth);
    vh = Math.max(1, canvas.clientHeight);
    dpr = Math.min(window.devicePixelRatio || 1, o.maxDpr);
    renderer.setPixelRatio(dpr);
    renderer.setSize(vw, vh, false);
    camera.right = vw;
    camera.bottom = -vh;
    camera.updateProjectionMatrix();
  }

  function readStyles(it) {
    const cs = getComputedStyle(it.img);
    it.fit = cs.objectFit || 'fill';
    it.radiusCss = cs.borderTopLeftRadius || '0px';
    it.showDelay = opacityTransitionSeconds(cs);
  }

  function hideImg(it) {
    if (it.hidden) return;
    it.hidden = true;
    it.img.style.opacity = '0';
    it.img.setAttribute('data-gl-hover-hidden', '');
  }
  function showImg(it) {
    if (!it.hidden) return;
    it.hidden = false;
    it.img.style.opacity = it.prevOpacity;
    it.img.removeAttribute('data-gl-hover-hidden');
  }

  function requestRender() {
    if (running || dead || lost || document.hidden) return;
    running = true;
    last = performance.now();
    renderer.setAnimationLoop(frame);
  }
  function stop() {
    running = false;
    renderer.setAnimationLoop(null);
  }

  function frame(now) {
    const t = now ?? performance.now();
    const dt = Math.min(Math.max((t - last) / 1000, 1 / 240), 1 / 30);
    last = t;
    const kv = 1 - Math.exp(-dt * 6); // velocity easing, ~170 ms time constant
    const kh = 1 - Math.exp(-dt * 8); // hover easing
    let busy = false;
    let anyVisible = false;
    const toHide = [];

    for (const it of items.values()) {
      if (it.state !== 'ready') continue;
      const needs = it.hovered || it.alpha > 0 || it.vx !== 0 || it.vy !== 0 || (o.rest === 'gl' && it.near);
      if (!needs) { // nothing of this plane is on screen: settle its state instead of animating it
        it.mesh.visible = false;
        it.hover = it.vx = it.vy = 0;
        it.on = false;
        continue;
      }
      const r = it.img.getBoundingClientRect();
      const w = r.width, h = r.height;
      const onScreen = w > 0 && h > 0 && r.bottom > 0 && r.top < vh && r.right > 0 && r.left < vw;
      const u = it.mat.uniforms;

      // Pointer position and eased velocity, in CSS px with y up. `over` re-checks the rect every frame, so an
      // image that scrolls out from under a still pointer lets go even before the browser sends pointerleave.
      const over = it.hovered && hasPointer && w > 0 && h > 0 &&
        px >= r.left && px <= r.right && py >= r.top && py <= r.bottom;
      // Velocity uses the real time between samples (not the clamped dt), so a loop that stopped and restarted
      // between two pointer events still measures the true speed. Samples older than 200 ms are discarded.
      let rvx = 0, rvy = 0;
      if (over) {
        const lx = px - r.left, ly = py - r.top;
        if (it.lx !== null && t - it.lt < 200) {
          const vdt = Math.max((t - it.lt) / 1000, 1 / 240);
          rvx = (lx - it.lx) / vdt;
          rvy = -(ly - it.ly) / vdt;
        }
        it.lx = lx; it.ly = ly; it.lt = t;
        u.uPointer.value.set(lx / w, 1 - ly / h);
      } else {
        it.lx = it.ly = null;
      }
      it.vx += (rvx / VMAX - it.vx) * kv;
      it.vy += (rvy / VMAX - it.vy) * kv;
      let sp = Math.hypot(it.vx, it.vy);
      if (sp > 1) { it.vx /= sp; it.vy /= sp; sp = 1; }
      if (sp < 1e-3 && rvx === 0 && rvy === 0) { it.vx = it.vy = 0; sp = 0; }
      const ht = over ? 1 : 0;
      it.hover += (ht - it.hover) * kh;
      if (Math.abs(ht - it.hover) < 1e-3) it.hover = ht;

      const amount = it.hover * sp; // how much distortion is on screen right now
      if (amount > 0.004) it.on = true;
      else if (amount < 0.0008) it.on = false; // hysteresis: no flapping near zero
      if (amount > 0) it.time += dt;
      const target = o.rest === 'gl' ? 1 : it.on ? 1 : 0;

      // Cross-fade. The canvas sits above the <img>, so the plane fades in over a visible image and the image is
      // hidden only after that; on the way out the image comes back first, then the plane fades.
      let fading = false;
      if (target === 1) {
        if (onScreen && it.alpha < 1) { it.alpha = Math.min(1, it.alpha + dt / fadeTime); fading = true; }
      } else if (it.alpha > 0) {
        if (it.hidden) { showImg(it); it.holdUntil = t + it.showDelay * 1000; }
        if (t >= it.holdUntil) it.alpha = Math.max(0, it.alpha - dt / fadeTime);
        fading = true;
      }

      // The browser paints an <img> snapped to whole device pixels; a plane left at fractional CSS px is resampled
      // half a pixel off and reads soft. Snap its edges to the canvas pixel grid (measured MAD vs the <img>:
      // 3.2-8.0 unsnapped, 0.2-2.5 snapped, on thin-line test patterns).
      const sl = snap(r.left), st = snap(r.top);
      const sw = Math.max(snap(r.right) - sl, 1), sh = Math.max(snap(r.bottom) - st, 1);
      const short = Math.min(w, h);
      u.uSize.value.set(sw, sh);
      setFit(u, it.fit, sw, sh, it.img.naturalWidth, it.img.naturalHeight);
      u.uRadius.value = Math.min(parseRadius(it.radiusCss, short), short / 2);
      u.uVel.value.set(it.vx, it.vy);
      u.uHover.value = it.hover;
      u.uTime.value = it.time;
      u.uDrag.value = DRAG * short * o.strength * it.strength;
      u.uReach.value = Math.max(o.radius * short, 1);
      u.uAlpha.value = it.alpha;
      it.mesh.visible = it.alpha > 0 && onScreen;
      it.mesh.position.set(sl + sw / 2, -(st + sh / 2), 0);
      it.mesh.scale.set(sw, sh, 1);
      anyVisible ||= it.mesh.visible;
      if (it.mesh.visible && it.alpha >= 1 && target === 1 && !it.hidden) toHide.push(it);

      busy ||= fading || it.hover !== ht || sp !== 0 || rvx !== 0 || rvy !== 0;
    }

    if (anyVisible || drawn) { renderer.render(scene, camera); renders++; } // one extra frame clears the last plane
    drawn = anyVisible;
    for (const it of toHide) hideImg(it); // same frame as the plane's first full-alpha draw
    if (!busy) stop();
  }

  function makeItem(img) {
    const attr = parseFloat(img.getAttribute('data-gl-hover'));
    const it = {
      img, state: 'idle', near: false, hovered: false, hidden: false, on: false, prevOpacity: img.style.opacity,
      strength: Number.isFinite(attr) ? attr : 1, hover: 0, vx: 0, vy: 0, lx: null, ly: null, lt: 0, alpha: 0, time: 0,
      holdUntil: 0, showDelay: 0, fit: 'fill', radiusCss: '0px', tex: null, mat: null, mesh: null,
    };
    it.onEnter = (e) => {
      if (e.pointerType === 'touch' || it.hovered) return;
      it.hovered = true; hovered++;
      px = e.clientX; py = e.clientY; hasPointer = true;
      requestRender();
    };
    it.onLeave = () => {
      if (!it.hovered) return;
      it.hovered = false; hovered--;
      requestRender();
    };
    it.onLoad = () => { if (it.tex) it.tex.needsUpdate = true; requestRender(); }; // srcset swapped currentSrc
    img.addEventListener('pointerenter', it.onEnter);
    img.addEventListener('pointerleave', it.onLeave);
    img.addEventListener('load', it.onLoad);
    io.observe(img);
    ro.observe(img);
    return it;
  }

  async function prepare(it) {
    it.state = 'loading';
    const img = it.img;
    try {
      if (!img.complete) {
        await new Promise((resolve, reject) => {
          img.addEventListener('load', resolve, { once: true });
          img.addEventListener('error', reject, { once: true });
        });
      }
      await img.decode?.().catch(() => {});
      if (dead || !img.isConnected || !img.naturalWidth) throw new Error('image not renderable');
      readStyles(it);
      if (!FITS.has(it.fit)) throw new Error(`object-fit: ${it.fit} is not replicated`);
      assertCorsClean(img);
      it.tex = new THREE.Texture(img);
      // Deliberately NOT SRGBColorSpace: decoding to linear before mip filtering brightens thin dark detail by
      // 2-4 levels compared with the browser's own <img> scaling (measured). Keep the bytes encoded, output as-is.
      it.tex.colorSpace = THREE.NoColorSpace;
      it.tex.needsUpdate = true;
      it.mat = new THREE.ShaderMaterial({
        vertexShader: VERT, fragmentShader: FRAG,
        transparent: true, depthTest: false, depthWrite: false, toneMapped: false, // photos are display-referred
        uniforms: {
          uMap: { value: it.tex }, uSize: { value: new THREE.Vector2(1, 1) }, uScale: { value: new THREE.Vector2(1, 1) },
          uContain: { value: 0 }, uRadius: { value: 0 }, uPointer: { value: new THREE.Vector2(0.5, 0.5) },
          uVel: { value: new THREE.Vector2() }, uHover: { value: 0 }, uTime: { value: 0 }, uDrag: { value: 0 },
          uReach: { value: 1 }, uAlpha: { value: 0 },
        },
      });
      it.mesh = new THREE.Mesh(geometry, it.mat);
      it.mesh.visible = false;
      it.mesh.frustumCulled = false;
      scene.add(it.mesh);
      renderer.initTexture(it.tex); // upload now, not on first hover
      compiled ||= renderer.compileAsync(it.mesh, camera, scene); // one program, shared by every plane
      await compiled;
      if (dead || it.state !== 'loading') return;
      it.state = 'ready';
      requestRender();
    } catch {
      if (it.state === 'loading') it.state = 'failed'; // this image simply stays a plain <img>
      if (it.mesh) scene.remove(it.mesh);
      it.mat?.dispose();
      it.tex?.dispose();
      it.mesh = it.mat = it.tex = null;
    }
  }

  function dropItem(it) {
    it.img.removeEventListener('pointerenter', it.onEnter);
    it.img.removeEventListener('pointerleave', it.onLeave);
    it.img.removeEventListener('load', it.onLoad);
    io.unobserve(it.img);
    ro.unobserve(it.img);
    if (it.hovered) hovered--;
    showImg(it);
    if (it.mesh) scene.remove(it.mesh);
    it.mat?.dispose();
    it.tex?.dispose();
    it.state = 'dropped';
    items.delete(it.img);
  }

  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      const it = items.get(e.target);
      if (!it) continue;
      it.near = e.isIntersecting;
      if (it.near && it.state === 'idle') prepare(it);
    }
    if (o.rest === 'gl') requestRender();
  }, { rootMargin: o.rootMargin });

  // Layout that moves without a scroll or resize (late content above an image) re-syncs through this.
  const ro = new ResizeObserver(() => {
    for (const it of items.values()) if (it.state === 'ready') readStyles(it);
    if (o.rest === 'gl' || drawn || hovered > 0) requestRender();
  });

  const onPointerMove = (e) => {
    if (e.pointerType === 'touch') return;
    px = e.clientX; py = e.clientY; hasPointer = true;
    if (hovered > 0) requestRender();
  };
  const onScroll = () => { if (o.rest === 'gl' || drawn || hovered > 0) requestRender(); };
  const onResize = () => { resize(); requestRender(); };
  const onVisibility = () => (document.hidden ? stop() : requestRender());
  const onLost = () => {
    lost = true;
    stop();
    drawn = false;
    for (const it of items.values()) { showImg(it); it.alpha = 0; it.on = false; }
  };
  const onRestored = () => {
    lost = false;
    compiled = null;
    for (const it of items.values()) if (it.tex) it.tex.needsUpdate = true;
    requestRender();
  };

  try {
    document.body.appendChild(canvas);
    document.head.appendChild(printCss);
    resize();
    ro.observe(document.documentElement);
    listen(window, 'pointermove', onPointerMove, { passive: true });
    listen(window, 'scroll', onScroll, { passive: true, capture: true });
    listen(window, 'resize', onResize);
    listen(document, 'visibilitychange', onVisibility);
    listen(canvas, 'webglcontextlost', onLost);
    listen(canvas, 'webglcontextrestored', onRestored);
    refresh();
  } catch (err) {
    dispose();
    throw err;
  }

  function refresh() {
    if (dead) return;
    for (const [img, it] of items) if (!img.isConnected) dropItem(it);
    for (const img of document.querySelectorAll(o.selector)) if (!items.has(img)) items.set(img, makeItem(img));
    for (const it of items.values()) if (it.state === 'ready') readStyles(it);
    onResize();
  }

  function dispose() {
    if (dead) return;
    dead = true;
    stop();
    io.disconnect();
    ro.disconnect();
    for (const off of listeners) off();
    for (const it of [...items.values()]) dropItem(it);
    geometry.dispose();
    renderer.dispose();
    renderer.forceContextLoss(); // give the context slot back (browsers cap live contexts at ~16)
    canvas.remove();
    printCss.remove();
  }

  return {
    refresh,
    dispose,
    state: () => ({
      live: !dead && !lost, running, renders,
      planes: [...items.values()].filter((it) => it.state === 'ready').length,
      dpr: renderer.getPixelRatio(),
    }),
  };
}

/* ---------- helpers ---------- */

function setFit(u, fit, w, h, iw, ih) {
  const pa = w / Math.max(h, 1), ia = iw / Math.max(ih, 1);
  if (fit === 'cover') u.uScale.value.set(pa > ia ? 1 : pa / ia, pa > ia ? ia / pa : 1);
  else if (fit === 'contain') u.uScale.value.set(pa > ia ? pa / ia : 1, pa > ia ? 1 : ia / pa);
  else u.uScale.value.set(1, 1); // fill
  u.uContain.value = fit === 'contain' ? 1 : 0;
}

function parseRadius(css, short) {
  const first = String(css).trim().split(/\s+/)[0] || '0';
  const v = parseFloat(first) || 0;
  return first.endsWith('%') ? (v / 100) * short : v;
}

// Longest opacity transition authored on the <img>, so the plane waits for the image to be fully back before fading.
function opacityTransitionSeconds(cs) {
  const props = cs.transitionProperty.split(',').map((s) => s.trim());
  const durs = cs.transitionDuration.split(',').map(parseFloat);
  const dels = cs.transitionDelay.split(',').map(parseFloat);
  let t = 0;
  props.forEach((p, i) => {
    if (p === 'opacity' || p === 'all') t = Math.max(t, (durs[i % durs.length] || 0) + (dels[i % dels.length] || 0));
  });
  return t;
}

// three logs (but does not throw) when WebGL rejects a tainted image, so check first.
function assertCorsClean(img) {
  const c = document.createElement('canvas');
  c.width = c.height = 1;
  const ctx = c.getContext('2d');
  ctx.drawImage(img, 0, 0, 1, 1);
  ctx.getImageData(0, 0, 1, 1); // throws SecurityError for a cross-origin image without CORS
}

function canRunWebGL2(failIfMajorPerformanceCaveat) {
  try {
    const gl = document.createElement('canvas').getContext('webgl2', { failIfMajorPerformanceCaveat });
    gl?.getExtension('WEBGL_lose_context')?.loseContext(); // don't hold one of the ~16 context slots
    return !!gl;
  } catch {
    return false;
  }
}

function afterLoadIdle() {
  return new Promise((resolve) => {
    const idle = () => ('requestIdleCallback' in window
      ? requestIdleCallback(() => resolve(), { timeout: 2000 })
      : setTimeout(resolve, 200));
    if (document.readyState === 'complete') idle();
    else addEventListener('load', idle, { once: true });
  });
}
