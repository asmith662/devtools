# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, S311, TRY003
"""Prospective simple random sample of frozen neutral Graph-2 targets."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_33.mechanics import ROOT
from experiments.increment_33.population import BLINDED_NAME, JUDGMENT_FREEZE_NAME
from experiments.retrieval_judgment_coverage import validate_neutral_target_coverage

if TYPE_CHECKING:
    from pathlib import Path

SAMPLE_SIZE = 128
SEED = 330128
FREEZE_NAME = "graph_round_two_sampling_freeze.json"
SAMPLED_INPUT_NAME = "graph_round_two_sampled_blinded_judgment_input.json"


def build_sample(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Select neutral identities uniformly after complete candidate freeze."""
    source_path = root / BLINDED_NAME
    source = _verified_json(source_path)
    judgment_freeze = _verified_json(root / JUDGMENT_FREEZE_NAME)
    if (
        source["content_identity"]
        != judgment_freeze["payload"]["blinded_input_identity"]
        or source["payload"]["schema"] != "devtools-neutral-resource-judgment-input-v1"
        or judgment_freeze["payload"]["new_usefulness_outcomes"]
    ):
        raise ValueError("Graph-2 neutral sampling frame differs.")
    cases = source["payload"]["cases"]
    if any(
        set(case)
        != {"neutral_case_id", "information_need", "parent_snapshot_sha", "resources"}
        or any(
            set(resource) != {"neutral_resource_id", "address", "content"}
            for resource in case["resources"]
        )
        for case in cases
    ):
        raise ValueError("Sampling frame contains structural or outcome fields.")
    targets = [
        {
            "neutral_case_id": case["neutral_case_id"],
            "neutral_resource_id": resource["neutral_resource_id"],
            "information_need": case["information_need"],
            "parent_snapshot_sha": case["parent_snapshot_sha"],
            "address": resource["address"],
            "usefulness_semantics": USEFULNESS_SEMANTICS,
        }
        for case in cases
        for resource in case["resources"]
    ]
    ordered = sorted(validate_neutral_target_coverage(targets))
    if (
        len(ordered) != judgment_freeze["payload"]["counts"]["new_judgments_required"]
        or len(ordered) <= SAMPLE_SIZE
    ):
        raise ValueError("Graph-2 unresolved frame is not a large complete population.")
    selected = set(random.Random(SEED).sample(ordered, SAMPLE_SIZE))
    sampled_cases = []
    for case in cases:
        resources = [
            resource
            for resource in case["resources"]
            if (case["neutral_case_id"], resource["neutral_resource_id"]) in selected
        ]
        if resources:
            sampled_cases.append(
                {
                    "neutral_case_id": case["neutral_case_id"],
                    "information_need": case["information_need"],
                    "parent_snapshot_sha": case["parent_snapshot_sha"],
                    "resources": resources,
                }
            )
    sample_payload = {
        "schema": "devtools-neutral-resource-judgment-input-v1",
        "cases": sampled_cases,
    }
    sample = {
        "schema": sample_payload["schema"],
        "content_identity": _digest(sample_payload),
        "payload": sample_payload,
    }
    freeze_payload = {
        "source_neutral_input_content_identity": source["content_identity"],
        "source_neutral_input_sha256": sha256_file(source_path),
        "candidate_population_identity": judgment_freeze["payload"][
            "candidate_identity"
        ],
        "population_size": len(ordered),
        "sampling_method": "simple-random-sampling-without-replacement",
        "sample_size": SAMPLE_SIZE,
        "random_generator": "python-random.Random.sample",
        "seed": SEED,
        "canonical_order": "lexicographically sorted (neutral_case_id, neutral_resource_id) tuples",
        "sampled_neutral_identities": [list(identity) for identity in sorted(selected)],
        "unsampled_neutral_identities": [
            list(identity) for identity in ordered if identity not in selected
        ],
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "sampled_input_content_identity": sample["content_identity"],
        "outcomes_accessed_before_freeze": False,
        "candidate_population_changed": False,
        "confirmation_executed": False,
    }
    freeze = {
        "schema": "devtools-i33-graph-round-two-sampling-freeze-v1",
        "content_identity": _digest(freeze_payload),
        "payload": freeze_payload,
    }
    return freeze, sample


def write_sample(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist exact neutral sample identities and the blinded input."""
    freeze, sample = build_sample(root)
    for name, artifact in ((FREEZE_NAME, freeze), (SAMPLED_INPUT_NAME, sample)):
        path = root / name
        if path.exists() and _read_json(path) != artifact:
            raise ValueError("Existing Graph-2 sample differs from frozen protocol.")
        write_artifact(path=path, payload=artifact)
    return freeze, sample


if __name__ == "__main__":
    write_sample()
