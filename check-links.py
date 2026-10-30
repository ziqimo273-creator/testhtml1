#!/usr/bin/env python3
"""Check local HTML links in the three mirrored site folders."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote
import sys

ROOT = Path(__file__).resolve().parent / "offline-sites"
ATTRS = {"href", "src", "action", "poster"}

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ATTRS and value:
                self.links.append((tag, key, value))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

def check_site(site_dir: Path):
    html_files = list(site_dir.rglob("*.html")) + list(site_dir.rglob("*.htm"))
    missing = []
    checked = 0
    for page in html_files:
        try:
            text = page.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            missing.append((page, f"[READ ERROR] {exc}"))
            continue
        parser = LinkParser()
        parser.feed(text)
        for tag, attr, raw in parser.links:
            value = raw.strip()
            if not value or value.startswith(("#", "data:", "javascript:", "mailto:", "tel:")):
                continue
            parsed = urlparse(value)
            if parsed.scheme in ("http", "https", "ftp") or parsed.netloc:
                # Remaining remote links are not offline links; report them for manual review.
                continue
            path = unquote(parsed.path)
            if not path:
                continue
            target = (page.parent / path).resolve()
            checked += 1
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                # Wget may save extensionless URL pages as .html.
                candidates = [Path(str(target) + ".html"), target.with_suffix(".html")]
                if not any(c.exists() for c in candidates):
                    missing.append((page, f"{attr}={raw} -> {target}"))
    print(f"\n[{site_dir.name}] HTML pages: {len(html_files)} | local links checked: {checked} | missing: {len(missing)}")
    for page, detail in missing[:300]:
        print(f"  MISSING: {page.relative_to(site_dir)} :: {detail}")
    if len(missing) > 300:
        print(f"  ... plus {len(missing)-300} more")
    return len(missing)

def main():
    if not ROOT.exists():
        print(f"No mirror directory found: {ROOT}\nRun mirror-sites.ps1 first.")
        return 2
    dirs = [p for p in ROOT.iterdir() if p.is_dir()]
    if not dirs:
        print("No site folders found. Run mirror-sites.ps1 first.")
        return 2
    total = 0
    for folder in sorted(dirs):
        total += check_site(folder)
    print(f"\nTotal missing local targets: {total}")
    return 1 if total else 0

if __name__ == "__main__":
    sys.exit(main())
