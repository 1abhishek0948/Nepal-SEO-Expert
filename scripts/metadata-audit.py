#!/usr/bin/env python3
"""
metadata-audit.py - read-only on-page metadata audit.

Checks title, meta description, robots directives, canonical, viewport, lang,
hreflang, headings, images, links, Open Graph / Twitter tags, JSON-LD presence,
and cross-page duplicates.

INPUTS (any mix)
  * http(s) URLs                  -> fetched with GET (read-only)
  * HTML files                    -> read from disk
  * directories                   -> every .html/.htm file found (recursive)

DEPENDENCIES
  Python 3.8+ standard library only. No paid APIs. No network access is needed
  for local files.

SAFETY
  * Never writes to the audited project. Output goes to stdout only.
  * Only GET requests, sent with an identifying User-Agent and a delay between
    requests (default 1 second). Respect the site owner's rules: audit sites
    you own or have permission to audit.
  * Reads server-rendered HTML only. Metadata injected by JavaScript will not
    be seen; confirm with Search Console URL Inspection before reporting it
    as missing.

EXAMPLES
  python3 metadata-audit.py https://example.com/ https://example.com/about
  python3 metadata-audit.py ./dist --format json
  python3 metadata-audit.py page1.html page2.html --format markdown

Results are heuristics. Length guidelines are rules of thumb: Google truncates
titles and snippets by pixel width, not character count.
"""

import argparse
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "nepal-seo-expert-audit/1.1 (read-only SEO audit script)"
MAX_BYTES = 10 * 1024 * 1024
SEVERITIES = ["Critical", "High", "Medium", "Low", "Info"]
HREFLANG_RE = re.compile(r"^(x-default|[a-z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|\d{3}))?)$")
GENERIC_ANCHORS = {"click here", "read more", "here", "more", "learn more", "link", "this"}
SPA_ROOT_RE = re.compile(r'id=["\'](root|app|__next|__nuxt)["\']', re.I)
TEMPLATE_RE = re.compile(r"\{%|\{\{")


# ----------------------------------------------------------------------------
# Fetching
# ----------------------------------------------------------------------------

def is_url(value):
    return re.match(r"^https?://", value, re.I) is not None


