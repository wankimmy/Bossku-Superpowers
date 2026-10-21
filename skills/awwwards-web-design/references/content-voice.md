# Content, copy and storytelling

Last updated: 2026-09-25

Use this when: you are writing any word that will ship (headline, chapter copy, loader, cursor label, 404, consent line, page metadata) or planning the scroll story before layout.

## Rules

1. Write the copy deck before layout: concept sentence, headline set, beat sheet, facts sheet, microcopy sheet, per-route metadata (section 9). Lay the design out around real words. Never lorem.
2. Lead line: 3 to 8 words (median 6 across the 51 teardowns, 43/51 at 8 or fewer), on one or two lines at 390px. If it runs longer, cut words. Do not shrink the type to make it fit.
3. The headline must be true of this brand only. If a competitor could sign it, add the fact that makes it yours (a number, place, date or proper name). Otherwise drop the slogan and lead with the facts (gil-huybrecht).
4. Pick one voice archetype from the direction (section 3, [./directions.md](./directions.md)) and use it on every string, including the loader, cursor labels and 404. Keep a second, plain register for anything the visitor must act on. At least 7 of the 51 winners visibly run two registers.
5. Every chapter carries at least one specific: a number with a unit, a name, a date or a place. Adjectives do not count.
6. Never fabricate testimonials, client logos, awards, metrics, press quotes or people. When a fact is missing, mark it as a draft in the deck. Do not fill the gap with plausible fiction.
7. Tell the scroll in beats: one sentence per beat. Alternate loud and quiet sections (about half the winners do: 26/51 by keyword count), show progress the reader can see, and end on one literal action.
8. All copy ships in server HTML and is visible by default. Motion changes emphasis and position, never whether the text exists. A reveal is a turn in the story, not an opacity fade.
9. Each route gets one h1 that says what the page is (it may be set small), plus its own title, description, canonical and OG image. Any text drawn in WebGL has a real DOM twin.
10. Microcopy is one to three words, verb first, in the site's own world: loader status, cursor labels (only on targets with no text of their own), sound gates, the 404. Buttons stay literal (verb + object) even when the headline above them is a metaphor.
11. The default is no full-screen preloader. If a scene needs one, scope it to the stage, count real asset promises, cap it at 1.5s, and write its status words in the brand's world.
12. Localize natively: `lang` on the page and on inline foreign phrases, a display face that covers every glyph, type steps per language, and localized canvas text.
13. Proofread every string, templated and per-breakpoint copies included. 7 of the 51 winners shipped visible copy defects (section 6).
14. No em dashes (U+2014) in copy, no headlines stacked three or more lines deep, no kicker label over every section head, no filler. Say less.

## 1. What Content buys you

