# Copyright (c) 2026
"""Closed publication metadata, actual file mutation and explicit driver faults."""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import closing
from dataclasses import replace
from types import SimpleNamespace
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import pytest

from devtools.learning.evidence.context import RecordingError
from devtools.learning.evidence.events import Admitted, ExecutionEvent, Lifecycle
from devtools.learning.integrations.local import ledger, publication
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    SQLiteInspectionSession,
    _decode_record,
    _event_position,
    _validate_stage,
)
from devtools.learning.integrations.local.publication import (
    PublicationError,
    _digest,
    _read_json,
    _read_manifest,
    _string,
    _uuid,
    _writer,
    inspect_publication_recovery,
    publish_artifacts,
    reconcile_publication,
)
from tests.learning.integrations.local.test_ledger import _history
from tests.learning.integrations.local.test_publication import _publish

if TYPE_CHECKING:
    from pathlib import Path

_EXPECTED_GENERATIONS = 2


@pytest.mark.parametrize("fault", ["array", "artifact", "dependency"])
def test_closed_manifest_arrays_and_entries(tmp_path: Path, fault: str) -> None:
    """Unknown records remain corrupt rather than being dropped while reading."""
    original = _publish(tmp_path / "publication")
    path = original.directory / "manifest.json"
    value = json.loads(path.read_bytes())
    if fault == "array":
        value["artifacts"] = {}
    elif fault == "artifact":
        value["artifacts"] = [{}]
    else:
        value["dependencies"] = [{}]
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises((TypeError, ValueError), match=r"arrays|entry"):
        _read_manifest(path)


def test_bounded_object_metadata_and_canonical_scalars(tmp_path: Path) -> None:
    """Metadata length, JSON object shape and nominal UUID spelling are separate."""
    path = tmp_path / "metadata.json"
    path.write_bytes(b" " * ((1 << 20) + 1))
    with pytest.raises(ValueError, match="1 MiB"):
        _read_json(path)
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(TypeError, match="JSON object"):
        _read_json(path)
    with pytest.raises(TypeError, match="string"):
        _string(None)
    with pytest.raises(ValueError, match="noncanonical"):
        _uuid(str(UUID(int=10)).upper())


def test_digest_detects_actual_file_change_during_inspection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mutate this test's opened file immediately before its final real stat."""
    path = tmp_path / "data"
    path.write_bytes(b"before")
    original = os.fstat

    def mutate(descriptor: int) -> os.stat_result:
        path.write_bytes(b"after-and-longer")
        return original(descriptor)

    monkeypatch.setattr(os, "fstat", mutate)
    with pytest.raises(PublicationError, match="changed during"):
        _digest(path)


def test_absent_and_older_publications_reconcile_original_snapshot(
    tmp_path: Path,
) -> None:
    """A pinned snapshot checks its database; old generations keep their ACK status."""
    database = tmp_path / "science.sqlite"
    with SQLiteExecutionRecorder(database) as recorder:
        first = _publish(tmp_path / "publication", recorder=recorder)
        _publish(tmp_path / "publication", recorder=recorder)
    with SQLiteInspectionSession(database) as session:
        assert (
            reconcile_publication(tmp_path / "missing", database, session=session)
            is None
        )
    recovery = inspect_publication_recovery(tmp_path / "publication", database=database)
    assert len(recovery.generations) == _EXPECTED_GENERATIONS
    assert first.manifest is not None
    assert any(item.manifest == first.manifest for item in recovery.generations)


def test_bad_declared_payload_and_implicit_observer_refuse_before_writes(
    tmp_path: Path,
) -> None:
    """A callback and a negative member reservation do not confer execution custody."""
    with pytest.raises(ValueError, match="nonnegative"):
        publish_artifacts(tmp_path, uuid4(), ("a",), lambda _: None, payload_bytes=-1)
    with pytest.raises(ValueError, match="explicit recorder"):
        publish_artifacts(
            tmp_path,
            uuid4(),
            ("a",),
            lambda _: None,
            observer=lambda _: None,
        )
    assert not tuple(tmp_path.iterdir())


def test_foreign_decoded_order_identity_and_idempotent_close(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a decoder identity fault against original SQL rows, never acceptance."""
    database = tmp_path / "science.sqlite"
    _history(database)
    original = _decode_record

    def foreign(row: tuple[str, str, str, int, str, str]) -> ExecutionEvent:
        return replace(original(row), event_id=uuid4())

    monkeypatch.setattr(ledger, "_decode_record", foreign)
    with closing(sqlite3.connect(database)) as connection:
        identity = connection.execute("SELECT id FROM events LIMIT 1").fetchone()[0]
        with pytest.raises(RecordingError, match="identity differs"):
            _event_position(connection, UUID(identity))
    recorder = SQLiteExecutionRecorder(tmp_path / "second.sqlite")
    recorder.close()
    recorder.close()
    assert _validate_stage(
        Admitted("component-control"),
        Lifecycle.RUNNING,
        None,
        None,
    ) == (None, None)


def test_posix_lock_adapter_and_failure_reports_are_explicit_controls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercise the alternate adapter with reported locks, not POSIX qualification."""
    locks: list[tuple[int, int]] = []
    reported = SimpleNamespace(
        LOCK_EX=1,
        LOCK_NB=2,
        flock=lambda *args: locks.append(args),
    )
    monkeypatch.setattr(
        ledger,
        "os",
        SimpleNamespace(name="posix", getpid=os.getpid, SEEK_END=os.SEEK_END),
    )
    monkeypatch.setattr(ledger, "import_module", lambda _: reported)
    with SQLiteExecutionRecorder(tmp_path / "science.sqlite"):
        pass
    monkeypatch.setattr(
        publication,
        "os",
        SimpleNamespace(**(vars(os) | {"name": "posix"})),
    )
    monkeypatch.setattr(publication, "import_module", lambda _: reported)
    with _writer(tmp_path):
        pass
    assert len(locks) == _EXPECTED_GENERATIONS
