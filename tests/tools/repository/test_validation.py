# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independent effects and literal procedure outcomes
"""Scope, deterministic selection, partial effects and retained original failures."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.context import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.tools import ToolRunner
from devtools.tools.errors import ToolInputError
from devtools.tools.repository.validation import CheckSelection
from tests.tools.repository.fixtures import CHECK, MODULE, procedure, repository

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.resources.commands import Command, CommandResult
    from devtools.tools.repository.git import GitInspection


@pytest.mark.parametrize(
    "status",
    ["passed", "failed", "skipped", "scope", "revision", "conflict", "drift"],
)
def test_real_procedure_and_deterministic_selection(
    tmp_path: Path,
    status: str,
) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        code = "raise SystemExit(7)" if status == "failed" else CHECK
        if status == "drift":
            code += ";from pathlib import Path;Path('later.txt').write_text('effect')"
        tool = procedure(tmp_path, revision, scope, code=code)
        if status == "scope":
            tool.plan = replace(tool.plan, allowed_changes=frozenset())
        elif status == "revision":
            tool.plan = replace(tool.plan, expected_revision="0" * 40)
        elif status == "skipped":
            tool.plan = replace(
                tool.plan,
                selection=(
                    CheckSelection(
                        "behavior",
                        frozenset({RepositoryResourceAddress("not-changed.py")}),
                    ),
                ),
            )
        elif status == "conflict":
            actual = tool.inspection.execute

            async def conflict(arguments: None) -> GitInspection:
                result = await actual(arguments)
                return replace(
                    result,
                    changes=(replace(result.changes[0], index="U", worktree="U"),),
                )

            tool.inspection.execute = conflict  # type: ignore[method-assign]
        result = await ToolRunner().execute(tool, None)
        expected = (
            "refused"
            if status in {"scope", "revision", "conflict"}
            else "incomplete"
            if status == "drift"
            else status
        )
        assert result.status == expected
        assert tool.last_report is result
        assert result.before is not None
        assert result.before.root == scope.root
        if status in {"scope", "revision", "conflict", "skipped"}:
            assert result.checks == ()
            assert not (tmp_path / ".local/count").exists()
        elif status == "failed":
            assert result.checks[0].status == "failed"
            assert result.checks[0].result.command_result.exit_code == 7  # type: ignore[union-attr]
        else:
            completed = result.checks[0].result
            assert completed is not None
            assert (
                completed.command_result.stdout == b"verified:7\nPRIVATE_SENTINEL\r\n"
                or completed.command_result.stdout.replace(b"\r\n", b"\n")
                == b"verified:7\nPRIVATE_SENTINEL\n"
            )
            assert completed.inputs_current is True
            assert (tmp_path / ".local/count").read_text() == "x"
        safe = json.dumps([asdict(x) for x in result.observations], default=str)
        assert "PRIVATE_SENTINEL" not in safe
        assert str(tmp_path) not in safe
        assert CHECK not in safe

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    ["missing", "cwd", "timeout", "lost", "partial", "source-drift"],
)
def test_incomplete_checks_retain_prefix_and_unknown_effects(
    tmp_path: Path,
    fault: str,
) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        code = CHECK
        if fault == "timeout":
            code += ";import time;time.sleep(30)"
        elif fault == "source-drift":
            code += (
                ";from pathlib import Path;import sys;"
                "Path(sys.argv[1]).write_text('UNKNOWN')"
            )
        tool = procedure(tmp_path, revision, scope, code=code, extra=fault == "partial")
        checks = list(tool.check_tool.plan.checks)
        if fault in {"missing", "cwd", "timeout"}:
            command = checks[0].command
            command = (
                replace(command, executable="devtools-missing-executable-e961")
                if fault == "missing"
                else command.cwd(resolve_path(tmp_path / "missing"))
                if fault == "cwd"
                else command.with_timeout(Duration.seconds(0.2))
            )
            checks[0] = replace(checks[0], command=command)
            tool.check_tool.plan = replace(tool.check_tool.plan, checks=tuple(checks))
        original = tool.check_tool.executor.execute
        entries: list[Command] = []
        failure = OSError("PRIVATE_SENTINEL acknowledgment lost")

        async def interrupted(command: Command) -> CommandResult:
            entries.append(command)
            result = await original(command)
            if fault == "lost" or (fault == "partial" and len(entries) == 2):
                raise failure
            return result

        tool.check_tool.executor.execute = interrupted  # type: ignore[method-assign]
        result = await ToolRunner().execute(tool, None)
        assert result.status == "incomplete"
        assert result.checks[-1].status in {"unknown", "failed"}
        assert len(entries) == (2 if fault == "partial" else 1)
        if fault in {"lost", "partial"}:
            assert result.error is failure
            assert result.checks[-1].error is failure
            assert result.observations[-1].entered is None
            assert result.observations[-1].exit_code is None
            assert (tmp_path / ".local/count").read_text() == (
                "xx" if fault == "partial" else "x"
            )
        if fault == "partial":
            assert result.checks[0].result.command_result.exit_code == 0  # type: ignore[union-attr]
        if fault == "source-drift":
            assert result.checks[0].result.command_result.exit_code == 0  # type: ignore[union-attr]
            assert result.checks[0].result.inputs_current is False  # type: ignore[union-attr]
            assert (tmp_path / MODULE).read_text() == "UNKNOWN"

    asyncio.run(run())


def test_real_cancellation_preserves_effect_and_propagates(tmp_path: Path) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        tool = procedure(
            tmp_path,
            revision,
            scope,
            code=CHECK + ";import time;time.sleep(30)",
        )
        task = asyncio.create_task(ToolRunner().execute(tool, None))
        async with asyncio.timeout(5):
            while not (tmp_path / ".local/count").exists():  # noqa: ASYNC110 -- bounded cross-process file handshake
                await asyncio.sleep(0.01)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        result = tool.last_report
        assert result is not None
        assert result.status == "cancelled"
        assert result.checks[-1].status == "cancelled"
        assert result.observations[-1].entered is None
        assert (tmp_path / ".local/count").read_text() == "x"

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    [
        "revision",
        "scope",
        "selection",
        "empty",
        "duplicate",
        "rule",
        "env-policy",
        "env-names",
    ],
)
def test_invalid_host_plan_refuses_before_effect(tmp_path: Path, fault: str) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        tool = procedure(tmp_path, revision, scope)
        changes: dict[str, Any] = (
            {"expected_revision": "bad"}
            if fault == "revision"
            else {"allowed_changes": []}
            if fault == "scope"
            else {"selection": []}
            if fault == "selection"
            else {"selection": ()}
            if fault == "empty"
            else {"selection": tool.plan.selection * 2}
            if fault == "duplicate"
            else {"selection": (CheckSelection("behavior", cast("Any", [])),)}
            if fault == "rule"
            else {"environment_names": frozenset()}
            if fault == "env-policy"
            else {"environment_names": []}
        )
        with pytest.raises((ValueError, ToolInputError)):
            replace(tool.plan, **changes)
        assert not (tmp_path / ".local/count").exists()

    asyncio.run(run())


def test_no_model_arguments_or_unadmitted_check(tmp_path: Path) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        tool = procedure(tmp_path, revision, scope)
        with pytest.raises(ToolInputError):
            await ToolRunner().execute(cast("Any", tool), {"shell": "arbitrary"})
        with pytest.raises(ToolInputError):
            replace(tool.plan, selection=(CheckSelection("arbitrary"),))
        assert tool.inspection.observations == []
        assert not (tmp_path / ".local/count").exists()

    asyncio.run(run())


@pytest.mark.parametrize("stop", [True, False])
def test_known_failed_check_stop_policy(tmp_path: Path, *, stop: bool) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        tool = procedure(
            tmp_path,
            revision,
            scope,
            code="raise SystemExit(3)",
            extra=True,
            stop=stop,
        )
        result = await ToolRunner().execute(tool, None)
        assert result.status == "failed"
        assert len(result.checks) == (1 if stop else 2)
        assert all(c.result.command_result.exit_code == 3 for c in result.checks)  # type: ignore[union-attr]

    asyncio.run(run())


def test_one_origin_cannot_replay_or_concurrently_duplicate_a_procedure(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        tool = procedure(tmp_path, revision, scope)
        results = await asyncio.gather(
            ToolRunner().execute(tool, None),
            ToolRunner().execute(tool, None),
            return_exceptions=True,
        )
        assert sum(isinstance(r, ToolInputError) for r in results) == 1
        assert (tmp_path / ".local/count").read_text() == "x"
        count = len(tool.inspection.observations)
        with pytest.raises(ToolInputError, match="fresh"):
            await ToolRunner().execute(tool, None)
        assert len(tool.inspection.observations) == count
        assert (tmp_path / ".local/count").read_text() == "x"

    asyncio.run(run())
