# Copyright (c) 2026
# ruff: noqa: T201, COM812 -- operator CLI
"""Prepare, govern execution, or observe experiments through their controller."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from devtools.core.paths import get_temp_dir, resolve_path
from devtools.orchestration.experiments import receipts
from devtools.orchestration.experiments.pipeline import (
    ExperimentExecutionPipeline,
    summary,
    target_python,
)


def main() -> int:
    """Coordinate experiments while keeping approval publication outside this CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("prepare", "execute", "reconcile", "status", "history")
    )
    parser.add_argument("plan", nargs="?", type=Path)
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--python", type=Path)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--preparation", type=Path)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Reconcile execution evidence without dispatch",
    )
    parser.add_argument(
        "--receipts",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--active", action="store_true", help="Select an unresolved execution"
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.command == "execute" and (
        args.receipts is None or args.work_root is None or args.plan is None
    ):
        parser.error(
            "execute requires plan, --receipts and --work-root; "
            "existing exact approval is mandatory"
        )
    root = resolve_path(
        args.receipts or get_temp_dir().value / "devtools-experiment-preparations",
        base_directory=Path.cwd(),
    ).value
    if args.command in {"execute", "reconcile"} or args.refresh:
        target = resolve_path(args.target, base_directory=Path.cwd()).value
        pipeline = ExperimentExecutionPipeline(
            target, root, args.python or target_python(target)
        )
        if args.command == "execute":

            def observe(event: dict[str, object]) -> None:
                print(json.dumps(event), file=sys.stderr, flush=True)

            result = asyncio.run(
                pipeline.execute(
                    args.plan,
                    args.work_root,
                    preparation=args.preparation,
                    observer=observe,
                )
            )
        else:
            result = asyncio.run(pipeline.reconcile(args.plan))
        print(receipts.encoded(result) if args.json else summary(result))
        return 0 if result["disposition"] == "COMPLETE" else 1
    if args.command == "prepare":
        if args.plan is None:
            parser.error("prepare requires a plan")
        target = resolve_path(args.target, base_directory=Path.cwd()).value
        result = asyncio.run(
            ExperimentExecutionPipeline(
                target,
                root,
                args.python or target_python(target),
            ).prepare(args.plan),
        )
        print(receipts.encoded(result) if args.json else summary(result))
        return 0 if result["disposition"] == "READY_FOR_APPROVAL" else 1
    plan = args.plan.as_posix() if args.plan else None
    if args.command == "history":
        rows = receipts.history(root, plan)
        if args.json:
            print(receipts.encoded(rows))
        else:
            for row in rows:
                print(
                    f"{row['started']} {row['disposition']} {row['plan']} "
                    f"target={row['target']} report={row['report']}",
                )
    else:
        result = receipts.latest(root, plan, active=args.active)
        print(receipts.encoded(result) if args.json else summary(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
