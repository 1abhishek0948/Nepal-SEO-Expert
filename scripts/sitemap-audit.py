#!/usr/bin/env python3
"""
sitemap-audit.py - read-only XML sitemap audit.

Checks sitemap structure and limits, URL hygiene, duplicates, host/protocol
consistency, lastmod validity, hreflang annotations, and (optionally) the HTTP
status of a sample of listed URLs.

INPUT
  A sitemap URL (http/https), a local sitemap file (.xml or .xml.gz), or a
  sitemap index. Child sitemaps of an index are fetched if they are http(s)
  URLs (up to --max-sitemaps).

DEPENDENCIES
  Python 3.8+ standard library only. No paid APIs.

SAFETY
  * Read-only. Never writes files. Output goes to stdout.
  * Remote requests are GET (sitemaps) and HEAD (optional status sampling) with
    an identifying User-Agent and a delay between requests (default 1 second).
  * Status sampling is OFF by default. Enable with --check-status N (N is the
    number of URLs to sample; hard-capped at 200). Audit sites you own or have
    permission to audit.
  * Files containing XML entity declarations (<!ENTITY) are refused to avoid
    entity-expansion attacks.

EXAMPLES
  python3 sitemap-audit.py https://example.com/sitemap.xml
  python3 sitemap-audit.py ./public/sitemap.xml --check-status 20
  python3 sitemap-audit.py https://example.com/sitemap_index.xml --format json

Results are heuristics. Confirm in Google Search Console (Sitemaps and Pages
reports), which is the authority on what Google processed and indexed.
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
import xml.etree.ElementTree as ET
from collections import Counter

UA = "nepal-seo-expert-audit/1.0 (read-only SEO audit script)"
MAX_FETCH_BYTES = 60 * 1024 * 1024      # slightly above the 50 MB sitemap limit so oversize is detectable
SITEMAP_URL_LIMIT = 50000
SITEMAP_SIZE_LIMIT = 50 * 1024 * 1024
STATUS_SAMPLE_CAP = 200
SEVERITIES = ["Critical", "High", "Medium", "Low", "Info"]
LASTMOD_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2}))?)?)?$")
NS_SITEMAP = "http://www.sitemaps.org/schemas/sitemap/0.9"
NS_XHTML = "http://www.w3.org/1999/xhtml"


def is_url(value):
    return re.match(r"^https?://", value, re.I) is not None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url, timeout=20, method="GET", follow=True, limit=MAX_FETCH_BYTES):
    req = urllib.request.Request(
        url, method=method,
        headers={"User-Agent": UA, "Accept": "application/xml,text/xml,*/*;q=0.5", "Accept-Encoding": "gzip"})
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    try:
        resp = opener.open(req, timeout=timeout)
        status, headers = resp.status, resp.headers
        body = resp.read(limit + 1) if method == "GET" else b""
    except urllib.error.HTTPError as exc:
        status, headers = exc.code, exc.headers
        body = b""
        if method == "GET":
            try:
                body = exc.read(limit + 1)
            except Exception:
                pass
    except Exception as exc:
        return {"url": url, "error": str(exc)}
    if method == "GET" and headers.get("Content-Encoding", "").lower() == "gzip":
        try:
            body = gzip.decompress(body)
        except Exception:
            pass
    return {"url": url, "status": status, "headers": headers, "body": body}


def load_sitemap_bytes(source, timeout):
    """Return (bytes, error, http_status). Handles .gz by magic bytes."""
    if is_url(source):
        resp = fetch(source, timeout=timeout)
        if "error" in resp:
            return None, resp["error"], None
        data, status = resp["body"], resp["status"]
        if status != 200:
            return None, "HTTP %s" % status, status
    else:
        try:
            with open(source, "rb") as fh:
                data = fh.read(MAX_FETCH_BYTES + 1)
        except OSError as exc:
            return None, str(exc), None
        status = None
    if data[:2] == b"\x1f\x8b":
        try:
            data = gzip.decompress(data)
        except Exception as exc:
            return None, "gzip decode failed: %s" % exc, status
    return data, None, status


def add(findings, severity, code, message, examples=None):
    findings.append({"severity": severity, "code": code, "message": message, "examples": (examples or [])[:5]})


def local(tag):
    return tag.split("}", 1)[1] if "}" in tag else tag


def parse_sitemap(data, label, findings):
    """Return ('urlset'|'sitemapindex'|None, entries). entries: list of dicts."""
    if b"<!ENTITY" in data[:100000] or b"<!entity" in data[:100000]:
        add(findings, "High", "SM001", "[%s] XML contains entity declarations; refusing to parse." % label)
        return None, []
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        add(findings, "Critical", "SM002", "[%s] XML is not well-formed: %s" % (label, exc))
        return None, []

    kind = local(root.tag)
    ns = root.tag.split("}", 1)[0][1:] if "}" in root.tag else ""
    if kind not in ("urlset", "sitemapindex"):
        add(findings, "Critical", "SM003", "[%s] Root element is <%s>; expected <urlset> or <sitemapindex>." % (label, kind))
        return None, []
    if ns != NS_SITEMAP:
        add(findings, "High", "SM004", "[%s] Missing or incorrect sitemap namespace (expected %s)." % (label, NS_SITEMAP), [ns or "none"])

    entries = []
    for child in root:
        if local(child.tag) not in ("url", "sitemap"):
            continue
        entry = {"loc": None, "lastmod": None, "priority": None, "changefreq": None, "alternates": []}
        for sub in child:
            name = local(sub.tag)
            text = (sub.text or "").strip()
            if name == "loc":
                entry["loc"] = text
            elif name == "lastmod":
                entry["lastmod"] = text
            elif name == "priority":
                entry["priority"] = text
            elif name == "changefreq":
                entry["changefreq"] = text
            elif name == "link" and sub.get("rel") == "alternate":
                entry["alternates"].append((sub.get("hreflang", ""), sub.get("href", "")))
        entries.append(entry)
    return kind, entries


def analyze_urls(entries, findings, label):
    locs = [e["loc"] for e in entries]
    missing = [i for i, v in enumerate(locs) if not v]
    if missing:
        add(findings, "High", "SM101", "[%s] %d entr(ies) have no <loc>." % (label, len(missing)))
    valid = [v for v in locs if v]

    if len(entries) > SITEMAP_URL_LIMIT:
        add(findings, "High", "SM102", "[%s] %d URLs exceeds the 50,000 URL limit per sitemap file; split it or use a sitemap index." % (label, len(entries)))
    if not entries:
        add(findings, "Medium", "SM103", "[%s] Sitemap contains no entries." % label)

    relative = [v for v in valid if not is_url(v)]
    if relative:
        add(findings, "High", "SM111", "[%s] %d <loc> value(s) are not absolute http(s) URLs." % (label, len(relative)), relative)
    too_long = [v for v in valid if len(v) > 2048]
    if too_long:
        add(findings, "Medium", "SM112", "[%s] %d URL(s) exceed 2,048 characters." % (label, len(too_long)), [v[:80] for v in too_long])
    spaces = [v for v in valid if re.search(r"\s", v)]
    if spaces:
        add(findings, "High", "SM113", "[%s] %d URL(s) contain whitespace (must be URL-encoded)." % (label, len(spaces)), spaces)
    fragments = [v for v in valid if "#" in v]
    if fragments:
        add(findings, "Medium", "SM114", "[%s] %d URL(s) contain a #fragment (fragments are not separate pages)." % (label, len(fragments)), fragments)

    dup = [u for u, c in Counter(valid).items() if c > 1]
    if dup:
        add(findings, "Medium", "SM121", "[%s] %d duplicate URL(s) listed." % (label, len(dup)), dup)

    hosts = Counter(urllib.parse.urlparse(v).netloc.lower() for v in valid if is_url(v))
    if len(hosts) > 1:
        add(findings, "High", "SM131", "[%s] URLs span multiple hosts (a sitemap should list URLs for one site/host): %s" % (
            label, ", ".join("%s (%d)" % (h, c) for h, c in hosts.most_common(5))))
    schemes = Counter(urllib.parse.urlparse(v).scheme.lower() for v in valid if is_url(v))
    if len(schemes) > 1:
        add(findings, "High", "SM132", "[%s] Mixed http and https URLs." % label)
    elif "http" in schemes:
        add(findings, "Medium", "SM133", "[%s] All URLs use http. Confirm the site should not be https." % label)

    params = [v for v in valid if "?" in v]
    if params:
        add(findings, "Medium", "SM141", "[%s] %d URL(s) contain query parameters. Sitemaps should list canonical URLs; confirm these are the canonical versions." % (label, len(params)), params)

    upper = [v for v in valid if is_url(v) and urllib.parse.urlparse(v).path != urllib.parse.urlparse(v).path.lower()]
    if upper and len(upper) < len(valid):
        add(findings, "Info", "SM142", "[%s] %d URL path(s) contain uppercase characters. Make sure only one case variant is canonical." % (label, len(upper)), upper)

    paths = [urllib.parse.urlparse(v).path for v in valid if is_url(v)]
    with_slash = sum(1 for p in paths if p.endswith("/") and p != "/")
    without = sum(1 for p in paths if not p.endswith("/") and "." not in p.rsplit("/", 1)[-1])
    if with_slash and without:
        add(findings, "Low", "SM143", "[%s] Mixed trailing-slash conventions (%d with, %d without). Pick one and redirect the other." % (label, with_slash, without))

    # lastmod
    lastmods = [e["lastmod"] for e in entries if e["lastmod"]]
    no_lastmod = len(entries) - len(lastmods)
    if entries and no_lastmod == len(entries):
        add(findings, "Info", "SM151", "[%s] No <lastmod> values. Optional, but accurate lastmod helps crawl scheduling." % label)
    elif no_lastmod:
        add(findings, "Low", "SM152", "[%s] %d entr(ies) have no <lastmod>." % (label, no_lastmod))
    bad = [v for v in lastmods if not LASTMOD_RE.match(v)]
    if bad:
        add(findings, "Medium", "SM153", "[%s] %d <lastmod> value(s) are not W3C datetime format (e.g. 2026-11-04 or 2026-11-04T10:00:00+05:45)." % (label, len(bad)), bad)
    if len(lastmods) > 20 and len(set(lastmods)) == 1:
        add(findings, "Medium", "SM154", "[%s] Every <lastmod> has the same value (%s). Google ignores lastmod if it is not consistently accurate; set it to real content-change dates." % (label, lastmods[0]))
    today = time.strftime("%Y-%m-%d", time.gmtime())
    future = [v for v in lastmods if LASTMOD_RE.match(v) and v[:10] > today]
    if future:
        add(findings, "Medium", "SM155", "[%s] %d <lastmod> value(s) are in the future." % (label, len(future)), future)

    if any(e["priority"] or e["changefreq"] for e in entries):
        add(findings, "Info", "SM161", "[%s] <priority>/<changefreq> present. Google ignores these; they are harmless but unnecessary." % label)

    # hreflang alternates in sitemap
    alt_entries = [e for e in entries if e["alternates"]]
    if alt_entries:
        invalid = 0
        non_reciprocal = 0
        by_loc = {e["loc"]: {h for _, h in e["alternates"]} for e in alt_entries if e["loc"]}
        for e in alt_entries:
            if e["loc"] and e["loc"] not in {h for _, h in e["alternates"]}:
                invalid += 1
            for _, href in e["alternates"]:
                other = by_loc.get(href)
                if other is not None and e["loc"] not in other:
                    non_reciprocal += 1
        if invalid:
            add(findings, "Medium", "SM171", "[%s] %d entr(ies) have hreflang alternates that omit a self-referencing link." % (label, invalid))
        if non_reciprocal:
            add(findings, "Medium", "SM172", "[%s] %d hreflang link(s) are not reciprocated by the target entry." % (label, non_reciprocal))


def sample_urls(urls, n):
    if n >= len(urls):
        return list(urls)
    step = len(urls) / float(n)
    return [urls[int(i * step)] for i in range(n)]


def check_status(urls, n, delay, timeout, findings):
    n = max(0, min(n, STATUS_SAMPLE_CAP))
    sample = sample_urls(urls, n)
    results = {"checked": 0, "ok": 0, "redirect": [], "client_error": [], "server_error": [], "noindex": [], "failed": []}
    for i, url in enumerate(sample):
        if i:
            time.sleep(max(delay, 0))
        resp = fetch(url, timeout=timeout, method="HEAD", follow=False)
        if "error" not in resp and resp["status"] == 405:
            resp = fetch(url, timeout=timeout, method="GET", follow=False, limit=65536)
        results["checked"] += 1
        if "error" in resp:
            results["failed"].append("%s (%s)" % (url, resp["error"][:60]))
            continue
        st = resp["status"]
        if st == 200:
            results["ok"] += 1
            if "noindex" in resp["headers"].get("X-Robots-Tag", "").lower():
                results["noindex"].append(url)
        elif 300 <= st < 400:
            results["redirect"].append("%s -> %s (%s)" % (url, resp["headers"].get("Location", "?"), st))
        elif 400 <= st < 500:
            results["client_error"].append("%s (%s)" % (url, st))
        else:
            results["server_error"].append("%s (%s)" % (url, st))
    if results["redirect"]:
        add(findings, "High", "SM201", "%d of %d sampled URL(s) redirect. Sitemaps should list final canonical URLs." % (len(results["redirect"]), results["checked"]), results["redirect"])
    if results["client_error"]:
        add(findings, "High", "SM202", "%d of %d sampled URL(s) return 4xx." % (len(results["client_error"]), results["checked"]), results["client_error"])
    if results["server_error"]:
        add(findings, "High", "SM203", "%d of %d sampled URL(s) return 5xx." % (len(results["server_error"]), results["checked"]), results["server_error"])
    if results["noindex"]:
        add(findings, "Critical", "SM204", "%d sampled URL(s) send an X-Robots-Tag noindex header but are listed in the sitemap." % len(results["noindex"]), results["noindex"])
    if results["failed"]:
        add(findings, "Medium", "SM205", "%d sampled URL(s) could not be requested." % len(results["failed"]), results["failed"])
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only XML sitemap audit (URL or local file).")
    ap.add_argument("source", help="sitemap URL or local file path (.xml or .xml.gz)")
    ap.add_argument("--check-status", type=int, default=0, metavar="N",
                    help="optionally sample N listed URLs with HEAD requests (default 0 = off; max %d)" % STATUS_SAMPLE_CAP)
    ap.add_argument("--max-sitemaps", type=int, default=10, help="max child sitemaps to fetch from an index (default 10)")
    ap.add_argument("--no-follow", action="store_true", help="do not fetch child sitemaps of an index")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between remote requests (default 1.0)")
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    findings = []
    data, err, _ = load_sitemap_bytes(args.source, args.timeout)
    if err:
        print("error: could not load %s: %s" % (args.source, err), file=sys.stderr)
        return 2

    if len(data) > SITEMAP_SIZE_LIMIT:
        add(findings, "High", "SM005", "Sitemap is larger than 50 MB uncompressed; split it.")

    kind, entries = parse_sitemap(data, args.source, findings)
    all_urls = []
    children = []
    summary = {"source": args.source, "type": kind, "entries": len(entries)}

    if kind == "urlset":
        analyze_urls(entries, findings, os.path.basename(args.source) or args.source)
        all_urls = [e["loc"] for e in entries if e["loc"] and is_url(e["loc"])]
    elif kind == "sitemapindex":
        child_locs = [e["loc"] for e in entries if e["loc"]]
        children = child_locs
        if len(child_locs) > 50000:
            add(findings, "High", "SM301", "Sitemap index lists more than 50,000 sitemaps.")
        dup = [u for u, c in Counter(child_locs).items() if c > 1]
        if dup:
            add(findings, "Medium", "SM302", "Duplicate child sitemap entries.", dup)
        nested = 0
        fetched = 0
        if not args.no_follow:
            for loc in child_locs[:args.max_sitemaps]:
                if not is_url(loc):
                    add(findings, "High", "SM303", "Child sitemap is not an absolute URL.", [loc])
                    continue
                if fetched:
                    time.sleep(max(args.delay, 0))
                fetched += 1
                cdata, cerr, _ = load_sitemap_bytes(loc, args.timeout)
                if cerr:
                    add(findings, "High", "SM304", "Child sitemap could not be loaded: %s" % cerr, [loc])
                    continue
                if len(cdata) > SITEMAP_SIZE_LIMIT:
                    add(findings, "High", "SM005", "[%s] larger than 50 MB uncompressed." % loc)
                ckind, centries = parse_sitemap(cdata, loc, findings)
                if ckind == "urlset":
                    analyze_urls(centries, findings, loc)
                    all_urls.extend(e["loc"] for e in centries if e["loc"] and is_url(e["loc"]))
                elif ckind == "sitemapindex":
                    nested += 1
            if nested:
                add(findings, "High", "SM305", "%d child sitemap(s) are themselves sitemap indexes (nesting is not allowed)." % nested)
            if len(child_locs) > args.max_sitemaps:
                add(findings, "Info", "SM306", "Only the first %d of %d child sitemaps were fetched (use --max-sitemaps)." % (args.max_sitemaps, len(child_locs)))
        summary["child_sitemaps"] = len(child_locs)

    summary["urls_analyzed"] = len(all_urls)
    if all_urls:
        dup_all = [u for u, c in Counter(all_urls).items() if c > 1]
        if dup_all and kind == "sitemapindex":
            add(findings, "Medium", "SM122", "%d URL(s) appear in more than one child sitemap." % len(dup_all), dup_all)

    status_summary = None
    if args.check_status and all_urls:
        status_summary = check_status(all_urls, args.check_status, args.delay, args.timeout, findings)
        summary["status_sample"] = {k: (len(v) if isinstance(v, list) else v) for k, v in status_summary.items()}

    findings.sort(key=lambda f: SEVERITIES.index(f["severity"]))

    if args.format == "json":
        print(json.dumps({"summary": summary, "findings": findings}, indent=2, ensure_ascii=False))
        return 0

    print("Sitemap audit: %s" % args.source)
    print("  type: %s | entries: %s | URLs analyzed: %s" % (kind, len(entries), len(all_urls)))
    if status_summary:
        print("  status sample: checked %d, OK %d" % (status_summary["checked"], status_summary["ok"]))
    elif args.check_status == 0:
        print("  status sampling: off (use --check-status N to enable)")
    print("-" * 72)
    counts = Counter(f["severity"] for f in findings)
    for f in findings:
        print("[%-8s] %s %s" % (f["severity"], f["code"], f["message"]))
        for ex in f["examples"]:
            print("             - %s" % ex)
    if not findings:
        print("No findings from automated checks.")
    print("-" * 72)
    print(", ".join("%s: %d" % (s, counts.get(s, 0)) for s in SEVERITIES))
    print("Note: heuristic checks. Confirm in Search Console (Sitemaps and Pages reports).")
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
