# Copyright (c) 2026
# ruff: noqa: D103 -- literal execution and uncertainty controls
"""Fixed names, actual Commands, declared input correspondence and no retries."""

from __future__ import annotations

import asyncio
import sys
from dataclasses import FrozenInstanceError, replace
from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandOutputPolicy, CommandResult
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan, FixedCheckTool
from devtools.tools.errors import ToolInputError
from tests.tools.source_fixture import source_fixture

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.tools.source import SourceScope


def check(
    root: Path,
    code: str = 'import sys; sys.stdout.buffer.write(b"exact\\n")',
) -> FixedCheck:
    return FixedCheck(
        "literal",
        Command(sys.executable)
        .args("-B", "-c", code)
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(10)),
    )


@pytest.mark.parametrize("bound", [True, False])
def test_real_fixed_command_and_immutable_plan(tmp_path: Path, *, bound: bool) -> None:
    scope, _ = source_fixture(tmp_path)
    selected = check(tmp_path)
    plan = FixedCheckPlan(scope.root, (selected,), scope if bound else None)
    result = asyncio.run(ToolRunner().execute(FixedCheckTool(plan), "literal"))
    assert result.command_result.command is selected.command
    assert result.command_result.stdout == b"exact\n"
    assert result.command_result.exit_code == 0
    assert result.inputs_current is (True if bound else None)
    assert result.passed is True
    with pytest.raises(FrozenInstanceError):
        plan.checks = ()  # type: ignore[misc]


@pytest.mark.parametrize(
    "fault",
    [
        "empty",
        "mutable",
        "duplicate",
        "blank",
        "foreign-scope",
        "cwd",
        "outside",
        "timeout",
        "zero",
    ],
)
def test_unbounded_or_conflicting_plan_refused(tmp_path: Path, fault: str) -> None:
    scope, _ = source_fixture(tmp_path)
    selected = check(tmp_path)
    checks: tuple[FixedCheck, ...] = (selected,)
    source: SourceScope | None = None
    if fault == "empty":
        checks = ()
    elif fault == "mutable":
        checks = [selected]  # type: ignore[assignment]
    elif fault == "duplicate":
        checks = (selected, selected)
    elif fault == "blank":
        checks = (replace(selected, name=" "),)
    elif fault == "foreign-scope":
        source = replace(scope, root=resolve_path(tmp_path.parent))
    else:
        command = replace(
            selected.command,
            working_directory=None
            if fault == "cwd"
            else resolve_path(tmp_path.parent)
            if fault == "outside"
            else scope.root,
            timeout=None
            if fault == "timeout"
            else Duration.seconds(0)
            if fault == "zero"
            else Duration.seconds(10),
        )
        checks = (replace(selected, command=command),)
    with pytest.raises(ValueError, match="Fixed check"):
        FixedCheckPlan(scope.root, checks, source)


def test_unadmitted_check_and_stale_source_never_enter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scope, _ = source_fixture(tmp_path)
    tool = FixedCheckTool(FixedCheckPlan(scope.root, (check(tmp_path),), scope))

    async def forbidden(_command: Command) -> CommandResult:
        pytest.fail("Admission failure entered Commands")

    monkeypatch.setattr(tool.executor, "execute", forbidden)
    with pytest.raises(ToolInputError, match="host-admitted"):
        asyncio.run(ToolRunner().execute(tool, "model-shell"))
    (tmp_path / "module.py").write_text("drift", encoding="utf-8")
    with pytest.raises(ToolInputError, match="current"):
        asyncio.run(ToolRunner().execute(tool, "literal"))


def test_known_result_survives_post_command_drift(tmp_path: Path) -> None:
    scope, _ = source_fixture(tmp_path)
    selected = check(
        tmp_path,
        'from pathlib import Path; Path("module.py").write_text("known change")',
    )
    result = asyncio.run(
        ToolRunner().execute(
            FixedCheckTool(FixedCheckPlan(scope.root, (selected,), scope)),
            "literal",
        ),
    )
    assert result.command_result.exit_code == 0
    assert result.inputs_current is False
    assert isinstance(result.input_error, ToolInputError)
    assert result.passed is False
    assert (tmp_path / "module.py").read_text() == "known change"


@pytest.mark.parametrize(
    "code",
    [
        "raise SystemExit(7)",
        'import sys; sys.stdout.buffer.write(b"12345678")',
        'import sys; sys.stderr.buffer.write(b"12345678")',
    ],
)
def test_failed_or_truncated_output_is_not_a_passing_check(
    tmp_path: Path,
    code: str,
) -> None:
    plan = FixedCheckPlan(
        resolve_path(tmp_path),
        (check(tmp_path, code),),
        output_policy=CommandOutputPolicy(max_stdout_bytes=4, max_stderr_bytes=4),
    )
    result = asyncio.run(ToolRunner().execute(FixedCheckTool(plan), "literal"))
    assert result.passed is False


@pytest.mark.parametrize("cancel", [False, True])
def test_unknown_ack_after_effect_not_retried(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    cancel: bool,
) -> None:
    tool = FixedCheckTool(FixedCheckPlan(resolve_path(tmp_path), (check(tmp_path),)))
    error = asyncio.CancelledError("lost") if cancel else OSError("lost")
    entries: list[Command] = []

    async def lost(command: Command) -> CommandResult:
        entries.append(command)
        (tmp_path / "effect").write_text("entered", encoding="utf-8")
        raise error

    monkeypatch.setattr(tool.executor, "execute", lost)
    with pytest.raises(type(error)) as raised:
        asyncio.run(ToolRunner().execute(tool, "literal"))
    assert raised.value is error
    assert len(entries) == 1
    assert (tmp_path / "effect").read_text() == "entered"


@pytest.mark.parametrize("changed", ["root", "cwd"])
def test_changed_canonical_working_scope_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    changed: str,
) -> None:
    from devtools.tools import checks  # noqa: PLC0415 -- fault at canonical boundary

    directory = tmp_path / "child"
    directory.mkdir()
    plan = FixedCheckPlan(resolve_path(tmp_path), (check(directory),))
    original = resolve_path

    def current(path: object) -> object:
        if path == (tmp_path if changed == "root" else directory):
            return original(tmp_path.parent)
        return original(path)  # type: ignore[arg-type]

    monkeypatch.setattr(checks, "resolve_path", current)
    with pytest.raises(ToolInputError, match="working scope changed"):
        asyncio.run(ToolRunner().execute(FixedCheckTool(plan), "literal"))
