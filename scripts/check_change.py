# Copyright (c) 2026
# ruff: noqa: INP001 -- supported operational entry point in existing scripts namespace
"""Operator entry point for the framework's host-fixed change procedure."""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import TYPE_CHECKING

from devtools.context import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.observability.commands.models import CommandOrigin
from devtools.resources.commands import Command
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.repository.validation import (
    ChangeValidationPlan,
    CheckSelection,
    InspectAndValidateTool,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.core.paths import ResolvedPath
    from devtools.tools.repository.validation import ChangeValidationReport


def selected_checks(root: ResolvedPath, names: tuple[str, ...]) -> FixedCheckPlan:
    """Project this operator's finite check vocabulary, never model-supplied argv."""
    checks = []
    for name in names:
        if name == "whitespace":
            command = Command("git").args("diff", "--check", "HEAD")
        elif name == "tests":
            command = Command("uv").args(
                "run",
                "python",
                "scripts/validate_development.py",
            )
        elif name == "lint":
            command = Command("uv").args(
                "run",
                "ruff",
                "check",
                "src",
                "tests",
                "apps",
                "scripts",
            )
        elif name == "typing":
            command = Command("uv").args("run", "mypy")
        else:
            msg = "Operator check name is not in the fixed selection."
            raise ValueError(msg)
        checks.append(
            FixedCheck(name, command.cwd(root).with_timeout(Duration.minutes(30))),
        )
    return FixedCheckPlan(root, tuple(checks))


def report_data(report: ChangeValidationReport) -> dict[str, object]:
    """Return operator metadata without raw command/output/env/error payloads."""
    return {
        "status": report.status,
        "revision": report.before.revision if report.before else None,
        "changes": [
            {
                "path": c.path,
                "index": c.index,
                "worktree": c.worktree,
                "original_path": c.original_path,
            }
            for c in report.before.changes
        ]
        if report.before
        else None,
        "checks": [
            {
                "name": c.name,
                "status": c.status,
                "exit_code": c.result.command_result.exit_code if c.result else None,
                "seconds": c.result.command_result.duration.total_seconds
                if c.result
                else None,
                "inputs_current": c.result.inputs_current if c.result else None,
                "stdout_truncated": c.result.command_result.stdout_truncated
                if c.result
                else None,
                "stderr_truncated": c.result.command_result.stderr_truncated
                if c.result
                else None,
                "error_kind": type(c.error).__name__ if c.error else None,
            }
            for c in report.checks
        ],
        "reason": report.reason,
        "observed_commands": len(report.observations),
        "authority": (
            "declared inspection/check evidence only; no review or "
            "publication authority"
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Run only explicitly selected operator checks in one admitted repository."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    parser.add_argument("--revision", required=True)
    parser.add_argument(
        "--run",
        required=True,
        help="Host-selected unique invocation correlation label",
    )
    parser.add_argument("--allow", action="append", default=[])
    parser.add_argument(
        "--check",
        action="append",
        choices=("whitespace", "tests", "lint", "typing"),
        required=True,
    )
    args = parser.parse_args(argv)
    root = resolve_path(args.root)
    names = tuple(args.check)
    plan = ChangeValidationPlan(
        selected_checks(root, names),
        args.revision,
        frozenset(RepositoryResourceAddress(p) for p in args.allow),
        tuple(CheckSelection(n) for n in names),
    )
    report = asyncio.run(
        ToolRunner().execute(
            InspectAndValidateTool(
                plan,
                origin=CommandOrigin("operator", "change", args.run, "inspect"),
            ),
            None,
        ),
    )
    print(json.dumps(report_data(report)))  # noqa: T201 -- ASCII-safe JSON preserves Unicode through escapes
    return 0 if report.status in {"passed", "skipped"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