- **Weight.** The jury total is `0.4·Design + 0.3·Usability + 0.2·Creativity + 0.1·Content`, verified on 9 of 9 annual winners [awwwards-editorial §1.2]. A 0.5 gain in Content alone adds 0.05 to the total.
- **It colours the other scores.** Across the 51 teardowns, Content correlates r = 0.55 with Design, 0.49 with Usability and 0.31 with Creativity (computed from each teardown's published sub-scores). Mean Content is 7.77 (range 7.10 to 8.34), against Design 7.83, Usability 7.40 and Creativity 7.98. In the recent corpus (575 sites) the Content mean is 7.48 [stats].
- **The concept is content, but it is scored under Creativity (20%).** A parody launch for a coaster (oryzo-ai, Creativity 8.35), a courier story on a tiny planet (messenger, 8.23), a manifesto you unlock by drawing a zero (why-zero, 8.16): each premise is a sentence before it becomes a scene.
- **What the criterion covers.** Copy, imagery, video and sound. What costs points: stock imagery, lorem, and a beautiful shell around thin copy [awwwards-editorial §1.3]. For imagery rules see [./imagery.md](./imagery.md).
- **The dev jury scores structure.** Semantics/SEO (0.20) and Markup (0.15) are 35% of the Developer Award [usability-a11y-perf §2 H]. Recent means are Semantics 7.23, Markup 7.16 and Accessibility 6.83 [stats]. See section 8.

The two ends of the sample show what scores. The observed copy trait of each site:

| Content score | Site | Copy trait (observed) |
|---|---|---|
| 8.34 | immersive-garden-website | Formal manifesto sentences (a little lofty) carried by a real project list; menu labels extend into full sentences on hover |
| 8.18 | lando-norris | First-person racer voice plus a working fan hub: results, career stats, calendar, store |
| 8.18 | brunos-portfolio | Warm first person, collaborators credited by name, 13 explorable areas |
| 8.15 | messenger | The story is told entirely in quest dialogue and quest cards |
| 8.11 | akaru-2 | French only; one long, rhythmic studio sentence, then the work |
| 8.09 | tracing-art | One dated fact per scroll beat (owner, city, event) |
| 8.09 | the-renaissance-edition | Period pastiche in the visuals, plain product copy, a hard count of updates |
| 7.40 | david-whyte-experience | Poems carry the emotion, but the footer credits line shipped with its name slot empty |
| 7.39 | lama-lama-2 | Self-mocking labels on most small strings |
| 7.13 | lacoste-polo-factory | A one-line heritage welcome, then prize-draw promo copy |
| 7.10 | everswap | Metaphor-only chapters, no numbers on the hero, a primary CTA that goes nowhere |

Reading (inferred, n = 11): the top scores carry a lot of real subject matter; the bottom ones are thin, promotional or broken. Voice alone does not score. Target Content ≥ 7.8 [awwwards-editorial §6.4], and treat that as a writing job finished before the first layout.

## 2. Headlines

| Measure | Value | Basis |
|---|---|---|
| Lead-line length | median 6 words; 37/51 at 7 or fewer, 43/51 at 8 or fewer; longest 13 (akaru-2, dropbox-brand) | first `content_voice.examples` entry per teardown |
| Case | caps 22/51, sentence case 12/51 (3 of them mix both), lowercase 2/51, no conventional headline 6/51 | keyword count over `content_voice.headline_style` |
| Mobile display size | median 46.8px at 390 (p25 32, p75 80) | [probe] |
| `text-wrap: balance/pretty` shipped | 13/51 | [probe] |

Eight structures recur. The Winners column quotes at most one short line per site, for reference only. The last column is for a fictional kettle maker, "Ferrow" (invented brand). Use the structure, never a winner's words (house law: take the language from references, never the content).

| Structure | Mechanics | Winners | Invented example |
|---|---|---|---|
| Category coinage | A 4-5 word claim that puts the product in a new class, then a factual subline | opal-tadpole ("A new species of webcam") | "The kettle you inherit." + "1.2 L, 1,380 g, enamelled in six colours." |
| Fact as pitch | No slogan: availability, counts, dates, record IDs | gil-huybrecht ("Available September 2026"), igloo-inc | "Taking commissions from March 2027." |
| Proper names as headlines | Product, model, client or film names at display size; spec under them | the-watch, cartier-watches-wonders-2025, bennett-clive, depo-luxe | "Model 12" over "1.2 L · cast iron · 1998" |
| Declarative with a full stop | Short claim, full stop, one accent word per clause | lando-norris ("ALWAYS BRINGING THE FIGHT."), lama-lama-2, shed, mindmarket | "Boiling since 1998." |
| Setup and turn | A promise on one screen, the reversal on the next. Three-beat variant: claim, mechanism, outcome, where the second ends open and the third completes it | why-zero ("You Believed / College would land You / JOB"), terminal-industries | "Kettles are built to be replaced." / "Ours are built to be repaired." |
| Process triplet | Three clipped verbs, only when they are the real steps | artefakt ("We shoot. We produce. We finish."), everswap, leo-parpeix-portfolio-2026 | "Cast. Enamel. Fire." |
| Place line | A sensory or mythic line anchored by hard facts in the same viewport | son-daven ("Where the mountains speak"), era-residence, san-rita | "Made where the Aire meets the canal." + "Workshop open Thursdays, 10 to 4." |
| No headline | The logo, world or object owns the screen, with a one-word CTA | messenger, active-theory-v6, pacome-pertant-portfolio | Only for games and famous senders. The active-theory-v6 teardown flags the logo-only first screen as failing for anyone else |

Setting decisions:

- Hold the display line to one or two lines at every width, and write the 390px break first. At the mobile median of about 47px, six words already fill two lines. Count lines at 390 and shorten rather than shrink [typography §7]. A stack of three or more lines is a house-law tell.
- One emphasis per headline, as an italic or tonal word at the same cap height (lando-norris swaps one serif word per clause; the-power-of-storytelling puts one italic serif word per line). Mechanics are in [./typography.md](./typography.md). Never strand a coloured word at the foot of a wrapped stack.
- A full stop on a declarative reads as certainty. Questions are allowed only when the answer is the next thing on screen: active-theory-v6's search prompt, dont-board-me's FAQ heads.
- "The X for Y", "the future of X" and "X. Reimagined." are the most interchangeable forms (steven-com, hubtown, artefakt's mono tagline). steven-com's positioning line sits at Content 7.47, fifth from the bottom of the 51. If you use one, the next line has to carry a fact.
- Tone check: read the line aloud next to two competitors' lines. If it could swap in without anyone noticing, rule 3 applies.

## 3. Voice archetypes, tied to direction

Choose the direction first, then its voice. Direction does not buy Content: mean Content per primary direction runs only 7.64 (Process filter) to 7.88 (Object hero), while the spread inside each direction is wider (Flown world 7.10 to 7.96). The voice and the facts decide the score. Default pairings, from the primaries listed in [./directions.md](./directions.md):

| Direction | Default voice | Second register | Primaries in the 51 (mean Content) |
|---|---|---|---|
| Flown world | Manifesto on display lines; terminal sub-register only on real data | Plain product sentence per chapter | 10 (7.70) |
| Playable toy | Playful, diegetic (signage, dialogue, quest cards) | Plain controls, credits, legal | 5 (7.77) |
| Object hero | Technical-precise, scale by comparison; parody only for a studio's own product | Wry sublines | 6 (7.88) |
| Reel as interface | Hushed luxury: credits format, names | Single-word UI verbs | 4 (7.82) |
| Editorial catalogue | Curatorial, one dated fact per beat | Captions and footnotes | 4 (7.82) |
| Kinetic poster | Playful or manifesto, shouted in one case rule | Plain join and pricing lines | 3 (7.78) |
| Illustrated story | Playful, brand as friend; plain words for care subjects | Plain service facts | 4 (7.75) |
| Material calm | Hushed luxury or manifesto, anchored by sizes, prices and distances | Plain sales facts | 5 (7.79) |
| Process filter | Curatorial or pastiche, matching the filter's era or craft | Plain product copy | 5 (7.64) |
| Archive index | Technical-precise: names, counts, dates as the pitch | Verb-only cursor labels | 5 (7.85) |

The archetypes in detail. Scores are each site's jury Content score.

| Archetype | Direction it fits | Sentence mechanics | Winners (Content) | Failure mode |
|---|---|---|---|---|
| **Technical-precise** (spec sheet, catalogue, press release) | Hardware, product launch, B2B, space and industrial, engineering portfolios | Nouns + numbers + units. Scale told by everyday comparison. One plain sentence per feature. First-person persona titles on B2B cards | vast 7.92, gil-huybrecht 7.92, igloo-inc 7.91, the-watch 7.90, opal-tadpole 7.64, terminal-industries 7.57 | A spec wall with no hierarchy; mono used on every label |
| **Manifesto** (declarative brand statement) | Celebrity and brand platforms, agency sites, gaming and web3 worlds, luxury launches | One sentence split into clauses across beats, one accent word per clause, followed at once by utility copy. Each clause rides the signature scene (lando-norris's helmet, the-power-of-storytelling's bird); never a kicker plus one centred serif sentence on a flat section | immersive-garden-website 8.34, lando-norris 8.18, the-power-of-storytelling 7.83, zentry 7.78, bennett-clive 7.67 | Abstract nouns with no fact behind them; the big serif statement block |
| **Deadpan parody** (satire of a genre's register) | Studio self-promotion, experimental work, campaign microsites | Copy a genre's register exactly (AI launch, 80s enterprise brochure, soda ad). Undercut with footnotes and fine print, escalate, then name the sender and the real pitch at the end. The joke reaches the 404 and the legal pages | slosh-seltzer 7.87, shader-development-studio 7.81, oryzo-ai 7.76, why-zero 7.75 | Fake numbers read as real; a joke on a client's actual claims |
| **Playful** (brand as a friend, or a character) | Illustrated and character sites, games and worlds, consumer, family and care | First person or brand-as-friend, the audience's own idioms, short lines with full stops, one consistent case rule (all lowercase or all shouted). In worlds, copy is diegetic: signage, NPC dialogue, quest cards | brunos-portfolio 8.18, messenger 8.15, ponpon-mania 7.78, maxima-therapy 7.76, mindmarket 7.75, dont-board-me 7.73, pacome-pertant-portfolio 7.66 | Exclamation marks everywhere; jokes inside error, payment or consent flows |
| **Hushed luxury** (credits and names) | Luxury, film, fashion, watches, cinema | Names do the persuading (client, director, product). Credits format (title, director, client, numeral). Press quotes with festival credits. Single-word UI verbs. Native language first | siena-film-foundation 8.00, gq-ap-the-extraordinary-lab 7.96, depo-luxe 7.84, cartier-watches-wonders-2025 7.56 | Lofty adjectives with nothing named; the letterspaced serif wordmark |
| **Curatorial** (narrative non-fiction) | Museums, culture, archives, editorial, non-profit, research | One plain sentence per beat carrying a date, an owner, a city or an event. Footnotes, credits, attributed quotes. The dark turn lands without adjectives | tracing-art 8.09, the-renaissance-edition 8.09, aim-ai-modernism-of-kharkiv 7.67, david-whyte-experience 7.40 | Long reading inside a scroll-jacked stage; 12px captions |

Decisions that cut across archetypes:

- **Two registers.** The signature voice goes on display lines. A plain register goes on anything the visitor acts on or needs to trust. lando-norris pairs its racer manifesto with fan-hub utility lines. the-renaissance-edition pairs painted pastiche with plain product copy. son-daven and era-residence set a folkloric or aspirational line beside prices, unit sizes and drive times. everswap's metaphor chapters each carry one plain sentence explaining the product. lama-lama-2 keeps its lead copy plain under joke labels. david-whyte-experience keeps its sales copy plain beside the poems.
- **The terminal or lab register** (IDs, slash prefixes, readouts: igloo-inc, active-theory-v6, artefakt) is a sub-register of technical-precise. The house law allows mono only where the content really is data. When every eyebrow, button and colophon wears the same tracked caps, that is the "one label treatment" tell. Give labels a second treatment.
- **Parody needs a sender who can afford the joke:** studios selling their own craft (oryzo-ai is by Lusion, shader-development-studio promotes itself, slosh-seltzer is an in-house brand exploration). Signal the parody on screen, with a footnote or fine print that undercuts the claim, and reveal it by the end. Never parody on a client's real product claims.
- **Care and serious subjects get plain words.** maxima-therapy states its stance in one plain sentence and softens clinical terms. tracing-art lets the looting history land without adjectives.

## 4. Narrative arcs for a scroll page

### 4.1 Arc templates

| Arc | Shape | Winners |
|---|---|---|
| Setup, turn, payoff | A promise, an emptied beat, the reversal, then the reward | why-zero (the stage clears to one image for a beat before the reversal lands); terminal-industries (claim, mechanism, outcome over one film); oryzo-ai (a straight-faced launch, escalating footnote gags, then the admission that the product does not exist, followed by the studio pitch) |
| Acts with an index | Numbered chapters, a visible index, optional side rooms | gq-ap-the-extraordinary-lab (3 narrated acts, act navigation, optional deep-dive rooms, skip intro); the-renaissance-edition (12 chapters indexed I to XII); hubtown (6 chapters, each named by a value word on a side rail); ponpon-mania (chapters titled like album tracks) |
| One object, its history | The object stays pinned while time moves round it | tracing-art (one painting, a year scrubber, one owner per beat); the-watch (display scenes, spec scenes, then an exploded view) |
| A world with places | Content as locations you visit | brunos-portfolio (13 areas, and an achievement for visiting all of them); messenger (quests); san-rita (trails and hotspots, a next-trail footer) |
| Product tour | Emotion alternates with spec | opal-tadpole (photo and video beats against dark technical sections); vast (quiet statement, 3D set piece, dated news) |

### 4.2 Beat sheet and budgets

| Beat | Job | Copy budget | Scroll budget |
|---|---|---|---|
| Arrival | Name + promise, readable at first paint | h1 of 8 words or fewer + one factual line | 100vh; no loader, or a stage loader capped at 1.5s |
| Premise | The one idea | 1 sentence | 100 to 150vh |
| Chapters (5 to 8) | One fact each | Title of 3 words or fewer + body of 3 lines or fewer + at least 1 specific | 150 to 500vh (pinned set pieces take the top of the range) |
| Turn | Reversal or reveal | 1 short line, or nothing | 50 to 100vh gate |
| Proof | Names, dates, press | Lists set as type, not cards | 100vh |
| Ending | One literal action + a way back round | 6 words or fewer + real links | 100vh |

Where the numbers come from:

- **Dwell per chapter:** everswap gives each full-screen chapter 100vh of content plus 75 to 500vh of padding. hubtown runs chapters of 400 to 500vh over a sticky stage (2,800vh in total). why-zero uses 175 to 368vh stages separated by 50vh gates. cartier-watches-wonders-2025 snaps between 8 stops (intro, 6 universes, outro): each universe spans a quarter of progress and starts at the midpoint of the previous one, so a stop falls every 12.5%. Forged sizes scenes in viewport heights to tune pace [awwwards-editorial §3.3].
- **Chapter count:** 3 acts (gq-ap-the-extraordinary-lab), 6 (hubtown; cartier-watches-wonders-2025 between an intro and an outro), 7 sections (floema), 12 (the-renaissance-edition, where each chapter is a product), 17 sections (son-daven). Default to 5 to 8. Go past 10 only when every chapter holds a distinct product or record (inferred).
- **Document length:** long-form story pages run 13,732px (mindmarket) to 81,450px (tracing-art); portfolios and app-like homes run one viewport (depo-luxe) to under 6,000px (gil-huybrecht, david-whyte-experience). Long is fine when every beat carries a fact. Length with nothing new in it is scroll-jacking.
- **Body length:** one plain sentence per chapter (everswap, tracing-art); 2 to 3 lines under each headline and a single action (hubtown). The body measure caps at 65ch [typography §4.3].
- **Rhythm:** about half the section rhythms (26 of 51 by keyword count) alternate loud and quiet, or dense and sparse, every one or two screens (floema, odd-ritual, lando-norris, vast, mindmarket, the-renaissance-edition). Put copy in the quiet sections and let the loud ones be image, object or type at display size. Section layout is in [./layout.md](./layout.md); per-site detail in [./casebook.md](./casebook.md).

### 4.3 Reveals without hiding

- The whole sentence is in the DOM from first paint. A manifesto split across screens (the-power-of-storytelling, why-zero) is one `h2` with a span per clause. Scroll moves the active clause into place and dims the clauses already read (read-state dimming [elements-catalog X1, R3b]). It never holds unread clauses at `opacity: 0`, and the dimmed ink still passes 4.5:1 (`--ink-read` in [elements-catalog R3b](../data/research/elements-catalog.md)).
- A masked line rise is allowed on the hero only, with a deadline that shows the text if JS stalls: `data-reveal="lines"` and the intro deadline in [../recipes/motion-core.js](../recipes/motion-core.js) and [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html). Motion detail is in [./motion.md](./motion.md).
- The turn is a pause in the content, not in the page: a 50 to 100vh gate carrying only the image (why-zero) or an object seen edge-on while its label changes [elements-catalog S1]. The words for the next beat are already in the DOM.
- A counter that shows 00 until it fires is invisible content. Render the real number in HTML. Animate from it, or count only on a user action [elements-catalog §4].

### 4.4 Orientation and endings

- **Show where the reader is.** Numbered indexes (the-renaissance-edition, depo-luxe), a year scrubber (tracing-art), act navigation (gq-ap-the-extraordinary-lab), a value-word rail (hubtown), chapter marks drawn from the logo (everswap), a counter rail (floema). About 22 of 51 also ship a scroll cue (a "scroll to explore" or "scroll down" label, a SCROLL circle, a chevron). The good ones speak in voice: san-rita invites you to scroll into its world, cartier-watches-wonders-2025 writes it in French. A progress index does the cue's job and orients as well [elements-catalog S6]. Set the index as text links in the margin or header, never as 01/02/03 beside a vertical rule (a house-law slop layout).
- **End on a continuation, not a banner.** Next project or next trail with its thumbnail (pacome-pertant-portfolio, san-rita), a teaser for the next program (maxima-therapy), restart (david-whyte-experience; gq-ap-the-extraordinary-lab in its non-US editions), waitlist plus share (why-zero), the studio's own pitch after the parody (oryzo-ai). Decision: one literal action (a real `<a href>`) plus one way back round.

## 5. Microcopy

**Loaders.** At least 7 of 51 show a numeric readout (active-theory-v6, gil-huybrecht, immersive-garden-website, lama-lama-2, slosh-seltzer, thelinestudio-com, why-zero). The memorable ones make the number or the status words belong to the brand: a frames-per-second counter for a production studio (thelinestudio-com), a mission-log checklist for a trail-map studio (san-rita), a party line wrapped round the counter for a drink (slosh-seltzer), a BIOS boot for a retro-satire studio (shader-development-studio), a legend line over a walking sheep for a valley resort (son-daven). Status verbs that change with context work too [elements-catalog P6]. Two faults to avoid: thelinestudio-com's counter is a 3s timed tween, not real load progress, and a bare "Loading" says nothing. Decisions: no full-screen loader by default; if a scene needs one, scope it to the stage, count real asset promises, expose `role="progressbar"` with `aria-valuenow` (why-zero's DOM loader does), cap any intro at 1.5s, make it skippable (click or Esc), show it once per session and skip it under reduced motion [usability-a11y-perf §3.6]. For the hero text itself, the CSS intro deadline in [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html) guarantees the words show even if JS never runs. The best loader is already the first frame: immersive-garden-website sets brand, promise and progress on one baseline; akaru-2 and son-daven hand the loader's wordmark to the hero, and steven-com turns the wordmark's last glyph into the first 3D object.

**CTAs.** Luxury uses single-word verbs (cartier-watches-wonders-2025, immersive-garden-website). Worlds use one in-world verb (messenger's single CTA on the title screen). The metaphor may colour the headline above a button, but the button label stays literal: everswap's summit metaphor ran into its CTA, and its primary button has no href and rolls its label to a coming-soon notice on hover. That is a dead control. Decisions: verb plus object, 1 to 3 words, a real `<a href>` or `<button>`, one primary action per screen, never a filled button beside an outlined twin (house law). The motion for the label is in [../recipes/magnetic.js](../recipes/magnetic.js): the box never moves.

**Cursor labels.** About 15 of 51 winners trail a text label beside the pointer (14 confirmed in the `motion.cursor` field). The native cursor is hidden on only 2/51 [probe]. The good ones are verbs naming what a click will do on a target with no text of its own: a one-word label on image planes (gil-huybrecht, immersive-garden-website), view labels on project media (thelinestudio-com), previous and next over gallery halves (odd-ritual), a visit label with an arrow over news cards (shed), a story invitation whose letters trail the pointer (dont-board-me). Decisions: 1 or 2 words, verb first; never repeat the target's own label [elements-catalog H2]; `aria-hidden`, off on touch and under reduced motion; the same state also visible on the element for keyboard and touch users [usability-a11y-perf §3.9].

**Sound gates and captions.** 21 of 51 ship sound, and nearly all of it stays off until a click or a toggle. The gate copy must offer both choices at equal weight. pacome-pertant-portfolio set its no-sound option at 14px and 70% opacity, which is the fault to avoid. Narrated stories need text: gq-ap-the-extraordinary-lab lights its subtitles character by character from the audio position and ships a transcript menu whose block heights equal the cue durations, so scrolling the text seeks the film. The dev checklist asks for captions on video [awwwards-editorial §1.4].

**404.** Designed 404s show up in about 10 of 51 teardowns (shader-development-studio's bank vault with a busy line, son-daven's breathing idle scene, the-power-of-storytelling's ice shader, the-renaissance-edition, iyo, maxima-therapy, thelinestudio-com, pacome-pertant-portfolio, dont-board-me, era-residence). The 404 tag is about three times as common on recent SOTDs as on HM-only sites (10.3% vs 3.6%) [awwwards-editorial §3.3]. Decisions: a scene or line in the site's voice, served with HTTP status 404, a `<title>` that says not found, and real links to home and the top routes. Jurors click past the homepage.

**Consent, nav taglines, footers.** ponpon-mania writes its cookie line in the site's voice and gives accept and decline the same treatment. lama-lama-2 changes the nav pill's tagline per section, so the chrome speaks in context. Decisions: consent says plainly what is collected, with equal-weight choices; the joke, if any, goes in the greeting and never in the terms. A footer is not a closing banner: say one thing in voice and give the real addresses, credits and legal links (shader-development-studio's parody seal links to a real accessibility statement).

## 6. Real specifics over lorem

| Kind | What winners print | Where it sits |
|---|---|---|
| Numbers with units | Weight in grams, part and material counts, glass thickness in mm, cable length in cm (opal-tadpole); residence count, unit sizes in sq.m, drive times to three towns (era-residence); price per m² in local currency and minutes to landmarks (son-daven); effect count, member count, quarterly price (made-with-gsap-1); a product-update count (the-renaissance-edition); days to go live, stated in a sentence (terminal-industries) | Hero subline, spec rail, chapter body |
| Names | Clients as headlines (bennett-clive), client names in film-credit format (depo-luxe), festival credits and press quotes (siena-film-foundation), collaborators credited by name (brunos-portfolio, leo-parpeix-portfolio-2026), named testimonials (made-with-gsap-1), map places named after team members (san-rita) | Proof beats, credits, captions |
| Dates | An availability month (gil-huybrecht), dated hardware milestones (vast), a painting's ownership timeline (tracing-art), stamped readouts (igloo-inc) | Hero, news, timeline |
| Places | Addresses in the footer (floema, son-daven), live city clocks (bennett-clive, lama-lama-2), local production claims (odd-ritual) | Meta rows, footer |

Decisions:

- **Scale by comparison.** Pair the exact figure with an everyday object (opal-tadpole compares the webcam's height to a sweet). The number earns trust and the comparison makes it vivid.
- **Counts as proof.** Award and project counts replace adjectives (gil-huybrecht lists its SOTD count; made-with-gsap-1 its combined SOTDs). Use a count only if you can source it.
- **Sources or drafts, nothing in between.** Every fact in the deck has a source (the brief, the client, a public page). An unknown is written as `[DRAFT: confirm]` and listed in the handoff. The house law allows real logos only when you can honestly claim them, and treats invented customers and fake metrics in testimonial cards as slop. Imagery follows the same rule: no AI people presented as real [imagery research]. Awwwards also rejects sites built from pre-made templates [awwwards-editorial §1.1].
- **Dates are sentences, not widgets.** A lead time or launch date is a fact in the copy ("live in 5 days"). A DAYS/HRS/MIN countdown box row is a house-law tell unless something really ends at that moment.
- **Quotes are set as type.** A press or client quote gets its source and date in the same line, in the text face. No giant quote-mark glyph, no avatar card.
- **Parody numbers are the only exception.** oryzo-ai's percentage gags and fake paper work because the site says it is joking. Never apply this to a real client's claims.
- **Proofread the template layer.** Seven winners shipped visible defects: a pull quote cut off mid-phrase, a brand name spelled two ways and 14 em dashes (era-residence); a waitlist line that spliced the user's name into the wrong slot (why-zero); French-English typos (made-with-gsap-1); a credits line with its name slot empty (david-whyte-experience); a nav link whose `title` names a different page (hubtown); a grammar slip plus a mobile manifesto with a desktop line fragment pasted in, because each breakpoint's line breaks were typed by hand (aim-ai-modernism-of-kharkiv); a tripled letter in a German word on the mission wall (champions-for-good). Render every templated string with real, long and empty data, and split lines at runtime rather than keeping a hand-broken copy per breakpoint.

## 7. Bilingual and localized sites

At least 10 of 51 winners are non-English-first or ship a language switch: akaru-2 (French only, Content 8.11), cartier-watches-wonders-2025 (French first), son-daven (UA/EN, locale in the URL), champions-for-good (English hooks, German explanations), gq-ap-the-extraordinary-lab (copy for 10 GQ editions bundled, US copy loaded from a payload), san-rita and ponpon-mania (EN/FR), lama-lama-2 (NL/EN), floema (a language dropdown), the-renaissance-edition (a locale segment in its routes).

Decisions:

- **Write each language natively.** akaru-2 scored 8.11 in French alone, so a foreign-language site loses nothing with the jury. Headline wordplay rarely survives translation (inferred), so write the display line fresh in each language and translate only the utility register.
- **Split by role only on purpose.** champions-for-good sets its hooks in English (the sport's culture) and its explanations in German (the audience). If you mix languages, give each one a job.
- **Budget length.** cartier-watches-wonders-2025 adds a long-text class that steps body copy down to 13 and 15px for longer languages. Set a `:lang()` or class-scoped type step, and fit the display line to 2 lines in the longest language.
- **Glyph coverage is voice.** champions-for-good writes umlauts out as two letters in its caps display face (apparently so the caps render; inferred). Choose display faces with full Latin Extended coverage, and never transliterate. son-daven goes the other way on purpose: a dotted capital I makes the UI feel of its place.
- **Canvas text needs its own localization.** san-rita ships a French variant of its trails model (`sanrita-trails@fr.glb`), but its baked place-name labels file has no locale variant. Any text baked into a texture or mesh needs one asset per locale (name them `file@<lang>.glb`) and a DOM twin.
- **Markup.** `<html lang>` on every page (55/60 winners set it [usability-a11y-perf §1.5]), `lang` on inline foreign phrases, one URL per locale, and `hreflang` alternates with a self-reference plus `x-default` (standard practice, not measured in the teardowns). Put the switch in the header meta row as short codes, and move it to a reachable corner on mobile (ponpon-mania moves it to the bottom left). List each language by its own name.
- **Punctuation belongs to the language.** French puts a space before `!` `?` `:`; pacome-pertant-portfolio carries that habit into its English lines as a mannerism. Decide it deliberately. Do not let it leak.

## 8. Content structure the dev jury scores

What winners ship, from the static probe of 60 Developer Award SOTDs [usability-a11y-perf §1.5]: `<html lang>` 55/60; `<h1>` in server HTML 45/60; `<main>` 48/60; skip link 1/60; under 200 characters of server-rendered text (JS-only content) 8/60; `alt` present on 88% of images (presence only, not quality). The dev checklist asks for unique per-page titles and descriptions, clean URLs, a heading hierarchy, canonicals, sitemaps, text links rather than JS links, Open Graph and Schema.org [awwwards-editorial §1.4].

Patterns in the 51, and the decision each one implies:

- **The h1 does not have to be the biggest type.** artefakt's h1 is a two-line company description at 12px. depo-luxe's is its 14.3px italic tagline. the-renaissance-edition's is a 14px header. Decision: the h1 is the sentence that says what the page is, and display type can be `h2`, a `<p>` or a decorative SVG.
- **No h1 at all** on at least 5 homes: brunos-portfolio (no DOM text on the first screen; Accessibility 6.6, Semantics 7.0), odd-ritual (hero numerals marked up as h2), pacome-pertant-portfolio, siena-film-foundation, and messenger's title screen. **Two h1s** on tracing-art, opal-tadpole and son-daven. Decision: exactly one per route.
- **Visually hidden real h1 behind a decorative display:** lando-norris (the display is an inline SVG wordmark), made-with-gsap-1, fluid-glass, opal-tadpole. This works when the hiding uses clipping. immersive-garden-website and everswap hide the DOM h1 with `visibility: hidden` while WebGL draws it, which also removes it from the accessibility tree. Use the clip-based class below.
- **Split text keeps one accessible copy:** steven-com keeps the real sentence in a visually hidden span and marks the animated clone `aria-hidden` and `data-nosnippet`. hubtown's scramble nav keeps an sr-only full label. Or use `data-reveal="lines"` in [../recipes/motion-core.js](../recipes/motion-core.js), which handles the accessible name.
- **WebGL-only text needs a mirror:** active-theory-v6 draws its nav in WebGL and keeps clipped screen-reader links in the DOM. shader-development-studio renders all visible type in WebGL over a full DOM text mirror and ships an accessibility statement page. gq-ap-the-extraordinary-lab tethers real DOM buttons to 3D anchors. Decision: DOM is the source of truth, and the canvas is `aria-hidden` [usability-a11y-perf §2 A].
- **Client routing must carry the metadata:** [../recipes/page-transitions.js](../recipes/page-transitions.js) animates the swap, but your router still owns the words. Inside the update callback, set the title and description, then move focus to the new h1:

```js
window.pageTransitions.swap(() => {
  render(route);                                   // your router's DOM update
  document.title = route.title;
  document.querySelector('meta[name="description"]')?.setAttribute('content', route.description);
  const h1 = document.querySelector('main h1');
  h1?.setAttribute('tabindex', '-1');
  h1?.focus({ preventScroll: true });
});
```
- **Real values stay machine-readable:** the-renaissance-edition renders prices and quantities as Roman numerals through CSS counters, while the real value stays in the DOM and `aria-label`.

```html
<html lang="en">
<head>
  <style>.vh{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}</style>
  <title>Ferrow Model 12: a 1.2 litre cast-iron kettle</title>
  <meta name="description" content="1,380 g of cast iron, enamelled by hand in six colours.">
  <link rel="canonical" href="https://ferrow.example/model-12/">
  <link rel="alternate" hreflang="en" href="https://ferrow.example/model-12/">
  <link rel="alternate" hreflang="fr" href="https://ferrow.example/fr/model-12/">
  <link rel="alternate" hreflang="x-default" href="https://ferrow.example/model-12/">
  <meta property="og:image" content="https://ferrow.example/og/model-12.jpg">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <main id="main">
    <h1 class="vh">Ferrow Model 12, a 1.2 litre cast-iron kettle</h1>
    <svg class="wordmark" aria-hidden="true" focusable="false"><!-- display wordmark --></svg>
    <h2><span class="vh">Boiling since 1998.</span><span aria-hidden="true" data-nosnippet><!-- split clone --></span></h2>
    <canvas aria-hidden="true"></canvas>
  </main>
</body>
</html>
```

## 9. The copy deck (write it first)

Keep this file next to the build and treat it as the source of truth for every string. Fill it in before any layout work.

```yaml
concept: "One sentence a stranger could repeat."     # Creativity is scored on this
direction: object-hero                                 # ./directions.md
voice: technical-precise                               # section 3
registers:
  display: "short declaratives, full stops, one accent word per line"
  utility: "plain verbs, literal labels, no jokes"
  banned: ["em dash", "lorem", "headline of 3+ lines", "unsourced number"]
facts:                                                 # every line sourced or marked
  - { claim: "1,380 g", source: "client spec sheet" }
  - { claim: "enamelled by hand", source: "[DRAFT: confirm]" }
headlines:
  hero: { text: "...", words: 6, lines_at_390: 2 }
beats:                                                 # section 4.2
  - { id: arrival, job: "name + promise", copy: "...", specific: "...", scroll_vh: 100 }
  - { id: premise, job: "the one idea",   copy: "...", specific: "...", scroll_vh: 120 }
microcopy:
  loader_status: "..."          # only if a stage loader exists; <= 1.5s, real progress
  cursor: { media: "Open", drag: "Drag" }
  sound_gate: { on: "Sound on", off: "Continue without sound" }   # equal weight
  not_found: { line: "...", links: ["/", "/work"] }
routes:
  "/": { title: "...", description: "...", h1: "...", og: "/og/home.jpg" }
locales: [en]                   # add hreflang pairs when there is more than one
```

Checks before shipping: every beat has a specific; no fact without a source; every headline fits 2 lines at 390 in the longest locale; every templated string rendered with real, long and empty data; a search for the em dash character (U+2014) finds nothing.

## Crafted vs slop

| Award habit | Slop version | Crafted version |
|---|---|---|
| Manifesto split across scroll beats | Clauses parked at `opacity: 0` until a ScrollTrigger fires | Full sentence in the DOM, visible; scroll moves the active clause and dims the ones already read |
| One accent word in the headline | Neon on a stray last word at the foot of a four-line stack | One italic or tonal word inside a 1-2 line headline, at the same cap height |
| Percentage preloader with a brand line | Full-screen timed 0-100 counter over a bare "Loading" | No full-screen loader; a stage-scoped loader with real progress and a status verb from the brand's world, capped at 1.5s, skippable |
| Cursor label | `cursor: none`, a lagging ring, a label repeating the button's own text | Native cursor, 1-2 word verb only over targets with no text, state also shown on the element |
| Scroll hint | A generic "Scroll to explore" and a bouncing chevron as the only orientation | A cue written in the brand's voice, plus a chapter index or year scrubber that shows position |
| Chapter index | 01/02/03 stacked beside a vertical rule | Chapter names as text links in the margin or header, the active one set by weight or ink |
| Terminal or lab voice | Mono caps on every eyebrow, button and colophon | Mono only on real data (IDs, readouts, timestamps); labels get a second treatment |
| Deadpan parody | Fake metrics and testimonials presented straight | The parody is signalled on screen, reveals itself by the end, and only ever spends the sender's own reputation |
| Section openers | A tiny caps kicker over a serif H2 on every section | Open sections with a number, a full sentence, an image or nothing, and vary them |
| Manifesto beat | A kicker plus one centred serif sentence with an italic word, on a flat section | The clauses ride the signature scene across beats, one accent per 1-2 line clause, and a fact follows on the next screen |
| Launch date | A DAYS/HRS/MIN countdown box row | The date or lead time written in a sentence |
| Social proof | A testimonial card with a quote-mark icon, initials avatar and invented metric | Named clients set as type, credit-format lists, press quotes with source and date in the text face, logos you can claim |
| Closing section | A gradient pre-footer banner with a filled + outlined button pair | A continuation: the next project or chapter, one literal link, a way back round |
| 404 | "Oops, page not found" and a home button | A scene or line in voice, status 404, real links to home and the top routes |
| Stats row | Counters showing 00 until scrolled into view | Real numbers in server HTML; animate from them or on a user action |
| Sound gate | Click to enable sound as the only visible exit | Two equal choices; captions or a transcript for anything narrated |
| Metaphor CTA | A button in the metaphor with no href that rolls to a coming-soon notice | The metaphor stays in the headline; the button is a literal verb and a live link, or it is not shown |
| Hidden h1 for a WebGL title | `visibility: hidden` on the h1 (gone for screen readers) | Clip-based visually hidden h1 or a real DOM line; canvas `aria-hidden` |
| Em dashes in copy | A dozen em-dashed asides in body copy | A colon, a full stop, or a split line |

## Exemplars

- **tracing-art**: curatorial non-fiction; one dated fact per beat; a year scrubber for orientation over an 81,450px story.
- **oryzo-ai**: deadpan parody arc; footnotes undercut the hero claim; the end admits the joke and pitches the studio.
- **opal-tadpole**: technical-precise at its best; each claim gets a factual subline, and scale is told by comparison.
- **the-renaissance-edition**: 12 indexed chapters, two registers (pastiche and plain product copy), real values kept machine-readable.
- **gq-ap-the-extraordinary-lab**: three acts with act navigation, narration with live subtitles and a seekable transcript, 10 localized editions.
- **lando-norris**: manifesto display voice with fan-hub utility copy; one serif accent word per clause; a real h1 behind an SVG wordmark.
- **terminal-industries**: B2B story in three beats over one film; first-person persona card titles; operational specifics.
- **gil-huybrecht**: no slogan, facts as the pitch; verb-only cursor labels on text-less image planes.
- **messenger**: diegetic copy (quest dialogue and cards) with one in-world CTA; what a world does with words.
- **san-rita**: one metaphor carried through every string (loader, map names, footer); EN/FR, with a per-locale 3D trails file.
- **immersive-garden-website**: highest Content score in the sample; a loader row that is already the hero; menu items that complete their sentence.
- **shader-development-studio**: satire with the joke reaching the 404, plus a full DOM mirror of its WebGL text and a real accessibility statement.

## Evidence

- `data/teardowns/<slug>.json` for all 51 sites: `content_voice`, `scores`, `first_screen`, `layout.section_rhythm`, `motion.preloader`, `motion.cursor`, `navigation_interaction`, `performance_accessibility`, `steal_this`, `slop_risks`. Headline length and case counts are computed from `content_voice`; correlations and per-direction means from `scores`. Loader, sound, cursor-label, scroll-cue, 404, rhythm and copy-defect counts are keyword counts over those fields, re-run in the 2026-09-25 audit.
- `evidence/digests/content.md`: per-site content voice, first screen and navigation digest (all 51 read).
- [awwwards-editorial](../data/research/awwwards-editorial.md) §0, §1.2 to §1.4, §3.1, §3.3, §6.4: score formula, Content criterion, dev checklist, 404 tag differential.
- [usability-a11y-perf](../data/research/usability-a11y-perf.md) §1.5, §2 A and H, §3.6, §3.9: probe of 60 dev-award SOTDs, the semantics checklist, preloaders, cursor followers.
- [elements-catalog](../data/research/elements-catalog.md) §2.1 P6, §2.4 H2, §2.7 X1, §2.8 S1 and S6, §4, R3b: themed status copy, cursor chips, read-state dimming and its contrast floor, progress, zero-counters.
- [directions](./directions.md): primaries per direction, used for the voice-per-direction table and its mean Content scores (computed from `scores.content`).
- [typography](../data/research/typography.md) §4.3, §7: measure, line counts at 390. [imagery](../data/research/imagery.md): stock and AI-image rules.
- [stats](../data/stats.md) recent_2024_plus cut: Content mean 7.48, dev means (Semantics 7.23, Markup 7.16, Accessibility 6.83). [probe](../data/probe_summary.json): mobile display median 46.8px, `text-wrap` on 13/51, `cursor: none` on 2/51.
- House law: `deslop-law.md` (em dashes, multi-line headline, kicker + H2, big serif statement block, numbered steps beside a line, countdown timer, filled + outlined button pair, dead controls, testimonial card and decorative quote marks, pre-footer CTA, one label treatment, mono as house voice, invisible-content trap, real logo walls, real specificity, take the language not the content, say less).
- Recipes linked, not duplicated: [../recipes/motion-core.js](../recipes/motion-core.js), [../recipes/boot.html-snippet.html](../recipes/boot.html-snippet.html), [../recipes/page-transitions.js](../recipes/page-transitions.js), [../recipes/magnetic.js](../recipes/magnetic.js).
