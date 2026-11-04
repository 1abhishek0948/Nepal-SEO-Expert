# SaaS and Web App SEO

Contents: site structure, landing and feature pages, pricing, comparison and alternatives pages, integrations and templates, docs and help center, programmatic pages, JavaScript apps, product-led content, measurement, checklist.

Applies to SaaS products, online tools, marketplaces and custom web applications with a public marketing surface.

## 1. Separate the marketing site from the app

- Public, indexable: homepage, feature and use-case pages, pricing, integrations, comparisons, blog, docs, changelog, customer stories, templates, public tool pages.
- Not indexable: logged-in app screens, dashboards, settings, checkout, user-generated private content. Use authentication; add `noindex` where pages are reachable but pointless to index.
- Put marketing pages on server-rendered or statically generated routes. Single-page apps that render marketing content only on the client risk poor indexing. See `technical-seo.md` section 5.
- Subdomain vs subdirectory: docs and blog are generally easier to keep consolidated in subdirectories (`/blog/`, `/docs/`). Do not migrate just for SEO without a plan and redirects.

## 2. Homepage, feature and use-case pages

- Match intent. A homepage cannot rank for everything. Create dedicated pages for each important feature, use case, industry or audience, each with a distinct purpose, not near-duplicates.
- Lead with the problem and outcome in plain language, state who it is for, show the product (screenshots with alt text, short video with transcript), and provide proof (real customer logos, case studies, metrics you can substantiate).
- Clear primary call to action. Reduce friction (free trial or demo path).
- Internal links between related features, use cases and docs.

## 3. Pricing page

- Crawlable, text-based pricing with plans, limits, billing terms and currency. For Nepal and South Asia, clarify NPR or USD billing and local payment options only if supported.
- Include a short FAQ addressing real objections (billing, cancellations, data security) if users actually ask them.
- Avoid hiding pricing behind forms unless the business model requires it; "contact sales" only pricing limits both search and AI answers.

## 4. Comparison and alternatives pages

- "X vs Y" and "Alternatives to X" pages can capture high-intent queries. Be honest and verifiable: feature tables with dates, accurate competitor facts from public sources, clear criteria, and the cases where the competitor is the better choice.
- Do not make defamatory or unverifiable claims, and respect trademark use (nominative fair use). Update when competitors change.
- Do not mass-generate comparison pages for every possible competitor with templated text; each page needs real analysis.

## 5. Integrations, templates and use-case libraries

- Integration pages can rank for "[tool] + [tool]" queries. Each needs unique substance: what the integration does, setup steps, screenshots, limitations.
- Template and example galleries can work well if each has unique value and a crawlable URL. Do not publish thousands of near-empty variants.

## 6. Documentation and help center

- Docs rank for long-tail troubleshooting and how-to queries and often get cited by AI engines.
- Descriptive page titles using the user's words (error messages, task names), stable URLs, version info, last updated date, code samples in text (not images), clear step lists.
- Search-friendly navigation: sidebar with crawlable links, breadcrumbs, previous and next links, related articles.
- Avoid duplicating the same doc across versions without canonicals; point older versions to the latest where appropriate.
- Consider `TechArticle` or `Article` markup only when it matches the page. Use `SoftwareApplication` markup for the product page only with truthful values (name, category, operating system, offers), and check current Google guidance for eligibility before expecting rich results.

## 7. Programmatic SEO (use carefully)

Programmatic pages (many pages generated from data) can be legitimate: for example public tool pages, location data, integration directories. Scaled content abuse is a spam policy violation. Before recommending it:

1. Is there real query demand (validated, not guessed)?
2. Does each page contain unique, useful data or functionality beyond template text?
3. Would a human editor be comfortable with each page?
4. Can quality be maintained (accuracy, freshness)?
5. Start with a small batch, measure indexing and engagement in Search Console, expand only if pages are indexed and perform.

If the answer to 2 is no, do not build the pages. Never recommend doorway pages or auto-spun text.

## 8. JavaScript-heavy products

- Verify rendered HTML via URL Inspection. Ensure titles, canonicals, headings, links and JSON-LD exist after rendering and ideally in the initial HTML.
- Use real URLs for public views. Avoid hash routing.
- Keep JavaScript bundles lean. Check INP on interactive pages and LCP on landing pages.

## 9. Product-led and community content

- Public tool pages, calculators, benchmarks and original research earn natural links and AI citations because they offer something unique.
- Publish genuine expertise: engineering and product blog posts, how-we-built-it write-ups, data studies, with named authors.
- Customer stories with real quotes and measured results. Never fabricate testimonials or logos.

## 10. Measurement

- Search Console: queries and pages by intent group (brand, category, comparison, docs).
- Analytics: signups, trial starts and demo requests by landing page; assisted conversions.
- Track branded search growth as a sign of awareness.
- AI referrals and citations: see `geo.md`.

## 11. Checklist

- [ ] Public marketing pages rendered server-side or statically; app pages excluded
- [ ] Distinct pages for key features, use cases and audiences
- [ ] Pricing visible and crawlable
- [ ] Comparison pages honest and verifiable
- [ ] Docs crawlable, versioned, and have useful titles
- [ ] Programmatic pages validated by demand and unique value
- [ ] JS rendering and INP checked
- [ ] Conversion tracking tied to landing pages
