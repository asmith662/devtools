# Copyright (c) 2026
# ruff: noqa: T201, ASYNC240 -- bounded synthetic benchmark, never a scientific run
"""Measure the real-process fixture with temporary Git publication, never remote."""

from __future__ import annotations

import asyncio
import tempfile
import time
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.__main__ import adopt_completed
from experiments.orchestration.controller import Controller, implementation
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import exclusive
from experiments.orchestration.tests.test_controller import FixtureController, fixture


async def measured(controller: Controller) -> dict[str, Any]:
    """Keep timing descriptive; authenticate the complete fixture result."""
    start = time.perf_counter()
    result = await controller.run()
    if not result["status"].startswith("COMPLETE"):
        raise ValueError(str(result))
    elapsed = time.perf_counter() - start
    return {
        "elapsed_seconds": elapsed,
        "run_id": controller.run_id,
        "concurrency": controller.value["concurrency"],
        "publications": result["publications"],
        "cache": {
            case.identity: result["stages"][case.identity + "/prepare"]
            for case in controller.plan.cases
        },
        "branch_seconds": {
            key: value["duration_seconds"]
            for key, value in result["stages"].items()
            if key.endswith(("/B", "/C"))
        },
        "automatic_scientific_retries": 0,
        "verification": (await controller.verify())["verification"],
    }


async def main() -> None:
    """Retain engineering measurements; no treatment effectiveness or model call."""
    root = Path(tempfile.mkdtemp(prefix="devtools-controller-fixture-")).resolve()
    serial = await fixture(root / "serial", root / "serial-work", concurrency=1)
    parallel = await fixture(root / "parallel", root / "parallel-work", concurrency=6)
    serial_result = await measured(serial)
    parallel_result = await measured(parallel)
    value = parallel.plan.value
    value["attempt"] = 2
    plan = RunPlan.parse(value)
    (parallel.repository.root / "plan.json").write_bytes(plan.canonical)
    (parallel.repository.root / "approval.json").write_bytes(
        json_bytes(
            {
                "approved": True,
                "stage_a_checkpoint": value["stage_a"]["checkpoint"],
                "plan_sha256": digest(plan.canonical),
            },
        ),
    )
    await parallel.repository.git("add", "plan.json", "approval.json")
    await parallel.repository.git(
        "commit",
        "-m",
        "Approve second fake cache measurement",
    )
    cached = await FixtureController.from_plan(
        parallel.repository.root,
        "plan.json",
        parallel.work_root,
    )
    cached_result = await measured(cached)
    repo_root = Path(__file__).resolve().parents[3]
    output = {
        "scope": "SYNTHETIC_ENGINEERING_ONLY_NO_PROSPECTIVE_EFFECTIVENESS_CLAIM",
        "controller_implementation": implementation(),
        "host": "Windows; Python fake workers; temporary Git; no remote/model",
        "sample_count_per_configuration": 1,
        "serial_cold": serial_result,
        "parallel_cold": parallel_result,
        "parallel_cache_hit": cached_result,
        "read_only_adoption": await adopt_completed(repo_root),
        "live_models": 0,
        "scientific_treatments": 0,
        "historical_deep_replays": 0,
        "retained_fixture_root": str(root),
    }
    destination = repo_root / "experiments/orchestration/engineering/measurements.json"
    exclusive(destination, output)
    print(
        json_bytes(
            {
                "measurement": str(destination),
                "seconds": {
                    "serial_cold": serial_result["elapsed_seconds"],
                    "parallel_cold": parallel_result["elapsed_seconds"],
                    "parallel_cache_hit": cached_result["elapsed_seconds"],
                },
            },
        ).decode(),
    )


if __name__ == "__main__":
    asyncio.run(main())
