# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- literal privacy and command lifecycle contracts
"""Real framework handle observation without secondary execution or raw capture."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.observability.commands.inspection import (
    CommandInspector,
    completed_observation,
)
from devtools.observability.commands.models import (
    CommandObservation,
    CommandOrigin,
    CommandPattern,
)
from devtools.observability.commands.patterns import summarize_patterns
from devtools.resources.commands import (
    Command,
    CommandError,
    CommandExecutor,
    CommandOutputPolicy,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from pathlib import Path

    from devtools.resources.commands import CommandEvent

ORIGIN = CommandOrigin("worker", "task", "run", "command")
PATTERN = CommandPattern(
    "python",
    "literal-check",
    ("script",),
    ("python",),
    "tools.checks.FixedCheckTool",
)


@pytest.mark.parametrize("exit_code", [0, 7])
def test_exact_handle_result_and_safe_observation(exit_code: int) -> None:
    async def run() -> None:
        execution = CommandExecutor().start(
            Command(sys.executable).args(
                "-I",
                "-c",
                f"print('PRIVATE_SENTINEL');raise SystemExit({exit_code})",
            ),
        )
        inspector = CommandInspector(ORIGIN, PATTERN)
        result = await inspector.observe(execution)
        assert result is await execution
        assert result.exit_code == exit_code
        assert b"PRIVATE_SENTINEL" in result.stdout
        value = inspector.observation
        assert value.entered is True
        assert value.exit_code == exit_code
        assert value.duration is result.duration
        assert value.outcome == ("succeeded" if exit_code == 0 else "failed")
        assert "PRIVATE_SENTINEL" not in json.dumps(asdict(value), default=str)
        assert (
            completed_observation(result, origin=ORIGIN, pattern=PATTERN).source
            == "framework-result"
        )

    asyncio.run(run())


@pytest.mark.parametrize("fault", ["missing", "timeout", "capture"])
def test_unknown_entry_outcome_or_incomplete_event_feed(fault: str) -> None:
    async def run() -> None:
        executor = CommandExecutor(
            output_policy=CommandOutputPolicy(max_pending_events=1),
        )
        command = (
            Command("devtools-not-installed-27917")
            if fault == "missing"
            else Command(sys.executable).args(
                "-I",
                "-c",
                "import time;print('SECRET');time.sleep(30)"
                if fault == "timeout"
                else "print('hello')",
            )
        )
        if fault == "timeout":
            command = command.with_timeout(Duration.seconds(0.1))
        execution = executor.start(command)
        inspector = CommandInspector(ORIGIN, PATTERN)
        if fault == "capture":
            async for _ in execution.events():
                pass
            result = await inspector.observe(execution)
            assert result.exit_code == 0
            assert inspector.observation.capture_incomplete
            assert inspector.observation.entered is True
            return
        with pytest.raises(CommandError):
            await inspector.observe(execution)
        assert inspector.observation.outcome == "unknown"
        assert inspector.observation.exit_code is None
        assert inspector.observation.duration is None
        if fault == "missing":
            assert inspector.observation.entered is None

    asyncio.run(run())


def test_cancellation_awaits_original_handle_cleanup(tmp_path: Path) -> None:
    async def run() -> None:
        inspector = CommandInspector(ORIGIN, PATTERN)
        command = (
            Command(sys.executable)
            .args(
                "-I",
                "-c",
                (
                    "from pathlib import Path;import time;"
                    "Path('entered').write_text('x');time.sleep(30)"
                ),
            )
            .cwd(resolve_path(tmp_path))
        )
        execution = CommandExecutor().start(command)
        task = asyncio.create_task(inspector.observe(execution))
        async with asyncio.timeout(5):
            while not (tmp_path / "entered").exists():  # noqa: ASYNC110 -- bounded cross-process file handshake
                await asyncio.sleep(0.01)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert execution.is_complete
        assert inspector.observation.outcome == "cancelled"
        assert inspector.observation.exit_code is None
        assert (tmp_path / "entered").read_text() == "x"

    asyncio.run(run())


def test_dropped_lifecycle_events_do_not_erase_completed_result() -> None:
    async def run() -> None:
        execution = CommandExecutor(
            output_policy=CommandOutputPolicy(max_pending_events=1),
        ).start(Command(sys.executable).args("-I", "-c", "print('x')"))
        await execution
        inspector = CommandInspector(ORIGIN, PATTERN)
        result = await inspector.observe(execution)
        assert result.exit_code == 0
        assert execution.events_dropped > 0
        assert inspector.observation.entered is True
        assert inspector.observation.outcome == "succeeded"
        assert inspector.observation.events_dropped == execution.events_dropped
        assert inspector.observation.capture_incomplete
        assert (
            completed_observation(result, origin=ORIGIN, pattern=PATTERN).events_dropped
            == result.events_dropped
        )

    asyncio.run(run())


def test_cancelled_secondary_capture_does_not_erase_known_result() -> None:
    async def run() -> None:
        execution = CommandExecutor().start(
            Command(sys.executable).args("-I", "-c", "print('known')"),
        )

        async def unavailable() -> AsyncIterator[CommandEvent]:
            events: tuple[CommandEvent, ...] = ()
            for event in events:
                yield event
            raise asyncio.CancelledError

        execution.events = unavailable  # type: ignore[method-assign]
        inspector = CommandInspector(ORIGIN, PATTERN)
        result = await inspector.observe(execution)
        assert result.exit_code == 0
        assert result.stdout.replace(b"\r\n", b"\n") == b"known\n"
        assert inspector.observation.capture_incomplete
        assert inspector.observation.outcome == "succeeded"

    asyncio.run(run())


@pytest.mark.parametrize("field", ["agent", "task", "run", "call"])
def test_invalid_origin(field: str) -> None:
    with pytest.raises(ValueError, match="origin"):
        replace(ORIGIN, **{field: "private text with spaces"})


@pytest.mark.parametrize(
    "fault",
    ["roles", "capabilities", "role-count", "cap-count", "label", "role", "equivalent"],
)
def test_invalid_pattern(fault: str) -> None:
    changed: dict[str, Any] = (
        {"argument_roles": []}
        if fault == "roles"
        else {"capabilities": []}
        if fault == "capabilities"
        else {"argument_roles": ("flag",) * 65}
        if fault == "role-count"
        else {"capabilities": ("tag",) * 17}
        if fault == "cap-count"
        else {"family": "raw secret string"}
        if fault == "label"
        else {"argument_roles": ("PRIVATE_SENTINEL",)}
        if fault == "role"
        else {"equivalent_tool": "not a tool"}
    )
    with pytest.raises(ValueError, match="pattern"):
        replace(PATTERN, **changed)


@pytest.mark.parametrize("fault", ["drop", "exit-type", "missing-exit", "false-entry"])
def test_inconsistent_observation(fault: str) -> None:
    changed = (
        {"events_dropped": -1}
        if fault == "drop"
        else {"exit_code": True}
        if fault == "exit-type"
        else {"outcome": "succeeded"}
        if fault == "missing-exit"
        else {"entered": False, "exit_code": 0}
    )
    with pytest.raises(ValueError, match="observation"):
        CommandObservation(ORIGIN, PATTERN, "framework-result", **changed)


def test_deterministic_patterns_dedup_unknowns_and_cooccurrence() -> None:
    success = CommandObservation(
        ORIGIN,
        PATTERN,
        "framework-result",
        entered=True,
        outcome="succeeded",
        exit_code=0,
    )
    failure = replace(
        success,
        origin=replace(ORIGIN, task="task-2", call="other"),
        outcome="failed",
        exit_code=3,
    )
    unknown = replace(
        success,
        origin=replace(ORIGIN, agent="other", call="third"),
        outcome="unknown",
        exit_code=None,
        entered=None,
    )
    cancelled = replace(
        unknown,
        origin=replace(unknown.origin, call="cancelled"),
        outcome="cancelled",
    )
    conflict = replace(
        unknown,
        origin=replace(unknown.origin, call="conflict"),
        outcome="conflict",
    )
    git = replace(
        success,
        origin=replace(ORIGIN, call="git"),
        pattern=CommandPattern("git", "status"),
    )
    rows = (success, failure, unknown, cancelled, conflict, git, success)
    result = summarize_patterns(rows)
    assert result == summarize_patterns(tuple(reversed(rows)))
    assert len(result) == 2
    pattern = result[1]
    assert pattern.frequency == 5
    assert pattern.distinct_tasks == 2
    assert pattern.distinct_agents == 2
    assert (
        pattern.succeeded,
        pattern.failed,
        pattern.unknown,
        pattern.cancelled,
        pattern.conflicting,
    ) == (1, 1, 1, 1, 1)
    assert pattern.co_occurring_operations == ("git:status",)
    assert pattern.pattern.equivalent_tool == "tools.checks.FixedCheckTool"
    with pytest.raises(ValueError, match="Conflicting"):
        summarize_patterns((success, replace(success, outcome="unknown")))
    with pytest.raises(ValueError, match="bound"):
        summarize_patterns(rows, maximum_observations=1)
    with pytest.raises(ValueError, match="bound"):
        summarize_patterns((), maximum_observations=0)
    assert summarize_patterns(()) == ()


def test_composition_candidates_have_explicit_output_bounds() -> None:
    rows = tuple(
        CommandObservation(
            replace(ORIGIN, call="call-" + str(i)),
            CommandPattern("git", "operation-" + str(i)),
            "framework-result",
        )
        for i in range(5)
    )
    result = summarize_patterns(rows, maximum_related_operations=2)
    assert len(result) == 5
    assert all(
        len(x.co_occurring_operations) == 2 and x.co_occurrence_truncated
        for x in result
    )
    with pytest.raises(ValueError, match="bound"):
        summarize_patterns(rows, maximum_related_operations=0)
