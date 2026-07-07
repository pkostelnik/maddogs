# Mad Dogs Germany — Website-Relaunch

Modernes, barrierefreies, Mobile-First-Redesign der Website von **Mad Dogs
Germany** (Chris Knittel) — Dogwalker-Service, Hundesport und Mantrailing in
Niederkassel bei Köln/Bonn.

Diese Website besteht ausschließlich aus **statischem HTML, CSS und
Vanilla-JavaScript**. Es gibt **keinen Build-Schritt, keine Abhängigkeiten,
kein Framework** — die Dateien in diesem Ordner sind bereits das fertige
Produkt und können 1:1 auf einen beliebigen Webspace (z. B. das bisherige
IONOS-Hosting), Netlify, Vercel oder GitHub Pages hochgeladen werden.

---

## 1. Projektstruktur

```
/                        Startseite (Deutsch, Standardsprache)
/ueber-uns/               Über uns
/training/                Hundesport, Mantrailing, Spürhunde
/dogwalker-service/       Dogwalker-Service (Preise, Galerie)
/shop/                    Shop-Übersicht + Reico-Partnerlink
/kundenstimmen/           Kundenstimmen (bewusst ehrlicher Platzhalter)
/kontakt/                 Kontaktformular + Kontaktdaten
/impressum/               Impressum
/datenschutz/             Datenschutzerklärung
/404.html                 Fehlerseite (zweisprachig)
/en/…                     Vollständige englische Version aller Seiten

/assets/css/styles.css    Gesamtes Stylesheet (Design-Tokens + Komponenten)
/assets/js/main.js        Nav-Toggle, Lightbox, Formular, Footer-Jahr
/assets/images/           Alle Bilder als JPEG/PNG + WebP (mit <picture>)
/assets/contact/send.php  Optionaler PHP-Handler fürs Kontaktformular

robots.txt, sitemap.xml, site.webmanifest, favicons — SEO/PWA-Grundausstattung

/_tools/                  NUR internes Autoren-Werkzeug, siehe Abschnitt 6
```

## 2. Lokal ansehen

Da die Seiten mit **root-relativen Pfaden** arbeiten (z. B. `/assets/...`),
funktioniert das direkte Doppelklick-Öffnen der `.html`-Dateien im Browser
nicht korrekt. Stattdessen lokal einen einfachen Webserver starten:

```bash
python3 -m http.server 8000
# dann im Browser: http://localhost:8000/
```

