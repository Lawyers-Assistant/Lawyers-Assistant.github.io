#!/usr/bin/env python3
"""
check_docs.py — validate the generated docs website.

Run standalone (python check_docs.py) or import main() from build_docs.py so
the build fails loudly on any regression.

Checks (every generated page + landing + hub):
  1. Meta tags: description, keywords, robots, canonical (never "None", right
     URL), OG set, Twitter set, author, theme-color.
  2. JSON-LD: every doc page has SoftwareApplication, WebSite, Organization,
     BreadcrumbList, FAQPage — each parses as valid JSON with the right @type.
  3. FAQ parity: visible .faq-item count == FAQPage question count, and every
     schema question + answer text appears in the page's visible (non-script)
     HTML.
  4. Link resolution: every internal .html href resolves relative to its own
     page's directory (how a browser resolves it).
  5. Stale output: docs/<slug>.html must be newer than build_docs.py,
     doc_seo.json and its source ../docs/<name>.md; docs.html must be newer
     than all sources (i.e. someone edited docs and forgot to rebuild).
  6. Landing page (index.html): meta + 4 JSON-LD blocks + FAQ parity.

Exit code = number of problems (0 = clean).
"""
import html
import io
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # website/
DOCS_SRC = ROOT.parent / "docs"                 # ../docs
OUT = ROOT / "docs"

REPO_URL = "https://github.com/haal-lab/Lawyer-Assistant"

# JSON-LD types required on every doc page
DOC_LD_TYPES = ["SoftwareApplication", "WebSite", "Organization", "BreadcrumbList", "FAQPage"]
# JSON-LD types required on the landing page
LANDING_LD_TYPES = ["SoftwareApplication", "WebSite", "Organization", "FAQPage"]


