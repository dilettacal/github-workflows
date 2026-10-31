import tempfile
import unittest
from pathlib import Path

from scripts.release import rollover_changelog, validate_changelog, validate_project_version, version


class ReleaseContractTests(unittest.TestCase):
    def test_versions_are_stable_semver(self):
        self.assertEqual(version("1.2.3"), (1, 2, 3))
        for value in ("v1.2.3", "1.2", "1.2.3-rc.1", "01.2.3"):
            with self.assertRaises(ValueError): version(value)

    def test_semantic_and_legacy_history_are_preserved_formats(self):
        for fixture in ("semantic-version.md", "date-only.md"):
            validate_changelog((Path("tests/fixtures") / fixture).read_text(), "0.6.0")

    def test_rollover_preserves_unreleased_content_and_history(self):
        for fixture in ("semantic-version.md", "date-only.md"):
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "CHANGELOG.md"
                original = (Path("tests/fixtures") / fixture).read_text()
                path.write_text(original)
                rollover_changelog(path, "0.6.0", "2026-10-31")
                updated = path.read_text()
                self.assertIn("## [Unreleased]\n\n## [0.6.0] - 2026-10-31", updated)
                self.assertIn("## [0.5.0] - 2026-10-28" if fixture.startswith("semantic") else "## [2026-10-27]", updated)
                if fixture.startswith("semantic"):
                    self.assertIn('print("puzzle")', updated)
                    self.assertIn("[0.5.0]: https://example.test", updated)

    def test_rejects_missing_duplicate_empty_and_duplicate_version(self):
        cases = ("missing-unreleased.md", "duplicate-unreleased.md", "empty-unreleased.md", "duplicate-version.md")
        for fixture in cases:
            with self.subTest(fixture=fixture), self.assertRaises(ValueError):
                validate_changelog((Path("tests/fixtures") / fixture).read_text(), "0.6.0")

    def test_requires_an_increasing_literal_pyproject_version(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pyproject.toml"
            path.write_text('[project]\nversion = "0.5.0"\n')
            validate_project_version(path, "0.6.0")
            with self.assertRaises(ValueError): validate_project_version(path, "0.5.0")

    def test_workflow_repository_can_use_a_version_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "VERSION"
            path.write_text("0.0.0\n")
            validate_project_version(path, "0.1.0")
