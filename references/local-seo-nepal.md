# Local SEO and the Nepal Module

Contents: when to apply this module, Nepal search behavior, keyword research, locations and city pages, Google Business Profile, NAP and citations, LocalBusiness schema, reviews, content opportunities, trust and payment signals, multilingual setup, measurement, prohibited tactics, audit checklist.

Apply this module only when the audience includes Nepal. Do not assume every site targets Nepal or Kathmandu; confirm the market first. Everything here is guidance. Never invent search volumes, rankings or business facts.

## 1. Nepal search behavior

- Users search in **English**, **Nepali in Devanagari** (for example नेपालमा ...), and **Roman Nepali** (Nepali typed in Latin letters, with inconsistent spellings). Many queries mix English product or service terms with Nepali words.
- Mobile-first, often on mid-range Android phones and variable connections. Fast, light pages matter.
- Search intent is frequently local ("near me", area names, landmarks) and price-sensitive (cost, rate, fee, price in Nepal).
- Regional languages (Maithili, Bhojpuri, Newari, Tamang and others) matter in specific regions. Research before investing; do not assume demand.
- Dates and numbers: Bikram Sambat (BS) calendar is used locally alongside AD. Amounts appear in NPR and in lakh and crore. Match how the audience writes them.

## 2. Keyword research for Nepal

Use real data sources only: Search Console queries, Google autocomplete and related searches, Google Trends (relative interest only), Google Keyword Planner if the owner has an Ads account (ranges, not exact), customer questions, social media comments, WhatsApp and Messenger inquiries, and competitor SERP review. Label anything observed manually as an observation.

For each topic, build three keyword columns and record the source for each:

| Topic | English | Nepali (Devanagari) | Roman Nepali / transliteration |
|---|---|---|---|

Guidance:
- Do not translate word for word. Interview users or check how they actually phrase queries.
- Transliteration varies (for example "pasal" vs "pasaal"). Cover the common variants naturally in content (for example in a short note, headings or image captions) without stuffing.
- Check each variant's SERP. If Google shows the same results for variants, one strong page is enough; if the SERPs differ, consider separate content only when each page offers real, distinct value.
- Use Nepali place names in both scripts where relevant (काठमाडौं / Kathmandu, पोखरा / Pokhara).
- Pair service terms with places only when the business actually serves those places.
- Keep a note of assumptions: "Assumption: users in Biratnagar search in Nepali more than English. Verify in Search Console."

## 3. Locations and service areas

Nepal has seven provinces and hundreds of local levels (metropolitan and sub-metropolitan cities, municipalities, rural municipalities), each divided into wards. People often describe locations by city, ward, tole (neighbourhood), and landmarks.

Cities and areas to support when relevant: Kathmandu, Lalitpur, Bhaktapur, Pokhara, Biratnagar, Lahan, Butwal, Birgunj, Dharan, Itahari, Janakpur, Bharatpur (Chitwan), Hetauda, Nepalgunj, Dhangadhi, and others. Treat this list as examples, not a requirement.

Rules:
- Identify where the business really operates: physical locations, service areas, delivery areas, or fully online/national.
- Do not target a city the business does not serve.
- Greater Kathmandu Valley (Kathmandu, Lalitpur, Bhaktapur) is competitive and often searched by neighbourhood (for example Baneshwor, Thamel, Patan, Lazimpat). Use neighbourhoods only for real service coverage.

### City or area landing pages

Create them only when:
1. The business has a real presence or genuine service in that place.
2. Each page offers unique useful content: local team or branch details, address or service coverage, local pricing or delivery notes, local examples or case studies (with permission), local FAQs from real customers, travel directions or landmarks, opening hours, real photos.

Avoid doorway pages: near-identical pages that only swap the city name, mass-produced for every town. Google treats these as spam. If two cities cannot honestly have distinct content, serve them from one "service areas" page with a clear list.

Structure: `/locations/pokhara/` or `/pokhara/` with clear unique title, H1, local content, embedded map (optional), contact, internal links from the locations hub and relevant service pages.

