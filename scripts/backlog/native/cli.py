# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, E501 -- finite operational receipts and formatter compatibility
"""Native administrative entry; configured workers are injected by trusted hosts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from scripts.backlog.intake import load_json
from scripts.backlog.work import WorkCycle

if TYPE_CHECKING:
    import argparse


def confirm(value: dict[str, Any]) -> bool:
    """Require real host consent; never accept worker-supplied approval text."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise PermissionError(
            "Native authorization/review requires an interactive host terminal"
        )
    print(json.dumps(value, indent=2))  # noqa: T201 -- terminal decision
    try:
        return (
            input(
                "Approve exactly this native decision? No installation/publication authority. [y/N] "
            )
            .strip()
            .lower()
            == "y"
        )
    except (EOFError, KeyboardInterrupt):
        return False


def configure(commands: Any) -> None:  # noqa: ANN401, PLR0915 -- finite argparse boundary
    """Extend existing administration with finite native commands."""
    prepare = commands.add_parser("native-prepare")
    prepare.add_argument("item")
    prepare.add_argument("--branch", required=True)
    prepare.add_argument("--task", required=True)
    prepare.add_argument("--supervisor", required=True)
    preview = commands.add_parser("native-preview")
    preview.add_argument("item")
    approval = commands.add_parser("native-authorize")
    approval.add_argument("item")
    approval.add_argument("--reference", required=True)
    approval.add_argument("--expires", required=True)
    review = commands.add_parser("native-review")
    review.add_argument("item")
    review.add_argument("--reviewer", required=True)
    review.add_argument("--reference", required=True)
    review.add_argument("--rationale", required=True)
    review.add_argument("--decision", choices=("accept", "reject"), required=True)
    actor = commands.add_parser("native-review-prepare")
    actor.add_argument("item")
    actor.add_argument("--policy", required=True)
    actor = commands.add_parser("native-review-authorize")
    actor.add_argument("item")
    actor.add_argument(
        "--attempt", help="Exact prospective continuation subject SHA256"
    )
    actor.add_argument("--reference", required=True)
    actor.add_argument("--expires", required=True)
    actor = commands.add_parser("native-review-proposal")
    actor.add_argument("item")
    actor.add_argument("--attempt")
    actor = commands.add_parser("native-review-decide")
    actor.add_argument("item")
    actor.add_argument("--attempt")
    actor.add_argument("--proposal", required=True)
    actor.add_argument("--reference", required=True)
    actor.add_argument("--rationale", required=True)
    actor.add_argument("--decision", choices=("accept", "reject"), required=True)
    actor = commands.add_parser("native-review-continue")
    actor.add_argument("item")
    actor.add_argument(
        "--previous", required=True, help="Exact original blocked proposal SHA256"
    )
    actor.add_argument("--policy", required=True)
    actor.add_argument(
        "--correction", required=True, help="Trusted host correction provenance"
    )
    diagnostic = commands.add_parser("native-diagnostic-prepare")
    diagnostic.add_argument("item")
    diagnostic.add_argument("--archive", required=True)
    diagnostic.add_argument("--policy", required=True)
    diagnostic = commands.add_parser("native-diagnostic-authorize")
    diagnostic.add_argument("item")
    diagnostic.add_argument("--reference", required=True)
    diagnostic.add_argument("--expires", required=True)
    diagnostic = commands.add_parser("native-diagnostic-proposal")
    diagnostic.add_argument("item")


async def run(args: argparse.Namespace, root: Path) -> dict[str, Any]:  # noqa: PLR0911, C901 -- finite administrative commands
    """Prepare/inspect/approve/review only; integration planning has its own command."""
    native = WorkCycle(root).native
    if args.command == "native-diagnostic-prepare":
        return await native.diagnostic_reviewer.prepare(
            args.item,
            archive=args.archive,
            reviewer=load_json(
                resolve_path(args.policy, base_directory=Path.cwd()).value
            ),
        )
    if args.command == "native-diagnostic-authorize":
        return await native.diagnostic_reviewer.authorize(
            args.item,
            reference=args.reference,
            expires=Timestamp.from_isoformat(args.expires),
            authorize=confirm,
        )
    if args.command == "native-diagnostic-proposal":
        await native.diagnostic_reviewer.current(args.item)
        return native.diagnostic_reviewer.record(args.item, "proposal")
    if args.command == "native-review-prepare":
        return await native.reviewer.prepare(
            args.item,
            reviewer=load_json(
                resolve_path(args.policy, base_directory=Path.cwd()).value
            ),
        )
    if args.command == "native-review-continue":
        return await native.reviewer.prepare_continuation(
            args.item,
            previous=args.previous,
            reviewer=load_json(
                resolve_path(args.policy, base_directory=Path.cwd()).value
            ),
            correction_reference=args.correction,
        )
    if args.command == "native-review-authorize":
        return await native.reviewer.select(args.attempt).authorize(
            args.item,
            reference=args.reference,
            expires=Timestamp.from_isoformat(args.expires),
            authorize=confirm,
        )
    if args.command == "native-review-proposal":
        owner = native.reviewer.select(args.attempt)
        await owner.current(args.item)
        return owner.record(args.item, "proposal")
    if args.command == "native-review-decide":
        return await native.reviewer.select(args.attempt).decide(
            args.item,
            proposal=args.proposal,
            accept=args.decision == "accept",
            reference=args.reference,
            rationale=args.rationale,
            authorize=confirm,
        )
    if args.command == "native-prepare":
        return await native.prepare(
            args.item,
            branch=args.branch,
            task=load_json(resolve_path(args.task, base_directory=Path.cwd()).value),
            supervisor=args.supervisor,
        )
    if args.command == "native-preview":
        packet = native.record(args.item, "assignment")
        await native.validate(packet)
        return {
            "assignment": packet,
            "authority": "preparation-only; no dispatch or integration authority",
        }
    if args.command == "native-authorize":
        return await native.authorize(
            args.item,
            reference=args.reference,
            expires=Timestamp.from_isoformat(args.expires),
            authorize=confirm,
        )
    if args.command == "native-review":
        return await native.review(
            args.item,
            reviewer=args.reviewer,
            reference=args.reference,
            rationale=args.rationale,
            accept=args.decision == "accept",
            authorize=confirm,
        )
    raise ValueError("Unsupported native administration command")
