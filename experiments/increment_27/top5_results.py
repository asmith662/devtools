# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, EM102, PLR0912, PLR2004, TRY003
"""Analyze frozen Increment-27 top-five judgments against saved rankings."""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    sha256_file,
)
from experiments.increment_27.lexical_top5_judgments import (
    content_identity as judgment_identity,
)
from experiments.increment_27.lexical_top5_judgments import (
    validate_frozen_judgments,
)

if TYPE_CHECKING:
    from pathlib import Path

METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")
LABELS = ("USEFUL", "NOT_USEFUL", "UNJUDGED")
EXPECTED_SHA256 = {
    "lexical_comparison_freeze.json": "5243f9243235edff4341a2520a8ca820753217699639b4f30ca2e8ce915d4c0f",
    "lexical_comparison_rankings.json": "7d566ba0e402d180b2ddfc0840f3002ec8c8337edbed0e3d14e391b717b5f46e",
    "lexical_top5_judgment_freeze.json": "6dac0200a8d8bd5493b99b74fc71a118eb6ce86a6b0b9d648adb2f13911eda10",
    "lexical_top5_pooled_pairs.json": "58078b9e43cc0d5fac49194d2c1f26823c60a338b0911dca20559bb855821212",
    "lexical_top5_reused_judgments.json": "13cbeceb9da69fbbb81324e3536b000fb164a86db9fd21a3ffd4c5b2d30b03d9",
    "lexical_top5_blinded_judgment_input.json": "00889562f8ef02d7ed8ef0a3804e92d36e5fd22a569776bbfceb44b806343b72",
    "lexical_top5_frozen_judgments.json": "5dd0fed43db4895f275277943783dd46971326f4c95efbac5ca8a9b869a34a75",
    "development_depth_summary.json": "8f977509b67d17b6ec77de6006213da2ccdc76879e7f9221b8a453b8ad1938ed",
    "canonical_positive_lexical_rankings.json": "6072195afe50376722c06157ae04e8b33ed1346e4c75c763d83f22f30dd72657",
}
EXPECTED_IDENTITIES = {
    "lexical_comparison_freeze.json": "bc01df59626dd19dceee2a78031d387273c62b26af5ccea4aef59b5dc33328ef",
    "lexical_comparison_rankings.json": "e256e90e5b09367f28a749fddc4cd0e39d1bf1645a0cf4931c16535eab57ea86",
    "lexical_top5_judgment_freeze.json": "ace8c18e42bc88f1304030c399f29daea66baf26772558ed867244e9dd20ce44",
    "lexical_top5_pooled_pairs.json": "d2c9c4fe41307c67dc647e78b400c0a15c6fd753a935e98a4c09ac3831ab0b3f",
    "lexical_top5_reused_judgments.json": "d7bc881400a2fc475c098f153c94829f23e39257c7bc3a8a857cfacb44cce1b9",
    "lexical_top5_blinded_judgment_input.json": "f2dabd43c8de35b9bc3f9ae4ef5d8d0149849bee6270d9f9744a6f533fc19555",
    "lexical_top5_frozen_judgments.json": "4ad2219a71f161c1ed3a7576300e707f0154b5bc8b1732015618b7f44e3e0960",
}
POOL_IDENTITY = "5095a7dbdd054bdba51c41d9a171ef718151caa05360557e8b702aae46b53390"


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def load_verified_sources(root: Path) -> dict[str, dict[str, Any]]:
    """Reject changed files, envelopes, populations, or source bindings."""
    sources: dict[str, dict[str, Any]] = {}
    for name, expected_sha in EXPECTED_SHA256.items():
        path = root / name
        if sha256_file(path) != expected_sha:
            raise ValueError(f"Frozen source SHA-256 changed: {name}.")
        source = _read_json(path)
        identity = EXPECTED_IDENTITIES.get(name)
        if identity is not None:
            if source.get("content_identity") != identity:
                raise ValueError(f"Frozen source identity changed: {name}.")
            value = (
                cast("dict[str, object]", source["payload"])
                if "payload" in source
                else {
                    key: item
                    for key, item in source.items()
                    if key != "content_identity"
                }
            )
            actual = (
                judgment_identity(value)
                if name == "lexical_top5_frozen_judgments.json"
                else _digest(value)
            )
            if actual != identity:
                raise ValueError(f"Frozen source content digest invalid: {name}.")
        sources[name] = source
    freeze = sources["lexical_top5_judgment_freeze.json"]["payload"]
    pool = sources["lexical_top5_pooled_pairs.json"]["payload"]
    reuse = sources["lexical_top5_reused_judgments.json"]["payload"]
    blind = sources["lexical_top5_blinded_judgment_input.json"]
    judged = sources["lexical_top5_frozen_judgments.json"]
    rankings = sources["lexical_comparison_rankings.json"]
    configuration = sources["lexical_comparison_freeze.json"]
    if (
        pool["population_identity"] != POOL_IDENTITY
        or freeze["pooled_population_identity"] != POOL_IDENTITY
        or reuse["pooled_population_identity"] != POOL_IDENTITY
        or freeze["reused_judgment_mapping_identity"]
        != sources["lexical_top5_reused_judgments.json"]["content_identity"]
        or freeze["new_blinded_population_identity"] != blind["content_identity"]
        or freeze["lexical_rankings_sha256"]
        != EXPECTED_SHA256["lexical_comparison_rankings.json"]
        or freeze["lexical_ranking_identity"] != rankings["content_identity"]
        or freeze["lexical_comparison_configuration_identity"]
        != configuration["content_identity"]
        or judged["payload"]["top5_freeze_identity"]
        != sources["lexical_top5_judgment_freeze.json"]["content_identity"]
        or sources["development_depth_summary.json"]["freeze_identity"]
        != freeze["phase0_freeze_identity"]
        or sources["canonical_positive_lexical_rankings.json"]["freeze_identity"]
        != freeze["phase0_freeze_identity"]
    ):
        raise ValueError("Frozen source identities do not bind to one another.")
    validate_frozen_judgments(blind, judged)
    dev = cast("list[str]", freeze["development_case_ids"])
    held = cast("list[str]", configuration["payload"]["heldout_case_ids_sealed"])
    if (
        len(dev) != 24
        or len(set(dev)) != 24
        or len(held) != 14
        or set(dev) & set(held)
        or freeze["heldout_confirmation_outcomes_included"] is not False
        or [case["case_id"] for case in rankings["cases"]] != dev
        or len(pool["pairs"]) != 191
        or len(reuse["records"]) != 58
        or len(judged["payload"]["judgments"]) != 133
    ):
        raise ValueError("Frozen development/held-out or judgment population changed.")
    source_paths = {
        "increment_25_confirmation_judgment_input": root.parent
        / "increment_25"
        / "confirmation_judgment_input.json",
        "increment_25_confirmation_judgments": root.parent
        / "increment_25"
        / "confirmation_frozen_judgments.json",
        "increment_25_confirmation_neutral_mapping": root.parent
        / "increment_25"
        / "confirmation_neutral_mapping.json",
        "increment_26_development_judgment_input": root.parent
        / "increment_26"
        / "development_judgment_input.json",
        "increment_26_development_judgments": root.parent
        / "increment_26"
        / "development_frozen_judgments.json",
    }
    if {name: sha256_file(path) for name, path in source_paths.items()} != freeze[
        "source_judgment_artifact_sha256"
    ]:
        raise ValueError("Prior judgment source hashes changed.")
    return sources


