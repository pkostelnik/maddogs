# Mad Dogs Germany Relaunch — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ein vollständiger, barrierefreier, performanter Multi-Page-Prototyp der Mad-Dogs-Germany-Website.

**Architecture:** Vite Multi-Page-Build. HTML-Partials über ein eigenes Vite-Plugin (`<!--#include ...-->`). Ein zentrales CSS-Token-System mit `@layer`. Vanilla-JS-Module, progressiv verbessernd. Inhalte als JSON, per Build-Skript in HTML gerendert wo sinnvoll, sonst direkt im Markup.

**Tech Stack:** Vite 7, HTML, CSS (Layers, Grid, Container Queries, Custom Properties), Vanilla ES-Module, Playwright + axe-core für Accessibility-Tests, Lighthouse CI.

## Global Constraints

- Sprache aller Inhalte: Deutsch, `lang="de"`.
- Keine Third-Party-Requests zur Laufzeit. Fonts self-hosted.
- Kein UI-Framework, kein CSS-Framework.
- WCAG 2.2 AA verbindlich.
- JS gzip < 15 kB, CSS gzip < 30 kB.
- Farbtokens: Ink `#16181A`, Paper `#F5F3EF`, Moss `#2F3B2F`, Ember `#E4622A`, Bone `#C9C3B8`.
- Kontakt: `info@mad-dogs-germany.de`, `+49 173 3649143`, Niederkassel.
- Entwurfstexte tragen sichtbar das Badge „Entwurf".
- Nur innerhalb von `opus5/` arbeiten.

---

### Task 1: Projekt-Setup und Build-Pipeline

**Files:**
- Create: `package.json`, `vite.config.js`, `.gitignore`, `plugins/html-includes.js`

**Produces:** `npm run dev`, `npm run build`, `npm run preview`; Include-Plugin das `<!--#include file="partials/x.html" -->` auflöst.

- [ ] Vite 7 installieren, MPA-Input für alle 16 Seiten konfigurieren
- [ ] Include-Plugin schreiben (transformIndexHtml, rekursiv, mit HMR-Invalidierung)
- [ ] `npm run build` läuft fehlerfrei durch
- [ ] Commit

### Task 2: Assets beschaffen

**Files:**
- Create: `scripts/fetch-assets.mjs`, `src/assets/images/*`, `src/assets/fonts/*`

- [ ] Skript, das Logo, Hero- und Galeriebilder von der Live-Domain lädt
- [ ] Bilder zu WebP/AVIF konvertieren, mehrere Breiten (480/960/1600)
- [ ] Archivo + Inter als WOFF2 (Latin-Subset) ablegen
- [ ] Manifest `src/content/images.json` mit Pfaden, Maßen, Alt-Texten
- [ ] Commit

### Task 3: Design-System (CSS-Fundament)

**Files:**
- Create: `src/styles/main.css`, `tokens.css`, `reset.css`, `base.css`, `layout.css`

**Produces:** Tokens `--c-ink`, `--c-paper`, `--c-moss`, `--c-ember`, `--space-1..12`, `--step--2..8`; Grid-Utility `.wrap` mit `full/content/narrow`.

- [ ] `@layer reset, tokens, base, layout, components, utilities`
- [ ] Fluid Type Scale mit `clamp()`, Font-Face-Deklarationen
- [ ] Light/Dark über `color-scheme` und `[data-theme]`
- [ ] Focus-Ring, Skip-Link, `prefers-reduced-motion`-Guard
- [ ] Kontrastwerte nachrechnen und dokumentieren
- [ ] Commit

### Task 4: Komponenten-Bibliothek

**Files:**
- Create: `src/styles/components/*.css` (button, card, hero, section, stat, testimonial, faq, form, gallery, badge, breadcrumb, prose)

- [ ] Jede Komponente mit Container Queries statt Media Queries wo sinnvoll
- [ ] Touch-Targets ≥ 44 px verifizieren
- [ ] Commit

### Task 5: Header, Footer, Navigation

**Files:**
- Create: `src/partials/head.html`, `header.html`, `footer.html`, `cta.html`
- Create: `src/styles/components/nav.css`, `src/scripts/nav.js`, `src/scripts/theme.js`

