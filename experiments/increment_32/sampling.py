# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, S311, TRY003
"""Prospectively frozen simple random sample of neutral Graph-1 targets."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.mechanics import ROOT
from experiments.increment_32.population import BLINDED_NAME
from experiments.retrieval_judgment_coverage import validate_neutral_target_coverage

if TYPE_CHECKING:
    from pathlib import Path

SAMPLE_SIZE = 128
POPULATION_SIZE = 702
SEED = 320128
FREEZE_NAME = "graph_round_one_sampling_freeze.json"
SAMPLED_INPUT_NAME = "graph_round_one_sampled_blinded_judgment_input.json"
SOURCE_IDENTITY = "ec6896c208ad0dcadd698e6cd97235c3efcb065110466b19b6ef638beb2a1362"
SOURCE_SHA256 = "2721f737aff1bc0d266f767dcbb49ab623bc1b2d7c19c05aec4ef55a89b603b9"


def build_sample(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Select 128 neutral identities uniformly without reading outcomes."""
    source_path = root / BLINDED_NAME
    source = _verified_json(source_path)
    if (
        source["content_identity"] != SOURCE_IDENTITY
        or sha256_file(source_path) != SOURCE_SHA256
        or source["payload"]["schema"] != "devtools-neutral-resource-judgment-input-v1"
    ):
        raise ValueError("Frozen Graph-1 neutral sampling frame differs.")
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
        raise ValueError("Sampling frame contains non-neutral fields.")
    targets: list[dict[str, Any]] = [
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
    indexed = validate_neutral_target_coverage(targets)
    ordered = sorted(indexed)
    if len(ordered) != POPULATION_SIZE:
        raise ValueError("Graph-1 neutral sampling frame is not 702 distinct targets.")
    selected = set(random.Random(SEED).sample(ordered, SAMPLE_SIZE))
    sampled_ids = sorted(selected)
    unsampled_ids = [identity for identity in ordered if identity not in selected]
    sampled_cases: list[dict[str, Any]] = []
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
    sampled_payload = {
        "schema": "devtools-neutral-resource-judgment-input-v1",
        "cases": sampled_cases,
    }
    sampled_input = {
        "schema": sampled_payload["schema"],
        "content_identity": _digest(sampled_payload),
        "payload": sampled_payload,
    }
    payload = {
        "source_neutral_input_content_identity": SOURCE_IDENTITY,
        "source_neutral_input_sha256": SOURCE_SHA256,
        "population_size": POPULATION_SIZE,
        "sampling_method": "simple-random-sampling-without-replacement",
        "sample_size": SAMPLE_SIZE,
        "random_generator": "python-random.Random.sample",
        "seed": SEED,
        "canonical_order": "lexicographically sorted (neutral_case_id, neutral_resource_id) tuples",
        "sampled_neutral_identities": [list(identity) for identity in sampled_ids],
        "unsampled_neutral_identities": [list(identity) for identity in unsampled_ids],
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "sampled_input_content_identity": sampled_input["content_identity"],
        "outcomes_accessed_before_freeze": False,
        "candidate_population_changed": False,
        "confirmation_executed": False,
    }
    freeze = {
        "schema": "devtools-i32-graph-round-one-sampling-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }
    return freeze, sampled_input


def write_sample(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist immutable sampling identities and the neutral sampled input."""
    freeze, sampled_input = build_sample(root)
    for name, artifact in ((FREEZE_NAME, freeze), (SAMPLED_INPUT_NAME, sampled_input)):
        path = root / name
        if path.exists() and _read_json(path) != artifact:
            raise ValueError("An existing Graph-1 sample differs from the protocol.")
        write_artifact(path=path, payload=artifact)
    return freeze, sampled_input


if __name__ == "__main__":
    write_sample()
