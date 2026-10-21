# Concepts: finding the idea that cannot be moved

A concept is a **rule system borrowed from a world**. "Minimal dark portfolio with WebGL" is not a
concept; it is a style. "The site is a contact sheet: every project is a roll of film you scrub
through" is a concept: it dictates layout (strips, frames), motion (film advance, shutter),
type (edge-print labels), interaction (scrub, loupe), and copy (frames, exposures).

Test: can you derive at least four design decisions from the sentence? If not, it is a style.

## Five territories (generate one concept from at least three of them)

1. **Name / etymology / identity.** What does the name mean, sound like, look like as letterforms?
   Initials as a structural shape, the meaning of the name, a pun only if it is elegant.
   - "Marco" = in Spanish/Portuguese/Italian *marco* is a frame, a landmark, a boundary stone.
     Concept: *"Everything on the site is framed: the viewport is a picture frame, projects are
     hung, and the frame itself moves to show you where to look."*
2. **The material of the profession.** Code (grids, cursors, diffs, compile states), type design
   (outlines, glyph grids, proofs), photography (contact sheets, exposure, grain), architecture
   (plans, sections, models, light studies), music (scores, waveforms, tempo), film (frames,
   timecode, cuts), print (registration marks, folds, ink).
3. **Place and culture.** Where they are from or work: local typography, signage, materials,
   climate, transit maps, street furniture, market stalls. Specific, never a flag or a cliché.
4. **How they work (process metaphor).** Sketch to final, layers, iterations, a workbench,
   a field notebook, a lab protocol, a kitchen mise en place. The site performs the process.
5. **A formal system.** One strict rule taken to the extreme: everything is a single line of
   text; everything lives on a 3x3 grid; the page is one infinite horizontal scroll of type; the
   whole site is a single typeface at one size with weight as the only hierarchy.

## Method

1. Write 3 concepts, each from a different territory, each one sentence.
2. For each, list: layout rule, motion verb, type voice, palette source, signature moment,
   the frame people would screenshot.
3. For each, write the **anchor**: the specific fact about this subject the concept depends on
   (a name's meaning, a real material, a real place, how they actually work). Then run the swap
   test: put a different subject in the sentence. If it still works, the concept is a style;
   portability is 4 or 5.
4. Score 1 to 5: originality, fit to the person/brand, feasibility in ~1 day of code,
   portability (could it be moved to someone else? lower is better).
5. Pick the best total. Optionally steal one secondary idea from a runner-up for a detail
   (404 page, loader, footer), never for the main structure.
6. Kill the concept if its only expression is a hero effect. A concept must survive to the
   footer, the case page and the 404.

## Worked examples (the method, not ideas to reuse)

These examples show how to reason. **Never reuse their ideas**, even adapted to a new subject:
no code that compiles into an image, no homepage made of one sentence, no viewport frame, no
running balance, no fire that cools down, no mise en place. If one of your concepts resembles
an idea below, it is borrowed. Replace it with one built on your own subject's anchor.

### "make me a portfolio, my name is Marco"

| | A. The frame (name) | B. Source & render (material) | C. One sentence (formal) |
|---|---|---|---|
| Idea | *Marco* means frame: a thick frame surrounds the viewport and reshapes itself around each project | Every project shown as its source first, then rendered live on hover | The whole homepage is one sentence about Marco; each noun opens a project |
| Layout | Viewport-as-frame; projects hung off-center on a wall grid | Split: code column / render column | One giant line of text wrapping across the viewport |
| Motion verb | slide and lock, like a frame being hung | compile: snap, flicker, resolve | words lift out of the sentence |
| Type | condensed grotesk on the frame edges, small serif captions like museum labels | mono + neo-grotesk | one grotesk at display size |
| Signature | the frame's inner edge animates (clip-path) to crop each project as you scroll; page transitions are the frame closing and reopening | hover a project: code text dissolves into its image (shader) | hovering a noun pulls its project image from behind the letters |
| Screenshot | a project perfectly cropped by the moving frame, museum label beneath | the half-code, half-image frame | the sentence with one image blooming out of a word |
| Scores (O/F/Fe/P) | 4 / 5 / 4 / 2 | 3 / 4 / 3 / 3 | 4 / 3 / 5 / 3 |

Pick A: strongest fit to the name, a complete rule system (frame → layout, transitions, captions,
cursor), feasible with clip-path + the engine. Steal from C for the 404: a frame with nothing in it,
labeled like an empty museum wall.

### "a launch page for Ledger, a budgeting app"

| | Idea | Anchor | Signature | O/F/Fe/P |
|---|---|---|---|---|
| A. Formal | The page is one running balance: every section is an entry, and a corner total updates as you scroll | the product's core object is a balance | entries post into the column and the total ticks over | 4 / 5 / 5 / 2 |
| B. Material | Double-entry: each problem on the left is answered on the right, and a section closes when both sides balance | double-entry bookkeeping | the ruled line draws itself when a section balances | 4 / 4 / 4 / 2 |
| C. Process | Month-end close: scrolling crosses a month as receipts pile up and file themselves | how people actually budget | receipts fly into folders on scroll | 3 / 4 / 3 / 3 |

Pick A: it fits the product best and is the cheapest to build well. The 404 is an entry that
doesn't reconcile.

### "a site for Brasa, a wood-fire restaurant in Lisbon"

| | Idea | Anchor | Signature | O/F/Fe/P |
|---|---|---|---|---|
| A. Name | *Brasa* means ember: the page is a fire across one evening, hot at the top and ash grey at closing time | the name and the kitchen | ground and ink cool through one global variable as you scroll | 4 / 5 / 4 / 2 |
| B. Place | The menu is set like *calçada*, Lisbon's black-and-white stone pavement: every dish is a stone in the pattern | the city's streets | the pattern assembles stone by stone as the menu reveals | 4 / 3 / 3 / 2 |
| C. Process | Mise en place: each section brings one ingredient from the station to the fire | how a kitchen works | ingredients slide onto the grill in order | 3 / 4 / 4 / 4 |

Pick A, and scale the theatre down: no loader, no GL, just the color of the evening. Steal from
B for the footer: the address set into a strip of pavement.

## Signature moment catalog (pick one; recipes in motion.md / webgl.md)

| Moment | Good for | Recipe |
|---|---|---|
| Hover list with floating image preview that follows the pointer and distorts with velocity | portfolios, studios, indexes | motion.md "Index list with cursor preview" |
| Scroll-scrubbed light / color / time of day across the whole site | narrative, personal | webgl.md "Fullscreen scroll-driven shader" |
| Images that bend and split with scroll velocity | photography, fashion, studios | engine `data-gl` (tune shader) |
| Kinetic display type: letters rearrange, stretch, or follow scroll | type-led brands, designers | motion.md "Kinetic type" |
| Shared-element transition: thumbnail grows into the case-study hero | any portfolio | motion.md "Flip shared-element transition" |
| Pinned sequence where one object transforms across chapters | product, storytelling | motion.md "Pinned chapters" |
| Draggable / infinite canvas of work | big archives, playful | motion.md "Drag canvas" |
| Generative system seeded by the visitor (time, pointer, local hour) | personal, experimental | webgl.md "Procedural covers" + time uniforms |
| Sound design toggled on by the visitor | music, film, immersive | motion.md "Sound" (always opt-in, off by default) |

## Concept quality bar

- Specific: it names a real thing from the subject's world.
- Generative: it produces decisions for layout, motion, type, color, copy, details.
- Restrained: one signature moment; everything else serves it.
- Legible: a visitor gets it without explanation in 10 seconds.
- Honest: no fake data or credentials to make the concept work.
