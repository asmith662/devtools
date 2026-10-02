"""Focused isolated checks; no production imports or repository test collection."""

import contextlib
import copy
import io
import runpy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class SupportTests(unittest.TestCase):
    """Check deterministic replay and rejection of corrupt adjudication data."""

    @classmethod
    def setUpClass(cls):
        previous = sys.argv
        try:
            sys.argv = ["freeze_blind_judgments.py", "--check"]
            with contextlib.redirect_stdout(io.StringIO()):
                cls.namespace = runpy.run_path(str(ROOT / "freeze_blind_judgments.py"))
        finally:
            sys.argv = previous

    def rejected(self, mutate):
        value = copy.deepcopy(self.namespace["artifact"])
        mutate(value)
        with self.assertRaises(AssertionError):
            self.namespace["validate"](value)

    def test_exact_coverage_and_deterministic_replay(self):
        value = self.namespace["artifact"]
        self.namespace["validate"](value)
        self.assertEqual(len(value["resource_matrix"]), 498)
        self.assertEqual(
            self.namespace["canonical"](value),
            (ROOT / "blind_judgments.json").read_bytes(),
        )

    def test_duplicate_missing_and_unexpected_resources(self):
        self.rejected(
            lambda value: value["resource_matrix"].append(value["resource_matrix"][0])
        )
        self.rejected(lambda value: value["resource_matrix"].pop())
        self.rejected(
            lambda value: value["resource_matrix"][0].update(
                resource_identity="unknown"
            )
        )

    def test_unknown_witness_and_duplicate_unit(self):
        self.rejected(
            lambda value: value["obligations"][0]["acceptable_witness_alternatives"][0][
                "all_of"
            ].append("unknown")
        )
        self.rejected(
            lambda value: value["obligations"][0]["information_units"].append(
                value["obligations"][0]["information_units"][0]
            )
        )

    def test_missing_inferability_and_wrong_applicability(self):
        self.rejected(
            lambda value: value["obligations"][0]["information_units"][0].update(
                inferability=""
            )
        )
        self.rejected(lambda value: value["obligations"][0].update(applicability=""))

    def test_forbidden_field_and_digest_corruption(self):
        self.rejected(lambda value: value.update(query_text="forbidden"))
        self.rejected(lambda value: value["artifact_digest"].update(value="0" * 64))

    def test_matrix_cannot_disagree_with_units(self):
        self.rejected(
            lambda value: value["resource_matrix"][0]["dispositions"].update(
                validation="REQUIRED"
            )
        )


if __name__ == "__main__":
    unittest.main()
