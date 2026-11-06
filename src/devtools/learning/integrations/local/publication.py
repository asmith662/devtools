# Copyright (c) 2026
"""Single-writer immutable generations and atomically selected publication visibility.

Roots must be operator-controlled local directories. Cooperative writers hold an
OS-released ownership lock. Links/reparse points are rejected, but this is not a
sandbox against an adversary racing directory replacement. No cross-resource
transaction or universal power-loss guarantee is claimed.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, cast, runtime_checkable
from uuid import UUID, uuid4, uuid5

from devtools.core.time import Timestamp
from devtools.learning.evidence.context import ExecutionContext, ExecutionRecorder
from devtools.learning.evidence.events import (
    Admitted,
    ExecutionEvent,
    Fact,
    FailureCategory,
    Outcome,
    Terminal,
)
from devtools.learning.evidence.publication import (
    ArtifactRecord,
    PublicationManifest,
    PublicationRecordingStatus,
    PublicationStatus,
    _validate_publication_request,
    _validate_sha256,
    generation_name,
    validate_generation_name,
)
from devtools.learning.integrations.local.ledger import (
    SQLiteInspectionSession,
    inspect_execution,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


class PublicationError(RuntimeError):
    """Observed publication/integrity failure; original causes remain chained."""


@dataclass(frozen=True, slots=True)
class PublicationInspection:
    """One pinned generation; invalid observations expose no validated paths."""

    status: PublicationStatus
    directory: Path
    manifest: PublicationManifest | None
    artifact_paths: tuple[Path, ...]
    issues: tuple[str, ...] = ()
    manifest_sha256: str | None = None
    recording_status: PublicationRecordingStatus = (
        PublicationRecordingStatus.UNINSPECTED
    )
    publication_execution_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class PublicationRecoveryInspection:
    """Observed current, staged and available data; no automatic cleanup/restoration."""

    current: PublicationInspection | None
    current_issues: tuple[str, ...]
    generations: tuple[PublicationInspection, ...]
    staging: tuple[PublicationInspection, ...]


def _safe_path(path: Path) -> Path:
    absolute = Path(os.path.normpath(path.absolute()))
    for component in (*reversed(absolute.parents), absolute):
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(
            info,
            "st_file_attributes",
            0,
        ) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024):
            msg = f"symlink/reparse point is not allowed: {component}"
            raise PublicationError(msg)
    return absolute


def _regular(path: Path) -> os.stat_result:
    _safe_path(path)
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        msg = f"artifact/metadata must be a regular unaliased file: {path}"
        raise PublicationError(msg)
    return info


def _digest(path: Path, *, synchronize: bool = False) -> tuple[int, str]:
    before = _regular(path)
    digest = hashlib.sha256()
    size = 0
    with path.open("r+b" if synchronize else "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
        if synchronize:
            os.fsync(stream.fileno())
        after = os.fstat(stream.fileno())
    if (before.st_ino, before.st_size, before.st_mtime_ns) != (
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    ) or size != after.st_size:
        msg = f"file changed during integrity inspection: {path}"
        raise PublicationError(msg)
    return (size, digest.hexdigest())


def _sync_directory(path: Path) -> None:
    if os.name != "nt":
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _write_json(path: Path, value: object) -> None:
    _safe_path(path)
    with path.open("xb") as stream:
        stream.write((json.dumps(value, indent=2, allow_nan=False) + "\n").encode())
        stream.flush()
        os.fsync(stream.fileno())


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            msg = "duplicate JSON field"
            raise ValueError(msg)
        result[key] = value
    return result


def _read_json(path: Path) -> dict[str, object]:
    if _regular(path).st_size > 1024 * 1024:
        msg = "publication metadata exceeds the 1 MiB limit"
        raise ValueError(msg)
    value: object = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
    )
    if not isinstance(value, dict):
        msg = "publication metadata must be a JSON object"
        raise ValueError(msg)
    return cast("dict[str, object]", value)


def _string(value: object) -> str:
    if not isinstance(value, str):
        msg = "metadata string required"
        raise TypeError(msg)
    return value


def _uuid(value: object) -> UUID:
    identity = UUID(_string(value))
    if str(identity) != value:
        msg = "noncanonical UUID"
        raise ValueError(msg)
    return identity


def _manifest_data(manifest: PublicationManifest) -> dict[str, object]:
    value = asdict(manifest)
    for key in ("publication_id", "producing_execution_id", "publication_execution_id"):
        value[key] = str(value[key]) if value[key] is not None else None
    value["created_at"] = manifest.created_at.isoformat()
    value["artifacts"] = [
        dict(asdict(a), artifact_id=str(a.artifact_id)) for a in manifest.artifacts
    ]
    return value


def _read_manifest(path: Path) -> PublicationManifest:
    value = _read_json(path)
    if set(value) != set(PublicationManifest.__dataclass_fields__):
        msg = "unknown or missing manifest fields"
        raise ValueError(msg)
    artifacts = value["artifacts"]
    names, dependencies = (value["expected_artifact_names"], value["dependencies"])
    if (
        not isinstance(artifacts, list)
        or not isinstance(names, list)
        or (not isinstance(dependencies, list))
    ):
        msg = "manifest arrays required"
        raise TypeError(msg)
    records = []
    for entry in artifacts:
        if not isinstance(entry, dict) or set(entry) != set(
            ArtifactRecord.__dataclass_fields__,
        ):
            msg = "invalid artifact entry"
            raise ValueError(msg)
        records.append(
            ArtifactRecord(
                _uuid(entry["artifact_id"]),
                entry["name"],
                entry["relative_path"],
                entry["byte_size"],
                entry["sha256"],
            ),
        )
    facts = []
    for entry in dependencies:
        if not isinstance(entry, dict) or set(entry) != {"name", "value"}:
            msg = "invalid dependency entry"
            raise ValueError(msg)
        facts.append(Fact(entry["name"], entry["value"]))
    return PublicationManifest(
        _uuid(value["publication_id"]),
        _uuid(value["producing_execution_id"]),
        _string(value["generation_id"]),
        datetime.fromisoformat(_string(value["created_at"])),
        tuple(_string(n) for n in names),
        tuple(records),
        tuple(facts),
        None
        if value["publication_execution_id"] is None
        else _uuid(value["publication_execution_id"]),
        cast("int", value["schema_version"]),
        cast("bool", value["complete"]),
    )


@contextmanager
def _writer(root: Path) -> Iterator[None]:
    """Immediate bounded acquisition; process death releases ownership, not files."""
    lock = root / ".publication.writer.lock"
    _safe_path(lock)
    if lock.exists():
        _regular(lock)
    with lock.open("a+b") as stream:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                msvcrt = import_module("msvcrt")

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl = import_module("fcntl")

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            msg = "publication root already has a writer or is inaccessible"
            raise PublicationError(msg) from error
        yield


def _inspect_directory(
    directory: Path,
    *,
    staged: bool = False,
) -> PublicationInspection:
    manifest = None
    manifest_digest = None
    try:
        _safe_path(directory)
        validate_generation_name(directory.name)
        manifest = _read_manifest(directory / "manifest.json")
        manifest_digest = _digest(directory / "manifest.json")[1]
        if manifest.generation_id != directory.name:
            msg = "manifest generation differs from its directory"
            raise ValueError(msg)
        expected = {*manifest.expected_artifact_names, "manifest.json"}
        if staged and (directory / "intent.json").exists():
            expected.add("intent.json")
        if {p.name for p in directory.iterdir()} != expected:
            msg = "generation contains missing or unexpected members"
            raise ValueError(msg)
        for entry in manifest.artifacts:
            if _digest(directory / entry.relative_path) != (
                entry.byte_size,
                entry.sha256,
            ):
                msg = f"artifact size/digest mismatch: {entry.name}"
                raise ValueError(msg)
        return PublicationInspection(
            PublicationStatus.STAGED if staged else PublicationStatus.AVAILABLE,
            directory,
            manifest,
            tuple(directory / a.relative_path for a in manifest.artifacts),
            manifest_sha256=manifest_digest,
            publication_execution_id=manifest.publication_execution_id,
        )
    except (OSError, ValueError, TypeError, PublicationError) as error:
        return PublicationInspection(
            PublicationStatus.INCOMPLETE
            if staged and manifest is None
            else PublicationStatus.CORRUPT,
            directory,
            manifest,
            (),
            (f"{type(error).__name__}: {error}",),
            manifest_sha256=manifest_digest,
            publication_execution_id=manifest.publication_execution_id
            if manifest
            else None,
        )


def inspect_publication(
    root: Path,
    *,
    generation_id: str | None = None,
) -> PublicationInspection | None:
    """Pin the pointer once; validate one generation, never fall back or mix files."""
    root = _safe_path(root)
    if generation_id is not None:
        validate_generation_name(generation_id)
        return _inspect_directory(root / "generations" / generation_id)
    pointer_path = root / "current.json"
    if not pointer_path.exists():
        _safe_path(pointer_path)
        return None
    try:
        pointer = _read_json(pointer_path)
        if set(pointer) != {
            "schema_version",
            "publication_id",
            "producing_execution_id",
            "generation_id",
            "manifest_sha256",
            "publication_execution_id",
        }:
            msg = "invalid current-publication fields"
            raise ValueError(msg)
        if type(pointer["schema_version"]) is not int or pointer["schema_version"] != 1:
            msg = "unsupported current-publication schema"
            raise ValueError(msg)
        generation = validate_generation_name(_string(pointer["generation_id"]))
        pub_id, producer = (
            _uuid(pointer["publication_id"]),
            _uuid(pointer["producing_execution_id"]),
        )
        publishing = (
            None
            if pointer["publication_execution_id"] is None
            else _uuid(pointer["publication_execution_id"])
        )
        _validate_sha256(_string(pointer["manifest_sha256"]))
        inspected = _inspect_directory(root / "generations" / generation)
        if inspected.manifest is None or inspected.status is PublicationStatus.CORRUPT:
            return replace(inspected, publication_execution_id=publishing)
        m = inspected.manifest
        if (
            m.publication_id,
            m.producing_execution_id,
            m.publication_execution_id,
            inspected.manifest_sha256,
        ) != (pub_id, producer, publishing, pointer["manifest_sha256"]):
            return replace(
                inspected,
                status=PublicationStatus.CORRUPT,
                artifact_paths=(),
                issues=("current reference disagrees with manifest identities/digest",),
            )
        return replace(inspected, status=PublicationStatus.CURRENT)
    except (OSError, ValueError, TypeError) as error:
        msg = f"invalid current-publication reference: {error}"
        raise PublicationError(msg) from error


def reconcile_publication(
    root: Path,
    database: Path,
    *,
    generation_id: str | None = None,
    session: SQLiteInspectionSession | None = None,
) -> PublicationInspection | None:
    """Observe filesystem and ledger independently; never repair or infer success."""
    if session is not None:
        session.require_database(database)
    inspected = inspect_publication(root, generation_id=generation_id)
    if inspected is None:
        return None
    execution_id = inspected.publication_execution_id
    status = PublicationRecordingStatus.UNMANAGED
    if execution_id is not None:
        history = inspect_execution(database, execution_id, session=session)
        status = PublicationRecordingStatus.MISSING
        if history is not None:
            status = (
                PublicationRecordingStatus.INCOMPLETE
                if history.incomplete
                else PublicationRecordingStatus.NOT_ACKNOWLEDGED
            )
            request = history.events[0].payload
            admitted = (
                {f.name: f.value for f in request.facts}
                if isinstance(request, Admitted)
                else {}
            )
            manifest = inspected.manifest
            if history.operation != "artifacts.publication" or (
                manifest is not None
                and (
                    admitted.get("publication_id") != str(manifest.publication_id)
                    or admitted.get("producing_execution_id")
                    != str(manifest.producing_execution_id)
                    or admitted.get("generation_id") != manifest.generation_id
                )
            ):
                status = PublicationRecordingStatus.MISMATCH
            elif history.outcome is Outcome.COMPLETED:
                terminal = next(
                    e.payload for e in history.events if isinstance(e.payload, Terminal)
                )
                facts = {f.name: f.value for f in terminal.facts}
                m = inspected.manifest
                status = (
                    PublicationRecordingStatus.ACKNOWLEDGED
                    if m is not None
                    and (
                        facts.get("publication_id") == str(m.publication_id)
                        and facts.get("producing_execution_id")
                        == str(m.producing_execution_id)
                        and (facts.get("generation_id") == m.generation_id)
                        and (facts.get("manifest_sha256") == inspected.manifest_sha256)
                        and (facts.get("current_reference_committed") is True)
                    )
                    else PublicationRecordingStatus.MISMATCH
                )
    return replace(inspected, recording_status=status)


def inspect_publication_recovery(
    root: Path,
    *,
    database: Path | None = None,
) -> PublicationRecoveryInspection:
    """Inspect retained staging/older generations without deleting or restoring them."""
    root = _safe_path(root)
    issues: tuple[str, ...] = ()
    try:
        current = (
            inspect_publication(root)
            if database is None
            else reconcile_publication(root, database)
        )
    except PublicationError as error:
        current, issues = (None, (str(error),))
    observations: list[tuple[PublicationInspection, ...]] = []
    for name in ("generations", ".staging"):
        container = _safe_path(root / name)
        values = []
        if container.exists():
            for directory in sorted(container.iterdir()):
                item = _inspect_directory(directory, staged=name == ".staging")
                if current is not None and item.directory == current.directory:
                    item = current
                elif (
                    database is not None
                    and name == "generations"
                    and (item.manifest is not None)
                ):
                    reconciled = reconcile_publication(
                        root,
                        database,
                        generation_id=directory.name,
                    )
                    if reconciled is not None:
                        item = reconciled
                values.append(item)
        observations.append(tuple(values))
    return PublicationRecoveryInspection(
        current,
        issues,
        observations[0],
        observations[1],
    )


@runtime_checkable
class PublicationReservation(Protocol):
    """Optional source-local quota hook; no durable resource store or authority."""

    def reserve_publication(self, payload_bytes: int | None) -> None:
        """Apply the explicit reserve publication contract within this owner."""
        ...


def publish_artifacts(
    root: Path,
    producing_execution_id: UUID,
    expected_artifact_names: tuple[str, ...],
    write_artifacts: Callable[[Path], None],
    *,
    validate_artifacts: Callable[[Path], None] | None = None,
    dependencies: tuple[Fact, ...] = (),
    publication_id: UUID | None = None,
    recorder: ExecutionRecorder | None = None,
    observer: Callable[[ExecutionEvent], None] | None = None,
    parent: ExecutionContext | None = None,
    payload_bytes: int | None = None,
) -> PublicationInspection:
    """Write a new generation; pointer visibility precedes required terminal recording.

    The callback writes only expected flat members into private staging. All files
    are closed before it returns. Failure retains staging/unreferenced generations.
    Publication identities are one-use within a root, including failed attempts.
    Inspect by identity after an uncertain acknowledgment; do not blindly retry.
    """
    if payload_bytes is not None and (
        type(payload_bytes) is not int or payload_bytes < 0
    ):
        msg = "nonnegative declared member bytes required"
        raise ValueError(msg)
    if isinstance(recorder, PublicationReservation):
        recorder.reserve_publication(payload_bytes)
    identity, created = (publication_id or uuid4(), Timestamp.now().value)
    generation = generation_name(created, identity)
    if recorder is None:
        if observer is not None or parent is not None:
            msg = "observer/parent requires an explicit recorder"
            raise ValueError(msg)
        return _publish(
            root,
            producing_execution_id,
            expected_artifact_names,
            write_artifacts,
            validate_artifacts,
            dependencies,
            identity,
            created,
            generation,
        )
    with ExecutionContext(
        recorder,
        Admitted(
            "artifacts.publication",
            (
                Fact("publication_id", str(identity)),
                Fact("generation_id", generation),
                Fact("producing_execution_id", str(producing_execution_id)),
                Fact(
                    "artifact_count",
                    len(expected_artifact_names)
                    if isinstance(expected_artifact_names, tuple)
                    else None,
                ),
            ),
        ),
        observer=observer,
        parent=parent,
    ) as execution:
        result = _publish(
            root,
            producing_execution_id,
            expected_artifact_names,
            write_artifacts,
            validate_artifacts,
            dependencies,
            identity,
            created,
            generation,
            execution,
        )
        execution.completed(
            (
                Fact("publication_id", str(identity)),
                Fact("generation_id", generation),
                Fact("producing_execution_id", str(producing_execution_id)),
                Fact("manifest_sha256", result.manifest_sha256),
                Fact("current_reference_committed", True),
            ),
        )
    return replace(result, recording_status=PublicationRecordingStatus.ACKNOWLEDGED)


def _publish(
    root: Path,
    producer: UUID,
    names: tuple[str, ...],
    writer: Callable[[Path], None],
    validator: Callable[[Path], None] | None,
    dependencies: tuple[Fact, ...],
    identity: UUID,
    created: datetime,
    generation: str,
    execution: ExecutionContext | None = None,
) -> PublicationInspection:

    def stage(name: str, description: str) -> None:
        if execution:
            execution.stage(name, description, FailureCategory.PUBLICATION)

    stage("publication_configuration", "Validate membership and local publication root")
    if not isinstance(names, tuple):
        msg = "expected artifact membership must be an immutable tuple"
        raise TypeError(msg)
    names = _validate_publication_request(
        identity,
        producer,
        execution.execution_id if execution else None,
        generation,
        created,
        names,
        dependencies,
    )
    root = _safe_path(root)
    root.mkdir(parents=True, exist_ok=True)
    with _writer(root):
        for name in ("generations", ".staging"):
            container = _safe_path(root / name)
            container.mkdir(exist_ok=True)
            if any(p.name.endswith(str(identity)) for p in container.iterdir()):
                msg = "publication identity is already reserved in this root"
                raise PublicationError(msg)
        previous = inspect_publication(root)
        if previous is not None and previous.status is PublicationStatus.CORRUPT:
            msg = "current publication is corrupt; explicit investigation required"
            raise PublicationError(msg)
        stage(
            "staging",
            "Write expected artifacts into a unique retained staging directory",
        )
        staging = root / ".staging" / generation
        staging.mkdir()
        _write_json(
            staging / "intent.json",
            {
                "schema_version": 1,
                "publication_id": str(identity),
                "producing_execution_id": str(producer),
                "generation_id": generation,
                "created_at": created.isoformat(),
                "expected_artifact_names": names,
                "publication_execution_id": str(execution.execution_id)
                if execution
                else None,
                "dependencies": [asdict(f) for f in dependencies],
                "complete": False,
            },
        )
        if execution:
            execution.progress("artifacts_written", 0, len(names))
        writer(staging)
        for name in (*names, "intent.json"):
            _regular(staging / name)
        if execution:
            execution.progress("artifacts_written", len(names), len(names))
        stage(
            "validation",
            "Validate exact membership, content and SHA-256 observations",
        )
        if {p.name for p in staging.iterdir()} != {*names, "intent.json"}:
            msg = "staging contains missing or unexpected artifacts"
            raise PublicationError(msg)
        if validator:
            validator(staging)
        records = tuple(
            ArtifactRecord(
                uuid5(identity, n),
                n,
                n,
                *_digest(staging / n, synchronize=True),
            )
            for n in names
        )
        if execution:
            execution.progress("artifacts_verified", len(records), len(names))
        stage(
            "manifest_construction",
            "Write and validate complete version-one manifest",
        )
        manifest = PublicationManifest(
            identity,
            producer,
            generation,
            created,
            names,
            records,
            dependencies,
            execution.execution_id if execution else None,
        )
        _write_json(staging / "manifest.json", _manifest_data(manifest))
        checked = _inspect_directory(staging, staged=True)
        if checked.status is not PublicationStatus.STAGED:
            raise PublicationError("; ".join(checked.issues))
        (staging / "intent.json").unlink()
        _sync_directory(staging)
        stage(
            "generation_publication",
            "Finalize complete generation without replacing earlier data",
        )
        target = _safe_path(root / "generations" / generation)
        if target.exists():
            msg = "generation already exists"
            raise PublicationError(msg)
        staging.rename(target)
        _sync_directory(root / "generations")
        _sync_directory(root / ".staging")
        stage(
            "current_commit",
            "Atomically select the complete generation on this filesystem",
        )
        pointer = {
            "schema_version": 1,
            "publication_id": str(identity),
            "producing_execution_id": str(producer),
            "generation_id": generation,
            "manifest_sha256": checked.manifest_sha256,
            "publication_execution_id": str(execution.execution_id)
            if execution
            else None,
        }
        temporary = root / (".current-" + str(identity) + ".tmp")
        _write_json(temporary, pointer)
        _safe_path(root / "current.json")
        temporary.replace(root / "current.json")
        _sync_directory(root)
        stage(
            "inspection_reconciliation",
            "Verify selected generation before ledger completion acknowledgment",
        )
        result = inspect_publication(root)
        if (
            result is None
            or result.status is not PublicationStatus.CURRENT
            or result.manifest != manifest
        ):
            msg = "committed current reference did not validate"
            raise PublicationError(msg)
        return result
