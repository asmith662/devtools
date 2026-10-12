# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, PLR2004, T201
"""Validate performance artifacts and bindings without scientific full replay."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import ROOT, json_bytes
from experiments.performance.retrieval.benchmark import PACKAGE
from experiments.performance.retrieval.measurement import CATEGORIES, summary
from experiments.performance.retrieval.workload import read_json, sha


def validate_samples(result: Any) -> None:
    """Require raw sample/summary/category agreement and frozen benchmark policy."""
    for name, row in result["measurements"].items():
        if row["category"] not in CATEGORIES or row["summary"] != summary(
            row["samples_ns"],
        ):
            raise ValueError("Sample/category mismatch: " + name)
        if row["category"] == "ONLINE_QUERY" and (
            row["warmup"] < 10 or len(row["samples_ns"]) < 50
        ):
            raise ValueError("Online repetition policy: " + name)
    if result["configuration"]["bm25"] != {
        "k1": 1.2,
        "b": 0.75,
        "filename_weight": 0.25,
    }:
        raise ValueError("Canonical BM25 settings differ")
    if result["configuration"]["ppr"] != {
        "damping": 0.85,
        "tolerance": 1e-10,
        "maximum_iterations": 200,
        "initial": "personalization",
        "dangling": "personalization",
    }:
        raise ValueError("Frozen kernel settings differ")
    if result["configuration"]["rrf"] != {"k": 60, "weights": [1, 1]}:
        raise ValueError("Frozen RRF settings differ")


def verify() -> dict[str, str]:  # noqa: C901 -- independent bounded artifact checks
    """Check publication/current function bytes; do not rerun expensive benchmarks."""
    result = read_json(PACKAGE / "results.json")
    validate_samples(result)
    if json_bytes(result) != (PACKAGE / "results.json").read_bytes():
        raise ValueError("Unstable result JSON")
    for name, expected in result["implementation_sha256"].items():
        if sha((ROOT / name).read_bytes()) != expected:
            raise ValueError("Implementation binding differs: " + name)
    for i in range(1, 7):
        row = result["validation"][f"Q{i}"]
        if (
            any(row[k] != "EXACT" for k in ("A_order", "B_order", "C_order"))
            or row["stationary_max_abs_error"] > row["stationary_tolerance"]
        ):
            raise ValueError("Frozen output equivalence missing")
    supplement = read_json(PACKAGE / "supplement.json")
    for name, row in supplement["measurements"].items():
        if (
            row["summary"] != summary(row["samples_ns"])
            or row["category"] not in CATEGORIES
        ):
            raise ValueError("Supplement samples: " + name)
    profile = read_json(PACKAGE / "stage_d_profile.json")
    if (
        profile["full_stage_d_verify"] != "NOT_RUN"
        or profile["gold_join"] != "NOT_PERFORMED"
        or profile["gate_evaluation"] != "NOT_PERFORMED"
    ):
        raise ValueError("Profiler exceeded engineering scope")
    manifest = read_json(PACKAGE / "integrity.json")
    for name, expected in manifest["sha256"].items():
        if sha((PACKAGE / name).read_bytes()) != expected:
            raise ValueError("Performance artifact differs: " + name)
    return {
        "status": "PASS",
        "sample_policy": "PASS",
        "frozen_output_equivalence": "PASS",
        "current_implementation_bindings": "PASS",
        "stable_json": "PASS",
        "engineering_scope": "PASS",
        "physical_artifact_hashes": "PASS",
    }


if __name__ == "__main__":
    print(verify())
