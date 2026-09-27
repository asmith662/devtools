# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PLR0912, PLR2004, TRY003
"""Exact judgment reuse and neutral input after containment mechanics freeze."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.phase1_population import _neutral_id, _resource_contents
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_29.analysis import build_results as build_i29_results
from experiments.increment_29.population import _prior_states
from experiments.increment_30.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    _verified_json,
    build_freeze,
)

JUDGMENT_FREEZE_NAME = "package_containment_judgment_freeze.json"
BLINDED_NAME = "package_containment_blinded_judgment_input.json"
RESULT_NAME = "package_containment_development_results.json"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")


def build_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Join labels only after checking the persisted outcome-blind candidate freeze."""
    protocol = _verified_json(root / FREEZE_NAME)
    mechanics = _verified_json(root / CANDIDATES_NAME)
    if (
        protocol != build_freeze(root)
        or mechanics["freeze_identity"] != protocol["content_identity"]
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
    ):
        raise ValueError("Containment mechanics were not frozen outcome-blind.")
    allowed = list(protocol["payload"]["development_case_ids"])
    task_population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in task_population["payload"]["task_cards"]
        if row["case_id"] in allowed
    }
    if len(cards) != 24 or [case["case_id"] for case in mechanics["cases"]] != allowed:
        raise ValueError(
            "Containment judgment population differs from frozen development."
        )

    # The Increment-29 result builder validates its own frozen blind/judgment join.
    prior = _prior_states(root.parent / "increment_29", cards)
    i29_results = build_i29_results(root.parent / "increment_29")
    if (
        _verified_json(
            root.parent / "increment_29" / "references_calls_development_results.json"
        )
        != i29_results
    ):
        raise ValueError("Persisted Increment-29 result differs from validated join.")
    for row in i29_results["payload"]["joined_pairs"]:
        key = (str(row["case_id"]), str(row["address"]))
        state = str(row["judgment"])
        previous = prior.get(key)
        if state not in STATES or (previous is not None and previous["state"] != state):
            raise ValueError("Existing exact judgments conflict.")
        prior.setdefault(key, {"state": state, "source": "increment-29-frozen"})

    reused: list[dict[str, Any]] = []
    new: list[dict[str, Any]] = []
    for case in mechanics["cases"]:
        case_id = str(case["case_id"])
        card = cards[case_id]
        if case["parent_snapshot_sha"] != card.parent_snapshot_sha or case[
            "information_need"
        ] != {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        }:
            raise ValueError("Containment candidate identity differs from task card.")
        for candidate in case["candidates"]:
            identity = {
                "case_id": case_id,
                "information_need": case["information_need"],
                "parent_snapshot_sha": card.parent_snapshot_sha,
                "address": candidate["address"],
                "usefulness_semantics": USEFULNESS_SEMANTICS,
            }
            previous = prior.get((case_id, str(candidate["address"])))
            if previous is None:
                new.append(
                    {
                        **identity,
                        "neutral_case_id": _neutral_id(
                            "case", f"{mechanics['content_identity']}|{case_id}"
                        ),
                        "neutral_resource_id": _neutral_id(
                            "resource",
                            f"{mechanics['content_identity']}|{case_id}|{candidate['address']}",
                        ),
                    }
                )
            else:
                reused.append(
                    {
                        **identity,
                        "judgment": previous["state"],
                        "source": previous["source"],
                    }
                )
    if len(new) + len(reused) != mechanics["summary"]["candidate_pairs"] or len(
        {(row["case_id"], row["address"]) for row in [*new, *reused]}
    ) != len(new) + len(reused):
        raise ValueError("Containment population is incomplete or duplicated.")
    contents = _resource_contents(
        list(dict.fromkeys((row["parent_snapshot_sha"], row["address"]) for row in new))
    )
    blind_cases: list[dict[str, Any]] = []
    for case_id in allowed:
        card = cards[case_id]
        resources: list[dict[str, str]] = [
            {
                "neutral_resource_id": row["neutral_resource_id"],
                "address": row["address"],
                "content": contents[(card.parent_snapshot_sha, row["address"])],
            }
            for row in new
            if row["case_id"] == case_id
        ]
        if resources:
            blind_cases.append(
                {
                    "neutral_case_id": _neutral_id(
                        "case", f"{mechanics['content_identity']}|{case_id}"
                    ),
                    "information_need": {
                        "purpose": card.information_need_purpose,
                        "lexical_query": card.lexical_query,
                    },
                    "parent_snapshot_sha": card.parent_snapshot_sha,
                    "resources": sorted(
                        resources, key=lambda item: item["neutral_resource_id"]
                    ),
                }
            )
    blind_payload = {
        "schema": "devtools-neutral-resource-judgment-input-v1",
        "cases": sorted(blind_cases, key=lambda row: str(row["neutral_case_id"])),
    }
    blind = {
        "schema": blind_payload["schema"],
        "content_identity": _digest(blind_payload),
        "payload": blind_payload,
    }
    reused_counts = Counter(row["judgment"] for row in reused)
    payload = {
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": protocol["payload"]["heldout_case_ids_sealed"],
        "candidate_freeze_identity": protocol["content_identity"],
        "candidate_identity": mechanics["content_identity"],
        "candidate_sha256": sha256_file(root / CANDIDATES_NAME),
        "prior_judgment_source_sha256": {
            "increment_29/references_calls_development_results.json": sha256_file(
                root.parent
                / "increment_29"
                / "references_calls_development_results.json"
            ),
            "increment_29/references_calls_frozen_judgments.json": sha256_file(
                root.parent / "increment_29" / "references_calls_frozen_judgments.json"
            ),
            "increment_27/comparison_frozen_judgments.json": sha256_file(
                root.parent / "increment_27" / "comparison_frozen_judgments.json"
            ),
        },
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "three_states": list(STATES),
        "pair_identity_rule": [
            "InformationNeed purpose",
            "frozen query",
            "parent snapshot",
            "resource address",
            "usefulness semantics",
        ],
        "reused_judgments": reused,
        "new_judgment_pairs": new,
        "counts": {
            "candidate_pairs": len(new) + len(reused),
            "exact_reused": len(reused),
            "new_judgments_required": len(new),
            "reused_states": {state: reused_counts[state] for state in STATES},
            "new_by_case": dict(sorted(Counter(row["case_id"] for row in new).items())),
        },
        "blinded_input_identity": blind["content_identity"],
        "new_usefulness_outcomes": False,
        "confirmation_executed": False,
    }
    frozen = {
        "schema": "devtools-i30-package-containment-judgment-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }
    return frozen, blind


def write_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist hidden reuse mapping separately from neutral human input."""
    frozen, blind = build_population(root)
    for name, artifact in ((JUDGMENT_FREEZE_NAME, frozen), (BLINDED_NAME, blind)):
        path = root / name
        if path.exists() and _read_json(path) != artifact:
            raise ValueError("Existing containment judgment population differs.")
        write_artifact(path=path, payload=artifact)
    return frozen, blind


def build_results(root: Path = ROOT) -> dict[str, Any]:
    """Report the completed baseline only when every exact pair is judged."""
    protocol = _verified_json(root / FREEZE_NAME)
    mechanics = _verified_json(root / CANDIDATES_NAME)
    population = _verified_json(root / JUDGMENT_FREEZE_NAME)["payload"]
    if population["new_judgment_pairs"]:
        raise ValueError("New judgments are required; stop before an outcome join.")
    if (
        population["candidate_freeze_identity"] != protocol["content_identity"]
        or population["candidate_identity"] != mechanics["content_identity"]
        or population["candidate_sha256"] != sha256_file(root / CANDIDATES_NAME)
    ):
        raise ValueError("Completed result source identities differ.")
    reused = {
        (row["case_id"], row["address"]): row for row in population["reused_judgments"]
    }
    joined = []
    for case in mechanics["cases"]:
        for candidate in case["candidates"]:
            prior = reused[(case["case_id"], candidate["address"])]
            joined.append(
                {
                    "case_id": case["case_id"],
                    "parent_snapshot_sha": case["parent_snapshot_sha"],
                    "address": candidate["address"],
                    "judgment": prior["judgment"],
                    "judgment_source": prior["source"],
                    "directions": candidate["directions"],
                    "absent_all_saved_positive_lexical": candidate[
                        "absent_all_saved_positive_lexical"
                    ],
                    "existing_import_candidate": candidate["existing_import_candidate"],
                    "existing_references_calls_candidate": candidate[
                        "existing_references_calls_candidate"
                    ],
                    "absent_existing_evidence_union": candidate[
                        "absent_existing_evidence_union"
                    ],
                }
            )
    counts = Counter(row["judgment"] for row in joined)
    if len(joined) != mechanics["summary"]["candidate_pairs"] or len(joined) != len(
        reused
    ):
        raise ValueError("Completed result coverage differs from candidate surface.")
    payload = {
        "development_case_ids": protocol["payload"]["development_case_ids"],
        "source_content_identities": {
            FREEZE_NAME: protocol["content_identity"],
            CANDIDATES_NAME: mechanics["content_identity"],
            JUDGMENT_FREEZE_NAME: _verified_json(root / JUDGMENT_FREEZE_NAME)[
                "content_identity"
            ],
        },
        "joined_pairs": joined,
        "outcome_counts": {state: counts[state] for state in STATES},
        "useful_escape_pairs": [
            {"case_id": row["case_id"], "address": row["address"]}
            for row in joined
            if row["judgment"] == "USEFUL" and row["absent_existing_evidence_union"]
        ],
        "candidate_summary": mechanics["summary"],
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i30-package-containment-development-results-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_results(root: Path = ROOT) -> dict[str, Any]:
    """Persist the result only at Stop State B."""
    result = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != result:
        raise ValueError("Existing containment result differs.")
    write_artifact(path=path, payload=result)
    return result
