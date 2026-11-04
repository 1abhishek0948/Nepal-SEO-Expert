# Changelog

## 1.2.0 — 2026-11-04

- Added a safe one-command installer for Claude Code, OpenCode, Codex, and Agent Skills-compatible project folders. It copies the complete skill, excludes `.git`, and refuses to overwrite an existing installation.
- Added repository-owned package validation, installer tests, and a GitHub Actions workflow that runs on every push and pull request.
- Added clearly labelled fictional local-business and ecommerce audit examples, so users can see the evidence-based reporting standard without mistaking sample data for real results.
- Simplified README installation and usage instructions for Claude Code, OpenCode, Codex, and compatible tools.

## 1.1.0 — 2026-11-04

- Added a conditional SEO/AEO/GEO file applicability matrix: robots, sitemap variants, `llms.txt`, `ads.txt`, `security.txt`, webmaster verification, and the explicit non-standard status of `gemini.txt`.
- Added `site-files-audit.py`, a standard-library, read-only checker for root-file discovery, crawler-purpose reporting, limited hosting evidence, and light page-performance/AEO signals.
- Added safe-generation guidance: use platform-native mechanisms only after explicit approval; never overwrite a file, invent verification tokens, or change hosting, CDN, WAF, DNS, redirects, cache, or deployment configuration.
- Updated GEO guidance to distinguish search, training, AI/search retrieval, and user-triggered fetchers.
- Expanded the audit report template, README, fixtures, and automated tests.

## 1.0.0

- Initial public release.
