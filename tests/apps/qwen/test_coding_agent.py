# Copyright (c) 2026
# ruff: noqa: D103 -- actual legacy/public boundary instrumentation
"""Both actual Qwen modes delegate to the framework process and custody owner."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop
from devtools.agents.coding import process
from devtools.agents.coding.custody import SourceCustody
from tests.apps.qwen.test_coding_loop import (
    _TINY_OLD,
    _TINY_SOURCE,
    _TINY_TYPED_GOOD,
    _tiny_task,
    _TinyScripted,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("native", [False, True])
def test_real_qwen_modes_use_framework_process_and_known_custody(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    native: bool,
) -> None:
    root = tmp_path / "task"
    task = asyncio.run(_tiny_task(root, native=native))
    before_hash = task.definition_sha256
    model = _TinyScripted(task, ((_TINY_OLD, _TINY_TYPED_GOOD),))
    entered: list[object] = []
    restored: list[object] = []
    original, restore = process.run_coding_agent, SourceCustody.restore_known

    async def shared(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401 -- transparent generic entry instrumentation
        entered.append(kwargs["host"])
        result = await original(*args, **kwargs)
        assert result.accepted
        assert result.progress.proposals == 1
        assert result.progress.model_calls == (2 if native else 1)
        return result

    def custody(owner: SourceCustody, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401 -- transparent host effect boundary
        restored.append(owner)
        return restore(owner, *args, **kwargs)

    monkeypatch.setattr(process, "run_coding_agent", shared)
    monkeypatch.setattr(SourceCustody, "restore_known", custody)
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            root / ".local/run",
            model,
            task=task,
            coordinated_edits=native,
            observed_edits=native,
        ),
    )
    assert len(entered) == len(restored) == 1
    assert type(entered[0]).__module__ == "apps.qwen.turns.loop"
    assert result["schema"] == "qwen-coding-loop-v2"
    assert result["accepted"] is True
    assert result["disposition"] == "ACCEPTED"
    assert result["source_restored"] is True
    assert result["task_definition_sha256"] == task.definition_sha256 == before_hash
    assert result["proposals_attempted"] == result["proposals_admitted"] == 1
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD
    assert (root / ".local/run/final-source.py").read_text() == _TINY_TYPED_GOOD


def test_framework_boundary_failure_cannot_fall_back_to_app_loop(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "task"
    task = asyncio.run(_tiny_task(root))
    model = _TinyScripted(task, ((_TINY_OLD, _TINY_TYPED_GOOD),))
    calls: list[str] = []

    async def failed(*_args: Any, **_kwargs: Any) -> Any:  # noqa: ANN401 -- actual shared boundary fault
        calls.append("entered")
        message = "shared coding process unavailable"
        raise OSError(message)

    monkeypatch.setattr(process, "run_coding_agent", failed)
    result = asyncio.run(
        coding_loop.run_coding_task(root, root / ".local/run", model, task=task),
    )
    assert calls == ["entered"]
    assert model.requests == []
    assert result["accepted"] is False
    assert result["error"] == "OSError: shared coding process unavailable"
    assert result["source_restored"] is True
