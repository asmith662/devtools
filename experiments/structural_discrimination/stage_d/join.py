# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- exact captured scientific boundary
"""Exact identity joins and ordinal diagnostics without any scientific acquisition."""

from __future__ import annotations

from collections import Counter
from statistics import median
from typing import Any

from experiments.structural_discrimination.decision import (
    Label,
    case_category,
    classify_pair,
)
from experiments.structural_discrimination.stage_b.reporting import canonical_validate
from experiments.structural_discrimination.stage_c.import_gold import LABELS, require

IDENTITY = ("address", "document_identity", "content_identity")
FRAME = ("repository_id", "snapshot_id", "corpus_id")
PAIR_COUNTS = (
    "BENEFICIAL",
    "NEUTRAL",
    "HARMFUL",
    "STRONG_BENEFICIAL",
    "STRONG_HARMFUL",
)
PROPERTIES = (
    "distinct_supporting_source_count",
    "native_occurrence_count",
    "best_supporting_source_rank",
    "target_lexical_rank",
    "rank_distance",
    "intervening_unnecessary",
)


def label_counts(labels: Any) -> dict[str, int]:
    """Keep all categorical counts, including zero cells."""
    counts = Counter(labels)
    require(set(counts) <= set(LABELS), "Unknown gold label")
    return {label: counts[label] for label in LABELS}


def rate(numerator: int, denominator: int) -> Any:
    """Expose exact denominators; zero rate is distinct from undefined."""
    return {
        "numerator": numerator,
        "denominator": denominator,
        "proportion": numerator / denominator if denominator else None,
    }


def distributions(targets: Any) -> Any:
    """Descriptive empirical distributions, never thresholds or structural scores."""
    result: dict[str, Any] = {}
    for label in LABELS:
        result[label] = {}
        for key in PROPERTIES:
            values = sorted(t[key] for t in targets if t["target_gold_label"] == label)
            result[label][key] = {
                "n": len(values),
                "values": values,
                "min": min(values) if values else None,
                "median": median(values) if values else None,
                "max": max(values) if values else None,
            }
    return result


def ablate(query: Any) -> Any:
    """Remove treatment annotations/pairs while retaining captured A byte identity."""
    return {"A": query["A"], "annotations": [], "local_pairs": []}