- [ ] Skip-Link, Landmarks, Logo, 5-Punkte-Navigation mit Training-Dropdown
- [ ] Mobile-Menü: `aria-expanded`, Focus-Trap, Escape, Fokus-Rückgabe
- [ ] Theme-Toggle mit `localStorage` und FOUC-Guard im `<head>`
- [ ] Sticky-CTA nach Hero via `IntersectionObserver`
- [ ] Footer mit Kontakt, Social, Rechtslinks
- [ ] Commit

### Task 6: Inhalte als JSON

**Files:**
- Create: `src/content/site.json`, `services.json`, `shop.json`, `about.json`, `testimonials.json`, `faq.json`

- [ ] Echte Bestandsinhalte übernehmen (Preise, Vita, Kategorien)
- [ ] Entwurfstexte für Spürhunde, Sporthunde, Man/Pet Trail, Ernährung mit `"draft": true`
- [ ] Commit

### Task 7: Startseite

**Files:** `index.html`, `src/styles/pages/home.css`, `src/scripts/reveal.js`

- [ ] Hero mit Preload-LCP-Bild, Claim, Doppel-CTA
- [ ] Leistungskarten, Trust-Leiste, Dogwalking-Highlight, Shop-Teaser, Testimonials, Galerie-Streifen, Kontakt-CTA
- [ ] Scroll-Reveal mit Reduced-Motion-Guard
- [ ] Commit

### Task 8: Training-Hub und vier Service-Seiten

**Files:** `src/pages/training/{index,dogwalking,man-pet-trail,spuerhunde,sporthunde}.html`, `src/styles/pages/service.css`

- [ ] Gemeinsames Seitengerüst: Hero, Eignung, Leistungen, Ablauf, Preise, FAQ, CTA
- [ ] Dogwalking mit echten Preisen und WhatsApp-Link
- [ ] Entwurfs-Badges auf den drei neu getexteten Seiten
- [ ] Commit

### Task 9: Shop-Vitrine und Kategorieseite

**Files:** `src/pages/shop/{index,halsbaender}.html`, `src/styles/pages/shop.css`, `src/scripts/filter.js`

- [ ] Kategorie-Grid mit neun Kacheln
- [ ] Kategorieseite mit Produktkarten und Filter-Chips (Tastatur bedienbar, `aria-pressed`)
- [ ] Externe Kauf-Links mit `rel="noopener"` und Hinweis „öffnet externen Shop"
- [ ] Commit

### Task 10: Ernährung, Über uns, Kundenstimmen, Galerie

**Files:** `src/pages/{ernaehrung,ueber-uns,kundenstimmen,galerie}.html`, `src/scripts/lightbox.js`

- [ ] Über uns mit Vita-Timeline und Qualifikationen
- [ ] Galerie mit `<dialog>`-Lightbox, Pfeiltasten, Escape, Fokusverwaltung
- [ ] Commit

### Task 11: Kontakt und Rechtstexte

**Files:** `src/pages/{kontakt,impressum,datenschutz,agb}.html`, `src/scripts/form.js`

- [ ] Formular mit Labels, `aria-describedby`-Fehlern, `aria-live`-Status, ohne Versand
- [ ] Honeypot statt Captcha
- [ ] Rechtstexte als klar markierte Entwürfe
- [ ] Commit

### Task 12: SEO, PWA-Basics, Sitemap

**Files:** `public/robots.txt`, `public/sitemap.xml`, `public/site.webmanifest`, Favicons, JSON-LD in `head.html`

- [ ] Pro Seite Title, Description, Canonical, OG/Twitter
- [ ] `LocalBusiness`-JSON-LD
- [ ] Commit

### Task 13: Verifikation

**Files:** `tests/a11y.spec.js`, `lighthouserc.json`

- [ ] Playwright + axe-core über alle Seiten, null Violations
- [ ] Tastatur-Durchlauf: Menü, Dropdown, Lightbox, Filter, Formular
- [ ] Lighthouse CI ≥ 95 in allen vier Kategorien
- [ ] Bundle-Budget prüfen
- [ ] `README.md` mit Setup, Struktur, Entscheidungen, offenen Punkten
- [ ] Commit

## Self-Review

- Spec-Abdeckung: IA (T5,7–11), Content (T6), Design-System (T3,4), A11y (T3,4,5,10,11,13), Performance/SEO (T1,2,12,13). Vollständig.
- Keine Platzhalter, keine „siehe Task N"-Verweise.
- Namenskonsistenz der Tokens zwischen T3 und T4–T11 geprüft.
