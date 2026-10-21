# Content and copy

Content is 10% of the score but it colors the other 90%: specific words make a design feel
designed; generic words make any design look like a template.

## Voice

- Write like the person talks at their best: plain, specific, a little personality. Sentence case.
- Say what they do, for whom, and what is different, in under 20 words for the hero line.
- Concrete nouns and verbs over adjectives. "I design and build websites for architects and
  galleries" beats "Crafting meaningful digital experiences".
- No em or en dashes in visible text (they read as generated). Use periods, commas, colons, parentheses.
- Banned: elevate, seamless, unleash, cutting-edge, next-gen, synergy, passionate, pixel-perfect,
  "crafting digital experiences", "where X meets Y", "not just X, but Y".
- Labels say what they are: "Work", "About", "Contact", "Next project". No "Explore our universe".
- One action, one name across the site: if the CTA is "Email me", the footer says "Email me" too.

## Honest placeholders (name-only prompts)

When facts are missing, write **plausible, clearly fictional** content that demonstrates the design,
and mark it:
- In `src/data/site.ts`: `placeholder: true` on invented projects; a top comment listing every assumption.
- Projects: invent believable client types and briefs, never real company names or logos, never
  awards, never metrics presented as fact. Titles can be evocative but should sound like real
  project names ("Harbor Lights", "Atlas of Small Rooms"), not lorem ipsum.
- Bio: plausible and modest. "Based in [city]" only if known; otherwise omit location.
- Contact: use an obvious placeholder the owner must replace (`hello@<name>.studio` style domain
  derived from the name) and list it in the final message.
- Images: generated (image tool) or procedural covers; never stock photos of strangers presented
  as the person or their work.

## The content file (`src/data/site.ts`)

Every visible string and project lives in one typed file, so the owner can swap in real
material without touching markup. Extend the shape to fit the site (products, services,
chapters).

```ts
// Assumptions: <list every invented fact here, mirrored in the final message>.
export type Project = {
  slug: string;
  title: string;
  client: string;
  year: number;
  role: string[];
  summary: string;                                     // one sentence: what changed, for whom
  cover: { src?: string; alt: string; seed: number };  // no src → procedural GL cover (seeded)
  body: { heading: string; text: string }[];           // context, idea, craft, outcome
  placeholder?: boolean;                               // true = invented, owner must replace
};

export const site = {
  name: 'Ana Ruiz',
  role: 'Independent designer & creative developer',
  url: 'https://anaruiz.studio',                       // production URL: canonical, OG, sitemap
  description: '120 to 160 characters, a human sentence about what they make and for whom.',
  email: 'hello@anaruiz.studio',
  socials: [{ label: 'GitHub', href: 'https://github.com/…' }],
  glPalette: ['#101010', '#6b6b6b', '#f2f2f2'] as [string, string, string], // keep in sync with tokens
};

export const projects: Project[] = [/* … */];
```

## Case study structure (each project page)

1. Title + one-line summary (what was made, for whom, what changed).
2. Meta: client, year, role(s), team/credits, link (if real).
3. Hero media.
4. Context: the problem in 2 to 3 sentences.
5. Idea: the decision that made it work, 2 to 3 sentences.
6. Craft: 3 to 5 media frames with one-line captions about specific details.
7. Outcome: what happened (real results only; otherwise describe what shipped).
8. Next project (continuous transition).

## About section

- A portrait or a working image (honest), 60 to 120 words of bio in first person or third (pick one
  site-wide), services as a short list, clients only if real, a contact line.

## Microcopy

- 404: in the concept's voice, with a way back.
- Loader: name or a short word, plus the counter; no "Loading awesomeness...".
- Alt text: describes the image's content and purpose ("Mobile screens of the Harbor Lights
  booking flow"), not "image of" or the file name. Decorative images: `alt=""`.
- Footer: name, year, real links (email, social), maybe a colophon (typefaces, built with): designers read it.
- Meta descriptions: unique per page, 120 to 160 characters, human sentences.