def validate_join(case: str, design: Any, trace: Any, gold: Any) -> Any:  # noqa: PLR0915
    """Reject every malformed or stale join; sealed provenance stays externally anchored."""
    require(
        trace["summary"]["case"]
        == gold["case"]
        == case
        == design["case_id"].removeprefix("case-"),
        "Join case identity",
    )
    require(
        trace["summary"]["frame"] == gold["frame"] == design["parent_frame"],
        "Join frame identity",
    )
    require(gold["task_identity"] == design["task_identity"], "Join task identity")
    require(trace["summary"]["task"] == design["task_text"], "Join task text")
    require(
        trace["summary"]["ablation"]["status"] == "PASS"
        and trace["summary"]["ablation"]["ranking_side_effect"] == "NONE",
        "Captured A ablation",
    )
    require(
        all(
            trace["summary"][k] == 0
            for k in (
                "rank_modifications",
                "ppr_executions",
                "rrf_executions",
                "graph_only_admissions",
            )
        ),
        "Captured mechanical invariant",
    )
    require(
        [
            {k: o[k] for k in g}
            for o, g in zip(design["obligations"], gold["obligations"], strict=True)
        ]
        == gold["obligations"],
        "Join obligation interpretation",
    )
    require(
        len(trace["queries"]) == len(design["obligations"]),
        "Missing/duplicate query",
    )
    cells = {}
    resources: dict[str, Any] = {}
    obligations = {o["id"]: o for o in design["obligations"]}
    for cell in gold["cells"]:
        key = (cell["obligation"], cell["address"])
        require(key not in cells, "Duplicate gold cell")
        require(
            cell["obligation"] in obligations
            and cell["obligation_identity"]
            == obligations[cell["obligation"]]["obligation_identity"],
            "Gold obligation identity",
        )
        require(all(cell[k] == gold["frame"][k] for k in FRAME), "Gold frame identity")
        require(cell["label"] in LABELS, "Unknown gold label")
        identity = {k: cell[k] for k in (*IDENTITY, "source_blob_sha256")}
        require(
            cell["address"] not in resources or resources[cell["address"]] == identity,
            "Conflicting gold resource",
        )
        resources[cell["address"]] = identity
        cells[key] = cell
    require(
        len(resources) == gold["frame"]["resource_count"]
        and set(cells) == {(o, a) for o in obligations for a in resources},
        "Missing gold cell",
    )
    # Existing canonical verifier supplies completeness against the captured native facts.
    try:
        canonical_validate(trace)
    except (KeyError, IndexError) as error:
        raise ValueError("Missing captured target/source/pair identity") from error  # noqa: EM101, TRY003 -- fail closed at captured boundary
    facts = {f["fact_identity"]: f for f in trace["positive_references"]}
    require(
        len(facts) == len(trace["positive_references"]),
        "Duplicate Reference provenance",
    )
    joined_a = joined_pairs = joined_sources = occurrences = 0
    for q, obligation in zip(trace["queries"], design["obligations"], strict=True):
        require(
            q["obligation"] == obligation["id"]
            and q["query_identity"] == obligation["query_identity"]
            and q["query"] == obligation["query"]
            and q["information_need"] == obligation["need"]
            and q["task_identity"] == design["task_identity"],
            "Captured query/obligation identity",
        )
        require(
            q["frame"] == {k: gold["frame"][k] for k in FRAME},
            "Query frame identity",
        )
        by_address = {r["address"]: r for r in q["A"]}
        for ranked in q["A"]:
            cell = cells[(q["obligation"], ranked["address"])]
            require(
                all(ranked[k] == cell[k] for k in IDENTITY),
                "A resource/document/content join",
            )
            joined_a += 1
        require(ablate(q)["A"] == q["A"], "A ablation identity")
        for annotation, pair in zip(q["annotations"], q["local_pairs"], strict=True):
            target = annotation["target"]
            require(
                pair["obligation"] == q["obligation"]
                and pair["query"] == q["query_identity"]["value"],
                "Pair obligation/query identity",
            )
            require(
                target["a_rank"] > 1
                and pair["predecessor"]["a_rank"] == target["a_rank"] - 1,
                "Pair predecessor rank",
            )
            require(pair["target"] == target, "Pair target identity")
            require(
                (q["obligation"], pair["predecessor"]["address"]) in cells,
                "Predecessor gold join",
            )
            source_addresses = set()
            support_ids = set()
            for source in annotation["sources"]:
                require(
                    source["address"] not in source_addresses,
                    "Duplicate supporting source",
                )
                source_addresses.add(source["address"])
                require(source["address"] in by_address, "Source absent from A")
                require(
                    source["address"] != target["address"]
                    and source["a_rank"] < target["a_rank"],
                    "Self/source<target eligibility",
                )
                require(
                    source["snapshot_id"] == gold["frame"]["snapshot_id"],
                    "Source snapshot identity",
                )
                require(source["supports"], "Empty source support")
                joined_sources += 1
                for support in source["supports"]:
                    require(
                        support["fact_identity"] not in support_ids,
                        "Duplicate qualifying occurrence",
                    )
                    support_ids.add(support["fact_identity"])
                    require(
                        facts.get(support["fact_identity"]) == support,
                        "Unsupported Reference provenance",
                    )
                    require(
                        support["source_address"] == source["address"]
                        and support["target_address"] == target["address"]
                        and support["target_content_identity"]
                        == target["content_identity"],
                        "Reference endpoint identity",
                    )
                    require(
                        support["source_snapshot_id"]
                        == support["target_snapshot_id"]
                        == gold["frame"]["snapshot_id"],
                        "Reference frame identity",
                    )
            require(
                annotation["distinct_supporting_source_count"]
                == len(source_addresses)
                > 0,
                "Source count",
            )
            require(
                annotation["native_occurrence_count"] == len(support_ids),
                "Occurrence count",
            )
            require(
                annotation["best_supporting_source_rank"]
                == min(s["a_rank"] for s in annotation["sources"]),
                "Best source rank",
            )
            joined_pairs += 1
            occurrences += len(support_ids)
        require(
            q["counts"]["supported_targets"] == len(q["annotations"])
            and q["counts"]["local_pairs"] == len(q["local_pairs"]),
            "Captured target/pair counts",
        )
    return {
        "status": "PASS",
        "join_defects": 0,
        "gold_cells": len(cells),
        "a_gold_cell_joins": joined_a,
        "target_gold_cell_joins": joined_pairs,
        "predecessor_gold_cell_joins": joined_pairs,
        "supporting_source_gold_cell_joins": joined_sources,
        "qualifying_occurrences": occurrences,
        "frame_obligation_resource_document_content": "EXACT",
        "A_ablation_identity": "PASS",
    }


