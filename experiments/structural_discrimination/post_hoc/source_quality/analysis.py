# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- bounded captured-projection diagnostic
"""POST_HOC / ORACLE / NON_GATING / NOT_RUNTIME_AVAILABLE exact decomposition."""

from __future__ import annotations

from collections import Counter
from statistics import median
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.structural_discrimination.stage_c.import_gold import LABELS, require
from experiments.structural_discrimination.stage_d import join

STATUS = ("POST_HOC", "ORACLE", "NON_GATING", "NOT_RUNTIME_AVAILABLE")
GROUPS = (
    "HAS_REQUIRED_SOURCE",
    "HAS_HELPFUL_SOURCE_NO_REQUIRED",
    "ONLY_UNNECESSARY_SOURCES",
)
USEFUL = frozenset(("REQUIRED", "HELPFUL_ONLY"))
PUBLISHED_STRONG_TARGET_RANK = 13
PUBLISHED_STRONG_PREDECESSOR_RANK = 12


def source_group(labels: Any) -> str:
    """Apply the predeclared precedence partition, never qualify runtime support."""
    labels = set(labels)
    require(bool(labels) and labels <= set(LABELS), "Missing/invalid source gold")
    return (
        GROUPS[0]
        if "REQUIRED" in labels
        else GROUPS[1]
        if "HELPFUL_ONLY" in labels
        else GROUPS[2]
    )


def gold_cells(gold: Any) -> Any:
    """Index exact same-obligation cells; reject missing and duplicate labels."""
    cells = {}
    addresses = set()
    obligations = {o["id"] for o in gold["obligations"]}
    for cell in gold["cells"]:
        key = (cell["obligation"], cell["address"])
        require(key not in cells, "Duplicate source/target gold cell")
        require(
            cell["obligation"] in obligations and cell["label"] in LABELS,
            "Wrong obligation/invalid gold",
        )
        require(
            all(cell[k] == gold["frame"][k] for k in join.FRAME),
            "Foreign gold frame",
        )
        cells[key] = cell
        addresses.add(cell["address"])
    require(
        len(addresses) == gold["frame"]["resource_count"]
        and set(cells) == {(o, a) for o in obligations for a in addresses},
        "Missing source/target gold cell",
    )
    return cells


