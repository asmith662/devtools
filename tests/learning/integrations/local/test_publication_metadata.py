# Copyright (c) 2026
"""Closed publication metadata, actual file mutation and explicit driver faults."""

from __future__ import annotations

import json
import os
import sqlite3
import stat
from contextlib import closing
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
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
    _sync_directory,
    _uuid,
    _validate_members,
    _writer,
    inspect_publication,
    inspect_publication_recovery,
    publish_artifacts,
    reconcile_publication,
)
from tests.learning.integrations.local.test_ledger import _history
from tests.learning.integrations.local.test_publication import _publish

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


def test_reported_reparse_point_and_lock_failure_never_publish(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercise explicit platform report faults without creating shared aliases."""
    original = Path.lstat

    def reparse(path: Path) -> os.stat_result:
        if path == tmp_path:
            return os.stat_result((stat.S_IFLNK, 0, 0, 1, 0, 0, 0, 0, 0, 0))
        return original(path)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "lstat", reparse)
        with pytest.raises(PublicationError, match="symlink/reparse"):
            inspect_publication(tmp_path)

    def fail(_: object, *__: object) -> None:
        message = "reported lock failure"
        raise OSError(message)

    monkeypatch.setattr(
        publication,
        "os",
        SimpleNamespace(**(vars(os) | {"name": "posix"})),
    )
    monkeypatch.setattr(
        publication,
        "import_module",
        lambda _: SimpleNamespace(
            LOCK_EX=1,
            LOCK_NB=2,
            flock=fail,
        ),
    )
    with (
        pytest.raises(PublicationError, match="already has a writer"),
        _writer(tmp_path),
    ):
        pytest.fail("reported lock failure was accepted")


def test_directory_sync_adapter_closes_only_its_owned_descriptor(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate directory opening with a real exclusively owned file descriptor."""
    owned = tmp_path / "sync-control"
    owned.write_bytes(b"control")
    original = os.open
    descriptor = original(owned, os.O_RDWR)
    monkeypatch.setattr(
        publication,
        "os",
        SimpleNamespace(
            **(
                vars(os)
                | {
                    "name": "posix",
                    "open": lambda *_: descriptor,
                }
            ),
        ),
    )
    _sync_directory(tmp_path)
    with pytest.raises(OSError, match=r"invalid|Bad file descriptor"):
        os.fstat(descriptor)


def test_current_schema_generation_and_corruption_refuse_new_publication(
    tmp_path: Path,
) -> None:
    """Refuse corrupted original files before selecting a new generation."""
    root = tmp_path / "publication"
    item = _publish(root)
    assert item.manifest is not None
    with pytest.raises(ValueError, match="differs from its directory"):
        _validate_members(tmp_path / "foreign", item.manifest, staged=False)
    pointer = root / "current.json"
    data = json.loads(pointer.read_bytes())
    data["schema_version"] = True
    before = pointer.read_bytes()
    pointer.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(
        PublicationError,
        match="unsupported current-publication schema",
    ):
        inspect_publication(root)
    pointer.write_bytes(before)
    item.artifact_paths[0].write_bytes(b"corrupt")
    with pytest.raises(PublicationError, match="current publication is corrupt"):
        _publish(root)


@pytest.mark.parametrize("fault", ["staging", "target", "current"])
def test_failed_publication_boundaries_retain_original_files_without_false_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Inject an owned staging fault, competing target or inspection return failure."""
    root = tmp_path / "publication"
    if fault == "current":
        original = inspect_publication
        monkeypatch.setattr(
            publication,
            "inspect_publication",
            lambda path, **kw: (
                None if (path / "current.json").exists() else original(path, **kw)
            ),
        )

    def writer(directory: Path) -> None:
        (directory / "data.txt").write_bytes(b"original")
        if fault == "staging":
            (directory / "unexpected").write_bytes(b"fault")
        elif fault == "target":
            (root / "generations" / directory.name).mkdir()

    with pytest.raises(
        PublicationError,
        match=r"unexpected|already exists|did not validate",
    ):
        publish_artifacts(root, uuid4(), ("data.txt",), writer)
    assert tuple(root.rglob("data.txt"))


def test_recovery_keeps_unreconciled_generation_and_empty_containers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing second read cannot invent a ledger ACK or erase observed files."""
    empty = inspect_publication_recovery(tmp_path / "empty")
    assert empty.generations == empty.staging == ()
    root, database = tmp_path / "publication", tmp_path / "science.sqlite"
    with SQLiteExecutionRecorder(database) as recorder:
        _publish(root, recorder=recorder)
        _publish(root, recorder=recorder)
    monkeypatch.setattr(
        publication,
        "reconcile_publication",
        lambda path, db, **kw: (
            None if "generation_id" in kw else reconcile_publication(path, db, **kw)
        ),
    )
    result = inspect_publication_recovery(root, database=database)
    assert len(result.generations) == _EXPECTED_GENERATIONS


def test_validator_cannot_add_unobserved_members_after_initial_membership_check(
    tmp_path: Path,
) -> None:
    """Actual late member creation must fail independent staged-manifest inspection."""

    def writer(directory: Path) -> None:
        (directory / "data.txt").write_bytes(b"original")

    def invalid_validator(directory: Path) -> None:
        (directory / "unexpected.txt").write_bytes(b"unobserved")

    with pytest.raises(PublicationError, match="unexpected members"):
        publish_artifacts(
            tmp_path,
            uuid4(),
            ("data.txt",),
            writer,
            validate_artifacts=invalid_validator,
        )
    assert tuple((tmp_path / ".staging").glob("*/unexpected.txt"))
    assert not (tmp_path / "current.json").exists()
