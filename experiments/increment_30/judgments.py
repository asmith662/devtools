# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Origin-blind judgments for the frozen Increment-30 neutral input."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest

if TYPE_CHECKING:
    from collections.abc import Mapping

ROOT = Path(__file__).resolve().parent
INPUT_NAME = "package_containment_blinded_judgment_input.json"
OUTPUT_NAME = "package_containment_frozen_judgments.json"
INPUT_IDENTITY = "58efd8c4c506a770eb7afed00df3214e4a239be25bd2d84210cd035e53b605f7"
INPUT_SHA256 = "7ea5664fd8ed90216b9f60e5afb16453e3cc0e6caf94452ce927c24caf8ba244"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")

# The IDs and rationales below were assigned from the verified neutral input only.
DECISIONS: Mapping[str, tuple[str, str]] = {
    "resource-5c0d0594fc1a72fe": (
        "NOT_USEFUL",
        "Only labels the Tool test package; it gives no behavior or tests for the model-native Tool boundary.",
    ),
    "resource-3ce7366efd125c98": (
        "NOT_USEFUL",
        "Only labels provider tests; it gives no request-boundary implementation or test behavior.",
    ),
    "resource-6fe731bcb1ac7f76": (
        "NOT_USEFUL",
        "Only labels Context tests; it gives no resource-discovery behavior or constraints.",
    ),
    "resource-46eb23d0e9e9a128": (
        "NOT_USEFUL",
        "Only labels import-declaration tests; it gives no explicit-root module interpretation behavior.",
    ),
    "resource-90d2e6cfab445ee6": (
        "NOT_USEFUL",
        "Only labels Repository Context tests; it gives no module interpretation rules or examples.",
    ),
    "resource-79fe621fc5ac2bd3": (
        "NOT_USEFUL",
        "Only labels Context tests; it gives no declaration aggregation logic or cases.",
    ),
    "resource-8469e86b314b05ed": (
        "NOT_USEFUL",
        "Only labels benchmark infrastructure and exports nothing; it gives no model usage measurement behavior.",
    ),
    "resource-da38f9a7ab417c0c": (
        "NOT_USEFUL",
        "Only labels conversation-message tests; it gives no Repository Context discovery material.",
    ),
    "resource-2a0b11cfa780e597": (
        "NOT_USEFUL",
        "Only labels benchmark tests; it gives no repository snapshot observation behavior.",
    ),
    "resource-f7fb169df9f046af": (
        "NOT_USEFUL",
        "Only labels model-serving tests; it gives no repository snapshot observation behavior.",
    ),
    "resource-5e6cdac0fc1c9960": (
        "NOT_USEFUL",
        "Only labels Context tests; it gives no function source materialization logic or cases.",
    ),
    "resource-52ffa72dbe5614a4": (
        "NOT_USEFUL",
        "Only labels Qwen experiment tests; it gives no selection-stress fixture behavior.",
    ),
    "resource-9eee937e91b32229": (
        "NOT_USEFUL",
        "Only gives a general project description; it gives no selection-stress fixture behavior.",
    ),
    "resource-116356e81c612915": (
        "NOT_USEFUL",
        "Only labels provider tests; it gives no thinking-control implementation or test cases.",
    ),
    "resource-ac18fe2db363464f": (
        "NOT_USEFUL",
        "Only labels execution-domain tests; it gives no model interaction thinking-control behavior.",
    ),
    "resource-72dbecef5e038663": (
        "NOT_USEFUL",
        "Only labels filesystem codec tests; it gives no repository text document representation behavior.",
    ),
    "resource-9f632ee858263d90": (
        "NOT_USEFUL",
        "Only labels evidence tests; it gives no direct Python function declaration derivation behavior.",
    ),
    "resource-0083a3f65199f16d": (
        "NOT_USEFUL",
        "Only labels Context tests; it gives no explicit-resource declaration derivation behavior.",
    ),
    "resource-56bf5fd59e093eba": (
        "NOT_USEFUL",
        "Only labels model-interaction tests; it gives no reasoning-content implementation or cases.",
    ),
    "resource-b158a328f1554c5c": (
        "NOT_USEFUL",
        "Only labels Context tests; it gives no exact-name function resource selection behavior.",
    ),
}


def build_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Bind exactly one decision to each verified neutral target."""
    input_path = root / INPUT_NAME
    blind = cast("dict[str, Any]", _read_json(input_path))
    if (
        blind["content_identity"] != INPUT_IDENTITY
        or sha256_file(input_path) != INPUT_SHA256
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
                    "usefulness_semantics": USEFULNESS_SEMANTICS,
                    "judgment": state,
                    "rationale": rationale,
                }
            )
    if len(records) != 20 or seen != set(DECISIONS):
        raise ValueError("Judgments do not exactly cover the frozen 20 targets.")
    counts = Counter(row["judgment"] for row in records)
    payload = {
        "schema": "devtools-i30-neutral-frozen-judgments-v1",
        "blinded_input_content_identity": INPUT_IDENTITY,
        "blinded_input_sha256": INPUT_SHA256,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
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
    """Persist the neutral decisions before any candidate-origin join."""
    artifact = build_judgments(root)
    path = root / OUTPUT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Increment-30 frozen judgments differ.")
    write_artifact(path=path, payload=artifact)
    return artifact
