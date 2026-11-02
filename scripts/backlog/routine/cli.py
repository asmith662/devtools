# Copyright (c) 2026
# ruff: noqa: T201, EM101, TRY003 -- actual operator control, default No
"""One-time policy control, separate from unattended per-task grants."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from scripts.backlog.intake import load_json

if TYPE_CHECKING:
    import argparse

    from scripts.backlog.work import WorkCycle


def configure(commands: Any) -> None:  # noqa: ANN401 -- argparse subparser contract
    """Expose explicit operator activation/replacement, inspection and stop controls."""
    activate = commands.add_parser("routine-activate")
    activate.add_argument("--policy", required=True)
    activate.add_argument("--reference", required=True)
    commands.add_parser("routine-show")
    revoke = commands.add_parser("routine-revoke")
    revoke.add_argument("--reference", required=True)
    deny = commands.add_parser("routine-deny")
    deny.add_argument("--subject", required=True)
    deny.add_argument("--reference", required=True)


def confirm(request: dict[str, Any]) -> bool:
    """Authenticate one actual operator decision; no response remains No."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise PermissionError("Policy control requires a genuine operator decision")
    print(json.dumps(request, indent=2))
    try:
        return (
            input("Authorize this standing policy control? [y/N] ").strip().lower()
            == "y"
        )
    except (EOFError, KeyboardInterrupt):
        return False


async def run(args: argparse.Namespace, cycle: WorkCycle) -> dict[str, Any]:
    """Reuse the coordinator and existing immutable writer; no execution follows."""
    await cycle._coordinator()  # noqa: SLF001
    if args.command == "routine-show":
        return {"controls": cycle.routine.controls(), "execution_started": False}
    return await cycle.routine.control(
        args.command.removeprefix("routine-"),
        reference=args.reference,
        policy=load_json(resolve_path(args.policy, base_directory=cycle.root).value)
        if args.command == "routine-activate"
        else None,
        subject=args.subject if args.command == "routine-deny" else None,
        authorize=confirm,
    )
