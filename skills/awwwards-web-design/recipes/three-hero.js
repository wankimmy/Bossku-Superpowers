/**
 * three-hero.js
 * Mounts one hero 3D object over a poster, with image-based lighting, subtle pointer parallax and an optional
 * scroll-scrubbed camera move. The poster is the content; the canvas is decoration laid over it.
 *
 * WHAT IT DOES
 *   - After LCP it creates a <canvas aria-hidden> inside the container, stacked right after the poster, at opacity 0.
 *   - It builds a procedural subject: a turned ceramic vessel from a lathe profile, so no model file is fetched.
 *     Pass `geometry` for your own object.
 *   - Material: MeshPhysicalMaterial with clearcoat, plus a generated roughness map for micro-variation.
 *   - Lighting: RoomEnvironment through PMREM, plus one directional key light. Neutral tone mapping by default.
 *   - Ground contact: a two-layer procedural contact shadow.
 *   - It compiles shaders (compileAsync), renders the first frame, then fades the canvas in over the poster.
 *   - The poster stays in the DOM and is never hidden, so it shows through again whenever the canvas goes.
 *
 * USAGE
 *   <script type="importmap">{ "imports": {
 *     "three": "https://cdn.jsdelivr.net/npm/three@0.186.1/+esm",
 *     "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.186.1/examples/jsm/",
 *     "gsap": "https://cdn.jsdelivr.net/npm/gsap@3.15.0/+esm",                          (only for `scroll`)
 *     "gsap/ScrollTrigger": "https://cdn.jsdelivr.net/npm/gsap@3.15.0/ScrollTrigger.js/+esm"
 *   } }</script>
 *   The gsap lines are the same as boot.html-snippet.html's, so motion-core.js and this module share one GSAP and one
 *   ScrollTrigger (and its Lenis sync). With that snippet, add only the two "three" lines.
 *   <div class="hero3d">                          position: relative; with a real height (e.g. 100svh)
 *     <img data-hero-poster src="/hero-poster.webp" width="1600" height="1000" alt="…" fetchpriority="high">
 *     <h1 class="hero3d__copy">…</h1>             copy needs position: relative to paint above the canvas
 *   </div>
 *   .hero3d > [data-hero-poster] { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
 *   import { mountHero } from './three-hero.js';
 *   const hero = mountHero(document.querySelector('.hero3d'), { scroll: true });   // hero.ready -> Promise<boolean>
 *
 *   The best poster is a frame of this scene: open the page once, then copy hero.snapshot('image/webp', 0.9).
 *   It is rendered with the same camera, so the cross-fade does not jump.
 *
 * OPTIONS (all optional)
 *   poster       '[data-hero-poster]'   Selector or element: the canvas is stacked right after it (or its <picture>).
 *   color        '#262626'   Glaze colour. The default is neutral: choose one from the brand.
 *   material     {}          Extra MeshPhysicalMaterial params (e.g. { sheen: 1 } for fabric, { metalness: 1 }).
 *   geometry     null        (THREE) => BufferGeometry. It is centred on x/z and set on the ground (y = 0).
 *   toneMapping  'neutral'   'neutral' keeps brand/product colours; 'aces' is moodier; 'agx' suits hot highlights.
 *   exposure     1
 *   envIntensity 1           RoomEnvironment strength.
 *   keyIntensity 1.4         The single directional key light. There is no rim or colour rig.
 *   fov          24          Vertical FOV. A long lens (18-35) keeps products undistorted.
 *   view         { azimuth: -28, polar: 72, fill: 0.7 }   Degrees, and the fraction of the frame the object fills.
 *   parallax     3           Max camera orbit in degrees at the viewport edges. 0 turns it off.
 *   scroll       false       true or { trigger, start: 'top top', end: 'bottom top', azimuth: 40, polar: -16,
 *                            dolly: 0.2 }. A scrubbed camera move (delta degrees; dolly = fraction closer).
 *                            trigger defaults to the container. For a position: sticky stage, pass its scrolling
 *                            track instead, with end 'bottom bottom' (sticky boxes measure wrong when scrolled).
 *   maxDpr       2           Clamp; coarse pointers are capped at 1.5.
 *   background   'auto'      Opaque clear colour = the first opaque ancestor background, so the canvas edge
 *                            disappears into the page. Pass any CSS colour, or 'transparent' when the fallback is a
 *                            CSS background rather than a poster image (a poster would show through).
 *   shadow       true        Procedural contact shadow (dark core + soft penumbra pushed away from the key light).
 *   fadeMs       600         Canvas fade-in over the poster (200 under reduced motion).
 *   failIfMajorPerformanceCaveat  true   false also runs on software renderers. Keep true in production.
 *   loadThree / loadRoomEnvironment / loadGsap / loadScrollTrigger   () => import(...). Override for bundlers.
 *   onError      (err) => console.warn(…)
 *
 * RETURNS  { ready: Promise<boolean>, state(), snapshot(type?, quality?) -> dataURL | null, dispose() }
 *
 * FALLBACKS
 *   - No JS, no WebGL2, a software renderer (caveat), Save-Data, or the CDN import failing: the poster stays and
 *     nothing else changes.
 *   - Context loss: the canvas fades out, so the poster shows. On restore the clear colour is re-applied (three
 *     resets it to black), the PMREM environment is rebuilt, and the canvas returns.
 *   - Reduced motion, from the OS or from <html data-motion="reduce"> (the in-page toggle of motion-core.js and the
 *     boot snippet): one static render (rest pose, no parallax, no scroll move), and GSAP is not loaded at boot. A 200 ms
 *     opacity fade is the only change. Both are followed live (media `change`, window `motionchange`), both ways.
 *   - GSAP failing to load only disables the scroll move.
 *
 * BUDGET (webgl-3d-stack.md section 6)
 *   - Init after load + the first LCP entry + idle.
 *   - DPR min(dpr, 2), or 1.5 on coarse pointers.
 *   - About 31k triangles, 3 draw calls, two 128 x 128 textures (64 KB each before mips).
 *   - Frameloop on demand: it renders only while the parallax or scroll damping is settling, and stops when settled.
 *     There is no idle auto-rotate.
 *   - It pauses offscreen (IntersectionObserver) and when the tab is hidden.
 *   - dispose() frees geometry, materials, textures and the PMREM target, and releases the context.
 *
 * TESTED 2026-09-25 with three 0.186.1 (jsDelivr +esm) and gsap 3.15.0 (+esm, ScrollTrigger) in Playwright
 *   Chromium 145 (headless, ANGLE Metal GPU).
 *   The SwiftShader fallback, reduced motion (OS and in-page toggle, live), no-JS, CDN-blocked, touch, context
 *   loss/restore and dispose paths were also tested. Not run in Safari or Firefox.
 */

