# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- operator messages and structured receipts
"""Focused development, impact preview, failure recovery and protected validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pytest

from devtools.core.time import Stopwatch, Timestamp
from devtools.resources.commands import CommandError, CommandTimeoutError
from scripts.validate_development import pytest_arguments
from scripts.validation.evidence import git, inputs, save
from scripts.validation.observation import Observations, failure_kind
from scripts.validation.protected import run_protected
from scripts.validation.selection import select


def recovery(previous: dict[str, Any], correction: str) -> list[str]:
    """Recover failed IDs only after the operator names a correction/diagnosis."""
    if not correction.strip():
        message = "Recovery requires a meaningful correction or diagnostic purpose"
        raise ValueError(message)
    failed = sorted(
        {p["nodeid"] for p in previous["phases"] if p["outcome"] == "failed"}
    )
    if not failed:
        message = (
            "No failed test IDs: diagnose collection/configuration/infrastructure first"
        )
        raise ValueError(message)
    return failed


def main() -> int:  # noqa: C901, PLR0912, PLR0915 -- finite operator modes
    """Require an explicit mode; never fall back to the full suite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode", choices=("targeted", "impact", "recover", "comprehensive")
    )
    parser.add_argument(
        "--base",
        default="HEAD",
        help="Compare this revision to index and working bytes",
    )
    parser.add_argument("--test", action="append", default=[])
    parser.add_argument(
        "--changed",
        action="append",
        default=[],
        help="Additional declared paths for impact preview",
    )
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--correction", default="")
    parser.add_argument(
        "--execute", action="store_true", help="Otherwise emit a selection only"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="New receipt address; never overwritten",
    )
    args = parser.parse_args()
    root = Path.cwd()
    if not args.output.resolve().is_relative_to(root / ".local"):
        parser.error("Receipts must be written under canonical .local/")
    if args.output.exists():
        parser.error("Output already exists; use a fresh receipt path")
    before = inputs(root)
    changed = sorted(
        set(
            args.changed
            + git(
                root, "diff", "--name-only", "--no-renames", args.base, "--"
            ).splitlines()
            + git(
                root,
                "ls-files",
                "--others",
                "--exclude-standard",
                "--",
                "src",
                "tests",
                "scripts",
                "apps",
            ).splitlines()
        )
    )
    plan = select(root, changed)
    new_paths = git(
        root,
        "ls-files",
        "--others",
        "--exclude-standard",
        "--",
        "src",
        "tests",
        "scripts",
        "apps",
    ).splitlines()
    plan["uncertainty"].extend(
        f"{p}: new file/layout needs owner review" for p in new_paths
    )
    targets = list(args.test)
    previous = None
    if args.mode == "recover":
        if args.previous is None:
            parser.error("Recovery requires --previous and --correction")
        previous = json.loads(args.previous.read_text(encoding="utf-8"))
        targets += recovery(previous, args.correction)
        targets += list(plan["groups"])
        if plan["uncertainty"] and not args.test and args.execute:
            parser.error(
                "Recovery impact is uncertain; supply reviewed --test groups for the correction"
            )
    elif args.mode in {"targeted", "impact"} and not targets:
        targets = list(plan["groups"])
        if plan["uncertainty"] and args.execute:
            parser.error(
                "Impact evidence is incomplete; preview uncertainty, provide --test groups after review, or explicitly choose comprehensive"
            )
    for target in targets:
        path = target.split("::")[0]
        if (
            target.startswith("-")
            or not path.startswith("tests/")
            or ".." in Path(path).parts
            or path.startswith("tests/experiments/")
            or not (root / path).resolve().is_relative_to(root / "tests")
        ):
            parser.error(
                "Targets must be protected repository tests/ paths or node IDs"
            )
    if args.mode == "comprehensive":
        arguments = pytest_arguments(root)
    else:
        if not targets:
            parser.error(
                "No sufficient selection; supply tests or choose comprehensive explicitly"
            )
        arguments = [
            *sorted(
                t
                for t in set(targets)
                if not any(
                    t.startswith((p + "/", p + "::")) for p in set(targets) if p != t
                )
            ),
            "--no-cov",
            f"--ignore={root / 'tests/experiments'}",
        ]
    report: dict[str, Any] = {
        "schema": "development-validation-v1",
        "mode": args.mode,
        "selection": plan,
        "argv": arguments,
        "inputs": before,
        "started_at": str(Timestamp.now()),
        "previous": str(args.previous) if previous else None,
        "correction": args.correction,
        "reuse_policy": "fresh-only; historical observations are not a new comprehensive pass",
        "status": "planned",
        "phases": [],
        "environment_overrides": {
            "COVERAGE_FILE": str(
                args.output.with_suffix(args.output.suffix + ".coverage").absolute()
            )
        }
        if args.mode == "comprehensive"
        else {},
    }
    if not args.execute:
        save(args.output, json.dumps(report, indent=2))
        print(json.dumps(plan, indent=2))  # noqa: T201
        return 0
    save(
        args.output.with_suffix(args.output.suffix + ".intent"),
        json.dumps(report, indent=2),
    )
    observations = Observations()
    watch = Stopwatch()
    infrastructure = None
    try:
        code = (
            run_protected(root, args.output, arguments, observations)
            if args.mode == "comprehensive"
            else int(
                pytest.main([*arguments, "--durations=30"], plugins=[observations])
            )
        )
    except (CommandError, OSError, RuntimeError) as error:
        code = 3
        infrastructure = (
            "timeout" if isinstance(error, CommandTimeoutError) else "infrastructure"
        )
        report["error"] = str(error)
    report.update(
        exit_code=code,
        status=infrastructure or failure_kind(code, observations),
        seconds=watch.stop().total_seconds,
        phases=observations.phases,
        collection_errors=observations.collection_errors,
        finished_at=str(Timestamp.now()),
        inputs_unchanged=inputs(root) == before,
    )
    if not report["inputs_unchanged"]:
        report["status"] = "input-drift"
    save(args.output, json.dumps(report, indent=2))
    return code if report["inputs_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
