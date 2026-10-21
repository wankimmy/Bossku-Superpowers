/* ==========================================================================
   motion-core.js: smooth scroll plus scroll choreography from data attributes
   --------------------------------------------------------------------------
   What it does
     Lenis smooth wheel scroll driven by GSAP's ticker and synced to
     ScrollTrigger, plus a registry of scroll effects you switch on in markup:
       data-intro / data-intro-item / data-intro-media   above-the-fold intro (needs the CSS deadline in boot.html-snippet.html)
       data-reveal="lines"   masked line rise (SplitText, headings only, reverted after)
       data-reveal="image"   clip-inset un-clip plus media scale settle
       data-reveal="settle"  small y settle, never opacity
       data-reveal="items"   children settle, row by row, total spread capped
       data-parallax="0.15"  scrubbed y travel = 0.15 x viewport height; + lags (reads deeper), - leads.
                             On img/video/canvas/picture the media is over-scaled so its clipping frame never shows an edge.
       data-marquee          CSS keyframe loop + scroll-velocity boost + pause button (WCAG 2.2.2)
       data-pin="horizontal" pinned horizontal track; vertical stack under reduced motion and below pinMinWidth
       data-stack            sticky stacking cards (CSS does the stacking; JS adds the covered card's recede)
     Usage
       <script type="module">
         import { init } from './motion-core.js';
         const motion = init();            // or init({ smoothScroll: false, pinMinWidth: '64em' })
       </script>
     Markup contracts are in the demo (demo/index.html) and in motion-core.css.
   Options (init)
     root          Document|Element  scope for data-* lookups (default document)
     smoothScroll  boolean  Lenis on wheel input; touch stays native (syncTouch: false). Default true
     lenis         object   extra Lenis options, merged over { lerp: 0.1, anchors: true, stopInertiaOnNavigate: true,
                            respectReducedMotion: true }. Pass lerp OR duration, never both
     intro, reveals, parallax, marquee, pin, stack   booleans, each default true
     pinMinWidth   CSS length. Below it data-pin stays a vertical stack. Default '60em'
     revealStart   ScrollTrigger start for reveals. Default 'top bottom' (the first pixel entering)
     introFailsafe ms after which a starved intro is forced to its end state. Default 3500
     introMaxStart ms since navigation start. If the module boots later than this, the intro is shown
                   at rest instead of animated. Measured: the heading's LCP entry lands when the intro
                   ENDS (SplitText's revert paints the full text node), i.e. boot + ~1.3s, so a late boot
                   would push LCP past 2.5s. Default 800 (worst case LCP ~2.1s). Infinity disables it
     motionToggle  selector for an in-page "Reduce motion" button (aria-pressed). Default '[data-motion-toggle]'
   Exports
     init(options) -> api { gsap, ScrollTrigger, SplitText, lenis (getter), refresh(), scrollTo(target, opts), destroy() }
     destroy(), registerReveal(name, fn), setMotionPreference('reduce'|'full'), getLenis()
     window event 'motionchange' (detail: 'full'|'reduce') fires when the effective motion setting flips,
     so WebGL, video and other recipes can follow it.
   Fallback behaviour
     - HTML+CSS render every element at rest. JS sets a hidden start state only in the
       frame its animation starts, only inside gsap.matchMedia('(prefers-reduced-motion:
       no-preference)'), and never on an element already on screen at boot. The one
       exception is the intro, which the CSS deadline protects.
     - If a CDN import fails, this module never runs: nothing was hidden, the CSS
       deadline releases the intro, the marquee stays a static wrapped row, the pin
       section stays a vertical stack, and sticky cards still stack. If only Lenis
       fails, native scroll is kept.
     - Reduced motion (OS setting or the in-page toggle) reverts everything live: Lenis
       destroyed, split text restored, pins removed, marquee static.
   Tested against
     gsap 3.15.0 and lenis 1.3.26 from cdn.jsdelivr.net (+esm builds via the import map
     in boot.html-snippet.html). Chromium 145 (headless shell 145.0.7632.6), Playwright
     1.58, 2026-09-25: 91/91 checks in evidence/recipes-qa/qa.py covering
     no-JS, reduced motion, full motion at 1440 and 390, CDN blocked, slow module boot,
     live OS reduced-motion flip, in-page toggle, live resize across pinMinWidth,
     anchors and skip-link focus, zero layout shift from split masks, and the page
     transition. Firefox and WebKit not run.
   ========================================================================== */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
