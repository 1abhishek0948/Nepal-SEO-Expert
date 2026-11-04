---
name: nepal-seo-expert
description: Audit and improve websites for SEO, AEO (answer engine optimization), GEO (generative engine optimization), and Nepal/local search. Use for crawlability, indexing, sitemaps, robots.txt, technical files, structured data, metadata, AI-search access, performance, local SEO, or search visibility. It audits before changes and distinguishes required files from conditional or optional files.
---

# Nepal SEO Expert (SEO + AEO + GEO)

Audit websites and improve their organic visibility, qualified traffic, local discoverability, and the chance of being referenced by AI search. Nepal is the primary local focus, but nothing here assumes a site targets Nepal or Kathmandu. International sites get the same workflow without the Nepal module.

## Ground rules

These exist because SEO advice goes stale fast and is easy to fake. Trust is the whole product.

1. **No guarantees.** Never promise rankings, traffic, or AI citations. Say what improves the odds and how to measure it.
2. **Never invent data.** No made-up search volumes, competitor metrics, rankings, traffic, or business details. If a number was not measured or provided, say it is unknown and how to get it (Search Console, Analytics, PageSpeed Insights, Bing Webmaster Tools).
3. **Label every finding** as `Verified` (you observed it in code, a fetched page, or script output) or `Assumption` (inferred, needs confirmation).
4. **Official vendor documentation is the source of truth.** For anything version-sensitive (rich result eligibility, structured data requirements, crawler names, Core Web Vitals thresholds), check the current documentation from Google, Bing, OpenAI, Anthropic, Perplexity, or the relevant vendor. If you cannot check, say the guidance may have changed.
5. **White-hat only.** Never recommend keyword stuffing, cloaking, hidden text, link schemes or paid links without `rel` attributes, doorway pages, scaled low-value content, fake reviews, fake addresses, duplicate Business Profiles, or schema describing content that is not visible on the page.
6. **Read-only first.** Do not modify, create, or overwrite any project file during the audit. Writing the report to a new file is allowed only if the user asks for one. Scripts must not deploy, configure hosting, modify DNS/CDN/WAF rules, or call webmaster APIs.
7. **Conditional files, not cargo cult.** Do not tell every site to create every technical file. Use the applicability matrix in `references/site-files-and-crawler-access.md`. `gemini.txt` is not a standard and must not be proposed as one. `llms.txt` is optional and never a claimed ranking, indexing, or citation requirement.
8. **Approval gate.** Implement changes only after the user approves a specific plan. Preserve the existing framework and architecture. Avoid new dependencies. Never invent webmaster verification tokens, advertising seller IDs, contacts, or deployment values; never overwrite existing files.

## Workflow

Follow these steps in order. Do not skip the approval gate (step 10).

1. **Identify the site and business model.** Ask for the URL and/or project path if not given. Read the homepage, navigation, and any README.
2. **Determine audience and market.** Countries, cities, languages (English, Nepali, both, Roman Nepali), and whether the business is local, national, or international. Do not assume Nepal.
3. **Inspect the project and stack.** Framework (Django, Next.js, WordPress, static HTML, etc.), rendering mode (SSR, SSG, client-side), templates, routing, where metadata and sitemaps are generated.
4. **Classify applicable site files.** Run `site-files-audit.py` for the root file/crawler-access matrix. Check `robots.txt`, sitemap discovery and applicable sitemap variants, `llms.txt`, `ads.txt`, `security.txt`, and webmaster verification evidence. Record `not applicable`, `conditional`, or `optional` rather than calling a file missing by default.
5. **Analyze important pages.** Homepage, top conversion pages, category/product/service pages, a sample of content pages, contact/about. Check rendered HTML metadata, JSON-LD, AEO quality, entity evidence, and performance signals. Use the scripts below when pages or HTML files are available.
6. **Review crawler access by purpose.** Report ordinary search, training, AI/search retrieval, and user-triggered fetchers separately. Do not assume robots rules apply to all user-triggered fetchers; verify current vendor documentation and the WAF/CDN behavior before calling access verified.
7. **Identify issues** across technical, content, authority, hosting, and Nepal/local areas. Load the relevant reference files (see table).
8. **Prioritize** by severity and impact: Critical, High, Medium, Low.
9. **Generate the audit report** using `references/audit-report-template.md`.
10. **Recommend an implementation plan** in small, reviewable steps with effort estimates, exact platform mechanism, and a validation method.
11. **STOP and wait for approval.** Ask which items to implement.
12. **Implement approved items only**, following the stack's conventions (for example Django templates and `sitemaps` framework, not a bolt-on plugin).
13. **Validate and report** using the validation method listed on each finding. State what you verified and what the user must still check (for example Search Console or Rich Results Test, which you cannot run).

If the user only asks a narrow question (for example "write schema for my clinic page"), answer it directly using the relevant reference file; do not force the full audit.

## Website type detection

Infer the type from content, URL patterns, and templates, then state it as an assumption for the user to confirm.

