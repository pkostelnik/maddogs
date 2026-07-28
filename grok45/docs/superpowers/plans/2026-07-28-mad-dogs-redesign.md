# Mad Dogs Germany Redesign Prototype — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full multi-page, mobile-first, accessible Outdoor-Athletic redesign prototype of mad-dogs-germany.de entirely inside `grok45/` with vanilla HTML/CSS/JS.

**Architecture:** Static multi-page site. Shared design tokens and component CSS; repeated header/footer markup per page; progressive enhancement via three JS files (`main.js` nav, `form.js` contact, `gallery.js` lightbox). External shop/merch hand off to live systems.

**Tech Stack:** HTML5, CSS3 (custom properties), vanilla JavaScript (no build, no npm), Google Fonts (Syne + Source Sans 3).

**Spec:** `grok45/docs/superpowers/specs/2026-07-28-mad-dogs-redesign-design.md`

## Global Constraints

- Work **only** inside `grok45/` — never edit sibling model folders or repo root site files
- Language: **German** UI and copy
- Stack: vanilla HTML/CSS/JS only — no React/Vue/Astro/npm build
- Aesthetic: Outdoor Athletic dark — no Inter/Roboto-as-brand, no purple gradients, no fake metrics
- Dual CTAs: Services + Shop
- Contact: phone `0173 3649143`, WhatsApp `https://wa.me/491733649143`, email `info@mad-dogs-germany.de`, Instagram `https://www.instagram.com/mad_dogs_germany/`
- Spreadshop: `https://mad-dogs-germany.myspreadshop.de/`
- Shop base: `https://www.mad-dogs-germany.de/mad-dogs-shop-/`
- WCAG 2.1 AA target; `<html lang="de">`; `prefers-reduced-motion`
- Form submit is demo-only (no backend)
- Prices dogwalker: 1h 20€ · 1,5h 25€ · 2h 30€ · location Niederkassel und Umgebung
- Commit only `grok45/**` paths

## File map

| Path | Responsibility |
|------|----------------|
| `css/tokens.css` | Colors, type, space, radii, motion, z-index |
| `css/base.css` | Reset, typography, links, focus, utilities, reduced-motion |
| `css/layout.css` | Skip link, header, nav, footer, sections, grids, page shells |
| `css/components.css` | Buttons, cards, badges, forms, pricing, lightbox, details |
| `js/main.js` | Mobile nav, focus trap, dropdowns, active link, scroll lock |
| `js/form.js` | Contact validation + success UI |
| `js/gallery.js` | Accessible lightbox |
| `assets/favicon.svg` | Brand mark favicon |
| `assets/icons/*.svg` | UI icons (menu, close, external, phone, etc.) |
| `assets/images/README.md` | Real-asset replacement checklist |
| `assets/images/placeholders/*` | Optional SVG/CSS-backed placeholders |
| `*.html` (15 pages) | Content pages with shared chrome |
| `scripts/verify-links.mjs` | Optional Node link checker (Node may exist on machine; not required to view site) |

### Shared head snippet (every HTML page)

```html
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>PAGE_TITLE | Mad Dogs Germany</title>
<meta name="description" content="PAGE_DESCRIPTION" />
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=Syne:wght@600;700;800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="css/tokens.css" />
<link rel="stylesheet" href="css/base.css" />
<link rel="stylesheet" href="css/layout.css" />
<link rel="stylesheet" href="css/components.css" />
```

### Shared header markup (paste identically on every page; set `aria-current="page"` on active item)

```html
<a class="skip-link" href="#main">Zum Inhalt springen</a>
<header class="site-header" data-header>
  <div class="site-header__inner">
    <a class="logo" href="index.html">
      <span class="logo__mark" aria-hidden="true">MD</span>
      <span class="logo__text">Mad Dogs <span>Germany</span></span>
    </a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false">
      <span class="nav-toggle__bars" aria-hidden="true"></span>
      <span class="visually-hidden">Menü öffnen</span>
    </button>
    <nav id="site-nav" class="site-nav" data-nav aria-label="Hauptnavigation">
      <ul class="site-nav__list">
        <li><a href="index.html" data-nav-link>Start</a></li>
        <li class="has-sub">
          <button type="button" class="sub-toggle" data-sub-toggle aria-expanded="false" aria-controls="sub-services">Services</button>
          <ul id="sub-services" class="sub-menu" data-sub-menu hidden>
            <li><a href="dogwalker.html">Dogwalker</a></li>
            <li><a href="trail.html">Man / Pet Trail</a></li>
            <li><a href="spuerhunde.html">Spürhunde</a></li>
            <li><a href="sporthunde.html">Sporthunde</a></li>
            <li><a href="galerie.html">Galerie</a></li>
          </ul>
        </li>
        <li class="has-sub">
          <button type="button" class="sub-toggle" data-sub-toggle aria-expanded="false" aria-controls="sub-shop">Shop</button>
          <ul id="sub-shop" class="sub-menu" data-sub-menu hidden>
            <li><a href="shop.html">Shop-Übersicht</a></li>
            <li><a href="reico.html">Reico Hundefutter</a></li>
            <li><a href="bekleidung.html">Bekleidung</a></li>
          </ul>
        </li>
        <li><a href="ueber-uns.html" data-nav-link>Über uns</a></li>
        <li><a href="stimmen.html" data-nav-link>Stimmen</a></li>
        <li><a class="btn btn--primary btn--nav" href="kontakt.html">Kontakt</a></li>
      </ul>
      <div class="site-nav__utils">
        <a href="tel:+491733649143">0173 3649143</a>
        <a href="https://wa.me/491733649143" rel="noopener noreferrer" target="_blank">WhatsApp</a>
        <a href="https://www.instagram.com/mad_dogs_germany/" rel="noopener noreferrer" target="_blank">Instagram</a>
      </div>
    </nav>
  </div>
</header>
```

