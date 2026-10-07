# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- frozen prospective scientific invariants
"""Independent arithmetic, tamper rejection and joined-evidence replay checks."""

from __future__ import annotations

import asyncio
import gzip
import json
import math
import statistics
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from typing import Any, NoReturn

import pytest

from experiments.codex_dogfood.case_0009.artifacts import binary, json_bytes, read_json
from experiments.codex_dogfood.case_0010 import analyze, execute
from experiments.codex_dogfood.case_0010.freeze import CASE
from experiments.codex_dogfood.case_0010.reporting import report


@pytest.fixture(scope="module")
def analysis() -> dict[str, Any]:
    """Rebuild all exact joined evidence without producing new captured outcomes."""
    return analyze.build(asyncio.run(analyze.provenance()))


def test_committed_chain_join_and_clean_gold(analysis: dict[str, Any]) -> None:
    """Check exact frozen inputs, complete join and independent gold counts."""
    assert len(analysis["provenance"]["chain"]) == 6
    coverage = analysis["join"]["coverage"]
    assert (coverage["resources"], coverage["obligations"], coverage["cells"]) == (
        531,
        10,
        5310,
    )
    assert all(
        v == 0
        for k, v in coverage.items()
        if k not in {"resources", "obligations", "cells"}
    )
    assert analysis["gold"]["unique_required_resources_across_all_alternatives"] == 22
    assert analysis["gold"]["valid_cross_obligation_combinations"] == 9
    assert all(v == "NO" for v in analysis["stage_c_blindness_attestation"].values())
    assert not analysis["confirmation_accessed"]
    assert not analysis["production_parameters_changed"]


def test_independent_alternative_prefix_and_positive_arithmetic(
    analysis: dict[str, Any],
) -> None:
    """Calculate completion and label composition directly from captured rows."""
    captured = json.loads(gzip.decompress(binary(CASE / "results.json.gz")))
    gold = read_json(CASE / "adjudication/judgments.json")
    labels = {
        (c["obligation_id"], c["resource_address"]): c["label"] for c in gold["cells"]
    }
    required = {p for (_, p), label in labels.items() if label == "REQUIRED"}
    helpful = {
        p for (_, p), label in labels.items() if label == "HELPFUL_ONLY"
    } - required
    for arm in "ABCD":
        row = analysis["arms"][arm]
        metrics, lanes = row["metrics"], captured["arms"][arm]["lanes"]
        global_ranks = {r["address"]: r["rank"] for r in lanes["global"]["rows"]}
        union: set[str] = set()
        counts: Counter[str] = Counter()
        occurrences = 0
        cells: list[tuple[str, str]] = []
        top: dict[str, Counter[str]] = {str(k): Counter() for k in (5, 10, 20)}
        for ob in gold["obligations"]:
            name = ob["identity"]
            rows = lanes[name + "-query"]["rows"]
            ranks = {r["address"]: r["rank"] for r in rows}
            depths = [
                max(ranks[p] for p in alt["resource_addresses"])
                for alt in ob["acceptable_alternatives"]
            ]
            depth = min(depths)
            assert depth == metrics["own_depths"][name]
            assert [a["depth"] for a in row["completion_alternatives"][name]] == depths
            prefix = rows[:depth]
            union.update(r["address"] for r in prefix)
            counts.update(labels[name, r["address"]] for r in prefix)
            occurrences += len(prefix)
            cells.extend((name, r["address"]) for r in rows)
            for k in (5, 10, 20):
                top[str(k)].update(labels[name, r["address"]] for r in rows[:k])
        assert metrics["global"] == max(global_ranks[p] for p in required)
        assert metrics["prefix_occurrences"] == occurrences
        assert metrics["prefix_union"] == len(union)
        assert metrics["complete_prefix_composition"] == dict(counts)
        assert row["positive"]["own_cells"] == len(cells)
        assert row["positive"]["own_union"] == len({p for _, p in cells})
        assert len(metrics["required_resource_reach"]) == 22
        assert len(metrics["required_cells_reached"]) == 39
        assert len(metrics["required_unit_judgments_reached"]) == 45
        assert len(metrics["distinct_units_reached"]) == 40
        for k in (5, 10, 20):
            assert metrics["top_k"][str(k)]["labels"] == dict(top[str(k)])
            global_counts = Counter(
                "REQUIRED"
                if r["address"] in required
                else "HELPFUL_ONLY"
                if r["address"] in helpful
                else "UNNECESSARY"
                for r in lanes["global"]["rows"][:k]
            )
            assert row["global_top_k"][str(k)] == {
                label: global_counts[label]
                for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
            }
    for identity in captured["arms"]["A"]["lanes"]:
        members = [
            {r["address"] for r in captured["arms"][a]["lanes"][identity]["rows"]}
            for a in "ABCD"
        ]
        assert all(s == members[0] for s in members)


