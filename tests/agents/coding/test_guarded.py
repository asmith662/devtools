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


def test_guarded_projected_repair_uses_real_source_checks_and_custody(
    tmp_path: Path,
) -> None:
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args(
                "-B",
                str(Path(__file__).with_name("independent_host.py")),
                "repair",
                "--projection",
            )
            .cwd(resolve_path(tmp_path))
            .with_timeout(Duration.seconds(35)),
        ),
    )
    assert result.exit_code == 0, result.stderr.decode()
    value = json.loads(result.stdout)
    assert value["denied"] == ["import:apps", "file:apps/qwen/tasks.py"]
    assert value["accepted"]
    assert value["restored"]
    assert value["model_calls"] == 3
    assert value["apply_entries"] == ["apply", "apply"]
    assert value["feedback_ids"] == ["read-1", "edit-2", "repair-3"]
    assert [c[0]["exit"] for c in value["checks"]] == [1, 0]
    assert value["checks"][-1][0]["stdout"] == "checked:7\n"
    assert value["source"] == SOURCE
    assert value["usage"] == [None, None, None]
    assert value["projections"][-1]["status"] == "reduced"
    assert value["projections"][-1]["omitted"] == [[1, 3, "stale-source"]]


def test_guarded_semantic_repair_consumes_notes_and_exact_failed_check(
    tmp_path: Path,
) -> None:
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args(
                "-B",
                str(Path(__file__).with_name("independent_host.py")),
                "repair",
                "--projection",
                "--semantic",
            )
            .cwd(resolve_path(tmp_path))
            .with_timeout(Duration.seconds(35)),
        )
    )
    assert result.exit_code == 0, result.stderr.decode()
    value = json.loads(result.stdout)
    assert value["denied"] == ["import:apps", "file:apps/qwen/tasks.py"]
    assert value["accepted"]
    assert value["restored"]
    assert value["model_calls"] == 3
    assert value["summary_requests"] == 1
    assert value["apply_entries"] == ["apply", "apply"]
    assert [c[0]["exit"] for c in value["checks"]] == [1, 0]
    assert value["checks"][-1][0]["stdout"] == "checked:7\n"
    assert value["usage"] == [None, None, None]
    assert value["summaries"][0]["usage"] is None
    assert value["summaries"][0]["adopted"]
    assert value["summaries"][0]["after"] < value["summaries"][0]["before"]
    assert value["source"] == SOURCE
    assert "return 7" in value["archive"]["module.py"]
    assert value["feedback_ids"] == ["read-1", "edit-2", "repair-3"]
