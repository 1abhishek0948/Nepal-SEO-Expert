#!/usr/bin/env python3
"""
site-files-audit.py - read-only audit for published SEO, AI-access, and trust files.

Audits a site URL or a built/static site directory. It detects files and configuration
evidence; it never creates, overwrites, deploys, or changes configuration. Missing
optional files are reported as conditional recommendations, not errors.

Examples:
  python3 site-files-audit.py https://example.com --format markdown
  python3 site-files-audit.py ./dist --site-type publisher --format json
  python3 site-files-audit.py ./public --site-type ecommerce --has-public-pages yes
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
from html.parser import HTMLParser

UA = "nepal-seo-expert-audit/1.1 (read-only site-file audit)"
MAX_BYTES = 2 * 1024 * 1024
SEVERITIES = ["Critical", "High", "Medium", "Low", "Info"]
SITEMAP_NAMES = ("sitemap.xml", "sitemap-index.xml", "sitemap_index.xml")
CRAWLER_GROUPS = {
    "search": ("Googlebot", "Bingbot"),
    "training": ("Google-Extended", "GPTBot", "ClaudeBot"),
    "user-triggered fetch": ("ChatGPT-User", "Claude-User"),
    "AI/search retrieval": ("OAI-SearchBot", "PerplexityBot", "Claude-SearchBot"),
}
CRAWLER_GROUP_LABELS = {
    "search": "Search",
    "training": "Training",
    "user-triggered fetch": "User-triggered fetch",
    "AI/search retrieval": "AI/search retrieval",
}
VERIFICATION_NAMES = {
    "google-site-verification", "msvalidate.01", "bing-site-verification",
    "p:domain_verify", "facebook-domain-verification", "yandex-verification",
}


def is_url(value):
    return re.match(r"^https?://", value, re.I) is not None


def add(findings, severity, code, message, evidence="", applicability="applicable"):
    findings.append({"severity": severity, "code": code, "message": message,
                     "evidence": evidence, "applicability": applicability})


def fetch(url, timeout):
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/plain,text/html,application/xml,*/*;q=0.5"})
    start = time.monotonic()
    try:
        response = urllib.request.urlopen(request, timeout=timeout)
        status, final, headers = response.status, response.geturl(), response.headers
        body = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        status, final, headers = exc.code, url, exc.headers
        body = exc.read(MAX_BYTES + 1)
    except Exception as exc:
        return {"url": url, "error": str(exc)}
    return {"url": url, "status": status, "final_url": final, "headers": dict(headers),
            "body": body[:MAX_BYTES], "truncated": len(body) > MAX_BYTES,
            "elapsed_ms": round((time.monotonic() - start) * 1000)}


def decode(body):
    return body.decode("utf-8", "replace")


def local_file(root, relative):
    candidate = os.path.join(root, *relative.split("/"))
    if os.path.isfile(candidate):
        try:
            with open(candidate, "rb") as fh:
                return {"path": candidate, "status": 200, "body": fh.read(MAX_BYTES), "local": True}
        except OSError as exc:
            return {"path": candidate, "error": str(exc), "local": True}
    return {"path": candidate, "status": 404, "body": b"", "local": True}


def response_summary(item):
    if item.get("error"):
        return {"state": "unavailable", "detail": item["error"]}
    return {"state": "present" if item.get("status") == 200 else "missing",
            "status": item.get("status"), "path": item.get("path") or item.get("url")}


class HomeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas = []
        self.scripts = []
        self.images = []
        self.headings = []
        self.links = []
        self.text = []
        self._heading = None
        self._script_type = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            self.metas.append({k.lower(): v for k, v in attrs.items()})
        elif tag == "script":
            self._script_type = attrs.get("type", "").lower()
        elif tag == "img":
            self.images.append(attrs)
        elif tag in ("h1", "h2", "h3"):
            self._heading = tag
        elif tag == "a":
            self.links.append(attrs)

    def handle_endtag(self, tag):
        if tag == self._heading:
            self._heading = None
        if tag == "script":
            self._script_type = None

    def handle_data(self, data):
        if self._script_type == "application/ld+json":
            self.scripts.append(data)
        elif self._heading:
            self.headings.append((self._heading, data.strip()))
        else:
            self.text.append(data)


def parse_robots(text):
    groups, current = {}, []
    sitemaps = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = [part.strip() for part in line.split(":", 1)]
        key = key.lower()
        if key == "user-agent":
            agent = value.lower()
            current = [agent]
            groups.setdefault(agent, [])
        elif key in ("allow", "disallow"):
            for agent in current or ["*"]:
                groups.setdefault(agent, []).append((key, value))
        elif key == "sitemap":
            sitemaps.append(value)
    return groups, sitemaps


def crawler_status(groups, agent):
    rules = groups.get(agent.lower(), [])
    wildcard = groups.get("*", [])
    # This intentionally reports presence of blocking rules, not a full robots matcher.
    disallows = [value for key, value in rules + wildcard if key == "disallow" and value]
    if not rules and not wildcard:
        return "no matching rule found"
    if "/" in disallows:
        return "blocked for all paths"
    return "rules present; manual path review needed" if disallows else "explicitly allowed or no disallow rule"


def detect_platform(root):
    signals = []
    known = {
        "vercel.json": "Vercel", "netlify.toml": "Netlify", "_headers": "Netlify/static headers",
        "nginx.conf": "Nginx", ".htaccess": "Apache", "wrangler.toml": "Cloudflare Workers",
        "firebase.json": "Firebase Hosting", "Dockerfile": "container deployment",
    }
    for path, name in known.items():
        if os.path.exists(os.path.join(root, path)):
            signals.append(name)
    return signals


def applicability(site_type, has_public_pages):
    publisher = site_type in ("publisher", "news")
    media = site_type in ("publisher", "news", "portfolio", "tourism")
    return [
        ("robots.txt", "expected", "Public website: publish only intentional crawl rules and an absolute sitemap reference."),
        ("sitemap.xml", "expected" if has_public_pages else "not applicable", "Public canonical HTML URLs need discovery; use the platform's generator."),
        ("sitemap index", "conditional", "Use only when the site has multiple sitemap files or exceeds per-file limits."),
        ("news sitemap", "conditional" if publisher else "not applicable", "Use only for a qualifying, frequently updated news publisher."),
        ("image sitemap", "conditional" if media else "not applicable", "Use when images are important discovery assets and the CMS cannot expose them otherwise."),
        ("video sitemap", "conditional" if media else "not applicable", "Use when video pages are important and eligible video metadata exists."),
        ("llms.txt", "optional", "Community convention only; it is not a ranking, indexing, or citation requirement."),
        ("gemini.txt", "do not create", "Not a recognised standard; do not substitute it for llms.txt or robots.txt."),
        ("ads.txt", "conditional", "Needed when the organisation sells programmatic display advertising, not for ordinary sites."),
        ("security.txt", "conditional", "Useful only when a monitored security contact and disclosure process exist."),
        ("webmaster verification", "conditional", "Verify ownership in each service; never invent or commit verification tokens."),
    ]


def audit(source, site_type="unknown", has_public_pages="auto", timeout=15):
    remote = is_url(source)
    if remote:
        parsed = urllib.parse.urlparse(source if source.endswith("/") else source + "/")
        root_url = "%s://%s" % (parsed.scheme, parsed.netloc)
        get = lambda path: fetch(root_url + path, timeout)
        root_label = root_url
        platform = []
    else:
        root = os.path.abspath(source)
        if not os.path.isdir(root):
            raise ValueError("local source must be a directory")
        get = lambda path: local_file(root, path.lstrip("/"))
        root_label = root
        platform = detect_platform(root)

    home = get("/") if remote else local_file(source, "index.html")
    robots = get("/robots.txt")
    llms = get("/llms.txt")
    gemini = get("/gemini.txt")
    ads = get("/ads.txt")
    security = get("/.well-known/security.txt")
    sitemaps = {name: get("/" + name) for name in SITEMAP_NAMES}
    homepage_html = decode(home.get("body", b"")) if home.get("status") == 200 else ""
    parser = HomeParser()
    if homepage_html:
        parser.feed(homepage_html)
        parser.close()
    if has_public_pages == "auto":
        has_public_pages_bool = bool(homepage_html) or any(v.get("status") == 200 for v in sitemaps.values())
    else:
        has_public_pages_bool = has_public_pages == "yes"

    matrix = [{"item": item, "applicability": app, "reason": reason} for item, app, reason in applicability(site_type, has_public_pages_bool)]
    findings = []
    if has_public_pages_bool and robots.get("status") != 200:
        add(findings, "Medium", "F001", "robots.txt is not available at the site root.", response_summary(robots), "expected")
    elif robots.get("status") == 200:
        robot_text = decode(robots.get("body", b""))
        groups, robot_sitemaps = parse_robots(robot_text)
        if not robot_sitemaps and has_public_pages_bool:
            add(findings, "Low", "F002", "robots.txt has no Sitemap directive; confirm the sitemap is discovered another way.", "robots.txt", "expected")
        if re.search(r"(?im)^\s*noindex\s*:", robot_text):
            add(findings, "High", "F003", "robots.txt contains a non-standard noindex directive; use page-level robots controls for indexing decisions.", "robots.txt", "expected")
    else:
        groups, robot_sitemaps = {}, []

    present_sitemaps = [name for name, value in sitemaps.items() if value.get("status") == 200]
    if has_public_pages_bool and not present_sitemaps and not robot_sitemaps:
        add(findings, "High", "F010", "No conventional sitemap or robots.txt Sitemap directive was found for public pages.", root_label, "expected")
    if len(present_sitemaps) > 1:
        add(findings, "Low", "F011", "Multiple conventional sitemap filenames were found; confirm there is one deliberate discovery path.", ", ".join(present_sitemaps), "conditional")

    if llms.get("status") != 200:
        add(findings, "Info", "F020", "llms.txt is absent. This is optional and should not be created as a claimed SEO or AI-ranking fix.", response_summary(llms), "optional")
    if gemini.get("status") == 200:
        add(findings, "Low", "F021", "gemini.txt exists, but it is not a recognised web standard. Review its purpose; do not rely on it for crawler access or ranking.", response_summary(gemini), "do not create")
    if ads.get("status") == 200:
        text = decode(ads.get("body", b""))
        if not re.search(r"^[^,\s]+,\s*[^,\s]+,\s*[^,\s]+", text, re.M):
            add(findings, "Medium", "F030", "ads.txt is present but does not contain an obvious seller record; validate against authorised advertising sellers.", "ads.txt", "conditional")
    else:
        add(findings, "Info", "F031", "ads.txt is absent. This matters only if the site sells programmatic display advertising.", response_summary(ads), "conditional")
    if security.get("status") == 200:
        text = decode(security.get("body", b""))
        if not re.search(r"(?im)^\s*contact\s*:", text):
            add(findings, "Medium", "F040", "security.txt is present but has no Contact field.", ".well-known/security.txt", "conditional")
    else:
        add(findings, "Info", "F041", "security.txt is absent. Add it only with a monitored security contact and response process.", response_summary(security), "conditional")

    if homepage_html:
        verification = [m for m in parser.metas if m.get("name", "").lower() in VERIFICATION_NAMES]
        if verification:
            add(findings, "Info", "F050", "Webmaster verification meta tag(s) detected. Their tokens are intentionally not printed.", ", ".join(m.get("name") for m in verification), "conditional")
        else:
            add(findings, "Info", "F051", "No homepage webmaster-verification meta tag detected. This does not prove ownership is unverified; DNS and file methods are also valid.", root_label, "conditional")
        if not any(t.lower().startswith("h2") and "?" in h for t, h in parser.headings):
            add(findings, "Low", "F060", "No question-style H2 heading was detected on the sampled homepage. Review priority pages manually for direct answers to real customer questions; this is not a requirement for every page.", "homepage sample", "conditional")
        text = " ".join(parser.text)
        if len(text.split()) < 100:
            add(findings, "Low", "F061", "Very little server-rendered homepage text was found. Confirm the primary answer, entity information, and conversion details are available without client-side execution.", "words=%d" % len(text.split()), "applicable")
        if not parser.scripts:
            add(findings, "Info", "F062", "No JSON-LD block was detected on the homepage sample. Schema is conditional: add only types that accurately describe visible content.", "homepage sample", "conditional")
        missing_dims = [img.get("src", "?") for img in parser.images if not (img.get("width") and img.get("height"))]
        if missing_dims:
            add(findings, "Low", "F070", "%d homepage image(s) lack width and height attributes; confirm dimensions or CSS aspect-ratio to reduce layout shifts." % len(missing_dims), ", ".join(missing_dims[:3]), "applicable")

    if remote and home.get("status") == 200:
        elapsed = home.get("elapsed_ms")
        if elapsed and elapsed > 1500:
            add(findings, "Low", "F071", "Homepage response took %d ms in this single synthetic request. Treat this as a diagnostic only; confirm performance with field data and PageSpeed Insights." % elapsed, home.get("final_url"), "applicable")
        headers = {k.lower(): v for k, v in home.get("headers", {}).items()}
        if not headers.get("cache-control"):
            add(findings, "Info", "F072", "Homepage has no Cache-Control response header. Caching policy needs hosting-specific review; do not change it without deployment approval.", home.get("final_url"), "conditional")
    if platform:
        add(findings, "Info", "F080", "Local hosting/deployment signals detected. Use the existing platform convention for any later approved file generation.", ", ".join(platform), "conditional")

    if robots.get("status") == 200:
        for category, agents in CRAWLER_GROUPS.items():
            statuses = ["%s: %s" % (agent, crawler_status(groups, agent)) for agent in agents]
            add(findings, "Info", "F090", "%s crawler policy observed. Decide deliberately; do not treat training consent, search retrieval, and user-triggered fetching as the same choice." % CRAWLER_GROUP_LABELS[category], "; ".join(statuses), "conditional")

    findings.sort(key=lambda item: SEVERITIES.index(item["severity"]))
    return {
        "source": root_label, "mode": "remote" if remote else "local", "site_type": site_type,
        "has_public_pages": has_public_pages_bool, "file_status": {
            "robots.txt": response_summary(robots), "sitemaps": {k: response_summary(v) for k, v in sitemaps.items()},
            "llms.txt": response_summary(llms), "gemini.txt": response_summary(gemini),
            "ads.txt": response_summary(ads), "security.txt": response_summary(security),
        }, "applicability_matrix": matrix, "findings": findings,
        "limitations": [
            "Does not verify Search Console, Bing Webmaster Tools, DNS ownership, WAF/CDN behaviour, real crawler identity, or field Core Web Vitals.",
            "Robots matching is summarised by agent group; validate exact paths with the crawler vendor's current documentation.",
            "Absence of optional files is not an error and is never a direction to create them automatically.",
        ],
    }


def render_text(result, markdown=False):
    lines = (["# Site file, crawler access, and readiness audit", ""] if markdown else [])
    lines.append(("**Source:** " if markdown else "Source: ") + result["source"])
    lines.append(("**Mode:** " if markdown else "Mode: ") + result["mode"])
    lines.append("")
    lines.append("## Applicability matrix" if markdown else "Applicability matrix")
    if markdown:
        lines.extend(["| Item | Applicability | Reason |", "|---|---|---|"])
        lines.extend("| %s | %s | %s |" % (m["item"], m["applicability"], m["reason"]) for m in result["applicability_matrix"])
    else:
        lines.extend("- %s: %s — %s" % (m["item"], m["applicability"], m["reason"]) for m in result["applicability_matrix"])
    lines.append("")
    lines.append("## Findings" if markdown else "Findings")
    for finding in result["findings"]:
        prefix = "- **[%s] %s**" % (finding["severity"], finding["code"]) if markdown else "[%s] %s" % (finding["severity"], finding["code"])
        lines.append("%s %s" % (prefix, finding["message"]))
        if finding["evidence"]:
            lines.append("  Evidence: %s" % finding["evidence"])
    if not result["findings"]:
        lines.append("No automated findings.")
    lines.append("")
    lines.append("## Limits" if markdown else "Limits")
    lines.extend("- " + item for item in result["limitations"])
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only audit of SEO, AI-access, and trust files for a site URL or built site directory.")
    ap.add_argument("source", help="site root URL or built/static site directory")
    ap.add_argument("--site-type", choices=["unknown", "business", "ecommerce", "saas", "publisher", "news", "portfolio", "tourism"], default="unknown")
    ap.add_argument("--has-public-pages", choices=["auto", "yes", "no"], default="auto")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    args = ap.parse_args(argv)
    try:
        result = audit(args.source, args.site_type, args.has_public_pages, args.timeout)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_text(result, args.format == "markdown"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
