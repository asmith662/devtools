# Copyright (c) 2026
# ruff: noqa: COM812, EM101, PLR2004, TRY003
"""Fixed-budget development fusion of saved lexical and direct-import evidence."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import (
    MECHANICS_NAME,
    _digest,
    read_candidate_artifact,
)
from experiments.increment_27.structural_imports.mechanics import (
    build_freeze as build_structural_freeze,
)
from experiments.increment_27.window_unit import audit_saved_baseline

if TYPE_CHECKING:
    from pathlib import Path

FREEZE_NAME = "lexical_import_fusion_freeze.json"
CANDIDATES_NAME = "lexical_import_fusion_candidates.json"
STRUCTURAL_RESULT_IDENTITY = (
    "c1f70f19210e06e04d52ffff31ab9f0e58be950b73e5f4d8721765dc276600eb"
)
STRUCTURAL_RESULT_SHA256 = (
    "21d1bd3a3935c1a400d266bdd19538f59d90b11a541f4af331a6210fc7dbafcf"
)
FROZEN_JUDGMENT_SHA256 = (
    "08cf1c7e05e1299fbb76eaa956657cb625852765fa446009c3cc06c47a9f6383"
)


def _sources(root: Path) -> dict[str, str]:
    return {
        name: sha256_file(root / name)
        for name in (
            "experiment_freeze.json",
            "canonical_positive_lexical_rankings.json",
            "lexical_comparison_rankings.json",
            "structural_import_freeze.json",
            MECHANICS_NAME,
            "structural_import_development_results.json",
            "structural_import_judgment_freeze.json",
            "comparison_blinded_judgment_input.json",
            "comparison_frozen_judgments.json",
            "lexical_top5_development_results.json",
        )
    }


def build_freeze(root: Path) -> dict[str, Any]:
    """Freeze allocation and selection before consulting usefulness outcomes."""
    baseline, heldout = audit_saved_baseline(root)
    structural = cast("dict[str, Any]", build_structural_freeze(root))
    candidate = read_candidate_artifact(root / MECHANICS_NAME)
    source_hashes = _sources(root)
    if (
        source_hashes["structural_import_development_results.json"]
        != STRUCTURAL_RESULT_SHA256
        or source_hashes["comparison_frozen_judgments.json"] != FROZEN_JUDGMENT_SHA256
        or candidate["freeze_identity"] != structural["content_identity"]
        or [row["case_id"] for row in candidate["cases"]]
        != [row["case_id"] for row in baseline]
        or len(heldout) != 14
        or len(structural["payload"]["suspended_increment_26_case_ids_not_executed"])
        != 16
    ):
        raise ValueError("Saved development evidence or sealed partition differs.")
    payload = {
        "development_case_ids": [row["case_id"] for row in baseline],
        "heldout_case_ids_sealed": heldout,
        "suspended_increment_26_case_ids_not_executed": structural["payload"][
            "suspended_increment_26_case_ids_not_executed"
        ],
        "source_sha256": source_hashes,
        "source_content_identity": {
            "structural_import_candidates": candidate["content_identity"],
            "structural_import_development_results": STRUCTURAL_RESULT_IDENTITY,
            "structural_import_freeze": structural["content_identity"],
        },
        "budget_k": 5,
        "strategies": {
            "canonical_top5": "saved canonical positive ranks 1 through 5",
            "lexical4_import1": (
                "canonical positive ranks 1 through 4, then the first eligible "
                "direct-import candidate; if none, canonical rank 5"
            ),
            "structural_top5_diagnostic": (
                "up to five direct-import candidates; fewer where expansion is sparse; "
                "not a full-budget comparator"
            ),
        },
        "structural_selection_order": [
            "lowest canonical rank among distinct supporting lexical seeds",
            "highest count of distinct supporting lexical seeds",
            "resource address ascending as deterministic non-relevance tie-break",
        ],
        "direction_policy": (
            "outgoing and incoming are jointly eligible; preserve both memberships "
            "without a direction preference"
        ),
        "duplicate_policy": (
            "one resource address per InformationNeed and parent snapshot; "
            "retain all directed relation and seed support identities"
        ),
        "structural_order_caveat": (
            "no native structural relevance rank; seed rank is transferred lexical "
            "evidence, distinct seeds are corroboration, and address is only "
            "a tie-break"
        ),
        "usefulness_join_during_freeze_or_candidate_generation": False,
    }
    return {
        "schema": "devtools-i27-lexical-import-fusion-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_freeze(root: Path) -> dict[str, Any]:
    """Persist the outcome-independent protocol as a separate checkpoint."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing fusion freeze differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def _structural_evidence(case: dict[str, Any]) -> list[dict[str, Any]]:
    by_address: dict[str, dict[str, Any]] = {}
    for direction in ("outgoing", "incoming"):
        for candidate in case["arms"][direction]["candidates"]:
            address = str(candidate["address"])
            entry = by_address.setdefault(
                address,
                {
                    "address": address,
                    "canonical_positive_rank": candidate["canonical_positive_rank"],
                    "absent_all_saved_positive_lexical": candidate[
                        "absent_all_saved_positive_lexical"
                    ],
                    "outgoing": False,
                    "incoming": False,
                    "seed_addresses": [],
                    "relation_identities": [],
                    "path_count": 0,
                },
            )
            entry[direction] = True
            entry["seed_addresses"].extend(
                path["seed_address"] for path in candidate["paths"]
            )
            entry["relation_identities"].extend(
                path["relation_identity"] for path in candidate["paths"]
            )
            entry["path_count"] += len(candidate["paths"])
    seed_rank = {row["address"]: row["canonical_rank"] for row in case["seeds"]}
    for entry in by_address.values():
        entry["seed_addresses"] = sorted(set(entry["seed_addresses"]))
        entry["relation_identities"] = sorted(set(entry["relation_identities"]))
        entry["best_seed_rank"] = min(
            seed_rank[address] for address in entry["seed_addresses"]
        )
        entry["distinct_seed_count"] = len(entry["seed_addresses"])
    return sorted(
        by_address.values(),
        key=lambda row: (
            row["best_seed_rank"],
            -row["distinct_seed_count"],
            row["address"],
        ),
    )


