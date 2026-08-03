# SEO / AEO / GEO Plan — Lawyer Assistant Website

Goal: appear first when people search for "lawyer assistant", "legal research AI",
"AI for lawyers", "legal document chatbot", and get quoted by AI engines
(ChatGPT, Perplexity, Gemini, Claude).

Three fronts, one content base:

- **SEO** — classic Google/Bing ranking: keywords, meta, structured data, links.
- **AEO** — Answer Engine Optimization: win featured snippets ("position zero")
  and People-Also-Ask boxes with direct, self-contained answers.
- **GEO** — Generative Engine Optimization: get cited by AI chat engines when
  users ask them about legal AI tools.

Everything implemented here lives in `website/` (gitignored — not pushed).

---

## 1. Target keywords (primary)

| Intent | Query | Page |
|---|---|---|
| Brand | lawyer assistant, lawyer assistant app, lawyer assistant AI | landing |
| Category | legal research AI, AI for lawyers, legal document search | landing |
| Tool | free legal document chatbot, legal AI desktop app, offline legal AI | landing |
| Problem | how to search legal documents, AI that cites legal sources | landing + FAQ |
| Privacy | private legal AI, local legal AI, no cloud legal research | landing + privacy |

Secondary (long-tail, for blog/FAQ): "BGE-M3 reranking legal", "playbook
compliance scan", "hybrid search BM25 dense", "LLM offline legal", "RAG for
law firms".

---

## 2. On-page SEO (implemented)

1. **Title tag** — one keyword-phrase, brand at end:
   `Lawyer Assistant — Private AI Legal Research for Your Documents`
2. **Meta description** — 150–160 chars, action + benefit, keyword-front-loaded.
3. **Canonical** on every page (prevents duplicate-content dilution if served
   from multiple hosts).
4. **Semantic HTML** — one H1 per page, logical H2/H3 hierarchy, `<article>`,
   `<nav>`, `<footer>`. Already in place.