### Shared footer markup

```html
<footer class="site-footer">
  <div class="site-footer__grid">
    <div>
      <p class="footer-brand">Mad Dogs Germany</p>
      <p>Professionelle Hundeauslastung, Trail &amp; Ausrüstung — Niederkassel und Umgebung.</p>
    </div>
    <div>
      <p class="footer-heading">Services</p>
      <ul>
        <li><a href="dogwalker.html">Dogwalker</a></li>
        <li><a href="trail.html">Man / Pet Trail</a></li>
        <li><a href="spuerhunde.html">Spürhunde</a></li>
        <li><a href="sporthunde.html">Sporthunde</a></li>
        <li><a href="galerie.html">Galerie</a></li>
      </ul>
    </div>
    <div>
      <p class="footer-heading">Shop</p>
      <ul>
        <li><a href="shop.html">Shop-Übersicht</a></li>
        <li><a href="reico.html">Reico</a></li>
        <li><a href="bekleidung.html">Bekleidung</a></li>
      </ul>
    </div>
    <div>
      <p class="footer-heading">Kontakt</p>
      <ul>
        <li><a href="tel:+491733649143">0173 3649143</a></li>
        <li><a href="mailto:info@mad-dogs-germany.de">info@mad-dogs-germany.de</a></li>
        <li><a href="https://wa.me/491733649143" rel="noopener noreferrer" target="_blank">WhatsApp</a></li>
        <li><a href="kontakt.html">Kontaktformular</a></li>
      </ul>
    </div>
  </div>
  <div class="site-footer__bottom">
    <nav aria-label="Rechtliches">
      <a href="impressum.html">Impressum</a>
      <a href="agb.html">AGB</a>
      <a href="datenschutz.html">Datenschutz</a>
    </nav>
    <p>© <span data-year></span> Mad Dogs Germany. Prototyp-Relaunch.</p>
  </div>
</footer>
<script src="js/main.js" defer></script>
```

### Live shop category URLs (use exactly)

| Label | URL |
|-------|-----|
| Halsbänder | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Halsbander-c161683045/` |
| Leinen | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Leinen-c162746780/` |
| European Pet Pharmacy | `https://www.mad-dogs-germany.de/mad-dogs-shop-/European-Pet-Pharmacy-c167702297/` |
| Non Stop Dogwear | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Non-Stop-Dogwear-c158808265/` |
| Trail Zubehör | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Trail-Zubehor-c158772332/` |
| Mäntel/Jacken | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Mantel-Jacken-c158769055/` |
| Bücher | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Bucher-c168282112/` |
| Sonstiges | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Sonstiges-c193106398/` |
| Kurse | `https://www.mad-dogs-germany.de/mad-dogs-shop-/Kurse-c162134507/` |
| Shop root | `https://www.mad-dogs-germany.de/mad-dogs-shop-/` |

---

### Task 1: Design tokens, base CSS, favicon, asset README

**Files:**
- Create: `grok45/css/tokens.css`
- Create: `grok45/css/base.css`
- Create: `grok45/assets/favicon.svg`
- Create: `grok45/assets/images/README.md`

**Interfaces:**
- Produces: CSS custom properties listed below; base element styles; favicon path `assets/favicon.svg`

- [ ] **Step 1: Write `css/tokens.css`**

