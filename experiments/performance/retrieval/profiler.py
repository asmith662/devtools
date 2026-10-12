# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, T201, E501
"""Bounded mechanical Stage D diagnostics; no gold join or gate evaluation."""

from __future__ import annotations

import argparse
import ast
import asyncio
import copy
import json
import sys
import time
from pathlib import Path
from threading import Event, Thread
from typing import Any, cast

from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.commands.errors import CommandTimeoutError
from experiments.codex_dogfood.case_0009.artifacts import ROOT, json_bytes
from experiments.codex_dogfood.case_0012.stage_b import durability
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal
from experiments.performance.retrieval.benchmark import PACKAGE, publish
from experiments.performance.retrieval.measurement import summary
from experiments.performance.retrieval.workload import (
    CAPTURE,
    CASE,
    authenticate,
    read_json,
    sha,
)

STAGE_D = CASE / "stage_d"
LIMIT_SECONDS = 120
PHASES = (
    "artifact_hashing",
    "stage_d_json_parse",
    "stage_d_deepcopy",
    "stage_d_json_encoding",
    "stage_d_markdown_json_sections",
    "native_return_authentication",
)


def source_audit() -> dict[str, Any]:
    """Retain static call/loop sites without invoking scientific constructors."""
    paths = [
        STAGE_D / name
        for name in (
            "analysis.py",
            "metrics.py",
            "reporting.py",
            "authentication.py",
            "validation.py",
        )
    ]
    paths += [
        CASE / "adjudication/reviewed/materialize.py",
        CAPTURE.parents[1] / "reporting.py",
        ROOT / "experiments/codex_dogfood/case_0012/stage_b/durability.py",
    ]
    output = {}
    for path in paths:
        tree = ast.parse(path.read_bytes())
        output[path.relative_to(ROOT).as_posix()] = {
            "sha256": sha(path.read_bytes()),
            "functions": {
                node.name: {
                    "line": node.lineno,
                    "calls": [
                        {"line": call.lineno, "function": ast.unparse(call.func)}
                        for call in ast.walk(node)
                        if isinstance(call, ast.Call)
                    ],
                    "loop_lines": [
                        loop.lineno
                        for loop in ast.walk(node)
                        if isinstance(loop, (ast.For, ast.While, ast.comprehension))
                        and hasattr(loop, "lineno")
                    ],
                }
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            },
        }
    return output


def worker(phase: str, output: Path) -> None:  # noqa: C901, PLR0915 -- explicit bounded diagnostic phases
    """Time an independent mechanical phase; parent kills immediate child at 120s."""
    if phase not in PHASES:
        raise ValueError("Unknown bounded phase")
    # No primary/gold files are read. Existing Stage D data is opaque retained output.
    authentication = authenticate()
    raw = (STAGE_D / "analysis.json").read_bytes()
    value: Any = (
        json.loads(raw)
        if phase
        in {
            "stage_d_deepcopy",
            "stage_d_json_encoding",
            "stage_d_markdown_json_sections",
        }
        else None
    )
    state: dict[str, Any] = {
        "phase": phase,
        "category": "EXPERIMENT_ONLY",
        "status": "RUNNING",
        "timestamp": Timestamp.now().isoformat(),
        "phase_started_counter_ns": time.perf_counter_ns(),
        "raw_bytes": len(raw),
        "limit_seconds": LIMIT_SECONDS,
    }
    state["components"] = {}
    if phase == "native_return_authentication":
        # Local worker-only observation, byte-identical native functions.
        # Inclusive function counters overlap and are not an additive breakdown.
        for name in (
            "read_json",
            "unpack",
            "describe",
            "json_bytes",
            "digest",
            "binary",
        ):
            original = getattr(durability, name)

            def observe(
                *args: Any,
                _original: Any = original,
                _name: str = name,
                **kwargs: Any,
            ) -> Any:
                before = time.perf_counter_ns()
                result = _original(*args, **kwargs)
                elapsed = time.perf_counter_ns() - before
                counter = state["components"].setdefault(
                    _name,
                    {"calls": 0, "inclusive_ns": 0},
                )
                counter["calls"] += 1
                counter["inclusive_ns"] += elapsed
                return result

            setattr(durability, name, observe)
    publish(output, state)
    stop = Event()

    def heartbeat() -> None:
        while not stop.wait(20):
            state["last_observed_running_elapsed_ns"] = (
                time.perf_counter_ns() - state["phase_started_counter_ns"]
            )
            publish(output, state)

    thread = Thread(target=heartbeat, daemon=True)
    thread.start()
    samples = []
    for _ in range(1 if phase == "native_return_authentication" else 3):
        started = time.perf_counter_ns()
        if phase == "artifact_hashing":
            hashes = {
                name: sha((CAPTURE / name).read_bytes())
                for name in authentication
                if not name.startswith("stage_a/")
            }
            if hashes != {
                name: digest
                for name, digest in authentication.items()
                if not name.startswith("stage_a/")
            }:
                raise ValueError("Artifact changed during diagnostic")
        elif phase == "stage_d_json_parse":
            parsed = json.loads(raw)
            state["top_level_fields"] = len(parsed)
        elif phase == "stage_d_deepcopy":
            cloned = copy.deepcopy(value)
            del cloned
        elif phase == "stage_d_json_encoding":
            if json_bytes(value) != raw:
                raise ValueError("Retained Stage D JSON encoding differs")
        elif phase == "stage_d_markdown_json_sections":
            # Actual reporter's JSON-block construction, isolated from gold inputs,
            # tables and outcome computation. Do not claim full Markdown timing.
            encoded = "\n".join(
                "## " + name + "\n\n" + json_bytes(item).decode()
                for name, item in value.items()
            ).encode()
            state["rendered_section_bytes"] = len(encoded)
        else:
            journal = Journal.load(CAPTURE)
            state["validated_returns"] = len(journal.state["operations"])
        samples.append(time.perf_counter_ns() - started)
    state.update(status="COMPLETE", samples_ns=samples, summary=summary(samples))
    stop.set()
    thread.join()
    publish(output, state)


