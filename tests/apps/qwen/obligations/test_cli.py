# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- literal authorized CLI fixtures
"""Actual CLI, Checkout custody and independent shared-check consumers."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any

import pytest

from scripts.backlog.coordinator import git
from scripts.qwen import coding_worker as cli
from tests.apps.qwen.obligations.test_native import (
    EDIT,
    Scripted,
    frame,
    member,
    obligation,
    read,
)
from tests.apps.qwen.test_coding_loop import (
    _TINY_OLD,
    _TINY_SOURCE,
    _TINY_TYPED_GOOD,
    _tiny_task,
)

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelInteraction


async def local_task(root: Path) -> CodingTask:
    """Create tiny independent source and administrative custody prerequisites."""
    task = await _tiny_task(root, native=True)
    backlog = root / "docs/backlog"
    backlog.mkdir(parents=True)
    (backlog / "overview.md").write_text("# Authored fixture backlog\n")
    await git(root, "config", "devtools.backlogCoordinator", str(root))
    await git(root, "branch", "-m", "feat/host")
    await git(root, "add", "--", "docs/backlog/overview.md")
    await git(
        root,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@localhost",
        "commit",
        "-m",
        "Authored local administration",
    )
    return replace(
        task,
        baseline_revision=await git(root, "rev-parse", "HEAD"),
        quality_checks=True,
        command_tools=True,
        maximum_calls=4,
        maximum_proposals=1,
    )


@pytest.mark.parametrize("foreign", [False, True])
def test_actual_cli_binds_frame_before_provider_and_preserves_closeout_authority(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, foreign: bool
) -> None:
    """Reach actual entrypoint, custody, native checks, currentness and return code."""
    root = tmp_path / "task"
    task = asyncio.run(local_task(root))
    selected = frame(task, [obligation("owner", [member()])])
    if foreign:
        selected = replace(selected, task_definition_sha256="0" * 64)
    definition = root / ".local/task.json"
    definition.parent.mkdir()
    definition.write_text(json.dumps(asdict(task)))
    frame_file = root / ".local/frame.json"
    frame_file.write_text(json.dumps(selected.to_dict()))
    folder = root / ".local/run"
    model = Scripted([read(), EDIT, ("check_changes", {})])
    factories: list[str] = []

    async def factory(_root: Path) -> tuple[ModelInteraction, dict[str, Any]]:
        factories.append("provider constructed")
        return model, {"model": "deterministic fixture"}

    monkeypatch.setattr(cli, "_ROOT", root)
    monkeypatch.setattr(cli, "local_interaction", factory)
    monkeypatch.setattr(
        "sys.argv",
        [
            "worker",
            "--task-definition",
            str(definition),
            "--obligation-frame",
            str(frame_file),
            "--report-directory",
            str(folder),
            "--observed-edits",
            "--check-changes-before-completion",
        ],
    )
    if foreign:
        with pytest.raises(SystemExit) as raised:
            asyncio.run(cli.main())
        assert raised.value.code == 2
        assert not factories
        assert not folder.exists()
        return
    assert asyncio.run(cli.main()) == 0
    result = json.loads((folder / "result.json").read_text())
    assert result["accepted"]
    assert result["change_check"]["ready_for_review"]
    assert result["change_check_freshness"]["current"]
    assert result["turns"][1]["obligation_context"]["readiness"] == "ready"
    assert result["turns"][1]["edit_context_assessment"]
    # A later read/check turn cannot automatically reapprove changed source.
    assert result["obligation_context"]["readiness"] == "blocked"
    assert result["obligation_frame_sha256"] == selected.sha256
    assert factories == ["provider constructed"]
    assert result["source_restored"]
    assert result["provenance"]["publication_authority"] == "NONE"
    assert (folder / "final-source.py").read_text() == _TINY_TYPED_GOOD
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD
    assert asyncio.run(git(root, "branch", "--show-current")) == "feat/host"
    assert not (root / ".local/backlog/checkout-owner").exists()
    assert not (root / ".local/backlog/work").exists()
