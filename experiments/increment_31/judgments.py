# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Origin-blind decisions for the frozen Increment-31 neutral input."""

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
INPUT_NAME = "mirrored_test_paths_blinded_judgment_input.json"
OUTPUT_NAME = "mirrored_test_paths_frozen_judgments.json"
INPUT_IDENTITY = "64fb7e675d6d7d0b28e72af7ef5adb1a7bc20bfc384cf21dc5a781c1a5eb85d8"
INPUT_SHA256 = "968a8d32cfe852252a4a2fdeb2906059f4200e700829ddb02dd5ce9f39d296e3"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")

# These decisions concern only usefulness of the neutral parent-snapshot material.
DECISIONS: Mapping[str, tuple[str, str]] = {
    "resource-89c1f9e3e765252b": (
        "NOT_USEFUL",
        "Resource discovery lists bounded file addresses but provides no explicit-root Python module naming or package interpretation rules.",
    ),
    "resource-da7856baf3efacac": (
        "NOT_USEFUL",
        "The Markdown filesystem codec does not define repository text-document representation.",
    ),
    "resource-7fe0a8d26e70ec1e": (
        "USEFUL",
        "Bounded resource discovery supplies the canonical addresses and traversal limits needed before repository text resources can be observed.",
    ),
    "resource-b8a7a61ae8d8e96d": (
        "NOT_USEFUL",
        "Model-interaction Evidence does not parse Python source or derive direct function declarations.",
    ),
    "resource-3476f590c13826e1": (
        "USEFUL",
        "The protocol test shows the existing Prompt-to-ModelResponse request contract and continuation behavior that the request boundary must preserve.",
    ),
    "resource-4eb224cfb6e80a67": (
        "USEFUL",
        "This concrete model interaction maps a Prompt into a provider request and returns ModelResponse, showing the request boundary in use.",
    ),
    "resource-156bbe3ed9696657": (
        "NOT_USEFUL",
        "Text-file codec tests cover byte decoding and encoding, not model reasoning content.",
    ),
    "resource-5ddbe1653bd24832": (
        "NOT_USEFUL",
        "The generic send protocol names ModelResponse but provides no reasoning-content representation or handling behavior.",
    ),
    "resource-625cbf8584f86a91": (
        "NOT_USEFUL",
        "JSON filesystem codec tests do not define or validate reasoning content in model responses.",
    ),
    "resource-a67ab262543b235d": (
        "NOT_USEFUL",
        "Markdown filesystem codec tests do not address model reasoning content.",
    ),
    "resource-991d75ecbe4fb3a7": (
        "USEFUL",
        "The model invocation protocol is the existing send signature where an output-token bound would need to be represented.",
    ),
    "resource-4aa9e15bfe14f12d": (
        "USEFUL",
        "The llama.cpp interaction shows where request options enter send and become provider payload fields, which is material to adding thinking control.",
    ),
}


def build_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Bind one three-state decision to each verified neutral target."""
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
            identity = str(resource["neutral_resource_id"])
            if identity in seen or identity not in DECISIONS:
                raise ValueError("Neutral target is duplicate or lacks a decision.")
            seen.add(identity)
            state, rationale = DECISIONS[identity]
            if state not in STATES or not rationale.strip():
                raise ValueError("Judgment state or rationale is invalid.")
            records.append(
                {
                    "neutral_case_id": case["neutral_case_id"],
                    "information_need": case["information_need"],
                    "parent_snapshot_sha": case["parent_snapshot_sha"],
                    "neutral_resource_id": identity,
                    "address": resource["address"],
                    "usefulness_semantics": USEFULNESS_SEMANTICS,
                    "judgment": state,
                    "rationale": rationale,
                }
            )
    if len(records) != 12 or seen != set(DECISIONS):
        raise ValueError("Judgments do not cover exactly the frozen 12 targets.")
    counts = Counter(row["judgment"] for row in records)
    payload = {
        "schema": "devtools-i31-neutral-frozen-judgments-v1",
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
    """Persist all neutral decisions before opening candidate origins."""
    artifact = build_judgments(root)
    path = root / OUTPUT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Increment-31 frozen judgments differ.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    freeze_judgments()
