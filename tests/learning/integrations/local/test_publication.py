# Copyright (c) 2026
# Adapted independent contracts from donor
# e069092e9b83c349ddb4efee09a3b1891ea0ad63.
"""Actual filesystem publication, crash boundaries and ledger reconciliation."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import FrozenInstanceError, replace
from typing import TYPE_CHECKING, Any, cast
from uuid import UUID, uuid4

import pytest

from devtools.learning.evidence.context import (
    ExecutionContext,
    ExecutionRecorder,
    RecordingError,
)
from devtools.learning.evidence.events import (
    Admitted,
    Diagnostic,
    ExecutionEvent,
    ExecutionHistory,
    FailureCategory,
    Outcome,
    StageStarted,
    Terminal,
)
from devtools.learning.evidence.publication import (
    PublicationManifest,
    PublicationRecordingStatus,
    PublicationStatus,
    artifact_name,
)
from devtools.learning.integrations.local import publication as filesystem
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    inspect_execution,
)
from devtools.learning.integrations.local.publication import (
    PublicationError,
    PublicationInspection,
    inspect_publication,
    inspect_publication_recovery,
    publish_artifacts,
    reconcile_publication,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def _history(database: Path, identity: UUID | None) -> ExecutionHistory:
    assert identity is not None
    value = inspect_execution(database, identity)
    assert value is not None
    return value


def _manifest(value: PublicationInspection) -> PublicationManifest:
    assert value.manifest is not None
    return value.manifest


def _inspect(root: Path, *, generation_id: str | None = None) -> PublicationInspection:
    value = inspect_publication(root, generation_id=generation_id)
    assert value is not None
    return value


def _reconcile(root: Path, database: Path) -> PublicationInspection:
    value = reconcile_publication(root, database)
    assert value is not None
    return value


NAMES = ("rows.csv", "result.json", "notes.txt")


def _writer(marker: str) -> Callable[[Path], None]:
    """Writer."""

    def write(directory: Path) -> None:
        """Write."""
        for name in NAMES:
            (directory / name).write_text(marker, encoding="utf-8")

    return write


def _publish(
    root: Path,
    marker: str = "first",
    *,
    publication_id: UUID | None = None,
    recorder: ExecutionRecorder | None = None,
    observer: Callable[[ExecutionEvent], None] | None = None,
) -> PublicationInspection:
    """Publish."""
    return publish_artifacts(
        root,
        uuid4(),
        NAMES,
        _writer(marker),
        publication_id=publication_id,
        recorder=recorder,
        observer=observer,
    )


def test_publication_replacement_pinned_readers_and_immutable_identity(
    tmp_path: Path,
) -> None:
    """Publication replacement pinned readers and immutable identity."""
    root = tmp_path / "publications"
    first = _publish(root)
    assert first.status is PublicationStatus.CURRENT
    assert _manifest(first).complete
    assert _manifest(first).schema_version == 1
    assert all(p.read_text() == "first" for p in first.artifact_paths)
    assert _manifest(first).publication_id != _manifest(first).producing_execution_id
    assert len({a.artifact_id for a in _manifest(first).artifacts}) == 3
    with pytest.raises(FrozenInstanceError):
        _manifest(first).complete = False  # type: ignore[misc]  # deliberate frozen mutation
    with pytest.raises(ValueError, match="identity"):
        replace(_manifest(first).artifacts[0], artifact_id=uuid4()) and replace(
            _manifest(first),
            artifacts=(
                replace(_manifest(first).artifacts[0], artifact_id=uuid4()),
                *_manifest(first).artifacts[1:],
            ),
        )
    second = _publish(root, "second")
    assert _manifest(second).publication_id != _manifest(first).publication_id
    assert _inspect(root).directory == second.directory
    old = _inspect(root, generation_id=_manifest(first).generation_id)
    assert old.status is PublicationStatus.AVAILABLE
    assert all(
        p.parent == first.directory and p.read_text() == "first"
        for p in first.artifact_paths
    )
    assert all(
        p.parent == second.directory and p.read_text() == "second"
        for p in second.artifact_paths
    )
    with pytest.raises(PublicationError, match="already reserved"):
        _publish(root, "conflict", publication_id=_manifest(first).publication_id)
    assert _inspect(root).directory == second.directory


@pytest.mark.parametrize(
    "point",
    [
        "first",
        "partial",
        "validator",
        "manifest",
        "before_generation",
        "before_pointer",
    ],
)
def test_failed_replacement_preserves_previous_and_retains_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    point: str,
) -> None:
    """Failed replacement preserves previous and retains evidence."""
    root = tmp_path / "outputs"
    previous = _publish(root)
    pointer = (root / "current.json").read_bytes()

    def write(directory: Path) -> None:
        """Write."""
        if point == "first":
            message = "first artifact write failed"
            raise OSError(message)
        (directory / NAMES[0]).write_text("new")
        if point == "partial":
            message = "after partial writes"
            raise OSError(message)
        for name in NAMES[1:]:
            (directory / name).write_text("new")

    original_write = filesystem._write_json

    def write_json(path: Path, value: object) -> None:
        """Write json."""
        if point == "manifest" and path.name == "manifest.json":
            message = "manifest write failed"
            raise OSError(message)
        if point == "before_pointer" and path.name.startswith(".current-"):
            message = "pointer construction failed"
            raise OSError(message)
        return original_write(path, value)

    monkeypatch.setattr(filesystem, "_write_json", write_json)
    original_sync = filesystem._sync_directory

    def synchronize(path: Path) -> None:
        """Synchronize."""
        if point == "before_generation" and path.parent.name == ".staging":
            message = "before generation rename"
            raise OSError(message)
        return original_sync(path)

    monkeypatch.setattr(filesystem, "_sync_directory", synchronize)

    def validate(directory: Path) -> None:
        """Validate."""
        del directory
        if point == "validator":
            message = "application content invalid"
            raise ValueError(message)

    with pytest.raises((OSError, ValueError)):
        publish_artifacts(root, uuid4(), NAMES, write, validate_artifacts=validate)
    assert (root / "current.json").read_bytes() == pointer
    assert _inspect(root).directory == previous.directory
    assert all(p.read_text() == "first" for p in previous.artifact_paths)
    recovery = inspect_publication_recovery(root)
    if point == "before_pointer":
        assert len(recovery.generations) == 2
        assert recovery.staging == ()
        assert any(
            g.status is PublicationStatus.AVAILABLE for g in recovery.generations
        )
    else:
        assert len(recovery.staging) == 1
        if point in ("first", "partial", "validator", "manifest"):
            assert (recovery.staging[0].directory / "intent.json").exists()


@pytest.mark.parametrize(
    "name",
    [
        "",
        " ",
        "../escape",
        "/absolute",
        "x/y",
        "x\\y",
        "C:stream",
        "file.",
        "file ",
        "NUL.txt",
        "COM1.csv",
        "manifest.json",
        "intent.json",
        ".hidden",
        "café.csv",
        True,
    ],
)
def test_portable_flat_artifact_paths(name: str) -> None:
    """Portable flat artifact paths."""
    with pytest.raises(ValueError):
        artifact_name(name)


@pytest.mark.parametrize("names", [("x", "x"), ("x", "X"), ()])
def test_duplicate_or_empty_membership_rejected_before_writing(
    tmp_path: Path,
    names: tuple[str, ...],
) -> None:
    """Duplicate or empty membership rejected before writing."""
    with pytest.raises(ValueError):
        publish_artifacts(
            tmp_path / "root",
            uuid4(),
            names,
            lambda _d: pytest.fail("must not write"),
        )


@pytest.mark.parametrize("mode", ["missing", "extra", "directory", "hardlink"])
def test_exact_membership_and_file_kinds(tmp_path: Path, mode: str) -> None:
    """Exact membership and file kinds."""
    external = tmp_path / "external.txt"
    external.write_text("external")

    def write(directory: Path) -> None:
        """Write."""
        _writer("value")(directory)
        path = directory / NAMES[0]
        if mode == "missing":
            path.unlink()
        elif mode == "extra":
            (directory / "extra.txt").write_text("extra")
        elif mode == "directory":
            path.unlink()
            path.mkdir()
        else:
            path.unlink()
            os.link(external, path)

    with pytest.raises((PublicationError, FileNotFoundError)):
        publish_artifacts(tmp_path / "root", uuid4(), NAMES, write)
    assert inspect_publication(tmp_path / "root") is None
    assert external.read_text() == "external"


def _mutate_manifest(
    root: Path,
    published: PublicationInspection,
    change: Callable[[dict[str, Any]], None],
) -> None:
    """Mutate manifest."""
    path = published.directory / "manifest.json"
    value = json.loads(path.read_text())
    change(value)
    path.write_text(json.dumps(value))
    pointer = json.loads((root / "current.json").read_text())
    pointer["manifest_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    (root / "current.json").write_text(json.dumps(pointer))


@pytest.mark.parametrize(
    "change",
    [
        lambda v: v.update(schema_version=2),
        lambda v: v.update(complete=False),
        lambda v: v.update(generation_id="../outside"),
        lambda v: v.update(publication_id=str(uuid4())),
        lambda v: v.update(expected_artifact_names=["unknown.csv"]),
        lambda v: v["artifacts"][0].update(relative_path="../escape"),
        lambda v: v["artifacts"][0].update(byte_size=True),
        lambda v: v["artifacts"][0].update(byte_size=-1),
        lambda v: v["artifacts"][0].update(sha256="bad"),
        lambda v: v["artifacts"].append(v["artifacts"][0]),
        lambda v: v.update(unexpected="value"),
    ],
)
def test_manifest_invariants_even_with_rehashed_pointer(
    tmp_path: Path,
    change: Callable[[dict[str, Any]], None],
) -> None:
    """Manifest invariants even with rehashed pointer."""
    root = tmp_path / "root"
    result = _publish(root)
    _mutate_manifest(root, result, change)
    inspected = _inspect(root)
    assert inspected.status is PublicationStatus.CORRUPT
    assert inspected.artifact_paths == ()
    assert inspected.issues


@pytest.mark.parametrize(
    "mode",
    ["artifact", "missing", "manifest", "pointer", "missing_generation"],
)
def test_corruption_never_falls_back_to_old_files(tmp_path: Path, mode: str) -> None:
    """Corruption never falls back to old files."""
    root = tmp_path / "root"
    first, current = (_publish(root), _publish(root, "second"))
    if mode == "artifact":
        current.artifact_paths[0].write_text("tampered")
    elif mode == "missing":
        current.artifact_paths[0].unlink()
    elif mode == "manifest":
        (current.directory / "manifest.json").write_text("{not json")
    elif mode == "pointer":
        (root / "current.json").write_text("{}")
    else:
        current.directory.rename(current.directory.with_name("missing-copy"))
    if mode == "pointer":
        with pytest.raises(PublicationError):
            inspect_publication(root)
    else:
        bad = _inspect(root)
        assert bad.status is PublicationStatus.CORRUPT
        assert not bad.artifact_paths
    assert (
        _inspect(root, generation_id=_manifest(first).generation_id).status
        is PublicationStatus.AVAILABLE
    )
    recovery = inspect_publication_recovery(root)
    assert (
        recovery.current is None or recovery.current.status is PublicationStatus.CORRUPT
    )
    if mode == "pointer":
        assert recovery.current_issues


def test_duplicate_json_fields_and_pointer_identity_mismatch(tmp_path: Path) -> None:
    """Duplicate json fields and pointer identity mismatch."""
    root = tmp_path / "root"
    current = _publish(root)
    pointer = (root / "current.json").read_text()
    (root / "current.json").write_text('{"schema_version":1,' + pointer[1:])
    with pytest.raises(PublicationError, match="duplicate"):
        inspect_publication(root)
    (root / "current.json").write_text(pointer)
    data = json.loads(pointer)
    data["publication_id"] = str(uuid4())
    (root / "current.json").write_text(json.dumps(data))
    assert _inspect(root).status is PublicationStatus.CORRUPT
    assert (
        _inspect(root, generation_id=_manifest(current).generation_id).status
        is PublicationStatus.AVAILABLE
    )


def test_managed_publication_admission_progress_and_consistent_reconciliation(
    tmp_path: Path,
) -> None:
    """Managed publication admission progress and consistent reconciliation."""
    root, database = (tmp_path / "root", tmp_path / "ledger.sqlite")
    with SQLiteExecutionRecorder(database) as recorder:
        with ExecutionContext(recorder, Admitted("application")) as parent:
            current = publish_artifacts(
                root,
                parent.execution_id,
                NAMES,
                _writer("value"),
                recorder=recorder,
                parent=parent,
            )
    manifest = _manifest(current)
    assert current.recording_status is PublicationRecordingStatus.ACKNOWLEDGED
    assert manifest.producing_execution_id == parent.execution_id
    assert manifest.publication_execution_id != parent.execution_id
    history = _history(database, manifest.publication_execution_id)
    assert history.parent_execution_id == parent.execution_id
    assert history.outcome is Outcome.COMPLETED
    assert _history(database, parent.execution_id).outcome is Outcome.COMPLETED
    assert [
        e.payload.stage for e in history.events if isinstance(e.payload, StageStarted)
    ] == [
        "publication_configuration",
        "staging",
        "validation",
        "manifest_construction",
        "generation_publication",
        "current_commit",
        "inspection_reconciliation",
    ]
    reconciled = _reconcile(root, database)
    assert reconciled.recording_status is PublicationRecordingStatus.ACKNOWLEDGED
    assert reconciled.directory == current.directory


def test_terminal_recording_failure_keeps_visible_generation_and_incomplete_history(
    tmp_path: Path,
) -> None:
    """Terminal recording failure keeps visible generation and incomplete history."""
    root, database = (tmp_path / "root", tmp_path / "ledger.sqlite")
    with SQLiteExecutionRecorder(database) as recorder:

        class Fault:
            def record(self, event: ExecutionEvent) -> ExecutionEvent:
                """Record."""
                if isinstance(event.payload, Terminal):
                    message = "no terminal acknowledgment"
                    raise RecordingError(message)
                return recorder.record(event)

        with pytest.raises(RecordingError) as error:
            _publish(root, recorder=Fault())
        assert error.value.computation_outcome is Outcome.COMPLETED
    current = _reconcile(root, database)
    assert current.status is PublicationStatus.CURRENT
    assert current.recording_status is PublicationRecordingStatus.INCOMPLETE
    assert _history(database, current.publication_execution_id).incomplete


def test_publication_failure_keeps_original_error_and_failed_parent(
    tmp_path: Path,
) -> None:
    """Publication failure keeps original error and failed parent."""
    database = tmp_path / "ledger.sqlite"
    with SQLiteExecutionRecorder(database) as recorder:
        with pytest.raises(OSError, match="write failed"):
            with ExecutionContext(recorder, Admitted("application")) as parent:
                parent.stage(
                    "publication",
                    "Required publication",
                    FailureCategory.PUBLICATION,
                )

                def fail(directory: Path) -> None:
                    """Fail."""
                    del directory
                    message = "write failed"
                    raise OSError(message)

                publish_artifacts(
                    tmp_path / "root",
                    parent.execution_id,
                    NAMES,
                    fail,
                    recorder=recorder,
                    parent=parent,
                )
    assert _history(database, parent.execution_id).outcome is Outcome.FAILED
    from devtools.learning.integrations.local.ledger import inspect_child_execution_ids

    (child,) = inspect_child_execution_ids(database, parent.execution_id)
    h = _history(database, child)
    d = next(e.payload for e in h.events if isinstance(e.payload, Diagnostic))
    assert h.outcome is Outcome.FAILED
    assert d.category is FailureCategory.PUBLICATION
    assert d.root_cause is None
    assert d.exception_chain[0].type_name == "builtins.OSError"


def test_optional_observer_failure_and_missing_or_mismatched_ledger(
    tmp_path: Path,
) -> None:
    """Optional observer failure and missing or mismatched ledger."""
    root, database = (tmp_path / "root", tmp_path / "ledger.sqlite")

    def observer(event: ExecutionEvent) -> None:
        """Observer."""
        del event
        message = "optional display failed"
        raise RuntimeError(message)

    with SQLiteExecutionRecorder(database) as recorder:
        current = _publish(root, recorder=recorder, observer=observer)
    assert (
        _reconcile(root, database).recording_status
        is PublicationRecordingStatus.ACKNOWLEDGED
    )
    h = _history(database, current.publication_execution_id)
    assert any(
        isinstance(e.payload, Diagnostic)
        and e.payload.category is FailureCategory.OBSERVER
        for e in h.events
    )
    other = tmp_path / "other.sqlite"
    with SQLiteExecutionRecorder(other):
        pass
    assert (
        _reconcile(root, other).recording_status is PublicationRecordingStatus.MISSING
    )
    with SQLiteExecutionRecorder(other) as recorder:
        with ExecutionContext(recorder, Admitted("unrelated")) as unrelated:
            pass
    _mutate_manifest(
        root,
        current,
        lambda v: v.update(publication_execution_id=str(unrelated.execution_id)),
    )
    data = json.loads((root / "current.json").read_text())
    data["publication_execution_id"] = str(unrelated.execution_id)
    (root / "current.json").write_text(json.dumps(data))
    assert (
        _reconcile(root, other).recording_status is PublicationRecordingStatus.MISMATCH
    )


def test_admission_refusal_does_not_create_root_or_write_artifacts(
    tmp_path: Path,
) -> None:
    """Admission refusal does not create root or write artifacts."""

    class Unavailable:
        def record(self, event: ExecutionEvent) -> ExecutionEvent:
            """Record."""
            del event
            message = "required recorder unavailable"
            raise RecordingError(message)

    root = tmp_path / "root"
    with pytest.raises(RecordingError):
        publish_artifacts(
            root,
            uuid4(),
            NAMES,
            lambda _p: pytest.fail("no admitted work"),
            recorder=Unavailable(),
        )
    assert not root.exists()


def test_visible_generation_with_failed_post_pointer_synchronization(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Visible generation with failed post pointer synchronization."""
    root, database = (tmp_path / "root", tmp_path / "ledger.sqlite")
    previous = _publish(root)
    original = filesystem._sync_directory

    def fail(path: Path) -> None:
        """Fail."""
        if path == root:
            message = "post-pointer directory synchronization failed"
            raise OSError(message)
        original(path)

    monkeypatch.setattr(filesystem, "_sync_directory", fail)
    with SQLiteExecutionRecorder(database) as recorder:
        with pytest.raises(OSError, match="post-pointer"):
            _publish(root, "new", recorder=recorder)
    current = _reconcile(root, database)
    assert current.status is PublicationStatus.CURRENT
    assert current.recording_status is PublicationRecordingStatus.NOT_ACKNOWLEDGED
    assert (
        _history(database, current.publication_execution_id).outcome is Outcome.FAILED
    )
    assert all(p.read_text() == "first" for p in previous.artifact_paths)


