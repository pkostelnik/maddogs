# Mad Dogs Germany — Website-Relaunch

Modernes, barrierefreies Mobile-First-Redesign der Website von **Mad Dogs
Germany** (Chris Knittel) — Dogwalker-Service, Hundesport und Mantrailing in
Niederkassel bei Köln/Bonn.

Die Website besteht ausschließlich aus **statischem HTML, CSS und
Vanilla-JavaScript**. Es gibt **keinen Build-Schritt, keine Abhängigkeiten,
kein Framework** — alle Dateien in diesem Ordner sind bereits das fertige
Produkt und können 1:1 auf einen beliebigen Webspace (z. B. das bisherige
IONOS-Hosting), Netlify, Vercel oder GitHub Pages hochgeladen werden.

---

## 1. Projektstruktur

```
/                         Startseite (Deutsch)
/ueber-mich/              Über Chris Knittel: Werdegang, Qualifikation, Haltung
/training/                Hundesport, Mantrailing, Spürhunde (eine Seite, drei Abschnitte)
/dogwalker-service/       Dogwalker-Service: Preise, Galerie mit Lightbox
/shop/                    Mad Dogs Shop (extern) + Reico Hundefutter
/kundenstimmen/           Ehrlicher Platzhalter statt erfundener Bewertungen
/kontakt/                 Kontaktformular + direkte Kontaktwege
/impressum/               Impressum
/datenschutz/             Datenschutzerklärung
/404.html                 Fehlerseite (zweisprachig DE/EN)

/en/                      Vollständige englische Version aller Seiten oben
/en/about/, /en/training/, /en/dogwalker-service/, /en/shop/,
/en/testimonials/, /en/contact/, /en/legal-notice/, /en/privacy/

/assets/css/styles.css    Gesamtes Stylesheet (Design-Tokens + Komponenten)
/assets/js/main.js        Nav-Toggle, Lightbox, Formular, Anker-Fokus, Footer-Jahr
/assets/images/           Bilder als JPEG/PNG + WebP (mit <picture>), Favicons

robots.txt, sitemap.xml, site.webmanifest, .htaccess — SEO/PWA/Hosting-Grundausstattung

/tools/build.py           NUR internes Autoren-Werkzeug, siehe Abschnitt 6
```

## 1a. Sprachen & Sprachumschalter

Jede Seite existiert vollständig auf Deutsch (Standardsprache, root-relative
Pfade wie `/training/`) und Englisch (`/en/training/`). Der Umschalter im
Header (und die Sprachlogik dahinter) merkt sich dabei den **Seitenkontext**:
Ein Klick auf „EN" auf `/training/` führt zu `/en/training/`, nicht zur
englischen Startseite. Technisch relevant:

- `<html lang="de">` bzw. `<html lang="en">` je nach Seite.
- `<link rel="alternate" hreflang="…">` (de/en/x-default) im `<head>` jeder
  Seite, plus passende `og:locale` / `og:locale:alternate`.
- `sitemap.xml` enthält beide Sprachversionen inkl. `xhtml:link`-Alternates.
- Die 404-Seite ist bewusst zweisprachig (ein einzelnes Fehlerdokument, das
  die meisten Static-Hosts ohnehin nur einmal erlauben).
- Rechtstexte (Impressum/Datenschutz) sind auf Englisch übersetzt, die
  zitierten Gesetzesparagrafen (TMG, DSGVO/GDPR, MStV) bleiben als Referenz
  auf die tatsächlich geltende deutsche Rechtsgrundlage bestehen — das ist
  bei deutschen Unternehmen mit fremdsprachigem Impressum üblich und korrekt.

## 1b. Automatische Theme-Erkennung: Hell / Dunkel / Mehr Kontrast

Die Website fragt **nicht** manuell nach einem Theme, sondern erkennt und
respektiert ausschließlich die vom Betriebssystem/Browser bereits
eingestellte Präferenz — vollautomatisch, ganz ohne JavaScript, rein über
CSS-Medienabfragen in `assets/css/styles.css` (Abschnitt 01):

