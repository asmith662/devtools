# Copyright (c) 2026
# ruff: noqa: C901, E501, EM101, PLR2004, TRY003
"""Mechanical post-checkpoint join to already frozen development judgments."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.analysis import _verify_and_join
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_28.import_use import (
    EVIDENCE_NAME,
    FREEZE_NAME,
    ROOT27,
    build_freeze,
)

if TYPE_CHECKING:
    from pathlib import Path

RESULT_NAME = "import_use_development_results.json"
PRE_OUTCOME_COMMIT = "8809c478d0d0509e4eb921740eed2d4f78a2216e"
PRE_OUTCOME_EVIDENCE_IDENTITY = "e65f8073fd894c14a889aa1d7428360e18b1655d13decdeb6ef8847808dc3451"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")
CATEGORIES = ("SUPPORTED", "NO_QUALIFYING_OCCURRENCE", "INDETERMINATE")


def _surface(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["judgment"] for row in rows)
    judged = counts["USEFUL"] + counts["NOT_USEFUL"]
    return {
        "pairs": len(rows),
        **{state: counts[state] for state in STATES},
        "judged": judged,
        "useful_fraction_among_binary_judgments": round(counts["USEFUL"] / judged, 6) if judged else None,
        "cases": len({row["case_id"] for row in rows}),
    }


def _category(row: dict[str, Any]) -> str:
    counts = row["state_counts"]
    if counts["SUPPORTED"]:
        return "SUPPORTED"
    if counts["INDETERMINATE"]:
        return "INDETERMINATE"
    return "NO_QUALIFYING_OCCURRENCE"


def build_results(root: Path = ROOT27) -> dict[str, Any]:
    """Join exact frozen labels only after the independent evidence checkpoint."""
    root28 = root.parent / "increment_28"
    frozen = cast("dict[str, Any]", _read_json(root28 / FREEZE_NAME))
    evidence = cast("dict[str, Any]", _read_json(root28 / EVIDENCE_NAME))
    if (
        frozen != build_freeze(root)
        or evidence["content_identity"] != PRE_OUTCOME_EVIDENCE_IDENTITY
        or evidence["content_identity"] != _digest({key: value for key, value in evidence.items() if key != "content_identity"})
        or evidence["freeze_identity"] != frozen["content_identity"]
        or evidence["candidate_identity"] != frozen["payload"]["candidate_identity"]
        or evidence["window_identity"] != frozen["payload"]["window_identity"]
        or evidence["usefulness_outcomes_loaded"] is not False
    ):
        raise ValueError("Pre-outcome evidence identity differs.")
    joined, sources = _verify_and_join(root)
    labels = {(row["case_id"], row["address"]): row for row in joined if row["outgoing_structural"]}
    if len(labels) != 99:
        raise ValueError("Frozen outgoing judgment population differs.")
    rows: list[dict[str, Any]] = []
    for case in evidence["cases"]:
        for candidate in case["outgoing"]:
            key = (case["case_id"], candidate["address"])
            label = labels.get(key)
            if label is None or label["parent_snapshot_sha"] != case["parent_snapshot_sha"] or label["information_need"] != next(row["information_need"] for row in joined if row["case_id"] == case["case_id"]):
                raise ValueError("Import-use pair lacks exact frozen InformationNeed judgment.")
            if label["absent_all_saved_positive_lexical"] != candidate["absent_all_saved_positive_lexical"] or label["incoming_structural"] != candidate["incoming"]:
                raise ValueError("Candidate reach or direction differs from frozen judgment population.")
            state = str(label["judgment"])
            if state not in STATES:
                raise ValueError("Frozen judgment has invalid state.")
            rows.append({
                "case_id": case["case_id"], "address": candidate["address"],
                "judgment": state, "category": _category(candidate),
                "any_supported": candidate["any_supported"],
                "any_indeterminate": candidate["state_counts"]["INDETERMINATE"] > 0,
                "supported_support_count": candidate["state_counts"]["SUPPORTED"],
                "indeterminate_support_count": candidate["state_counts"]["INDETERMINATE"],
                "support_count": candidate["existing_support_count"],
                "seed_count": len(candidate["distinct_supporting_seeds"]),
                "best_seed_rank": candidate["existing_best_seed_rank"],
                "absent_all_saved_positive_lexical": candidate["absent_all_saved_positive_lexical"],
                "incoming_overlap": candidate["incoming"],
            })
    if len(rows) != 99 or {(row["case_id"], row["address"]) for row in rows} != set(labels):
        raise ValueError("Analysis changed the fixed outgoing candidate set.")
    groups = {category: _surface([row for row in rows if row["category"] == category]) for category in CATEGORIES}
    hard = [row for row in rows if row["absent_all_saved_positive_lexical"]]
    hard_groups = {category: _surface([row for row in hard if row["category"] == category]) for category in CATEGORIES}
    per_case = [
        {
            "case_id": case["case_id"],
            "all_outgoing": _surface([row for row in rows if row["case_id"] == case["case_id"]]),
            "supported": _surface([row for row in rows if row["case_id"] == case["case_id"] and row["category"] == "SUPPORTED"]),
            "without_supported": _surface([row for row in rows if row["case_id"] == case["case_id"] and row["category"] != "SUPPORTED"]),
            "hard_supported": _surface([row for row in hard if row["case_id"] == case["case_id"] and row["category"] == "SUPPORTED"]),
        }
        for case in evidence["cases"]
    ]
    coarse: dict[str, dict[str, dict[str, Any]]] = {}
    for field in ("support_count", "seed_count", "best_seed_rank"):
        coarse[field] = {}
        for value in sorted({int(row[field]) for row in rows}):
            stratum = [row for row in rows if row[field] == value]
            coarse[field][str(value)] = {
                "all": _surface(stratum),
                "supported": _surface([row for row in stratum if row["category"] == "SUPPORTED"]),
                "without_supported": _surface([row for row in stratum if row["category"] != "SUPPORTED"]),
            }
    matched: dict[tuple[int, int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        matched[(row["support_count"], row["seed_count"], row["best_seed_rank"])].append(row)
    matched_strata = [
        {
            "support_count": key[0], "seed_count": key[1], "best_seed_rank": key[2],
            "supported": _surface([row for row in values if row["category"] == "SUPPORTED"]),
            "without_supported": _surface([row for row in values if row["category"] != "SUPPORTED"]),
        }
        for key, values in sorted(matched.items())
        if any(row["category"] == "SUPPORTED" for row in values) and any(row["category"] != "SUPPORTED" for row in values)
    ]
    leave_one_case_out = []
    for case in evidence["cases"]:
        remaining = [row for row in rows if row["case_id"] != case["case_id"]]
        leave_one_case_out.append({
            "omitted_case_id": case["case_id"],
            "supported": _surface([row for row in remaining if row["category"] == "SUPPORTED"]),
            "without_supported": _surface([row for row in remaining if row["category"] != "SUPPORTED"]),
        })
    payload = {
        "schema": "devtools-i28-import-use-development-results-v1",
        "pre_outcome_commit": PRE_OUTCOME_COMMIT,
        "source_sha256": {
            FREEZE_NAME: sha256_file(root28 / FREEZE_NAME),
            EVIDENCE_NAME: sha256_file(root28 / EVIDENCE_NAME),
            "structural_import_judgment_freeze.json": sha256_file(root / "structural_import_judgment_freeze.json"),
            "comparison_frozen_judgments.json": sha256_file(root / "comparison_frozen_judgments.json"),
        },
        "pre_outcome_freeze_identity": frozen["content_identity"],
        "pre_outcome_evidence_identity": evidence["content_identity"],
        "frozen_judgment_identity": sources["frozen_judgment_identity"],
        "development_case_ids": frozen["payload"]["development_case_ids"],
        "candidate_population": {"union": evidence["summary"]["fixed_union_pairs"], "outgoing": len(rows), "incoming_only_unclassified": evidence["summary"]["incoming_only_pairs"]},
        "outgoing": _surface(rows), "categories": groups,
        "any_indeterminate": _surface([row for row in rows if row["any_indeterminate"]]),
        "hard_lexical_escapes": {"all": _surface(hard), "categories": hard_groups},
        "per_case": per_case, "coarse_signals": coarse, "exact_coarse_matched_strata": matched_strata,
        "leave_one_case_out": leave_one_case_out,
        "pairs": rows, "new_judgments": 0, "judgments_changed": False,
        "heldout_executed": False, "suspended_increment_26_confirmation_executed": False,
    }
    return {"schema": payload["schema"], "content_identity": _digest(payload), "payload": payload}


def write_results(root: Path = ROOT27) -> dict[str, Any]:
    """Persist deterministic descriptive development results after checkpoint."""
    artifact = build_results(root)
    path = root.parent / "increment_28" / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Increment 28 development results differ.")
    write_artifact(path=path, payload=artifact)
    return artifact
