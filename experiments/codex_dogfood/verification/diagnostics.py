# Copyright (c) 2026
# ruff: noqa: T201, EM101, TRY003, COM812, PLC0415, ASYNC240 -- bounded engineering measurement boundary
"""Representative exact-authentication measurements, separate from full verify."""

from __future__ import annotations

import argparse
import asyncio
import gc
import sys
import time
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator

from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.commands.errors import CommandTimeoutError
from experiments.codex_dogfood.case_0009.artifacts import ROOT, json_bytes, read_json
from experiments.codex_dogfood.case_0016.stage_b.authenticate import CAPTURE
from experiments.performance.retrieval.benchmark import publish

from .case_0016 import Invocation
from .journal import ArchiveMemo


@contextmanager
def collection_scope() -> Iterator[None]:
    """Restore interpreter collection state even when a diagnostic rejects input."""
    enabled = gc.isenabled()
    gc.disable()
    try:
        yield
    finally:
        start = time.perf_counter_ns()
        try:
            gc.collect()
        finally:
            if enabled:
                gc.enable()
        print(
            "scoped GC collection", (time.perf_counter_ns() - start) / 1e9, flush=True
        )


def measure(output: Path) -> None:
    """Measure a single child invocation with no state inherited from another."""
    with collection_scope():
        measured(output)


def measured(output: Path) -> None:
    """Report cold unique-state authentication and later envelope reuse honestly."""
    from experiments.performance.retrieval.workload import native_inputs

    invocation = Invocation()
    invocation.captured_bytes()
    values = native_inputs()
    archives = ArchiveMemo()
    implementation = {
        p.name: sha256(p.read_bytes()).hexdigest()
        for p in Path(__file__).parent.glob("*.py")
    }
    records = {
        read_json(p)["operation"]["identity"]: p
        for p in (CAPTURE / "operations").glob("*.returned.json")
    }
    ri = [k for k in records if k.startswith("ri:references:")]
    sizes = sorted(ri, key=lambda k: records[k].stat().st_size)
    graph = [k for k in records if k.startswith("graph:")]
    selected = [
        "frame:prepare",
        "lexical:index",
        sizes[0],
        sizes[-1],
        *graph,
        "query:Q1:A",
        "query:Q1:B",
        "query:Q1:C",
        "query:Q1:definitions",
    ]
    rows: list[dict[str, Any]] = []
    began = time.perf_counter_ns()
    for identity in selected:
        print(Timestamp.now().isoformat(), identity, "START", flush=True)
        publish(
            output,
            {
                "status": "RUNNING",
                "selected": selected,
                "returns": rows,
                "running": identity,
                "elapsed_ns": time.perf_counter_ns() - began,
            },
        )
        record = read_json(records[identity])
        start = time.perf_counter_ns()
        raw = archives.unpack(record["canonical"])
        decode = time.perf_counter_ns() - start
        memo = invocation.memo
        before = (memo.json_decodes, memo.recursive_visits, memo.blocks_checked)
        start = time.perf_counter_ns()
        passed = memo.corresponds(values[identity], raw)
        elapsed = time.perf_counter_ns() - start
        row = {
            "identity": identity,
            "pass": passed,
            "archive_ns": decode,
            "correspond_ns": elapsed,
            "json_decodes": memo.json_decodes - before[0],
            "recursive_visits": memo.recursive_visits - before[1],
            "block_hits": memo.blocks_checked - before[2],
            "unique_nodes": len(memo.unique_nodes),
            "certificate_times_ns": dict(memo.certificates.times),
            "block_events": list(memo.certificates.events),
        }
        rows.append(row)
        memo.certificates.events.clear()
        print(row, flush=True)
        if not passed:
            raise ValueError("Representative native/canonical correspondence differs")
    publish(
        output,
        {
            "status": "PASS",
            "scope": "REPRESENTATIVE_AUTHENTICATION_ONLY",
            "returns": rows,
            "envelopes": memo.envelopes,
            "json_decodes": memo.json_decodes,
            "recursive_visits": memo.recursive_visits,
            "unique_nodes": len(memo.unique_nodes),
            "cache_hits": memo.blocks_checked,
            "archive_decompressions": archives.decompressions,
            "implementation_sha256": implementation,
            "gc_policy": (
                "SCOPED_DISABLED; COLLECTION INCLUDED IN PARENT WALL; RESTORED"
            ),
        },
    )


async def bounded(output: Path) -> None:
    """Stop the immediate managed diagnostic child at 120 seconds; never retry."""
    output = output.resolve()
    if output.exists() or output.with_suffix(".child.json").exists():
        raise FileExistsError("Diagnostic output already exists")
    command = (
        Command(sys.executable)
        .args(
            "-X",
            "utf8",
            "-m",
            "experiments.codex_dogfood.verification.diagnostics",
            "child",
            str(output.with_suffix(".child.json")),
        )
        .cwd(resolve_path(ROOT))
        .with_timeout(Duration.seconds(120))
    )
    start = time.perf_counter_ns()
    result = {
        "status": "RUNNING",
        "timestamp": Timestamp.now().isoformat(),
        "hard_wall_seconds": 120,
    }
    publish(output, result)
    try:
        completed = await CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=1024 * 1024, max_stderr_bytes=1024 * 1024
            )
        ).execute(command)
        result.update(
            status="PASS" if completed.exit_code == 0 else "FAILED",
            stdout=completed.stdout.decode("utf8"),
            stderr=completed.stderr.decode("utf8"),
            exit_code=completed.exit_code,
        )
    except CommandTimeoutError as error:
        result.update(status="HARD_STOP; NOT_REPEATED", error=str(error))
    result["wall_ns"] = time.perf_counter_ns() - start
    publish(output, result)
    print(json_bytes(result).decode())


def main() -> None:
    """Run a bounded representative diagnostic, never the full verifier."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("run", "child"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.mode == "child":
        measure(args.output)
    else:
        asyncio.run(bounded(args.output))


if __name__ == "__main__":
    main()