def extract(case: Any, trace: Any, gold: Any, design: Any) -> tuple[Any, Any, Any]:
    """Join published targets/sources to captured References and authoritative gold."""
    join.validate_join(case["case"], design, trace, gold)
    join.validate_case_result(case)
    cells = gold_cells(gold)
    require(
        [q["obligation"] for q in case["queries"]]
        == [q["obligation"] for q in trace["queries"]],
        "Published obligation identities",
    )
    pairs, targets = [], []
    unsupported: list[Any] = []
    for q, captured in zip(case["queries"], trace["queries"], strict=True):
        obligation = q["obligation"]
        require(
            len(q["targets"]) == len(captured["annotations"]),
            "Published target count",
        )
        supported_addresses = set()
        for target, annotation, local in zip(
            q["targets"],
            captured["annotations"],
            captured["local_pairs"],
            strict=True,
        ):
            require(
                target["case"] == case["case"]
                and target["obligation"] == obligation
                and target["frame"] == captured["frame"],
                "Target case/obligation/frame",
            )
            require(
                target["target"] == annotation["target"] == local["target"]
                and target["predecessor"] == local["predecessor"],
                "Published target/predecessor identity",
            )
            native_target = target["target"]
            target_cell = cells[(obligation, native_target["address"])]
            require(
                target["obligation_identity"] == target_cell["obligation_identity"],
                "Target obligation identity",
            )
            require(
                target["target_gold_label"] == target_cell["label"]
                and target["target_primary_cell_pointer"]
                == target_cell["primary_cell_pointer"],
                "Target gold identity",
            )
            require(
                all(native_target[k] == target_cell[k] for k in join.IDENTITY),
                "Target content identity",
            )
            predecessor = cells[(obligation, target["predecessor"]["address"])]
            require(
                target["predecessor_gold_label"] == predecessor["label"],
                "Predecessor gold identity",
            )
            require(
                native_target["address"] not in supported_addresses,
                "Duplicate target identity",
            )
            supported_addresses.add(native_target["address"])
            require(
                len(target["sources"]) == len(annotation["sources"]),
                "Source count aggregation",
            )
            target_sources = []
            for source, native_source in zip(
                target["sources"],
                annotation["sources"],
                strict=True,
            ):
                require(
                    {k: source[k] for k in native_source} == native_source,
                    "Malformed Reference/source provenance",
                )
                source_cell = cells[(obligation, source["address"])]
                require(
                    source["source_gold_label"] == source_cell["label"]
                    and source["primary_cell_pointer"]
                    == source_cell["primary_cell_pointer"],
                    "Source gold identity",
                )
                require(
                    all(source[k] == source_cell[k] for k in join.IDENTITY),
                    "Source content identity",
                )
                require(
                    source["address"] != native_target["address"]
                    and source["a_rank"] < native_target["a_rank"],
                    "Self edge/source rank eligibility",
                )
                row = {
                    "case": case["case"],
                    "obligation": obligation,
                    "obligation_identity": target["obligation_identity"],
                    "frame": target["frame"],
                    "source": {k: source[k] for k in (*join.IDENTITY, "a_rank")},
                    "source_gold": source_cell["label"],
                    "source_primary_cell_pointer": source_cell["primary_cell_pointer"],
                    "target": native_target,
                    "target_gold": target_cell["label"],
                    "target_primary_cell_pointer": target_cell["primary_cell_pointer"],
                    "occurrence_count": len(source["supports"]),
                    "provenance": source["supports"],
                    "rank_distance": native_target["a_rank"] - source["a_rank"],
                    "original_local_pair": {
                        k: target[k]
                        for k in (
                            "predecessor",
                            "predecessor_gold_label",
                            "classification",
                            "strong_beneficial",
                            "strong_harmful",
                        )
                    },
                }
                pairs.append(row)
                target_sources.append(row)
            require(
                sum(p["occurrence_count"] for p in target_sources)
                == target["native_occurrence_count"]
                and len(target_sources) == target["distinct_supporting_source_count"],
                "Inconsistent occurrence aggregation",
            )
            targets.append(
                {
                    "case": case["case"],
                    "obligation": obligation,
                    "obligation_identity": target["obligation_identity"],
                    "frame": target["frame"],
                    "target": native_target,
                    "target_gold": target_cell["label"],
                    "target_primary_cell_pointer": target_cell["primary_cell_pointer"],
                    "source_group": source_group(
                        p["source_gold"] for p in target_sources
                    ),
                    "sources": [
                        {
                            "source": p["source"],
                            "source_gold": p["source_gold"],
                            "occurrence_count": p["occurrence_count"],
                        }
                        for p in target_sources
                    ],
                    "original_local_pair": target_sources[0]["original_local_pair"],
                },
            )
        required_in_a = {
            r["address"]
            for r in captured["A"]
            if cells[(obligation, r["address"])]["label"] == "REQUIRED"
        }
        expected_unsupported = required_in_a - supported_addresses
        require(
            {r["address"] for r in q["required_cells"] if r["unsupported"]}
            == expected_unsupported,
            "Unsupported REQUIRED accounting",
        )
        unsupported.extend(
            {
                "case": case["case"],
                "obligation": obligation,
                "gold_cell": cells[(obligation, address)],
                "status": "REQUIRED_IN_A_WITH_NO_DIRECT_STRUCTURAL_SUPPORT; not a source-qualification failure",
            }
            for address in sorted(expected_unsupported)
        )
    return pairs, targets, unsupported