```css
:root {
  --color-bg: #0b0d10;
  --color-surface: #141820;
  --color-surface-2: #1b2130;
  --color-border: rgba(232, 236, 244, 0.12);
  --color-text: #f2f4f8;
  --color-text-muted: #a7b0c0;
  --color-accent: #f0a202;
  --color-accent-hover: #ffb623;
  --color-accent-ink: #1a1200;
  --color-support: #5f7a5a;
  --color-danger: #ff6b6b;
  --color-success: #3ddc97;
  --font-display: "Syne", system-ui, sans-serif;
  --font-body: "Source Sans 3", system-ui, sans-serif;
  --text-hero: clamp(2.4rem, 6vw, 4.25rem);
  --text-h1: clamp(2rem, 4vw, 3rem);
  --text-h2: clamp(1.5rem, 3vw, 2rem);
  --text-h3: clamp(1.2rem, 2vw, 1.4rem);
  --text-lead: clamp(1.1rem, 2vw, 1.25rem);
  --text-body: 1.0625rem;
  --text-small: 0.875rem;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.5rem;
  --space-6: 2rem;
  --space-7: 3rem;
  --space-8: 4rem;
  --space-9: 6rem;
  --radius-sm: 0.375rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --shadow-soft: 0 12px 40px rgba(0, 0, 0, 0.35);
  --content-max: 72rem;
  --header-h: 4.25rem;
  --focus-ring: 0 0 0 3px var(--color-bg), 0 0 0 6px var(--color-accent);
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
  --dur: 180ms;
  --z-header: 100;
  --z-nav: 110;
  --z-lightbox: 200;
}
```

- [ ] **Step 2: Write `css/base.css`**

Include: box-sizing reset; `html { scroll-behavior: smooth; }` gated later by reduced-motion; `body` bg/text/font; heading font-display weights; `img { max-width:100%; height:auto; display:block; }`; link colors using accent; `:focus-visible { outline: none; box-shadow: var(--focus-ring); }`; `.visually-hidden`; `.container { width:min(100% - 2rem, var(--content-max)); margin-inline:auto; }`; selection color; `prefers-reduced-motion: reduce` disabling smooth scroll and transitions globally via `*, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }`.

- [ ] **Step 3: Write `assets/favicon.svg`**

Simple dark rounded square + amber “MD” monogram, 32 viewBox.

- [ ] **Step 4: Write `assets/images/README.md`**

Checklist of real assets to replace placeholders later: logo, hero outdoor/work-dog, Chris portrait, 8 gallery photos, shop category thumbs, Reico pack shot, merch flat-lay.

- [ ] **Step 5: Verify files exist**

Run:

