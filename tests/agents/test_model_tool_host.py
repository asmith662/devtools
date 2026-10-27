# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independent literal host assertions
"""Exercise real library composition in a process denied application access."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor


@pytest.mark.parametrize(
    "scenario",
    [
        "success",
        "unauthorized",
        "arguments",
        "stale",
        "foreign-source",
        "missing-id",
        "duplicate-id",
        "check-failed",
        "cancel-admission",
        "lost-result",
        "cancel-effect",
        "tool-exception",
        "partial-batch",
    ],
)
def test_independent_native_host(tmp_path: Path, scenario: str) -> None:
    host = Path(__file__).with_name("native_tool_host.py")
    actual = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args("-B", str(host), scenario)
            .cwd(resolve_path(tmp_path))
            .with_timeout(Duration.seconds(25)),
        ),
    )
    assert actual.exit_code == 0, actual.stderr.decode()
    result = json.loads(actual.stdout)
    assert result["usage"] is None
    assert result["content_identity"]
    assert result["snapshot"]
    assert "src" in result["framework_file"]
    assert result["denied"] == ["import:apps", "file:apps/qwen/tasks.py"]
    if scenario == "success":
        assert result["outcome"] == "success"
        assert result["model_calls"] == 3
        assert (
            result["shared_entries"] == result["feedback_ids"] == ["read-1", "check-1"]
        )
        assert result["check"] == {"exit_code": 0, "stdout": "checked:7\n"}
        assert result["source"] == "def answer():\n    return 7\n"
    else:
        assert result["outcome"] != "success"
        if scenario in {"unauthorized", "foreign-source", "missing-id", "duplicate-id"}:
            assert (
                result["shared_entries"]
                == result["feedback_ids"]
                == result["events"]
                == []
            )
        elif scenario in {"arguments", "stale", "cancel-admission"}:
            assert result["shared_entries"] == ["read-1"]
            assert result["events"] == result["feedback_ids"] == []
        elif scenario == "check-failed":
            assert result["check"] == {"exit_code": 9, "stdout": ""}
            assert result["feedback_ids"] == ["read-1"]
        else:
            assert result["shared_entries"] == ["read-1", "effect-2"]
            assert result["feedback_ids"] == ["read-1"]
            assert result["source"] == (
                "def answer():\n    return 7\n"
                if scenario == "tool-exception"
                else "known effect\n"
            )
            assert result["events"].count("effect-entered") == 1
        assert result["model_calls"] == (2 if scenario == "check-failed" else 1)
