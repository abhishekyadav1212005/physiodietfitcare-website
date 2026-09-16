#!/usr/bin/env python3
"""Verification harness for the PhysioDietFitCare static site.

There is no test framework in this repo. This script is it.
Run from the repo root:  python tools/verify_site.py

Six checks, all of which must pass before deploying:
  1. local assets exist          every local href/src resolves on disk
  2. no dummy links              no action="#", href="#", href="", src=""
  3. form fields named           booking form fields all carry name=
  4. legal text verbatim         legal copy matches the client document
  5. nav and footer consistency  every page links to Events and the legal pages
  6. SEO head tags               unique description, canonical, OG, twitter
"""
import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent

LINK_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]*)"', re.I)
TAG_RE = re.compile(r"<[^>]+>")

FORM_RE = re.compile(
    r"<form\b[^>]*class=\"[^\"]*booking-form[^\"]*\"[^>]*>(.*?)</form>", re.I | re.S
)
FIELD_RE = re.compile(r"<(input|select|textarea)\b([^>]*)>", re.I)
NAME_ATTR_RE = re.compile(r'\bname\s*=\s*"[^"]+"', re.I)

# One distinctive sentence from each legal document, exactly as the client's
# requirements document writes it. If a rendered page does not contain it
# verbatim, the copy was paraphrased somewhere.
LEGAL_SENTINELS = {
    "privacy-policy.html": [
        "We do not sell or commercially share your personal information with third parties.",
        "We take reasonable measures to protect your information. However, no internet-based system can be guaranteed to be completely secure.",
        "Last Updated: 15/08/2026",
    ],
    "terms-conditions.html": [
        "By accessing or using the PhysioDietFitCare website or services, you agree to these Terms & Conditions.",
        "PhysioDietFitCare does not guarantee specific treatment outcomes or recovery timelines.",
        "Last Updated: 15/08/2026",
    ],
    "medical-disclaimer.html": [
        "It should not be considered a substitute for an individual medical examination, diagnosis, or professional medical advice.",
        "If you have severe, sudden, worsening, or potentially life-threatening symptoms, seek appropriate medical attention immediately.",
    ],
}

# thank-you.html is a minimal confirmation page with no nav; it only needs
# the legal links in its footer. It is also deliberately noindex.
NAV_EXEMPT = {"thank-you.html"}
SEO_EXEMPT = {"thank-you.html"}

REQUIRED_LEGAL_LINKS = (
    "privacy-policy.html",
    "terms-conditions.html",
    "medical-disclaimer.html",
)


def html_pages(root):
    """Every shipped HTML page, sorted."""
    return sorted(p for p in root.glob("*.html") if p.is_file())


def _is_local(target):
    if not target:
        return False
    skip = ("http://", "https://", "//", "mailto:", "tel:", "#", "data:", "javascript:")
    return not target.startswith(skip)


def _text_of(page):
    """Rendered text of a page: tags stripped, entities resolved, space normalised.

    Entities matter here — the legal sentinels are written the way a reader
    sees them ("Terms & Conditions"), not the way the markup escapes them
    ("Terms &amp; Conditions").
    """
    stripped = TAG_RE.sub(" ", page.read_text(encoding="utf-8", errors="replace"))
    return " ".join(html.unescape(stripped).split())


def check_local_assets_exist(pages, root):
    """Every local href/src resolves to a file that exists on disk."""
    failures = []
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        for raw in LINK_RE.findall(text):
            if not _is_local(raw):
                continue
            target = unquote(urlparse(raw).path)
            if not target:
                continue
            if not (root / target).exists():
                failures.append("%s: missing local target %r" % (page.name, raw))
    return failures


