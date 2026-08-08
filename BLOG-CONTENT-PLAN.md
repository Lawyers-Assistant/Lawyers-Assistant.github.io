# Blog Content Plan — AI for Legal Work & AI Lawyer Assistants

> **Goal:** make lawyers-assistant.github.io the main source lawyers turn to when they
> want to understand AI in legal work — trustworthy, accurate, and genuinely useful.
>
> **Long-term target:** ~1,000 posts mapped to the taxonomy in §3.
> **Right now:** a **2-month, quality-first execution** — posts are written **one by one,
> each with deep research**, and each is **marked complete in the checklist** (§7) only
> after it passes the quality gate.
>
> **The contract:** no bad-law posts. One wrong citation or invented authority destroys
> trust with a legal audience — and can get the site (and its readers) into trouble.
> Quality gates are non-negotiable; the count is flexible.

---

## 1. What "the main source" means

Lawyers search for AI in legal work in four distinct modes. We win all four:

| Mode | What they want | Our answer |
|---|---|---|
| **Research** ("how does AI contract review work") | Explainers that are technically accurate and legally sound | Deep-dive posts with verified facts |
| **Decision** ("should my firm use AI") | Honest trade-offs, risks, costs, ethics | Comparison + ethics posts |
| **Doing** ("how do I actually use it") | Step-by-step workflows they can copy | How-to posts |
| **Trust** ("can I get in trouble") | Ethics opinions, malpractice, privilege | Authority posts with real citations |

Every post should answer at least one of these. Every post should also, where honest,
lead the reader toward the Lawyer Assistant product (the promo strip) — but the
content must stand alone as genuinely useful even if they never download the app.

---

## 2. The quality contract (non-negotiable)

These rules apply to **every** post, every time. If a post can't pass them, it doesn't
get published — it gets revised.

1. **No fabricated citations.** Every case name, statute, rule number, ABA opinion,
   statistic, or quote must be verified against a real source during the research
   phase. If the research can't verify it, the claim is removed or rewritten as
   general ("most state bars") — never published as a specific citation.
2. **Deep research before drafting.** Minimum 3 authoritative sources per post:
   official sources first (ABA / state bar opinions, court rules, official docs),
   then reputable secondary sources. Research happens *before* drafting, not after.
3. **Jurisdiction honesty.** Legal claims get qualifiers: "in most US states," "check
   your state bar," "under the EU AI Act." Never imply a rule is universal.
4. **No certainty where the law is unsettled.** If it's a gray area (and most of AI +
   law is), say so explicitly and flag the open questions.
5. **Human legal review.** At least one legal-knowledgeable review pass per post
   before it's marked complete.
6. **Date-stamped + refresh policy.** Every post shows a date. Facts about the law and
   tools change fast; a post older than ~6 months gets a freshness check.
7. **Plain but precise language.** Written for lawyers, not like a press release.
   No marketing fluff, no filler sentences, no "in today's fast-paced world."
8. **Disclaimers.** Each post carries a short note that it's general information, not
   legal advice for the reader's matter.

---

## 3. The 1,000-post map (taxonomy)

Twelve categories. The first 2 months pull from the **priority clusters** (marked ★);
the rest fill in over time. Counts are targets, not quotas — quality gates always win.

| # | Category | Target | Priority |
|---|---|---|---|
| 1 | AI for specific legal tasks (contracts, research, discovery, drafting, diligence, litigation support, compliance) | 190 | ★ |
| 2 | Ethics, privilege & professional responsibility | 125 | ★ |
| 3 | How-to guides & practical workflows | 135 | ★ |
| 4 | AI lawyer assistants & tools (incl. Lawyer Assistant, comparisons, models) | 115 | ★ |
| 5 | Practice-area deep dives (litigation, transactional, IP, family, immigration, criminal, PI, real estate, tax, employment, healthcare, estates) | 90 | |
| 6 | Practice management & adoption (ROI, training, client comms, pricing) | 70 | |
| 7 | Legal AI technology fundamentals (LLMs, RAG, embeddings, agents, local vs cloud) | 70 | ★ |
| 8 | Career, skills & the profession (future of legal work, upskilling, law students) | 50 | |
| 9 | Data, privacy & security (client data, encryption, breaches, retention) | 45 | |
| 10 | Research, citations & sources (verification, hallucination, databases) | 40 | |
| 11 | Courts, justice & public interest (AI in courts, access to justice, UPL) | 30 | |
| 12 | Opinion, trends & analysis | 40 | |
| | **Total** | **≈ 1,000** | |

