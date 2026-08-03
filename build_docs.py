#!/usr/bin/env python3
"""
build_docs.py — convert ../docs/*.md into styled HTML pages for the website.

Outputs:
  website/docs.html              — hub: grouped index of every document
  website/docs/<slug>.html       — one styled page per markdown doc

Self-contained: no external packages (plain stdlib). The doc pages embed the
same "chambers" design tokens as the landing page (index.html) so the docs
feel like part of the site.
"""
import html
import io
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # website/
DOCS_SRC = ROOT.parent / "docs"                 # ../docs
OUT = ROOT / "docs"

REPO_URL = "https://github.com/haal-lab/Lawyer-Assistant"
# Where the site will be deployed. Canonicals/OG/sitemap point here; swap to the
# real production domain once the site is hosted (keep the trailing path off).
SITE_URL = REPO_URL

# ─────────────────────────────────────────────────────────────
# Grouping for the hub + sidebar (order matters)
# ─────────────────────────────────────────────────────────────
GROUPS = [
    ("🚀 Getting started", [
        "QUICKSTART", "DEVELOPMENT", "TESTING", "BENCHMARKING",
        "CONFIGURATION", "DEPLOYMENT",
    ]),
    ("🏛️ Architecture & core", [
        "ARCHITECTURE", "BACKEND", "FRONTEND", "DATA_FLOW", "CHATBOT_FLOW",
        "PIPELINE_EDITOR", "PIPELINE_JSON", "PIPELINE_ROADMAP",
    ]),
    ("🖥️ GPU & performance", [
        "GPU_MANAGEMENT",
    ]),
    ("☁️ API & launcher", [
        "API_PROVIDER", "LAUNCHER", "CLI_TOOLS",
    ]),
    ("🔒 Security & storage", [
        "SECURITY", "STORAGE", "WORKSPACE", "TROUBLESHOOTING",
    ]),
    ("📚 Reference", [
        "GLOSSARY", "AGENT_KNOWLEDGE_BASE", "CHANGELOG", "README",
        "UI_BRAINSTORM", "chatbot-ui-design",
    ]),
]

# Short one-line descriptions for the hub cards
BLURBS = {
    "QUICKSTART": "Clone → install → run → first query → verify",
    "DEVELOPMENT": "Dev environment, hot reload, debugging, profiling",
    "TESTING": "Test suite, fixtures, running the tests",
    "BENCHMARKING": "Performance benchmarks & metrics",
    "CONFIGURATION": "Every environment variable & setting",
    "DEPLOYMENT": "Production deployment & hardening",
    "ARCHITECTURE": "System overview, ports, runtime modes",
    "BACKEND": "FastAPI endpoints, routers, tools, retrieval, scan",
    "FRONTEND": "React layout, stores, streaming, theming",
    "DATA_FLOW": "Document ingestion: parse → chunk → embed → index",
    "CHATBOT_FLOW": "Message → intent → tools → rerank → LLM → answer",
    "PIPELINE_EDITOR": "Visual canvas, sub-nodes, toggles, bypass",
    "PIPELINE_JSON": "Exact JSON schema for pipeline layouts",
    "PIPELINE_ROADMAP": "Planned improvements to the RAG pipeline",
    "GPU_MANAGEMENT": "VRAM sharing, RAM-first residency, auto-tuning",
    "API_PROVIDER": "Cloud mode, providers, env vars, rerank modes",
    "LAUNCHER": "Setup page internals, provider picker, Ollama automation",
    "CLI_TOOLS": "Command-line helpers for ingestion & queries",
    "SECURITY": "CSP, Electron sandbox, key handling, threat model",
    "STORAGE": "Where every piece of data lives",
    "WORKSPACE": "Project folders & the workspace model",
    "TROUBLESHOOTING": "12 failure scenarios with exact fixes",
    "GLOSSARY": "One-line definitions of every term",
    "AGENT_KNOWLEDGE_BASE": "Fast Q&A for AI agents & developers",
    "CHANGELOG": "Recent feature history",
    "README": "The documentation index itself",
    "UI_BRAINSTORM": "Design explorations & future UI ideas",
    "chatbot-ui-design": "Chat UI design notes",
}

# ─────────────────────────────────────────────────────────────
# Per-doc SEO: hand-written meta descriptions, keywords, and FAQ
# Q&A (AEO/GEO blocks) loaded from doc_seo.json. Each doc page
# renders these + JSON-LD schema (SoftwareApplication, WebSite,
# Organization, BreadcrumbList, FAQPage).
# ─────────────────────────────────────────────────────────────
DOC_SEO = json.loads((ROOT / "doc_seo.json").read_text(encoding="utf-8"))

