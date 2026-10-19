# Copyright (c) 2026
# ruff: noqa: T201, EM101, TRY003, COM812 -- local operator-facing CLI
"""Run as ``uv run python -m scripts.backlog`` from the repository root."""

from __future__ import annotations

import argparse
import asyncio
import getpass
import json
import sys
from functools import partial
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem.errors import FilesystemError
from scripts.backlog.coordinator import designate, locate
from scripts.backlog.intake import DOMAINS, Intake, load_json
from scripts.backlog.work import WorkCycle, task_from_dict


def confirm(request: dict[str, Any]) -> bool:
    """Trusted local operator boundary, default No; never read model consent."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise PermissionError(
            "Review/publication requires a genuine interactive terminal"
        )
    print(json.dumps(request, indent=2))
    try:
        return (
            input(
                "Authorize this exact backlog-only decision/publication? "
                "No implementation authority. [y/N] "
            )
            .strip()
            .lower()
            == "y"
        )
    except (EOFError, KeyboardInterrupt):
        return False


def confirm_work(request: dict[str, Any]) -> bool:
    """Separate exact implementation consent; never inherit backlog approval."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise PermissionError(
            "Implementation requires genuine interactive terminal consent"
        )
    if request["grant"]["principal"] != getpass.getuser():
        raise PermissionError("Local host principal differs from implementation grant")
    print(json.dumps(request, indent=2))
    try:
        return (
            input(
                "Authorize this exact bounded local Qwen assignment? "
                "No commit/merge/push authority. [y/N] "
            )
            .strip()
            .lower()
            == "y"
        )
    except (EOFError, KeyboardInterrupt):
        return False


async def _work(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    cycle = WorkCycle(root)
    match args.command:
        case "work-prepare":
            return await cycle.prepare(
                args.item,
                target=resolve_path(args.target, base_directory=Path.cwd()).value,
                branch=args.branch,
                task=task_from_dict(
                    load_json(
                        resolve_path(
                            args.task_definition, base_directory=Path.cwd()
                        ).value
                    )
                ),
            )
        case "work-authorize":
            return await cycle.authorize(
                args.item,
                principal=getpass.getuser(),
                reference=args.reference,
                expires_at=Timestamp.from_isoformat(args.expires),
                authorize=confirm_work,
            )
        case "work-execute":
            from scripts.qwen.coding_worker import local_interaction  # noqa: PLC0415

            return await cycle.execute(
                args.item,
                interaction_factory=partial(local_interaction, root),
                authorize=confirm_work,
            )
        case "work-discover":
            payload = load_json(
                resolve_path(args.input, base_directory=Path.cwd()).value
            )
            return {
                "proposal": await cycle.discover(args.item, payload),
                "state": "PENDING_REVIEW",
            }
        case "work-status":
            return cycle.status(args.item)
    raise ValueError("Unknown work operation")


def main(arguments: list[str] | None = None) -> int:  # noqa: PLR0915 -- explicit local subcommands
    """Capture/list/show/advisory/review/promote within one explicit checkout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("designate")
    capture = commands.add_parser("capture")
    capture.add_argument(
        "input", help="JSON proposal with discovery/evidence references"
    )
    listing = commands.add_parser("list")
    listing.add_argument("--pending", action="store_true")
    show = commands.add_parser("show")
    show.add_argument("id")
    review = commands.add_parser("review")
    review.add_argument("id")
    review.add_argument(
        "--decision",
        choices=("ADVISORY", "APPROVED", "DEFERRED", "REJECTED"),
        required=True,
    )
    review.add_argument(
        "--reference", required=True, help="Actual decision/advice provenance"
    )
    review.add_argument("--rationale", required=True)
    review.add_argument(
        "--duplicates", required=True, help="Explicit reviewer duplicate disposition"
    )
    review.add_argument("--domain", choices=DOMAINS)
    review.add_argument(
        "--advisor", help="Advisory attribution only, never an authority principal"
    )
    promote = commands.add_parser("promote")
    promote.add_argument("id")
    prepare = commands.add_parser("work-prepare")
    prepare.add_argument("item")
    prepare.add_argument("--target", required=True)
    prepare.add_argument("--branch", required=True)
    prepare.add_argument("--task-definition", required=True)
    grant = commands.add_parser("work-authorize")
    grant.add_argument("item")
    grant.add_argument("--reference", required=True)
    grant.add_argument("--expires", required=True)
    commands.add_parser("work-execute").add_argument("item")
    commands.add_parser("work-status").add_argument("item")
    discovery = commands.add_parser("work-discover")
    discovery.add_argument("item")
    discovery.add_argument("input")
    args = parser.parse_args(arguments)
    try:
        root = resolve_path(args.root, base_directory=Path.cwd()).value
        if args.command.startswith("work-"):
            work_result = asyncio.run(_work(args, root))
            print(json.dumps(work_result, indent=2))
            return (
                1
                if work_result.get("disposition")
                in {"ESCALATION_REQUIRED", "RECONCILIATION_REQUIRED"}
                else 0
            )
        if args.command == "designate":
            print(asyncio.run(designate(root, authorize=confirm)))
            return 0
        coordinator = (
            asyncio.run(locate(root))
            if args.command in {"capture", "review", "promote"}
            else None
        )
        intake = Intake(root, coordinator=coordinator)
        match args.command:
            case "capture":
                identity = intake.capture(
                    load_json(resolve_path(args.input, base_directory=Path.cwd()).value)
                )
                result: Any = {
                    "id": identity,
                    "state": "PENDING_REVIEW",
                    "duplicates": intake.duplicates(identity),
                }
            case "list":
                result = intake.queue()
                if args.pending:
                    result["proposals"] = [
                        p for p in result["proposals"] if p["state"] == "PENDING_REVIEW"
                    ]
            case "show":
                result = {
                    **intake.get(args.id),
                    "duplicates": intake.duplicates(args.id),
                }
            case "review":
                result = intake.review(
                    args.id,
                    decision=args.decision,
                    reviewer=(args.advisor or "unattributed advisor")
                    if args.decision == "ADVISORY"
                    else getpass.getuser(),
                    reference=args.reference,
                    rationale=args.rationale,
                    duplicate_disposition=args.duplicates,
                    domain=args.domain,
                    authorize=confirm,
                )
            case "promote":
                result = {
                    "backlog_id": intake.promote(args.id, authorize=confirm),
                    "execution_authorization": "NONE",
                }
        print(json.dumps(result, indent=2))
        return 1 if isinstance(result, dict) and result.get("errors") else 0
    except (ValueError, KeyError, TypeError, OSError, FilesystemError) as error:
        print(f"Backlog intake refused: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
