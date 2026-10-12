"""Owning-obligation support algebra and frozen metrics over captured rankings."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812, PLR0912, PLR0915, C901, PLR2004, PLR0913, PLR0917
import math
from collections import Counter
from typing import Any

from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize as m
from experiments.task_conditioned_graph import gates

LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")


def label_counts(values: Any) -> Any:
    counter = Counter(values)
    return {label: counter[label] for label in LABELS}


def prefix(addresses: list[str], obligation: str, labels: Any, resources: Any) -> Any:
    unique = sorted(set(addresses))
    return {
        "resources": unique,
        "unique_resources": len(unique),
        "occurrences": len(addresses),
        "duplicate_occurrences": len(addresses) - len(unique),
        "labels": label_counts(labels[obligation, s] for s in addresses),
        "distinct_utf8_bytes": sum(
            len(resources[s]["content"].encode()) for s in unique
        ),
    }


def witness(
    w: Any,
    ranks: Any,
    order: list[str],
    labels: Any,
    resources: Any,
    addresses: list[str],
) -> Any:
    members = [addresses[i] for i in w["resources"]]
    member_ranks = {s: ranks.get(s) for s in members}
    complete = all(v is not None for v in member_ranks.values())
    depth = max(member_ranks.values(), default=0) if complete else None
    return {
        "id": w["id"],
        "obligation": w["obligation"],
        "repository_members": members,
        "member_ranks": member_ranks,
        "complete": complete,
        "depth": depth,
        "prefix": prefix(order[:depth], w["obligation"], labels, resources)
        if complete
        else None,
    }


def select(values: Any) -> Any:
    complete = [w for w in values if w["complete"]]
    if complete:
        return min(complete, key=lambda w: (w["depth"], w["id"]))
    return {
        "id": None,
        "obligation": values[0]["obligation"],
        "repository_members": [],
        "member_ranks": {},
        "complete": False,
        "depth": None,
        "prefix": None,
    }


def flow(data: Any, query: str, address: str) -> Any:
    state = next(s for s in data["states"][query] if s["address"] == address)
    pairs = [
        p for p in data["flows"][query] if p["target"] == address and p["pair_flow"] > 0
    ]
    self_flow = math.fsum(p["pair_flow"] for p in pairs if p["source"] == address)
    cross = math.fsum(p["pair_flow"] for p in pairs if p["source"] != address)
    total = state["incoming_structural_flow"]
    m.require(
        math.isclose(self_flow + cross, total, rel_tol=0, abs_tol=2e-10),
        "Self/cross flow reconciliation",
    )
    contributors = sorted(pairs, key=lambda p: (-p["pair_flow"], p["source"]))
    return {
        "seed": state["seed"],
        "seed_only": state["seed"] and total == 0,
        "incoming_structural_flow": total,
        "incoming_self_flow": self_flow,
        "incoming_cross_resource_flow": cross,
        "self_flow_share": self_flow / total if total else None,
        "cross_resource_flow_share": cross / total if total else None,
        "major_incoming_contributors": contributors[:10],
        "top_cross_resource_referencers": [
            p for p in contributors if p["source"] != address
        ][:10],
        "all_incoming_pair_flows": contributors,
        "native_reference_identities": sorted(
            {r for p in pairs for r in p["reference_identities"]}
        ),
        "direct_restart_mass": state["direct_restart_mass"],
        "dangling_return_mass": state["dangling_return_mass"],
        "diagnostic_only": True,
        "new_threshold": False,
    }


def analyze(data: Any) -> Any:
    gold = data["gold"]["primary"]
    addresses = [r["address"] for r in gold["resource_frame"]]
    resources = {r["address"]: r for r in data["resources"]}
    labels = {
        (c["obligation"], c["resource_address"]): c["label"] for c in gold["cells"]
    }
    m.require(
        len(labels) == 3084 and len(set(addresses)) == 514, "Complete unique joins"
    )
    orders: Any = {arm: {} for arm in "ABC"}
    ranks: Any = {arm: {} for arm in "ABC"}
    bindings = []
    for i, obligation in enumerate(data["design"]["requirement_matrix"], 1):
        q, o = f"Q{i}", f"O{i}"
        m.require(
            obligation["obligation"] == o and obligation["query_id"] == q,
            "Exact query owner",
        )
        m.require(
            data["arms"]["A"][q]["query"]["text"] == obligation["query"],
            "Exact native query",
        )
        for arm in "ABC":
            rows = (
                data["arms"][arm][q]["matches"] if arm == "A" else data["arms"][arm][q]
            )
            orders[arm][o] = [r["address"] for r in rows]
            ranks[arm][o] = {r["address"]: r["rank"] for r in rows}
            m.require(
                len(ranks[arm][o]) == len(rows)
                and set(ranks[arm][o]) <= set(addresses),
                "No missing/duplicate/stale rank join",
            )
            for n, row in enumerate(rows, 1):
                m.require(row["rank"] == n, "Captured rank order")
                native = resources[row["address"]]
                if arm == "A":
                    m.require(
                        all(
                            row[k] == native[k]
                            for k in (
                                "address",
                                "document_identity",
                                "content_identity",
                            )
                        ),
                        "Exact native ranked identity",
                    )
                bindings.append(
                    {
                        "case": gold["case"],
                        "task_identity": gold["task_identity"],
                        "obligation": o,
                        "query": q,
                        "arm": arm,
                        "rank": n,
                        **{
                            k: native[k]
                            for k in (
                                "repository_id",
                                "snapshot_id",
                                "corpus_id",
                                "address",
                                "document_identity",
                                "content_identity",
                            )
                        },
                        "label": labels[o, row["address"]],
                    }
                )
        m.require(
            set(orders["C"][o]) == set(orders["A"][o]) | set(orders["B"][o]),
            "Captured C union",
        )
        ablated = sorted(
            data["arms"]["C"][q],
            key=lambda r: (-r["a_contribution"], r["a_rank"] or math.inf, r["address"]),
        )
        m.require(
            [r["address"] for r in ablated if r["a_contribution"] > 0]
            == orders["A"][o],
            "Deterministic graph-channel ablation",
        )
        for row in data["arms"]["C"][q]:
            ar, br = (
                ranks["A"][o].get(row["address"]),
                ranks["B"][o].get(row["address"]),
            )
            ac, bc = 1 / (60 + ar) if ar else 0, 1 / (60 + br) if br else 0
            m.require(
                (
                    row["a_rank"],
                    row["b_rank"],
                    row["a_contribution"],
                    row["b_contribution"],
                    row["score"],
                    row["graph_channel_ablated_a_rank"],
                )
                == (ar, br, ac, bc, ac + bc, ar),
                "Captured RRF/ablation arithmetic",
            )
    required = []
    for cell in gold["cells"]:
        if cell["label"] != "REQUIRED":
            continue
        o, s, idx = cell["obligation"], cell["resource_address"], cell["resource_index"]
        q = "Q" + o[1:]
        ar, br, cr = (ranks[arm][o].get(s) for arm in "ABC")
        c = next((r for r in data["arms"]["C"][q] if r["address"] == s), None)
        f = flow(data, q, s)
        rescue = ar is None and cr is not None
        meaningful = gates.meaningful_rank(ar, cr)
        regression = ar is not None and cr is not None and cr > ar
        movement = rescue or (ar is not None and cr is not None and cr < ar)
        graph = (
            movement
            and br is not None
            and f["incoming_structural_flow"] > 0
            and bool(f["native_reference_identities"])
            and c is not None
            and c["b_contribution"] > 0
        )
        overtakers = []
        if regression:
            for t in orders["C"][o][: cr - 1]:
                ta = ranks["A"][o].get(t)
                if ta is None or ta > ar:
                    tc = next(r for r in data["arms"]["C"][q] if r["address"] == t)
                    tf = flow(data, q, t)
                    overtakers.append(
                        {
                            "address": t,
                            "label": labels[o, t],
                            "a_rank": ta,
                            "c_rank": ranks["C"][o][t],
                            "b_rank": ranks["B"][o].get(t),
                            "graph_rrf": tc["b_contribution"],
                            "incoming_flow": tf["incoming_structural_flow"],
                            "reference_identities": tf["native_reference_identities"],
                            "self_flow_share": tf["self_flow_share"],
                        }
                    )
        failures = []
        if ar is not None and br is None:
            failures.append("LEXICAL_ONLY_REQUIRED_EVIDENCE")
            if not any(p["target"] == s for p in data["flows"][q]):
                failures.append("GRAPH_MISSES_DISCONNECTED_REQUIRED_EVIDENCE")
        if regression and any(
            t["label"] == "UNNECESSARY"
            and t["graph_rrf"] > 0
            and t["incoming_flow"] > 0
            for t in overtakers
        ):
            failures.append("GRAPH_PROPAGATION_NOISE")
        required.append(
            {
                "obligation": o,
                "query": q,
                "resource_address": s,
                "resource_index": idx,
                "provenance": cell["provenance"]
                | {"document_identity": cell["resource_identity"]},
                "reviewed_witness_membership": [
                    w["id"]
                    for w in gold["minimal_witnesses"][o]
                    if idx in w["resources"]
                ],
                "obligation_indispensable": idx
                in gold["obligation_indispensability"][o]["resources"],
                "task_indispensable": idx
                in gold["task_sufficiency"]["task_indispensable_resources"],
                "membership": {arm: s in ranks[arm][o] for arm in "ABC"},
                "ranks": {arm: ranks[arm][o].get(s) for arm in "ABC"},
                "c_minus_a_rank": cr - ar
                if cr is not None and ar is not None
                else None,
                "b_propagated_reference_score": next(
                    (r["score"] for r in data["arms"]["B"][q] if r["address"] == s),
                    None,
                ),
                "reach_rescue": rescue,
                "meaningful_finite_rank_gain": meaningful,
                "finite_rank_regression": regression,
                "complementary_regression_bound": gates.bounded(ar, cr, 10),
                "graph_channel_rrf_contribution": c["b_contribution"] if c else 0,
                "lexical_channel_rrf_contribution": c["a_contribution"] if c else 0,
                "graph_ablation": {
                    "rank": ar,
                    "reach_rescue": False,
                    "finite_rank_gain": False,
                    "gain_disappears": movement,
                },
                "graph_contributed_gain": graph,
                "graph_contributed_meaningful_rank_gain": graph and meaningful,
                "graph_contributed_reach_rescue": graph and rescue,
                "flow": f,
                "failure_attribution": failures,
                "new_overtakers": overtakers,
                "mechanism_diagnoses_without_demonstrated_consequence": "NOT_ASSIGNED",
            }
        )
    witnesses: Any = []
    selected: Any = {}
    for o, values in gold["minimal_witnesses"].items():
        per_arm = {
            arm: [
                witness(w, ranks[arm][o], orders[arm][o], labels, resources, addresses)
                for w in values
            ]
            for arm in "ABC"
        }
        for j, w in enumerate(values):
            witnesses.append(
                {
                    "id": w["id"],
                    "obligation": o,
                    "support": w["support"],
                    "units": w["units"],
                    "arms": {arm: per_arm[arm][j] for arm in "ABC"},
                }
            )
        chosen = {arm: select(per_arm[arm]) for arm in "ABC"}
        ad, cd = chosen["A"]["depth"], chosen["C"]["depth"]
        meaningful = gates.meaningful_depth(ad, cd)
        relevant = [
            r
            for r in required
            if r["obligation"] == o
            and r["resource_address"] in chosen["C"]["repository_members"]
            and r["graph_contributed_gain"]
        ]
        ablated = select(per_arm["A"])
        selected[o] = {
            "arms": chosen,
            "c_minus_a_depth": cd - ad if cd is not None and ad is not None else None,
            "meaningful_witness_gain": meaningful,
            "complementary_depth_bound": gates.bounded(ad, cd, 5),
            "graph_contributed_witness_gain": meaningful
            and bool(relevant)
            and not gates.meaningful_depth(ad, ablated["depth"]),
            "graph_attribution_cells": [r["resource_address"] for r in relevant],
            "graph_ablation_selected": {"id": ablated["id"], "depth": ablated["depth"]},
        }
    burden: Any = {}
    reach: Any = {}
    unit_results: Any = []
    units = gold["primary"]["units"]
    for unit in units:
        for o in unit["obligations"]:
            outcomes = {}
            for arm in "ABC":
                alternatives = [
                    v["id"]
                    for v in unit["alternatives"]
                    if all(addresses[i] in ranks[arm][o] for i in v["resources"])
                ]
                outcomes[arm] = {
                    "reached": unit["evidence_class"] == "TASK_BACKED"
                    or bool(alternatives),
                    "complete_alternatives": alternatives,
                    "task_backed_unranked": unit["evidence_class"] == "TASK_BACKED",
                }
            unit_results.append(
                {
                    "unit": unit["id"],
                    "obligation": o,
                    "evidence_class": unit["evidence_class"],
                    "arms": outcomes,
                }
            )
    for arm in "ABC":
        scoped = [
            (o, s)
            for o, v in selected.items()
            if v["arms"][arm]["complete"]
            for s in orders[arm][o][: v["arms"][arm]["depth"]]
        ]
        unique = sorted({s for _, s in scoped})
        incomplete = [o for o, v in selected.items() if not v["arms"][arm]["complete"]]
        burden[arm] = {
            "unique_resources": len(unique),
            "occurrences": len(scoped),
            "duplicate_occurrences": len(scoped) - len(unique),
            "labels": label_counts(labels[o, s] for o, s in scoped),
            "distinct_utf8_bytes": sum(
                len(resources[s]["content"].encode()) for s in unique
            ),
            "resources": unique,
            "owning_query_prefix_occurrences": [
                {"obligation": o, "address": s, "label": labels[o, s]}
                for o, s in scoped
            ],
            "incomplete_obligations": incomplete,
            "comparison_eligible": not incomplete,
            "scope": "Selected complete mandatory witness prefixes only; incomplete obligations have no invented prefix",
        }
        rc = [r for r in required if r["membership"][arm]]
        repo = sorted(
            {
                u["unit"]
                for u in unit_results
                if u["evidence_class"] != "TASK_BACKED" and u["arms"][arm]["reached"]
            }
        )
        all_units = sorted(
            {u["unit"] for u in unit_results if u["arms"][arm]["reached"]}
        )
        reach[arm] = {
            "required_resources": sorted({r["resource_address"] for r in rc}),
            "required_resource_count": len({r["resource_address"] for r in rc}),
            "required_cells": [[r["obligation"], r["resource_address"]] for r in rc],
            "required_cell_count": len(rc),
            "repository_supported_units": repo,
            "repository_supported_unit_count": len(repo),
            "all_units": all_units,
            "all_unit_count": len(all_units),
            "owning_obligation_unit_reach": [
                [u["obligation"], u["unit"]]
                for u in unit_results
                if u["arms"][arm]["reached"]
            ],
            "repository_units_reached_in_every_owning_obligation": sorted(
                {
                    u["id"]
                    for u in units
                    if u["evidence_class"] != "TASK_BACKED"
                    and all(
                        next(
                            v
                            for v in unit_results
                            if v["unit"] == u["id"] and v["obligation"] == o
                        )["arms"][arm]["reached"]
                        for o in u["obligations"]
                    )
                }
            ),
            "obligation_completeness": {
                o: v["arms"][arm]["complete"] for o, v in selected.items()
            },
        }
    novel: Any = {}
    seed_diagnostic: Any = {}
    top_k: Any = {}
    for i in range(1, 7):
        o, q = f"O{i}", f"Q{i}"
        new = sorted(set(orders["B"][o]) - set(orders["A"][o]))
        novel[o] = {
            "query": q,
            "count": len(new),
            "labels": label_counts(labels[o, s] for s in new),
            "resources": [
                {
                    "address": s,
                    "label": labels[o, s],
                    "b_rank": ranks["B"][o][s],
                    "c_rank": ranks["C"][o].get(s),
                    "c_rescued": labels[o, s] == "REQUIRED" and s in ranks["C"][o],
                    "provenance": {
                        k: resources[s][k]
                        for k in (
                            "repository_id",
                            "snapshot_id",
                            "corpus_id",
                            "document_identity",
                            "content_identity",
                        )
                    },
                    "flow": flow(data, q, s),
                }
                for s in new
            ],
        }
        positives = []
        for s in orders["B"][o]:
            if labels[o, s] == "UNNECESSARY":
                continue
            f = flow(data, q, s)
            lexical_seed = s in data["seeds"][q]["lexical"]
            exact_seed = (
                s
                in next(r for r in data["summary"]["queries"] if r["query"] == q)[
                    "exact_seeds"
                ]
            )
            category = (
                "seed-only resource"
                if f["seed_only"]
                else "lexical seed with propagated flow"
                if lexical_seed
                else "exact seed with propagated flow"
                if exact_seed
                else "nonseed propagated resource"
            )
            positives.append(
                {
                    "address": s,
                    "label": labels[o, s],
                    "lexical_seed": lexical_seed,
                    "exact_seed": exact_seed,
                    "category": category,
                    "flow": f,
                }
            )
        seed_diagnostic[o] = {
            "gold_positive_B": positives,
            "category_counts": dict(Counter(r["category"] for r in positives)),
            "seed_only_positive_B": sum(r["flow"]["seed_only"] for r in positives),
        }
        top_k[o] = {}
        for k in (10, 20, 50):
            sets = {arm: set(orders[arm][o][:k]) for arm in "ABC"}
            comparisons = {}
            for first, second in (("A", "B"), ("A", "C"), ("B", "C")):
                entered, exited = (
                    sorted(sets[second] - sets[first]),
                    sorted(sets[first] - sets[second]),
                )
                comparisons[first + "_" + second] = {
                    "overlap": len(sets[first] & sets[second]),
                    "entered": [{"address": s, "label": labels[o, s]} for s in entered],
                    "exited": [{"address": s, "label": labels[o, s]} for s in exited],
                    "entered_labels": label_counts(labels[o, s] for s in entered),
                    "exited_labels": label_counts(labels[o, s] for s in exited),
                }
            top_k[o][str(k)] = {
                "labels": {
                    arm: label_counts(labels[o, s] for s in sets[arm]) for arm in "ABC"
                },
                "comparisons": comparisons,
                "diagnostic_only": True,
            }
    unit_loss = any(
        u["arms"]["A"]["reached"] and not u["arms"]["C"]["reached"]
        for u in unit_results
    )
    contributed = any(
        r["graph_contributed_meaningful_rank_gain"]
        or r["graph_contributed_reach_rescue"]
        for r in required
    ) or any(s["graph_contributed_witness_gain"] for s in selected.values())
    inputs = gates.DecisionInputs(
        depths=tuple(
            (s["arms"]["A"]["depth"], s["arms"]["C"]["depth"])
            for s in selected.values()
        ),
        required_ranks=tuple((r["ranks"]["A"], r["ranks"]["C"]) for r in required),
        a_burden=tuple(
            burden["A"][k]
            for k in ("unique_resources", "occurrences", "distinct_utf8_bytes")
        ),
        c_burden=tuple(
            burden["C"][k]
            for k in ("unique_resources", "occurrences", "distinct_utf8_bytes")
        ),
        graph_contributed_gain=contributed,
        ranking_defect=any(v["seed_only_positive_B"] for v in seed_diagnostic.values()),
        required_unit_reach_loss=unit_loss,
    )
    decision = gates.decide(inputs)
    return {
        "case": "0016",
        "task_identity": gold["task_identity"],
        "comparison": "C versus A",
        "exact_rank_bindings": bindings,
        "required_cells": required,
        "witnesses": witnesses,
        "selected_witnesses": selected,
        "unit_reach": unit_results,
        "reach": reach,
        "burdens": burden,
        "graph_novel": novel,
        "graph_novel_overall": {
            "occurrences": sum(v["count"] for v in novel.values()),
            "distinct_resources": sorted(
                {r["address"] for v in novel.values() for r in v["resources"]}
            ),
            "labels": {
                label: sum(v["labels"][label] for v in novel.values())
                for label in LABELS
            },
        },
        "seed_propagation": seed_diagnostic,
        "top_k": top_k,
        "gate_inputs": {
            "depths": inputs.depths,
            "required_ranks": inputs.required_ranks,
            "a_burden": inputs.a_burden,
            "c_burden": inputs.c_burden,
            "graph_contributed_gain": contributed,
            "contract_defect": inputs.contract_defect,
            "ranking_defect": inputs.ranking_defect,
            "required_unit_reach_loss": unit_loss,
        },
        "gates": decision,
        "precedence": data["design"]["decision_rule"]["precedence"],
        "outcome": decision["outcome"],
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "production_behavior": "UNCHANGED",
        "confirmation_reserve": "NOT_ACCESSED",
        "scientific_reruns": 0,
        "next_step": "Maintainer reviews the completed Graph-3 Stage D verdict and causal diagnostics.",
    }
