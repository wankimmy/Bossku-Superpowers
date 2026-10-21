/* ==========================================================================
   magnetic.js: magnetic pull for buttons and standalone links. The box never moves.
   --------------------------------------------------------------------------
   What it does
     Inside a static hit area, the label drifts a few px toward the pointer and
     eases back on leave. The element's box does not lift, scale or translate
     (house law: no hover boop), so the target never slides out from under the
     cursor. The hover STATE is a tonal colour or fill change, or an icon nudge
     inside the box, done in your CSS, e.g.:
       .btn { transition: background-color var(--dur-2) var(--ease-micro), color var(--dur-2) var(--ease-micro); }
       .btn:hover { background: var(--ink); color: var(--surface); }   // tonal step, no movement
       .btn [data-magnetic-icon] { transition: translate var(--dur-3) var(--ease-micro); }
       .btn:hover [data-magnetic-icon] { translate: 0.25em 0; }        // icon slides inside the box
   Usage
     <a class="btn" href="/contact" data-magnetic><span data-magnetic-label>Start a project</span></a>
     import { initMagnetic } from './magnetic.js';
     const stop = initMagnetic();   // returns a cleanup function
   Options
     selector  '[data-magnetic]'
     max       6     px of label travel. Per element: data-magnetic="10". Hard cap 12
     duration  0.45  s for the follow to settle (a lagged follower, 0.35-0.5s)
     ease      'power3.out'  GSAP built-in, same family as --ease-out-quart
     If an element has no [data-magnetic-label] child, its contents are wrapped in
     one span while the effect is active and unwrapped on cleanup. Keep it off
     inline links inside running text.
   Fallback behaviour
     Runs only under (hover: hover) and (pointer: fine) and
     (prefers-reduced-motion: no-preference), and not while <html data-motion="reduce">
     (in-page toggle, see motion-core.js). Otherwise nothing happens and the CSS
     hover state still works. Keyboard focus gets your focus ring and no
     movement. If the gsap import fails, the module never runs and nothing changes.
   Tested against
     gsap 3.15.0 (jsdelivr +esm), Chromium 145, Playwright 1.58, 2026-09-24.
   ========================================================================== */
import { gsap } from 'gsap';

const QUERY = '(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)';

export function initMagnetic({ selector = '[data-magnetic]', max = 6, duration = 0.45, ease = 'power3.out', root = document } = {}) {
  let mm = null;

  const build = () => {
    mm = gsap.matchMedia();
    mm.add(QUERY, () => {
      if (document.documentElement.dataset.motion === 'reduce') return;
      const offs = [];
      const rects = new Map(); // cached per element: read on enter, dropped on scroll
      const dropRects = () => rects.clear();
      addEventListener('scroll', dropRects, { passive: true });
      offs.push(() => removeEventListener('scroll', dropRects));

      root.querySelectorAll(selector).forEach((el) => {
        let label = el.querySelector('[data-magnetic-label]');
        if (!label) { label = wrapContents(el); offs.push(() => unwrap(label)); }
        if (getComputedStyle(label).display === 'inline') { // transforms need a box
          label.style.display = 'inline-block';
          offs.push(() => label.style.removeProperty('display'));
        }
        const travel = Math.min(12, parseFloat(el.dataset.magnetic) || max);
        const xTo = gsap.quickTo(label, 'x', { duration, ease });
        const yTo = gsap.quickTo(label, 'y', { duration, ease });

        const enter = () => rects.set(el, el.getBoundingClientRect());
        const move = (e) => {
          let r = rects.get(el);
          if (!r) { r = el.getBoundingClientRect(); rects.set(el, r); }
          const dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
          const dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
          xTo(gsap.utils.clamp(-1, 1, dx) * travel);
          yTo(gsap.utils.clamp(-1, 1, dy) * travel * 0.5); // less vertical pull keeps the baseline calm
        };
        const leave = () => { rects.delete(el); xTo(0); yTo(0); };
        el.addEventListener('pointerenter', enter);
        el.addEventListener('pointermove', move);
        el.addEventListener('pointerleave', leave);
        offs.push(() => {
          el.removeEventListener('pointerenter', enter);
          el.removeEventListener('pointermove', move);
          el.removeEventListener('pointerleave', leave);
          gsap.set(label, { clearProps: 'transform' });
        });
      });
      return () => offs.forEach((off) => off());
    });
  };

  // Follow motion-core's in-page toggle.
  const onMotionChange = () => { mm?.revert(); build(); };
  addEventListener('motionchange', onMotionChange);
  build();
  return () => { removeEventListener('motionchange', onMotionChange); mm?.revert(); };
}

function wrapContents(el) {
  const span = document.createElement('span');
  span.setAttribute('data-magnetic-label', '');
  span.dataset.magneticAuto = '';
  span.style.display = 'inline-block';
  while (el.firstChild) span.append(el.firstChild);
  el.append(span);
  return span;
}

function unwrap(span) {
  if (!span.isConnected) return;
  span.replaceWith(...span.childNodes);
}
