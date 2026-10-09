# Copyright (c) 2026
# ruff: noqa: C901, E501, PLR0912, PLR0915, PLR2004, EM101, TRY003, FBT001, FBT003, COM812 -- mathematical predicates; formatter owns commas
"""Measure alternatives and responsible subsets over authenticated captures."""

from __future__ import annotations

import itertools
import math
from collections import Counter
from fractions import Fraction
from typing import Any

from experiments.codex_dogfood.case_0011.stage_d.inputs import require, unique
from experiments.retrieval_diagnostics.models import DiagnosticPolicy

LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")

INCOMPLETE = "INCOMPLETE_INFORMATION_NEED_COVERAGE"


def depth(rows: dict[str, Any], resources: list[str]) -> int | None:
    """Return all-member completion; never replace a miss with a numeric rank."""
    return (
        max((rows[p]["rank"] for p in resources), default=0)
        if all(p in rows for p in resources)
        else None
    )


def burden(
    s: dict[str, Any],
    prefixes: dict[str, int],
    *,
    unit_count: int | None = None,
) -> dict[str, Any]:
    """Count counterfactual prefix occurrences and deduplicated content volume."""
    occurrences = []
    union: set[str] = set()
    for qid, d in sorted(prefixes.items()):
        q = s["queries"][qid]
        for r in s["capture"]["queries"][qid]["rows"][:d]:
            p = r["address"]
            union.add(p)
            occurrences.append(label(s, q["obligation"], p))
    return {
        "prefix_depths": dict(sorted(prefixes.items())),
        "query_count_used": sum(d > 0 for d in prefixes.values()),
        "occurrences": len(occurrences),
        "unique_resources": len(union),
        "duplicates": len(occurrences) - len(union),
        "occurrence_labels": {k: occurrences.count(k) for k in LABELS},
        "unique_global_labels": dict(Counter(label(s, None, p) for p in sorted(union))),
        "resources": sorted(union),
        "utf8_bytes": sum(len(s["contents"][p].encode("utf-8")) for p in union),
        "resources_per_covered_unit": len(union) / unit_count if unit_count else None,
        "actual_evidence_inspection_cost": "NOT MEASURED",
        "metric_scope": "counterfactual completion-prefix inspection burden",
    }


def label(s: dict[str, Any], obligation: str | None, address: str) -> str:
    """Use lane-relative labels, or strongest reviewed global resource label."""
    if obligation:
        return str(s["cells"][obligation, address]["label"])
    return str(s["global_labels"][address])


def explain(
    s: dict[str, Any],
    qid: str,
    address: str,
    obligation: str | None,
) -> dict[str, Any]:
    """Expose exact captured score evidence and all unnecessary overtakers."""
    rows = s["capture"]["queries"][qid]["rows"]
    row = next((r for r in rows if r["address"] == address), None)
    ahead = rows[: row["rank"] - 1] if row else []
    unnecessary = [
        r for r in ahead if label(s, obligation, r["address"]) == "UNNECESSARY"
    ]
    return {
        "query": qid,
        "resource": address,
        "rank": row["rank"] if row else None,
        "score_evidence": row,
        "unnecessary_overtakers": [r["address"] for r in unnecessary],
        "unnecessary_overtaker_count": len(unnecessary),
        "overtaker_score_evidence": unnecessary[:5],
        "mechanical_cause": "Positive lexical evidence competes with higher scored unnecessary rows."
        if unnecessary
        else "No unnecessary overtakers."
        if row
        else "No positive captured lexical match; not a result-bound omission.",
    }


