"""Explicit blind comparison and neutral-packet validation, without collection."""

# Standalone non-installable JSON evidence scripts; long sealed claims remain literal.
# ruff: noqa: INP001, CPY001, COM812, D103, S101, PLR2004, PT018, RUF005
from __future__ import annotations

import copy
import gzip
import json
from typing import Any

import pytest
from build_packet import DEST, build, metadata_check, validate_packet
from compare_gold import (
    EXPECTED,
    LABELS,
    ROOT,
    canonical,
    compare,
    frame_check,
    load,
    markdown,
    sha,
    write_new,
)


@pytest.fixture(scope="module")
def comparison() -> dict[str, Any]:
    return compare()


def test_import_hashes() -> None:
    assert {n: sha((ROOT / n).read_bytes()) for n in EXPECTED} == EXPECTED


def test_frame_and_duplicate_rejection(comparison: dict[str, Any]) -> None:
    assert comparison["frame_integrity"] == {
        "resources": 531,
        "obligations": 9,
        "qualified_cells": 4779,
        "duplicates": 0,
        "missing": 0,
        "unexpected": 0,
        "exact_task_and_obligations": True,
    }
    p = load(ROOT.parent / "judgments.json")
    r = load(ROOT / "stage_c_r_review.json")
    m = load(ROOT.parent / "manifest.json")
    resources = json.loads(
        gzip.decompress((ROOT.parent / "resources.json.gz").read_bytes())
    )["resources"]
    r["cells"][-1] = r["cells"][0]
    with pytest.raises(AssertionError):
        frame_check(p, r, m, resources)


def test_frame_foreign_identity_rejection() -> None:
    p = load(ROOT.parent / "judgments.json")
    r = load(ROOT / "stage_c_r_review.json")
    m = load(ROOT.parent / "manifest.json")
    r["frame"]["corpus_id"] = "foreign"
    with pytest.raises(AssertionError):
        frame_check(p, r, m, [])


def test_applicability(comparison: dict[str, Any]) -> None:
    assert len(comparison["applicability"]) == 9
    assert all(
        o["primary"] == o["review"] == "APPLICABLE" for o in comparison["applicability"]
    )


def test_confusion_partition(comparison: dict[str, Any]) -> None:
    matrix = comparison["confusion"]["matrix"]
    assert matrix == [[22, 16, 0, 0], [2, 32, 42, 0], [0, 5, 4660, 0], [0, 0, 0, 0]]
    assert sum(map(sum, matrix)) == 4779
    assert sum(matrix[i][i] for i in range(4)) == comparison["agreement_count"] == 4714
    assert comparison["disagreement_count"] == 65
    for i, label in enumerate(LABELS):
        v = comparison["per_label"][label]
        assert len(v["primary_only"]) + v["intersection_count"] == sum(matrix[i])
        assert len(v["review_only"]) + v["intersection_count"] == sum(
            row[i] for row in matrix
        )


@pytest.mark.parametrize("label", ["REQUIRED", "HELPFUL_ONLY"])
def test_set_partitions(comparison: dict[str, Any], label: str) -> None:
    for v in [
        comparison["per_label"][label],
        *[o[label] for o in comparison["per_obligation"].values()],
    ]:
        common = {tuple(x) if isinstance(x, list) else x for x in v["intersection"]}
        left = {tuple(x) if isinstance(x, list) else x for x in v["primary_only"]}
        right = {tuple(x) if isinstance(x, list) else x for x in v["review_only"]}
        union = {tuple(x) if isinstance(x, list) else x for x in v["union"]}
        assert not common & left and not common & right and not left & right
        assert common | left | right == union
        assert len(union) == v["union_count"]
        if union:
            assert v["jaccard"] == len(common) / len(union)
    req = comparison["required_resources"]
    assert req["intersection_count"] == 17 and req["union_count"] == 26


def test_unit_alignment(comparison: dict[str, Any]) -> None:
    alignment = comparison["units"]
    assert (
        alignment["aligned_primary_count"] + len(alignment["unmatched_primary"]) == 42
    )
    assert alignment["aligned_review_count"] + len(alignment["unmatched_review"]) == 31
    allowed = {
        "EXACT",
        "SUBSTANTIALLY_EQUIVALENT",
        "PRIMARY_BROADER",
        "REVIEW_BROADER",
        "PARTIAL_OVERLAP",
        "NO_MATCH",
        "AMBIGUOUS",
    }
    for pair in alignment["proposals"]:
        assert pair["classification"] in allowed
        assert pair["primary_supports"] and pair["review_supports"]
        assert pair["semantic_rationale"] and pair["rationale"]
        for s in pair["source_overlap"]:
            assert max(s["primary_span"][0], s["review_span"][0]) < min(
                s["primary_span"][1], s["review_span"][1]
            )
    adapter = next(
        a
        for a in alignment["proposals"]
        if a["primary"] == "U04" and a["review"] == "F5"
    )
    assert adapter["primary_only_obligations"] == ["ownership"]
    assert adapter["review_only_obligations"] == ["frame"]


