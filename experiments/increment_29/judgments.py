# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Origin-blind judgments for the frozen Increment-29 neutral input."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest

if TYPE_CHECKING:
    from collections.abc import Mapping

ROOT = Path(__file__).resolve().parent
INPUT_NAME = "references_calls_blinded_judgment_input.json"
OUTPUT_NAME = "references_calls_frozen_judgments.json"
INPUT_IDENTITY = "5c00fbf66914df9f6ce2f6d47cf0a891b02b4ff34e69dda7ac6c12f54ef473ba"
INPUT_SHA256 = "14a34a48f3d21f6b069f1de32e8caf7b33d9c93c2faa1c100dc0c3fd2f4ff75c"
SEMANTICS = "purpose-relative-three-state-v1"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")

# Opaque resource identities come only from the verified neutral input.
# Rationale text describes task usefulness, never candidate provenance.
DECISIONS: Mapping[str, tuple[str, str]] = {
    "resource-026ccd13898217c5": (
        "USEFUL",
        "Tests combined declarations across resources and exact-name retrieval, including which source resource supplied each match.",
    ),
    "resource-3fdd6ba66abb0c2f": (
        "USEFUL",
        "Tests that direct function declarations retain distinct source resource addresses and identities needed for resource selection.",
    ),
    "resource-50e4f970d25a581b": (
        "NOT_USEFUL",
        "Tests model-request assembly after Context rendering; exact-name resource selection is only setup.",
    ),
    "resource-8f7ce49068a13c24": (
        "NOT_USEFUL",
        "Defines general addressed resource observation without exact-name function resource selection.",
    ),
    "resource-4306c12606b2a5b3": (
        "NOT_USEFUL",
        "Tests model-request assembly from a single-resource Context, not cross-resource source materialization.",
    ),
    "resource-5dddaf9575c53624": (
        "NOT_USEFUL",
        "Tests exact-name retrieval over one resource, without cross-resource source materialization.",
    ),
    "resource-276852ca85f80505": (
        "NOT_USEFUL",
        "Tests downstream model-request assembly rather than combining declaration analyses across resources.",
    ),
    "resource-a5ebfb1e923fe526": (
        "NOT_USEFUL",
        "Tests source extraction after disclosure, not multi-resource declaration aggregation.",
    ),
    "resource-0d186c0dedf2dc8c": (
        "NOT_USEFUL",
        "Tests downstream request assembly, not deriving declarations from an explicitly addressed resource.",
    ),
    "resource-e4eb1b5957276d18": (
        "NOT_USEFUL",
        "Tests materialization of already derived declarations, not explicit-resource declaration derivation.",
    ),
    "resource-f8193cdc16b3ef3c": (
        "NOT_USEFUL",
        "Tests retrieval over completed declaration knowledge, not explicit-resource derivation.",
    ),
    "resource-178d2149cf34d45c": (
        "NOT_USEFUL",
        "Tests a function Context pipeline over caller-specified addresses, without discovering repository resources.",
    ),
    "resource-1a1962e561de610c": (
        "NOT_USEFUL",
        "Tests model-request assembly from prepared Context, without repository resource discovery.",
    ),
    "resource-3059ec9a840ab905": (
        "NOT_USEFUL",
        "Tests function source materialization from an explicit snapshot, without resource discovery.",
    ),
    "resource-4c779572dce4d243": (
        "NOT_USEFUL",
        "Tests rendering of materialized function Context, without resource discovery.",
    ),
    "resource-6c4e915c2b17b06b": (
        "NOT_USEFUL",
        "Tests exact-name function retrieval, without repository resource discovery.",
    ),
    "resource-7914f14580fd1643": (
        "NOT_USEFUL",
        "Tests selecting resources from completed function retrieval results, not discovering repository resources.",
    ),
    "resource-91c6581e07638a40": (
        "NOT_USEFUL",
        "Tests Context disclosure of function matches, without repository resource discovery.",
    ),
    "resource-9e5b69e91a850ccb": (
        "NOT_USEFUL",
        "Tests function declarations in explicitly observed resources, without discovering repository resources.",
    ),
}


def build_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Bind one decision per neutral target without opening origin evidence."""
    path = root / INPUT_NAME
    blind = cast("dict[str, Any]", _read_json(path))
    if (
        blind["content_identity"] != INPUT_IDENTITY
        or sha256_file(path) != INPUT_SHA256
        or blind["content_identity"] != _digest(blind["payload"])
    ):
        raise ValueError("Neutral input identity changed before adjudication.")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for case in blind["payload"]["cases"]:
        for resource in case["resources"]:
            neutral_id = str(resource["neutral_resource_id"])
            if neutral_id in seen or neutral_id not in DECISIONS:
                raise ValueError("Neutral target is duplicate or lacks a decision.")
            seen.add(neutral_id)
            state, rationale = DECISIONS[neutral_id]
            if state not in STATES or not rationale.strip():
                raise ValueError("Judgment state or rationale is invalid.")
            records.append(
                {
                    "neutral_case_id": case["neutral_case_id"],
                    "information_need": case["information_need"],
                    "parent_snapshot_sha": case["parent_snapshot_sha"],
                    "neutral_resource_id": neutral_id,
                    "address": resource["address"],
                    "usefulness_semantics": SEMANTICS,
                    "judgment": state,
                    "rationale": rationale,
                }
            )
    if len(records) != 19 or seen != set(DECISIONS):
        raise ValueError("Judgment coverage differs from frozen 19 targets.")
    counts = Counter(row["judgment"] for row in records)
    payload = {
        "schema": "devtools-i29-neutral-references-calls-frozen-judgments-v1",
        "blinded_input_content_identity": INPUT_IDENTITY,
        "blinded_input_sha256": INPUT_SHA256,
        "usefulness_semantics": SEMANTICS,
        "three_states": list(STATES),
        "target_count": len(records),
        "state_counts": {state: counts[state] for state in STATES},
        "records": records,
    }
    return {
        "schema": payload["schema"],
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Persist all blinded outcomes before any candidate-origin join."""
    artifact = build_judgments(root)
    path = root / OUTPUT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Increment-29 frozen judgments differ.")
    write_artifact(path=path, payload=artifact)
    return artifact
