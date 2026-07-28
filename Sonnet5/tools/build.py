# -*- coding: utf-8 -*-
"""
Internes Autoren-Werkzeug für den Mad Dogs Germany Relaunch.
----------------------------------------------------------------------
KEIN Bestandteil der ausgelieferten Website. Dieses Skript erzeugt
ausschließlich statische .html-Dateien, robots.txt, sitemap.xml und
site.webmanifest. Das Ergebnis braucht keinerlei Build-Schritt, kein
Node, kein PHP — es kann 1:1 auf jeden Webspace hochgeladen werden.

Der Generator existiert nur, damit Header, Navigation und Footer über
alle Einzelseiten UND beide Sprachversionen (Deutsch/Englisch) hinweg
garantiert konsistent bleiben. Nach dem Lauf kann dieser gesamte
tools/-Ordner gelöscht werden, ohne dass die Website betroffen ist
(siehe README.md).

Aufruf:  python tools/build.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

SITE_NAME = "Mad Dogs Germany"
SITE_URL = "https://www.mad-dogs-germany.de"
PHONE_DISPLAY = "0173 3649143"
PHONE_E164 = "+491733649143"
WHATSAPP_URL = "https://wa.me/491733649143"
EMAIL = "info@mad-dogs-germany.de"
ADDRESS_STREET = "Hauptstraße 72"
ADDRESS_ZIP = "53859"
ADDRESS_CITY = "Niederkassel"
INSTAGRAM_URL = "https://www.instagram.com/mad_dogs_germany/"
INSTAGRAM_HANDLE = "@mad_dogs_germany"
SHOP_URL = "https://mad-dogs-germany.myspreadshop.de/"
REICO_URL = "https://reico-vital.com/de/vp/chrisknittel"

HOURS = {
    "de": "Mo\u2013Fr, 07:00\u201318:00 Uhr",
    "en": "Mon\u2013Fri, 7:00 AM\u20136:00 PM",
}

NEW_TAB = {
    "de": " (öffnet in einem neuen Tab)",
    "en": " (opens in a new tab)",
}

LANGS = ["de", "en"]
OTHER_LANG = {"de": "en", "en": "de"}

# ---------------------------------------------------------------------------
# Seiten-Schlüssel, URL-Pfade je Sprache, Navigations-Beschriftungen
# ---------------------------------------------------------------------------
PAGE_KEYS = [
    "home", "about", "training", "dogwalker", "shop",
    "testimonials", "contact", "legal", "privacy",
]

PATHS = {
    "home":         {"de": "/",                 "en": "/en/"},
    "about":        {"de": "/ueber-mich/",      "en": "/en/about/"},
    "training":     {"de": "/training/",        "en": "/en/training/"},
    "dogwalker":    {"de": "/dogwalker-service/", "en": "/en/dogwalker-service/"},
    "shop":         {"de": "/shop/",            "en": "/en/shop/"},
    "testimonials": {"de": "/kundenstimmen/",   "en": "/en/testimonials/"},
    "contact":      {"de": "/kontakt/",         "en": "/en/contact/"},
    "legal":        {"de": "/impressum/",       "en": "/en/legal-notice/"},
    "privacy":      {"de": "/datenschutz/",     "en": "/en/privacy/"},
}

NAV_ORDER = ["home", "about", "training", "dogwalker", "shop", "testimonials", "contact"]

NAV_LABELS = {
    "de": {
        "home": "Start", "about": "Über mich", "training": "Training",
        "dogwalker": "Dogwalking", "shop": "Shop",
        "testimonials": "Kundenstimmen", "contact": "Kontakt",
    },
    "en": {
        "home": "Home", "about": "About", "training": "Training",
        "dogwalker": "Dog Walking", "shop": "Shop",
        "testimonials": "Testimonials", "contact": "Contact",
    },
}

FOOTER_LEGAL_LABELS = {
    "de": {"legal": "Impressum", "privacy": "Datenschutz"},
    "en": {"legal": "Legal Notice", "privacy": "Privacy Policy"},
}

BREADCRUMB_LABELS = {
    "de": {
        "about": "Über mich", "training": "Training", "dogwalker": "Dogwalker-Service",
        "shop": "Shop", "testimonials": "Kundenstimmen", "contact": "Kontakt",
        "legal": "Impressum", "privacy": "Datenschutzerklärung",
    },
    "en": {
        "about": "About", "training": "Training", "dogwalker": "Dog Walking Service",
        "shop": "Shop", "testimonials": "Testimonials", "contact": "Contact",
        "legal": "Legal Notice", "privacy": "Privacy Policy",
    },
}

UI = {
    "de": {
        "skip_link": "Zum Hauptinhalt springen",
        "menu_open": "Menü öffnen",
        "menu_label": "Hauptnavigation",
        "footer_pages_label": "Seiten im Footer",
        "footer_pages_heading": "Seiten",
        "footer_contact_heading": "Kontakt",
        "footer_tagline": "Dogwalker-Service, Hundesport und Mantrailing rund um Niederkassel bei Köln/Bonn.",
        "footer_rights": "Alle Rechte vorbehalten.",
        "breadcrumb_home": "Start",
        "breadcrumb_label": "Breadcrumb",
        "whatsapp_aria": " (öffnet in einem neuen Tab)",
        "instagram_aria": "Instagram",
        "mail_aria": "E-Mail schreiben",
        "phone_aria": "Anrufen",
        "lang_switch_aria": "Sprache wechseln zu Englisch",
    },
    "en": {
        "skip_link": "Skip to main content",
        "menu_open": "Open menu",
        "menu_label": "Main navigation",
        "footer_pages_label": "Footer pages",
        "footer_pages_heading": "Pages",
        "footer_contact_heading": "Contact",
        "footer_tagline": "Dog walking, dog sports and mantrailing around Niederkassel near Cologne/Bonn, Germany.",
        "footer_rights": "All rights reserved.",
        "breadcrumb_home": "Home",
        "breadcrumb_label": "Breadcrumb",
        "whatsapp_aria": " (opens in a new tab)",
        "instagram_aria": "Instagram",
        "mail_aria": "Send an email",
        "phone_aria": "Call",
        "lang_switch_aria": "Switch language to German",
    },
}

# ---------------------------------------------------------------------------
# Icon-Set: konsistente, selbst gezeichnete Strichicons (24x24 Raster) —
# sprachunabhängig.
# ---------------------------------------------------------------------------
ICON_PATHS = {
    "check": '<polyline points="4 12 9 17 20 6"/>',
    "chevron-left": '<polyline points="15 6 9 12 15 18"/>',
    "chevron-right": '<polyline points="9 6 15 12 9 18"/>',
    "external": '<rect x="5" y="5" width="14" height="14" rx="2"/><path d="M9 15 19 5"/><path d="M13 5h6v6"/>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2"/><line x1="11" y1="18" x2="13" y2="18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3 7 12 13 21 7"/>',
    "map-pin": '<path d="M12 21s-7-6.5-7-11a7 7 0 0 1 14 0c0 4.5-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l4 2"/>',
    "chat": '<path d="M4 4h16v12H8l-4 4V4Z"/>',
    "camera": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7l1.5-3h5L16 7"/><circle cx="12" cy="13.5" r="3.5"/>',
    "paw": '<ellipse cx="12" cy="15.6" rx="4" ry="3.2"/><circle cx="6.3" cy="9.2" r="1.6"/><circle cx="9.8" cy="5.8" r="1.7"/><circle cx="14.2" cy="5.8" r="1.7"/><circle cx="17.7" cy="9.2" r="1.6"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>',
    "price-tag": '<path d="M3 11.5 11.5 3H19a2 2 0 0 1 2 2v7.5L12.5 21 3 11.5Z"/><circle cx="15.5" cy="8.5" r="1.5"/>',
    "leaf": '<path d="M5 19c8-1 12-6 13-13-8 1-13 6-13 13Z"/><path d="M5 19c2-3 4-5 8-8"/>',
    "shield": '<path d="M12 3l7 3v6c0 5-3.5 8-7 9-3.5-1-7-4-7-9V6l7-3Z"/>',
    "alert-circle": '<circle cx="12" cy="12" r="9"/><line x1="12" y1="7.5" x2="12" y2="13"/><circle cx="12" cy="16.3" r="0.9" fill="currentColor" stroke="none"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><polyline points="8 12.5 11 15.5 16 9"/>',
    "alert-triangle": '<path d="M12 4 21 20H3Z"/><line x1="12" y1="10" x2="12" y2="14.5"/><circle cx="12" cy="17" r="0.9" fill="currentColor" stroke="none"/>',
    "zoom": '<circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.2" y1="15.2" x2="20" y2="20"/><line x1="10.5" y1="7.5" x2="10.5" y2="13.5"/><line x1="7.5" y1="10.5" x2="13.5" y2="10.5"/>',
    "compass-nose": '<circle cx="12" cy="12" r="9"/><path d="m15 9-1.8 5.2L8 16l1.8-5.2Z"/>',
    "heart": '<path d="M12 20s-7.5-4.6-9.7-9A5.4 5.4 0 0 1 12 5.3 5.4 5.4 0 0 1 21.7 11c-2.2 4.4-9.7 9-9.7 9Z"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.6 2.7-6 6-6s6 2.4 6 6"/><circle cx="17.5" cy="9.5" r="2.4"/><path d="M15.8 14.2c2.5.4 4.2 2.4 4.2 5.8"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="16" rx="2"/><line x1="3.5" y1="10" x2="20.5" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><line x1="3" y1="12" x2="21" y2="12"/>',
}


def icon(name, css_class="icon", extra_attrs=""):
    path = ICON_PATHS[name]
    attrs = f' {extra_attrs}' if extra_attrs else ""
    return (
        f'<svg class="{css_class}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{attrs}>{path}</svg>'
    )


def external_note(lang):
    return f'<span class="visually-hidden">{NEW_TAB[lang]}</span>'


# ---------------------------------------------------------------------------
# <head>
# ---------------------------------------------------------------------------
def page_head(lang, page_key, title, description, og_image="/assets/images/og-image.jpg", extra_head="", noindex=False):
    path = PATHS[page_key][lang] if page_key else ("/404.html" if lang == "de" else "/404.html")
    canonical = SITE_URL + path
    other_lang = OTHER_LANG[lang]
    alt_href = SITE_URL + PATHS[page_key][other_lang] if page_key else None
    robots = '\n  <meta name="robots" content="noindex,follow">' if noindex else ""
    locale = "de_DE" if lang == "de" else "en_US"
    alt_locale = "en_US" if lang == "de" else "de_DE"

    hreflang_tags = ""
    if page_key:
        de_href = SITE_URL + PATHS[page_key]["de"]
        en_href = SITE_URL + PATHS[page_key]["en"]
        hreflang_tags = (
            f'\n  <link rel="alternate" hreflang="de" href="{de_href}">'
            f'\n  <link rel="alternate" hreflang="en" href="{en_href}">'
            f'\n  <link rel="alternate" hreflang="x-default" href="{de_href}">'
        )

    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <script>document.documentElement.classList.add('js');</script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">{hreflang_tags}{robots}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}{og_image}">
  <meta property="og:locale" content="{locale}">
  <meta property="og:locale:alternate" content="{alt_locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#fbfaf7" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#10171d" media="(prefers-color-scheme: dark)">
  <link rel="icon" href="/assets/images/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="/assets/images/favicon-16.png" sizes="16x16" type="image/png">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/css/styles.css">
{extra_head}</head>
"""