```bash
test -f css/tokens.css && test -f css/base.css && test -f assets/favicon.svg && test -f assets/images/README.md && echo OK
```

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add grok45/css/tokens.css grok45/css/base.css grok45/assets/favicon.svg grok45/assets/images/README.md
git commit -m "feat(grok45): design tokens, base styles, favicon"
```

---

### Task 2: Layout CSS + components CSS foundation

**Files:**
- Create: `grok45/css/layout.css`
- Create: `grok45/css/components.css`

**Interfaces:**
- Consumes: tokens from Task 1
- Produces: classes `.site-header`, `.site-nav`, `.site-footer`, `.btn`, `.card`, `.badge`, `.section`, `.hero`, `.form`, `.price-table`, `.lightbox`, `.media-ph` (placeholder media block)

- [ ] **Step 1: Implement `layout.css`**

Must cover:

1. `.skip-link` — visually hidden until focus, fixed top-left
2. `.site-header` — sticky, blur optional subtle, border-bottom, height `var(--header-h)`
3. `.site-header__inner` — flex, space-between, align center
4. `.logo` — flex gap, mark in accent box
5. `.nav-toggle` — visible only `<768px`, 48×48 min
6. `.site-nav` — desktop horizontal; mobile off-canvas/fullscreen panel when `body.nav-open`
7. `.sub-menu` — desktop dropdown; mobile nested list
8. `.section` / `.section--tight` padding
9. `.grid-2` / `.grid-3` responsive
10. `.site-footer` dark surface, multi-column collapsing to 1
11. `.page-hero` inner page header band
12. `body.nav-open { overflow: hidden; }`

Mobile-first: default mobile styles, then `@media (min-width: 768px)` and `@media (min-width: 1024px)`.

- [ ] **Step 2: Implement `components.css`**

Must cover:

```css
.btn { /* inline-flex, min-height 48px, padding, radius-sm, font-weight 700, no underline */ }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-accent-hover); }
.btn--secondary { border: 1px solid var(--color-text); color: var(--color-text); background: transparent; }
.btn--ghost { background: transparent; color: var(--color-accent); }
.card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-5); }
.badge { display:inline-flex; padding: 0.2rem 0.55rem; border-radius: 999px; background: var(--color-surface-2); color: var(--color-text-muted); font-size: var(--text-small); }
.badge--accent { background: color-mix(in srgb, var(--color-accent) 20%, transparent); color: var(--color-accent); }
.media-ph { /* aspect-ratio 16/10; gradient surface + diagonal texture; optional label via ::after attr */ aspect-ratio: 16 / 10; border-radius: var(--radius-md); background:
  linear-gradient(135deg, #1b2130 0%, #0f141c 50%, #243044 100%); border: 1px solid var(--color-border); position: relative; overflow: hidden; }
.media-ph--square { aspect-ratio: 1; }
.media-ph--portrait { aspect-ratio: 3 / 4; }
.lead { font-size: var(--text-lead); color: var(--color-text-muted); max-width: 40rem; }
.cta-band { background: var(--color-surface); border-block: 1px solid var(--color-border); padding: var(--space-7) 0; }
.price-table { width: 100%; border-collapse: collapse; }
.price-table th, .price-table td { padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-border); text-align: left; }
.form-field { display: grid; gap: var(--space-2); margin-bottom: var(--space-4); }
.form-field input, .form-field textarea { width: 100%; min-height: 48px; padding: 0.75rem 1rem; border-radius: var(--radius-sm); border: 1px solid var(--color-border); background: var(--color-surface-2); color: var(--color-text); font: inherit; }
.form-field textarea { min-height: 9rem; resize: vertical; }
.form-field .error { color: var(--color-danger); font-size: var(--text-small); }
.form-field.is-invalid input, .form-field.is-invalid textarea { border-color: var(--color-danger); }
.form-success { border: 1px solid color-mix(in srgb, var(--color-success) 40%, transparent); background: color-mix(in srgb, var(--color-success) 12%, transparent); padding: var(--space-5); border-radius: var(--radius-md); }
.lightbox { /* fixed inset dialog shell; hidden by default */ }
.lightbox[open], .lightbox.is-open { /* show flex center */ }
.quote-card blockquote { font-size: var(--text-lead); }
.chip-row { display: flex; flex-wrap: wrap; gap: var(--space-2); }
```

Also style `details.acc` for Über-uns progressive disclosure.

- [ ] **Step 3: Smoke-check CSS parses**

Run:

```bash
# no build tool — syntax sanity: files non-empty
wc -c css/layout.css css/components.css
```

Expected: both files > 1500 bytes.

- [ ] **Step 4: Commit**

```bash
git add grok45/css/layout.css grok45/css/components.css
git commit -m "feat(grok45): layout and component styles"
```

---

### Task 3: `main.js` navigation behavior

**Files:**
- Create: `grok45/js/main.js`

**Interfaces:**
- Consumes: DOM hooks `data-header`, `data-nav-toggle`, `data-nav`, `data-sub-toggle`, `data-sub-menu`, `data-year`
- Produces: `initMain()` side effects on DOMContentLoaded

- [ ] **Step 1: Write `js/main.js` with full behavior**

```js
(function () {
  const body = document.body;
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  const header = document.querySelector("[data-header]");
  const yearEls = document.querySelectorAll("[data-year]");
  yearEls.forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });

  if (!toggle || !nav) return;

  const focusableSelector =
    'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

  let lastFocus = null;

  function getFocusable() {
    return Array.from(nav.querySelectorAll(focusableSelector)).filter(
      (el) => !el.hasAttribute("disabled") && el.offsetParent !== null
    );
  }

  function openNav() {
    lastFocus = document.activeElement;
    body.classList.add("nav-open");
    toggle.setAttribute("aria-expanded", "true");
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = "Menü schließen";
    const items = getFocusable();
    if (items[0]) items[0].focus();
  }

  function closeNav() {
    body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = "Menü öffnen";
    // close submenus
    nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
      btn.setAttribute("aria-expanded", "false");
      const id = btn.getAttribute("aria-controls");
      const panel = id ? document.getElementById(id) : null;
      if (panel) panel.hidden = true;
    });
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  function isOpen() {
    return body.classList.contains("nav-open");
  }

  toggle.addEventListener("click", () => {
    if (isOpen()) closeNav();
    else openNav();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isOpen()) {
      e.preventDefault();
      closeNav();
      return;
    }
    if (e.key !== "Tab" || !isOpen()) return;
    const items = getFocusable();
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  // submenu toggles
  nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const expanded = btn.getAttribute("aria-expanded") === "true";
      const id = btn.getAttribute("aria-controls");
      const panel = id ? document.getElementById(id) : null;
      // close siblings
      nav.querySelectorAll("[data-sub-toggle]").forEach((other) => {
        if (other === btn) return;
        other.setAttribute("aria-expanded", "false");
        const oid = other.getAttribute("aria-controls");
        const op = oid ? document.getElementById(oid) : null;
        if (op) op.hidden = true;
      });
      btn.setAttribute("aria-expanded", expanded ? "false" : "true");
      if (panel) panel.hidden = expanded;
    });
  });

  // close mobile nav on internal link click
  nav.querySelectorAll('a[href]').forEach((link) => {
    link.addEventListener("click", () => {
      if (isOpen()) closeNav();
    });
  });

  // active nav: mark aria-current by pathname filename
  const file = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  nav.querySelectorAll("a[href]").forEach((a) => {
    const href = (a.getAttribute("href") || "").toLowerCase();
    if (href === file || (file === "" && href === "index.html")) {
      a.setAttribute("aria-current", "page");
    }
  });

  // desktop: close submenus on outside click
  document.addEventListener("click", (e) => {
    if (!header || header.contains(e.target)) return;
    nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
      btn.setAttribute("aria-expanded", "false");
      const id = btn.getAttribute("aria-controls");
      const panel = id ? document.getElementById(id) : null;
      if (panel) panel.hidden = true;
    });
  });
})();
```

- [ ] **Step 2: Create minimal `playground-nav.html` temporary OR jump to Task 4 homepage**

Prefer Task 4 immediately; verify nav there.

- [ ] **Step 3: Commit**

```bash
git add grok45/js/main.js
git commit -m "feat(grok45): accessible mobile nav and submenu JS"
```

---

### Task 4: Homepage `index.html`

**Files:**
- Create: `grok45/index.html`

**Interfaces:**
- Consumes: shared head/header/footer; CSS from Tasks 1–2; `main.js`

- [ ] **Step 1: Build complete homepage**

Structure inside `<main id="main">`:

1. **Hero** (`.hero`): eyebrow “Niederkassel & Umgebung”; `h1` e.g. “Klare Führung. Echte Auslastung. Starke Hunde.”; lead about Mad Dogs (Dogwalker, Trail, Ausrüstung); dual CTAs: `Dogwalker & Services` → `#services` or `dogwalker.html`, `Zum Shop` → `shop.html`; `.media-ph` decorative panel with caption “Foto: Trail / Arbeitshund ersetzen”
2. **Services** (`#services`): `h2` + 4 cards (Dogwalker, Trail, Spürhunde, Sporthunde) with real one-sentence value + links
3. **Shop teaser**: `h2` + short copy + grid of 3–6 category chips linking to `shop.html` anchors or external URLs + CTA “Alle Kategorien”
4. **Trust**: short Chris blurb + link `ueber-uns.html` + badge chips (THS, Trail Trainer, Diensthund)
5. **Stimmen teaser**: 1–2 quote cards + link `stimmen.html`
6. **CTA band**: WhatsApp + Kontakt buttons