5. **Image alt text** — descriptive, keyword-inclusive (already present).
6. **Open Graph + Twitter Card** — link previews on X/LinkedIn/Facebook/Slack.
7. **Schema.org JSON-LD**:
   - `SoftwareApplication` (category `BusinessApplication`/`LegalApplication`,
     OS list, `offers` free, feature list) → eligible for app-rich results.
   - `FAQPage` (mirrors the visible FAQ) → featured snippets + AI extraction.
   - `WebSite` + `Organization` → entity grounding (Google's knowledge graph).
8. **Internal linking** — every page links to the hub; nav links to Docs.
9. **Mobile + speed** — already responsive, single-file, system fonts +
   Google Fonts only; keep it fast.

---

## 3. AEO — answer-engine blocks (implemented)

AI Overviews and featured snippets extract **self-contained Q&A**. The landing
page now has a visible FAQ section where **each answer stands alone** (40–60
words, question repeated inside the answer) — the exact format LLMs lift.

- 7 FAQ questions mapped to real user queries ("Is it private?", "Which
  providers?", "What file formats?", "Does it cite sources?", "Is it free?",
  "Does it need the internet?", "What is the playbook scan?").
- Each answer is also in `FAQPage` JSON-LD with **identical wording** to the
  visible heading/text (Google requires the schema to match the page).
- A direct "What is Lawyer Assistant?" one-liner in the hero `<p class="lead">`
  doubles as a definitional snippet target.

---

## 4. GEO — generative-engine optimization (implemented)

1. **`/llms.txt`** (llmstxt.org standard) — a Markdown briefing file AI agents
   read at inference time: project summary, what it does, key facts, and a
   curated file list of the docs. This is the single biggest GEO win.
2. **`/robots.txt`** — explicitly *allow* AI crawlers (`GPTBot`,
   `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `PerplexityBot`,
   `anthropic-ai`, `Google-Extended`) so ChatGPT Search, Perplexity and Claude
   can cite the site. (When hosted, also consider blocking `CCBot`/`Bytespider`
   at the WAF if you don't want training-data scraping.)
3. **Citation-friendly content** — comparison tables ("vs generic chatbots"),
   feature lists, verified statistics ("local-first", "works offline", "BGE-M3",
   "hybrid BM25+dense"), explicit provider list. Princeton's GEO research:
   verifiable stats + structured lists raise AI visibility.
4. **Perplexity-style practical framing** — "How it works" (Ingest → Ask →
   Verify) and the provider matrix give Perplexity the actionable walkthrough
   it favors; the comparison table gives ChatGPT the "X vs Y" it favors.
5. **Fresh entity name** — consistent brand + description across landing, docs,
   GitHub README, and `llms.txt` so AI engines build one coherent entity.

---

## 5. Off-page (needs you — hosting + links)

### 5.1 Host the site (prerequisite for everything)
The site is currently local-only. Publish it so crawlers can reach it:

```bash
# GitHub Pages (free, HTTPS, includes the repo)
# push the website/ folder to a branch or a separate repo, then enable Pages
```
Or Netlify/Vercel/Cloudflare Pages — free tier, instant, HTTPS, edge CDN.

### 5.2 Google / Bing indexing
1. **Google Search Console** — add the domain, submit `sitemap.xml`,
   request indexing for `/`, `/docs.html`, `/llms.txt`.
2. **Bing Webmaster Tools** — same sitemap (Bing pulls Google data too).
3. Verify with Search Console that `/llms.txt` is crawlable.

### 5.3 Authority & backlinks (SEO's long game)
- The **GitHub repo** (`github.com/haal-lab/Lawyer-Assistant`) is your strongest
  backlink asset — put the live site URL in the README, profile, and repo
  About section; star-worthy repos accrue links organically.
- **Product Hunt** launch (free) — best single spike for a dev tool.
- **Directories**: AlternativeTo, Product Hunt Collections, Awesome lists
  ("awesome legal tech", "awesome RAG"), OSS alternatives lists.
- **Guest/blog content**: a "legal AI comparison" post pointing to the compare
  table; tutorials ("run legal RAG offline") linking the docs.
- **Community**: r/LawTech, r/LocalLLaMA, HN "Show HN", X/LinkedIn posts with
  the screenshot + link. Every share is a citation signal.

### 5.4 Ongoing content for long-tail
Add a lightweight `/blog/` with one article per long-tail keyword
("How to search 10,000 legal PDFs locally", "BM25 vs dense retrieval for
contracts"). Each blog post should include a FAQ block and a comparison table —
the two highest-citation formats.

---

## 6. Measurement

- **Google Search Console**: track queries for "lawyer assistant", "legal AI",
  "legal document search" → impressions, CTR, position; submit each new page.
- **Bing + Brave + DuckDuckGo** search for the brand term — check indexing.
- **AI citation audit** (monthly): ask ChatGPT/Perplexity/Gemini/Claude
  "what is the best free local legal research AI?" and check whether the site
  is cited; re-check `/llms.txt` is fetched.
- **Sitemap pings**: re-submit after every content release.

---

## 7. Quick wins checklist (this repo)

- [x] Title / description / canonical / OG / Twitter on landing
- [x] SoftwareApplication + FAQPage + WebSite + Organization JSON-LD
- [x] Visible FAQ with self-contained answers (AEO)
- [x] Comparison table + feature lists (GEO citation formats)
- [x] `/llms.txt`, `/robots.txt`, `/sitemap.xml`
- [x] Docs pages: meta description + canonical + OG
- [x] One H1 per page, semantic headings, alt text
- [ ] Host the site (GitHub Pages / Netlify / Vercel)
- [ ] Search Console + Bing Webmaster + sitemap submission
- [ ] GitHub README → live site link
- [ ] Product Hunt / AlternativeTo / awesome-list listings
- [ ] Blog with long-tail posts

**Priority order:** host → Search Console → llms.txt fetch check → GH README
link → Product Hunt → directories → blog.