import { CustomEase } from 'gsap/CustomEase';

gsap.registerPlugin(ScrollTrigger, SplitText, CustomEase);

const Q_FULL = '(prefers-reduced-motion: no-preference)';
const Q_REDUCE = '(prefers-reduced-motion: reduce)';
const STORE_KEY = 'motion';
const INTERACTIVE = 'a, button, input, select, textarea, summary, [tabindex], [contenteditable]';
// clearProps at rest: GSAP writes inline translate/rotate/scale: none next to its transform, which would
// otherwise keep overriding author CSS (e.g. a :hover translate) after the motion has finished.
const REST = 'transform,translate,rotate,scale';

const DEFAULTS = {
  root: document,
  smoothScroll: true,
  lenis: {},
  intro: true,
  reveals: true,
  parallax: true,
  marquee: true,
  pin: true,
  stack: true,
  pinMinWidth: '60em',
  revealStart: 'top bottom',
  introFailsafe: 3500,
  introMaxStart: 800,
  motionToggle: '[data-motion-toggle]',
};

// Token name -> fallback, used when tokens.css is absent. Same values as tokens.css.
// Each ease is registered as CustomEase 'motion<Key>' so JS and CSS share curves.
const EASES = {
  OutCubic: ['--ease-out-cubic', '.33,1,.68,1'],
  OutQuart: ['--ease-out-quart', '.25,1,.5,1'],
  OutQuint: ['--ease-out-quint', '.22,1,.36,1'],
  OutExpo: ['--ease-out-expo', '.16,1,.3,1'],
  InCubic: ['--ease-in-cubic', '.32,0,.67,0'],
  InOutQuart: ['--ease-in-out-quart', '.76,0,.24,1'],
  InOutExpo: ['--ease-in-out-expo', '.87,0,.13,1'],
  InOutSine: ['--ease-in-out-sine', '.37,0,.63,1'],
};
const SCALARS = {
  dur1: ['--dur-1', 0.12], dur2: ['--dur-2', 0.2], dur3: ['--dur-3', 0.35],
  dur4: ['--dur-4', 0.6], dur5: ['--dur-5', 1], dur6: ['--dur-6', 1.4],
  staggerLines: ['--stagger-lines', 0.08], staggerItems: ['--stagger-items', 0.08],
  staggerMax: ['--stagger-max', 0.6],
};

let S = null;          // live state: { o, mm, lenis, offs, running }
let memPref = null;    // in-page preference when localStorage throws (private mode, blocked storage)

/* ---------- public API ---------------------------------------------------- */

export function init(options = {}) {
  if (S) destroy();
  S = { o: { ...DEFAULTS, ...options }, mm: null, lenis: null, offs: [], running: new Set() };
  ScrollTrigger.config({ ignoreMobileResize: true }); // iOS toolbar show/hide must not re-measure

  syncFlag(false);
  const os = matchMedia(Q_REDUCE);
  const onOS = () => syncFlag(true);
  os.addEventListener('change', onOS);
  S.offs.push(() => os.removeEventListener('change', onOS));
  wireToggle();
  build();

  // Fonts and late images move trigger positions: re-measure once they settle.
  const refresh = () => S && ScrollTrigger.refresh();
  document.fonts?.ready.then(refresh);
  if (document.readyState !== 'complete') {
    addEventListener('load', refresh, { once: true });
    S.offs.push(() => removeEventListener('load', refresh));
  }
  // Print or "save as PDF" mid-reveal: jump running reveals to their end state.
  const finish = () => S?.running.forEach((a) => a.progress(1));
  addEventListener('beforeprint', finish);
  S.offs.push(() => removeEventListener('beforeprint', finish));

  return {
    gsap, ScrollTrigger, SplitText,
    get lenis() { return S?.lenis ?? null; },
    refresh: () => ScrollTrigger.refresh(),
    scrollTo,
    destroy,
  };
}

