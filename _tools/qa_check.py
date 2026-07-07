#!/usr/bin/env python3
"""QA-Check für die generierten, statischen HTML-Seiten.
Prüft: alt-Attribute, doppelte IDs, Label<->Input-Zuordnung, interne Links,
lang-Attribut, genau ein <h1>, Title/Description vorhanden.
"""
import pathlib
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOID_ELEMENTS = {"img", "input", "br", "hr", "meta", "link", "source", "area", "col", "embed", "track", "wbr"}


class PageChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.issues = []
        self.ids = {}
        self.labels_for = []
        self.input_ids = []
        self.h1_count = 0
        self.lang = None
        self.title = ""
        self.in_title = False
        self.description = None
        self.links = []  # (tag, attr, value)
        self.stack = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang = d.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta" and d.get("name") == "description":
            self.description = d.get("content", "")
        if "id" in d:
            self.ids.setdefault(d["id"], 0)
            self.ids[d["id"]] += 1
        if tag == "img":
            if "alt" not in d:
                self.issues.append(f"<img> ohne alt-Attribut: src={d.get('src')}")
            if "src" in d:
                self.links.append(("img", "src", d["src"]))
            if "srcset" in d:
                for part in d["srcset"].split(","):
                    url = part.strip().split(" ")[0]
                    if url:
                        self.links.append(("img", "srcset", url))
        if tag == "label" and "for" in d:
            self.labels_for.append(d["for"])
        if tag == "input" and "id" in d:
            self.input_ids.append(d["id"])
        if tag == "a" and "href" in d:
            href = d["href"]
            if href in ("#", ""):
                self.issues.append("‑ leeres <a href> gefunden")
            self.links.append(("a", "href", href))
            if tag == "a" and d.get("target") == "_blank":
                rel = d.get("rel", "")
                if "noopener" not in rel:
                    self.issues.append(f"target=_blank ohne rel=noopener: href={href}")
        if tag == "link" and d.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest", "canonical", "alternate"):
            href = d.get("href")
            if href:
                self.links.append(("link", "href", href))
        if tag == "script" and d.get("src"):
            self.links.append(("script", "src", d["src"]))
        if tag not in VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in VOID_ELEMENTS:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            # Tag mismatch – ungewöhnlich, aber wir versuchen, robust zu bleiben
            while self.stack and self.stack[-1] != tag:
                self.issues.append(f"möglicher unausgeglichener Tag: <{self.stack.pop()}>")
            if self.stack:
                self.stack.pop()

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def resolve_path(current_file: pathlib.Path, href: str):
    if href.startswith(("http://", "https://", "mailto:", "tel:", "//", "data:")):
        return None  # extern, nicht prüfbar/nötig
    href = href.split("#")[0]
    if href == "":
        return "SELF"
    if href.startswith("/"):
        target = ROOT / href.lstrip("/")
    else:
        target = current_file.parent / href
    if target.is_dir() or href.endswith("/"):
        target = target / "index.html"
    return target


def main():
    html_files = sorted(ROOT.glob("**/*.html"))
    html_files = [f for f in html_files if "_tools" not in f.parts]

    total_issues = 0
    for f in html_files:
        checker = PageChecker()
        text = f.read_text(encoding="utf-8")
        checker.feed(text)

        rel = f.relative_to(ROOT)
        local_issues = list(checker.issues)

        if not checker.lang:
            local_issues.append("kein lang-Attribut auf <html>")
        if checker.h1_count != 1:
            local_issues.append(f"{checker.h1_count} <h1>-Elemente gefunden (erwartet: 1)")
        if not checker.title.strip():
            local_issues.append("kein <title> Inhalt")
        if checker.description is None or not checker.description.strip():
            local_issues.append("keine meta description")

        dupes = {k: v for k, v in checker.ids.items() if v > 1}
        if dupes:
            local_issues.append(f"doppelte IDs: {dupes}")

        missing_label_targets = [fid for fid in checker.labels_for if fid not in checker.input_ids and fid not in checker.ids]
        if missing_label_targets:
            local_issues.append(f"label[for] ohne passendes Element: {missing_label_targets}")

        for tag, attr, href in checker.links:
            target = resolve_path(f, href)
            if target in (None, "SELF"):
                continue
            if not target.exists():
                local_issues.append(f"toter interner Link ({tag} {attr}): {href} -> {target.relative_to(ROOT)}")

        if local_issues:
            print(f"\n== {rel} ==")
            for issue in local_issues:
                print(f"  - {issue}")
            total_issues += len(local_issues)

    print(f"\n{'='*60}\nGeprüfte Dateien: {len(html_files)} | Gefundene Probleme: {total_issues}")


if __name__ == "__main__":
    main()
