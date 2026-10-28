import unittest

from releasevault import Artifact, Catalog
from releasevault.versions import parse_version, version_order


class VersionTests(unittest.TestCase):
    def test_presentation_uses_shared_precedence(self):
        versions = ["1.0.0", "1.0.0-rc.10", "1.0.0-rc.2"]
        records = [Artifact("paint", "linux", v, v) for v in versions]
        self.assertEqual(
            Catalog(records).versions("paint"), ("1.0.0-rc.2", "1.0.0-rc.10", "1.0.0")
        )

    def test_strict_parser_and_core_numeric_order(self):
        for invalid in ("1.0", "01.0.0", "v1.0.0", "1.0.0-01"):
            with self.assertRaises(ValueError):
                parse_version(invalid)
            with self.assertRaises(ValueError):
                version_order(invalid)
        self.assertLess(version_order("1.9.0"), version_order("1.10.0"))