export function destroy() {
  if (!S) return;
  S.mm?.revert();
  S.offs.forEach((off) => off());
  S = null;
}

export const getLenis = () => S?.lenis ?? null;

/** Add a reveal type. fn(el, tokens) runs when el first enters; it must create its hidden
 *  start state and start animating in the same call, and return the animation. */
export function registerReveal(name, fn) { REVEALS.set(name, fn); }

/** In-page motion choice, persisted per viewer. It can only reduce motion: when the OS
 *  asks for reduced motion, that always wins. */
export function setMotionPreference(pref) {
  memPref = pref === 'reduce' ? 'reduce' : null;
  try {
    if (memPref) localStorage.setItem(STORE_KEY, 'reduce');
    else localStorage.removeItem(STORE_KEY);
  } catch (e) { /* storage blocked: memPref holds it for this page view */ }
  syncFlag(true);
  if (S) { S.mm.revert(); build(); ScrollTrigger.refresh(); }
}

function scrollTo(target, opts = {}) {
  if (S?.lenis) return S.lenis.scrollTo(target, opts);
  const y = typeof target === 'number' ? target
    : (typeof target === 'string' ? document.querySelector(target) : target)?.getBoundingClientRect().top + scrollY;
  if (Number.isFinite(y)) window.scrollTo({ top: y + (opts.offset || 0), behavior: opts.immediate ? 'instant' : 'auto' });
}

/* ---------- motion flag and toggle ---------------------------------------- */

function savedPref() {
  if (memPref) return memPref;
  try { return localStorage.getItem(STORE_KEY); } catch (e) { return null; }
}
const osReduces = () => matchMedia(Q_REDUCE).matches;
const allowed = () => !osReduces() && savedPref() !== 'reduce';

// Mirrors the boot script: data-motion="full|reduce" (+ .motion-ok alias) on <html>.
function syncFlag(announce) {
  const root = document.documentElement;
  const next = allowed() ? 'full' : 'reduce';
  const changed = root.dataset.motion !== next;
  root.dataset.motion = next;
  root.classList.toggle('motion-ok', next === 'full');
  S?.toggles?.forEach((b) => {
    b.hidden = osReduces();                         // nothing to reduce further: the OS already does
    b.setAttribute('aria-pressed', String(next === 'reduce'));
  });
  if (changed && announce) dispatchEvent(new CustomEvent('motionchange', { detail: next }));
}

function wireToggle() {
  const btns = [...document.querySelectorAll(S.o.motionToggle)];
  const onClick = () => setMotionPreference(savedPref() === 'reduce' ? 'full' : 'reduce');
  btns.forEach((b) => b.addEventListener('click', onClick));
  S.toggles = btns;
  syncFlag(false);
  S.offs.push(() => btns.forEach((b) => { b.removeEventListener('click', onClick); b.hidden = true; }));
}

/* ---------- build: everything lives inside gsap.matchMedia ----------------- */

function build() {
  const { o } = S;
  const mm = (S.mm = gsap.matchMedia());

  // Pins first: their spacing must exist before triggers further down are measured.
  if (o.pin) mm.add(`${Q_FULL} and (min-width: ${o.pinMinWidth})`, () => (allowed() ? setupPins() : undefined));

  mm.add(Q_FULL, (ctx) => {
    if (!allowed()) { ownIntro(); return; }
    const T = readTokens();
    const offs = [];
    if (o.smoothScroll) offs.push(startLenis());
    if (o.intro) offs.push(setupIntro(T)); else ownIntro();
    if (o.reveals) setupReveals(ctx, T);
    if (o.parallax) setupParallax();
    if (o.marquee) offs.push(setupMarquees());
    if (o.stack) offs.push(setupStack());
    return () => { offs.forEach((off) => off && off()); S?.running.clear(); };
  });

  // Reduced motion: nothing to set up. Content is already at rest. Release a stray intro arm.
  mm.add(Q_REDUCE, () => { ownIntro(); });
}

