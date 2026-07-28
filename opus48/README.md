# Mad Dogs Germany – Website-Redesign

Modernes, barrierefreies und mobile-first Redesign von **mad-dogs-germany.de** –
Dogwalking, Training & Ausrüstung aus Niederkassel bei Köln.

Statische Website ohne Build-Schritt: reines **HTML5, CSS und Vanilla-JavaScript**.
Keine Frameworks, keine externen Tracker, selbst gehostete Schriften.

---

## Schnellstart / Vorschau

Da es eine statische Seite ist, genügt ein beliebiger Webserver. Beispiele:

```powershell
# Variante A: Python
python -m http.server 8080

# Variante B: Node (falls installiert)
npx serve .
```

Danach im Browser `http://localhost:8080` öffnen.
Ein direkter Doppelklick auf `index.html` funktioniert ebenfalls, ein lokaler
Server ist aber näher an der späteren Produktivumgebung.

---

## Seitenstruktur

| Datei              | Inhalt                                                        |
|--------------------|---------------------------------------------------------------|
| `index.html`       | Startseite: Hero, Leistungen, Ablauf, Stimmen, CTA            |
| `dogwalker.html`   | Dogwalker-Service: Nutzen, Ablauf, **Preise**, Galerie        |
| `training.html`    | Training: **Man/Pet Trail**, Spürhunde, Sporthunde            |
| `shop.html`        | Shop-Hub: Kategorien, Reico-Futter, Bekleidung                |
| `ueber-uns.html`   | Über Chris: Qualifikationen & Turniererfolge                  |
| `kontakt.html`     | Kontaktformular, Kontaktdaten, OpenStreetMap-Karte            |
| `impressum.html`   | Impressum (Vorlage – **bitte prüfen**)                        |
| `datenschutz.html` | Datenschutzerklärung (Vorlage – **bitte prüfen**)             |
| `404.html`         | Fehlerseite                                                   |

```
opus48/
├─ *.html
├─ css/
│  ├─ styles.css        # Designsystem (Tokens, Komponenten, Utilities)
│  └─ fonts.css         # @font-face für selbst gehostete Schriften
├─ js/
│  └─ main.js           # Nav, Reveal, Lightbox, Formular (Progressive Enhancement)
├─ assets/
│  ├─ img/              # optimierte Fotos, Logo, Icons, OG-Image
│  └─ fonts/            # Inter & Space Grotesk (woff2, latin)
├─ favicon.svg · site.webmanifest · robots.txt · sitemap.xml
```

---

## Umgesetzte Best Practices

**Barrierefreiheit (WCAG 2.1 AA)**
- Semantisches HTML, Landmarks, sinnvolle Überschriften-Hierarchie
- „Zum Inhalt springen“-Link, sichtbare `:focus-visible`-Stile
- Mobile-Navigation mit `aria-expanded`, Fokus-Falle, Escape & Backdrop
- Formular mit Labels, `aria-describedby`, Live-Fehlermeldungen, Pflichtfeld-Logik
- Alt-Texte für Fotos, dekorative Grafiken via `aria-hidden`
- Farbkontraste ≥ 4,5:1, Touch-Ziele ≥ 44 px
- `prefers-reduced-motion` wird respektiert

**Mobile-first & modern**
- Durchgängig mobile-first, mit `min-width`-Breakpoints hochskaliert
- Fluid Typography & Spacing via `clamp()`
- CSS Custom Properties als Design-Tokens, CSS Grid & Flexbox
- Sticky-Header, Reveal-on-Scroll, `<dialog>`-Lightbox

**Performance**
- Bilder verkleinert & komprimiert (z. B. Hero von 5 MB → ~330 KB)
- `loading="lazy"`, `decoding="async"`, `width`/`height` gegen Layout-Shift
- LCP-Bild mit `fetchpriority="high"` vorgeladen, Fonts via `preload`
- Kein Framework, kein Render-Blocking-JS (`defer`)

**SEO**
- Individuelle `<title>` & Meta-Descriptions, Canonicals
- Open-Graph-/Twitter-Tags inkl. generiertem OG-Image
- JSON-LD (`LocalBusiness`, `Service`, `ContactPage`)
- `sitemap.xml`, `robots.txt`, sprechende Dateinamen

**Datenschutz**
- Selbst gehostete Schriften (kein Google-Fonts-CDN)
- Keine Tracking-/Marketing-Cookies, kein Analytics
- Datensparsame OpenStreetMap-Einbettung statt Google Maps

---

## Vor dem Livegang zu erledigen

- [ ] **Impressum & Datenschutz prüfen/vervollständigen** (vollständiger Name,
      ggf. USt-IdNr., Hoster konkret benennen). Die Texte sind Vorlagen und
      ersetzen keine Rechtsberatung.
- [ ] **Kontaktformular anbinden:** In `kontakt.html` das Attribut
      `data-endpoint` mit einer echten Formular-URL (z. B. Formspree, Netlify
      Forms oder das Formular des Hosters) belegen. Ohne Endpoint öffnet das
      Formular als Fallback das E-Mail-Programm (`mailto:`).
- [ ] **Kundenstimmen ersetzen:** Auf der Startseite sind die Testimonials als
      Platzhalter gekennzeichnet (`<!-- PLATZHALTER ... -->`). Durch echte,
      freigegebene Bewertungen austauschen.
- [ ] **Fotos/Reihenfolge** nach Wunsch anpassen (Ordner `assets/img/`).
- [ ] **Domains/URLs** der Canonicals prüfen, falls ohne `.html` ausgeliefert wird.
- [ ] Optional: echte Öffnungszeiten/Geo-Koordinaten ins JSON-LD ergänzen.

---

## Inhaltliche Korrekturen gegenüber der alten Seite

- Lorem-Ipsum-Platzhalter (Man/Pet Trail, „Das sagen unsere Kunden“) durch
  echte bzw. sinnvolle Inhalte ersetzt.
- Leere Seiten (Spürhunde, Sporthunde) mit Inhalt gefüllt und in **Training**
  gebündelt.
- Defekte/kryptische Navigationslinks („test“, „div-id-myshop…“) entfernt und
  durch eine klare, flache Navigation ersetzt.

---

## Browser-Unterstützung

Aktuelle Versionen von Chrome, Edge, Firefox und Safari (Desktop & Mobil).
Ohne JavaScript bleibt die Seite vollständig nutzbar (Progressive Enhancement).

## Bild- & Schriftlizenzen

- Fotos & Logo: © Mad Dogs Germany (aus dem bestehenden Auftritt übernommen).
- Schriften: **Inter** und **Space Grotesk**, SIL Open Font License 1.1.