def analyze_case(
    case: str,
    design: Any,
    trace: Any,
    gold: Any,
    indispensable: Any,
) -> Any:
    """Describe frozen supported targets and every hypothetical local pair."""
    joins = validate_join(case, design, trace, gold)
    cells = {(c["obligation"], c["address"]): c for c in gold["cells"]}
    queries = []
    all_targets = []
    for q in trace["queries"]:
        o = q["obligation"]
        ranked = q["A"]
        targets = []
        supported = {a["target"]["address"] for a in q["annotations"]}
        labels = {r["address"]: cells[(o, r["address"])]["label"] for r in ranked}
        for a, pair in zip(q["annotations"], q["local_pairs"], strict=True):
            target, predecessor = pair["target"], pair["predecessor"]
            target_label, predecessor_label = (
                labels[target["address"]],
                labels[predecessor["address"]],
            )
            classification = classify_pair(
                Label(target_label),
                Label(predecessor_label),
            )
            best = a["best_supporting_source_rank"]
            sources = [
                {
                    **s,
                    "source_gold_label": labels[s["address"]],
                    "primary_cell_pointer": cells[(o, s["address"])][
                        "primary_cell_pointer"
                    ],
                }
                for s in a["sources"]
            ]
            targets.append(
                {
                    "case": case,
                    "obligation": o,
                    "obligation_identity": cells[(o, target["address"])][
                        "obligation_identity"
                    ],
                    "frame": q["frame"],
                    "target": target,
                    "target_gold_label": target_label,
                    "target_primary_cell_pointer": cells[(o, target["address"])][
                        "primary_cell_pointer"
                    ],
                    "predecessor": predecessor,
                    "predecessor_gold_label": predecessor_label,
                    "predecessor_primary_cell_pointer": cells[
                        (o, predecessor["address"])
                    ]["primary_cell_pointer"],
                    "classification": classification.direction,
                    "strong_beneficial": classification.strong_beneficial,
                    "strong_harmful": classification.strong_harmful,
                    "sources": sources,
                    "distinct_supporting_source_count": a[
                        "distinct_supporting_source_count"
                    ],
                    "native_occurrence_count": a["native_occurrence_count"],
                    "best_supporting_source_rank": best,
                    "target_lexical_rank": target["a_rank"],
                    "rank_distance": target["a_rank"] - best,
                    "intervening_unnecessary": sum(
                        labels[r["address"]] == "UNNECESSARY"
                        for r in ranked[best : target["a_rank"] - 1]
                    ),
                },
            )
        required = [
            c
            for c in gold["cells"]
            if c["obligation"] == o and c["label"] == "REQUIRED"
        ]
        coverage = [
            {
                "address": c["address"],
                "in_A": c["address"] in labels,
                "structurally_supported": c["address"] in supported,
                "unsupported": c["address"] in labels and c["address"] not in supported,
                "primary_cell_pointer": c["primary_cell_pointer"],
            }
            for c in required
        ]
        required_in_a = sum(r["in_A"] for r in coverage)
        supported_required = sum(r["structurally_supported"] for r in coverage)
        a_counts = label_counts(labels.values())
        support_counts = label_counts(t["target_gold_label"] for t in targets)
        pair_counts = count_pairs(targets)
        queries.append(
            {
                "obligation": o,
                "A_candidate_count": len(ranked),
                "A_gold_labels": a_counts,
                "supported_target_count": len(targets),
                "supported_gold_labels": support_counts,
                "useful_supported": support_counts["REQUIRED"]
                + support_counts["HELPFUL_ONLY"],
                "supported_useful_rate": rate(
                    support_counts["REQUIRED"] + support_counts["HELPFUL_ONLY"],
                    len(targets),
                ),
                "baseline_A_useful_rate": rate(
                    a_counts["REQUIRED"] + a_counts["HELPFUL_ONLY"],
                    len(ranked),
                ),
                "required_cells": coverage,
                "baseline_lexical_non_reach": [r for r in coverage if not r["in_A"]],
                "required_in_A": required_in_a,
                "structurally_supported_REQUIRED": supported_required,
                "unsupported_REQUIRED_in_A": required_in_a - supported_required,
                "required_in_A_support_coverage": rate(
                    supported_required,
                    required_in_a,
                ),
                "indispensability_scope": "CONDITIONAL REPOSITORY-INTEGRATION INDISPENSABILITY"
                if case == "0019"
                else "FROZEN GOLD INDISPENSABILITY",
                "indispensable_resources": [
                    {
                        "address": address,
                        "kind": kind,
                        "in_A": address in labels,
                        "structurally_supported": address in supported,
                        "unsupported": address in labels and address not in supported,
                    }
                    for kind, addresses in indispensable[o].items()
                    for address in addresses
                ],
                "pair_counts": pair_counts,
                "targets": targets,
                "evidence_characteristics": distributions(targets),
                "source_label_diagnostics": source_labels(targets),
                "captured_timings_ns": q["timings"],
                "A_ablation_identity": "PASS",
                "actual_rank_modifications": 0,
            },
        )
        all_targets.extend(targets)
    totals = aggregate_queries(queries)
    return {
        "case": case,
        "join_validation": joins,
        "queries": queries,
        "totals": totals,
        "category": case_category(
            totals["pair_counts"]["STRONG_BENEFICIAL"],
            totals["pair_counts"]["STRONG_HARMFUL"],
        ),
        "captured_self_reference_count": trace["summary"]["ri"]["self_references"],
        "self_reference_contribution": 0,
        "evidence_characteristics": distributions(all_targets),
        "source_label_diagnostics": source_labels(all_targets),
    }