def test_gate_boundaries_and_exact_outcome_vocabulary() -> None:
    """Exercise every conjunction separately, including exact equality thresholds."""
    base: dict[str, Any] = {
        "global": 100,
        "max_own": 100,
        "prefix_union": 100,
        "own_depths": {str(o): 100 for o in range(10)},
    }
    current = {**deepcopy(base), "prefix_union": 90, "reach_safe": True}
    cost = {"median_query_seconds": 3, "p95_query_seconds": 3}
    base_cost = {"median_query_seconds": 1, "p95_query_seconds": 1}
    assert all(analyze.gates(current, base, cost, base_cost, Fraction(5, 4)).values())
    for field, value, failed in (
        ("global", 106, "global_le_1_05"),
        ("max_own", 106, "max_own_le_1_05"),
        ("prefix_union", 91, "meaningful_primary_improvement"),
        ("reach_safe", False, "required_reach_safe"),
    ):
        mutated = {**deepcopy(current), field: value}
        assert not analyze.gates(mutated, base, cost, base_cost, Fraction(5, 4))[failed]
    boundary = deepcopy(current)
    boundary["global"] = boundary["max_own"] = 105
    boundary["own_depths"]["0"] = 125
    assert all(analyze.gates(boundary, base, cost, base_cost, Fraction(5, 4)).values())
    boundary["own_depths"]["0"] = 126
    assert not analyze.gates(boundary, base, cost, base_cost, Fraction(5, 4))[
        "no_obligation_gt_1_25"
    ]
    boundary["own_depths"] = {str(o): 101 if o < 6 else 100 for o in range(10)}
    assert not analyze.gates(boundary, base, cost, base_cost, Fraction(5, 4))[
        "half_obligations_nonworse"
    ]
    assert not analyze.gates(
        current, base, {**cost, "p95_query_seconds": 3.01}, base_cost, Fraction(5, 4)
    )["cost_le_3"]
    assert not analyze.gates(current, base, cost, base_cost, Fraction(126, 100))[
        "development_safe_le_1_25"
    ]
    passing = analyze.gates(current, base, cost, base_cost, Fraction(5, 4))
    arms: dict[str, Any] = {a: {"gates": passing} for a in "BCD"}
    assert analyze.outcome(arms) == ("NONBASELINE_PARAMETER_CANDIDATE", list("BCD"))
    for row in arms.values():
        row["gates"] = {**passing, "meaningful_primary_improvement": False}
        row["metrics"] = {
            "reach_safe": True,
            "normalized_exact": {
                k: [1, 1] for k in ("global", "max_own", "prefix_union")
            },
        }
    assert analyze.outcome(arms) == ("BASELINE_ROBUST", [])
    arms["B"]["metrics"]["normalized_exact"]["global"] = [106, 100]
    assert analyze.outcome(arms) == ("MIXED / NO SAFE REPLACEMENT", [])


def test_paired_partitions_costs_and_gates(analysis: dict[str, Any]) -> None:
    """Validate rank movement counts, actual captured timings and frozen safety."""
    base = analysis["arms"]["A"]
    for arm, row in analysis["arms"].items():
        cost = row["cost"]
        values = sorted(cost["query_seconds"].values())
        assert cost["median_query_seconds"] == statistics.median(values)
        assert cost["p95_query_seconds"] == max(values)
        assert cost["sum_query_seconds"] == sum(values)
        worst = Fraction(*row["development"]["worst_own_union_exact"])
        assert row["gates"] == analyze.gates(
            row["metrics"], base["metrics"], cost, base["cost"], worst
        )
        if arm != "A":
            pairs = row["paired_required"]
            deltas = [r["challenger"] - r["A"] for r in pairs["cells"]]
            assert len(deltas) == 39
            assert pairs["improved"] == sum(d < 0 for d in deltas)
            assert pairs["worsened"] == sum(d > 0 for d in deltas)
            assert pairs["unchanged"] == deltas.count(0)
            assert pairs["median_delta"] == statistics.median(deltas)
            assert pairs["best_improvement"] == min(deltas)
            assert pairs["worst_regression"] == max(deltas)
            assert all(
                not v
                for partition in row["reach_partitions"].values()
                for v in partition.values()
            )
    assert analyze.outcome(analysis["arms"]) == (
        analysis["outcome"],
        analysis["passing_candidates"],
    )


