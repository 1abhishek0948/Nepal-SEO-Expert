# nepal-seo-expert

A reusable AI skill that helps coding agents audit and improve websites for **SEO**, **AEO** (answer engine optimization) and **GEO** (generative engine optimization), with a dedicated **Nepal and local SEO** module. It works on any website and tech stack, and supports international SEO too.

It does not promise rankings, traffic or AI citations. It never invents metrics, search volumes, competitor data or business details. It audits first, waits for your approval, and only then changes code.

## What is inside

```
nepal-seo-expert/
├── SKILL.md                      # Workflow, ground rules, routing (the file Claude reads first)
├── README.md                     # This file
├── references/                   # Detailed guidance, loaded only when needed
│   ├── technical-seo.md          # Crawling, indexing, canonicals, sitemaps, CWV, hreflang
│   ├── on-page-seo.md            # Titles, descriptions, headings, links, images
│   ├── aeo.md                    # Answer engines, FAQ/definition patterns, structured data
│   ├── geo.md                    # AI Overviews, ChatGPT search, Perplexity, AI crawlers, measurement
│   ├── local-seo-nepal.md        # Nepal keywords, city pages, Business Profile, NAP, schema
│   ├── ecommerce-seo.md          # Product, category, facets, merchant data
│   ├── saas-seo.md               # Landing, pricing, comparison, docs, programmatic pages
│   ├── content-seo.md            # Intent, topical coverage, E-E-A-T, refreshes
│   └── audit-report-template.md  # Report structure and the 7-field finding format
├── scripts/                      # Read-only helpers, Python 3.8+ standard library only
│   ├── sitemap-audit.py
│   ├── metadata-audit.py
│   └── schema-audit.py
└── tests/sample-site/            # Sample HTML and sitemaps with known issues, for testing the scripts
```

## Install

### Claude Code (personal, available in every project)

```bash
mkdir -p ~/.claude/skills
cp -r nepal-seo-expert ~/.claude/skills/
```

### Claude Code (one project only, shareable through git)

```bash
mkdir -p .claude/skills
cp -r /path/to/nepal-seo-expert .claude/skills/
```

Restart Claude Code (or start a new session) so it discovers the skill. Then confirm:

1. Ask: `What skills do you have available?` and check that `nepal-seo-expert` is listed.
2. Or type `/nepal-seo-expert` to invoke it directly.

Keep the folder name equal to the `name` in SKILL.md (`nepal-seo-expert`), and keep `SKILL.md` at the folder root.

### Claude.ai or Claude desktop

Upload the packaged `nepal-seo-expert.skill` file under Settings > Capabilities > Skills (the location of this setting can change; check the current Claude Help Center). Script execution needs a code-execution-enabled environment.

### Requirements

- Python 3.8 or newer for the scripts. No pip installs, no API keys, no paid services.
- Network access only if you audit live URLs. Local HTML files and sitemaps need none.
- If your network uses a proxy and you audit localhost, set `no_proxy=127.0.0.1,localhost`.

## How to use

Just describe the job. The skill triggers on SEO, indexing, sitemap, schema, Core Web Vitals, AI search visibility, Business Profile and Nepal local search topics. A normal run looks like this:

1. You give a URL and/or project folder.
2. Claude identifies the site type and target market, inspects the stack, runs the scripts, and writes the audit report.
3. Claude stops and asks which items to implement. **No files are changed during the audit.**
4. After you approve, Claude implements only those items, then validates and reports what it could and could not verify.

### Running the scripts yourself

```bash
cd ~/.claude/skills/nepal-seo-expert/scripts

python3 sitemap-audit.py https://example.com/sitemap.xml
python3 sitemap-audit.py ./sitemap.xml --check-status 20      # optional: HEAD-check 20 sampled URLs
python3 metadata-audit.py https://example.com/ https://example.com/about
python3 metadata-audit.py ./dist --format markdown            # folder of built HTML
python3 schema-audit.py ./dist/products/*.html --format json
```

All three accept `--help`. They read files or send GET (and, for sitemap status sampling, HEAD) requests with an identifying User-Agent and a delay, and never write to the audited project. They read server-rendered HTML only: metadata or JSON-LD added by JavaScript will not be seen, so confirm those cases with Search Console URL Inspection. Findings are heuristic evidence, not verdicts.

Django users: audit rendered output, not raw templates containing `{% %}`. The scripts warn when they see template syntax.

## Example prompts

