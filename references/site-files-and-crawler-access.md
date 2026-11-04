# Site files, crawler access, and safe generation

Use this reference when an audit covers root files, crawler access, webmaster tools, hosting, or safe generation. Start with evidence: inspect the deployed site and the repository's existing delivery mechanism. A missing file is not automatically a defect.

## Applicability matrix

| Item | When it applies | Audit | Safe recommendation after approval |
|---|---|---|---|
| `robots.txt` | Public site | HTTP status/content type, important-path blocks, Sitemap lines, crawler groups | Update the existing platform mechanism; never use it as an indexing-only control |
| Primary XML sitemap | Public canonical pages | Discover from robots and conventional filenames; audit with `sitemap-audit.py` | Use the platform's native sitemap facility |
| Sitemap index | Multiple sitemap files or size/count limits | Confirm child sitemap URLs and limits | Split only when actually needed |
| News sitemap | Qualifying, regularly updated news publisher | Confirm current search-engine eligibility before recommending | Use only for the news content type |
| Image/video sitemap | Image/video discovery is material and the platform does not expose it already | Confirm media is indexable and has meaningful surrounding page content | Generate from the media CMS only after approval |
| `llms.txt` | Optional editorial convenience | Note existence and accuracy | May draft one, labelled optional; never claim crawler support, rankings, or citations |
| `gemini.txt` | Never a standard requirement | Note it only if present | Do not create or recommend as a standard |
| `ads.txt` | Site sells programmatic display advertising | Confirm authorised seller records with the ad operations owner | Draft only from seller IDs supplied by the owner |
| `security.txt` | A monitored security disclosure contact/process exists | Check `/.well-known/security.txt`, `Contact`, and policy links | Draft only with real monitored contacts and approval |
| Webmaster verification | Owner wants a property verified | Look for public meta/file evidence but do not infer ownership from absence | Tell owner to add the service-issued token through their chosen method; never invent tokens |

## Crawler decisions are separate decisions

When parsing `robots.txt`, report these groups independently. User-agent names and vendor behaviour change, so verify the current vendor documentation before proposing a production policy.

| Group | Examples to inspect | Decision to obtain from the owner |
|---|---|---|
| Search | `Googlebot`, `Bingbot` | Should public search engines crawl this content? |
| Training | `Google-Extended`, `GPTBot`, `ClaudeBot` | Is this content permitted for training where the vendor honors robots controls? |
| AI/search retrieval | `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` | May services retrieve content for search answers? |
| User-triggered fetch | `ChatGPT-User`, `Claude-User` | May a user ask an assistant to fetch a public page on demand? |

Do not collapse these into an “AI allowed” flag. `Google-Extended` is not a Google Search control; a training decision does not decide search appearance. Robots rules are advisory, and a WAF or CDN can block crawlers separately. Check access logs, vendor verification guidance, and hosting controls before calling crawler access verified.

## Read-only checks and limits

- Run `scripts/site-files-audit.py` for the root-file matrix and crawler grouping.
- Run `scripts/sitemap-audit.py` for each discovered sitemap. It assesses sitemap syntax and URL hygiene, not Search Console processing.
- Run `scripts/metadata-audit.py` and `scripts/schema-audit.py` on representative rendered pages. JSON-LD and meta tags belong in HTML/templates, not separate “SEO files.”
- Check AEO manually on priority pages: a real customer question, a direct accurate answer, visible evidence/sources, useful headings, and content that works outside its page context. Do not add filler FAQs.
- Performance needs field data (CrUX/Search Console) and a lab test such as PageSpeed Insights. A single script fetch is diagnostic, not a Core Web Vitals result.
- Hosting configuration should be read from existing Vercel, Netlify, Nginx, Apache, CDN, framework, or CMS files. Do not change headers, redirects, WAF, DNS, caching, or deployment settings during an audit.

## Safe generation gate

After the audit, create a small plan that names: the exact missing applicable file, the responsible platform mechanism, source data supplied by the owner, deployment path, and validation method. Then stop for explicit approval.

- Never overwrite an existing root file, even if it looks incomplete.
- Never create a verification file/token or an `ads.txt` seller record from a guess.
- Do not alter deployment, DNS, CDN, WAF, cache, redirects, or robots policy without explicit approval.
- Prefer native mechanisms: Django sitemaps, Next.js metadata routes, WordPress core/plugin output, or the host's documented static-public directory.
- A local file existing in source code does not prove it is deployed; validate the production URL after an approved release.

## Nepal-specific audit additions

Apply only when Nepal is a target market. Check `lang` and hreflang implementation for real English/Nepali pages, and sample English, Nepali (Devanagari), and Roman Nepali customer questions. Verify real NAP facts, `+977` phone formatting where applicable, `addressCountry: "NP"` only when it matches visible content, genuine service areas, and mobile performance on likely networks. Do not invent city pages, language variants, payment methods, or business-profile data.
