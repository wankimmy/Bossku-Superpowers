# Layout and composition

## Grid

- 12 columns with a fluid gutter (`--gutter`) for desktop, 4 or 6 on phones. Use CSS Grid with
  `grid-template-columns: repeat(12, minmax(0, 1fr))` and place by column lines; subgrid for
  aligned card internals.
- A visible logic beats symmetry: hang everything from 2 or 3 strong vertical lines (e.g. col 1,
  col 5, col 9). Text blocks start on those lines across the whole site.
- Outer margin = gutter. Corners are real estate: the four-corner frame (name, nav, context,
  action) is the genre's standard header/footer system.
- Vertical rhythm: section padding is not constant. Use 3 or 4 spacing "moods" (tight: 8u, normal:
  16u, airy: 28u, full viewport) and assign deliberately per section.

## Section layout families (each family at most once per page)

1. **Poster:** one display line or word fills the viewport width; minimal meta in corners.
2. **Index list:** full-width rows (title, discipline, year) with hover preview image. Obys-style.
3. **Asymmetric pair:** large image on 7 to 8 columns, text on 3 to 4 offset columns, staggered vertically.
4. **Gallery wall:** images of different sizes hung on the grid with deliberate empty cells.
5. **Filmstrip / horizontal pan:** pinned section scrolling horizontally (only if the content is a sequence).
6. **Sticky narrative:** sticky media on one side, chapters scroll on the other.
7. **Statement:** a paragraph set large (t-l) across 8 to 10 columns, manifesto voice.
8. **Data / facts:** big numerals in tabular figures with small labels (only real facts).
9. **Full-bleed media:** one image or GL scene edge to edge, type over it.
10. **Footer as finale:** giant name or call to action, real links, small print.

## Hero patterns (choose by concept, not by habit)

- **Name as image:** the person's name at mega size, one line or broken intentionally across the
  grid, with one meta line (what they do) and the four-corner frame.
- **Work-first:** the hero IS the work (a strip, a carousel, a 3D wall of projects) with tiny type.
- **Statement:** a sentence at t-xl that says what they do in plain words, no image.
- **Scene:** a fullscreen GL scene or video that embodies the concept, type minimal.
- **Split frame:** viewport divided by a strong line; type one side, media the other (Noho).

Hero must show what this is within 3 seconds: name/brand, what they do, where to go.

## Portfolio information architecture

```
/            hero → selected work (3 to 6) → short about → contact/footer
/work/<slug> case: title + meta (client, year, role) → hero media → context → idea → craft details
             (media sequence with captions) → outcome → next project (continuous transition)
/about       optional if home covers it: portrait or work-in-progress image, bio, services, clients
             (real only), recognition (real only), contact
/404         designed, carries the concept
```
Navigation: 2 to 4 items max (Work, About, Contact) plus the name linking home. An index of all
projects can live in a menu overlay if there are more than 6.

## Presenting work (pick one primary pattern)

| Pattern | Works when |
|---|---|
| Index list + cursor preview | many projects, type-led identity |
| Large staggered pairs | 3 to 6 strong visual projects |
| Grid wall of real screens | prolific web designers (Gil Huybrecht) |
| Horizontal filmstrip | sequential or photographic work |
| 3D carousel / curved wall | when the concept supports space (Jesper Landberg) |
| Stacked full-viewport cases | few, very strong projects |

## Menus

- Small corner nav on desktop; on phones a single "Menu" text button opening a full-screen
  overlay with large links that reveal with the system's motion. Focus trapped inside, Escape
  closes, `aria-expanded` on the button.

## Mobile composition (390 px)

- Redesign, do not shrink: mega type re-tuned (`clamp` minimums), grids to 1 or 2 columns with
  intentional offsets, corner frame collapses to top bar + menu.
- Replace hover-dependent interactions: hover preview list → inline thumbnails; cursor effects →
  tap/scroll-driven equivalents; horizontal pans → native horizontal scroll-snap.
- Keep the signature moment in an adapted form.
- Test: no horizontal overflow, nothing hidden behind the browser UI (`100svh`/`100dvh`), tap
  targets ≥ 24 px (44 px for primary actions).
- Desktop hero grids that use `1fr` rows to push content down leave a huge hole on tall phones:
  set explicit `auto` rows on mobile and center or end-align the stack deliberately.
- Horizontal strips (film strips, galleries) become native `overflow-x: auto` + `scroll-snap` rows
  on phones instead of shrinking to unreadable thumbnails.
