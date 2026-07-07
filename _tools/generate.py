#!/usr/bin/env python3
"""
Internes Autoren-Tool — KEIN Bestandteil der ausgelieferten Website.
---------------------------------------------------------------------
Dieses Skript existiert nur, damit Header/Footer/Nav auf allen Seiten
garantiert IDENTISCH bleiben (genau das war ein Kernproblem der alten
Website: doppelte, uneinheitliche Navigation). Es erzeugt reine,
statische .html-Dateien — das Ergebnis benötigt keinerlei Build-Schritt,
kein Node, kein PHP, keinen Server-Prozess. Nach dem Lauf kann dieser
gesamte _tools/-Ordner gelöscht werden, ohne dass die Website betroffen
ist (siehe README.md).

Aufruf:  python3 _tools/generate.py
"""
import pathlib
import json

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "_tools" / "content"

SITE_NAME = "Mad Dogs Germany"
SITE_URL = "https://www.mad-dogs-germany.de"

# ---------------------------------------------------------------------------
# Seitenregister: kanonischer Schlüssel -> Pfade je Sprache
# (dient u. a. der hreflang-Verknüpfung & dem Sprachumschalter)
# ---------------------------------------------------------------------------
PAGES = {
    "home":         {"de": "/",                      "en": "/en/"},
    "about":        {"de": "/ueber-uns/",             "en": "/en/about/"},
    "training":     {"de": "/training/",              "en": "/en/training/"},
    "dogwalker":    {"de": "/dogwalker-service/",      "en": "/en/dogwalker-service/"},
    "shop":         {"de": "/shop/",                  "en": "/en/shop/"},
    "testimonials": {"de": "/kundenstimmen/",          "en": "/en/testimonials/"},
    "contact":      {"de": "/kontakt/",                "en": "/en/contact/"},
    "legal":        {"de": "/impressum/",              "en": "/en/legal-notice/"},
    "privacy":      {"de": "/datenschutz/",            "en": "/en/privacy/"},
}

NAV_ORDER = ["home", "about", "training", "dogwalker", "shop", "testimonials", "contact"]

NAV_LABELS = {
    "de": {
        "home": "Startseite", "about": "Über uns", "training": "Training",
        "dogwalker": "Dogwalker", "shop": "Shop",
        "testimonials": "Kundenstimmen", "contact": "Kontakt",
    },
    "en": {
        "home": "Home", "about": "About", "training": "Training",
        "dogwalker": "Dogwalker", "shop": "Shop",
        "testimonials": "Testimonials", "contact": "Contact",
    },
}

FOOTER_TEXT = {
    "de": {
        "tagline": "Hundesport, Mantrailing und professioneller Dogwalker-Service in Niederkassel bei Köln/Bonn.",
        "nav_heading": "Navigation",
        "legal_heading": "Rechtliches",
        "contact_heading": "Kontakt",
        "legal_label": "Impressum",
        "privacy_label": "Datenschutzerklärung",
        "hours_label": "Mo–Fr 07:00–18:00 Uhr",
        "rights": "Alle Rechte vorbehalten.",
        "lang_switch": "English",
    },
    "en": {
        "tagline": "Dog sports, mantrailing and professional dog walking in Niederkassel near Cologne/Bonn, Germany.",
        "nav_heading": "Navigation",
        "legal_heading": "Legal",
        "contact_heading": "Contact",
        "legal_label": "Legal notice",
        "privacy_label": "Privacy policy",
        "hours_label": "Mon–Fri 7:00 AM–6:00 PM",
        "rights": "All rights reserved.",
        "lang_switch": "Deutsch",
    },
}

SKIP_LINK = {"de": "Zum Hauptinhalt springen", "en": "Skip to main content"}
MENU_LABEL = {"de": "Menü", "en": "Menu"}
OPEN_MENU = {"de": "Menü öffnen", "en": "Open menu"}


def nav_html(lang, active_key):
    other_lang = "en" if lang == "de" else "de"
    items = []
    for key in NAV_ORDER:
        href = PAGES[key][lang]
        label = NAV_LABELS[lang][key]
        current = ' aria-current="page"' if key == active_key else ""
        items.append(f'<li><a href="{href}"{current}>{label}</a></li>')

    lang_target = PAGES.get(active_key, PAGES["home"])[other_lang]
    lang_label = "EN" if other_lang == "en" else "DE"
    whatsapp_label = "WhatsApp" 
    whatsapp_aria = "Per WhatsApp kontaktieren (öffnet neuen Tab)" if lang == "de" else "Contact via WhatsApp (opens new tab)"

    return f'''    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" data-nav-toggle>
      <span class="visually-hidden">{OPEN_MENU[lang]}</span>
      <span class="nav-toggle__icon" aria-hidden="true"></span>
    </button>
    <nav class="primary-nav" id="primary-nav" aria-label="{MENU_LABEL[lang]}" data-primary-nav data-open="false">
      <ul class="primary-nav__list">
        {chr(10).join(items)}
      </ul>
      <div class="primary-nav__actions">
        <a class="lang-switch" href="{lang_target}" hreflang="{other_lang}" lang="{other_lang}">{lang_label}</a>
        <a class="btn btn--accent btn--sm" href="https://wa.me/491733649143" target="_blank" rel="noopener noreferrer" aria-label="{whatsapp_aria}">{whatsapp_label}<svg class="external-link-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6"/><path d="M10 14 21 3"/></svg></a>
      </div>
    </nav>'''


