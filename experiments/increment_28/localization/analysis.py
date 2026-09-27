# Copyright (c) 2026
# ruff: noqa: E501, EM101, PLR2004, TRY003
"""Mechanical outcome join for the frozen import-use location control."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.analysis import _verify_and_join
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_28.localization.evidence import (
    EVIDENCE_NAME,
    FREEZE_NAME,
    ROOT28,
    STATES,
    build_freeze,
)

if TYPE_CHECKING:
    from pathlib import Path

RESULT_NAME = "localization_development_results.json"
PRE_OUTCOME_COMMIT = "5b37d70dcec15d38bf31b7aee6441530d6fab2e9"
PRE_OUTCOME_EVIDENCE_IDENTITY = "f1b9cbd1fd803b6ca28f5d8bd6b723dfbe12911e0fa2c6ca95c9747cea8b1017"
JUDGMENT_STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")
INSIDE_STATES = ("IN_WINDOW_ONLY", "BOTH")


def _surface(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["judgment"] for row in rows)
    judged = counts["USEFUL"] + counts["NOT_USEFUL"]
    return {
        "pairs": len(rows),
        **{state: counts[state] for state in JUDGMENT_STATES},
        "judged": judged,
        "useful_fraction_among_binary_judgments": round(counts["USEFUL"] / judged, 6) if judged else None,
        "cases": len({row["case_id"] for row in rows}),
    }


def _groups(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "inside": _surface([row for row in rows if row["localization_state"] in INSIDE_STATES]),
        "outside_only": _surface([row for row in rows if row["localization_state"] == "OUTSIDE_WINDOW_ONLY"]),
        "no_qualifying_occurrence": _surface([row for row in rows if row["localization_state"] == "NO_QUALIFYING_OCCURRENCE"]),
        "indeterminate": _surface([row for row in rows if row["localization_state"] == "INDETERMINATE"]),
    }


def build_results(root: Path = ROOT28) -> dict[str, Any]:
    """Join only validated frozen development labels after the clean checkpoint."""
    freeze = cast("dict[str, Any]", _read_json(root / FREEZE_NAME))
    evidence = cast("dict[str, Any]", _read_json(root / EVIDENCE_NAME))
    if (
        freeze != build_freeze(root)
        or evidence["content_identity"] != PRE_OUTCOME_EVIDENCE_IDENTITY
        or evidence["content_identity"] != _digest({key: value for key, value in evidence.items() if key != "content_identity"})
        or evidence["freeze_identity"] != freeze["content_identity"]
        or evidence["import_use_evidence_identity"] != freeze["payload"]["import_use_evidence_identity"]
        or evidence["candidate_identity"] != freeze["payload"]["candidate_identity"]
        or evidence["window_identity"] != freeze["payload"]["window_identity"]
        or evidence["usefulness_outcomes_loaded"] is not False
    ):
        raise ValueError("Pre-outcome localization identity differs.")
    joined, sources = _verify_and_join(root.parent / "increment_27")
    labels = {(row["case_id"], row["address"]): row for row in joined if row["outgoing_structural"]}
    if len(labels) != 99:
        raise ValueError("Frozen outgoing judgment population differs.")
    rows: list[dict[str, Any]] = []
    for case in evidence["cases"]:
        for candidate in case["outgoing"]:
            key = (case["case_id"], candidate["address"])
            label = labels.get(key)
            if label is None or label["parent_snapshot_sha"] != case["parent_snapshot_sha"] or label["incoming_structural"] != candidate["incoming"] or label["absent_all_saved_positive_lexical"] != candidate["absent_all_saved_positive_lexical"]:
                raise ValueError("Localization pair differs from exact frozen judgment identity.")
            state = str(label["judgment"])
            if state not in JUDGMENT_STATES:
                raise ValueError("Frozen judgment has invalid state.")
            rows.append({
                "case_id": case["case_id"],
                "address": candidate["address"],
                "judgment": state,
                "localization_state": candidate["state"],
                "any_qualifying_read_anywhere": candidate["any_qualifying_read_anywhere"],
                "any_qualifying_read_inside": candidate["any_qualifying_read_inside"],
                "any_qualifying_read_outside": candidate["any_qualifying_read_outside"],
                "support_count": candidate["support_count"],
                "seed_count": len(candidate["distinct_supporting_seeds"]),
                "best_seed_rank": candidate["best_seed_rank"],
                "absent_all_saved_positive_lexical": candidate["absent_all_saved_positive_lexical"],
                "incoming_overlap": candidate["incoming"],
            })
    if len(rows) != 99 or {(row["case_id"], row["address"]) for row in rows} != set(labels):
        raise ValueError("Localization join changed fixed outgoing candidate pairs.")
    hard = [row for row in rows if row["absent_all_saved_positive_lexical"]]
    single = [row for row in rows if row["support_count"] == 1]
    single_hard = [row for row in hard if row["support_count"] == 1]
    grouped = {state: _surface([row for row in rows if row["localization_state"] == state]) for state in STATES}
    hard_grouped = {state: _surface([row for row in hard if row["localization_state"] == state]) for state in STATES}
    exact: dict[tuple[int, int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        exact[(row["support_count"], row["seed_count"], row["best_seed_rank"])].append(row)
    matched = [
        {
            "support_count": key[0], "seed_count": key[1], "best_seed_rank": key[2],
            "inside": _surface([row for row in values if row["localization_state"] in INSIDE_STATES]),
            "outside_only": _surface([row for row in values if row["localization_state"] == "OUTSIDE_WINDOW_ONLY"]),
            "indeterminate": _surface([row for row in values if row["localization_state"] == "INDETERMINATE"]),
        }
        for key, values in sorted(exact.items())
        if any(row["localization_state"] in INSIDE_STATES for row in values)
        and any(row["localization_state"] == "OUTSIDE_WINDOW_ONLY" for row in values)
    ]
    coarse: dict[str, dict[str, dict[str, Any]]] = {}
    for field in ("support_count", "seed_count", "best_seed_rank"):
        coarse[field] = {
            str(value): _groups([row for row in rows if row[field] == value])
            for value in sorted({int(row[field]) for row in rows})
        }
    per_case = [
        {
            "case_id": case["case_id"],
            "all": _surface([row for row in rows if row["case_id"] == case["case_id"]]),
            "groups": _groups([row for row in rows if row["case_id"] == case["case_id"]]),
            "hard_groups": _groups([row for row in hard if row["case_id"] == case["case_id"]]),
        }
        for case in evidence["cases"]
    ]
    paired_case_ids = {
        case["case_id"]
        for case in per_case
        if case["groups"]["inside"]["pairs"] and case["groups"]["outside_only"]["pairs"]
    }
    paired_rows = [row for row in rows if row["case_id"] in paired_case_ids]
    payload = {
        "schema": "devtools-i28-localization-development-results-v1",
        "pre_outcome_commit": PRE_OUTCOME_COMMIT,
        "source_sha256": {
            FREEZE_NAME: sha256_file(root / FREEZE_NAME),
            EVIDENCE_NAME: sha256_file(root / EVIDENCE_NAME),
            "increment_27/structural_import_judgment_freeze.json": sha256_file(root.parent / "increment_27" / "structural_import_judgment_freeze.json"),
            "increment_27/comparison_frozen_judgments.json": sha256_file(root.parent / "increment_27" / "comparison_frozen_judgments.json"),
        },
        "pre_outcome_freeze_identity": freeze["content_identity"],
        "pre_outcome_evidence_identity": evidence["content_identity"],
        "frozen_judgment_identity": sources["frozen_judgment_identity"],
        "development_case_ids": freeze["payload"]["development_case_ids"],
        "fixed_population": {"cases": 24, "structural_union_pairs": 109, "outgoing_pairs": len(rows), "incoming_only_unclassified": 10},
        "outgoing": _surface(rows),
        "groups": _groups(rows),
        "five_states": grouped,
        "single_support": {"all": _surface(single), "groups": _groups(single)},
        "hard_lexical_escapes": {"all": _surface(hard), "groups": _groups(hard), "five_states": hard_grouped, "single_support": {"all": _surface(single_hard), "groups": _groups(single_hard)}},
        "exact_coarse_matched_strata": matched,
        "coarse_signals": coarse,
        "paired_case_control": {"case_count": len(paired_case_ids), "groups": _groups(paired_rows)},
        "per_case": per_case,
        "pairs": rows,
        "new_candidates": 0, "new_judgments": 0, "judgments_changed": False,
        "heldout_executed": False, "suspended_increment_26_confirmation_executed": False,
    }
    return {"schema": payload["schema"], "content_identity": _digest(payload), "payload": payload}


def write_results(root: Path = ROOT28) -> dict[str, Any]:
    """Persist reproducible descriptive outcome counts separately from evidence."""
    artifact = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing localization result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