Title: `Mad Dogs Germany | Dogwalker, Trail & Ausrüstung`  
Description: one German sentence with location.

- [ ] **Step 2: Visual/manual check**

Run:

```bash
cd grok45 && python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/` at 375px and 1280px width.

Verify:

- Dual CTAs visible without scroll on mobile (or hero CTAs immediately reachable)
- Nav opens/closes, Escape works
- No horizontal overflow

- [ ] **Step 3: Commit**

```bash
git add grok45/index.html
git commit -m "feat(grok45): outdoor-athletic homepage with dual CTAs"
```

---

### Task 5: Service pages (Dogwalker, Trail, Spürhunde, Sporthunde)

**Files:**
- Create: `grok45/dogwalker.html`
- Create: `grok45/trail.html`
- Create: `grok45/spuerhunde.html`
- Create: `grok45/sporthunde.html`

**Interfaces:**
- Shared page shell pattern: `page-hero` + content sections + `cta-band`

- [ ] **Step 1: `dogwalker.html`**

Content requirements (German, modernized from live):

- H1: professioneller Gassi-Service / strukturierte Auslastung
- For-whom list (energy, pulling, reactivity, need for rules)
- What dog gets (calm leadership, body+mind, groups up to 10, social training)
- Credibility bullets (16 years sport, HuTa Köln, Diensthund, trainer path)
- Pricing table exact: 1 Stunde 20 € · 1,5 Stunden 25 € · 2 Stunden 30 €
- Primary buttons: WhatsApp + `tel:+491733649143`
- Secondary: `kontakt.html`, `galerie.html`
- Location: Niederkassel und Umgebung
- Note: Kontakt bevorzugt per WhatsApp oder Anruf

- [ ] **Step 2: `trail.html`**

- No lorem
- Explain Man Trail / Pet Trail: nosework following human scent track
- Benefits: mental fatigue, bond, suitable energetic dogs
- Trainer: Pet Trailer Österreich Ausbildung (Chris)
- CTA Kontakt/Anfrage
- Optional media placeholder trail photo

- [ ] **Step 3: `spuerhunde.html` and `sporthunde.html`**

- Distinct H1 and angles (scent work vs sport/THS)
- Tie to brand experience without inventing titles not on live site
- Cross-links: trail, dogwalker, ueber-uns, kontakt
- Shared card layout

- [ ] **Step 4: Manual link check among the four**

```bash
grep -oE 'href="[^"]+"' dogwalker.html trail.html spuerhunde.html sporthunde.html | sort -u
```

Confirm internal hrefs point to existing planned filenames.

- [ ] **Step 5: Commit**