| Einstellung im System | Ergebnis auf der Website |
| --- | --- |
| Hell (Standard) | Warmes, cremefarbenes Grundthema |
| Dunkel (`prefers-color-scheme: dark`) | Eigenständig abgestimmtes Dark Theme |
| „Kontrast erhöhen" (macOS/Firefox `prefers-contrast: more`) | Kräftigeres Schwarz/Weiß-Theme, dickere Rahmen (2px), keine Schatten, 4px-Fokusring |
| Kombination Dunkel + Mehr Kontrast | Eigene Variante (reines Schwarz/Weiß, hellere Gold-Akzente) |
| Windows-Hochkontrastmodus (`forced-colors: active`) | Der Browser erzwingt System-Farben; die Website ergänzt dafür sichtbare Rahmen um Buttons/Karten/Formularfelder und blendet rein dekorative Verlaufsflächen aus |

Alle vier eigenen Farbschemata (hell/dunkel × normal/mehr Kontrast) wurden
rechnerisch gegen die WCAG-Kontrastformel geprüft, nicht nur optisch
geschätzt (siehe Abschnitt 7). Zum Testen im Browser: DevTools → „Rendering"
→ „Emulate CSS media feature prefers-color-scheme / prefers-contrast" bzw.
`forced-colors`.



Die Seiten arbeiten mit **root-relativen Pfaden** (z. B. `/assets/...`),
daher funktioniert das direkte Doppelklick-Öffnen der `.html`-Dateien im
Browser nicht korrekt. Stattdessen lokal einen einfachen Webserver starten:

```bash
python -m http.server 8000
# dann im Browser: http://localhost:8000/
```

