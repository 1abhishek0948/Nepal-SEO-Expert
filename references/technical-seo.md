# Technical SEO

Contents: crawlability, indexability, canonicals, sitemaps, JavaScript rendering, status codes and redirects, HTTPS, mobile, Core Web Vitals, structured data basics, international SEO, verification checklist.

Confirm version-sensitive points against Google Search Central before stating them as current.

## 1. Crawlability

- **robots.txt** controls crawling, not indexing. A URL blocked in robots.txt can still be indexed (without content) if it is linked elsewhere. To keep a page out of the index, allow crawling and use `noindex` (meta robots or `X-Robots-Tag`), or require authentication.
- Check that `/robots.txt` returns 200, is plain text, does not block CSS, JS or images needed for rendering, does not block important sections, and references the sitemap with an absolute URL (`Sitemap: https://example.com/sitemap.xml`).
- Never combine `Disallow` with `noindex` on the same URL: Google cannot see the noindex if it cannot crawl the page.
- Staging sites: protect with HTTP authentication, not just robots.txt. Verify that no staging `noindex` ships to production (a classic launch bug).
- Internal links must be real `<a href>` links. Navigation that exists only as JavaScript click handlers cannot be reliably discovered.
- Avoid infinite crawl spaces: calendar widgets, unbounded filters and sort parameters, session IDs in URLs, internal search result pages.

## 2. Indexability

- Important pages should return HTTP 200, carry no `noindex`, have a self-referencing canonical (or one pointing to the intended preferred URL), be linked internally, and be listed in the sitemap.
- Check both the `<meta name="robots">` tag and the `X-Robots-Tag` response header. Either can carry `noindex`.
- Soft 404s are pages returning 200 with "not found" or empty thin content. Return a real 404 or 410 for missing pages.
- Search Console's Pages (indexing) report and URL Inspection give the authoritative reason a URL is not indexed. Scripts cannot replace them.

## 3. Canonicals and duplicate content

- `rel="canonical"` is a hint, not a directive. Use absolute URLs, one canonical per page, in the `<head>` (or in an HTTP header for non-HTML files).
- Consolidate duplicates caused by `http` vs `https`, `www` vs non-www, trailing slash, uppercase vs lowercase, tracking parameters, sort or filter parameters, print versions, and variant pages.
- Prefer a 301 redirect for true duplicates users should never see. Use canonical when both URLs must stay accessible.
- Each paginated page (page 2, 3, ...) should canonicalize to itself, not to page 1. Google does not use `rel=prev/next`.
- A canonical must point to a 200, indexable page. Do not canonicalize to redirects or noindex pages.
- Pick one host and protocol and redirect all others in a single 301 hop.

## 4. XML sitemaps

- Limits: 50,000 URLs and 50 MB uncompressed per sitemap file. Use a sitemap index for more.
- Include only canonical, indexable (200) URLs. Exclude redirects, 404s, noindex pages, and parameter duplicates.
- All URLs absolute, with the same host and protocol as the canonical site.
- `<lastmod>` is used only when it is consistently accurate (it reflects a meaningful content change). Do not set it to "now" on every build. Use W3C date format (`2026-11-04` or full ISO 8601).
- Google ignores `<priority>` and `<changefreq>`. Leaving them out is fine.
- Submit the sitemap in Search Console and reference it in robots.txt. Bing Webmaster Tools accepts the same file.
- Image, video and news sitemap extensions are optional. Use them only when relevant.
- Use what the stack already provides: Django `django.contrib.sitemaps`, Next.js `app/sitemap.ts`, WordPress core sitemaps or the SEO plugin already in use.

## 5. JavaScript and rendering

- Google renders JavaScript, but rendering is deferred and can fail. Critical content, links, titles, canonicals and structured data should be in the initial HTML where possible (server-side rendering or static generation).
- Client-only pages that set metadata after load are a risk. Verify with URL Inspection (crawled page and screenshot).
- Do not use URL fragments (`#/page`) for distinct content. Use the History API with real paths.
- Lazy-loaded content must load without user interaction. Use `loading="lazy"` for below-the-fold images only, never for the LCP image.
- Google describes dynamic rendering as a workaround, not a long-term solution.

## 6. Status codes and redirects

- 301 or 308 for permanent moves, 302 or 307 for temporary ones. Avoid chains (aim for one hop) and loops.
- 404 or 410 for removed content. Build a helpful custom 404 page that returns a real 404 status.
- 5xx errors and slow responses reduce crawl rate. Use 503 with `Retry-After` for planned downtime.
- For migrations or URL changes: map old URLs to new ones one to one, keep redirects for at least a year, and update internal links, the sitemap and canonicals.

