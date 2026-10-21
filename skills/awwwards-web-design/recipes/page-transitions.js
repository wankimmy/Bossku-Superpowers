/* ==========================================================================
   page-transitions.js: shared-element naming and direction for cross-document
   View Transitions, plus a same-document helper for SPAs
   --------------------------------------------------------------------------
   Load as a CLASSIC, parser-blocking script in <head>, after the boot snippet:
     <script src="page-transitions.js"></script>
   Not type=module, not defer: a pagereveal listener registered late misses the
   first render (Chrome docs). It is small, dependency-free and only registers
   listeners.
   What it does
     pageswap (old page): gives view-transition-name to each [data-vt-share]
       element that pairs with the destination, i.e. it has no link, or its
       data-vt-href (or enclosing <a href>) points at the destination URL.
     pagereveal (new page): the same pairing against the page we came from, and
       adds the transition type "back" on back traversal so the CSS reverses.
     Names are removed when the transition finishes, so bfcache restores clean.
     Duplicate names are never assigned (a duplicate would skip the transition).
   Markup
     index:  <a href="work/alpha.html"><img data-vt-share="hero" …></a>
     detail: <img data-vt-share="hero" …>                (no link: always paired)
     Big pages: add <link rel="expect" href="#hero-id" blocking="render"> on the
     detail page so the shared element is parsed before the first render.
     Measure its cost first.
   Options
     window.pageTransitions.swap(update, { types }) for same-document (SPA/PJAX)
     navigations: runs update() inside document.startViewTransition when
     available and motion is allowed, otherwise calls update() directly. The
     same ::view-transition-* CSS applies. Your router still owns
     document.title, focus (move it to the new <h1> or <main>) and scroll
     restoration on Back (usability-a11y-perf.md 3.4). Same-document View
     Transitions are Baseline (Firefox 144+).
   Fallback behaviour
     No cross-document support (Firefox): the events never fire, and the browser
     navigates normally. Reduced motion (OS or <html data-motion="reduce">): the
     transition is skipped, so the navigation is instant. No Navigation API:
     the destination comes from the last clicked link and the origin from
     document.referrer; direction defaults to forward.
   Tested against
     Chromium 145 (Playwright 1.58), 2026-09-24: shared element named on both
     sides, "back" type on traversal, reduced-motion skip. Safari 18.2+ not run.
   ========================================================================== */
(function () {
  'use strict';
  var root = document.documentElement;

  function reduced() {
    return root.getAttribute('data-motion') === 'reduce' ||
      (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function pageKey(url) {
    try { var u = new URL(url, location.href); return u.origin + u.pathname; } catch (e) { return ''; }
  }

  // Name the shared elements that pair with `otherUrl`; returns them so they can be cleared.
  function nameShared(otherUrl) {
    var named = [], seen = {};
    var target = pageKey(otherUrl);
    document.querySelectorAll('[data-vt-share]').forEach(function (el) {
      var name = el.getAttribute('data-vt-share');
      var link = el.getAttribute('data-vt-href') || (el.closest('a[href]') || {}).href;
      if (!name || seen[name]) return;
      if (link && pageKey(link) !== target) return;
      seen[name] = true;
      el.style.viewTransitionName = name;
      named.push(el);
    });
    return named;
  }

  function clearOnFinish(vt, named) {
    vt.finished.finally(function () {
      named.forEach(function (el) { el.style.viewTransitionName = ''; });
    });
  }

  // Fallback for engines without NavigationActivation: remember the last same-page link click.
  var lastClicked = null;
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (a) lastClicked = a.href;
  }, true);

  addEventListener('pageswap', function (e) {
    if (!e.viewTransition) return;
    if (reduced()) { e.viewTransition.skipTransition(); return; }
    var dest = (e.activation && e.activation.entry && e.activation.entry.url) || lastClicked;
    if (dest) clearOnFinish(e.viewTransition, nameShared(dest));
  });

  addEventListener('pagereveal', function (e) {
    if (!e.viewTransition) return;
    if (reduced()) { e.viewTransition.skipTransition(); return; }
    var act = window.navigation && navigation.activation;
    var from = (act && act.from && act.from.url) || document.referrer;
    var back = act && act.navigationType === 'traverse' && act.from && act.entry && act.entry.index < act.from.index;
    if (back && e.viewTransition.types) e.viewTransition.types.add('back');
    if (from) clearOnFinish(e.viewTransition, nameShared(from));
  });

  // Same-document helper for SPAs / PJAX routers.
  function swap(update, opts) {
    var types = (opts && opts.types) || [];
    if (typeof document.startViewTransition !== 'function' || reduced()) {
      return Promise.resolve().then(update);
    }
    var vt;
    try { vt = document.startViewTransition({ update: update, types: types }); } // Chrome 125+, Safari 18.2+, Firefox 147+
    catch (err) { vt = document.startViewTransition(update); }                    // older engines: callback form only
    return vt.finished;
  }

  window.pageTransitions = { swap: swap, nameShared: nameShared };
})();
