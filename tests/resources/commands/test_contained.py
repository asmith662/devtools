# Copyright (c) 2026
"""Actual Job1 custody, descendant refusal, timeout and cancellation controls."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandTimeoutError


def test_contained_child_cannot_create_descendant(tmp_path: Path) -> None:
    """A second process is denied by the Job before its code can write."""
    marker = tmp_path / "forbidden"
    code = "import subprocess,sys\ntry:\n subprocess.run([sys.executable,'-c',sys.argv[1]],check=True)\nexcept OSError:\n print('denied')\nelse:\n raise RuntimeError('descendant admitted')"
    result = asyncio.run(CommandExecutor(contained=True).execute(
        Command(str(getattr(sys, "_base_executable"))).args("-c", code, f"open({str(marker)!r},'w').write('entered')")
        .with_timeout(Duration.seconds(10)),
    ))
    assert result.succeeded, result.stderr
    assert result.stdout.strip() == b"denied"
    assert not marker.exists()


def test_contained_timeout_reaps_worker() -> None:
    """Timeout closes the verified empty Job and retains the public timeout."""
    command = Command(str(getattr(sys, "_base_executable"))).args("-c", "import time;time.sleep(30)").with_timeout(Duration.seconds(0.1))
    with pytest.raises(CommandTimeoutError, match="timeout|exceeded"):
        asyncio.run(CommandExecutor(contained=True).execute(command))


def test_contained_cancellation_settles_custody(tmp_path: Path) -> None:
    """Cancel only this invocation after its own child acknowledges entry."""
    marker = tmp_path / "ready"
    command = Command(str(getattr(sys, "_base_executable"))).args("-c", "import sys,time;open(sys.argv[1],'w').write('ready');time.sleep(30)", str(marker)).with_timeout(Duration.seconds(10))

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
