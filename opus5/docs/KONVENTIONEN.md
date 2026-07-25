# Konventionen für Seiten in diesem Prototyp

Verbindlich für alle neuen HTML-Seiten. Referenzseiten zum Abschauen:
`index.html`, `training/index.html`, `training/dogwalking/index.html`.

## Dateiablage

Jede Seite liegt als `<pfad>/index.html` im Projektwurzelverzeichnis, damit die
URL sauber ist. Beispiel: `shop/halsbaender/index.html` → `/shop/halsbaender/`.
Neue Seiten werden von `vite.config.js` automatisch erfasst, keine Registrierung nötig.

## Grundgerüst

```html
<!doctype html>
<html lang="de">
  <head>
    <!--#include file="src/partials/head.html" {
      "title": "Seitentitel ohne Markennamen",
      "description": "150-160 Zeichen, ohne Umlaute in dieser JSON-Zeile",
      "path": "/pfad/"
    } -->
  </head>
  <body>
    <!--#include file="src/partials/header.html" -->
    <main id="main">
      ...
      <!--#include file="src/partials/cta-band.html" {
        "title": "Kurze Handlungsaufforderung",
        "text": "Ein bis zwei Saetze."
      } -->
    </main>
    <!--#include file="src/partials/footer.html" -->
  </body>
</html>
```

**Wichtig:** Im JSON der Include-Direktive keine verschachtelten geschweiften
Klammern verwenden – der Parser trennt Direktiven an der ersten schließenden
Klammer.

Umlaute sind im JSON dagegen ausdrücklich erwünscht: `JSON.parse` verarbeitet
UTF-8 korrekt. Die Werte landen in Seitentiteln, Meta-Beschreibungen und
sichtbaren Überschriften. „Ueber uns“ oder „koennte“ dürfen dort niemals
auftauchen.

## Seitenkopf

Jede Unterseite beginnt mit `.page-head` (optional `.page-head--media` plus
`.page-head__bg` für ein Hintergrundbild), darin `.breadcrumb`, `<h1>` und ein
`.lead`. Genau eine `<h1>` pro Seite. Überschriftenebenen lückenlos.

## Verfügbare Layoutklassen

- `.wrap` – Rasterelement. Kinder liegen standardmäßig in der Spalte `wide`,
  `.narrow` verengt auf Lesebreite, `.full` bricht randlos aus.
- `.section`, `.section--tight`, `.section--surface`, `.section--deep`
- `.section__head`, `.section__head--split`
- `.grid-auto`, `.grid-auto--sm`, `.grid-auto--lg`
- `.split`, `.split--media-end`, `.split__media`
- `.stack`, `.cluster`, `.flow`, `.prose`, `.two-col-list`

## Verfügbare Komponenten

`.btn` (`--ember`, `--ghost`, `--quiet`, `--lg`, `--block`), `.link-arrow`,
`.badge` (`--accent`, `--draft`), `.draft-note`, `.chip`, `.card`
(`.card__media`, `.card__index`, `.card__title`, `.card__link`, `.card__text`,
`.card__foot`), `.tile` (`.tile__title`, `.tile__meta`), `.media`
(`--portrait`, `--landscape`, `--wide`, `--framed`), `.stats`/`.stat`,
`.checklist` (`--target`), `.steps`, `.price-table`, `.quote`,
`.quote-columns`, `.faq`, `.timeline`, `.partner-row`, `.form`, `.field`,
`.gallery`, `.product`, `.filter-bar`, `.product-grid`, `.service-layout`,
`.service-aside`, `.service-block`, `.service-hub-card`, `.eyebrow`, `.lead`,
`.text-muted`, `.visually-hidden`.

Reicht das Vorhandene nicht aus, ergänze eine neue Klasse in der passenden
Datei unter `src/styles/components/` oder `src/styles/pages/` – niemals
Inline-Styles für strukturelle Gestaltung. Vereinzelte Inline-Styles für
Feinheiten sind zulässig, aber die Ausnahme.

## Bilder

Alle Varianten liegen unter `/src/assets/images/`. Muster:
`name-BREITE.avif`, `name-BREITE.webp`, Rückfallebene `name.jpg` bzw. `.png`.
Das Manifest mit Alt-Texten und Maßen steht in `src/content/images.json`.

Immer als `<picture>` mit AVIF-Quelle, `sizes`, `width`, `height`,
`loading="lazy"` und `decoding="async"`. Ausnahme: das erste sichtbare Bild
einer Seite bekommt `fetchpriority="high"` und kein `lazy`.

Verfügbare Bildnamen: `logo-mad-dogs`, `logo-mad-dogs-alt`,
`logo-dogwalker-ndk`, `logo-reico-partner`, `hero-malinois-wiese`,
`chris-fuehrt-malinois`, `chris-mit-hund-umarmung`, `chris-portrait-hund`,
`training-platzarbeit`, `malinois-wald-fels`, `hund-geschirr-einsatz`,
`galerie-golden-retriever`, `galerie-hund-maulkorb`, `galerie-mischling-weg`,
`galerie-pinscher-feld`, `galerie-weisser-hund`, `galerie-hund-im-auto`.

Dekorative Bilder bekommen `alt=""`. Inhaltstragende Bilder bekommen einen
beschreibenden Alt-Text – niemals „Bild von …“.

## Barrierefreiheit (nicht verhandelbar)

- Jede `<section>` mit `aria-labelledby`, das auf ihre Überschrift zeigt.
- Interaktive Elemente mindestens 44 × 44 px.
- Buttons, die etwas umschalten, tragen `aria-expanded` oder `aria-pressed`.
- Listen von Karten als `<ul role="list">` mit `<li>`.
- Keine Information allein über Farbe.
- Externe Links: `rel="noopener"` und ein Hinweis im Linktext oder per
  `.visually-hidden`, dass ein externes Angebot geöffnet wird.

## Inhalte

Gesicherte Fakten: Standort Niederkassel, Telefon 0173 3649143,
E-Mail info@mad-dogs-germany.de, Instagram `mad_dogs_germany`,
gegründet 2023, Dogwalking-Preise 20 / 25 / 30 €, Gruppen bis 10 Hunde,
16 Jahre Hundeführung, über 70 Turnierstarts, Vizemeister DM GL 2000 (2017),
3. Platz SWHV CSC und GL 2000 (2018), Ehrenpreise der Stadt Metzingen 2017
und 2018, Schutzdiensthelfer, Pet-/Man-Trail-Trainer nach neunmonatiger
Ausbildung in Österreich, Diensthundeführer im zivilen und militärischen
Sicherheitsdienst, Hundetrainerausbildung bei Kynologisch, 1,5 Jahre in einer
großen Kölner Hundetagesstätte.

Alles, was darüber hinausgeht, ist erfunden und **muss** sichtbar als Entwurf
gekennzeichnet werden – entweder mit `<span class="badge badge--draft">Entwurf</span>`
oder mit einem `.draft-note`-Block am Anfang des betroffenen Abschnitts.

Tonfall: direkt, sachlich, per Du, keine Werbefloskeln, keine Ausrufezeichen,
keine Emoji. Kurze Sätze. Deutsche Anführungszeichen „so“.

## Prüfen

Nach dem Schreiben `npx vite build` ausführen. Der Build muss fehlerfrei
durchlaufen und die neue Seite in der Ausgabe auftauchen.