PAGE_CSS = """
:root{
  --ink:#0b110e; --ink-2:#101a15; --panel:#14201a; --panel-2:#18261f;
  --line:#23352c; --line-bright:#33503f; --paper:#f3ecdd; --paper-dim:#c9bfa9;
  --muted:#93a89c; --faint:#5d7267; --brass:#c9a35c; --brass-2:#e0c088;
  --oxblood:#a33d2e; --oxblood-2:#c65a47; --sage:#6fae8f;
  --font-d:"Fraunces",Georgia,serif; --font-s:"IBM Plex Sans",system-ui,sans-serif;
  --font-m:"IBM Plex Mono",ui-monospace,monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--paper);font-family:var(--font-s);line-height:1.7;-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0;z-index:-2;background:radial-gradient(1000px 480px at 85% -10%,rgba(201,163,92,.09),transparent 60%)}
body::after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.045;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E")}
::selection{background:var(--brass);color:var(--ink)}
a{color:var(--brass-2);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1240px;margin:0 auto;padding:0 26px}

/* nav */
nav{position:sticky;top:0;z-index:50;background:rgba(11,17,14,.85);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;justify-content:space-between;height:62px;gap:16px}
.brand{display:flex;align-items:center;gap:11px;font-family:var(--font-d);font-size:1.14rem;color:var(--paper)}
.brand img{width:28px;height:28px}
.brand .dot{color:var(--brass)}
.nav-links{display:flex;gap:24px;font-size:13.5px;color:var(--paper-dim)}
.nav-links a{padding:4px 0;color:var(--paper-dim)}
.nav-links a:hover{color:var(--brass-2);text-decoration:none}
.nav-links .active{color:var(--brass-2)}

/* layout */
.doc-grid{display:grid;grid-template-columns:260px minmax(0,1fr);gap:44px;padding:40px 0 70px;align-items:start}
.sidebar{position:sticky;top:86px;max-height:calc(100vh - 110px);overflow-y:auto;padding-right:8px;scrollbar-width:thin}
.sidebar::-webkit-scrollbar{width:5px}
.sidebar::-webkit-scrollbar-thumb{background:var(--line-bright);border-radius:99px}
.side-group{margin-bottom:20px}
.side-title{font-family:var(--font-m);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--faint);margin-bottom:7px}
.side-link{display:block;font-size:12.5px;color:var(--muted);padding:4px 10px;border-radius:6px;border-left:2px solid transparent;transition:all .15s ease}
.side-link:hover{color:var(--paper);background:var(--panel);text-decoration:none}
.side-link.active{color:var(--brass-2);border-left-color:var(--brass);background:var(--panel)}

/* article */
article.doc{min-width:0}
.crumb{font-family:var(--font-m);font-size:11px;letter-spacing:.12em;color:var(--faint);margin-bottom:20px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.crumb a{color:var(--muted)}
.crumb a:hover{color:var(--brass-2)}
.doc h1{font-family:var(--font-d);font-weight:500;font-size:clamp(1.9rem,4vw,2.7rem);line-height:1.15;letter-spacing:-.01em;margin:8px 0 18px}
.doc .doc-intro{color:var(--paper-dim);font-size:1.05rem;margin-bottom:30px;max-width:70ch}
.doc h2{font-family:var(--font-d);font-weight:500;font-size:1.55rem;margin:42px 0 14px;padding-top:18px;border-top:1px solid var(--line);letter-spacing:-.01em}
.doc h3{font-family:var(--font-d);font-weight:500;font-size:1.22rem;margin:30px 0 10px;color:var(--brass-2)}
.doc h4{font-size:1rem;margin:24px 0 8px;color:var(--paper);font-family:var(--font-d);font-weight:500}
.doc p{margin:0 0 16px;color:var(--paper-dim);font-size:15px}
.doc strong{color:var(--paper);font-weight:600}
.doc em{color:var(--brass-2)}
.doc a{text-decoration:underline;text-underline-offset:2px;text-decoration-color:rgba(201,163,92,.35)}
.doc a:hover{text-decoration-color:var(--brass)}
.doc ul,.doc ol{margin:0 0 16px;padding-left:26px;color:var(--paper-dim);font-size:15px}
.doc li{margin:5px 0}
.doc li::marker{color:var(--brass)}
.doc hr{border:none;border-top:1px solid var(--line);margin:34px 0}
.doc blockquote{border-left:3px solid var(--brass);background:var(--panel);padding:14px 18px;border-radius:0 10px 10px 0;margin:0 0 18px;color:var(--paper-dim)}
.doc blockquote p{margin:0 0 6px}
.doc blockquote p:last-child{margin:0}
.doc code{font-family:var(--font-m);font-size:12.5px;background:var(--panel-2);border:1px solid var(--line);border-radius:5px;padding:1.5px 6px;color:var(--brass-2)}
.doc pre{background:#070c09;border:1px solid var(--line);border-radius:12px;padding:18px 20px;overflow-x:auto;margin:0 0 20px;position:relative}
.doc pre code{background:none;border:none;padding:0;color:#cfe3d4;font-size:12.5px;line-height:1.65;display:block}
.doc pre .lang{position:absolute;top:10px;right:14px;font-family:var(--font-m);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint)}
.doc table{border-collapse:collapse;width:100%;margin:0 0 22px;font-size:13.5px;display:block;overflow-x:auto}
.doc th,.doc td{border:1px solid var(--line);padding:9px 13px;text-align:left;vertical-align:top}
.doc th{background:var(--panel);font-family:var(--font-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--brass-2)}
.doc td{color:var(--paper-dim)}
.doc tr:nth-child(even) td{background:rgba(255,255,255,.015)}
.doc td code,.doc th code{font-size:11.5px}
.doc img{max-width:100%;border-radius:10px;border:1px solid var(--line)}

/* search */
.doc-search{position:relative;max-width:540px;margin:28px auto 6px}
.doc-search input{width:100%;padding:13px 46px 13px 40px;font-family:var(--font-s);font-size:14px;color:var(--paper);background:var(--panel);border:1px solid var(--line-bright);border-radius:999px;outline:none;transition:border-color .2s ease,box-shadow .2s ease}
.doc-search input:focus{border-color:var(--brass);box-shadow:0 0 0 3px rgba(201,163,92,.15)}
.doc-search input::placeholder{color:var(--faint)}
.doc-search input::-webkit-search-cancel-button{display:none}
.s-ico{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:15px;height:15px;stroke:var(--faint);pointer-events:none}
.s-clear{position:absolute;right:8px;top:50%;transform:translateY(-50%);width:28px;height:28px;display:none;align-items:center;justify-content:center;border:none;border-radius:50%;background:var(--panel-2);color:var(--muted);cursor:pointer;font-size:12px;transition:color .15s,background .15s}
.s-clear.show{display:flex}
.s-clear:hover{color:var(--paper);background:var(--line)}
.search-meta{font-family:var(--font-m);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);min-height:20px;margin-top:10px}
.search-meta b{color:var(--brass-2)}
.search-empty{font-size:13px;color:var(--muted);letter-spacing:0;text-transform:none;padding:30px 0}
mark{background:rgba(201,163,92,.3);color:var(--brass-2);border-radius:3px;padding:0 2px}

/* hub */
.hub-hero{padding:70px 0 30px;text-align:center}
.hub-hero h1{font-family:var(--font-d);font-weight:500;font-size:clamp(2rem,4.6vw,3.2rem);margin:18px 0 14px;line-height:1.12}
.hub-hero .lead{color:var(--paper-dim);max-width:62ch;margin:0 auto;font-size:1.05rem}
.hub-count{font-family:var(--font-m);font-size:11px;letter-spacing:.18em;color:var(--faint);text-transform:uppercase;margin-top:16px}
.group{margin-bottom:46px}
.group-head{display:flex;align-items:center;gap:12px;margin-bottom:18px}
.group-head h2{font-family:var(--font-d);font-weight:500;font-size:1.3rem;color:var(--paper)}
.group-head::after{content:"";flex:1;height:1px;background:var(--line)}
.docs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.doc-card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 18px 16px;transition:transform .24s ease,border-color .24s ease,background .24s ease;display:flex;flex-direction:column;gap:8px}
.doc-card:hover{transform:translateY(-4px);border-color:var(--line-bright);background:var(--panel-2)}
.doc-card .d-name{font-family:var(--font-d);font-size:1.06rem;color:var(--paper)}
.doc-card .d-blurb{font-size:12.5px;color:var(--muted);flex:1}
.doc-card .d-file{font-family:var(--font-m);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}

/* footer */
footer{border-top:1px solid var(--line);padding:40px 0 34px;background:var(--ink-2)}
.foot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:center}
.foot-brand{display:flex;align-items:center;gap:9px;font-family:var(--font-d);font-size:1rem;color:var(--paper)}
.foot-brand img{width:22px;height:22px}
.foot-links{display:flex;gap:22px;font-size:13px;color:var(--muted);flex-wrap:wrap}
.foot-links a{color:var(--muted)}
.foot-links a:hover{color:var(--brass-2);text-decoration:none}
.foot-note{width:100%;text-align:center;font-family:var(--font-m);font-size:10.5px;color:var(--faint);margin-top:28px}

@media(max-width:1020px){.docs-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:860px){
  .doc-grid{grid-template-columns:1fr;gap:20px}
  .sidebar{position:static;max-height:none;display:flex;flex-wrap:wrap;gap:8px 20px;padding:0 0 6px}
  .side-group{display:contents}
  .side-title{display:none}
  .side-link{font-size:11px;padding:2px 8px;border-left:none;border-bottom:1px solid transparent}
  .side-link.active{border-left:none;border-bottom-color:var(--brass)}
  .nav-links{display:none}
}
@media(max-width:640px){
  .docs-grid{grid-template-columns:1fr}
  .wrap{padding:0 16px}
  .doc pre{padding:14px}
  .doc h2{font-size:1.3rem}
}

/* FAQ (AEO blocks) on doc pages */
.doc-faq{margin-top:56px;padding-top:34px;border-top:1px solid var(--line)}
.doc-faq h2{font-family:var(--font-d);font-weight:500;font-size:1.5rem;margin:0 0 6px;padding:0;border:none}
.doc-faq .sub{color:var(--faint);font-size:13px;margin-bottom:22px}
.faq-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.faq-item{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px}
.faq-item h3{font-family:var(--font-d);font-size:1.02rem;color:var(--paper);margin:0 0 8px;font-weight:500}
.faq-item p{font-size:13.5px;color:var(--muted);margin:0;line-height:1.65}
@media(max-width:860px){.faq-grid{grid-template-columns:1fr}}

@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto}}
"""