def test_alternatives_and_sufficient_unions(comparison: dict[str, Any]) -> None:
    assert len(comparison["alternatives"]) == 9
    for source, expected in [
        ("primary", (20, 144, 8, 23, 25, 22)),
        ("review", (12, 8, 2, 15, 17, 15)),
    ]:
        s = comparison["sufficient_unions"][source]
        assert (
            tuple(
                s[k]
                for k in (
                    "alternatives",
                    "combinations",
                    "distinct_unions",
                    "minimum",
                    "maximum",
                )
            )
            + (len(s["indispensable_resources"]),)
            == expected
        )
        assert set(s["indispensable_resources"]) == set.intersection(
            *(set(u) for u in s["unions"])
        )
        for o in s["by_obligation"]:
            assert set(o["indispensable_resources"]) == set.intersection(
                *(set(a["resources"]) for a in o["alternatives"])
            )
    assert comparison["sufficient_unions"]["set_overlap"]["intersection_count"] == 0
    for o in comparison["alternatives"]:
        assert len(o["candidate_pairs"]) == o["primary"]["count"] * o["review"]["count"]


def test_gap_comparison(comparison: dict[str, Any]) -> None:
    g = comparison["gaps"]
    assert len(g["primary_task"]) == len(g["primary_supplemental_units"]) == 1
    assert g["review_task"] == "NONE" and g["review_supplemental_units"] == []
    assert len(g["primary_limitations"]) == 4 and len(g["review_limitations"]) == 5
    assert g["primary_repository_gaps"] == [] and g["review_repository_gaps"] == "NONE"


def test_deterministic_comparison_replay(comparison: dict[str, Any]) -> None:
    assert (
        canonical(comparison)
        == canonical(compare())
        == (ROOT / "reliability_comparison.json").read_bytes()
    )
    assert markdown(comparison) == (ROOT / "reliability_comparison.md").read_bytes()


def test_packet_double_build_and_exact_seals(comparison: dict[str, Any]) -> None:
    first, audit = build()
    assert (first, audit) == build()
    assert {p.name for p in first} == {
        "packet.json",
        "manifest.json",
        "integrity.json",
        "INSTRUCTIONS.md",
        "task.txt",
        "resources.json.gz",
    }
    assert all(p.read_bytes() == raw for p, raw in first.items())
    integrity = json.loads(first[DEST / "integrity.json"])
    for name, digest in integrity["files"].items():
        assert sha(first[DEST / name]) == digest
    payload = gzip.decompress(first[DEST / "resources.json.gz"])
    assert sha(payload) == integrity["canonical_payload_sha256"]
    packet = json.loads(first[DEST / "packet.json"])
    resources = json.loads(payload)["resources"]
    validate_packet(packet, resources, comparison)
    original = json.loads(
        gzip.decompress((ROOT.parent / "resources.json.gz").read_bytes())
    )["resources"]
    originals = {r["address"]: r for r in original}
    assert all(r == originals[r["address"]] for r in resources)
    assert set(DEST.iterdir()) == set(first)
    assert canonical(audit) == (ROOT / "packet_audit.json").read_bytes()


@pytest.mark.parametrize(
    "key",
    [
        "queries",
        "information_needs",
        "arm",
        "ranks",
        "scores",
        "treatment_results",
        "traces",
        "acquisition_costs",
        "confirmation",
        "model_name",
        "source_mapping",
        "chronology",
    ],
)
def test_leakage_rejection(key: str) -> None:
    files, _ = build()
    packet = json.loads(files[DEST / "packet.json"])
    packet["positions"]["position_1"][key] = "excluded"
    with pytest.raises(AssertionError):
        metadata_check(packet)


@pytest.mark.parametrize(
    "identity", ["primary", "review", "Astra", "GPT-6", "stage_c_r", "chronology"]
)
def test_source_identity_rejection(identity: str) -> None:
    with pytest.raises(AssertionError):
        metadata_check({"rationale": identity})


def test_dispute_coverage_rejection(comparison: dict[str, Any]) -> None:
    files, _ = build()
    packet = json.loads(files[DEST / "packet.json"])
    resources = json.loads(gzip.decompress(files[DEST / "resources.json.gz"]))[
        "resources"
    ]
    corrupted = copy.deepcopy(packet)
    corrupted["propositions"] = [
        p for p in corrupted["propositions"] if p["kind"] != "CELL"
    ]
    with pytest.raises(AssertionError):
        validate_packet(corrupted, resources, comparison)
    resources[0]["content"] = "corrupt"
    with pytest.raises(AssertionError):
        validate_packet(packet, resources, comparison)


def test_overwrite_refusal() -> None:
    files, _ = build()
    before = {p: p.read_bytes() for p in files}
    with pytest.raises(FileExistsError):
        write_new(files)
    assert before == {p: p.read_bytes() for p in files}


def test_source_mapping_is_outside_packet() -> None:
    files, audit = build()
    assert set(audit["source_mapping"].values()) == {"position_1", "position_2"}
    packet = json.loads(files[DEST / "packet.json"])
    metadata_check(packet)
    # Digest order is neutral and independently checked.
    hashes = audit["neutral_claim_digests"]
    assert hashes["position_1"] < hashes["position_2"]
    assert not any(p.name == "packet_audit.json" for p in files)
