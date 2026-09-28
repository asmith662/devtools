# Copyright (c) 2026
# ruff: noqa: COM812, EM101, EM102, PLR0912, PLR2004, TRY003, C901
"""Join one frozen RRF selection to exact development outcomes."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_36.mechanics import FREEZE_NAME, ROOT
from experiments.retrieval_judgment_coverage import validated_outcome_mappings

if TYPE_CHECKING:
    from pathlib import Path

RESULT_NAME = "simple_rank_fusion_development_results.json"
FROZEN_SHA256 = "b76d50e630eac938204feed1f218dac35f626ae73a06394c00a513a7b7d99ea2"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED", "NEVER_ADJUDICATED")
Key = tuple[str, str, str]


def _key(case_id: str, parent: str, address: str) -> Key:
    return (case_id, parent, address)


def _sources(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Require the written selection freeze before opening any outcome row."""
    freeze_path = root / FREEZE_NAME
    if sha256_file(freeze_path) != FROZEN_SHA256:
        raise ValueError("Pre-outcome fusion freeze differs.")
    freeze = _verified_json(freeze_path)
    if (
        freeze["payload"]["usefulness_outcomes_loaded"]
        or freeze["payload"]["confirmation_executed"]
    ):
        raise ValueError("Fusion freeze crossed its outcome boundary.")
    union_ref = freeze["payload"]["source_artifacts"]["heterogeneous_union"]
    union_path = root.parent / union_ref["path"]
    if sha256_file(union_path) != union_ref["sha256"]:
        raise ValueError("Frozen heterogeneous candidate inventory differs.")
    union = _verified_json(union_path)
    if (
        union["content_identity"]
        != freeze["payload"]["source_content_identities"]["heterogeneous_union"]
    ):
        raise ValueError("Heterogeneous Union content identity differs.")
    return (
        freeze,
        union,
        {
            "freeze": {
                "path": FREEZE_NAME,
                "content_identity": freeze["content_identity"],
                "sha256": FROZEN_SHA256,
            },
            "heterogeneous_union": {
                "path": union_ref["path"],
                "content_identity": union["content_identity"],
                "sha256": union_ref["sha256"],
            },
        },
    )


def _summarize(selected: list[dict[str, Any]]) -> dict[str, Any]:
    by_case: dict[str, list[dict[str, Any]]] = {}
    for row in selected:
        by_case.setdefault(row["case_id"], []).append(row)
    counts = Counter(row["outcome_knowledge"] for row in selected)
    return {
        "selected_candidate_pairs": len(selected),
        "states": {state: counts[state] for state in STATES},
        "cases_with_at_least_one_known_useful": sum(
            any(row["outcome_knowledge"] == "USEFUL" for row in rows)
            for rows in by_case.values()
        ),
        "cases_with_at_least_two_known_useful": sum(
            sum(row["outcome_knowledge"] == "USEFUL" for row in rows) >= 2
            for rows in by_case.values()
        ),
    }


