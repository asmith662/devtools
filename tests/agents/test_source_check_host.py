# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, COM812 -- literal independent consumer expectations
"""Run reusable source and fixed checks with application imports/files denied."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor

SCENARIOS = (
    "success",
    "foreign",
    "range",
    "partial",
    "stale",
    "stale-check",
    "unadmitted-check",
    "failed-check",
    "cancel-admission",
    "lost-ack",
    "cancel-effect",
    "incomplete-feedback",
)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_independent_source_and_check_host(tmp_path: Path, scenario: str) -> None:
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args(
                "-B",
                str(Path(__file__).with_name("scoped_check_host.py")),
                scenario,
            )
            .cwd(resolve_path(tmp_path))
            .with_timeout(Duration.seconds(25)),
        )
    )
    assert result.exit_code == 0, result.stderr.decode()
    value = json.loads(result.stdout)
    assert value["denied"] == ["import:apps", "file:apps/qwen/tasks.py"]
    assert value["usage"] is None
    assert value["scope"]
    assert "src" in value["framework"]
    if scenario == "success":
        assert value["outcome"] == "success"
        assert value["model_calls"] == 3
        assert value["feedback"] == ["region-1", "check-2"]
        assert value["check"] == {
            "exit_code": 0,
            "stdout": "checked:7\n",
            "current": True,
        }
    elif scenario == "partial":
        assert value["outcome"] == "partial-acquisition"
        assert value["disclosure"]["text"] == "def a"
        assert value["disclosure"]["partial"] is True
        assert value["check_entries"] == []
    else:
        assert value["outcome"] == "refused-or-incomplete"
        assert value["model_calls"] <= 2
        assert value["feedback"] == (
            ["region-1"]
            if scenario
            in {
                "stale-check",
                "unadmitted-check",
                "failed-check",
                "lost-ack",
                "cancel-effect",
            }
            else []
        )
    if scenario in {"success", "failed-check", "lost-ack", "cancel-effect"}:
        assert len(value["check_entries"]) == 1
        assert value["check_entries"][0][:3] == [sys.executable, "-I", "-B"]
    else:
        assert value["check_entries"] == []
    assert value["effect"] is (scenario in {"lost-ack", "cancel-effect"})
    if value["disclosure"] is not None:
        assert value["disclosure"]["requested"] == [12, 39]
        assert value["disclosure"]["content_identity"]
        assert value["disclosure"]["snapshot"] == value["scope"]
