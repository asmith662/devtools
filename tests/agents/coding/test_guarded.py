# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, COM812 -- actual independent host boundary
"""A full coding workflow must succeed with application imports and files denied."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor
from tests.agents.coding.fixtures import SCENARIOS, SOURCE


@pytest.mark.parametrize("name", SCENARIOS)
def test_guarded_independent_coding_application(tmp_path: Path, name: str) -> None:
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args("-B", str(Path(__file__).with_name("independent_host.py")), name)
            .cwd(resolve_path(tmp_path))
            .with_timeout(Duration.seconds(35)),
        )
    )
    assert result.exit_code == 0, result.stderr.decode()
    value = json.loads(result.stdout)
    assert value["denied"] == ["import:apps", "file:apps/qwen/tasks.py"]
    assert value["accepted"] is (
        name in {"success", "repair", "completion-check", "two-edits"}
    )
    assert value["usage"] == [None] * value["model_calls"]
    if name == "repair":
        assert value["model_calls"] == 3
        assert value["apply_entries"] == ["apply", "apply"]
        assert [c[0]["exit"] for c in value["checks"]] == [1, 0]
        assert value["source"] == SOURCE
