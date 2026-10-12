"""Deterministic inspectable Stage D report; diagnostic summaries never gate."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, E501, RUF001
from typing import Any

from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize as m


def rank(value: Any) -> str:
    return "UNREACHED" if value is None else str(value)


def change(a: Any, c: Any, *, lower: bool = False) -> str:
    if a == c:
        return "TIED"
    return "IMPROVED" if (c < a if lower else c > a) else "WORSENED"


def movement(values: Any) -> str:
    if any(v is not None and v > 0 for v in values):
        return "WORSENED"
    if any(v is not None and v < 0 for v in values):
        return "IMPROVED"
    return "TIED"


def enrich(data: Any, result: Any) -> Any:
    required = result["required_cells"]
    selected = result["selected_witnesses"]
    burden = result["burdens"]
    reach = result["reach"]
    result["movement_summary"] = {
        "finite_improvements": sum(
            r["c_minus_a_rank"] is not None and r["c_minus_a_rank"] < 0
            for r in required
        ),
        "meaningful_finite_improvements": sum(
            r["meaningful_finite_rank_gain"] for r in required
        ),
        "finite_regressions": sum(r["finite_rank_regression"] for r in required),
        "unbounded_required_regressions": sum(
            not r["complementary_regression_bound"] for r in required
        ),
        "meaningful_witness_gains": sum(
            v["meaningful_witness_gain"] for v in selected.values()
        ),
        "unbounded_selected_depth_regressions": sum(
            not v["complementary_depth_bound"] for v in selected.values()
        ),
        "required_reach_rescues": sum(r["reach_rescue"] for r in required),
    }
    dimensions = {}
    for name, key in (
        ("REQUIRED resource reach", "required_resource_count"),
        ("REQUIRED cell reach", "required_cell_count"),
        ("required repository-unit reach", "repository_supported_unit_count"),
        ("all required-unit reach", "all_unit_count"),
    ):
        dimensions[name] = change(reach["A"][key], reach["C"][key])
    dimensions["obligation completeness"] = change(
        sum(reach["A"]["obligation_completeness"].values()),
        sum(reach["C"]["obligation_completeness"].values()),
    )
    dimensions["selected witness depths"] = movement(
        v["c_minus_a_depth"] for v in selected.values()
    )
    dimensions["meaningful witness gains"] = (
        "IMPROVED" if result["gates"]["witness_gain"] else "TIED"
    )
    dimensions["REQUIRED ranks"] = movement(r["c_minus_a_rank"] for r in required)
    dimensions["meaningful REQUIRED-rank gains"] = (
        "IMPROVED" if result["gates"]["rank_gain"] else "TIED"
    )
    dimensions["REQUIRED reach rescues"] = (
        "IMPROVED" if result["gates"]["required_reach_rescue"] else "TIED"
    )
    dimensions["REQUIRED regressions"] = (
        "WORSENED" if any(r["finite_rank_regression"] for r in required) else "TIED"
    )
    dimensions["task-indispensable ranks"] = movement(
        r["c_minus_a_rank"] for r in required if r["task_indispensable"]
    )
    dimensions["obligation-indispensable ranks"] = movement(
        r["c_minus_a_rank"] for r in required if r["obligation_indispensable"]
    )
    for name, key in (
        ("unique prefix resources", "unique_resources"),
        ("repeated prefix occurrences", "occurrences"),
        ("duplicates", "duplicate_occurrences"),
        ("UTF-8 byte burden", "distinct_utf8_bytes"),
    ):
        dimensions[name] = change(burden["A"][key], burden["C"][key], lower=True)
    dimensions["unnecessary occurrences"] = change(
        burden["A"]["labels"]["UNNECESSARY"],
        burden["C"]["labels"]["UNNECESSARY"],
        lower=True,
    )
    dimensions["graph-novel evidence"] = (
        "WORSENED"
        if result["graph_novel_overall"]["labels"]["UNNECESSARY"]
        and not result["graph_novel_overall"]["labels"]["REQUIRED"]
        and not result["graph_novel_overall"]["labels"]["HELPFUL_ONLY"]
        else "IMPROVED"
    )
    dimensions["treatment execution cost"] = "WORSENED"
    result["dimensions"] = dimensions
    result["dimension_policy"] = (
        "Movement dimensions are WORSENED if any regression exists; gains are reported separately. Graph-novel evidence is a diagnostic of added obligation-relative labels. Cost compares captured additional Graph-3 operations, with no scientific cost gate."
    )
    result["gate_audit"] = {
        "contract_gate": "PASS",
        "ranking_implementation_gate": "PASS",
        "required_resource_cell_unit_reach_loss": result["gates"][
            "required_reach_loss"
        ],
        "completion_loss": result["gates"]["completion_loss"],
        "unbounded_regression": not result["gates"]["complementary_bounds"],
        "meaningful_witness_gain": result["gates"]["witness_gain"],
        "graph_contributed_meaningful_witness_gain": any(
            v["graph_contributed_witness_gain"] for v in selected.values()
        ),
        "reach_rescue": result["gates"]["required_reach_rescue"],
        "graph_contributed_reach_rescue": any(
            r["graph_contributed_reach_rescue"] for r in required
        ),
        "meaningful_rank_gain": result["gates"]["rank_gain"],
        "graph_contributed_meaningful_rank_gain": any(
            r["graph_contributed_meaningful_rank_gain"] for r in required
        ),
        "strong_burden": result["gates"]["strong_burden"],
        "safe_material_gain": result["gates"]["safe_material_gain"],
        "complementary_value_gain_signal": result["gate_inputs"][
            "graph_contributed_gain"
        ],
        "complementary_value_eligible": not result["gates"]["required_reach_loss"]
        and not result["gates"]["completion_loss"]
        and result["gates"]["complementary_bounds"]
        and result["gate_inputs"]["graph_contributed_gain"],
        "selected_precedence": 3,
        "outcome": result["outcome"],
    }
    result["primary_answers"] = {
        "DID TASK-CONDITIONED PROPAGATED REFERENCE FLOW IMPROVE REPOSITORY EVIDENCE ACQUISITION IN CASE 0016?": "NO under the frozen primary rule: GRAPH_HARMFUL. Some required ranks and O2 improve, but unbounded REQUIRED-rank and selected-witness-depth regressions take precedence; reach is unchanged and burden increases.",
        "DID GRAPH-ONLY B FIND NECESSARY EVIDENCE A MISSED?": "NO. Every B-only resource is UNNECESSARY under its owning obligation. A already reaches all 36 REQUIRED cells and all 48 required units.",
        "DID HYBRID C ACTUALLY PRESERVE/USE IT?": "There is no graph-novel necessary evidence to preserve or rescue. C preserves A's complete reach, uses B to improve five meaningful REQUIRED ranks and O2 completion, and also worsens 30 REQUIRED ranks.",
        "WERE MATERIAL GAINS DRIVEN BY CROSS-RESOURCE FLOW OR SELF-REFERENCE?": "Both kinds of direct incoming flow occur. O2 resource.py and O5 planned_reference.py gains have 100% cross-resource incoming flow from tests/context/planning/test_plan.py. The three meaningful materialization.py gains are majority self-flow (85.5232%, 72.6508%, 53.8878% for O2/O3/O4), with captured cross-resource support. Shares partition the captured treatment; no self-edge ablation or new causal threshold is applied.",
        "DID RRF DILUTE OR AMPLIFY USEFUL GRAPH EVIDENCE?": "Mixed rank movement: C amplifies B's useful resource.py rank 11 to C rank 6 and planned_reference.py rank 14 to C rank 9; materialization.py B/C ranks are 3/2 (O2), 3/1 (O3), 7/8 (O4). Across necessary evidence C adds substantial regression and prefix burden. No new necessary reach appears; RRF cannot satisfy the frozen safety bounds.",
    }
    operations = {r["operation"]: r["runtime_ns"] for r in data["costs"]["operations"]}
    result["costs"] = data["costs"]
    result["publication_costs"] = data["publication_costs"]
    result["cost_comparison"] = {
        "A_query_operations_ns": sum(operations[f"query:Q{i}:A"] for i in range(1, 7)),
        "B_query_operations_ns": {
            f"Q{i}": operations[f"query:Q{i}:B"] for i in range(1, 7)
        },
        "C_fusion_operations_ns": sum(operations[f"query:Q{i}:C"] for i in range(1, 7)),
        "structural_preparation_operations_ns": {
            k: v for k, v in operations.items() if k.startswith(("ri:", "graph:"))
        },
        "interpretation": "Single captured run. Shared preparation, RI, B propagation, C fusion, diagnostic work and journal durability have separate scopes; never double-count runtime and durability. No production-performance claim or cost gate.",
    }
    historical = data["provenance"]["stage_a"]
    result["historical_comparison"] = {
        "provenance": "Authenticated amended Stage A historical_development seals; retained Increment 32/33 development results, freeze and README only",
        "amended_seal_sha256": historical["amended_integrity_sha256"],
        "Graph_1": {
            "novel_pairs": 704,
            "distinct_addresses": 183,
            "novel_support_paths": 10550,
            "sample_USEFUL": 2,
            "sample_NOT_USEFUL": 126,
        },
        "Graph_2": {
            "novel_pairs": 987,
            "distinct_addresses": 232,
            "novel_support_paths": 85015,
            "complete_three_edge_paths": 294154,
            "sample_USEFUL": 0,
            "sample_NOT_USEFUL": 128,
        },
        "Graph_3": {
            "nodes": 514,
            "directed_reference_pairs": 561,
            "native_occurrences": 3954,
            "path_enumeration": 0,
            "B_only_occurrences": result["graph_novel_overall"]["occurrences"],
            "B_only_distinct_resources": len(
                result["graph_novel_overall"]["distinct_resources"]
            ),
            "exact_novel_labels": result["graph_novel_overall"]["labels"],
        },
        "interpretation": "Graph-3 concentrates a compact ranked forward Reference view without path expansion, but finds no necessary graph-novel evidence here. Graph-1/2 retained large expansion/reversal/fanout surfaces and sampled 2/128 and 0/128 useful outcomes. Their unsampled populations remain unjudged; USEFUL is not identical to this gold's REQUIRED/HELPFUL labels. Tasks/populations differ; no controlled causal superiority claim across Graph-1/2 versus Graph-3. Reverse-dependency noise is not assigned to this forward-only Graph-3.",
    }
    result["failure_summary"] = {
        "supported_categories": sorted(
            {f for r in required for f in r["failure_attribution"]}
        ),
        "diagnosis_evidence": "Per REQUIRED regression retain newly overtaking resources, their owning labels, A/B/C ranks, graph RRF contributions and native incoming References. GRAPH_PROPAGATION_NOISE requires a demonstrated UNNECESSARY graph-supported overtaker. Disconnected REQUIRED evidence has no incoming edge; other A-only REQUIRED evidence is LEXICAL_ONLY_REQUIRED_EVIDENCE.",
        "not_demonstrated": [
            "DEGREE_DILUTION",
            "HUB_DOMINANCE",
            "AMBIGUOUS_IDENTIFIER_FANOUT",
            "REVERSE_DEPENDENCY_NOISE",
        ],
        "implementation_defects": [],
    }
    result["bounded_interpretation"] = (
        "This isolates deterministic ranking/fusion consequences within Case 0016's sealed frame and fixed treatments, conditional on the sole blind primary gold. It establishes no production benefit, universal retrieval superiority, agent success or search-policy failure. B uses A-derived seeds, so agreement is not independent evidence. Direct self/cross shares are post-gold diagnostics; no counterfactual edge removal or prospective treatment rerun occurred."
    )
    used = {
        identity
        for r in required
        for identity in r["flow"]["native_reference_identities"]
    }
    result["required_native_reference_provenance"] = {}
    for identity in sorted(used):
        ref = data["references"][identity]
        native = dict(ref["native"])
        target = dict(native["target_resource"])
        target.pop("content", None)
        native["target_resource"] = target
        result["required_native_reference_provenance"][identity] = {
            **ref,
            "native": native,
            "retained_content": "Exact target content remains in authenticated native_context/Reference graph and sealed resource frame; not duplicated here.",
        }
    return result


def markdown(data: Any, result: Any) -> bytes:
    lines = [
        "# Case 0016 Graph-3 Stage D",
        "",
        "**"
        + result["outcome"]
        + "** — C versus A under the unchanged prospective integer rule.",
        "",
    ]
    for question, answer in result["primary_answers"].items():
        lines += ["**" + question + "**", "", answer, ""]
    lines += [
        "## Reviewed gold",
        "",
        "Sole sealed GPT-6 Astra / High; PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. No second reviewer or reconciliation. 514 resources × six obligations = 3,084 cells: 36 REQUIRED, 49 HELPFUL_ONLY, 2,999 UNNECESSARY. All 48 units (21 task-backed, 27 repository-supported), 22 minimal witnesses, 864 combinations, 90 sufficient resource unions and 12 inclusion-minimal unions remain unchanged. Resource range 12–17; one 48-unit sufficient union; nine task-indispensable resources. All gaps NONE; five limitations and four ambiguity records preserved in reviewed gold.",
        "",
        "## Exhaustive REQUIRED-cell table",
        "",
        "UNREACHED is absence; delta = C-A only for finite ranks. Detailed native contributors, responsible identities, overtakers and ablation records follow in the complete cell records. Membership is explicit in each rank column (UNREACHED means no).",
        "",
    ]
    headers = [
        "Obligation",
        "Resource",
        "Witnesses",
        "Obligation indispensable",
        "Task indispensable",
        "A rank/member",
        "B rank/member",
        "B flow score",
        "C rank/member",
        "C-A",
        "Rescue",
        "Meaningful finite gain",
        "Finite regression",
        "Bound",
        "Graph RRF",
        "Lexical RRF",
        "Ablated rank",
        "Graph gain",
        "Seed",
        "Seed only",
        "Incoming",
        "Self",
        "Cross",
        "Major referencers",
        "Failure",
    ]
    lines += [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for r in sorted(
        result["required_cells"], key=lambda r: (r["obligation"], r["resource_address"])
    ):
        f = r["flow"]
        values = [
            r["obligation"],
            r["resource_address"],
            ", ".join(r["reviewed_witness_membership"]),
            r["obligation_indispensable"],
            r["task_indispensable"],
            rank(r["ranks"]["A"]),
            rank(r["ranks"]["B"]),
            r["b_propagated_reference_score"],
            rank(r["ranks"]["C"]),
            r["c_minus_a_rank"],
            r["reach_rescue"],
            r["meaningful_finite_rank_gain"],
            r["finite_rank_regression"],
            "PASS" if r["complementary_regression_bound"] else "FAIL",
            r["graph_channel_rrf_contribution"],
            r["lexical_channel_rrf_contribution"],
            rank(r["graph_ablation"]["rank"]),
            r["graph_contributed_gain"],
            f["seed"],
            f["seed_only"],
            f["incoming_structural_flow"],
            f["incoming_self_flow"],
            f["incoming_cross_resource_flow"],
            "; ".join(p["source"] for p in f["major_incoming_contributors"][:3]),
            ", ".join(r["failure_attribution"]),
        ]
        lines.append(
            "| " + " | ".join(str(v) if v is not None else "N/A" for v in values) + " |"
        )
    lines += [
        "",
        "## All 22 witnesses",
        "",
        "Task-backed units have no retrieval rank. Each witness uses exactly its own reviewed repository members; no mixed alternatives. Empty witnesses, if present, have complete depth zero.",
        "",
        "| Witness | Obligation | Members | A member ranks / depth | B member ranks / depth | C member ranks / depth |",
        "|---|---|---|---|---|---|",
    ]
    for w in result["witnesses"]:
        views = [
            ", ".join(
                s + "=" + rank(n) for s, n in w["arms"][arm]["member_ranks"].items()
            )
            + "; depth="
            + rank(w["arms"][arm]["depth"])
            for arm in "ABC"
        ]
        lines.append(
            "| "
            + " | ".join(
                [
                    w["id"],
                    w["obligation"],
                    ", ".join(w["arms"]["A"]["repository_members"]),
                    *views,
                ]
            )
            + " |"
        )
    lines += [
        "",
        "## Selected witnesses",
        "",
        "| Obligation | A witness/depth | B witness/depth | C witness/depth | C-A | Meaningful | Graph attributed | Bound |",
        "|---|---|---|---|---:|---|---|---|",
    ]
    for o, s in result["selected_witnesses"].items():
        values = [
            o,
            *(
                (s["arms"][arm]["id"] or "NONE") + "/" + rank(s["arms"][arm]["depth"])
                for arm in "ABC"
            ),
            str(s["c_minus_a_depth"]),
            str(s["meaningful_witness_gain"]),
            str(s["graph_contributed_witness_gain"]),
            "PASS" if s["complementary_depth_bound"] else "FAIL",
        ]
        lines.append("| " + " | ".join(values) + " |")
    lines += ["", "## Dimensions", "", "| Dimension | C versus A |", "|---|---|"]
    lines.extend(
        "| " + name + " | " + value + " |"
        for name, value in result["dimensions"].items()
    )
    lines += [
        "",
        result["dimension_policy"],
        "",
        "## Graph-novel owning-obligation labels",
        "",
        "| Query/obligation | B-only | REQUIRED | HELPFUL_ONLY | UNNECESSARY |",
        "|---|---:|---:|---:|---:|",
    ]
    for o, n in result["graph_novel"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    n["query"] + "/" + o,
                    str(n["count"]),
                    *(
                        str(n["labels"][label])
                        for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                    ),
                ]
            )
            + " |"
        )
    lines += ["", "## Exact frozen precedence", ""]
    lines.extend(str(i) + ". " + p for i, p in enumerate(result["precedence"], 1))
    lines += [
        "",
        result["bounded_interpretation"],
        "",
        "## Complete machine-inspectable detail",
        "",
        "The following complete records preserve every metric, unit, witness prefix, required alternative, graph attribution, pair-flow diagnostic, top-K join, cost scope and gate. Full gold semantics remain independently frozen in reviewed_gold.json.",
        "",
    ]
    for name, value in [
        (
            "Exact task and six obligations",
            {k: data["gold"]["primary"][k] for k in ("exact_task", "obligations")},
        ),
        (
            "All 48 semantic units and alternatives",
            data["gold"]["primary"]["primary"]["units"],
        ),
        (
            "Primary limitations and ambiguities",
            {
                k: data["gold"]["primary"]["primary"][k]
                for k in ("gaps", "limitations", "ambiguities")
            },
        ),
        ("Gold statistics", data["reviewed_replay"]["statistics"]),
        ("Authentication and seals", data["provenance"]),
        *[
            (k, result[k])
            for k in (
                "movement_summary",
                "reach",
                "unit_reach",
                "burdens",
                "required_cells",
                "witnesses",
                "selected_witnesses",
                "graph_novel",
                "graph_novel_overall",
                "seed_propagation",
                "top_k",
                "failure_summary",
                "required_native_reference_provenance",
                "cost_comparison",
                "costs",
                "publication_costs",
                "historical_comparison",
                "gate_inputs",
                "gates",
                "gate_audit",
            )
        ],
    ]:
        lines += [
            "### " + name,
            "",
            "```json",
            m.encoded(value).decode().rstrip(),
            "```",
            "",
        ]
    lines += [
        "Next step: " + result["next_step"],
        "No further retrieval increment begins in this task.",
        "",
    ]
    return "\n".join(lines).encode()
