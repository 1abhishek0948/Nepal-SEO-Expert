# Nepal SEO Expert

**Version 1.2.0** · A reusable, tested, read-only SEO, AEO, GEO, and Nepal local SEO audit skill.

Give it a website URL or project folder. It finds SEO issues, explains what matters, and gives a clear plan. It does **not** change website files until you approve specific fixes.

## Quick start

These commands are for macOS, Linux, or WSL. First download version 1.2.0:

```bash
git clone --depth 1 --branch v1.2.0 https://github.com/1abhishek0948/Nepal-SEO-Expert.git ~/nepal-seo-expert
```

Then choose the tool you use below. The installer copies the **whole** skill folder, including its scripts and reference guides. It never overwrites an existing installation.

| Tool | Install for all projects | Install in one project |
|---|---|---|
| Claude Code | `~/.claude/skills/nepal-seo-expert` | `.claude/skills/nepal-seo-expert` |
| OpenCode | `~/.config/opencode/skills/nepal-seo-expert` | `.opencode/skills/nepal-seo-expert` |
| Codex | `~/.codex/skills/nepal-seo-expert` | `.codex/skills/nepal-seo-expert` |
| Compatible agent tools | `~/.agents/skills/nepal-seo-expert` | `.agents/skills/nepal-seo-expert` |

### Claude Code

Install for all your projects:

```bash
sh ~/nepal-seo-expert/install.sh claude global
```

Or install only in the current project:

```bash
sh ~/nepal-seo-expert/install.sh claude project
```

Start a new Claude Code session in the website project, then ask:

> Use the nepal-seo-expert skill to audit this website for SEO, AEO, and GEO. Report only; do not change files yet.

### OpenCode

Install for all your projects:

```bash
sh ~/nepal-seo-expert/install.sh opencode global
```

Or install only in the current project:

```bash
sh ~/nepal-seo-expert/install.sh opencode project
```

OpenCode discovers the skill automatically. Start it in the website project and ask:

> Use the nepal-seo-expert skill. Audit this site for SEO, AEO, GEO, and Nepal local SEO. Give me a report first.

### Codex

Install for all your projects:

```bash
sh ~/nepal-seo-expert/install.sh codex global
```

Or install only in the current project:

```bash
sh ~/nepal-seo-expert/install.sh codex project
```

Open a new Codex chat in the website project and ask:

> Use `$nepal-seo-expert` to audit this project. Check SEO, AEO, GEO, technical files, and Nepal local relevance. Report only; wait for my approval before changing anything.

### Other Agent Skills-compatible tools

Many coding agents use the same `SKILL.md` format. The usual project location is `.agents/skills`:

```bash
sh ~/nepal-seo-expert/install.sh agents project
```

If your tool uses another skills folder, copy the complete folder there and keep this final path:

```text
<skills-folder>/nepal-seo-expert/SKILL.md
```

## How to use it

Start with an audit. Good first prompts:

> Audit https://example.com for SEO, AEO, and GEO. We serve Kathmandu and Pokhara. Report only; do not change files.

> Use the nepal-seo-expert skill to review this project. Check metadata, schema, sitemap, robots.txt, crawler access, performance, and Nepal local SEO.

After you read the report, approve only the items you want:

> Implement findings T-01 and G-02. Keep the current framework and show me how you validated the changes.

The skill will not claim that every site needs every file. For example, `llms.txt` is optional, `ads.txt` applies only to sites selling programmatic ads, and `gemini.txt` is not a web standard.

## What it checks

- Technical SEO: indexing, canonicals, robots.txt, sitemaps, redirects, rendered HTML, mobile, and performance signals.
- On-page SEO: titles, descriptions, headings, links, images, and content quality.
- Structured data: JSON-LD and schema consistency with visible content.
- AEO: direct answers, useful FAQs, sources, clear explanations, and accessible HTML.
- GEO: search, training, AI-search, and user-triggered crawler access as separate choices.
- Nepal local SEO: English, Nepali, and Roman Nepali language relevance; real NAP details; genuine service areas; and local schema.

## Why you can trust the workflow

- **Safe by default:** audits are read-only and implementation requires approval.
- **No fake requirements:** optional files are labelled optional; the skill does not claim `gemini.txt` is a standard.
- **No invented data:** findings must show evidence and distinguish verified facts from assumptions.
- **Tested on every change:** GitHub Actions checks package structure, compiles scripts, tests the installer and auditors, and checks shell syntax.
- **Learn by example:** see the clearly fictional reports in `examples/` for the expected report format.

## What is inside

```
nepal-seo-expert/
├── SKILL.md                      # Workflow, ground rules, routing
├── README.md                     # This file
├── install.sh                    # Safe one-command installer
├── examples/                     # Clearly fictional example audit reports
├── references/                   # Detailed guidance, loaded only when needed
│   ├── technical-seo.md          # Crawling, indexing, canonicals, sitemaps, CWV, hreflang
│   ├── site-files-and-crawler-access.md # Applicable files, crawler purpose, safe generation
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
│   ├── site-files-audit.py        # Root files, crawler groups, hosting evidence (read-only)
│   ├── metadata-audit.py
│   └── schema-audit.py
└── tests/sample-site/            # Sample HTML and sitemaps with known issues, for testing the scripts
```

## Requirements

