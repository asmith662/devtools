# Copyright (c) 2026
# ruff: noqa: ANN401, T201, E501 -- explicitly non-authoritative controller observability
"""Summarize retained operational timings; never determine scientific validity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import ROOT
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import load, save


def summarize(events: list[Any]) -> Any:
    """Retain complete intervals and explicit missingness without estimating costs."""
    workers = {}
    branches = {}
    for stage in ("B", "C"):
        starts: dict[str, float] = {}
        ends = {}
        for event in events:
            if event["stage"] != stage:
                continue
            case = event["case"]
            if event["status"] == "RUNNING":
                starts.setdefault(case, event["elapsed_seconds"])
            if event["status"] == "COMPLETE":
                ends[case] = event["elapsed_seconds"]
                workers[case + "/" + stage] = event.get("duration_seconds")
        branches[stage] = (
            max(ends.values()) - min(starts.values())
            if starts and set(starts) == set(ends)
            else None
        )
    return {
        "authority": "OPERATIONAL_ONLY_NOT_SCIENTIFIC_AUTHORITY",
        "worker_seconds": workers,
        "branch_critical_path_seconds": branches,
        "controller_elapsed_seconds": max(
            (e["elapsed_seconds"] for e in events),
            default=None,
        ),
        "controller_complete": any(
            e["stage"] == "run" and e["status"].startswith("COMPLETE") for e in events
        ),
        "limitations": "Local logs are replaceable and can be missing; never authorize, validate or change scientific categories from these timings. A FINAL-boundary snapshot excludes later push/finalization; rerun the same non-scientific summary after completion for full wall time.",
    }


def main() -> None:
    """Compute observability only, including during FINAL validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plan",
        type=Path,
        default=ROOT / "experiments/source_grounding/plans/run-plan.json",
    )
    args = parser.parse_args()
    plan = RunPlan.parse(load(args.plan))
    identity = plan.identity(plan.value["controller_implementation"])
    root = ROOT / ".local/experiment-runs" / identity
    path = root / "progress.log"
    events = (
        [json.loads(line) for line in path.read_bytes().splitlines()]
        if path.exists()
        else []
    )
    result = {"run_id": identity, **summarize(events)}
    save(root / "timing_summary.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
