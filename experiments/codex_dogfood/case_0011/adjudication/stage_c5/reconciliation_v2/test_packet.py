"""Repository-side tests read only the approved blinded packet and its binding."""

from __future__ import annotations

import gzip
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packet as b

ROOT = Path(__file__).resolve().parent
v = b.validator(ROOT / "packet/validate_packet.py")


class ConstructionTests(unittest.TestCase):
    def test_v1_defect_regression_and_unchanged_propositions(self) -> None:
        old_root = ROOT.parent / "reconciliation/packet"
        self.assertEqual(
            b.validator(old_root / "validate_packet.py").validate(old_root)["status"],
            "PASS",
        )
        old = v.load(gzip.decompress((old_root / "packet.json.gz").read_bytes()))
        pairs = set()
        for p in old["propositions"]:
            if p["kind"] in {"PAIR_LABEL", "DIRECT_RATIONALE"}:
                pairs.add((p["subject"]["need"], p["subject"]["unit"]))
            if p["kind"] == "UNIT_STATUS":
                for position in p["positions"].values():
                    pairs.update(
                        (r["need"], p["subject"]["unit"])
                        for r in position["rationales"]
                    )
        self.assertEqual(len(pairs), 50)
        self.assertEqual(18 * 32 - len(pairs), 526)
        self.assertNotIn("absent_pair_default", old)
        self.assertNotIn("pair_mappings", old)
        new = v.load(gzip.decompress(b.payloads()["packet.json.gz"]))
        self.assertEqual(old["propositions"], new["propositions"])
        self.assertEqual(old["semantics"], new["semantics"])
        self.assertEqual(old["position_order"], new["position_order"])

    def test_double_build_frozen_bytes_and_overwrite_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first, second = Path(temporary) / "first", Path(temporary) / "second"
            self.assertEqual(b.write(first), b.write(second))
            expected = b.payloads()
            for name, raw in expected.items():
                self.assertEqual((first / name).read_bytes(), raw)
                self.assertEqual((second / name).read_bytes(), raw)
                self.assertEqual((ROOT / "packet" / name).read_bytes(), raw)
            self.assertEqual(v.validate(first)["status"], "PASS")
            with self.assertRaisesRegex(AssertionError, "OVERWRITE_REFUSED"):
                b.write(first)

    def test_instructions_no_default_or_full_derivation(self) -> None:
        instructions = (ROOT / "packet/INSTRUCTIONS.md").read_text(encoding="utf-8")
        for rule in (
            "Do not derive the final 576-pair mapping.",
            "Do not assign labels to omitted pairs.",
            "Do not assume omitted pairs are DOES_NOT_COVER.",
            "Do not reconstruct source adjudications.",
            "Do not calculate final full-frame unit/need/alternative counts.",
            "Resolve only the 110 supplied propositions.",
            "WHY THIS PACKET DOES NOT CONTAIN 576 PAIR LABELS",
        ):
            self.assertIn(rule, instructions)


if __name__ == "__main__":
    unittest.main()
