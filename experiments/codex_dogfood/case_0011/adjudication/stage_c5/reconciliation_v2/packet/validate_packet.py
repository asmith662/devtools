"""Standalone neutral-packet integrity, identity, structure and leakage validator."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

FILES = {
    "packet.json.gz",
    "manifest.json",
    "integrity.json",
    "INSTRUCTIONS.md",
    "validate_packet.py",
    "reconcile_c5_v2.py",
    "test_reconcile_c5_v2.py",
}
COUNTS = {
    "PAIR_LABEL": 32,
    "DIRECT_RATIONALE": 12,
    "UNIT_STATUS": 11,
    "NEED_CLASSIFICATION": 7,
    "ALTERNATIVE_COMPLETENESS": 10,
    "UNIT_GRANULARITY": 32,
    "COLLECTIVE_COVERAGE": 6,
}
KINDS = {
    "PAIR_LABEL",
    "DIRECT_RATIONALE",
    "UNIT_STATUS",
    "NEED_CLASSIFICATION",
    "ALTERNATIVE_COMPLETENESS",
    "UNIT_GRANULARITY",
    "COLLECTIVE_COVERAGE",
}
DECISIONS = [
    "ACCEPT_POSITION_1",
    "ACCEPT_POSITION_2",
    "REPLACE_WITH_RECONCILED_JUDGMENT",
    "UNRESOLVED",
]
DENIED = {
    "lexical_query",
    "lexical_queries",
    "query_strings",
    "analyzed_terms",
    "analyzer_terms",
    "retrieval_route",
    "retrieval_routes",
    "retrieval_results",
    "result_resource",
    "result_resources",
    "rank",
    "ranks",
    "score",
    "scores",
    "acquisition_cost",
    "acquisition_costs",
    "costs",
    "arm_identity",
    "arm_id",
    "treatment",
    "treatment_results",
    "stage_d_outcomes",
    "confirmation_data",
    "source_path",
    "answer_path",
    "resource_path",
    "gold_answer_resource_paths",
    "model",
    "model_identity",
    "primary",
    "review",
    "independent",
    "author",
    "provenance",
    "chronology",
    "timestamp",
    "created_at",
    "query",
    "queries",
    "terms",
    "route",
    "results",
    "cost",
    "arm",
    "final_mapping",
    "pair_mappings",
    "unit_coverage_table",
    "need_classification_table",
    "alternative_coverage_table",
    "stage_d_metrics",
    "u1_outcome",
}
SOURCE_TEXT = re.compile(
    r"\b(primary|independent (?:reviewer|review|adjudication|C[.]5)|"
    r"astra|gpt[- ]?\d|qwen|deepseek|claude|chronology)\b|"
    r"before source inspection|after source inspection",
    re.IGNORECASE,
)
LEAK_TEXT = re.compile(
    r"(?:https?://|[A-Z]:\\|app://)|\b(?:lexical quer(?:y|ies)|"
    r"analyzer terms|retrieval results|treatment results|acquisition costs|"
    r"confirmation data|stage d outcomes)\s*[:=]",
    re.IGNORECASE,
)


def canonical(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        assert key not in result, "duplicate JSON field"
        result[key] = value
    return result


def load(raw: bytes) -> Any:
    return json.loads(raw, object_pairs_hook=unique)


def check_leakage(value: Any) -> None:
    if isinstance(value, dict):
        keys = {re.sub(r"[- ]", "_", key.lower()) for key in value}
        assert not DENIED & keys, "forbidden/source field"
        for key, child in value.items():
            assert not SOURCE_TEXT.search(key), "source identifier"
            check_leakage(child)
    elif isinstance(value, list):
        for child in value:
            check_leakage(child)
    elif isinstance(value, str):
        assert not SOURCE_TEXT.search(value), "source identity/chronology"
        assert not LEAK_TEXT.search(value), "external/treatment leakage"


def check_payload(packet: dict[str, Any]) -> None:
    check_leakage(packet)
    assert packet["schema"] == "case-0011-neutral-c5-reconciliation-v2"
    assert set(packet) == {
        "schema",
        "semantics",
        "bindings",
        "position_order",
        "propositions",
        "rules",
    }
    semantics = packet["semantics"]
    assert set(semantics) == {
        "case_identity",
        "task_identity",
        "task",
        "obligations",
        "information_needs",
        "units",
        "alternatives",
        "mapping_labels",
        "need_labels",
        "direct_coverage_rule",
        "unit_coverage",
        "display_aliases",
    }
    assert semantics["case_identity"] == "case-0011"
    assert semantics["task_identity"] == "case-0011-context-utf8-ceiling"
    needs = {n["identity"] for n in semantics["information_needs"]}
    units = {u["identity"] for u in semantics["units"]}
    alternatives = {
        a["identity"]: a for g in semantics["alternatives"] for a in g["alternatives"]
    }
    assert len(needs) == len(semantics["information_needs"]) == 18
    assert len(units) == len(semantics["units"]) == 32
    assert len(alternatives) == 12
    assert semantics["display_aliases"] == {
        "needs": {
            n["identity"]: f"N{i:02d}"
            for i, n in enumerate(semantics["information_needs"], 1)
        },
        "units": {
            u["identity"]: f"U{i:02d}" for i, u in enumerate(semantics["units"], 1)
        },
    }
    for group in semantics["alternatives"]:
        assert group["alternative_logic"] == "ANY_COMPLETE_ALTERNATIVE"
        for alternative in group["alternatives"]:
            assert alternative["member_logic"] == "ALL_COMPLEMENTARY"
            assert set(alternative["units"]) <= units
    for key, value in packet["bindings"].items():
        assert key in {
            "frozen_needs_sha256",
            "reviewed_gold_sha256",
            "reliability_comparison_sha256",
        }
        assert re.fullmatch("[0-9a-f]{64}", value)
    assert set(packet["bindings"]) == {
        "frozen_needs_sha256",
        "reviewed_gold_sha256",
        "reliability_comparison_sha256",
    }
    propositions = packet["propositions"]
    ids = [p["identity"] for p in propositions]
    assert ids == sorted(set(ids)), "duplicate or unordered propositions"
    assert len(ids) == 110
    assert dict(Counter(p["kind"] for p in propositions)) == COUNTS
    for p in propositions:
        kind, subject = p["kind"], p["subject"]
        assert kind in KINDS
        assert p["identity"] == sha(canonical({"kind": kind, "subject": subject}))
        if "need" in subject:
            assert subject["need"] in needs
        if "unit" in subject:
            assert subject["unit"] in units
        if "alternative" in subject:
            assert subject["alternative"] in alternatives
        positions = p["positions"]
        assert list(positions) == [
            f"position_{i}" for i in range(1, len(positions) + 1)
        ]
        assert len(positions) == (
            1 if kind in {"UNIT_GRANULARITY", "COLLECTIVE_COVERAGE"} else 2
        )
        digests = [sha(canonical(v)) for v in positions.values()]
        assert digests == sorted(digests), "non-neutral order"
        assert p["decisions"] == (
            DECISIONS
            if len(positions) == 2
            else [
                "CONFIRM_PROPOSITION",
                "REPLACE_WITH_RECONCILED_JUDGMENT",
                "UNRESOLVED",
            ]
        )
        if kind in {"PAIR_LABEL", "DIRECT_RATIONALE"}:
            assert all(
                v["label"] in semantics["mapping_labels"]
                and v["rationale"]
                and v["fact_sought"]
                and v["fact_established"]
                for v in positions.values()
            )
        if kind == "PAIR_LABEL":
            assert len({v["label"] for v in positions.values()}) == 2
        if kind == "DIRECT_RATIONALE":
            assert all(v["label"] == "DIRECTLY_COVERS" for v in positions.values())
        if kind == "UNIT_STATUS":
            assert all(
                v["status"] in semantics["unit_coverage"]
                and isinstance(v["rationales"], list)
                for v in positions.values()
            )
        if kind == "NEED_CLASSIFICATION":
            assert all(
                v["classification"] in semantics["need_labels"]
                and v["rationale"]
                and v["formulation_rationale"]
                for v in positions.values()
            )
        if kind == "ALTERNATIVE_COMPLETENESS":
            assert all(
                type(v["strict_direct_complete"]) is bool and v["rationale"]
                for v in positions.values()
            )
        if kind == "UNIT_GRANULARITY":
            assert positions["position_1"]["category"] in p["permitted_categories"]
            assert positions["position_1"]["rationale"]
            assert p["permitted_categories"] == [
                "ATOMIC_FOR_NEED_MAPPING",
                "COLLECTIVELY_COVERABLE",
                "OVERCOMPOUND_FOR_PAIRWISE_MAPPING",
                "AMBIGUOUS_GRANULARITY",
            ]
        if kind == "COLLECTIVE_COVERAGE":
            for proposed in positions["position_1"]["sets"]:
                assert len(proposed["needs"]) == len(set(proposed["needs"])) >= 2
                assert set(proposed["needs"]) <= needs
                assert (
                    proposed["sufficiency_rationale"]
                    and proposed["minimality_rationale"]
                )
                assert {r["need"] for r in proposed["member_necessity"]} == set(
                    proposed["needs"]
                )
                assert all(
                    r["covered_part"] and r["missing_without_others"]
                    for r in proposed["member_necessity"]
                )
    assert sum(p["kind"] == "UNIT_GRANULARITY" for p in propositions) == 32


def validate(root: Path, *, completed: bool = False) -> dict[str, Any]:
    assert root.is_dir() and not root.is_symlink()
    assert not getattr(root.lstat(), "st_file_attributes", 0) & 0x400
    files = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        assert (
            not path.is_symlink()
            and not getattr(path.lstat(), "st_file_attributes", 0) & 0x400
        )
        if path.is_file():
            files.add(relative)
        elif path.is_dir():
            raise AssertionError("unexpected directory")
    outputs = {
        "c5_reconciliation_v2_decisions.json",
        "c5_reconciliation_v2_validation.json",
        "c5_reconciliation_v2_hashes.json",
    }
    assert files == FILES | (outputs if completed else set()), (
        "sterile workspace whitelist"
    )
    integrity = load((root / "integrity.json").read_bytes())
    manifest_raw = (root / "manifest.json").read_bytes()
    manifest = load(manifest_raw)
    assert manifest["schema"] == "case-0011-neutral-c5-manifest-v2"
    assert integrity["schema"] == "case-0011-neutral-c5-integrity-v2"
    assert manifest["output_scope"] == "BOUNDED_110_PROPOSITION_DECISIONS_ONLY"
    assert manifest["absent_pair_default"] is None
    assert integrity["manifest_sha256"] == sha(manifest_raw)
    assert set(integrity["files"]) == FILES - {"integrity.json"}
    for name, expected in integrity["files"].items():
        assert sha((root / name).read_bytes()) == expected, f"file hash: {name}"
    archive = (root / "packet.json.gz").read_bytes()
    payload = gzip.decompress(archive)
    assert sha(archive) == manifest["archive_sha256"] == integrity["archive_sha256"]
    assert (
        sha(payload)
        == manifest["canonical_payload_sha256"]
        == integrity["canonical_payload_sha256"]
    )
    packet = load(payload)
    check_payload(packet)
    assert canonical(packet) == payload
    assert manifest["packet_identity"] == sha(payload)
    assert manifest["semantic_propositions_sha256"] == sha(
        canonical(packet["propositions"])
    )
    assert packet["bindings"] == manifest["bindings"]
    counts = dict(sorted(Counter(p["kind"] for p in packet["propositions"]).items()))
    assert counts == manifest["proposition_counts"]
    assert counts == COUNTS
    assert [p["identity"] for p in packet["propositions"]] == manifest[
        "proposition_identities"
    ]
    return {
        "status": "PASS",
        "proposition_counts": counts,
        "archive_sha256": sha(archive),
        "payload_sha256": sha(payload),
        "manifest_sha256": sha(manifest_raw),
        "integrity_sha256": sha((root / "integrity.json").read_bytes()),
        "whitelist": sorted(FILES),
    }


if __name__ == "__main__":
    print(
        json.dumps(validate(Path(__file__).resolve().parent), sort_keys=True, indent=2)
    )
