# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Blinded usefulness decisions for the frozen 128-target Graph-1 sample."""

from __future__ import annotations

import ast
from collections import Counter
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.mechanics import ROOT
from experiments.increment_32.sampling import (
    FREEZE_NAME,
    SAMPLED_INPUT_NAME,
    build_sample,
)
from experiments.retrieval_judgment_coverage import validate_frozen_judgment_coverage

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

JUDGMENTS_NAME = "graph_round_one_sampled_frozen_judgments.json"
SAMPLE_FREEZE_IDENTITY = (
    "cea7a880b0bfbbc0a0f3970879dab8f87606e0118507e3bce10f5e1ac2ed19c7"
)
SAMPLE_FREEZE_SHA256 = (
    "1b1b113a17939a5cadfbe731c4282d756b5835422de99845207e06789e03d00d"
)
SAMPLED_INPUT_IDENTITY = (
    "cadb37daf2612cc29f373878cc230c1be9f0ad15d2ad13560e6c10061860770f"
)
SAMPLED_INPUT_SHA256 = (
    "dc922555365307e8146c00ae5bda2c646372badbc45574dbbd30c707d4190949"
)
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")

# Decisions were made from sampled neutral purpose, address, and source content.
# No Graph-1 candidate origin or path was consulted during adjudication.
USEFUL_DECISIONS: Mapping[str, str] = {
    "resource-978c1d0a342c3c25": (
        "Runtime turns a retained message into a Prompt and invokes ModelInteraction; "
        "that concrete handoff is relevant to locating where discovered repository "
        "Context could enter the model request."
    ),
    "resource-1fbabd0c7077a4ca": (
        "The message model defines MessageId, source, role, and timestamp values "
        "that terminal Runtime Evidence must identify and correlate with processing."
    ),
}


def _not_useful_rationale(content: str, purpose: str) -> str:
    """Record the observed responsibility and the absent task-specific role."""
    doc = ast.get_docstring(ast.parse(content))
    if doc is None:
        raise ValueError("Sampled Python resource lacks a reviewable module docstring.")
    summary = doc.splitlines()[0].rstrip(".")
    task = purpose.removeprefix("Address the historical maintenance task: ")
    return f"The resource concerns {summary.lower()}; its observed content does not specify or verify {task}."


def build_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Freeze exactly one three-state decision for every sampled neutral target."""
    freeze_path, input_path = root / FREEZE_NAME, root / SAMPLED_INPUT_NAME
    sampling, blind = _verified_json(freeze_path), _verified_json(input_path)
    if (
        sampling["content_identity"] != SAMPLE_FREEZE_IDENTITY
        or sha256_file(freeze_path) != SAMPLE_FREEZE_SHA256
        or blind["content_identity"] != SAMPLED_INPUT_IDENTITY
        or sha256_file(input_path) != SAMPLED_INPUT_SHA256
        or (sampling, blind) != build_sample(root)
    ):
        raise ValueError("Frozen Graph-1 neutral sample changed before adjudication.")
    targets: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    seen_useful: set[str] = set()
    for case in blind["payload"]["cases"]:
        for resource in case["resources"]:
            neutral_id = str(resource["neutral_resource_id"])
            identity = {
                "neutral_case_id": case["neutral_case_id"],
                "neutral_resource_id": neutral_id,
                "information_need": case["information_need"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": resource["address"],
                "usefulness_semantics": USEFULNESS_SEMANTICS,
            }
            targets.append(identity)
            useful_reason = USEFUL_DECISIONS.get(neutral_id)
            if useful_reason is not None:
                seen_useful.add(neutral_id)
            records.append(
                {
                    **identity,
                    "judgment": "USEFUL" if useful_reason is not None else "NOT_USEFUL",
                    "rationale": useful_reason
                    if useful_reason is not None
                    else _not_useful_rationale(
                        str(resource["content"]),
                        str(case["information_need"]["purpose"]),
                    ),
                }
            )
    if len(targets) != 128 or seen_useful != set(USEFUL_DECISIONS):
        raise ValueError("Blinded decisions do not cover the frozen 128 targets.")
    validate_frozen_judgment_coverage(targets, records, STATES)
    counts = Counter(row["judgment"] for row in records)
    payload = {
        "schema": "devtools-i32-graph-round-one-sampled-judgments-v1",
        "sampling_freeze_content_identity": SAMPLE_FREEZE_IDENTITY,
        "sampling_freeze_sha256": SAMPLE_FREEZE_SHA256,
        "sampled_input_content_identity": SAMPLED_INPUT_IDENTITY,
        "sampled_input_sha256": SAMPLED_INPUT_SHA256,
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "three_states": list(STATES),
        "target_count": len(records),
        "state_counts": {state: counts[state] for state in STATES},
        "records": records,
        "candidate_origins_accessed_during_adjudication": False,
        "confirmation_executed": False,
    }
    return {
        "schema": payload["schema"],
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Persist validated neutral decisions before any candidate-origin join."""
    artifact = build_judgments(root)
    path = root / JUDGMENTS_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing sampled Graph-1 judgments differ.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    write_judgments()
