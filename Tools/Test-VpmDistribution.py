import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "kqnade/SPS-Setup-Assistant"
LISTING_ID = "com.kqnade.sps2-listing"
LISTING_URL = "https://kqnade.github.io/SPS-Setup-Assistant/index.json"
PACKAGE_ID = "com.lumakroma.sps2-setup-assistant"
VERSION = "1.1.2-kqnade.1"


def text(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for key, value in attrs if key == "href")


class VpmDistributionTests(unittest.TestCase):
    def test_listing_has_a_distinct_fork_identity(self):
        source = json.loads(text("source.json"))
        self.assertEqual(source["id"], LISTING_ID)
        self.assertEqual(source["url"], LISTING_URL)
        self.assertEqual(source["infoLink"]["url"], f"https://github.com/{REPOSITORY}")
        self.assertEqual(source["author"]["name"], "kqnade")

    def test_package_preserves_identity_and_attribution_with_a_new_prerelease(self):
        manifest = json.loads(text(f"Packages/{PACKAGE_ID}/package.json"))
        self.assertEqual(manifest["name"], PACKAGE_ID)
        self.assertEqual(manifest["version"], VERSION)
        self.assertEqual(manifest["author"]["name"], "LumaKroma")
        self.assertEqual(manifest["license"], "MIT")

    def test_release_tools_resolve_only_fork_assets(self):
        for path in (
            "Tools/Build-VpmPackage.ps1",
            "Tools/Build-VpmListing.ps1",
            "Tools/Test-VpmListing.ps1",
        ):
            with self.subTest(path=path):
                script = text(path)
                self.assertIn(
                    f"https://github.com/{REPOSITORY}/releases/download/", script
                )
                self.assertNotIn(
                    "https://github.com/LumaKroma/SPS2-Setup-Assistant/releases/",
                    script,
                )
        script = text("Tools/Prepare-VpmListing.ps1")
        self.assertIn(f"https://api.github.com/repos/{REPOSITORY}/releases?", script)
        self.assertNotIn(
            "https://api.github.com/repos/LumaKroma/SPS2-Setup-Assistant/releases",
            script,
        )

    def test_listing_validators_require_the_fork_identity(self):
        for path in ("Tools/Build-VpmListing.ps1", "Tools/Test-VpmListing.ps1"):
            with self.subTest(path=path):
                self.assertIn(f"-ne '{LISTING_ID}'", text(path))

    def test_package_validator_requires_the_release_version(self):
        self.assertIn(
            f"$manifest.version -eq '{VERSION}'", text("Tools/Validate-Package.ps1")
        )

    def test_readmes_register_the_fork_and_explain_prerelease_status(self):
        for path in ("README.md", f"Packages/{PACKAGE_ID}/README.md"):
            with self.subTest(path=path):
                readme = text(path)
                self.assertIn(LISTING_URL, readme)
                self.assertIn(VERSION, readme)
                self.assertIn("未検証", readme)
                self.assertNotIn(
                    "https://lumakroma.github.io/SPS2-Setup-Assistant/", readme
                )

    def test_website_registers_the_fork_without_upstream_installers(self):
        html = text("Website/index.html")
        links = Links()
        links.feed(html)
        registration_urls = [
            parse_qs(urlsplit(href).query).get("url", [None])[0]
            for href in links.hrefs
            if href.startswith("vcc://vpm/addRepo?")
        ]
        self.assertIn(LISTING_URL, registration_urls)
        self.assertIn(VERSION, html)
        self.assertIn("未検証", html)
        self.assertFalse(
            any(
                "github.com/LumaKroma/SPS2-Setup-Assistant/releases/download/" in href
                for href in links.hrefs
            )
        )

    def test_ci_runs_distribution_checks_and_marks_prereleases(self):
        self.assertIn(
            "python ./Tools/Test-VpmDistribution.py",
            text(".github/workflows/validate.yml"),
        )
        self.assertIn(
            "prerelease: version.includes('-')", text(".github/workflows/release.yml")
        )


if __name__ == "__main__":
    unittest.main()