# ---------------------------------------------------------------------------
# Header / Navigation (inkl. Sprachumschalter)
# ---------------------------------------------------------------------------
def header_html(lang, active_key):
    t = UI[lang]
    items = []
    for key in NAV_ORDER:
        href = PATHS[key][lang]
        label = NAV_LABELS[lang][key]
        current = ' aria-current="page"' if key == active_key else ""
        items.append(f'          <li><a href="{href}"{current}>{label}</a></li>')
    items_html = "\n".join(items)

    other = OTHER_LANG[lang]
    lang_target = PATHS[active_key][other] if active_key else ("/en/" if lang == "de" else "/")
    lang_label = other.upper()
    home_href = PATHS["home"][lang]

    return f"""  <a class="skip-link" href="#main">{t['skip_link']}</a>
  <header class="site-header" data-site-header>
    <div class="container site-header__inner">
      <a class="brand" href="{home_href}">
        <picture>
          <source srcset="/assets/images/logo-128.webp" type="image/webp">
          <img class="brand__logo" src="/assets/images/logo-128.jpg" alt="" width="48" height="48" loading="eager" decoding="async">
        </picture>
        <span>Mad Dogs<span class="brand__sub">Germany</span></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" data-nav-toggle>
        <span class="visually-hidden">{t['menu_open']}</span>
        <span class="nav-toggle__icon" aria-hidden="true"></span>
      </button>
      <nav class="primary-nav" id="primary-navigation" aria-label="{t['menu_label']}" data-primary-nav data-open="false">
        <div class="primary-nav__list-wrap">
          <ul class="primary-nav__list">
{items_html}
          </ul>
          <div class="primary-nav__actions">
            <a class="lang-switch" href="{lang_target}" hreflang="{other}" lang="{other}" aria-label="{t['lang_switch_aria']}">{lang_label}</a>
            <a class="btn btn--accent btn--sm" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">
              {icon('chat', 'icon')} WhatsApp{external_note(lang)}
            </a>
          </div>
        </div>
      </nav>
    </div>
  </header>
"""


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
def footer_html(lang):
    t = UI[lang]
    nav_items = "\n".join(
        f'          <li><a href="{PATHS[key][lang]}">{NAV_LABELS[lang][key]}</a></li>' for key in NAV_ORDER
    )
    legal_labels = FOOTER_LEGAL_LABELS[lang]
    legal_href = PATHS["legal"][lang]
    privacy_href = PATHS["privacy"][lang]
    home_href = PATHS["home"][lang]

    return f"""  <footer class="site-footer">
    <div class="container site-footer__grid">
      <div class="site-footer__brand">
        <a class="brand" href="{home_href}">
          <picture>
            <source srcset="/assets/images/logo-128.webp" type="image/webp">
            <img class="brand__logo" src="/assets/images/logo-128.jpg" alt="" width="40" height="40" loading="lazy" decoding="async">
          </picture>
          <span>Mad Dogs<span class="brand__sub">Germany</span></span>
        </a>
        <p>{t['footer_tagline']}</p>
        <ul class="social-links">
          <li><a href="{INSTAGRAM_URL}" target="_blank" rel="noopener noreferrer" aria-label="{t['instagram_aria']}{t['whatsapp_aria']}">{icon('camera')}</a></li>
          <li><a href="mailto:{EMAIL}" aria-label="{t['mail_aria']}">{icon('mail')}</a></li>
          <li><a href="tel:{PHONE_E164}" aria-label="{t['phone_aria']}">{icon('phone')}</a></li>
        </ul>
      </div>
      <nav class="site-footer__nav" aria-label="{t['footer_pages_label']}">
        <h2>{t['footer_pages_heading']}</h2>
        <ul>
{nav_items}
        </ul>
      </nav>
      <div class="site-footer__contact">
        <h2>{t['footer_contact_heading']}</h2>
        <ul>
          <li>{icon('map-pin')} {ADDRESS_STREET}, {ADDRESS_ZIP} {ADDRESS_CITY}</li>
          <li>{icon('phone')} <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a></li>
          <li>{icon('mail')} <a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{icon('clock')} {HOURS[lang]}</li>
        </ul>
      </div>
    </div>
    <div class="container site-footer__bottom">
      <p>© <span data-year>2026</span> {SITE_NAME}. {t['footer_rights']}</p>
      <ul class="legal-links">
        <li><a href="{legal_href}">{legal_labels['legal']}</a></li>
        <li><a href="{privacy_href}">{legal_labels['privacy']}</a></li>
      </ul>
    </div>
  </footer>
"""


def breadcrumb_html(lang, active_key):
    if active_key == "home" or active_key not in BREADCRUMB_LABELS[lang]:
        return ""
    label = BREADCRUMB_LABELS[lang][active_key]
    home_href = PATHS["home"][lang]
    home_label = UI[lang]["breadcrumb_home"]
    return f"""    <nav class="breadcrumb container" aria-label="{UI[lang]['breadcrumb_label']}">
      <ol>
        <li><a href="{home_href}">{home_label}</a></li>
        <li aria-current="page">{label}</li>
      </ol>
    </nav>
"""


# ---------------------------------------------------------------------------
# Seiten-Gerüst
# ---------------------------------------------------------------------------
def render_page(lang, active_key, title, description, content, og_image=None, extra_head="", noindex=False, with_breadcrumb=True):
    head = page_head(lang, active_key, title, description, og_image=og_image or "/assets/images/og-image.jpg", extra_head=extra_head, noindex=noindex)
    header = header_html(lang, active_key)
    footer = footer_html(lang)
    crumb = breadcrumb_html(lang, active_key) if with_breadcrumb else ""
    return f"""{head}<body>
{header}  <main id="main">
{crumb}{content}
  </main>
{footer}  <script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def write_file(rel_path, content):
    out_path = ROOT / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  geschrieben: {rel_path}")


# ===========================================================================
# Seiteninhalte — Deutsch
# ===========================================================================

def home_content_de():
    return f"""    <section class="hero container two-col">
      <div>
        <p class="eyebrow">Niederkassel · Köln/Bonn</p>
        <h1 class="hero__title">Ruhige Führung, klare Aufgaben \u2013 für Hunde mit viel Temperament.</h1>
        <p class="lead hero__lead">
          Mad Dogs Germany ist das Ein-Mann-Angebot von Chris Knittel: professioneller
          Dogwalker-Service sowie Training in Hundesport, Mantrailing und Nasenarbeit
          rund um Niederkassel, Köln und Bonn \u2013 für Hunde, denen eine Runde um den
          Block nicht reicht.
        </p>
        <div class="button-row">
          <a class="btn btn--primary" href="/dogwalker-service/">Dogwalker-Service entdecken</a>
          <a class="btn btn--outline" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">
            {icon('chat')} Direkt per WhatsApp schreiben{external_note('de')}
          </a>
        </div>
        <div class="hero__stats">
          <div class="stat">
            <span class="stat__value">16 Jahre</span>
            <span class="stat__label">Erfahrung im Umgang mit Hunden</span>
          </div>
          <div class="stat">
            <span class="stat__value">70+</span>
            <span class="stat__label">Turnierstarts im Hundesport</span>
          </div>
          <div class="stat">
            <span class="stat__value">\u226410</span>
            <span class="stat__label">Hunde pro Gassi-Gruppe</span>
          </div>
          <div class="stat">
            <span class="stat__value">9 Monate</span>
            <span class="stat__label">Trail-Ausbildung in Österreich</span>
          </div>
        </div>
      </div>
      <div class="hero__media">
        <picture>
          <source type="image/webp" srcset="/assets/images/hero-home-420.webp 420w, /assets/images/hero-home-640.webp 640w, /assets/images/hero-home-960.webp 960w" sizes="(min-width: 56em) 22rem, 90vw">
          <img
            src="/assets/images/hero-home-640.jpg"
            srcset="/assets/images/hero-home-420.jpg 420w, /assets/images/hero-home-640.jpg 640w, /assets/images/hero-home-960.jpg 960w"
            sizes="(min-width: 56em) 22rem, 90vw"
            alt="Schwarz-brauner Schäferhund-Mix sitzt aufmerksam in einer Wiese voller Margeriten und blickt konzentriert nach oben."
            width="960" height="1200" loading="eager" fetchpriority="high" decoding="async">
        </picture>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Angebot</p>
          <h2>Ein Trainer, drei Wege zu einem ausgeglicheneren Hund</h2>
          <p class="lead">Ob Auslastung im Alltag oder gezieltes Training \u2013 jedes Angebot basiert auf derselben ruhigen, konsequenten Arbeitsweise.</p>
        </div>
        <div class="grid grid--cards">
          <a class="card" href="/dogwalker-service/">
            <span class="card__icon">{icon('paw')}</span>
            <h3>Dogwalker-Service</h3>
            <p>Strukturierte Spaziergänge in kleinen Gruppen für Hunde mit viel Energie \u2013 in Niederkassel und Umgebung.</p>
            <span class="card__link">Service ansehen \u2192</span>
          </a>
          <a class="card" href="/training/">
            <span class="card__icon">{icon('target')}</span>
            <h3>Hundesport &amp; Mantrailing</h3>
            <p>Turnierhundesport, Mantrailing und Erfahrung aus dem Diensthundewesen \u2013 Auslastung für Kopf und Nase.</p>
            <span class="card__link">Training entdecken \u2192</span>
          </a>
          <a class="card" href="/shop/">
            <span class="card__icon">{icon('price-tag')}</span>
            <h3>Mad Dogs Shop</h3>
            <p>Halsbänder, Leinen, Trail-Zubehör, Bekleidung, Bücher und Kurse für dich und deinen Hund.</p>
            <span class="card__link">Shop ansehen \u2192</span>
          </a>
          <a class="card" href="/shop/#reico">
            <span class="card__icon">{icon('leaf')}</span>
            <h3>Reico Hundefutter</h3>
            <p>Hochwertige Vitalstoff-Ernährung für Hunde \u2013 über meinen persönlichen Reico-Partnerlink.</p>
            <span class="card__link">Mehr erfahren \u2192</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Passt das zu deinem Hund?</p>
          <h2>Wenn eine normale Gassi-Runde nicht mehr reicht</h2>
          <p class="lead">Der Dogwalker-Service richtet sich besonders an Hunde mit viel Temperament \u2013 aber auch an alle, die verlässliche Betreuung mit klarer Linie suchen.</p>
          <ul class="icon-list icon-list--check">
            <li>{icon('check', 'icon-list__icon')}<span>Hunde mit viel Energie und eigenem Kopf</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Hunde, die an der Leine ziehen oder bei Begegnungen aufdrehen</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Halter:innen, die klare Regeln und echte Auslastung schätzen</span></li>
          </ul>
          <div class="button-row">
            <a class="btn btn--primary" href="/dogwalker-service/">Mehr zum Dogwalker-Service</a>
          </div>
        </div>
        <div class="hero__media">
          <picture>
            <source srcset="/assets/images/gallery-6.webp" type="image/webp">
            <img src="/assets/images/gallery-6.jpg" alt="Zottliger braun-schwarzer Mischlingshund mit offenem Fang an der Leine auf einem Schotterweg." width="384" height="512" loading="lazy" decoding="async">
          </picture>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container two-col two-col--reverse">
        <div class="hero__media">
          <picture>
            <source srcset="/assets/images/founder-384.webp" type="image/webp">
            <img src="/assets/images/founder-384.jpg" alt="Chris Knittel lächelt in die Kamera und hält seinen Malinois im Arm, der glücklich die Zunge heraushängen lässt." width="384" height="512" loading="lazy" decoding="async">
          </picture>
        </div>
        <div>
          <p class="eyebrow">Wer steckt dahinter?</p>
          <h2>Chris Knittel \u2013 seit 2014 im Hundesport zu Hause</h2>
          <p class="lead">
            Turniererfahrung, eine Ausbildung zum Pet-/Man-Trail-Trainer in Österreich,
            der Alltag als Diensthundeführer und 1,5 Jahre in einer der größten Kölner
            Hundetagesstätten \u2013 diese Mischung prägt jede Trainingsstunde und jeden
            Spaziergang.
          </p>
          <div class="button-row">
            <a class="btn btn--outline" href="/ueber-mich/">Mehr über mich \u2192</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Kontakt</p>
          <h2>Lass uns über deinen Hund sprechen</h2>
          <p class="lead">Ob Frage zum Training oder Anfrage für den Dogwalker-Service: Melde dich \u2013 am schnellsten per WhatsApp oder Telefon.</p>
          <ul class="info-list">
            <li class="info-list__item">
              <span class="info-list__icon">{icon('map-pin')}</span>
              <span>{ADDRESS_CITY} und Umgebung (Köln/Bonn)</span>
            </li>
            <li class="info-list__item">
              <span class="info-list__icon">{icon('clock')}</span>
              <span>{HOURS['de']}</span>
            </li>
            <li class="info-list__item">
              <span class="info-list__icon">{icon('phone')}</span>
              <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a>
            </li>
          </ul>
          <div class="button-row">
            <a class="btn btn--accent" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">WhatsApp schreiben{external_note('de')}</a>
            <a class="btn btn--outline" href="/kontakt/">Zum Kontaktformular</a>
          </div>
        </div>
        <figure class="badge-figure">
          <picture>
            <source srcset="/assets/images/logo-256.webp" type="image/webp">
            <img src="/assets/images/logo-256.jpg" alt="" width="180" height="180" loading="lazy" decoding="async">
          </picture>
          <figcaption>Mad Dogs Germany \u2013 Est. 2023</figcaption>
        </figure>
      </div>
    </section>
