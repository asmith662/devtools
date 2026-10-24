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
from scripts.backlog.delegation import Delegations
from scripts.backlog.intake import DOMAINS, Intake, load_json
from scripts.backlog.integration import cli as integration_cli
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


def confirm_delegation(request: dict[str, Any]) -> bool:
    """One genuine local-host issue/revocation decision, default No."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise PermissionError(
            "Standing delegation requires a genuine interactive terminal"
        )
    if request["grant"]["principal"] != getpass.getuser():
        raise PermissionError("Standing decision principal differs from local host")
    print(json.dumps(request, indent=2))
    try:
        return (
            input(
                "Authorize this exact standing delegation decision? "
                "No protected publication. [y/N] "
            )
            .strip()
            .lower()
            == "y"
        )
    except (EOFError, KeyboardInterrupt):
        return False


async def _work(args: argparse.Namespace, root: Path) -> dict[str, Any]:  # noqa: C901, PLR0911 -- explicit commands
    cycle = WorkCycle(root)
    match args.command:
        case "work-recover":
            from scripts.backlog.checkout import recover  # noqa: PLC0415

            if not sys.stdin.isatty() or not sys.stdout.isatty():
                raise PermissionError(
                    "Checkout recovery requires a genuine interactive terminal"
                )
            print(
                json.dumps(
                    load_json(root / ".local/backlog/checkout-owner/owner.json"),
                    indent=2,
                )
            )
            consent = (
                input(  # noqa: ASYNC250 -- deliberate trusted terminal boundary
                    "Confirm the recorded owner is stopped and restore only "
                    "authenticated temporary edits? No redispatch or authority "
                    "transfer. [y/N] "
                )
                .strip()
                .lower()
                == "y"
            )
            await recover(cycle, authorize=consent)
            return {"disposition": "CHECKOUT_RECOVERED", "dispatch_authorized": False}
        case "delegation-issue":
            return await Delegations(cycle).issue(
                load_json(resolve_path(args.policy, base_directory=Path.cwd()).value),
                principal=getpass.getuser(),
                reference=args.reference,
                expires_at=Timestamp.from_isoformat(args.expires),
                authorize=confirm_delegation,
            )
        case "delegation-revoke":
            return await Delegations(cycle).revoke(
                args.delegation,
                principal=getpass.getuser(),
                reference=args.reference,
                authorize=confirm_delegation,
            )
        case "delegation-check":
            from scripts.backlog.work import _load  # noqa: PLC0415

            assignment = _load(
                cycle._folder(args.item) / "assignment.json",  # noqa: SLF001
                "backlog-qwen-assignment-v1",
            )
            task = await cycle._validate(assignment)  # noqa: SLF001
            policy = load_json(
                resolve_path(args.policy, base_directory=Path.cwd()).value
            )
            Delegations.eligible(policy, assignment, task)
            return {
                "item": args.item,
                "policy_applicable": True,
                "execution_authorized": False,
                "reservation_created": False,
            }
        case "work-review":
            return await Delegations(cycle).review(
                args.item,
                args.delegation,
                reference=args.reference,
                rationale=args.rationale,
                disposition=args.decision,
                result_sha256=args.result_sha256,
            )
        case "work-delegate":
            return await Delegations(cycle).authorize(
                args.item, args.delegation, args.supervision
            )
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


def main(arguments: list[str] | None = None) -> int:  # noqa: C901, PLR0915 -- explicit local subcommands
    """Capture/list/show/advisory/review/promote within one explicit checkout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("designate")
    commands.add_parser("work-recover")
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
    issue = commands.add_parser("delegation-issue")
    issue.add_argument("--policy", required=True)
    issue.add_argument("--reference", required=True)
    issue.add_argument("--expires", required=True)
    revoke = commands.add_parser("delegation-revoke")
    revoke.add_argument("delegation")
    revoke.add_argument("--reference", required=True)
    check = commands.add_parser("delegation-check")
    check.add_argument("item")
    check.add_argument("--policy", required=True)
    supervisory = commands.add_parser("work-review")
    supervisory.add_argument("item")
    supervisory.add_argument("--delegation", required=True)
    supervisory.add_argument("--reference", required=True)
    supervisory.add_argument("--rationale", required=True)
    supervisory.add_argument(
        "--decision",
        required=True,
        choices=(
            "APPROVE_ROUTINE",
            "ACCEPT_RECOMMENDED",
            "REWORK_RECOMMENDED",
            "ESCALATE",
            "REJECT",
        ),
    )
    supervisory.add_argument("--result-sha256")
    delegated = commands.add_parser("work-delegate")
    delegated.add_argument("item")
    delegated.add_argument("--delegation", required=True)
    delegated.add_argument("--supervision", required=True)
    discovery = commands.add_parser("work-discover")
    discovery.add_argument("item")
    discovery.add_argument("input")
    integration_cli.configure(commands)
    args = parser.parse_args(arguments)
    try:
        root = resolve_path(args.root, base_directory=Path.cwd()).value
        if args.command.startswith("integration-"):
            integration_result = asyncio.run(integration_cli.run(args, root))
            print(json.dumps(integration_result, indent=2))
            return (
                1
                if integration_result.get("disposition")
                in {
                    "REWORK_REQUIRED",
                    "POST_INTEGRATION_FAILED",
                    "RECONCILIATION_REQUIRED",
                    "BLOCKED",
                }
                else 0
            )
        if args.command.startswith(("work-", "delegation-")):
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
