# Mad Dogs Germany — Relaunch-Prototyp

Ein vollständiger Prototyp für die Website von
[mad-dogs-germany.de](https://www.mad-dogs-germany.de). Sechzehn Seiten,
mobile first, WCAG 2.2 AA, ohne Framework.

## Was du bekommst: reines HTML, CSS, JavaScript

Der Ordner `dist/` ist das Produkt. Er enthält 16 HTML-Dateien, **eine**
CSS-Datei, **eine** JavaScript-Datei (8,1 kB) sowie Bilder und Schriften.
Kein `require`, kein `process.env`, kein Node-Konstrukt.

**Die Seite braucht kein Node zum Laufen.** Sie funktioniert auf jedem
Webspace, jedem Apache, jedem CDN — ebenso wie durch einfaches Doppelklicken
auf `dist/index.html`, ohne jeden Server. Alle Pfade sind relativ, deshalb
läuft der Ordner auch in einem Unterverzeichnis.

Node und Vite sind reine Werkzeuge zur **Erzeugung**, vergleichbar mit einem
Bildkonverter: nötig zum Herstellen, nicht zum Betreiben.

### Der Quelltext braucht dagegen einen Build

Die Dateien im Projektwurzelverzeichnis sind **nicht** direkt lauffähig. Sie
enthalten `<!--#include file="src/partials/header.html" -->` und Platzhalter
wie `{{site.contact.phone}}`. Das versteht kein Browser — erst `npm run build`
macht daraus fertiges HTML.

Der Grund ist Pflegbarkeit: Kopf, Navigation und Fußzeile existieren genau
einmal statt sechzehnmal. Eine Menüänderung ist ein Eingriff, nicht sechzehn.
Genau daran krankt die bestehende Baukastenseite.

Wer den Build nicht will, nimmt einfach `dist/` — dort ist alles bereits
aufgelöst und direkt bearbeitbar.

## Schnellstart

```bash
npm install
npm run dev         # Entwicklungsserver
npm run build       # Sitemap erzeugen und nach dist/ bauen
npm run preview     # gebaute Fassung auf Port 4321
npm run test:a11y   # axe-core, Struktur, Tastatur (Preview muss laufen)
npm run test:lh     # Lighthouse CI gegen dist/
```

## Ergebnisse

| Prüfung | Ergebnis |
| --- | --- |
| axe-core, 16 Seiten × helles und dunkles Theme | 0 Verstöße |
| Lighthouse, 11 Seiten × 3 Läufe, alle vier Kategorien | jeweils 100 |
| Cumulative Layout Shift | 0 auf allen Seiten |
| CSS | 9,3 kB gzip |
| JavaScript | 3,2 kB gzip |
| Läuft ohne Server (file://) | ja |
| Third-Party-Requests | keine |

## Was sich gegenüber der Bestandsseite ändert

**Navigation.** Aus zehn Hauptpunkten werden fünf: Training, Shop, Ernährung,
Über uns, Kontakt. Entfallen sind die Seite `test` und ein Menüpunkt, dessen
URL rohes HTML enthielt. Rechtliches wandert in den Footer.

**Startseite.** Bestand aus einer Überschrift und einem Kontaktformular.
Jetzt: Hero, Kennzahlen, Positionierung, vier Leistungen, Preise, Shop-Teaser,
Kundenstimmen, Galerie, Handlungsaufforderung.

**Inhaltliche Lücken.** `/man-pet-trail/` enthielt Lorem Ipsum, `/spuerhunde/`
war leer. Beide sind jetzt ausformuliert — durchgehend als Entwurf markiert.

**Konsistenz.** Eine Kontaktadresse statt zweier widersprüchlicher, der
Instagram-Link zeigt auf das Profil statt auf die Startseite von Instagram.

**Cookie-Banner.** Entfällt ersatzlos. Ohne Tracker, ohne externe Schriften
und ohne Übersetzungsdienst gibt es nichts einzuwilligen.

## Was echt ist und was nicht

Übernommen wurden alle belegbaren Inhalte: Dogwalking-Beschreibung und Preise
(20 / 25 / 30 €), Gruppengröße bis zehn Hunde, Standort Niederkassel,
Telefonnummer, Chris' Werdegang samt Turniererfolgen, die neun Shop-Kategorien
sowie sämtliche Bilder der Live-Seite.

Alles Übrige ist erfunden und **sichtbar als Entwurf gekennzeichnet** — über
`badge--draft` an einzelnen Elementen oder `draft-note` für ganze Abschnitte.
Das betrifft Man/Pet Trail, Spürhunde, Sporthunde, Teile der Ernährungsseite,
alle Kundenstimmen, die Produktdaten im Shop und die drei Rechtstexte.

Die Rechtstexte enthalten zusätzlich Platzhalter in eckigen Klammern und
stehen auf `noindex`. Sie ersetzen keine Rechtsberatung.

## Aufbau

```
index.html               Startseite
training/                Hub und vier Leistungsseiten
shop/                    Vitrine und eine ausgebaute Kategorie
ernaehrung/  ueber-uns/  kundenstimmen/  galerie/  kontakt/
impressum/   datenschutz/  agb/

src/
  partials/    head, header, footer, cta-band
  styles/      tokens, reset, base, layout, components/, pages/
  scripts/     nav, theme, reveal, lightbox, form, filter, focus-trap
  content/     images.json
  assets/      Bilder (AVIF/WebP/Fallback), Schriften
plugins/       html-includes.js
scripts/       Assets holen, Bilder aufbereiten, Schriften subsetten, Sitemap
tests/         a11y.mjs
docs/          Spezifikation, Umsetzungsplan, Konventionen
```

## Technische Entscheidungen

**Keine Frameworks.** Sechzehn weitgehend statische Seiten brauchen weder
React noch Tailwind. Ein eigenes Vite-Plugin löst
`<!--#include file="..." {"key":"wert"} -->` auf, damit Kopf, Navigation und
Footer nur einmal existieren.

**CSS-Layer.** `reset, tokens, base, layout, components, pages, utilities`
legen die Reihenfolge fest, unabhängig von der Import-Reihenfolge und der
Selektor-Spezifität. Kein `!important` außer im Reduced-Motion-Block.

**Farben aus dem echten Logo.** Das Markenblau `#103090` wurde aus der
Logodatei ausgezählt, nicht geschätzt. Jede Textfarbe ist gegen ihren
tatsächlich gerenderten Hintergrund gemessen — bei `color-mix` in oklab weicht
der reale Wert spürbar von einer sRGB-Rechnung ab.

**Zwei Themes.** Dunkel ist Standard, hell folgt `prefers-color-scheme`, die
manuelle Auswahl liegt in `localStorage`. Ein Inline-Skript im `<head>` setzt
das Theme vor dem ersten Paint. Hero, Seitenköpfe und das CTA-Band schalten
ihre Tokens fest auf Dark, weil sie immer auf dunklem Grund liegen.

**Bilder.** `scripts/fetch-assets.mjs` lädt die Originale einmalig,
`scripts/process-images.mjs` erzeugt AVIF und WebP in mehreren Breiten und
schreibt das Manifest. Das LCP-Bild wird vorgeladen, alle anderen sind lazy,
jedes trägt `width` und `height`. Ergebnis: CLS 0.

**Schriften.** Archivo und Inter liegen als variable Schnitte lokal und sind
auf die tatsächlich vorkommenden Zeichen subsettet — 88 → 54 kB und
47 → 33 kB. Archivo behält die Breitenachse, weil die kondensierten
Überschriften darauf beruhen.

**Inhalte als Daten.** Wiederkehrende Strukturen liegen in `src/content/`:
Kontaktdaten, Leistungen, Shop-Kategorien und -Produkte, Werdegang,
Kundenstimmen, FAQ. Das Include-Plugin kennt dafür Schleifen
(`<!--#each in="shop.categories" file="…" -->`), Bedingungen (`{{#if draft}}`)
und indirekte Verweise (`{{images.[image].alt}}`). Eine Preisänderung ist
damit eine Zeile in `site.json`, keine Suche über sechzehn Dateien.
Nicht aufgelöste Platzhalter brechen den Build ab, statt sichtbar zu werden.

**Portabler Build.** `plugins/portable-output.js` macht wurzelabsolute
Verweise relativ, entfernt `crossorigin` und ersetzt `type="module"` durch
`defer`. Grund: Module und Ressourcen mit `crossorigin` werden vom Browser per
CORS geladen, was über `file://` grundsätzlich scheitert. Das gebündelte
Skript enthält keine Modul-Syntax und ist damit gültiges klassisches
JavaScript.

**JavaScript.** Sechs Module in einem Bundle. Jedes prüft selbst, ob seine
Hooks im DOM liegen, und tut sonst nichts. Ohne JavaScript bleiben alle
Inhalte lesbar; nur Menü, Lightbox, Filter und Themewechsel entfallen.

## Barrierefreiheit

Skip-Link, Landmarks, genau eine `h1` je Seite, lückenlose
Überschriftenhierarchie. Fokusring mit 3 px und Versatz. Mobile-Menü und
Lightbox mit Fokusfalle, Escape und Fokusrückgabe. Formularfehler über
`aria-describedby`, Status in einer Live-Region, nie allein über Farbe.
Bedienelemente mindestens 44 × 44 px. Alle Animationen unter
`prefers-reduced-motion: reduce` abgeschaltet.

`npm run test:a11y` prüft zusätzlich zu axe-core auch Dinge, die
automatisierte Regeln nicht abdecken: Überschriftensprünge, fehlende
Bildmaße, Länge der Meta-Beschreibungen, Tastaturbedienung von Menü,
Lightbox, Formular und Shop-Filter — sowie transliterierte Umlaute wie
„Ueber“ oder „koennte“ in sichtbarem Text.

## Hinweis zur Ablage

Das Projekt liegt derzeit in einem OneDrive-synchronisierten Ordner. Das ist
für `node_modules` riskant: OneDrive ersetzt selten genutzte Dateien durch
Platzhalter, die bei Zugriff nachgeladen werden. Schlägt das fehl, liefert das
Lesen `ETIMEDOUT` oder eine mit Nullbytes gefüllte Datei — der Build hängt
oder bricht mit rätselhaften Fehlern ab. Beides ist während der Entwicklung
aufgetreten.

Abhilfe: `node_modules` in den OneDrive-Einstellungen von der Synchronisation
ausnehmen, oder das Projekt außerhalb von OneDrive ablegen. Das ausgelieferte
`dist/` ist davon nicht betroffen.

## Offene Punkte für den Livegang

1. Alle Entwurfstexte durch Chris freigeben oder ersetzen.
2. Rechtstexte juristisch prüfen, Platzhalter füllen, `noindex` entfernen.
3. Echte Kundenstimmen mit schriftlicher Einwilligung einholen.
4. Formularversand anbinden; danach den Datenschutzhinweis ergänzen.
5. Entscheiden, ob der Shop bei IONOS bleibt oder integriert wird.
6. Fotos für Spürhunde und Sporthunde ergänzen — dafür gibt es bislang keine.
