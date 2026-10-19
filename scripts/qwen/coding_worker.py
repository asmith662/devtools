# Copyright (c) 2026
# ruff: noqa: E402, INP001, T201 -- concrete local entrypoint
"""Run a bounded local coding evaluation; production publication is separate."""

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
from apps.qwen.tasks import TASK_NAMES, select_task
from devtools.core.paths import PathError, resolve_path
from devtools.models.interaction import InteractionSource
from devtools.models.interaction.providers import LlamaCppInteraction
from devtools.resources.filesystem import FilesystemError
from scripts.backlog.checkout import Checkout
from scripts.backlog.coordinator import git
from scripts.backlog.intake import load_json
from scripts.backlog.work import WorkCycle, task_from_dict
from scripts.qwen.llama_cpp_profile import QWEN38_27B_UD_IQ4_XS
from scripts.qwen.patch_proposal_worker_acceptance import _qwen_status

if TYPE_CHECKING:
    from apps.qwen.tasks import CodingTask
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


def report_directory(value: str | Path) -> Path:
    """Resolve a new evidence directory before service or source operations."""
    folder = resolve_path(value, base_directory=Path.cwd()).value
    try:
        folder.stat()
    except FileNotFoundError:
        pass
    else:
        message = "Report directory must not already exist."
        raise ValueError(message)
    existing_parent = next(parent for parent in folder.parents if parent.exists())
    if not existing_parent.is_dir():
        message = "Report directory has a non-directory parent."
        raise ValueError(message)
    return folder


async def run_local_task(
    root: Path,
    folder: Path,
    *,
    task: CodingTask,
    branch: str | None = None,
) -> dict[str, Any]:
    """Trusted host invocation authorizes this local evaluation, not publication.

    Checkout supplies serialization/recovery. No approved backlog item, standing
    grant or WorkCycle assignment is consulted/created. Never let model-provided
    data select the host task or validation commands.
    """
    folder = report_directory(folder)
    cycle = WorkCycle(root)
    selected = branch or "feat/qwen-local-" + task.definition_sha256[:12]
    if not selected.startswith("feat/"):
        message = "Local evaluation requires an ordinary feature branch."
        raise PermissionError(message)
    source = await cycle._baseline(  # noqa: SLF001 -- existing exact Git binding
        task,
        task.source,
        dict(task.baseline_hashes)[task.source],
    )
    worker_head = await git(root, "rev-parse", "HEAD")
    async with Checkout(
        cycle,
        "local-evaluation:" + task.definition_sha256,
        selected,
        task.baseline_revision,
        files=[{"path": task.source, "text": source}],
        create=True,
    ) as owner:
        interaction, provenance = await local_interaction(root)
        provenance.update(
            worker_source_head=worker_head,
            execution_category="trusted-local-development-evaluation",
            publication_authority="NONE",
        )
        return await run_coding_task(
            root,
            folder,
            interaction,
            task=task,
            provenance=provenance,
            admit_edit=owner.expect,
        )


async def main() -> int:
    """Invoke one constrained local task without production approval rituals."""
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--task", choices=TASK_NAMES, default="markdown-fences")
    selection.add_argument(
        "--task-definition",
        help="Trusted host CodingTask JSON; never accept model-authored configuration.",
    )
    parser.add_argument(
        "--report-directory",
        required=True,
        help=(
            "New report directory; relative paths resolve against "
            "the current working directory."
        ),
    )
    parser.add_argument("--branch", help="Optional ordinary feature source branch.")
    args = parser.parse_args()
    try:
        task = (
            task_from_dict(
                load_json(
                    resolve_path(
                        args.task_definition,
                        base_directory=Path.cwd(),
                    ).value,
                ),
            )
            if args.task_definition
            else select_task(args.task)
        )
    except (
        PathError,
        ValueError,
        TypeError,
        KeyError,
        FilesystemError,
        OSError,
    ) as error:
        parser.error(f"Invalid host task definition: {error}")
    args.task = task.name
    try:
        args.report_directory = report_directory(args.report_directory)
    except (PathError, ValueError, OSError) as error:
        parser.error(f"Invalid report directory: {error}")
    try:
        result = await run_local_task(
            _ROOT,
            args.report_directory,
            task=task,
            branch=args.branch,
        )
    except RuntimeError:
        print("MODEL_SERVICE_NOT_READY_OR_PROFILE_CHANGED; no model invocation")
        return 2
    print(
        f"{result['disposition']}; calls: {len(result['turns'])}; "
        f"elapsed: {result['elapsed_seconds']:.2f}s; "
        f"report: {args.report_directory / 'result.json'}",
    )
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