"""


def about_content_de():
    return f"""    <section class="container two-col">
      <div class="hero__media">
        <picture>
          <source srcset="/assets/images/founder-384.webp" type="image/webp">
          <img src="/assets/images/founder-384.jpg" alt="Chris Knittel lächelt in die Kamera und hält seinen Malinois im Arm, der glücklich die Zunge heraushängen lässt, im Hintergrund blauer Himmel." width="384" height="512" loading="eager" fetchpriority="high" decoding="async">
        </picture>
      </div>
      <div>
        <p class="eyebrow">Über mich</p>
        <h1>Chris Knittel \u2013 Hundetrainer, Dogwalker &amp; Diensthundeführer</h1>
        <div class="prose">
          <p>
            Mad Dogs Germany ist kein Unternehmen mit Personalabteilung, sondern eine
            Person mit einer klaren Haltung: Ich begleite seit 2014 Hunde im
            Turnierhundesport, arbeite als Diensthundeführer im zivilen und
            militärischen Sicherheitsdienst und habe mich zusätzlich zum
            Pet-/Man-Trail-Trainer sowie zum Hundetrainer ausbilden lassen.
          </p>
          <p>
            Diese Mischung aus Leistungssport, sicherheitsdienstlicher Praxis und
            pädagogischer Ausbildung prägt meine Arbeitsweise: ruhig, konsequent und
            mit einem Blick für Hunde, die etwas mehr Führung brauchen \u2013 ob im
            Wettkampf, im Training oder auf dem ganz normalen Spaziergang.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Werdegang</p>
          <h2>Stationen im Hundesport</h2>
        </div>
        <ol class="timeline">
          <li class="timeline__item">
            <p class="timeline__year">seit 2014</p>
            <h3>Einstieg in den Turnierhundesport</h3>
            <p>Aktiver Turnierhundesportler mit Teilnahmen bei SWHV-, VDH-DM- und DHV-DM-Wettbewerben sowie über 70 Turnierstarts im THS.</p>
          </li>
          <li class="timeline__item">
            <p class="timeline__year">2017</p>
            <h3>Vizemeister Deutsche Meisterschaft GL 2000</h3>
            <p>Ausgezeichnet mit dem Ehrenpreis der Stadt Metzingen für besondere Leistungen im Hundesport.</p>
          </li>
          <li class="timeline__item">
            <p class="timeline__year">2018</p>
            <h3>3. Platz SWHV CSC &amp; 3. Platz SWHV GL 2000m</h3>
            <p>Erneut ausgezeichnet mit dem Ehrenpreis der Stadt Metzingen für besondere Leistungen im Hundesport.</p>
          </li>
          <li class="timeline__item">
            <p class="timeline__year">laufend</p>
            <h3>Schutzdiensthelfer im Verein</h3>
            <p>Unterstützung im vereinsinternen Schutzdienst sowie Erfahrung im Umgang mit Angst- und Problemhunden.</p>
          </li>
        </ol>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Ausbildung &amp; Qualifikation</p>
          <h2>Fundiert ausgebildet, praktisch erprobt</h2>
        </div>
        <div class="grid grid--cards">
          <div class="card">
            <span class="card__icon">{icon('compass-nose')}</span>
            <h3>Pet-/Man-Trail-Trainer</h3>
            <p>Neunmonatige Ausbildung bei Pet Trailer in Österreich \u2013 die fachliche Basis für das Mantrailing-Training bei Mad Dogs Germany.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('shield')}</span>
            <h3>Diensthundeführer</h3>
            <p>Tätig im zivilen und militärischen Sicherheitsdienst \u2013 praktische Erfahrung in Führung, Gehorsam und Nasenarbeit unter realen Bedingungen.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('users')}</span>
            <h3>Hundetrainer-Ausbildung</h3>
            <p>Ausbildung zum Hundetrainer bei Kynologisch, ergänzt durch Kenntnisse im Umgang mit Angst- und Problemhunden.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('paw')}</span>
            <h3>Dogwalker mit Rudel-Erfahrung</h3>
            <p>1,5 Jahre Mitarbeit in einer der größten Hundetagesstätten Kölns \u2013 Betreuung und Gassiführung im Großrudel.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Haltung</p>
          <h2>Wie ich arbeite</h2>
        </div>
        <div class="grid grid--cards" style="grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));">
          <div class="card">
            <span class="card__icon">{icon('clock')}</span>
            <h3>Ruhe vor Tempo</h3>
            <p>Ein Hund lernt am schnellsten, wenn er nicht unter Druck steht. Ich arbeite in dem Tempo, das der jeweilige Hund braucht \u2013 nicht in dem, das am schnellsten aussieht.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('heart')}</span>
            <h3>Vertrauen statt Zwang</h3>
            <p>Klare Regeln ja, harte Methoden nein. Führung entsteht aus Konsequenz und Verlässlichkeit \u2013 nicht aus Druckmitteln.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('target')}</span>
            <h3>Kopf und Nase mitfordern</h3>
            <p>Reine Bewegung ermüdet selten nachhaltig. Aufgaben für die Nase und den Kopf sorgen für echte, langanhaltende Auslastung.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container text-center max-w-prose mx-auto">
        <p class="eyebrow">Kontakt</p>
        <h2>Interessiert an Training oder Dogwalking?</h2>
        <p class="lead" style="margin-inline:auto;">Melde dich \u2013 wir besprechen gemeinsam, was zu dir und deinem Hund passt.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--accent" href="/kontakt/">Jetzt kontaktieren</a>
          <a class="btn btn--outline" href="/training/">Trainingsangebote ansehen</a>
        </div>
      </div>
    </section>
"""


def training_content_de():
    return f"""    <section class="container">
      <p class="eyebrow">Training</p>
      <h1>Hundesport, Mantrailing &amp; Spürhunde-Erfahrung</h1>
      <p class="lead max-w-prose">
        Drei Trainingswelten, eine Grundidee: Hunde brauchen Aufgaben für Kopf und
        Nase \u2013 nicht nur Bewegung. Alle drei Bereiche bauen auf meiner Erfahrung aus
        Turniersport, Trail-Ausbildung und Diensthundewesen auf.
      </p>
      <ul class="tag-list" aria-label="Direkt zu einem Bereich springen" style="margin-block-start: var(--space-l);">
        <li><a class="tag" href="#hundesport">{icon('target', 'icon-inline')} Hundesport</a></li>
        <li><a class="tag" href="#mantrailing">{icon('compass-nose', 'icon-inline')} Mantrailing</a></li>
        <li><a class="tag" href="#spuerhunde">{icon('shield', 'icon-inline')} Spürhunde</a></li>
      </ul>
    </section>

    <section class="section" id="hundesport">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Turnierhundesport</p>
          <h2>Hundesport</h2>
          <div class="prose">
            <p>
              Turnierhundesport (THS) verbindet Gehorsam, Geschicklichkeit und
              Teamarbeit zwischen Hund und Halter:in in einem sportlichen,
              wettkampforientierten Rahmen. Ich bin seit 2014 selbst aktiver
              Turnierhundesportler \u2013 mit Teilnahmen bei SWHV-, VDH-DM- und
              DHV-DM-Wettbewerben, über 70 Turnierstarts sowie mehreren
              Podiumsplätzen und Ehrenpreisen der Stadt Metzingen.
            </p>
            <p>
              Diese Wettkampferfahrung fließt direkt ins Training ein: sauberer
              Grundgehorsam, Teamgeist und die Freude an gemeinsamer Leistung stehen
              im Mittelpunkt \u2013 unabhängig davon, ob du selbst turnieren möchtest
              oder deinem Hund einfach eine sportliche Aufgabe geben willst.
            </p>
          </div>
        </div>
        <figure class="badge-figure">
          <picture>
            <source srcset="/assets/images/logo-256.webp" type="image/webp">
            <img src="/assets/images/logo-256.jpg" alt="" width="180" height="180" loading="lazy" decoding="async">
          </picture>
          <figcaption>Seit 2014 aktiv im Turnierhundesport \u2013 über 70 Starts, mehrere Podiumsplätze.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--alt" id="mantrailing">
      <div class="container">
        <p class="eyebrow">Nasenarbeit</p>
        <h2>Mantrailing (Man/Pet Trail)</h2>
        <div class="prose max-w-prose">
          <p>
            Beim Mantrailing folgt der Hund der individuellen Geruchsspur eines
            bestimmten Menschen (Man Trail) oder Tieres (Pet Trail) \u2013 nicht der
            allgemeinen Fährte am Boden, sondern der einzigartigen Geruchsmischung
            einer Person. Der Hund arbeitet dabei weitgehend selbstständig, während
            du lernst, seine Körpersprache zu lesen und ihm zu vertrauen.
          </p>
          <p>
            Gerade für Hunde mit viel Energie und Grips ist das eine ideale Aufgabe:
            konzentrierte Nasenarbeit ermüdet oft stärker als reine Bewegung und
            stärkt gleichzeitig die Bindung zwischen Mensch und Hund. Grundlage des
            Trainings ist meine neunmonatige Ausbildung zum Pet-/Man-Trail-Trainer
            bei Pet Trailer in Österreich.
          </p>
        </div>
        <div class="callout" style="margin-block-start: var(--space-l); margin-block-end: 0;">
          {icon('compass-nose')}
          <p>Einsteiger:innen sind ausdrücklich willkommen \u2013 Mantrailing lässt sich unabhängig von Rasse, Alter oder Vorerfahrung aufbauen.</p>
        </div>
      </div>
    </section>

    <section class="section" id="spuerhunde">
      <div class="container two-col two-col--reverse">
        <div class="hero__media">
          <picture>
            <source srcset="/assets/images/gallery-2.webp" type="image/webp">
            <img src="/assets/images/gallery-2.jpg" alt="Schwarzer Malinois mit taktischem Geschirr liegt aufmerksam im Gras vor einem Zelt." width="384" height="512" loading="lazy" decoding="async">
          </picture>
        </div>
        <div>
          <p class="eyebrow">Erfahrung aus dem Diensthundewesen</p>
          <h2>Spürhunde</h2>
          <div class="prose">
            <p>
              Über meine Tätigkeit als Diensthundeführer im zivilen und militärischen
              Sicherheitsdienst bringe ich zusätzliche Erfahrung in der
              professionellen Spürhundearbeit mit \u2013 etwa im gezielten Aufbau von
              Anzeigeverhalten und im ruhigen, kontrollierten Einsatz der Hundenase
              unter realen Bedingungen.
            </p>
            <p>
              Ein eigenständiges Spürhunde-Kursangebot befindet sich aktuell im
              Aufbau. Wenn du Interesse an individueller Beratung in diesem Bereich
              hast, sprich mich gerne direkt an.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container text-center max-w-prose mx-auto">
        <h2>Welcher Bereich passt zu deinem Hund?</h2>
        <p class="lead" style="margin-inline:auto;">Erzähl mir kurz von deinem Hund \u2013 ich empfehle dir gerne den passenden Einstieg.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--accent" href="/kontakt/">Trainingsanfrage stellen</a>
        </div>
      </div>
    </section>
