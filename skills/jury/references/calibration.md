# Calibration: the critic against real juries

The critic scores stills and measurements under a strict rubric. A real jury browses the live
site, feels the motion, hears the sound, and doesn't run axe or throttle a phone. The two scales
differ, and this file holds the measured gap.

**This file is for the agent writing the score card, never for the critic.** A critic that knows
the gap scores toward it. The jury scores below appear nowhere in `quality-bar.md` for the same
reason.

## Runs

Each site was scored with the normal /jury workflow (`shoot.mjs --crawl --nav`, `audit.mjs`,
one fresh critic with the brief from `quality-bar.md`) on Oct 15 2026, a week after its award.
Jury scores are from the site's page on awwwards.com.

| Site of the Day | | Overall | Design | Usability | Creativity | Content |
|---|---|---|---|---|---|---|
| Maria Vasilyeva portfolio, Oct 9 2026 (mariavasilyeva.com) | jury | 7.28 | 7.31 | 7.02 | 7.56 | 7.33 |
| | critic | 6.15 | 6.5 | 5.0 | 7.0 | 6.5 |
| LPAS architecture studio, Oct 10 2026 (lpas.com) | jury | 7.24 | 7.19 | 7.19 | 7.31 | 7.50 |
| | critic | 6.10 | 6.5 | 5.5 | 6.5 | 5.5 |

| Developer areas | | Sem/SEO | Anim | A11y | WPO | Resp | Markup |
|---|---|---|---|---|---|---|---|
| Maria Vasilyeva | jury | 7.20 | 8.00 | 6.40 | 7.60 | 7.40 | 7.00 |
| | critic | 4 | 6.5 | 3 | 6.5 | 5 | 6.5 |
| LPAS | jury | 7.80 | 8.00 | 7.00 | 7.60 | 7.40 | 7.20 |
| | critic | 5 | 5 | 4 | 3.5 | 6 | 4.5 |

Not usable: TWKS (Site of the Day, Aug 2020; jury 7.52). twks.ch has been rebuilt since, so
today's site isn't the one the jury scored.

## What the gap says

- **Overall: the critic ran 1.13 and 1.14 below the jury.** Two sites agree closely, but two is
  few, and both are winners: the gap on weaker sites is not measured.
- **Closest on what both judge from the page:** Design (0.75 below on average) and Creativity
  (0.69 below).
- **Furthest on what only the critic measures:** Accessibility (3.2 below), Semantics/SEO (3.0)
  and WPO (2.6). Juries rarely run axe, tab through a page or throttle a phone; the critic does
  every time. Both winners lost focus on the first Tab, or had no skip link and serious axe
  violations, and the jury still gave Accessibility 6.4 and 7.
- **Animations/Transitions (2.25 below):** the jury watches the motion; the critic sees frames.
- The LPAS critic read `mobile.loaderMs` (29.7 s) as a loader. It was the load event of a 5.3 MB
  page on the throttled phone, since split into `loadMs` and `loaderMs`. That cost it some WPO
  and Usability points, so part of its gap is a reporting bug that is now fixed.

## Using it on a score card

- **Jury estimate = critic overall + 1.1.** Write it as "about 7.3", never with two decimals,
  and say it comes from two sites.
- Put the band on the estimate, against real thresholds: Honorable Mention from 6.5, recent
  Sites of the Day 7.2 to 7.6.
- Leave the critic's own scores and fix list as they are. The fixes are real even where a jury
  would forgive them, and the strict scale is what makes the list useful.
- Don't estimate jury scores for the developer areas. The gap there is too wide and too uneven.

## Adding a run

1. Pick a Site of the Day from the last few weeks, so the live site is the one the jury scored.
   Its awwwards.com page lists the jury scores; write them here, never anywhere the critic reads.
2. Run /jury on it as usual, one fresh critic.
3. Add both rows above, then recompute the offset from every usable run.

A run on a site that won nothing (or only an Honorable Mention) is the most useful next one: it
shows whether the gap holds below the winners.
