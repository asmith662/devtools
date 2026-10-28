import unittest

from releasevault import Artifact as A
from releasevault import Catalog
from releasevault.cli import selection_summary
from releasevault.manifest import decode_manifest, encode_manifest


def row(version, uri=None, **kwargs):
    return A(
        kwargs.get("project", "paint"),
        kwargs.get("platform", "linux"),
        version,
        uri or version,
        kwargs.get("enabled", True),
    )


class CatalogTests(unittest.TestCase):
    def test_stable_outranks_preview(self):
        stable, preview = row("2.0.0"), row("2.0.0-rc.9")
        self.assertIs(
            Catalog([preview, stable]).choose("paint", "linux", include_previews=True),
            stable,
        )

    def test_numeric_preview_precedence(self):
        earlier, later = row("2.0.0-rc.2"), row("2.0.0-rc.10")
        self.assertIs(
            Catalog([earlier, later]).choose("paint", "linux", include_previews=True),
            later,
        )

    def test_build_metadata_tie_preserves_first(self):
        first, second = row("1.5.0+aaa"), row("1.5.0+zzz")
        original = [first, second]
        self.assertIs(Catalog(original).choose("paint", "linux"), first)
        self.assertEqual(original, [first, second])

    def test_existing_eligibility(self):
        good = row("1.2.0")
        rows = [
            row("9.0.0", enabled=False),
            row("8.0.0", project="other"),
            row("7.0.0", platform="mac"),
            row("6.0.0-rc.1"),
            row("bad"),
            good,
        ]
        self.assertIs(Catalog(rows).choose("paint", " LINUX "), good)

    def test_interchange_and_ui(self):
        original = (row("1.0.0"), row("1.1.0"))
        catalog = Catalog.from_manifest(encode_manifest(original))
        self.assertEqual(decode_manifest(encode_manifest(original)), original)
        self.assertEqual(
            selection_summary(catalog, "paint", "linux")["version"], "1.1.0"
        )
        self.assertEqual(
            selection_summary(catalog, "absent", "linux"), {"status": "unavailable"}
        )