def reach(s: dict[str, Any], arm: str) -> dict[str, Any]:
    """Keep union reach distinct from owner-lane resource and unit reach."""
    qs = [q for q in s["queries"].values() if q["arm"] == arm]
    sets = {
        q["identity"]: {
            r["address"] for r in s["capture"]["queries"][q["identity"]]["rows"]
        }
        for q in qs
    }
    union = set().union(*sets.values())
    required = {c["address"] for c in s["gold"]["cells"] if c["label"] == "REQUIRED"}
    own = {
        ob: set().union(
            *(sets[q["identity"]] for q in qs if arm == "A" or q["obligation"] == ob),
        )
        for ob in (o["identity"] for o in s["treatment"]["obligations"])
    }
    cells = [
        (c["obligation"], c["address"])
        for c in s["gold"]["cells"]
        if c["label"] == "REQUIRED" and c["address"] in own[c["obligation"]]
    ]
    units = [
        uid
        for uid, u in s["units"].items()
        if all(
            {e["address"] for e in u["supports"]} <= own[ob] for ob in u["obligations"]
        )
    ]
    return {
        "resources": sorted(required & union),
        "cells": sorted(cells),
        "units": sorted(units),
        "obligation_units": sorted(
            (ob, uid) for uid in units for ob in s["units"][uid]["obligations"]
        ),
        "indispensable_resources": sorted(
            set(s["gold_statistics"]["task_indispensable_resources"]) & union,
        ),
        "owner_lane_positive_resources": {ob: sorted(ps) for ob, ps in own.items()},
        "unit_semantics": "All reviewed support resources in each owning obligation's positive lane union; resource reach is not need-semantic completion.",
    }


def responsible_subset(
    s: dict[str, Any],
    covered: list[str],
    collective: bool,
) -> dict[str, Any]:
    """Require every pre-reviewed responsible query, including collective members."""
    prefixes: dict[str, int] = {}
    b_prefixes: dict[str, int] = {}
    records = []
    for uid in covered:
        u, c = s["units"][uid], s["coverage"][uid]
        needs = c["direct_needs"]
        if not needs and collective:
            choices = [
                r
                for r in s["semantic"]["collective_coverage"]
                if r["unit"] == uid
                and r["classification"] == "VALID_MINIMAL_COLLECTIVE_SET"
            ]
            require(
                len(choices) == 1,
                "Collective responsibility is not uniquely frozen",
            )
            needs = choices[0]["needs"]
        supports = sorted({e["address"] for e in u["supports"]})
        routes = []
        for need in needs:
            qid = next(
                q["identity"]
                for q in s["queries"].values()
                if q["information_need"] == need
            )
            rows = unique(s["capture"]["queries"][qid]["rows"], "address")
            d = depth(rows, supports)
            require(
                d is not None,
                "Covered subset has unreachable responsible evidence",
            )
            if d is None:
                raise ValueError("Responsible query miss")
            prefixes[qid] = max(prefixes.get(qid, 0), d)
            routes.append(
                {
                    "need": need,
                    "query": qid,
                    "depth": d,
                    "evidence": [
                        explain(s, qid, p, u["obligations"][0]) for p in supports
                    ],
                },
            )
        b_routes = []
        for ob in u["obligations"]:
            qid = f"B.{ob}"
            d = depth(unique(s["capture"]["queries"][qid]["rows"], "address"), supports)
            require(d is not None, "Baseline subset miss")
            if d is None:
                raise ValueError("Baseline subset miss")
            b_prefixes[qid] = max(b_prefixes.get(qid, 0), d)
            b_routes.append(
                {
                    "obligation": ob,
                    "query": qid,
                    "depth": d,
                    "evidence": [explain(s, qid, p, ob) for p in supports],
                },
            )
        c_depth = max(r["depth"] for r in routes)
        b_depth = max(r["depth"] for r in b_routes)
        records.append(
            {
                "unit": uid,
                "gold_unit": u["id"],
                "alias": c["alias"],
                "obligations": u["obligations"],
                "statement": u["statement"],
                "resources": supports,
                "responsible_routes": routes,
                "B_routes": b_routes,
                "C_max_depth": c_depth,
                "B_max_depth": b_depth,
                "depth_delta": c_depth - b_depth,
                "comparison": "IMPROVEMENT"
                if c_depth < b_depth
                else "REGRESSION"
                if c_depth > b_depth
                else "TIE",
            },
        )
    cb, bb = (
        burden(s, prefixes, unit_count=len(covered)),
        burden(s, b_prefixes, unit_count=len(covered)),
    )
    return {
        "label": "GRANULARITY_AWARE_SUBSET_DIAGNOSTIC"
        if collective
        else "STRICT_COVERED_SUBSET_DIAGNOSTIC",
        "not_full_task_completion": True,
        "unit_count": len(covered),
        "units": records,
        "C": cb,
        "B_same_units": bb,
        "comparison_counts": dict(Counter(r["comparison"] for r in records)),
        "misses": 0,
        "burden_deltas_C_minus_B": {
            k: cb[k] - bb[k]
            for k in ("occurrences", "unique_resources", "duplicates", "utf8_bytes")
        },
        "unnecessary_delta": cb["occurrence_labels"]["UNNECESSARY"]
        - bb["occurrence_labels"]["UNNECESSARY"],
    }