(Alternativ z. B. die VS-Code-Erweiterung „Live Server".)

## 3. Hosting / Deployment

Alle Dateien außer `/_tools/` per FTP/SFTP bzw. Git-Deploy auf den Webspace
hochladen. Der Server muss lediglich `index.html` als Verzeichnis-Index
ausliefern (Standard bei praktisch jedem Static-Hosting/Apache/Nginx/IONOS).

- **IONOS Webhosting (klassisch, wie bisher):** Dateien per FTP hochladen;
  `send.php` funktioniert dort direkt (PHP ist Standard bei IONOS).
- **Netlify/Vercel/GitHub Pages:** funktioniert ebenso, PHP dann aber nicht —
  siehe Formular-Hinweis unten.

## 4. Kontaktformular

Das Formular unter `/kontakt/` sendet per `fetch()` an
`/assets/contact/send.php` (progressive enhancement: **ohne JavaScript**
funktioniert ein normales POST-Submit an dieselbe URL genauso).

- **Bei PHP-Hosting (z. B. IONOS):** `send.php` einfach mit hochladen,
  Empfänger-E-Mail in der Datei prüfen/anpassen. Empfehlenswert:
  SPF/DKIM für die Absender-Domain beim Hoster einrichten, damit die Mails
  nicht im Spam landen.
- **Ohne PHP (Netlify/Vercel/…):** `send.php` funktioniert nicht. Alternativen:
  - Netlify Forms: `<form>`-Tag um `netlify` Attribut ergänzen.
  - [Formspree](https://formspree.io) oder [Web3Forms](https://web3forms.com):
    kostenloser Form-Endpunkt, `action`-URL im `<form>` in
    `_tools/content/{de,en}/contact.html` austauschen und `_tools/generate.py`
    erneut laufen lassen (oder direkt in den fertigen `index.html`-Dateien
    unter `/kontakt/` und `/en/contact/` anpassen).

Bis ein Formular-Backend läuft, bleiben Telefon, WhatsApp und E-Mail auf jeder
Seite prominent als zuverlässiger Kontaktweg sichtbar.

## 5. Bitte vor Veröffentlichung prüfen (TODO)

Diese Punkte sind bewusst offen/markiert, weil sie nur der Betreiber
verbindlich klären kann:

- ⚠️ **Adress-Unstimmigkeit:** Die alte Website nannte im Impressum/Kontakt
  „Hauptstraße 72, 53859 Niederkassel", in der alten Datenschutzerklärung aber
  „Bennoplatz 14, 51103 Köln". Diese Seiten übernehmen Niederkassel — bitte
  bestätigen und ggf. überall konsistent korrigieren
  (`/impressum/`, `/datenschutz/`, `/en/legal-notice/`, `/en/privacy/`,
  `/kontakt/`, `/en/contact/`, Footer in `_tools/generate.py`).
- ⚠️ **Umsatzsteuer-ID** im Impressum ergänzen (oder Kleinunternehmer-Hinweis).
- ⚠️ **Hosting-Anbieter** in der Datenschutzerklärung eintragen, sobald final
  entschieden (Name, Anschrift, Link zur AVV/Datenschutzerklärung des Hosters).
- ⚠️ Beide Rechtstexte (`/impressum/`, `/datenschutz/` und die
  englischen Pendants) vor Live-Schaltung von einer rechtskundigen Person
  gegenlesen lassen. Sie wurden bewusst schlank und akkurat zum tatsächlichen
  Funktionsumfang neu geschrieben (keine Cookies, kein Tracking) — sind aber
  **kein Ersatz für rechtliche Beratung**.
- ⚠️ **Alte AGB-Seite wurde bewusst nicht übernommen:** Sie beschrieb
  fälschlich eine Shopify-Anbindung, obwohl der Shop über IONOS/Spreadshop
  läuft — inhaltlich falsche Rechtstexte sind ein echtes Risiko. Falls für den
  Dogwalker-/Trainingsservice eigene Leistungsbedingungen gewünscht sind,
  sollten diese neu und zutreffend von einer Rechtsberatung aufgesetzt werden.
- ⚠️ **Kundenstimmen:** Seite zeigt bewusst einen ehrlichen Platzhalter statt
  erfundener Bewertungen. Sobald echte, freigegebene Zitate vorliegen, können
  sie in `/kundenstimmen/` (und `/en/testimonials/`) eingepflegt werden
  (Komponente `.testimonial` in `styles.css` steht bereits bereit).
- Externe Shop-URL (`https://mad-dogs-germany.myspreadshop.de/`) bitte
  verifizieren — sie wurde aus einem defekten Embed-Link der alten Seite
  rekonstruiert.

## 6. `_tools/` — optionales Autoren-Werkzeug

Die Live-Website selbst braucht **keinen Build-Schritt**. Damit Header, Navigation
und Footer über 19 Einzelseiten (DE + EN) hinweg aber garantiert konsistent
bleiben — genau das war ein Kernproblem der alten Seite (doppelte,
widersprüchliche Navigation) — wurden alle Seiten aus wenigen Textbausteinen
generiert:

```bash
python3 _tools/generate.py   # erzeugt alle index.html-Dateien + sitemap.xml + 404.html
python3 _tools/qa_check.py   # prüft interne Links, alt-Texte, doppelte IDs, Labels ...
```

Wenn sich z. B. Telefonnummer, Öffnungszeiten oder ein Navigationspunkt
ändern, genügt eine Anpassung in `_tools/generate.py` bzw. den Dateien unter
`_tools/content/{de,en}/*.html`, gefolgt von `python3 _tools/generate.py`.

**Der `_tools/`-Ordner kann jederzeit gelöscht werden**, ohne dass die
Website davon betroffen ist — er wird zur Laufzeit nicht eingebunden. Wer
lieber komplett ohne dieses Tooling arbeitet, bearbeitet die erzeugten
`index.html`-Dateien einfach direkt (Header/Footer dann von Hand in jeder
Datei konsistent halten).

## 7. Design- und Technik-Entscheidungen (Best Practices)

- **Mobile-first CSS**: jede Regel gilt zuerst fürs Telefon, danach folgen
  `min-width`-Erweiterungen für Tablet/Desktop.
- **Keine Web-/Google-Fonts**: reiner Systemfont-Stack. Das ist nicht nur
  schneller (kein Render-Blocking, kein zusätzlicher Request), sondern
  vermeidet auch die in Deutschland rechtlich heikle Google-Fonts-Problematik
  (Nachladen von Schriften über Google-Server ohne Einwilligung).
- **Keine Cookies, kein Tracking, keine eingebetteten Drittinhalte** → es ist
  aktuell kein Cookie-Consent-Banner nötig (im Gegensatz zur alten Seite).
- **Bilder**: JPEG/PNG + WebP parallel (`<picture>`), `loading="lazy"` für
  Inhalte unterhalb des ersten Sichtbereichs, `width`/`height` gegen
  Layout-Verschiebungen (CLS), beschreibende Alt-Texte auf Basis der
  tatsächlichen Bildinhalte (keine generischen Platzhalter).
- **Barrierefreiheit**: Skip-Link, semantische Landmarken, sichtbarer
  Fokusring, ARIA-konforme mobile Navigation (Disclosure-Pattern inkl.
  Escape-Taste und Fokus-Rückgabe), natives `<dialog>` für die Lightbox
  (native Fokus-Falle + Escape), Formular mit verknüpften Labels und
  live-angesagten Fehlermeldungen, Honeypot statt CAPTCHA.
  Automatisiert geprüft mit **axe-core** (0 Verstöße gegen WCAG 2.1 A/AA auf
  allen 19 Seiten) sowie manuell gegen Tastaturbedienung getestet.
- **Performance**: eine einzige, kompakte CSS-Datei, kein JS-Framework,
  Gesamtgröße des gesamten Assets-Ordners ca. 4,7 MB verteilt auf alle
  Bilder aller Seiten (pro Seite lädt jeweils nur ein Bruchteil davon).
- **SEO/Struktur**: eindeutige Title/Description je Seite, kanonische URLs,
  `hreflang`-Alternates zwischen DE/EN, `sitemap.xml`, `robots.txt`,
  LocalBusiness-JSON-LD auf der Startseite.

## 8. Bekannte Abweichungen von der alten Seite (bewusst)

- „Spürhunde", „Sporthunde" und „Man/Pet Trail" waren zuvor separate,
  teils leere/Platzhalter-Unterseiten. Sie sind hier zu **einer** Seite
  `/training/` mit drei klar strukturierten Abschnitten zusammengeführt —
  bessere Nutzerführung, keine Dünn-Content-Seiten.
- Die defekten Navigationspunkte „test" und „Bekleidung" (kaputte
  Embed-Shortcodes) wurden nicht übernommen.
- Der Shop bleibt bewusst ein gestalteter Teaser mit Link zum externen
  Spreadshop-Angebot statt einer erneuten fehleranfälligen Einbettung.

## 9. Nächste sinnvolle Ausbaustufen (optional, nicht Teil dieses Auftrags)

- Echte Kundenstimmen einpflegen, sobald verfügbar.
- Eigene, hochauflösende Fotografien statt der übernommenen Bestandsbilder.
- Eigenständige Unterseiten für Hundesport/Mantrailing/Spürhunde, falls der
  Content dafür künftig umfangreich genug ist.
- Dark-Mode (`prefers-color-scheme`) — Design-Tokens sind so aufgebaut, dass
  sich das später sauber ergänzen lässt.