- Python 3.8 or newer for the scripts. No pip installs, no API keys, no paid services.
- Network access only if you audit live URLs. Local HTML files and sitemaps need none.
- If your network uses a proxy and you audit localhost, set `no_proxy=127.0.0.1,localhost`.

## Run the audit scripts yourself

```bash
cd ~/nepal-seo-expert/scripts

python3 sitemap-audit.py https://example.com/sitemap.xml
python3 sitemap-audit.py ./sitemap.xml --check-status 20      # optional: HEAD-check 20 sampled URLs
python3 site-files-audit.py https://example.com --format markdown
python3 site-files-audit.py ./dist --site-type ecommerce
python3 metadata-audit.py https://example.com/ https://example.com/about
python3 metadata-audit.py ./dist --format markdown            # folder of built HTML
python3 schema-audit.py ./dist/products/*.html --format json
```

All four accept `--help`. They read files or send GET (and, for sitemap status sampling, HEAD) requests with an identifying User-Agent and a delay, and never write to the audited project. They read server-rendered HTML only: metadata or JSON-LD added by JavaScript will not be seen, so confirm those cases with Search Console URL Inspection. Findings are heuristic evidence, not verdicts.

### File and crawler applicability

The audit does not prescribe a pile of files for every site. It reports each as expected, conditional, optional, or not applicable.

| Item | When it applies |
|---|---|
| `robots.txt`, primary XML sitemap | A public site with crawlable canonical pages |
| Sitemap index | Multiple sitemap files or sitemap size/count limits |
| News/image/video sitemap | Only when the corresponding content is material and eligible |
| `llms.txt` | Optional community convention; not an SEO, indexing, or AI-citation requirement |
| `gemini.txt` | Not a recognised standard; do not create it as an SEO/GEO file |
| `ads.txt` | A site selling programmatic display ads, using seller data supplied by ad operations |
| `security.txt` | A site with a monitored security contact and disclosure process |
| Webmaster verification | When the owner wants to verify a property; only use a service-issued token |

Crawler access is reported separately for ordinary search, model training, AI/search retrieval, and user-triggered fetches. These choices have different consequences and must be confirmed against current vendor documentation and the site's WAF/CDN behavior. The audit never changes `robots.txt`, DNS, CDN, WAF, cache headers, redirects, or deployment configuration without explicit approval.

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
- Use current official documentation from Google and the relevant crawler vendor for version-sensitive details such as rich-result eligibility, crawler names, and performance thresholds.
- Scripts avoid third-party dependencies, never touch API keys, and never overwrite project files.
- Missing optional files are not presented as errors. The skill never invents webmaster verification tokens, ad seller IDs, security contacts, or business details.

## Testing checklist

Run through this after installing or modifying the skill.

**Structure**
- [ ] `SKILL.md` exists at the folder root with `name: nepal-seo-expert` and a `description`
- [ ] Folder name matches the skill name; every file named in SKILL.md exists
- [ ] All ten reference files exist and are non-empty
- [ ] No unfinished to-do notes or sample placeholder text left in the skill files

**Scripts** (from the skill folder)
- [ ] `python3 -m py_compile scripts/*.py` succeeds
- [ ] `python3 -m unittest discover -s tests -p 'test_*.py'` succeeds
- [ ] `python3 scripts/validate-skill.py .` succeeds
- [ ] `sh -n install.sh` succeeds
- [ ] `python3 scripts/metadata-audit.py tests/sample-site` flags the issues in `bad.html`, `spa.html`, `template.html` and the duplicate pair, and reports no findings for `good.html`
- [ ] `python3 scripts/schema-audit.py tests/sample-site/bad.html tests/sample-site/bad-local.html` reports invalid JSON, placeholders, 0,0 coordinates and missing properties
- [ ] `python3 scripts/sitemap-audit.py tests/sample-site/sitemap-bad.xml` reports duplicates, mixed hosts and protocols, bad and future lastmod; `sitemap-good.xml` reports none
- [ ] `--format json` output parses; `--help` works on all scripts
- [ ] `python3 scripts/site-files-audit.py tests/site-files --format json` reports the applicability matrix, does not recommend `gemini.txt`, and keeps verification token values out of output
- [ ] Scripts leave the audited folder unchanged (check `git status` or file timestamps)

**Discovery and invocation**
- [ ] The skill is found from the documented Claude Code, OpenCode, Codex, or `.agents` folder
- [ ] `sh install.sh codex project` installs the whole skill and refuses to overwrite an existing install
- [ ] An explicit prompt such as `Use $nepal-seo-expert to audit this site` loads the skill
- [ ] A prompt such as "audit my site's SEO" triggers it without naming it

**Behavior**
- [ ] The first response is an audit, not code edits
- [ ] The agent asks for approval before changing files
- [ ] The report uses all seven fields per finding and labels Verified vs Assumption
- [ ] No invented numbers (volumes, rankings, competitor metrics)
- [ ] Nepal module is applied for a Nepal-targeted site and skipped for a non-Nepal one
- [ ] The agent says what it cannot validate itself (Search Console, Rich Results Test, field Core Web Vitals)
- [ ] The agent refuses fake reviews, fake addresses, doorway pages and similar requests

## Maintenance

SEO guidance changes. Review the reference files whenever Google changes Search documentation, rich result eligibility, spam policies, or AI features. The files that most often need updates are `geo.md` and `site-files-and-crawler-access.md` (crawler names and platform behavior), `aeo.md` (structured data eligibility), and `technical-seo.md` (Core Web Vitals thresholds).
