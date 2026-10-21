# Art direction: what winning sites look like, and how to choose

## Observed patterns in 2026 winners (probed live: screenshots, computed styles, scripts)

Sites: Jesper Landberg, Gil Huybrecht, Maria Vasilyeva, Boc.Studio, LxL Creative, Noho, Meer
Mohsin (recent SOTDs) and Lando Norris (SOTY 2025), Locomotive, Immersive Garden, Obys, Unseen,
Basic/Dept, Dogstudio, Studio Freight, Cerebrium.

- **Type does the work.** One neo-grotesk carries almost everything (Neue Montreal, PP Mori,
  Helvetica Now, Suisse Intl, Scto Grotesk, Mona Sans, Switzer), often with ONE contrasting voice:
  a serif (Saol Display, PS Times, GT Sectra, Brier), a script/handwriting accent (LxL, Maria
  Vasilyeva's "Scroll" scribble), or a mono for data. Display sizes run from 60 px to 200+ px with
  tracking around -0.02 to -0.05em and leading 0.85 to 1.0.
- **UI text is small and confident.** Nav, meta and captions at 11 to 16 px in the corners. The
  "four corners" frame (name top-left, nav top-right, context bottom-left, action bottom-right) is
  a standard of the genre.
- **Color comes from the work.** Most winners are monochrome (#000/#fff or near) and let imagery
  bring color; others commit to one bold field color (Boc's red band, Meer's blood red #990000,
  Lando's acid yellow-green on off-white). Pure black and white are common; that is fine.
- **WebGL is standard, not special.** 6 of 7 recent SOTD portfolios render a WebGL canvas; the
  stack is Lenis + GSAP (+ SplitText) + OGL or Three. What differs is how meaningfully it is used.
- **A loader on first visit** (counter, bar, or logo build), short, then a choreographed handoff.
- **Index-style work presentation** is everywhere: lists with hover previews (Obys), grids of real
  screenshots (Gil Huybrecht), 3D carousels (Jesper Landberg), filmstrips.
- **Personality through one unexpected element:** a handwritten annotation layer, a sound toggle,
  a playful consent message (Boc), a mascot, a coordinate strip that is actually their address.
- **Native cursor kept** everywhere (see Interaction patterns below). Followers add, never replace.

## Interaction patterns (probed live Oct 2026: pointer moved onto targets, styles and pixels compared)

Sites: Cuberto, Immersive Garden, Rejouice, 14islands, Lando Norris, GSAP, Inkfish, Locomotive,
Obys, Unseen, Dogstudio, basement.studio, Darkroom, Lusion, Justine Soulié, Aristide Benoist,
plus Oct 2026 SOTDs twks, Tengile Malamala and Aevion (Riotters).

Read this as a vocabulary of mechanisms (the inner span moves, a fill floods, an arrow travels),
not as a catalogue. The named hovers are those studios' signatures: take the mechanism, restyle
it in your motion verb, and never copy one as seen.

- **Something moves at rest.** On 16 of 19, pixels kept changing with the pointer still: WebGL
  scenes, video, drifting shapes (Lando's topographic lines), slow type. Almost always it is
  the concept itself moving, not a decoration added on top. A still page is the exception.
- **Native cursor kept on 19 of 19.** A follower appeared on 4 (Cuberto, Immersive Garden,
  Inkfish, Tengile): a small dot that grows or shows a word ("Click" on Immersive Garden).
  Followers are a choice, not a requirement, and they add to the native cursor, never replace it.
- **Primary targets move; utility links may only change color.** CTAs and project links move or
  transform. Cookie, legal, social and sometimes secondary nav links just change color
  (Tengile's cookie bar, Dogstudio's social links, GSAP's top nav). Nobody spends motion on a
  privacy link.
- **The inner text moves, not the box.** The most common hover changes the transform of a
  child span: a letter roll or a slide inside a clipped line (Cuberto nav, 14islands nav, Lando
  "Store", Immersive Garden "See all projects"). A finished roll looks identical to rest, which
  is why it reads as craft rather than as a state change.
- **Fills invert or flood.** Cuberto's black "Contacts" pill turns into an outline as the
  follower dot lands on it, and the button leans toward the pointer (the only magnetic pull
  noted in this probe). GSAP's outlined "Get GSAP" fills cream. Tengile's "Explore Collection"
  floods olive and its arrow chip turns into a circle.
- **Arrows travel.** Rejouice moves the ↗ of "Learn more" from the end of the label to the
  start. Most arrow links nudge along their direction.
- **Underlines draw.** twks and Locomotive draw an underline under nav links. Darkroom toggles
  `text-decoration`.
- **Type changes axis.** Inkfish shifts a variable font's `font-variation-settings` on its mono
  nav and adds a square marker to the hovered item.
- **Hover reveals media.** twks's "contact" opens a moving image behind the word. Immersive
  Garden lifts the white relief behind the link. Index lists with a floating preview (Obys)
  belong to the same family.

## Archetypes (starting points; mutate them with the concept)

| Archetype | Ground / ink / accent | Type | Motion | Fits |
|---|---|---|---|---|
| Swiss index | #f4f4f4 / #0e0e0e / one saturated (e.g. #ff3b00) | one neo-grotesk, 2 weights | precise, short, line reveals | designers, studios, devs |
| Gallery dark | #0a0a0a / #ededed / none, imagery is color | grotesk + serif italic accent | slow, cinematic, GL images | photographers, 3D, film |
| Field color | one saturated field (cobalt #1f3cff, red #c8102e, yellow #ffd400) / ink | heavy grotesk or wide | bold, snappy, blocks wipe | brands, launches, music |
| Editorial modern | paper white #fafaf7 / near-black / no accent | serif display + grotesk text | settle like paper, masks | writers, architects, culture |
| Tech precise | #0b0d10 / #d8dde3 / signal (e.g. #3df5a8 used sparingly) | grotesk + mono | snap, scramble, compile | dev tools, AI, engineers |
| Warm analog | a specific material color (clay, olive, sky) / ink | humanist or grotesk + script | organic, drift, grain | food, craft, wellness |
| Experimental | anything, but one strict system | one family, extreme scale | physics, drag, play | creative technologists |

## Palette rules

- Write 4 to 6 named roles: `ground`, `ink`, `muted` (secondary text, must pass AA on ground),
  `line` (hairlines, ~10 to 16% ink), `accent` (one, used rarely and meaningfully), `curtain`.
- Derive from the concept's world (a frame: gallery wall white, frame black, label ivory; a contact sheet:
  film black, safelight red). Sample real references mentally; name them in DESIGN.md.
- Dark and light modes are optional for portfolios; a single committed theme is normal for award
  sites. If you do both, both must be designed.
- One color can be a whole-section field; color changes between sections should be motivated
  (a chapter change), and animated (background tween on scroll) rather than hard-cut.

## Defaults to avoid (AI tells), unless the concept genuinely calls for it

1. Warm cream (#F4F1EA family) + high-contrast serif + terracotta/clay accent.
2. Near-black + single acid-green or vermilion accent as the whole identity.
3. Broadsheet layout: hairline rules everywhere, zero radius, dense newspaper columns.
4. SaaS card kit: identical rounded cards, the same soft shadow, gradient washes.
5. Template chrome: tracked uppercase eyebrow above every heading, "A · B · C" meta strings,
   "WORD — fragment" labels, mono for every small label, "→" appended to every link.
6. Purple-blue gradient glow, glassmorphism on everything, centered hero over a blob.
7. Inter / Fraunces / Instrument Serif as the reflexive choice.
8. Accenting one word of the headline in italic serif or color as the only typographic idea.

These are defaults, not crimes. If the brief or concept asks for one, do it with conviction and
say why in DESIGN.md.

## Details that separate 7 from 8

- Selection color, scrollbar treatment (or none), focus ring in the system's accent.
- Favicon that matches the identity; OG image composed, not a crop.
- Hover states that belong to the concept (a frame tightening for "Marco", a film advance for "contact sheet").
- Footer as a final composition (big name, real links, local time only if it is meaningful).
- 404 page that carries the concept.
- Numbers set in tabular figures; real typographic quotes and apostrophes; non-breaking spaces
  between numbers and units; no widows in display lines.
- Image treatment consistent: one aspect-ratio family, one reveal, one hover.
