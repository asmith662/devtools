# Copyright (c) 2026
# ruff: noqa: C901, E501, EM101, EM102, PLR0912, PLR0915, PLR2004, TRY003
"""Freeze the neutral top-five union from the saved lexical comparison."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, cast

from experiments.increment_25.development import _task_card, write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import (
    EXPECTED_DEVELOPMENT_SIZE,
    _read_json,
    canonical_json_bytes,
    load_existing_judgments,
    prior_judgment_matches,
    sha256_file,
)
from experiments.increment_27.phase1_population import _resource_contents

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from experiments.increment_25.task_population import TaskCard

METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")
TOP_K = 5
EXPECTED_POOL_SIZE = 191
EXPECTED_REUSED_SIZE = 58
EXPECTED_NEW_SIZE = 133
ALLOWED_STATES = {"useful", "not-useful", "unjudged"}
EXPECTED_PHASE0_SHA256 = (
    "846e88929234261ac8e0fc3c872b65c329bb571f129181597bae1be8a9a7b800"
)
EXPECTED_PHASE0_RANKINGS_SHA256 = (
    "6072195afe50376722c06157ae04e8b33ed1346e4c75c763d83f22f30dd72657"
)
EXPECTED_PHASE1_SHA256 = {
    "phase1_population_freeze.json": "9cc4795711ac44e2a9537605af7bb78fa8968d0ffb15eb52488915e23063e19b",
    "phase1_pooled_pairs.json": "a9d56ba5ce3ddcf5a21411daa0a0d0ea14d3487e33c2cc20408e3bbe2181310d",
    "phase1_reused_judgments.json": "0475e11f86a385f5b91c0f5778444cd9c23f63d0d6551e9e6ca2ec3203e47783",
    "phase1_blinded_judgment_input.json": "b7ccacfe76990cfab5ad0f17b70886ca5d9c4d8fc8e4c88f03b2d8ddb00f55e2",
}
EXPECTED_PHASE1_CONTENT_IDENTITY = (
    "44ea9b89baec2e68e11ee3ba476317e7ef65f9c396b965b1bcc38e727cd07642"
)
FREEZE_SCHEMA = "devtools-increment-27-top5-lexical-pool-freeze-v1"
POOL_SCHEMA = "devtools-increment-27-top5-lexical-pooled-pairs-v1"
REUSE_SCHEMA = "devtools-increment-27-top5-lexical-reused-judgments-v1"
BLINDED_SCHEMA = "devtools-increment-27-top5-blinded-judgment-input-v1"


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _neutral_id(prefix: str, identity: str) -> str:
    return f"{prefix}-{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:16]}"


def _validated_source_judgments(
    *,
    experiment_root: Path,
    development_ids: set[str],
) -> tuple[
    dict[tuple[str, str], dict[str, object]],
    dict[str, str],
]:
    """Return exact source-row identities after the existing audits validate them."""
    i25_judgments_path = (
        experiment_root / "increment_25" / "confirmation_frozen_judgments.json"
    )
    i25_mapping_path = (
        experiment_root / "increment_25" / "confirmation_neutral_mapping.json"
    )
    i25_input_path = (
        experiment_root / "increment_25" / "confirmation_judgment_input.json"
    )
    i26_judgments_path = (
        experiment_root / "increment_26" / "development_frozen_judgments.json"
    )
    i26_input_path = (
        experiment_root / "increment_26" / "development_judgment_input.json"
    )
    source_hashes = {
        "increment_25_confirmation_judgments": sha256_file(i25_judgments_path),
        "increment_25_confirmation_neutral_mapping": sha256_file(i25_mapping_path),
        "increment_25_confirmation_judgment_input": sha256_file(i25_input_path),
        "increment_26_development_judgments": sha256_file(i26_judgments_path),
        "increment_26_development_judgment_input": sha256_file(i26_input_path),
    }
    i25_judgments = _read_json(i25_judgments_path)
    i25_mapping = _read_json(i25_mapping_path)
    i26_judgments = _read_json(i26_judgments_path)
    rows: dict[tuple[str, str], dict[str, object]] = {}

    i25_payload = cast("dict[str, object]", i25_judgments["payload"])
    i25_map_payload = cast("dict[str, object]", i25_mapping["payload"])
    map_cases = {
        str(item["case_id"]): cast("list[dict[str, object]]", item["mappings"])
        for item in cast("list[dict[str, object]]", i25_map_payload["cases"])
    }
    for case in cast("list[dict[str, object]]", i25_payload["cases"]):
        case_id = str(case["case_id"])
        if case_id not in development_ids:
            continue
        address_by_neutral = {
            str(item["neutral_id"]): str(item["address"]) for item in map_cases[case_id]
        }
        for record in cast("list[dict[str, object]]", case["records"]):
            neutral = str(record["neutral_id"])
            address = address_by_neutral[neutral]
            identity = _digest(
                {
                    "source_artifact_sha256": source_hashes[
                        "increment_25_confirmation_judgments"
                    ],
                    "source_case_id": case_id,
                    "source_resource_address": address,
                    "source_record": record,
                },
            )
            rows[(case_id, address)] = {
                "source_artifact": "experiments/increment_25/confirmation_frozen_judgments.json",
                "source_artifact_sha256": source_hashes[
                    "increment_25_confirmation_judgments"
                ],
                "source_mapping_artifact": "experiments/increment_25/confirmation_neutral_mapping.json",
                "source_mapping_artifact_sha256": source_hashes[
                    "increment_25_confirmation_neutral_mapping"
                ],
                "source_judgment_identity": identity,
                "judgment": str(record["judgment"]),
            }

    i26_payload = cast("dict[str, object]", i26_judgments["payload"])
    for case in cast("list[dict[str, object]]", i26_payload["cases"]):
        case_id = str(case["case_id"])
        if case_id not in development_ids:
            continue
        for record in cast("list[dict[str, object]]", case["records"]):
            address = str(record["address"])
            identity = _digest(
                {
                    "source_artifact_sha256": source_hashes[
                        "increment_26_development_judgments"
                    ],
                    "source_case_id": case_id,
                    "source_resource_address": address,
                    "source_record": record,
                },
            )
            key = (case_id, address)
            if key in rows:
                raise ValueError(
                    f"Prior judgment sources overlap for {case_id}/{address}.",
                )
            rows[key] = {
                "source_artifact": "experiments/increment_26/development_frozen_judgments.json",
                "source_artifact_sha256": source_hashes[
                    "increment_26_development_judgments"
                ],
                "source_blinded_input_artifact": "experiments/increment_26/development_judgment_input.json",
                "source_blinded_input_artifact_sha256": source_hashes[
                    "increment_26_development_judgment_input"
                ],
                "source_judgment_identity": identity,
                "judgment": str(record["judgment"]),
            }
    return rows, source_hashes


def build_top5_artifacts(*, experiment_root: Path) -> dict[str, dict[str, object]]:
    """Build the non-blinded pool, exact reuse map, blinded input, and freeze."""
    i27_root = experiment_root / "increment_27"
    phase0_path = i27_root / "experiment_freeze.json"
    phase0 = _read_json(phase0_path)
    phase0_identity = str(phase0["content_identity"])
    phase0_payload = cast("dict[str, object]", phase0["payload"])
    if (
        phase0_identity
        != "758f338af25a5f88fa66229d5ed29f1065a244f4116e0ac843e169114624254c"
        or phase0_identity != _digest(phase0_payload)
        or sha256_file(phase0_path) != EXPECTED_PHASE0_SHA256
    ):
        raise ValueError("Phase-0 freeze integrity check failed.")
    baseline_path = i27_root / "canonical_positive_lexical_rankings.json"
    if sha256_file(baseline_path) != EXPECTED_PHASE0_RANKINGS_SHA256:
        raise ValueError("Phase-0 canonical ranking artifact changed.")
    phase1_freeze = _read_json(i27_root / "phase1_population_freeze.json")
    if phase1_freeze.get("content_identity") != EXPECTED_PHASE1_CONTENT_IDENTITY:
        raise ValueError("Suspended Phase-1 deep-pool freeze identity changed.")
    for filename, expected_sha in EXPECTED_PHASE1_SHA256.items():
        if sha256_file(i27_root / filename) != expected_sha:
            raise ValueError(f"Suspended Phase-1 artifact changed: {filename}.")
    development = cast(
        "list[dict[str, object]]",
        cast("dict[str, object]", phase0_payload["source_population"])[
            "development_cases"
        ],
    )
    cards_by_id: dict[str, TaskCard] = {}
    task_freeze = _read_json(
        experiment_root / "increment_25" / "task_population_freeze.json",
    )
    for item in cast(
        "list[dict[str, object]]",
        cast("dict[str, object]", task_freeze["payload"])["task_cards"],
    ):
        card = _task_card(item)
        if card.case_id in {str(record["case_id"]) for record in development}:
            cards_by_id[card.case_id] = card
    development_ids = set(cards_by_id)
    if len(development_ids) != EXPECTED_DEVELOPMENT_SIZE:
        raise ValueError(
            "Top-five population requires exactly 24 frozen development cases.",
        )

    comparison_freeze_path = i27_root / "lexical_comparison_freeze.json"
    comparison_rankings_path = i27_root / "lexical_comparison_rankings.json"
    comparison_analysis_path = i27_root / "lexical_comparison_analysis.json"
    comparison_freeze = _read_json(comparison_freeze_path)
    comparison_payload = cast("dict[str, object]", comparison_freeze["payload"])
    rankings = _read_json(comparison_rankings_path)
    analysis = _read_json(comparison_analysis_path)
    ranking_body = {
        key: value for key, value in rankings.items() if key != "content_identity"
    }
    analysis_body = {
        key: value for key, value in analysis.items() if key != "content_identity"
    }
    if (
        comparison_freeze["content_identity"] != _digest(comparison_payload)
        or rankings["content_identity"] != _digest(ranking_body)
        or analysis["content_identity"] != _digest(analysis_body)
        or rankings["configuration_identity"] != comparison_freeze["content_identity"]
        or analysis["configuration_identity"] != comparison_freeze["content_identity"]
        or analysis["rankings_identity"] != rankings["content_identity"]
        or analysis["rankings_sha256"] != sha256_file(comparison_rankings_path)
    ):
        raise ValueError("Lexical comparison artifact identity binding failed.")
    if (
        comparison_payload["phase0_freeze_identity"] != phase0_identity
        or comparison_payload["phase0_freeze_sha256"] != EXPECTED_PHASE0_SHA256
    ):
        raise ValueError("Lexical comparison is bound to another Phase-0 freeze.")
    frozen_methods = [
        str(item["id"])
        for item in cast("list[dict[str, object]]", comparison_payload["methods"])
    ]
    if tuple(frozen_methods) != METHODS:
        raise ValueError("Top-five method set differs from the frozen comparison.")
    comparison_case_ids = set(
        cast("list[str]", comparison_payload["development_case_ids"]),
    )
    heldout_ids = set(cast("list[str]", comparison_payload["heldout_case_ids_sealed"]))
    if (
        comparison_case_ids != development_ids
        or len(heldout_ids) != 14
        or heldout_ids & development_ids
    ):
        raise ValueError("Comparison case population or sealed partition changed.")
    ranked_cases = cast("list[dict[str, object]]", rankings["cases"])
    if (
        len(ranked_cases) != EXPECTED_DEVELOPMENT_SIZE
        or {str(item["case_id"]) for item in ranked_cases} != development_ids
    ):
        raise ValueError(
            "Saved lexical comparison rankings differ from 24 development cases.",
        )

    method_pairs: dict[str, set[tuple[str, str, str, str]]] = {
        method: set() for method in METHODS
    }
    pooled: dict[tuple[str, str, str, str], dict[str, object]] = {}
    case_identity_seen: dict[tuple[str, str, str], str] = {}
    for case in ranked_cases:
        case_id = str(case["case_id"])
        card = cards_by_id[case_id]
        need = {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        }
        parent = str(card.parent_snapshot_sha)
        if (
            case["parent_snapshot_sha"] != parent
            or case["query_text"] != card.lexical_query
            or case_id in heldout_ids
        ):
            raise ValueError(f"Saved comparison identity mismatch for {case_id}.")
        key_prefix = (card.information_need_purpose, card.lexical_query, parent)
        previous_case = case_identity_seen.setdefault(key_prefix, case_id)
        if previous_case != case_id:
            raise ValueError(
                "Two case IDs share one exact InformationNeed/snapshot identity.",
            )
        rank_sets = cast("dict[str, list[dict[str, object]]]", case["rankings"])
        if set(rank_sets) != set(METHODS):
            raise ValueError(f"Method ranking set differs for {case_id}.")
        for method in METHODS:
            rows = rank_sets[method]
            selected = rows[:TOP_K]
            if [cast("int", row["rank"]) for row in rows] != list(
                range(1, len(rows) + 1),
            ):
                raise ValueError(
                    f"Saved {method} ranking has invalid ranks for {case_id}.",
                )
            for row in selected:
                address = str(row["address"])
                key = (*key_prefix, address)
                method_pairs[method].add(key)
                record = pooled.setdefault(
                    key,
                    {
                        "case_id": case_id,
                        "information_need": need,
                        "parent_snapshot_sha": parent,
                        "address": address,
                        "method_ranks": {},
                    },
                )
                cast("dict[str, int]", record["method_ranks"])[method] = cast(
                    "int",
                    row["rank"],
                )

    pair_keys = set(pooled)
    if len(pair_keys) != EXPECTED_POOL_SIZE:
        raise ValueError(f"Top-five union size is {len(pair_keys)}, expected 191.")
    method_occurrences = {method: len(method_pairs[method]) for method in METHODS}
    overlaps = {
        f"{left} x {right}": len(method_pairs[left] & method_pairs[right])
        for index, left in enumerate(METHODS)
        for right in METHODS[index + 1 :]
    }
    exclusive = {
        method: len(
            method_pairs[method]
            - set().union(
                *(method_pairs[other] for other in METHODS if other != method),
            ),
        )
        for method in METHODS
    }
    membership_distribution = {
        str(count): sum(
            len(cast("dict[str, int]", record["method_ranks"])) == count
            for record in pooled.values()
        )
        for count in range(1, len(METHODS) + 1)
    }
    pair_rows = list(pooled.values())
    pooled_identity = _digest(pair_rows)

    # Build the set before loading labels; judgments never affect membership.
    prior_rows = load_existing_judgments(
        experiment_root=experiment_root,
        cards=cards_by_id,
    )
    prior_by_pair = {
        (case_id, str(record["address"])): record
        for case_id, records in prior_rows.items()
        for record in records
    }
    raw_sources, source_hashes = _validated_source_judgments(
        experiment_root=experiment_root,
        development_ids=development_ids,
    )
    reused_rows: list[dict[str, object]] = []
    new_rows: list[dict[str, object]] = []
    for pair in pooled.values():
        case_id = str(pair["case_id"])
        address = str(pair["address"])
        prior = prior_by_pair.get((case_id, address))
        if prior is None:
            new_rows.append({"case_id": case_id, "address": address})
            continue
        if not prior_judgment_matches(
            card=cards_by_id[case_id],
            prior_information_need=cast(
                "Mapping[str, object]",
                prior["information_need_identity"],
            ),
            prior_parent_snapshot=str(prior["parent_snapshot_sha"]),
            prior_address=address,
            resource_address=address,
            prior_usefulness_semantics=str(prior["judgment_semantics"]),
        ):
            raise ValueError(f"Prior label identity mismatch for {case_id}/{address}.")
        source = raw_sources.get((case_id, address))
        if source is None or source["judgment"] != prior["judgment"]:
            raise ValueError(
                f"Could not bind exact source judgment for {case_id}/{address}.",
            )
        state = str(prior["judgment"])
        if state not in ALLOWED_STATES:
            raise ValueError(f"Unknown prior usefulness state for {case_id}/{address}.")
        reused_rows.append(
            {
                "case_id": case_id,
                "information_need": pair["information_need"],
                "parent_snapshot_sha": pair["parent_snapshot_sha"],
                "address": address,
                "judgment": state,
                "judgment_semantics": USEFULNESS_SEMANTICS,
                "source_artifact": source["source_artifact"],
                "source_artifact_sha256": source["source_artifact_sha256"],
                "source_mapping_artifact": source.get("source_mapping_artifact"),
                "source_mapping_artifact_sha256": source.get(
                    "source_mapping_artifact_sha256",
                ),
                "source_blinded_input_artifact": source.get(
                    "source_blinded_input_artifact",
                ),
                "source_blinded_input_artifact_sha256": source.get(
                    "source_blinded_input_artifact_sha256",
                ),
                "source_judgment_identity": source["source_judgment_identity"],
            },
        )
    if len(reused_rows) != EXPECTED_REUSED_SIZE:
        raise ValueError(f"Reusable judgment count is {len(reused_rows)}, expected 58.")
    if len(new_rows) != EXPECTED_NEW_SIZE:
        raise ValueError(f"New judgment count is {len(new_rows)}, expected 133.")

    ranking_sha = sha256_file(comparison_rankings_path)
    pool_payload: dict[str, object] = {
        "schema": POOL_SCHEMA,
        "comparison_configuration_identity": comparison_freeze["content_identity"],
        "lexical_ranking_identity": rankings["content_identity"],
        "lexical_rankings_sha256": ranking_sha,
        "pool_definition": "union of ranks 1 through 5 per frozen method and development InformationNeed; deduplicate exact InformationNeed/purpose+query, parent snapshot, and resource address",
        "population_identity": pooled_identity,
        "method_membership_distribution": membership_distribution,
        "per_method_occurrences": method_occurrences,
        "pairwise_method_overlap": overlaps,
        "method_exclusive_counts": exclusive,
        "pairs": pair_rows,
    }
    pool_artifact = {
        "schema": POOL_SCHEMA,
        "content_identity": _digest(pool_payload),
        "payload": pool_payload,
    }
    reuse_payload: dict[str, object] = {
        "schema": REUSE_SCHEMA,
        "pooled_population_identity": pooled_identity,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "identity_rule": [
            "exact InformationNeed purpose",
            "exact frozen query",
            "exact parent snapshot identity",
            "exact resource address",
            "exact usefulness semantics",
        ],
        "source_judgment_artifact_sha256": source_hashes,
        "reused_count": len(reused_rows),
        "state_counts": {
            state: sum(row["judgment"] == state for row in reused_rows)
            for state in ("useful", "not-useful", "unjudged")
        },
        "records": reused_rows,
    }
    reuse_artifact = {
        "schema": REUSE_SCHEMA,
        "content_identity": _digest(reuse_payload),
        "payload": reuse_payload,
    }

    neutral_case_id = {
        case_id: _neutral_id(
            "case",
            f"{comparison_freeze['content_identity']}|{case_id}",
        )
        for case_id in development_ids
    }
    new_by_case: dict[str, list[dict[str, object]]] = {
        case_id: [] for case_id in development_ids
    }
    for row in new_rows:
        new_by_case[str(row["case_id"])].append(row)
    parent_pairs: list[tuple[str, str]] = []
    for row in new_rows:
        case_id = str(row["case_id"])
        parent_pairs.append(
            (cards_by_id[case_id].parent_snapshot_sha, str(row["address"])),
        )
    contents = _resource_contents(list(dict.fromkeys(parent_pairs)))
    blind_cases: list[dict[str, object]] = []
    for case_id, card in cards_by_id.items():
        targets = []
        for row in new_by_case[case_id]:
            address = str(row["address"])
            targets.append(
                {
                    "neutral_resource_id": _neutral_id(
                        "resource",
                        f"{comparison_freeze['content_identity']}|{case_id}|{address}",
                    ),
                    "address": address,
                    "content": contents[(card.parent_snapshot_sha, address)],
                },
            )
        targets.sort(key=lambda item: str(item["neutral_resource_id"]))
        blind_cases.append(
            {
                "neutral_case_id": neutral_case_id[case_id],
                "information_need": {
                    "purpose": card.information_need_purpose,
                    "lexical_query": card.lexical_query,
                },
                "parent_snapshot_sha": card.parent_snapshot_sha,
                "resources": targets,
            },
        )
    blind_cases.sort(key=lambda item: str(item["neutral_case_id"]))
    blinded_payload: dict[str, object] = {
        "schema": BLINDED_SCHEMA,
        "cases": blind_cases,
    }
    blinded_artifact = {
        "schema": BLINDED_SCHEMA,
        "content_identity": _digest(blinded_payload),
        "payload": blinded_payload,
    }
    blinded_identity = str(blinded_artifact["content_identity"])
    reuse_identity = str(reuse_artifact["content_identity"])
    freeze_payload: dict[str, object] = {
        "phase0_freeze_identity": phase0_identity,
        "phase1_deep_pool_freeze_identity": EXPECTED_PHASE1_CONTENT_IDENTITY,
        "phase1_deep_pool_status": "preserved frozen population; adjudication suspended",
        "phase1_deep_pool_artifact_sha256": EXPECTED_PHASE1_SHA256,
        "lexical_comparison_configuration_identity": comparison_freeze[
            "content_identity"
        ],
        "lexical_comparison_configuration_sha256": sha256_file(comparison_freeze_path),
        "lexical_ranking_identity": rankings["content_identity"],
        "lexical_rankings_sha256": ranking_sha,
        "development_case_ids": [str(item["case_id"]) for item in development],
        "heldout_confirmation_case_count": len(heldout_ids),
        "heldout_confirmation_outcomes_included": False,
        "pooled_population_identity": pooled_identity,
        "method_surface_diagnostics": {
            "membership_distribution": membership_distribution,
            "per_method_occurrences": method_occurrences,
            "pairwise_method_overlap": overlaps,
            "method_exclusive_counts": exclusive,
        },
        "pooled_pair_count": len(pair_rows),
        "pooled_pairs": pair_rows,
        "reused_judgment_mapping_identity": reuse_identity,
        "reused_judgment_count": len(reused_rows),
        "reused_judgments": reused_rows,
        "new_blinded_population_identity": blinded_identity,
        "new_judgment_count": len(new_rows),
        "new_judgment_pairs": new_rows,
        "source_judgment_artifact_sha256": source_hashes,
        "judgment_semantics": {
            "useful": "useful for the frozen InformationNeed purpose",
            "not_useful": "not useful for the frozen InformationNeed purpose",
            "unjudged": "no usefulness outcome; never coerce to not-useful",
        },
        "blinding_rules": [
            "expose only neutral case ID, frozen purpose and query, parent snapshot identity, neutral resource ID/address, and parent-snapshot content",
            "hide method membership, method-exclusive status, overlap, rank, score, BM25 components, identifier/path/RRF evidence, prior structural/semantic evidence, changed paths, task diff, post-change content, and other-resource judgments",
            "include no usefulness label in the new blinded input",
            "sort neutral case and resource identities by their opaque identifiers, not retrieval rank or method",
        ],
        "new_usefulness_outcomes": False,
    }
    freeze_artifact = {
        "schema": FREEZE_SCHEMA,
        "content_identity": _digest(freeze_payload),
        "payload": freeze_payload,
    }
    return {
        "lexical_top5_judgment_freeze.json": cast("dict[str, object]", freeze_artifact),
        "lexical_top5_pooled_pairs.json": cast("dict[str, object]", pool_artifact),
        "lexical_top5_reused_judgments.json": cast("dict[str, object]", reuse_artifact),
        "lexical_top5_blinded_judgment_input.json": cast(
            "dict[str, object]",
            blinded_artifact,
        ),
    }


def write_top5_artifacts(*, experiment_root: Path) -> dict[str, str]:
    """Write deterministic artifacts derived only from saved rankings."""
    artifacts = build_top5_artifacts(experiment_root=experiment_root)
    output_root = experiment_root / "increment_27"
    return {
        name: _write_artifact_identity(path=output_root / name, artifact=artifact)
        for name, artifact in artifacts.items()
    }


def _write_artifact_identity(*, path: Path, artifact: Mapping[str, object]) -> str:
    write_artifact(path=path, payload=artifact)
    return hashlib.sha256(path.read_bytes()).hexdigest()