def select_outcome(
    contract_valid: bool,
    omitted: bool,
    misformulated: bool,
    gates: dict[str, bool],
    benefit: bool,
) -> str:
    """Apply the literal frozen precedence before interpreting subset benefit."""
    if not contract_valid:
        return "EXPERIMENTAL_CONTRACT_DEFECT"
    if omitted or misformulated:
        return "INFORMATION_NEED_AUTHORING_DEFECT"
    if all(gates.values()):
        return "INFORMATION_NEED_DECOMPOSITION_SUPPORTED"
    if gates["required_reach_safe"] and benefit:
        return "COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER"
    return "NO_MATERIAL_VALUE"


def build(s: dict[str, Any], proof: dict[str, Any]) -> dict[str, Any]:
    """Compute frozen gates, alternatives and disjoint earliest-stage attribution."""
    treatment, gold, semantic = s["treatment"], s["gold"], s["semantic"]
    queries = s["queries"]
    ranks = {
        qid: unique(s["capture"]["queries"][qid]["rows"], "address") for qid in queries
    }
    positive = {
        a: set().union(
            *(set(ranks[qid]) for qid, q in queries.items() if q["arm"] == a),
        )
        for a in "ABC"
    }
    costs = s["costs"]
    arms: dict[str, Any] = {}
    for arm in "ABC":
        qs = [qid for qid, q in queries.items() if q["arm"] == arm]
        occurrences = sum(len(ranks[qid]) for qid in qs)
        arms[arm] = {
            "query_count": len(qs),
            "query_seconds": math.fsum(costs["query_seconds"][qid] for qid in qs),
            "query_costs": {qid: costs["query_seconds"][qid] for qid in qs},
            "positive_occurrences": occurrences,
            "unique_positive_resources": len(positive[arm]),
            "duplicate_occurrences": occurrences - len(positive[arm]),
            "positive_resources": sorted(positive[arm]),
            "reach": reach(s, arm),
        }
    combinations = list(
        itertools.product(*(o["alternatives"] for o in gold["obligations"])),
    )
    require(len(combinations) == 6, "Witness combination partition differs")
    combos: list[dict[str, Any]] = [
        {
            "alternatives": [a["id"] for a in c],
            "resources": sorted({p for a in c for p in a["resources"]}),
            "units": sorted({uid for a in c for uid in a["units"]}),
        }
        for c in combinations
    ]
    require(
        combos == s["gold_statistics"]["complete_task_combinations"],
        "Exact witness combinations differ",
    )
    for c in combos:
        c["depth"] = depth(ranks["A.task"], c["resources"])
    best = min(
        (c for c in combos if c["depth"] is not None),
        key=lambda c: (c["depth"], c["alternatives"]),
    )
    arms["A"]["completion"] = {
        "combinations": combos,
        "selected": best,
        "depth": best["depth"],
        "last_indispensable_resource_rank": depth(
            ranks["A.task"],
            s["gold_statistics"]["task_indispensable_resources"],
        ),
        **burden(s, {"A.task": best["depth"]}),
    }
    b_alts: dict[str, Any] = {}
    c_alts: dict[str, Any] = {}
    prefixes: dict[str, int] = {}
    for o in gold["obligations"]:
        ob = o["obligation"]
        choices = [
            {
                "alternative": a["id"],
                "units": a["units"],
                "resources": a["resources"],
                "depth": depth(ranks[f"B.{ob}"], a["resources"]),
            }
            for a in o["alternatives"]
        ]
        selected = min(
            (a for a in choices if a["depth"] is not None),
            key=lambda a: (a["depth"], a["alternative"]),
        )
        prefixes[f"B.{ob}"] = selected["depth"]
        b_alts[ob] = {
            "alternatives": choices,
            "selected": selected,
            "burden": burden(s, {f"B.{ob}": selected["depth"]}),
        }
        c_alts[ob] = [
            {
                "alternative": a["id"],
                "units": a["units"],
                "noncovered_units": [
                    s["projection"]["unit_projection"][uid]
                    for uid in a["units"]
                    if s["coverage"][s["projection"]["unit_projection"][uid]]["status"]
                    != "COVERED"
                ],
                "semantic_completion": INCOMPLETE,
                "completion_depth": None,
                "completion_burden": None,
            }
            for a in o["alternatives"]
        ]
        require(
            all(a["noncovered_units"] for a in c_alts[ob]),
            "Unexpected semantically complete C alternative",
        )
    arms["B"]["completion"] = {"obligations": b_alts, **burden(s, prefixes)}
    arms["C"]["completion"] = {
        "semantic_completion": INCOMPLETE,
        "completion_depth": None,
        "completion_burden": None,
        "obligations": c_alts,
    }
    for arm in "AB":
        b = arms[arm]["completion"]
        b["excess_over_15_minimum"] = b["unique_resources"] - 15
        b["ratio_to_15_minimum_exact"] = [b["unique_resources"], 15]
    strict = responsible_subset(
        s,
        [uid for uid, c in s["coverage"].items() if c["status"] == "COVERED"],
        False,
    )
    granular = responsible_subset(
        s,
        [
            uid
            for uid, c in s["coverage"].items()
            if c["granularity_aware_status"] == "GRANULARITY_AWARE_COVERED"
        ],
        True,
    )
    cqs = [qid for qid, q in queries.items() if q["arm"] == "C"]
    required = s["gold_statistics"]["required_resource_union"]
    oracle_resources = {
        p: min(
            (
                {"query": qid, "rank": ranks[qid][p]["rank"]}
                for qid in cqs
                if p in ranks[qid]
            ),
            key=lambda r: (r["rank"], r["query"]),
        )
        for p in required
    }
    oracle_combos = []
    for c in combos:
        selected_routes = {p: oracle_resources[p] for p in c["resources"]}
        pd: dict[str, int] = {}
        for r in selected_routes.values():
            pd[r["query"]] = max(pd.get(r["query"], 0), r["rank"])
        oracle_combos.append(
            {
                "alternatives": c["alternatives"],
                "max_best_resource_rank": max(
                    r["rank"] for r in selected_routes.values()
                ),
                "routes": selected_routes,
                "burden": burden(s, pd),
            },
        )
    oracle = {
        "label": "UNCONSTRAINED_QUERY_ORACLE",
        "excluded_from_U1_rule": True,
        "selection_rule": "Per-resource best rank across all C queries, tie by query identity; prefix projection, not globally optimized set cover or a responsible acquisition policy.",
        "resources": oracle_resources,
        "combinations": oracle_combos,
        "selected": min(
            oracle_combos,
            key=lambda c: (c["max_best_resource_rank"], c["alternatives"]),
        ),
    }
    unit_records: list[dict[str, Any]] = []
    for uid, u in sorted(
        s["units"].items(),
        key=lambda item: s["coverage"][item[0]]["alias"],
    ):
        c = s["coverage"][uid]
        supports = sorted({e["address"] for e in u["supports"]})
        partials = [
            s["semantic"]["mappings"][i]
            for i in range(len(s["semantic"]["mappings"]))
            if s["semantic"]["mappings"][i]["unit"] == uid
            and s["semantic"]["mappings"][i]["label"] == "PARTIALLY_COVERS"
        ]
        routes = [r for r in strict["units"] if r["unit"] == uid]
        direct_evidence = routes[0]["responsible_routes"] if routes else []
        noise = max(
            (
                e["unnecessary_overtaker_count"]
                for r in direct_evidence
                for e in r["evidence"]
            ),
            default=0,
        )
        failure = (
            "MISSING_INFORMATION_NEED"
            if c["status"] == "UNCOVERED"
            else "INCOMPLETE_INFORMATION_NEED"
            if c["status"] == "PARTIAL_ONLY"
            else "RETRIEVAL_RANKING_DISCRIMINATION_FAILURE"
            if noise >= DiagnosticPolicy().substantial_unnecessary_ahead
            else "NO_ACQUISITION_FAILURE"
        )
        if c["alias"] == "U05":
            failure = "GOOD_NEED_BAD_QUERY"
        elif c["alias"] == "U27":
            failure = "REPRESENTATION_FAILURE"
        unit_records.append(
            {
                "unit": uid,
                "gold_unit": u["id"],
                "alias": c["alias"],
                "statement": u["statement"],
                "obligations": u["obligations"],
                "resources": supports,
                "strict_status": c["status"],
                "granularity_aware_status": c["granularity_aware_status"],
                "direct_needs": c["direct_needs"],
                "partial_needs": c["partial_needs"],
                "partial_mapping_evidence": partials,
                "missing_semantic_component": {
                    "statement": u["statement"],
                    "reviewed_component_rationales": [
                        m.get("rationale", m.get("source_rationales", []))
                        for m in partials
                    ],
                    "rule": "No complete answer is sought by a directly responsible frozen need.",
                }
                if c["status"] != "COVERED"
                else None,
                "responsible_retrieval": direct_evidence,
                "oracle_resource_ranks": {p: oracle_resources[p] for p in supports},
                "oracle_unit_depth": max(oracle_resources[p]["rank"] for p in supports),
                "any_C_resource_reach": all(p in positive["C"] for p in supports),
                "oracle_credit": "Descriptive only; unrelated/partial need routes do not establish semantic completion.",
                "earliest_failure": failure,
                "ranking_noise_count": noise,
                "ranking_diagnostic_threshold": DiagnosticPolicy().substantial_unnecessary_ahead,
                "failed_stage": "INFORMATION_NEED_FORMULATION"
                if c["status"] != "COVERED"
                else "RETRIEVAL_RANKING"
                if noise >= DiagnosticPolicy().substantial_unnecessary_ahead
                else None,
                "semantic_evidence": c,
                "mechanical_evidence": direct_evidence
                or {p: oracle_resources[p] for p in supports},
                "contributing_factors": (
                    ["EXPERIMENTAL_GRANULARITY_LIMITATION"]
                    if any(
                        r["unit"] == uid
                        and r["classification"] == "COLLECTIVELY_COVERABLE"
                        for r in semantic["granularity"]
                    )
                    else []
                ),
                "what_would_have_to_change": "Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule."
                if c["status"] != "COVERED"
                else "Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it."
                if noise >= DiagnosticPolicy().substantial_unnecessary_ahead
                else "No change required for this bounded acquisition.",
            },
        )
    for record in unit_records:
        if record["alias"] == "U05":
            record["failed_stage"] = "QUERY_FORMULATION"
            record["contributing_factors"] += [
                "QUERY_DILUTION",
                "RETRIEVAL_RANKING_DISCRIMINATION_FAILURE",
            ]
            record["what_would_have_to_change"] = (
                "Retain distinguishing copied ModelRequest/Context Planning vocabulary in a prospectively frozen literal query. This query matches the actual planning test only on 'tests'; numeric-validation wording instead supplies effective routes to U26 and unrelated argument documentation. No repaired query was tested."
            )
        elif record["alias"] == "U27":
            record["failed_stage"] = "LEXICAL_REPRESENTATION"
            record["contributing_factors"] += [
                "RETRIEVAL_RANKING_DISCRIMINATION_FAILURE",
            ]
            record["what_would_have_to_change"] = (
                "Prospectively test whole-identifier plus subtoken evidence or a deterministic owner route. 'rendered' is hidden inside RenderedContextDisclosure in canonical source analysis; the source contributes only 'context' to this query. No alternative representation was executed."
            )
        elif record["alias"] == "U06":
            record["contributing_factors"] += ["POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH"]
    safety = {}
    for key in ("resources", "cells", "units", "obligation_units"):
        left, right = arms["B"]["reach"][key], arms["C"]["reach"][key]
        ls, rs = (
            set(map(tuple, left))
            if key in ("cells", "obligation_units")
            else set(left),
            set(map(tuple, right))
            if key in ("cells", "obligation_units")
            else set(right),
        )
        safety[key] = {"B_lost_in_C": sorted(ls - rs), "C_only_vs_B": sorted(rs - ls)}
    gates = {
        "required_reach_safe": all(not v["B_lost_in_C"] for v in safety.values()),
        "100_percent_direct_unit_coverage": len(strict["units"]) == 32,
        "20_percent_burden_improvement_and_other_le_1_05": False,
        "every_mandatory_obligation_le_1_25": False,
    }
    omitted = any(c["status"] == "UNCOVERED" for c in s["coverage"].values())
    misformulated = any(
        n["classification"] == "MISFORMULATED"
        and (n["direct_units"] or n["partial_units"])
        for n in semantic["need_classifications"]
    )
    outcome = select_outcome(
        True,
        omitted,
        misformulated,
        gates,
        strict["C"]["unique_resources"] < strict["B_same_units"]["unique_resources"],
    )
    return {
        "schema": "case-0011-stage-d-v1",
        "provenance": proof,
        "join_integrity": {
            "status": "PASSED",
            **gold["frame"],
            "resources": 531,
            "obligations": 9,
            "cells": 4779,
            "required_cells": 23,
            "required_units": 32,
            "needs": 18,
            "mappings": 576,
            "queries": 28,
            "query_execution_count_each": 1,
            "alternatives": 12,
            "task_combinations": 6,
            "duplicate_missing_unexpected": 0,
            "exact_statements_and_content_identities": "PASSED",
        },
        "reviewed_gold": s["gold_statistics"],
        "task_gap": gold["task_gap"],
        "repository_information_gap": "NONE",
        "reviewed_C5": semantic["statistics"],
        "decision_rule": treatment["decision_rule"],
        "arms": arms,
        "cost_scope": {
            "shared_content_index_seconds": costs["shared_content_index_seconds"],
            "timing_scope": costs["timing_scope"],
            "index_reuse": "One shared content index; native filename index creation included in each query time.",
            "actual_evidence_inspection_cost": "NOT MEASURED",
        },
        "overlap": {
            f"{a}_{b}": {
                "intersection": len(positive[a] & positive[b]),
                f"{a}_only": len(positive[a] - positive[b]),
                f"{b}_only": len(positive[b] - positive[a]),
            }
            for a, b in itertools.combinations("ABC", 2)
        },
        "required_reach_partitions": {
            "A_only": sorted(
                set(arms["A"]["reach"]["resources"])
                - set(arms["B"]["reach"]["resources"])
                - set(arms["C"]["reach"]["resources"]),
            ),
            "B_only": sorted(
                set(arms["B"]["reach"]["resources"])
                - set(arms["A"]["reach"]["resources"])
                - set(arms["C"]["reach"]["resources"]),
            ),
            "C_only": sorted(
                set(arms["C"]["reach"]["resources"])
                - set(arms["A"]["reach"]["resources"])
                - set(arms["B"]["reach"]["resources"]),
            ),
            "common_all": sorted(
                set.intersection(*(set(arms[a]["reach"]["resources"]) for a in "ABC")),
            ),
            "missed_all": sorted(
                set(required)
                - set.union(*(set(arms[a]["reach"]["resources"]) for a in "ABC")),
            ),
        },
        "strict_subset": strict,
        "granularity_subset": granular,
        "oracle": oracle,
        "unit_failures": unit_records,
        "failure_class_totals": dict(
            Counter(u["earliest_failure"] for u in unit_records),
        ),
        "failure_classes_not_established": [
            "GOOD_NEED_BAD_QUERY",
            "QUERY_DILUTION",
            "REPRESENTATION_FAILURE",
            "POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH",
        ],
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "safety_sets": safety,
        "gates": gates,
        "gate_status": {
            "burden": "NOT_EVALUABLE: no complete C alternative; false for support",
            "per_obligation": {
                ob: {
                    "B_depth": x["selected"]["depth"],
                    "C_responsible_complete_union": None,
                    "bound_exact": [5 * x["selected"]["depth"], 4],
                    "pass": False,
                }
                for ob, x in b_alts.items()
            },
        },
        "outcome": outcome,
        "outcome_reason": "Two UNCOVERED units have no direct or partial frozen need (U02/U19). Literal frozen omitted-unit precedence selects authoring defect before support/complementary/no-value; eight PARTIAL_ONLY needs are not adjudicated MISFORMULATED.",
        "production_changed": False,
        "confirmation_accessed": False,
        "reserve_accessed": False,
        "next_step": "Prepare a separately authorized U2 exact-hint extraction and deterministic-routing experiment; do not implement in this checkpoint.",
        "U2": "FUTURE",
        "U3": "FUTURE",
        "R1.7": "RETAINED after upstream evidence",
        "R2_true_BM25F": "MANDATORY",
    }