function readTokens() {
  const cs = getComputedStyle(document.documentElement);
  for (const [key, [prop, fallback]] of Object.entries(EASES)) {
    const m = cs.getPropertyValue(prop).match(/cubic-bezier\(([^)]+)\)/);
    CustomEase.create('motion' + key, m ? m[1].replace(/\s+/g, '') : fallback);
  }
  const T = {};
  for (const [key, [prop, fallback]] of Object.entries(SCALARS)) {
    const raw = cs.getPropertyValue(prop).trim();
    const n = parseFloat(raw);
    T[key] = Number.isFinite(n) ? (raw.endsWith('ms') ? n / 1000 : n) : fallback;
  }
  return T;
}

/* ---------- smooth scroll -------------------------------------------------- */

function startLenis() {
  let lenis = null;
  let live = true;
  const raf = (time) => lenis?.raf(time * 1000); // GSAP ticker seconds -> Lenis ms: one rAF loop
  import('lenis')
    .then(({ default: Lenis }) => {
      if (!live || !S) return;
      lenis = S.lenis = new Lenis({
        lerp: 0.1,                   // 0.08-0.12. Lower feels floaty. Never pass duration as well
        smoothWheel: true,
        syncTouch: false,            // touch keeps native momentum
        anchors: true,               // in-page #links scroll through Lenis, honouring scroll-margin/padding.
                                     // 1.3.26 does not preventDefault, so the hash and focus start point stay native
        stopInertiaOnNavigate: true,
        autoRaf: false,
        respectReducedMotion: true,  // 1.3.26 default, explicit: lerp 1 + instant scrollTo under reduce.
                                     // Belt and braces: this code never creates Lenis under reduce anyway.
        ...S.o.lenis,
      });
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(raf);
      gsap.ticker.lagSmoothing(0);  // no catch-up jumps against the smoothed scroll
    })
    .catch((err) => console.warn('[motion-core] Lenis did not load; keeping native scroll.', err));
  return () => {
    live = false;
    gsap.ticker.remove(raf);
    gsap.ticker.lagSmoothing(500, 33); // GSAP defaults
    lenis?.destroy();
    if (S) S.lenis = null;
  };
}

/* ---------- intro (above the fold, guarded by the CSS deadline) ------------ */

const ownIntro = () => document.documentElement.setAttribute('data-intro-owned', '');
const splittable = (el) => /^H[1-6]$/.test(el.tagName) && !el.querySelector(INTERACTIVE);

function setupIntro(T) {
  const heading = document.querySelector('[data-intro]');
  const items = gsap.utils.toArray('[data-intro-item]');
  const media = gsap.utils.toArray('[data-intro-media]');
  const all = [heading, ...items, ...media].filter(Boolean);
  if (!all.length) return;
  const root = document.documentElement;
  // Only animate content the CSS deadline is still holding. Once the deadline has fired (or the
  // snippet is missing) the content is on screen and must not be hidden again.
  const armed = all.every((el) => el.getAnimations().some(
    (a) => a.animationName?.startsWith('intro-deadline') && a.playState !== 'finished'));
  if (root.hasAttribute('data-intro-owned') || !armed) { ownIntro(); return; }
  // LCP budget: a late boot shows the intro at rest now rather than finishing it ~1.3s later.
  if (performance.now() > S.o.introMaxStart) { ownIntro(); return; }

  // Read the CSS arm's offsets first so the JS start state matches it exactly.
  const shifts = items.map((el) => parseFloat(getComputedStyle(el).translate.split(' ')[1]) || 0);
  const scales = media.map((el) => parseFloat(getComputedStyle(el).scale) || 1);
  // Release the CSS arm BEFORE creating any tween. GSAP 3.12+ folds the CSS individual transform
  // properties (translate, scale) into its transform cache, so a from() created while the arm is
  // still applied records the ARMED offset as its end state: it would tween 16px -> 16px and leave
  // the item low (and a later revert would restore the armed look). Everything below runs in this
  // same task, so no frame is painted between un-arming and the JS start states: no flash.
  root.setAttribute('data-intro-owned', '');
  let headTween = null;
  const tweens = [];

  if (heading && splittable(heading)) {
    SplitText.create(heading, {
      type: 'lines', mask: 'lines', linesClass: 'rv-line', aria: 'auto',
      autoSplit: true, // re-split on font load/resize; the returned tween is time-synced
      onSplit: (self) => (headTween = gsap.from(self.lines, {
        yPercent: 120, duration: T.dur5 * 1.1, ease: 'motionOutExpo', stagger: T.staggerLines,
        onComplete: () => self.revert(), // restore the original DOM (a11y, find-in-page, text spacing)
      })),
    });
  } else if (heading) {
    tweens.push(gsap.fromTo(heading, { clipPath: 'inset(0% 0% 100% 0%)' },
      { clipPath: 'inset(0% 0% 0% 0%)', duration: T.dur5, ease: 'motionOutExpo', clearProps: 'clipPath' }));
  }
  if (items.length) tweens.push(gsap.from(items, {
    y: (i) => shifts[i], duration: T.dur4, ease: 'motionOutQuart',
    delay: heading ? 0.35 : 0, stagger: T.staggerItems, clearProps: REST,
  }));
  if (media.length) tweens.push(gsap.from(media, {
    scale: (i) => scales[i], duration: T.dur6 * 1.2, ease: 'motionOutExpo', clearProps: REST,
  }));

  // A background tab can starve the ticker. Force the end state rather than leave text clipped.
  const timer = setTimeout(() => [headTween, ...tweens].forEach((t) => t && t.progress(1)), S.o.introFailsafe);
  return () => clearTimeout(timer);
}