const DEFAULTS = {
  poster: '[data-hero-poster]',
  color: '#262626',
  material: {},
  geometry: null,
  toneMapping: 'neutral',
  exposure: 1,
  envIntensity: 1,
  keyIntensity: 1.4,
  fov: 24,
  view: { azimuth: -28, polar: 72, fill: 0.7 },
  parallax: 3,
  scroll: false,
  maxDpr: 2,
  background: 'auto',
  shadow: true,
  fadeMs: 600,
  failIfMajorPerformanceCaveat: true,
  loadThree: () => import('three'),
  loadRoomEnvironment: () => import('three/addons/environments/RoomEnvironment.js'),
  loadGsap: () => import('gsap'),
  loadScrollTrigger: () => import('gsap/ScrollTrigger'),
  onError: (err) => console.warn('[three-hero] kept the poster:', err),
};

const SCROLL_DEFAULTS = { start: 'top top', end: 'bottom top', azimuth: 40, polar: -16, dolly: 0.2 };

export function mountHero(container, options = {}) {
  const o = { ...DEFAULTS, ...options, view: { ...DEFAULTS.view, ...options.view } };
  let app = null;
  let dead = false;

  const ready = (async () => {
    try {
      if (!container || navigator.connection?.saveData === true) return false;
      await afterLCP();
      if (dead || !canRunWebGL2(o.failIfMajorPerformanceCaveat)) return false;
      const [THREE, room] = await Promise.all([o.loadThree(), o.loadRoomEnvironment()]);
      if (dead) return false;
      app = await createApp(THREE, room.RoomEnvironment, container, o, () => dead);
      if (dead) { app.dispose(); app = null; return false; }
      return true;
    } catch (err) {
      app?.dispose();
      app = null;
      try { o.onError?.(err); } catch { /* reporting must not break the page */ }
      return false;
    }
  })();

  return {
    ready,
    state: () => (app ? app.state() : { live: false, running: false, renders: 0 }),
    snapshot: (type = 'image/webp', quality = 0.9) => (app ? app.snapshot(type, quality) : null),
    dispose() {
      dead = true;
      app?.dispose();
      app = null;
    },
  };
}

