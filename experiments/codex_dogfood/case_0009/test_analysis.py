# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004, S101 -- bounded scientific fixtures
"""Verify prospective joins, metric partitions, attribution and frozen gates."""

from __future__ import annotations

import gzip
import json
import math
from copy import deepcopy
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.analyze import (
    arm_metrics,
    attribution,
    best_completion,
    build,
    decision,
    render,
    validate_join,
)
from experiments.codex_dogfood.case_0009.artifacts import (
    CASE,
    binary,
    json_bytes,
    read_json,
)


@pytest.fixture(scope="module")
def analysis() -> dict[str, Any]:
    """Reconstruct deterministically once without any prospective query run."""
    return build()


def test_replay_and_all_primary_totals(analysis: dict[str, Any]) -> None:
    """Freeze exact independent totals and both serialized outputs."""
    assert binary(CASE / "analysis.json") == json_bytes(analysis)
    assert binary(CASE / "analysis.md") == render(analysis).encode()
    expected = {
        "A": (529, 472, 1805, 342, 185, 454, 257, 46, 372),
        "B": (529, 478, 2151, 331, 231, 423, 252, 45, 342),
    }
    for arm, values in expected.items():
        m = analysis["arms"][arm]
        p = m["completion_prefix"]
        assert (
            m["positive_global_count"],
            len(m["obligation_positive_union"]),
            m["obligation_positive_cells"],
            m["global_completion_depth"],
            m["maximum_own_completion_depth"],
            p["occurrences"],
            p["union_count"],
            p["labels"]["HELPFUL_ONLY"],
            p["labels"]["UNNECESSARY"],
        ) == values
        assert p["labels"]["REQUIRED"] == 36
        assert sum(p["labels"].values()) == p["occurrences"]
        assert len(m["required_global_resources"]) == 23
        assert len(m["required_cells"]) == 37
        assert len(m["required_unit_judgments"]) == 42
        assert len(m["distinct_required_units"]) == 40


def test_disjoint_paired_partitions(analysis: dict[str, Any]) -> None:
    """Every required member is in exactly one reach partition."""
    expected = {
        "global_resources": 23,
        "any_lane_resources": 23,
        "cells": 37,
        "unit_judgments": 42,
        "distinct_units": 40,
    }
    for key, count in expected.items():
        p = analysis["reach_partitions"][key]
        assert len(p["both"]) == count
        assert p["A_only"] == p["B_only"] == p["neither"] == []
        flattened = [
            json.dumps(member, sort_keys=True)
            for members in p.values()
            for member in members
        ]
        assert len(flattened) == len(set(flattened)) == count
        assert len(p["B_only"]) - len(p["A_only"]) == 0


def test_best_alternative_never_mixes_incompatible_members() -> None:
    """Partial competing alternatives cannot manufacture sufficient coverage."""
    alternatives = [
        {"identity": name, "witnesses": [{"resource": {"address": p}} for p in paths]}
        for name, paths in (("x", ("a", "b")), ("y", ("c", "d")))
    ]
    assert best_completion(alternatives, {"a": 1, "c": 2})["depth"] is None
    value = best_completion(alternatives, {"a": 1, "b": 90, "c": 2, "d": 3})
    assert value["depth"] == 3
    assert value["best_alternative"] == "y"
    assert [r["depth"] for r in value["alternatives"]] == [90, 3]


def test_all_real_completion_alternatives(analysis: dict[str, Any]) -> None:
    """Check depths directly against captured ranks and all gold alternatives."""
    capture = json.loads(gzip.decompress(binary(CASE / "results.json.gz")))
    gold = read_json(CASE / "adjudication/judgments.json")
    for arm in ("A", "B"):
        recomputed = arm_metrics(capture["arms"][arm], gold)
        assert recomputed == analysis["arms"][arm]
        for lane in recomputed["obligations"].values():
            alternatives = lane["completion"]["alternatives"]
            assert lane["completion"]["depth"] == min(
                a["depth"] for a in alternatives if not a["missing"]
            )
        combos = recomputed["global_completion_combinations"]
        assert sorted(len(c["resources"]) for c in combos) == [22, 23]
        ranks = {
            r["address"]: r["rank"] for r in capture["arms"][arm]["global"]["rows"]
        }
        assert all(c["depth"] == max(ranks[p] for p in c["resources"]) for c in combos)