"""


GALLERY_ZOOM_LABEL = {"de": "\u2013 Bild vergrößern", "en": "\u2013 view larger image"}


def _gallery_item(lang, num, caption):
    aria_label = f"{caption} {GALLERY_ZOOM_LABEL[lang]}"
    return f"""          <li>
            <a class="gallery__link" href="/assets/images/gallery-{num}.jpg" data-lightbox-trigger data-caption="{caption}" aria-label="{aria_label}">
              <picture>
                <source srcset="/assets/images/gallery-{num}.webp" type="image/webp">
                <img src="/assets/images/gallery-{num}.jpg" alt="" width="384" height="512" loading="lazy" decoding="async">
              </picture>
              <span class="gallery__zoom">{icon('zoom')}</span>
            </a>
          </li>"""


GALLERY_CAPTIONS_DE = [
    (1, "Kleiner schwarz-brauner Terrier-Mix steht mit heraushängender Zunge auf einer Wiese"),
    (2, "Schwarzer Malinois mit taktischem Geschirr liegt entspannt im Gras vor einem Zelt"),
    (3, "Golden Retriever blickt neugierig nach oben, an roter Leine auf einem Weg"),
    (4, "Schäferhund-Mix liegt entspannt auf dem Beifahrersitz eines Autos"),
    (5, "Deutscher Schäferhund-Mix mit Maulkorb sitzt aufmerksam an der Leine"),
    (6, "Zottliger Mischlingshund mit offenem Fang an der Leine auf einem Schotterweg"),
    (7, "Weißer, flauschiger Hund blickt nah in die Kamera vor bewölktem Himmel"),
]

GALLERY_CAPTIONS_EN = [
    (1, "Small black-and-tan terrier mix standing in a meadow with its tongue out"),
    (2, "Black Malinois wearing a tactical harness, resting calmly in the grass in front of a tent"),
    (3, "Golden Retriever looking up curiously, on a red leash on a path"),
    (4, "Shepherd mix resting comfortably in the passenger seat of a car"),
    (5, "German Shepherd mix wearing a muzzle, sitting attentively on a leash"),
    (6, "Shaggy mixed-breed dog with its mouth open, on a leash on a gravel path"),
    (7, "White, fluffy dog looking closely into the camera against a cloudy sky"),
]


def dogwalker_content_de():
    gallery_items = "\n".join(_gallery_item("de", num, cap) for num, cap in GALLERY_CAPTIONS_DE)

    return f"""    <section class="container two-col">
      <div>
        <p class="eyebrow">Dogwalker-Service Niederkassel</p>
        <h1>Professioneller Gassi-Service \u2013 auch für anspruchsvolle Hunde</h1>
        <p class="lead">
          Du hast einen Hund mit viel Energie, eigenem Kopf oder starkem Charakter?
          Mad Dogs bietet mehr als einen Spaziergang: strukturierte Auslastung, klare
          Führung und individuelle Betreuung.
        </p>
        <div class="button-row">
          <a class="btn btn--accent" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">
            {icon('chat')} Per WhatsApp Kontakt aufnehmen{external_note('de')}
          </a>
          <a class="btn btn--outline" href="tel:{PHONE_E164}">{PHONE_DISPLAY} anrufen</a>
        </div>
      </div>
      <figure class="badge-figure">
        <picture>
          <source srcset="/assets/images/badge-dogwalker-260.webp" type="image/webp">
          <img src="/assets/images/badge-dogwalker-260.png" alt="Rundabzeichen „Dogwalker NDK" mit dem Mad-Dogs-Germany-Logo im Zentrum." width="220" height="220" loading="eager" fetchpriority="high" decoding="async">
        </picture>
      </figure>
    </section>

    <section class="section">
      <div class="container two-col">
        <div>
          <h2>Ideal für Hunde, die \u2026</h2>
          <ul class="icon-list icon-list--check">
            <li>{icon('check', 'icon-list__icon')}<span>viel Energie haben</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>an der Leine ziehen</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>bei Begegnungen aufdrehen</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>klare Regeln und Auslastung brauchen</span></li>
          </ul>
        </div>
        <div>
          <h2>Was dein Hund bei mir bekommt</h2>
          <ul class="icon-list icon-list--check">
            <li>{icon('check', 'icon-list__icon')}<span>Ruhige, konsequente Führung</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Gezielte Auslastung für Körper &amp; Kopf</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Spaziergänge in kleinen, passenden Gruppen mit bis zu 10 Hunden</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Soziales Training und Reizkontrolle unterwegs</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Zuverlässigkeit &amp; Erfahrung im Umgang mit „starken Typen"</span></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Hintergrund</p>
          <h2>16 Jahre Erfahrung im Umgang mit Hunden</h2>
        </div>
        <div class="prose max-w-prose">
          <p>
            Seit 16 Jahren führe ich Hunde verschiedenster Rassen im Hundesport. In
            einer der größten Hundetagesstätten Kölns habe ich 1,5 Jahre lang
            gearbeitet und dort Hunde im Großrudel betreut und Gassi geführt. Zudem
            bin ich als Diensthundeführer tätig und habe meine
            Hundetrainer-Ausbildung durchlaufen.
          </p>
          <p><strong>Auslastung mit Kopf, nicht nur mit Kilometern.</strong></p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Preise</p>
          <h2>Transparent &amp; fair</h2>
        </div>
        <div class="price-table-wrap">
          <table class="price-table">
            <caption>Preise Dogwalker-Service (Gruppenspaziergang)</caption>
            <thead>
              <tr>
                <th scope="col">Dauer</th>
                <th scope="col">Preis</th>
              </tr>
            </thead>
            <tbody>
              <tr><th scope="row">1 Stunde</th><td>20 €</td></tr>
              <tr><th scope="row">1,5 Stunden</th><td>25 €</td></tr>
              <tr><th scope="row">2 Stunden</th><td>30 €</td></tr>
            </tbody>
          </table>
        </div>
        <p class="price-note">{icon('map-pin')} Einsatzgebiet: {ADDRESS_CITY} und Umgebung. Terminabsprache bevorzugt per WhatsApp oder Anruf.</p>
        <p class="value-badge" style="margin-block-start: var(--space-m);">{icon('check-circle')} Erstes Kennenlerngespräch ohne Verpflichtung</p>
        <div class="button-row">
          <a class="btn btn--accent" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">
            {icon('chat')} Kennenlern-Proberunde vereinbaren{external_note('de')}
          </a>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Galerie</p>
          <h2>Unterwegs mit Mad Dogs</h2>
          <p class="lead">Ein paar Eindrücke von echten Gassi-Gruppen. Bild anklicken für die Großansicht.</p>
        </div>
        <ul class="gallery">
{gallery_items}
        </ul>
      </div>
    </section>

    <dialog class="lightbox" data-lightbox aria-label="Bildergalerie Großansicht">
      <div class="lightbox__inner">
        <button class="lightbox__close" type="button" data-lightbox-close aria-label="Großansicht schließen">&times;</button>
        <button class="lightbox__nav lightbox__nav--prev" type="button" data-lightbox-prev aria-label="Vorheriges Bild">{icon('chevron-left')}</button>
        <button class="lightbox__nav lightbox__nav--next" type="button" data-lightbox-next aria-label="Nächstes Bild">{icon('chevron-right')}</button>
        <img class="lightbox__image" data-lightbox-image src="" alt="">
        <p class="lightbox__caption" data-lightbox-caption></p>
      </div>
    </dialog>
"""


def shop_content_de():
    categories = [
        "Halsbänder", "Leinen", "European Pet Pharmacy", "Non Stop Dogwear",
        "Trail-Zubehör", "Mäntel &amp; Jacken", "Bücher", "Sonstiges", "Kurse",
    ]
    tags = "\n".join(
        f'          <li class="tag">{icon("price-tag", "icon-inline")} {cat}</li>' for cat in categories
    )
    return f"""    <section class="container">
      <p class="eyebrow">Mad Dogs Shop</p>
      <h1>Ausrüstung für dich und deinen Hund</h1>
      <p class="lead max-w-prose">
        Vom Halsband bis zum Trail-Zubehör: Der Mad Dogs Shop läuft über meinen
        externen Shop-Partner. Ein Klick auf „Zum Shop" öffnet ihn in einem neuen
        Tab \u2013 dort gilt die Datenschutzerklärung des Shop-Betreibers.
      </p>
      <ul class="tag-list" style="margin-block-start: var(--space-l);">
{tags}
      </ul>
      <div class="button-row">
        <a class="btn btn--primary" href="{SHOP_URL}" target="_blank" rel="noopener noreferrer">
          Zum Mad Dogs Shop{external_note('de')}
          {icon('external')}
        </a>
      </div>
    </section>

    <section class="section section--alt" id="reico">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Ernährung</p>
          <h2>Reico Hundefutter</h2>
          <p class="lead">
            Hochwertige Vitalstoff-Ernährung nach dem Reico-Konzept \u2013 über meinen
            persönlichen Partnerlink. Auch hier gilt: Der Link führt auf das Angebot
            des Anbieters, inklusive dessen eigener Datenschutzerklärung.
          </p>
          <div class="button-row">
            <a class="btn btn--primary" href="{REICO_URL}" target="_blank" rel="noopener noreferrer">
              Zur Reico-Partnerseite{external_note('de')}
              {icon('external')}
            </a>
          </div>
        </div>
        <div class="card" style="align-self:center;">
          <span class="card__icon">{icon('leaf')}</span>
          <h3>Vitalstoff-Konzept</h3>
          <p>Ergänzungsfutter und Rezepturen, die ich meinen eigenen Hunden genauso gebe \u2013 daher die persönliche Empfehlung.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container text-center max-w-prose mx-auto">
        <h2>Fragen zu Produkten oder Bestellungen?</h2>
        <p class="lead" style="margin-inline:auto;">Bestellungen, Versand und Rückgaben laufen direkt über den jeweiligen Shop-Anbieter. Bei allgemeinen Fragen erreichst du mich trotzdem gerne direkt.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--outline" href="/kontakt/">Kontakt aufnehmen</a>
        </div>
      </div>
    </section>
"""


def testimonials_content_de():
    return f"""    <section class="container">
      <p class="eyebrow">Kundenstimmen</p>
      <h1>Das sagen meine Kund:innen</h1>
      <div class="empty-state">
        <span class="empty-state__icon">{icon('chat', 'icon', 'style="width:100%;height:100%;"')}</span>
        <h2>Hier entstehen bald echte Erfahrungsberichte</h2>
        <p>
          Ich zeige an dieser Stelle bewusst keine erfundenen Bewertungen. Sobald mir
          Kund:innen ihr Einverständnis geben, veröffentliche ich hier echte Stimmen
          zum Dogwalker-Service und Training.
        </p>
        <p>Warst du schon mit deinem Hund dabei? Ich freue mich über dein Feedback.</p>
        <a class="btn btn--primary" href="/kontakt/">Erfahrung teilen</a>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container text-center max-w-prose mx-auto">
        <h2>Auch auf Instagram unterwegs</h2>
        <p class="lead" style="margin-inline:auto;">Einblicke in Training und Alltag gibt es auch auf Instagram.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--outline" href="{INSTAGRAM_URL}" target="_blank" rel="noopener noreferrer">
            {icon('camera')} {INSTAGRAM_HANDLE} auf Instagram{external_note('de')}
          </a>
        </div>
      </div>
    </section>
"""


def contact_content_de():
    return f"""    <section class="container two-col">
      <div>
        <p class="eyebrow">Kontakt</p>
        <h1>Sprich mit mir über deinen Hund</h1>
        <p class="lead">
          Am schnellsten erreichst du mich per WhatsApp oder Telefon. Alternativ
          kannst du auch das Formular nutzen \u2013 ich melde mich so schnell wie
          möglich zurück.
        </p>
        <ul class="info-list">
          <li class="info-list__item">
            <span class="info-list__icon">{icon('phone')}</span>
            <div>
              <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a><br>
              <a href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">auch per WhatsApp{external_note('de')}</a>
            </div>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">{icon('mail')}</span>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">{icon('map-pin')}</span>
            <address style="font-style:normal;">{ADDRESS_STREET}, {ADDRESS_ZIP} {ADDRESS_CITY}</address>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">{icon('clock')}</span>
            <span>{HOURS['de']}</span>
          </li>
        </ul>
      </div>

      <form class="form" data-contact-form action="mailto:{EMAIL}" method="get" novalidate>
        <div class="form-field">
          <label for="name">Name *</label>
          <input id="name" name="name" type="text" autocomplete="name" required aria-describedby="name-error">
          <p class="form-error" id="name-error" role="alert"></p>
        </div>
        <div class="form-field">
          <label for="email">E-Mail *</label>
          <input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-error">
          <p class="form-error" id="email-error" role="alert"></p>
        </div>
        <div class="form-field">
          <label for="message">Nachricht *</label>
          <textarea id="message" name="message" required aria-describedby="message-error"></textarea>
          <p class="form-error" id="message-error" role="alert"></p>
        </div>
        <div class="form-field form-field--hp">
          <label for="website">Bitte freilassen</label>
          <input id="website" name="website" type="text" tabindex="-1" autocomplete="off">
        </div>
        <div class="form-field form-field--checkbox">
          <input id="consent" name="consent" type="checkbox" required aria-describedby="consent-error">
          <label for="consent">
            Ich bin damit einverstanden, dass meine Angaben zur Bearbeitung meiner
            Anfrage genutzt werden. Ich kann meine Einwilligung jederzeit
            widerrufen. Details in der <a href="/datenschutz/">Datenschutzerklärung</a>. *
          </label>
        </div>
        <p class="form-error" id="consent-error" role="alert"></p>
        <p class="required-note">* Pflichtfeld</p>
        <button class="btn btn--primary btn--block" type="submit">Nachricht senden</button>
        <p class="form-status" role="status" aria-live="polite" data-form-status></p>
        <p class="text-small text-soft">
          Hinweis: Diese Website versendet Formulardaten ohne eigenen Server direkt
          über dein E-Mail-Programm. Öffnet sich nichts, schreib mir gerne direkt an
          <a href="mailto:{EMAIL}">{EMAIL}</a>.
        </p>
      </form>
    </section>
"""


def legal_content_de():
    return f"""    <section class="container max-w-prose">
      <h1>Impressum</h1>
      <div class="callout">
        {icon('alert-circle')}
        <div>
          <p><strong>Hinweis zur Neugestaltung:</strong> Dieser Text wurde im Rahmen des Relaunchs auf Basis der zuvor öffentlich einsehbaren Angaben neu erstellt.</p>
          <p>Bitte vor Veröffentlichung von Chris Knittel bzw. einer rechtskundigen Person prüfen lassen \u2013 insbesondere Anschrift und Umsatzsteuer-ID.</p>
        </div>
      </div>

      <div class="prose">
        <h2>Angaben gemäß § 5 TMG</h2>
        <p>
          Mad Dogs Germany<br>
          Chris Knittel<br>
          {ADDRESS_STREET}<br>
          {ADDRESS_ZIP} {ADDRESS_CITY}<br>
          Deutschland
        </p>

        <h2>Kontakt</h2>
        <p>
          Telefon: <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a><br>
          E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>

        <h2>Umsatzsteuer-ID</h2>
        <p class="text-soft">
          Sofern vorhanden, wird hier die Umsatzsteuer-Identifikationsnummer gemäß
          § 27a Umsatzsteuergesetz ergänzt. Greift stattdessen die
          Kleinunternehmerregelung nach § 19 UStG, wird dies an dieser Stelle kurz
          vermerkt.
        </p>

        <h2>Verantwortlich für den Inhalt gemäß § 18 Abs. 2 MStV</h2>
        <p>Chris Knittel (Anschrift wie oben)</p>

        <h2>EU-Streitschlichtung</h2>
        <p>
          Die Europäische Kommission stellt eine Plattform zur
          Online-Streitbeilegung (OS) bereit, die du unter
          <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener noreferrer">ec.europa.eu/consumers/odr{external_note('de')}{icon('external', 'icon-inline')}</a>
          findest. Ich bin nicht verpflichtet und grundsätzlich nicht bereit, an
          Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle
          teilzunehmen.
        </p>

        <h2>Social-Media-Präsenz</h2>
        <p>
          Dieses Impressum gilt auch für die Social-Media-Präsenz:
          <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener noreferrer">instagram.com/mad_dogs_germany{external_note('de')}{icon('external', 'icon-inline')}</a>
        </p>

        <h2>Haftung für Inhalte</h2>
        <p>
          Die Inhalte dieser Website wurden mit größtmöglicher Sorgfalt erstellt.
          Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann
          jedoch keine Gewähr übernommen werden. Als Diensteanbieter bin ich gemäß
          § 7 Abs. 1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen
          Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG bin ich als Diensteanbieter
          jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde
          Informationen zu überwachen oder nach Umständen zu forschen, die auf eine
          rechtswidrige Tätigkeit hinweisen.
        </p>

        <h2>Haftung für Links</h2>
        <p>
          Dieses Angebot enthält Links zu externen Websites Dritter (u. a. Shop und
          Reico-Partnerseite), auf deren Inhalte ich keinen Einfluss habe. Deshalb
          kann ich für diese fremden Inhalte auch keine Gewähr übernehmen. Für die
          Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder
          Betreiber der Seiten verantwortlich.
        </p>

        <h2>Urheberrecht</h2>
        <p>
          Die durch den Seitenbetreiber erstellten Inhalte und Werke auf diesen
          Seiten unterliegen dem deutschen Urheberrecht. Beiträge Dritter sind als
          solche gekennzeichnet. Die Vervielfältigung, Bearbeitung, Verbreitung und
          jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen
          der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.
        </p>
      </div>
    </section>
