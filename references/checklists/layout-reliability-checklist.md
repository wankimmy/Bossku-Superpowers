# Layout Reliability Checklist

A layout that breaks on real content is a bug, not a nit. Fix the geometry. A global `overflow-x: hidden` on `html`, `body` or a wrapper hides the defect, so it is a defect itself, not a fix.

## Prevention

- [ ] Flex and grid children where text can grow get `min-width: 0` (and `min-height: 0` for scroll areas).
- [ ] Use flexible widths, `max-width`, `minmax()` and `clamp()` instead of fixed pixel widths.
- [ ] Long words, emails and URLs wrap: `overflow-wrap: anywhere` or `word-break`, with `hyphens` where the language allows.
- [ ] Inputs and buttons can shrink (`min-width: 0`, `width: 100%` in a flex row).
- [ ] Modals and drawers have a `max-height` (use `dvh`) and scroll inside; the close control stays visible.
- [ ] Know the stacking contexts: `transform`, `filter`, `opacity` below 1, `position` with `z-index` and `isolation` each create one. A clipped dropdown needs a portal, not a bigger `z-index`.
- [ ] Respect safe-area insets (`env(safe-area-inset-*)`) on fixed headers, footers and bottom bars.
- [ ] Set breakpoints where the content breaks, not at device names.
- [ ] Tables scroll inside their own container (`overflow-x: auto`) or restack into cards on small screens. The page itself must not scroll sideways.
- [ ] Content reflows at 320 CSS px with no two-dimensional scrolling, text resizes to 200 percent, and a focused element is not hidden by sticky UI [U6: WCAG 2.2 1.4.10, 1.4.4, 2.4.11].
- [ ] Pointer targets are at least 24 by 24 CSS px, 44 by 44 for primary and touch controls [U6: 2.5.8 for the 24 floor; 44 is house practice].
- [ ] Reserve space for images, ads and late content so the page does not jump; Cumulative Layout Shift good is below 0.1 [C4: Google targets, not outcome proof].

## Test data

Put these into the real screens, not just a mock:

- [ ] Long names (60 characters, no spaces) and long emails.
- [ ] Large amounts (1,234,567,890.00) and negative values.
- [ ] Long error text and long validation messages.
- [ ] Translated strings about 30 to 40 percent longer; a right-to-left locale if the product ships one.
- [ ] Empty list, one item, and an overloaded list (hundreds of rows).
- [ ] Text zoom at 200 percent.

## The check

```bash
node <BosskuAI install>/scripts/layout-check.mjs <url>
```

Run it at widths 320, 375, 390, 768, 1024, 1440 and 1920. Exit 0 means no errors (read any warnings it lists), 1 means errors to fix, 2 means the check did not run. Exit 2 is not a pass: say the check did not run.

Then take screenshots with `node <BosskuAI install>/scripts/shot.mjs <url>` (add `--widths 320,768` for flagged widths) and look at them. The session-start line prints both full paths. A clean exit does not prove the design is good. Pixel baselines catch change, not quality, and only compare like environments [C5: Playwright docs].

Report widths, pages and data run. Source ids: the playbook's section 8. Never claim a visual check that did not happen.
