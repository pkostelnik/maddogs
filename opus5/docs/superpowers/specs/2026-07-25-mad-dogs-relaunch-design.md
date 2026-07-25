# Mad Dogs Germany — Relaunch-Prototyp

Datum: 2026-07-25
Status: freigegeben

## Ziel

Ein vollständiger, produktionsnaher Prototyp der Website von mad-dogs-germany.de.
Kompletter Seitenumfang, mobile first, WCAG 2.2 AA, modernes Layout und Design.
Der Prototyp muss handgemacht wirken — keine generischen Template-Muster.

## Ausgangslage

Die bestehende Seite ist mit dem IONOS-Baukasten gebaut. Befunde der Analyse:

- Startseite besteht faktisch nur aus einer Überschrift und einem Kontaktformular.
- Navigation hat 10 Hauptpunkte, darunter eine Seite `test` und ein Menüpunkt,
  dessen URL-Slug rohes HTML/JS enthält.
- `/man-pet-trail/` enthält Lorem-Ipsum-Überschriften und ein Platzhalterbild.
- `/spuerhunde/` ist vollständig leer.
- Rechtliches liegt unter `/dogwalker-service/`.
- Zwei widersprüchliche Kontaktadressen: `info@mad-dogs-germany.de` im Header,
  `chris-mit-den-malis@gmx.de` im Footer.
- Instagram-Link im Footer zeigt auf `instagram.com` statt auf das Profil.
- Cookie-Banner für IONOS SiteAnalytics und Übersetzungsdienst.

## Entscheidungen

| Thema | Entscheidung |
| --- | --- |
| Umfang | Komplette Site, alle Seiten ausgearbeitet |
| Stack | Vite 7, Multi-Page, HTML/CSS/Vanilla-JS, kein UI-Framework |
| Inhalte | Echte Texte übernehmen, Originalbilder lokal einbinden |
| Lücken | Fachlich plausible Entwurfstexte, sichtbar als „Entwurf" markiert |
| Design | Rugged & Professional — dunkel, erdig, Signal-Orange |
| Shop | Statische Vitrine, Kaufaktionen verlinken extern |
| Navigation | Neustrukturierung auf 5 Hauptpunkte |

## Informationsarchitektur

```
/                          Startseite
/training/                 Hub Trainingsangebote
/training/dogwalking/      Gassi-Service
/training/man-pet-trail/   Nasenarbeit / Personensuche
/training/spuerhunde/      Spürhunde
/training/sporthunde/      Sporthunde / Turnierhundesport
/shop/                     Shop-Vitrine, 9 Kategorien
/shop/halsbaender/         Beispielhafte Kategorieseite
/ernaehrung/               Reico Hundefutter
/ueber-uns/                Chris, Vita, Qualifikationen
/kundenstimmen/            Testimonials
/galerie/                  Bildergalerie mit Lightbox
/kontakt/                  Formular, WhatsApp, Anfahrt
/impressum/                nur Footer
/datenschutz/              nur Footer
/agb/                      nur Footer
```

Hauptnavigation: Training · Shop · Ernährung · Über uns · Kontakt.
„Training" als Dropdown auf Desktop, aufklappbare Gruppe im Mobile-Menü.
Sticky-CTA „Proberunde vereinbaren" erscheint nach Verlassen des Heros.

Entfernt: `test`, kaputter Bekleidungs-Slug (wird Shop-Kategorie mit externem
Link zu Spreadshop), Rechtliches aus der Hauptnavigation.

## Content-Strategie

Alle Texte liegen als JSON unter `src/content/`, getrennt vom Markup.

Übernommen aus dem Bestand:
- Dogwalking: Zielgruppe, Leistungsversprechen, Preise 20 / 25 / 30 €,
  Gruppengröße bis 10 Hunde, Standort Niederkassel, Telefon 0173 3649143.
- Über uns: Hundesport seit 2014, 70+ Turnierstarts THS, Vizemeister DM
  GL 2000 (2017), 3. Platz SWHV CSC und GL 2000 (2018), Ehrenpreise der Stadt
  Metzingen 2017 und 2018, Schutzdiensthelfer, Pet-/Man-Trail-Trainer
  (9 Monate Ausbildung in Österreich), Diensthundeführer, Hundetrainer.
- Shop-Kategorien: Halsbänder, Leinen, European Pet Pharmacy, Non Stop Dogwear,
  Trail Zubehör, Mäntel/Jacken, Bücher, Kurse, Bekleidung.

Neu verfasst und als Entwurf markiert: Man/Pet Trail, Spürhunde, Sporthunde,
Ernährung, Kundenstimmen, Rechtstexte.

