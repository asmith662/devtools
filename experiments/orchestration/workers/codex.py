# Copyright (c) 2026
# ruff: noqa: ANN401 -- installed CLI external-Agent boundary
"""Launch only fresh isolated Codex primaries with frozen model/configuration."""

from __future__ import annotations

import json
import shutil
from typing import TYPE_CHECKING, Any

from experiments.orchestration.storage import require
from experiments.orchestration.workers import runtime

if TYPE_CHECKING:
    from pathlib import Path


def executable(configuration: Any) -> str:
    """Resolve the frozen external CLI without constructing a model invocation."""
    executable = configuration.get("executable", "codex")
    return str(
        shutil.which("codex.cmd") or executable
        if executable == "codex"
        else executable,
    )


def argv(
    configuration: Any,
    workspace: Path,
    *,
    schema: Path | None = None,
    response: Path | None = None,
) -> list[str]:
    """Build the installed 0.162.1 stdin/schema interface; never resume/fork."""
    require(
        schema is not None and response is not None,
        "Host-owned response schema/capture required",
    )
    arguments = [
        executable(configuration),
        "--no-daemon",
        "-a",
        "never",
        "exec",
        "--ignore-user-config",
        "--ignore-rules",
        "--ephemeral",
        "--skip-git-repo-check",
        "--cd",
        str(workspace),
        "--model",
        configuration["model_id"],
        "-c",
        "model_reasoning_effort=" + json.dumps(configuration["reasoning"].lower()),
        "-c",
        'web_search="disabled"',
        "--json",
        "--output-schema",
        str(schema),
        "--output-last-message",
        str(response),
        "-",
    ]
    arguments[-1:-1] = runtime.overrides(configuration["runtime"], workspace)
    return arguments
