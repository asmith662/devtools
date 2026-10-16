# Copyright (c) 2026
# ruff: noqa: T201 -- operator CLI
"""Prepare experiments or inspect pipeline-owned preparation history."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from devtools.core.paths import get_temp_dir, resolve_path
from devtools.orchestration.experiments import receipts
from devtools.orchestration.experiments.pipeline import (
    ExperimentExecutionPipeline,
    summary,
    target_python,
)


def main() -> int:
    """Expose preparation only; scientific approval remains in the controller."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "status", "history"))
    parser.add_argument("plan", nargs="?", type=Path)
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--python", type=Path)
    parser.add_argument(
        "--receipts",
        type=Path,
        default=get_temp_dir().value / "devtools-experiment-preparations",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = resolve_path(args.receipts, base_directory=Path.cwd()).value
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
        result = receipts.latest(root, plan)
        print(receipts.encoded(result) if args.json else summary(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
