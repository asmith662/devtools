# Copyright (c) 2026
# ruff: noqa: ARG001, D103, EM101, PLR2004, S607, S603, TRY003
"""Tests for the frozen Increment-27 top-five blinded judgment population."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, cast

from experiments.increment_25 import development as i25_development
from experiments.increment_27.depth_diagnostic import _read_json, canonical_json_bytes
from experiments.increment_27.lexical_top5_judgment_pool import (
    EXPECTED_NEW_SIZE,
    EXPECTED_POOL_SIZE,
    EXPECTED_REUSED_SIZE,
    METHODS,
    build_top5_artifacts,
)
from experiments.increment_27.phase1_population import _resource_contents

if TYPE_CHECKING:
    import pytest

ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS = ROOT / "experiments"
I27 = EXPERIMENTS / "increment_27"


def _artifacts() -> dict[str, dict[str, object]]:
    return build_top5_artifacts(experiment_root=EXPERIMENTS)


def test_union_and_diagnostics_use_exact_saved_top_five_rankings() -> None:
    artifacts = _artifacts()
    pool_artifact = artifacts["lexical_top5_pooled_pairs.json"]
    pool = cast("dict[str, object]", pool_artifact["payload"])
    phase0 = _read_json(I27 / "experiment_freeze.json")
    comparison = _read_json(I27 / "lexical_comparison_freeze.json")
    rankings = _read_json(I27 / "lexical_comparison_rankings.json")
    comparison_payload = cast("dict[str, object]", comparison["payload"])
    heldout = set(cast("list[str]", comparison_payload["heldout_case_ids_sealed"]))
    dev_ids = set(cast("list[str]", comparison_payload["development_case_ids"]))
    assert len(dev_ids) == 24
    assert pool["comparison_configuration_identity"] == comparison["content_identity"]
    assert pool["lexical_ranking_identity"] == rankings["content_identity"]
    ranking_cases = cast("list[dict[str, object]]", rankings["cases"])
    assert len(ranking_cases) == 24
    methods = cast("list[dict[str, object]]", comparison_payload["methods"])
    assert [m["id"] for m in methods] == list(METHODS)
    pairs = cast("list[dict[str, object]]", pool["pairs"])
    assert len(pairs) == EXPECTED_POOL_SIZE
    assert {str(row["case_id"]) for row in pairs} == dev_ids
    assert not {str(row["case_id"]) for row in pairs} & heldout
    expected: dict[tuple[str, str], dict[str, int]] = {}
    for case in ranking_cases:
        case_rankings = cast("dict[str, list[dict[str, object]]]", case["rankings"])
        for method in METHODS:
            rows = case_rankings[method][:5]
            for row in rows:
                expected.setdefault(
                    (str(case["case_id"]), str(row["address"])),
                    {},
                )[method] = cast(
                    "int",
                    row["rank"],
                )
    actual = {
        (str(row["case_id"]), str(row["address"])): row["method_ranks"] for row in pairs
    }
    assert actual == expected
    occurrence_counts = {
        str(n): sum(len(ranks) == n for ranks in expected.values())
        for n in range(1, len(METHODS) + 1)
    }
    assert pool["method_membership_distribution"] == occurrence_counts
    assert occurrence_counts == {"1": 51, "2": 33, "3": 27, "4": 70, "5": 10}
    assert pool["per_method_occurrences"] == {
        "canonical": 120,
        "bm25_plus": 120,
        "identifier": 120,
        "path": 48,
        "rrf": 120,
    }
    expected_overlap = {
        "canonical x bm25_plus": 118,
        "canonical x identifier": 92,
        "canonical x path": 11,
        "canonical x rrf": 93,
        "bm25_plus x identifier": 91,
        "bm25_plus x path": 11,
        "bm25_plus x rrf": 92,
        "identifier x path": 13,
        "identifier x rrf": 94,
        "path x rrf": 19,
    }
    assert pool["pairwise_method_overlap"] == expected_overlap
    assert pool["method_exclusive_counts"] == {
        "canonical": 0,
        "bm25_plus": 1,
        "identifier": 14,
        "path": 28,
        "rrf": 8,
    }
    assert (
        phase0["content_identity"]
        == "758f338af25a5f88fa66229d5ed29f1065a244f4116e0ac843e169114624254c"
    )


def test_exact_reuse_sources_and_three_state_counts() -> None:
    artifacts = _artifacts()
    freeze = cast(
        "dict[str, object]",
        artifacts["lexical_top5_judgment_freeze.json"]["payload"],
    )
    reuse = cast(
        "dict[str, object]",
        artifacts["lexical_top5_reused_judgments.json"]["payload"],
    )
    pool = cast(
        "dict[str, object]",
        artifacts["lexical_top5_pooled_pairs.json"]["payload"],
    )
    records = cast("list[dict[str, object]]", reuse["records"])
    assert len(records) == EXPECTED_REUSED_SIZE
    assert freeze["reused_judgment_count"] == EXPECTED_REUSED_SIZE
    assert freeze["new_judgment_count"] == EXPECTED_NEW_SIZE
    assert freeze["pooled_pair_count"] == EXPECTED_POOL_SIZE
    assert reuse["state_counts"] == {"useful": 28, "not-useful": 29, "unjudged": 1}
    pairs = cast("list[dict[str, object]]", pool["pairs"])
    pooled_ids = {(row["case_id"], row["address"]) for row in pairs}
    reused_ids = {(row["case_id"], row["address"]) for row in records}
    assert reused_ids <= pooled_ids
    assert len(reused_ids) == EXPECTED_REUSED_SIZE
    assert all(len(str(row["source_judgment_identity"])) == 64 for row in records)
    assert all(row["source_artifact_sha256"] for row in records)
    assert all(
        row["judgment_semantics"] == "purpose-relative-three-state-v1"
        for row in records
    )
    assert sum(row["judgment"] == "unjudged" for row in records) == 1


def test_blinded_input_has_only_new_pairs_and_neutral_fields() -> None:
    artifacts = _artifacts()
    freeze = cast(
        "dict[str, object]",
        artifacts["lexical_top5_judgment_freeze.json"]["payload"],
    )
    blinded = cast(
        "dict[str, object]",
        artifacts["lexical_top5_blinded_judgment_input.json"]["payload"],
    )
    new_pairs = cast("list[dict[str, object]]", freeze["new_judgment_pairs"])
    assert len(new_pairs) == EXPECTED_NEW_SIZE
    assert set(blinded) == {"schema", "cases"}
    forbidden = {
        "case_id",
        "method",
        "methods",
        "method_ranks",
        "method_membership",
        "exclusive",
        "overlap",
        "rank",
        "score",
        "component_scores",
        "matched_terms",
        "identifier_evidence",
        "path_evidence",
        "rrf_evidence",
        "structural_origin",
        "semantic_origin",
        "changed_paths",
        "task_commit_diff",
        "post_change_content",
        "judgment",
        "usefulness",
    }
    cases = cast("list[dict[str, object]]", blinded["cases"])
    assert len(cases) == 24
    blind_count = 0
    for case in cases:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        assert set(cast("dict[str, object]", case["information_need"])) == {
            "purpose",
            "lexical_query",
        }
        assert not forbidden.intersection(case)
        resources = cast("list[dict[str, object]]", case["resources"])
        assert resources == sorted(
            resources,
            key=lambda row: str(row["neutral_resource_id"]),
        )
        for resource in resources:
            assert set(resource) == {"neutral_resource_id", "address", "content"}
            assert not forbidden.intersection(resource)
            blind_count += 1
    assert blind_count == EXPECTED_NEW_SIZE
    assert not any(
        forbidden.intersection(resource)
        for case in cases
        for resource in cast("list[dict[str, object]]", case["resources"])
    )


def test_parent_snapshot_content_and_sealed_case_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_materialization(*args: object, **kwargs: object) -> None:
        raise AssertionError("Top-five pool must not materialize a retrieval snapshot.")

    monkeypatch.setattr(
        i25_development,
        "_materialize_git_snapshot",
        forbidden_materialization,
    )
    artifacts = _artifacts()
    blinded = cast(
        "dict[str, object]",
        artifacts["lexical_top5_blinded_judgment_input.json"]["payload"],
    )
    phase0 = _read_json(I27 / "experiment_freeze.json")
    phase0_payload = cast("dict[str, object]", phase0["payload"])
    confirmation = cast(
        "dict[str, object]",
        phase0_payload["increment_27_confirmation"],
    )
    heldout = set(cast("list[str]", confirmation["case_ids"]))
    pool = cast(
        "dict[str, object]",
        artifacts["lexical_top5_pooled_pairs.json"]["payload"],
    )
    pool_pairs = cast("list[dict[str, object]]", pool["pairs"])
    assert not {str(row["case_id"]) for row in pool_pairs} & heldout
    freeze = cast(
        "dict[str, object]",
        artifacts["lexical_top5_judgment_freeze.json"]["payload"],
    )
    new_pairs = cast("list[dict[str, object]]", freeze["new_judgment_pairs"])
    comparison = _read_json(I27 / "lexical_comparison_freeze.json")
    blind_cases = cast("list[dict[str, object]]", blinded["cases"])
    blind_pair_ids = {
        (str(case["neutral_case_id"]), str(resource["address"]))
        for case in blind_cases
        for resource in cast("list[dict[str, object]]", case["resources"])
    }
    expected_blind_pair_ids = {
        (
            "case-"
            + hashlib.sha256(
                f"{comparison['content_identity']}|{row['case_id']}".encode(),
            ).hexdigest()[:16],
            str(row["address"]),
        )
        for row in new_pairs
    }
    assert blind_pair_ids == expected_blind_pair_ids
    parent_pairs = [
        (str(case["parent_snapshot_sha"]), str(resource["address"]))
        for case in blind_cases
        for resource in cast("list[dict[str, object]]", case["resources"])
    ]
    contents = _resource_contents(parent_pairs)
    for case in blind_cases:
        for resource in cast("list[dict[str, object]]", case["resources"]):
            key = (str(case["parent_snapshot_sha"]), str(resource["address"]))
            assert resource["content"] == contents[key]
    for parent, address in (
        parent_pairs[0],
        parent_pairs[len(parent_pairs) // 2],
        parent_pairs[-1],
    ):
        expected = subprocess.run(
            ["git", "show", f"{parent}:{address}"],
            check=True,
            capture_output=True,
        ).stdout.decode("utf-8")
        assert contents[(parent, address)] == expected


def test_freeze_identities_are_deterministic_and_phase1_is_untouched() -> None:
    before = {
        name: (I27 / name).read_bytes()
        for name in (
            "phase1_population_freeze.json",
            "phase1_pooled_pairs.json",
            "phase1_reused_judgments.json",
            "phase1_blinded_judgment_input.json",
        )
    }
    first = _artifacts()
    second = _artifacts()
    assert first == second
    freeze = first["lexical_top5_judgment_freeze.json"]
    freeze_payload = cast("dict[str, object]", freeze["payload"])
    assert (
        freeze["content_identity"]
        == hashlib.sha256(canonical_json_bytes(freeze_payload)).hexdigest()
    )
    assert freeze_payload["pooled_population_identity"]
    assert freeze_payload["reused_judgment_mapping_identity"]
    assert freeze_payload["new_blinded_population_identity"]
    assert freeze_payload["new_usefulness_outcomes"] is False
    assert freeze_payload["phase1_deep_pool_status"] == (
        "preserved frozen population; adjudication suspended"
    )
    assert before == {name: (I27 / name).read_bytes() for name in before}
