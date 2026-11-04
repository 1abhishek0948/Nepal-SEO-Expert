# Fictional example: ecommerce audit

**Scope:** `https://example-shop.invalid/` (fictional) · one category and one product page

This is a made-up example. It contains no real prices, analytics, reviews, stock data, or ranking claims.

## Executive summary

The fictional store needs clear canonical handling for filtered category URLs and Product schema that exactly reflects visible price and availability. It should not create `ads.txt` unless it sells programmatic display advertising.

### T-01 Keep filtered URLs out of the primary sitemap

- **Issue or opportunity:** The fictional sitemap includes category URLs with sort and colour query parameters.
- **Evidence:** Verified in this fictional example: sitemap audit output identifies query parameters.
- **Why it matters:** Search engines may spend crawl budget on duplicate variants instead of key categories.
- **Recommended solution:** Decide one policy per filter pattern: self-canonicalize useful indexable landing pages, or canonicalize/noindex non-search pages. Keep non-canonical variants out of the sitemap.
- **Priority:** High
- **Estimated effort:** 2 to 4 hours
- **Validation method:** Re-run the sitemap audit and inspect canonical/robots signals on a representative filter URL.

### S-01 Match Product JSON-LD to visible content

- **Issue or opportunity:** The fictional product JSON-LD says `InStock` while the page visibly says unavailable.
- **Evidence:** Verified in this fictional example: rendered HTML and JSON-LD comparison.
- **Why it matters:** Structured data that contradicts visible content can mislead users and reduce trust.
- **Recommended solution:** Generate price, currency, and availability from the same approved product data used on the page. Do not create ratings or reviews that do not exist.
- **Priority:** High
- **Estimated effort:** 1 to 2 hours
- **Validation method:** Compare rendered page facts with JSON-LD and run the Schema Markup Validator.

### F-01 Do not add ads.txt by default

- **Issue or opportunity:** The fictional store has no evidence of programmatic advertising sales.
- **Evidence:** Assumption. No advertising operations information was provided.
- **Why it matters:** An `ads.txt` record needs authorised seller data and is not an ecommerce SEO requirement.
- **Recommended solution:** Mark `ads.txt` as not applicable unless the advertising owner supplies authorised seller records.
- **Priority:** Low
- **Estimated effort:** 5 minutes to record the decision
- **Validation method:** Confirm the business model with the owner; do not create the file without supplied records.