async def profile(output: Path) -> dict[str, Any]:
    """Run isolated phases sequentially, with a hard managed-process timeout."""
    results = {}
    for phase in PHASES:
        phase_output = output.parent / "phases" / (phase + ".json")
        phase_output.parent.mkdir(parents=True, exist_ok=True)
        print(
            f"{Timestamp.now().isoformat()} Stage D diagnostic {phase} START; limit={LIMIT_SECONDS}s",
            flush=True,
        )
        started = time.perf_counter_ns()
        command = (
            Command(sys.executable)
            .args(
                "-X",
                "utf8",
                "-m",
                "experiments.performance.retrieval.profiler",
                "--worker",
                phase,
                "--output",
                str(phase_output),
            )
            .cwd(resolve_path(ROOT))
            .with_timeout(Duration.seconds(LIMIT_SECONDS))
        )
        try:
            result = await CommandExecutor(
                output_policy=CommandOutputPolicy(
                    max_stdout_bytes=4096,
                    max_stderr_bytes=16384,
                ),
            ).execute(command)
        except CommandTimeoutError:
            partial: dict[str, Any] = (
                read_json(phase_output) if phase_output.exists() else {"phase": phase}
            )
            partial.update(
                status="TIME_LIMIT_STOPPED_NOT_REPEATED",
                process_elapsed_ns=time.perf_counter_ns() - started,
            )
            partial["phase_elapsed_lower_bound_ns"] = partial.get(
                "last_observed_running_elapsed_ns",
                0,
            )
            partial["bound_note"] = (
                "Lower bound is the last heartbeat while the worker was running; "
                "process wall includes preparation and cleanup. Worker hard cap is 120 seconds."
            )
            publish(phase_output, partial)
            results[phase] = partial
        else:
            if result.failed:
                raise ValueError("Diagnostic worker failed: " + result.stderr.decode())
            results[phase] = read_json(phase_output)
        print(
            f"{Timestamp.now().isoformat()} Stage D diagnostic {phase} {results[phase]['status']} elapsed={(time.perf_counter_ns() - started) / 1e9:.3f}s",
            flush=True,
        )
        publish(
            output,
            {
                "schema": "bounded-stage-d-profiler-v1",
                "category": "EXPERIMENT_ONLY",
                "phase_limit_seconds": LIMIT_SECONDS,
                "phases": results,
                "source_audit": source_audit(),
                "full_stage_d_verify": "NOT_RUN",
                "gold_join": "NOT_PERFORMED",
                "gate_evaluation": "NOT_PERFORMED",
            },
        )
    return cast("dict[str, Any]", read_json(output))


def main() -> None:
    """Expose bounded diagnostics and private isolated phase execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PACKAGE / "stage_d_profile.json")
    parser.add_argument("--worker", choices=PHASES)
    args = parser.parse_args()
    if args.worker:
        worker(args.worker, args.output)
    else:
        asyncio.run(profile(args.output))


if __name__ == "__main__":
    main()