## 7. HTTPS and security

- Whole site on HTTPS with a valid certificate covering every hostname in use (including `www`), HTTP redirecting to HTTPS, and no mixed content.
- Check Search Console for security issues and manual actions.

## 8. Mobile usability

- Google uses mobile-first indexing: the mobile version is what gets indexed. Mobile and desktop must carry equivalent content, metadata, structured data and links.
- `<meta name="viewport" content="width=device-width, initial-scale=1">` must be present.
- Tap targets not cramped, text readable without zooming, no intrusive interstitials covering main content after a click from search.
- For Nepal audiences, many visitors use mid-range Android phones on variable mobile networks. Test on a throttled 4G profile and a slow-CPU profile, not only on a fast desktop.

## 9. Core Web Vitals and performance

Verify thresholds on web.dev before quoting them:

| Metric | Good threshold (75th percentile) |
|---|---|
| LCP (Largest Contentful Paint) | 2.5 s or less |
| INP (Interaction to Next Paint) | 200 ms or less |
| CLS (Cumulative Layout Shift) | 0.1 or less |

INP replaced FID in March 2024. Field data (Chrome UX Report, Search Console's Core Web Vitals report) is what counts. Lab data (Lighthouse) helps diagnose. If the site lacks enough traffic for field data, say so instead of inventing numbers.

Common fixes:
- **LCP:** optimize and correctly size the hero image, serve WebP or AVIF, add `fetchpriority="high"` to the LCP image, preload critical resources, reduce server response time (caching, CDN), remove render-blocking CSS and JS.
- **INP:** break up long JavaScript tasks, defer non-critical third-party scripts, reduce main-thread work, avoid heavy hydration.
- **CLS:** set `width` and `height` (or `aspect-ratio`) on images, iframes and ads; reserve space for embeds; avoid inserting content above existing content; use `font-display` with metric-compatible fallbacks.
- **General:** Brotli or gzip, HTTP caching headers, minimal third-party tags, and a CDN with an edge reasonably close to the audience. For Nepal audiences, check latency from South Asia.
- Page experience is a minor signal compared with relevance. Do not trade content quality for tiny score gains.

Measure with PageSpeed Insights, Search Console, Chrome UX Report, Lighthouse and WebPageTest.

## 10. Structured data basics

- Prefer JSON-LD. Markup must describe content that is visible to users on that page.
- Validate with the Rich Results Test and the Schema Markup Validator. Monitor Search Console enhancement reports.
- Eligibility rules change. For example, FAQ rich results are limited to well-known authoritative government and health sites, and HowTo rich results were retired. Check the current Search Gallery before promising any rich result.
- See `aeo.md` for answer-oriented markup and `scripts/schema-audit.py` for a quick check.

## 11. International and multilingual SEO

- Use separate URLs per language or region version (subdirectory such as `/ne/`, subdomain, or ccTLD). Do not rely on cookies, IP redirects or JavaScript to switch language.
- `hreflang` annotations (in `<head>`, HTTP header or sitemap) must be reciprocal (each version lists all others and itself), use absolute URLs, and use valid codes: `en`, `ne`, `en-NP`, `en-US`, `ne-NP`. Include `x-default` for a fallback or language selector page.
- Language codes are ISO 639-1 and region codes ISO 3166-1 alpha-2 (Nepal is `NP`). A region alone (`NP`) is invalid.
- Translate genuinely. Avoid publishing unreviewed machine translation at scale.
- Set `<html lang="...">` per page (`ne` for Nepali, `en` for English).
- A ccTLD (`.np`, `.com.np`) is a strong geo signal. Generic TLDs rely on hreflang, content, local signals and Search Console settings. Check current Search Console options, since the International Targeting report has been retired.
- Google does not use `<meta name="keywords">`, and `geo.*` meta tags are not a ranking signal.

## 12. Verification checklist

- [ ] robots.txt reachable and not blocking key content
- [ ] One canonical host and protocol; redirects are single-hop
- [ ] Sitemap valid, clean and submitted
- [ ] Key pages return 200, are indexable, listed in the sitemap and internally linked
- [ ] Rendered HTML contains title, description, canonical, headings, links and JSON-LD
- [ ] Core Web Vitals measured with field data when available
- [ ] hreflang reciprocal and valid (if multilingual)
- [ ] Search Console reviewed for indexing, enhancements, manual actions and security issues
