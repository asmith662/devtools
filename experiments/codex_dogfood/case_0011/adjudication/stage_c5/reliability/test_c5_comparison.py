"""Scientific comparison, packet completeness and negative integrity checks."""

from __future__ import annotations

import copy
import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packet as packet_builder
import compare_c5 as comparison
import validate_packet as packet_validator


@pytest.fixture(scope="module")
def data() -> dict[str, Any]:
    return comparison.load()


@pytest.fixture(scope="module")
def result(data: dict[str, Any]) -> dict[str, Any]:
    return comparison.build(data)


def test_exact_frame(data: dict[str, Any], result: dict[str, Any]) -> None:
    assert data["review"]["frozen_packet"] == data["packet"]
    assert result["frame_alignment"]["pairs"] == 576
    assert data["manifest"]["mapping_count"] == 576
    assert data["manifest"]["required_unit_count"] == 32
    assert data["manifest"]["need_count"] == 18
    for field in ("duplicate_pairs", "missing_pairs", "unexpected_pairs"):
        assert result["frame_alignment"][field] == 0


def test_duplicate_pair_rejected(data: dict[str, Any]) -> None:
    rows = list(data["p"].values())
    with pytest.raises(AssertionError, match="duplicate"):
        comparison.pair_index([*rows, rows[0]])


def test_pair_partition(result: dict[str, Any]) -> None:
    matrix = result["pair_comparison"]["matrix"]
    assert matrix == [[12, 1, 0, 0], [9, 34, 16, 0], [0, 6, 498, 0], [0, 0, 0, 0]]
    assert sum(map(sum, matrix)) == 576
    assert result["pair_comparison"]["agreement_count"] == 544
    assert len(result["pair_disagreements"]) == 32
    assert [sum(row) for row in matrix] == [13, 59, 504, 0]
    assert [sum(row[i] for row in matrix) for i in range(4)] == [21, 41, 514, 0]


def test_direct_partition(result: dict[str, Any]) -> None:
    direct = result["per_label"]["DIRECTLY_COVERS"]
    assert (direct["intersection"], direct["union"]) == (12, 22)
    assert direct["jaccard"] == 12 / 22
    assert direct["primary_retained_by_review"] == 12 / 13
    assert direct["review_retained_by_primary"] == 12 / 21
    assert len(direct["primary_only"]) == 1 and len(direct["review_only"]) == 9
    assert len(result["agreed_direct_rationale_comparisons"]) == 12


def test_partial_and_noncoverage_partition(result: dict[str, Any]) -> None:
    partial = result["per_label"]["PARTIALLY_COVERS"]
    assert (partial["intersection"], partial["union"]) == (34, 66)
    assert (len(partial["primary_only"]), len(partial["review_only"])) == (25, 7)
    noncoverage = result["per_label"]["DOES_NOT_COVER"]
    assert (noncoverage["intersection"], noncoverage["union"]) == (498, 520)
    assert (len(noncoverage["primary_only"]), len(noncoverage["review_only"])) == (
        6,
        16,
    )


def test_unit_coverage_and_uncovered_resolution(result: dict[str, Any]) -> None:
    assert result["unit_comparison"]["matrix"] == [
        [12, 1, 0, 0],
        [8, 9, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 0],
    ]
    assert result["unit_comparison"]["agreement_count"] == 21
    uncovered = [u for u in result["units"] if u["primary"]["status"] == "UNCOVERED"]
    assert len(uncovered) == 2
    assert all(u["review"]["status"] == "PARTIAL_ONLY" for u in uncovered)


