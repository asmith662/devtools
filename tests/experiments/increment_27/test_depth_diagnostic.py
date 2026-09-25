# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Tests for Increment-27 freeze and existing-judgment depth accounting."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import cast

import pytest

from experiments.increment_25.development import _task_card
from experiments.increment_27.depth_diagnostic import (
    K_CHECKPOINTS,
    build_depth_case,
    build_freeze,
    build_summary,
    canonical_json_bytes,
    load_existing_judgments,
    prior_judgment_matches,
)

ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS = ROOT / "experiments"


def test_freeze_partitions_24_development_and_14_sealed_confirmation() -> None:
    freeze = build_freeze(experiment_root=EXPERIMENTS)
    freeze_payload = cast("dict[str, object]", freeze["payload"])
    population = cast("dict[str, object]", freeze_payload["source_population"])
    development_cases = cast("list[dict[str, object]]", population["development_cases"])
    source_partition = cast(
        "dict[str, object]", population["increment_25_source_partition"]
    )
    heldout_ids = cast(
        "list[str]", source_partition["increment_27_heldout_confirmation_case_ids"]
    )
    assert len(development_cases) == 24
    assert len(heldout_ids) == 14
    heldout = cast("dict[str, object]", freeze_payload["increment_27_confirmation"])
    heldout_status = str(heldout["status"])
    assert heldout_status.startswith("sealed")
    assert "retrieval" in heldout_status
    protocol = cast("dict[str, object]", freeze_payload["canonical_retrieval"])
    assert protocol["combination"] == "content BM25 + 0.25 * filename-stem BM25"
    assert protocol["identity"] == (
        "devtools.context.retrieval.lexical.retrieve_repository_text_documents_by_bm25"
    )
    boundary = cast("dict[str, object]", freeze_payload["protocol_boundary"])
    assert boundary["heldout_confirmation_execution"] is False
    assert boundary["top_50_neutral_judgment_pool"] is False
    suspended = cast(
        "dict[str, object]",
        freeze_payload["preserved_suspended_increment_26_confirmation"],
    )
    assert str(suspended["status"]).startswith("preserved-suspended")


def test_freeze_records_frozen_parent_snapshots_and_queries_without_outcomes() -> None:
    freeze = build_freeze(experiment_root=EXPERIMENTS)
    freeze_payload = cast("dict[str, object]", freeze["payload"])
    population = cast("dict[str, object]", freeze_payload["source_population"])
    for case in cast("list[dict[str, object]]", population["development_cases"]):
        assert len(str(case["parent_snapshot_sha"])) == 40
        need = cast("dict[str, object]", case["information_need"])
        assert need["lexical_query"]
    heldout = cast("dict[str, object]", freeze_payload["increment_27_confirmation"])
    heldout_cards = cast("list[dict[str, object]]", heldout["cards"])
    assert all("positive_lexical_ordering" not in case for case in heldout_cards)
    assert all("results" not in case for case in heldout_cards)


def test_existing_judgments_are_joined_with_three_states_and_exact_identity() -> None:
    freeze_payload = json.loads(
        (EXPERIMENTS / "increment_25/task_population_freeze.json").read_text(
            encoding="utf-8"
        )
    )["payload"]
    cards = {
        _task_card(item).case_id: _task_card(item)
        for item in freeze_payload["task_cards"]
    }
    selected = {
        case_id: cards[case_id]
        for case_id in (
            *freeze_payload["split"]["development_case_ids"],
            *freeze_payload["split"]["confirmation_case_ids"],
        )
    }
    judgments = load_existing_judgments(experiment_root=EXPERIMENTS, cards=selected)
    assert sum(map(len, judgments.values())) == 120
    states = {
        str(item["judgment"]) for records in judgments.values() for item in records
    }
    assert states <= {"useful", "not-useful", "unjudged"}
    assert Counter(
        str(item["judgment"]) for records in judgments.values() for item in records
    ) == {"useful": 49, "not-useful": 69, "unjudged": 2}
    assert all(
        item["judgment_semantics"] == "purpose-relative-three-state-v1"
        for records in judgments.values()
        for item in records
    )


def test_depth_checkpoints_keep_unjudged_and_missing_positive_rank_explicit() -> None:
    case = build_depth_case(
        case_id="fixture",
        parent_snapshot_sha="a" * 40,
        query_text="frozen query",
        rankings=[
            {"rank": 1, "address": "a.py", "score": 2.0},
            {"rank": 2, "address": "b.py", "score": 1.0},
        ],
        judgments=[
            {"address": "a.py", "judgment": "useful"},
            {"address": "b.py", "judgment": "unjudged"},
            {"address": "missing.py", "judgment": "useful"},
        ],
    )
    case_checkpoints = cast(
        "list[dict[str, object]]", case["known_useful_reached_by_k"]
    )
    assert [item["requested_k"] for item in case_checkpoints] == list(K_CHECKPOINTS)
    assert [item["effective_k"] for item in case_checkpoints] == [
        1,
        2,
        2,
        2,
        2,
        2,
    ]
    judged_resources = cast("list[dict[str, object]]", case["judged_resources"])
    by_address = {str(item["address"]): item for item in judged_resources}
    assert (
        by_address["missing.py"]["positive_rank_state"]
        == "absent-from-positive-results"
    )
    assert by_address["b.py"]["judgment"] == "unjudged"
    assert case["known_useful_without_positive_rank"] == ["missing.py"]
    assert case["unjudged_identities"] == ["b.py"]


def test_unknown_judgment_state_is_rejected_instead_of_treated_as_negative() -> None:
    with pytest.raises(ValueError, match="Unknown three-state"):
        build_depth_case(
            case_id="fixture",
            parent_snapshot_sha="a" * 40,
            query_text="query",
            rankings=[],
            judgments=[{"address": "a.py", "judgment": "unknown"}],
        )