def build_result(root: Path = ROOT) -> dict[str, Any]:
    """Compare frozen selections to saved baselines and known-useful ceiling."""
    freeze, union, source_artifacts = _sources(root)
    payload = union["payload"]
    basis = {case["case_id"]: case for case in payload["case_basis"]}
    candidates = {
        _key(row["case_id"], row["parent_snapshot_sha"], row["address"]): row
        for row in payload["candidates"]
    }
    if len(candidates) != payload["surfaces"]["heterogeneous"]["candidate_pairs"]:
        raise ValueError("Heterogeneous candidate identity repeats or differs.")
    frozen_cases = freeze["payload"]["cases"]
    if len(frozen_cases) != 24 or [case["case_id"] for case in frozen_cases] != [
        case["case_id"] for case in payload["case_basis"]
    ]:
        raise ValueError("Frozen fusion case population differs.")
    # Check the complete ranked universe, not only its selected five.
    for case in frozen_cases:
        case_id, parent = case["case_id"], case["parent_snapshot_sha"]
        if (
            case["information_need"] != basis[case_id]["information_need"]
            or parent != basis[case_id]["parent_snapshot_sha"]
        ):
            raise ValueError("Frozen fusion InformationNeed/snapshot differs.")
        if any(
            _key(case_id, parent, ranked["address"]) not in candidates
            for ranked in case["ranking"]
        ):
            raise ValueError("Fusion ranked a candidate outside Increment 35.")
        if case["selected_top_five"] != [row["address"] for row in case["ranking"][:5]]:
            raise ValueError("Frozen top five differs from full ranking.")
    strategies: dict[str, list[dict[str, Any]]] = {
        name: [] for name in ("canonical", "lexical_rrf", "fusion")
    }
    per_case = []
    for case in frozen_cases:
        case_id, parent = case["case_id"], case["parent_snapshot_sha"]
        indexed = {
            row["address"]: row
            for row in payload["candidates"]
            if row["case_id"] == case_id
        }
        selections = {
            "canonical": [
                row["address"]
                for row in sorted(
                    (
                        row
                        for row in indexed.values()
                        if row["lexical_ranks"].get("canonical", 10**9) <= 5
                    ),
                    key=lambda row: row["lexical_ranks"]["canonical"],
                )
            ],
            "lexical_rrf": [
                row["address"]
                for row in sorted(
                    (
                        row
                        for row in indexed.values()
                        if row["lexical_ranks"].get("rrf", 10**9) <= 5
                    ),
                    key=lambda row: row["lexical_ranks"]["rrf"],
                )
            ],
            "fusion": case["selected_top_five"],
        }
        if any(
            len(addresses) != 5 or len(set(addresses)) != 5
            for addresses in selections.values()
        ):
            raise ValueError("A strategy lacks five distinct frozen candidates.")
        for name, addresses in selections.items():
            for address in addresses:
                record = indexed[address]
                if record["outcome_knowledge"] not in STATES:
                    raise ValueError("Frozen candidate has an invalid outcome state.")
                strategies[name].append(
                    {
                        "case_id": case_id,
                        "parent_snapshot_sha": parent,
                        "address": address,
                        "information_need": basis[case_id]["information_need"],
                        "usefulness_semantics": USEFULNESS_SEMANTICS,
                        "outcome_knowledge": record["outcome_knowledge"],
                        "modalities": record["modalities"],
                        "structural_families": record["structural_families"],
                    }
                )
        canonical, fusion = set(selections["canonical"]), set(selections["fusion"])
        useful_canonical = sum(
            indexed[address]["outcome_knowledge"] == "USEFUL" for address in canonical
        )
        useful_fusion = sum(
            indexed[address]["outcome_knowledge"] == "USEFUL" for address in fusion
        )
        oracle = min(
            5, sum(row["outcome_knowledge"] == "USEFUL" for row in indexed.values())
        )
        saved_oracle = next(
            row["oracle_known_useful_at_k5"]
            for row in payload["per_case"]
            if row["case_id"] == case_id
        )
        if oracle != saved_oracle:
            raise ValueError("Known-useful heterogeneous oracle differs.")
        per_case.append(
            {
                "case_id": case_id,
                "dense_available": "dense" in case["source_coverage"],
                "canonical_known_useful": useful_canonical,
                "fusion_known_useful": useful_fusion,
                "delta_known_useful": useful_fusion - useful_canonical,
                "fusion_never_adjudicated": sum(
                    indexed[address]["outcome_knowledge"] == "NEVER_ADJUDICATED"
                    for address in fusion
                ),
                "oracle_known_useful_at_k5": oracle,
                "overlap_with_canonical": len(canonical & fusion),
                "replacements": len(fusion - canonical),
                "useful_additions": sum(
                    indexed[address]["outcome_knowledge"] == "USEFUL"
                    for address in fusion - canonical
                ),
                "useful_displacements": sum(
                    indexed[address]["outcome_knowledge"] == "USEFUL"
                    for address in canonical - fusion
                ),
                "structural_only_selected": sum(
                    indexed[address]["modalities"] == ["structural"]
                    for address in fusion
                ),
            }
        )
    for name, rows in strategies.items():
        known = [
            {**row, "judgment": row["outcome_knowledge"]}
            for row in rows
            if row["outcome_knowledge"] != "NEVER_ADJUDICATED"
        ]
        validated_outcome_mappings(known, {})
        if len(rows) != 120:
            raise ValueError(f"Strategy {name} does not select five per case.")
    summaries = {name: _summarize(rows) for name, rows in strategies.items()}
    canonical_useful = summaries["canonical"]["states"]["USEFUL"]
    fusion_useful = summaries["fusion"]["states"]["USEFUL"]
    oracle_total = sum(row["oracle_known_useful_at_k5"] for row in per_case)
    if (
        canonical_useful
        != payload["known_useful_oracle_at_k5"]["canonical_top_five_known_useful"]
        or oracle_total
        != payload["known_useful_oracle_at_k5"]["total_retained_known_useful"]
    ):
        raise ValueError("Canonical or heterogeneous known-useful ceiling differs.")
    result_payload = {
        "source_artifacts": source_artifacts,
        "algorithm": freeze["payload"]["algorithm"],
        "constant": freeze["payload"]["constant"],
        "budget_k": freeze["payload"]["budget_k"],
        "strategy_summaries": summaries,
        "selected_pairs": strategies,
        "per_case": per_case,
        "case_change_counts": {
            "improved": sum(row["delta_known_useful"] > 0 for row in per_case),
            "unchanged": sum(row["delta_known_useful"] == 0 for row in per_case),
            "worsened": sum(row["delta_known_useful"] < 0 for row in per_case),
        },
        "canonical_comparison": {
            "candidate_overlap": sum(row["overlap_with_canonical"] for row in per_case),
            "replacements": sum(row["replacements"] for row in per_case),
            "useful_additions": sum(row["useful_additions"] for row in per_case),
            "useful_displacements": sum(
                row["useful_displacements"] for row in per_case
            ),
            "net_known_useful_change": fusion_useful - canonical_useful,
        },
        "lexical_rrf_comparison": {
            "candidate_overlap": len(
                {
                    _key(row["case_id"], row["parent_snapshot_sha"], row["address"])
                    for row in strategies["lexical_rrf"]
                }
                & {
                    _key(row["case_id"], row["parent_snapshot_sha"], row["address"])
                    for row in strategies["fusion"]
                }
            ),
            "net_known_useful_change": fusion_useful
            - summaries["lexical_rrf"]["states"]["USEFUL"],
        },
        "known_useful_oracle": {
            "total_at_k5": oracle_total,
            "canonical_known_useful": canonical_useful,
            "available_headroom": oracle_total - canonical_useful,
            "fusion_increment_over_canonical": fusion_useful - canonical_useful,
            "fraction_of_known_headroom_captured": (fusion_useful - canonical_useful)
            / (oracle_total - canonical_useful),
        },
        "dense_coverage": {
            coverage: {
                "case_count": len(cases),
                "fusion": _summarize(
                    [
                        row
                        for row in strategies["fusion"]
                        if row["case_id"] in {case["case_id"] for case in cases}
                    ]
                ),
                "canonical": _summarize(
                    [
                        row
                        for row in strategies["canonical"]
                        if row["case_id"] in {case["case_id"] for case in cases}
                    ]
                ),
            }
            for coverage, cases in (
                ("available", [case for case in per_case if case["dense_available"]]),
                (
                    "unavailable",
                    [case for case in per_case if not case["dense_available"]],
                ),
            )
        },
        "selected_modality_membership": {
            "+".join(modalities): count
            for modalities, count in sorted(
                Counter(
                    tuple(row["modalities"]) for row in strategies["fusion"]
                ).items()
            )
        },
        "dense_supported_selected": sum(
            "dense" in row["modalities"] for row in strategies["fusion"]
        ),
        "graph_supported_selected": sum(
            any(family.startswith("graph_") for family in row["structural_families"])
            for row in strategies["fusion"]
        ),
        "structural_only_selected": sum(
            row["structural_only_selected"] for row in per_case
        ),
        "structural_rank_available": False,
        "graph_rank_available": False,
        "new_judgments_created": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i36-simple-rrf-development-result-v1",
        "content_identity": _digest(result_payload),
        "payload": result_payload,
    }


def write_result(root: Path = ROOT) -> dict[str, Any]:
    """Write only the deterministic post-freeze development result."""
    artifact = build_result(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing fusion result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    write_result()