def exact_gate(c_unique: int, b_unique: int, c_noise: int, b_noise: int) -> bool:
    """Apply the frozen quantitative disjunction with exact rational arithmetic."""
    unique_improves = (
        Fraction(c_unique, b_unique) <= Fraction(4, 5) if b_unique else False
    )
    noise_improves = Fraction(c_noise, b_noise) <= Fraction(4, 5) if b_noise else False
    unique_safe = (
        Fraction(c_unique, b_unique) <= Fraction(21, 20) if b_unique else c_unique == 0
    )
    noise_safe = (
        Fraction(c_noise, b_noise) <= Fraction(21, 20) if b_noise else c_noise == 0
    )
    return (unique_improves and noise_safe) or (noise_improves and unique_safe)


def evaluate(s: dict[str, Any], proof: dict[str, Any]) -> dict[str, Any]:
    """Attach explanatory diagnostics after freezing primary measurements."""
    from experiments.codex_dogfood.case_0011.stage_d.diagnostics import (  # noqa: PLC0415 -- post-metric explanatory layer
        diagnose,
    )

    data = build(s, proof)
    data["diagnostics"] = diagnose(s, data["strict_subset"])
    data["diagnostics"]["R1.5_reconstructed_explanations"] = s["r15_explanations"]
    for unit in data["unit_failures"]:
        hints = [
            h
            for h in data["diagnostics"]["exact_hints"]
            if h["declaration_resource"] in unit["resources"]
            and any(
                r["query"] in {x["query"] for x in unit["responsible_retrieval"]}
                and r["declaration"]["unnecessary_overtaker_count"] > 0
                for r in h["queries"]
            )
        ]
        if hints:
            unit["contributing_factors"].append("EXACT_HINT_NOT_ROUTED")
            unit["exact_hint_evidence"] = [h["hint"] for h in hints]
    data["covered_subset_obligation_diagnostics"] = {}
    for ob, baseline in data["arms"]["B"]["completion"]["obligations"].items():
        scoped = responsible_subset(
            s,
            [
                u["unit"]
                for u in data["strict_subset"]["units"]
                if ob in u["obligations"]
            ],
            False,
        )
        scoped["C_union_vs_B_full_depth_exact"] = [
            scoped["C"]["unique_resources"],
            baseline["selected"]["depth"],
        ]
        scoped["secondary_le_1_25_B_full_depth"] = (
            4 * scoped["C"]["unique_resources"] <= 5 * baseline["selected"]["depth"]
        )
        data["covered_subset_obligation_diagnostics"][ob] = scoped
    data["failure_classes_not_established"] = ["POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH"]
    data["contributing_failure_class_totals"] = dict(
        Counter(f for u in data["unit_failures"] for f in u["contributing_factors"]),
    )
    for key in ("strict_subset", "granularity_subset"):
        subset = data[key]
        c, b = subset["C"], subset["B_same_units"]
        subset["secondary_quantitative_gate"] = exact_gate(
            c["unique_resources"],
            b["unique_resources"],
            c["occurrence_labels"]["UNNECESSARY"],
            b["occurrence_labels"]["UNNECESSARY"],
        )
        subset["ratios_exact"] = {
            k: [c[k], b[k]] for k in ("unique_resources", "occurrences", "utf8_bytes")
        }
        subset["unnecessary_ratio_exact"] = [
            c["occurrence_labels"]["UNNECESSARY"],
            b["occurrence_labels"]["UNNECESSARY"],
        ]
    data["subset_depth_comparison_scope"] = (
        "Per-unit depth is max across every responsible need and every B owning obligation; individual owner-lane comparisons remain in paired_required_evidence. Unit depths cannot be averaged with semantically incomplete units."
    )
    data["comparisons"] = {}
    surfaces = {
        "A_vs_B_complete": (
            data["arms"]["A"]["completion"],
            data["arms"]["B"]["completion"],
        ),
        "B_vs_C_strict_same_units": (
            data["strict_subset"]["B_same_units"],
            data["strict_subset"]["C"],
        ),
        "B_vs_C_granularity_same_units": (
            data["granularity_subset"]["B_same_units"],
            data["granularity_subset"]["C"],
        ),
    }
    for name, (left, right) in surfaces.items():
        data["comparisons"][name] = {}
        for key in (
            "unique_resources",
            "occurrences",
            "duplicates",
            "utf8_bytes",
            "query_count_used",
            "UNNECESSARY",
        ):
            a = left["occurrence_labels"][key] if key == "UNNECESSARY" else left[key]
            b = right["occurrence_labels"][key] if key == "UNNECESSARY" else right[key]
            data["comparisons"][name][key] = {
                "baseline": a,
                "changed": b,
                "delta": b - a,
                "percent_change": 100 * (b - a) / a if a else None,
                "ratio_exact": [b, a] if a else None,
            }
    data["ranking_lane_comparison_counts"] = dict(
        Counter(
            "IMPROVEMENT"
            if row["rank_delta"] < 0
            else "REGRESSION"
            if row["rank_delta"] > 0
            else "TIE"
            for row in data["diagnostics"]["paired_required_evidence"]
        )
    )
    data["required_resource_failure_records"] = [
        {
            "resource": p,
            "attached_units": [
                {
                    "unit": u["unit"],
                    "alias": u["alias"],
                    "strict_status": u["strict_status"],
                    "earliest_failure": u["earliest_failure"],
                }
                for u in data["unit_failures"]
                if p in u["resources"]
            ],
            "required_owning_cells": [
                c["obligation"]
                for c in s["gold"]["cells"]
                if c["address"] == p and c["label"] == "REQUIRED"
            ],
            "positive_required_reach": {
                a: p in data["arms"][a]["reach"]["resources"] for a in "ABC"
            },
            "oracle": data["oracle"]["resources"][p],
            "scope": "No positive resource miss; semantic responsibility and failure stage are unit-specific even for shared resources.",
        }
        for p in s["gold_statistics"]["required_resource_union"]
    ]
    data["required_reach_all_partitions"] = {}
    for key in (
        "resources",
        "cells",
        "units",
        "obligation_units",
        "indispensable_resources",
    ):
        sets = {
            a: {
                tuple(r) if isinstance(r, (list, tuple)) else r
                for r in data["arms"][a]["reach"][key]
            }
            for a in "ABC"
        }
        universe = (
            set(s["gold_statistics"]["required_resource_union"])
            if key == "resources"
            else {
                (c["obligation"], c["address"])
                for c in s["gold"]["cells"]
                if c["label"] == "REQUIRED"
            }
            if key == "cells"
            else set(s["units"])
            if key == "units"
            else {(ob, uid) for uid, u in s["units"].items() for ob in u["obligations"]}
            if key == "obligation_units"
            else set(s["gold_statistics"]["task_indispensable_resources"])
        )
        data["required_reach_all_partitions"][key] = {
            **{
                f"{a}_only": sorted(
                    sets[a] - set.union(*(sets[b] for b in "ABC" if b != a)),
                )
                for a in "ABC"
            },
            "common_all": sorted(set.intersection(*sets.values())),
            "missed_all": sorted(universe - set.union(*sets.values())),
        }
    return data