def cross_tab(pairs: Any, *, occurrence_weighted: bool = False) -> Any:
    """Expose exact counts and both directional percentages with named denominators."""
    counts = {s: dict.fromkeys(LABELS, 0) for s in LABELS}
    for pair in pairs:
        counts[pair["source_gold"]][pair["target_gold"]] += (
            pair["occurrence_count"] if occurrence_weighted else 1
        )
    rows = {s: sum(counts[s].values()) for s in LABELS}
    columns = {t: sum(counts[s][t] for s in LABELS) for t in LABELS}
    collapsed = {
        s: dict.fromkeys(("USEFUL_TARGET", "UNNECESSARY_TARGET"), 0)
        for s in ("USEFUL_SOURCE", "UNNECESSARY_SOURCE")
    }
    for s in LABELS:
        for t in LABELS:
            collapsed["USEFUL_SOURCE" if s in USEFUL else "UNNECESSARY_SOURCE"][
                "USEFUL_TARGET" if t in USEFUL else "UNNECESSARY_TARGET"
            ] += counts[s][t]
    collapsed_columns = {
        target: sum(source_row[target] for source_row in collapsed.values())
        for target in ("USEFUL_TARGET", "UNNECESSARY_TARGET")
    }
    return {
        "weighting": "OCCURRENCE_WEIGHTED_SECONDARY"
        if occurrence_weighted
        else "DISTINCT_SOURCE_TARGET_OBLIGATION_PAIR_PRIMARY",
        "counts": counts,
        "row_totals": rows,
        "column_totals": columns,
        "total": sum(rows.values()),
        "row_percentages": {
            s: {t: 100 * counts[s][t] / rows[s] if rows[s] else None for t in LABELS}
            for s in LABELS
        },
        "column_percentages": {
            s: {
                t: 100 * counts[s][t] / columns[t] if columns[t] else None
                for t in LABELS
            }
            for s in LABELS
        },
        "useful_source_collapse": collapsed,
        "collapsed_row_percentages": {
            s: {
                t: 100 * n / sum(row.values()) if sum(row.values()) else None
                for t, n in row.items()
            }
            for s, row in collapsed.items()
        },
        "collapsed_column_percentages": {
            s: {
                t: 100 * n / collapsed_columns[t] if collapsed_columns[t] else None
                for t, n in row.items()
            }
            for s, row in collapsed.items()
        },
        "collapsed_useful_target_rate": {
            s: join.rate(collapsed[s]["USEFUL_TARGET"], sum(collapsed[s].values()))
            for s in collapsed
        },
    }


def target_groups(targets: Any) -> Any:
    """Partition each supported target once with original local outcomes intact."""
    result = {}
    for group in GROUPS:
        members = [t for t in targets if t["source_group"] == group]
        labels = join.label_counts(t["target_gold"] for t in members)
        outcomes = Counter(t["original_local_pair"]["classification"] for t in members)
        result[group] = {
            "targets": len(members),
            "target_labels": labels,
            "useful_target_rate": join.rate(
                labels["REQUIRED"] + labels["HELPFUL_ONLY"],
                len(members),
            ),
            "original_pair_outcomes": {
                k: outcomes[k] for k in ("BENEFICIAL", "NEUTRAL", "HARMFUL")
            },
            "STRONG_BENEFICIAL": sum(
                t["original_local_pair"]["strong_beneficial"] for t in members
            ),
            "STRONG_HARMFUL": sum(
                t["original_local_pair"]["strong_harmful"] for t in members
            ),
        }
    return result


def distribution(values: Any) -> Any:
    """Retain empirical ranks/density without selecting any numeric cutoff."""
    values = sorted(values)
    return {
        "n": len(values),
        "values": values,
        "min": min(values) if values else None,
        "median": median(values) if values else None,
        "max": max(values) if values else None,
    }


def characteristics(pairs: Any) -> Any:
    """Pair-weighted ranks and exact captured relation traffic by source gold."""
    result = {}
    for label in LABELS:
        rows = [p for p in pairs if p["source_gold"] == label]

        def resource_key(p: Any, role: str) -> tuple[Any, ...]:
            return (
                p["case"],
                tuple(p["frame"][k] for k in join.FRAME),
                p["obligation"],
                tuple(p[role][k] for k in join.IDENTITY),
            )

        result[label] = {
            "rank_weighting": "one sample per distinct source-target/obligation pair; a source repeats across its distinct targets",
            "source_A_rank": distribution(p["source"]["a_rank"] for p in rows),
            "target_A_rank": distribution(p["target"]["a_rank"] for p in rows),
            "rank_distance": distribution(p["rank_distance"] for p in rows),
            "distinct_source_resource_obligation_occurrences": len(
                {resource_key(p, "source") for p in rows},
            ),
            "distinct_target_resource_obligation_occurrences": len(
                {resource_key(p, "target") for p in rows},
            ),
            "distinct_source_target_obligation_pairs": len(rows),
            "native_occurrences": sum(p["occurrence_count"] for p in rows),
            "occurrences_per_pair": distribution(p["occurrence_count"] for p in rows),
        }
    return result