# ─────────────────────────────────────────────────────────────
# Slug helpers
# ─────────────────────────────────────────────────────────────
def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return s


def doc_slug(filename: str) -> str:
    return slugify(filename[:-3] if filename.endswith(".md") else filename)


# ─────────────────────────────────────────────────────────────
# Minimal markdown → HTML converter (GFM subset)
# ─────────────────────────────────────────────────────────────
INLINE_RE = [
    (re.compile(r"`([^`]+)`"), lambda m: f'<code>{m.group(1)}</code>'),
    (re.compile(r"\*\*(.+?)\*\*"), lambda m: f"<strong>{m.group(1)}</strong>"),
    (re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)"), lambda m: f"<em>{m.group(1)}</em>"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def fix_link(url: str, from_doc: str) -> str:
    """Rewrite .md links to .html; absolute links pass through."""
    url = url.strip()
    if url.startswith(("http://", "https://", "#", "mailto:")):
        return url
    if "://" in url:
        return url
    # strip anchor
    anchor = ""
    if "#" in url:
        url, anchor = url.split("#", 1)
        anchor = "#" + anchor
    if url.endswith(".md"):
        name = url[:-3]
        # handle ../ or ./ prefixes + subdirectories
        base = os.path.basename(name)
        return f"{doc_slug(base)}.html{anchor}" if base else url + anchor
    if url.endswith((".png", ".jpg", ".gif", ".svg", ".webp")):
        return url
    # relative to docs dir (no extension) — assume it's a doc link
    if "/" not in url and not url.startswith((".", "assets")):
        return f"{doc_slug(url)}.html{anchor}"
    return url + anchor


def inline(s: str, from_doc: str) -> str:
    s = esc(s)
    # links first so link text doesn't get mangled
    def link_repl(m):
        txt = m.group(1)
        url = m.group(2)
        if url.startswith("http"):
            return f'<a href="{esc(url)}" target="_blank" rel="noopener">{txt}</a>'
        return f'<a href="{esc(fix_link(url, from_doc))}">{txt}</a>'
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link_repl, s)
    for pat, rep in INLINE_RE:
        s = pat.sub(rep, s)
    return s


