#!/usr/bin/env python3
"""Small, dependency-free release check for this skill package."""

import re
import sys
from pathlib import Path


REQUIRED = (
    "SKILL.md",
    "README.md",
    "VERSION",
    "CHANGELOG.md",
    "install.sh",
    "references/aeo.md",
    "references/audit-report-template.md",
    "references/content-seo.md",
    "references/ecommerce-seo.md",
    "references/geo.md",
    "references/local-seo-nepal.md",
    "references/on-page-seo.md",
    "references/saas-seo.md",
    "references/site-files-and-crawler-access.md",
    "references/technical-seo.md",
    "scripts/metadata-audit.py",
    "scripts/schema-audit.py",
    "scripts/site-files-audit.py",
    "scripts/sitemap-audit.py",
    "scripts/validate-skill.py",
)


def main(argv=None):
    argv = argv or sys.argv[1:]
    root = Path(argv[0] if argv else ".").resolve()
    errors = []
    for relative in REQUIRED:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append("missing or empty required file: %s" % relative)

    skill = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").is_file() else ""
    if not skill.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    if not re.search(r"(?m)^name:\s*nepal-seo-expert\s*$", skill):
        errors.append("SKILL.md must declare name: nepal-seo-expert")
    if not re.search(r"(?m)^description:\s*\S+", skill):
        errors.append("SKILL.md must declare a non-empty description")

    version = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").is_file() else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("VERSION must be semantic version text such as 1.2.0")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").is_file() else ""
    if version and ("## " + version) not in changelog:
        errors.append("CHANGELOG.md needs a section for version %s" % version)

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    for marker in (".claude/skills", ".opencode/skills", ".codex/skills", ".agents/skills", "install.sh"):
        if marker not in readme:
            errors.append("README.md is missing installation guidance for %s" % marker)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print("- " + error, file=sys.stderr)
        return 1
    print("Skill package is valid: nepal-seo-expert %s" % version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
