#!/usr/bin/env python3
"""
schema-audit.py - read-only structured data (schema.org) audit.

Extracts JSON-LD (plus a list of Microdata / RDFa types), checks that JSON-LD
parses, that common types carry their key properties, that placeholder values
are not left in, and (heuristically) that marked-up text appears in the visible
page text.

INPUTS (any mix)
  * http(s) URLs, HTML files, or directories containing .html/.htm files

DEPENDENCIES
  Python 3.8+ standard library only. No paid APIs.

SAFETY
  * Never writes to the audited project. Output goes to stdout.
  * Only GET requests with an identifying User-Agent and a delay (default 1s).
  * Audit sites you own or have permission to audit.

IMPORTANT LIMITS
  * This is a heuristic linter, not Google's validator. Required and
    recommended properties and rich result eligibility change. Always confirm
    with the Rich Results Test (https://search.google.com/test/rich-results) and
    the Schema Markup Validator (https://validator.schema.org/).
  * Reads server-rendered HTML only. JSON-LD injected by JavaScript is not seen.
  * The visible-text check is approximate. A miss means "verify manually".

EXAMPLES
  python3 schema-audit.py https://example.com/
  python3 schema-audit.py ./dist/products/*.html --format json
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import gzip
from html.parser import HTMLParser

UA = "nepal-seo-expert-audit/1.0 (read-only SEO audit script)"
MAX_BYTES = 10 * 1024 * 1024
SEVERITIES = ["Critical", "High", "Medium", "Low", "Info"]

LOCAL_BUSINESS_TYPES = {
    "LocalBusiness", "Restaurant", "Hotel", "LodgingBusiness", "Store", "Dentist", "MedicalBusiness",
    "ProfessionalService", "TravelAgency", "RealEstateAgent", "FoodEstablishment", "HealthAndBeautyBusiness",
    "AutomotiveBusiness", "FinancialService", "LegalService", "HomeAndConstructionBusiness", "BarOrPub",
    "CafeOrCoffeeShop", "Physician", "Pharmacy", "Hospital", "BeautySalon", "Bakery", "GroceryStore",
    "ShoppingCenter", "SportsActivityLocation", "TouristInformationCenter", "BedAndBreakfast", "Resort",
    "AccountingService", "Attorney", "Electrician", "Plumber", "AutoRepair", "ChildCare", "DaySpa",
}
ARTICLE_TYPES = {"Article", "BlogPosting", "NewsArticle", "TechArticle", "Report", "ScholarlyArticle"}
ORG_TYPES = {"Organization", "Corporation", "NGO", "EducationalOrganization", "School", "CollegeOrUniversity",
             "GovernmentOrganization", "OnlineStore", "OnlineBusiness"}
HELPER_TYPES = {
    "PostalAddress", "GeoCoordinates", "GeoShape", "OpeningHoursSpecification", "Question", "Answer", "ListItem",
    "ContactPoint", "Brand", "Rating", "MonetaryAmount", "QuantitativeValue", "Place", "PropertyValue", "Country",
    "AdministrativeArea", "City", "State", "OfferShippingDetails", "MerchantReturnPolicy", "ShippingDeliveryTime",
    "DefinedRegion", "WebPage", "ItemList", "Thing", "VirtualLocation", "PerformanceRole", "InteractionCounter",
    "SearchAction", "ReadAction", "EntryPoint", "Language", "HowToStep", "HowToSection", "Clip", "SeekToAction",
}
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")
PLACEHOLDER_RE = re.compile(r"\b(REPLACE|TODO|TBD|lorem ipsum|your[- ]?(business|company|site)[- ]?name)\b|example\.(com|org)", re.I)

# type -> (required, recommended). Heuristic lists, verify against current Google documentation.
RULES = {
    "Organization": (["name"], ["url", "logo", "sameAs", "contactPoint"]),
    "LocalBusiness": (["name", "address"], ["telephone", "url", "image", "openingHoursSpecification", "geo", "priceRange"]),
    "Product": (["name"], ["image", "description", "offers", "brand", "sku"]),
    "Offer": (["price", "priceCurrency"], ["availability", "url"]),
    "Article": (["headline"], ["image", "datePublished", "dateModified", "author", "publisher"]),
    "BreadcrumbList": (["itemListElement"], []),
    "WebSite": (["name", "url"], []),
    "FAQPage": (["mainEntity"], []),
    "Person": (["name"], ["url", "jobTitle", "sameAs"]),
    "Event": (["name", "startDate", "location"], ["endDate", "description", "image", "offers", "eventStatus"]),
    "VideoObject": (["name", "thumbnailUrl", "uploadDate"], ["description", "contentUrl", "embedUrl", "duration"]),
    "Review": (["reviewRating", "author"], ["itemReviewed", "reviewBody", "datePublished"]),
    "AggregateRating": (["ratingValue"], ["bestRating"]),
    "ImageObject": ([], ["contentUrl"]),
}


# ----------------------------------------------------------------------------
# Fetching helpers (same behavior as metadata-audit.py)
# ----------------------------------------------------------------------------

def is_url(value):
    return re.match(r"^https?://", value, re.I) is not None


def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.5", "Accept-Encoding": "gzip"})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        status, headers, final = resp.status, resp.headers, resp.geturl()
        body = resp.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        status, headers, final = exc.code, exc.headers, url
        try:
            body = exc.read(MAX_BYTES + 1)
        except Exception:
            body = b""
    except Exception as exc:
        return {"url": url, "error": str(exc)}
    if headers.get("Content-Encoding", "").lower() == "gzip":
        try:
            body = gzip.decompress(body)
        except Exception:
            pass
    return {"url": url, "final_url": final, "status": status, "headers": headers, "body": body[:MAX_BYTES]}


def decode_html(body, headers=None):
    charset = None
    if headers is not None:
        m = re.search(r"charset=([\w-]+)", headers.get("Content-Type", ""), re.I)
        if m:
            charset = m.group(1)
    if not charset:
        m = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", body[:4096], re.I)
        if m:
            charset = m.group(1).decode("ascii", "ignore")
    for enc in (charset, "utf-8"):
        if enc:
            try:
                return body.decode(enc)
            except (LookupError, UnicodeDecodeError):
                continue
    return body.decode("utf-8", "replace")


def collect_sources(inputs, max_pages):
    sources = []
    for item in inputs:
        if is_url(item):
            sources.append(("url", item, item))
        elif os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
                for name in sorted(files):
                    if name.lower().endswith((".html", ".htm")):
                        p = os.path.join(root, name)
                        sources.append(("file", os.path.relpath(p, item), p))
        elif os.path.isfile(item):
            sources.append(("file", item, item))
        else:
            print("warning: skipping %r (not a URL, file or directory)" % item, file=sys.stderr)
    if len(sources) > max_pages:
        print("note: %d pages found, auditing the first %d (use --max-pages)" % (len(sources), max_pages), file=sys.stderr)
        sources = sources[:max_pages]
    return sources


# ----------------------------------------------------------------------------
# HTML extraction
# ----------------------------------------------------------------------------

class SchemaParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.jsonld = []          # raw strings
        self._ld_buf = None
        self.microdata_types = []
        self.rdfa_types = []
        self._skip = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "script" and "ld+json" in a.get("type", "").lower():
            self._ld_buf = []
        elif tag in ("script", "style", "noscript", "template"):
            self._skip += 1
        if a.get("itemtype"):
            self.microdata_types.append(a["itemtype"])
        if a.get("typeof"):
            self.rdfa_types.append(a["typeof"])

    def handle_endtag(self, tag):
        if tag == "script" and self._ld_buf is not None:
            self.jsonld.append("".join(self._ld_buf))
            self._ld_buf = None
        elif tag in ("script", "style", "noscript", "template") and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._ld_buf is not None:
            self._ld_buf.append(data)
        elif self._skip == 0:
            self.text_parts.append(data)


def norm(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()


# ----------------------------------------------------------------------------
# Schema walking and checks
# ----------------------------------------------------------------------------

def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def types_of(node):
    return [t for t in as_list(node.get("@type")) if isinstance(t, str)]


def walk(obj, path="$"):
    """Yield (path, node) for every dict that has an @type, at any depth."""
    if isinstance(obj, dict):
        if "@type" in obj:
            yield path, obj
        for key, value in obj.items():
            if key.startswith("@") and key != "@graph":
                continue
            for item in walk(value, "%s.%s" % (path, key)):
                yield item
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            for item in walk(value, "%s[%d]" % (path, i)):
                yield item


def has_value(node, prop):
    value = node.get(prop)
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    if isinstance(value, (list, dict)) and not value:
        return False
    return True


def canonical_rule_key(t):
    if t in LOCAL_BUSINESS_TYPES:
        return "LocalBusiness"
    if t in ARTICLE_TYPES:
        return "Article"
    if t in ORG_TYPES:
        return "Organization"
    return t if t in RULES else None


def add(findings, severity, code, message, evidence=""):
    findings.append({"severity": severity, "code": code, "message": message, "evidence": evidence})


def check_strings_for_placeholders(obj, findings, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            check_strings_for_placeholders(v, findings, "%s.%s" % (path, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            check_strings_for_placeholders(v, findings, "%s[%d]" % (path, i))
    elif isinstance(obj, str) and PLACEHOLDER_RE.search(obj):
        add(findings, "High", "S003", "Placeholder or sample value left in structured data.", "%s = %r" % (path, obj[:80]))


def check_node(node, path, findings, visible, parent_types):
    for t in types_of(node):
        key = canonical_rule_key(t)
        if key:
            required, recommended = RULES[key]
            for prop in required:
                if not has_value(node, prop):
                    add(findings, "High", "S101", "%s is missing required-style property '%s' (heuristic; verify in the Rich Results Test)." % (t, prop), path)
            missing = [p for p in recommended if not has_value(node, p)]
            if missing:
                add(findings, "Low", "S102", "%s is missing commonly recommended properties: %s." % (t, ", ".join(missing)), path)
        elif t not in HELPER_TYPES:
            add(findings, "Info", "S190", "Type '%s' has no built-in rules in this script; validate manually." % t, path)

        # --- type-specific checks
        if key == "LocalBusiness":
            addr = node.get("address")
            if isinstance(addr, dict):
                if not addr.get("addressCountry"):
                    add(findings, "Medium", "S111", "address has no addressCountry (use ISO code, e.g. NP for Nepal).", path)
                if str(addr.get("addressCountry", "")).upper() in ("NP", "NEPAL"):
                    tel = str(node.get("telephone", ""))
                    if tel and not tel.replace(" ", "").startswith("+977"):
                        add(findings, "Low", "S112", "Nepal business telephone is not in +977 international format.", tel)
            elif addr is not None and not isinstance(addr, str):
                add(findings, "Medium", "S113", "address should be a PostalAddress object or string.", path)
            geo = node.get("geo")
            if isinstance(geo, dict):
                try:
                    if float(geo.get("latitude", 0)) == 0.0 and float(geo.get("longitude", 0)) == 0.0:
                        add(findings, "High", "S114", "geo coordinates are 0,0 (placeholder).", path)
                except (TypeError, ValueError):
                    add(findings, "Medium", "S115", "geo latitude/longitude are not numeric.", path)
            if node.get("aggregateRating") or node.get("review"):
                add(findings, "Medium", "S116",
                    "Review/rating markup on the business's own page is generally not eligible for review rich results "
                    "(self-serving reviews). Use only real, visible reviews and verify eligibility.", path)

        if key == "Organization" and (node.get("aggregateRating") or node.get("review")):
            add(findings, "Medium", "S116", "Self-serving review/rating markup on Organization is generally not eligible for rich results; verify.", path)

        if key == "Product":
            offers = node.get("offers")
            if not offers and not node.get("review") and not node.get("aggregateRating"):
                add(findings, "High", "S121", "Product has none of offers, review or aggregateRating (needed for product rich results).", path)

        if key == "AggregateRating" and not (has_value(node, "reviewCount") or has_value(node, "ratingCount")):
            add(findings, "High", "S124", "AggregateRating needs reviewCount or ratingCount.", path)

        if key == "Offer":
            price = node.get("price")
            if isinstance(price, str) and re.search(r"[^\d.,\s]", price):
                add(findings, "Medium", "S122", "Offer price should be numeric only; put the currency in priceCurrency.", str(price))
            cur = node.get("priceCurrency")
            if cur and not re.match(r"^[A-Z]{3}$", str(cur)):
                add(findings, "Medium", "S123", "priceCurrency should be a 3-letter ISO 4217 code (e.g. NPR, USD).", str(cur))

        if key == "Article":
            headline = str(node.get("headline", ""))
            if len(headline) > 110:
                add(findings, "Low", "S131", "Article headline is %d characters; Google suggests concise headlines (under ~110)." % len(headline), path)
            for dprop in ("datePublished", "dateModified"):
                if node.get(dprop) and not ISO_DATE_RE.match(str(node[dprop])):
                    add(findings, "Medium", "S132", "%s is not ISO 8601." % dprop, str(node[dprop]))

        if key == "BreadcrumbList":
            items = as_list(node.get("itemListElement"))
            for i, it in enumerate(items):
                if not isinstance(it, dict):
                    add(findings, "Medium", "S141", "BreadcrumbList item %d is not an object." % (i + 1), path)
                    continue
                if not it.get("position"):
                    add(findings, "Medium", "S142", "BreadcrumbList item %d has no position." % (i + 1), path)
                if not (it.get("name") or (isinstance(it.get("item"), dict) and it["item"].get("name"))):
                    add(findings, "Medium", "S143", "BreadcrumbList item %d has no name." % (i + 1), path)
                if i < len(items) - 1 and not it.get("item"):
                    add(findings, "Medium", "S144", "BreadcrumbList item %d (not last) has no item URL." % (i + 1), path)

        if key == "FAQPage":
            add(findings, "Info", "S151",
                "FAQ rich results are currently limited to well-known authoritative government and health sites (verify). "
                "Keep FAQPage only if the visible page really contains these questions and answers.", path)
            for q in as_list(node.get("mainEntity")):
                if not isinstance(q, dict):
                    continue
                qtext = q.get("name")
                ans = q.get("acceptedAnswer")
                if not qtext:
                    add(findings, "High", "S152", "FAQ Question has no name.", path)
                if not (isinstance(ans, dict) and ans.get("text")):
                    add(findings, "High", "S153", "FAQ Question has no acceptedAnswer.text.", str(qtext)[:60])
                if qtext and norm(qtext) not in visible:
                    add(findings, "Medium", "S154", "FAQ question text not found in visible page text; marked-up content must be visible. Verify manually.", str(qtext)[:80])

        if t == "HowTo":
            add(findings, "Info", "S161", "HowTo rich results have been retired by Google. Keep only if it accurately mirrors visible steps and has other value.", path)

        # visible-text heuristic for primary names
        for prop in ("headline", "name"):
            val = node.get(prop)
            if isinstance(val, str) and val.strip() and key in ("Article", "Product", "Event", "LocalBusiness"):
                if norm(val) not in visible:
                    add(findings, "Low", "S171",
                        "%s '%s' value was not found verbatim in visible page text (may be fine if the page text differs slightly or is JS-rendered). Verify the markup matches visible content." % (t, prop),
                        str(val)[:80])
                break

    # relative URLs
    for prop in ("url", "logo", "image", "sameAs"):
        for v in as_list(node.get(prop)):
            if isinstance(v, str) and v and not re.match(r"^https?://", v, re.I):
                add(findings, "Low", "S181", "'%s' should be an absolute URL." % prop, v[:80])


def analyze(label, html, status=None):
    parser = SchemaParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as exc:
        return {"page": label, "error": "HTML parse error: %s" % exc, "findings": []}

    findings = []
    visible = norm(" ".join(parser.text_parts))
    nodes_found = []

    if status is not None and status != 200:
        add(findings, "High", "S001", "Page returned HTTP %s." % status)

    if not parser.jsonld and not parser.microdata_types and not parser.rdfa_types:
        add(findings, "Info", "S002", "No structured data found in server-rendered HTML (it may be injected by JavaScript, or simply not used).")

    for idx, raw in enumerate(parser.jsonld, start=1):
        try:
            data = json.loads(raw)
        except ValueError as exc:
            add(findings, "High", "S004", "JSON-LD block %d is not valid JSON: %s" % (idx, exc), raw.strip()[:80])
            continue
        blocks = data if isinstance(data, list) else [data]
        for block in blocks:
            if not isinstance(block, dict):
                add(findings, "Medium", "S005", "JSON-LD block %d contains a non-object value." % idx)
                continue
            ctx = json.dumps(block.get("@context", "")) if "@context" in block else ""
            if "@context" not in block:
                add(findings, "High", "S006", "JSON-LD block %d has no @context (expected https://schema.org)." % idx)
            elif "schema.org" not in ctx:
                add(findings, "High", "S007", "JSON-LD block %d @context does not reference schema.org." % idx, ctx[:80])
            check_strings_for_placeholders(block, findings, "$block%d" % idx)
            for path, node in walk(block, "$block%d" % idx):
                ts = types_of(node)
                nodes_found.append({"type": ts, "path": path})
                parent_types = []
                check_node(node, path, findings, visible, parent_types)

    if parser.microdata_types:
        add(findings, "Info", "S010", "Microdata types present (not validated by this script): %s" % ", ".join(sorted(set(parser.microdata_types))[:8]))
    if parser.rdfa_types:
        add(findings, "Info", "S011", "RDFa types present (not validated by this script): %s" % ", ".join(sorted(set(parser.rdfa_types))[:8]))

    # duplicates: same type repeated for top-level entities
    seen = {}
    for n in nodes_found:
        for t in n["type"]:
            if t in ("Organization", "WebSite", "LocalBusiness") or t in LOCAL_BUSINESS_TYPES:
                seen[t] = seen.get(t, 0) + 1
    for t, count in seen.items():
        if count > 1:
            add(findings, "Low", "S012", "%d %s nodes found on one page. Confirm they are not duplicates." % (count, t))

    findings.sort(key=lambda f: SEVERITIES.index(f["severity"]))
    return {
        "page": label,
        "status": status,
        "json_ld_blocks": len(parser.jsonld),
        "types": sorted({t for n in nodes_found for t in n["type"]}),
        "findings": findings,
    }


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------

def render_text(results):
    lines = []
    counts = {s: 0 for s in SEVERITIES}
    for r in results:
        lines.append("=" * 72)
        lines.append(r["page"])
        if "error" in r:
            lines.append("  ERROR: %s" % r["error"])
            continue
        lines.append("  JSON-LD blocks: %d | types: %s" % (r["json_ld_blocks"], ", ".join(r["types"]) or "none"))
        for f in r["findings"]:
            counts[f["severity"]] += 1
            ev = ("  -> " + f["evidence"]) if f["evidence"] else ""
            lines.append("  [%-8s] %s %s%s" % (f["severity"], f["code"], f["message"], ev))
        if not r["findings"]:
            lines.append("  No findings from automated checks.")
    lines.append("=" * 72)
    lines.append("Pages audited: %d | %s" % (len(results), ", ".join("%s: %d" % (s, counts[s]) for s in SEVERITIES)))
    lines.append("Note: heuristic linter. Confirm with the Rich Results Test and Schema Markup Validator.")
    return "\n".join(lines)


def render_markdown(results):
    lines = ["# Structured data audit", ""]
    for r in results:
        lines.append("## %s" % r["page"])
        if "error" in r:
            lines.append("- ERROR: %s" % r["error"])
            continue
        lines.append("- JSON-LD blocks: %d; types: %s" % (r["json_ld_blocks"], ", ".join(r["types"]) or "none"))
        lines.append("")
        lines.append("| Severity | Code | Finding | Evidence |")
        lines.append("|---|---|---|---|")
        for f in r["findings"]:
            lines.append("| %s | %s | %s | %s |" % (f["severity"], f["code"], f["message"].replace("|", "\\|"), f["evidence"].replace("|", "\\|")))
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only structured data audit for URLs, HTML files, or directories.")
    ap.add_argument("inputs", nargs="+", help="URL(s), HTML file(s), or directory of HTML files")
    ap.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    ap.add_argument("--max-pages", type=int, default=100)
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between remote requests (default 1.0)")
    ap.add_argument("--timeout", type=float, default=15.0)
    args = ap.parse_args(argv)

    sources = collect_sources(args.inputs, args.max_pages)
    if not sources:
        print("error: nothing to audit", file=sys.stderr)
        return 2

    results = []
    first_remote = True
    for kind, label, ref in sources:
        if kind == "url":
            if not first_remote:
                time.sleep(max(args.delay, 0))
            first_remote = False
            resp = http_get(ref, timeout=args.timeout)
            if "error" in resp:
                results.append({"page": label, "error": resp["error"], "findings": []})
                continue
            results.append(analyze(label, decode_html(resp["body"], resp["headers"]), status=resp["status"]))
        else:
            try:
                with open(ref, "rb") as fh:
                    body = fh.read(MAX_BYTES)
            except OSError as exc:
                results.append({"page": label, "error": str(exc), "findings": []})
                continue
            results.append(analyze(label, decode_html(body)))

    if args.format == "json":
        print(json.dumps({"pages": results}, indent=2, ensure_ascii=False))
    elif args.format == "markdown":
        print(render_markdown(results))
    else:
        print(render_text(results))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # output piped to head/less and closed early
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
