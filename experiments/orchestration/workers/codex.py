# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- installed CLI external-Agent boundary
"""Launch only fresh isolated Codex primaries with frozen model/configuration."""

from __future__ import annotations

import json
import shutil
from typing import TYPE_CHECKING, Any

from experiments.orchestration.storage import require, safe

if TYPE_CHECKING:
    from pathlib import Path


def argv(configuration: Any, workspace: Path) -> list[str]:
    """Build the installed 0.162.1 fresh exec interface; never resume/fork."""
    executable = configuration.get("executable", "codex")
    executable = (
        shutil.which("codex.cmd") or executable if executable == "codex" else executable
    )
    instruction = safe(workspace, configuration["prompt_file"])
    require(instruction.is_file(), "Frozen instruction artifact missing")
    prompt = (
        "Authenticate this case's packet. Read "
        + configuration["prompt_file"]
        + ". Perform exactly one primary adjudication under that authoritative contract; validate the required scientific artifacts, preserve packet bytes, and stop. Do not access any external case/repository/history or another review."
    )
    return [
        executable,
        "--no-daemon",
        "-a",
        "never",
        "exec",
        "--ignore-user-config",
        "--ignore-rules",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--cd",
        str(workspace),
        "--model",
        configuration["model_id"],
        "-c",
        "model_reasoning_effort=" + json.dumps(configuration["reasoning"].lower()),
        "-c",
        'web_search="disabled"',
        "--json",
        prompt,
    ]
