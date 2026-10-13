# Copyright (c) 2026
# ruff: noqa: T201, ASYNC240, EM101, TRY003, COM812 -- bounded experiment I/O
"""Hard-wall managed child runner; never retries a timed-out verification."""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.commands.errors import CommandTimeoutError
from experiments.codex_dogfood.case_0009.artifacts import ROOT, json_bytes
from experiments.performance.retrieval.benchmark import publish


async def run(phase: str, output: Path, *, deep_limit: int = 120) -> None:
    """Keep timing/result records outside the immutable scientific case."""
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError("Bounded phase already recorded; no automatic retry")
    if deep_limit <= 0:
        raise ValueError("Deep wall must be positive")
    limit = 60 if phase == "verify" else deep_limit
    command = (
        Command(sys.executable)
        .args(
            "-X",
            "utf8",
            "-m",
            "experiments.codex_dogfood.verification.case_0016",
            phase,
            "--progress",
            str(output.with_suffix(".progress.json")),
        )
        .cwd(resolve_path(ROOT))
        .with_timeout(Duration.seconds(limit))
    )
    started = time.perf_counter_ns()
    record = {
        "phase": phase,
        "timestamp": Timestamp.now().isoformat(),
        "hard_wall_seconds": limit,
        "status": "RUNNING",
    }
    publish(output, record)
    try:
        result = await CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=16 * 1024 * 1024, max_stderr_bytes=1024 * 1024
            )
        ).execute(command)
        record.update(
            status="PASS" if result.exit_code == 0 else "FAILED",
            stdout=result.stdout.decode("utf-8"),
            stderr=result.stderr.decode("utf-8"),
            exit_code=result.exit_code,
        )
    except CommandTimeoutError as error:
        record.update(status="HARD_STOP; NOT_REPEATED", error=str(error))
    record["wall_ns"] = time.perf_counter_ns() - started
    publish(output, record)
    print(json_bytes(record).decode())


def main() -> None:
    """Launch exactly one managed child for the selected phase."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "phase",
        choices=(
            "native",
            "gold",
            "probe",
            "probe-profile",
            "construction",
            "verify",
            "deep",
        ),
    )
    parser.add_argument("output", type=Path)
    parser.add_argument("--deep-limit", type=int, default=120)
    args = parser.parse_args()
    asyncio.run(run(args.phase, args.output, deep_limit=args.deep_limit))


if __name__ == "__main__":
    main()