async function createApp(THREE, RoomEnvironment, container, o, isCancelled) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  // Motion is allowed only when the OS allows it AND the in-page toggle (<html data-motion>) is not on reduce.
  const motionOK = () => !reduce.matches && document.documentElement.dataset.motion !== 'reduce';
  const cleanups = [];
  const listen = (target, type, fn, opts) => {
    target.addEventListener(type, fn, opts);
    cleanups.push(() => target.removeEventListener(type, fn, opts));
  };

  const canvas = document.createElement('canvas');
  canvas.setAttribute('aria-hidden', 'true');
  canvas.setAttribute('data-hero-canvas', '');
  const fade = () => (motionOK() ? o.fadeMs : 200);
  canvas.style.cssText =
    'position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none;opacity:0;' +
    `transition:opacity ${fade()}ms cubic-bezier(.33,1,.68,1)`;

  let renderer = null, envRT = null, grain = null, shadowTex = null, io = null, ro = null, mm = null;
  let running = false, inView = true, lost = false, dead = false, shown = false, renders = 0, last = 0;
  const scene = new THREE.Scene();

  function dispose() {
    if (dead) return;
    dead = true;
    stop();
    mm?.revert();
    io?.disconnect();
    ro?.disconnect();
    for (const off of cleanups) off();
    scene.traverse((obj) => {
      obj.geometry?.dispose();
      for (const m of [].concat(obj.material || [])) m.dispose();
    });
    grain?.dispose();
    shadowTex?.dispose();
    envRT?.dispose();
    if (renderer) {
      renderer.dispose();
      renderer.forceContextLoss(); // release the context slot
    }
    canvas.remove();
  }

  try {
    if (getComputedStyle(container).position === 'static') container.style.position = 'relative';
    // Stack the canvas right after the container's child that holds the poster (which may be inside a <picture>).
    let anchor = typeof o.poster === 'string' ? container.querySelector(o.poster) : o.poster;
    while (anchor && anchor.parentNode !== container) anchor = anchor.parentNode;
    if (anchor) anchor.after(canvas);
    else container.prepend(canvas);

    const bg = o.background === 'transparent' ? null : resolveBackground(container, o.background);
    renderer = new THREE.WebGLRenderer({
      canvas, antialias: true, alpha: !bg, powerPreference: 'high-performance',
      failIfMajorPerformanceCaveat: o.failIfMajorPerformanceCaveat,
    });
    const dprCap = matchMedia('(pointer: coarse)').matches ? Math.min(o.maxDpr, 1.5) : o.maxDpr;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, dprCap));
    renderer.toneMapping = {
      neutral: THREE.NeutralToneMapping, aces: THREE.ACESFilmicToneMapping, agx: THREE.AgXToneMapping,
    }[o.toneMapping] ?? THREE.NeutralToneMapping;
    renderer.toneMappingExposure = o.exposure;
    // three rebuilds its background state on a context restore (clear colour back to black), so this runs again then.
    const applyClear = () => {
      if (bg) renderer.setClearColor(new THREE.Color().setRGB(bg[0] / 255, bg[1] / 255, bg[2] / 255, THREE.SRGBColorSpace), 1);
      else renderer.setClearColor(0x000000, 0);
    };
    applyClear();

    // Image-based light: a neutral studio room, prefiltered once. It is rebuilt after a context restore.
    const makeEnv = () => {
      const gen = new THREE.PMREMGenerator(renderer);
      const room = new RoomEnvironment();
      const rt = gen.fromScene(room, 0.04);
      room.dispose();
      gen.dispose();
      return rt;
    };
    envRT = makeEnv();
    scene.environment = envRT.texture;
    scene.environmentIntensity = o.envIntensity;

    // Subject: centred on x/z, standing on y = 0.
    const geometry = o.geometry ? o.geometry(THREE) : vesselGeometry(THREE);
    geometry.computeBoundingBox();
    const box = geometry.boundingBox;
    const center = box.getCenter(new THREE.Vector3());
    geometry.translate(-center.x, -box.min.y, -center.z);
    geometry.computeBoundingBox();
    geometry.computeBoundingSphere();
    const size = geometry.boundingBox.getSize(new THREE.Vector3());
    grain = roughnessNoise(THREE);
    const material = new THREE.MeshPhysicalMaterial({
      color: o.color, roughness: 0.42, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.05,
      roughnessMap: grain, ...o.material,
    });
    scene.add(new THREE.Mesh(geometry, material));

    const key = new THREE.DirectionalLight(0xffffff, o.keyIntensity);
    key.position.set(2.6, 4.2, 3.2);
    scene.add(key);

    if (o.shadow) {
      shadowTex = shadowTexture(THREE);
      const foot = Math.max(size.x, size.z);
      const away = new THREE.Vector2(-key.position.x, -key.position.z).normalize().multiplyScalar(0.1 * foot);
      const addShadow = (diameter, opacity, dx, dz, y, order) => {
        const m = new THREE.Mesh(
          new THREE.PlaneGeometry(1, 1),
          new THREE.MeshBasicMaterial({
            map: shadowTex, color: 0x000000, transparent: true, opacity,
            depthWrite: false, toneMapped: false, dithering: true,
          }),
        );
        m.rotation.x = -Math.PI / 2;
        m.scale.set(diameter, diameter, 1);
        m.position.set(dx, y, dz);
        m.renderOrder = order;
        scene.add(m);
      };
      addShadow(foot * 1.9, 0.22, away.x, away.y, 0.001, 1); // soft penumbra, cast away from the key
      addShadow(foot * 0.78, 0.5, 0, 0, 0.002, 2);           // tight contact core
    }

    // Camera rig: spherical coordinates around the object's optical centre.
    const camera = new THREE.PerspectiveCamera(o.fov, 1, 0.05, 100);
    const target = new THREE.Vector3(0, size.y * 0.46, 0);
    const R = geometry.boundingSphere.radius;
    const rad = THREE.MathUtils.degToRad;
    const baseAz = rad(o.view.azimuth), basePo = rad(o.view.polar), par = rad(o.parallax);
    const sc = o.scroll ? { ...SCROLL_DEFAULTS, ...(typeof o.scroll === 'object' ? o.scroll : {}) } : null;
    const dAz = sc ? rad(sc.azimuth) : 0, dPo = sc ? rad(sc.polar) : 0, dolly = sc ? sc.dolly : 0;
    const pT = { x: 0, y: 0 }, pC = { x: 0, y: 0 };
    let sT = 0, sC = 0, dist = 3, sizeW = -1, sizeH = -1;

    function resize() {
      sizeW = canvas.clientWidth;
      sizeH = canvas.clientHeight;
      const w = Math.max(1, sizeW), h = Math.max(1, sizeH);
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      const vf = rad(camera.fov);
      const hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect);
      const f = Math.min(vf, hf); // fit to the narrower side, so portrait screens don't crop the object
      dist = R / Math.sin(Math.atan(Math.tan(f / 2) * o.view.fill));
      camera.near = dist / 50;
      camera.far = dist * 10;
      camera.updateProjectionMatrix();
    }

    function place() {
      const s = sC * sC * (3 - 2 * sC); // ease the scrubbed move
      const az = baseAz + dAz * s + pC.x * par;
      const po = Math.min(Math.max(basePo + dPo * s + pC.y * par * 0.6, 0.15), Math.PI / 2 - 0.01); // never below the floor
      camera.position.setFromSphericalCoords(dist * (1 - dolly * s), po, az).add(target);
      camera.lookAt(target);
    }

    function draw() {
      place();
      renderer.render(scene, camera);
      renders++;
    }

    function request() {
      if (running || dead || lost || !inView || document.hidden) return;
      running = true;
      last = performance.now();
      renderer.setAnimationLoop(frame);
    }
    function stop() {
      running = false;
      renderer?.setAnimationLoop(null);
    }

    function frame(now) {
      const dt = Math.min(Math.max(((now ?? performance.now()) - last) / 1000, 1 / 240), 1 / 30);
      last = now ?? performance.now();
      const kp = 1 - Math.exp(-dt * 5), ks = 1 - Math.exp(-dt * 6); // frame-rate-independent damping
      pC.x += (pT.x - pC.x) * kp;
      pC.y += (pT.y - pC.y) * kp;
      sC += (sT - sC) * ks;
      const settled = Math.abs(pT.x - pC.x) < 1e-4 && Math.abs(pT.y - pC.y) < 1e-4 && Math.abs(sT - sC) < 1e-4;
      if (settled) { pC.x = pT.x; pC.y = pT.y; sC = sT; }
      draw();
      if (settled) stop(); // frameloop on demand: nothing moves, nothing renders
    }

    async function enableScroll() {
      if (!sc || mm || dead || !motionOK()) return;
      try {
        const [g, st] = await Promise.all([o.loadGsap(), o.loadScrollTrigger()]);
        const gsap = g.gsap ?? g.default;
        const ScrollTrigger = st.ScrollTrigger ?? st.default;
        if (dead || mm || !motionOK()) return; // the setting may have flipped while GSAP loaded
        gsap.registerPlugin(ScrollTrigger);
        mm = gsap.matchMedia();
        mm.add('(prefers-reduced-motion: no-preference)', () => {
          if (document.documentElement.dataset.motion === 'reduce') return;
          const trigger = ScrollTrigger.create({
            trigger: sc.trigger ?? container, start: sc.start, end: sc.end,
            onUpdate: (self) => { sT = self.progress; request(); },
            onRefresh: (self) => { sT = self.progress; request(); },
          });
          sT = trigger.progress;
          request();
          return () => { sT = sC = 0; request(); }; // reverted (reduced motion): back to the rest pose
        });
      } catch (err) {
        try { o.onError?.(err); } catch { /* scroll move is optional */ }
      }
    }

    listen(window, 'pointermove', (e) => {
      if (!o.parallax || !motionOK() || !fine.matches || e.pointerType === 'touch') return;
      pT.x = Math.max(-1, Math.min(1, (e.clientX / window.innerWidth) * 2 - 1));
      pT.y = Math.max(-1, Math.min(1, (e.clientY / window.innerHeight) * 2 - 1));
      request();
    }, { passive: true });
    listen(document.documentElement, 'pointerleave', () => { pT.x = pT.y = 0; request(); });
    listen(document, 'visibilitychange', () => (document.hidden ? stop() : request()));
    const onMotion = () => {
      canvas.style.transition = `opacity ${fade()}ms cubic-bezier(.33,1,.68,1)`;
      if (motionOK()) { enableScroll(); return; }
      mm?.revert(); // matchMedia reverts itself for the OS setting, but not for the in-page toggle
      mm = null;    // a reverted matchMedia never re-runs; enableScroll() builds a fresh one
      pT.x = pT.y = pC.x = pC.y = 0; sT = sC = 0; // cut to the rest pose: one still frame, no glide
      request();
    };
    listen(reduce, 'change', onMotion);
    listen(window, 'motionchange', onMotion);
    listen(canvas, 'webglcontextlost', () => { lost = true; stop(); canvas.style.opacity = '0'; });
    listen(canvas, 'webglcontextrestored', () => {
      lost = false;
      applyClear();
      envRT.dispose();
      envRT = makeEnv(); // PMREM target contents do not survive a context loss
      scene.environment = envRT.texture;
      grain.needsUpdate = true;
      if (shadowTex) shadowTex.needsUpdate = true;
      draw();
      requestAnimationFrame(() => { if (!lost && !dead) canvas.style.opacity = '1'; });
    });

    resize();
    place();
    await renderer.compileAsync(scene, camera); // no shader-compile hitch on the first visible frame
    if (isCancelled()) { dispose(); return { dispose() {}, state: () => ({}), snapshot: () => null }; }
    draw();
    requestAnimationFrame(() => {
      if (dead || lost) return;
      canvas.style.opacity = '1'; // the poster underneath is untouched
      shown = true;
    });

    let stale = false; // resized while offscreen: draw once on the way back in
    io = new IntersectionObserver(([e]) => {
      inView = e.isIntersecting;
      if (!inView) { stop(); return; }
      if (stale && !lost) { stale = false; draw(); }
      if (pT.x !== pC.x || pT.y !== pC.y || sT !== sC) request();
    }, { rootMargin: '100px' });
    io.observe(container);
    ro = new ResizeObserver(() => {
      if (canvas.clientWidth === sizeW && canvas.clientHeight === sizeH) return; // e.g. the initial callback
      resize();
      if (running) return;
      if (inView && !lost) draw();
      else stale = true;
    });
    ro.observe(container);
    enableScroll();

    return {
      dispose,
      state: () => ({ live: shown && !dead && !lost, running, renders, dpr: renderer.getPixelRatio(), scroll: !!mm }),
      snapshot(type, quality) {
        draw(); // toDataURL in the same task as the render, so preserveDrawingBuffer is not needed
        return canvas.toDataURL(type, quality);
      },
    };
  } catch (err) {
    dispose();
    throw err;
  }
}

