# Copyright (c) 2026
# ruff: noqa: INP001 -- supported operational entry point in existing scripts namespace
"""Project an explicitly selected bounded Codex JSONL file into safe candidates."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from typing import TYPE_CHECKING, cast

from devtools.agents.integrations.codex.commands import CodexCommandObserver
from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.core.paths import resolve_path
from devtools.observability.commands.models import CommandOrigin
from devtools.observability.commands.patterns import summarize_patterns
from devtools.resources.filesystem import BinaryFile, FileFormat, read

if TYPE_CHECKING:
    from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """Read only the supplied file; never find personal sessions or invoke Codex."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events")
    parser.add_argument("--agent", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args(argv)
    bound = 4 << 20
    data = cast(
        "BinaryFile",
        read(
            resolve_path(args.events),
            file_format=FileFormat.BINARY,
            max_bytes=bound + 1,
        ),
    ).content
    if len(data) > bound:
        msg = "Selected command observation input exceeds its byte bound."
        raise ValueError(msg)
    observer = CodexCommandObserver(
        CommandOrigin(args.agent, args.task, args.run, "codex"),
    )
    for index, line in enumerate(line for line in data.splitlines() if line.strip()):
        if line.strip():
            try:
                observer.feed(line)
            except CodexOutputError:
                # The report retains a bounded issue count and known earlier facts.
                if index >= observer.maximum_records:
                    break
    report = observer.report()
    print(  # noqa: T201 -- explicit operator output
        json.dumps(
            {
                "patterns": [
                    asdict(p) for p in summarize_patterns(report.observations)
                ],
                "malformed_records": report.malformed_records,
                "terminal_observed": report.terminal_observed,
                "coverage": (
                    "available CLI reports only; process entry and "
                    "feed completeness unknown"
                ),
                "authority": (
                    "diagnostic candidates only; no execution or promotion authority"
                ),
            },
        ),
    )
    return int(bool(report.malformed_records))


if __name__ == "__main__":
    raise SystemExit(main())