def surface(pairs: Any, targets: Any) -> Any:
    """Apply the same complete descriptive analysis at each declared scope."""
    return {
        "status": STATUS,
        "pair_weighted": cross_tab(pairs),
        "occurrence_weighted": cross_tab(pairs, occurrence_weighted=True),
        "target_source_quality": target_groups(targets),
        "rank_and_density": characteristics(pairs),
    }


def validate_records(pairs: Any, targets: Any) -> None:
    """Reject duplicate identities, provenance/count drift and partition defects."""
    pair_keys = set()
    for pair in pairs:
        key = (
            pair["case"],
            tuple(pair["frame"][k] for k in join.FRAME),
            pair["obligation"],
            pair["source"]["address"],
            pair["target"]["address"],
        )
        require(key not in pair_keys, "Duplicate source-target pair")
        pair_keys.add(key)
        require(
            pair["source_gold"] in LABELS and pair["target_gold"] in LABELS,
            "Invalid source/target gold",
        )
        require(
            pair["source"]["address"] != pair["target"]["address"]
            and pair["source"]["a_rank"] < pair["target"]["a_rank"],
            "Self/source rank eligibility",
        )
        facts = pair["provenance"]
        require(
            pair["occurrence_count"] == len(facts) > 0
            and len({f["fact_identity"] for f in facts}) == len(facts),
            "Inconsistent occurrence aggregation/provenance",
        )
        require(
            all(
                f["source_address"] == pair["source"]["address"]
                and f["target_address"] == pair["target"]["address"]
                and f["target_content_identity"] == pair["target"]["content_identity"]
                and f["source_snapshot_id"]
                == f["target_snapshot_id"]
                == pair["frame"]["snapshot_id"]
                for f in facts
            ),
            "Malformed Reference provenance",
        )
    target_keys = set()
    for target in targets:
        target_key = (
            target["case"],
            tuple(target["frame"][k] for k in join.FRAME),
            target["obligation"],
            target["target"]["address"],
        )
        require(target_key not in target_keys, "Duplicate target occurrence")
        target_keys.add(target_key)
        rows = [
            p
            for p in pairs
            if p["case"] == target["case"]
            and p["obligation"] == target["obligation"]
            and p["target"] == target["target"]
            and p["frame"] == target["frame"]
        ]
        require(
            rows
            and target["source_group"] == source_group(p["source_gold"] for p in rows),
            "Target source-group misclassification",
        )
        require(
            target["sources"]
            == [
                {
                    "source": p["source"],
                    "source_gold": p["source_gold"],
                    "occurrence_count": p["occurrence_count"],
                }
                for p in rows
            ],
            "Target source aggregation",
        )
        require(
            all(
                p["target_gold"] == target["target_gold"]
                and p["original_local_pair"] == target["original_local_pair"]
                for p in rows
            ),
            "Original pair-outcome partition",
        )
    require(
        {
            (
                p["case"],
                tuple(p["frame"][k] for k in join.FRAME),
                p["obligation"],
                p["target"]["address"],
            )
            for p in pairs
        }
        == target_keys,
        "Missing target/source pair association",
    )


