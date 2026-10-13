---
name: bosskuai-uswds
description: "Use when building or auditing a U.S. federal or public-sector site with the U.S. Web Design System (USWDS): theme through design tokens and Sass settings, official components, .gov banner and Identifier, Drupal or WordPress."
---

# BosskuAI USWDS

Use this skill for frontend work on government interfaces built with USWDS. The rule of thumb is to theme through tokens, use the maintained components, and keep the package upgradable instead of overriding it.

## How this differs from nearby skills

- **`bosskuai-design-systems`**: creating or auditing a design system in general (DESIGN.md, tokens, components). USWDS is an existing system you adopt, so this skill is about using it correctly.
- **`accessibility`**: WCAG audits and fixes for any UI. Combine it with this skill for AT testing.
- **`bosskuai-ui-ux-design-to-code`**: mockups to code; here the component library is fixed by USWDS.
- **`antislop-ui`**: audits generic-looking visuals, which does not apply to a mandated design language.

## Workflow

1. Foundation. Confirm the USWDS version, how it is integrated (npm with the official compile tooling, or CDN), and the upgrade plan. Check the current USWDS documentation for settings names, which change between major versions.
2. Theme settings file. Express the agency brand as USWDS design tokens in the project's theme settings (colour families and grades, spacing unit, type scale, fonts). Set tokens; do not write override CSS on USWDS classes, and do not edit files inside `node_modules`.
3. Components. For each need (accordion, alert, date picker, combo box, modal, step indicator, side nav, forms), use the official component, its documented markup and classes, and its JavaScript initialisation. Customise only through settings, utility classes, documented variants, or by composing components. If nothing fits, build a new component from USWDS pieces and document why.
4. Required federal elements. Check that the official government banner and the Identifier (with its required links) are present using the official components, as listed in current federal website standards.
5. Layout. Build mobile-first on the USWDS grid and breakpoints. Use spacing units, type-scale tokens, and colour tokens instead of magic numbers. Verify at small widths, at 400 percent zoom without horizontal scroll, and on a real phone.
6. Forms. Use USWDS form patterns for labels, hints, validation, and error states.
7. CMS integration. In Drupal, enqueue assets as theme libraries and map components to templates or single-directory components with matching markup. In WordPress, enqueue assets in the theme and have blocks and template parts output USWDS markup. Keep custom code separate from the package.
8. Verification. Keyboard and screen-reader pass on every component and flow, contrast re-checked after theming, banner and Identifier confirmed, HTTPS enforced, version pinned, changelog reviewed.
9. Audit mode. Find drift: hard-coded hex values, forked components, off-system widgets, vendor edits. Report each with the token or component that replaces it.

## Guardrails

- Accessibility is the baseline. Do not break the keyboard, focus, role, and contrast behaviour the components ship with.
- Federal requirements (Section 508, WCAG level, the 21st Century IDEA Act, the Federal Website Standards) are legal and policy matters that change. Check current official sources; this skill organises the work and is not legal or compliance advice. A qualified accessibility and compliance reviewer must sign off before launch.
- Do not publish, change a live government site, or file a conformance statement without explicit user approval.
- Do not ship third-party widgets that you have not tested for accessibility.

## Output format

```text
USWDS version and integration: [version, npm/CDN]
Token map: [token, value, reason]
Component decisions: [need, component, custom? why]
Required elements check: [banner, identifier, header/footer, HTTPS]
Responsive checks: [widths, zoom, device]
CMS plan: [Drupal/WordPress steps]
Accessibility results: [tests, findings]
Drift findings: [item, replacement]
```

Adapted from agency-agents/engineering/engineering-uswds-developer.md (agency-agents, MIT).
