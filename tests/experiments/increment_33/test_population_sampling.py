# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Frozen Graph-2 population, blind sample, and exact support coverage."""

from __future__ import annotations

from experiments.increment_30.mechanics import _verified_json
from experiments.increment_33.mechanics import (
    CANDIDATES_NAME,
    ROOT,
    build_freeze,
    graph_one,
    reconstruct_path,
)
from experiments.increment_33.mechanics import FREEZE_NAME as PROTOCOL_NAME
from experiments.increment_33.population import (
    BLINDED_NAME,
    JUDGMENT_FREEZE_NAME,
    STATES,
    build_population,
)
from experiments.increment_33.sampling import (
    FREEZE_NAME,
    SAMPLED_INPUT_NAME,
    build_sample,
)
from experiments.retrieval_judgment_coverage import (
    validate_frozen_judgment_coverage,
    validate_neutral_target_coverage,
)


def test_compact_frozen_surface_exactly_reconstructs_all_novel_paths() -> None:
    assert build_freeze() == _verified_json(ROOT / PROTOCOL_NAME)
    artifact = _verified_json(ROOT / CANDIDATES_NAME)
    first = graph_one()
    reconstructed = 0
    assert len(artifact["cases"]) == len(first["cases"]) == 24
    for case, old in zip(artifact["cases"], first["cases"], strict=True):
        prefixes = {
            candidate["address"]: candidate["paths"] for candidate in old["candidates"]
        }
        assert case["frontier_count"] == len(prefixes)
        assert len({candidate["address"] for candidate in case["candidates"]}) == len(
            case["candidates"]
        )
        for candidate in case["candidates"]:
            count = 0
            for edge_id in candidate["third_edge_ids"]:
                edge = case["third_edges"][edge_id]
                assert edge["target"] == candidate["address"]
                for prefix in prefixes[edge["source"]]:
                    path = reconstruct_path(prefix, edge)
                    assert path["graph_two_candidate_resource"] == candidate["address"]
                    count += 1
            assert count == candidate["support_path_count"]
            reconstructed += count
    assert reconstructed == artifact["summary"]["novel_typed_paths"]
    assert artifact["summary"]["candidate_count"] == sum(
        case["candidate_count"] for case in artifact["cases"]
    )


def test_prior_reuse_and_neutral_population_reproduce_exactly() -> None:
    frozen, blind = build_population()
    assert frozen == _verified_json(ROOT / JUDGMENT_FREEZE_NAME)
    assert blind == _verified_json(ROOT / BLINDED_NAME)
    counts = frozen["payload"]["counts"]
    assert (
        counts["candidate_pairs"]
        == counts["exact_reused"] + counts["new_judgments_required"]
    )
    assert sum(counts["reused_states"].values()) == counts["exact_reused"]
    assert set(counts["reused_states"]) == set(STATES)
    assert not frozen["payload"]["new_usefulness_outcomes"]


def test_sample_is_reproducible_complete_and_blind() -> None:
    freeze, sampled = build_sample()
    assert freeze == _verified_json(ROOT / FREEZE_NAME)
    assert sampled == _verified_json(ROOT / SAMPLED_INPUT_NAME)
    frame = _verified_json(ROOT / BLINDED_NAME)
    expected = {
        (case["neutral_case_id"], resource["neutral_resource_id"])
        for case in frame["payload"]["cases"]
        for resource in case["resources"]
    }
    selected = {tuple(pair) for pair in freeze["payload"]["sampled_neutral_identities"]}
    unselected = {
        tuple(pair) for pair in freeze["payload"]["unsampled_neutral_identities"]
    }
    actual = {
        (case["neutral_case_id"], resource["neutral_resource_id"])
        for case in sampled["payload"]["cases"]
        for resource in case["resources"]
    }
    assert actual == selected
    assert selected.isdisjoint(unselected)
    assert selected | unselected == expected
    assert len(selected) == freeze["payload"]["sample_size"]
    assert len(expected) == freeze["payload"]["population_size"]
    for case in sampled["payload"]["cases"]:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        assert all(
            set(resource) == {"neutral_resource_id", "address", "content"}
            for resource in case["resources"]
        )


def test_three_state_exact_coverage_semantics_on_synthetic_target() -> None:
    target = {
        "neutral_case_id": "synthetic-case",
        "neutral_resource_id": "synthetic-resource",
        "information_need": {"purpose": "synthetic", "lexical_query": "synthetic"},
        "parent_snapshot_sha": "synthetic-parent",
        "address": "synthetic.py",
        "usefulness_semantics": "synthetic-semantics",
    }
    indexed = validate_neutral_target_coverage([target])
    assert len(indexed) == 1
    for state in STATES:
        decisions = [
            {**target, "judgment": state, "rationale": "synthetic test decision"}
        ]
        assert len(validate_frozen_judgment_coverage([target], decisions, STATES)) == 1
