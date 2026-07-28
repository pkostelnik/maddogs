# Mad Dogs Germany — Website Redesign Prototype

**Date:** 2026-07-28  
**Status:** Approved for implementation planning  
**Scope directory:** `grok45/` only (greenfield)  
**Live reference:** https://www.mad-dogs-germany.de

---

## 1. Goal

Build a full multi-page redesign prototype of Mad Dogs Germany that:

- Modernizes layout, IA, UX, and visual identity
- Feels **Outdoor Athletic**, not generic “AI slop” pet-site design
- Is **mobile-first**, accessible (WCAG 2.1 AA target), and best-practice static web
- Covers **all live site topics** (full showcase), without implementing real checkout or CMS
- Lives entirely inside `grok45/` using **vanilla HTML, CSS, and JavaScript**

### Success criteria

- Clear dual conversion paths: **Services** and **Shop**
- Navigation is simpler and more scannable than the live site
- Keyboard-usable mobile menu, visible focus, semantic structure, reduced-motion support
- Consistent design system (tokens → components → pages)
- Real business facts preserved; marketing copy modernized; lorem/broken live content replaced
- External shop/merch links point to real destinations with correct URLs
- Prototype runs via static files (local open or simple static server)

### Out of scope

- Real backend, email delivery, analytics, cookie consent platform, site translator
- Full e-commerce product catalog, cart, checkout, accounts
- CMS, build tooling, frameworks (React/Vue/Astro/etc.)
- Work outside `grok45/`
- Pixel-perfect recreation of the old WordPress theme

---

## 2. Product context

Mad Dogs Germany is a German dog specialist brand combining:

- **Services:** professional dog walking (incl. demanding dogs), Man/Pet Trail, scent/sport dog expertise
- **Commerce:** equipment shop (external), Reico dog food partner content, branded clothing (Spreadshop)
- **Trust:** owner Chris’s sport/training credentials, customer voices, gallery

**Primary audience:** dog owners near Niederkassel / region seeking capable handling for energetic or challenging dogs; buyers of quality gear; people interested in nosework/trail and sport.

**Primary actions:** contact via WhatsApp/phone for services; browse categories into external shop; explore brand trust content.

---

## 3. Approach

**Chosen:** Dual-Hub Multi-Page (vanilla static site)

Rejected:

- One-page story site — too shallow for full live topic coverage
- SPA app-shell — unnecessary complexity, weaker progressive enhancement

---

## 4. Information architecture

### Primary navigation

| Label | Target | Notes |
|-------|--------|--------|
| Start | `index.html` | |
| Services ▾ | — | Dropdown/disclosure: Dogwalker, Man/Pet Trail, Spürhunde, Sporthunde, Galerie |
| Shop ▾ | — | Dropdown: Shop-Übersicht, Reico, Bekleidung |
| Über uns | `ueber-uns.html` | |
| Stimmen | `stimmen.html` | “Das sagen unsere Kunden” |
| Kontakt | `kontakt.html` | |

Header utilities (desktop + mobile drawer): Instagram, phone, WhatsApp (service intent).

### Footer

- Repeat primary groups (Services, Shop, Marke)
- Legal: Impressum, AGB, Datenschutz
- Contact block: phone, email, WhatsApp, Instagram
- Copyright Mad Dogs Germany
- Optional one-line prototype note (not a cookie wall)

### Removed / fixed vs live

- Remove broken “test” nav item and malformed Spreadshop path slugs from IA
- Bekleidung uses correct Spreadshop URL: `https://mad-dogs-germany.myspreadshop.de/`
- Shop categories deep-link to live shop category URLs where known
- Dogwalker legal pages remain available site-wide (not buried only under dogwalker)

### Page inventory

| File | Purpose |
|------|---------|
| `index.html` | Dual-hub homepage |
| `dogwalker.html` | Dog walking service + pricing + CTA |
| `trail.html` | Man/Pet Trail |
| `spuerhunde.html` | Scent dogs expertise page |
| `sporthunde.html` | Sport dogs expertise page |
| `galerie.html` | Photo gallery + accessible lightbox |
| `shop.html` | Category hub → external shop |
| `reico.html` | Reico food partner page |
| `bekleidung.html` | Merch teaser → Spreadshop |
| `ueber-uns.html` | Chris / brand story |
| `stimmen.html` | Testimonials |
| `kontakt.html` | Contact form + direct channels |
| `impressum.html` | Legal imprint (structured; finalize with owner data) |
| `agb.html` | Terms (structured placeholder/content from live where available) |
| `datenschutz.html` | Privacy (structured placeholder suitable for static prototype) |

---

## 5. Visual design system

### Mode

**Persuade** (marketing site) with strong operational clarity on service/contact pages.

### Aesthetic direction: Outdoor Athletic

- Dark base, high contrast type, one decisive accent
- Sport/trail energy without cyber-neon or generic SaaS gradients
- Photography-forward sections with dark scrims for legibility
- Sharp, confident UI: restrained radius, thin borders, purposeful motion

### Color tokens (implementation targets)