def count_pairs(targets: Any) -> dict[str, int]:
    """Sum local diagnostics; strong categories are subsets, not extra pairs."""
    result = Counter(t["classification"] for t in targets)
    result["STRONG_BENEFICIAL"] = sum(t["strong_beneficial"] for t in targets)
    result["STRONG_HARMFUL"] = sum(t["strong_harmful"] for t in targets)
    return {k: result[k] for k in PAIR_COUNTS}


def source_labels(targets: Any) -> Any:
    """Secondary source-label analysis; source eligibility never consumes labels."""
    sources = [s for t in targets for s in t["sources"]]
    return {
        "scope": "SECONDARY/DESCRIPTIVE; no eligibility filtering",
        "distinct_source_target_obligation_pairs": label_counts(
            s["source_gold_label"] for s in sources
        ),
        "qualifying_occurrences": label_counts(
            s["source_gold_label"] for s in sources for _ in s["supports"]
        ),
    }


def aggregate_queries(queries: Any) -> Any:
    """Sum exact case/obligation occurrences with explicit denominators."""
    a_counts = {k: sum(q["A_gold_labels"][k] for q in queries) for k in LABELS}
    support = {k: sum(q["supported_gold_labels"][k] for q in queries) for k in LABELS}
    supported_total = sum(support.values())
    a_total = sum(a_counts.values())
    required = sum(q["required_in_A"] for q in queries)
    return {
        "A_candidate_occurrences": a_total,
        "A_gold_labels": a_counts,
        "supported_targets": supported_total,
        "supported_gold_labels": support,
        "local_pairs": supported_total,
        "pair_counts": {
            k: sum(q["pair_counts"][k] for q in queries) for k in PAIR_COUNTS
        },
        "qualifying_support_occurrences": sum(
            t["native_occurrence_count"] for q in queries for t in q["targets"]
        ),
        "distinct_source_target_obligation_pairs": sum(
            t["distinct_supporting_source_count"] for q in queries for t in q["targets"]
        ),
        "baseline_A_useful_candidate_occurrences": a_counts["REQUIRED"]
        + a_counts["HELPFUL_ONLY"],
        "supported_useful_target_occurrences": support["REQUIRED"]
        + support["HELPFUL_ONLY"],
        "supported_useful_rate": rate(
            support["REQUIRED"] + support["HELPFUL_ONLY"],
            supported_total,
        ),
        "baseline_A_useful_rate": rate(
            a_counts["REQUIRED"] + a_counts["HELPFUL_ONLY"],
            a_total,
        ),
        "required_in_A": required,
        "supported_REQUIRED_in_A": support["REQUIRED"],
        "unsupported_REQUIRED_in_A": required - support["REQUIRED"],
        "required_in_A_support_coverage": rate(support["REQUIRED"], required),
    }


