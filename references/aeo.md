# AEO: Answer Engine Optimization

Contents: what AEO is, finding questions, writing answerable content, content patterns, structured data, accessibility to engines, what to avoid, measurement, audit checklist.

AEO means making content easy to understand, extract and trust when a search engine or assistant answers a question directly (featured snippets, People Also Ask, AI summaries, voice assistants). It builds on normal SEO. There is no special markup that guarantees an answer or snippet.

## 1. Find the real questions

Use only sources that exist. Never invent question volumes.

- Search Console Performance report: filter queries that start with who, what, why, how, when, where, can, does, is, best, vs, near me.
- Google's autocomplete, People Also Ask and Related searches (observe manually; note them as observations, not volume data).
- Customer sources: support emails, WhatsApp and Messenger questions, sales calls, site search logs, reviews, comments, community forums, social media questions.
- Competitor and SERP review: what format answers the query (paragraph, list, table, video, map)?
- Nepal: collect questions in English, Nepali and Roman Nepali (for example how-to and cost questions phrased the way locals type them). Check how people actually search; do not machine-translate keyword lists.

Record each question with its source and intent (informational, comparison, local, transactional).

## 2. Write answerable content

- Put a **direct answer first**: one to three sentences (roughly 40 to 60 words is a useful guide, not a rule) immediately under a heading that matches the question. Then add depth, examples, caveats and sources.
- Be specific and accurate: numbers with units and dates, names, prices with currency (NPR where relevant), eligibility criteria, steps and prerequisites. State the date or "last reviewed" for facts that change (fees, laws, schedules).
- Define terms where first used. Answer the question as asked before introducing nuance.
- Use headings that reflect user language, in logical order. One topic per section so passages can stand alone when extracted.
- Prefer plain, unambiguous language. Avoid pronouns without clear referents at the start of sections, since extracted passages lose context.
- Show experience and sourcing: author byline with real credentials, original data or photos, links to primary sources (laws, official fee schedules, standards bodies).
- Keep the answer consistent everywhere (site, Business Profile, social profiles, directories).

## 3. Content patterns that fit answer formats

| Pattern | Use when | Structure |
|---|---|---|
| Definition | "What is X" | Heading as question, 1 to 2 sentence definition, then context and example |
| Step-by-step | "How to X" with a real sequence | Ordered list with one action per step, prerequisites first, expected result last |
| Comparison | "X vs Y", "best X for Y" | Table with the same criteria for each option, then a recommendation with reasoning |
| List | "types of", "best ways" | Short list with one-line explanation per item |
| Cost / time | "how much", "how long" | Range with conditions and date, what changes the price |
| Local | "near me", "in Pokhara" | Name, area, hours, contact, real distinguishing details |
| Troubleshooting | "why is X not working" | Symptom, likely causes in order, fix for each |

Add an FAQ section only when users genuinely ask those questions and the answers add value beyond the page body. Do not add filler FAQs to every page, and do not repeat the same FAQ block across many pages.

## 4. Structured data for answers

Structured data helps engines understand content; it does not guarantee display. Rules:

- Markup must match visible page content. Never mark up content that users cannot see.
- Prefer JSON-LD. Validate with the Rich Results Test and Schema Markup Validator.
- Check the current Google Search Gallery before recommending anything for rich results.

Current-eligibility notes (verify, as these change):
- **FAQPage:** Google restricts FAQ rich results to well-known authoritative government and health sites. For most sites the markup will not produce a rich result. It can still be valid and semantically accurate when a visible FAQ exists, but do not promise visibility and do not add it just for rich results.
- **HowTo:** Google retired HowTo rich results. Do not add it for SERP appearance.
- **Article / BlogPosting / NewsArticle:** useful for authorship and dates; headline, image, datePublished, dateModified, author.
- **BreadcrumbList:** matches visible breadcrumbs.
- **Organization / LocalBusiness / Person / WebSite:** entity clarity (name, logo, URL, sameAs links to real profiles, contact, address).
- **Product / Offer / Review (real reviews only):** see `ecommerce-seo.md`.
- **QAPage:** only for pages with a single question and user-submitted answers (forum-style).
- **VideoObject, Event, Course, JobPosting:** use when the content type truly applies and meets Google's guidelines.

## 5. Accessibility to engines

- Answers must be in crawlable, indexable HTML text, not only in images, PDFs behind forms, or content loaded after interaction.
- Do not block Googlebot or Bingbot. For AI-specific crawlers, see `geo.md`.
- Avoid text hidden in collapsed elements only if it is hidden from users with no way to see it; ordinary accordions with visible toggles are fine.
- Make tables real `<table>` elements with header cells. Make lists real `<ol>`/`<ul>`.
- Provide transcripts or text summaries for video and audio content.

## 6. What to avoid

- Padding pages with unneeded FAQs, question-stuffed headings, or repeated templated answers.
- Answers without sources on YMYL topics (health, finance, legal, safety). Cite official sources and have qualified review.
- Contradictory facts across pages.
- Schema for content not on the page, self-serving review markup, or fabricated Q&A.
- Over-short answers that omit conditions and risk misleading readers.

## 7. Measurement

- Search Console: impressions and clicks for question queries; featured snippet presence is observed manually in the SERP, not reported as a separate metric.
- Track rankings only with tools the client already uses; never invent positions.
- Analytics: engagement on answer pages; conversions that follow.
- Voice and assistant visibility is hard to measure; note it as unmeasurable rather than guessing.

## 8. AEO audit checklist

- [ ] Priority questions listed with a source for each
- [ ] Each target page opens its answer section with a direct, accurate answer
- [ ] Headings reflect user questions in logical order
- [ ] Opportunities identified: definitions, comparisons, steps, local answers
- [ ] FAQs only where genuinely useful and visible; no duplicated blocks
- [ ] Structured data matches visible content; checked with validators
- [ ] Authorship, dates and sources present on factual content
- [ ] Key facts consistent across pages and profiles
