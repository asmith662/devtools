"""Frozen held-out requirements and independent finite-table positive control.

Reference mode validates these tests and the public focused tests before entry.
The table is not a candidate patch and is never exposed to the model.
"""

import ast
import importlib
import re
import sys
import unittest
from pathlib import Path

REFERENCE_ORDER = (
    "0.9.0",
    "1.0.0-1",
    "1.0.0-2",
    "1.0.0-10",
    "1.0.0-11",
    "1.0.0-alpha",
    "1.0.0-alpha.1",
    "1.0.0-alpha.beta",
    "1.0.0-beta",
    "1.0.0-beta.2",
    "1.0.0-beta.11",
    "1.0.0-rc.1",
    "1.0.0-rc.2",
    "1.0.0-rc.9",
    "1.0.0-rc.10",
    "1.0.0",
    "1.1.0",
    "1.2.0",
    "1.5.0",
    "1.9.0",
    "1.10.0",
    "2.0.0-rc.2",
    "2.0.0-rc.9",
    "2.0.0-rc.10",
    "2.0.0",
    "3.0.0-rc.1",
    "6.0.0-rc.1",
    "7.0.0",
    "8.0.0",
    "9.0.0",
)


def reference_order(text):
    # Independent literal ranks: no candidate parser/key/selector is called.
    core = text.partition("+")[0]
    if "+" in text and not re.fullmatch(
        r"[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*", text.partition("+")[2]
    ):
        raise ValueError("Invalid finite-oracle build spelling")
    if core not in REFERENCE_ORDER:
        raise ValueError("Outside the finite independently authored oracle language")
    return REFERENCE_ORDER.index(core)


def reference_catalog_type():
    from releasevault.manifest import decode_manifest

    class ReferenceCatalog:
        def __init__(self, records):
            self.records = tuple(records)

        @classmethod
        def from_manifest(cls, text):
            return cls(decode_manifest(text))

        def choose(self, project, platform, *, include_previews=False):
            admitted = []
            for row in self.records:
                if (
                    not row.enabled
                    or row.project != project
                    or row.platform.strip().casefold() != platform.strip().casefold()
                ):
                    continue
                try:
                    reference_order(row.version)
                except ValueError:
                    continue
                if not include_previews and "-" in row.version.partition("+")[0]:
                    continue
                admitted.append(row)
            return max(
                admitted, key=lambda row: reference_order(row.version), default=None
            )

        def versions(self, project):
            rows = []
            for row in self.records:
                if row.project != project:
                    continue
                try:
                    reference_order(row.version)
                except ValueError:
                    continue
                rows.append(row.version)
            return tuple(sorted(rows, key=reference_order))

    return ReferenceCatalog


class Heldout(unittest.TestCase):
    def row(self, version, uri=None, **kw):
        return self.Artifact(
            kw.get("project", "paint"),
            kw.get("platform", "linux"),
            version,
            uri or version,
            kw.get("enabled", True),
        )

    def test_official_precedence_chain(self):
        # Literal sequence in the SemVer2 precedence examples, with numeric cases.
        versions = list(REFERENCE_ORDER[1:16])
        actual = self.Catalog([self.row(v) for v in reversed(versions)]).versions(
            "paint"
        )
        self.assertEqual(actual, tuple(versions))

    def test_numeric_identifiers_precede_nonnumeric(self):
        numeric, text = self.row("1.0.0-11"), self.row("1.0.0-alpha")
        self.assertIs(
            self.Catalog([text, numeric]).choose(
                "paint", "linux", include_previews=True
            ),
            text,
        )

    def test_shorter_prerelease_prefix(self):
        shorter, longer = self.row("1.0.0-alpha"), self.row("1.0.0-alpha.1")
        self.assertIs(
            self.Catalog([longer, shorter]).choose(
                "paint", "linux", include_previews=True
            ),
            longer,
        )

    def test_build_metadata_does_not_change_display_order(self):
        rows = [self.row("1.0.0+zzz"), self.row("1.0.0+aaa"), self.row("1.0.0")]
        self.assertEqual(
            self.Catalog(rows).versions("paint"), ("1.0.0+zzz", "1.0.0+aaa", "1.0.0")
        )

    def test_prerelease_build_ties_keep_first_object(self):
        first, second = self.row("1.0.0-rc.2+a"), self.row("1.0.0-rc.2+z")
        self.assertIs(
            self.Catalog([first, second]).choose(
                "paint", "linux", include_previews=True
            ),
            first,
        )

    def test_newer_core_beats_older_stable(self):
        newer, stable = self.row("3.0.0-rc.1"), self.row("2.0.0")
        catalog = self.Catalog([stable, newer])
        self.assertIs(catalog.choose("paint", "linux", include_previews=True), newer)
        self.assertIs(catalog.choose("paint", "linux"), stable)

    def test_project_platform_status_and_invalid_records(self):
        good = self.row("1.0.0")
        rows = [
            self.row("9.0.0", enabled=False),
            self.row("8.0.0", project="else"),
            self.row("7.0.0", platform="mac"),
            self.row("1.0.0-01"),
            self.row("bad"),
            good,
        ]
        self.assertIs(
            self.Catalog(iter(rows)).choose("paint", " LINUX ", include_previews=True),
            good,
        )
        self.assertIsNone(self.Catalog(rows).choose("absent", "linux"))

    def test_snapshot_input_ownership(self):
        original = [self.row("1.0.0"), self.row("2.0.0")]
        catalog = self.Catalog(iter(original))
        catalog.versions("paint")
        self.assertEqual([r.version for r in original], ["1.0.0", "2.0.0"])
        self.assertIs(catalog.choose("paint", "linux"), original[1])

    def test_strict_key_and_parser_invalid_inputs(self):
        for invalid in ("v1.0.0", "1.0", "01.0.0", "1.0.0-01", "1.0.0-", "1.0.0+"):
            with self.assertRaises(ValueError):
                self.order(invalid)
            with self.assertRaises(ValueError):
                self.parse(invalid)

    def test_runtime_standard_library_only(self):
        for path in (self.root / "releasevault").glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                names = (
                    [a.name.split(".")[0] for a in node.names]
                    if isinstance(node, ast.Import)
                    else [node.module.split(".")[0]]
                    if isinstance(node, ast.ImportFrom)
                    and not node.level
                    and node.module
                    else []
                )
                self.assertTrue(
                    all(
                        n in sys.stdlib_module_names or n == "releasevault"
                        for n in names
                    ),
                    str(path),
                )


def main():
    root = Path(sys.argv[1]).resolve()
    reference = "--reference" in sys.argv
    focused = "--focused" in sys.argv
    sys.path.insert(0, str(root))
    import releasevault
    from releasevault.versions import parse_version, version_order

    catalog = reference_catalog_type() if reference else releasevault.Catalog
    order = reference_order if reference else version_order
    if focused:
        modules = [
            importlib.import_module(n)
            for n in ("tests.test_catalog", "tests.test_versions")
        ]
        if reference:
            for module in modules:
                module.Catalog = catalog
            modules[1].version_order = reference_order
        suite = unittest.TestSuite(
            unittest.defaultTestLoader.loadTestsFromModule(m) for m in modules
        )
    else:
        Heldout.Catalog = catalog
        Heldout.Artifact = releasevault.Artifact
        Heldout.order = staticmethod(order)
        Heldout.parse = staticmethod(parse_version)
        Heldout.root = root
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Heldout)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
