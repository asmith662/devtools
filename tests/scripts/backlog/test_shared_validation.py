# Copyright (c) 2026
# ruff: noqa: D103 -- authored integration and owner-entry assertions
"""Codex-attributed closeout uses shared checks without private worker helpers."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

from devtools.tools.checks import FixedCheckTool
from scripts.backlog.coordinator import git
from tests.scripts.backlog.test_local_closeout import evidence
from tests.scripts.backlog.test_work import fixture as fixture  # noqa: PLC0414

if TYPE_CHECKING:
    import pytest


def test_codex_closeout_enters_shared_fixed_checks(
    fixture: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = FixedCheckTool.execute
    entries: list[tuple[str, ...]] = []

    async def execute(tool: FixedCheckTool, name: str) -> Any:  # noqa: ANN401 -- transparent owner instrumentation
        entries.append(tool.plan.select(name).command.argv)
        return await original(tool, name)

    monkeypatch.setattr(FixedCheckTool, "execute", execute)

    async def run() -> None:
        root, task = fixture["root"], fixture["task"]
        folder = evidence(fixture)
        path = folder / "result.json"
        record = json.loads(path.read_text())
        record["implementation_by"] = "Codex"
        path.write_text(json.dumps(record))
        await git(root, "switch", "feat/fixture")
        head = await git(root, "rev-parse", "HEAD")
        before = (root / task.source).read_text(encoding="utf-8")
        result = await fixture["cycle"].integration.closeout_local(
            task,
            folder,
            branch="feat/fixture",
            expected_head=head,
            implementation_author="Codex",
        )
        assert result["disposition"] == "SUPERVISORY_REVIEW"
        assert result["implementation_by"] == "Codex"
        assert (root / task.source).read_text(encoding="utf-8") == before
        assert await git(root, "rev-parse", "HEAD") == head
        assert await git(root, "diff") == ""
        assert sum(argv[-1].endswith("tests-runner.py") for argv in entries) == 1
        assert sum(argv[-1].endswith("oracle-runner.py") for argv in entries) == 1

    asyncio.run(run())
