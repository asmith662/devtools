# Copyright (c) 2026
# ruff: noqa: C401, COM812, E501, EM101, PLR2004, TRY003
"""Join pre-frozen lexical rankings with existing labels; size unjudged pools."""

from __future__ import annotations

import hashlib
from collections import Counter
from typing import TYPE_CHECKING, cast

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_27.depth_diagnostic import (
    _judgment_source_identities,
    canonical_json_bytes,
    load_existing_judgments,
    sha256_file,
)
from experiments.increment_27.lexical_comparison import (
    K_CHECKPOINTS,
    METHODS,
    _read,
    build_comparison_freeze,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _rank_maps(
    rankings: Mapping[str, Sequence[Mapping[str, object]]],
) -> dict[str, dict[str, int]]:
    results: dict[str, dict[str, int]] = {}
    for method in METHODS:
        items = rankings[method]
        addresses = [str(item["address"]) for item in items]
        ranks = [int(cast("int", item["rank"])) for item in items]
        if len(addresses) != len(set(addresses)) or ranks != list(
            range(1, len(items) + 1)
        ):
            raise ValueError("Nonunique resources or noncontiguous positive ranks.")
        results[method] = dict(zip(addresses, ranks, strict=True))
    return results


def _case_diagnostic(
    *,
    case_id: str,
    maps: Mapping[str, Mapping[str, int]],
    judgments: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    labels = {str(item["address"]): str(item["judgment"]) for item in judgments}
    if len(labels) != len(judgments) or set(labels.values()) - {
        "useful",
        "not-useful",
        "unjudged",
    }:
        raise ValueError("Invalid existing three-state judgment population.")
    methods: dict[str, object] = {}
    baseline = maps["canonical"]
    for method in METHODS:
        ranks = maps[method]
        known_useful = sorted(
            ranks[address]
            for address, state in labels.items()
            if state == "useful" and address in ranks
        )
        at_k = {
            str(k): dict(
                Counter(
                    labels[address]
                    for address in labels
                    if ranks.get(address, 10**9) <= k
                )
            )
            for k in K_CHECKPOINTS
        }
        overlap = {
            str(k): {
                "shared": len(
                    set(address for address, rank in ranks.items() if rank <= k)
                    & set(address for address, rank in baseline.items() if rank <= k)
                ),
                "method_only": len(
                    set(address for address, rank in ranks.items() if rank <= k)
                    - set(address for address, rank in baseline.items() if rank <= k)
                ),
                "baseline_only": len(
                    set(address for address, rank in baseline.items() if rank <= k)
                    - set(address for address, rank in ranks.items() if rank <= k)
                ),
            }
            for k in K_CHECKPOINTS
        }
        methods[method] = {
            "positive_count": len(ranks),
            "known_useful_at_k": {
                str(k): sum(rank <= k for rank in known_useful) for k in K_CHECKPOINTS
            },
            "known_label_exposure_at_k": at_k,
            "first_known_useful_rank": known_useful[0] if known_useful else None,
            "known_useful_no_positive_rank": [
                address
                for address, state in labels.items()
                if state == "useful" and address not in ranks
            ],
            "comparison_to_canonical_at_k": overlap,
        }
    return {"case_id": case_id, "judged_pair_count": len(labels), "methods": methods}


def _pool(
    *,
    case_maps: Sequence[tuple[str, Mapping[str, Mapping[str, int]]]],
    labels_by_case: Mapping[str, Mapping[str, str]],
    depth: int,
) -> dict[str, object]:
    total = judged = 0
    support_histogram: Counter[int] = Counter()
    exclusive: Counter[str] = Counter()
    method_counts: Counter[str] = Counter()
    for case_id, maps in case_maps:
        by_address: dict[str, set[str]] = {}
        for method, ranks in maps.items():
            for address, rank in ranks.items():
                if rank <= depth:
                    by_address.setdefault(address, set()).add(method)
                    method_counts[method] += 1
        total += len(by_address)
        judged += sum(address in labels_by_case[case_id] for address in by_address)
        for methods in by_address.values():
            support_histogram[len(methods)] += 1
            if len(methods) == 1:
                exclusive[next(iter(methods))] += 1
    return {
        "depth_per_method": depth,
        "unique_pairs": total,
        "already_judged_pairs": judged,
        "new_judgments_required": total - judged,
        "method_candidate_counts": dict(sorted(method_counts.items())),
        "method_support_histogram": dict(sorted(support_histogram.items())),
        "method_exclusive_pairs": {method: exclusive[method] for method in METHODS},
        "estimated_new_judgment_hours_at_1_to_2_minutes_each": [
            round((total - judged) / 60, 1),
            round((total - judged) / 30, 1),
        ],
    }


def analyze_comparison(*, output_root: Path) -> dict[str, object]:
    """Analyze only after a complete ranking artifact exists on disk."""
    freeze = build_comparison_freeze(output_root=output_root)
    if _read(output_root / "lexical_comparison_freeze.json") != freeze:
        raise ValueError("Frozen configuration identity changed.")
    rankings_path = output_root / "lexical_comparison_rankings.json"
    rankings = _read(rankings_path)
    identity = rankings.get("content_identity")
    ranking_body = {
        key: value for key, value in rankings.items() if key != "content_identity"
    }
    if (
        identity != _digest(ranking_body)
        or rankings.get("configuration_identity") != freeze["content_identity"]
    ):
        raise ValueError(
            "Rankings are incomplete or not bound to frozen configuration."
        )
    cases = cast("list[dict[str, object]]", rankings["cases"])
    allowed = cast(
        "list[str]",
        cast("dict[str, object]", freeze["payload"])["development_case_ids"],
    )
    if [case["case_id"] for case in cases] != allowed:
        raise ValueError("Rankings include missing, extra, or held-out cases.")
    task_freeze = _read(
        output_root.parent / "increment_25" / "task_population_freeze.json"
    )
    task_cards = cast(
        "list[dict[str, object]]",
        cast("dict[str, object]", task_freeze["payload"])["task_cards"],
    )
    cards = {
        str(item["case_id"]): _task_card(item)
        for item in task_cards
        if str(item["case_id"]) in allowed
    }
    judgments = load_existing_judgments(experiment_root=output_root.parent, cards=cards)
    if sum(map(len, judgments.values())) != 120:
        raise ValueError("Expected exactly 120 reused judgments.")
    labels_by_case = {
        case_id: {str(item["address"]): str(item["judgment"]) for item in records}
        for case_id, records in judgments.items()
    }
    case_maps: list[tuple[str, dict[str, dict[str, int]]]] = []
    diagnostics: list[dict[str, object]] = []
    for case in cases:
        case_id = str(case["case_id"])
        card = cards[case_id]
        if (
            case["parent_snapshot_sha"] != card.parent_snapshot_sha
            or case["query_text"] != card.lexical_query
        ):
            raise ValueError("Ranking task identity differs from frozen card.")
        maps = _rank_maps(cast("dict[str, list[dict[str, object]]]", case["rankings"]))
        case_maps.append((case_id, maps))
        diagnostics.append(
            _case_diagnostic(case_id=case_id, maps=maps, judgments=judgments[case_id])
        )
    aggregate: dict[str, object] = {}
    for method in METHODS:
        entries = [
            cast(
                "dict[str, object]", cast("dict[str, object]", case["methods"])[method]
            )
            for case in diagnostics
        ]
        aggregate[method] = {
            "positive_candidates": sum(
                int(cast("int", entry["positive_count"])) for entry in entries
            ),
            "known_useful_at_k": {
                str(k): sum(
                    int(cast("dict[str, int]", entry["known_useful_at_k"])[str(k)])
                    for entry in entries
                )
                for k in K_CHECKPOINTS
            },
            "known_label_exposure_at_k": {
                str(k): dict(
                    sum(
                        (
                            Counter(
                                cast(
                                    "dict[str, int]",
                                    cast(
                                        "dict[str, object]",
                                        entry["known_label_exposure_at_k"],
                                    )[str(k)],
                                )
                            )
                            for entry in entries
                        ),
                        Counter(),
                    )
                )
                for k in K_CHECKPOINTS
            },
            "known_useful_no_positive_rank": sum(
                len(cast("list[str]", entry["known_useful_no_positive_rank"]))
                for entry in entries
            ),
            "cases_with_known_useful_in_positive_ranking": sum(
                entry["first_known_useful_rank"] is not None for entry in entries
            ),
            "comparison_to_canonical_at_k": {
                str(k): {
                    name: sum(
                        int(
                            cast(
                                "dict[str, int]",
                                cast(
                                    "dict[str, object]",
                                    entry["comparison_to_canonical_at_k"],
                                )[str(k)],
                            )[name]
                        )
                        for entry in entries
                    )
                    for name in ("shared", "method_only", "baseline_only")
                }
                for k in K_CHECKPOINTS
            },
        }
    artifact: dict[str, object] = {
        "schema": "devtools-i27-lexical-comparison-analysis-v1",
        "configuration_identity": freeze["content_identity"],
        "rankings_identity": identity,
        "rankings_sha256": sha256_file(rankings_path),
        "judgment_source_sha256": _judgment_source_identities(output_root.parent),
        "known_judgment_counts": dict(
            Counter(
                label for labels in labels_by_case.values() for label in labels.values()
            )
        ),
        "cases": diagnostics,
        "aggregate": aggregate,
        "prospective_pools": [
            _pool(case_maps=case_maps, labels_by_case=labels_by_case, depth=k)
            for k in (5, 10, 20)
        ],
        "interpretation_boundary": "Incomplete existing judgments; counts are not exhaustive Recall@K and no unknown candidate receives a usefulness label.",
    }
    artifact["content_identity"] = _digest(artifact)
    write_artifact(
        path=output_root / "lexical_comparison_analysis.json", payload=artifact
    )
    return artifact
