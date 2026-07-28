# Mad Dogs Germany – LLM-Alternative-Versionen

Dieses Repository enthält mehrere alternative Umsetzungen der Website „Mad Dogs Germany“ – jeweils als eigene Version in einem Ordner. Die Varianten entstanden aus unterschiedlichen LLM-Ansätzen und unterscheiden sich vor allem im Aufbau, im technischen Stack und in der Art der Inhalte.

## Überblick

| Ordner | Variante | Tech-Stack | Kurzcharakteristik |
| --- | --- | --- | --- |
| `gemini31` | Gemini 3.1-Variante | – | Ordner vorhanden, derzeit ohne sichtbare Content-Dateien |
| `gemini35` | Gemini 3.5 | HTML5, CSS, Vanilla JS | Statische Mehrseiten-Website ohne Build-Schritt |
| `gpt55` | GPT-5-Variante | HTML, CSS, JS, PHP-Contact-Endpoint, `.htaccess` | Statische Seiten mit Kontakt-Formular-Fallback und Redirects |
| `grok45` | Grok 4.5-Variante | HTML, CSS, JS, Node-Skripte | Strukturierte, modulare Umsetzung mit getrennten CSS- und JS-Bereichen |
| `MAI1` | MAI-1-Variante | HTML, CSS, JS | Kleine, einfache und kompakte statische Umsetzung |
| `opus48` | Opus 4.8-Variante | HTML5, CSS, Vanilla JS | Moderne statische Website mit Progressive Enhancement und selbst gehosteten Schriften |
| `opus5` | Opus 5-Variante | Node.js, Vite, HTML, CSS, JS, Playwright, Lighthouse CI | Vollständigere Build-Pipeline mit Multi-Page-Generierung |
| `Sonnet5` | Sonnet 5-Variante | Python, HTML, CSS, JS | Generator-basiert, erzeugt die Seiten aus einem zentralen Build-Skript |

---

## 1. `gemini31`

### Status
- Der Ordner ist vorhanden, aber aktuell ohne sichtbare Content-Dateien oder erkennbare Website-Struktur.

### Tech-Stack
- Noch nicht näher spezifiziert

### Struktur
- Nur der Ordner selbst ist vorhanden

### Besonderheit
- Noch nicht weiter ausgearbeitet; als leere oder vorbereitete Variante im Repository erkennbar.

---

## 2. `gemini35`

### Tech-Stack
- HTML5
- CSS
- Vanilla JavaScript
- Bild-Assets als JPEG/PNG/WebP
- Kein Build-Tool, keine Frameworks

### Struktur
- Root-Seiten wie `index.html`, `shop.html`, `dogwalker.html`, `training.html`, `impressum.html`, `datenschutz.html`
- `css/` mit `styles.css` und `fonts.css`
- `js/main.js`
- `assets/img/` für Bilder und Icons
- `assets/fonts/` für Schriftdateien

### Besonderheit
- Sehr einfache, direkt nutzbare statische Website mit klarer Seitenstruktur.

---

## 3. `gpt55`

### Tech-Stack
- HTML
- CSS
- Vanilla JavaScript
- PHP-Formular-Endpoint (`assets/contact/send.php`)
- Apache-Redirects über `.htaccess`

### Struktur
- Root-Dateien wie `index.html`, `404.html`, `README.md`
- `assets/css/styles.css`
- `assets/js/main.js`
- `assets/contact/send.php`
- Mehrere Unterordner wie `dogwalker-service/`, `training/`, `shop/`, `ueber-uns/`, `kontakt/`, `impressum/`, `datenschutz/`
- `robots.txt`, `sitemap.xml`, `site.webmanifest`

### Besonderheit
- Die Variante legt besonderen Wert auf klassische Webspace-Kompatibilität und Redirect-Handling.

---

## 4. `grok45`

### Tech-Stack
- HTML
- CSS
- Vanilla JavaScript
- Node-basierte QA-/Link-Prüfskripte

### Struktur
- Root-Seiten wie `index.html`, `shop.html`, `dogwalker.html`, `kontakt.html`, `impressum.html`, `datenschutz.html`
- `css/` mit getrennten Dateien:
  - `base.css`
  - `layout.css`
  - `components.css`
  - `tokens.css`
- `js/` mit `main.js`, `form.js`, `gallery.js`
- `assets/images/` und `assets/icons/`
- `scripts/verify-links.mjs`
- `docs/` für Planungs- und Spezifikationsdateien

### Besonderheit
- Die Struktur ist am stärksten modularisiert und wirkt wie eine „Design-System“-Umsetzung.

---

## 5. `MAI1`

### Tech-Stack
- HTML
- CSS
- Vanilla JavaScript

### Struktur
- Kompakte Seitenstruktur mit Unterordnern wie:
  - `about/`
  - `contact/`
  - `dogwalker-service/`
  - `legal/`
  - `privacy/`
  - `shop/`
  - `testimonials/`
  - `training/`
- `styles.css`
- `script.js`
- `index.html`

### Besonderheit
- Sehr schlanke und leicht verständliche Umsetzung ohne zusätzliche Build- oder Generator-Mechanik.

---

## 6. `opus48`

### Tech-Stack
- HTML5
- CSS
- Vanilla JavaScript
- Selbst gehostete Schriften
- Keine Frameworks

### Struktur
- Root-Seiten wie `index.html`, `dogwalker.html`, `training.html`, `shop.html`, `ueber-uns.html`, `kontakt.html`, `impressum.html`, `datenschutz.html`
- `css/styles.css` und `css/fonts.css`
- `js/main.js`
- `assets/img/` für Fotografien und Icons
- `assets/fonts/` für lokale Schriftarten
- `favicon.svg`, `site.webmanifest`, `robots.txt`, `sitemap.xml`

### Besonderheit
- Akzent auf Barrierefreiheit, progressive enhancement und moderne statische SEO-Praktiken.

---

## 7. `opus5`

### Tech-Stack
- Node.js
- Vite
- HTML/CSS/JS
- Playwright
- Lighthouse CI
- Sharp für Bildverarbeitung

### Struktur
- `package.json`
- `vite.config.js`
- `plugins/` für HTML-Includes und portable Ausgabe
- `dist/` für Build-Ausgabe
- `docs/` und `tests/`
- `.lighthouseci/` für automatisierte Qualitätsprüfungen
- Mehrere Inhalte und Seiten direkt im Ordnerstrukturmodell

### Besonderheit
- Die technisch ausgereifteste Variante mit echter Build-Pipeline und Qualitäts-Checks.

---

## 8. `Sonnet5`

### Tech-Stack
- Python
- HTML
- CSS
- Vanilla JavaScript

### Struktur
- `tools/build.py` als zentraler Generator für die statischen Seiten
- Root-Seiten wie `index.html`, `404.html`, `robots.txt`, `sitemap.xml`, `site.webmanifest`
- Mehrsprachige Inhalte unter `en/` und deutschen Seiten im Root
- `assets/css/styles.css`
- `assets/js/main.js`
- `assets/images/`
- `.htaccess`

### Besonderheit
- Diese Variante ist generator-basiert und erzeugt Inhalte konsistent aus einem zentralen Skript heraus.

---

## Ziel dieses Repositories

Die verschiedenen Ordner zeigen, wie dieselbe Websiteidee mit unterschiedlichen Ansätzen und Prioritäten umgesetzt werden kann – von einer einfachen statischen Seite bis hin zu einer build-basierten, stärker automatisierten Lösung.