| Token | Role | Guidance |
|-------|------|----------|
| `--color-bg` | Page background | Near-black / deep anthracite (`#0B0D10`) |
| `--color-surface` | Cards/panels | Slightly lifted (`#141820`) |
| `--color-surface-2` | Nested surfaces | `#1B2130` |
| `--color-border` | Dividers | Low-contrast cool gray border |
| `--color-text` | Primary text | Off-white |
| `--color-text-muted` | Secondary text | Muted gray, still ≥ 4.5:1 on bg where used as body |
| `--color-accent` | CTAs, links, focus | Warm amber/orange signal (single accent family) |
| `--color-accent-hover` | Hover/active | Darker/brighter step of accent |
| `--color-support` | Optional nature cue | Muted moss — never primary CTA |
| `--color-danger` | Form errors | Clear red, not only color (icon/text too) |
| `--color-success` | Form success | Clear green + text |

No purple-blue AI gradients. No rainbow accents.

### Typography

| Role | Direction |
|------|-----------|
| Display / headings | Distinctive sans with athletic character (e.g. Syne or Outfit via Google Fonts) |
| Body / UI | Highly readable sans (e.g. Source Sans 3 or DM Sans) |
| Scale | Fluid `clamp()` scale: hero, h1–h3, lead, body, small |
| Style | Tight display tracking sparingly; body comfortable 1.5–1.7 line-height |

### Spacing & layout

- 8px spacing scale
- Content max-width ~1120–1200px
- Section vertical rhythm generous on mobile, denser but breathable on desktop
- Grid: 1 col mobile → 2–3 col cards where content warrants
- Avoid equal-weight “three generic feature icons” blocks without real copy

### Components

- **Buttons:** primary (filled accent), secondary (light outline), ghost
- **Cards:** surface + border; optional media top
- **Badges/pills:** for price tags, “Externer Shop”, location
- **Forms:** top labels, required indicators, inline errors, checkbox legal consent
- **Nav:** sticky header; mobile full-screen/drawer with focus trap, Escape, restored focus
- **Lightbox:** dialog semantics, focus trap, arrow optional, close button, Esc
- **Skip link:** first focusable control
- **Focus:** visible `:focus-visible` ring using accent

### Motion

- Short transitions (150–250ms) on interactive UI only
- Honor `prefers-reduced-motion: reduce` (no non-essential animation)

### Imagery strategy

- Placeholder visuals in-brand (CSS/SVG/graded blocks) plus `assets/images/README.md` asset checklist
- Prefer local assets under `assets/`; do not depend on fragile hotlinks for core layout
- When using stock-like placeholders, caption what real photo should replace them
- Gallery page demonstrates real interaction pattern even with placeholders

### Anti-slop rules (mandatory)

- No Inter/Roboto default pairing as the “design”
- No centered wall-of-text hero without hierarchy
- No decorative glassmorphism soup
- No icon row that could belong to any startup
- No fake metrics (“10k+ happy pets”) unless sourced
- Personality comes from trail/work-dog language, structure, and craft — not stickers

---

## 6. UX & content by page

### Global content rules

- Language: **German** (UI and copy)
- Modernize wording; keep factual claims aligned with live site (prices, location, credentials)
- Replace live lorem (e.g. parts of Trail page) with coherent Man/Pet Trail explanations
- Chris CV: highlight story + milestones first; long seminar list behind progressive disclosure (`<details>` or equivalent)
- Testimonials: use real quotes if available from live page; otherwise clearly labeled replaceable samples
- Legal pages: honest structure; mark owner-final fields where prototype cannot assert legal completeness
- Phone (from live): service contact `0173 3649143` / WhatsApp `https://wa.me/491733649143`
- Email: `info@mad-dogs-germany.de` (header live); do not invent alternate primary emails in UI chrome
- Instagram: `https://www.instagram.com/mad_dogs_germany/`
- Location emphasis: Niederkassel und Umgebung

### Homepage (`index.html`)

1. Hero: clear value proposition + dual CTAs (Services / Shop)
2. Services snapshot cards → deep links
3. Shop category teaser → `shop.html` / external
4. Trust strip: Chris one-liner + link to Über uns
5. Testimonials teaser → Stimmen
6. Final CTA band: WhatsApp / Kontakt

### Dogwalker (`dogwalker.html`)

- Positioning: structured walks for energetic / demanding dogs, not “just a stroll”
- Benefits and fit criteria (from live)
- Group size note (up to 10 where stated live)
- Pricing table: 1h 20€ · 1,5h 25€ · 2h 30€
- Primary CTAs: WhatsApp, Call
- Secondary: Kontakt form, Galerie

### Trail (`trail.html`)

- Explain Man/Pet Trail in plain German
- Benefits: nosework, bond, mental load
- Trainer credibility (Pet Trailer AT training)
- CTA: Kontakt / Anfrage

### Spürhunde / Sporthunde

- Distinct pages, shared layout pattern
- Expertise framing tied to brand experience
- Cross-links to Trail, Dogwalker, Über uns, Kontakt

### Galerie (`galerie.html`)

- Responsive image grid
- Accessible lightbox
- Link back to Dogwalker / Kontakt

### Shop (`shop.html`)