"""


def privacy_content_de():
    return f"""    <section class="container max-w-prose">
      <h1>Datenschutzerklärung</h1>
      <div class="callout">
        {icon('alert-circle')}
        <div>
          <p><strong>Hinweis zur Neugestaltung:</strong> Diese Erklärung wurde bewusst schlank und auf die tatsächlich eingesetzten Funktionen zugeschnitten neu verfasst (keine Cookies, kein Tracking, keine eingebetteten Drittinhalte).</p>
          <p>Bitte vor Veröffentlichung von einer rechtskundigen Person prüfen lassen.</p>
        </div>
      </div>

      <div class="prose">
        <h2>Verantwortlicher</h2>
        <p>
          Chris Knittel<br>
          {ADDRESS_STREET}, {ADDRESS_ZIP} {ADDRESS_CITY}<br>
          E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>

        <h2>Auf einen Blick</h2>
        <p>Diese Website verzichtet bewusst auf:</p>
        <ul>
          <li>Cookies zu Analyse- oder Marketingzwecken</li>
          <li>Externe Schriftarten (z. B. Google Fonts) \u2013 verwendet werden ausschließlich auf deinem Gerät bereits vorhandene Systemschriften</li>
          <li>Eingebettete Social-Media-Widgets oder Landkarten Dritter</li>
        </ul>
        <p>
          Verarbeitet werden ausschließlich Daten, die für den Betrieb der Website
          technisch nötig sind, sowie Daten, die du aktiv über das Kontaktformular
          oder auf anderem Weg (Telefon, E-Mail, WhatsApp) mitteilst.
        </p>

        <h2>Hosting &amp; Server-Logfiles</h2>
        <p>
          Diese Website wird bei einem externen Hosting-Anbieter gehostet (Name,
          Anschrift und Link zur Datenschutzerklärung des Hosters werden hier
          ergänzt, sobald der endgültige Hosting-Vertrag feststeht). Beim Aufruf
          der Website erhebt der Hosting-Anbieter automatisch sogenannte
          Server-Logfiles, die dein Browser übermittelt \u2013 etwa IP-Adresse, Datum
          und Uhrzeit der Anfrage, Browsertyp und Betriebssystem. Diese Daten sind
          technisch nicht zu vermeiden und werden nicht mit anderen Datenquellen
          zusammengeführt. Rechtsgrundlage ist das berechtigte Interesse an einem
          sicheren und funktionsfähigen Betrieb der Website (Art. 6 Abs. 1 S. 1
          lit. f DSGVO).
        </p>

        <h2>Kontaktformular</h2>
        <p>
          Nutzt du das Kontaktformular, verarbeite ich die von dir angegebenen
          Daten (Name, E-Mail-Adresse, Nachricht) ausschließlich zur Bearbeitung
          deiner Anfrage und für eventuelle Anschlussfragen. Rechtsgrundlage ist
          Art. 6 Abs. 1 S. 1 lit. b DSGVO (vorvertragliche Anfrage) bzw. lit. a
          DSGVO (deine Einwilligung über die Checkbox). Die Daten werden gelöscht,
          sobald sie für die Bearbeitung deiner Anfrage nicht mehr erforderlich
          sind, sofern keine gesetzlichen Aufbewahrungspflichten entgegenstehen.
        </p>
        <p>
          Technisch sendet das Formular deine Angaben über das E-Mail-Programm
          deines Geräts \u2013 es gibt keinen eigenen Formular-Server, der die Daten
          zwischenspeichert.
        </p>

        <h2>Kontaktaufnahme per Telefon, E-Mail oder WhatsApp</h2>
        <p>
          Kontaktierst du mich per Telefon oder E-Mail, verarbeite ich die dabei
          anfallenden Daten (z. B. Rufnummer, E-Mail-Adresse, Inhalt der
          Nachricht) zur Bearbeitung deines Anliegens auf Grundlage des
          berechtigten Interesses an einer effizienten Kommunikation (Art. 6
          Abs. 1 S. 1 lit. f DSGVO).
        </p>
        <p>
          Für die Kontaktaufnahme per WhatsApp nutze ich den Dienst WhatsApp, der
          von WhatsApp Ireland Limited (einem Meta-Unternehmen) betrieben wird.
          Nimmst du über den WhatsApp-Link Kontakt auf, werden deine Nachricht
          sowie technische Metadaten (z. B. Telefonnummer, Gerätedaten) an
          WhatsApp/Meta übertragen und dort nach deren eigenen
          Datenschutzbestimmungen verarbeitet, unter anderem auch außerhalb der
          EU. Die Nutzung von WhatsApp erfolgt freiwillig und ausschließlich auf
          deine Initiative, wenn du den entsprechenden Link anklickst.
        </p>

        <h2>Externe Links (Shop, Reico, Instagram)</h2>
        <p>
          Diese Website verlinkt auf externe Angebote (Mad Dogs Shop,
          Reico-Partnerseite, Instagram-Profil). Beim Anklicken dieser Links
          verlässt du diese Website; es handelt sich um reine Hyperlinks, keine
          eingebetteten Inhalte. Für die Datenverarbeitung auf diesen externen
          Seiten gelten ausschließlich die Datenschutzerklärungen der jeweiligen
          Anbieter.
        </p>

        <h2>Cookies &amp; Tracking</h2>
        <p>
          Diese Website setzt keine Cookies zu Analyse-, Marketing- oder
          Tracking-Zwecken ein und bindet keine entsprechenden Dienste Dritter
          ein. Es findet keine Erstellung von Nutzungsprofilen statt.
        </p>

        <h2>Deine Rechte als betroffene Person</h2>
        <p>Du hast im Rahmen der geltenden gesetzlichen Bestimmungen jederzeit das Recht auf:</p>
        <ul>
          <li>Auskunft über deine gespeicherten personenbezogenen Daten (Art. 15 DSGVO)</li>
          <li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
          <li>Löschung deiner gespeicherten Daten (Art. 17 DSGVO)</li>
          <li>Einschränkung der Datenverarbeitung (Art. 18 DSGVO)</li>
          <li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
          <li>Widerspruch gegen die Verarbeitung (Art. 21 DSGVO)</li>
          <li>Widerruf erteilter Einwilligungen mit Wirkung für die Zukunft</li>
        </ul>
        <p>
          Wende dich hierzu einfach an die oben genannte E-Mail-Adresse. Dir steht
          zudem ein Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde zu, z. B.
          bei der für Nordrhein-Westfalen zuständigen Landesbeauftragten für
          Datenschutz und Informationsfreiheit.
        </p>

        <h2>Änderungen dieser Datenschutzerklärung</h2>
        <p>
          Diese Datenschutzerklärung wird angepasst, sobald sich die Website oder
          die eingesetzten Funktionen ändern. Es gilt jeweils die auf dieser Seite
          veröffentlichte, aktuelle Fassung.
        </p>
        <p class="text-small text-soft">Stand: Juli 2026</p>
      </div>
    </section>
"""


def notfound_content():
    return f"""    <section class="container error-page">
      <p class="error-page__code" aria-hidden="true">404</p>
      <h1>Seite nicht gefunden / Page not found</h1>
      <p class="lead max-w-prose text-center" style="margin-inline:auto;">
        Die angeforderte Seite existiert nicht (mehr) oder wurde verschoben.<br>
        The page you are looking for does not exist (anymore) or has been moved.
      </p>
      <div class="button-row button-row--center">
        <a class="btn btn--primary" href="/">Zur Startseite</a>
        <a class="btn btn--primary" href="/en/">Go to English homepage</a>
        <a class="btn btn--outline" href="/kontakt/">Kontakt / Contact</a>
      </div>
    </section>
"""


# ===========================================================================
# Seiteninhalte — Englisch
# ===========================================================================

def home_content_en():
    return f"""    <section class="hero container two-col">
      <div>
        <p class="eyebrow">Niederkassel · Cologne/Bonn, Germany</p>
        <h1 class="hero__title">Calm guidance, clear structure \u2013 for dogs with real character.</h1>
        <p class="lead hero__lead">
          Mad Dogs Germany is the one-person practice of Chris Knittel: professional
          dog walking plus training in dog sports, mantrailing and scent work around
          Niederkassel, Cologne and Bonn \u2013 for dogs who need more than a lap
          around the block.
        </p>
        <div class="button-row">
          <a class="btn btn--primary" href="/en/dogwalker-service/">Discover the dog walking service</a>
          <a class="btn btn--outline" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">
            {icon('chat')} Message us on WhatsApp{external_note('en')}
          </a>
        </div>
        <div class="hero__stats">
          <div class="stat">
            <span class="stat__value">16 years</span>
            <span class="stat__label">Experience working with dogs</span>
          </div>
          <div class="stat">
            <span class="stat__value">70+</span>
            <span class="stat__label">Competition starts in dog sports</span>
          </div>
          <div class="stat">
            <span class="stat__value">\u226410</span>
            <span class="stat__label">Dogs per walking group</span>
          </div>
          <div class="stat">
            <span class="stat__value">9 months</span>
            <span class="stat__label">Trail training in Austria</span>
          </div>
        </div>
      </div>
      <div class="hero__media">
        <picture>
          <source type="image/webp" srcset="/assets/images/hero-home-420.webp 420w, /assets/images/hero-home-640.webp 640w, /assets/images/hero-home-960.webp 960w" sizes="(min-width: 56em) 22rem, 90vw">
          <img
            src="/assets/images/hero-home-640.jpg"
            srcset="/assets/images/hero-home-420.jpg 420w, /assets/images/hero-home-640.jpg 640w, /assets/images/hero-home-960.jpg 960w"
            sizes="(min-width: 56em) 22rem, 90vw"
            alt="Black-and-tan Belgian Malinois mix sits attentively in a meadow full of daisies, looking up intently."
            width="960" height="1200" loading="eager" fetchpriority="high" decoding="async">
        </picture>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">What I offer</p>
          <h2>One trainer, three paths to a calmer dog</h2>
          <p class="lead">Whether it's everyday enrichment or focused training \u2013 every service is built on the same calm, consistent approach.</p>
        </div>
        <div class="grid grid--cards">
          <a class="card" href="/en/dogwalker-service/">
            <span class="card__icon">{icon('paw')}</span>
            <h3>Dog Walking Service</h3>
            <p>Structured walks in small groups for dogs with plenty of energy \u2013 in and around Niederkassel.</p>
            <span class="card__link">See the service \u2192</span>
          </a>
          <a class="card" href="/en/training/">
            <span class="card__icon">{icon('target')}</span>
            <h3>Dog Sports &amp; Mantrailing</h3>
            <p>Competitive dog sports, mantrailing and experience from professional service-dog work \u2013 an outlet for body and nose.</p>
            <span class="card__link">Explore training \u2192</span>
          </a>
          <a class="card" href="/en/shop/">
            <span class="card__icon">{icon('price-tag')}</span>
            <h3>Mad Dogs Shop</h3>
            <p>Collars, leashes, trail gear, apparel, books and courses for you and your dog.</p>
            <span class="card__link">Visit the shop \u2192</span>
          </a>
          <a class="card" href="/en/shop/#reico">
            <span class="card__icon">{icon('leaf')}</span>
            <h3>Reico Dog Food</h3>
            <p>Premium nutrient-rich dog food \u2013 through my personal Reico partner link.</p>
            <span class="card__link">Learn more \u2192</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Is this right for your dog?</p>
          <h2>When a normal walk around the block isn't enough anymore</h2>
          <p class="lead">The dog walking service is aimed especially at dogs with a lot of temperament \u2013 but also at anyone looking for dependable care with a clear structure.</p>
          <ul class="icon-list icon-list--check">
            <li>{icon('check', 'icon-list__icon')}<span>Dogs with plenty of energy and a mind of their own</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Dogs who pull on the leash or get worked up around other dogs</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Owners who value clear rules and real physical/mental outlets</span></li>
          </ul>
          <div class="button-row">
            <a class="btn btn--primary" href="/en/dogwalker-service/">More about the dog walking service</a>
          </div>
        </div>
        <div class="hero__media">
          <picture>
            <source srcset="/assets/images/gallery-6.webp" type="image/webp">
            <img src="/assets/images/gallery-6.jpg" alt="Shaggy brown-and-black mixed-breed dog with its mouth open, on a leash on a gravel path." width="384" height="512" loading="lazy" decoding="async">
          </picture>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container two-col two-col--reverse">
        <div class="hero__media">
          <picture>
            <source srcset="/assets/images/founder-384.webp" type="image/webp">
            <img src="/assets/images/founder-384.jpg" alt="Chris Knittel smiles at the camera, holding his Malinois, who happily lets his tongue hang out." width="384" height="512" loading="lazy" decoding="async">
          </picture>
        </div>
        <div>
          <p class="eyebrow">Who's behind Mad Dogs?</p>
          <h2>Chris Knittel \u2013 in competitive dog sports since 2014</h2>
          <p class="lead">
            Competition experience, training as a Pet/Man Trail instructor in Austria,
            everyday work as a service dog handler, and 1.5 years at one of Cologne's
            largest dog daycare centres \u2013 this mix shapes every training session
            and every walk.
          </p>
          <div class="button-row">
            <a class="btn btn--outline" href="/en/about/">More about me \u2192</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Get in touch</p>
          <h2>Let's talk about your dog</h2>
          <p class="lead">Whether it's a question about training or a request for the dog walking service: get in touch \u2013 fastest via WhatsApp or phone.</p>
          <ul class="info-list">
            <li class="info-list__item">
              <span class="info-list__icon">{icon('map-pin')}</span>
              <span>{ADDRESS_CITY} and surrounding area (Cologne/Bonn)</span>
            </li>
            <li class="info-list__item">
              <span class="info-list__icon">{icon('clock')}</span>
              <span>{HOURS['en']}</span>
            </li>
            <li class="info-list__item">
              <span class="info-list__icon">{icon('phone')}</span>
              <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a>
            </li>
          </ul>
          <div class="button-row">
            <a class="btn btn--accent" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">Message on WhatsApp{external_note('en')}</a>
            <a class="btn btn--outline" href="/en/contact/">Go to contact form</a>
          </div>
        </div>
        <figure class="badge-figure">
          <picture>
            <source srcset="/assets/images/logo-256.webp" type="image/webp">
            <img src="/assets/images/logo-256.jpg" alt="" width="180" height="180" loading="lazy" decoding="async">
          </picture>
          <figcaption>Mad Dogs Germany \u2013 Est. 2023</figcaption>
        </figure>
      </div>
    </section>