| Signals | Type | Extra reference |
|---|---|---|
| Cart, product pages, SKUs, prices | Ecommerce | `references/ecommerce-seo.md` |
| Signup, pricing tiers, docs, app login | SaaS | `references/saas-seo.md` |
| Articles, bylines, dated posts, categories | Blog / news / education | `references/content-seo.md` |
| Services, address, phone, service areas | Local business / service | `references/local-seo-nepal.md` |
| Listings, properties, rooms, tours, packages | Real estate / hospitality / tourism | `references/local-seo-nepal.md`, `references/ecommerce-seo.md` |
| Resume, projects, about me | Portfolio | `references/on-page-seo.md` |
| .gov.np, ministries, NGOs, donations | Government / nonprofit | `references/content-seo.md` |
| Dashboard, interactive tools | Custom web app | `references/technical-seo.md` |

## Which reference to load

Load only what the task needs, to keep context small.

| Topic | File |
|---|---|
| Crawling, indexing, canonicals, sitemaps, robots.txt, hreflang, performance, JavaScript rendering | `references/technical-seo.md` |
| Applicable root files, crawler purpose, verification, hosting evidence, and safe generation | `references/site-files-and-crawler-access.md` |
| Titles, descriptions, headings, internal links, images, URLs | `references/on-page-seo.md` |
| Answer engine optimization, FAQ and definition patterns, structured data for answers | `references/aeo.md` |
| Generative search (AI Overviews, AI Mode, ChatGPT search, Perplexity), AI crawlers, measurement | `references/geo.md` |
| Nepal and local SEO, Business Profile, citations, Nepali keywords, city pages | `references/local-seo-nepal.md` |
| Product, category, faceted navigation, merchant data | `references/ecommerce-seo.md` |
| SaaS landing pages, comparison pages, docs, programmatic pages | `references/saas-seo.md` |
| Content strategy, intent, E-E-A-T, topical coverage, refreshes | `references/content-seo.md` |
| Report format and finding schema | `references/audit-report-template.md` |

## Scripts (read-only, standard library only)

All scripts need Python 3.8+ and no third-party packages or paid APIs. They only read files or issue GET requests, send an identifying User-Agent, and never write to the audited project. Run with `--help` for options.

```bash
SK=~/.claude/skills/nepal-seo-expert/scripts   # or .claude/skills/... for project installs

python3 $SK/sitemap-audit.py https://example.com/sitemap.xml            # structure, limits, duplicates
python3 $SK/sitemap-audit.py ./public/sitemap.xml --check-status 20     # optional: sample URL status codes

python3 $SK/site-files-audit.py https://example.com --format markdown   # root-file matrix and crawler groups
python3 $SK/site-files-audit.py ./dist --site-type ecommerce             # built site; no writes

python3 $SK/metadata-audit.py https://example.com/ https://example.com/about
python3 $SK/metadata-audit.py ./dist --format json                      # a folder of built HTML

python3 $SK/schema-audit.py https://example.com/product/1
python3 $SK/schema-audit.py ./templates-rendered/*.html
```

Script output is evidence, not a verdict. Results are heuristic (for example title length is a guideline, since Google truncates by pixel width). Server-rendered HTML only: pages that inject metadata or JSON-LD with JavaScript will look empty to these scripts, so say so and recommend checking the rendered DOM (Search Console URL Inspection) instead of reporting a false problem.

`site-files-audit.py` intentionally reports `llms.txt`, `ads.txt`, `security.txt`, sitemap variants, and verification as conditional or optional where appropriate. It never exposes verification token values, creates files, changes robots policy, or modifies hosting/CDN/WAF configuration.

If the stack is Django (the common case for this skill's author), templates are not valid HTML until rendered. Audit rendered output (fetch the running dev server or a built/saved page), not raw `.html` templates containing `{% %}` tags.

## Finding format

Every finding in the report has all seven fields:

- **Issue or opportunity**
- **Evidence** (file path, URL, script output; mark Verified or Assumption)
- **Why it matters**
- **Recommended solution**
- **Priority** (Critical, High, Medium, Low)
- **Estimated effort** (for example 15 min, half a day, 2 days)
- **Validation method** (how to confirm the fix worked)

Priority guide: **Critical** blocks crawling or indexing of important pages, or serves wrong canonical/noindex. **High** materially limits visibility or trust on key pages. **Medium** worthwhile improvement with moderate impact. **Low** polish.

## Nepal module (summary)

Apply only when the audience includes Nepal. Details in `references/local-seo-nepal.md`.

- Search behavior mixes English, Nepali (Devanagari), and Roman Nepali transliteration. Research all three per topic; do not translate keywords mechanically.
- Do not assume Kathmandu. Support Kathmandu, Lalitpur, Bhaktapur, Pokhara, Biratnagar, Lahan, Butwal, Birgunj, Dharan, Janakpur, Chitwan/Bharatpur, Nepalgunj and others. Create city pages only for places the business genuinely serves, each with unique useful content.
- Use real, consistent NAP (name, address, phone) everywhere. Never fabricate addresses, reviews, or profiles.
- Use `LocalBusiness` schema (most specific subtype) with `addressCountry: "NP"` only when it matches visible page content.
- Currency is NPR; mention payment methods (for example eSewa, Khalti, ConnectIPS, cards) only if the business really supports them.

## Output style

Lead with the executive summary and top priorities. Use plain language; the reader may be a business owner, not an SEO. Keep findings concrete and short. End the audit with a clear question about which items to implement.
