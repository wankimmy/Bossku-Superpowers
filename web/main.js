// Progressive enhancement only: without this file (or with the CDN blocked) every panel shows as a list,
// the globes stay blank, the check marks are static SVG and nothing is hidden.
(() => {
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  const gsap = window.gsap;
  const still = () => motion.matches || !gsap;

  // ---------- The skill globe: one dot per skill (258 listed, 416 in the library) ----------
  const TOTAL = 674, LISTED = 258;
  const hash = (s) => { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
  const golden = Math.PI * (3 - Math.sqrt(5));
  const POINTS = Array.from({ length: TOTAL }, (_, i) => {
    const y = 1 - (i / (TOTAL - 1)) * 2, r = Math.sqrt(1 - y * y), t = golden * i;
    return { x: Math.cos(t) * r, y, z: Math.sin(t) * r, listed: (i * LISTED) % TOTAL < LISTED };
  });
  let paused = false;

  class Globe {
    constructor(el, dark) {
      this.el = el; this.canvas = el.querySelector("canvas"); this.ctx = this.canvas.getContext("2d");
      this.dark = dark; this.yaw = 0.6; this.pitch = -0.32; this.dim = 0; this.lit = null; this.label = "";
      this.visible = true; this.target = null; this.spin = 0;
      new ResizeObserver(() => { this.resize(); this.draw(); }).observe(this.canvas);
      new IntersectionObserver(([e]) => { this.visible = e.isIntersecting; }).observe(this.canvas);
      this.resize();
    }
    resize() {
      const r = this.canvas.getBoundingClientRect();
      this.dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.w = r.width; this.h = r.height;
      this.canvas.width = Math.max(1, Math.round(r.width * this.dpr));
      this.canvas.height = Math.max(1, Math.round(r.height * this.dpr));
    }
    setSkill(id) { this.lit = id ? hash(id) % TOTAL : null; this.label = id || ""; }
    frontYaw() {
      const p = POINTS[this.lit], phi = Math.atan2(p.z, p.x);
      let t = phi - Math.PI / 2;
      return t + 2 * Math.PI * Math.round((this.yaw - t) / (2 * Math.PI));
    }
    draw() {
      const { ctx, w, h } = this;
      if (!w || !h) return;
      const css = getComputedStyle(document.documentElement);
      const col = (n) => css.getPropertyValue(n).trim();
      const ink = col(this.dark ? "--night-ink" : "--ink"), soft = col(this.dark ? "--night-muted" : "--muted");
      const hot = col(this.dark ? "--night-accent" : "--accent");
      ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      const cx = w / 2, cy = h / 2, R = Math.min(w, h) * 0.42, f = 3.2;
      const cyw = Math.cos(this.yaw), syw = Math.sin(this.yaw), cp = Math.cos(this.pitch), sp = Math.sin(this.pitch);
      const fade = 1 - this.dim * 0.7;
      let litPos = null;
      POINTS.forEach((p, i) => {
        const x1 = p.x * cyw + p.z * syw, z1 = -p.x * syw + p.z * cyw;
        const y1 = p.y * cp - z1 * sp, z2 = p.y * sp + z1 * cp;
        const s = f / (f - z2), px = cx + x1 * R * s, py = cy - y1 * R * s, depth = (z2 + 1) / 2;
        if (i === this.lit) { litPos = { px, py, z2, s }; return; }
        const size = (p.listed ? 3.2 : 2) * s;
        ctx.globalAlpha = (0.18 + 0.82 * depth) * (p.listed ? 1 : 0.75) * fade;
        ctx.fillStyle = p.listed ? ink : soft;
        ctx.fillRect(px - size / 2, py - size / 2, size, size);
      });
      ctx.globalAlpha = 1;
      if (!litPos) return;
      const front = Math.max(0, Math.min(1, (litPos.z2 + 0.2) / 0.9));
      const k = 6 + 4 * front;
      ctx.fillStyle = hot; ctx.globalAlpha = 0.35 + 0.65 * front;
      ctx.fillRect(litPos.px - k / 2, litPos.py - k / 2, k, k);
      if (front > 0.4) {
        ctx.globalAlpha = front;
        ctx.strokeStyle = hot; ctx.lineWidth = 1.5;
        ctx.strokeRect(litPos.px - k - 5, litPos.py - k - 5, 2 * k + 10, 2 * k + 10);
        const t = this.leaderTarget();
        if (t) {
          ctx.beginPath(); ctx.moveTo(litPos.px + k + 5, litPos.py);
          ctx.lineTo(t.x - 24, litPos.py); ctx.lineTo(t.x, t.y); ctx.stroke();
        } else if (this.label) {
          ctx.font = "600 13px " + col("--mono");
          ctx.fillStyle = hot;
          const tw = ctx.measureText(this.label).width;
          const lx = this.labelLeft ? litPos.px - k - 12 - tw : Math.min(litPos.px + k + 12, w - tw - 4);
          ctx.fillText(this.label, lx, litPos.py + 4);
        }
      }
      ctx.globalAlpha = 1;
    }
    leaderTarget() {
      if (!this.target) return null;
      const c = this.canvas.getBoundingClientRect(), r = this.target.getBoundingClientRect();
      const x = r.left - c.left, y = r.top - c.top + 28;
      return x > 0 && x < c.width && y > 0 && y < c.height ? { x, y } : null;
    }
  }

  const heroEl = document.querySelector('[data-globe="hero"]');
  const termEl = document.querySelector('[data-globe="term"]');
  const hero = heroEl && new Globe(heroEl, false);
  const term = termEl && new Globe(termEl, true);
  if (term) term.labelLeft = true; // the right half of this globe is cropped by the terminal edge
  if (hero) {
    hero.setSkill(heroEl.dataset.skill);
    hero.target = document.querySelector(".hero__stamp");
    hero.yaw = hero.frontYaw();
    hero.draw();
  }

  // The hero loop: spin, then the router "picks" the lit skill and brings it to the front, then hold.
  let heroLoop = null;
  const startHero = () => {
    if (!hero || still()) return;
    heroLoop = gsap.timeline({ repeat: -1, repeatRefresh: true, delay: 1.6 })
      .to(hero, { yaw: "+=2.4", duration: 7, ease: "sine.inOut" })
      .to(hero, { yaw: () => hero.frontYaw(), duration: 1.6, ease: "expo.out" })
      .to({}, { duration: 3.2 });
  };
  if (gsap) {
    gsap.ticker.add(() => {
      if (paused || motion.matches) return;
      if (hero && hero.visible) hero.draw();
      if (term && term.visible) term.draw();
    });
  }
  const pauseBtn = heroEl && heroEl.querySelector(".globe__pause");
  const syncMotion = () => {
    if (heroLoop) { heroLoop.kill(); heroLoop = null; }
    if (hero) { hero.yaw = hero.frontYaw(); hero.draw(); }
    if (pauseBtn) pauseBtn.hidden = still();
    if (!paused) startHero();
  };
  if (pauseBtn) {
    pauseBtn.addEventListener("click", () => {
      paused = !paused;
      pauseBtn.setAttribute("aria-pressed", String(paused));
      pauseBtn.textContent = paused ? "Play motion" : "Pause motion";
      if (heroLoop) paused ? heroLoop.pause() : heroLoop.resume();
    });
  }
  // Drag to turn the hero globe, mouse only, so touch scrolling is never captured.
  if (hero) {
    let drag = null;
    hero.canvas.addEventListener("pointerdown", (e) => {
      if (e.pointerType !== "mouse" || still()) return;
      drag = { x: e.clientX, y: e.clientY, yaw: hero.yaw, pitch: hero.pitch };
      if (heroLoop) heroLoop.pause();
      hero.canvas.setPointerCapture(e.pointerId);
    });
    hero.canvas.addEventListener("pointermove", (e) => {
      if (!drag) return;
      hero.yaw = drag.yaw + (e.clientX - drag.x) * 0.008;
      hero.pitch = Math.max(-1.1, Math.min(1.1, drag.pitch + (e.clientY - drag.y) * 0.006));
    });
    const end = () => { if (!drag) return; drag = null; gsap.to(hero, { pitch: -0.32, duration: 1, ease: "expo.out" }); if (heroLoop && !paused) heroLoop.resume(); };
    hero.canvas.addEventListener("pointerup", end);
    hero.canvas.addEventListener("pointercancel", end);
  }

  // ---------- "One turn, checked": two groups of tabs share one terminal ----------
  const root = document.querySelector("[data-tabs]");
  if (root) {
    const termBox = root.querySelector(".term");
    const tabs = [...root.querySelectorAll("[data-tab]")];
    const panels = tabs.map((tab) => document.getElementById(tab.dataset.tab));

    root.querySelectorAll("[data-tablist]").forEach((list) => {
      list.setAttribute("role", "tablist");
      list.setAttribute("aria-orientation", "vertical");
    });
    tabs.forEach((tab, i) => {
      tab.id = `${tab.dataset.tab}-tab`;
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-controls", panels[i].id);
      panels[i].setAttribute("role", "tabpanel");
      panels[i].setAttribute("aria-labelledby", tab.id);
      panels[i].tabIndex = 0;
    });
    termBox.removeAttribute("aria-live");
    termBox.dataset.ready = "";

    const pointGlobe = (skill) => {
      if (!term) return;
      term.setSkill(skill);
      if (still()) { term.dim = skill ? 0 : 1; if (skill) term.yaw = term.frontYaw(); term.draw(); return; }
      gsap.to(term, { dim: skill ? 0 : 1, yaw: skill ? term.frontYaw() : term.yaw + 1.2, duration: 1.4, ease: "expo.out" });
    };

    const select = (i, focus) => {
      tabs.forEach((tab, j) => {
        const on = i === j;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
        panels[j].classList.remove("is-new");
      });
      if (!motion.matches) {
        void panels[i].offsetWidth; // restart the panel animation
        panels[i].classList.add("is-new");
      }
      pointGlobe(tabs[i].dataset.skill);
      if (focus) tabs[i].focus();
    };

    tabs.forEach((tab, i) => {
      tab.addEventListener("click", () => {
        select(i, false);
        // On a phone the terminal sits below the list: bring it into view.
        if (termBox.getBoundingClientRect().top > innerHeight * 0.6) {
          termBox.scrollIntoView({ block: "nearest", behavior: motion.matches ? "auto" : "smooth" });
        }
      });
      tab.addEventListener("keydown", (e) => {
        const step = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (step) { e.preventDefault(); select((i + step + tabs.length) % tabs.length, true); }
        else if (e.key === "Home") { e.preventDefault(); select(0, true); }
        else if (e.key === "End") { e.preventDefault(); select(tabs.length - 1, true); }
      });
    });
    select(0, false);
    panels[0].classList.remove("is-new");
    if (term) { term.dim = 0; term.yaw = term.frontYaw(); term.draw(); }
  }

  // ---------- Copy buttons stay hidden unless the clipboard is there to use ----------
  if (navigator.clipboard) {
    document.querySelectorAll(".copy").forEach((btn) => {
      btn.hidden = false;
      btn.addEventListener("click", async () => {
        const text = btn.parentElement.querySelector("code").textContent;
        try {
          await navigator.clipboard.writeText(text);
          btn.textContent = "Copied";
        } catch {
          btn.textContent = "Select it";
        }
        setTimeout(() => { btn.textContent = "Copy"; }, 1600);
      });
    });
  }

  // ---------- Lottie check: a square, then the tick (the inline SVG stays if Lottie is blocked) ----------
  const tween = (t0, t1) => ({ a: 1, k: [{ i: { x: [0.16], y: [1] }, o: { x: [0.3], y: [0] }, t: t0, s: [0] }, { t: t1, s: [100] }] });
  const still0 = (v) => ({ a: 0, k: v });
  const group = (verts, closed, rgb, width, t0, t1) => ({
    ty: "gr", it: [
      { ty: "sh", ks: still0({ i: verts.map(() => [0, 0]), o: verts.map(() => [0, 0]), v: verts, c: closed }) },
      { ty: "tm", s: still0(0), e: tween(t0, t1), o: still0(0), m: 1 },
      { ty: "st", c: still0([...rgb, 1]), o: still0(100), w: still0(width), lc: 2, lj: 2, ml: 4 },
      { ty: "tr", p: still0([0, 0]), a: still0([0, 0]), s: still0([100, 100]), r: still0(0), o: still0(100), sk: still0(0), sa: still0(0) },
    ],
  });
  const CHECK = {
    v: "5.12.2", fr: 60, ip: 0, op: 60, w: 96, h: 96, nm: "check", ddd: 0, assets: [],
    layers: [{
      ddd: 0, ind: 1, ty: 4, nm: "mark", sr: 1, ao: 0, ip: 0, op: 60, st: 0, bm: 0,
      ks: { o: still0(100), r: still0(0), p: still0([0, 0, 0]), a: still0([0, 0, 0]), s: still0([100, 100, 100]) },
      shapes: [
        group([[8, 8], [88, 8], [88, 88], [8, 88]], true, [0.086, 0.094, 0.106], 4, 0, 28),
        group([[28, 50], [42, 64], [70, 34]], false, [0.706, 0.082, 0.18], 8, 18, 48),
      ],
    }],
  };
  const ticks = [];
  if (window.lottie) {
    document.querySelectorAll("[data-lottie]").forEach((box) => {
      box.textContent = "";
      const anim = window.lottie.loadAnimation({ container: box, renderer: "svg", loop: false, autoplay: false, animationData: JSON.parse(JSON.stringify(CHECK)) });
      ticks.push({ box, anim });
    });
    const finish = () => ticks.forEach(({ anim }) => anim.goToAndStop(59, true));
    if (still()) finish();
    else {
      const io = new IntersectionObserver((entries) => entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const t = ticks.find((x) => x.box === e.target);
        if (t) t.anim.goToAndPlay(0, true);
        io.unobserve(e.target);
      }), { rootMargin: "0px 0px -15% 0px" });
      ticks.forEach(({ box }) => io.observe(box));
    }
    motion.addEventListener("change", () => { if (motion.matches) finish(); });
  }

  // ---------- Page choreography: GSAP + ScrollTrigger, full motion only ----------
  if (gsap && window.ScrollTrigger) {
    gsap.registerPlugin(window.ScrollTrigger);
    const mm = gsap.matchMedia();
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      // World first, type second, chrome last.
      const intro = gsap.timeline({ defaults: { ease: "expo.out" } })
        .from(".hero__globe canvas", { opacity: 0, scale: 0.86, duration: 1.4 }, 0)
        .from(".hero__title .line > span", { yPercent: 110, duration: 1, stagger: 0.07 }, 0.15)
        .from(".hero__works, .hero__lead, .hero__cta, .globe__key", { y: 16, opacity: 0, duration: 0.8, stagger: 0.06 }, 0.45)
        .from(".hero__stamp", { y: 24, opacity: 0, duration: 0.8 }, 0.7)
        .from(".nav", { opacity: 0, duration: 0.6 }, 0.85);

      const rise = (sel, extra = {}) => gsap.utils.toArray(sel).forEach((el) => gsap.from(el, {
        y: 28, opacity: 0, duration: 1, ease: "expo.out", ...extra,
        scrollTrigger: { trigger: el, start: "top 88%", once: true },
      }));
      rise(".flow__head, .try__head, .overlap__head, .proof__head, .new__head, .install__head, .overlap__table tr, .proof__cell, .new article, .steps li, .flow__steps li");
      gsap.utils.toArray(".usp li").forEach((li) => {
        const tl = gsap.timeline({ scrollTrigger: { trigger: li, start: "top 85%", once: true }, defaults: { ease: "expo.out" } });
        tl.from(li.querySelector(".usp__word"), { yPercent: 40, opacity: 0, duration: 1.1 })
          .from(li.querySelector("div"), { y: 20, opacity: 0, duration: 0.9 }, 0.15);
      });

      // The flow diagram draws as you scroll through it.
      gsap.utils.toArray(".flow__svg").forEach((svg) => {
        const rail = svg.querySelector(".flow__rail");
        const len = rail.getTotalLength();
        gsap.set(rail, { strokeDasharray: len, strokeDashoffset: len });
        gsap.timeline({ scrollTrigger: { trigger: svg, start: "top 80%", end: "bottom 55%", scrub: 0.6 } })
          .to(rail, { strokeDashoffset: 0, ease: "none", duration: 1 }, 0)
          .from(svg.querySelectorAll(".flow__node"), { opacity: 0, y: 12, stagger: 0.18, duration: 0.3, ease: "power2.out" }, 0)
          .from(svg.querySelectorAll(".flow__loop, .flow__arrow, .flow__tag"), { opacity: 0, duration: 0.25 }, 0.6)
          .from(svg.querySelectorAll(".flow__back, .flow__tag--muted, .flow__arrow--muted"), { opacity: 0, duration: 0.25 }, 0.85);
      });

      gsap.utils.toArray(".bars__row").forEach((row) => {
        gsap.from(row.querySelectorAll(".bar"), {
          scaleX: 0, duration: 1.2, stagger: 0.08, ease: "expo.out",
          scrollTrigger: { trigger: row, start: "top 85%", once: true },
        });
      });
      gsap.from(".foot__line", { yPercent: 40, opacity: 0, duration: 1.2, ease: "expo.out", scrollTrigger: { trigger: ".foot", start: "top 85%", once: true } });

      // Safety net: if the clock never ticks (a frozen or prerendered tab), show the end state, never hidden text.
      const frame0 = gsap.ticker.frame;
      const net = setTimeout(() => {
        if (gsap.ticker.frame - frame0 > 2) return;
        intro.progress(1);
        window.ScrollTrigger.getAll().forEach((st) => st.animation && st.animation.progress(1));
      }, 1500);
      return () => clearTimeout(net);
    });
  }

  syncMotion();
  motion.addEventListener("change", syncMotion);
})();
