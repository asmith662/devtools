# Copyright (c) 2026
# ruff: noqa: COM812, D103, SLF001, PLR2004 -- deterministic real worker boundary regressions
"""Actual native worker check completion; scripted responses are not inference."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop
from apps.qwen.coding_loop import _prepare_workspace
from apps.qwen.commands import CodingCommands
from apps.qwen.tasks import MARKDOWN
from devtools.models.interaction import ModelRequest, ModelResponse, ModelToolCall
from tests.apps.qwen.test_change_checks import _contract
from tests.apps.qwen.test_coding_loop import Scripted

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("required", "ending"),
    [(False, "check"), (True, "check"), (True, "poison"), (True, "without-check")],
)
def test_native_accepted_candidate_can_be_checked_before_restoration(
    tmp_path: Path, *, required: bool, ending: str
) -> None:
    _, ns = _contract()
    root = tmp_path.resolve()
    task, folder = asyncio.run(ns["fixture"](root))
    task = replace(task, maximum_calls=4, maximum_proposals=1)
    _prepare_workspace(root, folder, task)

    class Implementation(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            assert {"run_check", "check_changes", "is_current"} <= {
                d.name for d in request.tools
            }
            number = len(self.requests)
            if number == 1:
                name, args = "inspect_source", {"path": task.source, "start": 0}
            elif number == 2:
                name, args = (
                    "replace_source",
                    {
                        "path": task.source,
                        "old_text": "VALUE: int = 1",
                        "new_text": "VALUE: int = 2",
                    },
                )
            else:
                assert number == 3
                assert "VALUE: int = 2" in (root / task.source).read_text()
                if ending == "without-check":
                    return ModelResponse("Finished", self.source)
                name, args = "check_changes", {}
            calls: tuple[ModelToolCall, ...] = (
                ModelToolCall(name, json.dumps(args), f"native-{number}"),
            )
            if number == 3 and ending == "poison":
                calls += (ModelToolCall("run_check", '{"check":"shell"}', "invalid"),)
            return ModelResponse(
                "scripted",
                self.source,
                tool_calls=calls,
            )

    model = Implementation([])
    report: dict[str, Any] = {"turns": [], "accepted": False}
    operation = coding_loop._turns(
        root,
        folder,
        model,
        report,
        maximum_calls=4,
        task=task,
        coordinated_edits=True,
        observed_edits=True,
        check_changes_before_completion=required,
    )
    if ending == "poison":
        with pytest.raises(ValueError, match="Unsupported"):
            asyncio.run(operation)
        assert not report["accepted"]
        assert "change_check_freshness" not in report
        return
    asyncio.run(operation)
    if ending == "without-check":
        assert not report["accepted"]
        assert report["disposition"] == "MODEL_COMPLETED_WITHOUT_CHANGE_CHECK"
        return
    assert report["accepted"], report
    feedback = json.loads((folder / "turn-02/tools.json").read_text())[0]["result"]
    versions = feedback["validation"]["repair_contract"]["source_versions"]
    assert versions[task.new_paths[0]] is None
    assert versions[task.source]
    assert len(model.requests) == (3 if required else 2)
    if required:
        checked = report["change_check"]
        assert report["change_check_freshness"]["current"]
        assert "host_limits" not in checked
        assert CodingCommands(root, folder, task).is_current(checked)
        event = json.loads((folder / "turn-03/tools.json").read_text())[0]
        assert event["call"]["name"] == "check_changes"
        assert event["result"] == checked
        assert event["host_limits"]["proposals_remaining"] == 0
        (root / task.source).write_text(ns["BASE"])
        assert not CodingCommands(root, folder, task).is_current(checked)


def test_completion_option_requires_authorized_native_checks(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="requires native"):
        asyncio.run(
            coding_loop.run_coding_task(
                tmp_path,
                tmp_path / "refused",
                Scripted([]),
                task=MARKDOWN,
                check_changes_before_completion=True,
            )
        )