### Example topics per category (the style of titles we're aiming for)

1. **Tasks:** How AI reads a contract · what AI actually flags in due diligence ·
   AI for deposition prep · drafting demand letters with verification · eDiscovery TAR
2. **Ethics:** ABA Formal Opinion 512 in practice · disclosure duties · privilege and
   the third-party doctrine · sanctions cases from AI use
3. **How-to:** verify an AI citation in five minutes · build a clause playbook ·
   OCR a 10,000-page case file · prompt patterns for legal analysis
4. **Tools:** Lawyer Assistant vs CoCounsel vs Lexis+AI · local models vs cloud for
   client work · what a pipeline editor is and why it matters
5. **Practice areas:** AI for family law discovery · immigration filings with AI ·
   AI in personal injury demand letters
6. **Management:** pricing AI-assisted work · training associates to verify · telling
   clients you use AI
7. **Tech fundamentals:** RAG explained for lawyers · hybrid search (BM25 + dense) ·
   why local models preserve privilege
8. **Career:** which legal tasks AI commoditizes · AI literacy for associates
9. **Privacy/security:** client data on the cloud vs your machine · ethics walls and AI
10. **Citations:** hallucinated case law: the anatomy · how to check a generated cite
11. **Justice:** court standing orders on AI · AI legal advice and UPL
12. **Opinion:** where legal AI is in 3 years · the billable hour and AI

---

## 4. The 2-month execution plan (gradual, one at a time)

**Shape of the 2 months:** ~2–4 posts/week, written strictly one at a time, each with
its own deep-research pass. Realistic committed target: **~24 posts**, but the quality
gate decides — 20 excellent posts beat 30 rushed ones.

### Weeks 1–2 — Foundation + first posts
- Establish the **manual template**: the existing 6 posts are the pattern — every new
  post is a hand-written HTML file in `blog/` written to match their exact structure
  (head + schema, breadcrumbs, FAQ cards, related reading, promo strip, older/newer
  chain). Decide category labels and the per-post naming scheme.
- Set editorial standards (this file is the source of truth).
- Publish **posts 1–4** from the Month-1 batch (§7), written by hand.

### Weeks 3–8 — Publish by cluster, one post at a time
- Each cluster is researched and written as a set so the posts cross-link into a
  coherent sub-site (cluster hub → pillar → spokes).
- Cadence: **3 posts/week**; each week covers one cluster theme.
- After every post: mark it complete in §7 only when it passes §2's quality gate.

### What we have at the end of 2 months
- ~24 deep-research posts, every one citation-verified and legally reviewed.
- A proven **hand-written template** that keeps every next post consistent without
  any shortcuts.
- The foundation of the four biggest clusters (contracts, research, ethics, tools) —
  which is where the search traffic is.
- A monthly cadence decision point: hold at quality, or raise the cadence.

---

## 5. Production workflow — one post at a time

Every post runs this exact checklist. Nothing publishes early; nothing skips steps.