@pytest.mark.parametrize(
    "fault", ["snapshot", "resource", "query", "lane", "duplicate", "gold_task"]
)
def test_corrupt_join_is_rejected(fault: str) -> None:
    """Reject corrupted provenance or result membership before metrics."""
    capture = json.loads(gzip.decompress(binary(CASE / "results.json.gz")))
    gold = read_json(CASE / "adjudication/judgments.json")
    manifest = read_json(CASE / "pre_execution.json")
    packet = read_json(CASE / "adjudication/manifest.json")
    resources = json.loads(
        gzip.decompress(binary(CASE / "adjudication/resources.json.gz"))
    )["resources"]
    if fault == "snapshot":
        capture["snapshot_id"] = "foreign"
    elif fault == "resource":
        capture["arms"]["A"]["global"]["rows"][0]["content_identity"] = "foreign"
    elif fault == "query":
        capture["arms"]["A"]["global"]["query_text"] = "foreign"
    elif fault == "lane":
        capture["arms"]["A"].pop("frame-query")
    elif fault == "duplicate":
        capture["arms"]["A"]["global"]["rows"].append(
            capture["arms"]["A"]["global"]["rows"][0]
        )
    else:
        gold["frame"]["task_identity"] = "foreign"
    with pytest.raises(ValueError, match=r"(?i)(differ|mismatch|invalid)"):
        validate_join(capture, gold, manifest, packet, resources)


