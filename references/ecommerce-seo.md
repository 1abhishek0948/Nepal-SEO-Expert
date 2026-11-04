# Ecommerce SEO

Contents: architecture, category pages, product pages, variants, faceted navigation, structured data, merchant listings, reviews, out-of-stock handling, performance and trust, Nepal notes, checklist.

Also applies to tourism packages, hotel rooms, real estate listings and course catalogs, which share the same listing-and-detail pattern.

## 1. Site architecture

- Shallow, logical hierarchy: Home > Category > Subcategory > Product. Every product reachable through crawlable category links and pagination.
- Clean URLs: `/category/subcategory/product-name/`. Avoid IDs and parameters in indexable URLs. One canonical URL per product regardless of the path used to reach it.
- Breadcrumbs matching the hierarchy, with `BreadcrumbList` markup.
- Keep internal search result pages out of the index (`noindex`), but allow crawling so the tag is seen.

## 2. Category pages

Category pages usually carry the highest commercial value.
- Target the broad commercial query ("men's trekking boots"). Unique title, H1 and introductory copy that helps buyers choose (buying criteria, sizing, differences), placed so it does not push products below the fold.
- Crawlable pagination with real links. Each page self-canonical. Avoid "load more" that exposes products only after JavaScript interaction unless it also has crawlable paginated URLs.
- Avoid thin category pages (one or two products); merge or noindex them.
- Link to important subcategories and best sellers from the category.

## 3. Product pages

- Unique title (product name, key attribute, brand), unique description (not manufacturer copy pasted across many sites), clear H1.
- Show key facts in HTML text: price in NPR with currency, availability, SKU or model, brand, size, color, material, warranty, delivery estimate, return policy.
- Several high-quality, compressed images with descriptive alt text. Video where helpful.
- Real customer reviews and Q&A that are visible on the page.
- Related products and category links via crawlable anchors.
- Unique content matters most for products where you are the only seller or have first-hand knowledge (tests, measurements, photos).

## 4. Variants

- Prefer one canonical product URL with variant selection (size, color) when variants differ only by attribute. Use separate URLs for variants only when each has distinct demand and unique content, and then give each a self-canonical.
- Variant URLs created by parameters should canonicalize to the main product unless intentionally indexed.
- Make sure the default variant's price and availability match the structured data.

## 5. Faceted navigation

- Facets (filters and sorts) can create millions of URL combinations. Decide which facet combinations match real search demand (for example "red running shoes") and make those indexable with clean URLs and unique titles.
- Block or neutralize the rest: keep them out of the sitemap, add `noindex`, canonicalize to the main category, or prevent crawling of parameter patterns with robots.txt (remember robots.txt prevents crawling, so noindex will not be seen on blocked URLs). Choose one approach per pattern and test.
- Never link every filter combination with followable links if they would create crawl traps.

## 6. Structured data

- **Product** with **Offer**: `name`, `image`, `description`, `sku`/`gtin` if available, `brand`, `offers` (`price`, `priceCurrency` such as `NPR`, `availability`, `url`, `priceValidUntil` if relevant). Values must match the visible page.
- **Merchant return policy, shipping details:** add when the data is accurate and the business is eligible (check current Google documentation).
- **AggregateRating / Review:** only with real reviews displayed on the page, about the product itself. Never mark up self-written or copied reviews. Do not use site-wide ratings on product pages.
- **BreadcrumbList** for navigation. **Organization** with logo and contact details sitewide.
- Validate with the Rich Results Test. Merchant listing eligibility may require a Google Merchant Center feed; check availability for Nepal in Google's current documentation before promising anything. Do not promise Shopping visibility.

## 7. Out-of-stock, discontinued and expired products

- Temporarily out of stock: keep the page, show availability clearly, offer alternatives or notify-me, and update `availability` in schema.
- Permanently discontinued: 301 redirect to the closest replacement or category if a good match exists; otherwise return 404 or 410. Do not redirect everything to the homepage.
- Seasonal or recurring items: keep the URL stable year to year.

## 8. Performance and UX

- Product images are usually the LCP element. Size properly, use modern formats, and set explicit dimensions.
- Avoid layout shift from late-loading banners, reviews widgets or personalization.
- Keep checkout, cart and account pages out of the index (`noindex` or robots.txt as appropriate). They should still work fast on mobile.

## 9. Nepal notes

- Show prices in NPR and clarify VAT if applicable. State delivery coverage by city or district, delivery times, and cash on delivery availability if offered.
- Show supported payment options (for example eSewa, Khalti, ConnectIPS, bank transfer, cards) only if actually enabled.
- Provide Nepali and English product details where the audience uses both. Do not duplicate content under multiple URLs without `hreflang`.
- Local contact methods (phone, WhatsApp, Viber) near the buy button build trust.
- If the store has a physical shop, add a GBP profile and LocalBusiness data (see `local-seo-nepal.md`).

## 10. Checklist

- [ ] Hierarchy shallow and crawlable; canonical URL per product
- [ ] Category pages have unique intro, crawlable pagination, no thin pages
- [ ] Product pages have unique copy, visible price and availability, real reviews only
- [ ] Facets controlled; indexable combinations deliberate
- [ ] Product schema matches visible data; validated
- [ ] Out-of-stock and discontinued handling defined
- [ ] Cart, checkout, account, internal search excluded from the index
- [ ] LCP image optimized; no layout shift on product pages
