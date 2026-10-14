# Copyright (c) 2026
# ruff: noqa: ANN401 -- experiment-owned operational reporting
"""Human lifecycle reporting; never authority or scientific evidence."""

from __future__ import annotations

import asyncio
import contextlib
import json
import sys
import time
from typing import TYPE_CHECKING, Any

from devtools.core.time import Timestamp
from experiments.codex_dogfood.case_0009.artifacts import digest

HEARTBEAT_SECONDS = 15.0

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from pathlib import Path

PROCESS_FIELDS = (
    "operation",
    "status",
    "timestamp",
    "duration_seconds",
    "model",
    "reasoning",
    "pid",
    "workspace",
    "instruction",
    "instruction_sha256",
    "packet_sha256",
    "argv",
    "launch_utc",
    "exit_utc",
    "timeout_remaining_seconds",
    "output_idle_seconds",
    "operation_progress",
    "stdout_path",
    "stderr_path",
    "exit_code",
    "failure_category",
    "fresh",
    "semantic",
    "process_role",
    "stdout_truncated",
    "stderr_truncated",
    "first_diagnostic",
    "stdout_tail",
    "stderr_tail",
    "supervisor_stderr_tail",
    "supervisor_stderr_path",
)


def sanitized(argv: list[str]) -> list[str]:
    """Keep exact executable/options while replacing prompt bodies and secrets."""
    result = list(argv)
    if (
        "exec" in result
        and "--model" in result
        and result
        and not result[-1].startswith("<prompt-sha256:")
    ):
        result[-1] = "<prompt-sha256:" + digest(result[-1].encode()) + ">"
    for i, value in enumerate(result[:-1]):
        if value.casefold() in {"--token", "--password", "--api-key"}:
            result[i + 1] = "<redacted>"
    return result


def process_metadata(config: Any, workspace: Path) -> dict[str, Any]:
    """Expose identity, never the instruction or packet contents."""
    instruction = workspace / config["prompt_file"]
    packet = workspace / "packet.json"
    return {
        "model": config["model"],
        "reasoning": config["reasoning"],
        "fresh": True,
        "semantic": True,
        "instruction": str(instruction),
        "instruction_sha256": digest(instruction.read_bytes()),
        "packet_sha256": digest(packet.read_bytes()) if packet.exists() else None,
    }


class Console:
    """Render bounded operational dictionaries on stderr, or JSONL for a viewer."""

    def __init__(self, *, json_output: bool = False) -> None:
        """Start a monotonic display clock; no execution state is created."""
        self.started = time.perf_counter()
        self.json_output = json_output

    def emit(self, event: dict[str, Any]) -> None:
        """Flush each lifecycle record without making console IO authoritative."""
        value = {
            "timestamp": str(Timestamp.now()),
            "elapsed_seconds": time.perf_counter() - self.started,
            **event,
        }
        if self.json_output:
            line = json.dumps(value, sort_keys=True)
            stream = sys.stdout
        else:
            fields = [
                value["timestamp"],
                f"+{value['elapsed_seconds']:.3f}s",
                "case=" + str(value.get("case", "cohort")),
                "stage=" + str(value.get("stage", "controller")),
                "op=" + str(value.get("operation", value.get("stage", "controller"))),
                str(value.get("status", "UPDATE")),
            ]
            for name in (
                "duration_seconds",
                "model",
                "reasoning",
                "pid",
                "workspace",
                "instruction_sha256",
                "packet_sha256",
                "fresh",
                "launch_utc",
                "exit_utc",
                "timeout_remaining_seconds",
                "output_idle_seconds",
                "operation_progress",
                "exit_code",
                "failure_category",
                "stdout_truncated",
                "stderr_truncated",
                "stdout_path",
                "stderr_path",
                "supervisor_stderr_path",
                "semantic_summary",
                "process_role",
                "instruction",
                "commit",
            ):
                if value.get(name) is not None:
                    fields.append(  # noqa: PERF401 -- conditional operational fields
                        name + "=" + json.dumps(value[name], ensure_ascii=True),
                    )
            if "argv" in value:
                fields.append("command=" + json.dumps(sanitized(value["argv"])))
            line = " ".join(fields)
            if value.get("status") == "FAILED":
                line = "\n=== FAILED ===\n" + line
            for name in (
                "first_diagnostic",
                "stdout_tail",
                "stderr_tail",
                "supervisor_stderr_tail",
                "error",
            ):
                if value.get(name):
                    line += "\n  " + name + ": " + str(value[name])[:6000]
            stream = sys.stderr
        with contextlib.suppress(OSError):
            print(line, file=stream, flush=True)


def diagnostic(path: Path, *, first: bool = False) -> str:
    """Read a bounded useful prefix or tail; preserve full streams separately."""
    if not path.exists():
        return ""
    with path.open("rb") as stream:
        if not first:
            stream.seek(max(0, path.stat().st_size - 8192))
        raw = stream.read(8192)
    lines = [line for line in raw.decode(errors="replace").splitlines() if line.strip()]
    return "\n".join(lines[:8] if first else lines[-20:])[:6000]


async def observed_wait[T](
    operation: Awaitable[T],
    observer: Callable[[dict[str, Any]], None] | None,
    event: dict[str, Any],
    *,
    interval: float = HEARTBEAT_SECONDS,
) -> T:
    """Observe a long authentication/publication wait without granting authority."""
    task = asyncio.ensure_future(operation)
    started = time.perf_counter()
    try:
        while not task.done():
            await asyncio.wait({task}, timeout=interval)
            if not task.done() and observer is not None:
                observer(
                    {
                        **event,
                        "status": "HEARTBEAT",
                        "duration_seconds": time.perf_counter() - started,
                    },
                )
        return await task
    except BaseException:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        raise
