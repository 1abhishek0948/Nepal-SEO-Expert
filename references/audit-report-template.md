# SEO, AEO and GEO Audit Report Template

Use this structure for every audit. Fill each section from evidence. Delete sections that do not apply (for example the Nepal section for a site that does not target Nepal) and say why.

Rules for the report:
- Mark every finding **Verified** (observed in code, fetched page, or script output) or **Assumption** (inferred, needs confirmation).
- Never invent metrics, competitor data, search volumes or rankings. Write "Not measured" or "Unknown" and name the tool that would provide the number.
- Do not promise rankings, traffic or AI citations.
- Keep language plain. Sort findings by priority within each section.

---

# SEO / AEO / GEO Audit: [Site name or domain]

**Date:** [YYYY-MM-DD]
**Prepared for:** [Name]
**Scope:** [URLs and/or project path audited; pages sampled; what was not examined]
**Data sources:** [Script outputs, fetched pages, Search Console access yes/no, Analytics access yes/no, Pagespeed Insights run yes/no]

## 1. Executive summary

- Overall assessment in 3 to 5 sentences.
- Top 5 priorities (one line each, with priority level).
- What is working well.
- What could not be verified and why.

## 2. Website type and target audience

| Item | Finding | Status |
|---|---|---|
| Website type | [Business, ecommerce, SaaS, blog, ...] | Verified / Assumption |
| Business model | | |
| Target markets and cities | | |
| Languages | [English / Nepali / Roman Nepali] | |
| Tech stack and rendering | [Framework, SSR / SSG / CSR, CMS] | |
| Primary conversion goals | | |

## 3. Technical SEO findings

Cover: crawlability, indexability, canonicals, sitemap, robots.txt, redirects and status codes, HTTPS, mobile, Core Web Vitals, JavaScript rendering, structured data validity, hreflang.

### Applicable-file matrix

Record each item as **Present**, **Missing**, **Conditional**, **Optional**, or **Not applicable**. A missing conditional or optional file is not a defect by itself.

| Item | Status | Applicability/evidence | Recommendation (if any) |
|---|---|---|---|
| robots.txt | | | |
| Primary sitemap / sitemap index | | | |
| News, image, video sitemap | | | |
| llms.txt | | | |
| gemini.txt | Do not create as a standard | | |
| ads.txt | | | |
| security.txt | | | |
| Webmaster verification | | | |

### Hosting, performance, and crawler access

Cover existing hosting/CDN/WAF evidence, redirects and cache headers without changing them. Separate crawler policy and evidence by **search**, **training**, **AI/search retrieval**, and **user-triggered fetch**. State what cannot be verified without logs, vendor IP validation, Search Console, or field Core Web Vitals.

[Findings in the format below]

## 4. On-page SEO findings

Cover: titles, descriptions, headings, URLs, internal links, images, content quality and intent match.

## 5. AEO opportunities

Cover: priority questions, direct-answer opportunities, FAQ, definition, comparison and how-to opportunities, structured data that matches visible content.

## 6. GEO opportunities

Cover: original value, expertise and authorship signals, entity information, sources and references, crawler access (including AI crawlers), consistency of business information, measurement of AI referrals.

## 7. Nepal-specific SEO opportunities

Cover: Nepali, English and Roman Nepali keyword coverage, city and area pages, Google Business Profile, NAP consistency, citations, LocalBusiness schema, reviews process, local content, mobile performance on typical networks, multilingual setup.

## 8. Competitor and keyword opportunities

State the method (for example manual SERP review of N queries on [date] from [location]). Include only observed data.

| Query or topic | Intent | Source | Who ranks (observed) | Opportunity |
|---|---|---|---|---|

Search volume column only if taken from a named tool. Otherwise omit it.

## 9. Prioritized implementation roadmap

| Phase | Items | Effort | Dependencies |
|---|---|---|---|
| Phase 1 (week 1): Critical and quick wins | | | |
| Phase 2 (weeks 2 to 4): High | | | |
| Phase 3 (month 2 to 3): Medium | | | |
| Ongoing: Low and monitoring | | | |

End with: **"Which of these would you like me to implement? No files will be changed until you approve."**

## 10. Recommended KPIs

Name the source for each. Set baselines from real data when available; otherwise "baseline to be captured first".

| KPI | Source | Baseline | Review cadence |
|---|---|---|---|
| Indexed pages vs submitted pages | Search Console | | Monthly |
| Organic clicks and impressions (country-filtered) | Search Console | | Monthly |
| Clicks to priority pages | Search Console | | Monthly |
| Core Web Vitals pass rate | Search Console / CrUX | | Monthly |
| Organic conversions or leads | Analytics | | Monthly |
| Business Profile calls, directions, website clicks | GBP Performance | | Monthly |
| Review count and recency | GBP | | Monthly |
| AI referral sessions | Analytics referrers | | Monthly |
| AI citation sample (fixed query list) | Manual log | | Quarterly |

---

## Finding format

Use this block for every finding. All seven fields are required.

### [ID] [Short title]

- **Issue or opportunity:** [what is wrong or possible]
- **Evidence:** [file path, URL, script output; label Verified or Assumption]
- **Why it matters:** [impact on crawling, indexing, relevance, users, trust, local visibility, or AI discoverability]
- **Recommended solution:** [specific action; for code changes name the file or template and the approach]
- **Priority:** Critical | High | Medium | Low
- **Estimated effort:** [for example 15 minutes, 2 hours, 1 to 2 days]
- **Validation method:** [how to confirm: tool, URL, expected result]

### Priority definitions

- **Critical:** Blocks crawling or indexing of important pages, or sends wrong canonical, noindex or redirect signals. Fix immediately.
- **High:** Materially limits visibility, trust or conversion on key pages. Fix in the next sprint.
- **Medium:** Worthwhile improvement with moderate impact.
- **Low:** Polish or long-term hygiene.

### Example finding

### T-01 Homepage canonical points to staging domain

- **Issue or opportunity:** `<link rel="canonical">` on the homepage references `https://staging.example.com/`.
- **Evidence:** Verified. metadata-audit.py output for `https://example.com/` shows canonical `https://staging.example.com/`.
- **Why it matters:** Google may treat the staging URL as the preferred version and drop or demote the production page.
- **Recommended solution:** Generate the canonical from the production site URL setting in the base template; ensure staging is protected by authentication.
- **Priority:** Critical
- **Estimated effort:** 30 minutes
- **Validation method:** Re-run metadata-audit.py; confirm canonical equals the page URL; inspect the URL in Search Console and check "User-declared canonical" and "Google-selected canonical".

---

## Implementation and validation report (after approval)

Use this section after changes are made.

| Finding ID | Change made | Files touched | Validation performed | Result | Still to verify (needs the user) |
|---|---|---|---|---|---|

Include a list of files changed, any new dependencies (ideally none), and rollback notes. State clearly what cannot be validated from the environment (for example Search Console indexing, Rich Results Test, field Core Web Vitals) and give the exact steps for the owner to run.