Kontaktdaten werden auf `info@mad-dogs-germany.de` vereinheitlicht, der
Instagram-Link auf `instagram.com/mad_dogs_germany/` korrigiert.

Bilder werden einmalig von der Live-Seite gezogen, nach `src/assets/images/`
gelegt und mit `srcset` responsiv ausgeliefert.

## Design-System

Farbtokens als CSS Custom Properties:

- Ink `#16181A`, Paper `#F5F3EF`, Moss `#2F3B2F`, Ember `#E4622A`,
  Bone `#C9C3B8`, plus Statusfarben für Formularvalidierung.
- Kontrast: Fließtext ≥ 4.5:1, große Headlines ≥ 3:1, UI-Komponenten ≥ 3:1.
- Light- und Dark-Theme über `color-scheme`, Umschalter mit `localStorage`,
  Default folgt `prefers-color-scheme`.

Typografie:
- Headlines Archivo (kondensiert), Fließtext Inter. Self-hosted WOFF2,
  Latin-Subset, `font-display: swap`, Preload der kritischen Schnitte.
- Fluid Type Scale über `clamp()`, Zeilenlänge 60–75 Zeichen.

Layout:
- CSS Grid mit benannten Spalten `full` / `content` / `narrow`.
- Spacing-Skala in 8-px-Schritten als Tokens.
- Container Queries für Karten.
- CSS Layers: `reset, tokens, base, layout, components, utilities`.

Motion:
- Scroll-Reveal über `IntersectionObserver`, Hover-Lift auf Karten,
  weiche Übergänge im Mobile-Menü.
- Vollständig deaktiviert unter `prefers-reduced-motion: reduce`.

## Seiten-Anatomie

Startseite: Hero (Vollbild, Claim „Gassi mit Köpfchen", Doppel-CTA) →
vier Leistungskarten → Trust-Leiste mit Kennzahlen → Dogwalking-Highlight mit
Preisen → Shop-Teaser → Testimonials → Galerie-Streifen → Kontakt-CTA.

Service-Seiten: Hero → „Für wen geeignet" → „Was dein Hund bekommt" →
Ablauf in Schritten → Preise → FAQ als `<details>` → CTA.

Shop: Kategorie-Grid mit Bildkacheln. Eine Kategorieseite (Halsbänder) ist mit
Produktkarten und Filter-Chips ausgebaut; Kauf-Buttons verlinken extern.

Kontakt: Formular mit Client-Validierung ohne echten Versand, WhatsApp-
Direktlink, Telefon, Einzugsgebiet.

## Accessibility (WCAG 2.2 AA)

- Skip-Link, semantische Landmarks, eine `<h1>` pro Seite, lückenlose Hierarchie.
- Sichtbarer 2-px-Focus-Ring mit Offset auf allen interaktiven Elementen.
- Mobile-Menü: `aria-expanded`, Focus-Trap, Escape schließt, Fokus kehrt zurück.
- Lightbox als natives `<dialog>` mit `showModal()`.
- Formular: `<label>` für jedes Feld, Fehler über `aria-describedby`,
  Statusmeldung in `aria-live="polite"`, kein Farbcode als einziger Indikator.
- Touch-Targets ≥ 44 × 44 px, `lang="de"`, aussagekräftige Alt-Texte.
- Zoom bis 200 % ohne horizontales Scrollen.

## Performance und SEO

- Lighthouse-Ziel ≥ 95 in allen vier Kategorien.
- LCP-Bild mit `fetchpriority="high"` und Preload; weitere Bilder lazy,
  jeweils mit `width` und `height` gegen Layout-Shift.
- JS-Budget unter 15 kB gzip, CSS unter 30 kB gzip.
- Keine Third-Party-Requests, dadurch entfällt das Cookie-Banner ersatzlos.
- Pro Seite eigene Meta-Description und Open-Graph-Tags, kanonische URLs,
  `LocalBusiness`-JSON-LD mit Standort Niederkassel, `sitemap.xml`, `robots.txt`.

## Projektstruktur

```
opus5/
  index.html
  src/
    pages/          weitere HTML-Seiten
    partials/       header, footer, cta, seo-head
    styles/         tokens, base, layout, components, pages
    scripts/        nav, theme, lightbox, form, reveal
    content/        JSON-Inhalte
    assets/         Bilder, Fonts, Icons
  public/           robots.txt, sitemap.xml, favicons
  vite.config.js
  docs/
```

## Nicht im Umfang

- Echter Warenkorb, Checkout, Zahlungsanbindung.
- Backend für den Formularversand.
- Mehrsprachigkeit.
- CMS-Anbindung.