## 4. Google Business Profile (GBP)

For businesses with a physical location or in-person service.

- Claim and verify the one profile per business location. Do not create duplicates. Search for existing profiles first and claim them.
- Use the real-world business name as customers know it (no keyword additions such as "Best Plumber Kathmandu").
- Choose the most specific primary category, add relevant secondary categories.
- Address: accurate, as customers would find it. Nepali addresses are often descriptive; follow GBP's address fields and add precise map pin placement. Service-area businesses without a customer-facing location can hide the address and define service areas.
- Never use a fake address, a virtual office, a co-working address to look local, or a PO box as a physical location.
- Phone in international format (+977...) with a local number the business really answers. Website link to the most relevant landing page (usually the homepage or the location page).
- Hours, special hours (festivals such as Dashain and Tihar), services, products, attributes, and description (accurate, no promotions or URLs in the description).
- Photos and short videos: real storefront, interior, team, work samples. Add regularly.
- Posts and updates: optional, useful for events or offers.
- Respond to reviews professionally, including negative ones.
- Verification can involve video or other methods depending on the business and region. Follow the options Google offers; do not buy verification help.
- Also consider Bing Places and Apple Business Connect if relevant to the audience.

## 5. NAP consistency and citations

- **NAP** (name, address, phone) must match exactly across the website, GBP, social profiles and directories. Use one canonical form (including +977 country code format) and reuse it.
- Put NAP in crawlable text in the site header or footer and on the contact page, not only in an image.
- Citations: list the business only on legitimate sources that real customers or partners use: Google Business Profile, Bing Places, Apple Business Connect, Facebook page, relevant industry associations and chambers (for example national and local chambers of commerce or sector bodies such as tourism associations, where the business is genuinely a member), reputable local directories, and local news or blogs that cover the business.
- Verify that any directory is active, reputable and relevant before submitting. Avoid mass-submission to low-quality directory lists.
- Audit existing listings for old addresses, old phone numbers and duplicates. Fix or request removal of incorrect duplicates rather than creating more listings.
- Recording evidence: keep a log of where each listing lives, the login owner, and the date checked.

## 6. LocalBusiness structured data

Use the most specific `LocalBusiness` subtype that fits (for example `Dentist`, `Restaurant`, `Hotel`, `TravelAgency`, `RealEstateAgent`, `ProfessionalService`). Include only values that are true and visible on the page. Replace all placeholders; remove any property you cannot support.

```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "https://example.com/#business",
  "name": "REPLACE business name",
  "url": "https://example.com/",
  "telephone": "+977-REPLACE",
  "image": "https://example.com/images/storefront.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "REPLACE tole / street, ward no.",
    "addressLocality": "REPLACE city",
    "addressRegion": "REPLACE province",
    "addressCountry": "NP"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 0.0,
    "longitude": 0.0
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "10:00",
    "closes": "17:00"
  }],
  "areaServed": ["REPLACE city 1", "REPLACE city 2"],
  "sameAs": ["REPLACE official profile URLs only"]
}
```

Notes:
- Nepal's working week varies by sector (many offices are Sunday to Friday, with Saturday as the weekly holiday). Use the business's real hours.
- Add `priceRange`, `aggregateRating`, or `review` only when they are accurate, visible and compliant with Google's review guidelines. Self-serving review markup for your own business is not eligible for review rich results.
- Use latitude and longitude from the actual location. Never estimate.
- One block per location on its page; the homepage can carry the main Organization or LocalBusiness block.
- Postal codes are not widely used in everyday Nepali addresses; include `postalCode` only if the business actually uses one.

## 7. Reviews

- Ask real customers to review, via GBP's review link, after real transactions. Make it easy; do not require positive reviews, do not offer rewards for reviews, and do not filter who is invited ("review gating").
- Never write, buy, trade or fake reviews, and do not post reviews as employees without disclosure.
- Respond to every review within a reasonable time. Treat negative reviews as service feedback. Report policy-violating reviews through GBP.
- Quote reviews on the site only when they are real, attributed with permission, and not misrepresented.