```
[ ] 1. TOPIC — pick the next title from §7 (one at a time, no parallel drafting)
[ ] 2. RESEARCH — deep-research pass (minimum 3 authoritative sources):
        · official: ABA/state-bar opinions, court rules, statutes, official docs
        · secondary: reputable industry/legal press, peer-reviewed or firm research
        · product: the actual tool/docs (never describe features we can't verify)
        · collect the exact facts, citations, and stats that will appear in the post
[ ] 3. OUTLINE — H2 structure + the FAQ questions the post will answer
[ ] 4. DRAFT — write the post (AI-assisted is fine; the research and review are human)
[ ] 5. VERIFY — every citation/fact/stat in the draft checked against the research;
        remove or soften anything unverifiable (the §2 rules)
[ ] 6. LEGAL REVIEW — one legal-knowledgeable pass: accuracy, qualifiers, disclaimers
[ ] 7. WRITE BY HAND — write the post's HTML by hand, matching the existing post
        template exactly: head (BlogPosting + FAQPage + BreadcrumbList JSON-LD),
        breadcrumbs, visible FAQ cards, related reading, promo strip, older/newer
        chain. No scripts, no generators — every line typed into the file.
[ ] 8. CONNECT BY HAND — open blog.html and add the post card by hand; update
        sitemap.xml and llms.txt by hand; add cross-links to cluster neighbors
        by editing each neighbor's related-reading list.
[ ] 9. VALIDATE BY HAND — open the finished page in a browser: schema section
        loads, FAQ cards render, every link resolves when clicked, visible FAQ
        text matches the FAQPage schema 1:1. No scripts involved.
[ ] 10. PUBLISH + MARK COMPLETE — date it, mark [x] in §7
```

---

## 6. Post template (structure + schema)

Reuses the exact pattern already in the repo's blog posts (and enforced for the docs
by `check_docs.py`):

- **Head:** `<title>` (keyword-phrase + brand), meta description, canonical, OG/Twitter,
  `BlogPosting` JSON-LD, `FAQPage` JSON-LD, `BreadcrumbList` JSON-LD.
- **Body:** breadcrumb (Blog / Category) → title + dek → article → **visible FAQ cards**
  (schema-backed, 3–4 Q&As) → Related reading → Older/Newer chain → promo strip.
- **Category tags** in the post footer, matching the cluster hub.
- Every post links out to 3–5 cluster neighbors (auto or manual) so the site forms a
  connected graph — this is what makes us a "source," not a pile of pages.

---

## 7. Batch 1 — the first ~24 posts (checklist)

Mark `[x]` only after a post passes §2 and §5 end-to-end. Written one at a time.

### Month 1 — contracts, research, ethics (★ clusters)

**Contract review** (extends `ai-contract-review-for-lawyers.html`)
- [x] 01 · How AI Reads a Contract: From Raw Text to Risk Flags — A Lawyer's Guide
- [x] 02 · Force Majeure, Indemnification, and What AI Actually Flags in a Review
- [x] 03 · Building a Clause Playbook: How to Make AI Review Your Firm's Way
- [x] 04 · The Honest Limits of AI Contract Review: What Still Needs a Human Eye

**Legal research** (extends `can-you-trust-ai-legal-research.html` + `how-to-use-ai-for-legal-research.html`)
- [x] 05 · How AI Legal Research Works Under the Hood: Retrieval, Reranking, and Why It Matters
- [x] 06 · Verifying an AI's Case Citation in Five Minutes
- [x] 07 · AI vs. Westlaw and Lexis: What Actually Changes, and What Doesn't
- [ ] 08 · Finding Authority You Didn't Know Existed: AI-Assisted Research Strategy

**Ethics & professional responsibility** (extends `attorney-client-privilege-and-ai.html`)
- [x] 08 · AI and Attorney-Client Privilege: What Happens When the Machine Sees the File (written early, per user direction — covers the privilege/third-party doctrine planned for item 11)
- [x] 09 · ABA Formal Opinion 512 in Practice: What It Means at Your Desk
- [x] 10 · Disclosure Duties: Do You Have to Tell Clients You Use AI?
- [ ] 11 · AI, Attorney–Client Privilege, and the Third-Party Doctrine
- [ ] 12 · Sanctions and AI: What the Early Cases Teach Us

### Month 2 — tools, workflows, practice areas

