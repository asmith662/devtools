# Copyright (c) 2026
# ruff: noqa: T201, EM101, TRY003, COM812 -- local operator-facing CLI
"""Run as ``uv run python -m scripts.backlog`` from the repository root."""

from __future__ import annotations

import argparse
import getpass
import json
import sys
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.resources.filesystem.errors import FilesystemError
from scripts.backlog.intake import DOMAINS, Intake, load_json


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


def main(arguments: list[str] | None = None) -> int:
    """Capture/list/show/advisory/review/promote within one explicit checkout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
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
    args = parser.parse_args(arguments)
    try:
        intake = Intake(resolve_path(args.root, base_directory=Path.cwd()).value)
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
