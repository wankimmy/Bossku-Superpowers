---
name: bosskuai-baidu-seo-specialist
description: "Use when a site must rank on Baidu for mainland China: ICP filing, China hosting, Chinese keyword research, Baidu Webmaster setup, Baidu ecosystem pages, and a Baidu SEO audit that is not Google SEO."
---

# BosskuAI Baidu SEO Specialist

Use this skill to plan or audit search visibility on Baidu for a mainland China audience. Baidu differs from Google in compliance, hosting, language, crawling, and which properties it favours.

## How this differs from nearby skills

- **`seo-audit`**: general technical and on-page SEO, Google-centred. Use it first for site-agnostic fixes; use this skill when Baidu and China rules decide the work.
- **`bosskuai-seo-geo`**: one-pass SEO plus AI-answer readiness for your own site, not China-specific.
- **`ai-seo`**: getting cited in AI answers, not Baidu ranking.
- **`programmatic-seo`**: pages at scale from templates; can be combined, but it does not cover Baidu rules.

## Workflow

1. Compliance first. Confirm the site has a valid ICP filing (备案) and record the filing number. If it is missing, the filing is the first task. Check current filing rules and timelines with the official regulator or the hosting provider.
2. Hosting and network. Check where the server sits and latency from mainland cities. Plan a CDN that works inside China.
3. Blocked resources. List scripts, fonts, analytics, captchas, and embeds that are blocked or slow in China and replace them with domestic equivalents (for example Baidu Tongji for analytics).
4. Webmaster setup. Verify the site in Baidu's webmaster tool, submit sitemaps, and read crawl and index reports. Check robots.txt against Baiduspider.
5. Rendering. Confirm Baiduspider can read the content. Prefer server-rendered HTML for key pages; test with the webmaster tool's fetch or diagnosis feature.
6. Keyword research in Chinese. Mine Baidu Index, Baidu autocomplete, related searches, and the paid keyword planner. Classify: core, long-tail, brand, competitor, question. Map synonyms and regional wording. Do not translate English keywords.
7. On-page. Write Simplified Chinese titles and descriptions. Check current Baidu guidance for length limits before applying a number.
8. Content. Original content, accurately titled. Health, finance, and legal topics need extra care and proof of qualification.
9. Ecosystem presence. Decide which Baidu properties fit (Baike, Zhidao, Tieba, Wenku, Jingyan). Each has its own editorial rules; follow them.
10. Off-page. Earn links from relevant Chinese sites. Check paid and organic overlap if Baidu ads run too.
11. Track: indexed pages, rankings on a fixed keyword set, organic traffic, crawl errors, brand-query results.

## Guardrails

- Algorithm names, limits, and product names change. Verify against current Baidu documentation before stating them as fact.
- Do not use click farms, fake CTR, scraped duplicate content, or bought-account seeding. These violate Baidu rules and risk penalties.
- Content restrictions and data-localisation law are legal topics. This skill organises the work; confirm requirements with a qualified China-based adviser. Do not file anything or submit to any regulator or platform without explicit user approval.
- Keep brand mentions in Q&A or community posts honest and disclosed.

## Output format

```text
Compliance: [ICP status and number, hosting, blocked resources]
Technical: [crawl, rendering, mobile, speed, sitemap]
Keywords: [classified table with intent]
Content and ecosystem plan: [pages, properties, owners]
Risks: [compliance, algorithm, unverified claims]
Next 3 actions: [owner, date]
```

Adapted from agency-agents/marketing/marketing-baidu-seo-specialist.md (agency-agents, MIT).