- Intro: quality gear hub
- Category cards linking to live shop categories:
  - Halsbänder, Leinen, European Pet Pharmacy, Non Stop Dogwear, Trail Zubehör, Mäntel/Jacken, Bücher, Sonstiges, Kurse
- Each external link labeled as external
- No fake product grid pretending to be a full cart shop

### Reico (`reico.html`)

- Partner/food value page, trust-oriented
- CTA toward contact or purchase path consistent with available public info (no invented medical claims)

### Bekleidung (`bekleidung.html`)

- Brand merch story
- Strong CTA to Spreadshop

### Über uns (`ueber-uns.html`)

- Human story of Chris
- Milestone chips (THS, Meisterschaft, Ehrenpreise, Diensthund, Trainer paths)
- Education list collapsed by default

### Stimmen (`stimmen.html`)

- Quote cards, optional first-name attribution
- CTA to Kontakt / Dogwalker

### Kontakt (`kontakt.html`)

- Direct channels first (phone, WhatsApp, mail, Instagram)
- Form fields: Name*, E-Mail*, Nachricht*, privacy consent*
- Client-side validation + success/error UI (demo only, no network send)
- No dark patterns on consent

### Legal pages

- Readable typography, headings, last-updated note
- Impressum fields structured for German requirements; use known public contact data where appropriate and placeholder only when unknown
- Do not invent company registration details

---

## 7. Technical architecture

### Stack

- HTML5, CSS3, vanilla ES modules or plain JS (no build step)
- Optional Google Fonts (with `preconnect` + font-display swap)
- No npm requirement to view

### Directory layout

```text
grok45/
├── index.html
├── dogwalker.html
├── trail.html
├── spuerhunde.html
├── sporthunde.html
├── galerie.html
├── shop.html
├── reico.html
├── bekleidung.html
├── ueber-uns.html
├── stimmen.html
├── kontakt.html
├── impressum.html
├── agb.html
├── datenschutz.html
├── css/
│   ├── tokens.css
│   ├── base.css
│   ├── layout.css
│   └── components.css
├── js/
│   ├── main.js
│   ├── form.js
│   └── gallery.js
├── assets/
│   ├── favicon.svg
│   ├── icons/
│   └── images/
│       └── README.md
└── docs/superpowers/specs/
    └── 2026-07-28-mad-dogs-redesign-design.md
```

### Shared page chrome

- Repeated header/footer markup per page (static prototype; keep consistent via careful copy)
- Shared CSS/JS includes
- `main.js` on all pages; `form.js` on contact; `gallery.js` on gallery

### JS responsibilities

| File | Responsibility |
|------|----------------|
| `main.js` | Mobile nav toggle, focus trap, Escape, body scroll lock, active nav state, dropdown keyboard support |
| `form.js` | Validate required fields + email + consent; announce errors; show success state |
| `gallery.js` | Open/close lightbox dialog; focus management; prev/next if multiple |

### Accessibility requirements

- One `h1` per page; logical heading order
- Landmark regions: header, nav, main, footer
- Alt text meaningful; decorative images empty alt
- Contrast AA for text and UI controls
- Target sizes ≥ 44px where primary controls
- Form labels associated with controls
- Dialog/lightbox: `role="dialog"`, `aria-modal="true"`, labelled by title
- Language: `<html lang="de">`

### Performance

- Minimal JS
- Lazy-load below-fold images
- Prefer SVG icons
- Avoid heavy carousels/autoplay video

### External link policy

- `target="_blank"` only when useful for shop handoff; always `rel="noopener noreferrer"`
- Visible external indication in copy or icon + accessible name

---

## 8. Key user flows

### Service conversion

`Start` → `Dogwalker` or `Trail` → WhatsApp / Call / `Kontakt`

### Shop conversion

`Start` → `Shop` → category (external live shop)  
or `Bekleidung` → Spreadshop

### Trust path

`Start` → `Über uns` / `Stimmen` / `Galerie` → `Kontakt`

---

## 9. Testing & verification (prototype)

Manual checks before calling done:

- [ ] All internal links resolve within `grok45/`
- [ ] Mobile nav keyboard + screen-reader basic pass
- [ ] Homepage dual CTAs obvious above the fold on 375px
- [ ] Contact form validation states work without server
- [ ] Gallery lightbox open/close/focus
- [ ] External shop/merch URLs correct
- [ ] Reduced motion does not break UI
- [ ] Legal pages reachable from footer on every page
- [ ] No edits outside `grok45/`

---

## 10. Decisions log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Scope | Full redesign showcase | User chose full multi-page relaunch prototype |
| Page set | All live topics | User chose complete coverage including Reico, Bekleidung, Galerie, legal |
| Stack | Vanilla HTML/CSS/JS | User choice; simple static demo |
| Visual | Outdoor Athletic dark | Fits sport/trail/work-dog brand |
| CTA strategy | Dual Service + Shop | Matches real business split |
| Content | Modernized real facts | Credible prototype without waiting on full asset drop |
| Commerce | Link out | Avoid fake checkout; reuse live shop systems |

---

## 11. Next step

After user approval of this written spec → create implementation plan via writing-plans, then build only inside `grok45/`.
