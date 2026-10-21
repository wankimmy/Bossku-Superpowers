# Awwwards editorial: what the jury rewards, and where taste is heading

Last updated: 2026-09-24

Scope: how Awwwards scores sites, what the last three Sites of the Year actually did, what separates the top tiers from an Honorable Mention, where 2025-2026 taste is moving, and which studios keep winning. Written for an agent that will build sites, so every section ends in decisions.

Evidence labels used below:

- **[doc]** documented by Awwwards on its own pages (read 2026-09-24).
- **[obs]** observed by this research in Awwwards' public data: per-site score pages and award listings fetched with curl on 2026-09-24 and parsed locally. Scratch data and parsers live in `evidence/editorial/`.
- **[sec]** secondary: practitioner posts, studio case studies, press, third-party scans. Treated as claims, not facts.

---

## 0. Decision rules for the building agent (read this first)

1. **Optimise for the floor, not the ceiling.** The published score is a plain weighted mean, 0.40 Design + 0.30 Usability + 0.20 Creativity + 0.10 Content, of the trimmed jury average (verified to two decimals on 9 of 9 annual winners, section 1.2). Across all 28 SOTM and annual-winner score pages sampled, **Usability was the lowest sub-score on 27** (section 3.1). The easiest points left on the table are Usability points.
2. **One owned idea, rendered live.** Every recent Site of the Year is one concept embodied in one object or world the visitor can touch: a helmet (Lando Norris), a tiny planet (Messenger), ice-encased projects (Igloo Inc), an astronaut flying through portals (Lusion v3). The object is rendered in real time, not played back as video.
3. **Performance is part of the art.** The Developer SOTY winners scored 8.0 to 9.0 on WPO while shipping full 3D. Messenger publicly loads about 5.7 MB up front ([webgpu.com showcase](https://www.webgpu.com/showcase/messenger/), [sec]). Budget before you design the signature moment.
4. **Accessibility, semantics and markup are where even winners lose.** On the Developer Award breakdown, Accessibility is the lowest sub-score on 18 of 28 top-tier pages and Markup or Semantics on 8 more (section 3.1). Doing them properly is cheap differentiation.
5. **Content is scored, and brand-real content wins.** Winners carry real products, real people, real stories (race calendar and store, a portfolio company roster, a playable game). No template demos: Awwwards does not accept sites built from pre-made templates ([FAQ](https://www.awwwards.com/faqs/), [doc]).
6. **House law beats award habit.** Several award-site staples are slop tells under this repo's design law (section 3.4). Build the crafted version, not the habit.

---

## 1. The scoring system, and what each criterion means in practice

### 1.1 The pipeline [doc]

| Stage | Rule | Source |
|---|---|---|
| Submission | Manual approval, can take up to a week. Pre-made templates are rejected; template demos built entirely by the submitter are accepted. | [Evaluation](https://www.awwwards.com/about-evaluation/), [FAQ](https://www.awwwards.com/faqs/) |
| Jury vote | Sent to at least **18 jurors**; the **3 scores furthest from the average are dropped automatically**. Voting lasts **5 days**; a site with a high jury score and at least 10 PRO-user votes can win SOTD early. | [Evaluation](https://www.awwwards.com/about-evaluation/) |
| Community vote | Only validated users count. Chief, Pro and Jury votes count toward SOTD and HM; Tribe (basic) users do not. | [Status system](https://www.awwwards.com/about-status/) |
| Honorable Mention | Jury score **6.5 or more** AND users' score 6.5 or more; the two votes run separately. | [Evaluation](https://www.awwwards.com/about-evaluation/), [FAQ](https://www.awwwards.com/faqs/) |
| Site of the Day | Highest jury score of the day. Jury scores are only published for SOTD winners. A site stays eligible for SOTD for 3 months after approval. | [Evaluation](https://www.awwwards.com/about-evaluation/), [FAQ](https://www.awwwards.com/faqs/), [Terms](https://www.awwwards.com/terms/) |
| Developer Award | Every SOTD goes to a separate developer jury; **score above 7** wins it. | [Evaluation](https://www.awwwards.com/about-evaluation/), [Developer Award](https://www.awwwards.com/developer-award/) |
| Site of the Month | The **8 highest-scoring sites** of the month are re-reviewed by the jury; the site with most user votes carries extra weight in the jury's decision. | [Evaluation](https://www.awwwards.com/about-evaluation/) |
| Site of the Year | All SOTMs are auto-nominated plus some Awwwards favourites; winner announced in February of the following year. | [Evaluation](https://www.awwwards.com/about-evaluation/) |
| Honors | Six category awards (Typography, No-code, E-commerce, Product, Portfolio, Business & Services); the **top 20 highest-rated projects per category**, SOTD or not, are nominated. | [Honors about](https://www.awwwards.com/honors/about) |

Selectivity, as displayed in the site navigation on 2026-09-24 [obs]: Nominees 48K, Honorable Mentions 25K, Sites of the Day 6,472, Sites of the Month 196, Sites of the Year 64 ([listing nav](https://www.awwwards.com/websites/sites_of_the_year/)). Roughly one in seven nominees becomes SOTD and about one in 33 SOTDs becomes SOTM.

The annual vote is a plurality among roughly 30 nominees per category ([Stefano Bartoletti's scan of the 30 SOTY 2025 nominees](https://www.linkedin.com/posts/stefanobartoletti_awwwards-2025-soty-nominees-tech-overview-activity-7417862429986152448-eU1Y), [sec]; nominee voting ran 12 to 22 January 2026 per [Awwwards' own post](https://www.facebook.com/awwwards/posts/check-out-the-best-of-the-web-2025-the-nominees-for-the-annual-awwwards-are-now-/1193695102880006/)). Winning jury shares [doc]:

| Award | Winner | Jury votes |
|---|---|---|
| SOTY 2025 | Lando Norris | [43 of 253](https://www.awwwards.com/annual-awards-2025/site-of-the-year) (17%) |
| Developer SOTY 2025 | Messenger | [54 of 180](https://www.awwwards.com/annual-awards-2025/developer-site-of-the-year) (30%) |
| SOTY 2024 | Igloo Inc | [43 of 309](https://www.awwwards.com/annual-awards-2024/site-of-the-year) (14%) |
| Developer SOTY 2024 | Igloo Inc | [87 of 286](https://www.awwwards.com/annual-awards-2024/developer-site-of-the-year) (30%) |
| SOTY 2023 | Lusion v3 | [70 of 233](https://www.awwwards.com/annual-awards-2023/site-of-the-year) (30%) |

Consequence: SOTY is won by the site the largest bloc of jurors agrees on, not by the most polarising one. The 3-outlier trim on daily scores pushes the same way.

### 1.2 The math, verified [obs]

The published SOTD score is **only the jury's weighted mean**; the "Pro and Chief" community score is displayed separately and is not blended in. Recomputing `0.4·D + 0.3·U + 0.2·Cr + 0.1·Co` from the published sub-scores reproduces the published total on all 9 annual-winner pages sampled (for example Lando Norris: 0.4·8.12 + 0.3·7.90 + 0.2·8.71 + 0.1·8.18 = 8.178, published 8.18; [page](https://www.awwwards.com/sites/lando-norris)). Community scores ran 0 to 2.2 points above the jury score, +1.0 on average, across the 28 top-tier pages (Messenger: jury 7.92, community 9.56; [page](https://www.awwwards.com/sites/messenger)). Do not calibrate against community enthusiasm.

The Developer Award total likewise equals the documented weights exactly (Igloo Inc: 0.2·WPO 8.0 + 0.2·RWD 8.4 + 0.15·Markup 6.4 + 0.2·Semantics 6.6 + 0.15·Animations 9.6 + 0.1·Accessibility 6.6 = 7.66, published 7.66; [page](https://www.awwwards.com/sites/igloo-inc)).

A practitioner post claims SOTD usually takes a score in the mid-to-high 8s ([hontran.dev, 2026-07-22](https://www.hontran.dev/blog/awwwards-judging-criteria), [sec]). The data disagrees: annual winners won their SOTD with 7.52 to 8.25, and all 28 top-tier pages sit between 7.51 and 8.25 (sections 2.2 and 3.1). A jury average of about 7.5 to 8.3 is SOTD-and-above territory.

### 1.3 What each criterion means in practice

Awwwards names the four criteria and their weights but publishes no rubric text for them ([Evaluation](https://www.awwwards.com/about-evaluation/), [Terms](https://www.awwwards.com/terms/)). The definitions below combine the Developer Guidelines (which the dev jury does publish), the observed sub-score patterns, and juror-attributed commentary. Where a line rests on secondary commentary it is marked.

**Design, 40%.** Art direction as a system: type, colour, composition, hierarchy and consistency across every page, not just the hero. Annual winners land Design 7.73 to 8.26; it is never their weakest criterion and is the strongest on 3 of 9 (7 of the 28 top-tier pages) [obs]. It is the steady base. Winners use tiny palettes: the palette recorded on each Awwwards page lists 2 colours for Lando Norris (#D2FF00, #111112), Messenger, Igloo, Lusion, Opal, Mana, Scout Motors and Don't Board Me, and 1 for Noomo [obs]. A self-described juror writes that copying the season's trend board costs points fast, naming the ubiquitous horizontal-scroll gallery as the example ([hontran.dev, 2026-06-27](https://www.hontran.dev/blog/how-to-win-an-awwwards-site-of-the-day), [sec]).

**Usability, 30%.** Can a stranger orient, move and leave without friction, on a laptop and a mid-range phone. In practice this is navigation clarity, load and input responsiveness, frame-rate stability, mobile parity, and an accessibility floor (focus states, reduced-motion path, contrast). It is the lowest sub-score for 8 of 9 annual winners (range 7.27 to 7.95) and for 27 of the 28 top-tier pages [obs], so the jury is visibly marking down even the best immersive sites here. The 2024 SOTY jury quote singles out Igloo for pairing an immersive 3D experience with easy scroll navigation, which it says few sites achieve ([SOTY 2024 page](https://www.awwwards.com/annual-awards-2024/site-of-the-year), [doc]). Practitioner jurors name jank, broken mobile, long progress-bar preloaders and cursor replacements as the common penalties ([hontran.dev](https://www.hontran.dev/blog/how-to-win-an-awwwards-site-of-the-day), [sec]). An independent critique notes SOTMs are "rarely navigable with a keyboard" ([trost.codes](https://trost.codes/posts/accessible-awwwards/), undated, [sec]), which matches the low Accessibility sub-scores below.

**Creativity, 20%.** Originality of concept and of the interaction that expresses it. It is the top sub-score for 6 of 9 annual winners (Lando 8.71, Lusion 8.65, Mana 8.45, Igloo 8.31, Messenger 8.23) and 19 of the 28 top-tier pages [obs]. The one exception with low Creativity (Opal Tadpole, 7.27) won E-commerce of the Year on product clarity instead. Creativity is scored on the idea, not on the amount of WebGL: Don't Board Me, a 2D graphic storytelling site, scored Creativity 8.0 and won the 2024 Users' Choice ([page](https://www.awwwards.com/sites/dont-board-me), [obs]).

**Content, 10%.** Quality and fit of copy, imagery, video and sound, and whether they serve the concept. Winners' Content scores (7.64 to 8.38) track close to Design [obs]. What scores: authored words and commissioned imagery made with the design (Messenger's characters and story, Lando's race calendar and helmet archive, Igloo's portfolio companies). What loses: stock imagery, lorem ipsum, and a beautiful shell around thin copy ([hontran.dev](https://www.hontran.dev/blog/awwwards-judging-criteria), [sec]). Awwwards also scores the submission itself: thumbnails are 1600×1200 and Awwwards strongly recommends adding videos ([FAQ](https://www.awwwards.com/faqs/), [doc]). Site pages show jurors a desktop and a mobile thumbnail side by side [obs], so the mobile composition is part of the first impression.

### 1.4 The Developer Award [doc] and what it rewards in practice [obs]

The published [Developer Guidelines](https://docs.google.com/document/d/1Gvmg6Z60UQ-4BOM3XyUcBKvq2shd4J-l_MoXT26JFEg/) (Google Doc, linked from the [Developer Award page](https://www.awwwards.com/developer-award/); it announces a revision co-authored by developers from Ingamana, Darkroom, Unseen, Antinomy and others, with no date on the doc) weight six categories:

| Category | Weight | What the checklist asks for (condensed) |
|---|---|---|
| WPO | 0.20 | Critical rendering path, deferred/async JS, above-the-fold priority, compressed and responsive media, CDN and caching, few third parties, no console errors, HTTP/2 and HTTPS, cross-browser |
| RWD / Mobile | 0.20 | Fluid grid, flexible media, responsive type, correct viewport, feature detection, retina assets, proper tap targets, input methods (click, swipe, pinch) |
| Markup / Metadata | 0.15 | Valid HTML, sectioning model, meta, Open Graph and Schema.org, image alt/width/height, no div-soup, favicon set |
| Semantics / SEO | 0.20 | Unique per-page titles and descriptions, clean URLs, heading hierarchy, canonicals, sitemaps, text links (HTML links over JS), no broken links |
| Animations / Transitions | 0.15 | Smooth stable frame rate, easing and rhythm, consistency, GPU and memory hygiene, page transitions with history and a friendly loading UI. Real-time animation only; video and image sequences do not count. |
| Accessibility | 0.10 | Keyboard operable, visible focus, labelled controls, no information only on hover, captions for video, pause control for anything auto-playing more than 5 seconds, **content accessible with no CSS and with no JS**, ARIA where custom widgets exist |

Observed on the 9 annual winners [obs]: **Animations** is the highest dev sub-score almost everywhere (Lusion 10.00, Igloo 9.60, Mana 9.20, Messenger 9.00, Lando 8.60), while **Accessibility, Markup and Semantics** are the lowest (Igloo: 6.60 / 6.40 / 6.60; Lando: 7.00 / 7.40 / 7.40). Igloo still won Developer SOTY 2024. Read that as: the developer jury currently rewards real-time craft and performance first. The 60% of the weight in WPO, RWD and Semantics is where a technically solid build can out-score flashier rivals.

Build checklist distilled for the agent:

- Server-render all copy and navigation as real HTML; WebGL layers decorate, they do not own the text. Igloo and Messenger render UI text in WebGL for effect, and their semantics scores show the cost.
- Every route has its own title, description, canonical and OG image; links are `<a href>`.
- Give the canvas an accessible name or `aria-hidden="true"`, and mirror interactive 3D choices in DOM controls.
- `prefers-reduced-motion` path that is a designed state, not a disabled one.
- Pause and dispose off-screen WebGL; cap device pixel ratio on phones.
- No console errors at submission.

### 1.5 Mobile Excellence: legacy [doc], current status unverified

The Mobile Excellence Award launched with Google in 2017 with a 75/100 threshold ([announcement, 2017-09-07](https://www.awwwards.com/google-and-awwwards-present-the-mobile-excellence-award.html)), lowered to 70/100 in version 2 ([2018-10-30](https://www.awwwards.com/update-version-2-of-the-google-awwwards-mobile-excellence-award.html)), with a checklist PDF built on Google's speed and mobile-friendliness criteria ([guidelines PDF](https://www.awwwards.com/mobile-excellence-guidelines.pdf)). No Mobile Excellence badge or score appears on any of the 28 top-tier score pages or on the evaluation page fetched 2026-09-24 [obs]; the blog still carries a "Mobile Excellence" category. Treat the badge as dormant (unverified). The substance still counts: RWD/Mobile is 20% of the Developer score and jurors see the mobile thumbnail.

---

## 2. Sites of the Year 2023-2025

### 2.1 Winners by category [doc]

From the [Hall of Fame](https://www.awwwards.com/annual-awards/hall-of-fame) (2025), [2024](https://www.awwwards.com/annual-awards/hall-of-fame/2024) and [2023](https://www.awwwards.com/annual-awards/hall-of-fame/2023) pages:

| Category | 2025 (announced Feb 2026) | 2024 | 2023 |
|---|---|---|---|
| Site of the Year | Lando Norris (OFF+BRAND.) | Igloo Inc (abeto) | Lusion v3 (Lusion) |
| Developer Site of the Year | Messenger (abeto) | Igloo Inc (abeto) | Lusion v3 (Lusion) |
| E-commerce of the Year | Scout Motors | Opal Tadpole (Claudio Guglieri, dev Ingamana) | Mana Yerba Mate (Louis Paquet) |
| Users' Choice | Lando Norris | Don't Board Me (The First The Last) | Noomo Agency |
| Agency of the Year | Immersive Garden | Locomotive | Locomotive |
| Studio of the Year | Malvah | Immersive Garden | Obys |
| Independent of the Year | Louis Paquet | Jesper Landberg | Aristide Benoist |

The 2025 result was publicised around 25-26 February 2026 ([Webflow staff post, 2026-02-26](https://www.linkedin.com/posts/jordan-maslyn_super-excited-to-share-that-the-lando-norris-activity-7432823998394134528-l6R-), [sec]).

### 2.2 Scores of the annual winners [obs]

Jury sub-scores are Design / Usability / Creativity / Content. Dev sub-scores are Semantics / Animations / Accessibility / WPO / Responsive / Markup. Lowest jury sub-score in bold.

| Site (award) | SOTD date | Jury | D / U / Cr / Co | Dev | Sem / Anim / A11y / WPO / RWD / Mk | Community |
|---|---|---|---|---|---|---|
| [Lando Norris](https://www.awwwards.com/sites/lando-norris) (SOTY + Users' 2025) | 2025-11-17 | 8.18 | 8.12 / **7.90** / 8.71 / 8.18 | 7.58 | 7.4 / 8.6 / 7.0 / 7.6 / 7.4 / 7.4 | 8.86 |
| [Messenger](https://www.awwwards.com/sites/messenger) (Dev SOTY 2025) | 2025-11-10 | 7.92 | 8.04 / **7.46** / 8.23 / 8.15 | 8.21 | 7.6 / 9.0 / 7.6 / 8.8 / 8.4 / 7.6 | 9.56 |
| [Scout Motors](https://www.awwwards.com/sites/scout-motors) (E-com 2025) | 2025-01-16 | 7.60 | 7.73 / **7.27** / 7.79 / 7.69 | 7.36 | 7.2 / 7.8 / 7.4 / 7.4 / 7.4 / 7.0 | 7.60 |
| [Igloo Inc](https://www.awwwards.com/sites/igloo-inc) (SOTY + Dev 2024) | 2024-07-23 | 7.92 | 8.05 / **7.50** / 8.31 / 7.91 | 7.66 | 6.6 / 9.6 / 6.6 / 8.0 / 8.4 / 6.4 | 8.55 |
| [Don't Board Me](https://www.awwwards.com/sites/dont-board-me) (Users' 2024) | 2024-03-11 | 7.83 | 8.08 / **7.41** / 8.00 / 7.73 | 7.26 | 7.2 / 7.2 / 7.0 / 6.8 / 8.0 / 7.2 | 8.92 |
| [Opal Tadpole](https://www.awwwards.com/sites/opal-tadpole) (E-com 2024) | 2024-01-11 | 7.52 | 7.73 / 7.34 / **7.27** / 7.64 | 7.84 | 7.6 / 8.6 / 7.6 / 7.8 / 8.0 / 7.4 | 8.55 |
| [Lusion v3](https://www.awwwards.com/sites/lusion-v3) (SOTY + Dev 2023) | 2023-10-02 | 8.25 | 8.26 / **7.95** / 8.65 / 8.26 | 8.41 | 7.6 / 10.0 / 7.4 / 9.0 / 8.4 / 7.8 | 9.22 |
| [Noomo Agency](https://www.awwwards.com/sites/noomo-agency) (Users' 2023) | 2023-09-21 | 7.72 | 7.93 / **7.41** / 7.73 / 7.79 | 7.47 | 7.8 / 7.8 / 7.2 / 7.2 / 7.2 / 7.6 | 8.73 |
| [Mana Yerba Mate](https://www.awwwards.com/sites/mana-yerba-mate) (E-com 2023) | 2023-03-13 | 8.03 | 8.06 / **7.61** / 8.45 / 8.38 | 7.80 | 7.6 / 9.2 / 7.4 / 7.8 / 7.6 / 7.2 | 8.90 |

### 2.3 Why each Site of the Year won

**Lando Norris, SOTY 2025 and Users' Choice (OFF+BRAND., Webflow).** A personal site for an F1 driver that treats one owned object, the racing helmet, as the whole interaction language. The hero is a photograph of Norris given depth with a depth map, alpha map and roughness map so it breathes under the cursor, with a real-time 3D helmet revealed through a fluid, cursor-driven mask shader; further down, a glTF helmet spins with scroll and swaps per-season livery textures (colour, metalness, roughness and normal maps), image frames are cut with SVG masks and `clip-path` reveals, and a Rive-animated signature draws itself ([Syntax teardown, 2025-10-23](https://www.youtube.com/watch?v=HzL65tTeANs), [sec]). OFF+BRAND lists the services as Webflow, WebGL, 3D, Rive and motion ([case study](https://www.itsoffbrand.com/our-work/lando-norris), [sec]); Awwwards tags it WebGL, GSAP, 3D, Gestures and Webflow [obs]. It is also a working fan platform with calendar, media and store, which is why Content scored 8.18 rather than a demo's usual dip. The palette is two colours, a fluorescent lime #D2FF00 on near-black #111112 [obs]. Its Creativity 8.71 was the highest sub-score of any annual winner in this sample, and the driver's fanbase plausibly carried the Users' Choice (unverified). Lesson: a celebrity or brand's signature object, rendered live and made touchable, beats a generic "immersive" scene.

**Messenger, Developer SOTY 2025 (abeto).** A free, roughly 15-minute multiplayer browser game on a tiny spherical planet where you walk a teenage courier around to make deliveries ([abeto on Awwwards blog, 2026-01-15](https://www.awwwards.com/messenger.html), [doc]). The team capped rooms at 10 players because more broke the calm mood, limited communication to emoji, automated camera centring so non-gamers could play, rendered the UI in WebGL with GPU text from WebAssembly-generated glyphs, and targeted old phones ([same post](https://www.awwwards.com/messenger.html); [Communication Arts, 2025-12-11](https://www.commarts.com/webpicks/messenger), [sec]). The stack is Three.js with three-mesh-bvh, Houdini and Blender models, and a custom WebSocket back end, loading about 5.7 MB initially and 17.5 MB total ([webgpu.com, 2025-12-22](https://www.webgpu.com/showcase/messenger/), [sec]). It posted the highest community score in this sample (9.56) and WPO 8.8. Lesson: a whole game can win on performance if the budget is the design constraint from day one.

**Igloo Inc, SOTY and Developer SOTY 2024 (abeto with Bureaux).** A three-section corporate landing page for the parent company of Pudgy Penguins, turned into a scroll through a frozen world. Each portfolio company sits inside its own ice block, grown procedurally by a custom crystal-growth algorithm so blocks differ and new ones are cheap to add; the intro is animated in-engine rather than pre-rendered; the footer is a particle simulation whose shapes come from VDB volume data converted by a custom exporter; the UI is WebGL so text scrambles become SDF offset changes instead of DOM relayouts; sound follows particle motion ([abeto case study on Awwwards, 2024-10-31](https://www.awwwards.com/igloo-inc-case-study.html), [doc]). abeto built and profiled directly in the browser to hold frame rate on low-end devices (same source). The jury quote praises combining immersive 3D with easy scroll navigation ([SOTY 2024](https://www.awwwards.com/annual-awards-2024/site-of-the-year)), and the Developer SOTY quote cites fast performance and game-like delight ([Dev SOTY 2024](https://www.awwwards.com/annual-awards-2024/developer-site-of-the-year)). Lesson: a thin brief (three sections) can win if the content itself (the portfolio) becomes the object you scroll through.

**Lusion v3, SOTY and Developer SOTY 2023 (Lusion).** The real-time studio's own portfolio. The signature is an astronaut that travels through portals as you scroll, breaking through glass at the end; scroll back and the journey reverses, press to slow it down; the site uses a FLIP fluid solver, ray marching and ray tracing, and on phones swaps cursor play for accelerometer tilt, with asynchronous loading and compression to keep it fast ([Communication Arts](https://www.commarts.com/project/36283/lusion), [sec]). It scored a perfect 10.00 on Animations and 9.0 on WPO [obs], and won the SOTY jury vote by the widest margin of the three years (70 of 233). The jury quote credits a tasteful balance between current trends and real innovation, and calls it a refreshing take on a portfolio ([SOTY 2023](https://www.awwwards.com/annual-awards-2023/site-of-the-year), [doc]). Lesson: when the work is real-time craft, the portfolio should be a demonstration of that craft, and mobile needs its own input model, not a disabled one.

**The other annual winners, briefly.** Don't Board Me (Users' 2024) proves a flat, colourful 2D storytelling site with a strong voice can beat 3D in the public vote. Opal Tadpole (E-commerce 2024) won on single-page product clarity with photography and micro-interactions despite the lowest Creativity in the set. Mana Yerba Mate (E-commerce 2023, Shopify) paired illustration and 3D with a real store. Scout Motors (E-commerce 2025) is the lowest-scoring winner here (7.60) and the least effect-driven: a brand-launch vehicle site that won its category on commerce fit rather than spectacle.

---

## 3. What separates SOTD, SOTM and SOTY from an Honorable Mention

### 3.1 Score anatomy of the top tier [obs]

Sample: the 28 distinct score pages for every Site of the Month from January 2025 to August 2026 plus the 2023-2025 annual winners, fetched 2026-09-24 (SOTM list from [Sites of the Month](https://www.awwwards.com/websites/sites_of_the_month/); pages such as [Oryzo AI](https://www.awwwards.com/sites/oryzo-ai), [Bruno's Portfolio](https://www.awwwards.com/sites/brunos-portfolio), [GQ & AP](https://www.awwwards.com/sites/gq-ap-the-extraordinary-lab), [Son Daven](https://www.awwwards.com/sites/son-daven)).

| Measure | Result |
|---|---|
| Jury total | median **7.73**, range 7.51 to 8.25 |
| Lowest jury sub-score | **Usability on 27 of 28** (mean 7.45, range 7.12 to 7.95) |
| Highest jury sub-score | Creativity on 19 of 28 (mean 8.05), Design on 7 |
| Design / Content means | 7.91 / 7.86 |
| Developer total | median 7.67, range 7.18 to 8.41 |
| Lowest dev sub-score | **Accessibility on 18 of 28** (mean 7.02, low 6.00 on GQ & AP), then Markup (5) and Semantics (3) |
| Highest dev sub-score | Animations on 24 of 28 (mean 8.59) |
| Community minus jury | +1.0 on average |

A SOTD can win with less: "Ai in Design Report 2026" won SOTD on 2026-08-26 with 7.4 ([page](https://www.awwwards.com/sites/ai-in-design-report-2026), [obs] via search extract). Its sub-scores were 7.66 / 7.21 / 7.14 / 7.38, so Creativity, not Usability, was its weakest. The daily bar floats with the day's competition, roughly 7.4 at the low end, while SOTM winners cluster 7.5 to 8.2. Inference (sub-scores for ordinary SOTDs were not sampled beyond this one): what lifts a site into SOTM is not a higher Usability score, which stays around 7.1 to 7.9 even at the top, but a clearly higher Creativity score on an unbroken Design and Content base.

### 3.2 Tag differentials, SOTD vs Honorable Mention [obs]

Compared: 117 SOTDs from 2026-06-01 to 2026-09-25 against the 139 HM-only sites (no SOTD) on the first six pages of the [Honorable Mentions listing](https://www.awwwards.com/websites/) (2026-08-09 to 2026-09-25). Tags are self-reported by submitters, so read these as tendencies.

| Tag | SOTD | HM only | Reading |
|---|---|---|---|
| WebGL | 42.7% | 16.5% | Real-time graphics is the single largest separator |
| 3D | 40.2% | 23.7% | |
| Three.js | 29.9% | 18.0% | |
| GSAP | 54.7% | 38.1% | Directed, timeline-based motion |
| Technology (category) | 25.6% | 14.4% | Tech and AI companies commissioning ambitious sites |
| Promotional | 13.7% | 2.2% | Campaign microsites with one idea |
| Minimal | 7.7% | 17.3% | Minimalism alone tends to stall at HM |
| Parallax | 6.0% | 11.5% | Parallax as the main effect stalls at HM |
| Illustration / Graphic design | 3.4% / 6.8% | 10.1% / 14.4% | Flat graphic work wins less often now, though it still wins when authored (MindMarket, Don't Board Me) |
| Figma (tagged) | 15.4% | 28.1% | |
| Framer / WordPress / React | 3.4% / 3.4% / 1.7% | 7.9% / 7.9% / 7.9% | Builder- and theme-shaped sites skew HM |
| Webflow | 22.2% | 18.7% | Platform is not the differentiator: Webflow reaches SOTY (Lando Norris) |

Studio maturity also separates the tiers: **84%** of those SOTDs came from PRO accounts (the paid professional plan) versus **39%** of HM-only sites; the PRO share of all SOTDs rose from 58.5% (2023) to 76.8% (2026 to date) [obs]. Treat that as a signal of how much iteration and craft time the winners have, not a pay-to-win claim; PRO votes count the same as Chief votes for SOTD and HM ([status system](https://www.awwwards.com/about-status/)).

### 3.3 Recurring traits of SOTM and SOTY work

Distilled from the 28 score pages above, the studio case studies cited in section 2, and the Awwwards jury quotes:

1. **One idea you can say in a sentence, carried by one object or world.** Helmet, tiny planet, ice blocks, astronaut through portals, a giant sneaker opening a fintech launch ([Razorpay Sprint26, 2026-08-31](https://www.awwwards.com/razorpay-sprint26-the-future-of-payments.html)). Juror-attributed advice matches: one sentence of concept, one signature moment, protect the performance budget around it ([hontran.dev](https://www.hontran.dev/blog/how-to-win-an-awwwards-site-of-the-day), [sec]).
2. **Real time, not playback.** The dev guidelines only count real-time scripted animation, not video or image sequences ([Developer Guidelines](https://docs.google.com/document/d/1Gvmg6Z60UQ-4BOM3XyUcBKvq2shd4J-l_MoXT26JFEg/)). Winners animate intros in-engine (Igloo), render live helmets rather than scrubbed video (Lando), and pre-bake physics into textures only to replay them live (Lusion's 2019 approach, [case study](https://www.awwwards.com/case-study-for-lusion-by-lusion-winner-of-site-of-the-month-may.html)).
3. **Scroll as a single, legible axis.** Winners map scroll to one direction of travel through a scene and cut between scenes like film edits; Forged describes exactly this and sizes each scene in viewport heights to tune pace ([Codrops, 2025-10-20](https://tympanus.net/codrops/2025/10/20/from-garage-to-browser-forged-build-and-the-webgpu-revolution/), [sec]). GQ & AP uses one continuous timeline, scrubbed by scroll or drag, that drives camera, dialogue, sound and UI together ([Immersive Garden on Awwwards, 2026-06-03](https://www.awwwards.com/gq-audemars-piguet-the-extraordinary-lab.html)).
4. **Performance treated as a design constraint.** Build and profile in the browser from day one (abeto), cap players per room to keep the mood and the frame rate (Messenger), ship compressed GPU textures (Bruno Simon's repo compresses GLB textures to KTX2/ETC1S, [folio-2025](https://github.com/brunosimon/folio-2025)).
5. **Mobile gets its own input model.** Accelerometer tilt instead of cursor play (Lusion), automated camera for non-gamers (Messenger), a separate mobile Rive landscape file (Lando, per a public mirror of its assets, [sec](https://github.com/nachitzaid/lando-noris)).
6. **Consistency beyond the homepage.** The 2024 Agency of the Year jury quote praises Locomotive for getting visuals, interactions, usability and performance all right at once ([Agency of the Year 2024](https://www.awwwards.com/annual-awards-2024/agency-of-the-year)). The 404-page tag is three times as common on recent SOTDs as on HM-only sites (10.3% vs 3.6%) [obs]: jurors click past the homepage.
7. **Tiny palettes, owned colour.** Two recorded colours on nearly every page in the sample that records a palette (4 of the 28 record none) [obs]; where a saturated colour appears it is the client's identity colour (Dropbox #0061FE, Lando #D2FF00), not decoration.
8. **Sound at the top tier, not in the middle.** Howler.js appears on 7 of 30 SOTY 2025 nominees ([Bartoletti scan](https://www.linkedin.com/posts/stefanobartoletti_awwwards-2025-soty-nominees-tech-overview-activity-7417862429986152448-eU1Y), [sec]), while the "Sound-Audio" tag sits at 5-8% of all SOTDs every year [obs].

What caps work at Honorable Mention (combining 3.1 and 3.2 with juror commentary [sec]): minimalism or parallax as the whole idea, builder or theme structure a juror recognises, motion with no hierarchy, frame drops, a collapsed phone layout, long progress-bar preloaders, a custom cursor that hides the real one, and thin or stock content ([hontran.dev](https://www.hontran.dev/blog/how-to-win-an-awwwards-site-of-the-day)).

### 3.4 Award habits that break this repo's design law, and the crafted alternative

The house law (`deslop-law.md`) overrides award habit. Several patterns that do appear on winning sites are named slop tells there.

| Award-site habit | Where it shows up | Why the house law rejects it | Build this instead |
|---|---|---|---|
| Content parked at `opacity: 0` until a ScrollTrigger or IntersectionObserver reveal fires | Ubiquitous in GSAP `from()` reveals | Invisible-content trap: if the trigger never fires (background tab, screenshot pass, hydration hiccup, no JS) the section is blank. It also fails the dev guideline that content stay accessible without JS. | Content is visible by default. Animate transform on already-visible elements (a small scrubbed lift or drift), or animate decorative media only. Recipes 6.1 and 6.2. |
| Per-letter roll or underline that grows on hover | Lando Norris text hovers (each letter in a span, staggered up and down, per the [Syntax teardown](https://www.youtube.com/watch?v=HzL65tTeANs)) | Underline-fill hovers are banned outright; letter-roll is the same reflex | A quiet tonal colour shift, or an icon that slides. One state change, no travel. |
| Magnetic buttons and hover lift | Agency portfolios (frequency not measured) | "Hover boop": buttons do not move on hover | Fill or tone change in place. |
| Poster-bright accent on type, dots and buttons | Recorded palettes include #D2FF00 (Lando), #FF8539 (Oryzo AI), #FF6D38 (Navigate) [obs]; how each is applied was not audited | Saturated accent is a slop tell unless it is the brand's owned colour | Tonal accents by default; use a saturated hue only when the client owns it, and then as a field or object colour, not sprayed across labels. |
| Warm cream or bone ground | #F9F4EB Lama Lama, #FAF7EF Siena Film Foundation, #F7F7EE Renaissance Edition [obs] | Cream is the new safe default | Pick a specific ground that belongs to the brand; dark, cool or odd grounds are allowed. |
| Film grain over the whole page | Luxury and film sites (frequency not measured) | Grain over text hurts legibility | Grain on the substrate behind content; at most masked onto one display word. |
| Long preloader with percentage counter | WebGL sites (frequency not measured) | Usability cost (juror commentary) and a blank first frame | Stream the first view as HTML; load heavy scenes after first paint; a branded intro only if it is under about 2 seconds and skippable. |
| Custom cursor replacing the native one | Portfolios (frequency not measured) | Juror-flagged as carelessness; breaks affordance | Keep the native cursor; any follower is decorative, off on touch and under reduced motion. |
| UI text drawn in WebGL | Igloo, Messenger | Costs Semantics and Accessibility (Igloo 6.6 / 6.6) | DOM text is the source of truth; WebGL draws the effect on top or mirrors it, with the DOM copy readable and focusable. |
| Giant footer wordmark pasted in | "Footer Design" tag rising (6.8% in 2023 to 10.5% in 2026) [obs] | Only allowed when composed: centred, uncut, spaced, with a reason | Compose it or skip it. |

---

## 4. 2025-2026 direction: what is rising, what is fading

### 4.1 How to read the tag data [obs]

The trend numbers below come from 1,426 SOTDs from 2022-10-30 to 2026-09-25 parsed from the [Sites of the Day listing](https://www.awwwards.com/websites/sites_of_the_day/). Two cautions:

- Tags are chosen by the submitter.
- **Awwwards changed its tagging in August 2025.** Technology tags (GSAP, WebGL, Three.js, Webflow and so on) appear on 0-16% of SOTDs in every month through July 2025, then on 94-100% from September 2025; mean tags per site rose from about 7.8 to 10. Any "GSAP went from 1% to 50%" reading across that line is an artifact. Technology trends below use only September 2025 to September 2026 (388 SOTDs). Non-technology tags remain comparable across years; the average number of non-technology tags per site fell only slightly (7.5-7.7 to 7.3).

### 4.2 Rising

| Signal | Evidence |
|---|---|
| **Real-time 3D as the dividing line** | WebGL tagged on 28.3% of SOTDs (Sep 2025-Feb 2026) then 39.4% (Mar-Sep 2026); 42.7% of recent SOTDs vs 16.5% of HMs. "3D" steady at 34-40% of SOTDs every year since 2023 [obs]. All three Sites of the Year are real-time 3D. |
| **Worlds and games as websites** | Messenger (Dev SOTY 2025), Bruno Simon's drivable portfolio (SOTM Jan 2026), built on Three.js with TSL so one shader codebase targets WebGPU and WebGL, Rapier physics and a multiplayer message feature called Whispers ([bruno-simon.com](https://bruno-simon.com/), [devlog](https://www.youtube.com/watch?v=OBZtVz6IM18), [LinkedIn, 2025-03-13](https://www.linkedin.com/posts/simonbruno77_whispers-multiplayer-feature-portfolio-activity-7305933018672553985-eQxJ), [sec]). The "Games & Entertainment" category tag fell from 9.3% (2023) to 4.9% (2026) [obs]: game mechanics are moving into brand and portfolio sites, not game marketing. |
| **Shared presence** | Multiplayer rooms (Messenger, WebSockets), ghost messages (Bruno Simon). |
| **WebGPU in production at the top end** | Bruno Simon (above); Forged.build runs on a custom WebGPU engine ([Codrops](https://tympanus.net/codrops/2025/10/20/from-garage-to-browser-forged-build-and-the-webgpu-revolution/)); Codrops' 2025 review lists WebGPU fluid and TSL tutorials ([2025-12-29](https://tympanus.net/codrops/2025/12/29/2025-a-very-special-year-in-review/)). Awwwards has no WebGPU tag, so share is unmeasurable (gap). |
| **Serious and B2B brands going expressive** | "Business & Corporate" 20.2% (2023) to 24.3% (2026); "Technology" 17.2% to 21-26% [obs]. SOTMs for Terminal Industries (Sep 2025), Oryzo AI (Apr 2026), Dropbox Brand (Feb 2025); SOTD for Microsoft AI (Nov 2025, [Honors listing](https://www.awwwards.com/websites/winner_category_business-services/)); Razorpay's case study argues that the safe, product-in-the-hero B2B formula is the thing to break. |
| **Luxury and editorial real-time cinema** | "Luxury" 3.0% (2024) to 11.6% (2026) [obs] (the tag appears to be new in 2024). Cartier Watches & Wonders 2025 and GQ x Audemars Piguet (both SOTM, Immersive Garden) run a continuous cinematic timeline with sound as a navigation layer. |
| **Storytelling structure** | "Storytelling" 16.4% (2024) to 23.2% (2026) [obs]. |
| **Webflow and GSAP at the top** | SOTY 2025 built on Webflow; Webflow on 21% of SOTDs in the consistent window [obs]; GSAP is now free for all users, including former Club plugins such as SplitText and MorphSVG, with Webflow's backing ([gsap.com/pricing](https://gsap.com/pricing/), read 2026-09-24). Among the 30 SOTY 2025 nominees a Wappalyzer scan found Vue/Nuxt on 13, Webflow 6, GSAP 21, Lenis 18, Three.js 18, Howler 7 ([Bartoletti](https://www.linkedin.com/posts/stefanobartoletti_awwwards-2025-soty-nominees-tech-overview-activity-7417862429986152448-eU1Y), [sec]). |
| **Specificity over polish** | A 2026 Awwwards young-jury member reports that after 100+ sites, technically clean work had become the norm and the standouts were specific, opinionated and rooted in a place ([Medium, 2026-06-07](https://medium.com/design-bootcamp/i-judged-100-websites-for-awwwards-ai-is-winning-the-wrong-race-38efd7f3e3cc), [sec]). A measurement of 945 gallery sites found AI outputs cluster tightly in the middle of the human distribution, with the most expressive human cluster breaking its own grid ([ai-design-convergence](https://ai-design-convergence.vercel.app/), undated, [sec]). |

### 4.3 Fading (as a winning default, not banned)

| Signal | Evidence |
|---|---|
| **Typography-only minimalism** | "Typography" tag 27.3% (2023) to 18.7% (2026); "Minimal" 13.4% to 10.1%; Minimal is 2.2x more common on HM-only sites than SOTDs [obs]. The Telha Clarke case study says architecture portfolios have converged on neutral palettes, oversized imagery, minimal type and rigid grids ([Awwwards blog, 2026-07-10](https://www.awwwards.com/reshaping-telha-clarkes-digital-home.html)). |
| **Parallax and big-image heroes as the main idea** | "Parallax" 9.8% to 7.1%; "Big Background Images" 10.4% to 6.4% [obs]; parallax is twice as common on HM-only sites. |
| **Flat illustration and graphic design as default** | "Illustration" 8.5-11.8% through 2025, 6.0% in 2026; "Graphic design" about 10% to 4.9% [obs]. Still wins when authored (MindMarket SOTM Dec 2025). |
| **Page-transition showcases** | "Transitions" 26.8-28.3% through mid-2025, 15-20% since (possible taxonomy effect) [obs]. |
| **Horizontal-scroll galleries** | Rare (2-4% every year) [obs] and named by a juror as the stock derivative move [sec]. |
| **The clean, safe B2B page** | See Razorpay above; "Promotional" also fell to 11.6% in 2026, while corporate and technology categories rose [obs]. |

### 4.4 Conference and editorial signals (weak)

The Awwwards blog in 2026 is almost entirely studio-written case studies (Razorpay, Floema, Capitolium, La Revoltosa, Telha Clarke, fromanother, Obys, GQ & AP, Fluid Glass, San Rita; [blog index](https://www.awwwards.com/blog/), read 2026-09-24); no 2025 or 2026 Awwwards-authored trend report was found. The Awwwards Conference New York page frames its programme around AI in design methods, predictive UX, AR/VR and case studies, with speakers from Google, Porto Rocha, The New York Times and Locomotive ([conference page](https://conference.awwwards.com/new-york), undated); a listing puts a New York edition in December 2026 ([10times](https://10times.com/e1h4-x5z0-d8kr-r-awwwards-conference), unverified).

---

## 5. Studios that keep winning, and their house signatures

All-time counts from [Most Awarded Profiles](https://www.awwwards.com/winner-list/) (HM / SOTD / SOTM / SOTY, read 2026-09-24); recent SOTD counts since 2025-01-01 and SOTMs from the listings [obs]. Signatures are drawn from their awarded work and case studies; they describe tendencies, not rules.

| Studio | All-time | Since 2025 | House signature |
|---|---|---|---|
| **Immersive Garden** (Paris) | 89 / 68 / 13 / 3 | 9 SOTD; SOTMs Jan 2025, Jun 2025, Aug 2025, Mar 2026; Agency of the Year 2025, Studio of the Year 2024 | Luxury real-time cinema: material and lighting precision, continuous scrubbable timelines, sound as navigation (Cartier W&W 2025, GQ x AP). |
| **Locomotive** (Montreal) | 131 / 91 / 4 / 1 | 13 SOTD, the most of anyone; Agency of the Year 2023 and 2024 | Consistency: usability and performance held to the same bar as visuals (2024 jury quote above). Typographic layouts and smooth-scroll choreography are the common read of their style (unverified). |
| **Resn** (New Zealand) | 77 / 61 / 11 / 2 | 6 SOTD; SOTMs Navigate (Apr 2025), Tracing Art (Jul 2025) | Playful interactive storytelling for institutions and data; tagged data visualisation and illustration. |
| **Monks** | 112 / 59 / 8 / 4 | Not among the 2025-26 top SOTD winners [obs] | Large-scale campaign experiences (SOTY 2021 Umami Land, 2022 Persepolis Reimagined per [SOTY listing](https://www.awwwards.com/websites/sites_of_the_year/)). |
| **Active Theory** (US) | 77 / 58 / 10 / 3 | No SOTM since 2025 (last: Feb and Jun 2024) | Real-time 3D engineering for brands and its own studio sites (SOTY 2018 Active Theory v4, 2021 Prometheus Fuels). |
| **abeto** | n/a in top list | SOTY + Dev SOTY 2024, Dev SOTY 2025 | Technical artists who build worlds and multiplayer games in the browser with custom tools, WebGL UI and low-end-device budgets. |
| **Lusion** (Bristol) | n/a in top list | SOTM Oryzo AI (Apr 2026); SOTY 2023 | Physics, fluids and ray-marched real-time 3D, with simulations baked for the web. |
| **The First The Last** (US) | 46 / 23 / 1 / 2 | 11 SOTD; SOTMs Son Daven (Jun 2026), ERA Residence (Aug 2026) | Warm hospitality and real-estate storytelling; Webflow + GSAP + WebGL tags; Users' Choice 2024 with a flat, graphic site. |
| **Merci Michel** (France) | 62 / 43 / 6 / 2 | 8 SOTD | Game-like, playful brand activations in 3D. |
| **makemepulse** (France) | 56 / 42 / 8 / 1 | 6 SOTD | Interactive brand campaigns. |
| **Louis Paquet** (Montreal, independent) | 49 / 40 / 2 / 1 | 6 SOTD; SOTM MindMarket (Dec 2025); Independent of the Year 2025 | Colourful, illustration-led emotional interaction; proves 2D can still reach SOTM. |
| **Malvah** | n/a in top list | 9 SOTD; Studio of the Year 2025 | Brand-experience sites across architecture, services and immersive (listed SOTDs: Seventeen, Up&Up, Bitter Creek, Robot, dhk Architects, KODE Immersive; [Studio of the Year 2025](https://www.awwwards.com/annual-awards-2025/studio-of-the-year)). Style detail unverified. |
| **Obys** (Ukraine) | 42 / 33 / 2 / 0 | 6 SOTD; Studio of the Year 2023 | Editorial, art-historical storytelling with strong type (AIM, SOTM Jan 2024). |
| **OFF+BRAND.** | n/a in top list | SOTY 2025 | Webflow-built celebrity and brand platforms with WebGL, Rive and a bold two-colour system. |

Other studios with 5 or more SOTDs since January 2025 [obs]: HOLOGRAPHIK (9), Vide Infra, Unseen Studio, ET Studio (8 each), CUSP, Cuchillo, Beaucoup. (6 each), MONOGRID, ++hellohello, Dennis Snellenberg, ToyFight, Somefolk, FLOT NOIR, Tubik, Bürocratik, REJOUICE, BL/S, Noomo, Adoratorio (5 each).

---

## 6. Build recipes that satisfy both the jury and the house law

### 6.1 Visible-by-default scroll motion in CSS

Scroll-driven animations are supported in Chrome 115+ and Safari 26+, and only in Firefox preview builds per MDN's compatibility data (file last updated 2026-06-26; [BCD animation-timeline](https://github.com/mdn/browser-compat-data/blob/main/css/properties/animation-timeline.json)). Gate with `@supports` and animate only transform, so the worst case is a slightly offset but fully readable element.

```css
/* Content is fully visible without this block. */
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .lift {
      animation: lift linear both;      /* shorthand first ...            */
      animation-timeline: view();       /* ... because it resets timeline */
      animation-range: entry 0% entry 100%;
    }
  }
}
@keyframes lift {
  from { translate: 0 1.5rem; }
  to   { translate: 0 0; }
}
```

### 6.2 Scrubbed drift on already-visible media with GSAP

`gsap.matchMedia()` reverts everything created inside it when the condition stops matching, which makes reduced motion a first-class state ([GSAP docs](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29)).

```js
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();
mm.add({ motionOK: "(prefers-reduced-motion: no-preference)" }, (ctx) => {
  if (!ctx.conditions.motionOK) return;          // static layout is the designed fallback
  gsap.utils.toArray("[data-drift]").forEach((el) => {
    gsap.fromTo(el, { yPercent: -6 }, {           // element is visible at every frame
      yPercent: 6,
      ease: "none",
      scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true },
    });
  });
});
```

Never use `gsap.from(el, { opacity: 0 })` on copy or controls.

### 6.3 A WebGL layer that does not cost Usability or Semantics

```js
import * as THREE from "three";

const canvas = document.querySelector("canvas.scene");
canvas.setAttribute("aria-hidden", "true");      // the DOM carries the words and controls
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // no 3x rendering on phones

let onScreen = true;
new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; }).observe(canvas);

renderer.setAnimationLoop((t) => {
  if (!onScreen || document.hidden) return;      // skip work off-screen and in background tabs
  renderer.render(scene, camera);                 // scene and camera defined elsewhere
});
```

`setAnimationLoop` is the documented way to drive the loop ([three.js WebGLRenderer](https://github.com/mrdoob/three.js/blob/dev/docs/pages/WebGLRenderer.html.md)); the [three.js manual](https://github.com/mrdoob/three.js/blob/dev/manual/pages/creating-a-scene.html) notes it runs on `requestAnimationFrame` and pauses when the tab is hidden, so the `document.hidden` check is a belt-and-braces guard.

### 6.4 Self-score before shipping

Score each criterion 1-10 honestly, then apply the verified formula `0.4·D + 0.3·U + 0.2·Cr + 0.1·Co`. Targets for a SOTM-level build: Design ≥ 7.9, Usability ≥ 7.5 (above the top-tier mean of 7.45, which is where you out-score peers), Creativity ≥ 8.0, Content ≥ 7.8. For the developer jury: Accessibility, Markup and Semantics at 7.5 or better is already above the SOTM mean (7.0 to 7.4), and costs no creative ambition.

---

## Retrieval gaps

- `https://www.awwwards.com/annual-awards/winners`, `/annual-awards/about` and `/about-certificates/` returned HTTP 429 to curl; winners were confirmed instead from the Hall of Fame pages and the per-category `annual-awards-2025/...` pages (read through the research-pool extractor).
- The full list of the 30 SOTY 2025 nominees was not retrieved; nominees named here come from studios' own posts and a third-party Wappalyzer scan.
- The 2025 E-commerce of the Year category page (`annual-awards-2025/ecommerce-of-the-year` and a hyphenated variant) returned not-found; Scout Motors is confirmed by the Hall of Fame only, and its jury vote count is unknown.
- Awwwards publishes no rubric text for Design, Usability, Creativity or Content; the "in practice" definitions rest on observed sub-scores and secondary juror commentary (hontran.dev describes its author as a juror; not verified against the jury list).
- Mobile Excellence: only 2017-2018 documentation found; current status not confirmed.
- HM jury scores are never published, so the SOTD vs HM comparison uses tags and PRO status, not scores. HM sample covers only 2026-08-09 to 2026-09-25.
- Tag data is submitter-chosen and the taxonomy changed in August 2025; "Luxury" appears to be a 2024 addition. No WebGPU, Lenis or Rive tag exists, so their adoption is unmeasured in Awwwards data.
- The Developer Guidelines Google Doc has no visible revision date; it announces a first-quarter update without naming the year.
- Lando Norris implementation details (depth maps, helmet maps, masks, Rive files) come from a third-party teardown and a public asset mirror, not from OFF+BRAND; whether #D2FF00 is a client-owned brand colour is unverified.
- Awwwards Conference 2025 and 2026 programmes and dates were not verifiable from official dated pages.
- Awwwards jury 2026 composition was not extracted (the jury page is a client-side filter UI).
- "Most Awarded Profiles" rows are named only by logo alt text; three rows (US 32/29/1/0, Denmark 30/23/0/2, France 52/23/1/0) could not be matched to a name with certainty (the alt-text order suggests REJOUICE, Spring/Summer and BONHOMME) and were left out.
