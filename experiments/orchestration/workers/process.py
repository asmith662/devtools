# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0913, PLR0917, ASYNC109, ASYNC240, C901, PLR0915 -- documented CommandExecutor process boundary specialization
"""Managed worker execution using the canonical command lifecycle and tree ownership."""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import os
import signal
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.commands.events import CommandStderr, CommandStdout
from experiments.codex_dogfood.case_0009.artifacts import put_binary
from experiments.orchestration.observation import (
    HEARTBEAT_SECONDS,
    diagnostic,
    latest_operational,
    notify_operational,
    sanitized,
)
from experiments.orchestration.storage import load, save


class TreeExecutor(CommandExecutor):
    """Specialize external-worker process ownership; preserve canonical collection."""

    def __init__(
        self,
        environment: dict[str, str],
        pid_file: Path,
        grace: float,
        stream_directory: Path | None = None,
        stdin_bytes: bytes | None = None,
    ) -> None:
        """Bind explicit environment, process identity and cleanup grace."""
        super().__init__(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=32 << 20,
                max_stderr_bytes=8 << 20,
            ),
        )
        self.environment, self.pid_file, self.grace = environment, pid_file, grace
        self.child: asyncio.subprocess.Process | None = None
        self.stream_directory = stream_directory
        self.stdin_bytes = stdin_bytes
        self.stdin_task: asyncio.Task[None] | None = None

    async def _create_process(self, command: Command) -> asyncio.subprocess.Process:
        """Launch an owned POSIX session or hidden Windows supervisor, never a shell."""
        options: dict[str, Any] = {"env": self.environment}
        if os.name == "nt":
            options["creationflags"] = 0x08000000  # CREATE_NO_WINDOW
        else:
            options["start_new_session"] = True
        process = await asyncio.create_subprocess_exec(
            *command.argv,
            cwd=str(command.working_directory) if command.working_directory else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE
            if self.stdin_bytes is not None
            else asyncio.subprocess.DEVNULL,
            **options,
        )
        self.child = process
        if self.stdin_bytes is not None:

            async def deliver() -> None:
                assert process.stdin is not None  # noqa: S101 -- pipe selected above
                try:
                    process.stdin.write(self.stdin_bytes or b"")
                    await process.stdin.drain()
                except (BrokenPipeError, ConnectionResetError):
                    pass  # Process/transport authentication rejects an incomplete turn.
                finally:
                    process.stdin.close()

            self.stdin_task = asyncio.create_task(deliver())
        save(
            self.pid_file,
            {
                "pid": process.pid,
                "launch_utc": str(Timestamp.now()),
                "argv_sha256_only": hashlib.sha256(
                    repr(command.argv).encode(),
                ).hexdigest(),
                "ownership": "WINDOWS_SUPERVISOR_JOB"
                if os.name == "nt"
                else "POSIX_SESSION",
            },
        )
        return process

    async def _read_stream(
        self,
        stream: asyncio.StreamReader,
        emit: Any,
        event_type: Any,
        max_output_bytes: int,
    ) -> tuple[bytes, bool]:
        """Mirror every drained chunk before the canonical bounded event queue.

        This external-worker specialization retains full streams even when an
        observer falls behind. Canonical retention, timeout and cleanup remain
        owned by CommandExecutor. No framework subprocess mechanism is added.
        """
        if self.stream_directory is None:
            return await super()._read_stream(
                stream,
                emit,
                event_type,
                max_output_bytes,
            )
        name = "stdout.log" if event_type is CommandStdout else "stderr.log"
        with (self.stream_directory / name).open("ab") as output:

            def mirrored(event: Any) -> None:
                output.write(event.data)
                output.flush()
                emit(event)

            return await super()._read_stream(
                stream,
                mirrored,
                event_type,
                max_output_bytes,
            )

    async def _terminate_and_reap(self, process: asyncio.subprocess.Process) -> None:
        """Attempt graceful termination, then kill the owned tree and reap."""
        if os.name != "nt":
            with contextlib.suppress(ProcessLookupError):
                getattr(os, "killpg")(process.pid, signal.SIGTERM)  # noqa: B009 -- POSIX-only API, checked on Windows
        elif process.returncode is None:
            process.terminate()
        try:
            await asyncio.wait_for(process.wait(), self.grace)
        except TimeoutError:
            pass
        finally:
            if os.name != "nt":
                with contextlib.suppress(ProcessLookupError):
                    getattr(os, "killpg")(process.pid, signal.Signals(9))  # noqa: B009 -- POSIX-only API
            elif process.returncode is None:
                process.kill()
            await process.wait()


