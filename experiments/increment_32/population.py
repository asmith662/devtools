# Copyright (c) 2026
# ruff: noqa: COM812, EM101, PLR2004, TRY003
"""Exact development judgment reuse after Graph-1 candidate freeze."""

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
from experiments.increment_29.population import _prior_states
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    build_freeze,
)
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_neutral_target_coverage,
    validated_outcome_mappings,
)

JUDGMENT_FREEZE_NAME = "graph_round_one_judgment_freeze.json"
BLINDED_NAME = "graph_round_one_blinded_judgment_input.json"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")
RESULT_FILES = (
    ("increment_29", "references_calls_development_results.json"),
    ("increment_30", "package_containment_development_results.json"),
    ("increment_31", "mirrored_test_paths_development_results.json"),
)


def _prior(
    root: Path, cards: dict[str, Any]
) -> tuple[dict[tuple[str, str], dict[str, str]], dict[str, str]]:
    prior = _prior_states(root.parent / "increment_29", cards)
    shas: dict[str, str] = {}
    for directory, name in RESULT_FILES:
        path = root.parent / directory / name
        result = _verified_json(path)
        shas[f"{directory}/{name}"] = sha256_file(path)
        if result["payload"]["confirmation_executed"]:
            raise ValueError("Development prior source claims confirmation execution.")
        for row in result["payload"]["joined_pairs"]:
            case_id, address = str(row["case_id"]), str(row["address"])
            card = cards.get(case_id)
            state = str(row["judgment"])
            if (
                card is None
                or state not in STATES
                or row["parent_snapshot_sha"] != card.parent_snapshot_sha
                or row["information_need"]
                != {
                    "purpose": card.information_need_purpose,
                    "lexical_query": card.lexical_query,
                }
                or row["usefulness_semantics"] != USEFULNESS_SEMANTICS
            ):
                raise ValueError("Prior judgment identity differs from development.")
            key = (case_id, address)
            previous = prior.get(key)
            if previous is not None and previous["state"] != state:
                raise ValueError("Exact development judgments conflict.")
            prior.setdefault(key, {"state": state, "source": f"{directory}-frozen"})
    return prior, shas


def build_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Join only exact prior pairs; keep unresolved targets origin-blind."""
    protocol = _verified_json(root / FREEZE_NAME)
    mechanics = _verified_json(root / CANDIDATES_NAME)
    if (
        protocol != build_freeze(root)
        or mechanics["freeze_identity"] != protocol["content_identity"]
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
        or [case["case_id"] for case in mechanics["cases"]]
        != protocol["payload"]["development_case_ids"]
    ):
        raise ValueError("Graph-1 mechanics were not frozen outcome-blind.")
    population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    allowed = list(protocol["payload"]["development_case_ids"])
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in population["payload"]["task_cards"]
        if row["case_id"] in allowed
    }
    if len(cards) != 24:
        raise ValueError("Graph-1 development cards differ.")
    prior, prior_shas = _prior(root, cards)
    reused: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for case in mechanics["cases"]:
        case_id = str(case["case_id"])
        card = cards[case_id]
        if case["parent_snapshot_sha"] != card.parent_snapshot_sha or case[
            "information_need"
        ] != {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        }:
            raise ValueError("Graph-1 candidate case identity differs.")
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
                unresolved.append(
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
    if len(reused) + len(unresolved) != mechanics["summary"]["candidate_pairs"] or len(
        {judgment_identity(row) for row in [*reused, *unresolved]}
    ) != len(reused) + len(unresolved):
        raise ValueError(
            "Graph-1 candidate judgment identity is incomplete or duplicated."
        )
    validated_outcome_mappings(reused, {})
    validate_neutral_target_coverage(unresolved)
    contents = _resource_contents(
        list(
            dict.fromkeys(
                (row["parent_snapshot_sha"], row["address"]) for row in unresolved
            )
        )
    )
    blind_cases: list[dict[str, Any]] = []
    for case_id in allowed:
        card = cards[case_id]
        resources = sorted(
            (
                {
                    "neutral_resource_id": row["neutral_resource_id"],
                    "address": row["address"],
                    "content": contents[(card.parent_snapshot_sha, row["address"])],
                }
                for row in unresolved
                if row["case_id"] == case_id
            ),
            key=lambda row: str(row["neutral_resource_id"]),
        )
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
                    "resources": resources,
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
    counts = Counter(row["judgment"] for row in reused)
    payload = {
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": protocol["payload"]["heldout_case_ids_sealed"],
        "candidate_freeze_identity": protocol["content_identity"],
        "candidate_identity": mechanics["content_identity"],
        "candidate_sha256": sha256_file(root / CANDIDATES_NAME),
        "prior_development_results_sha256": prior_shas,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "three_states": list(STATES),
        "pair_identity_rule": protocol["payload"]["candidate_identity"],
        "reused_judgments": reused,
        "new_judgment_pairs": unresolved,
        "counts": {
            "candidate_pairs": len(reused) + len(unresolved),
            "exact_reused": len(reused),
            "new_judgments_required": len(unresolved),
            "affected_cases": len({row["case_id"] for row in unresolved}),
            "reused_states": {state: counts[state] for state in STATES},
            "new_by_case": dict(
                sorted(Counter(row["case_id"] for row in unresolved).items())
            ),
        },
        "blinded_input_identity": blind["content_identity"],
        "new_usefulness_outcomes": False,
        "confirmation_executed": False,
    }
    frozen = {
        "schema": "devtools-i32-graph-round-one-judgment-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }
    return frozen, blind


def write_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist hidden exact reuse and a separate neutral unresolved input."""
    frozen, blind = build_population(root)
    for name, artifact in ((JUDGMENT_FREEZE_NAME, frozen), (BLINDED_NAME, blind)):
        path = root / name
        if path.exists() and _read_json(path) != artifact:
            raise ValueError("Existing Graph-1 judgment population differs.")
        write_artifact(path=path, payload=artifact)
    return frozen, blind


if __name__ == "__main__":
    write_population()
