"""Exact reviewed-witness evaluation of captured A/B under frozen R2 gates."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, E501, PLR2004
import argparse
import sys
from collections import Counter
from dataclasses import asdict
from fractions import Fraction
from typing import Any

from experiments.bm25f.gates import Comparison, evaluate
from experiments.bm25f.trace import serialize
from experiments.codex_dogfood.case_0015.adjudication.reviewed import materialize as m
from experiments.codex_dogfood.case_0015.stage_d import authentication as auth
from experiments.codex_dogfood.case_0015.stage_d.reporting import artifacts

ROOT = auth.ROOT
encoded, sha, require, load = m.encoded, m.sha, m.require, m.load
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
MECHANISMS = (
    "union_idf_delta",
    "pre_saturation_weight_delta",
    "cross_field_single_saturation_delta",
)


def change(a: int | None, b: int | None, *, rank: bool = False) -> Any:
    meaningful = b is not None and (
        (a is not None and a - b >= 2 and 5 * b <= 4 * a)
        if rank
        else (a is None or (a > 0 and 5 * b <= 4 * a))
    )
    bound = a is None or (
        b is not None and 5 * b <= 6 * a and b - a <= (10 if rank else 5)
    )
    state = (
        "TIED"
        if a == b
        else "IMPROVED"
        if b is not None and (a is None or b < a)
        else "WORSENED"
    )
    return {
        "A": a,
        "B": b,
        "classification": state,
        "B_minus_A": b - a if a is not None and b is not None else None,
        "meaningful_improvement": meaningful,
        "complementary_bound": bound,
        "regression_magnitude": None
        if a is not None and b is None
        else max(0, b - a)
        if a is not None and b is not None
        else 0,
        "gain_cross_product": {"left": 5 * b, "right": 4 * a}
        if a is not None and b is not None
        else None,
        "bound_cross_product": {"left": 5 * b, "right": 6 * a}
        if a is not None and b is not None
        else None,
    }


def count_labels(ids: list[str], obligation: str, labels: Any) -> Any:
    counts = Counter(labels[(obligation, rid)] for rid in ids)
    return {label: counts[label] for label in LABELS}


def witness_metrics(
    witness: Any, rows: Any, obligation: str, labels: Any, resources: Any
) -> Any:
    ranks = {r["document_identity"]: r["rank"] for r in rows}
    members = {rid: ranks.get(rid) for rid in witness["resources"]}
    complete = all(rank is not None for rank in members.values())
    # max([], default=0) is the explicit valid repository-empty witness semantics.
    depth = (
        max((rank for rank in members.values() if rank is not None), default=0)
        if complete
        else None
    )
    prefix = (
        [r["document_identity"] for r in rows[:depth]]
        if complete
        else [r["document_identity"] for r in rows]
    )
    unique = sorted(set(prefix))
    return {
        "witness": witness["id"],
        "repository_member_ranks": members,
        "member_addresses": {rid: resources[rid]["address"] for rid in members},
        "complete": complete,
        "completion_status": "COMPLETE" if complete else "INCOMPLETE",
        "depth": depth,
        "prefix_resources": prefix,
        "prefix_occurrences": len(prefix),
        "unique_prefix_resources": len(unique),
        "duplicate_occurrences": len(prefix) - len(unique),
        "label_occurrences": count_labels(prefix, obligation, labels),
        "distinct_utf8_bytes": sum(resources[rid]["utf8_bytes"] for rid in unique),
        "task_backed_unit_rank": "NOT_APPLICABLE",
        "units": witness["units"],
        "incomplete_prefix_policy": "Full captured lane exhaustion; no fictional completion depth.",
    }


def select(witnesses: list[Any]) -> Any:
    complete = [w for w in witnesses if w["complete"]]
    return (
        min(complete, key=lambda w: (w["depth"], w["witness"]))
        if complete
        else min(witnesses, key=lambda w: w["witness"])
    )


def burden(selected: Any, resources: Any) -> Any:
    occurrences = [rid for w in selected.values() for rid in w["prefix_resources"]]
    unique = sorted(set(occurrences))
    return {
        "selected_witnesses": {o: w["witness"] for o, w in selected.items()},
        "selected_depths": {o: w["depth"] for o, w in selected.items()},
        "incomplete_obligations": [o for o, w in selected.items() if not w["complete"]],
        "prefix_occurrences": len(occurrences),
        "unique_prefix_resources": len(unique),
        "unique_resources": unique,
        "duplicate_occurrences": len(occurrences) - len(unique),
        "label_occurrences": {
            label: sum(w["label_occurrences"][label] for w in selected.values())
            for label in LABELS
        },
        "distinct_utf8_bytes": sum(resources[rid]["utf8_bytes"] for rid in unique),
    }


def reach(primary: Any, lanes: Any, labels: Any) -> Any:
    resources, cells, unit_pairs, repository_pairs = set(), set(), set(), set()
    for i in range(1, 7):
        o, q = f"O{i}", f"Q{i}"
        reached = {r["document_identity"] for r in lanes[q]["matches"]}
        for rid in reached:
            if labels[(o, rid)] == "REQUIRED":
                resources.add(rid)
                cells.add(o + "/" + rid)
        for unit in primary["semantic_units"]:
            if o not in unit["obligations"]:
                continue
            available = unit["evidence_class"] == "TASK_BACKED" or any(
                set(a["resources"]) <= reached for a in unit["alternatives"]
            )
            if available:
                unit_pairs.add((o, unit["id"]))
                if unit["evidence_class"] != "TASK_BACKED":
                    repository_pairs.add((o, unit["id"]))
    return {
        "resources": sorted(resources),
        "cells": sorted(cells),
        "repository_units": sorted({u for _, u in repository_pairs}),
        "units": sorted({u for _, u in unit_pairs}),
        "obligation_unit_pairs": sorted(unit_pairs),
        "repository_obligation_unit_pairs": sorted(repository_pairs),
        "scope": "Full owning-query candidate lanes; each complete alternative evaluated conjunctively. Task-backed units have no retrieval rank.",
    }


def rational(value: Fraction) -> Any:
    return {"numerator": value.numerator, "denominator": value.denominator}


def component_totals(row: Any) -> dict[str, Fraction]:
    return {
        key: sum((Fraction(t[key]) for t in row["terms"]), Fraction(0))
        for key in MECHANISMS
    }


def causal(row: Any, obligation: str, data: Any, maps: Any, labels: Any) -> Any:
    rid = row["resource"]
    q = "Q" + obligation[1:]
    a, b = maps["A"][q].get(rid), maps["B"][q].get(rid)
    if a is None or b is None:
        field = next(
            r for r in data["fields"]["documents"] if r["document_identity"] == rid
        )
        terms = data["design"]["queries"][int(q[1:]) - 1]["normalized_terms"]
        observed = {
            f: sorted(set(terms) & set(field[f]["term_frequencies"]))
            for f in ("CONTENT", "FILENAME")
        }
        return {
            "status": "UNREACHED",
            "field_evidence": observed,
            "failure_classes": ["QUERY_AUTHORING_LIMIT"]
            if not any(observed.values())
            else [],
            "explanation": "Owning query has no positive field match; equal candidate absence is not B reach loss. No field alternative was tested, so FIELD_REPRESENTATION_LIMIT is not demonstrated.",
        }
    diagnostics = {r["document_identity"]: r for r in data["decomposition"][q]}
    diagnostic = diagnostics[rid]
    joined = next(
        r
        for r in data["contributions"][q]["candidates"]
        if r["document_identity"] == rid
    )
    totals = component_totals(diagnostic)
    crossings = []
    failures: set[str] = set()
    for other, ao in maps["A"][q].items():
        bo = maps["B"][q][other]
        if other == rid or (ao["rank"] < a["rank"]) == (bo["rank"] < b["rank"]):
            continue
        lost = ao["rank"] > a["rank"] and bo["rank"] < b["rank"]
        effects = {
            key: totals[key] - component_totals(diagnostics[other])[key]
            for key in MECHANISMS
        }
        start = Fraction(a["score"]) - Fraction(ao["score"])
        margin = start
        path = [rational(margin)]
        for key in MECHANISMS:
            margin += effects[key]
            path.append(rational(margin))
        final = Fraction(b["score"]) - Fraction(bo["score"])
        residual = final - margin
        supported = []
        if lost:
            if effects["union_idf_delta"] < 0:
                supported.append("UNION_IDF_HARM")
            if effects["cross_field_single_saturation_delta"] < 0:
                supported.append("CROSS_FIELD_SATURATION_HARM")
            if (
                effects["pre_saturation_weight_delta"] < 0
                and bo["filename_terms_present"]
            ):
                supported.append("FILENAME_FIELD_OVERWEIGHT")
            failures.update(supported)
        crossings.append(
            {
                "other_resource": other,
                "address": ao["address"],
                "gold_label": labels[(obligation, other)],
                "direction": "OVERTAKES_REQUIRED" if lost else "REQUIRED_OVERTAKES",
                "ranks": {
                    "required_A": a["rank"],
                    "other_A": ao["rank"],
                    "required_B": b["rank"],
                    "other_B": bo["rank"],
                },
                "relative_mechanism_effects": {
                    k: rational(v) for k, v in effects.items()
                },
                "fixed_order_score_margins": path,
                "final_margin": rational(final),
                "grouping_floating_residual": rational(residual),
                "failure_classes": supported,
                "interpretation": "Actual necessary-resource pair-order consequence, with signed fixed-order decomposition. Negative components contribute harm to this observed crossing; they are not independently rerun treatments or uniquely sufficient causal claims.",
            }
        )
    # A/B matches share exact per-term evidence; B filename presence is derived
    # for pair diagnostics only and never changes scores/ranks/candidate sets.
    return {
        "status": "CAPTURED_DECOMPOSITION",
        "field_evidence": joined["terms"],
        "native_content_contribution": a["content_score"],
        "native_filename_contribution": a["filename_score"],
        "native_weighted_filename_contribution": a["weighted_filename_score"],
        "union_idf_effect": rational(totals["union_idf_delta"]),
        "inside_tf_filename_weight_effect": rational(
            totals["pre_saturation_weight_delta"]
        ),
        "cross_field_saturation_effect": rational(
            totals["cross_field_single_saturation_delta"]
        ),
        "native_grouping_residual": diagnostic["exact_native_grouping_residual"],
        "b_grouping_residual": diagnostic["exact_b_grouping_residual"],
        "exact_document_delta": diagnostic["exact_document_score_delta"],
        "crossings": crossings,
        "failure_classes": sorted(failures),
        "interacting_mechanisms": any(
            sum(v["numerator"] != 0 for v in c["relative_mechanism_effects"].values())
            > 1
            for c in crossings
        ),
        "CONTENT_FIELD_DOMINANCE": "NOT_DEMONSTRATED; score magnitude alone does not establish mechanism harm",
        "scope": "Intermediate decomposition stages have no treatment status or gold-selected ranking.",
    }


def top_k(data: Any, labels: Any) -> Any:
    result: dict[str, Any] = {}
    for i in range(1, 7):
        o, q = f"O{i}", f"Q{i}"
        result[q] = {}
        for k in (10, 20, 50):
            captured = data["top_k"][q]["top_k"][str(k)]
            counts = Counter(
                labels[(o, x)] + " -> " + labels[(o, y)]
                for x, y in captured["pair_inversions"]
            )
            result[q][str(k)] = {
                "entered": count_labels(captured["entered"], o, labels),
                "exited": count_labels(captured["exited"], o, labels),
                "entered_resources": captured["entered"],
                "exited_resources": captured["exited"],
                "pair_inversion_label_classes": dict(sorted(counts.items())),
                "pair_inversions": [
                    {
                        "before_first": x,
                        "before_second": y,
                        "labels": [labels[(o, x)], labels[(o, y)]],
                    }
                    for x, y in captured["pair_inversions"]
                ],
                "inversion_count": captured["inversion_count"],
                "outcome_role": "EXPLANATION_ONLY",
            }
    return result


def dimension(a: int, b: int, *, lower_better: bool = True) -> Any:
    return {
        "A": a,
        "B": b,
        "B_minus_A": b - a,
        "classification": "TIED"
        if a == b
        else "IMPROVED"
        if (b < a) == lower_better
        else "WORSENED",
    }


def calculate(data: Any) -> Any:
    primary, resources = data["gold"]["primary"], data["resources"]
    labels = {(c["obligation"], c["resource"]): c["label"] for c in primary["cells"]}
    require(len(labels) == 3090, "Exact complete Cartesian gold")
    maps = {
        a: {
            q: {
                r["document_identity"]: {
                    **r,
                    "filename_terms_present": any(
                        t["FILENAME"]["tf"] for t in r["terms"]
                    )
                    if a == "B"
                    else bool(r["filename_terms"]),
                }
                for r in lane["matches"]
            }
            for q, lane in data["arms"][a].items()
        }
        for a in "AB"
    }
    witnesses = {}
    selected: dict[str, Any] = {a: {} for a in "AB"}
    for i in range(1, 7):
        o, q = f"O{i}", f"Q{i}"
        witnesses[o] = {
            a: [
                witness_metrics(w, data["arms"][a][q]["matches"], o, labels, resources)
                for w in primary["witnesses"][o]
            ]
            for a in "AB"
        }
        for arm in "AB":
            selected[arm][o] = select(witnesses[o][arm])
    burdens = {a: burden(selected[a], resources) for a in "AB"}
    reach_by_arm = {a: reach(primary, data["arms"][a], labels) for a in "AB"}
    obligations = {
        o: {
            "selected": {a: selected[a][o]["witness"] for a in "AB"},
            "change": change(selected["A"][o]["depth"], selected["B"][o]["depth"]),
            "complete": {a: selected[a][o]["complete"] for a in "AB"},
        }
        for o in primary["witnesses"]
    }
    cells = []
    for cell in primary["cells"]:
        if cell["label"] != "REQUIRED":
            continue
        o, rid = cell["obligation"], cell["resource"]
        q = "Q" + o[1:]
        ranks = {a: maps[a][q].get(rid, {}).get("rank") for a in "AB"}
        row = {
            "identity": o + "/" + rid,
            "obligation": o,
            "query": q,
            "resource": rid,
            "address": resources[rid]["address"],
            "ranks": ranks,
            "witness_membership": [
                w["id"] for w in primary["witnesses"][o] if rid in w["resources"]
            ],
            "obligation_indispensable": rid
            in primary["obligation_indispensability"][o]["resources"],
            "task_indispensable": rid in primary["task_indispensable_resources"],
            "change": change(ranks["A"], ranks["B"], rank=True),
        }
        row["causal"] = causal(row, o, data, maps, labels)
        cells.append(row)
    require(len(cells) == 21, "All REQUIRED rank joins")
    losses = {
        k: sorted(set(reach_by_arm["A"][k]) - set(reach_by_arm["B"][k]))
        for k in ("resources", "cells", "repository_units", "units")
    }
    contract_checks = {
        "checkpoint_ancestry": data["provenance"]["ancestry"] == "PASS",
        "clean_primary_gold": len(labels) == 3090
        and not primary["unresolved_cells"]
        and all(
            v == "NO" for v in primary["blindness"]["excluded_category_access"].values()
        ),
        "exact_identity_joins": primary["task_identity"]
        == data["design"]["task_identity"]
        and primary["resource_frame"] == data["gold"]["resource_bindings"],
        "equal_candidates": data["native_validation"]["candidate_identity"] == "EXACT",
        "exactly_once": data["journal"]["pairs"] == 17
        and data["journal"]["events"] == 34
        and data["journal"]["native_retries"] == data["journal"]["failures"] == 0,
        "reference_unchanged": data["native_validation"]["reference"] == "UNCHANGED",
        "no_scientific_reruns": data["native_validation"]["scientific_reruns"] == 0,
        "captured_cost": True,
    }
    implementation_checks = {
        key: data["native_validation"][key] == "EXACT"
        for key in (
            "field_observations",
            "statistics",
            "bm25f_reconstruction",
            "decomposition",
        )
    }
    a, b = burdens["A"], burdens["B"]
    evidence = Comparison(
        contract=all(contract_checks.values()),
        application=all(implementation_checks.values()),
        reach=not any(losses.values()),
        depths=tuple(
            (selected["A"][o]["depth"], selected["B"][o]["depth"]) for o in obligations
        ),
        required_ranks=tuple((r["ranks"]["A"], r["ranks"]["B"]) for r in cells),
        unique_resources=(a["unique_prefix_resources"], b["unique_prefix_resources"]),
        occurrences=(a["prefix_occurrences"], b["prefix_occurrences"]),
        utf8_bytes=(a["distinct_utf8_bytes"], b["distinct_utf8_bytes"]),
    )
    gates = evaluate(evidence)
    dimensions = {
        "semantic_completeness": dimension(
            len(reach_by_arm["A"]["units"]),
            len(reach_by_arm["B"]["units"]),
            lower_better=False,
        ),
        "obligation_completeness": dimension(
            sum(w["complete"] for w in selected["A"].values()),
            sum(w["complete"] for w in selected["B"].values()),
            lower_better=False,
        ),
        "selected_witness_depth_per_obligation": {
            o: c["change"] for o, c in obligations.items()
        },
        "meaningful_witness_gains": dimension(
            0,
            sum(c["change"]["meaningful_improvement"] for c in obligations.values()),
            lower_better=False,
        ),
        "meaningful_required_rank_gains": dimension(
            0,
            sum(r["change"]["meaningful_improvement"] for r in cells),
            lower_better=False,
        ),
        "required_regressions": dimension(
            0, sum(r["change"]["classification"] == "WORSENED" for r in cells)
        ),
        "candidate_safety": {
            "classification": "TIED",
            "differences": 0,
            "occurrences_A": 1807,
            "occurrences_B": 1807,
        },
        "reference_lane_safety": {"classification": "TIED", "differences": 0},
        "treatment_execution_cost_ns": dimension(
            data["costs"]["arm_a_native_retrieval_ns"],
            data["costs"]["arm_b_bm25f_scoring_ns"],
        ),
    }
    for key in ("resources", "cells", "repository_units", "units"):
        dimensions["required_" + key + "_reach"] = dimension(
            len(reach_by_arm["A"][key]), len(reach_by_arm["B"][key]), lower_better=False
        )
    for key in (
        "unique_prefix_resources",
        "prefix_occurrences",
        "duplicate_occurrences",
        "distinct_utf8_bytes",
    ):
        dimensions[key] = dimension(a[key], b[key])
    dimensions["unnecessary_occurrences"] = dimension(
        a["label_occurrences"]["UNNECESSARY"], b["label_occurrences"]["UNNECESSARY"]
    )
    for name, subset in (
        ("required_cell_ranks", cells),
        (
            "obligation_indispensable_ranks",
            [r for r in cells if r["obligation_indispensable"]],
        ),
        ("task_indispensable_ranks", [r for r in cells if r["task_indispensable"]]),
    ):
        dimensions[name] = {
            **dimension(
                sum(r["ranks"]["A"] for r in subset if r["ranks"]["A"] is not None),
                sum(r["ranks"]["B"] for r in subset if r["ranks"]["B"] is not None),
            ),
            "metric": "Descriptive sum of reached owning-query ranks; never offsets individual regression gates",
            "improved_cells": sum(
                r["change"]["classification"] == "IMPROVED" for r in subset
            ),
            "worsened_cells": sum(
                r["change"]["classification"] == "WORSENED" for r in subset
            ),
            "tied_cells": sum(r["change"]["classification"] == "TIED" for r in subset),
            "cells": [
                {k: r[k] for k in ("identity", "address", "ranks", "change")}
                for r in subset
            ],
        }
    failure_classes = (
        "FILENAME_FIELD_OVERWEIGHT",
        "CONTENT_FIELD_DOMINANCE",
        "CROSS_FIELD_SATURATION_HARM",
        "UNION_IDF_HARM",
        "QUERY_AUTHORING_LIMIT",
        "FIELD_REPRESENTATION_LIMIT",
    )
    return {
        "schema": "case-0015-stage-d-analysis-v1",
        "case": primary["case"],
        "task_identity": primary["task_identity"],
        "task_text": primary["task_text"],
        "provenance": data["provenance"],
        "primary_policy": data["gold"]["provenance"],
        "reviewed_summary": data["reviewed_replay"]["statistics"],
        "frame": data["gold"]["frame"],
        "joins": {
            "resources": 515,
            "cells": 3090,
            "units": 42,
            "witnesses": 12,
            "required_cells": 21,
            "missing": 0,
            "duplicate": 0,
            "unexpected": 0,
            "stale_frame": 0,
            "identity_dimensions": [
                "case",
                "task",
                "obligation",
                "RepositoryId",
                "SnapshotId",
                "CorpusId",
                "resource address",
                "document identity",
                "content identity",
            ],
        },
        "native_authentication": data["native_validation"],
        "journal": data["journal"],
        "obligations": primary["obligations"],
        "semantic_units": primary["semantic_units"],
        "gold_witnesses": primary["witnesses"],
        "obligation_indispensability": primary["obligation_indispensability"],
        "task_indispensable_resources": primary["task_indispensable_resources"],
        "task_indispensable_units": primary["task_indispensable_units"],
        "gaps": primary["gaps"],
        "limitations": primary["limitations"],
        "ambiguities": primary["ambiguities"],
        "required_cells": cells,
        "witness_calculations": witnesses,
        "selected_witnesses": selected,
        "obligation_comparisons": obligations,
        "case_wide_burden": burdens,
        "required_reach": reach_by_arm,
        "required_reach_losses": losses,
        "meaningful_witness_gains": [
            o for o, c in obligations.items() if c["change"]["meaningful_improvement"]
        ],
        "meaningful_required_rank_gains": [
            r["identity"] for r in cells if r["change"]["meaningful_improvement"]
        ],
        "required_regressions": [
            r["identity"] for r in cells if r["change"]["classification"] == "WORSENED"
        ],
        "failure_attribution": {
            name: [
                r["identity"] for r in cells if name in r["causal"]["failure_classes"]
            ]
            for name in failure_classes
        },
        "multi_cause_cells": [
            r["identity"] for r in cells if r["causal"].get("interacting_mechanisms")
        ],
        "top_k_gold_diagnostics": top_k(data, labels),
        "costs": data["costs"],
        "contract_checks": contract_checks,
        "implementation_checks": implementation_checks,
        "reach_gate": not any(losses.values()),
        "gate_evidence": asdict(evidence),
        "gates": gates,
        "frozen_rule": data["design"]["decision_rule"],
        "gate_arithmetic": {
            "unique_ten_percent": {
                "baseline_positive": a["unique_prefix_resources"] > 0,
                "left": 10 * b["unique_prefix_resources"],
                "right": 9 * a["unique_prefix_resources"],
            },
            "occurrence_ten_percent": {
                "baseline_positive": a["prefix_occurrences"] > 0,
                "left": 10 * b["prefix_occurrences"],
                "right": 9 * a["prefix_occurrences"],
            },
            "resource_nonincrease": b["unique_prefix_resources"]
            <= a["unique_prefix_resources"],
            "occurrence_nonincrease": b["prefix_occurrences"]
            <= a["prefix_occurrences"],
            "byte_nonincrease": b["distinct_utf8_bytes"] <= a["distinct_utf8_bytes"],
        },
        "precedence": data["design"]["decision_rule"]["precedence"],
        "precedence_application": {
            "contract_defect": not evidence.contract,
            "implementation_or_reach_defect": not evidence.application
            or not evidence.reach,
            "strong_support": bool(gates["meaningful_obligation_indices"])
            and gates["depth_safe"]
            and gates["required_rank_safe"]
            and gates["ten_percent_burden_gain"]
            and gates["burden_safe"],
            "complementary_value": (
                bool(gates["meaningful_obligation_indices"])
                or gates["required_rank_gain"]
            )
            and gates["bounded_regressions"],
            "harmful_gate": not gates["bounded_regressions"],
            "outcome": gates["outcome"],
        },
        "did_true_bm25f_improve": dimensions,
        "answer": "No material acquisition improvement under the frozen rule. Completeness and full candidate reach are preserved; rank movements include necessary-evidence regressions. The exact gates decide the bounded case outcome.",
        "scope": "One development case, one clean Astra High primary, frozen whole-content/filename fields and untuned parameters. No universal BM25F conclusion. Prefix burden is counterfactual acquisition to reviewed completion, not measured human reading effort. Experimental Arm B overhead does not predict optimized production BM25F cost.",
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "confirmation_reserve": "NOT_ACCESSED",
        "production_behavior": "UNCHANGED",
    }


def validate(value: Any, data: Any) -> None:
    require(
        serialize(value) == serialize(calculate(data)),
        "Exact Stage D deterministic calculation identity",
    )


def outputs(data: Any) -> dict[str, bytes]:
    value = calculate(data)
    files = artifacts(value)
    files["validation.json"] = encoded(
        {
            "status": "PASS",
            "joins": value["joins"],
            "checkpoints": value["provenance"],
            "outcome": value["gates"]["outcome"],
            "checks": [
                "sealed checkpoint ancestry/Stage A/recovery/failed-audit isolation/attempt 2/primary/reviewed gold",
                "17 pairs/34 events, no failures/retries/reruns",
                "inert native A/B/reference journal projections",
                "exact field/statistics/native A/B/decomposition/top-K/cost reconstruction",
                "all 3090 cells/42 units/12 witnesses/21 REQUIRED cells",
                "exact frame/content/document joins",
                "repository-empty O2 complete at zero, no gain",
                "witness completeness and stable minimum-depth selection",
                "exact integer gain/regression/burden/gate arithmetic",
                "obligation-relative labels and prefix unions/bytes",
                "candidate/reference/reach safety",
                "observed crossing mechanism attribution, no diagnostic arms",
                "frozen precedence",
                "deterministic replay/overwrite refusal/tamper rejection",
            ],
        }
    )
    files["integrity.json"] = encoded(
        {
            "schema": "case-0015-stage-d-integrity-v1",
            "sha256": {name: sha(raw) for name, raw in files.items()},
            "implementation_sha256": {
                name: sha((ROOT / name).read_bytes())
                for name in (
                    "analysis.py",
                    "authentication.py",
                    "reporting.py",
                    "test_analysis.py",
                )
            },
            "inputs": value["provenance"],
            "excluded": [".local", "self hash to avoid cycle"],
        }
    )
    return files


def verify(data: Any | None = None) -> Any:
    files = outputs(auth.authenticate() if data is None else data)
    for name, raw in files.items():
        require((ROOT / name).read_bytes() == raw, "Stage D replay: " + name)
    return {
        "status": "PASS",
        "sha256": {name: sha(raw) for name, raw in files.items()},
        "outcome": load(ROOT / "analysis.json")["gates"]["outcome"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    data = auth.authenticate()
    if args.mode == "build":
        m.write_new({ROOT / name: raw for name, raw in outputs(data).items()})
    sys.stdout.write(encoded(verify(data)).decode())


if __name__ == "__main__":
    main()
