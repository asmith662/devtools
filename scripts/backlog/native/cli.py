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


def configure(commands: Any) -> None:  # noqa: ANN401 -- existing argparse boundary
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
    actor.add_argument("--reference", required=True)
    actor.add_argument("--expires", required=True)
    actor = commands.add_parser("native-review-proposal")
    actor.add_argument("item")
    actor = commands.add_parser("native-review-decide")
    actor.add_argument("item")
    actor.add_argument("--proposal", required=True)
    actor.add_argument("--reference", required=True)
    actor.add_argument("--rationale", required=True)
    actor.add_argument("--decision", choices=("accept", "reject"), required=True)


async def run(args: argparse.Namespace, root: Path) -> dict[str, Any]:  # noqa: PLR0911 -- finite administrative commands
    """Prepare/inspect/approve/review only; integration planning has its own command."""
    native = WorkCycle(root).native
    if args.command == "native-review-prepare":
        return await native.reviewer.prepare(
            args.item,
            reviewer=load_json(
                resolve_path(args.policy, base_directory=Path.cwd()).value
            ),
        )
    if args.command == "native-review-authorize":
        return await native.reviewer.authorize(
            args.item,
            reference=args.reference,
            expires=Timestamp.from_isoformat(args.expires),
            authorize=confirm,
        )
    if args.command == "native-review-proposal":
        await native.reviewer.current(args.item)
        return native.reviewer.record(args.item, "proposal")
    if args.command == "native-review-decide":
        return await native.reviewer.decide(
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
