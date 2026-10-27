# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- literal public compatibility characterization
"""Characterize existing source/check contracts before framework migration."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import commands
from devtools.context.planning import source as shared_source
from devtools.models.interaction import ModelToolCall
from devtools.tools.checks import FixedCheckTool
from tests.apps.qwen.test_check_bundle import (
    bundle as bundle,  # noqa: PLC0414 -- reuse authored fixture
)
from tests.apps.qwen.test_context_tools import (
    tools as tools,  # noqa: PLC0414 -- reuse authored fixture
)

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.context_tools import ContextTools


def test_existing_exact_source_boundary_and_observation(tools: ContextTools) -> None:
    text = "# prefix\r\n" + "\u03c0" * 3000 + "\r\n"
    (tools.root / tools.task.source).write_bytes(text.encode())
    tools.accept_source(text)
    version = str(tools.snapshot.resource_at(tools.addresses[0]).content_identity)
    call = ModelToolCall(
        "read_source",
        json.dumps(
            {
                "path": tools.task.source,
                "version": version,
                "start": 10,
                "end": len(text),
            },
        ),
        "literal-read",
    )
    result = asyncio.run(tools.dispatch(call))
    assert result["text"] == "\u03c0" * 2048
    assert result["span"] == [10, 2058]
    assert result["bytes"] == 4096
    assert result["truncated"] is True
    assert result["observation_call_id"] == "literal-read"
    assert tools.observations[-1]["text"] == result["text"]


def test_existing_fixed_argv_and_legacy_result(
    bundle: commands.CodingCommands,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entered: list[tuple[Path, tuple[str, ...]]] = []

    async def fixed(root: Path, *argv: str) -> dict[str, Any]:
        entered.append((root, argv))
        return {
            "exit_code": 7,
            "failed": True,
            "stdout": "literal",
            "stderr": "diagnostic",
        }

    monkeypatch.setattr(commands, "_timed_command", fixed)
    result = asyncio.run(
        commands.run_check(bundle.root, bundle.folder, bundle.task, "tests"),
    )
    assert entered == [
        (
            bundle.root,
            (sys.executable, "-I", "-B", str(bundle.folder / "tests-runner.py")),
        ),
    ]
    assert result == {
        "exit_code": 7,
        "failed": True,
        "stdout": "literal",
        "stderr": "diagnostic",
    }


@pytest.mark.parametrize("fail", [False, True])
def test_real_context_dispatch_enters_shared_range_owner(
    tools: ContextTools,
    monkeypatch: pytest.MonkeyPatch,
    *,
    fail: bool,
) -> None:
    original = shared_source.materialize_source_range
    entries: list[object] = []
    failure = OSError("shared source unavailable")

    def materialize(snapshot: Any, option: Any) -> Any:  # noqa: ANN401 -- transparent owner instrumentation
        entries.append(option)
        assert snapshot is tools.snapshot
        if fail:
            raise failure
        return original(snapshot, option)

    monkeypatch.setattr(shared_source, "materialize_source_range", materialize)
    unit = tools.index.views[0].units[0]
    call = ModelToolCall(
        "read_source",
        json.dumps(
            {
                "path": str(unit.resource.address),
                "version": str(unit.resource.content_identity),
                "start": 0,
                "end": 10,
            },
        ),
        "shared-range",
    )
    before = len(tools.observations)
    if fail:
        with pytest.raises(OSError, match="shared source unavailable") as raised:
            asyncio.run(tools.dispatch(call))
        assert raised.value is failure
        assert len(tools.observations) == before
    else:
        result = asyncio.run(tools.dispatch(call))
        assert result["text"] == unit.text[:10]
        assert result["span"] == [0, 10]
        assert result["observation_call_id"] == "shared-range"
    assert len(entries) == 1


@pytest.mark.parametrize("fail", [False, True])
def test_actual_fixed_check_dispatch_enters_shared_tool(
    bundle: commands.CodingCommands,
    monkeypatch: pytest.MonkeyPatch,
    *,
    fail: bool,
) -> None:
    original = FixedCheckTool.execute
    entries: list[tuple[str, ...]] = []

    async def execute(tool: FixedCheckTool, name: str) -> Any:  # noqa: ANN401 -- transparent owner instrumentation
        selected = tool.plan.select(name)
        entries.append(selected.command.argv)
        if fail:
            message = "shared fixed check unavailable"
            raise OSError(message)
        return await original(tool, name)

    monkeypatch.setattr(FixedCheckTool, "execute", execute)
    call = ModelToolCall("run_check", '{"check":"tests"}', "shared-check")
    if fail:
        with pytest.raises(OSError, match="shared fixed check unavailable"):
            asyncio.run(bundle.dispatch(call))
    else:
        result = asyncio.run(bundle.dispatch(call))
        assert result["status"] == "PASS"
    assert entries == [
        (sys.executable, "-I", "-B", str(bundle.folder / "tests-runner.py")),
    ]
    receipts = list(bundle.folder.glob("coding-command-*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text())
    assert receipt["status"] == ("EXECUTION_INTENT" if fail else "COMPLETED")