/* ---------- reveal registry ------------------------------------------------ */

const REVEALS = new Map([
  ['lines', revealLines],
  ['image', revealImage],
  ['settle', revealSettle],
  ['items', revealItems],
]);

function track(anim) {
  if (!anim || !S) return anim;
  S.running.add(anim);
  anim.then?.(() => S?.running.delete(anim));
  return anim;
}

function setupReveals(ctx, T) {
  gsap.utils.toArray('[data-reveal]', S.o.root).forEach((el) => {
    const run = REVEALS.get(el.dataset.reveal || 'settle');
    if (!run) { console.warn('[motion-core] unknown data-reveal:', el.dataset.reveal, el); return; }
    if (el.closest('[data-pin], [data-intro]')) return;     // pinned tracks and the intro have their own motion
    if (el.getBoundingClientRect().top < innerHeight) return; // on screen (or above) at boot: never hide it
    ScrollTrigger.create({
      trigger: el,
      start: el.dataset.revealStart || S.o.revealStart,
      once: true,
      // Lazy arming: the hidden start state is created here, in the frame the animation starts.
      // If this never fires, the element simply stays visible.
      onEnter: (self) => {
        // Anchor jumps, scroll restoration and hard flings land far past the start with the
        // content already in view: leave it as it is instead of hiding it for a replay.
        if (self.scroll() - self.start > innerHeight * 0.5 || Math.abs(self.getVelocity()) > 3000) return;
        ctx.add(() => track(run(el, T)));
      },
    });
  });
}

function revealLines(el, T) {
  // SplitText's aria:'auto' puts aria-label on the element, which ARIA 1.2 forbids on
  // generic/paragraph roles. So only split headings without interactive children.
  if (!splittable(el)) return revealSettle(el, T);
  SplitText.create(el, {
    type: 'lines', mask: 'lines', linesClass: 'rv-line', aria: 'auto', autoSplit: true,
    onSplit: (self) => track(gsap.from(self.lines, {
      yPercent: 120, duration: T.dur5, ease: 'motionOutExpo', stagger: T.staggerLines,
      onComplete: () => self.revert(),
    })),
  });
}

