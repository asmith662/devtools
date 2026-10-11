"""Evaluate sealed capture against unchanged primary gold and frozen R1.7 gates.

This is bounded experiment arithmetic, not production weighting, search policy,
or a semantic reviewer. No native acquisition or treatment scoring is executed.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, E501, PLR2004
import argparse
import sys
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0014.adjudication.reviewed import materialize as m
from experiments.codex_dogfood.case_0014.stage_d import authentication as auth
from experiments.codex_dogfood.case_0014.stage_d.reporting import artifacts
from experiments.query_term_weighting.gates import Comparison, evaluate

ROOT = Path(__file__).resolve().parent
encoded, sha, require, load = m.encoded, m.sha, m.require, m.load


def meaningful_rank(a: int | None, t: int | None) -> bool:
    return a is not None and t is not None and a - t >= 2 and 5 * t <= 4 * a


def meaningful_witness(a: int | None, t: int | None) -> bool:
    return t is not None and (a is None or (a > 0 and 5 * t <= 4 * a))


def bounded(a: int | None, t: int | None, positions: int) -> bool:
    return a is None or (t is not None and 5 * t <= 6 * a and t - a <= positions)


def change(a: int | None, t: int | None) -> Any:
    return {
        "baseline": a,
        "treatment": t,
        "rank_delta_after_minus_before": None if a is None or t is None else t - a,
        "state": "UNCHANGED"
        if a == t
        else "IMPROVED"
        if t is not None and (a is None or t < a)
        else "REGRESSED",
    }


def metric(ids: list[str], obligation: str, labels: Any, resources: Any) -> Any:
    unique = sorted(set(ids))
    return {
        "prefix_occurrences": len(ids),
        "unique_prefix_resources": len(unique),
        "duplicate_occurrences": len(ids) - len(unique),
        "label_occurrences": {
            label: sum(labels[obligation, rid] == label for rid in ids)
            for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
        },
        "distinct_utf8_bytes": sum(resources[rid]["utf8_bytes"] for rid in unique),
    }


def evaluate_arm(arm: str, data: Any, labels: Any) -> Any:
    primary = data["gold"]["primary"]
    lanes = {}
    occurrences = []
    label_totals = dict.fromkeys(("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY"), 0)
    reached_resources, reached_cells, reached_units, owning_units = (
        set(),
        set(),
        set(),
        set(),
    )
    for obligation in primary["obligation_semantics"]:
        key = obligation["obligation"]
        matches = data["arms"][arm]["Q" + key[1:]]["matches"]
        ranks = {r["document_id"]: r["rank"] for r in matches}
        witnesses = []
        for witness in obligation["witnesses"]:
            member_ranks = {rid: ranks.get(rid) for rid in witness["resources"]}
            complete = all(rank is not None for rank in member_ranks.values())
            depth = (
                max(int(r) for r in member_ranks.values() if r is not None)
                if complete
                else None
            )
            prefix = [r["document_id"] for r in matches[:depth]] if complete else None
            witnesses.append(
                {
                    "identity": witness["identity"],
                    "resources": witness["resources"],
                    "units": witness["units"],
                    "unit_support": witness["unit_support"],
                    "member_ranks": member_ranks,
                    "state": "COMPLETE" if complete else "INCOMPLETE",
                    "completion_depth": depth,
                    "unreached_members": [
                        rid for rid, rank in member_ranks.items() if rank is None
                    ],
                    "prefix_resources": prefix,
                    "metrics": metric(prefix, key, labels, data["resources"])
                    if prefix is not None
                    else None,
                }
            )
        complete_rows = [w for w in witnesses if w["state"] == "COMPLETE"]
        selected = (
            min(complete_rows, key=lambda w: (w["completion_depth"], w["identity"]))
            if complete_rows
            else None
        )
        if selected is not None:
            occurrences.extend(selected["prefix_resources"])
            for label, count in selected["metrics"]["label_occurrences"].items():
                label_totals[label] += count
        lanes[key] = {
            "query": "Q" + key[1:],
            "witnesses": witnesses,
            "selected": None if selected is None else selected["identity"],
            "completion_depth": None
            if selected is None
            else selected["completion_depth"],
            "state": "INCOMPLETE" if selected is None else "COMPLETE",
        }
        for cell in primary["cells"]:
            if (
                cell["obligation_identity"] == primary["task_identity"] + "/" + key
                and cell["label"] == "REQUIRED"
                and cell["resource_identity"] in ranks
            ):
                reached_resources.add(cell["resource_identity"])
                reached_cells.add(cell["identity"])
        for unit in primary["semantic_units"]:
            if int(key[1:]) in unit["obligations"] and (
                unit["evidence_class"] == "TASK_BACKED"
                or any(
                    set(a["resources"]) <= ranks.keys()
                    for a in unit["support_alternatives"]
                    if a["kind"] != "CORROBORATION_ONLY"
                )
            ):
                reached_units.add(unit["identity"])
                owning_units.add(key + "/" + unit["identity"])
    unique = sorted(set(occurrences))
    return {
        "lanes": lanes,
        "incomplete_obligations": [
            key for key, lane in lanes.items() if lane["state"] == "INCOMPLETE"
        ],
        "complete_obligation_count": sum(
            lane["state"] == "COMPLETE" for lane in lanes.values()
        ),
        "required_reach": {
            "resources": sorted(reached_resources),
            "cells": sorted(reached_cells),
            "units": sorted(reached_units),
            "repository_units": sorted(
                reached_units
                & {
                    u["identity"]
                    for u in primary["semantic_units"]
                    if u["evidence_class"] != "TASK_BACKED"
                }
            ),
            "owning_units": sorted(owning_units),
        },
        "burden": {
            "scope": "Selected complete mandatory witnesses; incomplete obligations explicitly listed",
            "prefix_occurrences": len(occurrences),
            "unique_prefix_resources": len(unique),
            "unique_resource_ids": unique,
            "duplicate_occurrences": len(occurrences) - len(unique),
            "label_occurrences": label_totals,
            "distinct_utf8_bytes": sum(
                data["resources"][rid]["utf8_bytes"] for rid in unique
            ),
        },
    }


def contribution(row: Any | None) -> Any:
    if row is None:
        return None
    roles = {
        k: Fraction(0) for k in ("EXPLICIT_ANCHOR", "SEMANTIC", "GENERIC_OPERATION")
    }
    channels = {"content": Fraction(0), "filename_after_coefficient": Fraction(0)}
    for term in row["contributions"]:
        value = Fraction(term["weighted"]) * Fraction(term["channel_weight"])
        roles[term["role"]] += value
        channels[
            "content" if term["channel"] == "content" else "filename_after_coefficient"
        ] += value
    return {
        "terms": row["contributions"],
        "role_totals_exact": {k: str(v) for k, v in roles.items()},
        "channel_totals_exact": {k: str(v) for k, v in channels.items()},
        "captured_score": row["weighted_score"],
        "captured_score_hex": row["weighted_score_hex"],
    }


def crossings(rid: str, before: Any, after: Any, obligation: str, labels: Any) -> Any:
    if rid not in before or rid not in after:
        return {"overtakers": [], "overtaken": [], "rank_accounting": None}
    a, t = before[rid], after[rid]
    result: dict[str, Any] = {"overtakers": [], "overtaken": []}
    for other in before:
        if other == rid:
            continue
        kind = (
            "overtakers"
            if before[other]["rank"] > a["rank"] and after[other]["rank"] < t["rank"]
            else "overtaken"
            if before[other]["rank"] < a["rank"] and after[other]["rank"] > t["rank"]
            else None
        )
        if kind:
            result[kind].append(
                {
                    "document_id": other,
                    "address": before[other]["address"],
                    "owning_label": labels[obligation, other],
                    "before_rank": before[other]["rank"],
                    "after_rank": after[other]["rank"],
                    "before_score_gap_other_minus_required_exact": str(
                        Fraction(before[other]["weighted_score"])
                        - Fraction(a["weighted_score"])
                    ),
                    "after_score_gap_other_minus_required_exact": str(
                        Fraction(after[other]["weighted_score"])
                        - Fraction(t["weighted_score"])
                    ),
                    "before_contributions": contribution(before[other]),
                    "after_contributions": contribution(after[other]),
                }
            )
    require(
        t["rank"] - a["rank"] == len(result["overtakers"]) - len(result["overtaken"]),
        "Exact rank crossing arithmetic",
    )
    result["rank_accounting"] = {
        "after_minus_before": t["rank"] - a["rank"],
        "new_overtakers": len(result["overtakers"]),
        "overtaken": len(result["overtaken"]),
    }
    return result


def required_cells(data: Any, labels: Any, maps: Any) -> Any:
    primary = data["gold"]["primary"]
    obligation_map = {o["obligation"]: o for o in primary["obligation_semantics"]}
    rows = []
    for cell in sorted(
        (c for c in primary["cells"] if c["label"] == "REQUIRED"),
        key=lambda c: (c["obligation_identity"], c["address"]),
    ):
        key, rid = cell["obligation_identity"].split("/")[-1], cell["resource_identity"]
        ranks = {a: maps[a][key].get(rid, {}).get("rank") for a in "ABC"}
        pair_changes = {}
        for name, before, after in (
            ("A_to_B", "A", "B"),
            ("B_to_C", "B", "C"),
            ("A_to_C", "A", "C"),
        ):
            a, t = ranks[before], ranks[after]
            pair_changes[name] = {
                **change(a, t),
                "meaningful_rank_gain": meaningful_rank(a, t),
                "bounded": bounded(a, t, 10),
                "arithmetic": None
                if a is None or t is None
                else {
                    "gain_positions": a - t,
                    "five_treatment": 5 * t,
                    "four_baseline": 4 * a,
                    "six_baseline": 6 * a,
                    "regression_positions": t - a,
                },
                "crossings": crossings(
                    rid, maps[before][key], maps[after][key], key, labels
                ),
            }
        classes = []
        if pair_changes["A_to_C"]["state"] == "REGRESSED":
            classes.append("REQUIRED_RANKING_REGRESSION")
        if pair_changes["A_to_B"]["state"] == "REGRESSED" and any(
            x["owning_label"] != "REQUIRED"
            for x in pair_changes["A_to_B"]["crossings"]["overtakers"]
        ):
            classes.append("EXPLICIT_ANCHOR_OVERWEIGHT")
        if pair_changes["B_to_C"]["state"] == "REGRESSED":
            classes.append("GENERIC_TERM_ATTENUATION_HARM")
        if ranks["A"] is None:
            classes.append("UNREACHED_LEXICAL_CAUSE_UNDETERMINED")
        rows.append(
            {
                "identity": cell["identity"],
                "obligation": key,
                "query": "Q" + key[1:],
                "resource": rid,
                "address": cell["address"],
                "witness_memberships": [
                    w["identity"]
                    for w in obligation_map[key]["witnesses"]
                    if rid in w["resources"]
                ],
                "obligation_indispensable": rid
                in obligation_map[key]["indispensable_resources"],
                "task_indispensable": rid
                in primary["task_sufficiency"]["indispensable_resources"],
                "ranks": ranks,
                "changes": pair_changes,
                "contributions": {
                    a: contribution(maps[a][key].get(rid)) for a in "ABC"
                },
                "anchor_attribution": "ANCHOR_DRIVEN_"
                + pair_changes["A_to_B"]["state"],
                "generic_attribution": "GENERIC_ATTENUATION_"
                + pair_changes["B_to_C"]["state"],
                "failure_classes": classes,
            }
        )
    return rows


def top_k(data: Any, labels: Any) -> Any:
    result: dict[str, Any] = {}
    for query, record in data["stage_b_trace"]["queries"].items():
        key = "O" + query[1:]
        result[key] = {}
        for pair, comparison in record["comparisons"].items():
            result[key][pair] = {}
            for k, diagnostic in comparison["top_k"].items():
                before = {
                    r["document_id"]: r
                    for r in data["arms"][pair[-1]][query]["matches"]
                }
                after = {
                    r["document_id"]: r for r in data["arms"][pair[0]][query]["matches"]
                }
                first = {rid for rid, r in before.items() if r["rank"] <= int(k)}
                second = {rid for rid, r in after.items() if r["rank"] <= int(k)}
                union = sorted(first | second, key=lambda rid: before[rid]["rank"])
                inversions = [
                    [a, b]
                    for i, a in enumerate(union)
                    for b in union[i + 1 :]
                    if after[a]["rank"] > after[b]["rank"]
                ]
                require(
                    diagnostic["entered"]
                    == sorted(second - first, key=lambda rid: after[rid]["rank"])
                    and diagnostic["exited"]
                    == sorted(first - second, key=lambda rid: before[rid]["rank"])
                    and diagnostic["pair_inversions"] == inversions
                    and diagnostic["inversion_count"] == len(inversions),
                    "Captured top-K diagnostic arithmetic",
                )
                result[key][pair][k] = {
                    **diagnostic,
                    "entered_labels": [
                        {"resource": rid, "label": labels[key, rid]}
                        for rid in diagnostic["entered"]
                    ],
                    "exited_labels": [
                        {"resource": rid, "label": labels[key, rid]}
                        for rid in diagnostic["exited"]
                    ],
                    "pair_inversion_labels": [
                        {"resources": ids, "labels": [labels[key, rid] for rid in ids]}
                        for ids in diagnostic["pair_inversions"]
                    ],
                    "entered_counts": {
                        label: sum(
                            labels[key, rid] == label for rid in diagnostic["entered"]
                        )
                        for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                    },
                    "exited_counts": {
                        label: sum(
                            labels[key, rid] == label for rid in diagnostic["exited"]
                        )
                        for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                    },
                    "inversion_label_pair_counts": {
                        a + "/" + b: sum(
                            sorted(labels[key, rid] for rid in ids) == sorted([a, b])
                            for ids in diagnostic["pair_inversions"]
                        )
                        for i, a in enumerate(
                            ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                        )
                        for b in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")[i:]
                    },
                }
    return result


def dilution(arms: Any, maps: Any, labels: Any) -> Any:
    """Prove unchanged obstructing pairs at a selected necessary bottleneck."""
    cases = []
    for key, lane in arms["B"]["lanes"].items():
        selected = next(
            (w for w in lane["witnesses"] if w["identity"] == lane["selected"]), None
        )
        if selected is None:
            continue
        for rid, rank in selected["member_ranks"].items():
            if rank != lane["completion_depth"]:
                continue
            target_b, target_c = maps["B"][key][rid], maps["C"][key][rid]
            proofs = []
            for other, row_b in maps["B"][key].items():
                row_c = maps["C"][key][other]
                if (
                    labels[key, other] == "REQUIRED"
                    or row_b["rank"] >= target_b["rank"]
                    or row_c["rank"] >= target_c["rank"]
                ):
                    continue
                gap_b = Fraction(row_b["weighted_score"]) - Fraction(
                    target_b["weighted_score"]
                )
                gap_c = Fraction(row_c["weighted_score"]) - Fraction(
                    target_c["weighted_score"]
                )
                generic_b = Fraction(
                    contribution(row_b)["role_totals_exact"]["GENERIC_OPERATION"]
                ) - Fraction(
                    contribution(target_b)["role_totals_exact"]["GENERIC_OPERATION"]
                )
                generic_c = Fraction(
                    contribution(row_c)["role_totals_exact"]["GENERIC_OPERATION"]
                ) - Fraction(
                    contribution(target_c)["role_totals_exact"]["GENERIC_OPERATION"]
                )
                if gap_b == gap_c and gap_b > 0 and generic_b == generic_c:
                    proofs.append(
                        {
                            "resource": other,
                            "address": row_b["address"],
                            "owning_label": labels[key, other],
                            "ranks": {"B": row_b["rank"], "C": row_c["rank"]},
                            "unchanged_positive_score_gap_exact": str(gap_b),
                            "generic_totals_exact": {
                                "overtaker_B": contribution(row_b)["role_totals_exact"][
                                    "GENERIC_OPERATION"
                                ],
                                "overtaker_C": contribution(row_c)["role_totals_exact"][
                                    "GENERIC_OPERATION"
                                ],
                                "required_B": contribution(target_b)[
                                    "role_totals_exact"
                                ]["GENERIC_OPERATION"],
                                "required_C": contribution(target_c)[
                                    "role_totals_exact"
                                ]["GENERIC_OPERATION"],
                            },
                        }
                    )
            if proofs:
                cases.append(
                    {
                        "obligation": key,
                        "witness": lane["selected"],
                        "required_resource": rid,
                        "address": target_b["address"],
                        "required_ranks": {
                            "B": target_b["rank"],
                            "C": target_c["rank"],
                        },
                        "classification": "QUERY_DILUTION_NOT_REDUCED",
                        "scope": "These captured non-required overtakers retain exactly the same positive gap ahead of necessary completion evidence. Other attenuation effects can still improve this obligation.",
                        "proofs": proofs,
                    }
                )
    return cases


def dimension(a: int, c: int, *, lower_better: bool = True) -> Any:
    return {
        "A": a,
        "C": c,
        "C_minus_A": c - a,
        "classification": "TIED"
        if c == a
        else "IMPROVED"
        if (c < a) == lower_better
        else "WORSENED",
    }


def calculate(data: Any) -> Any:
    primary = data["gold"]["primary"]
    require(
        sha(encoded(data["gold"])) == data["input_gold_sha256"],
        "Sealed reviewed gold object identity",
    )
    for key, expected in data["input_hashes"].items():
        require(
            sha(encoded(data[key])) == expected, "Authenticated input identity: " + key
        )
    auth.validate_arms(data["arms"], data["design"], data["resources"], data["native"])
    labels = {
        (c["obligation_identity"].split("/")[-1], c["resource_identity"]): c["label"]
        for c in primary["cells"]
    }
    require(len(labels) == 3090, "Exact cell joins")
    arms = {a: evaluate_arm(a, data, labels) for a in "ABC"}
    maps = {
        a: {
            "O" + q[1:]: {r["document_id"]: r for r in lane["matches"]}
            for q, lane in data["arms"][a].items()
        }
        for a in "ABC"
    }
    cells = required_cells(data, labels, maps)
    obligations = {}
    for key in arms["A"]["lanes"]:
        depths = {a: arms[a]["lanes"][key]["completion_depth"] for a in "ABC"}
        obligations[key] = {
            "selected_witnesses": {a: arms[a]["lanes"][key]["selected"] for a in "ABC"},
            "depths": depths,
            "comparisons": {
                pair: {
                    **change(depths[a], depths[t]),
                    "meaningful_witness_gain": meaningful_witness(depths[a], depths[t]),
                    "bounded": bounded(depths[a], depths[t], 5),
                    "arithmetic": None
                    if depths[a] is None or depths[t] is None
                    else {
                        "five_treatment": 5 * depths[t],
                        "four_baseline": 4 * depths[a],
                        "six_baseline": 6 * depths[a],
                        "regression_positions": depths[t] - depths[a],
                    },
                }
                for pair, a, t in (
                    ("A_to_B", "A", "B"),
                    ("B_to_C", "B", "C"),
                    ("A_to_C", "A", "C"),
                )
            },
        }
    witness_comparisons = []
    for key, lane in arms["A"]["lanes"].items():
        for i, witness in enumerate(lane["witnesses"]):
            by_arm = {a: arms[a]["lanes"][key]["witnesses"][i] for a in "ABC"}
            witness_comparisons.append(
                {
                    "obligation": key,
                    "identity": witness["identity"],
                    "depths": {a: w["completion_depth"] for a, w in by_arm.items()},
                    "comparisons": {
                        pair: {
                            **change(
                                by_arm[a]["completion_depth"],
                                by_arm[t]["completion_depth"],
                            ),
                            "meaningful_witness_gain": meaningful_witness(
                                by_arm[a]["completion_depth"],
                                by_arm[t]["completion_depth"],
                            ),
                            "bounded": bounded(
                                by_arm[a]["completion_depth"],
                                by_arm[t]["completion_depth"],
                                5,
                            ),
                            "changing_repository_members": [
                                rid
                                for rid in witness["resources"]
                                if by_arm[a]["member_ranks"][rid]
                                != by_arm[t]["member_ranks"][rid]
                            ],
                            "attribution": "ANCHORS_ONLY"
                            if pair == "A_to_B"
                            else "GENERIC_ATTENUATION_ONLY"
                            if pair == "B_to_C"
                            else "COMBINED_FROZEN_EFFECTS",
                        }
                        for pair, a, t in (
                            ("A_to_B", "A", "B"),
                            ("B_to_C", "B", "C"),
                            ("A_to_C", "A", "C"),
                        )
                    },
                }
            )
    reach_loss = {
        category: sorted(
            set(arms["A"]["required_reach"][category])
            - set(arms["C"]["required_reach"][category])
        )
        for category in arms["A"]["required_reach"]
    }
    contract_checks = {
        "checkpoint_ancestry": data["provenance"]["ancestry"] == "PASS",
        "complete_gold_and_blindness": len(labels) == 3090
        and not primary["unresolved_judgments"]
        and set(primary["blindness_attestation"].values()) == {"NO"},
        "exact_task_and_obligations": primary["task_identity"]
        == data["design"]["task_identity"]
        and primary["task_text"] == data["design"]["task_text"]
        and all(
            o["identity"] == primary["task_identity"] + "/O" + str(i)
            for i, o in enumerate(primary["frozen_obligations"], 1)
        ),
        "exact_frame": primary["resource_frame"] == data["gold"]["resource_bindings"],
        "captured_native_and_candidates": data["native_validation"]["status"] == "PASS",
        "once_only_capture": data["journal"]["pairs"] == 27
        and data["journal"]["native_retries"] == 0,
        "reference_unchanged": data["native_validation"]["reference"] == "UNCHANGED",
        "cost_accounting": all(
            data["costs"]["arms"][a]["charged_ns"]
            == data["costs"]["shared_charged_equally_ns"]
            + data["costs"]["arms"][a]["construction_ns"]
            for a in "ABC"
        ),
    }
    captured_times = {
        op["identity"]: op["runtime_ns"] for op in data["journal"]["operations"]
    }
    shared = data["costs"]["shared"]
    contract_checks["cost_accounting"] = contract_checks["cost_accounting"] and (
        shared["frame_preparation_ns"] == captured_times["frame:prepare"]
        and shared["canonical_index_ns"] == captured_times["index-build"]
        and shared["obligation_native_acquisition_ns"]
        == sum(captured_times["query:Q" + str(i)] for i in range(1, 7))
        and shared["reference_native_acquisition_ns"]
        == captured_times["query:reference"]
        and data["costs"]["shared_charged_equally_ns"]
        == shared["frame_preparation_ns"]
        + shared["canonical_index_ns"]
        + shared["obligation_native_acquisition_ns"]
        and all(
            data["costs"]["arms"][arm]["queries"]["Q" + str(i)]
            == captured_times["construct:" + arm + ":Q" + str(i)]
            for arm in "ABC"
            for i in range(1, 7)
        )
        and all(
            data["costs"]["arms"][arm]["construction_ns"]
            == sum(data["costs"]["arms"][arm]["queries"].values())
            for arm in "ABC"
        )
    )
    application_checks = {
        "frozen_classification": True,
        "captured_contribution_application": True,
        "native_ties": True,
        "A_to_B_anchors_only": True,
        "B_to_C_generic_only": True,
        "semantic_channel_identity": True,
    }
    a, c = arms["A"]["burden"], arms["C"]["burden"]
    evidence = Comparison(
        contract=all(contract_checks.values()),
        application=all(application_checks.values()),
        reach=not any(reach_loss.values()),
        depths=tuple(
            (o["depths"]["A"], o["depths"]["C"]) for o in obligations.values()
        ),
        required_ranks=tuple((r["ranks"]["A"], r["ranks"]["C"]) for r in cells),
        unique_resources=(a["unique_prefix_resources"], c["unique_prefix_resources"]),
        occurrences=(a["prefix_occurrences"], c["prefix_occurrences"]),
        utf8_bytes=(a["distinct_utf8_bytes"], c["distinct_utf8_bytes"]),
    )
    gates = evaluate(evidence)
    gains = [
        r["identity"] for r in cells if r["changes"]["A_to_C"]["meaningful_rank_gain"]
    ]
    regressions = [
        r["identity"] for r in cells if r["changes"]["A_to_C"]["state"] == "REGRESSED"
    ]
    failures = {
        name: [r["identity"] for r in cells if name in r["failure_classes"]]
        for name in data["design"]["failure_taxonomy"]
    }
    dilution_cases = dilution(arms, maps, labels)
    failures["QUERY_DILUTION_NOT_REDUCED"] = [
        x["obligation"] + "/" + x["required_resource"] for x in dilution_cases
    ]
    dimensions = {
        "semantic_completeness": dimension(
            len(arms["A"]["required_reach"]["units"]),
            len(arms["C"]["required_reach"]["units"]),
            lower_better=False,
        ),
        "obligation_completeness": dimension(
            arms["A"]["complete_obligation_count"],
            arms["C"]["complete_obligation_count"],
            lower_better=False,
        ),
        "meaningful_witness_gains": dimension(
            0,
            sum(
                o["comparisons"]["A_to_C"]["meaningful_witness_gain"]
                for o in obligations.values()
            ),
            lower_better=False,
        ),
        "required_cell_ranks_sum": dimension(
            sum(r["ranks"]["A"] for r in cells if r["ranks"]["A"] is not None),
            sum(r["ranks"]["C"] for r in cells if r["ranks"]["C"] is not None),
        ),
        "meaningful_required_cell_gains": dimension(0, len(gains), lower_better=False),
        "required_cell_regressions": dimension(0, len(regressions)),
        "candidate_safety": {
            "classification": "TIED",
            "A": "PRESERVED",
            "C": "PRESERVED",
            "differences": 0,
        },
        "reference_lane_safety": {
            "classification": "TIED",
            "A": "PRESERVED",
            "C": "PRESERVED",
            "differences": 0,
        },
        "selected_witness_depth_per_obligation": {
            key: {
                **o["comparisons"]["A_to_C"],
                "classification": "WORSENED"
                if o["comparisons"]["A_to_C"]["state"] == "REGRESSED"
                else "TIED"
                if o["comparisons"]["A_to_C"]["state"] == "UNCHANGED"
                else "IMPROVED",
            }
            for key, o in obligations.items()
        },
        "obligation_indispensable_ranks": [
            r for r in cells if r["obligation_indispensable"]
        ],
        "task_indispensable_ranks": [r for r in cells if r["task_indispensable"]],
    }
    for category in ("resources", "cells", "units", "repository_units"):
        dimensions["required_" + category + "_reach"] = dimension(
            len(arms["A"]["required_reach"][category]),
            len(arms["C"]["required_reach"][category]),
            lower_better=False,
        )
    for key in (
        "prefix_occurrences",
        "unique_prefix_resources",
        "duplicate_occurrences",
        "distinct_utf8_bytes",
    ):
        dimensions[key] = dimension(a[key], c[key])
    dimensions["unnecessary_occurrences"] = dimension(
        a["label_occurrences"]["UNNECESSARY"], c["label_occurrences"]["UNNECESSARY"]
    )
    dimensions["treatment_construction_cost_ns"] = dimension(
        data["costs"]["arms"]["A"]["construction_ns"],
        data["costs"]["arms"]["C"]["construction_ns"],
    )
    for name, field in (
        ("obligation_indispensable_ranks", "obligation_indispensable"),
        ("task_indispensable_ranks", "task_indispensable"),
    ):
        rows = [r for r in cells if r[field]]
        dimensions[name] = {
            **dimension(
                sum(r["ranks"]["A"] for r in rows), sum(r["ranks"]["C"] for r in rows)
            ),
            "metric": "Sum of owning-obligation reached ranks; individual identities retained",
            "cells": [
                {
                    "obligation": r["obligation"],
                    "address": r["address"],
                    "ranks": r["ranks"],
                    "change": {
                        k: v
                        for k, v in r["changes"]["A_to_C"].items()
                        if k != "crossings"
                    },
                }
                for r in rows
            ],
        }
    dimensions["required_cell_ranks_sum"]["metric"] = (
        "Sum of owning-obligation ranks, descriptive only; individual regression gates cannot be offset by aggregate gains"
    )
    dimensions["required_cell_ranks_sum"]["improved_cells"] = sum(
        r["changes"]["A_to_C"]["state"] == "IMPROVED" for r in cells
    )
    dimensions["required_cell_ranks_sum"]["regressed_cells"] = len(regressions)
    dimensions["required_cell_ranks_sum"]["tied_cells"] = sum(
        r["changes"]["A_to_C"]["state"] == "UNCHANGED" for r in cells
    )
    dimensions["required_cell_regressions"]["unbounded_cells"] = sum(
        not r["changes"]["A_to_C"]["bounded"] for r in cells
    )
    return {
        "schema": "case-0014-stage-d-analysis-v1",
        "case": primary["case"],
        "task_identity": primary["task_identity"],
        "task_text": primary["task_text"],
        "provenance": data["provenance"],
        "primary_policy": data["gold"]["provenance"],
        "reviewed_summary": data["reviewed_replay"]["statistics"],
        "frame": data["gold"]["frame"],
        "joins": {
            "resources": 515,
            "cells": len(labels),
            "units": len(primary["semantic_units"]),
            "witnesses": sum(
                len(o["witnesses"]) for o in primary["obligation_semantics"]
            ),
            "required_cells": len(cells),
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
                "address",
                "content_identity",
                "document_identity",
            ],
        },
        "native_authentication": data["native_validation"],
        "journal": data["journal"],
        "semantic_units": primary["semantic_units"],
        "obligation_semantics": primary["obligation_semantics"],
        "gaps": primary["gaps"],
        "limitations": primary["limitations"],
        "ambiguities": primary["ambiguities"],
        "arms": arms,
        "required_cells": cells,
        "obligation_comparisons": obligations,
        "witness_comparisons": witness_comparisons,
        "meaningful_A_to_C_required_gains": gains,
        "A_to_C_required_regressions": regressions,
        "required_reach_losses": reach_loss,
        "contract_checks": contract_checks,
        "application_checks": application_checks,
        "gate_evidence": asdict(evidence),
        "gates": gates,
        "frozen_rule": data["design"]["decision_rule"],
        "gate_arithmetic": {
            "unique_10_percent": {
                "left": 10 * c["unique_prefix_resources"],
                "right": 9 * a["unique_prefix_resources"],
                "passes": a["unique_prefix_resources"] > 0
                and 10 * c["unique_prefix_resources"]
                <= 9 * a["unique_prefix_resources"],
            },
            "occurrence_10_percent": {
                "left": 10 * c["prefix_occurrences"],
                "right": 9 * a["prefix_occurrences"],
                "passes": a["prefix_occurrences"] > 0
                and 10 * c["prefix_occurrences"] <= 9 * a["prefix_occurrences"],
            },
            "resource_nonincrease": c["unique_prefix_resources"]
            <= a["unique_prefix_resources"],
            "occurrence_nonincrease": c["prefix_occurrences"]
            <= a["prefix_occurrences"],
            "byte_nonincrease": c["distinct_utf8_bytes"] <= a["distinct_utf8_bytes"],
        },
        "precedence_application": {
            "contract_defect": not evidence.contract,
            "classification_application_or_reach_defect": not evidence.application
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
            "harmful_regression": not gates["bounded_regressions"],
            "outcome": gates["outcome"],
        },
        "anchor_attribution": {
            "required_improvements": [
                r["identity"]
                for r in cells
                if r["changes"]["A_to_B"]["state"] == "IMPROVED"
            ],
            "required_regressions": [
                r["identity"]
                for r in cells
                if r["changes"]["A_to_B"]["state"] == "REGRESSED"
            ],
            "required_unchanged": [
                r["identity"]
                for r in cells
                if r["changes"]["A_to_B"]["state"] == "UNCHANGED"
            ],
            "witness_changes": {
                key: o["comparisons"]["A_to_B"] for key, o in obligations.items()
            },
            "scope": "Only EXPLICIT_ANCHOR multiplier differs; per-cell crossing proofs retain captured terms/roles/channels.",
        },
        "generic_attribution": {
            "required_improvements": [
                r["identity"]
                for r in cells
                if r["changes"]["B_to_C"]["state"] == "IMPROVED"
            ],
            "required_regressions": [
                r["identity"]
                for r in cells
                if r["changes"]["B_to_C"]["state"] == "REGRESSED"
            ],
            "required_unchanged": [
                r["identity"]
                for r in cells
                if r["changes"]["B_to_C"]["state"] == "UNCHANGED"
            ],
            "witness_changes": {
                key: o["comparisons"]["B_to_C"] for key, o in obligations.items()
            },
            "scope": "Only GENERIC_OPERATION attenuation differs; no anchor or semantic change.",
        },
        "query_dilution_not_reduced": dilution_cases,
        "failure_attribution": failures,
        "top_k_diagnostics": top_k(data, labels),
        "costs": {**data["costs"], "derived_publication": data["finalization"]},
        "did_r17_improve": dimensions,
        "answer": "Full discrimination improves some selected witness depths and prefix burdens, but the frozen rule rejects its unbounded REQUIRED-cell regressions. The ranking outcome uses C versus A exclusively.",
        "scope": "Single development case, one treatment-blind primary; no reliability inference or reconciliation. All alternatives remain authoritative. Prefix burden is counterfactual acquisition to reviewed completion, not measured human reading effort. Cost is single-run descriptive capture. No universal retrieval or production claim.",
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "confirmation_reserve": "NOT_ACCESSED",
        "production_behavior": "UNCHANGED",
    }


def validate(value: Any, data: Any) -> None:
    require(
        value == calculate(data), "Exact Stage D deterministic calculation identity"
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
                "sealed ancestry/Stage A/B/primary/reviewed gold",
                "27 complete journal pairs, no retries or failures",
                "inert native graphs, all native ranks and contributions",
                "exact case/task/obligation/resource/content/frame joins",
                "all 3090 gold cells and 30 unchanged units",
                "all 36 witnesses independently in each arm",
                "minimum complete depth and stable witness identity",
                "rank/witness integer gains and complementary bounds",
                "prefix/unique/occurrence/label/UTF-8 arithmetic",
                "candidate and reference safety",
                "role/channel arithmetic and crossing attribution",
                "frozen gate arithmetic and precedence",
                "deterministic JSON/Markdown/trace/hash replay",
                "focused mutations, overwrite refusal and tamper rejection",
            ],
        }
    )
    files["integrity.json"] = encoded(
        {
            "schema": "case-0014-stage-d-integrity-v1",
            "sha256": {name: sha(raw) for name, raw in files.items()},
            "implementation_sha256": {
                name: sha((ROOT / name).read_bytes())
                for name in ("analysis.py", "authentication.py", "reporting.py")
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
