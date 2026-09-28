# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003
"""Mechanical development join after blinded Graph-2 judgment freeze."""

from __future__ import annotations

from collections import Counter
from math import sqrt
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_33.judgments import (
    FROZEN_NAME,
    build_judgments,
    sampled_targets,
)
from experiments.increment_33.mechanics import CANDIDATES_NAME, ROOT
from experiments.increment_33.population import JUDGMENT_FREEZE_NAME, STATES
from experiments.increment_33.sampling import FREEZE_NAME as SAMPLING_NAME
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_frozen_judgment_coverage,
    validated_outcome_mappings,
)

if TYPE_CHECKING:
    from pathlib import Path

RESULT_NAME = "graph_round_two_development_results.json"


def wilson_95(useful: int, sampled: int) -> dict[str, float | str | bool]:
    """Describe a sampled proportion with an approximate Wilson 95% interval."""
    if sampled <= 0 or useful < 0 or useful > sampled:
        raise ValueError("Invalid sampled useful count.")
    z = 1.959963984540054
    p = useful / sampled
    denominator = 1 + z * z / sampled
    center = (p + z * z / (2 * sampled)) / denominator
    half_width = (
        z * sqrt(p * (1 - p) / sampled + z * z / (4 * sampled * sampled)) / denominator
    )
    return {
        "method": "95% Wilson score interval, binomial approximation",
        "finite_population_correction_applied": False,
        "observed_useful_fraction": p,
        "lower": max(0.0, center - half_width),
        "upper": min(1.0, center + half_width),
    }


def build_result(root: Path = ROOT) -> dict[str, Any]:
    """Validate frozen decisions first, then join complete Graph-2 candidates."""
    judgment_path = root / FROZEN_NAME
    sampled = _verified_json(judgment_path)
    if sampled != build_judgments(sampled["payload"]["decisions"], root):
        raise ValueError("Graph-2 sampled decisions are not frozen exactly.")
    targets = sampled_targets(root)
    sampling = _verified_json(root / SAMPLING_NAME)
    selected = {
        tuple(identity)
        for identity in sampling["payload"]["sampled_neutral_identities"]
    }
    decisions = validate_frozen_judgment_coverage(
        targets, sampled["payload"]["decisions"], STATES, selected
    )
    population = _verified_json(root / JUDGMENT_FREEZE_NAME)
    reused, newly_judged = validated_outcome_mappings(
        population["payload"]["reused_judgments"], decisions
    )
    unresolved = {
        judgment_identity(row): row
        for row in population["payload"]["new_judgment_pairs"]
    }
    if len(unresolved) != sampling["payload"]["population_size"] or set(
        newly_judged
    ) - set(unresolved):
        raise ValueError("Sampled outcomes differ from unresolved Graph-2 frame.")
    # Candidate provenance is first read only after the judgment freeze validates.
    mechanics_path = root / CANDIDATES_NAME
    mechanics = _verified_json(mechanics_path)
    if (
        mechanics["content_identity"] != population["payload"]["candidate_identity"]
        or sha256_file(mechanics_path) != population["payload"]["candidate_sha256"]
        or mechanics["judgments_loaded"]
        or mechanics["heldout_executed"]
    ):
        raise ValueError("Frozen candidate surface differs after decisions.")
    joined: list[dict[str, Any]] = []
    sources: Counter[str] = Counter()
    for case in mechanics["cases"]:
        for candidate in case["candidates"]:
            row = {
                "case_id": case["case_id"],
                "information_need": case["information_need"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": candidate["address"],
                "usefulness_semantics": population["payload"]["usefulness_semantics"],
            }
            identity = judgment_identity(row)
            if identity in reused:
                row.update(
                    {
                        "population": "exact_reused_judged",
                        "judgment": reused[identity]["judgment"],
                    }
                )
            elif identity in newly_judged:
                row.update(
                    {
                        "population": "sampled_newly_judged",
                        "judgment": newly_judged[identity]["judgment"],
                    }
                )
            elif identity in unresolved:
                row["population"] = "unsampled_unadjudicated"
            else:
                raise ValueError("Graph-2 candidate escaped judgment population.")
            sources[str(row["population"])] += 1
            joined.append(row)
    if (
        len(joined) != mechanics["summary"]["candidate_count"]
        or len({judgment_identity(row) for row in joined}) != len(joined)
        or sources["exact_reused_judged"] != len(reused)
        or sources["sampled_newly_judged"] != len(newly_judged)
        or sources["unsampled_unadjudicated"] != len(unresolved) - len(newly_judged)
    ):
        raise ValueError("Graph-2 result population partition differs.")
    counts = sampled["payload"]["counts"]
    useful = counts["USEFUL"]
    payload = {
        "development_case_ids": [case["case_id"] for case in mechanics["cases"]],
        "candidate_content_identity": mechanics["content_identity"],
        "candidate_sha256": sha256_file(mechanics_path),
        "sampling_freeze_identity": sampling["content_identity"],
        "sampled_judgments_identity": sampled["content_identity"],
        "sampled_judgments_sha256": sha256_file(judgment_path),
        "prior_judgment_freeze_identity": population["content_identity"],
        "complete_candidate_summary": mechanics["summary"],
        "population_counts": dict(sorted(sources.items())),
        "reused_outcome_counts": population["payload"]["counts"]["reused_states"],
        "sampled_outcome_counts": counts,
        "sampled_useful_interval": wilson_95(useful, len(newly_judged)),
        "joined_pairs": joined,
        "breadth_verdict": "No useful Graph-2 candidate was observed in the frozen 128-target probability sample; useful complementary reach is not established, and absence from the complete 987-pair surface is not established.",
        "unsampled_pairs_have_no_outcome": True,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i33-graph-round-two-development-results-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_result(root: Path = ROOT) -> dict[str, Any]:
    """Persist the exact development join without changing frozen surfaces."""
    artifact = build_result(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Graph-2 development result differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    write_result()