async def invoke(
    argv: list[str],
    cwd: Path,
    environment: dict[str, str],
    timeout: float,
    grace: float,
    logs: Path,
    *,
    observer: Any = None,
    metadata: Any = None,
    heartbeat_seconds: float = HEARTBEAT_SECONDS,
    stdin_bytes: bytes | None = None,
) -> Any:
    """Run one supervisor; capture bounded output/PID and never retry."""
    logs.mkdir(parents=True, exist_ok=True)
    for name in ("stdout.log", "stderr.log"):
        with (logs / name).open("xb"):
            pass
    started = time.perf_counter()
    last_output = started
    next_heartbeat = started + heartbeat_seconds
    pid: Any = None
    common = {
        "workspace": str(cwd),
        "argv": sanitized(argv),
        "stdout_path": str(logs / "stdout.log"),
        "stderr_path": str(logs / "stderr.log"),
        **(metadata or {}),
    }

    def notify(status: str, **fields: Any) -> None:
        if observer is not None:
            notify_operational(
                observer,
                {
                    "timestamp": str(Timestamp.now()),
                    **common,
                    "status": status,
                    **fields,
                },
            )

    notify("QUEUED")
    spec = logs / "process.json"
    if stdin_bytes is not None:
        put_binary(logs / "stdin.bin", stdin_bytes)
    save(
        spec,
        {
            "argv": argv,
            "cwd": str(cwd),
            "environment_names": list(environment),
            "timeout": timeout,
            "grace": grace,
            "pid_file": str(logs / "child.json"),
            "log_root": str(logs),
            "stdin_file": str(logs / "stdin.bin") if stdin_bytes is not None else None,
        },
    )
    supervisor = Path(__file__).with_name("supervisor.py")
    executor = TreeExecutor(environment, logs / "supervisor.json", grace)
    command = (
        Command(sys.executable)
        .args("-I", "-B", str(supervisor), str(spec))
        .cwd(resolve_path(cwd))
        .with_timeout(Duration.seconds(timeout + 2 * grace + 2))
    )
    execution = executor.start(command)
    result_task = asyncio.ensure_future(execution)

    async def drain() -> None:
        nonlocal last_output
        async for event in execution.events():
            if isinstance(event, (CommandStdout, CommandStderr)) and event.data.strip():
                last_output = time.perf_counter()

    drain_task = asyncio.create_task(drain())
    try:
        while not result_task.done():
            await asyncio.wait({result_task}, timeout=0.1)
            child = logs / "child.json"
            if pid is None and child.exists():
                record = load(child)
                pid = record["pid"]
                notify("STARTED", pid=pid, launch_utc=record.get("launch_utc"))
                notify("PID", pid=pid, launch_utc=record.get("launch_utc"))
            now = time.perf_counter()
            if now >= next_heartbeat and not result_task.done():
                progress = latest_operational(cwd / "operational-progress.jsonl")
                counter = {
                    k: progress[k]
                    for k in ("operation", "current", "total", "telemetry_unavailable")
                    if k in progress
                }
                notify(
                    "HEARTBEAT",
                    pid=pid,
                    duration_seconds=now - started,
                    timeout_remaining_seconds=max(0, timeout - (now - started)),
                    output_idle_seconds=now - last_output,
                    operation_progress=counter,
                )
                next_heartbeat = now + heartbeat_seconds
        result = await result_task
        await drain_task
    except BaseException as error:
        result_task.cancel()
        drain_task.cancel()
        await asyncio.gather(result_task, drain_task, return_exceptions=True)
        save(
            logs / "exit.json",
            {
                "status": "FAILED_OR_TIMEOUT",
                "automatic_retries": 0,
                "exit_utc": str(Timestamp.now()),
                "launch_utc": load(logs / "child.json").get("launch_utc")
                if (logs / "child.json").exists()
                else None,
                "duration_seconds": time.perf_counter() - started,
            },
        )
        notify(
            "FAILED",
            pid=pid,
            failure_category="PROCESS_EXCEPTION",
            duration_seconds=time.perf_counter() - started,
            error=str(error),
            first_diagnostic=diagnostic(logs / "stderr.log", first=True),
            stdout_tail=diagnostic(logs / "stdout.log"),
            stderr_tail=diagnostic(logs / "stderr.log"),
        )
        raise
    # Full child logs are written by the supervisor, before event-buffer loss.
    child_exit = (
        load(logs / "child-exit.json") if (logs / "child-exit.json").exists() else {}
    )
    with (logs / "supervisor-stderr.log").open("xb") as supervisor_output:
        supervisor_output.write(result.stderr)
    if child_exit.get("status") == "COMPLETE":
        with (logs / "stdout.log").open("rb") as stream:
            stdout = stream.read((32 << 20) + 1)
        with (logs / "stderr.log").open("rb") as stream:
            stderr = stream.read((8 << 20) + 1)
        result = replace(
            result,
            stdout=stdout[: 32 << 20],
            stderr=stderr[: 8 << 20],
            stdout_truncated=len(stdout) > 32 << 20,
            stderr_truncated=len(stderr) > 8 << 20,
        )
    if pid is None and (logs / "child.json").exists():
        record = load(logs / "child.json")
        pid = record["pid"]
        notify("STARTED", pid=pid, launch_utc=record.get("launch_utc"))
        notify("PID", pid=pid, launch_utc=record.get("launch_utc"))
    exit_utc = child_exit.get("exit_utc", str(Timestamp.now()))
    category = (
        "TIMEOUT"
        if child_exit.get("error") == "CommandTimeoutError"
        else "NONZERO_EXIT"
        if result.failed
        else "OUTPUT_TRUNCATED"
        if result.stdout_truncated or result.stderr_truncated
        else None
    )
    save(
        logs / "exit.json",
        {
            "exit_code": result.exit_code,
            "duration_seconds": result.duration.total_seconds,
            "stdout_truncated": result.stdout_truncated,
            "stderr_truncated": result.stderr_truncated,
            "launch_utc": load(logs / "child.json").get("launch_utc")
            if (logs / "child.json").exists()
            else None,
            "exit_utc": exit_utc,
            "failure_category": category,
        },
    )
    notify(
        "FAILED" if category else "COMPLETE",
        pid=pid,
        exit_utc=exit_utc,
        exit_code=result.exit_code,
        duration_seconds=result.duration.total_seconds,
        failure_category=category,
        stdout_truncated=result.stdout_truncated,
        stderr_truncated=result.stderr_truncated,
        first_diagnostic=diagnostic(logs / "stdout.log", first=True)
        or diagnostic(logs / "stderr.log", first=True)
        if category
        else "",
        stdout_tail=diagnostic(logs / "stdout.log") if category else "",
        stderr_tail=diagnostic(logs / "stderr.log") if category else "",
        supervisor_stderr_path=str(logs / "supervisor-stderr.log"),
        supervisor_stderr_tail=diagnostic(logs / "supervisor-stderr.log")
        if category
        else "",
    )
    return result
