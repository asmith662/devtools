# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- actual independent subprocess assertions
"""A separate non-Qwen/non-Codex host uses real source, Git and fixed checks."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor


@pytest.mark.parametrize("scenario", ["success", "failed", "unauthorized"])
def test_guarded_host(tmp_path: Path, scenario: str) -> None:
    root = tmp_path / "worker space π & [host]"
    root.mkdir()
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args("-B", str(Path(__file__).with_name("independent_host.py")), scenario)
            .cwd(resolve_path(root))
            .with_timeout(Duration.seconds(30)),
        ),
    )
    assert result.exit_code == 0, result.stderr.decode()
    value = json.loads(result.stdout)
    assert value["model_calls"] == 0
    assert value["span"] == [0, 10]
    assert value["snapshot"]
    assert value["content"]
    assert value["denied"] == [
        "import:apps",
        "import:devtools.agents.integrations.codex",
        "file:apps/qwen/tasks.py",
    ]
    if scenario == "success":
        assert value["checks"] == [{"name": "behavior", "status": "passed", "exit": 0}]
        assert value["entered"] == 11
        assert (root / ".local/count").read_text() == "x"
        assert any(
            x["pattern"]["equivalent_tool"] == "tools.checks.FixedCheckTool"
            for x in value["patterns"]
        )
    elif scenario == "failed":
        assert value["checks"][0]["exit"] == 4
    else:
        assert value["checks"] == []
        assert not (root / ".local/count").exists()
