---
name: bosskuai-cms-development
description: "Use when building or reviewing a WordPress or Drupal site: custom theme or plugin/module, content model, Gutenberg or Layout Builder blocks, config in code, and a pre-launch security, accessibility, and performance check."
---

# BosskuAI CMS Development

Use this skill for code-first WordPress and Drupal work, where editors need a model they can use and developers need something maintainable.

## How this differs from nearby skills

- **`bosskuai-laravel-development`**: a custom PHP application on Laravel. Use this skill when the product is a CMS site.
- **`bosskuai-ui-ux-design-to-code`**: turning a design into UI. This skill covers the CMS structure under the theme.
- **`accessibility`**: the full WCAG audit method; this skill only adds the CMS-specific pass.
- **`bosskuai-web-performance`**: general web performance. Use it for Core Web Vitals deep dives.
- **`seo-audit`**: search audit; this skill only wires schema, sitemap, and robots correctly.

## Workflow

1. Confirm the target: WordPress or Drupal, new build or existing site, and the exact versions of core and major plugins/modules. Check the installed version or current official docs before using an API.
2. Lock the content model before theme code: content types, fields, relationships, display variants, editorial roles and workflow, multilingual needs.
3. Choose extensions deliberately. For each contrib plugin/module check last update, active installs, open issues, and security advisories. Do not build what a maintained extension already does.
4. Put structure in code: post types, taxonomies, fields, and blocks in code (WordPress: ACF JSON sync or code registration; Drupal: config export to YAML). The admin UI alone is not a source of truth.
5. Use child themes or custom themes; never edit a parent or contrib theme. Use hooks, filters, and plugin/module APIs; do not patch core.
6. Build the theme top-down: layout, regions, blocks, components, with design tokens as CSS custom properties. Use the CMS asset system (WordPress enqueue with version and defer; Drupal `.libraries.yml` attached per template).
7. Escape output and validate input at every boundary (WordPress `esc_html`, `esc_url`, nonces; Drupal Twig autoescape, access checks, cache metadata).
8. Run coding standards (PHPCS with WordPress or Drupal rulesets) and unit tests for business logic; add an end-to-end test for the main editor flow.
9. Walk the editor workflow as a non-technical user. If it is confusing, fix the CMS experience.
10. Pre-launch: config exported, debug off, errors logged not shown, caching headers and object cache, security headers, robots and sitemap, accessibility scan plus keyboard check, Core Web Vitals measured, update plan handed over.

## Guardrails

- Do not run migrations, updates, or config imports against a live site without a backup and the user's approval.
- Do not store secrets in the database or theme files; use environment config.
- Plugin/module and PHP API names change between versions; verify against the installed version.

## Output format

```text
Target: [CMS + versions, new/existing]
Content model: [types, fields, roles]
Extensions: [name, reason, vetting result]
Code layout: [theme, plugin/module, config]
Checks: [PHPCS, tests, a11y, performance, security]
```

Adapted from agency-agents/engineering/engineering-cms-developer.md (agency-agents, MIT).
