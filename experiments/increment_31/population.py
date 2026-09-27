# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, EM102, PLR0912, PLR2004, TRY003
"""Exact development judgment reuse after mirrored-test candidate freeze."""

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
from experiments.increment_30.analysis import build_results as build_i30_results
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_31.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    build_freeze,
)

JUDGMENT_FREEZE_NAME = "mirrored_test_paths_judgment_freeze.json"
BLINDED_NAME = "mirrored_test_paths_blinded_judgment_input.json"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")


def build_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Reuse only exact frozen development labels; keep new targets blind."""
    protocol = _verified_json(root / FREEZE_NAME)
    mechanics = _verified_json(root / CANDIDATES_NAME)
    if (
        protocol != build_freeze(root)
        or mechanics["freeze_identity"] != protocol["content_identity"]
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
    ):
        raise ValueError(
            "Mirrored-test candidate mechanics were not frozen outcome-blind."
        )
    allowed = list(protocol["payload"]["development_case_ids"])
    source = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in source["payload"]["task_cards"]
        if row["case_id"] in allowed
    }
    if len(cards) != 24 or [case["case_id"] for case in mechanics["cases"]] != allowed:
        raise ValueError("Candidate population differs from frozen development cases.")

    prior = _prior_states(root.parent / "increment_29", cards)
    for increment, builder, name in (
        (
            "increment-29",
            build_i29_results,
            "references_calls_development_results.json",
        ),
        (
            "increment-30",
            build_i30_results,
            "package_containment_development_results.json",
        ),
    ):
        directory = root.parent / increment.replace("-", "_")
        results = builder(directory)
        if _verified_json(directory / name) != results:
            raise ValueError(
                f"{increment} persisted result differs from exact frozen join."
            )
        for row in results["payload"]["joined_pairs"]:
            key = (str(row["case_id"]), str(row["address"]))
            state = str(row["judgment"])
            previous = prior.get(key)
            if state not in STATES or (
                previous is not None and previous["state"] != state
            ):
                raise ValueError("Conflicting exact previous judgment.")
            prior.setdefault(key, {"state": state, "source": f"{increment}-frozen"})

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
            raise ValueError("Candidate InformationNeed or snapshot identity differs.")
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
        raise ValueError("Candidate/judgment population is incomplete or duplicated.")

    contents = _resource_contents(
        list(dict.fromkeys((row["parent_snapshot_sha"], row["address"]) for row in new))
    )
    blind_cases = []
    for case_id in allowed:
        card = cards[case_id]
        resources = sorted(
            (
                {
                    "neutral_resource_id": row["neutral_resource_id"],
                    "address": row["address"],
                    "content": contents[(card.parent_snapshot_sha, row["address"])],
                }
                for row in new
                if row["case_id"] == case_id
            ),
            key=lambda row: row["neutral_resource_id"],
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
    reused_counts = Counter(row["judgment"] for row in reused)
    payload = {
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": protocol["payload"]["heldout_case_ids_sealed"],
        "candidate_freeze_identity": protocol["content_identity"],
        "candidate_identity": mechanics["content_identity"],
        "candidate_sha256": sha256_file(root / CANDIDATES_NAME),
        "prior_judgment_source_sha256": {
            f"{directory}/{name}": sha256_file(root.parent / directory / name)
            for directory, name in (
                ("increment_25", "confirmation_frozen_judgments.json"),
                ("increment_26", "development_frozen_judgments.json"),
                ("increment_27", "lexical_top5_frozen_judgments.json"),
                ("increment_27", "window_unit_frozen_judgments.json"),
                ("increment_27", "comparison_frozen_judgments.json"),
                ("increment_29", "references_calls_frozen_judgments.json"),
                ("increment_29", "references_calls_development_results.json"),
                ("increment_30", "package_containment_frozen_judgments.json"),
                ("increment_30", "package_containment_development_results.json"),
            )
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
    return (
        {
            "schema": "devtools-i31-mirrored-test-path-judgment-freeze-v1",
            "content_identity": _digest(payload),
            "payload": payload,
        },
        blind,
    )


def write_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist hidden reuse and neutral input separately."""
    frozen, blind = build_population(root)
    for name, artifact in ((JUDGMENT_FREEZE_NAME, frozen), (BLINDED_NAME, blind)):
        path = root / name
        if path.exists() and _read_json(path) != artifact:
            raise ValueError("Existing mirrored-test judgment population differs.")
        write_artifact(path=path, payload=artifact)
    return frozen, blind


if __name__ == "__main__":
    write_population()