(Alternativ z. B. die VS-Code-Erweiterung „Live Server".)

## 3. Hosting / Deployment

Alle Dateien außer `/tools/` per FTP/SFTP bzw. Git-Deploy auf den Webspace
hochladen. Der Server muss lediglich `index.html` als Verzeichnis-Index
ausliefern (Standard bei praktisch jedem Static-Hosting/Apache/Nginx/IONOS).

- **IONOS Webhosting (klassisch, wie bisher):** Dateien per FTP hochladen.
  Die mitgelieferte `.htaccess` aktiviert automatisch HTTPS-Erzwingung,
  Sicherheits-Header, Caching und Kompression (nur wirksam auf
  Apache-Servern mit den jeweiligen Modulen — IONOS bringt diese i. d. R.
  mit).
- **Netlify/Vercel/GitHub Pages:** funktioniert ebenso; `.htaccess` wird dort
  schlicht ignoriert (kein Apache).

## 4. Kontaktformular — bewusst ohne Server-Backend

Das Formular unter `/kontakt/` ist so gebaut, dass es **ganz ohne eigenen
Server, ohne PHP und ohne externen Formular-Dienst** funktioniert:

- JavaScript validiert die Eingaben (Name, E-Mail-Format, Mindestlänge der
  Nachricht, Einwilligung) und öffnet beim Absenden das **E-Mail-Programm
  der Besucher:in** mit vorausgefülltem Betreff und Text (`mailto:`-Link).
- Ist JavaScript deaktiviert, sendet das native `<form method="get"
  action="mailto:...">` die Daten als Query-String an dieselbe
  `mailto:`-Adresse — funktioniert in den meisten Browsern ebenfalls,
  Verhalten kann aber variieren.
- Bis auf Weiteres bleiben Telefon, WhatsApp und E-Mail auf jeder Seite
  zusätzlich prominent als zuverlässiger Kontaktweg sichtbar.

**Wer später ein "echtes" Formular-Backend möchte** (Zustellung ohne
Abhängigkeit vom lokalen Mail-Client der Besucher:innen), z. B. bei
Wechsel zu einem PHP-fähigen Hoster oder mit einem Dienst wie Formspree /
Web3Forms / Netlify Forms: einfach das `action`-Attribut des `<form
data-contact-form>` in `/kontakt/index.html` (bzw. in
`tools/build.py` → `contact_content()` und danach `python
tools/build.py` erneut ausführen) anpassen und optional den
JavaScript-Teil in `assets/js/main.js` → `initContactForm()` entsprechend
umbauen.

## 5. Bitte vor Veröffentlichung prüfen (TODO)

Diese Punkte sind bewusst offen markiert, weil sie nur der Betreiber
verbindlich klären kann:

- ⚠️ **Adress-Unstimmigkeit der alten Website:** Im bisherigen
  Impressum/Kontakt stand „Hauptstraße 72, 53859 Niederkassel", in der
  alten Datenschutzerklärung dagegen „Bennoplatz 14, 51103 Köln". Diese
  Seiten übernehmen durchgängig Niederkassel — bitte bestätigen und ggf.
  überall konsistent korrigieren (`/impressum/`, `/datenschutz/`,
  `/kontakt/`, Footer/JSON-LD in `tools/build.py`).
- ⚠️ **Kontakt-E-Mail-Adresse:** Die alte Website nannte im sichtbaren
  Bereich „info@mad-dogs-germany.de", in strukturierten Daten dagegen eine
  private gmx-Adresse. Diese Seiten verwenden durchgängig
  „info@mad-dogs-germany.de" — bitte bestätigen, welches Postfach
  tatsächlich aktiv überwacht wird.
- ⚠️ **Umsatzsteuer-ID** im Impressum ergänzen (oder Kleinunternehmer-Hinweis).
- ⚠️ **Hosting-Anbieter** in der Datenschutzerklärung eintragen, sobald final
  entschieden (Name, Anschrift, Link zur AVV/Datenschutzerklärung des Hosters).
- ⚠️ Beide Rechtstexte (`/impressum/`, `/datenschutz/`) vor Live-Schaltung
  von einer rechtskundigen Person gegenlesen lassen. Sie wurden bewusst
  schlank und akkurat zum tatsächlichen Funktionsumfang neu geschrieben
  (keine Cookies, kein Tracking) — sind aber **kein Ersatz für rechtliche
  Beratung**.
- ⚠️ **Kundenstimmen:** Seite zeigt bewusst einen ehrlichen Platzhalter statt
  erfundener Bewertungen. Sobald echte, freigegebene Zitate vorliegen,
  können sie in `/kundenstimmen/` eingepflegt werden (Komponente
  `.testimonial` in `styles.css` steht bereits bereit, aktuell aber
  ungenutzt).
- Externe Shop-URL (`mad-dogs-germany.myspreadshop.de`) und Reico-Partnerlink
  bitte verifizieren — sie wurden aus Links der alten Seite übernommen.

## 6. `tools/build.py` — optionales Autoren-Werkzeug

Die Live-Website selbst braucht **keinen Build-Schritt**. Damit Header,
Navigation und Footer über 9 Einzelseiten hinweg aber garantiert konsistent
bleiben, wurden alle Seiten aus einem einzigen Python-Skript generiert:

```bash
python tools/build.py   # erzeugt alle index.html-Dateien, 404.html,
                         # robots.txt, sitemap.xml, site.webmanifest, .htaccess
```

Wenn sich z. B. Telefonnummer, Preise oder ein Navigationspunkt ändern,
genügt eine Anpassung der entsprechenden Konstante bzw. Content-Funktion in
`tools/build.py`, gefolgt von einem erneuten `python tools/build.py`.

**Der `tools/`-Ordner kann jederzeit gelöscht werden**, ohne dass die
Website davon betroffen ist — er wird zur Laufzeit nicht eingebunden. Wer
lieber ganz ohne dieses Werkzeug arbeitet, bearbeitet die erzeugten
`index.html`-Dateien einfach direkt (Header/Footer dann von Hand in jeder
Datei konsistent halten).

## 7. Design- und Technik-Entscheidungen (Best Practices)

- **Mobile-first CSS** mit `em`-basierten Breakpoints (skalieren korrekt
  mit der Textgröße/dem Zoom der Nutzer:in) und fluiden Schriftgrößen über
  `clamp()`.
- **Keine Web-/Google-Fonts:** reiner Systemfont-Stack. Das ist nicht nur
  schneller (kein Render-Blocking, kein zusätzlicher Request), sondern
  vermeidet auch die in Deutschland rechtlich heikle Google-Fonts-Problematik.
- **Keine Cookies, kein Tracking, keine eingebetteten Drittinhalte** (keine
  Google-Maps-iframe, keine Social-Embeds) → aktuell ist kein
  Cookie-Consent-Banner nötig.
- **Farbpalette gegen WCAG-Kontrastwerte gerechnet** (nicht nur geschätzt):
  alle Text/Hintergrund-Kombinationen wurden rechnerisch gegen die
  WCAG-2.1-Kontrastformel geprüft (siehe `assets/css/styles.css`,
  Abschnitt 01), inklusive separater Fokusring-Farbe für dunkle Bereiche.
- **Dark Mode, „Mehr Kontrast" und Windows-Hochkontrastmodus** automatisch
  über `prefers-color-scheme`, `prefers-contrast` und `forced-colors` (siehe
  Abschnitt 1b) — keine manuelle Umschaltung nötig, alle Werte
  kontrastgeprüft.
- **Bilder:** JPEG/PNG + WebP parallel (`<picture>`), `loading="lazy"` für
  Inhalte unterhalb des ersten Sichtbereichs, `fetchpriority="high"` fürs
  jeweilige LCP-Bild, `width`/`height` gegen Layout-Verschiebungen (CLS),
  beschreibende Alt-Texte auf Basis der tatsächlichen Bildinhalte.
- **Barrierefreiheit:** Skip-Link, semantische Landmarken (`header`, `nav`,
  `main`, `footer`, `address`), durchgängig sichtbarer Fokusring,
  ARIA-konforme mobile Navigation (Disclosure-Pattern inkl. Escape-Taste
  und Fokus-Rückgabe), natives `<dialog>` für die Lightbox (native
  Fokus-Falle + Escape + Pfeiltasten-Navigation), Formular mit verknüpften
  Labels, live angesagten Fehlermeldungen (`aria-live`) und layoutstabilen
  Fehler-Slots (kein Sprung beim Erscheinen einer Fehlermeldung),
  barrierefreier Honeypot statt CAPTCHA.
- **Progressive Enhancement statt JavaScript-Pflicht:** Ohne JavaScript
  bleibt die komplette Navigation dauerhaft sichtbar/bedienbar, Galerie-Links
  führen direkt zum Originalbild, das Kontaktformular versendet nativ per
  `mailto:`. Erst mit JavaScript kommen Disclosure-Menü, Lightbox und
  Live-Validierung hinzu.
- **Performance:** eine einzige, kompakte CSS-Datei (~37 KB unkomprimiert),
  ein kleines Vanilla-JS ohne Framework, Bilder pro Seite nur in den
  tatsächlich benötigten Größen.
- **SEO/Struktur:** eindeutige Title/Description je Seite, kanonische URLs,
  Open-Graph-/Twitter-Meta-Tags, `sitemap.xml`, `robots.txt`,
  LocalBusiness-JSON-LD auf beiden Startseiten, sichtbare Breadcrumbs,
  `hreflang`-Alternates zwischen DE/EN.
- **Mehrsprachigkeit (DE/EN):** vollständige, eigenständig formulierte
  englische Fassung aller Seiten inkl. Rechtstexte, Sprachumschalter mit
  Seitenkontext-Erhalt (siehe Abschnitt 1a).

## 8. Qualitätssicherung — was tatsächlich automatisiert geprüft wurde

Alle folgenden Prüfungen wurden während der Entwicklung mit **Playwright +
axe-core** sowie einem selbst geschriebenen Link-Checker automatisiert
durchgeführt (nicht nur behauptet):

- **0 axe-core-Verstöße** gegen WCAG 2.0/2.1 A & AA auf allen 19 Seiten
  (9 × Deutsch, 9 × Englisch, 404) — erneut geprüft nach Einführung von
  Mehrsprachigkeit und Kontrast-Themes.
- **422 interne Links und 186 Asset-Referenzen** geprüft — keine defekten
  Verweise, keine fehlenden `alt`-Attribute, keine doppelten IDs, keine
  übersprungenen Heading-Ebenen.
- **Sprachumschalter:** automatisiert geprüft, dass er auf jeder Seite den
  Kontext beibehält (z. B. `/training/` ↔ `/en/training/`, nicht die
  jeweilige Startseite) und dass `hreflang`/`html lang` korrekt gesetzt sind.
- **Tastaturbedienung:** mobiles Menü (Öffnen/Escape/Fokus-Rückgabe),
  Lightbox (Öffnen per Enter, Pfeiltasten, Escape, Fokus-Rückgabe),
  Tab-Reihenfolge.
- **Formular-Validierung:** leere/ungültige Eingaben, Live-Korrektur,
  Honeypot. Dabei wurde per Playwright ein echter Bug gefunden und behoben:
  Eine erst beim ersten Absenden erscheinende Fehlermeldung verschob das
  Layout so, dass ein Klick auf „Senden" ins Leere laufen konnte — jetzt ist
  dafür fester Platz reserviert und die Live-Validierung startet bewusst
  erst nach dem ersten Sende-Versuch.
- **Kein horizontales Scrollen bei 320px Breite** (WCAG 1.4.10 Reflow) auf
  Kernseiten in beiden Sprachen.
- **Ohne JavaScript** (`javaScriptEnabled: false`): Navigation weiterhin
  vollständig sichtbar und bedienbar, Galerie-Links funktionieren als
  normale Bild-Links.
- **Alle vier Farbschemata** (hell/dunkel × normal/mehr Kontrast) sowie der
  Windows-Hochkontrastmodus (`forced-colors`) und `prefers-reduced-motion`
  per Emulation gegengeprüft und per Screenshot visuell kontrolliert.

## 9. Bekannte Abweichungen von der alten Seite (bewusst)

- „Spürhunde", „Sporthunde" und „Man/Pet Trail" waren zuvor separate,
  teils leere Unterseiten. Sie sind hier zu **einer** Seite `/training/`
  mit drei klar strukturierten, per Sprungmarken erreichbaren Abschnitten
  zusammengeführt — bessere Nutzerführung, keine Dünn-Content-Seiten.
- Die defekten Navigationspunkte „test" und der kaputte
  „Bekleidung"-Embed-Shortcode wurden nicht übernommen.
- Der Shop bleibt bewusst ein gestalteter Teaser mit Link zum externen
  Spreadshop-Angebot statt einer erneuten, fehleranfälligen Einbettung.
- Keine Cookie-Consent-Bar mehr: durch den bewussten Verzicht auf Tracking
  und Drittinhalte technisch nicht mehr nötig.

## 10. Nächste sinnvolle Ausbaustufen (optional, nicht Teil dieses Auftrags)

- Echte Kundenstimmen einpflegen, sobald verfügbar.
- Eigenständige, tiefere Unterseiten für Hundesport/Mantrailing/Spürhunde,
  falls der Content dafür künftig umfangreich genug ist.
- Weitere Sprachen nach demselben Muster wie Englisch ergänzen
  (`PATHS`/`PAGE_META` in `tools/build.py` um einen weiteren Sprachschlüssel
  erweitern).
- Formular-Backend mit serverseitiger Zustellung, sobald PHP-fähiges
  Hosting oder ein Formular-Dienst gewünscht ist (siehe Abschnitt 4).
- Optionaler manueller Theme-Schalter zusätzlich zur automatischen
  Erkennung, falls Besucher:innen das System-Theme nicht ändern
  können/wollen (aktuell bewusst nicht enthalten, da nicht angefragt und
  die automatische Erkennung bereits alle gängigen Fälle abdeckt).