def test_exact_source_and_score_attribution(analysis: dict[str, Any]) -> None:
    """Recorded examples and effect partitions must reproduce their evidence."""
    resources = {
        r["address"]: r
        for r in json.loads(
            gzip.decompress(binary(CASE / "adjudication/resources.json.gz"))
        )["resources"]
    }
    for row in analysis["required_attribution"]:
        assert math.isclose(
            sum(row["mechanisms"].values()), row["score_delta"], abs_tol=1e-9
        )
        assert (
            len(row["new_overtakers"]) - len(row["removed_overtakers"]) == row["delta"]
        )
        for field, value in row["fields"].items():
            assert not value["lost_terms"]
            text = (
                resources[row["resource"]]["content"]
                if field == "content"
                else row["resource"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
            )
            for term in value["added_matches"] + value["shared_terms"]:
                for span in term["source_identifier_spans"]:
                    assert text[span["start"] : span["end"]] == span["observed"]
                    assert term["term"] in span["expanded_terms"]
                    assert term["term"] != span["canonical"]
            for term in value["added_matches"]:
                for span in term["query_identifier_spans"]:
                    assert (
                        row["query_text"][span["start"] : span["end"]]
                        == span["observed"]
                    )
                    assert term["term"] in span["expanded_terms"]


def test_rescue_requires_new_positive_and_exact_identifier_source() -> None:
    """A true representation rescue needs zero A evidence and compound exposure."""
    la = {
        "query_text": "candidate member resolution",
        "query_terms": ["candidate", "member", "resolution"],
        "rows": [],
    }
    terms = [{"term": t, "contribution": 1} for t in la["query_terms"]]
    row = {
        "address": "example.py",
        "rank": 1,
        "content_score": 3,
        "filename_score": 0,
        "content_terms": terms,
        "filename_terms": [],
    }
    lb = {**la, "rows": [row]}
    result = attribution(
        None,
        row,
        la,
        lb,
        {"address": "example.py", "content": "CandidateMemberResolution"},
    )
    assert result["classification"] == "VERIFIED_IDENTIFIER_REPRESENTATION_RECOVERY"
    assert all(
        t["side"] == "DOCUMENT_SIDE"
        for t in result["fields"]["content"]["added_matches"]
    )
    with pytest.raises(ValueError, match="no source evidence"):
        attribution(
            None, row, la, lb, {"address": "example.py", "content": "Unrelated"}
        )


def test_observed_whole_forms_and_readiness_query_effect(
    analysis: dict[str, Any],
) -> None:
    """Whole-form lexical preservation coexists with ranking regressions."""
    assert len(analysis["whole_form_preservation"]) == 9
    assert all(r["B_tf"] >= r["A_tf"] for r in analysis["whole_form_preservation"])
    assert not any(r["only_A_field_term"] for r in analysis["whole_form_preservation"])
    row = next(
        r
        for r in analysis["required_attribution"]
        if r["lane"] == "readiness" and r["resource"].endswith("/promotion.py")
    )
    assert (row["A_rank"], row["B_rank"]) == (33, 11)
    assert row["classification"] == "IDENTIFIER_AWARE_RANKING_GAIN"
    assert row["query_added_terms"] == ["assessment", "localization"]
    assert row["fields"]["content"]["weighted_added_match_score"] > 12
    assert row["fields"]["filename"]["weighted_added_match_score"] == 0
    assert analysis["paired_own_required_ranks"]["counts"] == {
        "IMPROVED": 13,
        "UNCHANGED": 9,
        "WORSENED": 15,
    }


def test_exact_frozen_decision_and_cost_limits(analysis: dict[str, Any]) -> None:
    """Promotion fails two exact gates; separate-view precedence is preserved."""
    outcome = analysis["decision"]
    assert outcome["outcome"] == "RETAIN AS SEPARATE RETRIEVAL VIEW"
    assert outcome["burden_reduction"] == 5 / 257
    assert outcome["verified_required_cell_rescues"] == 0
    assert outcome["improved_own_completions"] == 3
    assert len(outcome["required_top20_entries"]) == 1
    assert outcome["promotion_conditions"] == {
        "valid_complete_gold_and_join": True,
        "no_A_positive_required_cells_lost": True,
        "no_worse_every_own_and_global_completion": False,
        "twenty_percent_burden_or_verified_required_rescue": False,
        "all_frozen_cost_limits": True,
    }
    assert all(ratio <= 3 for ratio in outcome["cost_B_over_A"].values())
    assert outcome["R2"] == "MANDATORY REGARDLESS OF R1 OUTCOME"


def test_twenty_percent_and_three_times_boundaries(analysis: dict[str, Any]) -> None:
    """The prospective 20% and 3x gates have their exact inclusive boundaries."""
    metrics = deepcopy(analysis["arms"])
    metrics["A"]["completion_prefix"]["union_count"] = 100
    metrics["B"]["completion_prefix"]["union_count"] = 80
    for name in metrics["A"]["obligations"]:
        metrics["B"]["obligations"][name]["completion"]["depth"] = metrics["A"][
            "obligations"
        ][name]["completion"]["depth"]
    costs = deepcopy(analysis["costs"])
    for field in analysis["decision"]["cost_B_over_A"]:
        costs["B"][field] = 3 * costs["A"][field]
    args = (
        metrics,
        analysis["reach_partitions"],
        analysis["required_attribution"],
        costs,
    )
    assert (
        decision(*args)["outcome"] == "PROMOTE / PRODUCTIONIZE REPRESENTATION CANDIDATE"
    )
    metrics["B"]["completion_prefix"]["union_count"] = 81
    assert not decision(*args)["promotion_conditions"][
        "twenty_percent_burden_or_verified_required_rescue"
    ]
    metrics["B"]["completion_prefix"]["union_count"] = 80
    costs["B"]["median_query_seconds"] += 0.000001
    assert not decision(*args)["promotion_conditions"]["all_frozen_cost_limits"]
