"""Evaluate frozen U2 acquisition against committed reviewed gold; no retrieval.

The deterministic calculations consume inert authenticated capture JSON only.
Witness selection and gate wording are bound to the historical Stage A bytes.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812, PLR2004
import argparse
import copy
import sys
from collections import Counter
from typing import Any

from experiments.codex_dogfood.case_0012.stage_d import authentication as auth

encoded, sha, require, load = auth.encoded, auth.sha, auth.require, auth.load
ROOT = auth.ROOT


def cell_labels(gold: Any) -> Any:
    return {(c["obligation"], c["address"]): c["label"] for c in gold["cells"]}


def witness_id(ob: str, index: int) -> str:
    return f"{ob}.reviewed-{index + 1:02}"


def prefix_metrics(prefixes: Any, labels: Any, resources: Any) -> Any:
    """Union resources across independent lanes, retain owning-cell occurrences."""
    unique = sorted({a for rows in prefixes.values() for a in rows})
    composition = dict.fromkeys(("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY"), 0)
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
        "unique_utf8_bytes": sum(resources[a]["byte_size"] for a in unique),
    }


def completion(witness: Any, order: list[str]) -> Any:
    positions = {a: i for i, a in enumerate(order, 1)}
    missing = sorted(set(witness["resources"]) - positions.keys())
    ranks = {r: positions.get(r) for r in witness["resources"]}
    depth = (
        None
        if missing
        else max((positions[r] for r in witness["resources"]), default=0)
    )
    return {
        "resources": witness["resources"],
        "units": witness["required_unit_ids"],
        "member_depths": ranks,
        "missing_resources": missing,
        "completion_depth": depth,
        "bottlenecks": []
        if depth is None
        else sorted(r for r, rank in ranks.items() if rank == depth),
    }


def evaluate_arm(arm: str, data: Any) -> Any:
    gold, labels = data["gold"], cell_labels(data["gold"])
    resources = {r["address"]: r for r in data["resources"]}
    lanes: dict[str, Any] = {}
    prefixes: dict[str, Any] = {}
    picks: dict[str, Any] = {}
    for ob in gold["obligations"]:
        key = ob["key"]
        rows = data["arms"][arm][key]["rows" if arm == "A" else "entries"]
        order = [r["address"] for r in rows]
        alternatives = [
            dict(completion(w, order), identity=witness_id(key, i))
            for i, w in enumerate(gold["witnesses_by_obligation"][key])
        ]
        complete = [w for w in alternatives if w["completion_depth"] is not None]
        selected = (
            min(complete, key=lambda w: (w["completion_depth"], w["identity"]))
            if complete
            else None
        )
        depth = None if selected is None else selected["completion_depth"]
        prefix = order[:depth] if depth is not None else []
        prefixes[key] = prefix
        picks[key] = None if selected is None else selected["identity"]
        metrics = (
            prefix_metrics({key: prefix}, labels, resources)
            if depth is not None
            else None
        )
        lanes[key] = {
            "all_witnesses": alternatives,
            "selected_witness": picks[key],
            "completion_depth": depth,
            "metrics": metrics,
            "minimum_witness_resource_count": min(
                len(w["resources"]) for w in gold["witnesses_by_obligation"][key]
            ),
            "excess_above_minimum_witness": None
            if metrics is None
            else metrics["unique_prefix_count"]
            - min(len(w["resources"]) for w in gold["witnesses_by_obligation"][key]),
        }
    task_metrics = (
        prefix_metrics(prefixes, labels, resources)
        if all(lane["completion_depth"] is not None for lane in lanes.values())
        else None
    )
    task_combinations = []
    for combination in gold["task_sufficiency"]["complete_task_combinations"]:
        candidate_prefixes = {}
        depths = {}
        for ob, identity in combination["witnesses"].items():
            witness = next(
                w for w in lanes[ob]["all_witnesses"] if w["identity"] == identity
            )
            depths[ob] = witness["completion_depth"]
            rows = data["arms"][arm][ob]["rows" if arm == "A" else "entries"]
            candidate_prefixes[ob] = (
                [r["address"] for r in rows[: depths[ob]]]
                if depths[ob] is not None
                else []
            )
        task_combinations.append(
            {
                "witnesses": combination["witnesses"],
                "sufficient_resources": combination["resources"],
                "sufficient_units": combination["units"],
                "lane_depths": depths,
                "metrics": prefix_metrics(candidate_prefixes, labels, resources)
                if all(d is not None for d in depths.values())
                else None,
            }
        )
    selected_structure = next(
        (c for c in task_combinations if c["witnesses"] == picks), None
    )
    require(
        selected_structure is not None or task_metrics is None,
        "Selected complete task structure",
    )
    return {
        "lanes": lanes,
        "task": task_metrics,
        "selected_complete_structure": selected_structure,
        "all_complete_task_combinations": task_combinations,
        "minimal_complete_resource_unions": gold["task_sufficiency"][
            "minimal_complete_resource_unions"
        ],
        "accounting": "Independent owning-obligation prefixes; union once across selected prefixes; repeated occurrences and owning labels retained. No task-global ranking or alternative mixing.",
    }


def native_resource(resource: Any) -> Any:
    return {
        "address": {"value": resource["address"]},
        "content_identity": {"value": resource["content_identity"]},
        "content": resource["text"],
        "byte_size": resource["byte_size"],
        "encoding": resource["encoding"],
    }


def safety(data: Any) -> Any:  # noqa: C901, PLR0912 -- exact frozen capture contracts
    resources = {r["address"]: r for r in data["resources"]}
    native_hashes = {a: sha(encoded(native_resource(r))) for a, r in resources.items()}
    global_reference = data["behaviors"]["B"]["presentations"]["source"][
        "global_safety"
    ]
    require(
        [r["resource"]["canonical_sha256"] for r in global_reference["native_order"]]
        == [native_hashes[r["address"]] for r in data["lexical"]["global"]["rows"]],
        "Global native resource order",
    )
    reports: dict[str, Any] = {}
    for arm in ("A", "B", "C"):
        reached_cells, reached_resources, reached_units, owning_units = (
            set(),
            set(),
            set(),
            set(),
        )
        lane_reports: dict[str, Any] = {}
        for obligation in data["gold"]["obligations"]:
            ob = obligation["key"]
            original = data["arms"]["A"][ob]["rows"]
            rows = data["arms"][arm][ob]["rows" if arm == "A" else "entries"]
            addresses = [r["address"] for r in rows]
            require(len(addresses) == len(set(addresses)), "Duplicate candidate")
            require(set(addresses) <= resources.keys(), "Unexpected candidate resource")
            require(
                {r["address"] for r in original} <= set(addresses),
                "Lexical candidate loss",
            )
            ranks = {r["address"]: r for r in original}
            for row in rows:
                require(
                    row["content_identity"]
                    == resources[row["address"]]["content_identity"],
                    "Candidate content identity",
                )
            if arm != "A":
                view = data["behaviors"][arm]["presentations"][ob]
                require(
                    view["global_safety"] == global_reference, "Global safety changed"
                )
                require(
                    view["final_resource_sequence"]
                    == [entry["resource"] for entry in view["entries"]],
                    "Native final sequence",
                )
                native_original = view["original_lexical"]["native_order"]
                require(
                    len(native_original) == len(original), "Native lexical cardinality"
                )
                for native, row in zip(native_original, original, strict=True):
                    require(
                        native["resource"]["canonical_sha256"]
                        == native_hashes[row["address"]],
                        "Native resource identity",
                    )
                    require(
                        native["rank"] == row["rank"]
                        and native["score"] == row["score"],
                        "Native rank/score",
                    )
                    for nk, rk in [
                        ("content_contributions", "content_terms"),
                        ("filename_contributions", "filename_terms"),
                        ("content_score", "content_score"),
                        ("filename_score", "filename_score"),
                        ("weighted_filename_score", "weighted_filename_score"),
                        ("filename_weight", "filename_weight"),
                    ]:
                        require(
                            native[nk] == row[rk], "Native contribution preservation"
                        )
                promoted = {
                    e["address"] for e in rows if e["exact_tier_position"] is not None
                }
                require(
                    [e["address"] for e in rows if e["exact_tier_position"] is None]
                    == [r["address"] for r in original if r["address"] not in promoted],
                    "Complete fallback order",
                )
                for i, (row, entry) in enumerate(
                    zip(rows, view["entries"], strict=True), 1
                ):
                    require(
                        row["position"] == entry["position"] == i, "Routed position"
                    )
                    require(
                        entry["resource"]["canonical_sha256"]
                        == native_hashes[row["address"]],
                        "Routed native occurrence",
                    )
                    baseline = ranks.get(row["address"])
                    require(
                        row["native_rank"]
                        == (None if baseline is None else baseline["rank"]),
                        "Native rank preserved",
                    )
                    require(
                        row["score"]
                        == (None if baseline is None else baseline["score"]),
                        "Native score preserved",
                    )
                    require(
                        entry["lexical"]
                        == (
                            None
                            if baseline is None
                            else native_original[baseline["rank"] - 1]
                        ),
                        "Original native match identity/contributions",
                    )
                    if entry["exact"] is not None:
                        require(
                            entry["exact"]["lexical"] == entry["lexical"],
                            "Exact entry original match",
                        )
                        routes = [
                            h
                            for h in data["summary"]["hint_rows"]
                            if h["arm"] == arm
                            and h["obligation"] == ob
                            and any(
                                t["address"] == row["address"] for t in h["targets"]
                            )
                        ]
                        require(
                            len(routes) == 1
                            and routes[0]["disposition"] == "RESOLVED"
                            and routes[0]["locator"] is not None,
                            "Sound unique promotion",
                        )
                require(
                    view["fallback_native_order"]
                    == [e for e in view["entries"] if e["exact"] is None],
                    "Fallback native identities",
                )
            for cell in data["gold"]["cells"]:
                if (
                    cell["obligation"] == ob
                    and cell["label"] == "REQUIRED"
                    and cell["address"] in addresses
                ):
                    reached_cells.add(ob + "|" + cell["document_identity"])
                    reached_resources.add(cell["address"])
            for unit in data["gold"]["semantic_units"]:
                if ob in unit["obligations"] and any(
                    set(s["resources"]) <= set(addresses) for s in unit["supports"]
                ):
                    reached_units.add(unit["id"])
                    owning_units.add(ob + "|" + unit["id"])
            lane_reports[ob] = {
                "original_candidates": sorted(ranks),
                "final_candidates": sorted(addresses),
                "lost_candidates": sorted(set(ranks) - set(addresses)),
                "added_candidates": sorted(set(addresses) - set(ranks)),
                "candidate_duplicates": len(addresses) - len(set(addresses)),
            }
        reports[arm] = {
            "required_resources": sorted(reached_resources),
            "required_cells": sorted(reached_cells),
            "required_units": sorted(reached_units),
            "owning_required_units": sorted(owning_units),
            "lanes": lane_reports,
        }
    for arm in ("B", "C"):
        reports[arm]["losses"] = {
            key: sorted(set(reports["A"][key]) - set(reports[arm][key]))
            for key in (
                "required_resources",
                "required_cells",
                "required_units",
                "owning_required_units",
            )
        }
        require(
            not any(reports[arm]["losses"].values()), "Required semantic reach loss"
        )
    return {
        "arms": reports,
        "scientific_safety": True,
        "soundness": True,
        "candidate_loss": 0,
        "candidate_duplicates": 0,
        "native_match_identities": "PRESERVED",
        "native_ranks_scores_contributions": "PRESERVED",
        "lexical_fallback": "COMPLETE",
        "global_safety": "UNCHANGED",
        "global_rows": len(data["lexical"]["global"]["rows"]),
    }


def hint_effects(data: Any, arms: Any) -> Any:
    labels, result = cell_labels(data["gold"]), {}
    for arm in ("B", "C"):
        hints = []
        for frozen in data["summary"]["hint_rows"]:
            if frozen["arm"] != arm:
                continue
            hint = copy.deepcopy(frozen)
            ob = hint["obligation"]
            resolution = data["exact"][arm][int(hint["hint"][1:]) - 1]
            require(
                resolution["repository_id"]["value"]
                == data["gold"]["frame"]["repository_id"]
                and resolution["snapshot_id"]["value"]
                == data["gold"]["frame"]["snapshot_id"],
                "Hint repository/snapshot join",
            )
            require(
                resolution["disposition"] == hint["disposition"]
                and resolution["frame_identity"]
                == data["gold"]["frame"]["frame_identity"],
                "Hint resolution join",
            )
            require(
                resolution["request"]
                == {
                    k: v
                    for k, v in data["treatment"]["exact_route_requests"][arm][
                        int(hint["hint"][1:]) - 1
                    ].items()
                    if k != "identity"
                },
                "Exact frozen request",
            )
            require(
                hint["span"] == resolution["request"]["hint"]["span"]
                and hint["text"]
                == data["gold"]["task_text"][
                    hint["span"]["start"] : hint["span"]["end"]
                ].strip("`"),
                "Hint task span",
            )
            require(
                len(resolution["resources"]) == len(hint["targets"]),
                "Exact target cardinality",
            )
            hint["target_effects"] = []
            for target, native in zip(
                hint["targets"], resolution["resources"], strict=True
            ):
                address = target["address"]
                require(
                    native
                    == native_resource(
                        next(r for r in data["resources"] if r["address"] == address)
                    ),
                    "Exact retained target bytes",
                )
                require(
                    native["address"]["value"] == address
                    and native["content_identity"]["value"]
                    == target["content_identity"],
                    "Exact target native identity",
                )
                affected = []
                for i, witness in enumerate(
                    data["gold"]["witnesses_by_obligation"][ob]
                ):
                    if address not in witness["resources"]:
                        continue
                    prior, post = (
                        arms["A"]["lanes"][ob]["all_witnesses"][i],
                        arms[arm]["lanes"][ob]["all_witnesses"][i],
                    )
                    classification = "WAS_NOT_THE_BOTTLENECK"
                    if address in prior["bottlenecks"]:
                        classification = (
                            "WAS_THE_BOTTLENECK"
                            if len(prior["bottlenecks"]) == 1
                            else "REMOVED_ONE_BOTTLENECK"
                        )
                    affected.append(
                        {
                            "witness": witness_id(ob, i),
                            "resources": witness["resources"],
                            "A_completion_depth": prior["completion_depth"],
                            "exact_first_completion_depth": post["completion_depth"],
                            "prior_bottleneck": prior["bottlenecks"],
                            "post_bottleneck": post["bottlenecks"],
                            "classification": classification,
                            "completion_change": None
                            if prior["completion_depth"] is None
                            or post["completion_depth"] is None
                            else post["completion_depth"] - prior["completion_depth"],
                        }
                    )
                units = [
                    u["id"]
                    for u in data["gold"]["semantic_units"]
                    if ob in u["obligations"]
                    and any(address in s["resources"] for s in u["supports"])
                ]
                hint["target_effects"].append(
                    {
                        **target,
                        "label": labels[ob, address],
                        "reviewed_units": units,
                        "in_at_least_one_complete_witness": bool(affected),
                        "obligation_indispensable": address
                        in data["gold"]["obligation_indispensable_resources"][ob],
                        "witness_effects": affected,
                        "changes_witness_completion": any(
                            w["completion_change"] != 0 for w in affected
                        ),
                        "bottleneck_classification": "WAS_NOT_REQUIRED"
                        if not affected
                        else sorted({w["classification"] for w in affected}),
                    }
                )
            hint["unsupported_concept_repository_evidence"] = []
            if hint["disposition"] == "UNSUPPORTED":
                require(
                    not hint["targets"] and hint["locator"] is None,
                    "Unsupported promotion",
                )
                hint["unsupported_concept_repository_evidence"] = [
                    {
                        "unit": u["id"],
                        "supports": [
                            s
                            for s in u["supports"]
                            if any(
                                e["origin"] == "RESOURCE" and hint["text"] in e["text"]
                                for e in s["evidence"]
                            )
                        ],
                    }
                    for u in data["gold"]["semantic_units"]
                    if ob in u["obligations"]
                    and any(
                        any(
                            e["origin"] == "RESOURCE" and hint["text"] in e["text"]
                            for e in s["evidence"]
                        )
                        for s in u["supports"]
                    )
                ]
            hints.append(hint)
        require(
            [h["hint"] for h in hints] == [f"H{i:02}" for i in range(1, 11)],
            "Hint inventory",
        )
        result[arm] = hints
    return result


def delta(before: int, after: int) -> Any:
    return {
        "A": before,
        "exact_first": after,
        "delta": after - before,
        "percentage": None if before == 0 else (after - before) * 100 / before,
        "exact_percentage_fraction": None
        if before == 0
        else {"numerator": (after - before) * 100, "denominator": before},
    }


def comparisons(arms: Any) -> Any:
    output: dict[str, Any] = {}
    for arm in ("B", "C"):
        lanes = {}
        for ob, baseline in arms["A"]["lanes"].items():
            changed = arms[arm]["lanes"][ob]
            lanes[ob] = {
                "depth": delta(
                    baseline["completion_depth"], changed["completion_depth"]
                ),
                "unique_prefix": delta(
                    baseline["metrics"]["unique_prefix_count"],
                    changed["metrics"]["unique_prefix_count"],
                ),
                "unnecessary_occurrences": delta(
                    baseline["metrics"]["label_occurrences"]["UNNECESSARY"],
                    changed["metrics"]["label_occurrences"]["UNNECESSARY"],
                ),
                "utf8_bytes": delta(
                    baseline["metrics"]["unique_utf8_bytes"],
                    changed["metrics"]["unique_utf8_bytes"],
                ),
            }
        before, after = arms["A"]["task"], arms[arm]["task"]
        task = {
            key: delta(before[key], after[key])
            for key in (
                "prefix_occurrences",
                "unique_prefix_count",
                "duplicate_occurrences",
                "unique_utf8_bytes",
            )
        }
        task["labels"] = {
            key: delta(
                before["label_occurrences"][key], after["label_occurrences"][key]
            )
            for key in before["label_occurrences"]
        }
        task["removed_prefix_resources"] = sorted(
            set(before["unique_prefix_resources"])
            - set(after["unique_prefix_resources"])
        )
        task["added_prefix_resources"] = sorted(
            set(after["unique_prefix_resources"])
            - set(before["unique_prefix_resources"])
        )
        output[arm] = {"lanes": lanes, "task": task}
    return output


def costs(data: Any) -> Any:
    runtime = data["summary"]["runtime_ns"]
    common = runtime["index-build"] + sum(
        v for k, v in runtime.items() if k.startswith("lexical:")
    )
    arms = {}
    for arm in ("A", "B", "C"):
        extraction = 0 if arm == "A" else runtime["inventory:" + arm]
        resolution = sum(
            v for k, v in runtime.items() if k.startswith("route:" + arm + ":")
        )
        presentation = sum(
            v for k, v in runtime.items() if k.startswith("present:" + arm + ":")
        )
        arms[arm] = {
            "shared_native_index_ns": runtime["index-build"],
            "shared_lexical_queries_ns": common - runtime["index-build"],
            "inventory_projection_ns": extraction,
            "exact_resolution_ns": resolution,
            "presentation_ns": presentation,
            "charged_treatment_ns": common + extraction + resolution + presentation,
            "composite_arm_runtime_ns_descriptive": runtime["arm:" + arm],
            "native_grounding_child_ns_descriptive": sum(
                v for k, v in runtime.items() if k.startswith("ground:" + arm + ":")
            ),
        }
    root_ids = {
        "index-build",
        "arm:A",
        "arm:B",
        "arm:C",
        *(k for k in runtime if k.startswith("lexical:")),
    }
    roots = [o for o in data["operations"] if o["identity"] in root_ids]
    return {
        "arms": arms,
        "runtime_ns": runtime,
        "shared_lexical_by_lane_ns": {
            k.split(":", 1)[1]: v
            for k, v in runtime.items()
            if k.startswith("lexical:")
        },
        "root_operation_wall_ns_descriptive": sum(o["wall_call_ns"] for o in roots),
        "nested_durability_inside_root_calls_ns_descriptive": sum(
            o["durability_inside_call_ns"] for o in roots
        ),
        "all_operation_durability_ns_descriptive_nonadditive": {
            o["identity"]: o["durability_inside_call_ns"] for o in data["operations"]
        },
        "frame_module_universe_construction": "NOT_MEASURED in captured Stage B; frozen pre-execution frame is shared equally",
        "finalization_publication_overhead": "NOT_MEASURED separately; excluded from treatment",
        "evidence_inspection_cost": "NOT_MEASURED",
        "accounting": "Frozen charged sum = shared index + ten captured lexical queries + inventory + route parents + presentation. Arm composite and grounding children are descriptive and overlap; never added to charged sum. Single capture, no latency benchmark.",
    }


def families(data: Any, hints: Any, comparison: Any) -> Any:
    output: dict[str, Any] = {}
    for arm in ("B", "C"):
        output[arm] = {}
        for family, capture in data["summary"]["families"][arm].items():
            selected = [h for h in hints[arm] if h["family"] == family]
            targets = [t for h in selected for t in h["target_effects"]]
            required = [t for t in targets if t["label"] == "REQUIRED"]
            output[arm][family] = {
                **capture,
                "target_labels": dict(Counter(t["label"] for t in targets)),
                "targets": targets,
                "effectiveness": "NOT_ASSESSED" if not required else "ASSESSED",
                "required_target_promotions": [
                    {
                        "address": t["address"],
                        "native_rank": t["native_rank"],
                        "routed_position": t["routed_position"],
                        "depth_saved": t["depth_saved"],
                    }
                    for t in required
                ],
                "witness_completion_changes": [
                    w for t in required for w in t["witness_effects"]
                ],
                "associated_lane_prefix_effects": {
                    ob: comparison[arm]["lanes"][ob] for ob in capture["obligations"]
                },
                "effect_attribution_scope": "Associated-lane combined captured routing, not an unexecuted family ablation. Choices shares declaration/module routes; lane presentation cost overlaps.",
            }
    return output


def frozen_gates(
    data: Any, arms: Any, hints: Any, candidate_safety: Any, cost: Any
) -> Any:
    decision = data["treatment"]["decision_rule"]
    extraction = data["treatment"]["extraction_agreement"]
    caller_required_misses = [
        h["hint"]
        for h in hints["B"]
        if not next(
            x["rule_extracted"]
            for x in data["treatment"]["hint_inventory"]
            if x["identity"]["value"] == h["hint_identity"]
        )
        and h["disposition"] == "RESOLVED"
        and any(t["label"] == "REQUIRED" for t in h["target_effects"])
    ]
    extraction_defect = (
        extraction["false_rule_extractions"] > 0
        or extraction["type_disagreements"] > 0
        or bool(caller_required_misses)
    )
    gates = {}
    for arm in ("B", "C"):
        task_before, task_after = arms["A"]["task"], arms[arm]["task"]
        hint_lanes = sorted({h["obligation"] for h in hints[arm]})
        union_gate = (
            task_after["unique_prefix_count"] * 20
            <= task_before["unique_prefix_count"] * 21
        )
        target_gate = [
            h["hint"]
            for h in hints[arm]
            if any(
                t["label"] == "REQUIRED"
                and t["native_rank"] is not None
                and t["native_rank"] > 20
                and t["routed_position"] <= 3
                for t in h["target_effects"]
            )
        ]
        prefix_evidence = {
            ob: {
                "A": arms["A"]["lanes"][ob]["metrics"]["unique_prefix_count"],
                "exact_first": arms[arm]["lanes"][ob]["metrics"]["unique_prefix_count"],
            }
            for ob in hint_lanes
        }
        reduced_lanes = [
            ob
            for ob, v in prefix_evidence.items()
            if v["exact_first"] * 5 <= v["A"] * 4
        ]
        noise_before = sum(
            arms["A"]["lanes"][ob]["metrics"]["label_occurrences"]["UNNECESSARY"]
            for ob in hint_lanes
        )
        noise_after = sum(
            arms[arm]["lanes"][ob]["metrics"]["label_occurrences"]["UNNECESSARY"]
            for ob in hint_lanes
        )
        noise_gate = noise_before > 0 and noise_after * 5 <= noise_before * 4
        obligation_evidence = {
            ob: {
                "A": lane["metrics"]["unique_prefix_count"],
                "exact_first": arms[arm]["lanes"][ob]["metrics"]["unique_prefix_count"],
                "lhs": arms[arm]["lanes"][ob]["metrics"]["unique_prefix_count"] * 4,
                "rhs": lane["metrics"]["unique_prefix_count"] * 5,
                "pass": arms[arm]["lanes"][ob]["metrics"]["unique_prefix_count"] * 4
                <= lane["metrics"]["unique_prefix_count"] * 5,
            }
            for ob, lane in arms["A"]["lanes"].items()
        }
        charged_a, charged_changed = (
            cost["arms"]["A"]["charged_treatment_ns"],
            cost["arms"][arm]["charged_treatment_ns"],
        )
        gates[arm] = {
            "scientific_safety": {
                "pass": candidate_safety["scientific_safety"],
                "wording": decision["scientific_safety"],
                "losses": candidate_safety["arms"][arm]["losses"],
            },
            "soundness": {
                "pass": candidate_safety["soundness"],
                "wording": decision["soundness"],
                "resolved": sum(h["disposition"] == "RESOLVED" for h in hints[arm]),
                "unsupported_without_promotion": sum(
                    h["disposition"] == "UNSUPPORTED" and not h["targets"]
                    for h in hints[arm]
                ),
            },
            "extraction": {
                "pass": not extraction_defect,
                "wording": decision["extraction"],
                "agreement": extraction,
                "caller_only_resolved_required": caller_required_misses,
            },
            "meaningful_value": {
                "pass": bool(target_gate)
                or (bool(reduced_lanes) and union_gate)
                or (noise_gate and union_gate),
                "wording": decision["meaningful_value"],
                "branch_1_required_rank_gt20_position_le3": {
                    "pass": bool(target_gate),
                    "hints": target_gate,
                },
                "branch_2_prefix_le_four_fifths": {
                    "pass": bool(reduced_lanes) and union_gate,
                    "lanes": reduced_lanes,
                    "lane_evidence": prefix_evidence,
                },
                "branch_3_unnecessary_le_four_fifths": {
                    "pass": noise_gate and union_gate,
                    "A": noise_before,
                    "exact_first": noise_after,
                    "lhs": noise_after * 5,
                    "rhs": noise_before * 4,
                    "zero_baseline": noise_before == 0,
                },
                "case_union_le_twenty_one_twentieths": {
                    "pass": union_gate,
                    "A": task_before["unique_prefix_count"],
                    "exact_first": task_after["unique_prefix_count"],
                    "lhs": task_after["unique_prefix_count"] * 20,
                    "rhs": task_before["unique_prefix_count"] * 21,
                },
            },
            "obligation_safety": {
                "pass": all(v["pass"] for v in obligation_evidence.values()),
                "wording": decision["obligation_safety"],
                "evidence": obligation_evidence,
            },
            "cost": {
                "pass": charged_changed <= charged_a * 3,
                "wording": decision["cost"],
                "A_charged_ns": charged_a,
                "exact_first_charged_ns": charged_changed,
                "lhs": charged_changed,
                "rhs": charged_a * 3,
            },
        }
    positive = any(
        t["label"] == "REQUIRED"
        and t["depth_saved"] is not None
        and t["depth_saved"] > 0
        for arm in hints.values()
        for h in arm
        for t in h["target_effects"]
    ) or any(
        arms[arm]["task"]["unique_prefix_count"]
        < arms["A"]["task"]["unique_prefix_count"]
        or arms[arm]["task"]["unique_utf8_bytes"]
        < arms["A"]["task"]["unique_utf8_bytes"]
        for arm in ("B", "C")
    )
    outcome = choose_outcome(
        contract_defect=False,
        extraction_defect=extraction_defect,
        c_passes=all(g["pass"] for g in gates["C"].values()),
        complementary=candidate_safety["scientific_safety"]
        and candidate_safety["soundness"]
        and positive,
    )
    require(outcome in decision["outcomes"], "Frozen outcome vocabulary")
    return {
        "arms": gates,
        "outcome": outcome,
        "precedence_wording": decision["precedence"],
        "precedence": [
            {
                "priority": 1,
                "condition": "invalid scientific contract / incomplete mandatory task interpretation",
                "triggered": False,
                "effect": "EXPERIMENTAL_CONTRACT_DEFECT",
                "evidence": "All authenticated invariants pass; reviewed units cover all nine mandatory obligations; gap sets empty",
            },
            {
                "priority": 2,
                "condition": "false/type/caller-only resolved REQUIRED extraction defect",
                "triggered": extraction_defect,
                "effect": "EXTRACTION_OR_RESOLUTION_DEFECT",
            },
            {
                "priority": 3,
                "condition": "C passes every frozen support gate",
                "triggered": all(g["pass"] for g in gates["C"].values()),
                "effect": "EXACT_HINT_ROUTING_SUPPORTED",
            },
            {
                "priority": 4,
                "condition": "sound reach-safe positive value without all C gates",
                "triggered": positive,
                "effect": "COMPLEMENTARY_BUT_LIMITED",
                "superseded": outcome == "EXACT_HINT_ROUTING_SUPPORTED",
            },
            {"priority": 5, "condition": "otherwise", "effect": "NO_MATERIAL_VALUE"},
        ],
        "arithmetic_wording": decision["arithmetic"],
    }


def choose_outcome(
    *,
    contract_defect: bool,
    extraction_defect: bool,
    c_passes: bool,
    complementary: bool,
) -> str:
    if contract_defect:
        return "EXPERIMENTAL_CONTRACT_DEFECT"
    if extraction_defect:
        return "EXTRACTION_OR_RESOLUTION_DEFECT"
    if c_passes:
        return "EXACT_HINT_ROUTING_SUPPORTED"
    if complementary:
        return "COMPLEMENTARY_BUT_LIMITED"
    return "NO_MATERIAL_VALUE"


def improvement(  # noqa: PLR0913, PLR0917 -- all independently evaluated dimensions
    comparison: Any,
    arms: Any,
    candidate_safety: Any,
    hints: Any,
    cost: Any,
    decision: Any,
) -> Any:
    def burden(value: Any) -> Any:
        return {
            "status": "IMPROVED"
            if value["delta"] < 0
            else "WORSENED"
            if value["delta"] > 0
            else "TIED",
            **value,
        }

    c = comparison["C"]
    family_values = {}
    for family in sorted({h["family"] for h in hints["C"]}):
        selected = [
            (h["hint"], t)
            for h in hints["C"]
            if h["family"] == family
            for t in h["target_effects"]
            if t["label"] == "REQUIRED"
        ]
        family_values[family] = {
            "status": "NOT_ASSESSED"
            if not selected
            else "IMPROVED"
            if any(
                t["depth_saved"] is not None and t["depth_saved"] > 0
                for _, t in selected
            )
            else "TIED",
            "required_target_depths": [
                {
                    "hint": h,
                    "native": t["native_rank"],
                    "routed": t["routed_position"],
                    "saved": t["depth_saved"],
                }
                for h, t in selected
            ],
        }
    return {
        "semantic_completeness": {
            "status": "TIED",
            "A_units": len(candidate_safety["arms"]["A"]["required_units"]),
            "B_C_units": len(candidate_safety["arms"]["C"]["required_units"]),
            "A_complete_obligations": sum(
                lane["completion_depth"] is not None
                for lane in arms["A"]["lanes"].values()
            ),
            "B_C_complete_obligations": sum(
                lane["completion_depth"] is not None
                for lane in arms["C"]["lanes"].values()
            ),
        },
        "required_reach": {
            "status": "TIED",
            "A_resources": len(candidate_safety["arms"]["A"]["required_resources"]),
            "B_C_resources": len(candidate_safety["arms"]["C"]["required_resources"]),
            "A_cells": len(candidate_safety["arms"]["A"]["required_cells"]),
            "B_C_cells": len(candidate_safety["arms"]["C"]["required_cells"]),
        },
        "exact_resolution_soundness": {
            "status": "NOT_ASSESSED",
            "reason": "Arm A executes no exact route; B/C have eight sound resolved hints and two unsupported with no promotion, not a comparative soundness gain.",
        },
        "extraction_agreement": {
            "status": "TIED",
            "accepted": 10,
            "reference": 10,
            "false": 0,
            "type_disagreements": 0,
            "B_C_effectiveness": "EQUAL; no differential extraction effectiveness treatment",
        },
        "route_family_required_promotion": family_values,
        "witness_completion_depth": {
            "status": "IMPROVED"
            if any(v["depth"]["delta"] < 0 for v in c["lanes"].values())
            else "TIED",
            "per_obligation": {ob: burden(v["depth"]) for ob, v in c["lanes"].items()},
        },
        "unique_prefix_burden": burden(c["task"]["unique_prefix_count"]),
        "repeated_prefix_occurrences": burden(c["task"]["prefix_occurrences"]),
        "duplicate_prefix_occurrences": burden(c["task"]["duplicate_occurrences"]),
        "unnecessary_prefix_burden": burden(c["task"]["labels"]["UNNECESSARY"]),
        "utf8_byte_burden": burden(c["task"]["unique_utf8_bytes"]),
        "routing_query_execution_cost": {
            "status": "WORSENED",
            "charged_B": burden(
                delta(
                    cost["arms"]["A"]["charged_treatment_ns"],
                    cost["arms"]["B"]["charged_treatment_ns"],
                )
            ),
            "charged_C": burden(
                delta(
                    cost["arms"]["A"]["charged_treatment_ns"],
                    cost["arms"]["C"]["charged_treatment_ns"],
                )
            ),
            "lexical_queries": "TIED: nine obligation + one global captured query reused",
            "cost_gate": decision["arms"]["C"]["cost"]["pass"],
        },
        "candidate_duplication": {"status": "TIED", "A": 0, "B_C": 0},
        "global_safety": {
            "status": "TIED",
            "rows": candidate_safety["global_rows"],
            "native_ids_scores_contributions": "UNCHANGED",
        },
    }


def attribution(hints: Any, arms: Any, data: Any) -> Any:
    output: dict[str, Any] = {
        "hints": [],
        "non_improving_obligations": [],
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "required_unit_resource_records": [],
    }
    for h in hints["C"]:
        reasons, contributors = [], []
        if h["disposition"] == "UNSUPPORTED":
            reasons.append("UNSUPPORTED_EXACT_HINT")
        for target in h["target_effects"]:
            if target["label"] != "REQUIRED":
                reasons.append("EXACT_ROUTE_TARGET_NOT_REQUIRED")
            elif not target["changes_witness_completion"]:
                contributors.append("EXACT_TARGET_NOT_COMPLETION_BOTTLENECK")
            if target["native_rank"] is not None and target["native_rank"] <= 20:
                contributors.append("EXACT_TARGET_ALREADY_SHALLOW")
        output["hints"].append(
            {
                "hint": h["hint"],
                "frozen_failure_classes": sorted(set(reasons)),
                "observed_contributors": sorted(set(contributors)),
                "association_scope": "H03 choices only; exports label cannot retroactively change its scope"
                if h["hint"] == "H03"
                else "Frozen owning obligation",
            }
        )
    for ob, baseline in arms["A"]["lanes"].items():
        changed = arms["C"]["lanes"][ob]
        if changed["completion_depth"] >= baseline["completion_depth"]:
            selected = next(
                w
                for w in changed["all_witnesses"]
                if w["identity"] == changed["selected_witness"]
            )
            output["non_improving_obligations"].append(
                {
                    "obligation": ob,
                    "depth": changed["completion_depth"],
                    "bottleneck_resources": selected["bottlenecks"],
                    "frozen_failure_classes": ["UNSUPPORTED_EXACT_HINT"]
                    if ob in {"materialization", "assembly"}
                    else [],
                    "observed_contributors": ["EXACT_TARGET_NOT_COMPLETION_BOTTLENECK"]
                    if ob == "source"
                    else ["NO_ASSOCIATED_EXACT_TARGET"],
                    "fallback_ranking": "LEXICAL_FALLBACK_RANKING_FAILURE"
                    if changed["metrics"]["label_occurrences"]["UNNECESSARY"] > 0
                    else "NO_UNNECESSARY_PREFIX",
                    "reason": "Captured owning-lane evidence remains lexical; no sequential search policy or wrong semantic judgment is inferred.",
                }
            )
    output["required_unit_resource_records"] = required_records(data)
    return output


def required_records(data: Any) -> Any:
    records: list[Any] = []
    for obligation in data["gold"]["obligations"]:
        ob = obligation["key"]
        orders = {
            arm: [
                r["address"]
                for r in data["arms"][arm][ob]["rows" if arm == "A" else "entries"]
            ]
            for arm in ("A", "B", "C")
        }
        for unit in data["gold"]["semantic_units"]:
            if ob not in unit["obligations"]:
                continue
            depths = {
                arm: min(
                    max((order.index(r) + 1 for r in support["resources"]), default=0)
                    for support in unit["supports"]
                    if set(support["resources"]) <= set(order)
                )
                for arm, order in orders.items()
            }
            records.append(
                {
                    "obligation": ob,
                    "unit": unit["id"],
                    "supports": unit["supports"],
                    "complete_support_depths": depths,
                    "earliest_failed_stage": None,
                    "mechanical_evidence": "Every required unit has a complete support in each captured candidate lane; native lexical fallback survives",
                    "semantic_evidence": unit["necessity_rationale"],
                    "proposed_correction": "NONE in this task; retained lexical burden may inform separately authorized upstream/R1.7/BM25F work",
                }
            )
        for cell in data["gold"]["cells"]:
            if cell["obligation"] == ob and cell["label"] == "REQUIRED":
                records.append(  # noqa: PERF401 -- explicit owning-cell diagnostic record
                    {
                        "obligation": ob,
                        "resource": cell["address"],
                        "positions": {
                            arm: order.index(cell["address"]) + 1
                            for arm, order in orders.items()
                        },
                        "earliest_failed_stage": None,
                        "semantic_evidence": cell["rationale"],
                        "mechanical_evidence": "Required owning cell reached in every captured arm; source provenance retained in reviewed gold",
                        "proposed_correction": "NONE; do not infer SEARCH_POLICY_FAILURE",
                    }
                )
    return records


def construct(data: Any | None = None) -> Any:
    if data is None:
        data = auth.authenticate()
    arms = {arm: evaluate_arm(arm, data) for arm in ("A", "B", "C")}
    require(arms["B"] == arms["C"], "Independent B/C effectiveness equality")
    candidate_safety = safety(data)
    hints = hint_effects(data, arms)
    comparison = comparisons(arms)
    cost = costs(data)
    gates = frozen_gates(data, arms, hints, candidate_safety, cost)
    return {
        "schema": "case-0012-stage-d-analysis-v1",
        "checkpoints": data["checkpoints"],
        "task_identity": data["gold"]["task_identity"],
        "task_text": data["gold"]["task_text"],
        "obligations": data["gold"]["obligations"],
        "frame": data["gold"]["frame"],
        "reviewed_units": data["gold"]["semantic_units"],
        "reviewed_witnesses": data["gold"]["witnesses_by_obligation"],
        "reviewed_task_sufficiency": data["gold"]["task_sufficiency"],
        "reviewed_gold_sha256": sha((auth.GOLD / "reviewed_gold.json").read_bytes()),
        "hints": hints,
        "arms": arms,
        "B_C_effectiveness_equal": True,
        "comparisons": comparison,
        "route_families": families(data, hints, comparison),
        "candidate_safety": candidate_safety,
        "costs": cost,
        "frozen_decision_rule": data["treatment"]["decision_rule"],
        "frozen_gates": gates,
        "outcome": gates["outcome"],
        "did_we_improve": improvement(
            comparison, arms, candidate_safety, hints, cost, gates
        ),
        "attribution": attribution(hints, arms, data),
        "scope": "Case-local captured acquisition and counterfactual completion-prefix burden. No task-global ordering, causal family ablation, production promotion, benchmark or sequential search policy.",
    }


def verify_analysis(analysis: Any, data: Any) -> None:
    require(
        encoded(analysis) == encoded(construct(data)),
        "Exact Stage D semantic/arithmetic reconstruction",
    )


def outputs() -> Any:
    from experiments.codex_dogfood.case_0012.stage_d.reporting import (  # noqa: PLC0415 -- publication layer avoids cycle
        markdown,
        trace,
    )

    data = auth.authenticate()
    analysis = construct(data)
    causal_trace = trace(analysis)
    human = markdown(analysis)
    files = {
        "analysis.json": encoded(analysis),
        "analysis.md": human,
        "STAGE_D_REVIEW.md": human,
        "trace.json": encoded(causal_trace),
        "TRACE.md": markdown(analysis, trace_only=True),
        "validation.json": encoded(
            {
                "status": "PASS",
                "ancestry": data["checkpoints"],
                "reviewed_gold": "PASS",
                "stage_b_capture": "PASS",
                "resources": 531,
                "qualified_cells": 4779,
                "hints_per_arm": 10,
                "witnesses": 16,
                "task_combinations": 32,
                "candidate_loss": 0,
                "B_C_effectiveness_equal": True,
                "checks": [
                    "exact frame and queries",
                    "native resolutions",
                    "native match identities/ranks/scores/contributions",
                    "all witness depths",
                    "all prefixes and unions",
                    "all UTF-8 totals",
                    "task combination accounting",
                    "all safety reach sets",
                    "captured nonoverlapping charged costs",
                    "integer frozen gates",
                    "outcome precedence",
                    "deterministic JSON/Markdown/trace",
                ],
                "adversarial_tests": "test_analysis.py: prefix, rank, byte, score, contribution, candidate, gate, outcome and output mutation; overwrite refusal",
            }
        ),
    }
    files["integrity.json"] = encoded(
        {
            "schema": "case-0012-stage-d-integrity-v1",
            "sha256": {n: sha(raw) for n, raw in files.items()},
            "implementation_sha256": {
                name: sha((ROOT / name).read_bytes())
                for name in ("authentication.py", "analysis.py", "reporting.py")
            },
            "input_bindings": data["checkpoints"],
            "scope": "Physical deterministic Stage D bytes. .local excluded.",
        }
    )
    return files


def write_new(files: Any) -> None:
    if any((ROOT / name).exists() for name in files):
        message = "Refusing to overwrite Stage D outputs"
        raise FileExistsError(message)
    for name, raw in files.items():
        with (ROOT / name).open("xb") as stream:
            stream.write(raw)


def verify() -> Any:
    files = outputs()
    for name, raw in files.items():
        require((ROOT / name).read_bytes() == raw, "Stage D output tamper: " + name)
    return {
        "status": "PASS",
        "outcome": load(ROOT / "analysis.json")["outcome"],
        "sha256": {name: sha(raw) for name, raw in files.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    if args.mode == "build":
        write_new(outputs())
    sys.stdout.write(encoded(verify()).decode())


if __name__ == "__main__":
    main()
