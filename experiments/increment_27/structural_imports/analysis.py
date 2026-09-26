# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PLR0912, PLR0915, PLR2004, TRY003
"""Mechanical development join of frozen usefulness and candidate evidence."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.comparison_judgments import (
    INPUT_IDENTITY,
    INPUT_SHA256,
)
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.phase1_population import _neutral_id
from experiments.increment_27.structural_imports.cost import load_prior_states
from experiments.increment_27.structural_imports.mechanics import (
    MECHANICS_NAME,
    RAW_CANDIDATE_SHA256,
    _digest,
    read_candidate_artifact,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

RESULT_NAME = "structural_import_development_results.json"
FROZEN_JUDGMENT_IDENTITY = (
    "4e7394f0c2cfa8079f5e0b8b06506834046c3035856f6ab8db8c92b21efadea2"
)
FROZEN_JUDGMENT_SHA256 = (
    "08cf1c7e05e1299fbb76eaa956657cb625852765fa446009c3cc06c47a9f6383"
)
FROZEN_POPULATION_IDENTITY = (
    "30396777d0f0e719a5c717a47697f83fa9f0ea7cd6a18c3d650da7d33d64439e"
)
FROZEN_POPULATION_SHA256 = (
    "a28d079344f85ecd0a79dbc50fdca2a336f1f80f4ee72cd9798dc6486b4416ee"
)
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")


def _key(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    need = cast("dict[str, str]", row["information_need"])
    return (
        need["purpose"],
        need["lexical_query"],
        str(row["parent_snapshot_sha"]),
        str(row["address"]),
        str(row["usefulness_semantics"]),
    )


def _surface(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(str(row["judgment"]) for row in rows)
    useful, not_useful, unjudged = (counts[state] for state in STATES)
    judged = useful + not_useful
    return {
        "total_candidates": len(rows),
        "USEFUL": useful,
        "NOT_USEFUL": not_useful,
        "UNJUDGED": unjudged,
        "judged_total": judged,
        "useful_rate_among_judged": round(useful / judged, 6) if judged else None,
    }


def _useful_identities(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "case_id": row["case_id"],
            "information_need": row["information_need"],
            "parent_snapshot_sha": row["parent_snapshot_sha"],
            "address": row["address"],
            "directions": [
                direction
                for direction in ("outgoing", "incoming")
                if row[f"{direction}_structural"]
            ],
            "canonical_positive_rank": row["canonical_positive_rank"],
            "saved_positive_method_ranks": row["saved_positive_method_ranks"],
        }
        for row in rows
        if row["judgment"] == "USEFUL"
    ]


def _verify_and_join(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidate = read_candidate_artifact(root / MECHANICS_NAME)
    frozen = _read_json(root / "structural_import_judgment_freeze.json")
    blind = _read_json(root / "comparison_blinded_judgment_input.json")
    judgment = _read_json(root / "comparison_frozen_judgments.json")
    cost = _read_json(root / "structural_import_judgment_cost.json")
    freeze = cast("dict[str, Any]", frozen["payload"])
    neutral = cast("dict[str, Any]", blind["payload"])
    labels = cast("dict[str, Any]", judgment["payload"])
    cost_payload = cast("dict[str, Any]", cost["payload"])
    if (
        frozen["content_identity"] != FROZEN_POPULATION_IDENTITY
        or sha256_file(root / "structural_import_judgment_freeze.json")
        != FROZEN_POPULATION_SHA256
        or _digest(freeze) != FROZEN_POPULATION_IDENTITY
        or blind["content_identity"] != INPUT_IDENTITY
        or sha256_file(root / "comparison_blinded_judgment_input.json") != INPUT_SHA256
        or _digest(neutral) != INPUT_IDENTITY
        or judgment["content_identity"] != FROZEN_JUDGMENT_IDENTITY
        or sha256_file(root / "comparison_frozen_judgments.json")
        != FROZEN_JUDGMENT_SHA256
        or _digest(labels) != FROZEN_JUDGMENT_IDENTITY
        or freeze["candidate_content_identity"] != candidate["content_identity"]
        or freeze["candidate_raw_sha256"] != RAW_CANDIDATE_SHA256
        or freeze["candidate_compressed_sha256"] != sha256_file(root / MECHANICS_NAME)
        or freeze["candidate_cost_identity"] != cost["content_identity"]
        or freeze["candidate_cost_sha256"]
        != sha256_file(root / "structural_import_judgment_cost.json")
        or cost["content_identity"] != _digest(cost_payload)
        or cost_payload["candidate_identity"] != candidate["content_identity"]
        or cost_payload["candidate_sha256"] != RAW_CANDIDATE_SHA256
        or freeze["candidate_freeze_identity"]
        != _read_json(root / "structural_import_freeze.json")["content_identity"]
        or freeze["blinded_input_identity"] != INPUT_IDENTITY
        or labels["blinded_input_content_identity"] != INPUT_IDENTITY
        or labels["blinded_input_sha256"] != INPUT_SHA256
        or labels["usefulness_semantics"] != USEFULNESS_SEMANTICS
        or freeze["usefulness_semantics"] != USEFULNESS_SEMANTICS
    ):
        raise ValueError("Frozen development source identity differs.")
    source_hashes = cast("dict[str, str]", freeze["frozen_judgment_source_sha256"])
    for name, expected in source_hashes.items():
        path = root.parent / name if name.startswith("increment_") else root / name
        if sha256_file(path) != expected:
            raise ValueError("Prior judgment source hash differs.")
    for name, expected in cast(
        "dict[str, str]", freeze["lexical_control_source_sha256"]
    ).items():
        if sha256_file(root / name) != expected:
            raise ValueError("Saved lexical source hash differs.")
    development = cast("list[str]", freeze["development_case_ids"])
    heldout = set(cast("list[str]", freeze["heldout_case_ids_sealed"]))
    if (
        len(development) != 24
        or len(set(development)) != 24
        or set(development) & heldout
        or [case["case_id"] for case in candidate["cases"]] != development
        or freeze["heldout_executed"] is not False
        or freeze["suspended_increment_26_confirmation_not_executed"] is not True
        or labels["target_count"] != 140
        or labels["state_counts"] != {"USEFUL": 41, "NOT_USEFUL": 68, "UNJUDGED": 31}
    ):
        raise ValueError("Development partition or judgment counts differ.")

    source = _read_json(root.parent / "increment_25" / "task_population_freeze.json")
    cards_all = {
        str(row["case_id"]): _task_card(row)
        for row in cast(
            "list[dict[str, Any]]",
            cast("dict[str, Any]", source["payload"])["task_cards"],
        )
    }
    cards = {case_id: cards_all[case_id] for case_id in development}
    prior = load_prior_states(root, cards)
    reused_rows = cast("list[dict[str, Any]]", freeze["reused_judgments"])
    new_rows = cast("list[dict[str, Any]]", freeze["new_judgment_pairs"])
    evidence_rows = cast("list[dict[str, Any]]", freeze["pair_evidence"])
    if len(reused_rows) != 61 or len(new_rows) != 140 or len(evidence_rows) != 201:
        raise ValueError("Frozen pair partition differs.")
    reused: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for row in reused_rows:
        case_id, address = str(row["case_id"]), str(row["address"])
        previous = prior.get((case_id, address))
        if (
            previous is None
            or previous["state"] != row["judgment"]
            or previous["source"] != row["source"]
            or row["usefulness_semantics"] != USEFULNESS_SEMANTICS
            or row["parent_snapshot_sha"] != cards[case_id].parent_snapshot_sha
            or row["information_need"]
            != {
                "purpose": cards[case_id].information_need_purpose,
                "lexical_query": cards[case_id].lexical_query,
            }
            or _key(row) in reused
        ):
            raise ValueError("Exact prior judgment reuse differs.")
        reused[_key(row)] = row

    new_by_key: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for row in new_rows:
        case_id, address = str(row["case_id"]), str(row["address"])
        if (
            (case_id, address) in prior
            or row["usefulness_semantics"] != USEFULNESS_SEMANTICS
            or row["parent_snapshot_sha"] != cards[case_id].parent_snapshot_sha
            or row["information_need"]
            != {
                "purpose": cards[case_id].information_need_purpose,
                "lexical_query": cards[case_id].lexical_query,
            }
            or _key(row) in new_by_key
            or _key(row) in reused
        ):
            raise ValueError("Frozen new-pair identity differs from exact reuse.")
        new_by_key[_key(row)] = row

    blind_cases = cast("list[dict[str, Any]]", neutral["cases"])
    blind_keys = {
        (
            case["neutral_case_id"],
            resource["neutral_resource_id"],
            case["information_need"]["purpose"],
            case["information_need"]["lexical_query"],
            case["parent_snapshot_sha"],
            resource["address"],
        )
        for case in blind_cases
        for resource in case["resources"]
    }
    if len(blind_keys) != 140 or len(blind_cases) != 23:
        raise ValueError("Neutral target population differs.")
    new_labels: dict[tuple[str, str, str, str, str], str] = {}
    for row in cast("list[dict[str, Any]]", labels["records"]):
        key = _key(row)
        source_row = new_by_key.get(key)
        if source_row is None:
            raise ValueError("Frozen judgment has no exact new target.")
        case_id = str(source_row["case_id"])
        neutral_case = _neutral_id("case", f"{candidate['content_identity']}|{case_id}")
        neutral_resource = _neutral_id(
            "resource", f"{candidate['content_identity']}|{case_id}|{row['address']}"
        )
        blind_key = (
            neutral_case,
            neutral_resource,
            row["information_need"]["purpose"],
            row["information_need"]["lexical_query"],
            row["parent_snapshot_sha"],
            row["address"],
        )
        if (
            row["neutral_case_id"] != neutral_case
            or row["neutral_resource_id"] != neutral_resource
            or blind_key not in blind_keys
            or row["judgment"] not in STATES
            or not str(row["rationale"]).strip()
            or key in new_labels
        ):
            raise ValueError("Frozen judgment differs from its neutral pair.")
        new_labels[key] = str(row["judgment"])
    if set(new_labels) != set(new_by_key):
        raise ValueError("Frozen judgment population is incomplete.")

    joined: list[dict[str, Any]] = []
    for row in evidence_rows:
        key = _key(row)
        if key in reused:
            state = str(reused[key]["judgment"])
            source_name = str(reused[key]["source"])
        elif key in new_labels:
            state = new_labels[key]
            source_name = "frozen-neutral-comparison"
        else:
            raise ValueError("Candidate pair lacks an exact judgment.")
        joined.append({**row, "judgment": state, "judgment_source": source_name})
    if len({_key(row) for row in joined}) != len(joined) or set(
        map(_key, joined)
    ) != set(reused) | set(new_labels):
        raise ValueError("Joined candidate population has duplicate or missing pairs.")
    return joined, {
        "development_case_ids": development,
        "heldout_case_ids_sealed": list(freeze["heldout_case_ids_sealed"]),
        "candidate_content_identity": candidate["content_identity"],
        "candidate_raw_sha256": RAW_CANDIDATE_SHA256,
        "candidate_compressed_sha256": sha256_file(root / MECHANICS_NAME),
        "candidate_freeze_identity": freeze["candidate_freeze_identity"],
        "candidate_cost_identity": cost["content_identity"],
        "candidate_cost_sha256": sha256_file(
            root / "structural_import_judgment_cost.json"
        ),
        "population_freeze_identity": frozen["content_identity"],
        "population_freeze_sha256": FROZEN_POPULATION_SHA256,
        "neutral_input_identity": INPUT_IDENTITY,
        "neutral_input_sha256": INPUT_SHA256,
        "frozen_judgment_identity": FROZEN_JUDGMENT_IDENTITY,
        "frozen_judgment_sha256": FROZEN_JUDGMENT_SHA256,
        "lexical_control_source_sha256": freeze["lexical_control_source_sha256"],
        "prior_judgment_source_sha256": source_hashes,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "new_judgment_count": len(new_labels),
        "exact_reused_count": len(reused),
    }


def build_results(root: Path) -> dict[str, Any]:
    """Report development surfaces without rescoring or changing judgments."""
    joined, sources = _verify_and_join(root)

    def structural(row: dict[str, Any]) -> bool:
        return bool(row["outgoing_structural"] or row["incoming_structural"])

    def control(row: dict[str, Any]) -> bool:
        return bool(row["outgoing_lexical_control"] or row["incoming_lexical_control"])

    selectors: dict[str, Callable[[dict[str, Any]], bool]] = {
        "structural_union": structural,
        "outgoing": lambda row: bool(row["outgoing_structural"]),
        "incoming": lambda row: bool(row["incoming_structural"]),
        "canonical_rank_gt_5": lambda row: bool(
            structural(row)
            and row["canonical_positive_rank"] is not None
            and row["canonical_positive_rank"] > 5
        ),
        "no_positive_canonical_rank": lambda row: bool(
            structural(row) and row["canonical_positive_rank"] is None
        ),
        "absent_all_saved_positive_lexical": lambda row: bool(
            structural(row) and row["absent_all_saved_positive_lexical"]
        ),
        "same_volume_lexical_control_union": control,
        "structural_only": lambda row: bool(structural(row) and not control(row)),
        "lexical_control_only": lambda row: bool(control(row) and not structural(row)),
        "structural_and_control": lambda row: bool(structural(row) and control(row)),
    }
    surfaces = {
        name: [row for row in joined if predicate(row)]
        for name, predicate in selectors.items()
    }
    surface_counts = {name: _surface(rows) for name, rows in surfaces.items()}
    useful_resource_identities = {
        name: _useful_identities(rows) for name, rows in surfaces.items()
    }
    useful_structural = [
        row for row in surfaces["structural_union"] if row["judgment"] == "USEFUL"
    ]
    reach = {
        "canonical_rank_gt_5": [
            row
            for row in useful_structural
            if row["canonical_positive_rank"] is not None
            and row["canonical_positive_rank"] > 5
        ],
        "no_positive_canonical_other_saved_positive": [
            row
            for row in useful_structural
            if row["canonical_positive_rank"] is None
            and not row["absent_all_saved_positive_lexical"]
        ],
        "absent_all_saved_positive_lexical": [
            row for row in useful_structural if row["absent_all_saved_positive_lexical"]
        ],
    }
    if sum(map(len, reach.values())) != len(useful_structural):
        raise ValueError("Useful structural lexical-reach partition is incomplete.")
    per_case: list[dict[str, Any]] = []
    for case_id in sources["development_case_ids"]:
        rows = [row for row in joined if row["case_id"] == case_id]
        s = [row for row in rows if structural(row)]
        c = [row for row in rows if control(row)]
        per_case.append(
            {
                "case_id": case_id,
                "structural_candidates": len(s),
                "useful_structural": sum(row["judgment"] == "USEFUL" for row in s),
                "useful_lexical_control": sum(row["judgment"] == "USEFUL" for row in c),
                "useful_no_positive_canonical": sum(
                    row["judgment"] == "USEFUL"
                    and row["canonical_positive_rank"] is None
                    for row in s
                ),
                "useful_absent_all_saved_positive_lexical": sum(
                    row["judgment"] == "USEFUL"
                    and row["absent_all_saved_positive_lexical"]
                    for row in s
                ),
                "unjudged_structural": sum(row["judgment"] == "UNJUDGED" for row in s),
            }
        )
    contingency = Counter(
        "both"
        if row["useful_structural"] and row["useful_lexical_control"]
        else "structure_only"
        if row["useful_structural"]
        else "lexical_control_only"
        if row["useful_lexical_control"]
        else "neither"
        for row in per_case
    )
    directional = {}
    for direction in ("outgoing", "incoming"):
        rows = surfaces[direction]
        directional[direction] = {
            "useful_no_positive_canonical": sum(
                row["judgment"] == "USEFUL" and row["canonical_positive_rank"] is None
                for row in rows
            ),
            "useful_absent_all_saved_positive_lexical": sum(
                row["judgment"] == "USEFUL" and row["absent_all_saved_positive_lexical"]
                for row in rows
            ),
            "cases_with_useful_addition": len(
                {row["case_id"] for row in rows if row["judgment"] == "USEFUL"}
            ),
        }
    if (
        surface_counts["structural_union"]["total_candidates"] != 109
        or surface_counts["outgoing"]["total_candidates"] != 99
        or surface_counts["incoming"]["total_candidates"] != 23
        or surface_counts["no_positive_canonical_rank"]["total_candidates"] != 66
        or surface_counts["absent_all_saved_positive_lexical"]["total_candidates"] != 54
        or surface_counts["same_volume_lexical_control_union"]["total_candidates"]
        != 101
        or len(per_case) != 24
    ):
        raise ValueError("Joined surface differs from frozen candidate counts.")
    payload: dict[str, Any] = {
        "schema": "devtools-i27-structural-import-development-results-v1",
        "sources": sources,
        "joined_population": joined,
        "surface_counts": surface_counts,
        "useful_resource_identities": useful_resource_identities,
        "lexical_reach_useful_structural": {
            name: {"count": len(rows), "resources": _useful_identities(rows)}
            for name, rows in reach.items()
        },
        "directional": directional,
        "per_case": per_case,
        "control_comparison": {
            "structural_union_candidates": len(surfaces["structural_union"]),
            "control_union_candidates": len(
                surfaces["same_volume_lexical_control_union"]
            ),
            "cases_with_useful_structural_addition": sum(
                row["useful_structural"] > 0 for row in per_case
            ),
            "cases_with_useful_lexical_control_addition": sum(
                row["useful_lexical_control"] > 0 for row in per_case
            ),
            "case_contingency": {
                name: contingency[name]
                for name in (
                    "structure_only",
                    "lexical_control_only",
                    "both",
                    "neither",
                )
            },
        },
        "unjudged": {
            "new_blinded_targets": 31,
            "structural_union": surface_counts["structural_union"]["UNJUDGED"],
            "outgoing": surface_counts["outgoing"]["UNJUDGED"],
            "incoming": surface_counts["incoming"]["UNJUDGED"],
            "lexical_control_union": surface_counts[
                "same_volume_lexical_control_union"
            ]["UNJUDGED"],
            "absent_all_saved_positive_lexical": surface_counts[
                "absent_all_saved_positive_lexical"
            ]["UNJUDGED"],
        },
        "heldout_executed": False,
        "suspended_increment_26_confirmation_executed": False,
        "judgments_changed": False,
    }
    return {
        "schema": payload["schema"],
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_results(root: Path) -> dict[str, Any]:
    """Persist one deterministic analysis of already-frozen development evidence."""
    artifact = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing structural development result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
