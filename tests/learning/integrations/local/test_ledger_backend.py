# Copyright (c) 2026
"""Real SQLite failure custody with explicitly injected driver-report faults."""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import closing
from dataclasses import replace
from functools import partial
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, ClassVar, cast

import pytest

from devtools.learning.evidence.context import ExecutionContext, RecordingError
from devtools.learning.evidence.events import Activated, Admitted, FailureCategory
from devtools.learning.integrations.local import ledger
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    SQLiteInspectionSession,
    _validate_lifecycle,
    inspect_execution,
)
from tests.learning.integrations.local.test_ledger import _history

if TYPE_CHECKING:
    from typing import Any


class _ReportedConnection(sqlite3.Connection):
    """Delegate actual transactions, changing only a selected driver report."""

    fault: ClassVar[str] = ""

    def execute(self, sql: str, parameters: object = ()) -> sqlite3.Cursor:
        """Retain actual schema effects and inject a documented external failure."""
        if self.fault == "schema" and sql.lstrip().startswith("CREATE TABLE"):
            message = "simulated schema driver failure"
            raise sqlite3.OperationalError(message)
        if self.fault == "quick" and sql == "PRAGMA quick_check":
            return super().execute("SELECT 'reported integrity failure'")
        if self.fault == "write-journal" and sql == "PRAGMA journal_mode=DELETE":
            super().execute(sql)
            return super().execute("SELECT 'wal'")
        if self.fault == "read-journal" and sql == "PRAGMA journal_mode":
            return super().execute("SELECT 'off'")
        return super().execute(sql, cast("Any", parameters))


@pytest.mark.parametrize(
    ("fault", "reason"),
    [
        ("schema", "driver failure"),
        ("quick", "integrity check failed"),
        ("write-journal", "DELETE could not"),
    ],
)
def test_reported_writer_failure_closes_custody_and_preserves_rollback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
    reason: str,
) -> None:
    """A driver report is never coerced into reliable admission or retried effects."""
    database = tmp_path / "science.sqlite"
    original = sqlite3.connect
    with monkeypatch.context() as patch:
        patch.setattr(_ReportedConnection, "fault", fault)
        patch.setattr(
            sqlite3,
            "connect",
            partial(original, factory=_ReportedConnection),
        )
        with pytest.raises(RecordingError, match=reason):
            SQLiteExecutionRecorder(database)
    # A fresh normal owner proves that failed setup released its own writer lock.
    with SQLiteExecutionRecorder(database):
        pass


def test_reported_unsupported_read_journal_refuses_readonly_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate an unsupported driver report without changing the original source."""
    database = tmp_path / "science.sqlite"
    _history(database)
    before = database.read_bytes()
    original = sqlite3.connect
    with monkeypatch.context() as patch:
        patch.setattr(_ReportedConnection, "fault", "read-journal")
        patch.setattr(
            sqlite3,
            "connect",
            partial(original, factory=_ReportedConnection),
        )
        with (
            pytest.raises(RecordingError, match="Unsupported inspection journal"),
            SQLiteInspectionSession(database),
        ):
            pytest.fail("unsupported reported journal was accepted")
    assert database.read_bytes() == before


def test_invalid_sqlite_bytes_and_missing_metadata_are_explicit_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Actual invalid bytes and simulated stat loss never become empty histories."""
    invalid = tmp_path / "invalid.sqlite"
    invalid.write_bytes(b"not an SQLite database")
    with (
        pytest.raises(RecordingError, match="Cannot open inspection"),
        SQLiteInspectionSession(invalid),
    ):
        pytest.fail("invalid database accepted")
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    with SQLiteInspectionSession(database) as session:
        original = Path.stat

        def absent(path: Path, *, follow_symlinks: bool = True) -> os.stat_result:
            if path == database:
                message = "simulated source metadata loss"
                raise OSError(message)
            return original(path, follow_symlinks=follow_symlinks)

        with monkeypatch.context() as patch:
            patch.setattr(Path, "stat", absent)
            with pytest.raises(RecordingError, match="snapshot is unavailable"):
                session.inspect_execution(identity)


