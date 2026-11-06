# Copyright (c) 2026
"""Actual Job1 custody, descendant refusal, timeout and cancellation controls."""

from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandTimeoutError
from devtools.resources.commands._windows_job import WindowsJob

if TYPE_CHECKING:
    from pathlib import Path


def test_contained_child_cannot_create_descendant(tmp_path: Path) -> None:
    """A second process is denied by the Job before its code can write."""
    marker = tmp_path / "forbidden"
    code = (
        "import subprocess,sys\ntry:\n subprocess.run([sys.executable,'-c',"
        "sys.argv[1]],check=True)\nexcept OSError:\n print('denied')\nelse:\n"
        " raise RuntimeError('descendant admitted')"
    )
    result = asyncio.run(
        CommandExecutor(contained=True).execute(
            Command(str(getattr(sys, "_base_executable", sys.executable)))
            .args("-c", code, f"open({str(marker)!r},'w').write('entered')")
            .with_timeout(Duration.seconds(10)),
        ),
    )
    assert result.succeeded, result.stderr
    assert result.stdout.strip() == b"denied"
    assert not marker.exists()


def test_contained_timeout_reaps_worker() -> None:
    """Timeout closes the verified empty Job and retains the public timeout."""
    command = (
        Command(str(getattr(sys, "_base_executable", sys.executable)))
        .args("-c", "import time;time.sleep(30)")
        .with_timeout(Duration.seconds(0.1))
    )
    with pytest.raises(CommandTimeoutError, match=r"timeout|exceeded"):
        asyncio.run(CommandExecutor(contained=True).execute(command))


def test_contained_cancellation_settles_custody(tmp_path: Path) -> None:
    """Cancel only this invocation after its own child acknowledges entry."""
    marker = tmp_path / "ready"
    command = (
        Command(str(getattr(sys, "_base_executable", sys.executable)))
        .args(
            "-c",
            "import sys,time;open(sys.argv[1],'w').write('ready');time.sleep(30)",
            str(marker),
        )
        .with_timeout(Duration.seconds(10))
    )

    async def cancel() -> None:
        task = asyncio.create_task(CommandExecutor(contained=True).execute(command))
        for _ in range(100):
            if marker.exists():
                break
            await asyncio.sleep(0.01)
        assert marker.exists()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(cancel())


def test_failed_admission_reaps_the_actual_suspended_child_without_entry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reap the real suspended child after an explicitly simulated admission refusal."""
    marker = tmp_path / "must-not-enter"
    created: list[asyncio.subprocess.Process] = []
    admissions: list[int] = []
    original = asyncio.create_subprocess_exec
    failure = OSError("authored admission refusal before resume")

    async def observe(*args: object, **kwargs: object) -> asyncio.subprocess.Process:
        process = await original(*cast("Any", args), **cast("Any", kwargs))
        created.append(process)
        return process

    def refuse(_job: WindowsJob, _handle: int, process_id: int) -> None:
        admissions.append(process_id)
        raise failure

    monkeypatch.setattr(asyncio, "create_subprocess_exec", observe)
    monkeypatch.setattr(WindowsJob, "assign_and_resume", refuse)
    command = (
        Command(str(getattr(sys, "_base_executable", sys.executable)))
        .args("-c", "import sys;open(sys.argv[1],'w').write('entered')", str(marker))
        .with_timeout(Duration.seconds(10))
    )
    with pytest.raises(OSError, match="admission refusal") as caught:
        asyncio.run(CommandExecutor(contained=True).execute(command))
    assert caught.value is failure
    assert len(created) == 1
    assert admissions == [created[0].pid]
    assert created[0].returncode is not None
    assert created[0].returncode != 0
    assert not marker.exists()
