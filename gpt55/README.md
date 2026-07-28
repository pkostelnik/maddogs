# Mad Dogs Germany - statischer Relaunch

Modernes, barrierearmes und mobile-first Redesign von `mad-dogs-germany.de` als statische Website ohne Framework, Build-Schritt, Tracking oder externe Schriftarten.

## Struktur

- `/` Startseite
- `/dogwalker-service/` Dogwalker-Service mit Preisen und Galerie
- `/training/` Hundesport, Mantrailing und Spürhunde
- `/shop/` Shop-Teaser und Reico-Partnerlink
- `/ueber-uns/` Qualifikation und Werdegang von Chris Knittel
- `/kundenstimmen/` Platzhalter für echte freigegebene Bewertungen
- `/kontakt/` Kontaktformular und direkte Kontaktwege
- `/impressum/`, `/datenschutz/` Rechtliche Seiten mit TODO-Hinweisen
- `/assets/css/styles.css` komplettes Designsystem
- `/assets/js/main.js` Navigation, Lightbox, Formular-Enhancement, Jahr

## Lokal ansehen

Die Seite nutzt root-relative Pfade. Im Ordner `gpt55` einen lokalen Server starten:

```powershell
python -m http.server 8000
```

Danach `http://localhost:8000/` öffnen.

## Best Practices

- Mobile-first CSS mit fluiden Größen über `clamp()`.
- Semantische HTML-Landmarks, Skip-Link, sichtbare Fokuszustände.
- ARIA-konforme mobile Navigation mit Escape-Schließen und Fokus-Rückgabe.
- Native Formularfelder mit Labels, Fehlermeldungen und Live-Status.
- `<dialog>`-Lightbox mit Tastaturbedienung und Fallback.
- Lokale Bilder mit `width`/`height`, Lazy Loading und WebP-Fallbacks.
- Keine Cookies, kein Analytics, keine Remote-Fonts, keine Social-/Shop-Embeds.
- Legacy-URLs werden per `.htaccess` und HTML-Fallback-Seiten weitergeleitet.

## Vor Veröffentlichung prüfen

- Impressum und Datenschutzerklärung rechtlich prüfen lassen.
- Adresse, Umsatzsteuer-ID/Kleinunternehmerhinweis und Hoster-Daten ergänzen.
- Empfänger und Mailzustellung in `assets/contact/send.php` testen.
- Externe URLs zu Spreadshop, Reico und Instagram final bestätigen.
- Optional echte Kundenstimmen einpflegen, sobald Freigaben vorliegen.