def test_diagnostic_replay_term_profiles_and_conservative_attribution(
    analysis: dict[str, Any],
) -> None:
    """Retain exact score terms, overtaker sets and independent judged yields."""
    for r in analysis["diagnostics"]:
        for side in ("A", "challenger"):
            ex = r[side]
            assert ex["score_reconstructed"]
            assert math.isclose(
                sum(t["weighted_contribution"] for t in ex["terms"]),
                ex["captured_score"],
                abs_tol=1e-10,
            )
            for term in ex["terms"]:
                saturation = term["tf_numerator"] / term["tf_denominator"]
                assert math.isclose(saturation, term["tf_saturation"])
                assert math.isclose(
                    term["idf"] * saturation * term["field_weight"],
                    term["weighted_contribution"],
                )
        left, right = (
            set(r["A"]["ranking"]["ahead_resources"]),
            set(r["challenger"]["ranking"]["ahead_resources"]),
        )
        assert r["pair"]["new_overtakers"] == sorted(right - left)
        assert r["pair"]["removed_overtakers"] == sorted(left - right)
        assert r["pair"]["changed_query_terms"] == {"added": [], "removed": []}
        for term in r["pair"]["mechanics"]["term_deltas"]:
            assert term["tf_delta"] == term["df_delta"] == term["idf_delta"] == 0
    for profiles in analysis["query_profiles"].values():
        for p in profiles:
            n = len(p["effective_matching_resources"])
            labels = p["judged_labels"]
            assert sum(labels.values()) == n
            assert p["unjudged_matched"] == 0
            assert p["required_yield"] == (labels.get("REQUIRED", 0) / n if n else None)


def test_gold_and_treatment_tamper_rejected() -> None:
    """Reject corrupt content binding, unit witnesses and treatment frame before use."""
    manifest, packet = analyze.SC.load_packet(CASE / "adjudication")
    gold = read_json(CASE / "adjudication/judgments.json")
    damaged = deepcopy(gold)
    damaged["cells"][0]["content_identity"] = "wrong"
    with pytest.raises(ValueError, match="content identity"):
        analyze.SC.verify_judgments(manifest, packet, damaged)
    damaged = deepcopy(gold)
    damaged["cells"].append(deepcopy(damaged["cells"][0]))
    with pytest.raises(ValueError, match="Duplicate observed cell"):
        analyze.SC.verify_judgments(manifest, packet, damaged)
    damaged = deepcopy(gold)
    damaged["obligations"][0]["acceptable_alternatives"][0]["all_of"].pop()
    with pytest.raises(ValueError, match="Incomplete alternative"):
        analyze.SC.verify_judgments(manifest, packet, damaged)
    case, _, _ = analyze.joined_case()
    capture = json.loads(gzip.decompress(binary(CASE / "results.json.gz")))
    treatment = read_json(CASE / "treatment.json")
    treatment["arms"][1]["parameters"][0] = 1.8
    with pytest.raises(ValueError, match="arm definitions"):
        analyze.engines(case, capture, treatment)


def forbidden_scoring(*_args: object, **_kwargs: object) -> NoReturn:
    """Forbid treatment queries during analysis replay."""
    message = "Treatments must not execute again"
    raise AssertionError(message)


def test_json_markdown_replay_without_scoring(
    analysis: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Compare published bytes and exercise the original diagnostics-only replay."""
    assert json_bytes(analysis) == binary(CASE / "analysis.json")
    assert report(analysis).encode() == binary(CASE / "analysis.md")
    monkeypatch.setattr(execute, "retrieve", forbidden_scoring)
    assert execute.verify()["status"] == "R1.5 exact score/universe replay PASSED"