"""


def about_content_en():
    return f"""    <section class="container two-col">
      <div class="hero__media">
        <picture>
          <source srcset="/assets/images/founder-384.webp" type="image/webp">
          <img src="/assets/images/founder-384.jpg" alt="Chris Knittel smiles at the camera, holding his Malinois, who happily lets his tongue hang out, blue sky in the background." width="384" height="512" loading="eager" fetchpriority="high" decoding="async">
        </picture>
      </div>
      <div>
        <p class="eyebrow">About me</p>
        <h1>Chris Knittel \u2013 Dog Trainer, Dog Walker &amp; Service Dog Handler</h1>
        <div class="prose">
          <p>
            Mad Dogs Germany isn't a company with an HR department \u2013 it's one
            person with a clear approach: I've been active in competitive dog sports
            since 2014, work as a service dog handler in both civilian and military
            security work, and have additionally trained as a Pet/Man Trail instructor
            and dog trainer.
          </p>
          <p>
            This mix of competitive sport, security-service practice and pedagogical
            training shapes how I work: calm, consistent, and attentive to dogs that
            need a bit more guidance \u2013 whether in competition, in training, or on
            an everyday walk.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Background</p>
          <h2>Milestones in dog sports</h2>
        </div>
        <ol class="timeline">
          <li class="timeline__item">
            <p class="timeline__year">since 2014</p>
            <h3>Getting started in competitive dog sports</h3>
            <p>Active competitor with entries at SWHV, VDH-DM and DHV-DM competitions, plus more than 70 competition starts in THS (German obedience/agility sport).</p>
          </li>
          <li class="timeline__item">
            <p class="timeline__year">2017</p>
            <h3>Runner-up, German Championship GL 2000</h3>
            <p>Awarded the City of Metzingen's medal of honour for outstanding achievement in dog sports.</p>
          </li>
          <li class="timeline__item">
            <p class="timeline__year">2018</p>
            <h3>3rd place SWHV CSC &amp; 3rd place SWHV GL 2000m</h3>
            <p>Awarded the City of Metzingen's medal of honour once again for outstanding achievement in dog sports.</p>
          </li>
          <li class="timeline__item">
            <p class="timeline__year">ongoing</p>
            <h3>Protection-work assistant at the club</h3>
            <p>Supporting club-level protection training, plus experience working with fearful and reactive dogs.</p>
          </li>
        </ol>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Training &amp; Qualifications</p>
          <h2>Solid training, tested in practice</h2>
        </div>
        <div class="grid grid--cards">
          <div class="card">
            <span class="card__icon">{icon('compass-nose')}</span>
            <h3>Pet/Man Trail Instructor</h3>
            <p>Nine-month training with Pet Trailer in Austria \u2013 the professional foundation for the mantrailing training at Mad Dogs Germany.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('shield')}</span>
            <h3>Service Dog Handler</h3>
            <p>Active in civilian and military security work \u2013 hands-on experience in handling, obedience and scent work under real-world conditions.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('users')}</span>
            <h3>Certified Dog Trainer</h3>
            <p>Trained as a dog trainer at Kynologisch, with additional knowledge in working with fearful and reactive dogs.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('paw')}</span>
            <h3>Dog Walker with Pack Experience</h3>
            <p>1.5 years at one of Cologne's largest dog daycare centres \u2013 supervising and walking dogs in large groups.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Philosophy</p>
          <h2>How I work</h2>
        </div>
        <div class="grid grid--cards" style="grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));">
          <div class="card">
            <span class="card__icon">{icon('clock')}</span>
            <h3>Calm over speed</h3>
            <p>A dog learns fastest when it isn't under pressure. I work at the pace each individual dog needs \u2013 not the pace that looks fastest.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('heart')}</span>
            <h3>Trust, not force</h3>
            <p>Clear rules, yes. Harsh methods, no. Guidance comes from consistency and reliability \u2013 not from pressure.</p>
          </div>
          <div class="card">
            <span class="card__icon">{icon('target')}</span>
            <h3>Engage the nose and the mind</h3>
            <p>Exercise alone rarely tires a dog out for long. Tasks for the nose and the mind provide real, lasting enrichment.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container text-center max-w-prose mx-auto">
        <p class="eyebrow">Get in touch</p>
        <h2>Interested in training or dog walking?</h2>
        <p class="lead" style="margin-inline:auto;">Get in touch \u2013 we'll figure out together what suits you and your dog.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--accent" href="/en/contact/">Get in touch now</a>
          <a class="btn btn--outline" href="/en/training/">See training options</a>
        </div>
      </div>
    </section>
"""


def training_content_en():
    return f"""    <section class="container">
      <p class="eyebrow">Training</p>
      <h1>Dog Sports, Mantrailing &amp; Scent Work Experience</h1>
      <p class="lead max-w-prose">
        Three worlds of training, one core idea: dogs need tasks for the mind and
        nose \u2013 not just exercise. All three areas draw on my experience in
        competitive sport, trail training and professional service-dog work.
      </p>
      <ul class="tag-list" aria-label="Jump straight to a section" style="margin-block-start: var(--space-l);">
        <li><a class="tag" href="#dogsports">{icon('target', 'icon-inline')} Dog Sports</a></li>
        <li><a class="tag" href="#mantrailing">{icon('compass-nose', 'icon-inline')} Mantrailing</a></li>
        <li><a class="tag" href="#scentdogs">{icon('shield', 'icon-inline')} Scent Detection</a></li>
      </ul>
    </section>

    <section class="section" id="dogsports">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Competitive Dog Sports</p>
          <h2>Dog Sports</h2>
          <div class="prose">
            <p>
              Competitive dog sport (known in Germany as THS) combines obedience,
              agility and teamwork between dog and handler in a sporting,
              competition-focused format. I've been an active competitor myself
              since 2014 \u2013 with entries at SWHV, VDH-DM and DHV-DM competitions,
              more than 70 competition starts, and several podium finishes and
              medals of honour from the City of Metzingen.
            </p>
            <p>
              That competitive experience feeds directly into training: solid basic
              obedience, teamwork and the enjoyment of achieving something together
              are the focus \u2013 whether or not you want to compete yourself, or
              simply want to give your dog an athletic outlet.
            </p>
          </div>
        </div>
        <figure class="badge-figure">
          <picture>
            <source srcset="/assets/images/logo-256.webp" type="image/webp">
            <img src="/assets/images/logo-256.jpg" alt="" width="180" height="180" loading="lazy" decoding="async">
          </picture>
          <figcaption>Active in competitive dog sports since 2014 \u2013 70+ starts, several podium finishes.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--alt" id="mantrailing">
      <div class="container">
        <p class="eyebrow">Scent Work</p>
        <h2>Mantrailing (Man/Pet Trail)</h2>
        <div class="prose max-w-prose">
          <p>
            In mantrailing, a dog follows the individual scent trail of a specific
            person (man trail) or animal (pet trail) \u2013 not a general ground
            trail, but the unique scent signature of one individual. The dog works
            largely independently, while you learn to read its body language and
            trust it.
          </p>
          <p>
            For dogs with a lot of energy and drive, this is an ideal task: focused
            scent work often tires a dog out more than exercise alone, while also
            strengthening the bond between dog and handler. This training is based
            on my nine-month training as a Pet/Man Trail instructor with Pet Trailer
            in Austria.
          </p>
        </div>
        <div class="callout" style="margin-block-start: var(--space-l); margin-block-end: 0;">
          {icon('compass-nose')}
          <p>Beginners are explicitly welcome \u2013 mantrailing can be built up regardless of breed, age or prior experience.</p>
        </div>
      </div>
    </section>

    <section class="section" id="scentdogs">
      <div class="container two-col two-col--reverse">
        <div class="hero__media">
          <picture>
            <source srcset="/assets/images/gallery-2.webp" type="image/webp">
            <img src="/assets/images/gallery-2.jpg" alt="Black Malinois wearing a tactical harness, resting attentively in the grass in front of a tent." width="384" height="512" loading="lazy" decoding="async">
          </picture>
        </div>
        <div>
          <p class="eyebrow">Experience from Professional Service-Dog Work</p>
          <h2>Scent Detection Dogs</h2>
          <div class="prose">
            <p>
              Through my work as a service dog handler in civilian and military
              security roles, I bring additional experience in professional
              scent-detection work \u2013 for example, in deliberately building
              indication behaviour and in the calm, controlled use of a dog's nose
              under real-world conditions.
            </p>
            <p>
              A dedicated scent-detection course offering is currently in
              development. If you're interested in individual advice in this area,
              feel free to reach out directly.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container text-center max-w-prose mx-auto">
        <h2>Which area suits your dog?</h2>
        <p class="lead" style="margin-inline:auto;">Tell me a bit about your dog \u2013 I'll gladly recommend the right starting point.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--accent" href="/en/contact/">Send a training enquiry</a>
        </div>
      </div>
    </section>
