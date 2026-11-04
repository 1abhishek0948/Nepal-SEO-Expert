# On-Page SEO

Contents: titles, meta descriptions, headings, URLs, content structure, internal linking, images, links, snippets, page-type notes.

## Titles (`<title>`)

- Unique per page, descriptive, matching the page's primary topic and intent. Put the most important words first, brand last (or omit on the homepage if the brand is the topic).
- Roughly 50 to 60 characters is a rule of thumb because Google truncates by pixel width, not characters. Do not report "over 60 characters" as an error; report it as "may be truncated".
- Google may rewrite titles that are missing, stuffed, boilerplate, or mismatched with the page. A rewritten title is a hint to improve the source title, not a penalty.
- Avoid keyword lists and repeated boilerplate ("Home | Home | Company").
- Nepal: for bilingual sites, keep the title in the page's language. Mixing Devanagari and Latin in one title is fine when it reflects real search behavior, but avoid stuffing both.

## Meta descriptions

- Not a ranking factor. They can be used as the snippet when they describe the page better than on-page text; otherwise Google generates the snippet from content.
- Unique, accurate summary with a reason to click, about 120 to 160 characters as a guide. No quotes that break HTML.
- Missing descriptions on important pages is a Low-to-Medium issue, not Critical. Duplicate descriptions across many pages is worth fixing in templates.
- `<meta name="keywords">` is ignored by Google; recommend removing only as cleanup.

## Headings

- Exactly one clear `<h1>` per page is a good convention (HTML allows more, but one keeps structure clear). It should match the page's main topic.
- Use `<h2>`/`<h3>` to organize sections logically. Headings are for structure, not styling, and not for keyword repetition.
- Headings written as the questions users ask help both readers and answer engines (see `aeo.md`).
- Do not skip headings purely for design reasons; use CSS for styling.

## URLs

- Short, readable, lowercase, hyphen-separated, stable. Reflect the hierarchy (`/services/web-design/`). Avoid IDs, session parameters, and deep nesting where possible.
- Choose one trailing-slash convention. Do not change URLs without 301 redirects.
- Nepali slugs: Google handles Unicode URLs, but Latin transliterated slugs are easier to share and type. If using Devanagari, they are percent-encoded when copied; pick one approach per site and be consistent. Do not mix transliteration spellings for the same page.

## Content on the page

- Satisfy the search intent first: informational, navigational, commercial investigation, transactional, local. Check what actually ranks for the query and what format it takes (guide, list, product page, map pack).
- Put the primary answer or offer near the top, then supporting depth.
- Original, useful, accurate; clear authorship and dates for editorial content; real contact and business information.
- Avoid: thin pages, near-duplicate pages with swapped city names, text hidden with CSS, auto-generated filler, content written only for search engines.
- Keyword use: use natural language and related terms/entities. No density targets exist.

## Internal linking

- Every important page reachable within a few clicks from the homepage through crawlable `<a href>` links. Orphan pages (no internal links) are often missed.
- Use descriptive anchor text ("Kathmandu web design services") instead of "click here" or "read more".
- Link from high-authority pages (homepage, popular posts) to priority pages. Add contextual links inside body copy, plus breadcrumbs, related-content blocks, and hub pages for topic clusters.
- Fix internal links that redirect or 404. Link to canonical URLs directly.
- Use `rel="nofollow"`/`sponsored`/`ugc` on paid, affiliate, and user-generated outbound links as appropriate.

## Images

- Descriptive file names and meaningful `alt` text (describes the image for accessibility; do not stuff keywords). Decorative images get `alt=""`.
- Responsive sizes (`srcset`, `sizes`), modern formats, explicit width and height, compression. Lazy load below the fold only.
- Use `<img>` (or `<picture>`) elements with real `src`. Images set only as CSS backgrounds are not indexed as images.
- Place images near relevant text. Consider an image sitemap only for image-heavy sites.

## Links, snippets, and SERP appearance

- Outbound links to credible sources support trust for factual content. Check for broken outbound links.
- Control snippets with `max-snippet`, `nosnippet`, `data-nosnippet` only with a business reason; restrictive snippet settings can reduce visibility in search and AI features.
- Open Graph and Twitter Card tags affect social sharing, not rankings, but are cheap polish (`og:title`, `og:description`, `og:image`, `og:url`).
- Favicon: provide a crawlable favicon (square, multiple of 48px, stable URL) so the brand icon can appear in results.
- Breadcrumb markup (`BreadcrumbList`) is eligible for rich display when matching visible breadcrumbs.

## Page-type quick checks

| Page type | Check |
|---|---|
| Homepage | Clear brand and category terms, links to key sections, Organization/WebSite schema, consistent NAP |
| Service page | One service per page, who/where it serves, process, proof (cases, reviews that are real), clear CTA, contact options |
| Product page | See `ecommerce-seo.md` |
| Blog post | Author, dates, original insight, internal links to related pages, sources |
| Category/hub | Unique intro, crawlable pagination, filtered pages controlled |
| About/contact | Real people and addresses, helps E-E-A-T and local trust |
| Portfolio | Descriptive project pages with outcomes, not only image galleries; clear name and specialty |

## Quick severity guide

- Critical: noindex or canonical pointing wrongly on key pages; title missing on key pages along with other indexing blockers.
- High: duplicate titles across key pages, missing H1/unclear topic on key pages, orphaned priority pages.
- Medium: weak descriptions, thin internal anchors, missing alt text on informative images.
- Low: Open Graph gaps, keywords meta tag cleanup.