def test_positive_ranking_requires_complete_contiguous_ordering() -> None:
    with pytest.raises(ValueError, match="contiguous complete ranks"):
        build_depth_case(
            case_id="fixture",
            parent_snapshot_sha="a" * 40,
            query_text="query",
            rankings=[{"rank": 2, "address": "a.py", "score": 1.0}],
            judgments=[],
        )


def test_summary_uses_judged_pool_language_and_exact_buckets() -> None:
    cases = [
        {
            "judged_resources": [{"judgment": "useful", "positive_lexical_rank": 4}],
            "first_known_useful_rank": 4,
        },
        {
            "judged_resources": [{"judgment": "useful", "positive_lexical_rank": 51}],
            "first_known_useful_rank": 51,
        },
        {
            "judged_resources": [{"judgment": "useful", "positive_lexical_rank": None}],
            "first_known_useful_rank": None,
        },
        {"judged_resources": [], "first_known_useful_rank": None},
    ]
    summary = build_summary(cases=cast("list[dict[str, object]]", cases))
    checkpoints = cast("list[dict[str, object]]", summary["known_useful_reached_by_k"])
    assert checkpoints[0] == {
        "k": 1,
        "known_useful_reached": 0,
        "total_known_useful": 3,
    }
    assert summary["known_useful_beyond_50"] == 1
    assert summary["known_useful_unreachable_by_positive_lexical_retrieval"] == 1
    assert summary["cases_with_no_known_useful_resource"] == 1
    assert "not exhaustive" in str(summary["metric_caveat"])


def test_serialization_is_deterministic() -> None:
    value = {"z": [2, 1], "a": "é"}
    assert canonical_json_bytes(value) == canonical_json_bytes({"a": "é", "z": [2, 1]})


def test_prior_judgment_requires_exact_need_snapshot_address_and_semantics() -> None:
    card = _task_card(
        {
            "case_id": "case",
            "source_commit_sha": "b" * 40,
            "parent_snapshot_sha": "a" * 40,
            "original_subject": "subject",
            "original_body": "",
            "information_need_purpose": "purpose",
            "lexical_query": "query",
            "maintenance_category": "feature",
            "repository_domain": "context",
            "corpus_source_roots": ["src", "tests"],
            "evaluator_only_changed_paths": [],
        }
    )
    matching = {
        "purpose": "purpose",
        "lexical_query": "query",
        "parent_snapshot_sha": "a" * 40,
        "address": "src/module.py",
        "semantics": "purpose-relative-three-state-v1",
    }
    assert prior_judgment_matches(
        card=card,
        prior_information_need=matching,
        prior_parent_snapshot=matching["parent_snapshot_sha"],
        prior_address=matching["address"],
        resource_address=matching["address"],
        prior_usefulness_semantics=matching["semantics"],
    )
    for field, changed in (
        ("purpose", "different purpose"),
        ("lexical_query", "different query"),
    ):
        candidate = {**matching, field: changed}
        assert not prior_judgment_matches(
            card=card,
            prior_information_need=candidate,
            prior_parent_snapshot=matching["parent_snapshot_sha"],
            prior_address=matching["address"],
            resource_address=matching["address"],
            prior_usefulness_semantics=matching["semantics"],
        )
    assert not prior_judgment_matches(
        card=card,
        prior_information_need=matching,
        prior_parent_snapshot="c" * 40,
        prior_address=matching["address"],
        resource_address=matching["address"],
        prior_usefulness_semantics=matching["semantics"],
    )
    assert not prior_judgment_matches(
        card=card,
        prior_information_need=matching,
        prior_parent_snapshot=matching["parent_snapshot_sha"],
        prior_address=matching["address"],
        resource_address=matching["address"],
        prior_usefulness_semantics="different-semantics",
    )
    assert not prior_judgment_matches(
        card=card,
        prior_information_need=matching,
        prior_parent_snapshot=matching["parent_snapshot_sha"],
        prior_address="src/other.py",
        resource_address=matching["address"],
        prior_usefulness_semantics=matching["semantics"],
    )


def test_saved_rankings_are_complete_positive_order_and_exclude_heldout() -> None:
    ranking_path = (
        ROOT / "experiments/increment_27/canonical_positive_lexical_rankings.json"
    )
    assert ranking_path.is_file()
    artifact = json.loads(ranking_path.read_text(encoding="utf-8"))
    assert len(artifact["cases"]) == 24
    assert artifact["prior_rank_agreement"]["status"] == (
        "all retained ranks and available scores agree"
    )
    assert artifact["prior_rank_agreement"]["retained_resource_rank_checks"] > 0
    for case in artifact["cases"]:
        items = case["positive_lexical_ordering"]
        assert [item["rank"] for item in items] == list(range(1, len(items) + 1))
        assert all(item["score"] > 0 for item in items)
    freeze = build_freeze(experiment_root=EXPERIMENTS)
    freeze_payload = cast("dict[str, object]", freeze["payload"])
    confirmation = cast(
        "dict[str, object]", freeze_payload["increment_27_confirmation"]
    )
    heldout_ids = set(cast("list[str]", confirmation["case_ids"]))
    assert heldout_ids.isdisjoint(case["case_id"] for case in artifact["cases"])
    diagnostic = json.loads(
        (
            ROOT / "experiments/increment_27/existing_judgment_depth_diagnostics.json"
        ).read_text(encoding="utf-8")
    )
    assert heldout_ids.isdisjoint(case["case_id"] for case in diagnostic["cases"])
