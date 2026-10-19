# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, T201 -- explicit operator/admin boundary
"""Existing backlog CLI's concrete integration subcommands."""

from __future__ import annotations

import getpass
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.commands import CommandError
from devtools.resources.filesystem.errors import FilesystemError
from scripts.backlog.coordinator import git
from scripts.backlog.intake import load_json
from scripts.backlog.work import WorkCycle

if TYPE_CHECKING:
    import argparse


def confirm(request: dict[str, Any]) -> bool:
    """Authenticate one genuine local-host integration/protection decision."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise PermissionError(
            "Integration policy requires a genuine interactive terminal"
        )
    if (
        request.get("grant", {"principal": getpass.getuser()})["principal"]
        != getpass.getuser()
    ):
        raise PermissionError("Integration policy principal differs from local host")
    print(json.dumps(request, indent=2))
    try:
        return (
            input("Authorize exactly this integration policy decision? [y/N] ")
            .strip()
            .lower()
            == "y"
        )
    except (KeyboardInterrupt, EOFError):
        return False


def configure(commands: Any) -> None:  # noqa: ANN401 -- argparse subparser boundary
    """Add fixed integration commands without another command framework."""
    issue = commands.add_parser("integration-issue")
    issue.add_argument("--policy", required=True)
    issue.add_argument("--reference", required=True)
    issue.add_argument("--expires", required=True)
    revoke = commands.add_parser("integration-revoke")
    revoke.add_argument("grant")
    revoke.add_argument("--reference", required=True)
    protect = commands.add_parser("integration-protection")
    protect.add_argument("--remote", required=True)
    protect.add_argument("--destination", required=True)
    protect.add_argument("--reference", required=True)
    protect.add_argument("--allow", action="store_true")
    plan = commands.add_parser("integration-plan")
    plan.add_argument("item")
    plan.add_argument("--review", required=True)
    plan.add_argument("--spec", required=True)
    status = commands.add_parser("integration-status")
    status.add_argument("item")
    status.add_argument("plan")
    for operation in (
        "install",
        "validate",
        "review",
        "publish",
        "promote",
        "verify",
        "close-review",
        "closeout",
    ):
        parser = commands.add_parser("integration-" + operation)
        parser.add_argument("item")
        parser.add_argument("plan")
        parser.add_argument("--grant", required=True)
        if operation in {"review", "close-review"}:
            parser.add_argument("--decision", required=True)
            parser.add_argument("--reference", required=True)
            parser.add_argument("--rationale", required=True)


async def run(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    """Retain bounded operational refusals alongside the existing phase evidence."""
    try:
        return await _run(args, root)
    except (
        ValueError,
        KeyError,
        TypeError,
        OSError,
        FilesystemError,
        CommandError,
    ) as error:
        if hasattr(args, "item") and hasattr(args, "plan"):
            cycle = WorkCycle(root)
            try:
                await cycle._coordinator()  # noqa: SLF001
                cycle.integration.refusal(args.item, args.plan, args.command, error)
            except (
                ValueError,
                KeyError,
                TypeError,
                OSError,
                FilesystemError,
            ) as record_error:
                print(
                    f"Refusal evidence could not be recorded: {record_error}",
                    file=sys.stderr,
                )
        raise ValueError(str(error)) from error


async def _run(args: argparse.Namespace, root: Path) -> dict[str, Any]:  # noqa: C901, PLR0911, PLR0912 -- closed commands
    """Route through WorkCycle; no model, shell or publication fallback."""
    cycle = WorkCycle(root)
    integration = cycle.integration
    match args.command:
        case "integration-issue":
            return await integration.authority.issue(
                load_json(resolve_path(args.policy, base_directory=Path.cwd()).value),
                reference=args.reference,
                expires=Timestamp.from_isoformat(args.expires),
                authorize=confirm,
            )
        case "integration-revoke":
            return await integration.authority.revoke(
                args.grant, reference=args.reference, authorize=confirm
            )
        case "integration-protection":
            await cycle._coordinator()  # noqa: SLF001
            await git(root, "remote", "get-url", args.remote)
            await git(root, "check-ref-format", "refs/heads/" + args.destination)
            value = args.remote + ":" + args.destination
            request = {
                "principal": getpass.getuser(),
                "operation": "repository-protected-promotion-policy",
                "target": value,
                "allow": args.allow,
                "reference": args.reference,
            }
            if not args.reference.strip() or not confirm(request):
                raise PermissionError("Repository protection policy consent required")
            with cycle.intake._writer():  # noqa: SLF001
                values = (
                    await git(
                        root,
                        "config",
                        "--get-all",
                        "devtools.integrationProtectedTarget",
                        missing_ok=True,
                    )
                ).splitlines()
                if args.allow and value not in values:
                    await git(
                        root,
                        "config",
                        "--local",
                        "--add",
                        "devtools.integrationProtectedTarget",
                        value,
                    )
                elif not args.allow and value in values:
                    await git(
                        root,
                        "config",
                        "--local",
                        "--fixed-value",
                        "--unset-all",
                        "devtools.integrationProtectedTarget",
                        value,
                    )
            return request
        case "integration-plan":
            return await integration.plan(
                args.item,
                args.review,
                load_json(resolve_path(args.spec, base_directory=Path.cwd()).value),
            )
        case "integration-status":
            return integration.status(args.item, args.plan)
        case "integration-review":
            return await integration.review(
                args.item,
                args.plan,
                args.grant,
                decision=args.decision,
                reference=args.reference,
                rationale=args.rationale,
            )
        case "integration-close-review":
            return await integration.close_review(
                args.item,
                args.plan,
                args.grant,
                decision=args.decision,
                reference=args.reference,
                rationale=args.rationale,
            )
        case "integration-install":
            return await integration.install(args.item, args.plan, args.grant)
        case "integration-validate":
            return await integration.validate(args.item, args.plan, args.grant)
        case "integration-publish":
            return await integration.publish(args.item, args.plan, args.grant)
        case "integration-promote":
            return await integration.promote(args.item, args.plan, args.grant)
        case "integration-verify":
            return await integration.verify(args.item, args.plan, args.grant)
        case "integration-closeout":
            return await integration.closeout(args.item, args.plan, args.grant)
    raise ValueError("Unknown integration operation")