def render_table(lines: list, from_doc: str) -> str:
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return "<p>" + inline(" ".join(lines), from_doc) + "</p>"
    out = ["<table>"]
    out.append("<thead><tr>" + "".join(f"<th>{inline(c, from_doc)}</th>" for c in rows[0]) + "</tr></thead>")
    body = rows[2:] if re.match(r"^[\s:\-|]+$", "|".join(rows[1]).replace(" ", "")) else rows[1:]
    out.append("<tbody>")
    for r in body:
        while len(r) < len(rows[0]):
            r.append("")
        out.append("<tr>" + "".join(f"<td>{inline(c, from_doc)}</td>" for c in r[:len(rows[0])]) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)



def render_list(items: list, from_doc: str) -> str:
    """Render (indent, ordered, text) list items as properly nested <ul>/<ol>.

    Items with a deeper indent become children of the previous item. Soft-wrapped
    continuation text is already joined into each item's text by the caller.
    """
    if not items:
        return ""
    idx, n = 0, len(items)
    lis: list[str] = []
    while idx < n:
        indent, ordered, text = items[idx]
        parts = ["<li>", inline(text, from_doc)]
        j = idx + 1
        children = []
        while j < n and items[j][0] > indent:
            children.append(items[j])
            j += 1
        if children:
            parts.append(render_list(children, from_doc))
        parts.append("</li>")
        lis.append("".join(parts))
        idx = j
    tag = "ol" if items[0][1] else "ul"
    return f"<{tag}>" + "".join(lis) + f"</{tag}>"