**AI lawyer assistants & tools**
- [ ] 13 · Lawyer Assistant vs. CoCounsel, Lexis+AI, and ChatGPT: An Honest Comparison
- [ ] 14 · Local Models vs. Cloud APIs for Client Work: The Privacy Trade-Off
- [ ] 15 · What Is a Retrieval Pipeline — and Why Should a Lawyer Care?
- [ ] 16 · Choosing an AI for Your Firm: A Decision Framework

**How-to workflows**
- [ ] 17 · Prompting for Legal Analysis: Patterns That Work (and Ones That Don't)
- [ ] 18 · OCR and Ingestion: Turning a 10,000-Page Case File Into Searchable Text
- [ ] 19 · Building a Firm Knowledge Base AI Can Actually Use
- [ ] 20 · A Verification Workflow You Can Defend in Court

**Practice-area guides**
- [ ] 21 · AI for Litigation: Deposition Prep, Briefing, and Case Strategy
- [ ] 22 · AI for Transactional Lawyers: Diligence, Drafting, and Deal Files
- [ ] 23 · AI for Family Law and Immigration: High-Volume Document Work
- [ ] 24 · AI for Criminal Defense and Public Defense: Risks and Rewards

> After Month 2, re-prioritize: the remaining ~976 posts draw from §3's full
> taxonomy, cluster by cluster — each still written by hand under §2's rules.

---

## 8. How posts are made (no scripts, no automation — everything by hand)

This is a hard rule for the blog: **no generators, no build scripts, no automation.**
Every file is written manually, the way the existing 6 posts were.

1. **The template is the existing posts.** Each new post is a hand-written HTML file
   in `blog/`, written to match their exact structure: `<head>` with the full schema
   stack (BlogPosting + FAQPage + BreadcrumbList), breadcrumbs, article body, visible
   FAQ cards (schema-backed), related reading, older/newer chain, promo strip.
2. **The hub is updated by hand.** `blog.html` gets a new post card written in by
   hand; the "6 articles" count is edited to match. No scripts touch it.
3. **sitemap.xml and llms.txt are updated by hand** with each new post.
4. **Cross-links are hand-edited** into each neighbor post's related-reading list.
5. **No RSS, no category-page generators** for now — the hub stays a single
   hand-maintained page (categories are used as post tags, and the hub lists all posts).

Why: every post is individually researched, written, and reviewed anyway, so hand-
writing the page shell is a small cost next to the research and review — and it keeps
full control over every line that ships.

---

## 9. Measurement (what "working" looks like)

- **Google Search Console:** track impressions/clicks for the cluster keywords
  ("AI contract review," "is it ethical to use AI in law," "AI legal research"),
  and submit each new post.
- **AI citation audit (monthly):** ask ChatGPT/Perplexity/Gemini/Claude "how do
  lawyers use AI ethically?" and check whether the site is cited; verify `/llms.txt`
  is fetched.
- **Dwell + repeat visits** on the hub: evidence of a real audience, not just crawlers.
- **Cluster health:** each of the four Month-1 clusters should have its pillar post
  ranking for the category term by month 3.

---

## 10. Risks & guardrails

| Risk | Guardrail |
|---|---|
| Hallucinated citations destroy trust | §2 rule 1 + step 5 verification — the hardest gate |
| YMYL legal content penalized by Google | E-E-A-T signals: dates, authors, verified sources, legal review, disclaimers |
| Volume race produces slop | One-post-at-a-time workflow; quality gate decides the count |
| Automation creeps in | Hard rule in §8: every file hand-written, hub/sitemap/llms.txt hand-updated |
| Fast-moving law/tool facts go stale | Date stamps + 6-month freshness pass |
| Over-promising what AI does | Comparison/honest-limits posts; never marketing-hype legal certainty |
| Tool features misdescribed | Research step requires verifying against the actual product/docs |

---

*This plan is the working document. Sections 2, 5, and 7 are the ones that get
executed daily; §7's checkboxes are the live progress tracker.*