def header_html(lang, active_key):
    home_href = PAGES["home"][lang]
    nav = nav_html(lang, active_key)
    return f'''  <a class="skip-link" href="#main">{SKIP_LINK[lang]}</a>
  <header class="site-header" data-site-header>
    <div class="container site-header__inner">
      <a class="brand" href="{home_href}">
        <picture>
          <source srcset="/assets/images/logo-256.webp" type="image/webp">
          <img class="brand__logo" src="/assets/images/logo-256.jpg" alt="" width="48" height="48" loading="eager" decoding="async">
        </picture>
        <span>Mad Dogs<span class="brand__sub">Germany</span></span>
      </a>
{nav}
    </div>
  </header>
'''


def footer_html(lang):
    t = FOOTER_TEXT[lang]
    other_lang = "en" if lang == "de" else "de"
    items = []
    for key in NAV_ORDER:
        href = PAGES[key][lang]
        label = NAV_LABELS[lang][key]
        items.append(f'<li><a href="{href}">{label}</a></li>')

    legal_href = PAGES["legal"][lang]
    privacy_href = PAGES["privacy"][lang]
    home_href = PAGES["home"][lang]
    lang_home_target = PAGES["home"][other_lang]

    address_line = (
        "Hauptstraße 72, 53859 Niederkassel" if lang == "de"
        else "Hauptstraße 72, 53859 Niederkassel, Germany"
    )
    phone_label = "Telefon" if lang == "de" else "Phone"
    mail_label = "E-Mail"
    whatsapp_label = "WhatsApp"

    return f'''  <footer class="site-footer">
    <div class="container site-footer__grid">
      <div class="site-footer__brand">
        <a class="brand" href="{home_href}">
          <picture>
            <source srcset="/assets/images/logo-256.webp" type="image/webp">
            <img class="brand__logo" src="/assets/images/logo-256.jpg" alt="" width="40" height="40" loading="lazy" decoding="async">
          </picture>
          <span>Mad Dogs<span class="brand__sub">Germany</span></span>
        </a>
        <p>{t['tagline']}</p>
        <ul class="social-links">
          <li><a href="https://www.instagram.com/mad_dogs_germany/" target="_blank" rel="noopener noreferrer" aria-label="Instagram (öffnet neuen Tab)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>
          </a></li>
          <li><a href="mailto:info@mad-dogs-germany.de" aria-label="{mail_label}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>
          </a></li>
          <li><a href="tel:+491733649143" aria-label="{phone_label}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.36 1.78.7 2.62a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.46-1.27a2 2 0 0 1 2.11-.45c.84.34 1.72.58 2.62.7A2 2 0 0 1 22 16.92z"/></svg>
          </a></li>
        </ul>
      </div>
      <nav class="site-footer__nav" aria-label="{t['nav_heading']}">
        <h2>{t['nav_heading']}</h2>
        <ul>
          {chr(10).join(items)}
          <li><a href="{lang_home_target}">{t['lang_switch']}</a></li>
        </ul>
      </nav>
      <div class="site-footer__contact">
        <h2>{t['contact_heading']}</h2>
        <ul>
          <li>{address_line}</li>
          <li><a href="tel:+491733649143">+49 173 3649143</a></li>
          <li><a href="mailto:info@mad-dogs-germany.de">info@mad-dogs-germany.de</a></li>
          <li><a href="https://wa.me/491733649143" target="_blank" rel="noopener noreferrer">{whatsapp_label} <svg class="external-link-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6"/><path d="M10 14 21 3"/></svg></a></li>
          <li>{t['hours_label']}</li>
        </ul>
      </div>
    </div>
    <div class="container site-footer__bottom">
      <p>&copy; <span data-year>2026</span> {SITE_NAME}. {t['rights']}</p>
      <ul class="legal-links">
        <li><a href="{legal_href}">{t['legal_label']}</a></li>
        <li><a href="{privacy_href}">{t['privacy_label']}</a></li>
      </ul>
    </div>
  </footer>
'''


