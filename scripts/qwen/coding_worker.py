# Copyright (c) 2026
# ruff: noqa: E402, INP001, T201 -- concrete local entrypoint
"""Run one host-selected coding task after real terminal confirmation."""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Any

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from apps.qwen.coding_loop import run_coding_task
from apps.qwen.development_task import _command
from apps.qwen.patch_proposal_worker import _read_text
from apps.qwen.tasks import TASK_NAMES, select_task
from devtools.core.paths import PathError, resolve_path
from devtools.models.interaction import InteractionSource
from devtools.models.interaction.providers import LlamaCppInteraction
from scripts.backlog.checkout import Checkout
from scripts.backlog.coordinator import git
from scripts.backlog.work import WorkCycle
from scripts.qwen.llama_cpp_profile import QWEN38_27B_UD_IQ4_XS
from scripts.qwen.patch_proposal_worker_acceptance import (
    _confirm_local_execution,
    _qwen_status,
)

if TYPE_CHECKING:
    from devtools.models.interaction import ModelInteraction


async def local_interaction(root: Path) -> tuple[ModelInteraction, dict[str, Any]]:
    """Check the existing local profile and construct its client; never invoke it."""
    status = await _qwen_status(root)
    if (
        status.get("state") != "READY"
        or not status.get("expected_fingerprint")
        or status.get("observed_fingerprint") != status.get("expected_fingerprint")
    ):
        message = "MODEL_SERVICE_NOT_READY_OR_PROFILE_CHANGED"
        raise RuntimeError(message)
    model = "qwen38-local"
    return LlamaCppInteraction(
        endpoint="http://127.0.0.1:8080",
        model=model,
        source=InteractionSource("qwen-coding-worker"),
    ), {
        "model": model,
        "endpoint": "http://127.0.0.1:8080",
        "profile": asdict(QWEN38_27B_UD_IQ4_XS),
        "service": status,
        "source_head": await _command(root, "git", "rev-parse", "HEAD"),
    }


async def main() -> int:
    """Confirm before service inspection, then dispatch at most one worker run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=TASK_NAMES, default="markdown-fences")
    parser.add_argument(
        "--report-directory",
        required=True,
        help=(
            "New report directory; relative paths resolve against "
            "the current working directory."
        ),
    )
    args = parser.parse_args()
    task = select_task(args.task)
    try:
        args.report_directory = resolve_path(
            args.report_directory,
            base_directory=Path.cwd(),
        ).value
        try:
            args.report_directory.stat()
        except FileNotFoundError:
            pass
        else:
            parser.error("Report directory must not already exist.")
        existing_parent = next(
            parent for parent in args.report_directory.parents if parent.exists()
        )
        if not existing_parent.is_dir():
            parser.error("Report directory has a non-directory parent.")
    except (PathError, ValueError, OSError) as error:
        parser.error(f"Invalid report directory: {error}")
    # This caller deliberately offers no noninteractive authorization switch.
    # The maintainer runs it in a real terminal and answers the default-No prompt.
    args.freeze_only = False
    args.authorize_local_execution = False
    args.coding_loop = True
    args.structured_edit = True
    args.model = "qwen38-local"
    args.report_path = args.report_directory
    args.task_objective = task.name + ": " + task.objective
    _confirm_local_execution(args)
    try:
        interaction, provenance = await local_interaction(_ROOT)
    except RuntimeError:
        print("MODEL_SERVICE_NOT_READY_OR_PROFILE_CHANGED; no model invocation")
        return 2
    cycle = WorkCycle(_ROOT)
    branch = await git(_ROOT, "branch", "--show-current")
    await cycle._target(_ROOT, branch, task)  # noqa: SLF001 -- same concrete host boundary
    source = _read_text(resolve_path(_ROOT / task.source)).content
    async with Checkout(
        cycle,
        "manual-coding:" + task.definition_sha256,
        branch,
        task.baseline_revision,
        files=[{"path": task.source, "text": source}],
    ) as owner:
        result = await run_coding_task(
            _ROOT,
            args.report_directory,
            interaction,
            task=task,
            provenance=provenance,
            admit_edit=owner.expect,
        )
    print(
        f"{result['disposition']}; calls: {len(result['turns'])}; "
        f"elapsed: {result['elapsed_seconds']:.2f}s; "
        f"report: {args.report_directory / 'result.json'}",
    )
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
