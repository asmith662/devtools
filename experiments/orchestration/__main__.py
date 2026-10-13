# Copyright (c) 2026
# ruff: noqa: T201, PLC0415, ASYNC240 -- human operator CLI
"""Plan/run/resume/status/verify approved experiment cohorts."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

from experiments.orchestration.controller import Controller, implementation
from experiments.orchestration.model import RunPlan
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import load, require, safe


async def adopt_completed(root: Path) -> dict[str, object]:
    """Audit completed 0017-0019 without execution or deep replay."""
    from experiments.structural_discrimination.post_hoc.source_quality.execute import (
        CHECKPOINT,
    )
    from experiments.structural_discrimination.stage_d.analyze import run

    require(
        root == Path(__file__).resolve().parents[2],
        "Adoption is scoped to this exact repository",
    )
    receipt = await run("verify", CHECKPOINT)
    return {
        "mode": "READ_ONLY_ADOPTION",
        "Stage_A": "COMPLETE/AUTHENTICATED",
        "cases": {
            c: {
                "packet": "COMPLETE/FROZEN",
                "Stage_B": "COMPLETE/SEALED",
                "Stage_C": "IMPORTED",
                "Stage_D": "COMPLETE",
            }
            for c in ("0017", "0018", "0019")
        },
        "verification": receipt,
        "scientific_executions": 0,
        "deep_replays": 0,
    }


async def main() -> None:
    """Offer machine-readable results and one-line progress summaries."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("plan", "run", "resume", "status", "verify", "adopt"),
    )
    parser.add_argument("identity", nargs="?")
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--work-root", type=Path)
    args = parser.parse_args()
    root = args.repository.resolve()
    result: Any
    if args.command == "adopt":
        result = await adopt_completed(root)
    elif args.command in {"plan", "run"}:
        require(
            args.identity is not None and args.work_root is not None,
            "Plan address and separate --work-root required",
        )
        controller = await Controller.from_plan(
            root,
            args.identity,
            args.work_root.resolve(),
        )
        result = (
            {
                "run_id": controller.run_id,
                "Stage_A": "AUTHENTICATED/APPROVED",
                "cases": [c.identity for c in controller.plan.cases],
                "concurrency": controller.value["concurrency"],
            }
            if args.command == "plan"
            else await controller.run()
        )
    else:
        require(args.identity is not None, "Run identity required")
        prefix = "experiments/orchestration/runs/" + args.identity
        # Published plan roots can be located through the operational locator only;
        # the immutable run.json and identity must independently authenticate it.
        locator = root / ".local/experiment-runs" / args.identity / "locator.json"
        if locator.exists():
            prefix = load(locator)["prefix"]
        run = load(safe(root, prefix + "/run.json"))
        plan = RunPlan.parse(run["plan"])
        require(
            run["implementation"] == implementation()
            and plan.identity(implementation()) == args.identity,
            "Run/code identity differs",
        )
        require(
            args.command != "resume" or args.work_root is not None,
            "Original separate --work-root required for resume",
        )
        repo = Repository(
            root,
            plan.value["publication"]["remote"],
            push=plan.value["publication"]["push"],
        )
        work = (
            args.work_root.resolve()
            if args.work_root
            else root.parent / "controller-status-unused"
        )
        controller = Controller(repo, plan, work)
        controller.approved_head = run["approval_checkpoint"]
        if args.command == "resume":
            result = await controller.run(resume=True)
        elif args.command == "status":
            result = controller.status()
            try:
                result = await controller.verify()
            except (ValueError, OSError) as error:
                result["verification"] = "PENDING_OR_REJECTED"
                result["verification_boundary"] = str(error)
        else:
            result = await controller.verify()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
