# Copyright (c) 2026
# ruff: noqa: S101, PLR2004, FBT003, COM812 -- assertions/truth tables; formatter owns commas
"""Verify joins, ownership, alternative semantics and independent prefix accounting."""

from __future__ import annotations

import copy
import gzip
import json
from collections import Counter
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.codex_dogfood.case_0011 import execute
from experiments.codex_dogfood.case_0011.stage_d import analyze, inputs, metrics
from experiments.retrieval_diagnostics.mechanics import Mechanics

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def data() -> dict[str, Any]:
    """Load scientific inputs with native retrieval and reconfiguration forbidden."""
    patch = pytest.MonkeyPatch()

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "Native retrieval or parameter reranking prohibited"
        raise AssertionError(msg)

    patch.setattr(execute, "retrieve_repository_text_documents_by_bm25", forbidden)
    patch.setattr(Mechanics, "reconfigured", forbidden)
    try:
        return inputs.load()
    finally:
        patch.undo()


@pytest.fixture(scope="module")
def result(data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate once; tests independently audit the retained calculations."""
    return metrics.evaluate(data, data["provenance"])


def test_chain_and_join(data: dict[str, Any], result: dict[str, Any]) -> None:
    """Require every committed checkpoint and exact scientific partition."""
    assert data["provenance"]["ancestry"] == "PASSED"
    assert len(data["provenance"]["chain"]) == 8
    assert result["join_integrity"]["duplicate_missing_unexpected"] == 0
    assert data["diagnostic_replay"]["queries"] == 28
    assert data["diagnostic_replay"]["native_queries_executed"] == 0
    assert len(data["gold"]["cells"]) == 4779
    assert len(data["semantic"]["mappings"]) == 576
    assert (
        data["provenance"]["chain"][0]["artifact_sha256"][
            "experiments/codex_dogfood/case_0011/C5_PROTOCOL.md"
        ]
        != data["provenance"]["chain"][3]["artifact_sha256"][
            "experiments/codex_dogfood/case_0011/C5_PROTOCOL.md"
        ]
    )


def test_alternative_completions_independently(
    data: dict[str, Any], result: dict[str, Any]
) -> None:
    """Recompute all six global and all 12 owning-lane completions."""
    ranks = {
        q: {r["address"]: r["rank"] for r in c["rows"]}
        for q, c in data["capture"]["queries"].items()
    }
    assert len(result["arms"]["A"]["completion"]["combinations"]) == 6
    for combo in result["arms"]["A"]["completion"]["combinations"]:
        assert combo["depth"] == max(ranks["A.task"][p] for p in combo["resources"])
    for ob, row in result["arms"]["B"]["completion"]["obligations"].items():
        for alternative in row["alternatives"]:
            assert alternative["depth"] == max(
                ranks[f"B.{ob}"][p] for p in alternative["resources"]
            )
        expected = min(
            row["alternatives"], key=lambda a: (a["depth"], a["alternative"])
        )
        assert row["selected"] == expected
    assert metrics.depth({"a": {"rank": 1}}, ["a", "missing"]) is None
    assert result["arms"]["A"]["completion"]["depth"] == 370
    assert result["arms"]["C"]["completion"]["completion_depth"] is None
    assert all(
        a["completion_depth"] is None
        for aa in result["arms"]["C"]["completion"]["obligations"].values()
        for a in aa
    )


def test_prefixes_and_bytes_independently(
    data: dict[str, Any], result: dict[str, Any]
) -> None:
    """Recompute occurrence/union/label/content accounting from captured prefixes."""
    surfaces = [result["arms"][a]["completion"] for a in "AB"]
    surfaces += [
        result[k][arm]
        for k in ("strict_subset", "granularity_subset")
        for arm in ("C", "B_same_units")
    ]
    surfaces += [result["oracle"]["selected"]["burden"]]
    for b in surfaces:
        pairs = [
            (q, r["address"])
            for q, d in b["prefix_depths"].items()
            for r in data["capture"]["queries"][q]["rows"][:d]
        ]
        resources = {p for _, p in pairs}
        assert b["occurrences"] == len(pairs)
        assert b["unique_resources"] == len(resources)
        assert b["duplicates"] == sum(
            c - 1 for c in Counter(p for _, p in pairs).values()
        )
        assert b["utf8_bytes"] == sum(
            len(data["contents"][p].encode("utf-8")) for p in resources
        )
        counts = Counter(
            metrics.label(data, data["queries"][q]["obligation"], p) for q, p in pairs
        )
        assert b["occurrence_labels"] == {k: counts[k] for k in metrics.LABELS}


def test_responsible_and_collective_members(
    data: dict[str, Any], result: dict[str, Any]
) -> None:
    """Require every reviewed direct/collective member and every B gold owner."""
    for u in result["strict_subset"]["units"]:
        assert {r["need"] for r in u["responsible_routes"]} == set(
            data["coverage"][u["unit"]]["direct_needs"]
        )
        assert {r["obligation"] for r in u["B_routes"]} == set(
            data["units"][u["unit"]]["obligations"]
        )
    collective = {
        u["alias"]: u
        for u in result["granularity_subset"]["units"]
        if u["alias"] in {"U07", "U28", "U30"}
    }
    assert len(collective) == 3
    assert all(
        {r["need"].split("/")[-1] for r in u["responsible_routes"]}
        == {"binding", "items"}
        for u in collective.values()
    )
    u26 = next(u for u in result["strict_subset"]["units"] if u["alias"] == "U26")
    assert {r["query"]: r["depth"] for r in u26["B_routes"]} == {
        "B.ceiling": 2,
        "B.tests": 122,
    }
    assert result["strict_subset"]["comparison_counts"] == {
        "IMPROVEMENT": 5,
        "REGRESSION": 10,
    }
    assert result["strict_subset"]["unit_count"] == 15
    assert result["granularity_subset"]["unit_count"] == 18


def test_oracle_is_secondary_and_independent(
    data: dict[str, Any], result: dict[str, Any]
) -> None:
    """Best all-C routes cannot substitute for responsible semantic mappings."""
    for p, row in result["oracle"]["resources"].items():
        options = [
            (r["rank"], q)
            for q, c in data["capture"]["queries"].items()
            if q.startswith("C.")
            for r in c["rows"]
            if r["address"] == p
        ]
        assert (row["rank"], row["query"]) == min(options)
    assert result["oracle"]["excluded_from_U1_rule"]
    assert result["oracle"]["selected"]["max_best_resource_rank"] == 104
    for u in result["unit_failures"]:
        if u["strict_status"] != "COVERED":
            assert not u["direct_needs"]
            assert not u["responsible_retrieval"]
            assert u["any_C_resource_reach"]


@pytest.mark.parametrize(
    ("cu", "bu", "cn", "bn", "expected"),
    [
        (80, 100, 105, 100, True),
        (80, 100, 106, 100, False),
        (105, 100, 80, 100, True),
        (106, 100, 80, 100, False),
        (100, 100, 0, 0, False),
        (80, 100, 0, 0, True),
        (80, 100, 1, 0, False),
    ],
)
def test_gate_boundaries(cu: int, bu: int, cn: int, bn: int, *, expected: bool) -> None:
    """Exercise exact inclusive ratios and zero-unnecessary-baseline semantics."""
    assert metrics.exact_gate(cu, bu, cn, bn) == expected


def test_outcome_precedence_and_failures(result: dict[str, Any]) -> None:
    """Separate omitted-unit precedence, contributor counts and complete partitions."""
    gates = {"required_reach_safe": True, "coverage": True}
    assert (
        metrics.select_outcome(False, False, False, gates, True)
        == "EXPERIMENTAL_CONTRACT_DEFECT"
    )
    assert (
        metrics.select_outcome(True, True, False, gates, True)
        == "INFORMATION_NEED_AUTHORING_DEFECT"
    )
    assert (
        metrics.select_outcome(True, False, True, gates, True)
        == "INFORMATION_NEED_AUTHORING_DEFECT"
    )
    assert (
        metrics.select_outcome(True, False, False, gates, False)
        == "INFORMATION_NEED_DECOMPOSITION_SUPPORTED"
    )
    gates["coverage"] = False
    assert (
        metrics.select_outcome(True, False, False, gates, True)
        == "COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER"
    )
    assert (
        metrics.select_outcome(True, False, False, gates, False) == "NO_MATERIAL_VALUE"
    )
    assert sum(result["failure_class_totals"].values()) == 32
    assert len({u["unit"] for u in result["unit_failures"]}) == 32
    assert result["outcome"] in result["decision_rule"]["outcomes"]
    assert result["SEARCH_POLICY_FAILURE"] == "NOT_ASSESSED"
    for unit in result["unit_failures"]:
        if unit["earliest_failure"] == "RETRIEVAL_RANKING_DISCRIMINATION_FAILURE":
            assert unit["ranking_noise_count"] >= unit["ranking_diagnostic_threshold"]
        elif unit["earliest_failure"] == "NO_ACQUISITION_FAILURE":
            assert unit["ranking_noise_count"] < unit["ranking_diagnostic_threshold"]
    assert len(result["required_resource_failure_records"]) == 16


@pytest.mark.parametrize(
    "kind", ["query", "count", "rank", "identity", "score", "duplicate"]
)
def test_capture_tamper_rejection(data: dict[str, Any], kind: str) -> None:
    """Reject scientific identity, execution and contribution corruption."""
    capture = copy.deepcopy(data["capture"])
    c = capture["queries"]["A.task"]
    if kind == "query":
        c["query_text"] += "tamper"
    elif kind == "count":
        c["execution_count"] = 2
    elif kind == "rank":
        c["rows"][0]["rank"] = 999
    elif kind == "identity":
        c["rows"][0]["content_identity"] = "foreign"
    elif kind == "score":
        c["rows"][0]["content_terms"][0]["contribution"] += 1
    else:
        c["rows"].append(c["rows"][0])
    identities = {
        r["address"]: r["content_identity"] for r in data["gold"]["resources"]
    }
    with pytest.raises(ValueError, match=r"differ|coverage|Duplicate"):
        inputs.validate_queries(data["queries"], capture, data["contents"], identities)


def test_artifact_correspondence_and_overwrite(
    data: dict[str, Any], tmp_path: Path
) -> None:
    """Require deterministic byte correspondence and no partial overwrite."""
    files = analyze.artifacts(data)
    assert files == analyze.artifacts(data)
    d, trace = json.loads(files["analysis.json"]), json.loads(files["trace.json"])
    r15_ref = d["diagnostics"]["R1.5_reconstructed_explanations"]
    assert digest(files[r15_ref["artifact"]]) == r15_ref["archive_sha256"]
    r15_payload = gzip.decompress(files[r15_ref["artifact"]])
    assert digest(r15_payload) == r15_ref["canonical_payload_sha256"]
    assert r15_payload == json_bytes(data["r15_explanations"])
    assert trace["final_outcome"] == d["outcome"]
    assert len(trace["reviewed_need_unit_mappings"]) == 576
    assert trace["reviewed_need_unit_mappings"] == data["semantic"]["mappings"]
    for q in trace["queries"]:
        assert (
            q["captured_query_text"]
            == data["capture"]["queries"][q["identity"]]["query_text"]
        )
        assert [
            {k: v for k, v in r.items() if k != "reviewed_label"}
            for r in q["ranked_results"]
        ] == data["capture"]["queries"][q["identity"]]["rows"]
    assert all(
        q["identity"] in files["STAGE_D_REVIEW.md"].decode() for q in trace["queries"]
    )
    ledger = json.loads(files["integrity.json"])
    assert all(digest(files[n]) == sha for n, sha in ledger["sha256"].items())
    assert not any(n.startswith(".local/") for n in ledger["sha256"])
    analyze.publish(files, tmp_path)
    analyze.validate(files, tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    with pytest.raises(FileExistsError, match="overwrite refused"):
        analyze.publish(files, tmp_path)
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    (tmp_path / "analysis.json").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="published replay differs"):
        analyze.validate(files, tmp_path)
    partial = tmp_path / "partial"
    partial.mkdir()
    (partial / "trace.json").write_bytes(b"existing")
    with pytest.raises(FileExistsError):
        analyze.publish(files, partial)
    assert not (partial / "analysis.json").exists()


def test_bad_identity_coverage() -> None:
    """Duplicate, missing and unexpected identities are separate rejected joins."""
    for observed in ((1, 1), (1,), (1, 3)):
        with pytest.raises(ValueError, match="Identity coverage"):
            inputs.exact((1, 2), observed)