def test_secondary_recorder_failure_preserves_primary_publication_error(
    tmp_path: Path,
) -> None:
    """Secondary recorder failure preserves primary publication error."""
    with SQLiteExecutionRecorder(tmp_path / "ledger.sqlite") as recorder:

        class Fault:
            def record(self, event: ExecutionEvent) -> ExecutionEvent:
                """Record."""
                if isinstance(event.payload, Diagnostic):
                    message = "secondary diagnostic recording failed"
                    raise RecordingError(message)
                return recorder.record(event)

        def fail(directory: Path) -> None:
            """Fail."""
            del directory
            message = "primary artifact write failed"
            raise OSError(message)

        with pytest.raises(OSError, match="primary artifact") as error:
            publish_artifacts(tmp_path / "root", uuid4(), NAMES, fail, recorder=Fault())
        assert "Required recording incomplete" in "\n".join(error.value.__notes__)


def test_actual_size_tampering_and_unmanaged_recording_status(tmp_path: Path) -> None:
    """Actual size tampering and unmanaged recording status."""
    root = tmp_path / "root"
    current = _publish(root)
    _mutate_manifest(root, current, lambda v: v["artifacts"][0].update(byte_size=999))
    assert _inspect(root).status is PublicationStatus.CORRUPT
    with SQLiteExecutionRecorder(tmp_path / "ledger.sqlite"):
        pass
    assert (
        _reconcile(root, tmp_path / "ledger.sqlite").recording_status
        is PublicationRecordingStatus.UNMANAGED
    )


def test_unsafe_members_are_rejected_before_application_validator(
    tmp_path: Path,
) -> None:
    """Unsafe members are rejected before application validator."""
    external = tmp_path / "external.txt"
    external.write_text("external")

    def write(directory: Path) -> None:
        """Write."""
        _writer("value")(directory)
        (directory / NAMES[0]).unlink()
        os.link(external, directory / NAMES[0])

    with pytest.raises(PublicationError, match="unaliased"):
        publish_artifacts(
            tmp_path / "root",
            uuid4(),
            NAMES,
            write,
            validate_artifacts=lambda _p: pytest.fail("unsafe validator access"),
        )


def test_mutable_expected_membership_rejected(tmp_path: Path) -> None:
    """Mutable expected membership rejected."""
    with pytest.raises(TypeError, match="immutable tuple"):
        publish_artifacts(
            tmp_path / "root",
            uuid4(),
            cast("tuple[str, ...]", list(NAMES)),
            _writer("bad"),
        )