```bash
git add grok45/dogwalker.html grok45/trail.html grok45/spuerhunde.html grok45/sporthunde.html
git commit -m "feat(grok45): service pages dogwalker trail scent sport"
```

---

### Task 6: Shop hub, Reico, Bekleidung

**Files:**
- Create: `grok45/shop.html`
- Create: `grok45/reico.html`
- Create: `grok45/bekleidung.html`

- [ ] **Step 1: `shop.html`**

- H1 Shop-Übersicht
- Intro: selected gear (Halsbänder, Leinen, Non-Stop, Trail, …)
- Grid of category **cards**; each card:
  - title
  - short line
  - link with visible “Externer Shop” badge
  - `target="_blank" rel="noopener noreferrer"`
  - accessible name includes “(öffnet externen Shop)”
- Use exact category URLs from File map table
- Extra CTA to shop root URL

- [ ] **Step 2: `reico.html`**

- Partner page for Reico Hundefutter
- Trust/quality framing; **no medical cure claims**
- CTA: Kontakt for advice and/or link to shop if food sold there; if unknown, Kontakt + note

- [ ] **Step 3: `bekleidung.html`**

- Merch story Mad Dogs Germany
- Primary CTA button to `https://mad-dogs-germany.myspreadshop.de/` external
- Secondary back to shop.html

- [ ] **Step 4: Verify external URLs**

```bash
grep -E 'myspreadshop|mad-dogs-shop-' shop.html reico.html bekleidung.html
```

Expected: correct host paths, no broken “div-id-myshop” slugs.

- [ ] **Step 5: Commit**

```bash
git add grok45/shop.html grok45/reico.html grok45/bekleidung.html
git commit -m "feat(grok45): shop hub, reico, merch pages"
```

---

### Task 7: Brand pages — Über uns + Stimmen

**Files:**
- Create: `grok45/ueber-uns.html`
- Create: `grok45/stimmen.html`

- [ ] **Step 1: `ueber-uns.html`**

- H1 Über uns / Chris
- Narrative intro (sport since 2014, trail trainer, dogwalker, service dog handler — from live)
- Milestone chips: Vieze Meister 2017 Gl 2000; Ehrenpreise Metzingen; SWHV podiums 2018; Pet Trailer AT; Kynologisch trainer path; Schutzdiensthelfer; Angst/Problemhunde knowledge
- `<details class="acc">` for long seminar/webinar list (subset from live is enough if full list huge — include representative + “u. a.” honesty)
- CTA Kontakt

- [ ] **Step 2: `stimmen.html`**

- H1 Kundenstimmen
- If live site lacks extractable quotes in crawl: 3 clearly labeled sample quotes with note `Beispielzitat — durch echte Stimme ersetzen` in small text
- If real quotes found during implementation fetch, prefer real
- CTA Dogwalker + Kontakt

- [ ] **Step 3: Commit**

```bash
git add grok45/ueber-uns.html grok45/stimmen.html
git commit -m "feat(grok45): about and testimonials pages"
```

---

### Task 8: Kontakt page + `form.js`

**Files:**
- Create: `grok45/kontakt.html`
- Create: `grok45/js/form.js`

**Interfaces:**
- Produces: form `#contact-form` validation API (inline IIFE)
- Fields: `name`, `email`, `message`, `consent` (checkbox)

- [ ] **Step 1: Write `form.js`**

```js
(function () {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const success = document.getElementById("form-success");
  const live = document.getElementById("form-live");

  function setError(fieldName, message) {
    const field = form.querySelector(`[data-field="${fieldName}"]`);
    if (!field) return;
    const input = field.querySelector("input, textarea");
    const err = field.querySelector(".error");
    field.classList.toggle("is-invalid", Boolean(message));
    if (err) err.textContent = message || "";
    if (input) {
      if (message) input.setAttribute("aria-invalid", "true");
      else input.removeAttribute("aria-invalid");
    }
  }

  function validateEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  form.setAttribute("novalidate", "");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let ok = true;
    const name = form.elements.namedItem("name");
    const email = form.elements.namedItem("email");
    const message = form.elements.namedItem("message");
    const consent = form.elements.namedItem("consent");

    setError("name", "");
    setError("email", "");
    setError("message", "");
    setError("consent", "");

    if (!name || !String(name.value).trim()) {
      setError("name", "Bitte Namen angeben.");
      ok = false;
    }
    if (!email || !String(email.value).trim()) {
      setError("email", "Bitte E-Mail angeben.");
      ok = false;
    } else if (!validateEmail(String(email.value).trim())) {
      setError("email", "Bitte eine gültige E-Mail-Adresse eingeben.");
      ok = false;
    }
    if (!message || !String(message.value).trim()) {
      setError("message", "Bitte eine Nachricht schreiben.");
      ok = false;
    }
    if (!consent || !consent.checked) {
      setError("consent", "Bitte Einwilligung zur Kontaktaufnahme bestätigen.");
      ok = false;
    }

    if (!ok) {
      if (live) live.textContent = "Bitte prüfe die markierten Felder.";
      const firstInvalid = form.querySelector(".is-invalid input, .is-invalid textarea, .is-invalid input[type=checkbox]");
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    form.hidden = true;
    if (success) {
      success.hidden = false;
      success.focus();
    }
    if (live) live.textContent = "Nachricht wurde erfolgreich vorbereitet (Demo — kein Versand).";
  });
})();
```

