"""Self-contained synthetic schema checks; these are never semantic decisions."""

from __future__ import annotations

import copy
import gzip
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from typing import Any
from unittest.mock import patch

import reconcile_c5_v2 as r
import validate_packet as v

ROOT = Path(__file__).resolve().parent


def packet() -> dict[str, Any]:
    value: dict[str, Any] = v.load(
        gzip.decompress((ROOT / "packet.json.gz").read_bytes())
    )
    return value


def synthetic(p: dict[str, Any], *, accept: bool = False) -> dict[str, Any]:
    """Placeholder texts in test memory only; no publication in the real workspace."""
    rows = []
    for prop in p["propositions"]:
        kind = prop["kind"]
        pos = prop["positions"]["position_1"]
        decision = (
            (
                "CONFIRM_PROPOSITION"
                if len(prop["positions"]) == 1
                else "ACCEPT_POSITION_1"
            )
            if accept
            else "UNRESOLVED"
        )
        payload: dict[str, Any]
        if kind in {"PAIR_LABEL", "DIRECT_RATIONALE"}:
            payload = {
                "label": pos["label"]
                if accept
                else "DIRECTLY_COVERS"
                if kind == "DIRECT_RATIONALE"
                else "AMBIGUOUS",
                "rationale": "Synthetic schema placeholder.",
                "covered_component": "Synthetic component.",
                "missing_component": "Synthetic missing component.",
                "complete_unit_counterfactual": "Synthetic counterfactual placeholder.",
            }
        elif kind in {"UNIT_STATUS", "NEED_CLASSIFICATION", "UNIT_GRANULARITY"}:
            field = "status" if kind == "UNIT_STATUS" else "classification"
            value = (
                pos["category" if kind == "UNIT_GRANULARITY" else field]
                if accept
                else {
                    "UNIT_STATUS": "AMBIGUOUS_ONLY",
                    "NEED_CLASSIFICATION": "AMBIGUOUS",
                    "UNIT_GRANULARITY": "AMBIGUOUS_GRANULARITY",
                }[kind]
            )
            payload = {field: value, "rationale": "Synthetic schema placeholder."}
        elif kind == "ALTERNATIVE_COMPLETENESS":
            a = next(
                a
                for group in p["semantics"]["alternatives"]
                for a in group["alternatives"]
                if a["identity"] == prop["subject"]["alternative"]
            )
            supplied = any("diagnostic_state" in x for x in prop["positions"].values())
            payload = {
                "strict_direct_complete": pos["strict_direct_complete"]
                if accept
                else None,
                "granularity_aware_state": pos.get("diagnostic_state", "AMBIGUOUS")
                if supplied
                else None,
                "rationale": "Synthetic schema placeholder.",
                "members": [
                    {"unit": unit, "rationale": "Synthetic member."}
                    for unit in sorted(a["units"])
                ],
            }
        else:
            payload = {
                "rationale": "Synthetic schema placeholder.",
                "sets": [
                    {
                        "needs": s["needs"],
                        "classification": "VALID_MINIMAL_COLLECTIVE_SET"
                        if accept
                        else "AMBIGUOUS",
                        "rationale": "Synthetic sufficiency.",
                        "minimality_analysis": "Synthetic minimality.",
                        "contributions": [
                            {
                                "need": n,
                                "distinct_contribution": "Synthetic contribution.",
                                "removal_analysis": "Synthetic removal.",
                            }
                            for n in sorted(s["needs"])
                        ],
                    }
                    for s in pos["sets"]
                ],
            }
        rows.append(
            {
                "identity": prop["identity"],
                "kind": kind,
                "subject": prop["subject"],
                "decision": decision,
                "payload": payload,
                "evidence_references": [f"proposition:{prop['identity']}/position_1"],
            }
        )
    return {
        "schema": "case-0011-c5-reconciliation-decisions-v2",
        "packet_identity": v.sha(v.canonical(p)),
        "bindings": p["bindings"],
        "decisions": rows,
        "decision_category_counts": dict(
            sorted(Counter(row["decision"] for row in rows).items())
        ),
        "unresolved_count": 0 if accept else 110,
        "method": {
            "scope": "BOUNDED_110_PROPOSITION_DECISIONS_ONLY",
            "procedure": "Synthetic schema test only.",
            "provenance": "TREATMENT_BLIND_SEMANTIC_RECONCILIATION",
        },
        "blindness_attestations": dict.fromkeys(r.ATTESTATIONS, True),
    }


