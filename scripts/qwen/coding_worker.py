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

from apps.qwen.coding_loop import preflight_coding_task, run_coding_task
from apps.qwen.development_task import _command
from apps.qwen.tasks import TASK_NAMES, select_task
from devtools.core.paths import PathError, resolve_path
from devtools.models.interaction import InteractionSource
from devtools.models.interaction.providers import LlamaCppInteraction
from devtools.resources.filesystem import FilesystemError, TextFile, write
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


async def run_local_task(  # noqa: PLR0913, C901 -- explicit bounded ownership/materialization options
    root: Path,
    folder: Path,
    *,
    task: CodingTask,
    branch: str | None = None,
    thinking_enabled: bool = False,
    coordinated_edits: bool = False,
    reasoning_effort: str | None = None,
) -> dict[str, Any]:
    """Trusted host invocation authorizes this local evaluation, not publication.

    Checkout supplies serialization/recovery. No approved backlog item, standing
    grant or WorkCycle assignment is consulted/created. Never let model-provided
    data select the host task or validation commands.
    """
    if type(thinking_enabled) is not bool:
        message = "thinking_enabled must be an explicit host boolean"
        raise ValueError(message)
    if reasoning_effort is not None and not thinking_enabled:
        message = "Reasoning effort requires thinking enabled"
        raise ValueError(message)
    if (
        type(coordinated_edits) is not bool
        or ((task.additional_edit_paths or task.new_paths) and not coordinated_edits)
        or (coordinated_edits and task.context_mode != "on-demand")
    ):
        message = "Coordinated edits require explicit native scoped operation"
        raise ValueError(message)
    folder = report_directory(folder)
    cycle = WorkCycle(root)
    selected = branch or "feat/qwen-local-" + task.definition_sha256[:12]
    if not selected.startswith("feat/"):
        message = "Local evaluation requires an ordinary feature branch."
        raise PermissionError(message)
    sources = {
        p: await cycle._baseline(task, p, dict(task.baseline_hashes)[p])  # noqa: SLF001 -- existing exact Git binding
        for p, _ in task.baseline_hashes
    }
    for p in task.new_paths:
        if (root / p).exists() or not (root / p).parent.is_dir():
            message = "New source must be absent under existing parent"
            raise ValueError(message)
    worker_head = await git(root, "rev-parse", "HEAD")
    async with Checkout(
        cycle,
        "local-evaluation:" + task.definition_sha256,
        selected,
        task.baseline_revision,
        files=[{"path": p, "text": text} for p, text in sources.items()]
        + [{"path": p, "text": ""} for p in task.new_paths],
        create=True,
    ) as owner:
        originals = {p: (root / p).read_bytes().decode("utf-8") for p in sources}
        try:
            for path, text in sources.items():
                if originals[path].replace("\r\n", "\n") != text.replace("\r\n", "\n"):
                    message = (
                        "Frozen baseline differs beyond Git line-ending materialization"
                    )
                    raise ValueError(message)
                owner.expect(path, originals[path])
                if originals[path] != text:
                    write(TextFile(resolve_path(root / path), text))
            interaction, provenance = await local_interaction(root)
            provenance.update(
                worker_source_head=worker_head,
                execution_category="trusted-local-development-evaluation",
                publication_authority="NONE",
                baseline_materialization={
                    p: "exact frozen bytes; original checkout bytes restored"
                    for p in sources
                    if originals[p] != sources[p]
                },
            )
            return await run_coding_task(
                root,
                folder,
                interaction,
                task=task,
                provenance=provenance,
                admit_edit=owner.expect,
                thinking_enabled=thinking_enabled,
                coordinated_edits=coordinated_edits,
                reasoning_effort=reasoning_effort,
            )
        finally:
            for path, text in originals.items():
                current = (root / path).read_bytes().decode("utf-8")
                # Never overwrite an unknown semantic change during recovery.
                if current.replace("\r\n", "\n") == sources[path].replace("\r\n", "\n"):
                    write(TextFile(resolve_path(root / path), text))


async def main() -> int:  # noqa: C901 -- closed local run/closeout entrypoint
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
    parser.add_argument(
        "--closeout",
        action="store_true",
        help="Validate an accepted local result through WorkCycle.integration; "
        "no inference.",
    )
    parser.add_argument(
        "--expected-head",
        help="Exact current feature HEAD for closeout.",
    )
    parser.add_argument(
        "--review-json",
        help="Trusted supervisory review of the exact closeout subject.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Explicit trusted feature commit effect; no protected promotion.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Publish that exact reviewed ordinary feature commit.",
    )
    parser.add_argument(
        "--thinking",
        choices=("disabled", "enabled"),
        default="disabled",
        help="Per-request local template setting; default unchanged.",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help=(
            "Exact baseline, regression/quality/type checks; no inference. "
            "Engineering review remains required."
        ),
    )
    parser.add_argument(
        "--coordinated-edits",
        action="store_true",
        help=(
            "Atomic observed/versioned multi-region edits with "
            "host-allowlisted API inspection."
        ),
    )
    parser.add_argument("--reasoning-effort", choices=("low", "medium", "xhigh"))
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
    if args.closeout:
        if not args.expected_head or args.preflight_only:
            parser.error("Closeout requires --expected-head and excludes preflight")
        cycle = WorkCycle(_ROOT)
        result = await cycle.integration.closeout_local(
            task,
            resolve_path(args.report_directory, base_directory=Path.cwd()).value,
            branch=args.branch or await git(_ROOT, "branch", "--show-current"),
            expected_head=args.expected_head,
            review=load_json(
                resolve_path(args.review_json, base_directory=Path.cwd()).value,
            )
            if args.review_json
            else None,
            commit=args.commit,
            push=args.push,
        )
        print(result["disposition"])
        return 0 if result["validation"]["accepted"] else 1
    if args.commit or args.push or args.review_json or args.expected_head:
        parser.error("Publication/review options require --closeout")
    try:
        args.report_directory = report_directory(args.report_directory)
    except (PathError, ValueError, OSError) as error:
        parser.error(f"Invalid report directory: {error}")
    if args.preflight_only:
        result = await preflight_coding_task(_ROOT, args.report_directory, task=task)
        print(result["disposition"])
        return (
            0 if result["disposition"] == "PREFLIGHT_CHECKS_PASS_REVIEW_REQUIRED" else 1
        )
    options: dict[str, Any] = {}
    if args.thinking == "enabled":
        options["thinking_enabled"] = True
    if args.coordinated_edits:
        options["coordinated_edits"] = True
    if args.reasoning_effort:
        options["reasoning_effort"] = args.reasoning_effort
    try:
        result = await run_local_task(
            _ROOT,
            args.report_directory,
            task=task,
            branch=args.branch,
            **options,
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