## 8. Nepal-specific content opportunities

Ideas only. Validate each with real queries before committing:
- Local how-to and cost guides (for example fees, registration steps and timelines for a service in Nepal), updated with dates.
- Process explainers for local rules: business registration, VAT and PAN, work permits, land purchase, tourism permits, import rules. Cite official sources (relevant ministries and departments), and say when to consult a professional.
- Seasonal and festival content (Dashain, Tihar, Holi, Chhath, Teej, Indra Jatra, wedding season) with real offers and availability.
- Local comparisons and best-of lists with transparent criteria, based on real experience.
- Tourism and hospitality: trekking permits, route conditions, altitude and weather by month, safety, packing lists, transport options, with accurate dates and sources.
- Education: admissions timelines, entrance exam guides, scholarship information, college comparisons.
- Real estate: neighbourhood guides, price ranges with date and source, legal checklists.
- Ecommerce: delivery coverage across districts, cash on delivery, return policy in plain language, local payment methods.
- Local case studies, customer stories (with permission), team and branch pages.
- Bilingual pages where users read both languages (see section 10).

## 9. Trust and payment signals

Show only what is true:
- Registered business name and registration or PAN details where the business is happy to display them.
- Contact options people in Nepal use: phone, WhatsApp, Viber, Messenger, email, map location.
- Payment methods that are actually supported (for example eSewa, Khalti, ConnectIPS, bank transfer, cards, cash on delivery). Prices in NPR, with VAT clarity where relevant.
- Clear delivery, refund and warranty policies, privacy policy, and terms.
- Real team photos and names, branch photos, and awards or certifications that can be verified.

## 10. Multilingual setup for Nepal

- Decide per page: English only, Nepali only, or both. Do not publish low-quality machine translations.
- Use separate URLs per language (for example `/ne/`), `<html lang="ne">` or `lang="en"`, and reciprocal `hreflang` (`en`, `ne`, optionally `en-NP`, `ne-NP`, plus `x-default`).
- Use Unicode (UTF-8) and a font stack that renders Devanagari correctly on Android (check fallback fonts and line height; conjuncts clip if line height is too tight).
- Keep titles and descriptions in the page language.
- Avoid auto-redirecting by IP or browser language; offer a visible language switcher.

## 11. Measurement

- GBP Performance: searches, calls, direction requests, website clicks (observed numbers only).
- Search Console: queries including place names and Nepali or Roman Nepali terms, filtered by country Nepal.
- Analytics: traffic by city, device, and language; calls and WhatsApp clicks as conversion events.
- Local pack and SERP checks: manual checks from real locations or through the owner's existing rank tool. Results vary by location, so record where and when checks were made. Do not invent ranking positions.
- Review count and recency over time, as recorded in GBP.

## 12. Prohibited tactics

- Fake addresses, virtual offices presented as branches, or duplicate profiles for the same location.
- Fake, purchased or incentivized-with-conditions reviews; review gating.
- Keyword-stuffed business names or descriptions.
- Doorway pages for every city.
- Paid or spammy link and citation schemes; mass directory blasting.
- Marking up reviews, awards, hours or addresses that are not real or not visible.
- Misleading claims such as "No. 1 in Nepal" without evidence.

## 13. Nepal audit checklist

- [ ] Target markets and cities confirmed with the owner
- [ ] Keyword set covers English, Nepali and Roman Nepali, with sources noted
- [ ] City pages exist only for real service locations and are genuinely unique
- [ ] One verified GBP per location; no duplicates; categories, hours and photos complete
- [ ] NAP consistent in site text, schema, GBP and citations (+977 format)
- [ ] LocalBusiness schema matches visible content; `addressCountry` is NP
- [ ] Real review process in place; responses given
- [ ] Citations only on legitimate, relevant sources
- [ ] Multilingual pages use correct `lang` and `hreflang`; Devanagari renders correctly
- [ ] Mobile speed checked on throttled mobile connection