def markdown_to_html(md: str, from_doc: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i, n = 0, len(lines)

    while i < n:
        ln = lines[i]

        # fenced code block (fences may be indented inside list items)
        mf = re.match(r"^\s*(```+)", ln)
        if mf:
            fence = mf.group(1)
            lang = ln[mf.end():].strip()
            buf = []
            i += 1
            while i < n and not re.match(rf"^\s*{re.escape(fence)}", lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            lang_badge = f'<span class="lang">{esc(lang)}</span>' if lang else ""
            out.append(f"<pre>{lang_badge}<code>{esc(chr(10).join(buf))}</code></pre>")
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            out.append(f"<h{level} id=\"{slugify(re.sub(r'<[^>]+>', '', inline(text, from_doc)))}\">{inline(text, from_doc)}</h{level}>")
            i += 1
            continue

        # horizontal rule
        if re.match(r"^(\s*([-*_])\s*){3,}$", ln) and not ln.startswith(" "):
            out.append("<hr/>")
            i += 1
            continue

        # table block
        if ln.lstrip().startswith("|") and i + 1 < n:
            sep = lines[i + 1].strip()
            if "-" in sep and re.match(r"^[\s|:\-]+$", sep):
                buf = [ln]
                i += 1
                while i < n and lines[i].lstrip().startswith("|"):
                    buf.append(lines[i])
                    i += 1
                out.append(render_table(buf, from_doc))
                continue

        # blockquote
        if ln.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(lines[i][1:].lstrip() if lines[i].startswith("> ") else lines[i][1:])
                i += 1
            out.append("<blockquote>" + inline(" ".join(buf), from_doc) + "</blockquote>")
            continue

        # lists
        if re.match(r"^\s*([-*+]|\d+\.)\s+", ln):
            items: list = []
            while i < n:
                nxt = lines[i]
                m2 = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", nxt)
                if not m2:
                    # blank line between items — skip it if more list items follow
                    if not nxt.strip():
                        j = i
                        while j < n and not lines[j].strip():
                            j += 1
                        if j < n and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[j]):
                            i = j
                            continue
                    break
                indent = len(m2.group(1))
                ordered = bool(re.match(r"^\s*\d+\.", m2.group(2)))
                text_parts = [m2.group(3)]
                i += 1
                # soft-wrapped continuation lines (indented deeper than the marker)
                while i < n:
                    nxt2 = lines[i]
                    if not nxt2.strip():
                        break
                    if re.match(r"^\s*([-*+]|\d+\.)\s+", nxt2):
                        break
                    if re.match(r"^(```|>|#{1,6}\s|\|)", nxt2.lstrip()):
                        break
                    if len(nxt2) - len(nxt2.lstrip()) <= indent:
                        break
                    text_parts.append(nxt2.strip())
                    i += 1
                items.append((indent, ordered, " ".join(text_parts)))
            out.append(render_list(items, from_doc))
            continue

        # blank line
        if not ln.strip():
            i += 1
            continue

        # paragraph (gather until blank or a block start)
        buf = [ln]
        i += 1
        while i < n:
            nxt = lines[i]
            if not nxt.strip() or re.match(r"^(#{1,6}\s|\s*```|>\s?|\s*([-*+]|\d+\.)\s+|\[)", nxt) or nxt.lstrip().startswith("|"):
                break
            buf.append(nxt)
            i += 1
        out.append("<p>" + inline(" ".join(buf), from_doc) + "</p>")

    return "\n".join(out)


# ─────────────────────────────────────────────────────────────
# Page shell
# ─────────────────────────────────────────────────────────────
def page_shell(title: str, body: str, active_doc: str | None, prefix: str = "", desc: str = "", seo: dict | None = None) -> str:
    seo = seo or {}
    keywords = seo.get("keywords", "")
    faq = seo.get("faq", [])
    if active_doc:
        canonical = f"{REPO_URL}/docs/{active_doc}.html"
        og_url = canonical
    else:
        canonical = f"{REPO_URL}/docs.html"
        og_url = f"{REPO_URL}/docs.html"

    # ── JSON-LD: app + website + org (same as landing) ──
    ld_app = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Lawyer Assistant",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Windows, macOS, Linux",
  "description": "Lawyer Assistant is a free, local-first legal research desktop app. Ask questions in plain English and get answers with citations you can verify, from your own legal documents — fully private and offline.",
  "url": "https://github.com/haal-lab/Lawyer-Assistant",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
  "featureList": [
    "Cited answers from your own documents",
    "Hybrid search (BM25 + dense vectors + reranking)",
    "Compliance playbook scan",
    "Visual pipeline editor",
    "Local models or your own API (Claude, ChatGPT, Groq, DeepSeek, Mistral, Gemini and more)",
    "Works 100% offline",
    "Open source"
  ],
  "author": {"@type": "Organization", "name": "Haal Lab", "url": "https://github.com/haal-lab"},
  "creator": {"@type": "Person", "name": "Hussain Nazary", "jobTitle": "AI Engineer"}
}
</script>"""
    ld_site = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Lawyer Assistant",
  "url": "https://github.com/haal-lab/Lawyer-Assistant",
  "description": "Free, local-first legal research AI. Cited answers from your own documents — private and offline.",
  "publisher": {"@type": "Organization", "name": "Haal Lab", "url": "https://github.com/haal-lab"}
}
</script>"""
    ld_org = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Haal Lab",
  "url": "https://github.com/haal-lab",
  "brand": "Lawyer Assistant",
  "founder": {"@type": "Person", "name": "Hussain Nazary", "jobTitle": "AI Engineer"},
  "knowsAbout": ["legal research", "retrieval-augmented generation", "local AI", "legal technology"]
}
</script>"""

    # ── JSON-LD: BreadcrumbList (per doc) ──
    if active_doc:
        ld_bread = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Docs", "item": "%s/docs.html"},
    {"@type": "ListItem", "position": 2, "name": "%s", "item": "%s/docs/%s.html"}
  ]
}
</script>""" % (REPO_URL, esc(title), REPO_URL, active_doc)
    else:
        ld_bread = ""

    # ── JSON-LD: FAQPage (per doc, hand-written Q&A) ──
    if faq:
        main_entity = []
        for q, a in faq:
            main_entity.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            })
        ld_faq = ('<script type="application/ld+json">' +
                  json.dumps({
                      "@context": "https://schema.org",
                      "@type": "FAQPage",
                      "mainEntity": main_entity,
                  }, ensure_ascii=False) +
                  '</script>')
    else:
        ld_faq = ""

    meta_extra = ""
    if keywords:
        meta_extra += f'<meta name="keywords" content="{esc(keywords)}"/>\n'
    meta_extra += f'<meta name="author" content="Haal Lab"/>\n'
    meta_extra += f'<meta name="theme-color" content="#0b110e"/>\n'

    nav_links = "".join(
        f'<a href="{prefix}index.html">Home</a><a href="{prefix}docs.html" class="active">Docs</a>'
        f'<a href="{REPO_URL}" target="_blank" rel="noopener">GitHub</a>'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{esc(title)} — Lawyer Assistant Docs</title>
<meta name="description" content="{esc(desc) or 'Documentation for Lawyer Assistant — a local-first legal research desktop app. Guides for quickstart, architecture, backend API, frontend, providers, launcher, security and troubleshooting.'}"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<link rel="canonical" href="{canonical}"/>
{meta_extra}<meta property="og:type" content="article"/>
<meta property="og:site_name" content="Lawyer Assistant"/>
<meta property="og:title" content="{esc(title)} — Lawyer Assistant Docs"/>
<meta property="og:description" content="{esc(desc) or 'Documentation for Lawyer Assistant.'}"/>
<meta property="og:url" content="{og_url}"/>
<meta property="og:image" content="https://github.com/haal-lab/Lawyer-Assistant/raw/main/website/assets/Screen.png"/>
<meta property="og:locale" content="en_US"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{esc(title)} — Lawyer Assistant Docs"/>
<meta name="twitter:description" content="{esc(desc) or 'Documentation for Lawyer Assistant.'}"/>
<meta name="twitter:image" content="https://github.com/haal-lab/Lawyer-Assistant/raw/main/website/assets/Screen.png"/>
<link rel="icon" type="image/svg+xml" href="{prefix}assets/icon.svg"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>{PAGE_CSS}</style>
{ld_app}
{ld_site}
{ld_org}
{ld_bread}
{ld_faq}
</head>
<body>
<nav><div class="wrap nav-in">
  <a class="brand" href="{prefix}index.html"><img src="{prefix}assets/icon.svg" alt="Lawyer Assistant logo"/>Lawyer Assistant<span class="dot">.</span></a>
  <div class="nav-links">{nav_links}</div>
</div></nav>
{body}
<footer><div class="wrap foot">
  <div class="foot-brand"><img src="{prefix}assets/icon.svg" alt="Lawyer Assistant logo"/>Lawyer Assistant<span style="color:var(--brass)">.</span></div>
  <div class="foot-links">
    <a href="{prefix}index.html">Home</a><a href="{prefix}docs.html">Docs</a>
    <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub</a>
    <a href="{REPO_URL}/issues" target="_blank" rel="noopener">Report an issue</a>
  </div>
  <p class="foot-note">© 2026 Lawyer Assistant · Local-first legal research · Free &amp; open source</p>
</div></footer>
</body>
</html>
"""




def sidebar_html(active_doc: str | None) -> str:
    groups = []
    for gtitle, names in GROUPS:
        links = []
        for name in names:
            slug = doc_slug(name)
            label = name.replace("-", " ").replace("_", " ").title()
            if name == "README":
                label = "Docs index"
            cls = "side-link active" if slug == active_doc else "side-link"
            links.append(f'<a class="{cls}" href="{slug}.html">{esc(label)}</a>')
        groups.append(
            f'<div class="side-group"><div class="side-title">{esc(gtitle)}</div>{"".join(links)}</div>'
        )
    return "".join(groups)


def title_from_md(md: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else None

def strip_text(md: str) -> str:
    """Plain-lowercased text of a doc for the search index."""
    s = re.sub(r"```.*?```", " ", md, flags=re.S)
    s = re.sub(r"`([^`]+)`", r"", s)
    s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"", s)
    s = re.sub(r"[#>*_|]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()


# ─────────────────────────────────────────────────────────────
# Build
# ─────────────────────────────────────────────────────────────
def build():
    OUT.mkdir(exist_ok=True)

    docs: dict[str, dict] = {}
    for f in sorted(DOCS_SRC.glob("*.md")):
        slug = doc_slug(f.name)
        md = f.read_text(encoding="utf-8-sig")
        title = title_from_md(md) or f.stem.replace("_", " ").title()
        docs[slug] = {"file": f.name, "title": title, "md": md}

    # ── per-doc pages ──
    for slug, d in docs.items():
        body_html = markdown_to_html(d["md"], slug)
        # intro = first paragraph after the title
        intro_m = re.search(r"<p>(.*?)</p>", body_html, re.S)
        intro = intro_m.group(1) if intro_m else ""
        # drop the markdown's own H1 + the intro paragraph (template renders both)
        body_html = re.sub(r"<p>(.*?)</p>", "", body_html, count=1, flags=re.S)
        body_html = re.sub(r"<h1[^>]*>.*?</h1>", "", body_html, count=1, flags=re.S)
        body = f"""
<div class="wrap doc-grid">
  <aside class="sidebar">{sidebar_html(slug)}</aside>
  <article class="doc">
    <div class="crumb"><a href="../docs.html">📚 Docs</a> <span style="color:var(--faint)">/</span> <span>{esc(d["title"])}</span></div>
    <h1>{esc(d["title"])}</h1>
    <div class="doc-intro">{intro}</div>
    {body_html}
  </article>
</div>"""
        out_file = OUT / f"{slug}.html"
        blurb = BLURBS.get(d["file"][:-3], "") or BLURBS.get(slug.upper(), "")
        seo = DOC_SEO.get(slug, {})
        faq = seo.get("faq", [])
        if faq:
            faq_blocks = "".join(
                f'<div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in faq
            )
            body += f"""
<div class="doc-faq">
  <h2>Questions, answered</h2>
  <p class="sub">Short, self-contained answers about this guide.</p>
  <div class="faq-grid">{faq_blocks}</div>
</div>"""
        out_file.write_text(
            page_shell(d["title"], body, slug, prefix="../",
                       desc=seo.get("desc") or blurb, seo=seo),
            encoding="utf-8",
        )
        print(f"  ✓ docs/{slug}.html")

    # ── hub ──
    groups_html = []
    search_index = {}
    for gtitle, names in GROUPS:
        cards = []
        for name in names:
            slug = doc_slug(name)
            if slug not in docs:
                continue
            d = docs[slug]
            blurb = BLURBS.get(name, "")
            cards.append(
                f'<a class="doc-card" href="docs/{slug}.html" data-slug="{esc(slug)}" '
                f'data-title="{esc(d["title"])}" data-blurb="{esc(blurb)}">'
                f'<span class="d-name">{esc(d["title"])}</span>'
                f'<span class="d-blurb">{esc(blurb)}</span>'
                f'<span class="d-file">{esc(d["file"])}</span></a>'
            )
            search_index[slug] = {"t": d["title"], "b": blurb, "x": strip_text(d["md"])}
        groups_html.append(
            f'<div class="group"><div class="group-head"><h2>{esc(gtitle)}</h2></div>'
            f'<div class="docs-grid">{"".join(cards)}</div></div>'
        )
    index_json = json.dumps(search_index, ensure_ascii=False)
    # Lazy search index: keep docs.html light (~5KB instead of ~220KB) by
    # writing the full-text index to its own file, fetched on first search.
    (ROOT / "docs-index.json").write_text(index_json, encoding="utf-8")

    search_script = """<script>
(function () {
  var INDEX = null;
  var indexLoading = null;
  function ensureIndex() {
    if (INDEX) return Promise.resolve(INDEX);
    if (!indexLoading) {
      indexLoading = fetch('docs-index.json').then(function (r) { return r.json(); })
        .then(function (d) { INDEX = d; })
        .catch(function () { INDEX = {}; });
    }
    return indexLoading;
  }
  var input = document.getElementById('docSearch');
  var clear = document.getElementById('docSearchClear');
  var meta = document.getElementById('docSearchMeta');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.doc-card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('.group'));
  var total = cards.length;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }
  function highlight(text, terms) {
    var lower = String(text).toLowerCase();
    var out = '';
    var i = 0;
    while (i < lower.length) {
      var best = -1, bestLen = 0;
      terms.forEach(function (term) {
        if (!term) return;
        var idx = lower.indexOf(term, i);
        if (idx !== -1 && (best === -1 || idx < best)) { best = idx; bestLen = term.length; }
      });
      if (best === -1) break;
      out += esc(text.slice(i, best)) + '<mark>' + esc(text.slice(best, best + bestLen)) + '</mark>';
      i = best + bestLen;
    }
    out += esc(text.slice(i));
    return out;
  }

  function run() {
    var q = input.value.trim().toLowerCase();
    var terms = q.split(/\s+/).filter(Boolean);
    var count = 0;
    cards.forEach(function (card) {
      var idx = INDEX[card.getAttribute('data-slug')];
      var hay = ((idx ? idx.t + ' ' + idx.b + ' ' + idx.x : '') + ' ' + card.getAttribute('data-title') + ' ' + card.getAttribute('data-blurb')).toLowerCase();
      var match = terms.length === 0 || terms.every(function (t) { return hay.indexOf(t) !== -1; });
      card.style.display = match ? '' : 'none';
      if (match) {
        count++;
        card.querySelector('.d-name').innerHTML = highlight(card.getAttribute('data-title'), terms);
        card.querySelector('.d-blurb').innerHTML = highlight(card.getAttribute('data-blurb'), terms);
      }
    });
    groups.forEach(function (g) {
      var vis = Array.prototype.some.call(g.querySelectorAll('.doc-card'), function (c) { return c.style.display !== 'none'; });
      g.style.display = vis ? '' : 'none';
    });
    clear.classList.toggle('show', input.value.length > 0);
    if (terms.length) {
      if (count === 0) {
        meta.innerHTML = '<div class="search-empty">No documents match — try &ldquo;ollama&rdquo;, &ldquo;api&rdquo;, &ldquo;gpu&rdquo;…</div>';
      } else {
        meta.innerHTML = '<b>' + count + '</b> of ' + total + ' docs match';
      }
    } else {
      meta.innerHTML = '';
    }
  }

  function doSearch() { ensureIndex().then(run); }
  input.addEventListener('input', doSearch);
  clear.addEventListener('click', function () { input.value = ''; doSearch(); input.focus(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      input.focus();
    }
    if (e.key === 'Escape' && document.activeElement === input) { input.blur(); }
  });
})();
</script>"""

    hub_body = f"""
