# Copyright (c) 2026
# ruff: noqa: D103, S101, EM101, TRY003, PLR2004, TC003
"""Capture-only recovery fixtures; never prospective Case 0016 operations."""

from __future__ import annotations

from pathlib import Path
from threading import Event, Thread

import pytest

from devtools.resources.filesystem.errors import FilesystemPermissionError
from experiments.codex_dogfood.case_0009.artifacts import binary, digest
from experiments.codex_dogfood.case_0012.stage_b import durability as native
from experiments.codex_dogfood.case_0016.stage_b import execute
from experiments.codex_dogfood.case_0016.stage_b.authenticate import FAILED
from experiments.codex_dogfood.case_0016.stage_b.durability import (
    Journal,
    checkpoint_bytes,
)
from experiments.codex_dogfood.case_0016.stage_b.recovery import (
    authenticate_failed,
    failed_hashes,
    scientific_identity,
)


def test_no_shared_mutable_per_operation_checkpoint(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise FilesystemPermissionError("Synthetic denied mutable checkpoint")

    monkeypatch.setattr(native, "atomic", forbidden)
    journal = Journal.start(
        tmp_path / "synthetic",
        {"execution": "synthetic-no-checkpoint"},
    )
    assert journal.call("one", {}, lambda: 1) == 1
    assert journal.call("two", {}, lambda: 2) == 2
    assert not (journal.root / "raw_checkpoint.json").exists()
    journal.complete()
    loaded = Journal.load(journal.root)
    assert checkpoint_bytes(loaded) == checkpoint_bytes(journal)
    assert not (journal.root / "raw_checkpoint.json").exists()


def test_derived_progress_permission_failure_after_return_continues(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    journal = Journal.start(
        tmp_path / "synthetic",
        {"execution": "synthetic-progress", "operation_schedule": ["one", "two"]},
    )
    progress = execute.Progress(journal, 2)
    original = native.exclusive
    calls = []

    def deny(path: Path, value: object) -> None:
        if path.parent.name == "progress":
            raise FilesystemPermissionError(
                "Synthetic post-return derived publication failure",
            )
        original(path, value)

    monkeypatch.setattr(execute, "exclusive", deny)

    def one() -> str:
        calls.append(1)
        return "one"

    assert progress.call("one", {}, one) == "one"
    assert progress.call("two", {}, lambda: "two") == "two"
    assert calls == [1]
    assert len(progress.warnings) == 4
    loaded = Journal.load(journal.root)
    assert loaded.state["values"]["one"] == "one"
    assert loaded.state["values"]["two"] == "two"


def test_authoritative_return_failure_blocks_advancement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    journal = Journal.start(
        tmp_path / "synthetic",
        {"execution": "synthetic-return-failure"},
    )
    original = native.exclusive
    calls = []

    def deny(path: Path, value: object) -> None:
        if "returned" in path.name:
            raise PermissionError("Synthetic authoritative RETURNED failure")
        original(path, value)

    monkeypatch.setattr(native, "exclusive", deny)
    with pytest.raises(PermissionError, match="authoritative"):
        journal.call("one", {}, lambda: calls.append(1))
    with pytest.raises(ValueError, match="STOP/no retry"):
        journal.call("two", {}, lambda: calls.append(2))
    assert calls == [1]
    assert Journal.load(journal.root).state["operations"][0]["status"] == "ENTERED"


def test_native_failure_blocks_advancement(tmp_path: Path) -> None:
    journal = Journal.start(
        tmp_path / "synthetic",
        {"execution": "synthetic-native-failure"},
    )

    def fail() -> None:
        raise ValueError("Synthetic native failure")

    with pytest.raises(ValueError, match="native failure"):
        journal.call("one", {}, fail)
    with pytest.raises(ValueError, match="STOP/no retry"):
        journal.call("two", {}, lambda: 2)
    assert (
        Journal.load(journal.root).state["operations"][0]["status"]
        == "FAILED_NO_RETURN"
    )


def test_append_only_progress_and_concurrent_immutable_reader(tmp_path: Path) -> None:
    journal = Journal.start(
        tmp_path / "synthetic",
        {"execution": "synthetic-reader", "operation_schedule": ["one", "two"]},
    )
    progress = execute.Progress(journal, 2)
    progress.call("one", {}, lambda: 1)
    before = {
        p: p.read_bytes()
        for folder in ("operations", "progress")
        for p in (journal.root / folder).iterdir()
    }
    stop = Event()
    reads = []

    def inspect() -> None:
        while not stop.is_set():
            for path, raw in before.items():
                assert path.read_bytes() == raw
            reads.append(1)

    reader = Thread(target=inspect)
    reader.start()
    try:
        assert progress.call("two", {}, lambda: 2) == 2
    finally:
        stop.set()
        reader.join()
    assert reads
    assert all(p.read_bytes() == raw for p, raw in before.items())
    assert len(list((journal.root / "progress").iterdir())) == 4
    progress.count = 0
    progress.emit("blocked-overwrite", 1, "DIAGNOSTIC", progress.started)
    assert all(p.read_bytes() == raw for p, raw in before.items())
    assert progress.warnings


def test_attempt_one_replay_immutable_and_scientific_composition_identical() -> None:
    seal = failed_hashes()
    result = authenticate_failed()
    assert result["status"] == "FAILED_AUDIT_ONLY"
    assert result["operations_returned"] == 166
    assert result["journal_events"] == 332
    assert all(
        digest(binary(FAILED / name)) == sha for name, sha in seal["sha256"].items()
    )
    scientific_identity()
