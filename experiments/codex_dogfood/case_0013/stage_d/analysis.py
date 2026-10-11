"""Evaluate authenticated capture against unchanged gold and prospective U3 gates."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812, C901
import argparse
import sys
from dataclasses import asdict
from typing import Any

from experiments.codex_dogfood.case_0013.adjudication.reviewed import materialize
from experiments.codex_dogfood.case_0013.stage_d import authentication as auth
from experiments.codex_dogfood.case_0013.stage_d.reporting import artifacts
from experiments.mechanism_routing.gates import GateEvidence, evaluate

encoded, sha, require, load = auth.encoded, auth.sha, auth.require, auth.load
ROOT = auth.ROOT
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")


def prefix_metrics(prefixes: Any, labels: Any, resources: Any) -> Any:
    unique = sorted({a for rows in prefixes.values() for a in rows})
    composition = dict.fromkeys(LABELS, 0)
    for ob, rows in prefixes.items():
        for address in rows:
            composition[labels[ob, address]] += 1
    occurrences = sum(map(len, prefixes.values()))
    return {
        "prefixes": prefixes,
        "prefix_occurrences": occurrences,
        "unique_prefix_resources": unique,
        "unique_prefix_count": len(unique),
        "duplicate_occurrences": occurrences - len(unique),
        "label_occurrences": composition,
        "unique_utf8_bytes": sum(
            len(resources[a]["text"].encode("utf-8")) for a in unique
        ),
    }


def completion(witness: Any, order: list[str], resource_addresses: Any) -> Any:
    resources = [resource_addresses[r] for r in witness["resources"]]
    ranks = {r: order.index(r) + 1 if r in order else None for r in resources}
    missing = [r for r, rank in ranks.items() if rank is None]
    depth = (
        None
        if missing
        else max((rank for rank in ranks.values() if rank is not None), default=0)
    )
    return {
        "identity": witness["identity"],
        "source_resource_identities": witness["resources"],
        "resources": resources,
        "units": witness["units"],
        "member_depths": ranks,
        "missing_resources": missing,
        "completion_depth": depth,
        "bottlenecks": []
        if depth is None
        else [r for r, rank in ranks.items() if rank == depth],
    }


def evaluate_arm(arm: str, data: Any, labels: Any) -> Any:
    primary = data["gold"]["primary"]
    addresses = {r["identity"]: r["address"] for r in primary["resources"]}
    prefixes = {}
    lanes = {}
    reach_resources: set[str] = set()
    reach_cells: set[str] = set()
    reach_units: set[str] = set()
    reach_owning_units: set[str] = set()
    for ob in primary["obligations"]:
        key = ob["key"]
        rows = data["arms"][arm][key]["rows" if arm == "A" else "entries"]
        order = [r["address"] for r in rows]
        require(
            len(order) == len(set(order)),
            "Duplicate treatment resource occurrence within lane",
        )
        for row in rows:
            require(
                row["content_identity"]
                == data["resources"][row["address"]]["content_identity"],
                "Exact row content join",
            )
        alternatives = []
        for witness in ob["witnesses"]:
            result = completion(witness, order, addresses)
            depth = result["completion_depth"]
            result["metrics"] = (
                None
                if depth is None
                else prefix_metrics({key: order[:depth]}, labels, data["resources"])
            )
            alternatives.append(result)
        complete = [w for w in alternatives if w["completion_depth"] is not None]
        selected = (
            min(complete, key=lambda w: (w["completion_depth"], w["identity"]))
            if complete
            else None
        )
        prefixes[key] = (
            [] if selected is None else order[: selected["completion_depth"]]
        )
        lanes[key] = {
            "all_witnesses": alternatives,
            "selected": selected,
            "completion_depth": None
            if selected is None
            else selected["completion_depth"],
            "complete_witness_count": len(complete),
            "applicability": ob["applicability_decision"],
            "indispensable_resources": [
                addresses[r] for r in ob["indispensable_resources"]
            ],
        }
        for cell in primary["cells"]:
            if (
                cell["obligation"] == ob["identity"]
                and cell["label"] == "REQUIRED"
                and cell["address"] in order
            ):
                reach_resources.add(cell["address"])
                reach_cells.add(cell["identity"])
        for unit in primary["semantic_units"]:
            if key not in unit["obligations"]:
                continue
            available = unit["evidence_class"] == "TASK_BACKED" or any(
                {addresses[r] for r in alternative["resources"]} <= set(order)
                for alternative in unit["support_alternatives"]
            )
            if available:
                reach_units.add(unit["identity"])
                reach_owning_units.add(key + ":" + unit["identity"])
    all_complete = all(lane["completion_depth"] is not None for lane in lanes.values())
    return {
        "lanes": lanes,
        "task_complete": all_complete,
        "complete_obligation_count": sum(
            lane["completion_depth"] is not None for lane in lanes.values()
        ),
        "selected_prefix_burden": prefix_metrics(prefixes, labels, data["resources"])
        if all_complete
        else None,
        "required_reach": {
            "resources": sorted(reach_resources),
            "cells": sorted(reach_cells),
            "units": sorted(reach_units),
            "owning_units": sorted(reach_owning_units),
        },
        "semantic_completeness": "All mandatory witnesses complete"
        if all_complete
        else "Incomplete mandatory witness coverage",
    }


def preservation(data: Any) -> Any:
    checks = {}
    for arm in "BC":
        for ob in data["gold"]["primary"]["obligations"]:
            key = ob["key"]
            native = data["lexical"][key]["rows"]
            entries = data["arms"][arm][key]["entries"]
            by_address = {e["address"]: e for e in entries}
            positives = all(
                r["address"] in by_address
                and by_address[r["address"]]["native_rank"] == r["rank"]
                and by_address[r["address"]]["score"] == r["score"]
                and by_address[r["address"]]["content_identity"]
                == r["content_identity"]
                and by_address[r["address"]]["native_row_reference"]
                == {"lane": key, "rank": r["rank"]}
                for r in native
            )
            promoted = [
                e["address"] for e in entries if e["exact_tier_position"] is not None
            ]
            targets = []
            resolved = sorted(
                [
                    h
                    for h in data["summary"]["hint_rows"]
                    if h["arm"] == arm
                    and h["obligation"] == key
                    and h["disposition"] == "RESOLVED"
                ],
                key=lambda h: (
                    h["span"]["start"],
                    h["span"]["end"],
                    h["request_identity"],
                ),
            )
            for row in resolved:
                for target in row["targets"]:
                    if target["address"] not in targets:
                        targets.append(target["address"])
            expected = targets + [
                r["address"] for r in native if r["address"] not in targets
            ]
            checks[arm + ":" + key] = {
                "all_native_positives_rank_score_content": positives,
                "complete_fallback_order": [e["address"] for e in entries] == expected,
                "exact_candidates_preserved": promoted == targets,
                "unique_entries": len(by_address) == len(entries),
                "positions": [e["position"] for e in entries]
                == list(range(1, len(entries) + 1)),
                "contributions": "Exact unchanged native_row_reference into authenticated complete lexical rows",
            }
    global_safety = (
        data["summary"]["global_safety"] == "PRESERVED"
        and data["native_validation"]["status"] == "PASS"
    )
    return {
        "lanes": checks,
        "global_safety": global_safety,
        "valid": global_safety
        and all(
            all(v for k, v in row.items() if k != "contributions")
            for row in checks.values()
        ),
    }


def hint_classification(data: Any, arms: Any, labels: Any) -> list[Any]:
    primary, t = data["gold"]["primary"], data["treatment"]
    cells = {
        (c["obligation"].split("/")[-1], c["address"]): c for c in primary["cells"]
    }
    resources = {r["address"]: r for r in primary["resources"]}
    rows = []
    for hint in t["hint_inventory"]:
        identity = hint["key"]
        native = {
            h["arm"]: h for h in data["summary"]["hint_rows"] if h["hint"] == identity
        }
        b = native["B"]
        key = b["obligation"]
        target = b["targets"][0] if b["targets"] else None
        witnesses = primary["obligations"][
            [o["key"] for o in primary["obligations"]].index(key)
        ]["witnesses"]
        a_selected, b_selected, c_selected = [
            arms[a]["lanes"][key]["selected"] for a in "ABC"
        ]
        improves = b_selected is not None and (
            a_selected is None
            or b_selected["completion_depth"] < a_selected["completion_depth"]
        )
        effect = {
            "A_witness": None if a_selected is None else a_selected["identity"],
            "B_witness": None if b_selected is None else b_selected["identity"],
            "C_witness": None if c_selected is None else c_selected["identity"],
            "A_depth": None if a_selected is None else a_selected["completion_depth"],
            "B_depth": None if b_selected is None else b_selected["completion_depth"],
            "C_depth": None if c_selected is None else c_selected["completion_depth"],
            "B_improves_selected_completion": improves,
            "pre_promotion_bottlenecks": []
            if a_selected is None
            else a_selected["bottlenecks"],
            "post_promotion_bottlenecks": []
            if b_selected is None
            else b_selected["bottlenecks"],
        }
        if target:
            address = target["address"]
            resource_id = resources[address]["identity"]
            label = labels[key, address]
            membership = [
                w["identity"] for w in witnesses if resource_id in w["resources"]
            ]
            all_task_membership = [
                w["identity"]
                for o in primary["obligations"]
                for w in o["witnesses"]
                if resource_id in w["resources"]
            ]
            obligation = next(o for o in primary["obligations"] if o["key"] == key)
            indispensable = resource_id in obligation["indispensable_resources"]
            selected_member = (
                b_selected is not None and address in b_selected["resources"]
            )
            participation = (
                selected_member
                and improves
                and (a_selected is None or address in a_selected["bottlenecks"])
            )
            attribution = (
                "REQUIRED_WITNESS_IMPROVING"
                if label == "REQUIRED" and participation
                else "SELECTED_ROUTE_NOT_COMPLETION_BOTTLENECK"
                if label == "REQUIRED"
                else "SELECTED_ROUTE_TARGET_NOT_REQUIRED"
            )
            units = cells[key, address]["units"]
        else:
            label, address, indispensable, membership, all_task_membership, units = (
                None,
                None,
                None,
                [],
                [],
                [],
            )
            participation = False
            attribution = "UNRESOLVED_ROUTE"
        c_invoked = "C" in native
        candidates = [
            candidate
            for account in b["native_accounts"]
            for candidate in account["candidates"]
        ]
        nonresolution_avoided = (
            not c_invoked and b["disposition"] == "UNRESOLVED" and not candidates
        )
        route_miss = (
            not c_invoked
            and b["disposition"] == "RESOLVED"
            and label == "REQUIRED"
            and (
                address
                not in {
                    target["address"]
                    for h in data["summary"]["hint_rows"]
                    if h["arm"] == "C" and h["obligation"] == key
                    for target in h["targets"]
                }
                or (
                    improves
                    and (
                        c_selected is None
                        or c_selected["completion_depth"]
                        > b_selected["completion_depth"]
                    )
                )
            )
        )
        rows.append(
            {
                "hint": identity,
                "text": b["text"],
                "frozen_role": b["role"],
                "family": b["family"],
                "obligation": key,
                "B_admission": True,
                "C_admission": c_invoked,
                "B_native_disposition": b["disposition"],
                "C_native_disposition": native["C"]["disposition"]
                if c_invoked
                else "NOT_INVOKED",
                "C_policy_disposition": "EXACT_PLUS_LEXICAL"
                if c_invoked
                else "LEXICAL_ONLY",
                "B_native_candidates": candidates,
                "B_targets": b["targets"],
                "C_targets": native["C"]["targets"] if c_invoked else [],
                "C_native_invocations": int(c_invoked),
                "resolved_resource": address,
                "qualified_resource_binding": None
                if address is None
                else next(
                    r
                    for r in data["gold"]["resource_bindings"]
                    if r["address"] == address
                ),
                "reviewed_label": label,
                "reviewed_units": units,
                "native_rank": None if target is None else target["native_rank"],
                "native_lexical_miss": None
                if target is None
                else target["native_rank"] is None,
                "exact_tier_position": None
                if target is None
                else target["exact_tier_position"],
                "routed_position": None
                if target is None
                else target["routed_position"],
                "depth_saved": None if target is None else target["depth_saved"],
                "obligation_witness_membership": membership,
                "any_complete_task_witness_membership": all_task_membership,
                "obligation_indispensable": indispensable,
                "selected_witness_effect": effect,
                "selected_improving_participant": participation,
                "failure_or_nonvalue_attribution": attribution,
                "route_selection_miss": route_miss,
                "low_value_avoided_subtype": "genuine native nonresolution"
                if nonresolution_avoided
                else None,
                "scope": "Obligation-relative captured outcome; future destinations have no invented existing target",
                "route_ns": {
                    a: native[a]["runtime_ns"] if a in native else 0 for a in "BC"
                },
            }
        )
    return rows


def delta(b: int, c: int, *, lower_better: bool = True) -> Any:
    change = c - b
    return {
        "B": b,
        "C": c,
        "C_minus_B": change,
        "classification": "TIED"
        if change == 0
        else "IMPROVED"
        if (change < 0) == lower_better
        else "WORSENED",
    }


def calculate(data: Any) -> Any:
    primary = data["gold"]["primary"]
    labels = {
        (c["obligation"].split("/")[-1], c["address"]): c["label"]
        for c in primary["cells"]
    }
    arms = {a: evaluate_arm(a, data, labels) for a in "ABC"}
    preserved = preservation(data)
    hints = hint_classification(data, arms, labels)
    b, c = arms["B"], arms["C"]
    meaningful = []
    obligation_checks = {}
    for key, lane in b["lanes"].items():
        a_depth, b_depth, c_depth = [
            arms[a]["lanes"][key]["completion_depth"] for a in "ABC"
        ]
        b_complete = b_depth is not None
        c_complete = c_depth is not None
        obligation_checks[key] = {
            "B_complete": b_complete,
            "C_complete": c_complete,
            "completion_preserved": not b_complete or c_complete,
            "depth_safe": not b_complete or (c_complete and c_depth <= b_depth),
            "unique_prefix_safe": not b_complete
            or (
                c_complete
                and c["lanes"][key]["selected"]["metrics"]["unique_prefix_count"]
                <= lane["selected"]["metrics"]["unique_prefix_count"]
            ),
            "A_depth": a_depth,
            "B_depth": b_depth,
            "C_depth": c_depth,
            "A_selected_witness": None
            if arms["A"]["lanes"][key]["selected"] is None
            else arms["A"]["lanes"][key]["selected"]["identity"],
            "B_selected_witness": None
            if lane["selected"] is None
            else lane["selected"]["identity"],
            "C_selected_witness": None
            if c["lanes"][key]["selected"] is None
            else c["lanes"][key]["selected"]["identity"],
            "meaningful_cross_product": None
            if a_depth is None or b_depth is None
            else {"five_B": 5 * b_depth, "four_A": 4 * a_depth},
        }
        gain = b_complete and (
            a_depth is None or (a_depth > 0 and 5 * b_depth <= 4 * a_depth)
        )
        if gain:
            meaningful.append(
                {
                    "obligation": key,
                    **obligation_checks[key],
                    "C_preserves_gain": c_complete and c_depth <= b_depth,
                    "exact_promoted_evidence": [
                        h
                        for h in hints
                        if h["obligation"] == key
                        and h["B_native_disposition"] == "RESOLVED"
                    ],
                    "pre_promotion_bottlenecks": []
                    if arms["A"]["lanes"][key]["selected"] is None
                    else arms["A"]["lanes"][key]["selected"]["bottlenecks"],
                    "post_promotion_bottlenecks": lane["selected"]["bottlenecks"],
                }
            )
    reach_loss = {
        baseline: {
            category: sorted(
                set(arms[baseline]["required_reach"][category])
                - set(c["required_reach"][category])
            )
            for category in ("resources", "cells", "units", "owning_units")
        }
        for baseline in "AB"
    }
    reach_safe = (
        not any(
            loss for categories in reach_loss.values() for loss in categories.values()
        )
        and preserved["valid"]
    )
    obligation_safe = all(
        all(
            row[k] for k in ("completion_preserved", "depth_safe", "unique_prefix_safe")
        )
        for row in obligation_checks.values()
    )
    soundness = {
        "frozen_task_only_policy": data["policy"]
        == {a: data["treatment"]["route_decisions"][a] for a in "BC"},
        "literal_locators": all(
            data["treatment"]["task_text"][h["span"]["start"] : h["span"]["end"]]
            == h["text"]
            for h in data["summary"]["hint_rows"]
        ),
        "uniquely_native_resolved_promotions": all(
            (len(h["targets"]) == 1)
            if h["disposition"] == "RESOLVED"
            else not h["targets"]
            for h in data["summary"]["hint_rows"]
        ),
        "no_fabricated_owner": all(
            h["qualified_resource_binding"] is not None
            for h in hints
            if h["resolved_resource"] is not None
        ),
        "frozen_role_admission": all(
            h["C_admission"] == (h["frozen_role"] == "INSPECT_EXISTING") for h in hints
        ),
    }
    costs = data["costs"]["arms"]
    invocations = {a: sum(h[a + "_admission"] for h in hints) for a in "BC"}
    burden_b, burden_c = b["selected_prefix_burden"], c["selected_prefix_burden"]
    contract_checks = {
        "checkpoint_frame_task_query_integrity": data["provenance"]["ancestry"]
        == "PASS",
        "blindness": set(primary["blindness_attestation"].values()) == {"NO"},
        "task_interpretation": not any(
            g["present"]
            for g in primary["gaps"]
            if g["category"] == "TASK_INTERPRETATION_GAP"
        ),
        "complete_gold_cells": len(primary["cells"])
        == len(primary["resources"]) * len(primary["obligations"]),
        "native_match_fallback_global": preserved["valid"],
        "cost_disclosure": all(
            costs[a]["mechanism_ns"]
            == costs[a]["route_ns"] + costs[a]["presentation_ns"]
            for a in "ABC"
        ),
        "complete_B_C_baselines": b["task_complete"] and c["task_complete"],
    }
    require(
        burden_b is not None and burden_c is not None,
        "Required selected completion accounting is unassessable; scientific contract defect",
    )
    positive = (
        invocations["C"] < invocations["B"]
        or costs["C"]["mechanism_ns"] < costs["B"]["mechanism_ns"]
        or any(
            c["lanes"][key]["completion_depth"] < b["lanes"][key]["completion_depth"]
            for key in b["lanes"]
        )
        or any(
            burden_c[k] < burden_b[k]
            for k in ("unique_prefix_count", "prefix_occurrences", "unique_utf8_bytes")
        )
        or burden_c["label_occurrences"]["UNNECESSARY"]
        < burden_b["label_occurrences"]["UNNECESSARY"]
    )
    evidence = GateEvidence(
        contract_valid=all(contract_checks.values()),
        router_sound=all(soundness.values()),
        reach_safe=reach_safe,
        obligation_safe=obligation_safe,
        preserves_b_gains=all(g["C_preserves_gain"] for g in meaningful),
        b_meaningful_gain_count=len(meaningful),
        invocations_b=invocations["B"],
        invocations_c=invocations["C"],
        mechanism_ns_b=costs["B"]["mechanism_ns"],
        mechanism_ns_c=costs["C"]["mechanism_ns"],
        charged_ns_b=costs["B"]["charged_ns"],
        charged_ns_c=costs["C"]["charged_ns"],
        unique_b=burden_b["unique_prefix_count"],
        unique_c=burden_c["unique_prefix_count"],
        bytes_b=burden_b["unique_utf8_bytes"],
        bytes_c=burden_c["unique_utf8_bytes"],
        positive_selective_value=positive,
    )
    gates = evaluate(evidence)
    arithmetic = {
        "invocations_25_percent": {
            "left": 4 * invocations["C"],
            "operator": "<=",
            "right": 3 * invocations["B"],
        },
        "mechanism_10_percent": {
            "left": 10 * costs["C"]["mechanism_ns"],
            "operator": "<=",
            "right": 9 * costs["B"]["mechanism_ns"],
        },
        "charged_within_5_percent": {
            "left": 20 * costs["C"]["charged_ns"],
            "operator": "<=",
            "right": 21 * costs["B"]["charged_ns"],
        },
        "unique_prefix_10_percent": {
            "left": 10 * burden_c["unique_prefix_count"],
            "operator": "<=",
            "right": 9 * burden_b["unique_prefix_count"],
        },
        "bytes_nonincrease": {
            "left": burden_c["unique_utf8_bytes"],
            "operator": "<=",
            "right": burden_b["unique_utf8_bytes"],
        },
        "charged_nonincrease": {
            "left": costs["C"]["charged_ns"],
            "operator": "<=",
            "right": costs["B"]["charged_ns"],
        },
    }
    for values in arithmetic.values():
        values["passes"] = values["left"] <= values["right"]
    families = {}
    for family in data["summary"]["families"]["B"]:
        family_hints = [h for h in hints if h["family"] == family]
        families[family] = {
            "B": data["summary"]["families"]["B"][family],
            "C": data["summary"]["families"]["C"][family],
            "gold_effects": [
                {
                    k: h[k]
                    for k in (
                        "hint",
                        "reviewed_label",
                        "reviewed_units",
                        "obligation_witness_membership",
                        "selected_witness_effect",
                        "selected_improving_participant",
                        "low_value_avoided_subtype",
                        "route_ns",
                    )
                }
                for h in family_hints
            ],
            "presentation_cost_scope": "Shared full lane timings are descriptive and overlap across families; do not sum.",
        }
    dimensions = {
        "semantic_completeness": delta(
            b["complete_obligation_count"],
            c["complete_obligation_count"],
            lower_better=False,
        ),
        "obligation_completeness": delta(
            b["complete_obligation_count"],
            c["complete_obligation_count"],
            lower_better=False,
        ),
        "meaningful_B_gains_retained": {
            "classification": "TIED" if evidence.preserves_b_gains else "WORSENED",
            "B": len(meaningful),
            "C": sum(g["C_preserves_gain"] for g in meaningful),
        },
        "exact_request_count": delta(invocations["B"], invocations["C"]),
        "native_nonresolving_calls": delta(
            sum(h["B_native_disposition"] == "UNRESOLVED" for h in hints),
            sum(h["C_native_disposition"] == "UNRESOLVED" for h in hints),
        ),
        "global_safety": {"classification": "TIED", "B": "PRESERVED", "C": "PRESERVED"},
        "witness_completion_depth": {
            "classification": "TIED"
            if all(x["B_depth"] == x["C_depth"] for x in obligation_checks.values())
            else "IMPROVED"
            if obligation_safe
            else "WORSENED",
            "B": {k: v["B_depth"] for k, v in obligation_checks.items()},
            "C": {k: v["C_depth"] for k, v in obligation_checks.items()},
        },
        "search_policy": {"classification": "NOT_ASSESSED"},
    }
    for category in ("resources", "cells", "units", "owning_units"):
        dimensions["required_" + category + "_reach"] = delta(
            len(b["required_reach"][category]),
            len(c["required_reach"][category]),
            lower_better=False,
        )
    for key in ("route_ns", "presentation_ns", "mechanism_ns", "charged_ns"):
        dimensions[key] = delta(costs["B"][key], costs["C"][key])
    for key in (
        "unique_prefix_count",
        "prefix_occurrences",
        "duplicate_occurrences",
        "unique_utf8_bytes",
    ):
        dimensions[key] = delta(burden_b[key], burden_c[key])
    dimensions["unnecessary_occurrences"] = delta(
        burden_b["label_occurrences"]["UNNECESSARY"],
        burden_c["label_occurrences"]["UNNECESSARY"],
    )
    attribution: dict[str, list[str]] = {
        name: [] for name in data["treatment"]["failure_taxonomy"]
    }
    for h in hints:
        if h["failure_or_nonvalue_attribution"] in attribution:
            attribution[h["failure_or_nonvalue_attribution"]].append(h["hint"])
        if h["route_selection_miss"]:
            attribution["ROUTE_SELECTION_MISS"].append(h["hint"])
    return {
        "schema": "case-0013-stage-d-analysis-v1",
        "case": primary["case"],
        "task_identity": primary["task_identity"],
        "task_text": primary["task_text"],
        "provenance": data["provenance"],
        "primary_policy": data["gold"]["provenance"],
        "reviewed_summary": data["reviewed_replay"]["statistics"],
        "frame": data["gold"]["frame"],
        "joins": {
            "resources": len(primary["resources"]),
            "cells": len(primary["cells"]),
            "units": len(primary["semantic_units"]),
            "witnesses": sum(len(o["witnesses"]) for o in primary["obligations"]),
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
            ],
        },
        "native_authentication": {
            "lexical": data["native_validation"],
            "exact": data["native_exact_validation"],
        },
        "journal": data["journal"],
        "arms": arms,
        "hints": hints,
        "skipped_routes": [h for h in hints if not h["C_admission"]],
        "families": families,
        "meaningful_B_gains": meaningful,
        "preservation": preserved,
        "required_reach_losses": reach_loss,
        "contract_checks": contract_checks,
        "soundness_checks": soundness,
        "obligation_safety_checks": obligation_checks,
        "gate_evidence": asdict(evidence),
        "gates": gates,
        "gate_arithmetic": arithmetic,
        "frozen_rule": data["treatment"]["decision_rule"],
        "precedence_application": {
            "contract_defect": not evidence.contract_valid,
            "router_defect": not (
                evidence.router_sound
                and evidence.reach_safe
                and evidence.obligation_safe
            ),
            "branch_1": gates["preserve_b_gains_and_reduce"],
            "branch_2": gates["burden_10_percent_gain_without_cost_increase"],
            "strict_positive_selective_value": positive,
            "outcome": gates["outcome"],
        },
        "costs": data["costs"],
        "publication_durability": {
            "publication": data["publication"],
            "captured_composite_durability_ns": data["durability_ns"],
            "scope": "Separate descriptive captured overhead; excluded from mechanism and charged cost; nested values are not added.",
        },
        "did_selective_routing_improve": dimensions,
        "failure_attribution": attribution,
        "search_policy_failure": "NOT_ASSESSED",
        "scope": "Case 0013 establishes only task-role-conditioned exact-route admission. It does not establish universal, graph, semantic retrieval, learned, sequential search, or arbitrary InformationNeed by mechanism routing. Single-run timings are descriptive development evidence; prefixes are counterfactual evidence inspection, not measured human effort.",
        "production_source": "UNCHANGED",
        "confirmation_reserve": "NOT_ACCESSED",
    }


def validate(value: Any, data: Any) -> None:
    require(
        value == calculate(data), "Exact Stage D deterministic calculation identity"
    )


def outputs(data: Any) -> dict[str, bytes]:
    analysis = calculate(data)
    validate(analysis, data)
    files = artifacts(analysis)
    files["validation.json"] = encoded(
        {
            "status": "PASS",
            "joins": analysis["joins"],
            "checkpoints": analysis["provenance"],
            "checks": [
                "immutable ancestry and Stage A/B seals",
                "primary/reviewed identity",
                "73 ENTERED/RETURNED pairs and no retries",
                "native JSON graphs/ranks/scores/contributions",
                "independent B/C capture",
                "literal/frozen policy and exact candidate preservation",
                "every qualified resource/cell/unit join",
                "all 48 witnesses in each arm and stable tie-break",
                "prefix/union/UTF-8 arithmetic",
                "required and owning unit reach",
                "nonoverlapping captured costs",
                "integer gate arithmetic and precedence",
                "deterministic JSON/Markdown/trace",
                "focused tamper and overwrite tests",
            ],
            "outcome": analysis["gates"]["outcome"],
        }
    )
    files["integrity.json"] = encoded(
        {
            "schema": "case-0013-stage-d-integrity-v1",
            "sha256": {n: sha(raw) for n, raw in files.items()},
            "implementation_sha256": {
                n: sha((ROOT / n).read_bytes())
                for n in ("analysis.py", "authentication.py", "reporting.py")
            },
            "inputs": analysis["provenance"],
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
        "sha256": {n: sha(raw) for n, raw in files.items()},
        "outcome": load(ROOT / "analysis.json")["gates"]["outcome"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    data = auth.authenticate()
    if args.mode == "build":
        materialize.write_new({ROOT / n: raw for n, raw in outputs(data).items()})
    sys.stdout.write(encoded(verify(data)).decode())


if __name__ == "__main__":
    main()