<div class="wrap">
  <div class="hub-hero">
    <span style="font-family:var(--font-m);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--brass)">The documentation</span>
    <h1>Everything about <span style="font-style:italic;color:var(--brass-2)">the assistant.</span></h1>
    <p class="lead">Guides, references, and deep dives — from a five-minute quickstart to the internals of the retrieval pipeline, GPU manager, security model, and every API endpoint.</p>
    <div class="doc-search">
      <svg class="s-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="docSearch" type="search" placeholder="Search all {len(docs)} docs — try &ldquo;ollama&rdquo;, &ldquo;api&rdquo;, &ldquo;gpu&rdquo;…" autocomplete="off" spellcheck="false" aria-label="Search documentation"/>
      <button class="s-clear" id="docSearchClear" aria-label="Clear search" title="Clear search">&times;</button>
    </div>
    <div class="search-meta" id="docSearchMeta"></div>
    <div class="hub-count">{len(docs)} documents · grouped by topic · press <b style="color:var(--brass-2)">/</b> to search</div>
  </div>
  {"".join(groups_html)}
</div>
{search_script}"""
    (ROOT / "docs.html").write_text(page_shell("Documentation", hub_body, None, prefix="", desc="All Lawyer Assistant documentation — quickstart, architecture, backend API, frontend, API providers, launcher, security and troubleshooting, with search.", seo={"keywords": "lawyer assistant docs, legal AI documentation, RAG documentation, quickstart, architecture, backend API"}), encoding="utf-8")
    print("  ✓ docs.html (hub, with search)")

    # ── sitemap.xml — every page, generated so it can never drift ──
    prio = {
        "index": 1.0, "hub": 0.9, "quickstart": 0.8, "architecture": 0.8,
        "backend": 0.8, "frontend": 0.8, "api-provider": 0.7, "launcher": 0.7,
        "security": 0.7, "troubleshooting": 0.7, "pipeline-editor": 0.7,
    }
    def sitemap_url(path, p):
        loc = f"{SITE_URL}/{path}" if path else SITE_URL
        return f"  <url>\n    <loc>{loc}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>{p}</priority>\n  </url>"
    entries = [sitemap_url("", 1.0), sitemap_url("install.html", 0.9), sitemap_url("docs.html", 0.9)]
    for slug, d in docs.items():
        entries.append(sitemap_url(f"docs/{slug}.html", prio.get(slug, 0.6)))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  ✓ sitemap.xml ({len(entries)} URLs)")

    # ── llms-full.txt — full text of every doc for AI crawlers (GEO) ──
    parts = ["# Lawyer Assistant — full documentation\n", "> Complete text of every guide, for AI assistants.\n"]
    for slug, d in docs.items():
        md = d["md"]
        # strip the leading H1 (title) since we emit our own heading
        body = re.sub(r"^#\s+.*?\n", "", md, count=1, flags=re.S).strip()
        parts.append(f"\n\n---\n\n# {d['title']}\n\n{body}")
    (ROOT / "llms-full.txt").write_text("".join(parts), encoding="utf-8")
    print(f"  ✓ llms-full.txt ({len(docs)} docs)")
if __name__ == "__main__":
    build()
    print("Done.")
    # Fail loudly on any site regression — meta, JSON-LD, FAQ parity, links, freshness.
    import sys
    import check_docs
    sys.exit(check_docs.main())