# ── helpers ────────────────────────────────────────────────────────────────
def slugify(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()


def doc_slug(filename: str) -> str:
    return slugify(filename[:-3] if filename.endswith(".md") else filename)


def read(p: Path) -> str:
    return io.open(p, encoding="utf-8").read()


def visible_html(raw: str) -> str:
    """HTML with <script> blocks stripped — for FAQ parity checks."""
    return re.sub(r"<script.*?</script>", "", raw, flags=re.S)


def parse_jsonld(raw: str):
    """Return list of parsed JSON-LD dicts; append problems for malformed ones."""
    out, problems = [], []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            out.append(json.loads(block))
        except Exception as e:
            problems.append(f"malformed JSON-LD: {e}")
    return out, problems


def check_meta(raw: str, name: str, problems, is_doc: bool):
    if 'name="description"' not in raw:
        problems.append(f"{name}: missing meta description")
    if 'name="keywords"' not in raw:
        problems.append(f"{name}: missing meta keywords")
    if 'name="robots"' not in raw or "max-image-preview:large" not in raw:
        problems.append(f"{name}: missing/incomplete robots meta")
    if 'name="author"' not in raw:
        problems.append(f"{name}: missing author meta")
    if 'name="theme-color"' not in raw:
        problems.append(f"{name}: missing theme-color")

    m = re.search(r'rel="canonical" href="([^"]+)"', raw)
    if not m:
        problems.append(f"{name}: missing canonical")
    elif "None" in m.group(1):
        problems.append(f"{name}: canonical contains 'None' ({m.group(1)})")
    elif is_doc and not m.group(1).endswith(f"/{name}"):
        problems.append(f"{name}: canonical mismatch ({m.group(1)})")
    elif not is_doc and REPO_URL not in m.group(1):
        problems.append(f"{name}: canonical not under {REPO_URL} ({m.group(1)})")

    for tag in ["og:title", "og:url", "og:image", "og:type", "og:description"]:
        if f'property="{tag}"' not in raw:
            problems.append(f"{name}: missing OG tag {tag}")
    for tag in ["twitter:card", "twitter:title", "twitter:image"]:
        if f'name="{tag}"' not in raw:
            problems.append(f"{name}: missing Twitter tag {tag}")


def check_faq_parity(raw: str, name: str, problems):
    """FAQPage schema must match visible .faq-item blocks exactly."""
    blocks, p = parse_jsonld(raw)
    problems.extend(p)
    faq = next((b for b in blocks if b.get("@type") == "FAQPage"), None)
    if faq is None:
        problems.append(f"{name}: missing FAQPage schema")
        return
    entities = faq.get("mainEntity", [])
    schema_qs = [q.get("name", "") for q in entities]
    visible_count = raw.count('class="faq-item"')
    if visible_count != len(schema_qs):
        problems.append(
            f"{name}: visible FAQ items ({visible_count}) != FAQPage questions ({len(schema_qs)})"
        )
    # Normalize typographic quotes + HTML entities so curly/straight and
    # entity differences never false-fail; real wording drift still trips it.
    _QMAP = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-'})
    def _norm(x):
        return html.unescape(x).translate(_QMAP)
    vis = _norm(visible_html(raw))
    for q in schema_qs:
        if not q:
            problems.append(f"{name}: FAQPage question with empty name")
            continue
        if _norm(q) not in vis:
            problems.append(f"{name}: schema question not visible on page: {q[:50]}")
    for q in entities:
        ans = q.get("acceptedAnswer", {}).get("text", "")
        if not ans:
            problems.append(f"{name}: FAQPage question '{q.get('name','')[:40]}' has empty answer")
        elif _norm(ans) not in vis:
            problems.append(f"{name}: schema answer not visible on page: {ans[:50]}")


def check_ld_types(raw: str, name: str, required, problems):
    blocks, p = parse_jsonld(raw)
    problems.extend(p)
    types = [b.get("@type") for b in blocks]
    for t in required:
        if t not in types:
            problems.append(f"{name}: missing {t} JSON-LD block (have {sorted(set(types))})")


def check_markdown_leaks(raw: str, name: str, problems):
    """Unrendered markdown in visible text (outside <pre>/<code>/<style>). This
    is the exact regression class the docs generator was repaired for, so it
    must never silently come back."""
    body = re.sub(r"<pre.*?</pre>", "", raw, flags=re.S)
    body = re.sub(r"<code.*?</code>", "", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    body = visible_html(body)
    if "**" in body:
        problems.append(f"{name}: unrendered **bold** markers in visible text")
    if "`" in body:
        problems.append(f"{name}: unrendered backtick markers in visible text")
    m = re.search(r"\[[^\]]+\]\([^)]*\)", body)
    if m:
        problems.append(f"{name}: unrendered [text](url) markdown link: {m.group(0)[:50]}")


def check_links(raw: str, name: str, base: str, problems):
    for m in re.finditer(r'href="([^"]+\.html[^"]*)"', raw):
        href = m.group(1).split("#")[0]
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        target = os.path.normpath(os.path.join(base, href))
        if not os.path.isfile(target):
            problems.append(f"{name}: broken link → {href}")


# ── per-page checks ─────────────────────────────────────────────────────────
def check_doc_page(path: Path, problems):
    name = path.name
    raw = read(path)
    check_meta(raw, name, problems, is_doc=True)
    check_ld_types(raw, name, DOC_LD_TYPES, problems)
    check_faq_parity(raw, name, problems)
    check_markdown_leaks(raw, name, problems)
    check_links(raw, name, str(path.parent), problems)


def check_landing(problems):
    path = ROOT / "index.html"
    if not path.exists():
        problems.append("index.html: missing")
        return
    name = "index.html"
    raw = read(path)
    check_meta(raw, name, problems, is_doc=False)
    check_ld_types(raw, name, LANDING_LD_TYPES, problems)
    check_faq_parity(raw, name, problems)
    check_links(raw, name, str(ROOT), problems)


def check_hub(problems):
    path = ROOT / "docs.html"
    if not path.exists():
        problems.append("docs.html: missing")
        return
    name = "docs.html"
    raw = read(path)
    check_meta(raw, name, problems, is_doc=False)
    check_ld_types(raw, name, ["SoftwareApplication", "WebSite", "Organization"], problems)
    check_links(raw, name, str(ROOT), problems)
    if raw.count('class="doc-card"') != len(list(DOCS_SRC.glob("*.md"))):
        problems.append(f"docs.html: doc-card count != number of source docs")


def check_stale(problems):
    """Generated output must be newer than the generator + its inputs."""
    gen_mtime = max(
        ROOT.joinpath("build_docs.py").stat().st_mtime,
        ROOT.joinpath("doc_seo.json").stat().st_mtime,
    )
    # map source slug → md path
    src_by_slug = {doc_slug(f.name): f for f in DOCS_SRC.glob("*.md")}
    for slug, md in src_by_slug.items():
        out_file = OUT / f"{slug}.html"
        if not out_file.exists():
            problems.append(f"docs/{slug}.html: missing (source {md.name} not built?)")
            continue
        if out_file.stat().st_mtime < max(gen_mtime, md.stat().st_mtime):
            problems.append(
                f"docs/{slug}.html: STALE — source {md.name} or the generator is newer; run build_docs.py"
            )
    # hub depends on every source
    hub = ROOT / "docs.html"
    newest_src = max((f.stat().st_mtime for f in DOCS_SRC.glob("*.md")), default=0)
    if hub.exists() and hub.stat().st_mtime < max(gen_mtime, newest_src):
        problems.append("docs.html: STALE — a source doc changed; run build_docs.py")
    # landing page depends on nothing generated, but must exist
    if not (ROOT / "index.html").exists():
        problems.append("index.html: missing")
    for geo in ["llms.txt", "robots.txt", "sitemap.xml"]:
        if not (ROOT / geo).exists():
            problems.append(f"{geo}: missing GEO file")


# ── entry ───────────────────────────────────────────────────────────────────
def main() -> int:
    problems: list[str] = []

    check_landing(problems)
    check_hub(problems)

    pages = sorted(OUT.glob("*.html"))
    if not pages:
        problems.append("no generated doc pages found (docs/*.html missing)")
    for p in pages:
        check_doc_page(p, problems)

    check_stale(problems)

    print(f"check_docs.py — validating {len(pages)} doc pages + docs.html + index.html")
    if problems:
        for x in problems:
            print(f"  ✗ {x}")
        print(f"FAILED: {len(problems)} problem(s).")
        return min(len(problems), 255)
    print("  ✓ all checks passed — meta, JSON-LD, FAQ parity, links, freshness")
    return 0


if __name__ == "__main__":
    sys.exit(main())