"""


def dogwalker_content_en():
    gallery_items = "\n".join(_gallery_item("en", num, cap) for num, cap in GALLERY_CAPTIONS_EN)

    return f"""    <section class="container two-col">
      <div>
        <p class="eyebrow">Dog Walking Service in Niederkassel</p>
        <h1>Professional Dog Walking \u2013 Even for Demanding Dogs</h1>
        <p class="lead">
          Do you have a dog with lots of energy, a strong will, or a lot of
          character? Mad Dogs offers more than a walk: structured enrichment,
          clear guidance and individual attention.
        </p>
        <div class="button-row">
          <a class="btn btn--accent" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">
            {icon('chat')} Get in touch on WhatsApp{external_note('en')}
          </a>
          <a class="btn btn--outline" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a>
        </div>
      </div>
      <figure class="badge-figure">
        <picture>
          <source srcset="/assets/images/badge-dogwalker-260.webp" type="image/webp">
          <img src="/assets/images/badge-dogwalker-260.png" alt="Circular patch reading 'Dogwalker NDK' with the Mad Dogs Germany logo at its centre." width="220" height="220" loading="eager" fetchpriority="high" decoding="async">
        </picture>
      </figure>
    </section>

    <section class="section">
      <div class="container two-col">
        <div>
          <h2>Ideal for dogs that\u2026</h2>
          <ul class="icon-list icon-list--check">
            <li>{icon('check', 'icon-list__icon')}<span>have plenty of energy</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>pull on the leash</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>get worked up around other dogs</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>need clear rules and real outlets</span></li>
          </ul>
        </div>
        <div>
          <h2>What your dog gets from me</h2>
          <ul class="icon-list icon-list--check">
            <li>{icon('check', 'icon-list__icon')}<span>Calm, consistent guidance</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Focused enrichment for body &amp; mind</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Walks in small, well-matched groups of up to 10 dogs</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Social skills training and impulse control while out and about</span></li>
            <li>{icon('check', 'icon-list__icon')}<span>Reliability &amp; experience handling "strong personalities"</span></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Background</p>
          <h2>16 years of experience working with dogs</h2>
        </div>
        <div class="prose max-w-prose">
          <p>
            I've been working with dogs of all kinds of breeds in dog sports for 16
            years. I spent 1.5 years working at one of Cologne's largest dog daycare
            centres, supervising and walking dogs in large groups. I'm also active
            as a service dog handler and have completed my dog trainer training.
          </p>
          <p><strong>Enrichment that works the mind, not just the legs.</strong></p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Pricing</p>
          <h2>Transparent &amp; fair</h2>
        </div>
        <div class="price-table-wrap">
          <table class="price-table">
            <caption>Dog Walking Service prices (group walk)</caption>
            <thead>
              <tr>
                <th scope="col">Duration</th>
                <th scope="col">Price</th>
              </tr>
            </thead>
            <tbody>
              <tr><th scope="row">1 hour</th><td>\u20ac20</td></tr>
              <tr><th scope="row">1.5 hours</th><td>\u20ac25</td></tr>
              <tr><th scope="row">2 hours</th><td>\u20ac30</td></tr>
            </tbody>
          </table>
        </div>
        <p class="price-note">{icon('map-pin')} Service area: {ADDRESS_CITY} and surrounding area. Please arrange appointments via WhatsApp or phone call.</p>
        <p class="value-badge" style="margin-block-start: var(--space-m);">{icon('check-circle')} Free, no-obligation introductory chat</p>
        <div class="button-row">
          <a class="btn btn--accent" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">
            {icon('chat')} Arrange a trial walk{external_note('en')}
          </a>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Gallery</p>
          <h2>Out and about with Mad Dogs</h2>
          <p class="lead">A few impressions from real walking groups. Click a photo for a larger view.</p>
        </div>
        <ul class="gallery">
{gallery_items}
        </ul>
      </div>
    </section>

    <dialog class="lightbox" data-lightbox aria-label="Photo gallery, full view">
      <div class="lightbox__inner">
        <button class="lightbox__close" type="button" data-lightbox-close aria-label="Close full view">&times;</button>
        <button class="lightbox__nav lightbox__nav--prev" type="button" data-lightbox-prev aria-label="Previous image">{icon('chevron-left')}</button>
        <button class="lightbox__nav lightbox__nav--next" type="button" data-lightbox-next aria-label="Next image">{icon('chevron-right')}</button>
        <img class="lightbox__image" data-lightbox-image src="" alt="">
        <p class="lightbox__caption" data-lightbox-caption></p>
      </div>
    </dialog>
"""


def shop_content_en():
    categories = [
        "Collars", "Leashes", "European Pet Pharmacy", "Non Stop Dogwear",
        "Trail Gear", "Coats &amp; Jackets", "Books", "Miscellaneous", "Courses",
    ]
    tags = "\n".join(
        f'          <li class="tag">{icon("price-tag", "icon-inline")} {cat}</li>' for cat in categories
    )
    return f"""    <section class="container">
      <p class="eyebrow">Mad Dogs Shop</p>
      <h1>Gear for You and Your Dog</h1>
      <p class="lead max-w-prose">
        From collars to trail gear: the Mad Dogs Shop runs through my external shop
        partner. Clicking "Visit the shop" opens it in a new tab \u2013 the shop
        operator's own privacy policy applies there.
      </p>
      <ul class="tag-list" style="margin-block-start: var(--space-l);">
{tags}
      </ul>
      <div class="button-row">
        <a class="btn btn--primary" href="{SHOP_URL}" target="_blank" rel="noopener noreferrer">
          Visit the Mad Dogs Shop{external_note('en')}
          {icon('external')}
        </a>
      </div>
    </section>

    <section class="section section--alt" id="reico">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Nutrition</p>
          <h2>Reico Dog Food</h2>
          <p class="lead">
            Premium nutrient-based food following the Reico concept \u2013 through my
            personal partner link. The same applies here: the link leads to the
            provider's own offering, including their own privacy policy.
          </p>
          <div class="button-row">
            <a class="btn btn--primary" href="{REICO_URL}" target="_blank" rel="noopener noreferrer">
              Go to the Reico partner page{external_note('en')}
              {icon('external')}
            </a>
          </div>
        </div>
        <div class="card" style="align-self:center;">
          <span class="card__icon">{icon('leaf')}</span>
          <h3>Nutrient Concept</h3>
          <p>Supplementary feed and formulas that I give my own dogs too \u2013 which is why I recommend it personally.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container text-center max-w-prose mx-auto">
        <h2>Questions about products or orders?</h2>
        <p class="lead" style="margin-inline:auto;">Orders, shipping and returns are handled directly by the respective shop provider. For general questions, feel free to contact me directly anyway.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--outline" href="/en/contact/">Get in touch</a>
        </div>
      </div>
    </section>
"""


def testimonials_content_en():
    return f"""    <section class="container">
      <p class="eyebrow">Testimonials</p>
      <h1>What My Clients Say</h1>
      <div class="empty-state">
        <span class="empty-state__icon">{icon('chat', 'icon', 'style="width:100%;height:100%;"')}</span>
        <h2>Real testimonials are coming soon</h2>
        <p>
          I deliberately don't show made-up reviews here. As soon as clients give
          their consent, I'll publish genuine testimonials about the dog walking
          service and training here.
        </p>
        <p>Already joined us with your dog? I'd love to hear your feedback.</p>
        <a class="btn btn--primary" href="/en/contact/">Share your experience</a>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container text-center max-w-prose mx-auto">
        <h2>Also on Instagram</h2>
        <p class="lead" style="margin-inline:auto;">Get a look at training and everyday life on Instagram too.</p>
        <div class="button-row button-row--center">
          <a class="btn btn--outline" href="{INSTAGRAM_URL}" target="_blank" rel="noopener noreferrer">
            {icon('camera')} {INSTAGRAM_HANDLE} on Instagram{external_note('en')}
          </a>
        </div>
      </div>
    </section>
"""


def contact_content_en():
    return f"""    <section class="container two-col">
      <div>
        <p class="eyebrow">Contact</p>
        <h1>Let's Talk About Your Dog</h1>
        <p class="lead">
          The fastest way to reach me is via WhatsApp or phone. You're also
          welcome to use the form \u2013 I'll get back to you as soon as possible.
        </p>
        <ul class="info-list">
          <li class="info-list__item">
            <span class="info-list__icon">{icon('phone')}</span>
            <div>
              <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a><br>
              <a href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">also on WhatsApp{external_note('en')}</a>
            </div>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">{icon('mail')}</span>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">{icon('map-pin')}</span>
            <address style="font-style:normal;">{ADDRESS_STREET}, {ADDRESS_ZIP} {ADDRESS_CITY}, Germany</address>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">{icon('clock')}</span>
            <span>{HOURS['en']}</span>
          </li>
        </ul>
      </div>

      <form class="form" data-contact-form action="mailto:{EMAIL}" method="get" novalidate>
        <div class="form-field">
          <label for="name">Name *</label>
          <input id="name" name="name" type="text" autocomplete="name" required aria-describedby="name-error">
          <p class="form-error" id="name-error" role="alert"></p>
        </div>
        <div class="form-field">
          <label for="email">Email *</label>
          <input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-error">
          <p class="form-error" id="email-error" role="alert"></p>
        </div>
        <div class="form-field">
          <label for="message">Message *</label>
          <textarea id="message" name="message" required aria-describedby="message-error"></textarea>
          <p class="form-error" id="message-error" role="alert"></p>
        </div>
        <div class="form-field form-field--hp">
          <label for="website">Please leave this field blank</label>
          <input id="website" name="website" type="text" tabindex="-1" autocomplete="off">
        </div>
        <div class="form-field form-field--checkbox">
          <input id="consent" name="consent" type="checkbox" required aria-describedby="consent-error">
          <label for="consent">
            I agree that my details will be used to process my enquiry. I can
            withdraw my consent at any time. Details in the
            <a href="/en/privacy/">Privacy Policy</a>. *
          </label>
        </div>
        <p class="form-error" id="consent-error" role="alert"></p>
        <p class="required-note">* Required field</p>
        <button class="btn btn--primary btn--block" type="submit">Send message</button>
        <p class="form-status" role="status" aria-live="polite" data-form-status></p>
        <p class="text-small text-soft">
          Note: This website sends form data straight through your own email
          program, without its own server. If nothing opens, feel free to email
          me directly at <a href="mailto:{EMAIL}">{EMAIL}</a>.
        </p>
      </form>
    </section>
"""


def legal_content_en():
    return f"""    <section class="container max-w-prose">
      <h1>Legal Notice</h1>
      <div class="callout">
        {icon('alert-circle')}
        <div>
          <p><strong>Note on this relaunch:</strong> This text was newly created as part of the relaunch, based on previously publicly available information.</p>
          <p>Please have this reviewed by Chris Knittel or a qualified legal professional before publishing \u2013 especially the address and VAT ID.</p>
        </div>
      </div>

      <div class="prose">
        <h2>Information pursuant to Section 5 TMG (German Telemedia Act)</h2>
        <p>
          Mad Dogs Germany<br>
          Chris Knittel<br>
          {ADDRESS_STREET}<br>
          {ADDRESS_ZIP} {ADDRESS_CITY}<br>
          Germany
        </p>

        <h2>Contact</h2>
        <p>
          Phone: <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a><br>
          Email: <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>

        <h2>VAT Identification Number</h2>
        <p class="text-soft">
          If applicable, the VAT identification number pursuant to Section 27a of
          the German VAT Act (UStG) will be added here. If the small business
          regulation (Section 19 UStG) applies instead, this will be noted briefly
          at this point.
        </p>

        <h2>Responsible for content pursuant to Section 18(2) MStV</h2>
        <p>Chris Knittel (address as above)</p>

        <h2>EU Dispute Resolution</h2>
        <p>
          The European Commission provides a platform for online dispute
          resolution (ODR), available at
          <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener noreferrer">ec.europa.eu/consumers/odr{external_note('en')}{icon('external', 'icon-inline')}</a>.
          I am not obliged, and generally not willing, to take part in
          dispute-resolution proceedings before a consumer arbitration board.
        </p>

        <h2>Social Media Presence</h2>
        <p>
          This legal notice also applies to the social media presence:
          <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener noreferrer">instagram.com/mad_dogs_germany{external_note('en')}{icon('external', 'icon-inline')}</a>
        </p>

        <h2>Liability for Content</h2>
        <p>
          The content of this website has been created with the greatest possible
          care. However, no guarantee can be given for the accuracy, completeness
          or timeliness of the content. As a service provider, I am responsible
          for my own content on these pages in accordance with general law,
          pursuant to Section 7(1) TMG. However, pursuant to Sections 8 to 10 TMG,
          I am not obliged as a service provider to monitor transmitted or stored
          third-party information, or to investigate circumstances that indicate
          unlawful activity.
        </p>

        <h2>Liability for Links</h2>
        <p>
          This site contains links to external third-party websites (including the
          shop and the Reico partner page) over whose content I have no influence.
          Therefore, I cannot accept any liability for this external content. The
          respective provider or operator of the linked pages is always
          responsible for their content.
        </p>

        <h2>Copyright</h2>
        <p>
          Content and works created by the site operator on these pages are
          subject to German copyright law. Contributions by third parties are
          marked as such. Any duplication, editing, distribution or any form of
          use beyond the limits of copyright law requires the written consent of
          the respective author or creator.
        </p>
      </div>
    </section>
