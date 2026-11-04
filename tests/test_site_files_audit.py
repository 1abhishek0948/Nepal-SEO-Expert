import importlib.util
import io
import json
import os
import unittest
from contextlib import redirect_stdout


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "site-files-audit.py")
FIXTURE = os.path.join(ROOT, "tests", "site-files")

spec = importlib.util.spec_from_file_location("site_files_audit", SCRIPT)
site_files_audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site_files_audit)


class SiteFilesAuditTests(unittest.TestCase):
    def test_local_fixture_detects_files_and_hides_token(self):
        result = site_files_audit.audit(FIXTURE, site_type="business")
        self.assertTrue(result["has_public_pages"])
        self.assertEqual("present", result["file_status"]["robots.txt"]["state"])
        self.assertEqual("present", result["file_status"]["sitemaps"]["sitemap.xml"]["state"])
        self.assertEqual("present", result["file_status"]["llms.txt"]["state"])
        output = site_files_audit.render_text(result)
        self.assertIn("Webmaster verification meta tag(s) detected", output)
        self.assertNotIn("test-token-must-not-be-printed", output)

    def test_matrix_keeps_gemini_non_standard_and_ads_conditional(self):
        result = site_files_audit.audit(FIXTURE, site_type="business")
        matrix = {row["item"]: row["applicability"] for row in result["applicability_matrix"]}
        self.assertEqual("do not create", matrix["gemini.txt"])
        self.assertEqual("conditional", matrix["ads.txt"])
        self.assertTrue(any(item["code"] == "F090" for item in result["findings"]))

    def test_json_cli_output_parses(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = site_files_audit.main([FIXTURE, "--format", "json"])
        self.assertEqual(0, code)
        payload = json.loads(stream.getvalue())
        self.assertEqual("local", payload["mode"])


if __name__ == "__main__":
    unittest.main()