def head_html(lang, page_key, title, description, og_image="/assets/images/mantrailing-hero-1000.jpg", noindex=False):
    canonical = SITE_URL.rstrip("/") + PAGES[page_key][lang]
    alt_de = SITE_URL.rstrip("/") + PAGES[page_key]["de"]
    alt_en = SITE_URL.rstrip("/") + PAGES[page_key]["en"]
    locale = "de_DE" if lang == "de" else "en_US"
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="de" href="{alt_de}">
  <link rel="alternate" hreflang="en" href="{alt_en}">
  <link rel="alternate" hreflang="x-default" href="{alt_de}">
  {robots}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}{og_image}">
  <meta property="og:locale" content="{locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#1e4034">
  <link rel="icon" href="/assets/images/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="/assets/images/favicon-16.png" sizes="16x16" type="image/png">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/css/styles.css">
</head>
'''


def render(lang, page_key, title, description, body, og_image=None, extra_head="", noindex=False):
    head = head_html(lang, page_key, title, description, og_image=og_image or "/assets/images/mantrailing-hero-1000.jpg", noindex=noindex)
    if extra_head:
        head = head.replace("</head>", extra_head + "\n</head>")
    header = header_html(lang, page_key)
    footer = footer_html(lang)
    script = '  <script src="/assets/js/main.js" defer></script>\n'
    return f'''{head}<body>
{header}  <main id="main">
{body}
  </main>
{footer}{script}</body>
</html>
'''


def local_business_jsonld(lang):
    name = "Mad Dogs Germany"
    description_de = "Dogwalker-Service, Hundesport- und Mantrailing-Training mit Chris Knittel in Niederkassel bei Köln/Bonn."
    description_en = "Dog walking, dog sport and mantrailing training with Chris Knittel in Niederkassel near Cologne/Bonn, Germany."
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "description": description_de if lang == "de" else description_en,
        "url": PAGES["home"][lang] and (SITE_URL.rstrip("/") + PAGES["home"][lang]),
        "image": SITE_URL + "/assets/images/logo-512.jpg",
        "telephone": "+49-173-3649143",
        "email": "info@mad-dogs-germany.de",
        "founder": "Chris Knittel",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Hauptstraße 72",
            "postalCode": "53859",
            "addressLocality": "Niederkassel",
            "addressCountry": "DE",
        },
        "sameAs": ["https://www.instagram.com/mad_dogs_germany/"],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "07:00",
            "closes": "18:00",
        }],
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{json_str}\n  </script>'


def write_page(lang, page_key, title, description, body_filename, og_image=None, noindex=False):
    content_path = CONTENT / lang / body_filename
    body = content_path.read_text(encoding="utf-8")
    extra_head = local_business_jsonld(lang) if page_key == "home" else ""
    html = render(lang, page_key, title, description, body, og_image=og_image, noindex=noindex, extra_head=extra_head)
    out_rel = PAGES[page_key][lang]
    out_dir = ROOT / out_rel.strip("/") if out_rel.strip("/") else ROOT
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote {out_dir / 'index.html'}")


# ---------------------------------------------------------------------------
# Seiteninhalte: (lang, key, title, description, content-fragment-datei)
# ---------------------------------------------------------------------------
PAGE_DEFS = [
    ("de", "home", "Mad Dogs Germany – Hundesport, Mantrailing & Dogwalker-Service in Niederkassel",
     "Professioneller Dogwalker-Service, Hundesport- und Mantrailing-Training mit Chris Knittel in Niederkassel bei Köln/Bonn. Struktur, Erfahrung und Vertrauen für Hunde mit Charakter.",
     "home.html"),
    ("de", "about", "Über uns – Chris Knittel | Mad Dogs Germany",
     "Seit 2014 im Hundesport aktiv: Turnierhundesport-Erfolge, Ausbildung zum Pet-/Man-Trail-Trainer, Diensthundeführer und Hundetrainer. Lerne Chris Knittel kennen.",
     "about.html"),
    ("de", "training", "Training: Hundesport, Mantrailing & Spürhunde | Mad Dogs Germany",
     "Turnierhundesport, Mantrailing (Man/Pet Trail) und Erfahrung aus dem Diensthundewesen: Auslastung für Kopf und Nase, für Hunde mit viel Energie.",
     "training.html"),
    ("de", "dogwalker", "Dogwalker-Service in Niederkassel | Mad Dogs Germany",
     "Professioneller Gassi-Service für anspruchsvolle Hunde mit viel Energie. Strukturierte Auslastung, klare Führung, kleine Gruppen bis 10 Hunde. Ab 20 €.",
     "dogwalker.html"),
    ("de", "shop", "Mad Dogs Shop & Reico Hundefutter | Mad Dogs Germany",
     "Halsbänder, Leinen, Trail-Zubehör, Bekleidung, Bücher und Kurse im Mad Dogs Shop – plus hochwertiges Reico Hundefutter über unseren Partnerlink.",
     "shop.html"),
    ("de", "testimonials", "Kundenstimmen | Mad Dogs Germany",
     "Echte Erfahrungsberichte unserer Kund:innen entstehen gerade. Du warst schon dabei? Teile gern deine Erfahrung mit Mad Dogs Germany.",
     "testimonials.html"),
    ("de", "contact", "Kontakt | Mad Dogs Germany",
     "Kontaktiere Chris Knittel von Mad Dogs Germany per Telefon, WhatsApp, E-Mail oder Formular – Niederkassel und Umgebung.",
     "contact.html"),
    ("de", "legal", "Impressum | Mad Dogs Germany", "Impressum von Mad Dogs Germany gemäß § 5 TMG.", "legal.html"),
    ("de", "privacy", "Datenschutzerklärung | Mad Dogs Germany", "Datenschutzerklärung von Mad Dogs Germany gemäß DSGVO.", "privacy.html"),

    ("en", "home", "Mad Dogs Germany – Dog Sports, Mantrailing & Dog Walking in Niederkassel",
     "Professional dog walking, dog sport and mantrailing training with Chris Knittel in Niederkassel near Cologne/Bonn, Germany. Structure, experience and trust for dogs with character.",
     "home.html"),
    ("en", "about", "About – Chris Knittel | Mad Dogs Germany",
     "Active in dog sports since 2014: competitive results, trained Pet/Man Trail instructor, service dog handler and certified dog trainer. Meet Chris Knittel.",
     "about.html"),
    ("en", "training", "Training: Dog Sports, Mantrailing & Detection Work | Mad Dogs Germany",
     "Competitive dog sport, mantrailing (Man/Pet Trail) and experience from professional service-dog handling: purposeful outlets for body and nose.",
     "training.html"),
    ("en", "dogwalker", "Dog Walking Service in Niederkassel | Mad Dogs Germany",
     "Professional dog walking for high-energy, strong-willed dogs. Structured outlets, calm and consistent guidance, small groups of up to 10 dogs. From €20.",
     "dogwalker.html"),
    ("en", "shop", "Mad Dogs Shop & Reico Dog Food | Mad Dogs Germany",
     "Collars, leashes, trail gear, apparel, books and courses in the Mad Dogs Shop – plus premium Reico dog food via our partner link.",
     "shop.html"),
    ("en", "testimonials", "Testimonials | Mad Dogs Germany",
     "Genuine customer testimonials are being collected right now. Already a client? Share your experience with Mad Dogs Germany.",
     "testimonials.html"),
    ("en", "contact", "Contact | Mad Dogs Germany",
     "Contact Chris Knittel of Mad Dogs Germany by phone, WhatsApp, email or contact form — Niederkassel and surrounding area.",
     "contact.html"),
    ("en", "legal", "Legal Notice | Mad Dogs Germany", "Legal notice (Impressum) of Mad Dogs Germany pursuant to German law (§ 5 TMG).", "legal.html"),
    ("en", "privacy", "Privacy Policy | Mad Dogs Germany", "Privacy policy of Mad Dogs Germany pursuant to the GDPR.", "privacy.html"),
]

if __name__ == "__main__":
    for lang, key, title, desc, fname in PAGE_DEFS:
        write_page(lang, key, title, desc, fname)

    # 404-Seite: Sonderfall, da sprachübergreifend (ein Error-Dokument für
    # die meisten Static-Hosts) und daher nicht Teil des PAGES-Registers.
    body_404 = (CONTENT / "de" / "404.html").read_text(encoding="utf-8")
    html_404 = f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>404 – Seite nicht gefunden | Mad Dogs Germany</title>
  <meta name="description" content="Die angeforderte Seite wurde nicht gefunden.">
  <meta name="robots" content="noindex,follow">
  <meta name="theme-color" content="#1e4034">
  <link rel="icon" href="/assets/images/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="/assets/images/favicon-16.png" sizes="16x16" type="image/png">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
{header_html("de", None)}  <main id="main">
{body_404}
  </main>
{footer_html("de")}  <script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
    (ROOT / "404.html").write_text(html_404, encoding="utf-8")
    print(f"wrote {ROOT / '404.html'}")

    # sitemap.xml mit hreflang-Alternates, aus PAGES abgeleitet (keine
    # manuelle Abschrift -> keine Inkonsistenzen zwischen Sitemap und Seiten).
    url_entries = []
    for key, paths in PAGES.items():
        for lang in ("de", "en"):
            loc = SITE_URL.rstrip("/") + paths[lang]
            alt_links = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL.rstrip("/") + paths[l]}"/>'
                for l in ("de", "en")
            )
            url_entries.append(f"  <url>\n    <loc>{loc}</loc>\n{alt_links}\n  </url>")
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(url_entries) + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"wrote {ROOT / 'sitemap.xml'}")

    print("\nFertig. Alle Kernseiten wurden generiert.")
