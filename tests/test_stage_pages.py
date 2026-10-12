import tempfile
import unittest
from pathlib import Path

from build import EXPS
from stage_pages import stage_site


class StageSiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.build = self.root / "build"
        self.build.mkdir()

        for version in ("A", "B"):
            version_dir = self.build / version
            version_dir.mkdir()
            names = ["index.html", "all-in-one.html"]
            names.extend(experiment["file"] + ".html" for experiment in EXPS)
            for name in names:
                (version_dir / name).write_text(
                    '<!doctype html><a href="all-in-one.html">合并版</a>',
                    encoding="utf-8",
                )

        (self.build / "index.html").write_text(
            '<a href="版本A-清透玻璃版/index.html">A</a>'
            '<a href="版本B-模拟器版/index.html">B</a>',
            encoding="utf-8",
        )
        self.site = self.root / "_site"

    def test_stages_both_versions_and_checks_local_links(self):
        stage_site(self.build, self.site)

        self.assertTrue((self.site / "index.html").is_file())
        for folder in ("版本A-清透玻璃版", "版本B-模拟器版"):
            self.assertTrue((self.site / folder / "index.html").is_file())
            self.assertTrue((self.site / folder / "all-in-one.html").is_file())
            for experiment in EXPS:
                self.assertTrue(
                    (self.site / folder / (experiment["file"] + ".html")).is_file()
                )

    def test_missing_generated_page_fails(self):
        (self.build / "B" / (EXPS[0]["file"] + ".html")).unlink()

        with self.assertRaisesRegex(FileNotFoundError, "Missing generated files"):
            stage_site(self.build, self.site)

    def test_broken_local_link_fails(self):
        (self.build / "index.html").write_text(
            '<a href="missing.html">missing</a>',
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Broken local link"):
            stage_site(self.build, self.site)


if __name__ == "__main__":
    unittest.main()