function revealImage(el, T) {
  const media = el.querySelector('img, video, canvas, picture, svg');
  const tl = gsap.timeline();
  // Both ends are inset(): GSAP cannot interpolate from `none`. The start is only partly
  // clipped, so a frozen frame still shows the image.
  tl.fromTo(el, { clipPath: 'inset(14% 10% 14% 10%)' },
    { clipPath: 'inset(0% 0% 0% 0%)', duration: T.dur6, ease: 'motionOutExpo', clearProps: 'clipPath' }, 0);
  if (media && !media.hasAttribute('data-parallax')) // parallax owns that media's scale
    tl.fromTo(media, { scale: 1.18 }, { scale: 1, duration: T.dur6 * 1.15, ease: 'motionOutExpo', clearProps: REST }, 0);
  return tl;
}

function revealSettle(el, T) {
  return gsap.from(el, { y: 24, duration: T.dur4, ease: 'motionOutQuart', clearProps: REST }); // no opacity: visible throughout
}

function revealItems(el, T) {
  const kids = [...el.children];
  const each = Math.min(T.staggerItems, T.staggerMax / Math.max(1, kids.length - 1));
  return gsap.from(kids, {
    y: 24, duration: T.dur4, ease: 'motionOutQuart', clearProps: REST,
    stagger: { each, grid: 'auto', from: 'start' }, // reading order, row by row
  });
}

/* ---------- parallax (scrubbed, on already-visible elements) ----------------- */