def build_candidates(root: Path) -> dict[str, Any]:
    """Generate frozen five-resource surfaces from persisted mechanics only."""
    freeze = cast("dict[str, Any]", _read_json(root / FREEZE_NAME))
    if freeze != build_freeze(root):
        raise ValueError("Fusion freeze differs from saved input mechanics.")
    baseline, heldout = audit_saved_baseline(root)
    structural = read_candidate_artifact(root / MECHANICS_NAME)
    cases = []
    for lexical, imported in zip(baseline, structural["cases"], strict=True):
        if lexical["case_id"] != imported["case_id"]:
            raise ValueError("Fusion case order differs.")
        lexical_five = [
            {"address": row["address"], "canonical_positive_rank": row["rank"]}
            for row in lexical["positive_lexical_ordering"][:5]
        ]
        ranked_imports = _structural_evidence(imported)
        if len(lexical_five) != 5:
            raise ValueError("Canonical top-five capacity is incomplete.")
        fusion = [row["address"] for row in lexical_five[:4]]
        fusion.append(
            ranked_imports[0]["address"]
            if ranked_imports
            else lexical_five[4]["address"]
        )
        surfaces = {
            "canonical_top5": [row["address"] for row in lexical_five],
            "lexical4_import1": fusion,
            "structural_top5_diagnostic": [
                row["address"] for row in ranked_imports[:5]
            ],
        }
        if any(
            len(set(addresses)) != len(addresses) for addresses in surfaces.values()
        ):
            raise ValueError("Fusion contains a duplicate resource.")
        cases.append(
            {
                "case_id": lexical["case_id"],
                "information_need": imported["information_need"],
                "parent_snapshot_sha": imported["parent_snapshot_sha"],
                "canonical_top5_evidence": lexical_five,
                "ranked_structural_evidence": ranked_imports,
                "surfaces": surfaces,
            }
        )
    if (
        len(cases) != 24
        or [case["case_id"] for case in cases]
        != freeze["payload"]["development_case_ids"]
        or set(heldout) & {case["case_id"] for case in cases}
    ):
        raise ValueError("Fusion surfaced a sealed or missing case.")
    payload = {
        "freeze_identity": freeze["content_identity"],
        "development_case_ids": freeze["payload"]["development_case_ids"],
        "heldout_case_ids_sealed": heldout,
        "budget_k": 5,
        "cases": cases,
        "usefulness_join_performed": False,
    }
    return {
        "schema": "devtools-i27-lexical-import-fusion-candidates-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_candidates(root: Path) -> dict[str, Any]:
    """Persist candidate surfaces before opening any usefulness result."""
    artifact = build_candidates(root)
    path = root / CANDIDATES_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing fusion candidates differ.")
    write_artifact(path=path, payload=artifact)
    return artifact