def test_need_classifications(result: dict[str, Any]) -> None:
    assert result["need_comparison"]["matrix"] == [
        [8, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [5, 1, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    assert result["need_comparison"]["agreement_count"] == 11
    for source, label, unique in (
        ("primary", "classification", "unique_units"),
        ("review", "label", "uniquely_direct_units"),
    ):
        for need in result["needs"]:
            claim = need[source]
            if claim[label] == "NECESSARY":
                assert claim[unique]
            elif claim[label] == "USEFUL_REDUNDANT":
                assert claim["direct_units"] and not claim[unique]
            elif claim[label] == "PARTIAL_ONLY":
                assert not claim["direct_units"]


def test_alternative_membership_and_completeness(result: dict[str, Any]) -> None:
    assert result["alternative_direct_comparison"]["matrix"] == [[0, 0], [6, 6]]
    counts = Counter(a["review"]["status"] for a in result["alternatives"])
    assert counts == {
        "FULLY_DIRECTLY_COVERED": 6,
        "FULLY_COVERED_ONLY_COLLECTIVELY": 2,
        "INCOMPLETE": 4,
    }
    assert all(
        set(a["primary_missing_direct_members"]) <= set(a["units"])
        for a in result["alternatives"]
    )
    assert all(
        set(a["review_missing_direct_members"]) <= set(a["units"])
        for a in result["alternatives"]
    )


def test_granularity_and_collective_structure(result: dict[str, Any]) -> None:
    assert list(result["granularity_counts"].values()) == [23, 6, 3, 0]
    assert len(result["collective"]) == 6
    assert sum(len(row["sets"]) for row in result["collective"]) == 7
    for row in result["collective"]:
        assert row["strict_status"] == "PARTIAL_ONLY"
        assert all(len(s["needs"]) == 2 for s in row["sets"])
        for s in row["sets"]:
            assert {m["need"] for m in s["member_necessity"]} == set(s["needs"])
            assert all(
                m["covered_part"] and m["missing_without_others"]
                for m in s["member_necessity"]
            )
    assert result["coverage"]["primary_strict_direct"] == 13
    assert result["coverage"]["review_strict_direct"] == 20
    assert result["coverage"]["review_granularity_aware"] == 26
    assert not result["coverage"]["frozen_direct_rule_passes_review"]


def test_deterministic_replay_and_manual_surface(
    data: dict[str, Any], result: dict[str, Any]
) -> None:
    assert comparison.encode(comparison.build()) == comparison.encode(result)
    review = comparison.render(result, data)
    assert review == comparison.render(comparison.build(), comparison.load())
    for row in result["pair_disagreements"]:
        assert row["primary"]["rationale"] in review
        assert row["review"]["rationale"] in review
    for row in result["needs"]:
        if row["primary"]["classification"] != row["review"]["label"]:
            assert (
                row["primary"]["rationale"] in review
                and row["review"]["rationale"] in review
            )


def test_full_disagreement_and_audit_coverage(
    data: dict[str, Any], result: dict[str, Any]
) -> None:
    packet, audit = comparison.neutral_packet(data, result)
    props = packet["propositions"]
    assert Counter(p["kind"] for p in props) == {
        "PAIR_LABEL": 32,
        "DIRECT_RATIONALE": 12,
        "UNIT_STATUS": 11,
        "NEED_CLASSIFICATION": 7,
        "ALTERNATIVE_COMPLETENESS": 10,
        "UNIT_GRANULARITY": 32,
        "COLLECTIVE_COVERAGE": 6,
    }
    assert {
        (p["subject"]["need"], p["subject"]["unit"])
        for p in props
        if p["kind"] == "PAIR_LABEL"
    } == {
        (n, u)
        for (n, u) in data["p"]
        if data["p"][n, u]["label"] != data["r"][n, u]["label"]
    }
    assert {p["subject"]["unit"] for p in props if p["kind"] == "UNIT_STATUS"} == {
        u for u in data["us"] if data["pu"][u]["status"] != data["ru"][u]["status"]
    }
    assert {
        p["subject"]["need"] for p in props if p["kind"] == "NEED_CLASSIFICATION"
    } == {
        n
        for n in data["ns"]
        if data["pn"][n]["classification"] != data["rn"][n]["label"]
    }
    assert {
        p["subject"]["unit"] for p in props if p["kind"] == "UNIT_GRANULARITY"
    } == set(data["us"])
    assert {
        p["subject"]["unit"] for p in props if p["kind"] == "COLLECTIVE_COVERAGE"
    } == set(data["collective"])
    assert {
        p["subject"]["alternative"]
        for p in props
        if p["kind"] == "ALTERNATIVE_COMPLETENESS"
    } == {
        row["identity"]
        for row in result["alternatives"]
        if row["primary_missing_direct_members"] != row["review_missing_direct_members"]
        or row["review"]["status"] == "FULLY_COVERED_ONLY_COLLECTIVELY"
    }
    assert {p["identity"] for p in audit["propositions"]} == {
        p["identity"] for p in props
    }
    packet_validator.check_payload(packet)
    assert "primary" not in packet["position_order"]
    for prop, source in zip(props, audit["propositions"], strict=True):
        assert prop["identity"] == source["identity"]
        assert set(prop["positions"]) == set(source["sources"])
        values = list(prop["positions"].values())
        assert [comparison.digest(comparison.encode(v)) for v in values] == sorted(
            comparison.digest(comparison.encode(v)) for v in values
        )


def test_packet_double_build(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    assert packet_builder.write(first) == packet_builder.write(second)
    assert {p.name: p.read_bytes() for p in first.iterdir()} == {
        p.name: p.read_bytes() for p in second.iterdir()
    }
    with pytest.raises(AssertionError, match="OVERWRITE_REFUSED"):
        packet_builder.write(first)


def test_overwrite_refusal(tmp_path: Path) -> None:
    target = tmp_path / "artifact"
    comparison.exclusive(target, b"frozen")
    with pytest.raises(FileExistsError):
        comparison.exclusive(target, b"changed")
    assert target.read_bytes() == b"frozen"


@pytest.mark.parametrize("key", sorted(packet_validator.DENIED))
def test_leakage_rejection(key: str) -> None:
    with pytest.raises(AssertionError):
        packet_validator.check_leakage({key: "injected"})


@pytest.mark.parametrize(
    "value",
    [
        "primary reviewer",
        "independent reviewer",
        "GPT-6",
        "Astra",
        "before source inspection",
        "C:\\secret\\answer",
        "https://example.invalid/results",
    ],
)
def test_source_and_chronology_rejection(value: str) -> None:
    with pytest.raises(AssertionError):
        packet_validator.check_leakage({"rationale": value})


def test_position_order_rejection(data: dict[str, Any], result: dict[str, Any]) -> None:
    packet, _ = comparison.neutral_packet(data, result)
    changed = copy.deepcopy(packet)
    row = next(p for p in changed["propositions"] if len(p["positions"]) == 2)
    row["positions"]["position_1"], row["positions"]["position_2"] = (
        row["positions"]["position_2"],
        row["positions"]["position_1"],
    )
    with pytest.raises(AssertionError, match="non-neutral"):
        packet_validator.check_payload(changed)


def test_whitelist_and_integrity_rejection(tmp_path: Path) -> None:
    root = tmp_path / "packet"
    packet_builder.write(root)
    (root / ".local").mkdir()
    (root / ".local/codex-result.md").write_text("Operational only; never evidence.")
    assert packet_validator.validate(root)["status"] == "PASS"
    (root / "unexpected.txt").write_text("unexpected")
    with pytest.raises(AssertionError, match="whitelist"):
        packet_validator.validate(root)
    (root / "unexpected.txt").unlink()
    (root / "INSTRUCTIONS.md").write_bytes(b"modified")
    with pytest.raises(AssertionError, match="file hash"):
        packet_validator.validate(root)


def test_packet_payload_bindings() -> None:
    files, _ = packet_builder.payloads()
    payload = gzip.decompress(files["packet.json.gz"])
    manifest = json.loads(files["manifest.json"])
    assert comparison.digest(payload) == manifest["canonical_payload_sha256"]
    assert json.loads(payload)["bindings"] == manifest["bindings"]


def test_frozen_repository_artifacts(
    data: dict[str, Any], result: dict[str, Any]
) -> None:
    root = comparison.ROOT
    assert (root / "c5_reliability_comparison.json").read_bytes() == comparison.encode(
        result
    )
    assert (root / "C5_RELIABILITY_REVIEW.md").read_bytes() == comparison.render(
        result, data
    ).encode()
    files, audit = packet_builder.payloads()
    assert (root / "source_audit.json").read_bytes() == comparison.encode(audit)
    packet_root = root.parent / "reconciliation/packet"
    assert {name: (packet_root / name).read_bytes() for name in files} == files
