# Copyright (c) 2026
# ruff: noqa: T201, PLC0415, ASYNC240 -- human operator CLI
"""Plan/run/resume/status/verify approved experiment cohorts."""

from __future__ import annotations

import argparse
import asyncio
import getpass
import json
from pathlib import Path
from typing import Any

from experiments.orchestration.authority import ApprovalRequest
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


async def prospective_command(
    controller: Controller,
    command: str,
    approve_id: str | None,
) -> dict[str, Any]:
    """Keep the explicit maintainer approval action at the trusted CLI boundary."""
    if command == "plan":
        result = controller.plan_report()
    elif command == "run":
        authorization = (
            await controller.approve(
                ApprovalRequest(
                    approve_id,
                    getpass.getuser(),
                    "explicit CLI run --approve " + approve_id,
                    "MAINTAINER_CLI",
                ),
            )
            if approve_id
            else await controller.execution_authorization()
        )
        result = await controller.run(authorization)
    elif command == "verify-approval":
        result = {
            "status": "APPROVAL_VALID",
            "execution_authorized": "YES",
            "approval": (await controller.execution_authorization()).__dict__,
        }
    else:
        if (controller.science / "authorization").exists():
            await controller.execution_authorization()
        result = (
            await controller.verify()
            if (controller.science / "run.json").exists()
            else controller.status()
        )
    return result


async def main() -> None:
    """Offer machine-readable results and one-line progress summaries."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=(
            "plan",
            "run",
            "resume",
            "status",
            "verify",
            "verify-approval",
            "adopt",
        ),
    )
    parser.add_argument("identity", nargs="?")
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--work-root", type=Path)
    parser.add_argument(
        "--approve",
        metavar="RUN_ID",
        help="Explicit maintainer grant for this exact reviewed run",
    )
    args = parser.parse_args()
    root = args.repository.resolve()
    require(
        args.approve is None or args.command == "run",
        "--approve is only valid with run",
    )
    result: Any
    if args.command == "adopt":
        result = await adopt_completed(root)
    elif args.command in {"plan", "run", "verify-approval"} or (
        args.command == "status" and args.identity and args.identity.endswith(".json")
    ):
        require(
            args.identity is not None
            and (args.command != "run" or args.work_root is not None),
            "Plan address and separate --work-root required for run",
        )
        controller = await Controller.from_plan(
            root,
            args.identity,
            args.work_root.resolve()
            if args.work_root
            else root.parent / "controller-status-unused",
        )
        result = await prospective_command(controller, args.command, args.approve)
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
            result = await controller.run(
                await controller.execution_authorization(),
                resume=True,
            )
        elif args.command == "status":
            await controller.execution_authorization()
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