def join_judgments(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Join 58 exact reused and 133 neutral new labels to all 191 pairs."""
    pool = sources["lexical_top5_pooled_pairs.json"]["payload"]["pairs"]
    reused = sources["lexical_top5_reused_judgments.json"]["payload"]["records"]
    blind = sources["lexical_top5_blinded_judgment_input.json"]["payload"]["cases"]
    new = sources["lexical_top5_frozen_judgments.json"]["payload"]["judgments"]
    frozen = sources["lexical_top5_judgment_freeze.json"]["payload"]
    pair_map = {(row["case_id"], row["address"]): row for row in pool}
    if len(pair_map) != 191 or {key[0] for key in pair_map} != set(
        frozen["development_case_ids"]
    ):
        raise ValueError("Pooled pair identities repeat or include sealed cases.")
    case_by_need = {
        (
            row["information_need"]["purpose"],
            row["information_need"]["lexical_query"],
            row["parent_snapshot_sha"],
        ): row["case_id"]
        for row in pool
    }
    if len(case_by_need) != 24:
        raise ValueError("The 24 InformationNeed/snapshot identities are not unique.")
    neutral_cases: dict[str, str] = {}
    neutral_resources: set[tuple[str, str, str]] = set()
    for case in blind:
        need = case["information_need"]
        key = (need["purpose"], need["lexical_query"], case["parent_snapshot_sha"])
        case_id = case_by_need.get(key)
        if case_id is None or case["neutral_case_id"] in neutral_cases:
            raise ValueError("Neutral case has no unique frozen InformationNeed match.")
        neutral_cases[case["neutral_case_id"]] = case_id
        for resource in case["resources"]:
            neutral_resources.add(
                (
                    case["neutral_case_id"],
                    resource["address"],
                    resource["neutral_resource_id"],
                )
            )
    if len(neutral_cases) != 24 or len(neutral_resources) != 133:
        raise ValueError("Blinded identity population changed.")
    labels: dict[tuple[str, str], tuple[str, str]] = {}
    for row in reused:
        pair_key = (row["case_id"], row["address"])
        pair = pair_map.get(pair_key)
        if (
            pair is None
            or row["information_need"] != pair["information_need"]
            or row["parent_snapshot_sha"] != pair["parent_snapshot_sha"]
        ):
            raise ValueError("Reused label lacks exact pooled identity.")
        label = str(row["judgment"]).upper().replace("-", "_")
        if pair_key in labels or label not in LABELS:
            raise ValueError("Duplicate or invalid reused judgment.")
        labels[pair_key] = (label, "REUSED")
    for row in new:
        neutral_key = (row["case_id"], row["address"], row["resource_id"])
        if neutral_key not in neutral_resources:
            raise ValueError("New judgment lacks exact neutral resource identity.")
        pair_key = (neutral_cases[row["case_id"]], row["address"])
        if pair_key in labels or row["judgment"] not in LABELS:
            raise ValueError("Duplicate or invalid new judgment.")
        labels[pair_key] = (row["judgment"], "NEW")
    if set(labels) != set(pair_map) or len(labels) != 191:
        raise ValueError("Judgment join misses or adds a pooled pair.")
    if {key for key, value in labels.items() if value[1] == "NEW"} != {
        (row["case_id"], row["address"]) for row in frozen["new_judgment_pairs"]
    }:
        raise ValueError("New labels do not cover the exact frozen new-pair set.")
    return [
        {
            "case_id": row["case_id"],
            "address": row["address"],
            "parent_snapshot_sha": row["parent_snapshot_sha"],
            "judgment": labels[(row["case_id"], row["address"])][0],
            "judgment_provenance": labels[(row["case_id"], row["address"])][1],
            "method_ranks": row["method_ranks"],
        }
        for row in pool
    ]


def summarize_pairs(pairs: list[dict[str, Any]], case_ids: list[str]) -> dict[str, Any]:
    """Compute independent method, overlap, agreement, and coverage counts."""
    by_method = {
        method: [row for row in pairs if method in row["method_ranks"]]
        for method in METHODS
    }
    methods: dict[str, Any] = {}
    for method, rows in by_method.items():
        counts = Counter(row["judgment"] for row in rows)
        first = {
            case_id: min(
                (
                    row["method_ranks"][method]
                    for row in rows
                    if row["case_id"] == case_id and row["judgment"] == "USEFUL"
                ),
                default=None,
            )
            for case_id in case_ids
        }
        methods[method] = {
            "candidate_occurrences": len(rows),
            "labels": {label: counts[label] for label in LABELS},
            "useful_fraction_among_binary_judgments": {
                "numerator": counts["USEFUL"],
                "denominator": counts["USEFUL"] + counts["NOT_USEFUL"],
                "value": counts["USEFUL"] / (counts["USEFUL"] + counts["NOT_USEFUL"])
                if counts["USEFUL"] + counts["NOT_USEFUL"]
                else None,
            },
            "cases_with_useful": sum(value is not None for value in first.values()),
            "cases_without_useful": sum(value is None for value in first.values()),
            "first_useful_rank_by_case": first,
            "useful_shared_with_another_method": sum(
                row["judgment"] == "USEFUL" and len(row["method_ranks"]) > 1
                for row in rows
            ),
            "exclusive_labels": {
                label: sum(
                    row["judgment"] == label and len(row["method_ranks"]) == 1
                    for row in rows
                )
                for label in LABELS
            },
        }
    agreement: dict[str, Any] = {}
    for n in range(1, 6):
        rows = [row for row in pairs if len(row["method_ranks"]) == n]
        counts = Counter(row["judgment"] for row in rows)
        agreement[str(n)] = {
            "pairs": len(rows),
            "labels": {label: counts[label] for label in LABELS},
            "useful_fraction_among_binary_judgments": counts["USEFUL"]
            / (counts["USEFUL"] + counts["NOT_USEFUL"])
            if counts["USEFUL"] + counts["NOT_USEFUL"]
            else None,
        }
    pairwise: dict[str, Any] = {}
    for index, left in enumerate(METHODS):
        for right in METHODS[index + 1 :]:
            a = {(row["case_id"], row["address"]): row for row in by_method[left]}
            b = {(row["case_id"], row["address"]): row for row in by_method[right]}
            overlap = set(a) & set(b)
            pairwise[f"{left} x {right}"] = {
                "candidate_overlap": len(overlap),
                "useful_overlap": sum(
                    a[key]["judgment"] == "USEFUL" for key in overlap
                ),
                "useful_left_absent_from_right": sum(
                    row["judgment"] == "USEFUL"
                    for key, row in a.items()
                    if key not in b
                ),
                "useful_right_absent_from_left": sum(
                    row["judgment"] == "USEFUL"
                    for key, row in b.items()
                    if key not in a
                ),
            }
    cases: list[dict[str, Any]] = []
    for case_id in case_ids:
        useful = [
            row
            for row in pairs
            if row["case_id"] == case_id and row["judgment"] == "USEFUL"
        ]
        successful = [
            method
            for method in METHODS
            if any(method in row["method_ranks"] for row in useful)
        ]
        cases.append(
            {
                "case_id": case_id,
                "useful_methods": successful,
                "union_useful_count": len(useful),
                "canonical_found_useful": "canonical" in successful,
                "other_method_recovered_when_canonical_did_not": bool(useful)
                and "canonical" not in successful,
                "no_tested_method_found_useful": not useful,
            }
        )
    total = Counter(row["judgment"] for row in pairs)
    target_cases = {row["case_id"] for row in pairs if row["judgment"] == "USEFUL"}
    minimal: list[dict[str, Any]] = []
    for size in range(1, len(METHODS) + 1):
        for subset in itertools.combinations(METHODS, size):
            coverage = {
                row["case_id"]
                for row in pairs
                if row["judgment"] == "USEFUL"
                and set(row["method_ranks"]) & set(subset)
            }
            if coverage == target_cases:
                useful_pairs = {
                    (row["case_id"], row["address"])
                    for row in pairs
                    if row["judgment"] == "USEFUL"
                    and set(row["method_ranks"]) & set(subset)
                }
                minimal.append(
                    {
                        "methods": list(subset),
                        "cases_with_useful": len(coverage),
                        "distinct_useful_pairs": len(useful_pairs),
                    }
                )
        if minimal:
            break
    return {
        "methods": methods,
        "agreement": agreement,
        "pairwise": pairwise,
        "cases": cases,
        "union": {
            "distinct_pairs": len(pairs),
            "labels": {label: total[label] for label in LABELS},
            "cases_with_useful": len(target_cases),
            "cases_without_useful": len(case_ids) - len(target_cases),
        },
        "minimal_method_subsets_preserving_union_case_coverage": minimal,
    }


def build_analysis(root: Path) -> dict[str, object]:
    """Bind frozen evidence, join labels, and retain descriptive development results."""
    sources = load_verified_sources(root)
    freeze = sources["lexical_top5_judgment_freeze.json"]["payload"]
    case_ids = cast("list[str]", freeze["development_case_ids"])
    pairs = join_judgments(sources)
    summary = summarize_pairs(pairs, case_ids)
    rankings = sources["lexical_comparison_rankings.json"]["cases"]
    full_ranks = {
        case["case_id"]: {
            method: {row["address"]: row for row in case["rankings"][method]}
            for method in METHODS
        }
        for case in rankings
    }
    evidence_pairs: list[dict[str, Any]] = []
    for row in pairs:
        case_id, address = row["case_id"], row["address"]
        evidence: dict[str, Any] = {}
        for method, rank in row["method_ranks"].items():
            source_row = full_ranks[case_id][method].get(address)
            if source_row is None or source_row["rank"] != rank:
                raise ValueError("Pooled method rank differs from saved native ranking.")
            evidence[method] = source_row
        evidence_pairs.append({**row, "native_method_evidence": evidence})
    rrf_useful = [
        row
        for row in pairs
        if row["judgment"] == "USEFUL" and "rrf" in row["method_ranks"]
    ]
    rrf_details: list[dict[str, Any]] = []
    for row in rrf_useful:
        case_id, address = row["case_id"], row["address"]
        source_ranks = {
            method: full_ranks[case_id][method][address]["rank"]
            for method in ("canonical", "identifier", "path")
            if address in full_ranks[case_id][method]
        }
        rrf_details.append(
            {
                "case_id": case_id,
                "address": address,
                "rrf_rank": row["method_ranks"]["rrf"],
                "underlying_positive_ranks": source_ranks,
                "absent_from_canonical_top5": "canonical" not in row["method_ranks"],
                "absent_from_identifier_top5": "identifier" not in row["method_ranks"],
                "absent_from_both_top5": "canonical" not in row["method_ranks"]
                and "identifier" not in row["method_ranks"],
                "absent_from_all_three_input_top5": not set(row["method_ranks"])
                & {"canonical", "identifier", "path"},
            }
        )
    distinctive: dict[str, Any] = {}
    for method in ("bm25_plus", "identifier", "path"):
        rows = [
            row
            for row in pairs
            if row["judgment"] == "USEFUL"
            and method in row["method_ranks"]
            and "canonical" not in row["method_ranks"]
        ]
        distinctive[method] = [
            {
                "case_id": row["case_id"],
                "address": row["address"],
                "method_rank": row["method_ranks"][method],
                "canonical_positive_rank": full_ranks[row["case_id"]]["canonical"]
                .get(row["address"], {})
                .get("rank"),
                "method_membership": row["method_ranks"],
                "native_evidence": {
                    key: full_ranks[row["case_id"]][method][row["address"]].get(key)
                    for key in ("score", "component_scores", "matched_terms")
                    if key in full_ranks[row["case_id"]][method][row["address"]]
                },
            }
            for row in rows
        ]
    diverse = [
        row
        for row in pairs
        if row["judgment"] == "USEFUL" and "canonical" not in row["method_ranks"]
    ]
    depth_details = [
        {
            "case_id": row["case_id"],
            "address": row["address"],
            "canonical_positive_rank": full_ranks[row["case_id"]]["canonical"]
            .get(row["address"], {})
            .get("rank"),
            "shallow_methods": sorted(row["method_ranks"]),
        }
        for row in diverse
    ]
    depth_counts = Counter(
        "no_positive_canonical_rank"
        if row["canonical_positive_rank"] is None
        else "canonical_rank_6_to_50"
        if row["canonical_positive_rank"] <= 50
        else "canonical_rank_beyond_50"
        for row in depth_details
    )
    phase0 = sources["development_depth_summary.json"]["summary"]
    payload: dict[str, object] = {
        "source_artifact_sha256": EXPECTED_SHA256,
        "source_content_identities": EXPECTED_IDENTITIES,
        "pooled_population_identity": POOL_IDENTITY,
        "source_prior_judgment_sha256": freeze["source_judgment_artifact_sha256"],
        "development_case_ids": case_ids,
        "joined_pairs": evidence_pairs,
        "judgment_provenance_counts": {"REUSED": 58, "NEW": 133},
        **summary,
        "rrf": {
            "useful_top5": len(rrf_useful),
            "useful_absent_canonical_top5": sum(
                row["absent_from_canonical_top5"] for row in rrf_details
            ),
            "useful_absent_identifier_top5": sum(
                row["absent_from_identifier_top5"] for row in rrf_details
            ),
            "useful_absent_both_top5": sum(
                row["absent_from_both_top5"] for row in rrf_details
            ),
            "useful_absent_all_three_input_top5": sum(
                row["absent_from_all_three_input_top5"] for row in rrf_details
            ),
            "useful_details": rrf_details,
        },
        "useful_candidates_absent_canonical_top5": distinctive,
        "depth_connection": {
            "phase0_known_useful_reached_by_k": phase0["known_useful_reached_by_k"],
            "phase0_known_useful_unreachable": phase0[
                "known_useful_unreachable_by_positive_lexical_retrieval"
            ],
            "diverse_top5_useful_absent_canonical_top5": len(diverse),
            "canonical_rank_categories": {
                name: depth_counts[name]
                for name in (
                    "canonical_rank_6_to_50",
                    "canonical_rank_beyond_50",
                    "no_positive_canonical_rank",
                )
            },
            "pair_details": depth_details,
        },
        "interpretation_boundaries": [
            "Development-only historical devtools sample; 24 InformationNeeds.",
            "The 191-pair top-five union is exhaustively judged under three-state semantics; the repository corpus is not exhaustively judged.",
            "Method subset sufficiency is descriptive on this sample, not production selection.",
            "RRF combines positive ranked inputs and cannot create a resource outside their union.",
            "No held-out confirmation, retrieval execution, usefulness revision, or Context disclosure evaluation occurred.",
        ],
    }
    return {
        "schema": "devtools-i27-top5-development-results-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_analysis(root: Path) -> dict[str, object]:
    """Write deterministic results after exact source audit and judgment join."""
    artifact = build_analysis(root)
    write_artifact(
        path=root / "lexical_top5_development_results.json", payload=artifact
    )
    return artifact