"""


def privacy_content_en():
    return f"""    <section class="container max-w-prose">
      <h1>Privacy Policy</h1>
      <div class="callout">
        {icon('alert-circle')}
        <div>
          <p><strong>Note on this relaunch:</strong> This policy was deliberately kept lean and tailored to the features actually in use (no cookies, no tracking, no embedded third-party content).</p>
          <p>Please have this reviewed by a qualified legal professional before publishing.</p>
        </div>
      </div>

      <div class="prose">
        <h2>Controller</h2>
        <p>
          Chris Knittel<br>
          {ADDRESS_STREET}, {ADDRESS_ZIP} {ADDRESS_CITY}, Germany<br>
          Email: <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>

        <h2>At a Glance</h2>
        <p>This website deliberately does without:</p>
        <ul>
          <li>Cookies for analytics or marketing purposes</li>
          <li>External fonts (e.g. Google Fonts) \u2013 only system fonts already installed on your device are used</li>
          <li>Embedded social media widgets or third-party maps</li>
        </ul>
        <p>
          Only data that is technically necessary to operate the website is
          processed, along with any data you actively share via the contact form
          or by other means (phone, email, WhatsApp).
        </p>

        <h2>Hosting &amp; Server Log Files</h2>
        <p>
          This website is hosted with an external hosting provider (name, address
          and a link to the hosting provider's privacy policy will be added here
          once the final hosting arrangement is confirmed). When you visit the
          website, the hosting provider automatically collects so-called server
          log files transmitted by your browser \u2013 such as IP address, date and
          time of the request, browser type and operating system. This data
          cannot be technically avoided and is not combined with other data
          sources. The legal basis is the legitimate interest in operating the
          website securely and reliably (Art. 6(1)(f) GDPR).
        </p>

        <h2>Contact Form</h2>
        <p>
          If you use the contact form, I process the data you provide (name,
          email address, message) solely to handle your enquiry and any
          follow-up questions. The legal basis is Art. 6(1)(b) GDPR
          (pre-contractual enquiry) or Art. 6(1)(a) GDPR (your consent via the
          checkbox). Your data will be deleted once it is no longer required to
          process your enquiry, unless statutory retention obligations apply.
        </p>
        <p>
          Technically, the form sends your details through your device's own
          email program \u2013 there is no dedicated form server that stores the
          data in between.
        </p>

        <h2>Contact via Phone, Email or WhatsApp</h2>
        <p>
          If you contact me by phone or email, I process the resulting data
          (e.g. phone number, email address, content of the message) to handle
          your enquiry, based on a legitimate interest in efficient communication
          (Art. 6(1)(f) GDPR).
        </p>
        <p>
          For contact via WhatsApp, I use the WhatsApp service operated by
          WhatsApp Ireland Limited (a Meta company). If you get in touch via the
          WhatsApp link, your message and technical metadata (e.g. phone number,
          device data) are transmitted to WhatsApp/Meta and processed there under
          their own privacy terms, including outside the EU in some cases. Using
          WhatsApp is voluntary and happens solely on your own initiative when
          you click the corresponding link.
        </p>

        <h2>External Links (Shop, Reico, Instagram)</h2>
        <p>
          This website links to external offerings (Mad Dogs Shop, Reico partner
          page, Instagram profile). Clicking these links takes you away from
          this website; they are plain hyperlinks, not embedded content. Data
          processing on these external sites is governed solely by the
          respective provider's own privacy policy.
        </p>

        <h2>Cookies &amp; Tracking</h2>
        <p>
          This website does not use cookies for analytics, marketing or tracking
          purposes and does not embed any corresponding third-party services. No
          user profiles are created.
        </p>

        <h2>Your Rights as a Data Subject</h2>
        <p>Under applicable law, you have the right at any time to:</p>
        <ul>
          <li>Access to your stored personal data (Art. 15 GDPR)</li>
          <li>Rectification of inaccurate data (Art. 16 GDPR)</li>
          <li>Erasure of your stored data (Art. 17 GDPR)</li>
          <li>Restriction of processing (Art. 18 GDPR)</li>
          <li>Data portability (Art. 20 GDPR)</li>
          <li>Objection to processing (Art. 21 GDPR)</li>
          <li>Withdrawal of any consent given, with effect for the future</li>
        </ul>
        <p>
          Simply get in touch via the email address above. You also have the
          right to lodge a complaint with a data protection supervisory
          authority, e.g. the data protection authority responsible for North
          Rhine-Westphalia.
        </p>

        <h2>Changes to this Privacy Policy</h2>
        <p>
          This privacy policy will be updated whenever the website or the
          features it uses change. The version published on this page is
          always the current one.
        </p>
        <p class="text-small text-soft">Last updated: July 2026</p>
      </div>
    </section>
"""


# ===========================================================================
# Strukturierte Daten (JSON-LD) für die jeweilige Startseite
# ===========================================================================
def local_business_jsonld(lang):
    description = (
        "Dogwalker-Service, Hundesport- und Mantrailing-Training mit Chris Knittel in Niederkassel bei Köln/Bonn."
        if lang == "de" else
        "Professional dog walking, dog sport and mantrailing training with Chris Knittel in Niederkassel near Cologne/Bonn, Germany."
    )
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": SITE_NAME,
        "description": description,
        "url": SITE_URL + PATHS["home"][lang],
        "inLanguage": lang,
        "image": SITE_URL + "/assets/images/og-image.jpg",
        "logo": SITE_URL + "/assets/images/logo-256.jpg",
        "telephone": PHONE_E164,
        "email": EMAIL,
        "founder": {"@type": "Person", "name": "Chris Knittel"},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADDRESS_STREET,
            "postalCode": ADDRESS_ZIP,
            "addressLocality": ADDRESS_CITY,
            "addressCountry": "DE",
        },
        "areaServed": ["Niederkassel", "Köln" if lang == "de" else "Cologne", "Bonn"],
        "sameAs": [INSTAGRAM_URL],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "07:00",
                "closes": "18:00",
            }
        ],
    }
    return '  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n  </script>\n"


# ===========================================================================
# Seiten-Registry: Inhalte, Titel & Meta-Beschreibungen je Sprache
# ===========================================================================
PAGE_META = {
    "home": {
        "de": {
            "title": "Mad Dogs Germany \u2013 Dogwalker-Service & Hundetraining in Niederkassel",
            "description": "Professioneller Dogwalker-Service, Hundesport- und Mantrailing-Training mit Chris Knittel in Niederkassel bei Köln/Bonn.",
            "content": home_content_de,
            "extra_head": lambda: local_business_jsonld("de"),
        },
        "en": {
            "title": "Mad Dogs Germany \u2013 Dog Walking & Dog Training in Niederkassel",
            "description": "Professional dog walking, dog sport and mantrailing training with Chris Knittel in Niederkassel near Cologne/Bonn, Germany.",
            "content": home_content_en,
            "extra_head": lambda: local_business_jsonld("en"),
        },
    },
    "about": {
        "de": {
            "title": "Über mich \u2013 Chris Knittel | Mad Dogs Germany",
            "description": "Seit 2014 im Hundesport aktiv: Turniererfolge, Ausbildung zum Pet-/Man-Trail-Trainer und Diensthundeführer. Lerne Chris Knittel kennen.",
            "content": about_content_de,
            "og_image": "/assets/images/founder-384.jpg",
        },
        "en": {
            "title": "About \u2013 Chris Knittel | Mad Dogs Germany",
            "description": "Active in competitive dog sports since 2014: trained Pet/Man Trail instructor and service dog handler. Meet Chris Knittel.",
            "content": about_content_en,
            "og_image": "/assets/images/founder-384.jpg",
        },
    },
    "training": {
        "de": {
            "title": "Training: Hundesport, Mantrailing & Spürhunde | Mad Dogs Germany",
            "description": "Turnierhundesport, Mantrailing (Man/Pet Trail) und Erfahrung aus dem Diensthundewesen: Auslastung für Kopf und Nase, für Hunde mit viel Energie.",
            "content": training_content_de,
        },
        "en": {
            "title": "Training: Dog Sports, Mantrailing & Scent Work | Mad Dogs Germany",
            "description": "Competitive dog sports, mantrailing (Man/Pet Trail) and experience from professional service-dog work: an outlet for dogs with plenty of energy.",
            "content": training_content_en,
        },
    },
    "dogwalker": {
        "de": {
            "title": "Dogwalker-Service in Niederkassel | Mad Dogs Germany",
            "description": "Professioneller Gassi-Service für anspruchsvolle Hunde mit viel Energie. Strukturierte Auslastung, klare Führung, kleine Gruppen bis 10 Hunde. Ab 20 €.",
            "content": dogwalker_content_de,
        },
        "en": {
            "title": "Dog Walking Service in Niederkassel | Mad Dogs Germany",
            "description": "Professional dog walking for demanding, high-energy dogs. Structured enrichment, clear guidance, small groups of up to 10 dogs. From \u20ac20.",
            "content": dogwalker_content_en,
        },
    },
    "shop": {
        "de": {
            "title": "Mad Dogs Shop & Reico Hundefutter | Mad Dogs Germany",
            "description": "Halsbänder, Leinen, Trail-Zubehör, Bekleidung, Bücher und Kurse im Mad Dogs Shop \u2013 plus hochwertiges Reico Hundefutter über den Partnerlink.",
            "content": shop_content_de,
        },
        "en": {
            "title": "Mad Dogs Shop & Reico Dog Food | Mad Dogs Germany",
            "description": "Collars, leashes, trail gear, apparel, books and courses in the Mad Dogs Shop \u2013 plus premium Reico dog food through the partner link.",
            "content": shop_content_en,
        },
    },
    "testimonials": {
        "de": {
            "title": "Kundenstimmen | Mad Dogs Germany",
            "description": "Echte Erfahrungsberichte entstehen gerade. Du warst schon dabei? Teile gern deine Erfahrung mit Mad Dogs Germany.",
            "content": testimonials_content_de,
        },
        "en": {
            "title": "Testimonials | Mad Dogs Germany",
            "description": "Real testimonials are being collected right now. Already joined us? Share your experience with Mad Dogs Germany.",
            "content": testimonials_content_en,
        },
    },
    "contact": {
        "de": {
            "title": "Kontakt | Mad Dogs Germany",
            "description": "Kontaktiere Chris Knittel von Mad Dogs Germany per Telefon, WhatsApp, E-Mail oder Formular \u2013 Niederkassel und Umgebung.",
            "content": contact_content_de,
        },
        "en": {
            "title": "Contact | Mad Dogs Germany",
            "description": "Get in touch with Chris Knittel of Mad Dogs Germany by phone, WhatsApp, email or contact form \u2013 Niederkassel and the surrounding area.",
            "content": contact_content_en,
        },
    },
    "legal": {
        "de": {
            "title": "Impressum | Mad Dogs Germany",
            "description": "Impressum von Mad Dogs Germany gemäß § 5 TMG.",
            "content": legal_content_de,
        },
        "en": {
            "title": "Legal Notice | Mad Dogs Germany",
            "description": "Legal notice of Mad Dogs Germany pursuant to Section 5 TMG (German Telemedia Act).",
            "content": legal_content_en,
        },
    },
    "privacy": {
        "de": {
            "title": "Datenschutzerklärung | Mad Dogs Germany",
            "description": "Datenschutzerklärung von Mad Dogs Germany gemäß DSGVO.",
            "content": privacy_content_de,
        },
        "en": {
            "title": "Privacy Policy | Mad Dogs Germany",
            "description": "Privacy policy of Mad Dogs Germany pursuant to the GDPR.",
            "content": privacy_content_en,
        },
    },
}


def out_path_for(key, lang):
    rel = PATHS[key][lang].strip("/")
    return f"{rel}/index.html" if rel else "index.html"


def build_pages():
    for key in PAGE_KEYS:
        for lang in LANGS:
            meta = PAGE_META[key][lang]
            html = render_page(
                lang=lang,
                active_key=key,
                title=meta["title"],
                description=meta["description"],
                content=meta["content"](),
                og_image=meta.get("og_image"),
                extra_head=meta["extra_head"]() if "extra_head" in meta else "",
            )
            write_file(out_path_for(key, lang), html)


def build_404():
    html = page_head(
        "de",
        None,
        "404 \u2013 Seite nicht gefunden / Page not found | Mad Dogs Germany",
        "Die angeforderte Seite wurde nicht gefunden. / The requested page was not found.",
        noindex=True,
    )
    header = header_html("de", None)
    footer = footer_html("de")
    content = notfound_content()
    full = f"""{html}<body>
{header}  <main id="main">
{content}
  </main>
{footer}  <script src="/assets/js/main.js" defer></script>
</body>
</html>
"""
    write_file("404.html", full)


def build_robots():
    content = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    write_file("robots.txt", content)


def build_sitemap():
    entries = []
    for key in PAGE_KEYS:
        for lang in LANGS:
            loc = SITE_URL + PATHS[key][lang]
            alt_links = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}{PATHS[key][l]}"/>'
                for l in LANGS
            )
            entries.append(f"  <url>\n    <loc>{loc}</loc>\n{alt_links}\n  </url>")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    write_file("sitemap.xml", xml)


def build_manifest():
    manifest = {
        "name": "Mad Dogs Germany",
        "short_name": "Mad Dogs",
        "description": "Dogwalker-Service, Hundesport und Mantrailing in Niederkassel bei Köln/Bonn.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#fbfaf7",
        "theme_color": "#1e3a5f",
        "lang": "de",
        "icons": [
            {"src": "/assets/images/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/images/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    write_file("site.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def build_htaccess():
    content = """# Mad Dogs Germany \u2013 Apache-Konfiguration (IONOS-kompatibel)
# Wird nur wirksam, wenn per Apache/IONOS-Webhosting ausgeliefert.

# HTTPS erzwingen
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} off
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>

# Eigene Fehlerseite
ErrorDocument 404 /404.html

# Sicherheits-Header
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>

# Caching statischer Assets
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/jpeg "access plus 6 months"
  ExpiresByType image/png "access plus 6 months"
  ExpiresByType image/webp "access plus 6 months"
  ExpiresByType image/x-icon "access plus 1 year"
</IfModule>

# Kompression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json
</IfModule>
"""
    write_file(".htaccess", content)


def main():
    print("Baue Mad Dogs Germany \u2013 statische Seiten (DE + EN) ...")
    build_pages()
    build_404()
    build_robots()
    build_sitemap()
    build_manifest()
    build_htaccess()
    total_pages = len(PAGE_KEYS) * len(LANGS) + 1
    print(f"\nFertig. {total_pages} HTML-Seiten (DE+EN) sowie robots.txt, sitemap.xml, site.webmanifest und .htaccess erzeugt.")


if __name__ == "__main__":
    main()