def cohort(cases: Any) -> Any:
    """Aggregate only after all three valid case results; no cohort gate."""
    require(
        [c["case"] for c in cases] == ["0017", "0018", "0019"],
        "Cohort case identities/order",
    )
    for case in cases:
        validate_case_result(case)
    queries = [q for c in cases for q in c["queries"]]
    targets = [t for q in queries for t in q["targets"]]
    return {
        "case_categories": {c["case"]: c["category"] for c in cases},
        "totals": aggregate_queries(queries),
        "evidence_characteristics": distributions(targets),
        "source_label_diagnostics": source_labels(targets),
    }


def validate_case_result(case: Any) -> None:
    """Independently reject mutated classification arithmetic and case categories."""
    for query in case["queries"]:
        for target in query["targets"]:
            expected = classify_pair(
                Label(target["target_gold_label"]),
                Label(target["predecessor_gold_label"]),
            )
            require(
                target["classification"] == expected.direction
                and target["strong_beneficial"] == expected.strong_beneficial
                and target["strong_harmful"] == expected.strong_harmful,
                "Pair classification calculation",
            )
        require(
            query["pair_counts"] == count_pairs(query["targets"]),
            "Pair count calculation",
        )
        require(
            query["supported_gold_labels"]
            == label_counts(t["target_gold_label"] for t in query["targets"]),
            "Supported target calculation",
        )
    require(
        case["totals"] == aggregate_queries(case["queries"]),
        "Case aggregation calculation",
    )
    counts = case["totals"]["pair_counts"]
    require(
        case["category"]
        == case_category(counts["STRONG_BENEFICIAL"], counts["STRONG_HARMFUL"]),
        "Case-category calculation",
    )


def validate_cohort_result(cases: Any, aggregate: Any) -> None:
    """Reject an altered cohort sum or case-category map; no extra gate."""
    require(aggregate == cohort(cases), "Cohort aggregation calculation")