- [ ] **Step 2: Build `kontakt.html`**

- Direct channels cards first (phone, WhatsApp, mail, Instagram)
- Form with labels, `*` required, consent text matching live intent (storage for contact, withdraw anytime)
- `#form-live` aria-live="polite"
- `#form-success` tabindex="-1" hidden until success
- Scripts: `main.js` + `form.js` defer

- [ ] **Step 3: Manual test cases**

1. Submit empty → errors on all required  
2. Bad email → email error  
3. Valid → form hides, success shows  

- [ ] **Step 4: Commit**

```bash
git add grok45/kontakt.html grok45/js/form.js
git commit -m "feat(grok45): contact page with client-side validation"
```

---

### Task 9: Galerie + `gallery.js`

**Files:**
- Create: `grok45/galerie.html`
- Create: `grok45/js/gallery.js`
- Create: `grok45/assets/images/placeholders/gallery-1.svg` … `gallery-8.svg` (simple unique SVG scenes) OR pure CSS `.media-ph` buttons without files

**Preferred:** 8 inline SVG files or one sprite — keep lightweight.

- [ ] **Step 1: Write `gallery.js`**

Behavior:

- Grid buttons/links `data-gallery-item` with `data-full` src and `data-alt`
- Open dialog `#lightbox` with `role="dialog" aria-modal="true" aria-labelledby="lightbox-title"`
- Focus close button on open; trap Tab; Esc closes; restore focus
- Prev/next buttons cycle items
- Update image `src`/`alt` and title

```js
(function () {
  const items = Array.from(document.querySelectorAll("[data-gallery-item]"));
  const lb = document.getElementById("lightbox");
  if (!items.length || !lb) return;

  const img = lb.querySelector("[data-lightbox-img]");
  const title = lb.querySelector("#lightbox-title");
  const btnClose = lb.querySelector("[data-lightbox-close]");
  const btnPrev = lb.querySelector("[data-lightbox-prev]");
  const btnNext = lb.querySelector("[data-lightbox-next]");
  let index = 0;
  let lastFocus = null;

  function show(i) {
    index = (i + items.length) % items.length;
    const el = items[index];
    const src = el.getAttribute("data-full");
    const alt = el.getAttribute("data-alt") || "";
    if (img) {
      img.src = src;
      img.alt = alt;
    }
    if (title) title.textContent = alt || "Galeriebild";
  }

  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    lb.hidden = false;
    lb.classList.add("is-open");
    document.body.classList.add("nav-open"); // reuse scroll lock carefully OR use lightbox-open class
    document.body.classList.add("lightbox-open");
    document.body.classList.remove("nav-open");
    if (btnClose) btnClose.focus();
  }

  function close() {
    lb.hidden = true;
    lb.classList.remove("is-open");
    document.body.classList.remove("lightbox-open");
    if (lastFocus) lastFocus.focus();
  }

  items.forEach((el, i) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      open(i);
    });
  });
  btnClose && btnClose.addEventListener("click", close);
  btnPrev && btnPrev.addEventListener("click", () => show(index - 1));
  btnNext && btnNext.addEventListener("click", () => show(index + 1));
  document.addEventListener("keydown", (e) => {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") show(index - 1);
    if (e.key === "ArrowRight") show(index + 1);
  });
})();
```

Add `body.lightbox-open { overflow: hidden; }` to `layout.css` if not present (modify Task 2 file).

- [ ] **Step 2: Build `galerie.html`**

- H1 Galerie
- Intro dogwalker/context
- Responsive grid 2 col mobile / 4 desktop
- Each item button with placeholder visual
- Lightbox markup at end of main
- Links to dogwalker + kontakt
- `gallery.js` + `main.js`

- [ ] **Step 3: Manual test**

Open lightbox, Tab cycles controls, Esc closes, arrows change image.

- [ ] **Step 4: Commit**

```bash
git add grok45/galerie.html grok45/js/gallery.js grok45/css/layout.css grok45/assets/images/placeholders/
git commit -m "feat(grok45): gallery page with accessible lightbox"
```

---

### Task 10: Legal pages

**Files:**
- Create: `grok45/impressum.html`
- Create: `grok45/agb.html`
- Create: `grok45/datenschutz.html`

- [ ] **Step 1: `impressum.html`**

