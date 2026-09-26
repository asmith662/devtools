# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR0913, PLR2004, TRY003
"""Exact frozen-judgment reuse and unlabeled-work counts only."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import (
    _read_json,
    load_existing_judgments,
    prior_judgment_matches,
    sha256_file,
)
from experiments.increment_27.structural_imports.mechanics import (
    DIRECTIONS,
    MECHANICS_NAME,
    RAW_CANDIDATE_SHA256,
    _digest,
    build_freeze,
    read_candidate_artifact,
)
from experiments.increment_27.top5_results import (
    join_judgments as join_top5_judgments,
)
from experiments.increment_27.top5_results import (
    load_verified_sources as load_top5_sources,
)
from experiments.increment_27.window_results import (
    join_frozen_labels as join_window_judgments,
)
from experiments.increment_27.window_results import (
    load_verified_sources as load_window_sources,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from experiments.increment_25.task_population import TaskCard

COST_NAME = "structural_import_judgment_cost.json"
STATES = {"USEFUL", "NOT_USEFUL", "UNJUDGED"}
CATEGORIES = ("top-five-overlap", "deeper-positive-rank", "no-positive-rank")


def _normalize_state(value: str) -> str:
    state = value.upper().replace("-", "_")
    if state not in STATES:
        raise ValueError("Prior judgment has an invalid three-state value.")
    return state


def _add_prior(
    prior: dict[tuple[str, str], dict[str, str]],
    *,
    card: TaskCard,
    address: str,
    judgment: str,
    source: str,
    information_need: Mapping[str, object],
    parent_snapshot_sha: str,
    semantics: str,
) -> None:
    if not prior_judgment_matches(
        card=card,
        prior_information_need=information_need,
        prior_parent_snapshot=parent_snapshot_sha,
        prior_address=address,
        resource_address=address,
        prior_usefulness_semantics=semantics,
    ):
        raise ValueError(
            "Prior judgment fails exact InformationNeed/snapshot/resource/semantics reuse."
        )
    state = _normalize_state(judgment)
    key = (card.case_id, address)
    existing = prior.get(key)
    if existing is not None and existing["state"] != state:
        raise ValueError("Frozen sources disagree about one exact judgment pair.")
    prior.setdefault(key, {"state": state, "source": source})


def load_prior_states(
    root: Path, cards: Mapping[str, TaskCard]
) -> dict[tuple[str, str], dict[str, str]]:
    """Verify existing frozen sources and preserve all three label states."""
    prior: dict[tuple[str, str], dict[str, str]] = {}
    earlier = load_existing_judgments(experiment_root=root.parent, cards=cards)
    for case_id, records in earlier.items():
        card = cards[case_id]
        for row in records:
            _add_prior(
                prior,
                card=card,
                address=str(row["address"]),
                judgment=str(row["judgment"]),
                source=str(row["source"]),
                information_need=cast(
                    "dict[str, object]", row["information_need_identity"]
                ),
                parent_snapshot_sha=str(row["parent_snapshot_sha"]),
                semantics=str(row["judgment_semantics"]),
            )
    top5 = join_top5_judgments(load_top5_sources(root))
    for row in top5:
        case_id = str(row["case_id"])
        card = cards[case_id]
        _add_prior(
            prior,
            card=card,
            address=str(row["address"]),
            judgment=str(row["judgment"]),
            source="increment-27-top-five",
            information_need={
                "purpose": card.information_need_purpose,
                "lexical_query": card.lexical_query,
            },
            parent_snapshot_sha=str(row["parent_snapshot_sha"]),
            semantics=USEFULNESS_SEMANTICS,
        )
    window = join_window_judgments(load_window_sources(root))
    for row in window:
        case_id = str(row["case_id"])
        _add_prior(
            prior,
            card=cards[case_id],
            address=str(row["address"]),
            judgment=str(row["judgment"]),
            source="increment-27-window",
            information_need=cast("dict[str, object]", row["information_need"]),
            parent_snapshot_sha=str(row["parent_snapshot_sha"]),
            semantics=USEFULNESS_SEMANTICS,
        )
    return prior


def _counts(
    rows: list[dict[str, Any]],
    prior: Mapping[tuple[str, str], Mapping[str, str]],
) -> dict[str, int]:
    reused = sum((row["case_id"], row["address"]) in prior for row in rows)
    return {"total": len(rows), "reused": reused, "new": len(rows) - reused}


def build_cost(
    *,
    mechanics: Mapping[str, Any],
    prior: Mapping[tuple[str, str], Mapping[str, str]],
    cards: Mapping[str, TaskCard],
) -> dict[str, Any]:
    """Count exact reuse without reporting usefulness by structural origin."""
    cases = cast("list[dict[str, Any]]", mechanics["cases"])
    if len(cases) != 24 or set(cards) != {str(row["case_id"]) for row in cases}:
        raise ValueError("Cost audit has an incomplete development population.")
    all_rows: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    by_case: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        card = cards[case_id]
        if case["parent_snapshot_sha"] != card.parent_snapshot_sha or case[
            "information_need"
        ] != {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        }:
            raise ValueError("Candidate case differs from frozen task identity.")
        arms = cast("dict[str, dict[str, Any]]", case["arms"])
        local: dict[str, list[dict[str, Any]]] = {}
        local_controls: dict[str, list[dict[str, Any]]] = {}
        for direction in DIRECTIONS:
            candidates = cast("list[dict[str, Any]]", arms[direction]["candidates"])
            local[direction] = [
                {
                    "case_id": case_id,
                    "address": str(row["address"]),
                    "direction": direction,
                    "canonical_category": row["canonical_category"],
                    "absent_all_saved_positive_lexical": row[
                        "absent_all_saved_positive_lexical"
                    ],
                }
                for row in candidates
            ]
            control = cast(
                "dict[str, Any]", arms[direction]["same_volume_lexical_control"]
            )
            local_controls[direction] = [
                {"case_id": case_id, "address": str(address), "direction": direction}
                for address in control["addresses"]
            ]
            all_rows.extend(local[direction])
            controls.extend(local_controls[direction])
        union_map: dict[tuple[str, str], dict[str, Any]] = {}
        for row in (*local["outgoing"], *local["incoming"]):
            key = (row["case_id"], row["address"])
            union_map.setdefault(key, row)
        union = list(union_map.values())
        by_case.append(
            {
                "case_id": case_id,
                "outgoing": _counts(local["outgoing"], prior),
                "incoming": _counts(local["incoming"], prior),
                "outgoing_incoming_overlap": len(local["outgoing"])
                + len(local["incoming"])
                - len(union),
                "structural_union": _counts(union, prior),
                "no_positive_canonical": _counts(
                    [
                        row
                        for row in union
                        if row["canonical_category"] == "no-positive-rank"
                    ],
                    prior,
                ),
                "absent_all_saved_positive_lexical": _counts(
                    [row for row in union if row["absent_all_saved_positive_lexical"]],
                    prior,
                ),
                "outgoing_lexical_control": _counts(local_controls["outgoing"], prior),
                "incoming_lexical_control": _counts(local_controls["incoming"], prior),
            }
        )
    union_map = {(row["case_id"], row["address"]): row for row in all_rows}
    union = list(union_map.values())
    control_union = list(
        {(row["case_id"], row["address"]): row for row in controls}.values()
    )
    by_direction = {
        direction: {
            "candidates": _counts(
                [row for row in all_rows if row["direction"] == direction], prior
            ),
            "no_positive_canonical": _counts(
                [
                    row
                    for row in all_rows
                    if row["direction"] == direction
                    and row["canonical_category"] == "no-positive-rank"
                ],
                prior,
            ),
            "absent_all_saved_positive_lexical": _counts(
                [
                    row
                    for row in all_rows
                    if row["direction"] == direction
                    and row["absent_all_saved_positive_lexical"]
                ],
                prior,
            ),
            "lexical_control": _counts(
                [row for row in controls if row["direction"] == direction], prior
            ),
        }
        for direction in DIRECTIONS
    }
    return {
        "by_case": by_case,
        "by_direction": by_direction,
        "structural_union": _counts(union, prior),
        "outgoing_incoming_overlap": len(all_rows) - len(union),
        "no_positive_canonical": _counts(
            [row for row in union if row["canonical_category"] == "no-positive-rank"],
            prior,
        ),
        "absent_all_saved_positive_lexical": _counts(
            [row for row in union if row["absent_all_saved_positive_lexical"]], prior
        ),
        "same_volume_control_union": _counts(control_union, prior),
        "previously_unjudged_reused_count": sum(
            prior[(row["case_id"], row["address"])]["state"] == "UNJUDGED"
            for row in union
            if (row["case_id"], row["address"]) in prior
        ),
        "new_pair_identities": [
            {"case_id": row["case_id"], "address": row["address"]}
            for row in union
            if (row["case_id"], row["address"]) not in prior
        ],
    }


def write_cost(root: Path) -> dict[str, Any]:
    """Run only after the complete candidate artifact is on disk and frozen."""
    freeze = build_freeze(root)
    mechanics_path = root / MECHANICS_NAME
    mechanics = read_candidate_artifact(mechanics_path)
    if (
        mechanics.get("freeze_identity") != freeze["content_identity"]
        or mechanics.get("content_identity")
        != _digest(
            {
                key: value
                for key, value in mechanics.items()
                if key != "content_identity"
            }
        )
        or mechanics.get("judgment_artifacts_loaded") is not False
        or mechanics.get("heldout_executed") is not False
    ):
        raise ValueError("Candidate mechanics are not frozen and outcome-blind.")
    source = _read_json(root.parent / "increment_25" / "task_population_freeze.json")
    task_rows = cast("dict[str, Any]", source["payload"])["task_cards"]
    allowed = cast(
        "list[str]", cast("dict[str, Any]", freeze["payload"])["development_case_ids"]
    )
    raw_cards = {str(row["case_id"]): _task_card(row) for row in task_rows}
    cards = {case_id: raw_cards[case_id] for case_id in allowed}
    prior = load_prior_states(root, cards)
    counts = build_cost(mechanics=mechanics, prior=prior, cards=cards)
    payload: dict[str, Any] = {
        "candidate_identity": mechanics["content_identity"],
        "candidate_sha256": RAW_CANDIDATE_SHA256,
        "frozen_judgment_source_sha256": {
            name: sha256_file(root / name)
            for name in (
                "lexical_top5_frozen_judgments.json",
                "window_unit_frozen_judgments.json",
            )
        }
        | {
            name: sha256_file(root.parent / name)
            for name in (
                "increment_25/confirmation_frozen_judgments.json",
                "increment_26/development_frozen_judgments.json",
            )
        },
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "counts": counts,
        "labels_by_origin_analyzed": False,
        "new_judgments_assigned": False,
        "blinded_input_frozen": False,
        "heldout_executed": False,
    }
    artifact: dict[str, Any] = {
        "schema": "devtools-i27-structural-import-judgment-cost-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }
    path = root / COST_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing structural cost artifact differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