def summarize(pairs: Any, targets: Any, unsupported: Any, published: Any) -> Any:
    """Preserve completed primary facts while decomposing them post hoc."""
    validate_records(pairs, targets)
    cases = {}
    for case in published["cases"]:
        identity = case["case"]
        case_pairs = [p for p in pairs if p["case"] == identity]
        case_targets = [t for t in targets if t["case"] == identity]
        obligations = {}
        for q in case["queries"]:
            o = q["obligation"]
            obligations[o] = surface(
                [p for p in case_pairs if p["obligation"] == o],
                [t for t in case_targets if t["obligation"] == o],
            )
        cases[identity] = {
            **surface(case_pairs, case_targets),
            "obligations": obligations,
            "unchanged_published_category": case["category"],
        }
    strong = [t for t in targets if t["original_local_pair"]["strong_beneficial"]]
    require(
        len(strong) == 1
        and strong[0]["case"] == "0018"
        and strong[0]["obligation"] == "O2"
        and strong[0]["target"]["address"]
        == "src/devtools/context/python/imports/declarations.py"
        and strong[0]["target"]["a_rank"] == PUBLISHED_STRONG_TARGET_RANK
        and strong[0]["target_gold"] == "REQUIRED",
        "Published strong-beneficial target identity",
    )
    predecessor = strong[0]["original_local_pair"]
    require(
        predecessor["predecessor"]["address"]
        == "docs/backlog/items/B-0008-investigate-repository-context-discovery.md"
        and predecessor["predecessor"]["a_rank"] == PUBLISHED_STRONG_PREDECESSOR_RANK
        and predecessor["predecessor_gold_label"] == "UNNECESSARY",
        "Published strong-beneficial predecessor identity",
    )
    groups = target_groups(targets)
    totals = published["cohort"]["totals"]
    require(
        len(targets) == totals["supported_targets"] == totals["local_pairs"]
        and len(pairs) == totals["distinct_source_target_obligation_pairs"]
        and sum(p["occurrence_count"] for p in pairs)
        == totals["qualifying_support_occurrences"],
        "Published cohort totals unchanged",
    )
    require(
        len(unsupported) == totals["unsupported_REQUIRED_in_A"],
        "Unsupported REQUIRED totals",
    )
    require(
        join.label_counts(t["target_gold"] for t in targets)
        == totals["supported_gold_labels"],
        "Published target labels unchanged",
    )
    require(
        all(
            sum(g["original_pair_outcomes"][k] for g in groups.values())
            == totals["pair_counts"][k]
            for k in ("BENEFICIAL", "NEUTRAL", "HARMFUL")
        )
        and all(
            sum(g[k] for g in groups.values()) == totals["pair_counts"][k]
            for k in ("STRONG_BENEFICIAL", "STRONG_HARMFUL")
        ),
        "Published pair outcomes unchanged",
    )
    return {
        "status": STATUS,
        "scope": "Completed DEVELOPMENT cohort only; descriptive oracle source gold is unavailable as a runtime feature",
        "cohort": surface(pairs, targets),
        "cases": cases,
        "strong_beneficial_trace": {
            "target": strong[0],
            "every_supporting_source_pair": [
                p
                for p in pairs
                if p["case"] == "0018"
                and p["obligation"] == "O2"
                and p["target"] == strong[0]["target"]
            ],
        },
        "supported_REQUIRED_targets": [
            t for t in targets if t["target_gold"] == "REQUIRED"
        ],
        "supported_useful_partition": {
            g: sum(
                t["source_group"] == g and t["target_gold"] in USEFUL for t in targets
            )
            for g in GROUPS
        },
        "supported_unnecessary_partition": {
            g: sum(
                t["source_group"] == g and t["target_gold"] == "UNNECESSARY"
                for t in targets
            )
            for g in GROUPS
        },
        "unsupported_REQUIRED_in_A": unsupported,
        "unchanged_published_categories": published["cohort"]["case_categories"],
        "unchanged_published_cohort_totals": totals,
        "published_interpretation_sha256": digest(
            published["non_gating_interpretation"].encode(),
        ),
    }


def validate_summary(
    result: Any,
    pairs: Any,
    targets: Any,
    unsupported: Any,
    published: Any,
) -> None:
    """Reject incorrect cross-tabs, percentages and local-outcome partitions."""
    require(
        json_bytes(result)
        == json_bytes(summarize(pairs, targets, unsupported, published)),
        "Incorrect cross-tab/source-group/pair-outcome partition",
    )