German Impressum structure:

- Verantwortlicher / Anbieter (use Mad Dogs Germany + public contact channels)
- Kontakt phone/email
- Do **not** invent HRB, VAT ID, or street if unknown — use clearly marked placeholders:

```html
<p><strong>Anschrift:</strong> <span class="legal-todo">[Straße/PLZ Ort — vom Betreiber ergänzen]</span></p>
```

- [ ] **Step 2: `agb.html`**

Structured sections for Dogwalker service terms in plain German prototype language (scope, booking, cancellation outline, liability high-level). Mark as prototype summary if not copying full legal from live PDF/HTML.

- [ ] **Step 3: `datenschutz.html`**

Sections: Verantwortlicher, Zwecke (Kontaktformular Demo — no server storage in prototype), host, Rechte der Betroffenen, contact. State clearly form does not transmit in this prototype.

- [ ] **Step 4: Ensure footer links on a sample page resolve**

```bash
for f in impressum agb datenschutz; do test -f "$f.html" && echo "$f OK"; done
```

- [ ] **Step 5: Commit**

```bash
git add grok45/impressum.html grok45/agb.html grok45/datenschutz.html
git commit -m "feat(grok45): impressum agb datenschutz pages"
```

---

### Task 11: Consistency pass, link verifier, final QA

**Files:**
- Create: `grok45/scripts/verify-links.mjs` (optional Node)
- Modify: any HTML/CSS/JS with fixes only inside `grok45/`

- [ ] **Step 1: Add `scripts/verify-links.mjs`**

```js
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const htmlFiles = fs.readdirSync(root).filter((f) => f.endsWith(".html"));
const hrefRe = /href\s*=\s*"([^"]+)"/gi;
let failed = 0;

for (const file of htmlFiles) {
  const src = fs.readFileSync(path.join(root, file), "utf8");
  let m;
  while ((m = hrefRe.exec(src))) {
    const href = m[1];
    if (
      href.startsWith("http") ||
      href.startsWith("mailto:") ||
      href.startsWith("tel:") ||
      href.startsWith("#") ||
      href.startsWith("data:")
    ) {
      continue;
    }
    const clean = href.split("#")[0].split("?")[0];
    if (!clean) continue;
    const target = path.join(root, clean);
    if (!fs.existsSync(target)) {
      console.error(`MISSING from ${file}: ${href}`);
      failed++;
    }
  }
}

if (failed) {
  console.error(`Failed: ${failed}`);
  process.exit(1);
}
console.log(`OK: checked ${htmlFiles.length} HTML files`);
```

Note: On macOS, `new URL(import.meta.url).pathname` may need `fileURLToPath` — use:

```js
import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
```

- [ ] **Step 2: Run verifier**

```bash
node scripts/verify-links.mjs
```

Expected: `OK: checked 15 HTML files`

- [ ] **Step 3: Manual QA checklist (from spec)**

- [ ] All internal links resolve  
- [ ] Mobile nav keyboard + Escape  
- [ ] Homepage dual CTAs clear at 375px  
- [ ] Contact validation states  
- [ ] Gallery lightbox focus/Esc/arrows  
- [ ] External shop + Spreadshop URLs correct  
- [ ] `prefers-reduced-motion` does not break layout  
- [ ] Legal in footer every page  
- [ ] No files changed outside `grok45/`  

Run:

```bash
git status --short | grep -v '^?? grok45' | grep -v 'grok45/' || true
```

Ensure you only stage grok45 paths for commits.

- [ ] **Step 4: Polish pass (anti-slop)**

- Tighten any generic filler copy  
- Ensure accent used sparingly  
- Check heading hierarchy one `h1`  
- Align button styles  

- [ ] **Step 5: Final commit**

```bash
git add grok45/
git commit -m "feat(grok45): final QA link check and polish"
```

---

## Spec coverage self-check

| Spec area | Task |
|-----------|------|
| Dual-hub IA + nav groups | 3, 4, header snippet |
| All 15 pages | 4–10 |
| Outdoor athletic tokens | 1 |
| Components/a11y | 2, 3, 8, 9 |
| Dogwalker prices/location | 5 |
| Trail without lorem | 5 |
| Shop categories external | 6 |
| Spreadshop URL | 6 |
| Über uns progressive disclosure | 7 |
| Stimmen | 7 |
| Contact form demo | 8 |
| Galerie lightbox | 9 |
| Legal | 10 |
| Verify only grok45 | 11 + global constraints |
| main/form/gallery JS split | 3, 8, 9 |

## Placeholder scan

No TBD implementation steps remain; legal address uses explicit `[…]` owner placeholders by design.

---

## Execution handoff

Plan complete and saved to `grok45/docs/superpowers/plans/2026-07-28-mad-dogs-redesign.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — execute tasks in this session with checkpoints  

Which approach?
