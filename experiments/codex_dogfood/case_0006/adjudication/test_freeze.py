"""Focused freeze integrity tests; do not import current production source."""

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from freeze_judgments import (
    ROOT,
    build,
    canonical,
    expanded_cells,
    load_packet,
    reject_fields,
    validate,
    write_once,
)


class FreezeTests(unittest.TestCase):
    """Exercise fail-closed targets, frame accounting and immutable freeze."""

    @classmethod
    def setUpClass(cls):
        cls.document = build()
        cls.manifest, cls.resources = load_packet()

    def assert_invalid(self, document, message):
        with self.assertRaisesRegex(ValueError, message):
            validate(document, self.manifest, self.resources)

    def test_deterministic_replay_and_exact_frame(self):
        self.assertEqual(canonical(self.document), canonical(build()))
        cells = expanded_cells(self.document)
        self.assertEqual(len(cells), 5310)
        self.assertEqual(
            len({(resource, obligation) for resource, obligation, _ in cells}), 5310
        )
        self.assertEqual(
            {o["applicability"] for o in self.document["judgments"]}, {"APPLICABLE"}
        )

    def test_both_packet_digest_changes_rejected(self):
        for filename, message in (
            ("blind_manifest.json", "Manifest digest mismatch"),
            ("blind_resources.json.gz", "Archive digest mismatch"),
        ):
            with tempfile.TemporaryDirectory(dir=ROOT) as directory:
                packet_root = Path(directory)
                for name in ("blind_manifest.json", "blind_resources.json.gz"):
                    data = (ROOT / name).read_bytes()
                    (packet_root / name).write_bytes(
                        data + b"changed" if name == filename else data
                    )
                with (
                    patch("freeze_judgments.ROOT", packet_root),
                    self.assertRaisesRegex(ValueError, message),
                ):
                    load_packet()

    def test_duplicate_and_missing_resource_rejected(self):
        changed = copy.deepcopy(self.document)
        changed["eligible_resource_identities"][-1] = changed[
            "eligible_resource_identities"
        ][0]
        self.assert_invalid(changed, "Resource coverage")

    def test_unexpected_resource_rejected(self):
        changed = copy.deepcopy(self.document)
        changed["eligible_resource_identities"][0]["content_identity"] = "0" * 64
        self.assert_invalid(changed, "Resource coverage")

    def test_foreign_required_target_rejected(self):
        changed = copy.deepcopy(self.document)
        changed["information_units"]["candidate-key"]["resource_identity"][
            "content_identity"
        ] = "0" * 64
        self.assert_invalid(changed, "Foreign unit target")

    def test_out_of_bounds_unit_rejected(self):
        changed = copy.deepcopy(self.document)
        changed["information_units"]["candidate-key"]["line_ranges"] = [[1, 99999]]
        self.assert_invalid(changed, "Unit range")

    def test_missing_obligation_or_applicability_rejected(self):
        changed = copy.deepcopy(self.document)
        changed["judgments"].pop()
        self.assert_invalid(changed, "Judgment completeness")
        changed = copy.deepcopy(self.document)
        changed["judgments"][0]["applicability"] = "unknown"
        self.assert_invalid(changed, "Applicability")

    def test_alternative_requires_all_valid_distinct_members(self):
        for members in ([], ["candidate-key", "candidate-key"], ["foreign"]):
            changed = copy.deepcopy(self.document)
            changed["judgments"][0]["acceptable_witness_alternatives"][0]["all"] = (
                members
            )
            self.assert_invalid(changed, "Alternative target structure")

    def test_required_member_cannot_be_orphaned(self):
        changed = copy.deepcopy(self.document)
        changed["judgments"][0]["acceptable_witness_alternatives"][0]["all"].pop()
        self.assert_invalid(changed, "Required units outside alternatives")

    def test_inferability_and_discovery_prerequisites_rejected(self):
        changed = copy.deepcopy(self.document)
        record = changed["judgments"][0]["required_units"][0]
        record["inferability"] = "unknown"
        self.assert_invalid(changed, "Inferability")
        record["inferability"] = "INHERENT_DISCOVERY"
        self.assert_invalid(changed, "Discovery prerequisites")

    def test_forbidden_structured_fields_but_ordinary_words_allowed(self):
        reject_fields(
            {"information": "grounding generation hypothesis evidence routing"}
        )
        for field in (
            "native_rank",
            "role_preferences",
            "locator",
            "projection_operator",
            "recovery_history",
        ):
            with self.assertRaisesRegex(ValueError, "Forbidden structured field"):
                reject_fields({"nested": [{field: "sealed"}]})

    def test_gap_representation_required(self):
        changed = copy.deepcopy(self.document)
        changed["task_interpretation_gaps"] = {}
        self.assert_invalid(changed, "Gap representation")

    def test_freeze_refuses_overwrite_and_keeps_bytes(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            output = Path(directory) / "judgments.json"
            write_once(self.document, output)
            before = output.read_bytes()
            with self.assertRaisesRegex(ValueError, "Refusing overwrite"):
                write_once(self.document, output)
            self.assertEqual(output.read_bytes(), before)
            self.assertTrue(output.with_suffix(".sha256").exists())


if __name__ == "__main__":
    unittest.main()