/* ---------- procedural assets ---------- */

// A turned vessel: the profile runs from the underside centre, up the outer wall, over a rounded lip and
// down the inner wall to the inside floor, so LatheGeometry's winding faces every surface outward.
function vesselGeometry(THREE) {
  const pts = [
    [0, 0], [0.2, 0], [0.232, 0.008], [0.246, 0.034], [0.292, 0.15], [0.352, 0.38], [0.39, 0.64],
    [0.404, 0.86], [0.41, 0.975], [0.402, 0.997], [0.388, 0.997], [0.381, 0.975], [0.373, 0.86],
    [0.358, 0.63], [0.32, 0.37], [0.25, 0.165], [0.15, 0.098], [0, 0.088],
  ].map(([x, y]) => new THREE.Vector3(x, y, 0));
  const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
  const profile = curve.getPoints(pts.length * 9).map((p) => new THREE.Vector2(Math.max(p.x, 0), p.y));
  profile[0].x = 0;
  profile[profile.length - 1].x = 0;
  return new THREE.LatheGeometry(profile, 96);
}

// Tileable value-noise roughness (G channel), 0.78-1.0 x base roughness: smudges, not a mirror.
function roughnessNoise(THREE, size = 128) {
  let seed = 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const octave = (period) => {
    const g = Float32Array.from({ length: period * period }, rnd);
    return (x, y) => {
      const fx = (x / size) * period, fy = (y / size) * period;
      const x0 = Math.floor(fx), y0 = Math.floor(fy);
      const tx = fx - x0, ty = fy - y0;
      const sx = tx * tx * (3 - 2 * tx), sy = ty * ty * (3 - 2 * ty);
      const at = (i, j) => g[((j % period) * period) + (i % period)];
      const a = at(x0, y0) + (at(x0 + 1, y0) - at(x0, y0)) * sx;
      const b = at(x0, y0 + 1) + (at(x0 + 1, y0 + 1) - at(x0, y0 + 1)) * sx;
      return a + (b - a) * sy;
    };
  };
  const o1 = octave(8), o2 = octave(16), o3 = octave(32);
  const data = new Uint8Array(size * size * 4);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const n = o1(x, y) * 0.5 + o2(x, y) * 0.3 + o3(x, y) * 0.2;
      const v = Math.round((0.78 + 0.22 * n) * 255);
      const i = (y * size + x) * 4;
      data[i] = data[i + 1] = data[i + 2] = v;
      data[i + 3] = 255;
    }
  }
  const tex = new THREE.DataTexture(data, size, size);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(4, 4);
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = THREE.LinearMipmapLinearFilter;
  tex.generateMipmaps = true;
  tex.needsUpdate = true;
  return tex;
}

