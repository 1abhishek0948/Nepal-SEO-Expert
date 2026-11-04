import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.sh"


class InstallerTests(unittest.TestCase):
    def test_project_install_copies_the_complete_skill_without_git(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                ["sh", str(INSTALLER), "codex", "project"],
                cwd=directory,
                text=True,
                capture_output=True,
                check=False,
            )
            installed = Path(directory) / ".codex" / "skills" / "nepal-seo-expert"
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "scripts" / "site-files-audit.py").is_file())
            self.assertTrue((installed / "references" / "geo.md").is_file())
            self.assertFalse((installed / ".git").exists())

            repeat = subprocess.run(
                ["sh", str(INSTALLER), "codex", "project"],
                cwd=directory,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, repeat.returncode)
            self.assertIn("already exists", repeat.stderr)

    def test_rejects_unknown_install_target(self):
        result = subprocess.run(
            ["sh", str(INSTALLER), "unknown", "project"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("Usage:", result.stderr)


if __name__ == "__main__":
    unittest.main()