function setupParallax() {
  gsap.utils.toArray('[data-parallax]', S.o.root).forEach((el) => {
    if (el.closest('[data-pin]')) return;
    const v = gsap.utils.clamp(-0.5, 0.5, parseFloat(el.dataset.parallax) || 0);
    if (!v) return;
    const isMedia = el.matches('img, video, canvas, picture');
    const frame = isMedia ? el.parentElement : el;
    const travel = () => v * innerHeight;
    // Over-scale media so +-travel/2 never uncovers the clipping frame's edge.
    const extra = isMedia ? { scale: () => 1 + Math.abs(travel()) / Math.max(1, frame.offsetHeight) } : {};
    gsap.fromTo(el, { y: () => -travel() / 2, ...extra }, {
      y: () => travel() / 2, ...extra, ease: 'none',
      scrollTrigger: { trigger: frame, start: 'top bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true },
    });
  });
}

/* ---------- marquee (CSS core, velocity boost, pause control) --------------- */

function setupMarquees() {
  const list = gsap.utils.toArray('[data-marquee]', S.o.root).map(liveMarquee).filter(Boolean);
  if (!list.length) return;
  let boost = 0;
  // Page-wide trigger for scroll velocity in px/s, with or without Lenis.
  ScrollTrigger.create({
    start: 0, end: 'max',
    onUpdate: (self) => { boost = Math.max(boost, Math.min(3, Math.abs(self.getVelocity()) / 1000)); },
  });
  const tick = () => {
    boost *= Math.pow(0.92, gsap.ticker.deltaRatio()); // frame-rate independent decay
    const rate = 1 + boost;
    list.forEach((m) => {
      if (m.boost && m.anim && Math.abs(m.anim.playbackRate - rate) > 0.01) m.anim.updatePlaybackRate(rate);
    });
  };
  gsap.ticker.add(tick);
  return () => { gsap.ticker.remove(tick); list.forEach((m) => m.off()); };
}

function liveMarquee(m) {
  const track = m.querySelector('[data-marquee-track]');
  const group = track?.querySelector('[data-marquee-group]');
  if (!group) return null;
  // One authored copy in HTML. The loop duplicate is JS-only, hidden from AT and focus.
  const clone = group.cloneNode(true);
  clone.setAttribute('aria-hidden', 'true');
  clone.inert = true;
  [clone, ...clone.querySelectorAll('[id]')].forEach((n) => n.removeAttribute('id'));
  track.append(clone);
  const speed = parseFloat(m.dataset.marqueeSpeed) || 60; // px/s
  const setDuration = () => m.style.setProperty('--marquee-duration', (group.offsetWidth / speed).toFixed(2) + 's');
  setDuration();
  const ro = new ResizeObserver(setDuration);
  ro.observe(group);
  m.classList.add('is-live');
  const anim = track.getAnimations().find((a) => a.animationName === 'marquee') || null;
  const btn = m.querySelector('[data-marquee-toggle]');
  const onClick = () => btn.setAttribute('aria-pressed', String(m.classList.toggle('is-paused')));
  if (btn) { btn.hidden = false; btn.addEventListener('click', onClick); }
  return {
    anim,
    boost: m.dataset.marqueeBoost !== 'false',
    off() {
      ro.disconnect();
      clone.remove();
      m.classList.remove('is-live', 'is-paused');
      m.style.removeProperty('--marquee-duration');
      if (btn) { btn.hidden = true; btn.setAttribute('aria-pressed', 'false'); btn.removeEventListener('click', onClick); }
    },
  };
}

/* ---------- pinned horizontal section --------------------------------------- */

function setupPins() {
  const offs = [];
  gsap.utils.toArray('[data-pin="horizontal"]', S.o.root).forEach((section) => {
    const track = section.querySelector('[data-pin-track]');
    if (!track) return;
    section.classList.add('is-pinned'); // CSS switches the vertical stack to a horizontal row
    const distance = () => Math.max(0, track.scrollWidth - section.clientWidth);
    const tween = gsap.to(track, {
      x: () => -distance(),
      ease: 'none', // required: children use it as containerAnimation
      scrollTrigger: {
        trigger: section, start: 'top top', end: () => '+=' + distance(),
        pin: true, scrub: true, anticipatePin: 1, invalidateOnRefresh: true, refreshPriority: 1,
      },
    });
    // Pins longer than ~1.5 viewports read as scroll-jacking (motion-stack.md 4.5, 6.1).
    if (distance() > innerHeight * 1.5) {
      console.warn(`[motion-core] data-pin track needs ${Math.round((distance() / innerHeight) * 100)}vh of scroll; keep it near 150vh (fewer or narrower panels).`, section);
    }
    track.querySelectorAll('[data-pin-media]').forEach((media) => {
      gsap.fromTo(media, { scale: 1.12 }, {
        scale: 1, ease: 'none',
        scrollTrigger: { trigger: media.parentElement, containerAnimation: tween, start: 'left right', end: 'right left', scrub: true },
      });
    });
    // Keyboard: tabbing into an off-screen panel scrolls the page to the scroll position that shows it.
    const onFocus = (e) => {
      const panel = e.target.closest('[data-pin-panel]');
      const st = tween.scrollTrigger;
      if (!panel || !st) return;
      const d = distance();
      const x = gsap.utils.clamp(0, d, panel.offsetLeft - (section.clientWidth - panel.offsetWidth) / 2);
      scrollTo(st.start + (d ? (x / d) * (st.end - st.start) : 0), { immediate: true, force: true });
    };
    track.addEventListener('focusin', onFocus);
    offs.push(() => {
      track.removeEventListener('focusin', onFocus);
      section.classList.remove('is-pinned');
      // Context.revert kills the ScrollTrigger AFTER reverting the tween, and the kill re-renders the tween
      // at progress 0, leaving an identity transform + translate: none inline. Cleanup functions run last.
      gsap.set(track, { clearProps: REST });
    });
  });
  ScrollTrigger.sort();
  return () => offs.forEach((off) => off());
}

/* ---------- sticky stacking cards ------------------------------------------- */

function setupStack() {
  const offs = [];
  gsap.utils.toArray('[data-stack]', S.o.root).forEach((stack) => {
    const cards = [...stack.children];
    cards.forEach((card, i) => {
      const next = cards[i + 1];
      if (!next) return;
      // Overlay opacity composites; animating filter: brightness() would repaint every frame.
      const shade = document.createElement('span');
      shade.className = 'stack-shade';
      shade.setAttribute('aria-hidden', 'true');
      card.append(shade);
      offs.push(() => shade.remove());
      gsap.timeline({
        defaults: { ease: 'none' },
        scrollTrigger: {
          trigger: next, start: 'top bottom',
          end: () => `top ${parseFloat(getComputedStyle(next).top) || 0}px`, // where `next` sticks
          scrub: true, invalidateOnRefresh: true,
        },
      })
        .to(card, { scale: 0.94 }, 0)
        .to(shade, { opacity: 0.35 }, 0);
    });
  });
  return () => offs.forEach((off) => off());
}
