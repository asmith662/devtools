# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, PLR2004, ASYNC240 -- deterministic operational fixtures
"""Windows sharing and telemetry defects cannot own scientific completion."""

from __future__ import annotations

import asyncio
import os
import sys
import threading
from typing import TYPE_CHECKING, Any

import pytest

from devtools.resources.filesystem.errors import FilesystemPermissionError
from experiments.orchestration.observation import (
    append_operational,
    latest_operational,
    operational_snapshot,
)
from experiments.orchestration.storage import save
from experiments.orchestration.workers.process import invoke

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.skipif(os.name != "nt", reason="Exact Windows delete-sharing behavior")
def test_windows_atomic_reader_conflict_is_operational_only(tmp_path: Path) -> None:
    path = tmp_path / "progress.json"
    save(path, {"current": 0})
    with path.open("rb"):
        with pytest.raises(FilesystemPermissionError) as raised:
            save(path, {"current": 1})
        assert "WinError 5" in str(raised.value.__cause__)
        assert not operational_snapshot(path, {"current": 1})
    save(path, {"current": 2})
    assert path.is_file()


def test_five_thousand_updates_with_concurrent_and_held_reader(tmp_path: Path) -> None:
    path = tmp_path / "operational-progress.jsonl"
    path.write_bytes(b"")
    stopped = threading.Event()
    errors = []

    def observe() -> None:
        try:
            while not stopped.is_set():
                latest_operational(path)
        except Exception as error:  # noqa: BLE001 -- expose reader defect in fixture
            errors.append(str(error))

    thread = threading.Thread(target=observe)
    thread.start()
    try:
        with path.open("rb"):
            for position in range(5000):
                assert append_operational(path, {"current": position, "total": 5000})
    finally:
        stopped.set()
        thread.join(timeout=5)
    assert not thread.is_alive()
    assert not errors
    assert latest_operational(path)["current"] == 4999
    path.write_bytes(b"corrupt\n")
    assert latest_operational(path) == {"telemetry_unavailable": True}
    assert latest_operational(tmp_path / "missing") == {"telemetry_unavailable": True}
    assert not append_operational(tmp_path, {"status": "COMPLETE"})


def test_observer_exception_does_not_stop_process_or_create_success(
    tmp_path: Path,
) -> None:
    def broken(_event: Any) -> None:
        message = "synthetic failed observation"
        raise PermissionError(message)

    async def run() -> None:
        result = await invoke(
            [sys.executable, "-c", "import sys; print(sys.stdin.read()); sys.exit(7)"],
            tmp_path,
            {
                k: os.environ[k]
                for k in ("PATH", "SystemRoot", "TEMP", "TMP")
                if k in os.environ
            },
            10,
            0.2,
            tmp_path / "logs",
            observer=broken,
            stdin_bytes=b"immutable synthetic input",
        )
        assert result.exit_code == 7
        assert b"immutable synthetic input" in result.stdout
        assert not list(tmp_path.glob("**/RETURNED.json"))

    asyncio.run(run())
