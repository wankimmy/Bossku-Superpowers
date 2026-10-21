# Typography on award-winning sites (2025–2026)

Last updated: 2026-09-24

Scope: which typefaces and foundries recent Awwwards winners actually ship, what the licences allow, the numbers (sizes, tracking, leading, measure) they set, and working recipes for the signature type moves. The house law ([deslop-law.md](../../../../../deslop-law.md)) outranks award-site habit. Where winners do something the law calls slop, this file says so and gives the crafted alternative.

## How this was gathered

- **Sample.** The 31 most recent Sites of the Day on the [SOTD listing](https://www.awwwards.com/websites/sites_of_the_day/) (listing dates 2026-08-26 to 2026-09-25) plus the 20 Sites of the Month from Jan 2025 to Aug 2026 on the [SOTM listing](https://www.awwwards.com/websites/sites_of_the_month/). One site (ERA Residence) is on both lists, so there are 50 unique winners. Fonts were extracted for 47 of them. Also sampled: 16 nominees tagged on [/websites/typography/](https://www.awwwards.com/websites/typography/) and [/websites/big-typography/](https://www.awwwards.com/websites/big-typography/), and 24 studio sites (Locomotive, Lusion, Active Theory, Studio Freight, 14islands and others).
- **Method.** For each Awwwards `/sites/<slug>` page I resolved the live URL, fetched its HTML and up to 8 stylesheets, parsed every `@font-face` (family and file name) and every `font-family`, `font-size`, `letter-spacing` and `line-height` declaration, then evaluated `vw`/`clamp()` sizes at 1440 px and 390 px widths. All fetches ran on 2026-09-24. Raw data is in `evidence/typo/` (`fonts_sotd.json`, `fonts_sotm.json`, `fonts_more.json`, `scale.json`, `css/`).
- **Caveats.**
  - A face declared in CSS is not always rendered.
  - Fonts loaded from JS bundles, canvas or WebGL are invisible to this method.
  - The 390 px figures come from the declaration alone. Media-query overrides were not applied.
  - The "role" I give each face (display, text, mono) is inferred from how often its `font-family` is used.
- **Evidence labels.** **Observed** means the file or declaration was seen in a winner's live CSS. **Documented** means stated on a foundry, MDN or W3C page. Anything else is marked (unverified).

---

## 0. Decisions for the builder (read first)

1. **Pick one display voice and at most one neutral companion.** 30 of the 47 winners load one or two families. Three or more families usually means script, pixel or legacy extras, not a richer system.
2. **License the display face.** The identity face on winners is overwhelmingly a licensed indie face. Pangram Pangram (8 winners) and Swiss Typefaces' Suisse Int'l (5) lead, then Dinamo, Displaay, Commercial Type and Due Studio (3 each). Free OFL faces mostly appear as body, mono or UI.
3. **Winners do ship the law's slop faces.** Work Sans, Archivo, Instrument Serif, Space Grotesk, Syne (declared), Inter and Fragment Mono were all found on winners, and JetBrains Mono on nominees. The jury's bar is lower than the house bar. Never cite "a winner used it" as a reason.
4. **Size display type in `clamp()` with a `rem` floor.**
   - Hero headlines on winners run 100–220 px at 1440 (7–15 vw).
   - Poster words and wordmarks run 225–470 px (15–33 vw).
   - Keep the clamp max within 2.5× its min, or treat the word as a logotype. Wider ranges can fail WCAG 1.4.4 ([Smashing, 2023](https://www.smashingmagazine.com/2023/11/addressing-accessibility-concerns-fluid-type/)).
5. **Tighten tracking as size grows.**
   - Grotesks at 120 px or more: −0.03 to −0.05 em.
   - 48–120 px: −0.02 em.
   - Body: 0.
   - Serif display: about 0 or slightly positive.
   - Never so tight that glyphs touch (law: "Cramped display type").
6. **Set display leading at 0.78–0.95.** Then protect ascenders and descenders from masks and `overflow: clip` ("clear the cut").
7. **Keep content visible by default.** Split-line reveals are allowed only as motion on text that is already visible. A hero mask reveal needs a completion failsafe. Never use opacity 0 until JS fires. A winner (Trevor Noah, SOTD) hides split text at opacity 0 until `html.is-ready`; that is the law's invisible-content trap.
8. **Use mono only for real data** (timestamps, prices, coordinates, indices). It was observed as the house voice on some winners; that is a slop tell.
9. **Check the licence before shipping.** Two winners ship font files or families named "Trial" (Cerebrium: "ABC Favorit Trial"; White Desert: `CardinalClassicLongWeb-*-Trial.woff2`). Trial terms at Dinamo and Production Type exclude live use.
10. **Never reuse the previous project's pairing** (law, "Default Google fonts" rule 2). Each site gets its own type decision.

---

## 1. What the winners actually load

### 1.1 Per-site evidence (live CSS, 2026-09-24)

Sites of the Day (listing dates 2026-08-26 → 2026-09-25):

| Site | Families found in `@font-face` | Foundry (verified where linked) |
|---|---|---|
| [The Tie-break](https://www.awwwards.com/sites/the-tie-break) | Instrument Serif (Italic file), Work Sans | Google/OFL: both on the law's slop lists |
| [Moto Finance](https://www.awwwards.com/sites/moto-finance) | Neue Montreal | Pangram Pangram |
| [Sobha Privy Collection](https://www.awwwards.com/sites/sobha-privy-collection) | TT Commons Pro, TT Ramillas, plus an Adobe Fonts kit (Altesse Std) | TypeType |
| [bleibtgleich26](https://www.awwwards.com/sites/bleibtgleich26) | Akzidenz-Grotesk Pro | Berthold |
| [Gil Huybrecht](https://www.awwwards.com/sites/gil-huybrecht) | Lay Grotesk (aliased as `sans`) | [Due Studio](https://www.due-studio.com/typefaces/lay-grotesk) |
| [Pensatori Irrazionali](https://www.awwwards.com/sites/pensatori-irrazionali) | Helvetica Now Var, PP Editorial Old, Novela, Ballet, Sometype Mono | Monotype, Pangram; Ballet and Sometype are OFL |
| [BOC Studio](https://www.awwwards.com/sites/boc-studio) | PP Mori | Pangram Pangram |
| [NOHO](https://www.awwwards.com/sites/noho) | Switzer (+ Variable) | Fontshare / ITF |
| [LXL Creative](https://www.awwwards.com/sites/lxl-creative) | Owners Wide, Manrope, Scribo Rough Pro | [MCKL](https://www.mckltype.com/essays/designing-owners); Manrope is OFL |
| [L.I.S.A. (Locomotive)](https://www.awwwards.com/sites/l-i-s-a) | PP Locomotive New (PP-prefixed custom), Helvetica Now Display | Pangram (custom, unverified), Monotype |
| [Aspen Search](https://www.awwwards.com/sites/aspen-search) | Suisse Int'l, Suisse Int'l Mono | Swiss Typefaces |
| [Leo Parpeix 2026](https://www.awwwards.com/sites/leo-parpeix-portfolio-2026) | Monument Grotesk, Avantt (variable) | Dinamo, [Displaay](https://displaay.net/typeface/avantt) |
| [Warm & Fuzzy](https://www.awwwards.com/sites/warm-fuzzy) | Suisse Int'l | Swiss Typefaces |
| [White Desert](https://www.awwwards.com/sites/white-desert) | Cardinal Classic Long/Mid (some files `-Trial`), Inter Tight, Oswald | [Production Type](https://productiontype.com/font/cardinal); Google |
| [Cerebrium](https://www.awwwards.com/sites/cerebrium) | "ABC Favorit Trial", Suisse Int'l + Mono | Dinamo (trial name), Swiss Typefaces |
| [USAvionix](https://www.awwwards.com/sites/usavionix) | Geist, Geist Mono | Vercel (OFL) |
| [Seasats](https://www.awwwards.com/sites/seasats) | Season Mix, Season Sans, PP Supply Mono | [Displaay](https://displaay.net/typeface/season), Pangram |
| [Why Zero](https://www.awwwards.com/sites/why-zero) | PP Supply Mono/Sans, Google Sans Flex/Code, Inter, Newsreader, STK Bureau Serif, Caveat | mixed |
| [United Carriers](https://www.awwwards.com/sites/united-carriers) | BT Steinhart + Mono, Helvetica Neue | [BeauType](https://www.myfonts.com/products/regular-bt-steinhart-989163) |
| [Gionatan Nese 26](https://www.awwwards.com/sites/gionatan-nese-26) | Lay Grotesk, Teodor | Due Studio, [Displaay](https://displaay.net/typeface/teodor) |
| [Illoca](https://www.awwwards.com/sites/illoca) | F37 Analog, Graphik, Architect Pro; also declares Space Grotesk, Syne, DM Sans | F37, Commercial Type |
| [Trevor Noah](https://www.awwwards.com/sites/trevor-noah) | Die Grotesk B / C / D | [Klim](https://klim.co.nz/fonts/die-grotesk/) |
| [Paul Kalkbrenner](https://www.awwwards.com/sites/paul-kalkbrenner) | ABC Diatype Plus Variable | [Dinamo](https://abcdinamo.com/typefaces/diatype) |
| [Squarespace Foundations](https://www.awwwards.com/sites/squarespace-foundations) | Clarkson, Clarkson Serif, Clarkson Condensed | brand superfamily (custom, unverified) |
| [ERA Residence](https://www.awwwards.com/sites/era-residence) (also SOTM) | Maison Neue Extended, plus an Adobe Fonts kit | [Milieu Grotesque](https://www.myfonts.com/products/maison-neue-extended-pack-package-1185269) |
| [Aardvark Book Club](https://www.awwwards.com/sites/aardvark-book-club) | Champ, Degular, Hello Organichand | [OH no Type](https://fonts.adobe.com/fonts/degular) (Degular) |
| [Hobro Digital](https://www.awwwards.com/sites/hobro-digital) | PP Neue Montreal, Kamerik 205, Freight Big Pro Light Italic, Akkurat Mono | Pangram, [Talbot Type](https://www.myfonts.com/collections/kamerik-205-font-talbot-type), Lineto |
| [Decathlon Yestalgia](https://www.awwwards.com/sites/decathlon-yestalgia) | Roboto Flex (13 axes requested) | Google |
| [SharpLink](https://www.awwwards.com/sites/sharplink) | Archivo, Archivo Narrow | Google: on the slop list |
| [AI in Design Report 2026](https://www.awwwards.com/sites/ai-in-design-report-2026) | Beausite Classic, Inter, Fragment Mono, Geist Mono | [Fatype](https://fatype.com/typefaces/beausite) |

Sites of the Month (Jan 2025 → Aug 2026):

| Site | Families | Foundry |
|---|---|---|
| [Lama Lama](https://www.awwwards.com/sites/lama-lama-2) | Suisse BP Int'l, Sometype Mono | Swiss Typefaces; OFL |
| [Son Daven](https://www.awwwards.com/sites/son-daven) | KTF Metro Roman, KTF Metro Blueline | [Kyiv Type Foundry](https://www.kyivtypefoundry.com/projects/kyiv-metro-fonts) |
| [Floema](https://www.awwwards.com/sites/floema) | Zimula (variable, custom `cnct` axis) | [La Bolde Vita](https://www.laboldevita.com/fonts/zimula) |
| [Oryzo](https://www.awwwards.com/sites/oryzo-ai) | Literata, DM Mono | Google/OFL |
| [GQ × AP Extraordinary Lab](https://www.awwwards.com/sites/gq-ap-the-extraordinary-lab) | GT America, Adobe Garamond/Garamond Premier, GQ Sans | Grilli Type, Adobe, custom |
| [Shopify Renaissance Edition](https://www.awwwards.com/sites/the-renaissance-edition) | Neue Montreal, Inter Variable, HW Cigars, Imperial Script | Pangram; others mixed |
| [Bruno Simon](https://www.awwwards.com/sites/brunos-portfolio) | Pally, Nunito, Amatic SC | Fontshare / ITF; Google |
| [Mindmarket](https://www.awwwards.com/sites/mindmarket) | Inter (only face in CSS) | Google |
| [Lando Norris](https://www.awwwards.com/sites/lando-norris) | Brier, Mona Sans Variable | [Type Department](https://type-department.com/products/brier); [GitHub OFL](https://github.com/github/mona-sans) |
| [Ponpon Mania](https://www.awwwards.com/sites/ponpon-mania) | Libre Franklin | Google |
| [Terminal Industries](https://www.awwwards.com/sites/terminal-industries) | Suisse Int'l, Geist Mono (mono is the most-used family variable) | Swiss Typefaces; Vercel |
| [Getty: Tracing Art](https://www.awwwards.com/sites/tracing-art) | Bradford LL, Graphik | Lineto, Commercial Type |
| [Montfort](https://www.awwwards.com/sites/montfort) | Josefin Sans, Century Gothic | Google, Monotype |
| [anime.js](https://www.awwwards.com/sites/anime-js) | DINish (variable), Berkeley Mono, Digital-7 | OFL; US Graphics |
| [Siena Film Foundation](https://www.awwwards.com/sites/siena-film-foundation) | Neue Brücke, NB International, P22 Parrish Roman | [Due Studio](https://www.due-studio.com/typefaces), Neubau, P22 |
| [Dropbox Brand](https://www.awwwards.com/sites/dropbox-brand) | Sharp Grotesk DB (variable), Atlas Grotesk | Dropbox cut of Sharp Grotesk (unverified); Commercial Type |
| [Immersive Garden](https://www.awwwards.com/sites/immersive-garden-website) | Helvetica Neue, PS Times | Monotype; PS Times unverified |

Not extracted: The Tuscan Journey (canvas/JS), Cartier Watches & Wonders (JS), Navigate (HTTP 525).

### 1.2 Tallies (47 winners with fonts; a site counts once per foundry)

| Foundry | Winner sites | Notes |
|---|---|---|
| Pangram Pangram | 8 | Neue Montreal ×3, Editorial Old, Mori, Supply Mono ×2, plus the PP-prefixed Locomotive custom |
| Monotype / Linotype / Berthold classics | 6 | Helvetica Now/Neue, Akzidenz-Grotesk, Century Gothic |
| Swiss Typefaces | 5 | Suisse Int'l, sometimes with its Mono |
| Dinamo, Displaay, Commercial Type, Due Studio | 3 each | |
| Lineto, Fontshare | 2 each | |
| Grilli, Klim, Production Type, OH no, TypeType, BeauType, MCKL, La Bolde Vita, Kyiv TF, Type Department, Talbot, Fatype, Milieu Grotesque, Neubau, P22, F37, US Graphics | 1 each | |
| Google / other OFL in **any** role | about 21 | |
| Google / other OFL as the **primary display** voice | 8 | Roboto Flex, Archivo, Literata, Instrument Serif, Inter, Libre Franklin, Josefin Sans, Geist |

- **Family count per winner:** 16 load one family, 14 load two, 7 load three, and the rest load four or more. The last group is inflated by mono, script and declared-but-unused faces.
- **Corroboration.** Typewolf's "Top 10 Most Popular Fonts of 2025" is Söhne, Feature, Neue Montreal, Founders Grotesk, Cardinal, Editorial Old, Signifier, Monument Grotesk, GT Super and Suisse Int'l ([typewolf.com/all-fonts](https://www.typewolf.com/all-fonts)). Its all-time top five are Apercu, GT America, Futura, Founders Grotesk and Neue Haas Grotesk. The same indie-foundry set dominates.
- **Motion stack in the same HTML (lower bound; bundled apps hide their imports):**
  - Lenis on 26 of 49 winner homepages.
  - GSAP SplitText on 9 (all via `gsap@3.12–3.15` CDN tags, mostly Webflow builds).
  - `split-type` on 2.

---

## 2. Display archetypes

Each archetype lists named faces with foundry, licence path and where they were observed, then a **free/self-hostable alternative that is not on the law's slop lists**, then the archetype's slop tells. Licence detail is in §3.

The law's banned faces:
- Sans: Inter, Space Grotesk, Sora, Syne, Archivo, Onest, Darker Grotesque, Geologica, Hanken Grotesk, Spline Sans, Schibsted Grotesk, Gabarito, Figtree, Work Sans.
- Rounded/novelty: Quicksand, Bagel Fat One, Baloo, Fredoka, Chewy, Lobster.
- Serif: Fraunces, Cormorant, Bodoni and the Didones (incl. Playfair), Petrona, Hedvig Letters Serif, Brygada 1918, Young Serif.
- Mono: JetBrains Mono, IBM Plex Mono, Spline Sans Mono, Fragment Mono.
- The "tasteful swap" set: Big Shoulders, Newsreader, IBM Plex Mono, Instrument Serif, Bricolage.
- Also flagged: Clash Display and General Sans ("read generic").

### 2.1 Grotesk with character (quirky sans that carries the brand)

Use it when the brand is contemporary and confident, and the page's drama comes from scale and composition, not ornament.

| Face | Foundry | Licence path | Evidence |
|---|---|---|---|
| PP Neue Montreal | Pangram Pangram | Web licence per (sub)domain, capped monthly pageviews, 1-year term; free personal-use trial | Moto Finance, Hobro, Shopify Renaissance Edition; Typewolf 2025 #3 |
| PP Mori | Pangram Pangram | as above | BOC Studio |
| ABC Favorit | Dinamo | One domain per web licence, unlimited traffic, priced by client headcount | Cerebrium (as a trial-named family) |
| ABC Monument Grotesk | Dinamo | as above | Leo Parpeix; Typewolf 2025 #8 |
| Die Grotesk (widths B/C/D) | Klim | Web licence by page views or unique users, one-off fee | Trevor Noah |
| Season Sans / Season Mix | Displaay | Perpetual, one-time, priced by company size | Seasats |
| Lay Grotesk | Due Studio | From €60 per style; metric unverified | Gil Huybrecht, Gionatan Nese |
| BT Steinhart (+ Mono) | BeauType (via MyFonts) | MyFonts web licence | United Carriers |

- **Free alternatives:**
  - [Apfel Grotezk](https://www.collletttivo.it/typefaces/apfel-grotezk) (Collletttivo, OFL, 5 weights).
  - [Pally](https://www.fontshare.com/fonts/pally) (Fontshare ITF FFL, variable 400–700). Named by the law; observed on the Bruno Simon SOTM.
  - Karrik (Velvetyne, OFL; [velvetyne.fr](https://velvetyne.fr/)).
- **Avoid:**
  - Space Grotesk, Syne, Sora, Clash Display/Grotesk, General Sans (General Sans observed on the Byotōne nominee).
  - Satoshi. It is Fontshare's most-viewed family by a wide margin: 108,818 views, against Clash Display's 69,460 and General Sans' 59,299 ([Fontshare API](https://api.fontshare.com/v2/fonts), 2026-09-24). Exposure that high reads generic (inference, not in the law).

### 2.2 Neo-grotesk at huge sizes (Swiss neutrality, scaled up)

Use it when the identity is structure: big neutral words, strict grid, photography or 3D doing the talking. The type needs precise negative tracking and an idea in the layout. A neutral face at huge size with nothing else is the "boring" failure in the law.

| Face | Foundry | Licence path | Evidence |
|---|---|---|---|
| Suisse Int'l (+ Mono, Condensed) | Swiss Typefaces | One-time licence; "no limits in regard to the number of uses, domains, or website visitors" ([source](https://www.swisstypefaces.com/fonts/suisse/)) | Aspen Search, Warm & Fuzzy, Cerebrium, Lama Lama, Terminal Industries; Rejouice |
| Helvetica Now Display / Var | Monotype | Pageview-based web licence ([MyFonts EULA](https://www.myfonts.com/pages/license-agreement?id=eula_2267)) | L.I.S.A., Pensatori; Locomotive |
| Neue Haas Grotesk Display | Monotype | as above | Build in Amsterdam (studio) |
| Akzidenz-Grotesk Pro | Berthold | Foundry licence (unverified) | bleibtgleich26 |
| ABC Diatype (Plus Variable) | Dinamo | Company-size pricing, one domain per web licence | Paul Kalkbrenner |
| Maison Neue (Extended) | Milieu Grotesque | via MyFonts / foundry | ERA Residence |
| Söhne | Klim | Page views or unique users | Stripe; Typewolf 2025 #1 |
| Graphik, Atlas Grotesk | [Commercial Type](https://commercialtype.com/catalog/graphik) | Domains + aggregated unique monthly visitors | Getty Tracing Art, Illoca; Dropbox Brand |

- **Free alternative:** [Switzer](https://www.fontshare.com/fonts/switzer) (Fontshare, variable 100–900, italic). Observed on the NOHO SOTD. Caveat: its exposure (30,217 views) is in Clash Grotesk's range (30,859). Use it only where neutrality is the point and scale, cropping and composition carry the identity. For body text the law allows `system-ui`.
- **Avoid:** Inter and Inter Tight (observed on White Desert and Mindmarket), Hanken, Schibsted, Archivo (SharpLink).

### 2.3 Editorial serif (the law's "signature serif headline")

Use it for culture, hospitality, publishing and considered luxury. The serif must have its own character; a thin high-contrast default is not premium.

| Face | Foundry | Licence path | Evidence |
|---|---|---|---|
| PP Editorial New / Old | Pangram Pangram | per-domain pageviews, 1-year term | Pensatori (Old), Money in Check nominee (Old); Typewolf 2025 #6 |
| Teodor | Displaay | perpetual, company size | Gionatan Nese |
| Reckless / Reckless Neue | [Displaay](https://displaay.net/typeface/reckless) | as above | Build in Amsterdam (Reckless Neue Book) |
| Cardinal (Classic Short/Mid/Long, Fruit) | Production Type | Web licence annual by default; metric is company size ([help](https://help.productiontype.com/docs/licensing/license_types/web_license)) | White Desert; Typewolf 2025 #5 |
| Tiempos Headline, Signifier | [Klim](https://klim.co.nz/fonts/signifier/) | page views or unique users | Typewolf 2025 #7 (Signifier) |
| GT Super, GT Sectra, GT Alpina | [Grilli Type](https://www.grillitype.com/typeface/gt-super) | unique monthly visitors | Dogstudio (GT Sectra Display); Typewolf 2025 #9 (GT Super) |
| Canela | [Commercial Type](https://commercialtype.com/catalog/canela) | domains + unique visitors | Typewolf all-time top 10 |
| Bradford LL | [Lineto](https://lineto.com/typefaces/bradford) | foundry licence (unverified) | Getty Tracing Art |

- **Free alternatives** (all Fontshare ITF FFL, [API](https://api.fontshare.com/v2/fonts)):
  - Sentient (variable 200–700, italic).
  - Gambarino (single weight). Sentient and Gambarino are both named by the law.
  - Zodiak (variable 100–900).
  - Erode (variable 300–700).
  - Boska (display, variable 200–900).
  - For an art-nouveau display: [Ouroboros](https://velvetyne.fr/fonts/ouroboros/) (Velvetyne, OFL).
- **Avoid:**
  - Instrument Serif. Observed on The Tie-break (SOTD) and the Stanzza and Matteo Vincenti nominees; it is on the law's "tasteful swap" list.
  - Cormorant Garamond (Loam House nominee).
  - Playfair Display (declared on Money in Check).
  - Fraunces, the Didones, Newsreader (Why Zero), Young Serif.
  - Literata as a signature face. It is the Oryzo SOTM display face, but law rule 1 keeps the signature line off the Google shelf.

### 2.4 Variable and kinetic (axes as material)

Use it when type itself is the interaction: weight or width responding to scroll or pointer, sans-to-serif morphs, ink-trap growth.

| Face | Foundry | Axes | Evidence |
|---|---|---|---|
| ABC Diatype Plus Variable | Dinamo | weight + others (unverified) | Paul Kalkbrenner |
| Zimula | La Bolde Vita | InkTrap ↔ InkSpot, plus weight ([source](https://www.laboldevita.com/fonts/zimula)) | Floema sets `font-variation-settings: "cnct" 1000, "wght" 500` |
| Season | Displaay | weight, slant, SERF (sans → serif) ([source](https://displaay.net/typeface/season)) | Seasats |
| Avantt | Displaay | weight, slant | Leo Parpeix (`avantt-variable.ttf`) |
| GT Flexa | [Grilli Type](https://www.grillitype.com/typeface/gt-flexa) | width (unverified range) | not observed |
| Obviously | OH no Type | 8 weights × 6 widths ([catalog](https://ohnotype.co/fonts)) | not observed |
| Roboto Flex | Google | 13 axes incl. `opsz, wdth, wght, XOPQ, XTRA, YOPQ, YTDE, YTFI, YTLC, YTUC` | Decathlon Yestalgia requests all of them |
| Mona Sans | GitHub (OFL) | wght 200–900, wdth, opsz 1–100 ([README](https://github.com/github/mona-sans)) | Lando Norris (`MonaSans-VariableFont_wdth,wght`) |

- **Free alternatives:**
  - Mona Sans (OFL). Use its axes as motion material, not as an untreated brand voice; it also ships on the Google shelf (unverified).
  - Collletttivo's variable families Sprat, Halibut, Sinistre and Aujournuit, all OFL ([list](https://www.collletttivo.it/typefaces)).
  - Switzer VF for weight-only motion.
- **Tells:** animating every word; axis motion on body text (it reflows); proximity effects on touch devices.

### 2.5 Mono accents (data only)

| Face | Foundry | Evidence |
|---|---|---|
| PP Supply Mono | Pangram Pangram | Seasats, Why Zero |
| Suisse Int'l Mono | Swiss Typefaces | Aspen Search, Cerebrium |
| Akkurat Mono | [Lineto](https://lineto.com/typefaces/akkurat-mono) | Hobro |
| Replica Mono, Lettera Mono | [Lineto](https://lineto.com/typefaces/replica) | darkroom.engineering (studio), Nothing (studio) |
| Berkeley Mono | US Graphics | anime.js |
| BT Steinhart Mono | BeauType | United Carriers |
| Geist Mono | Vercel (OFL) | USAvionix, Terminal Industries, AI in Design Report |

- **Free alternatives:**
  - Sometype Mono (OFL). Observed on [Lama Lama](https://www.awwwards.com/sites/lama-lama-2) (SOTM) and [Pensatori](https://www.awwwards.com/sites/pensatori-irrazionali) (SOTD).
  - Necto Mono (Collletttivo, OFL).
  - Steps Mono (Velvetyne, OFL).
  - Azeret Mono (OFL; on Fontshare; co-designed by Displaay's Martin Vácha per [Luc Devroye](https://luc.devroye.org/fonts-89008.html)).
- **Avoid:**
  - JetBrains Mono (the Sibal Design and Unimatic nominees use it).
  - IBM Plex Mono, Spline Sans Mono.
  - Fragment Mono (AI in Design Report uses it).
  - Any mono as the house voice. On Terminal Industries `var(--font-mono)` is the most-used family variable (60 declarations).

### 2.6 Condensed display

| Face | Foundry | Evidence |
|---|---|---|
| Druk | [Commercial Type](https://commercialtype.com/catalog/druk) | Typewolf all-time top 50 |
| PP Formula Condensed | [Pangram Pangram](https://pangrampangram.com/products/formula-condensed) | catalog |
| ABC Gravity | [Dinamo](https://abcdinamo.com/typefaces/gravity) | catalog |
| GT Standard (L Condensed) | Grilli Type | Velour Productions nominee (served as "Velour Display" = `GT-Standard-L-Condensed-Black`) |
| GT Walsheim Condensed | Grilli Type | DKTON nominee |
| Owners (XXNarrow → XXWide) | MCKL | LXL Creative (Wide) |
| Trade Gothic Next Condensed | Linotype | Project Cult nominee |

- **Free alternative:** [Tanker](https://www.fontshare.com/fonts/tanker) (Fontshare, single weight; named by the law). Free condensed options are thin. Oswald, Anton, Bebas Neue and League Gothic are Google-shelf defaults; Oswald is observed on White Desert as a support face.
- **Settings:** uppercase condensed at +0.02 to +0.06 em (Project Cult sets `0.06em` at 60.36vw), leading 0.85–0.9.
- **Tell:** Archivo Narrow solid, outline and accent-colour versions stacked as "three fonts" (law: Archivo).

### 2.7 Experimental and display-only (one moment per page)

| Face | Source | Evidence / licence |
|---|---|---|
| KTF Metro Blueline / Roman | Kyiv Type Foundry | Son Daven (SOTM). Free for Ukrainians, donation for others ([Fonts In Use](https://fontsinuse.com/typefaces/233079/ktf-metro-blueline)) |
| Brier | Type Department | Lando Norris (SOTM) |
| Neue Brücke | Due Studio | Siena Film Foundation (SOTM) |
| Eckmannpsych, Ohno Blazeface, Cheee | [OH no Type](https://ohnotype.co/fonts) | catalog with prices |
| Terminal Grotesque, Kaeru Kaeru, Trickster, Fungal, Ouroboros | [Velvetyne](https://velvetyne.fr/) | OFL |
| Mazius Display, Borges | [Collletttivo](https://www.collletttivo.it/typefaces) | OFL |
| Custom families | Obys Sans, Clarkson, Sharp Grotesk DB, GQ Sans, WITS | commissioned |

- **Free alternatives:** Velvetyne and Collletttivo faces (OFL). Fontshare Array, Stardom, Nippo and Bevellier (FFL).
- **Rule:** an experimental face gets one job, such as the wordmark or one hero word. It never sets nav, buttons, prices or body. That would be the law's "one font carrying the whole brand" and "novelty display" failure.

---

## 3. Licensing quick reference (documented, fetched 2026-09-24)

| Foundry | Web licence metric | Term | Trials | Self-host / subset | Source |
|---|---|---|---|---|---|
| Pangram Pangram | Per domain or subdomain, capped **monthly pageviews** | **1 year, renew** | Free for personal use only; no public website | Self-host (unverified subset rule) | [EULA](https://pangrampangram.com/pages/eula), [FAQ](https://pangrampangram.com/pages/faq); subscription from $29/yr covers 1 site ≤5,000 pv/mo ([FSP](https://pangrampangram.com/products/fsp)) |
| Dinamo (ABC) | **Client company size**; one domain, unlimited traffic | one-off | For deciding and pitching only | "welcome to self-host and subset" | [licenses](https://abcdinamo.com/licenses) |
| Grilli Type (GT) | **Unique monthly visitors**, any number of domains within the total | one-off | Minimal charset; fine in mockups and prototypes | Self-host; no public repos (GitHub) | [licenses](https://www.grillitype.com/licenses), [EULA](https://www.grillitype.com/eula) |
| Klim | Page views or unique users | one-off, no expiry | Free test fonts, internal only | — | [licences](https://klim.co.nz/licences/) |
| Commercial Type | Domains + aggregated unique monthly visitors; over for 3 consecutive months means upgrade | — | — | EULA restricts modifications (subsetting unclear) | [EULA](https://commercialtype.com/eula) |
| Displaay | Company size (minimum 3 people); covers any of your domains | perpetual | Free full trials, 1 user, internal/pitch | `@font-face` only | [licenses](https://displaay.net/help/licenses) |
| Production Type | Company size (no pageviews) | web annual by default | Trial = testing only, no live use | Self-host yes; **no user modification** (subsetting needs an addendum) | [web](https://help.productiontype.com/docs/licensing/license_types/web_license), [trial](https://help.productiontype.com/docs/licensing/license_types/trial_license) |
| Blaze Type | Company size + usage; all domains, no pageview caps | one-time | Limited charset, testing only | — | [license](https://blazetype.eu/license), [EULA](https://blazetype.eu/eula) |
| Swiss Typefaces | No limits on domains or visitors | lifelong | Desktop + web trials (reduced charset) | Ships WebS/WebM/WebXL subsets | [Suisse](https://www.swisstypefaces.com/fonts/suisse/) |
| OH no Type | Page-view tiers from 500k to Unlimited | — | — | Client must hold its own licence | [web licence](https://ohnotype.co/info/licenses/web) |
| Studio Feixen | Bundled desktop + web levels (Level 1: 1–5 computers / 50K monthly visitors) | perpetual | Trial licence exists | — | [EULA PDF](https://fonts.studiofeixen.ch/wp-content/uploads/downloads/Studio-Feixen-Fonts-EULA.pdf) |
| Tightype | — | — | Trials by request (Typographer subscription or à la carte agreement) | — | [contact](https://tightype.com/contact/) |
| Future Fonts | Each designer's own EULA; in-progress fonts get dearer as versions ship, and early buyers get free updates | — | — | — | [intro](https://medium.com/future-fonts/introducing-futurefonts-xyz-8c0569777db6) |
| Colophon | Monotype-owned; MyFonts perpetual or Monotype Fonts subscription | — | Free trials | — | third-party summary ([Typeyeah](https://typeyeah.com/foundry/colophon-foundry/)) (unverified on foundry site) |
| 205TF | EULA exists; terms not extractable | — | — | — | [EULA](https://www.205.tf/eula) (unverified) |
| Fontshare (ITF) | **Free** for personal and commercial use, any medium | unlimited | n/a | "Self-hosting … is permitted and recommended"; FFL fonts can't be redistributed or modified | [ITF FFL](https://fontshare.com/licenses/itf-ffl) |
| Velvetyne | SIL OFL | — | n/a | yes | [about](https://velvetyne.fr/about/) |
| Collletttivo | SIL OFL (credit requested) | — | n/a | yes | [licensing](https://www.collletttivo.it/licensing) |

Rules that follow from this:
- **The client owns the licence, not the studio.** Pangram, Dinamo and OH no all say so explicitly. Budget the licence in the proposal.
- **Pangram web licences expire after a year.** Put the renewal date in the handoff doc.
- **Never deploy trial files.** Check that the family names and file names in production CSS contain no `Trial`, `Test` or `Demo`.
- **Never pull fonts from pirate mirrors.** The Stanzza nominee serves `ofont.ru_Helios-Cond.woff`, a file name from a free-font mirror site.

---

## 4. Scale and rhythm

### 4.1 What winners set (live CSS, computed from the declaration)

| Site (award) | Selector | Value | px @1440 | px @390 | Tracking | Leading |
|---|---|---|---|---|---|---|
| NOHO (SOTD) | `.footer-slogan` | `15.625vw` | 225 | 61 | `-.625vw` (≈ −0.04em) | 100% |
| NOHO (SOTD) | `.h1` | `6.25vw` | 90 | 24* | — | 95% |
| Terminal Industries (SOTM) | `.title-h1` | `10.256vw` | 148 | 40* | `-.308vw` (≈ −0.03em) | — |
| Floema (SOTM) | `.-title-1` | `clamp(80px, 67.91px + 3.1vw, 120px)` | 113 | 80 | −0.04em | 1em |
| Floema (SOTM) | `.-title-2` | `clamp(32px, 22.64px + 2.4vw, 64px)` | 57 | 32 | −0.04em | 1.05em |
| Lama Lama (SOTM) | `.ll-display-rg` | `clamp(3.25rem, 1.0625rem + 4.38vw, 5rem)` | 80 | 52 | −0.02em | .8 |
| Leo Parpeix (SOTD) | `.title` | `11.25vw` | 162 | 44* | — | .9 |
| GQ × AP (SOTM) | `.splashScreen__title` | `7.5vw` | 108 | 29* | — | .87 |
| Shopify Renaissance (SOTM) | `.headline-1` | `clamp(7.5rem, 35.79px + 10.96vw, 13.75rem)` | 194 | 120 | — | — |
| Hobro (SOTD) | `.title--cursive` | `clamp(7.5rem, 15.1vw, 18.125rem)` | 218 | 120 | — | .88 |
| Decathlon (SOTD) | `.u-title-100` | `25vw` | 360 | 98 | — | .85 |
| Oryzo (SOTM) | `#sustainability-title-main` (serif) | `15vw` | 216 | 58 | **+0.018em** | 1 |
| Paul Kalkbrenner (SOTD) | `.rotating-text__heading` | `clamp(2.5em, 7.5vw, 4.5em)` | 72 | 40 | −0.02em | 1 |
| Lando Norris (SOTM) | `.marquee-advanced__item` | `max(4em, 8vw)` | 115 | 64 | — | — |
| Trevor Noah (SOTD) | `.book_detail_title` | `clamp(3.125rem, 2.46rem + 2.64vw, 5.625rem)` | 77 | 50 | — | .9 |
| Superhuge (nominee) | `[data-site-footer-word]` | `max(16rem, 28.5vw + 3.5625rem)` | 467 | 256 | 0 | .78 |
| Matteo Vincenti (nominee) | `.collective-words` | `clamp(10rem, 28vw, 23rem)` | 368 | 160 | −0.065em | .8 |
| DKTON (nominee) | `.footer_mark` | `9vw` | 130 | 35* | −0.005em | .78 |
| Project Cult (nominee) | `.work__left-title h1` (condensed caps) | `60.36vw` | 869 | 235 | **+0.06em** | 90% |
| 14islands (studio) | `h1` | `19.68vw` | 283 | 77* | −0.05em | 1 |
| Studio Freight (studio) | `.display` | `clamp(126px, …, 286px)` | 210 | 126 | −2.88px (≈ −0.014em) | 80% |

`*` means pure `vw` with no floor; a media query probably overrides it (unverified).

Across all 80 sampled stylesheets:
- **Most frequent `letter-spacing` values (em):** −0.02 (233 declarations), −0.01 (193), −0.04 (133), −0.03 (83), +0.01 (74), −0.06 (43), then small-label values +0.08 (34), +0.1 (29), +0.05 (25), +0.3 (25).
- **`text-wrap`:** `balance` appears 215 times and `pretty` 141 times.
- **Most common `max-width` in `ch`:** 12ch (16 declarations), 14ch (11), 18ch (10), 24ch (10). These force one- or two-line display lines. Text blocks sit at 30–65ch.

### 4.2 Pattern: viewport-scaled root (`html { font-size: …vw }`)

ERA Residence, Son Daven, bleibtgleich26, Seasats (`.6944vw`, i.e. 10 px at 1440), United Carriers, Squarespace Foundations, Getty Tracing Art and Koto set the root font size in `vw`, so the whole UI scales like a Figma frame.

This is a common Webflow/agency habit. It is also [WCAG failure F94](https://www.w3.org/WAI/WCAG22/Techniques/failures/F94): text sized in viewport units does not grow with browser zoom ([Roselli](http://adrianroselli.com/2019/12/responsive-type-and-zoom.html)). Squarespace Foundations is the partial exception; it clamps the root: `clamp(13px, 1.46484375vw, 14px)`.

**Rule:** never set the root in `vw`. Fluid-size individual steps with a `rem` term and clamps.

### 4.3 Recommended tokens (tested in Chromium 152 at 1440 and 390)

```css
:root {
  /* max ≤ 2.5 × min → passes WCAG 1.4.4 at any zoom per Barvian's analysis */
  --step-hero: clamp(3.5rem, 1.9rem + 6.3vw, 8.75rem);    /* 56px @390 · 121px @1440 · max 140 */
  --step-h2:   clamp(2.25rem, 1.5rem + 3.2vw, 5.5rem);    /* 36px · 70px · max 88 */
  --step-h3:   clamp(1.5rem, 1.2rem + 1.2vw, 2.5rem);     /* 24px · 36px · max 40 */
  --step-lead: clamp(1.125rem, 1rem + 0.5vw, 1.5rem);     /* 18px · 23px */
  --step-body: clamp(1rem, 0.95rem + 0.2vw, 1.1875rem);   /* 16px · 18px */
  --step-meta: 0.8125rem;                                  /* 13px captions */

  --lh-display: 0.9;   /* 1–2 line display; 0.78–0.85 only for single-line words */
  --lh-heading: 1.05;
  --lh-body: 1.5;      /* WCAG 1.4.8 (AAA) asks ≥1.5 */
  --measure: 65ch;     /* WCAG 1.4.8: no more than 80 characters */
}
h1, .display { font-size: var(--step-hero); line-height: var(--lh-display); letter-spacing: -0.03em; text-wrap: balance; max-width: 14ch; }
h2 { font-size: var(--step-h2); line-height: var(--lh-heading); letter-spacing: -0.02em; text-wrap: balance; }
p  { font-size: var(--step-body); line-height: var(--lh-body); max-width: var(--measure); text-wrap: pretty; }
```

Measured in the test page:
- At 1440: hero 121.12 px, h2 70.08 px, body 18.08 px.
- At 390: hero 56 px, h2 36.48 px, body 16 px.
- No horizontal overflow at 390.

`text-wrap: balance` is Baseline 2024 (Chrome 114, Firefox 121, Safari 17.5). `text-wrap: pretty` is Chromium and Safari 26 only; Firefox ignores it harmlessly ([web-features 3.40.0](https://cdn.jsdelivr.net/npm/web-features@3.40.0/data.json)).

Sources: the 2.5× rule is from [Smashing (Barvian, 2023)](https://www.smashingmagazine.com/2023/11/addressing-accessibility-concerns-fluid-type/). Measure and leading are from [WCAG 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html).

Poster type beyond 2.5× (winners go to 3–6×, for example Matteo's 160 → 368 px) must be either:
- (a) a logotype: an image of text, exempt from 1.4.4, with the same words present as real text elsewhere; or
- (b) zoom-tested at 200% across 1024–2560 px widths.

### 4.4 Tracking and leading by size

| Size | Grotesk tracking | Serif tracking | Leading |
|---|---|---|---|
| ≥ 200 px (wordmark/poster) | −0.04 to −0.065em | −0.01 to +0.02em | 0.78–0.85 (single line) |
| 100–200 px | −0.03 to −0.05em | 0 to −0.01em | 0.85–0.95 |
| 48–100 px | −0.02 to −0.03em | 0 | 0.95–1.05 |
| 24–48 px | −0.01 to −0.02em | 0 | 1.1–1.2 |
| 16–20 px body | 0 | 0 | 1.45–1.6 |
| 11–14 px uppercase labels | +0.04 to +0.1em | +0.04 to +0.08em | 1.2–1.3 |
| Condensed uppercase display | 0 to +0.06em | — | 0.85–0.9 |

- The range ends come from §4.1: 14islands −0.05em at 283 px, Matteo −0.065em at 368 px, Oryzo +0.018em serif at 216 px, Project Cult +0.06em for condensed caps.
- **Limit:** stop tightening when counters or joins start to touch, or when a separator (·, /, :) gets buried (law: "Cramped display type").
- **Accessibility:** WCAG 1.4.12 requires layouts to survive user overrides of line-height 1.5 and letter-spacing 0.12em ([Understanding 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)). Fixed-height line masks and `overflow: clip` boxes around text fail that; give them room or size them in `em` with padding.

---

## 5. Pairing logic

1. **One voice, one companion, optional data mono.** A superfamily is the strongest form:
   - Die Grotesk B/C/D across widths ([Trevor Noah](https://www.awwwards.com/sites/trevor-noah)).
   - Season Sans + Season Mix ([Seasats](https://www.awwwards.com/sites/seasats)).
   - Clarkson + Clarkson Serif + Condensed ([Squarespace Foundations](https://www.awwwards.com/sites/squarespace-foundations)).
   - Suisse Int'l + Mono ([Aspen Search](https://www.awwwards.com/sites/aspen-search)).
   - BT Steinhart + Mono ([United Carriers](https://www.awwwards.com/sites/united-carriers)).
   - This matches the law's "one type voice … optical sizes are ideal".
2. **Contrast on one axis only.** Examples: serif display with sans text (Lay Grotesk + Teodor on [Gionatan Nese](https://www.awwwards.com/sites/gionatan-nese-26); Graphik + Bradford on [Getty](https://www.awwwards.com/sites/tracing-art)), or width (Owners Wide display on LXL Creative), or weight. Change one axis, not three.
3. **The display face carries identity; the text face stays quiet.** The body may be `system-ui` (law). Never pair two characterful display faces; they argue. Brier + Mona Sans works on [Lando Norris](https://www.awwwards.com/sites/lando-norris) because Mona Sans is set as neutral UI.
4. **Match x-height and colour when two families share a line.** Use `font-size-adjust` (Baseline 2024: Chrome 127, Firefox 118, Safari 17; [web-features](https://cdn.jsdelivr.net/npm/web-features@3.40.0/data.json)) to lock the italic or serif to the roman's x-height, so the mixed line reads as one texture.
5. **Mono only on tokens that are data.** Wrap them (`<time>`, `<data>`, prices, coordinates) rather than switching whole labels to mono.
6. **Different roles get different treatments.** The law bans one tracked-caps costume on eyebrow, button, figure numbers, nav and colophon alike. For example:
   - nav: text face 15 px medium;
   - captions: text face 13 px, tonal colour;
   - data: mono;
   - only one role gets uppercase tracking.
7. **No house pairing across projects.** Check previous builds before choosing (law rule 2).

To get an x-height aspect for `font-size-adjust` (fontTools 4.66.0 on PyPI; WOFF2 input needs `brotli`):

```python
from fontTools.ttLib import TTFont
f = TTFont("display-italic.woff2")
print(f["OS/2"].sxHeight / f["head"].unitsPerEm)          # e.g. 0.49 → font-size-adjust: 0.49
print([(a.axisTag, a.minValue, a.defaultValue, a.maxValue) for a in f["fvar"].axes] if "fvar" in f else "static")
```

---

## 6. Signature type moves: recipes

All snippets below were assembled into one test page (`evidence/typo/demo.html`) and run in Chromium 152 (Claude preview browser) at 1440×900 and 390×844 with zero console errors. Not tested in Safari or Firefox.

Baseline data is from [MDN BCD 8.1.3](https://cdn.jsdelivr.net/npm/@mdn/browser-compat-data@8.1.3/data.json) and [web-features 3.40.0](https://cdn.jsdelivr.net/npm/web-features@3.40.0/data.json), both fetched 2026-09-24. Current stable versions per BCD: Chrome 154, Firefox 156, Safari 27.

### 6.1 Giant cropped wordmark (footer or hero)

Observed:
- Superhuge `[data-site-footer-word]` at 467 px, leading .78.
- NOHO `.footer-slogan` at 15.625vw, −0.04em.
- DKTON `.footer_mark` at 9vw, leading .78.

The law's placement rules:
- centred;
- anchored flush to the bottom edge, bleeding slightly;
- on the layer above texture;
- a deliberate case;
- no gradient inside the type;
- no glyph shaved by the container ("clear the cut").

```html
<footer class="site-foot">
  <nav>…</nav>
  <p class="wordmark" aria-hidden="true"><span>HALDEN</span></p> <!-- brand name also exists as real text/logo in the header -->
</footer>
```

```css
.site-foot { overflow: clip; padding: 3rem 1rem 0; }
.wordmark {
  font-family: var(--font-display); font-weight: 700;
  line-height: 0.8; letter-spacing: -0.04em;
  white-space: nowrap; text-align: center; margin: 0;
  text-box: trim-both cap alphabetic;         /* trims to cap-height + baseline */
  font-size: clamp(4rem, 0.5rem + 19vw, 24rem); /* fallback when nothing else runs */
  margin-block-end: -0.06em;                  /* deliberate bleed; only for words without descenders */
}
@supports (text-fit: grow) {                  /* Chromium 150+, experimental */
  .wordmark { font-size: 4rem; text-fit: grow; }
}
```

```js
// JS fit for engines without text-fit (Safari, Firefox). Measures the inline <span>.
function fitText(el) {
  const word = el.firstElementChild;
  let lastW = 0;
  const fit = (force = false) => {
    const box = el.clientWidth;
    if (!box || (!force && box === lastW)) return;
    lastW = box;
    el.style.fontSize = "100px";
    el.style.fontSize = (100 * box / word.getBoundingClientRect().width) * 0.995 + "px";
  };
  new ResizeObserver(() => fit()).observe(el);
  document.fonts.ready.then(() => fit(true));   // re-measure with the real font, not the fallback
}
if (!CSS.supports("text-fit", "grow")) document.querySelectorAll(".wordmark").forEach(fitText);
```

Support (BCD 8.1.3):
- [`text-fit`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-fit): Chrome 150+ only, experimental. Syntax is `grow | shrink [consistent | per-line | per-line-all] [<percentage>]`.
- [`text-box`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box): Chrome 133, Safari 18.2, Firefox 154. web-features 3.40.0 still lists it as non-Baseline without Firefox, so recheck.

Test result: `text-fit: grow` filled 1393/1393 px at 1440. The JS path filled 1386/1393 px. At 390 it filled 356/358 px.

Failure modes:
- `text-box: … cap` trims diacritics (Á, Ø) and the container then clips them. Trim to `text` for accented words.
- A descender word (g, j, p, q, y) with a negative bottom margin gets its tails cut off.
- Zoom into the clipped edge before calling it done.

### 6.2 Split-line masked reveal, law-compliant

Winners use GSAP SplitText everywhere (9 winner homepages reference it). The law's constraint: the text must be readable if JS, fonts or the timeline never run.

The hero pattern below:
- (a) hides nothing in CSS;
- (b) splits only when motion is allowed;
- (c) returns the tween so `autoSplit` re-splits after fonts load or the width changes;
- (d) forces completion after 2.5 s if the tween stalls.

GSAP is [free for commercial use including SplitText](https://gsap.com/community/standard-license/) since 3.13 ([release note](https://github.com/greensock/GSAP/commit/9f8eca1cc21cab9fc41fa1a3edb984d7ef02fd89)). The current npm version is 3.15.0 (2026-04-13). The license prohibits use inside visual no-code animation builders that compete with Webflow.

```html
<h1 class="hero-title" data-split>Quiet machines for loud cities</h1>
```

```css
.hero-title { text-wrap: balance; max-width: 14ch; }           /* visible by default: no opacity, no transform */
.hero-title .line-mask { padding-block: 0.08em; margin-block: -0.08em; } /* mask never shaves ascenders/descenders */
@media print { .hero-title .line { transform: none !important; } }
```

```js
import { gsap } from "gsap";
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(SplitText);

const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-split]").forEach((el) => {
    SplitText.create(el, {
      type: "lines",
      mask: "lines",          // v3.13+: wrapper with clip; class becomes "line-mask"
      linesClass: "line",
      autoSplit: true,        // re-split on font load / width change
      onSplit(self) {
        const tween = gsap.from(self.lines, { yPercent: 100, duration: 0.9, ease: "expo.out", stagger: 0.08 });
        const guard = setTimeout(() => tween.progress(1), 2500);   // never park text under its mask
        tween.eventCallback("onComplete", () => clearTimeout(guard));
        return tween;         // lets SplitText clean up and re-sync on re-split
      },
    });
  });
});
```

API behaviour ([SplitText docs](https://gsap.com/docs/v3/Plugins/SplitText) via Context7):
- `aria: "auto"` is the default. It adds `aria-label` to the element and `aria-hidden` to the line wrappers. Test result: the label was set to the full sentence, 3 lines at 390 px and 2 at 1440, all transforms at identity after 3.5 s.
- For text containing links, use `aria: "none"` plus a visually hidden copy.

Below the fold, **do not** hide lines until a ScrollTrigger fires; screenshot passes and print never fire it. Let already-visible lines settle instead:

```js
gsap.from(self.lines, { y: "0.35em", duration: 0.8, ease: "power3.out", stagger: 0.06,
  scrollTrigger: { trigger: el, start: "top 85%", once: true } });   // no opacity, no mask: always legible
```

Observed anti-pattern: Trevor Noah (SOTD) sets `[data-module='split'] { opacity: 0 }` and shows the text only under `html.is-ready`. If JS fails, the headline never appears.

### 6.3 Variable-axis animation on scroll and hover

Use the high-level properties (`font-weight` for `wght`, `font-stretch` for `wdth`). Keep `font-variation-settings` for custom axes such as Zimula's `cnct` or Season's `SERF`. [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variation-settings) calls it a low-level mechanism that overrides the basic properties.

Declare the real axis ranges in `@font-face`, or the browser clamps or synthesises.

```css
@font-face {
  font-family: "Mona Sans";
  src: url("/fonts/mona-sans-latin-wdth-normal.woff2") format("woff2");  /* @fontsource-variable/mona-sans 5.3.0 */
  font-weight: 200 900; font-stretch: 75% 125%; font-display: swap;
}
.kinetic { font: 400 var(--step-h2)/1 "Mona Sans", system-ui, sans-serif; }
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .kinetic { animation: weight-in linear both; animation-timeline: view(); animation-range: entry 0% cover 50%; }
  }
}
@keyframes weight-in { from { font-weight: 250; font-stretch: 125%; } to { font-weight: 800; font-stretch: 75%; } }

/* custom axis: register it so it interpolates */
@property --serf { syntax: "<number>"; inherits: true; initial-value: 0; }
.morph { font-variation-settings: "SERF" var(--serf); transition: --serf .6s ease; } /* axis tag per the font's fvar */
.morph:hover { --serf: 100; }
```

- Scroll-driven animations: Chrome 115+ and Safari 26+; Firefox is preview only in BCD 8.1.3, so Firefox users get the static state (still readable).
- `@property`: Baseline 2024 (Chrome 85, Firefox 128, Safari 16.4).
- Test result: in Chromium 152 the view timeline drove weight 250 → 800 and width 125% → 75%.

Pointer-proximity weight (desktop, short strings only; every frame reflows the line):

```html
<h2 class="proximity"><span class="sr-only">Built to be touched</span><span class="proximity-glyphs" aria-hidden="true">Built to be touched</span></h2>
```

```js
const prox = document.querySelector(".proximity-glyphs");
if (prox && matchMedia("(pointer: fine) and (prefers-reduced-motion: no-preference)").matches) {
  const chars = [...prox.textContent].map((c) => { const s = document.createElement("span"); s.textContent = c; return s; });
  prox.replaceChildren(...chars);
  let px = -1e4, py = -1e4, raf = 0;
  addEventListener("pointermove", (e) => { px = e.clientX; py = e.clientY; raf ||= requestAnimationFrame(tick); });
  function tick() {
    raf = 0;
    const centers = chars.map((s) => { const r = s.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }); // read all, then write
    centers.forEach(([x, y], i) => {
      const t = Math.max(0, 1 - Math.hypot(px - x, py - y) / 240);   // 240px radius
      chars[i].style.fontWeight = String(Math.round(300 + t * 600));  // 300 → 900
    });
  }
}
```

Do not rely on `aria-label` on a `<p>` or `<span>`. Some roles prohibit naming, and in practice `aria-label` is supported only on interactive elements, widgets, landmarks, images and iframes ([MDN](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-label)). Use the visually hidden copy.

### 6.4 Text on a path

```html
<svg class="orbit" viewBox="0 0 400 400" aria-hidden="true">
  <defs><path id="ring" d="M200,200 m-160,0 a160,160 0 1,1 320,0 a160,160 0 1,1 -320,0"/></defs>
  <text><textPath href="#ring" textLength="1005">Open studio · Fridays 18:00 · Kreuzberg · </textPath></text>
</svg>
```

```css
/* font-size is in viewBox units: rendered px = 24 × (svgWidth / 400) → ≥11.5px at the 12rem floor */
.orbit { width: clamp(12rem, 40vw, 22rem); font: 500 24px/1 var(--font-text); letter-spacing: 0.06em; fill: currentColor; }
@media (prefers-reduced-motion: no-preference) { .orbit { animation: spin 30s linear infinite; } }
@keyframes spin { to { rotate: 1turn; } }
```

- Rotate the whole `<svg>` (compositor-friendly) rather than animating `startOffset` every frame.
- `textLength` = 2πr (1005 for r = 160) closes the loop. The default `lengthAdjust="spacing"` only spaces glyphs; never use `spacingAndGlyphs`, which distorts letterforms.
- For scroll-linked flow along an open curve: `gsap.to(textPath, { attr: { startOffset: "-40%" }, scrollTrigger: { scrub: true } })`.
- Support (BCD): `textPath href` Chrome 50, Firefox 2, Safari 12.1. The `path` and `side` attributes are Firefox-only, so reference a `<path>` by id.
- Test result: legibility at 390 was below 6 px until the text was re-sized in viewBox units. Always check the smallest rendered width.

### 6.5 Marquee ticker

Observed: Lando Norris and Paul Kalkbrenner use `.marquee-advanced__item { font-size: max(4em, 8vw) }` (115 px at 1440, 64 px at 390). The Ride nominee uses `clamp(40px, 6.5vw, 96px)`. It is an animation of content already on screen, which the law explicitly allows. WCAG 2.2.2 still requires a pause mechanism for motion that lasts more than 5 s beside other content ([Understanding 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)); hover-pause alone does not cover touch or keyboard users.

```html
<div class="marquee" data-marquee>
  <div class="marquee__track">
    <ul class="marquee__group"><li>Arkiv</li><li>Nordlys</li><li>Halden</li><li>Vale</li></ul>
    <ul class="marquee__group" aria-hidden="true"><li>Arkiv</li><li>Nordlys</li><li>Halden</li><li>Vale</li></ul>
  </div>
</div>
<button type="button" data-marquee-toggle aria-pressed="false">Pause ticker</button>
```

```css
.marquee { overflow: clip; --gap: 0.5em; font: 500 clamp(2.5rem, 1.5rem + 4vw, 6rem)/1.1 var(--font-display); }
.marquee__track { display: flex; width: max-content; gap: var(--gap); }
.marquee__group { display: flex; gap: var(--gap); margin: 0; padding: 0; list-style: none; }
@media (prefers-reduced-motion: no-preference) {
  .marquee__track { animation: marquee var(--dur, 40s) linear infinite; }
  .marquee:is(:hover, :focus-within) .marquee__track,
  .marquee[data-paused] .marquee__track { animation-play-state: paused; }
}
@media (prefers-reduced-motion: reduce) {           /* static, wrapped, no duplicate */
  .marquee__track { flex-wrap: wrap; width: auto; }
  .marquee__group[aria-hidden] { display: none; }
}
@keyframes marquee { to { translate: calc(-50% - var(--gap) / 2) 0; } }   /* one group + one gap = seamless */
```

```js
for (const m of document.querySelectorAll("[data-marquee]")) {           // constant speed at any width
  const g = m.querySelector(".marquee__group");
  new ResizeObserver(() => m.style.setProperty("--dur", g.offsetWidth / 80 + "s")).observe(g); // 80 px/s
}
for (const b of document.querySelectorAll("[data-marquee-toggle]")) {
  b.addEventListener("click", () => {
    const paused = b.previousElementSibling.toggleAttribute("data-paused");
    b.setAttribute("aria-pressed", String(paused));
    b.textContent = paused ? "Play ticker" : "Pause ticker";
  });
}
```

- **Speed:** 60–100 px/s for display-size tickers; slower on phones.
- **Tell to avoid:** the logo-strip marquee of fake client names. Law: logos must be real and earned.

### 6.6 Mixed italic and roman in one line

Observed:
- Hobro sets PP Neue Montreal with Freight Big Pro Light Italic, outlined via `-webkit-text-stroke: 1px`.
- The Tie-break uses Instrument Serif Italic (slop list).
- The Matteo Vincenti nominee styles `.hero-statement em` at up to 28rem.

The law allows **one** emphasis inside a one- or two-line headline, shown as a **tonal** shift, never a saturated pop. A dangling accent word at the foot of a three- or four-line stack is a tell.

```css
@font-face { font-family: "Display"; src: url(/fonts/display-regular.woff2) format("woff2"); font-weight: 400; font-style: normal; font-display: swap; }
@font-face { font-family: "Display"; src: url(/fonts/display-italic.woff2)  format("woff2"); font-weight: 400; font-style: italic; font-display: swap; }
.headline { font-family: "Display", serif; font-synthesis: none; }  /* no faux italics or bold, ever */
.headline em {
  font-style: italic;
  font-size: 1.04em;                  /* many italics read smaller; tune by eye, 1.00–1.06 */
  color: color-mix(in oklab, currentColor 62%, var(--bg));   /* tonal, not an accent swatch */
}
/* cross-family italic (e.g. grotesk roman + serif italic): lock x-heights */
.headline--mixed em { font-family: "Serif Italic", serif; font-size-adjust: 0.49; } /* = roman's sxHeight/UPM */
```

`font-synthesis` is Baseline widely available. Without it, a missing italic file silently becomes an oblique roman.

### 6.7 Numbers and indices

Observed across the stylesheets:
- `font-feature-settings: "zero" 1` (63 declarations, all on the Unimatic nominee).
- `"case" on` (18).
- `font-variant-numeric: tabular-nums` (17).
- Stylistic sets such as `"ss01"` on bleibtgleich26, anime.js, Stripe and basement.studio.

```css
.stat   { font-variant-numeric: tabular-nums lining-nums; }            /* counters, prices, tables: no jitter */
.code   { font-variant-numeric: slashed-zero; }                        /* IDs, serials */
.caps   { font-feature-settings: "case" 1; }                           /* lifts ( ) - : to cap height in ALL CAPS */
.footnote-ref { font-feature-settings: "sups" 1; }                     /* only if the font has real superiors */

/* Index number cap-aligned to a big title: trim both boxes to cap height, then align tops */
.item { display: flex; align-items: flex-start; gap: 0.5rem; }
.item h3, .item .idx { margin: 0; text-box: trim-both cap alphabetic; }
.item .idx { font-size: 0.8125rem; font-variant-numeric: tabular-nums; }
```

- Test result: the index top and the 70 px title top landed on the same pixel row (1702 px) in Chromium 152.
- Do not rely on `font-variant-position: super`. BCD lists Chrome 117 and Safari 9.1, but web-features marks it non-Baseline with Firefox-only support, so treat it as unreliable (unverified which engines synthesize).
- Law: "01 / 02 / 03" steps beside a vertical rail is a slop layout. Indices belong on real lists (projects, chapters, archive entries).

### 6.8 Captions and meta: mono only on the data

```css
.meta { font: 400 var(--step-meta)/1.35 var(--font-text); font-variant-numeric: tabular-nums;
        color: color-mix(in oklab, currentColor 62%, var(--bg)); }
.meta :is(time, data, .coord) { font-family: var(--font-mono); font-size: 0.95em; letter-spacing: 0; }
.label-caps { font-variant-caps: all-small-caps; letter-spacing: 0.06em; } /* real smcp only; one role, not all */
```

```html
<p class="meta">Harbour Lab · <time datetime="2026-03-14">14.03.26</time> · <data value="59.91">59.91° N</data></p>
```

### 6.9 Hover: the character roll (instead of underline-fill or "boop")

Observed on Paul Kalkbrenner (SOTD) and the DKTON nominee. Each character carries a `text-shadow` copy 1.25em below and translates up on hover, with a per-character delay: `calc((var(--char) - var(--button-index-offset)) * var(--button-char-offset))`. The law bans growing underlines and translate or scale lifts on buttons; a clipped roll changes state without moving the box.

```css
.roll { display: inline-block; overflow: clip; line-height: 1.2; color: inherit; text-decoration: none; }
.roll__text { display: inline-block; text-shadow: 0 1.2em currentColor; transition: translate .45s cubic-bezier(.2,.7,.2,1); }
@media (hover: hover) and (prefers-reduced-motion: no-preference) {
  .roll:is(:hover, :focus-visible) .roll__text { translate: 0 -1.2em; }
}
.roll:focus-visible { outline: 2px solid currentColor; outline-offset: 4px; }   /* keep a real focus ring */
```

For a per-character stagger, split with SplitText `type: "chars"` and set `--char` on each character. Use it on nav and a single CTA only; on every link it becomes the new template tic.

---

## 7. Mobile type adaptation

1. **Floors, not pure `vw`.** Winners that declare pure `vw` collapse to 24–60 px at 390 unless a media query rescues them. The careful ones clamp:
   - Lama Lama 52 px.
   - Floema 80 px.
   - Shopify 120 px.
   - Hobro 120 px.
   - Matteo 160 px.
   - Superhuge 256 px.
2. **Count lines at 390.** In the test page, "Quiet machines for loud cities" ran to 3 lines at 56 px and 14ch; the law says 3+ stacked lines is slop. Shorten the copy, widen the measure to 16–18ch, or drop one step. Do not just shrink until it fits.
3. **Loosen as you shrink.** Take tracking from −0.04em (desktop) to about −0.02em (mobile) and leading from 0.85 to about 0.95. Tight settings that work at 200 px clog at 50 px.
4. **Use the width axis before the size axis.** A long single word can switch to a narrower `font-stretch` (e.g. 87.5%) on phones instead of losing size. For the rare giant word, `hyphens: auto` with a correct `lang` beats overflow. Never let a word force horizontal scroll (the test page kept `scrollWidth` at 390).
5. **Keep the wordmark fit-to-width** (text-fit or JS). Under a fixed `vw` it either overflows or dwindles.
6. **Give hover type a touch equivalent.** Proximity and roll effects are gated on `(hover: hover)` or `(pointer: fine)`; touch users get the static state. Tie variable-axis motion to scroll on phones, if anything.
7. **Size floors:** body 16 px minimum, captions and meta 12–13 px minimum, marquee text 40 px minimum (the clamp above floors at 2.5rem).
8. **Prevent iOS text inflation** with `-webkit-text-size-adjust: 100%` (Tailwind preflight ships it; observed on Decathlon, Superhuge and Kott). BCD lists `text-size-adjust` as Chromium-only; the `-webkit-` prefix is the one Safari reads (unverified in BCD).

---

## 8. Loading display fonts without layout shift

```html
<link rel="preload" href="/fonts/display-var.woff2" as="font" type="font/woff2" crossorigin>
```

```css
@font-face {
  font-family: "Display";
  src: url("/fonts/display-var.woff2") format("woff2");
  font-weight: 200 900; font-style: normal;
  font-display: swap;                 /* hero must show text immediately; the fallback below prevents the jump */
}
@font-face {                          /* metric-matched fallback */
  font-family: "Display Fallback";
  src: local("Arial");
  size-adjust: 104%;                  /* measure per font (Capsize metrics / fontaine) */
  ascent-override: 92%; descent-override: 24%; line-gap-override: 0%;
}
.display { font-family: "Display", "Display Fallback", system-ui, sans-serif; }
```

- **Preload** only the 1–2 files above the fold. Self-host WOFF2; every foundry above licenses `@font-face` self-hosting, and Dinamo forbids desktop formats like OTF for live web text.
- **Fallback metrics.** `size-adjust` is supported in Chrome 92, Firefox 92 and Safari 17. `ascent-override` and `descent-override` are Chrome 87 and Firefox 89 only; Safari is preview in BCD. So Safari gets width matching but not vertical metric matching; leave vertical slack.
- **Next.js** `next/font/local` generates these fallbacks automatically. The `"ppMori Fallback"`, `"seasonMix Fallback"` and `"suisseIntl Fallback"` families observed on BOC Studio, Seasats and Aspen Search are its output ([Next.js docs](https://nextjs.org/docs/pages/api-reference/components/font), `adjustFontFallback` defaults to `'Arial'` for local fonts).
- **Other stacks** (npm, checked 2026-09-24): `fontaine` 1.0.0, `@capsizecss/metrics` 4.3.0, `subfont` 7.3.0, `glyphhanger` 6.0.0.
- **Subset only where the licence allows it.** Dinamo allows it explicitly. Production Type forbids user modification. Swiss Typefaces ships its own WebS/WebM/WebXL subsets. Check the others in their EULA.
- **Split text only after `document.fonts.ready`.** SplitText's `autoSplit` handles this; otherwise the lines are computed on fallback metrics.

---

## 9. Failure modes (seen in the sample or implied by the data)

| Failure | Where seen | Fix |
|---|---|---|
| Content hidden until JS adds a class | Trevor Noah `[data-module='split']{opacity:0}` until `html.is-ready` | Visible by default; motion from a visible state; a 2.5 s completion guard (§6.2) |
| Trial or pirated font files in production | Cerebrium ("ABC Favorit Trial"), White Desert (`…-Trial.woff2`), Stanzza nominee (`ofont.ru_…`) | Licence at build time; grep production CSS for `Trial`, `Test`, `Demo` and mirror-site names |
| Root font size in `vw` (the whole UI ignores zoom) | ERA Residence, Son Daven, Seasats, United Carriers, Getty and others | `rem` root; fluid steps with a `rem` term; max ≤ 2.5× min or zoom-test |
| Slop-listed faces carrying the brand | Tie-break (Instrument Serif + Work Sans), SharpLink (Archivo), Illoca declares Space Grotesk and Syne | License or self-host a distinctive face (§2) |
| Mono as house voice | Terminal Industries (mono is the top family variable), AI in Design (Fragment + Geist Mono) | Mono on data tokens only (§6.8) |
| Too many families | Why Zero (9 declared), Illoca (10) | One voice + one companion; audit unused `@font-face` |
| Underline-grow nav hover | Matteo Vincenti nominee `.nav-link:after{transform:scaleX(0)}` → `scaleX(1)` | Tonal state change or the roll (§6.9) |
| Glyphs shaved by masks and `line-height < 1` | risk on every split-line and wordmark | Mask padding 0.08em; `text-box` trim; zoom-check the clipped edge |
| Faux italic or bold | any site missing a style file | `font-synthesis: none`, ship the real cut |
| Unregistered axes (`font-variation-settings` without ranges in `@font-face`) | — | Declare `font-weight: 200 900` and `font-stretch: 75% 125%` ranges matching `fvar` (§5 snippet) |
| Ticker with no pause control | common | Pause button + reduced-motion static fallback (§6.5) |
| SVG path text illegible on phones | found in this file's own test | Size text in viewBox units against the smallest rendered SVG width |
| Desktop font formats served to browsers | Son Daven serves KTF Metro as `.otf`; Siena serves NB International, Neue Brücke and P22 Parrish as `.ttf` | Serve WOFF2 only. Dinamo's EULA forbids desktop formats for live web text |
| Hidden scrollbars | Trevor Noah (`scrollbar-width: none` on html and body) | Keep native scrollbars or restyle them; never remove them |
| Pangram licence silently lapses | Pangram's EULA term is 1 year | Put renewal in the handoff doc; or pick a perpetual foundry (Displaay, Swiss Typefaces, Blaze, Klim) |

---

## Retrieval gaps

- **Awwwards site pages no longer list fonts or colours** in their server HTML. Fonts were inferred from live CSS only. Faces loaded inside JS bundles, canvas or WebGL were missed. Three winners could not be extracted: The Tuscan Journey (canvas), Cartier Watches & Wonders (JS) and Navigate (HTTP 525).
- **SOTM award status** comes from the SOTM listing page. The scraped individual site pages showed only "Site of the Day" strings. The Awwwards `annual-awards-2025` page is a JS shell, so Site of the Year 2025 winners were not verified.
- **Mobile sizes (390 px)** are computed from single declarations without applying media queries. Real mobile sizes may differ where marked `*`.
- **Role labels** (display, text, mono) are inferred from how often each family is used in CSS, not from rendered screenshots.
- **Foundry not verified:** Novela, Scribo Rough Pro, Champ, Hello Organichand, STK Bureau Serif, PS Times, HW Cigars, Selfso Sans (Superhuge nominee), AS Module/AS Therma (darkroom), Freight Big Pro's current publisher, Altesse Std. PP Locomotive New is assumed to be a Pangram custom from its `PP` file prefix.
- **Licence terms not extracted:** 205TF's EULA (JS-rendered page); Colophon (only a third-party summary); Due Studio, Lineto, Berthold, Milieu Grotesque, Neubau and Type Department licence metrics; Pangram's subsetting rule; Grilli's subsetting rule.
- **Axis ranges not verified:** ABC Diatype Plus Variable, GT Flexa width and Mona Sans `wdth`. The test used `font-stretch: 75% 125%`, which rendered, but I did not read the file's `fvar`.
- **Browser coverage of the recipes:** Chromium 152 only. Not tested in Safari or Firefox, including the JS text-fit fallback in real Safari, `text-box` in Firefox 154+ and SVG `textLength` rendering.
- **`text-box` Baseline status:** BCD 8.1.3 lists Firefox 154, while web-features 3.40.0 still marks it non-Baseline. Recheck before relying on it without a fallback.
- **Mona Sans on Google Fonts:** its presence there, and so its status under law rule 1, is unverified.
- **Fonts In Use:** only Typewolf was usable as a trend source; I found no usable year-level aggregate for web use on Fonts In Use.
