# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003
"""Freeze blinded Graph-2 sample decisions before structural origin join."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_33.mechanics import ROOT
from experiments.increment_33.population import JUDGMENT_FREEZE_NAME, STATES
from experiments.increment_33.sampling import FREEZE_NAME, SAMPLED_INPUT_NAME
from experiments.retrieval_judgment_coverage import (
    validate_frozen_judgment_coverage,
    validated_outcome_mappings,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

FROZEN_NAME = "graph_round_two_sampled_frozen_judgments.json"


def sampled_targets(root: Path = ROOT) -> list[dict[str, Any]]:
    """Flatten only the frozen neutral sampled input into exact judgment targets."""
    sample_path = root / SAMPLED_INPUT_NAME
    sample = _verified_json(sample_path)
    sampling = _verified_json(root / FREEZE_NAME)
    if (
        sample["content_identity"]
        != sampling["payload"]["sampled_input_content_identity"]
    ):
        raise ValueError("Graph-2 sampled input identity differs.")
    return [
        {
            "neutral_case_id": case["neutral_case_id"],
            "neutral_resource_id": resource["neutral_resource_id"],
            "information_need": case["information_need"],
            "parent_snapshot_sha": case["parent_snapshot_sha"],
            "address": resource["address"],
            "usefulness_semantics": USEFULNESS_SEMANTICS,
        }
        for case in sample["payload"]["cases"]
        for resource in case["resources"]
    ]


def build_judgments(
    decisions: Sequence[dict[str, Any]], root: Path = ROOT
) -> dict[str, Any]:
    """Validate all blinded decisions and bind them to the frozen sample."""
    sampling_path = root / FREEZE_NAME
    sample_path = root / SAMPLED_INPUT_NAME
    sampling = _verified_json(sampling_path)
    sample = _verified_json(sample_path)
    prior = _verified_json(root / JUDGMENT_FREEZE_NAME)
    targets = sampled_targets(root)
    expected = {
        tuple(identity)
        for identity in sampling["payload"]["sampled_neutral_identities"]
    }
    if len(targets) != sampling["payload"]["sample_size"]:
        raise ValueError("Graph-2 sampled target count differs.")
    outcomes = validate_frozen_judgment_coverage(targets, decisions, STATES, expected)
    validated_outcome_mappings(prior["payload"]["reused_judgments"], outcomes)
    counts = Counter(row["judgment"] for row in decisions)
    payload = {
        "sampling_freeze_identity": sampling["content_identity"],
        "sampling_freeze_sha256": sha256_file(sampling_path),
        "sampled_input_identity": sample["content_identity"],
        "sampled_input_sha256": sha256_file(sample_path),
        "complete_unresolved_neutral_input_identity": sampling["payload"][
            "source_neutral_input_content_identity"
        ],
        "sample_size": len(targets),
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "states": list(STATES),
        "counts": {state: counts[state] for state in STATES},
        "decisions": list(decisions),
        "provenance_inspected_before_freeze": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i33-graph-round-two-sampled-judgments-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_judgments(
    decisions: Sequence[dict[str, Any]], root: Path = ROOT
) -> dict[str, Any]:
    """Persist exact sampled outcomes only after coverage validation."""
    artifact = build_judgments(decisions, root)
    path = root / FROZEN_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Graph-2 sampled judgments differ.")
    write_artifact(path=path, payload=artifact)
    return artifact
