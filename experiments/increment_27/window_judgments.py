# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, PLR2004, TRY003
"""Freeze twelve origin-blind retrieval-unit usefulness judgments."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.window_unit import _digest

FREEZE_IDENTITY = "bfb805bcc124b5eef9cf27cb44905287cfef41a108fd903864024ad781eb8a62"
BLINDED_IDENTITY = "ae238e965b8278ed788f24ff93c21354bb167bfd7d0de2c9381d125fb20ce28c"
BLINDED_SHA256 = "a179fcbd35f6e1f175df7186381ad5ecdd0ab42ec020e62093e09984e82f372f"
EXPECTED_COUNT = 12
LABELS = {"USEFUL", "NOT_USEFUL", "UNJUDGED"}
SEMANTICS = {
    "USEFUL": "Parent-snapshot resource would materially help satisfy the frozen InformationNeed.",
    "NOT_USEFUL": "Parent-snapshot resource would not materially help satisfy the frozen InformationNeed.",
    "UNJUDGED": "The blinded InformationNeed and resource do not support a defensible binary judgment.",
}

# Each decision was made from the committed neutral input alone. Resource IDs
# refer to that input, not to method membership, rank, score, or window evidence.
DECISIONS: dict[str, tuple[str, str]] = {
    "resource-01896c8f8bc08b3a": (
        "NOT_USEFUL",
        "The tests exercise llama.cpp model interactions and HTTP response handling; they do not specify Python function source materialization.",
    ),
    "resource-697418696ac4d55c": (
        "UNJUDGED",
        "The frozen purpose is only 'ed evidence'; it does not identify the evidence work well enough to judge whether Session documentation would materially help.",
    ),
    "resource-7e946d62b8b944aa": (
        "NOT_USEFUL",
        "The tests cover llama.cpp provider behavior, not derivation of Python function declarations from source.",
    ),
    "resource-a95e76ab09a651c2": (
        "NOT_USEFUL",
        "The llama.cpp adapter handles model requests and responses; it contains no Python declaration derivation behavior or interface.",
    ),
    "resource-2fa9b098f7c866cb": (
        "NOT_USEFUL",
        "This filesystem overview covers file models and bounded reads and explicitly excludes directory traversal and repository indexing; it does not specify bounded repository resource discovery.",
    ),
    "resource-06152d4559675fce": (
        "NOT_USEFUL",
        "The vLLM benchmark runner collects streamed content, usage, and timing; it does not define or preserve model reasoning content in the interaction response.",
    ),
    "resource-f9993c89d51f5643": (
        "USEFUL",
        "The llama.cpp adapter constructs ModelResponse from provider output and parses assistant content, making it a direct integration point for separate reasoning content.",
    ),
    "resource-4a9c9743a4f29b55": (
        "NOT_USEFUL",
        "The Stopwatch implements elapsed-time measurement, with no repository Context discovery behavior.",
    ),
    "resource-e8557fc45206f311": (
        "NOT_USEFUL",
        "The timing document explains Stopwatch lifecycle and clock semantics, not repository Context discovery.",
    ),
    "resource-9a64913a5bc5d69a": (
        "NOT_USEFUL",
        "The regex overview describes generic pattern matching and explicitly excludes document querying or indexing; it does not specify repository text document representation.",
    ),
    "resource-5c56e4dae201f112": (
        "USEFUL",
        "The source materializer consumes exact-name disclosure items and their source occurrences, showing the downstream interface that exact-name function resource selection must supply.",
    ),
    "resource-32895fcca1c0369d": (
        "USEFUL",
        "The llama.cpp send method builds the provider request without an output bound, so it is the direct request path to extend for model interaction output limits.",
    ),
}


def validate_blinded_input(path: Path) -> dict[str, Any]:
    """Require the exact committed neutral target population and no origin fields."""
    if sha256_file(path) != BLINDED_SHA256:
        raise ValueError("Committed blinded input hash changed.")
    blind = cast("dict[str, Any]", _read_json(path))
    if (
        set(blind)
        != {
            "schema",
            "window_freeze_identity",
            "pool_identity",
            "judgment_semantics",
            "cases",
            "content_identity",
        }
        or blind["schema"] != "devtools-i27-window-unit-blinded-input-v1"
        or blind["window_freeze_identity"] != FREEZE_IDENTITY
        or blind["content_identity"] != BLINDED_IDENTITY
        or blind["content_identity"]
        != _digest(
            {key: value for key, value in blind.items() if key != "content_identity"}
        )
    ):
        raise ValueError("Blinded input schema or identity changed.")
    if len(blind["cases"]) != 9:
        raise ValueError("Blinded case population changed.")
    pairs: list[tuple[str, str, str]] = []
    resource_ids: set[str] = set()
    case_ids: set[str] = set()
    for case in blind["cases"]:
        if set(case) != {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        } or set(case["information_need"]) != {"purpose", "lexical_query"}:
            raise ValueError("Blinded case contains origin or unexpected fields.")
        if case["neutral_case_id"] in case_ids:
            raise ValueError("Blinded case identity repeats.")
        case_ids.add(case["neutral_case_id"])
        for resource in case["resources"]:
            if set(resource) != {"neutral_resource_id", "address", "content"}:
                raise ValueError(
                    "Blinded resource contains origin or unexpected fields."
                )
            resource_id = resource["neutral_resource_id"]
            if resource_id in resource_ids or not isinstance(resource["content"], str):
                raise ValueError(
                    "Blinded resource identity repeats or content is invalid."
                )
            resource_ids.add(resource_id)
            pairs.append((case["neutral_case_id"], resource_id, resource["address"]))
    if len(pairs) != EXPECTED_COUNT or set(DECISIONS) != resource_ids:
        raise ValueError("Blinded targets differ from the adjudicated twelve pairs.")
    return blind


def build_frozen_judgments(blind_path: Path) -> dict[str, Any]:
    """Serialize exactly twelve neutral, purpose-relative decisions."""
    blind = validate_blinded_input(blind_path)
    rows: list[dict[str, str]] = []
    for case in blind["cases"]:
        for resource in case["resources"]:
            label, rationale = DECISIONS[resource["neutral_resource_id"]]
            rows.append(
                {
                    "case_id": case["neutral_case_id"],
                    "resource_id": resource["neutral_resource_id"],
                    "address": resource["address"],
                    "judgment": label,
                    "rationale": rationale,
                }
            )
    rows.sort(key=lambda row: (row["case_id"], row["resource_id"]))
    population_identity = _digest(
        [
            {
                "case_id": row["case_id"],
                "resource_id": row["resource_id"],
                "address": row["address"],
            }
            for row in rows
        ]
    )
    payload = {
        "window_freeze_identity": FREEZE_IDENTITY,
        "blinded_input_identity": BLINDED_IDENTITY,
        "blinded_input_sha256": BLINDED_SHA256,
        "new_pair_population_identity": population_identity,
        "judgment_semantics": SEMANTICS,
        "judgments": rows,
        "provenance": {
            "method": "purpose-relative adjudication from committed blinded input only",
            "retrieval_evidence_joined": False,
        },
    }
    artifact = {
        "schema": "devtools-i27-window-unit-frozen-judgments-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }
    validate_frozen_judgments(blind, artifact)
    return artifact


def validate_frozen_judgments(blind: dict[str, Any], artifact: dict[str, Any]) -> None:
    """Reject incomplete labels, broken bindings, or retrieval evidence leakage."""
    if (
        set(artifact) != {"schema", "content_identity", "payload"}
        or artifact["schema"] != "devtools-i27-window-unit-frozen-judgments-v1"
    ):
        raise ValueError("Frozen judgment envelope changed.")
    payload = artifact["payload"]
    if set(payload) != {
        "window_freeze_identity",
        "blinded_input_identity",
        "blinded_input_sha256",
        "new_pair_population_identity",
        "judgment_semantics",
        "judgments",
        "provenance",
    } or artifact["content_identity"] != _digest(payload):
        raise ValueError("Frozen judgment identity or field boundary changed.")
    if (
        payload["window_freeze_identity"] != FREEZE_IDENTITY
        or payload["blinded_input_identity"] != BLINDED_IDENTITY
        or payload["blinded_input_sha256"] != BLINDED_SHA256
        or payload["judgment_semantics"] != SEMANTICS
        or payload["provenance"]
        != {
            "method": "purpose-relative adjudication from committed blinded input only",
            "retrieval_evidence_joined": False,
        }
    ):
        raise ValueError("Frozen judgment source binding or semantics changed.")
    expected = {
        (case["neutral_case_id"], resource["neutral_resource_id"], resource["address"])
        for case in blind["cases"]
        for resource in case["resources"]
    }
    rows = payload["judgments"]
    if len(rows) != EXPECTED_COUNT:
        raise ValueError("Frozen judgment count changed.")
    actual: list[tuple[str, str, str]] = []
    for row in rows:
        if (
            set(row) != {"case_id", "resource_id", "address", "judgment", "rationale"}
            or row["judgment"] not in LABELS
            or not isinstance(row["rationale"], str)
            or not row["rationale"].strip()
        ):
            raise ValueError(
                "Frozen judgment contains invalid label, rationale, or origin field."
            )
        actual.append((row["case_id"], row["resource_id"], row["address"]))
    if len(set(actual)) != EXPECTED_COUNT or set(actual) != expected:
        raise ValueError("Frozen judgments do not cover exact neutral targets once.")
    if payload["new_pair_population_identity"] != _digest(
        [
            {
                "case_id": row["case_id"],
                "resource_id": row["resource_id"],
                "address": row["address"],
            }
            for row in rows
        ]
    ):
        raise ValueError("Frozen new-pair population identity changed.")


def write_frozen_judgments(root: Path) -> dict[str, Any]:
    """Write the immutable blind judgment checkpoint without reading rankings."""
    path = root / "window_unit_frozen_judgments.json"
    value = build_frozen_judgments(root / "window_unit_blinded_judgment_input.json")
    if path.exists() and _read_json(path) != value:
        raise ValueError(
            "Existing window judgments differ from the blind decision set."
        )
    write_artifact(path=path, payload=value)
    return {
        "identity": value["content_identity"],
        "counts": dict(
            Counter(row["judgment"] for row in value["payload"]["judgments"])
        ),
    }
