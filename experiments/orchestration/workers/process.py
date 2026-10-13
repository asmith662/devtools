# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0913, PLR0917, ASYNC109, ASYNC240 -- documented CommandExecutor process boundary specialization
"""Managed worker execution using the canonical command lifecycle and tree ownership."""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import os
import signal
import sys
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from experiments.codex_dogfood.case_0009.artifacts import put_binary
from experiments.orchestration.storage import save


class TreeExecutor(CommandExecutor):
    """Specialize external-worker process ownership; preserve canonical collection."""

    def __init__(
        self,
        environment: dict[str, str],
        pid_file: Path,
        grace: float,
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
            **options,
        )
        self.child = process
        save(
            self.pid_file,
            {
                "pid": process.pid,
                "argv_sha256_only": hashlib.sha256(
                    repr(command.argv).encode(),
                ).hexdigest(),
                "ownership": "WINDOWS_SUPERVISOR_JOB"
                if os.name == "nt"
                else "POSIX_SESSION",
            },
        )
        return process

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
) -> Any:
    """Run one supervisor; capture bounded output/PID and never retry."""
    logs.mkdir(parents=True, exist_ok=True)
    spec = logs / "process.json"
    save(
        spec,
        {
            "argv": argv,
            "cwd": str(cwd),
            "environment_names": list(environment),
            "timeout": timeout,
            "grace": grace,
            "pid_file": str(logs / "child.json"),
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
    try:
        result = await executor.execute(command)
    except BaseException:
        save(
            logs / "exit.json",
            {"status": "FAILED_OR_TIMEOUT", "automatic_retries": 0},
        )
        raise
    put_binary(logs / "stdout.log", result.stdout)
    put_binary(logs / "stderr.log", result.stderr)
    save(
        logs / "exit.json",
        {
            "exit_code": result.exit_code,
            "duration_seconds": result.duration.total_seconds,
            "stdout_truncated": result.stdout_truncated,
            "stderr_truncated": result.stderr_truncated,
        },
    )
    return result