def check_no_dummy_links(pages, root):
    """No placeholder hrefs, srcs or form actions survive anywhere."""
    failures = []
    patterns = [
        (re.compile(r'action\s*=\s*"#"', re.I), 'action="#"'),
        (re.compile(r'href\s*=\s*""', re.I), 'href=""'),
        (re.compile(r'src\s*=\s*""', re.I), 'src=""'),
        (re.compile(r'href\s*=\s*"#"', re.I), 'bare href="#"'),
    ]
    for page in pages:
        lines = page.read_text(encoding="utf-8", errors="replace").splitlines()
        for lineno, line in enumerate(lines, 1):
            for pattern, label in patterns:
                if pattern.search(line):
                    failures.append("%s:%d: %s" % (page.name, lineno, label))
    return failures


def check_form_fields_named(pages, root):
    """Every field inside a .booking-form carries a name, or it submits blank."""
    failures = []
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        for form_index, body in enumerate(FORM_RE.findall(text), 1):
            for tag, attrs in FIELD_RE.findall(body):
                if not NAME_ATTR_RE.search(attrs):
                    snippet = " ".join(attrs.split())[:70]
                    failures.append(
                        "%s: form #%d: <%s> has no name= (%s)" % (page.name, form_index, tag, snippet)
                    )
    return failures


def check_legal_text_verbatim(pages, root):
    """Legal copy is reproduced word for word from the client document."""
    failures = []
    by_name = {p.name: p for p in pages}
    for filename, sentinels in LEGAL_SENTINELS.items():
        page = by_name.get(filename)
        if page is None:
            failures.append("%s: page does not exist" % filename)
            continue
        rendered = _text_of(page)
        for sentinel in sentinels:
            normalised = " ".join(sentinel.split())
            if normalised not in rendered:
                failures.append(
                    "%s: missing verbatim text: %r..." % (filename, normalised[:60])
                )
    return failures


def check_nav_footer_consistency(pages, root):
    """Every page links to Events (in nav) and to all three legal pages."""
    failures = []
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        if page.name not in NAV_EXEMPT and 'href="events.html"' not in text:
            failures.append("%s: no link to events.html" % page.name)
        for target in REQUIRED_LEGAL_LINKS:
            if page.name == target:
                continue  # a page need not link to itself
            if 'href="%s"' % target not in text:
                failures.append("%s: no link to %s" % (page.name, target))
    return failures


def check_seo_head(pages, root):
    """Each indexable page has a unique description, a canonical and OG tags."""
    failures = []
    descriptions = {}
    for page in pages:
        if page.name in SEO_EXEMPT:
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', text, re.I)
        if not match:
            failures.append("%s: no meta description" % page.name)
        else:
            descriptions.setdefault(match.group(1).strip(), []).append(page.name)
        canonical = re.search(
            r'<link\s+rel="canonical"\s+href="https://www\.physiodietfitcare\.com/', text, re.I
        )
        if not canonical:
            failures.append("%s: no canonical pointing at the live origin" % page.name)
        for prop in ("og:title", "og:description", "og:image", "og:url", "og:type"):
            if 'property="%s"' % prop not in text:
                failures.append("%s: missing %s" % (page.name, prop))
        if 'name="twitter:card"' not in text:
            failures.append("%s: missing twitter:card" % page.name)

    for description, owners in descriptions.items():
        if len(owners) > 1:
            failures.append(
                "duplicate meta description across %s: %r..." % (owners, description[:50])
            )
    return failures


CHECKS = [
    ("local assets exist", check_local_assets_exist),
    ("no dummy links", check_no_dummy_links),
    ("form fields named", check_form_fields_named),
    ("legal text verbatim", check_legal_text_verbatim),
    ("nav and footer consistency", check_nav_footer_consistency),
    ("SEO head tags", check_seo_head),
]


def main():
    pages = html_pages(ROOT)
    if not pages:
        print("FAIL  no HTML pages found")
        return 1
    print("Checking %d pages in %s\n" % (len(pages), ROOT))
    total = 0
    for name, check in CHECKS:
        failures = check(pages, ROOT)
        total += len(failures)
        print("%s  %s" % ("PASS" if not failures else "FAIL", name))
        for failure in failures:
            print("        %s" % failure)
    print("\n%d failure(s)" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
