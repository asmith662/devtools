# Copyright (c) 2026
# ruff: noqa: E402, PLC0415 -- standalone process-tree owner, not scientific worker
"""Own a Windows kill-on-close job before spawning workers."""

from __future__ import annotations

import asyncio
import contextlib
import ctypes
import os
import signal
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command
from devtools.resources.commands.events import CommandStderr, CommandStdout
from experiments.orchestration.storage import load, require
from experiments.orchestration.workers.process import TreeExecutor


def windows_job() -> object | None:
    """Assign this supervisor to a non-inheritable kill-on-close Windows job."""
    if os.name != "nt":
        return None
    from ctypes import wintypes

    class Basic(ctypes.Structure):
        _fields_ = [
            ("per_process", ctypes.c_int64),
            ("per_job", ctypes.c_int64),
            ("flags", wintypes.DWORD),
            ("min", ctypes.c_size_t),
            ("max", ctypes.c_size_t),
            ("active", wintypes.DWORD),
            ("affinity", ctypes.c_size_t),
            ("priority", wintypes.DWORD),
            ("scheduling", wintypes.DWORD),
        ]

    class Extended(ctypes.Structure):
        _fields_ = [
            ("basic", Basic),
            ("io", ctypes.c_uint64 * 6),
            ("process_memory", ctypes.c_size_t),
            ("job_memory", ctypes.c_size_t),
            ("peak_process", ctypes.c_size_t),
            ("peak_job", ctypes.c_size_t),
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    handle = kernel.CreateJobObjectW(None, None)
    info = Extended()
    info.basic.flags = 0x2000
    require(
        handle
        and kernel.SetInformationJobObject(
            handle,
            9,
            ctypes.byref(info),
            ctypes.sizeof(info),
        )
        and kernel.AssignProcessToJobObject(handle, kernel.GetCurrentProcess()),
        "Cannot establish worker job ownership; no worker started",
    )
    return int(handle)  # Held until exit; the OS terminates owned descendants.


async def main() -> int:
    """Create tree ownership before the child, then bound its canonical lifecycle."""
    spec = load(Path(sys.argv[1]))
    job = windows_job()
    executor = TreeExecutor(
        {n: os.environ[n] for n in spec["environment_names"] if n in os.environ},
        Path(spec["pid_file"]),
        spec["grace"],
    )
    if os.name != "nt":

        def cancel_owned_tree(_signum: int, _frame: object) -> None:
            if executor.child is not None and executor.child.returncode is None:
                with contextlib.suppress(ProcessLookupError):
                    getattr(os, "killpg")(executor.child.pid, signal.Signals(9))  # noqa: B009 -- platform-specific API
            raise SystemExit(143)

        signal.signal(signal.SIGTERM, cancel_owned_tree)
    command = (
        Command(spec["argv"][0])
        .args(*spec["argv"][1:])
        .cwd(resolve_path(spec["cwd"]))
        .with_timeout(Duration.seconds(spec["timeout"]))
    )
    execution = executor.start(command)
    async for event in execution.events():
        if isinstance(event, CommandStdout):
            sys.stdout.buffer.write(event.data)
            sys.stdout.buffer.flush()
        elif isinstance(event, CommandStderr):
            sys.stderr.buffer.write(event.data)
            sys.stderr.buffer.flush()
    result = await execution
    _ = job
    return result.exit_code


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