// Soft radial alpha falloff (many stops, so it does not band) for the contact shadow planes.
function shadowTexture(THREE) {
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  for (let i = 0; i <= 16; i++) {
    const t = i / 16;
    const s = t * t * (3 - 2 * t);
    grd.addColorStop(t, `rgba(255,255,255,${Math.pow(1 - s, 1.8).toFixed(4)})`);
  }
  g.fillStyle = grd;
  g.fillRect(0, 0, 128, 128);
  return new THREE.CanvasTexture(c);
}

/* ---------- boot helpers ---------- */

// Opaque sRGB [r, g, b] for the clear colour. An explicit colour wins; otherwise the first opaque ancestor background.
function resolveBackground(el, explicit) {
  const ctx = Object.assign(document.createElement('canvas'), { width: 1, height: 1 })
    .getContext('2d', { willReadFrequently: true });
  const read = (css) => {
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = 'rgba(0,0,0,0)';
    ctx.fillStyle = css; // any CSS colour syntax, including oklch() and color()
    ctx.fillRect(0, 0, 1, 1);
    const d = ctx.getImageData(0, 0, 1, 1).data;
    return d[3] === 255 ? [d[0], d[1], d[2]] : null;
  };
  if (explicit && explicit !== 'auto') return read(explicit) ?? [255, 255, 255];
  for (let n = el; n; n = n.parentElement) {
    const c = read(getComputedStyle(n).backgroundColor);
    if (c) return c;
  }
  return [255, 255, 255];
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

// Resolves after window load, the first largest-contentful-paint entry (where the API exists) and an idle slot.
function afterLCP(timeout = 2500) {
  return new Promise((resolve) => {
    const idle = () => ('requestIdleCallback' in window
      ? requestIdleCallback(() => resolve(), { timeout: 2000 })
      : setTimeout(resolve, 200));
    const afterLoad = () => {
      if (!PerformanceObserver.supportedEntryTypes?.includes('largest-contentful-paint')) { idle(); return; }
      let done = false;
      const go = () => { if (done) return; done = true; po.disconnect(); idle(); };
      const po = new PerformanceObserver((list) => { if (list.getEntries().length) go(); });
      po.observe({ type: 'largest-contentful-paint', buffered: true });
      setTimeout(go, timeout); // hidden-at-load pages never report LCP
    };
    if (document.readyState === 'complete') afterLoad();
    else addEventListener('load', afterLoad, { once: true });
  });
}