class SchemaTests(unittest.TestCase):
    def test_integrity_corruption_and_reparse_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in v.FILES:
                (root / name).write_bytes((ROOT / name).read_bytes())
            for name in v.FILES:
                original = (root / name).read_bytes()
                (root / name).write_bytes(original + b"corrupt")
                with (
                    self.subTest(name=name),
                    self.assertRaises((AssertionError, ValueError)),
                ):
                    v.validate(root)
                (root / name).write_bytes(original)
            real_lstat = Path.lstat

            def reparse(path: Path) -> Any:
                class Stat:
                    st_file_attributes = 0x400

                return Stat() if path == root else real_lstat(path)

            with (
                patch.object(Path, "lstat", reparse),
                self.assertRaises(AssertionError),
            ):
                v.validate(root)

    def test_required_rationale_attestations_and_accepted_value(self) -> None:
        p = packet()
        for kind in v.COUNTS:
            a = synthetic(p)
            row = next(row for row in a["decisions"] if row["kind"] == kind)
            row["payload"]["rationale"] = " "
            with self.assertRaises(AssertionError):
                r.check_decisions(p, a)
        a = synthetic(p)
        a["blindness_attestations"]["no_treatment_access"] = False
        with self.assertRaises(AssertionError):
            r.check_decisions(p, a)
        a = synthetic(p, accept=True)
        row = next(row for row in a["decisions"] if row["kind"] == "PAIR_LABEL")
        row["payload"]["label"] = "AMBIGUOUS"
        with self.assertRaises(AssertionError):
            r.check_decisions(p, a)
        a = synthetic(p)
        row = next(row for row in a["decisions"] if row["kind"] == "DIRECT_RATIONALE")
        row["payload"]["label"] = "AMBIGUOUS"
        with self.assertRaises(AssertionError):
            r.check_decisions(p, a)

    def test_packet_and_exact_categories(self) -> None:
        self.assertEqual(v.validate(ROOT)["status"], "PASS")
        v.check_payload(packet())

    def test_replay_acceptance_and_uncertainty(self) -> None:
        p = packet()
        for accept in (False, True):
            a = synthetic(p, accept=accept)
            self.assertEqual(r.replay(p, a), r.replay(p, copy.deepcopy(a)))
            self.assertEqual(r.check_decisions(p, a)["propositions"], 110)

    def test_no_full_mapping_no_default_and_closed_schema(self) -> None:
        p = packet()
        for key in (
            "final_mapping",
            "pair_mappings",
            "absent_pair_default",
            "unit_coverage_table",
            "need_classification_table",
            "alternative_coverage_table",
            "stage_d_metrics",
            "u1_outcome",
        ):
            with self.subTest(key=key):
                a = synthetic(p)
                a[key] = []
                with self.assertRaises(AssertionError):
                    r.check_decisions(p, a)

    def test_duplicate_missing_unexpected_and_order(self) -> None:
        p = packet()
        for mode in ("duplicate", "missing", "unexpected", "order"):
            a = synthetic(p)
            if mode == "duplicate":
                a["decisions"][1] = a["decisions"][0]
            elif mode == "missing":
                a["decisions"].pop()
            elif mode == "unexpected":
                a["decisions"][0]["identity"] = "0" * 64
            else:
                a["decisions"].reverse()
            with self.assertRaises(AssertionError):
                r.check_decisions(p, a)

    def test_all_payload_fields_required(self) -> None:
        p = packet()
        a = synthetic(p)
        for kind in v.COUNTS:
            index = next(
                i for i, row in enumerate(a["decisions"]) if row["kind"] == kind
            )
            for field in a["decisions"][index]["payload"]:
                changed = copy.deepcopy(a)
                del changed["decisions"][index]["payload"][field]
                with (
                    self.subTest(kind=kind, field=field),
                    self.assertRaises((AssertionError, KeyError)),
                ):
                    r.check_decisions(p, changed)

    def test_decision_vocabulary_and_evidence(self) -> None:
        p = packet()
        for kind in v.COUNTS:
            a = synthetic(p)
            row = next(row for row in a["decisions"] if row["kind"] == kind)
            row["decision"] = (
                "ACCEPT_POSITION_2"
                if kind in {"UNIT_GRANULARITY", "COLLECTIVE_COVERAGE"}
                else "CONFIRM_PROPOSITION"
            )
            with self.assertRaises(AssertionError):
                r.check_decisions(p, a)
        a = synthetic(p)
        a["decisions"][0]["evidence_references"] = ["source:external"]
        with self.assertRaises(AssertionError):
            r.check_decisions(p, a)

    def test_each_kind_rejects_invalid_label(self) -> None:
        p = packet()
        for kind in v.COUNTS:
            a = synthetic(p)
            row = next(row for row in a["decisions"] if row["kind"] == kind)
            payload = row["payload"]
            if kind in {"PAIR_LABEL", "DIRECT_RATIONALE"}:
                payload["label"] = "DEFAULT"
            elif kind == "UNIT_STATUS":
                payload["status"] = "DEFAULT"
            elif kind in {"NEED_CLASSIFICATION", "UNIT_GRANULARITY"}:
                payload["classification"] = "DEFAULT"
            elif kind == "ALTERNATIVE_COMPLETENESS":
                payload["strict_direct_complete"] = "DEFAULT"
            else:
                payload["sets"][0]["classification"] = "DEFAULT"
            with self.assertRaises(AssertionError):
                r.check_decisions(p, a)

    def test_leakage_and_anonymization(self) -> None:
        for key in v.DENIED:
            with self.subTest(key=key), self.assertRaises(AssertionError):
                v.check_leakage({key: "injected"})
        for value in (
            "primary reviewer",
            "independent reviewer",
            "GPT-6",
            "Qwen",
            "before source inspection",
            "C:\\secret\\answer",
            "https://invalid.example/result",
            "retrieval results: injected",
        ):
            with self.subTest(value=value), self.assertRaises(AssertionError):
                v.check_leakage({"rationale": value})
        p = packet()
        a = synthetic(p)
        a["decisions"][0]["payload"]["rationale"] = "primary reviewer"
        with self.assertRaises(AssertionError):
            r.check_decisions(p, a)

    def test_neutral_order_and_packet_coverage_rejection(self) -> None:
        p = packet()
        row = next(x for x in p["propositions"] if len(x["positions"]) == 2)
        row["positions"]["position_1"], row["positions"]["position_2"] = (
            row["positions"]["position_2"],
            row["positions"]["position_1"],
        )
        with self.assertRaises(AssertionError):
            v.check_payload(p)
        p = packet()
        p["propositions"].pop()
        with self.assertRaises(AssertionError):
            v.check_payload(p)

    def test_immutable_publish_completed_replay_and_whitelist(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in v.FILES:
                (root / name).write_bytes((ROOT / name).read_bytes())
            (root / ".local").mkdir()
            with self.assertRaises(AssertionError):
                v.validate(root)
            (root / ".local").rmdir()
            (root / "unexpected").write_bytes(b"unexpected")
            with self.assertRaises(AssertionError):
                v.validate(root)
            (root / "unexpected").unlink()
            r.publish(root, synthetic(packet()))
            self.assertEqual(r.validate_completed(root)["status"], "PASS")
            before = {name: (root / name).read_bytes() for name in r.OUTPUTS}
            with self.assertRaisesRegex(AssertionError, "OVERWRITE_REFUSED"):
                r.publish(root, synthetic(packet()))
            self.assertEqual(
                before, {name: (root / name).read_bytes() for name in r.OUTPUTS}
            )
            (root / "c5_reconciliation_v2_validation.json").write_bytes(b"{}")
            with self.assertRaises(AssertionError):
                r.validate_completed(root)


if __name__ == "__main__":
    unittest.main()
