# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PLR0912, PLR0915, PLR2004, TRY003
"""Exact judgment reuse and neutral input for frozen reference candidates."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.phase1_population import _neutral_id, _resource_contents
from experiments.increment_27.structural_imports.cost import load_prior_states
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_29.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    build_freeze,
)

POPULATION_NAME = "references_calls_judgment_freeze.json"
BLINDED_NAME = "references_calls_blinded_judgment_input.json"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")


def _prior_states(
    root: Path, cards: dict[str, Any]
) -> dict[tuple[str, str], dict[str, str]]:
    """Reuse all exact earlier states and the committed 140-pair comparison."""
    i27 = root.parent / "increment_27"
    prior = load_prior_states(i27, cards)
    comparison = cast(
        "dict[str, Any]", _read_json(i27 / "comparison_frozen_judgments.json")
    )
    payload = comparison["payload"]
    if (
        comparison["content_identity"] != _digest(payload)
        or payload["target_count"] != 140
        or len(payload["records"]) != 140
        or payload["usefulness_semantics"] != USEFULNESS_SEMANTICS
        or set(payload["three_states"]) != set(STATES)
    ):
        raise ValueError("Frozen comparison judgment artifact failed validation.")
    identities = {
        (
            card.information_need_purpose,
            card.lexical_query,
            card.parent_snapshot_sha,
        ): case_id
        for case_id, card in cards.items()
    }
    seen: set[tuple[str, str]] = set()
    for row in payload["records"]:
        need = row["information_need"]
        case_id = identities.get(
            (need["purpose"], need["lexical_query"], row["parent_snapshot_sha"])
        )
        if case_id is None:
            raise ValueError("Comparison judgment differs from development cases.")
        if row["usefulness_semantics"] != USEFULNESS_SEMANTICS:
            raise ValueError("Comparison judgment semantics differ.")
        key = (case_id, str(row["address"]))
        state = str(row["judgment"])
        if key in seen or state not in STATES:
            raise ValueError("Comparison judgments duplicate or change states.")
        seen.add(key)
        previous = prior.get(key)
        if previous is not None and previous["state"] != state:
            raise ValueError("Exact frozen judgments conflict.")
        prior.setdefault(key, {"state": state, "source": "increment-27-comparison"})
    return prior


def build_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Join exact reuse only after candidate mechanics are frozen."""
    protocol = cast("dict[str, Any]", _read_json(root / FREEZE_NAME))
    if protocol != build_freeze(root):
        raise ValueError("Candidate protocol changed before judgment reuse.")
    mechanics = cast("dict[str, Any]", _read_json(root / CANDIDATES_NAME))
    if (
        mechanics["freeze_identity"] != protocol["content_identity"]
        or mechanics["content_identity"]
        != _digest(
            {
                key: value
                for key, value in mechanics.items()
                if key != "content_identity"
            }
        )
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
    ):
        raise ValueError("Persisted candidate mechanics failed identity or blinding.")
    population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    allowed = cast("list[str]", protocol["payload"]["development_case_ids"])
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in population["payload"]["task_cards"]
        if row["case_id"] in allowed
    }
    if len(cards) != 24 or [row["case_id"] for row in mechanics["cases"]] != allowed:
        raise ValueError("Judgment reuse population differs from frozen development.")
    prior = _prior_states(root, cards)
    reused: list[dict[str, Any]] = []
    new: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    for case in mechanics["cases"]:
        case_id = str(case["case_id"])
        card = cards[case_id]
        if case["parent_snapshot_sha"] != card.parent_snapshot_sha or case[
            "information_need"
        ] != {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        }:
            raise ValueError("Candidate pair identity differs from frozen case.")
        for candidate in case["candidates"]:
            key = (case_id, str(candidate["address"]))
            identity = {
                "case_id": case_id,
                "information_need": case["information_need"],
                "parent_snapshot_sha": card.parent_snapshot_sha,
                "address": candidate["address"],
                "usefulness_semantics": USEFULNESS_SEMANTICS,
            }
            evidence.append(
                {
                    **identity,
                    "reference": candidate["reference"],
                    "direct_call": candidate["direct_call"],
                    "directions": candidate["directions"],
                    "canonical_positive_rank": candidate["canonical_positive_rank"],
                    "saved_positive_method_ranks": candidate[
                        "saved_positive_method_ranks"
                    ],
                    "existing_import_candidate": candidate["existing_import_candidate"],
                    "support_count": candidate["support_count"],
                }
            )
            previous = prior.get(key)
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
    if (
        len(evidence) != mechanics["summary"]["candidate_pairs"]
        or len({(row["case_id"], row["address"]) for row in evidence}) != len(evidence)
        or len(reused) + len(new) != len(evidence)
    ):
        raise ValueError("Candidate pair coverage or exact reuse is invalid.")
    contents = _resource_contents(
        list(dict.fromkeys((row["parent_snapshot_sha"], row["address"]) for row in new))
    )
    blind_cases: list[dict[str, Any]] = []
    for case_id in allowed:
        card = cards[case_id]
        resources = [
            {
                "neutral_resource_id": _neutral_id(
                    "resource",
                    f"{mechanics['content_identity']}|{case_id}|{row['address']}",
                ),
                "address": row["address"],
                "content": contents[(card.parent_snapshot_sha, row["address"])],
            }
            for row in new
            if row["case_id"] == case_id
        ]
        if resources:
            resources.sort(key=lambda item: item["neutral_resource_id"])
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
    blind_cases.sort(key=lambda row: row["neutral_case_id"])
    blind_payload = {
        "schema": "devtools-i29-neutral-references-calls-input-v1",
        "cases": blind_cases,
    }
    blind = {
        "schema": blind_payload["schema"],
        "content_identity": _digest(blind_payload),
        "payload": blind_payload,
    }
    reused_states = Counter(row["judgment"] for row in reused)
    new_keys = {(item["case_id"], item["address"]) for item in new}
    unjudged_distribution = Counter(
        "call_tagged" if row["direct_call"] else "reference_without_call"
        for row in evidence
        if (row["case_id"], row["address"]) in new_keys
    )
    new_evidence = [
        row for row in evidence if (row["case_id"], row["address"]) in new_keys
    ]
    new_by_direction = Counter(
        direction for row in new_evidence for direction in row["directions"]
    )
    new_by_case = Counter(row["case_id"] for row in new_evidence)
    prior_sources = cast(
        "dict[str, str]",
        cast(
            "dict[str, Any]",
            _read_json(
                root.parent / "increment_27" / "structural_import_judgment_freeze.json"
            ),
        )["payload"]["frozen_judgment_source_sha256"],
    )
    for name, digest in prior_sources.items():
        source = (
            root.parent / name
            if name.startswith("increment_")
            else root.parent / "increment_27" / name
        )
        if sha256_file(source) != digest:
            raise ValueError("An exact prior judgment source changed after freeze.")
    payload: dict[str, Any] = {
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": protocol["payload"]["heldout_case_ids_sealed"],
        "candidate_freeze_identity": protocol["content_identity"],
        "candidate_identity": mechanics["content_identity"],
        "candidate_sha256": sha256_file(root / CANDIDATES_NAME),
        "comparison_judgments_sha256": sha256_file(
            root.parent / "increment_27" / "comparison_frozen_judgments.json"
        ),
        "prior_judgment_source_sha256": prior_sources,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "three_states": list(STATES),
        "pair_identity_rule": [
            "InformationNeed purpose",
            "frozen query",
            "parent snapshot",
            "resource address",
            "usefulness semantics",
        ],
        "pair_evidence": evidence,
        "reused_judgments": reused,
        "new_judgment_pairs": new,
        "counts": {
            "candidate_pairs": len(evidence),
            "exact_reused": len(reused),
            "new_judgments_required": len(new),
            "reused_states": {state: reused_states[state] for state in STATES},
            "new_by_reference_call": dict(sorted(unjudged_distribution.items())),
            "new_by_direction": dict(sorted(new_by_direction.items())),
            "new_by_case": dict(sorted(new_by_case.items())),
            "new_absent_all_saved_positive_lexical": sum(
                all(
                    rank is None for rank in row["saved_positive_method_ranks"].values()
                )
                for row in new_evidence
            ),
            "new_absent_import_candidates": sum(
                not row["existing_import_candidate"] for row in new_evidence
            ),
            "new_absent_lexical_and_import": sum(
                not row["existing_import_candidate"]
                and all(
                    rank is None for rank in row["saved_positive_method_ranks"].values()
                )
                for row in new_evidence
            ),
        },
        "blinded_input_identity": blind["content_identity"],
        "new_usefulness_outcomes": False,
        "confirmation_executed": False,
    }
    frozen = {
        "schema": "devtools-i29-references-calls-judgment-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }
    return frozen, blind


def write_population(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist hidden pair evidence and separate origin-blind human input."""
    frozen, blind = build_population(root)
    for name, artifact in ((POPULATION_NAME, frozen), (BLINDED_NAME, blind)):
        path = root / name
        if path.exists() and _read_json(path) != artifact:
            raise ValueError("Existing References/Calls judgment population differs.")
        write_artifact(path=path, payload=artifact)
    return frozen, blind