def test_only_original_owner_can_close_a_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Foreign ownership cannot close the original owner's snapshot."""
    database = tmp_path / "science.sqlite"
    _history(database)
    with (
        SQLiteInspectionSession(database) as session,
        monkeypatch.context() as patch,
    ):
        patch.setattr(ledger, "os", SimpleNamespace(getpid=lambda: os.getpid() + 1))
        with pytest.raises(RecordingError, match="Only the owning process"):
            session.close()


@pytest.mark.parametrize("reader", ["membership", "order", "children"])
def test_malformed_stored_identifiers_keep_reader_failure_context(
    tmp_path: Path,
    reader: str,
) -> None:
    """Corrupt native storage is an inspection failure, never an available result."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    history = inspect_execution(database, identity)
    assert history is not None
    first, last = history.events[0].event_id, history.events[-1].event_id
    with closing(sqlite3.connect(database)) as connection, connection:
        if reader == "membership":
            connection.execute(
                "INSERT INTO executions VALUES "
                "('invalid-uuid','control','pending',NULL,NULL)",
            )
        else:
            data = json.loads(
                connection.execute(
                    "SELECT document FROM events WHERE sequence=1",
                ).fetchone()[0],
            )
            data["occurred_at"] = "invalid timestamp"
            connection.execute(
                "UPDATE events SET document=? WHERE sequence=1",
                (json.dumps(data),),
            )
    with SQLiteInspectionSession(database) as session:

        def read() -> None:
            if reader == "membership":
                session.execution_ids()
            elif reader == "order":
                session.recorded_before(first, last)
            else:
                session.child_execution_ids(identity)

        with pytest.raises(RecordingError, match="Cannot inspect"):
            read()


def test_unacknowledged_stored_event_has_no_comparison_position(tmp_path: Path) -> None:
    """Missing ACK evidence cannot manufacture an apparently reversed order."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    history = inspect_execution(database, identity)
    assert history is not None
    with closing(sqlite3.connect(database)) as connection, connection:
        data = json.loads(
            connection.execute(
                "SELECT document FROM events WHERE sequence=1",
            ).fetchone()[0],
        )
        data["observed_at"] = None
        connection.execute(
            "UPDATE events SET document=? WHERE sequence=1",
            (json.dumps(data),),
        )
    with (
        SQLiteInspectionSession(database) as session,
        pytest.raises(RecordingError, match="Unacknowledged event"),
    ):
        session.recorded_before(history.events[0].event_id, history.events[-1].event_id)


def test_read_validator_refuses_repeated_activation_in_an_authored_fault_copy(
    tmp_path: Path,
) -> None:
    """Qualify the lifecycle guard independently of the earlier SQL count guard."""
    database = tmp_path / "science.sqlite"
    identity = _history(database)
    history = inspect_execution(database, identity)
    assert history is not None
    events = list(history.events)
    events[2] = replace(events[2], payload=Activated(1, "host", "3", "windows"))
    with pytest.raises(RecordingError, match="Repeated or unordered activation"):
        _validate_lifecycle(tuple(events), history.activations, None)


def test_corrupt_old_progress_cannot_become_independently_accepted_history(
    tmp_path: Path,
) -> None:
    """A writer's new ACK does not certify corrupted earlier stage correspondence."""
    database = tmp_path / "science.sqlite"
    with (
        SQLiteExecutionRecorder(database) as recorder,
        ExecutionContext(recorder, Admitted("progress-control")) as run,
    ):
        run.stage("work", "Owned progress control", FailureCategory.INPUT)
        run.progress("rows", 0, 1)
        with closing(sqlite3.connect(database)) as connection, connection:
            sequence, raw = connection.execute(
                "SELECT sequence,document FROM events WHERE kind='Progress'",
            ).fetchone()
            value = json.loads(raw)
            value["payload"]["stage"] = "foreign"
            connection.execute(
                "UPDATE events SET document=? WHERE sequence=?",
                (json.dumps(value), sequence),
            )
        run.progress("rows", 1, 1)
        run.completed()
    with pytest.raises(RecordingError, match="stage/progress"):
        inspect_execution(database, run.execution_id)
