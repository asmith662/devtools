# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, EM102, PLR0912, PLR0915, PLR2004, TRY003
"""Mechanical outcome join for the frozen five-resource fusion surfaces."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.fusion import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    STRUCTURAL_RESULT_IDENTITY,
    build_candidates,
    build_freeze,
)
from experiments.increment_27.structural_imports.analysis import (
    RESULT_NAME as STRUCTURAL_RESULT_NAME,
)
from experiments.increment_27.structural_imports.analysis import (
    build_results as build_structural_results,
)
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_27.top5_results import build_analysis as build_top5_results

if TYPE_CHECKING:
    from pathlib import Path

RESULT_NAME = "lexical_import_fusion_development_results.json"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")


def _load_labels(root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    structural_saved = cast("dict[str, Any]", _read_json(root / STRUCTURAL_RESULT_NAME))
    lexical_saved = cast(
        "dict[str, Any]", _read_json(root / "lexical_top5_development_results.json")
    )
    if structural_saved != build_structural_results(
        root
    ) or lexical_saved != build_top5_results(root):
        raise ValueError("A frozen source judgment result does not reproduce.")
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for source_name, source_rows in (
        ("structural", structural_saved["payload"]["joined_population"]),
        ("lexical_top5", lexical_saved["payload"]["joined_pairs"]),
    ):
        for row in source_rows:
            key = (str(row["case_id"]), str(row["address"]))
            state = str(row["judgment"])
            parent = str(row["parent_snapshot_sha"])
            previous = rows.get(key)
            if state not in STATES or (
                previous
                and (previous["judgment"], previous["parent_snapshot_sha"])
                != (state, parent)
            ):
                raise ValueError("Frozen judgment sources disagree on an exact pair.")
            rows[key] = {
                "judgment": state,
                "parent_snapshot_sha": parent,
                "source": source_name if previous is None else "both_frozen_sources",
            }
    return rows


def _count(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["judgment"] for row in rows)
    judged = counts["USEFUL"] + counts["NOT_USEFUL"]
    return {
        "candidate_occurrences": len(rows),
        "distinct_pairs": len({(row["case_id"], row["address"]) for row in rows}),
        "USEFUL": counts["USEFUL"],
        "NOT_USEFUL": counts["NOT_USEFUL"],
        "UNJUDGED": counts["UNJUDGED"],
        "judged_total": judged,
        "useful_rate_among_judged": round(counts["USEFUL"] / judged, 6)
        if judged
        else None,
    }


def build_results(root: Path) -> dict[str, Any]:
    """Join only after the independent freeze and candidate surfaces exist."""
    freeze = cast("dict[str, Any]", _read_json(root / FREEZE_NAME))
    candidates = cast("dict[str, Any]", _read_json(root / CANDIDATES_NAME))
    if freeze != build_freeze(root) or candidates != build_candidates(root):
        raise ValueError("Frozen fusion protocol or candidate surfaces differ.")
    if candidates["payload"]["freeze_identity"] != freeze["content_identity"]:
        raise ValueError("Fusion candidate surface is bound to another freeze.")
    labels = _load_labels(root)
    joined: dict[str, list[dict[str, Any]]] = {
        name: [] for name in freeze["payload"]["strategies"]
    }
    per_case: list[dict[str, Any]] = []
    substitutions: list[dict[str, Any]] = []
    oracle_cases: list[dict[str, Any]] = []
    for case in candidates["payload"]["cases"]:
        case_id = str(case["case_id"])
        parent = str(case["parent_snapshot_sha"])
        structural = {row["address"]: row for row in case["ranked_structural_evidence"]}
        case_counts: dict[str, Any] = {"case_id": case_id}
        for name, addresses in case["surfaces"].items():
            current = []
            for address in addresses:
                pair = labels.get((case_id, address))
                if pair is None:
                    raise ValueError(f"New judgment required: {case_id} {address}")
                if pair["parent_snapshot_sha"] != parent:
                    raise ValueError("Fusion pair parent snapshot differs.")
                provenance = structural.get(address)
                row = {
                    "case_id": case_id,
                    "information_need": case["information_need"],
                    "parent_snapshot_sha": parent,
                    "address": address,
                    "judgment": pair["judgment"],
                    "judgment_source": pair["source"],
                    "canonical_positive_rank": (
                        provenance["canonical_positive_rank"]
                        if provenance
                        else next(
                            item["canonical_positive_rank"]
                            for item in case["canonical_top5_evidence"]
                            if item["address"] == address
                        )
                    ),
                    "outgoing": bool(provenance and provenance["outgoing"]),
                    "incoming": bool(provenance and provenance["incoming"]),
                    "absent_all_saved_positive_lexical": bool(
                        provenance and provenance["absent_all_saved_positive_lexical"]
                    ),
                }
                joined[name].append(row)
                current.append(row)
            case_counts[name] = {
                "candidate_count": len(current),
                "USEFUL": sum(row["judgment"] == "USEFUL" for row in current),
                "NOT_USEFUL": sum(row["judgment"] == "NOT_USEFUL" for row in current),
                "UNJUDGED": sum(row["judgment"] == "UNJUDGED" for row in current),
                "useful_all_lexical_escape": sum(
                    row["judgment"] == "USEFUL"
                    and row["absent_all_saved_positive_lexical"]
                    for row in current
                ),
            }
        baseline_useful = case_counts["canonical_top5"]["USEFUL"]
        fusion_useful = case_counts["lexical4_import1"]["USEFUL"]
        case_counts["fusion_minus_canonical_useful"] = fusion_useful - baseline_useful
        per_case.append(case_counts)

        baseline_fifth = case["surfaces"]["canonical_top5"][4]
        replacement = case["surfaces"]["lexical4_import1"][4]
        if replacement != baseline_fifth:
            lexical_state = labels[(case_id, baseline_fifth)]["judgment"]
            structural_state = labels[(case_id, replacement)]["judgment"]
            if "UNJUDGED" in (lexical_state, structural_state):
                kind = "unresolved"
            elif structural_state == "USEFUL" and lexical_state == "NOT_USEFUL":
                kind = "beneficial"
            elif structural_state == "NOT_USEFUL" and lexical_state == "USEFUL":
                kind = "harmful"
            elif structural_state == "USEFUL" and lexical_state == "USEFUL":
                kind = "useful_for_useful"
            else:
                kind = "not_useful_for_not_useful"
            substitutions.append(
                {
                    "case_id": case_id,
                    "displaced_lexical_address": baseline_fifth,
                    "displaced_lexical_judgment": lexical_state,
                    "selected_structural_address": replacement,
                    "selected_structural_judgment": structural_state,
                    "selected_structural_evidence": structural[replacement],
                    "kind": kind,
                }
            )
        available = set(case["surfaces"]["canonical_top5"]) | set(structural)
        oracle_useful = sum(
            labels[(case_id, address)]["judgment"] == "USEFUL" for address in available
        )
        oracle_cases.append(
            {
                "case_id": case_id,
                "available_candidate_count": len(available),
                "judged_useful_in_union": oracle_useful,
                "maximum_useful_at_k5": min(5, oracle_useful),
            }
        )
    if len(per_case) != 24 or len({row["case_id"] for row in per_case}) != 24:
        raise ValueError("Fusion development case partition differs.")
    summary = {}
    for name, rows in joined.items():
        counts = _count(rows)
        counts.update(
            {
                "cases_with_at_least_one_useful": sum(
                    case[name]["USEFUL"] >= 1 for case in per_case
                ),
                "cases_with_at_least_two_useful": sum(
                    case[name]["USEFUL"] >= 2 for case in per_case
                ),
                "cases_with_zero_useful": sum(
                    case[name]["USEFUL"] == 0 for case in per_case
                ),
                "useful_all_lexical_escape": sum(
                    case[name]["useful_all_lexical_escape"] for case in per_case
                ),
                "gap_to_oracle_useful_at_k5": sum(
                    case["maximum_useful_at_k5"] for case in oracle_cases
                )
                - counts["USEFUL"],
            }
        )
        summary[name] = counts
    substitution_counts = Counter(row["kind"] for row in substitutions)
    oracle = {
        "definition": (
            "post-hoc outcome-aware upper bound over canonical top five plus "
            "all saved direct-import additions; not an executable strategy"
        ),
        "per_case": oracle_cases,
        "maximum_useful_at_k5": sum(
            row["maximum_useful_at_k5"] for row in oracle_cases
        ),
        "cases_coverable_at_least_one": sum(
            row["judged_useful_in_union"] >= 1 for row in oracle_cases
        ),
        "cases_coverable_at_least_two": sum(
            row["judged_useful_in_union"] >= 2 for row in oracle_cases
        ),
    }
    payload = {
        "freeze_identity": freeze["content_identity"],
        "freeze_sha256": sha256_file(root / FREEZE_NAME),
        "candidate_identity": candidates["content_identity"],
        "candidate_sha256": sha256_file(root / CANDIDATES_NAME),
        "structural_result_identity": STRUCTURAL_RESULT_IDENTITY,
        "structural_result_sha256": sha256_file(root / STRUCTURAL_RESULT_NAME),
        "lexical_top5_result_sha256": sha256_file(
            root / "lexical_top5_development_results.json"
        ),
        "development_case_ids": freeze["payload"]["development_case_ids"],
        "heldout_case_ids_sealed": freeze["payload"]["heldout_case_ids_sealed"],
        "joined_surfaces": joined,
        "strategy_results": summary,
        "per_case": per_case,
        "fusion_vs_canonical": {
            "cases_gaining_useful": sum(
                row["fusion_minus_canonical_useful"] > 0 for row in per_case
            ),
            "cases_losing_useful": sum(
                row["fusion_minus_canonical_useful"] < 0 for row in per_case
            ),
            "cases_equal_useful": sum(
                row["fusion_minus_canonical_useful"] == 0 for row in per_case
            ),
            "substitution_counts": {
                name: substitution_counts[name]
                for name in (
                    "beneficial",
                    "harmful",
                    "useful_for_useful",
                    "unresolved",
                    "not_useful_for_not_useful",
                )
            },
            "substitutions": substitutions,
        },
        "oracle_upper_bound": oracle,
        "new_judgments_required": 0,
        "judgments_changed": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i27-lexical-import-fusion-development-results-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_results(root: Path) -> dict[str, Any]:
    """Persist the exact joined analysis after all pair coverage checks pass."""
    artifact = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing fusion result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
