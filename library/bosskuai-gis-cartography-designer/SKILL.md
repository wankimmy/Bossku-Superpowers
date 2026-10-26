---
name: bosskuai-gis-cartography-designer
description: "Use when styling a map so it reads clearly: colour schemes and classification, colour-blind-safe palettes, labels and typography, basemap choice, legend and layout, for print or web maps in QGIS, ArcGIS, or MapLibre."
---

# BosskuAI GIS Cartography Designer

Use this skill when the data is ready and the map must communicate. Cartography is information design: each colour, font, and label either helps the reader or gets in the way.

## How this differs from nearby skills

- **`bosskuai-gis-spatial-data-engineer`**: cleaning, converting, and reprojecting the data before it is styled.
- **`bosskuai-xr-interface-architect`**: spatial UI for headset apps, not maps.
- **`accessibility`**: general WCAG for UI; this skill applies colour-vision and contrast checks to map symbology.
- **`antislop-ui`**: audits generic-looking interface visuals; maps need the rules below instead.

## Workflow

1. Purpose. Who reads this map, what should they learn, and what decision does it support?
2. Medium. Print PDF, web tiles, slide, or dashboard. Print needs more contrast; small screens need simpler symbols; dark maps need light labels.
3. Basemap. Match context to the job: street for urban data, terrain or hillshade for environment, minimal light or dark grey when the data should dominate, or none for a poster.
4. Data-to-colour match. Sequential ramp for magnitude, diverging ramp for deviation from a midpoint, qualitative hues for categories, a high-contrast pair for yes/no.
5. Classification. Choose the method (natural breaks, quantiles, equal interval, manual) that fits the distribution, and look at the histogram before choosing. State the method on the map.
6. Colour-vision safety. Avoid red-green pairs; use blue-orange or another tested pair. Check with a colour-blindness simulator and a palette checker.
7. Labels. Rank features by importance, scale label size to rank, add halos over busy backgrounds, and handle multilingual and rotated text. Test collisions at each zoom or scale.
8. Generalise for scale. Do not draw every building at a small scale; simplify or drop detail.
9. Layout. Visual hierarchy (what is seen first, second, third), a legend that decodes every symbol, scale bar, north arrow where relevant, title, source and credits.
10. Review. Show the map to someone new and ask what it says. Check line weights, symbol consistency, tile-edge clipping, and series consistency.
11. Export at the right resolution, format, and colour space for the medium.

## Guardrails

- Fewer layers beat more. If a layer does not support the purpose, remove it.
- Check licence and attribution rules for each basemap and tile provider; some free tiers restrict heavy or commercial use.
- Do not hide uncertainty or data gaps with smooth colours. Show "no data" distinctly.
- Maps used for legal boundaries, navigation, or safety decisions need review by a qualified professional.
- Verify tool-specific style options in the installed QGIS, ArcGIS, or MapLibre docs.

## Output format

```text
Purpose and audience: [text]
Medium and size: [print / web / dashboard]
Basemap: [choice and reason]
Symbology: [data type, ramp, classes, method]
Labels: [fonts, hierarchy, halo rules]
Layout: [legend, scale, credits]
Checks: [colour-vision, contrast, readability test]
```

Adapted from agency-agents/gis/gis-cartography-designer.md (agency-agents, MIT).
