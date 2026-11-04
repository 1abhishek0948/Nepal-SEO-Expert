# Fictional example: local business audit

**Scope:** `https://example-clinic.invalid/` (fictional) · homepage and contact page only

This is an example of reporting style, not an audit of a real clinic. All observations below are fictional.

## Executive summary

The sample site makes its service clear but needs a deliberate sitemap and better bilingual page signals. Its address and phone number must be confirmed against the business owner before they are placed in schema or listings.

### T-01 Publish an applicable sitemap

- **Issue or opportunity:** The fictional `robots.txt` has no Sitemap line and the sampled site has no discovered sitemap.
- **Evidence:** Verified in this fictional example: root-file audit output.
- **Why it matters:** Important public pages may be harder for search engines to discover.
- **Recommended solution:** After approval, use the current website platform's native sitemap generator. Include only canonical, indexable pages and add its absolute URL to the existing `robots.txt` mechanism.
- **Priority:** High
- **Estimated effort:** 1 to 2 hours
- **Validation method:** Re-run the root-file and sitemap audits; submit the URL in the owner's verified Search Console property.

### L-01 Confirm bilingual service pages before adding hreflang

- **Issue or opportunity:** The sample claims Nepal relevance, but no confirmed Nepali-language page was available to inspect.
- **Evidence:** Assumption. The project brief, not a rendered page, mentions Nepali.
- **Why it matters:** Hreflang helps only when genuine language alternatives exist.
- **Recommended solution:** Ask the owner for approved English and Nepali content. Add `lang` and reciprocal hreflang only after each version is published and has equivalent helpful content.
- **Priority:** Medium
- **Estimated effort:** Half a day after approved translations are available
- **Validation method:** Inspect both rendered pages and validate reciprocal alternate URLs.

### A-01 Answer an actual appointment question

- **Issue or opportunity:** A sample homepage has no visible answer to “How do I book an appointment?”
- **Evidence:** Verified in this fictional example: manual review of the visible homepage text.
- **Why it matters:** A clear answer helps visitors and makes the page easier to understand when retrieved out of context.
- **Recommended solution:** Add a concise, visible booking section with the real booking channels, hours, and any conditions. Do not add an FAQ unless this is a genuine repeated question.
- **Priority:** Medium
- **Estimated effort:** 30 minutes once facts are approved
- **Validation method:** Confirm the answer is visible in server-rendered HTML and test the booking path on mobile.