Business or service site
> Audit https://my-business.example for SEO, AEO and GEO. We serve Pokhara and Kathmandu. Report only; don't change anything yet.

Local business in Nepal
> Review local SEO for our clinic in Biratnagar: Google Business Profile checklist, LocalBusiness schema for the contact page, and Nepali plus Roman Nepali keyword ideas from sources I can verify.

Ecommerce
> Audit the product and category templates in this Django project for SEO. Check Product schema, faceted URLs, canonicals and out-of-stock handling. Prices are in NPR.

SaaS
> Our SaaS marketing site is in /web. Which pages should exist for comparison and pricing intent, and are our docs crawlable and indexable?

Blog or news
> Audit this blog for topical coverage, E-E-A-T signals, internal linking and refresh candidates. Don't invent search volumes.

Education
> Check our college website for admissions-related questions we should answer directly, and whether the pages are structured so answer engines can use them.

Portfolio
> Audit my personal portfolio for SEO. It targets international clients, so skip the Nepal module.

Government or nonprofit
> Review this ministry-style site for bilingual (Nepali and English) SEO, hreflang, accessible PDF handling and clear service pages.

Real estate, hospitality or tourism
> Audit our trekking agency's site for tour package pages, seasonal content, local trust signals and AI search visibility. Add measurement for AI referrals.

Custom web app
> This is a Next.js app with a public marketing area. Check rendering, indexability and which routes should be noindex.

Narrow tasks
> Write a sitemap generator using Django's sitemaps framework for these models, then tell me how to validate it.
> Check this JSON-LD for problems and tell me what must be visible on the page for it to be valid.

Implementation after the audit
> Implement findings T-01, T-03 and O-02 from the report. Preserve the current structure and give me the validation steps.

## Safety principles

- Read-only audit; changes only after explicit approval.
- No keyword stuffing, cloaking, hidden text, link schemes, doorway pages, fake reviews, fake addresses, duplicate business profiles or schema for content that is not visible.
- No fabricated metrics. Findings are labeled Verified or Assumption.
- Official Google Search Central guidance is the reference for anything version-sensitive. Verify current details before relying on them (rich result eligibility, crawler names, thresholds).
- Scripts avoid third-party dependencies, never touch API keys, and never overwrite project files.

## Testing checklist

Run through this after installing or modifying the skill.

**Structure**
- [ ] `SKILL.md` exists at the folder root with `name: nepal-seo-expert` and a `description`
- [ ] Folder name matches the skill name; every file named in SKILL.md exists
- [ ] All nine reference files exist and are non-empty
- [ ] No unfinished to-do notes or sample placeholder text left in the skill files

**Scripts** (from the skill folder)
- [ ] `python3 -m py_compile scripts/*.py` succeeds
- [ ] `python3 scripts/metadata-audit.py tests/sample-site` flags the issues in `bad.html`, `spa.html`, `template.html` and the duplicate pair, and reports no findings for `good.html`
- [ ] `python3 scripts/schema-audit.py tests/sample-site/bad.html tests/sample-site/bad-local.html` reports invalid JSON, placeholders, 0,0 coordinates and missing properties
- [ ] `python3 scripts/sitemap-audit.py tests/sample-site/sitemap-bad.xml` reports duplicates, mixed hosts and protocols, bad and future lastmod; `sitemap-good.xml` reports none
- [ ] `--format json` output parses; `--help` works on all scripts
- [ ] Scripts leave the audited folder unchanged (check `git status` or file timestamps)

**Discovery and invocation (Claude Code)**
- [ ] The skill appears when you ask for available skills
- [ ] `/nepal-seo-expert` invokes it
- [ ] A prompt such as "audit my site's SEO" triggers it without naming it

**Behavior**
- [ ] The first response is an audit, not code edits
- [ ] Claude asks for approval before changing files
- [ ] The report uses all seven fields per finding and labels Verified vs Assumption
- [ ] No invented numbers (volumes, rankings, competitor metrics)
- [ ] Nepal module is applied for a Nepal-targeted site and skipped for a non-Nepal one
- [ ] Claude says what it cannot validate itself (Search Console, Rich Results Test, field Core Web Vitals)
- [ ] Claude refuses fake reviews, fake addresses, doorway pages and similar requests

## Maintenance

SEO guidance changes. Review the reference files whenever Google changes Search documentation, rich result eligibility, spam policies, or AI features. The files that most often need updates are `geo.md` (crawler names, platform behavior), `aeo.md` (structured data eligibility), and `technical-seo.md` (Core Web Vitals thresholds).
