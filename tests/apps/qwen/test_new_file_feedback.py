# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004 -- bounded deterministic native-loop evidence
"""Absent slots, creation, genuine check dispatch and canonical restoration."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen.commands import CodingCommands
from apps.qwen.context_tools import ContextTools
from apps.qwen.development_task import _hash
from apps.qwen.edits import admit_observed
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.models.interaction import ModelRequest, ModelResponse, ModelToolCall
from devtools.resources.filesystem import FilesystemNotFoundError
from scripts.backlog.coordinator import designate, git
from scripts.qwen import coding_worker
from tests.apps.qwen.test_change_checks import _contract
from tests.apps.qwen.test_coding_loop import Scripted
from tests.apps.qwen.test_context_tools import dispatch

if TYPE_CHECKING:
    from pathlib import Path


def test_new_module_feedback_checks_and_checkout_restoration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, ns = _contract()
    root = tmp_path.resolve()
    task, folder = asyncio.run(ns["fixture"](root))
    overview = root / "docs/backlog/overview.md"
    overview.parent.mkdir(parents=True)
    overview.write_text("# Authored fixture backlog\n", encoding="utf-8")
    asyncio.run(designate(root, authorize=lambda _: True))
    test = root / task.tests[0]
    test.write_text(test.read_text().replace("== 2", "in (1, 2)"), encoding="utf-8")
    asyncio.run(git(root, "add", "--", task.tests[0], "docs/backlog/overview.md"))
    asyncio.run(
        git(
            root,
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@invalid",
            "commit",
            "-qm",
            "Baseline-compatible test",
        )
    )
    task = replace(
        task,
        baseline_revision=asyncio.run(git(root, "rev-parse", "HEAD")),
        baseline_hashes=tuple((p, _hash(root / p)) for p, _ in task.baseline_hashes),
        maximum_calls=4,
        maximum_proposals=2,
        oracle="assert module.VALUE == 2\nassert module.EXTRA == 3\n",
    )
    new = task.new_paths[0]
    run = folder.parent / "native-new-file"

    class Implementation(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            number = len(self.requests)
            if number == 1:
                operations = [
                    ("inspect_source", {"path": task.source, "start": 0}),
                    ("inspect_source", {"path": new, "start": 0}),
                ]
            elif number == 2:
                operations = [
                    (
                        "replace_source",
                        {
                            "path": task.source,
                            "old_text": "VALUE: int = 1",
                            "new_text": "VALUE: int = 2",
                        },
                    )
                ]
            elif number == 3:
                feedback = json.loads((run / "turn-02/tools.json").read_text())[0][
                    "result"
                ]
                assert feedback["validation"]["oracle"]["status"] == "FAIL"
                assert (
                    feedback["validation"]["repair_contract"]["source_versions"][new]
                    is None
                )
                operations = [
                    (
                        "replace_source",
                        {
                            "path": task.source,
                            "old_text": ns["GOOD"],
                            "new_text": (
                                '"""Authored validation fixture."""\n\n'
                                "from devtools.new_module import EXTRA as EXTRA\n\n"
                                "VALUE: int = 2\n"
                            ),
                        },
                    ),
                    (
                        "replace_source",
                        {
                            "path": new,
                            "old_text": "",
                            "new_text": (
                                '"""Authorized new module."""\n\nEXTRA: int = 3\n'
                            ),
                        },
                    ),
                ]
            else:
                assert number == 4
                feedback = json.loads((run / "turn-03/tools.json").read_text())[0][
                    "result"
                ]
                versions = feedback["validation"]["repair_contract"]["source_versions"]
                observed = next(
                    o for o in feedback["source_observations"] if o["path"] == new
                )
                assert versions[new] == observed["version"]
                assert versions[new] is not None
                assert observed["text"] == (root / new).read_text()
                operations = [("check_changes", {})]
            return ModelResponse(
                "Scripted infrastructure regression, not inference",
                self.source,
                tool_calls=tuple(
                    ModelToolCall(name, json.dumps(args), f"native-{number}-{i}")
                    for i, (name, args) in enumerate(operations)
                ),
            )

    async def interaction(_: Path) -> tuple[Implementation, dict[str, Any]]:
        return Implementation([]), {"kind": "scripted regression; no local inference"}

    monkeypatch.setattr(coding_worker, "local_interaction", interaction)
    result = asyncio.run(
        coding_worker.run_local_task(
            root,
            run,
            task=task,
            branch="feat/new-file-fixture",
            coordinated_edits=True,
            observed_edits=True,
            check_changes_before_completion=True,
        )
    )
    assert result["accepted"], result
    assert result["change_check_freshness"]["current"]
    assert (root / task.source).read_text() == ns["BASE"]
    assert not (root / new).exists()
    assert result["original_unchanged"]
    assert not CodingCommands(root, run, task).is_current(result["change_check"])
    assert not (root / ".local/backlog/checkout-owner").exists()


def test_new_slots_do_not_hide_occupation_or_required_resource_loss(
    tmp_path: Path,
) -> None:
    _, ns = _contract()
    root = tmp_path.resolve()
    task, _ = asyncio.run(ns["fixture"](root))
    tools = ContextTools(root, task, direct_reads=True)
    new = task.new_paths[0]
    dispatch(tools, "inspect_source", path=new, start=0)
    (root / new).write_text("# external occupation\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unadmitted new source"):
        tools.check_current()
    call = ModelToolCall(
        "replace_source",
        json.dumps({"path": new, "old_text": "", "new_text": "VALUE = 2\n"}),
        "stale-absence",
    )
    with pytest.raises((ValueError, PatchProposalError)):
        admit_observed(root, {task.source: ns["BASE"], new: ""}, (call,), tools)
    assert (root / new).read_text() == "# external occupation\n"
    (root / new).unlink()
    unauthorized = "src/devtools/unauthorized.py"
    with pytest.raises(ValueError, match="Unauthorized"):
        dispatch(tools, "inspect_source", path=unauthorized, start=0)
    call = ModelToolCall(
        "replace_source",
        json.dumps({"path": unauthorized, "old_text": "", "new_text": "VALUE = 2\n"}),
        "unauthorized",
    )
    with pytest.raises(PatchProposalError, match="Unauthorized"):
        admit_observed(root, {task.source: ns["BASE"]}, (call,), tools)
    assert not (root / unauthorized).exists()
    (root / task.source).unlink()
    with pytest.raises(FilesystemNotFoundError):
        tools.check_current()
