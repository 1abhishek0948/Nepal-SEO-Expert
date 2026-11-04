# GEO: Generative Engine Optimization

Contents: what GEO is and is not, principles, content signals, entity and brand signals, technical access and AI crawlers, platform notes, measurement, honest limits, audit checklist.

GEO means improving the odds that a site is understood, trusted and referenced by AI-powered search experiences: Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Bing/Copilot and similar. Platform behavior changes quickly. Verify platform details against official documentation before stating them, and never claim that any technique guarantees inclusion or citation.

## 1. Principles

- Google states that AI features in Search use the same fundamentals as regular search. There is no separate markup or file required to appear in AI Overviews or AI Mode; pages must be indexed and eligible to show a snippet. Treat GEO as a superset of good SEO plus entity clarity and genuine reputation.
- AI answers are assembled from retrieved passages. Pages that are crawlable, clear, specific, current and corroborated are easier to retrieve and cite.
- Tactics that rely on tricking models (hidden instructions in text, cloaking, mass-generated pages, prompt-injection text on pages) are manipulation, risk penalties, and must never be recommended.

## 2. Content signals

- **Original and useful:** first-hand experience, original data, local knowledge, examples, photos, case studies, clear opinions backed by evidence. Content that only rephrases what is already everywhere gives an engine no reason to cite you.
- **Accurate and verifiable:** specific claims with sources, dates and units. Link to primary sources (laws, official fee schedules, standards, research). Correct errors visibly.
- **Demonstrable expertise (E-E-A-T):** real authors with bios and credentials, an about page, editorial policy for news and YMYL topics, reviewer attribution where qualified review matters, contact details.
- **Self-contained passages:** each section answers one thing under a descriptive heading and makes sense when extracted. See `aeo.md`.
- **Freshness where it matters:** visible "last updated" dates for time-sensitive facts, with real updates (not date-bumping).
- **Comprehensive coverage:** cover the follow-up questions a reader would have. Use topic clusters with internal links rather than many thin pages.

## 3. Entity and brand signals

- Clear entity information: legal or trading name, what the business does, where it operates, who runs it, how to contact it. Put this on the About and Contact pages and in Organization or LocalBusiness schema that matches the visible content.
- Consistent naming and business facts across the site, Google Business Profile, social profiles, business directories and press mentions.
- `sameAs` links in schema only to real profiles the business controls or that clearly represent it (official social profiles, Wikipedia or Wikidata if an entry genuinely exists).
- Genuine brand mentions and authority: quality coverage, partnerships, speaking, associations, citations by relevant publications, real reviews and community presence. These come from being worth mentioning. Do not buy links, mass-submit to directories, run fake review campaigns or use fake personas.
- In Nepal, relevant legitimate signals include verified Business Profile, listings on credible local directories and industry bodies, local media or blog coverage, university and community partnerships, and registered business details published consistently (see `local-seo-nepal.md`).

## 4. Technical access

- Pages must be crawlable, indexable and fast, with main content in HTML text. See `technical-seo.md`.
- Do not use `nosnippet`, `max-snippet:0` or similar directives on content you want shown in AI features, unless that is a deliberate business decision. Google's snippet controls also govern use in AI features.
- Review robots.txt for AI crawlers. Allowing or blocking is a business decision; present trade-offs and let the owner decide. Verify current user-agent names and their rules in each vendor's documentation, because they change. Keep these decisions separate: search, training, AI/search retrieval, and user-triggered fetching are not one "AI" permission. Commonly documented examples at the time of writing:

| Purpose | User-agent (verify) | Notes |
|---|---|---|
| Google Search and AI features | Googlebot | Same crawler as ordinary Search |
| Google Gemini and Vertex training/grounding control | Google-Extended | Robots.txt control token; does not affect Search ranking or inclusion |
| OpenAI search results | OAI-SearchBot | Allows appearance in ChatGPT search results |
| OpenAI model training | GPTBot | Separate from search |
| OpenAI user-initiated browsing | ChatGPT-User | Fetches pages when a user asks; OpenAI says robots rules may not apply to these user-initiated requests |
| Perplexity search index | PerplexityBot | Verify in Perplexity's docs |
| Anthropic | ClaudeBot, Claude-SearchBot, Claude-User | Verify in Anthropic's docs |

  Blocking training crawlers while allowing search crawlers is a common choice, but it is the owner's decision. Robots.txt is advisory; reputable bots follow it. Do not report a user-triggered fetcher as "blocked" only from robots.txt without confirming the vendor's current policy.
- CDN, WAF and bot-protection rules sometimes block legitimate crawlers by accident. Check logs and test with the vendor's documented IP ranges or verification method instead of assuming.
- `llms.txt`: a proposed community convention with no confirmed support from major search engines. Optional and harmless when accurate, but do not present it as a ranking or citation lever. `gemini.txt` is not a standard; do not recommend it.
- Render-critical content server-side. Many AI crawlers do not execute JavaScript.
- Provide clean, stable URLs, descriptive titles, canonical tags and a working sitemap so engines can retrieve and attribute correctly.

## 5. Platform notes (verify before relying on them)

- **Google AI Overviews and AI Mode:** eligibility follows normal indexing and snippet rules. Links shown come from pages Google deems helpful for the query. Measure impressions and clicks in Search Console; Google reports AI features traffic within overall Web search data, without a separate AI-only report (verify current reporting).
- **ChatGPT search:** uses web retrieval and cites sources. Allow OAI-SearchBot if you want to appear. Referral traffic may show up with a `chatgpt.com` referrer or `utm_source=chatgpt.com` (verify in your analytics).
- **Perplexity:** retrieves and cites sources heavily. Referral appears as `perplexity.ai`.
- **Bing / Copilot:** Bing Webmaster Tools and IndexNow can speed discovery. Bing's index also feeds several AI products.
- Different engines favor different sources. Do not optimize for one engine's quirk at the expense of users.

## 6. Measurement

Use only data you can observe; never fabricate citations or share of voice.

- **Referral traffic:** in Analytics (GA4), segment sessions by source or referrer for chatgpt.com, perplexity.ai, copilot.microsoft.com, gemini.google.com, claude.ai and similar. Referrers vary and some visits arrive without a referrer, so counts are a floor.
- **Server logs:** count hits by documented AI crawler user-agents to confirm they can fetch key pages.
- **Manual citation sampling:** a fixed list of 20 to 50 representative questions, asked periodically in each platform (logged out, same location setting). Record whether the site is cited, which URL, date, and platform. Treat results as a noisy sample, because AI answers vary between runs. State the method and sample size whenever reporting.
- **Search Console:** impressions and clicks for informational queries as a proxy for AI feature exposure.
- **Brand demand:** branded search impressions over time, direct traffic, and mentions found through manual search or alerts.
- Paid tracking tools exist but are not required. If the owner uses one, treat its numbers as vendor estimates.

## 7. Honest limits

- No technique guarantees inclusion in AI answers. Models and retrieval systems change without notice.
- Report effort as "improves the odds" and link each recommendation to a measurable proxy.
- Reputation and original contribution take months, not days.
- Do not copy competitors' content or restructure everything solely for AI. Users still matter most.

## 8. GEO audit checklist

- [ ] Key pages indexed, snippet-eligible and rendered in HTML
- [ ] Original value on top pages (data, experience, local expertise)
- [ ] Authors, dates, sources and editorial policy visible
- [ ] Consistent entity facts (name, address, phone, descriptions) across site and profiles
- [ ] Organization or LocalBusiness schema matches visible content, `sameAs` is accurate
- [ ] robots.txt AI-crawler decisions made deliberately and documented
- [ ] No accidental blocking of crawlers in WAF, CDN or login walls
- [ ] Authentic third-party mentions and reviews strategy (no purchased or fake signals)
- [ ] Measurement set up: referral segments, log review, manual citation sampling log