def http_get(url, timeout=15):
    """GET a URL. Returns dict with url, status, headers, body (bytes) or error."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
            "Accept-Encoding": "gzip",
        },
    )
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
    except Exception as exc:  # network errors, timeouts, bad URLs
        return {"url": url, "error": str(exc)}
    if headers.get("Content-Encoding", "").lower() == "gzip":
        try:
            body = gzip.decompress(body)
        except Exception:
            pass
    truncated = len(body) > MAX_BYTES
    return {
        "url": url,
        "final_url": final,
        "status": status,
        "headers": headers,
        "body": body[:MAX_BYTES],
        "truncated": truncated,
    }


def decode_html(body, headers=None):
    charset = None
    if headers is not None:
        match = re.search(r"charset=([\w-]+)", headers.get("Content-Type", ""), re.I)
        if match:
            charset = match.group(1)
    if not charset:
        match = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", body[:4096], re.I)
        if match:
            charset = match.group(1).decode("ascii", "ignore")
    for enc in (charset, "utf-8"):
        if not enc:
            continue
        try:
            return body.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return body.decode("utf-8", "replace")


def collect_sources(inputs, max_pages):
    """Expand inputs into a list of (kind, label, path_or_url)."""
    sources = []
    for item in inputs:
        if is_url(item):
            sources.append(("url", item, item))
        elif os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
                for name in sorted(files):
                    if name.lower().endswith((".html", ".htm")):
                        path = os.path.join(root, name)
                        sources.append(("file", os.path.relpath(path, item), path))
        elif os.path.isfile(item):
            sources.append(("file", item, item))
        else:
            print("warning: skipping %r (not a URL, file or directory)" % item, file=sys.stderr)
    if len(sources) > max_pages:
        print("note: %d pages found, auditing the first %d (use --max-pages)" % (len(sources), max_pages), file=sys.stderr)
        sources = sources[:max_pages]
    return sources


# ----------------------------------------------------------------------------
# HTML parsing
# ----------------------------------------------------------------------------

class PageParser(HTMLParser):
    SKIP_TAGS = ("script", "style", "noscript", "template")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.titles = []
        self._title_buf = None
        self.metas = []
        self.links = []
        self.headings = []
        self._head_level = None
        self._head_buf = []
        self.images = []
        self.anchors = []
        self._a_attrs = None
        self._a_buf = []
        self.jsonld_blocks = 0
        self._skip = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "title":
            self._title_buf = []
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._head_level = int(tag[1])
            self._head_buf = []
        elif tag == "img":
            self.images.append(a)
        elif tag == "a":
            self._a_attrs = a
            self._a_buf = []
        if tag == "script" and "ld+json" in a.get("type", "").lower():
            self.jsonld_blocks += 1
        if tag in self.SKIP_TAGS:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title" and self._title_buf is not None:
            self.titles.append(" ".join("".join(self._title_buf).split()))
            self._title_buf = None
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._head_level is not None:
            text = " ".join("".join(self._head_buf).split())
            self.headings.append((self._head_level, text))
            self._head_level = None
        elif tag == "a" and self._a_attrs is not None:
            text = " ".join("".join(self._a_buf).split())
            self.anchors.append((self._a_attrs, text))
            self._a_attrs = None
        if tag in self.SKIP_TAGS and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._title_buf is not None:
            self._title_buf.append(data)
        if self._head_level is not None:
            self._head_buf.append(data)
        if self._a_attrs is not None:
            self._a_buf.append(data)
        if self._skip == 0:
            self.text_parts.append(data)


# ----------------------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------------------

def meta_content(parser, key, attr="name"):
    out = []
    for m in parser.metas:
        if m.get(attr, "").lower() == key:
            out.append(m.get("content", "").strip())
    return out


def add(findings, severity, code, message, evidence=""):
    findings.append({"severity": severity, "code": code, "message": message, "evidence": evidence})


def analyze(label, html, status=None, headers=None, final_url=None):
    parser = PageParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as exc:
        return {"page": label, "error": "HTML parse error: %s" % exc, "findings": []}

    findings = []
    page_url = final_url if final_url else None
    page_host = urllib.parse.urlparse(page_url).netloc.lower() if page_url else ""

    # --- HTTP-level checks (remote pages only)
    if status is not None and status != 200:
        add(findings, "High", "M001", "Page returned HTTP %s." % status, "status=%s" % status)
    if final_url and final_url.rstrip("/") != label.rstrip("/"):
        add(findings, "Info", "M002", "Request was redirected.", "%s -> %s" % (label, final_url))
    if headers is not None:
        xrt = headers.get("X-Robots-Tag", "")
        if xrt:
            sev = "Critical" if "noindex" in xrt.lower() else "Info"
            add(findings, sev, "M003", "X-Robots-Tag header present. Confirm it is intended.", xrt)

    # --- unrendered template / SPA shell warnings
    if TEMPLATE_RE.search(html):
        add(findings, "Medium", "M004",
            "Source contains template syntax ({% %} or {{ }}). This may be an unrendered template or client-side template. "
            "Audit the rendered page instead of the template file.", "")
    text = " ".join(" ".join(parser.text_parts).split())
    words = len(text.split())
    if words < 40 and SPA_ROOT_RE.search(html):
        add(findings, "Medium", "M005",
            "Very little server-rendered text and a JavaScript app root element were found. Content and metadata may be "
            "rendered client-side. Verify with Search Console URL Inspection (rendered HTML).", "words=%d" % words)

    # --- title
    title = parser.titles[0] if parser.titles else None
    if not parser.titles:
        add(findings, "High", "M101", "Missing <title>.")
    else:
        if len(parser.titles) > 1:
            add(findings, "Medium", "M102", "Multiple <title> elements.", " | ".join(parser.titles))
        if not title:
            add(findings, "High", "M103", "Empty <title>.")
        else:
            if len(title) > 60:
                add(findings, "Low", "M104",
                    "Title is %d characters and may be truncated in results (guideline ~60; truncation is pixel-based)." % len(title), title)
            if len(title) < 15:
                add(findings, "Low", "M105", "Title is very short (%d characters); consider a more descriptive title." % len(title), title)

    # --- description
    descs = meta_content(parser, "description")
    desc = descs[0] if descs else None
    if not descs:
        add(findings, "Medium", "M111", "Missing meta description (Google may generate a snippet from page text; not a ranking factor).")
    else:
        if len(descs) > 1:
            add(findings, "Low", "M112", "Multiple meta description tags.")
        if not desc:
            add(findings, "Medium", "M113", "Empty meta description.")
        elif len(desc) > 160:
            add(findings, "Low", "M114", "Meta description is %d characters (guideline ~160); the snippet may be cut." % len(desc), desc)
        elif len(desc) < 70:
            add(findings, "Low", "M115", "Meta description is short (%d characters)." % len(desc), desc)

    if meta_content(parser, "keywords"):
        add(findings, "Low", "M116", "Meta keywords tag present. Google ignores it; safe to remove as cleanup.")

    # --- robots meta
    for r in meta_content(parser, "robots") + meta_content(parser, "googlebot"):
        low = r.lower()
        if "noindex" in low:
            add(findings, "Critical", "M121", "Robots meta contains noindex. Confirm this page should be excluded from search.", r)
        if "nofollow" in low:
            add(findings, "Medium", "M122", "Robots meta contains nofollow (links on this page do not pass signals).", r)
        if "nosnippet" in low or "max-snippet:0" in low.replace(" ", ""):
            add(findings, "Medium", "M123", "Snippet restriction present; this can reduce visibility in results and AI features.", r)

    # --- canonical
    canonicals = [l.get("href", "").strip() for l in parser.links if "canonical" in l.get("rel", "").lower().split()]
    canonical = canonicals[0] if canonicals else None
    if not canonicals:
        add(findings, "Medium", "M131", "Missing rel=canonical (a self-referencing canonical is recommended).")
    else:
        if len(canonicals) > 1 and len(set(canonicals)) > 1:
            add(findings, "High", "M132", "Multiple conflicting canonical links.", " | ".join(canonicals))
        if not re.match(r"^https?://", canonical, re.I):
            add(findings, "Medium", "M133", "Canonical is empty or not an absolute URL.", canonical)
        else:
            canon_host = urllib.parse.urlparse(canonical).netloc.lower()
            if page_url and canonical.rstrip("/") != page_url.rstrip("/"):
                sev = "High" if canon_host != page_host else "Info"
                add(findings, sev, "M134",
                    "Canonical differs from the page URL. Confirm this is intentional" +
                    (" (different host!)." if canon_host != page_host else "."),
                    "page=%s canonical=%s" % (page_url, canonical))

    # --- viewport, lang, favicon
    if not meta_content(parser, "viewport"):
        add(findings, "High", "M141", "Missing viewport meta tag (mobile usability).")
    if not parser.html_lang:
        add(findings, "Low", "M142", "<html> has no lang attribute.")
    if not any("icon" in l.get("rel", "").lower() for l in parser.links):
        add(findings, "Info", "M143", "No <link rel=icon> found (browsers fall back to /favicon.ico; confirm it exists).")

    # --- hreflang
    hreflangs = [(l.get("hreflang", ""), l.get("href", "")) for l in parser.links
                 if "alternate" in l.get("rel", "").lower().split() and l.get("hreflang")]
    if hreflangs:
        for code, href in hreflangs:
            if not HREFLANG_RE.match(code):
                add(findings, "Medium", "M151", "Invalid hreflang value.", code)
            if not re.match(r"^https?://", href, re.I):
                add(findings, "Medium", "M152", "hreflang href should be an absolute URL.", href)
        codes = [c.lower() for c, _ in hreflangs]
        if "x-default" not in codes:
            add(findings, "Low", "M153", "hreflang set has no x-default entry (recommended for a fallback page).")
        if page_url and not any(h.rstrip("/") == page_url.rstrip("/") for _, h in hreflangs):
            add(findings, "Medium", "M154", "hreflang set does not include a self-referencing entry for this URL.")

    # --- headings
    h1s = [t for lvl, t in parser.headings if lvl == 1]
    if not h1s:
        add(findings, "High", "M161", "No <h1> found.")
    elif len(h1s) > 1:
        add(findings, "Low", "M162", "%d <h1> elements; one clear H1 is the usual convention." % len(h1s), " | ".join(h1s[:3]))
    if any(not t for _, t in parser.headings):
        add(findings, "Low", "M163", "Empty heading element(s) found.")
    prev = 0
    for lvl, t in parser.headings:
        if prev and lvl > prev + 1:
            add(findings, "Low", "M164", "Heading level skips (h%d -> h%d)." % (prev, lvl), t)
            break
        prev = lvl

    # --- images
    no_alt = [i for i in parser.images if "alt" not in i]
    empty_alt = [i for i in parser.images if i.get("alt", None) == ""]
    if no_alt:
        add(findings, "Medium", "M171", "%d image(s) have no alt attribute (use alt=\"\" for decorative images)." % len(no_alt),
            ", ".join(i.get("src", "?")[:60] for i in no_alt[:3]))
    no_dims = [i for i in parser.images if not (i.get("width") and i.get("height"))]
    if no_dims:
        add(findings, "Low", "M172", "%d image(s) lack width/height attributes (layout shift risk)." % len(no_dims))
    if parser.images and len(empty_alt) == len(parser.images):
        add(findings, "Info", "M173", "All images have empty alt text. Informative images should be described.")

    # --- links
    internal = external = 0
    bad_links = 0
    generic = []
    for attrs, atext in parser.anchors:
        href = attrs.get("href")
        if href is None or href.strip() in ("", "#") or href.lower().startswith("javascript:"):
            bad_links += 1
            continue
        if re.match(r"^(mailto:|tel:)", href, re.I):
            continue
        parsed = urllib.parse.urlparse(href)
        if parsed.netloc and page_host and parsed.netloc.lower() != page_host:
            external += 1
        elif parsed.netloc and not page_host:
            external += 1
        else:
            internal += 1
        if atext.strip().lower() in GENERIC_ANCHORS:
            generic.append(atext)
    if bad_links:
        add(findings, "Medium", "M181", "%d anchor(s) without a crawlable href (empty, '#', or javascript:)." % bad_links)
    if generic:
        add(findings, "Low", "M182", "%d link(s) use generic anchor text such as 'click here' or 'read more'." % len(generic))
    if internal == 0 and parser.anchors:
        add(findings, "Low", "M183", "No internal links found on this page.")

    # --- social
    og = {m.get("property", "").lower(): m.get("content", "") for m in parser.metas if m.get("property", "").lower().startswith("og:")}
    missing_og = [k for k in ("og:title", "og:description", "og:image") if not og.get(k)]
    if missing_og:
        add(findings, "Low", "M191", "Missing Open Graph tags: %s (social sharing; not a ranking factor)." % ", ".join(missing_og))
    if not meta_content(parser, "twitter:card"):
        add(findings, "Info", "M192", "No twitter:card meta tag.")

    # --- content size heuristic
    if words < 150 and not (words < 40 and SPA_ROOT_RE.search(html)):
        add(findings, "Low", "M201", "Only about %d words of visible text. Thin content is only a problem if it does not satisfy the intent; verify." % words)

    findings.sort(key=lambda f: SEVERITIES.index(f["severity"]))
    return {
        "page": label,
        "status": status,
        "title": title,
        "title_length": len(title) if title else 0,
        "description": desc,
        "description_length": len(desc) if desc else 0,
        "canonical": canonical,
        "h1": h1s,
        "word_count": words,
        "json_ld_blocks": parser.jsonld_blocks,
        "internal_links": internal,
        "external_links": external,
        "images": len(parser.images),
        "findings": findings,
    }


def cross_page(results):
    """Duplicate titles / descriptions / H1s / canonicals across audited pages."""
    out = []
    for key, label, sev in (("title", "title", "High"), ("description", "meta description", "Medium"), ("canonical", "canonical URL", "Medium")):
        seen = {}
        for r in results:
            val = r.get(key)
            if val:
                seen.setdefault(val.strip().lower(), []).append(r["page"])
        for val, pages in seen.items():
            if len(pages) > 1:
                out.append({"severity": sev, "code": "X001",
                            "message": "Duplicate %s used on %d pages." % (label, len(pages)),
                            "evidence": "%r on: %s" % (val[:80], ", ".join(pages[:5]))})
    seen = {}
    for r in results:
        for h in r.get("h1", [])[:1]:
            seen.setdefault(h.strip().lower(), []).append(r["page"])
    for val, pages in seen.items():
        if len(pages) > 1 and val:
            out.append({"severity": "Medium", "code": "X002",
                        "message": "Same H1 used on %d pages." % len(pages),
                        "evidence": "%r on: %s" % (val[:80], ", ".join(pages[:5]))})
    return out


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------

def render_text(results, cross):
    lines = []
    for r in results:
        lines.append("=" * 72)
        lines.append(r["page"])
        if "error" in r:
            lines.append("  ERROR: %s" % r["error"])
            continue
        lines.append("  status=%s  words=%s  h1=%d  internal links=%s  images=%s  JSON-LD blocks=%s" % (
            r.get("status") or "local file", r["word_count"], len(r["h1"]), r["internal_links"], r["images"], r["json_ld_blocks"]))
        lines.append("  title (%d): %s" % (r["title_length"], r["title"]))
        lines.append("  description (%d): %s" % (r["description_length"], r["description"]))
        lines.append("  canonical: %s" % r["canonical"])
        for f in r["findings"]:
            ev = ("  -> " + f["evidence"]) if f["evidence"] else ""
            lines.append("  [%-8s] %s %s%s" % (f["severity"], f["code"], f["message"], ev))
        if not r["findings"]:
            lines.append("  No findings from automated checks.")
    if cross:
        lines.append("=" * 72)
        lines.append("CROSS-PAGE FINDINGS")
        for f in cross:
            lines.append("  [%-8s] %s %s -> %s" % (f["severity"], f["code"], f["message"], f["evidence"]))
    counts = {s: 0 for s in SEVERITIES}
    for r in results:
        for f in r.get("findings", []):
            counts[f["severity"]] += 1
    for f in cross:
        counts[f["severity"]] += 1
    lines.append("=" * 72)
    lines.append("Pages audited: %d | %s" % (len(results), ", ".join("%s: %d" % (s, counts[s]) for s in SEVERITIES)))
    lines.append("Note: severities are suggestions from heuristics. Confirm with Search Console and manual review.")
    return "\n".join(lines)


def render_markdown(results, cross):
    lines = ["# Metadata audit", ""]
    for r in results:
        lines.append("## %s" % r["page"])
        if "error" in r:
            lines.append("- ERROR: %s" % r["error"])
            continue
        lines.append("- Title (%d): %s" % (r["title_length"], r["title"]))
        lines.append("- Description (%d): %s" % (r["description_length"], r["description"]))
        lines.append("- Canonical: %s" % r["canonical"])
        lines.append("")
        lines.append("| Severity | Code | Finding | Evidence |")
        lines.append("|---|---|---|---|")
        for f in r["findings"]:
            lines.append("| %s | %s | %s | %s |" % (f["severity"], f["code"], f["message"].replace("|", "\\|"), f["evidence"].replace("|", "\\|")))
        lines.append("")
    if cross:
        lines.append("## Cross-page findings")
        for f in cross:
            lines.append("- **%s** %s %s (%s)" % (f["severity"], f["code"], f["message"], f["evidence"]))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only on-page metadata audit for URLs, HTML files, or directories.")
    ap.add_argument("inputs", nargs="+", help="URL(s), HTML file(s), or directory of HTML files")
    ap.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    ap.add_argument("--max-pages", type=int, default=100, help="maximum pages to audit (default 100)")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between remote requests (default 1.0)")
    ap.add_argument("--timeout", type=float, default=15.0, help="request timeout in seconds (default 15)")
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
            ctype = resp["headers"].get("Content-Type", "")
            if ctype and "html" not in ctype.lower() and "xml" not in ctype.lower():
                results.append({"page": label, "error": "Not an HTML response (Content-Type: %s)" % ctype, "findings": []})
                continue
            html = decode_html(resp["body"], resp["headers"])
            res = analyze(label, html, status=resp["status"], headers=resp["headers"], final_url=resp["final_url"])
            if resp.get("truncated"):
                add(res["findings"], "Low", "M006", "Response exceeded %d MB and was truncated for analysis." % (MAX_BYTES // 1048576))
            results.append(res)
        else:
            try:
                with open(ref, "rb") as fh:
                    body = fh.read(MAX_BYTES)
            except OSError as exc:
                results.append({"page": label, "error": str(exc), "findings": []})
                continue
            results.append(analyze(label, decode_html(body)))

    ok = [r for r in results if "error" not in r]
    cross = cross_page(ok) if len(ok) > 1 else []

    if args.format == "json":
        print(json.dumps({"pages": results, "cross_page": cross}, indent=2, ensure_ascii=False))
    elif args.format == "markdown":
        print(render_markdown(results, cross))
    else:
        print(render_text(results, cross))
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
