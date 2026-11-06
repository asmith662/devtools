# Copyright (c) 2026
"""Single-writer SQLite empirical history; large artifacts remain external."""

from __future__ import annotations

import itertools
import math
import os
import sqlite3
import stat
import threading
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, Self
from uuid import UUID

from devtools.core.time import Timestamp
from devtools.learning.evidence.context import RecordingError
from devtools.learning.evidence.events import (
    Activated,
    ActivationHistory,
    Admitted,
    Diagnostic,
    ExecutionEvent,
    ExecutionHistory,
    FailureCategory,
    Lifecycle,
    Outcome,
    Progress,
    Severity,
    StageFinished,
    StageStarted,
    Terminal,
)
from devtools.learning.integrations.local._codec import decode, encode

if TYPE_CHECKING:
    from types import TracebackType

_LOCK_TIMEOUT_LIMIT = 30
_MINIMUM_LEDGER_BYTES = 262144
_MAXIMUM_LEDGER_BYTES = 2**31

_SCHEMA_VERSION = 1
_COLUMNS = {
    "executions": {"id", "operation", "lifecycle", "outcome", "active_stage"},
    "activations": {"id", "execution_id", "producer", "started_at", "ended_at", "pid"},
    "events": {"id", "execution_id", "activation_id", "sequence", "kind", "document"},
}
_SCHEMA = (
    "\nCREATE TABLE executions (\n id TEXT PRIMARY KEY NOT NULL, operat"
    "ion TEXT NOT NULL,\n lifecycle TEXT NOT NULL CHECK(lifecycle IN ("
    "'pending','running','stopped')),\n outcome TEXT CHECK(outcome IN "
    "('completed','failed','interrupted','cancelled')),\n active_stage"
    " TEXT,\n CHECK ((lifecycle='stopped') = (outcome IS NOT NULL))\n);"
    "\nCREATE TABLE activations (\n id TEXT PRIMARY KEY NOT NULL,\n exec"
    "ution_id TEXT UNIQUE NOT NULL REFERENCES executions(id),\n produc"
    "er TEXT NOT NULL, started_at TEXT, ended_at TEXT, pid INTEGER\n);"
    "\nCREATE TABLE events (\n id TEXT PRIMARY KEY NOT NULL,\n execution"
    "_id TEXT NOT NULL REFERENCES executions(id),\n activation_id TEXT"
    " NOT NULL REFERENCES activations(id),\n sequence INTEGER NOT NULL"
    " CHECK(sequence>0),\n kind TEXT NOT NULL, document TEXT NOT NULL,"
    "\n UNIQUE(activation_id,sequence)\n);\nCREATE INDEX events_executio"
    "n ON events(execution_id,sequence);\n"
)


def _validate_schema(connection: sqlite3.Connection) -> None:
    version = connection.execute("PRAGMA user_version").fetchone()[0]
    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'",
        )
    }
    if version != _SCHEMA_VERSION or tables != set(_COLUMNS):
        msg = "Unsupported or unrelated execution database schema"
        raise RecordingError(msg)
    for table, expected in _COLUMNS.items():
        columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
        if columns != expected:
            msg = "Execution database schema is inconsistent"
            raise RecordingError(msg)
    if connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
        msg = "Execution database integrity check failed"
        raise RecordingError(msg)


class SQLiteExecutionRecorder:
    """One writer owner with short FULL-synchronous transactions.

    A record return is acknowledgment of SQLite commit, subject to filesystem/
    hardware guarantees. The advisory sidecar lock is released by OS process
    exit, including crashes; it is not a PID-based stale-lock heuristic.
    """

    def __init__(
        self,
        database: Path,
        *,
        timeout_seconds: float = 0.25,
        maximum_database_bytes: int | None = None,
    ) -> None:
        """Initialize the explicitly scoped scientific boundary."""
        if not isinstance(database, Path):
            msg = "database must be an explicit Path"
            raise TypeError(msg)
        if str(database) == ":memory:":
            msg = "durable recording requires a filesystem path"
            raise ValueError(msg)
        if type(timeout_seconds) not in (int, float) or (
            not math.isfinite(timeout_seconds)
            or not 0 <= timeout_seconds <= _LOCK_TIMEOUT_LIMIT
        ):
            msg = "timeout_seconds must be finite and between 0 and 30"
            raise ValueError(msg)
        self.database = database.resolve()
        if maximum_database_bytes is not None and (
            type(maximum_database_bytes) is not int
            or not _MINIMUM_LEDGER_BYTES
            <= maximum_database_bytes
            <= _MAXIMUM_LEDGER_BYTES
        ):
            msg = "explicit SQLite file bound must be 256KiB..2GiB"
            raise ValueError(msg)
        self.maximum_database_bytes = maximum_database_bytes
        self._pid = os.getpid()
        self._lock: BinaryIO | None = None
        self._connection: sqlite3.Connection | None = None
        try:
            self._lock = Path(str(self.database) + ".writer.lock").open("a+b")
            self._lock.seek(0, os.SEEK_END)
            if self._lock.tell() == 0:
                self._lock.write(b"0")
                self._lock.flush()
            self._lock.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)  # type: ignore[attr-defined]  # Windows has no fcntl stubs.
            connection = sqlite3.connect(
                self.database,
                timeout=timeout_seconds,
                isolation_level=None,
            )
            self._connection = connection
            if maximum_database_bytes is not None:
                page_size = int(connection.execute("PRAGMA page_size").fetchone()[0])
                pages = maximum_database_bytes // page_size
                actual = int(
                    connection.execute(f"PRAGMA max_page_count={pages}").fetchone()[0],
                )
                if actual != pages:
                    msg = "database cannot satisfy the explicit page ceiling"
                    raise RecordingError(msg)
            tables = connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'",
            ).fetchall()
            version = connection.execute("PRAGMA user_version").fetchone()[0]
            if tables or version:
                _validate_schema(connection)
            journal = connection.execute("PRAGMA journal_mode=DELETE").fetchone()[0]
            if journal != "delete":
                msg = "Rollback-journal DELETE could not be established"
                raise RecordingError(msg)
            connection.execute("PRAGMA synchronous=FULL")
            connection.execute("PRAGMA foreign_keys=ON")
            if not tables and version == 0:
                connection.execute("BEGIN IMMEDIATE")
                try:
                    for statement in _SCHEMA.split(";"):
                        if statement.strip():
                            connection.execute(statement)
                    connection.execute("PRAGMA user_version=1")
                    connection.commit()
                except BaseException:
                    connection.rollback()
                    raise
            _validate_schema(connection)
        except (OSError, sqlite3.Error, RecordingError) as error:
            self.close()
            if isinstance(error, RecordingError):
                raise
            msg = f"Cannot open execution recorder at {self.database}: {error}"
            raise RecordingError(msg) from error

    def __enter__(self) -> Self:
        """Apply the explicit   enter   contract within this owner."""
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        """Apply the explicit   exit   contract within this owner."""
        self.close()

    def close(self) -> None:
        """Release the writer owner; an unfinished activation remains unknown."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        if self._lock is not None:
            self._lock.close()
            self._lock = None

    def record(self, event: ExecutionEvent) -> ExecutionEvent:
        """Validate transition and commit event plus projection atomically."""
        if not isinstance(event, ExecutionEvent):
            msg = "record requires ExecutionEvent"
            raise TypeError(msg)
        connection = self._connection
        if connection is None or self._pid != os.getpid():
            msg = "Recorder is closed or belongs to another process"
            raise RecordingError(msg)
        try:
            connection.execute("BEGIN IMMEDIATE")
            result = self._record(connection, event)
            connection.commit()
            return result
        except BaseException as error:
            connection.rollback()
            if isinstance(error, sqlite3.Error):
                msg = f"Execution record commit failed: {error}"
                raise RecordingError(msg) from error
            raise

    def _record(
        self,
        connection: sqlite3.Connection,
        event: ExecutionEvent,
    ) -> ExecutionEvent:
        previous = connection.execute(
            "SELECT document FROM events WHERE id=?",
            (str(event.event_id),),
        ).fetchone()
        if previous:
            stored = decode(previous[0])
            if replace(stored, observed_at=None) != replace(event, observed_at=None):
                msg = "Conflicting duplicate event identity"
                raise ValueError(msg)
            return stored
        if event.observed_at is not None:
            msg = "observation time is assigned by the recorder"
            raise ValueError(msg)
        payload = event.payload
        eid, aid = (str(event.execution_id), str(event.activation_id))
        if isinstance(payload, Admitted):
            if event.sequence != 1:
                msg = "admission must be first"
                raise ValueError(msg)
            if event.parent_execution_id is not None:
                parent = connection.execute(
                    "SELECT lifecycle FROM executions WHERE id=?",
                    (str(event.parent_execution_id),),
                ).fetchone()
                if parent != ("running",):
                    msg = "child admission requires an active recorded parent"
                    raise ValueError(msg)
            connection.execute(
                "INSERT INTO executions VALUES (?,?,'pending',NULL,NULL)",
                (eid, payload.operation),
            )
            connection.execute(
                "INSERT INTO activations VALUES (?,?,?,NULL,NULL,NULL)",
                (aid, eid, event.producer),
            )
        else:
            row = connection.execute(
                "SELECT lifecycle,active_stage FROM executions WHERE id=?",
                (eid,),
            ).fetchone()
            activation = connection.execute(
                "SELECT execution_id,producer FROM activations WHERE id=?",
                (aid,),
            ).fetchone()
            last = connection.execute(
                (
                    "SELECT document FROM events WHERE activation_id=? ORDER BY seque"
                    "nce DESC LIMIT 1"
                ),
                (aid,),
            ).fetchone()
            if row is None or activation != (eid, event.producer) or last is None:
                msg = "event requires its admitted activation"
                raise ValueError(msg)
            prior = decode(last[0])
            if event.sequence != prior.sequence + 1 or (
                event.elapsed_seconds < prior.elapsed_seconds
                or event.parent_execution_id != prior.parent_execution_id
            ):
                msg = "event order, duration or parent identity is inconsistent"
                raise ValueError(msg)
            lifecycle, stage = row
            if lifecycle == "stopped" and (
                not (
                    isinstance(payload, Diagnostic)
                    and payload.category is FailureCategory.OBSERVER
                    and (payload.severity is Severity.WARNING)
                )
            ):
                msg = "execution is already terminal"
                raise ValueError(msg)
            if isinstance(payload, Activated):
                if lifecycle != "pending":
                    msg = "activation cannot start twice"
                    raise ValueError(msg)
                connection.execute(
                    "UPDATE executions SET lifecycle='running' WHERE id=?",
                    (eid,),
                )
                connection.execute(
                    "UPDATE activations SET started_at=?,pid=? WHERE id=?",
                    (event.occurred_at.isoformat(), payload.process_id, aid),
                )
            elif isinstance(payload, Terminal):
                if payload.outcome is Outcome.COMPLETED and (
                    lifecycle != "running" or stage is not None
                ):
                    msg = "completion requires activation and finished stage"
                    raise ValueError(msg)
                connection.execute(
                    "UPDATE executions SET lifecycle='stopped',outcome=? WHERE id=?",
                    (payload.outcome.value, eid),
                )
                connection.execute(
                    "UPDATE activations SET ended_at=? WHERE id=?",
                    (event.occurred_at.isoformat(), aid),
                )
            elif isinstance(payload, Diagnostic):
                if payload.stage != stage:
                    msg = "diagnostic stage differs from active stage"
                    raise ValueError(msg)
            else:
                if lifecycle != "running":
                    msg = "stage/progress requires activation"
                    raise ValueError(msg)
                if isinstance(payload, StageStarted):
                    if stage is not None:
                        msg = "finish the active stage before starting another"
                        raise ValueError(msg)
                    connection.execute(
                        "UPDATE executions SET active_stage=? WHERE id=?",
                        (payload.stage, eid),
                    )
                elif isinstance(payload, StageFinished):
                    if stage != payload.stage:
                        msg = "stage finish must match active stage"
                        raise ValueError(msg)
                    connection.execute(
                        "UPDATE executions SET active_stage=NULL WHERE id=?",
                        (eid,),
                    )
                elif isinstance(payload, Progress):
                    if stage != payload.stage:
                        msg = "progress must match active stage"
                        raise ValueError(msg)
                    rows = connection.execute(
                        (
                            "SELECT document FROM events WHERE activation_id=? "
                            "AND kind='Prog"
                            "ress' AND sequence > (SELECT MAX(sequence) FROM ev"
                            "ents WHERE act"
                            "ivation_id=? AND kind='StageStarted') ORDER BY seq"
                            "uence DESC"
                        ),
                        (aid, aid),
                    )
                    for row in rows:
                        old = decode(row[0]).payload
                        if isinstance(old, Progress) and old.stage == stage:
                            if (
                                old.unit != payload.unit
                                or old.total != payload.total
                                or (
                                    old.completed is not None
                                    and (
                                        payload.completed is None
                                        or payload.completed < old.completed
                                    )
                                )
                            ):
                                msg = "progress must preserve unit, total and monotone count"
                                raise ValueError(msg)
                            break
        observed = replace(event, observed_at=Timestamp.now().value)
        connection.execute(
            "INSERT INTO events VALUES (?,?,?,?,?,?)",
            (
                str(event.event_id),
                eid,
                aid,
                event.sequence,
                event.kind,
                encode(observed),
            ),
        )
        return observed


def _read_history(
    connection: sqlite3.Connection,
    execution_id: UUID,
) -> ExecutionHistory | None:
    row = connection.execute(
        "SELECT operation,lifecycle,outcome,active_stage FROM executions WHERE id=?",
        (str(execution_id),),
    ).fetchone()
    if row is None:
        return None
    events = tuple(
        _decode_record(item)
        for item in connection.execute(
            (
                "SELECT id,execution_id,activation_id,sequence,kind,document FROM"
                " events WHERE execution_id=? ORDER BY sequence"
            ),
            (str(execution_id),),
        )
    )
    if (
        not events
        or not isinstance(events[0].payload, Admitted)
        or events[0].payload.operation != row[0]
        or ([e.sequence for e in events] != list(range(1, len(events) + 1)))
        or any(
            e.execution_id != execution_id
            or e.observed_at is None
            or e.parent_execution_id != events[0].parent_execution_id
            for e in events
        )
        or any(
            (
                b.elapsed_seconds < a.elapsed_seconds
                for a, b in itertools.pairwise(events)
            ),
        )
    ):
        msg = "Stored execution event history is inconsistent"
        raise RecordingError(msg)
    outcome = None if row[2] is None else Outcome(row[2])
    activations = tuple(
        ActivationHistory(
            UUID(item[0]),
            None if item[1] is None else datetime.fromisoformat(item[1]),
            None if item[2] is None else datetime.fromisoformat(item[2]),
            item[3],
            outcome,
        )
        for item in connection.execute(
            "SELECT id,started_at,ended_at,pid FROM activations WHERE execution_id=?",
            (str(execution_id),),
        )
    )
    terminals = [e.payload for e in events if isinstance(e.payload, Terminal)]
    activated = [e for e in events if isinstance(e.payload, Activated)]
    expected_lifecycle = (
        Lifecycle.STOPPED
        if terminals
        else Lifecycle.RUNNING
        if activated
        else Lifecycle.PENDING
    )
    if (
        row[1] != expected_lifecycle
        or len(activations) != 1
        or len(activated) > 1
        or any(e.activation_id != activations[0].activation_id for e in events)
    ):
        msg = "Activation/lifecycle projection is inconsistent"
        raise RecordingError(msg)
    if (outcome is None and terminals) or (
        outcome is not None and (len(terminals) != 1 or terminals[0].outcome != outcome)
    ):
        msg = "Terminal projection conflicts with recorded events"
        raise RecordingError(msg)
    _validate_lifecycle(events, activations, row[3])
    return ExecutionHistory(
        execution_id,
        row[0],
        Lifecycle(row[1]),
        outcome,
        activations,
        events,
    )


def _decode_record(row: tuple[str, str, str, int, str, str]) -> ExecutionEvent:
    """One existing codec, with SQL projection/envelope identity correspondence."""
    event = decode(row[5])
    if row[:5] != (
        str(event.event_id),
        str(event.execution_id),
        str(event.activation_id),
        event.sequence,
        event.kind,
    ):
        msg = "Stored event columns conflict with event envelope"
        raise RecordingError(msg)
    return event


def _validate_lifecycle(
    events: tuple[ExecutionEvent, ...],
    activations: tuple[ActivationHistory, ...],
    projected_stage: str | None,
) -> None:
    """Read-side counterpart of the recorder's existing transition rules."""
    lifecycle, stage = (Lifecycle.PENDING, None)
    progress: Progress | None = None
    producer = events[0].producer
    for event in events[1:]:
        p = event.payload
        if event.producer != producer or isinstance(p, Admitted):
            msg = "Conflicting producer or repeated admission"
            raise RecordingError(msg)
        if lifecycle is Lifecycle.STOPPED and (
            not (
                isinstance(p, Diagnostic)
                and p.category is FailureCategory.OBSERVER
                and (p.severity is Severity.WARNING)
            )
        ):
            msg = "Unexpected event after terminal acknowledgment"
            raise RecordingError(msg)
        if isinstance(p, Activated):
            if lifecycle is not Lifecycle.PENDING:
                msg = "Repeated or unordered activation"
                raise RecordingError(msg)
            lifecycle = Lifecycle.RUNNING
            if (activations[0].started_at, activations[0].process_id) != (
                event.occurred_at,
                p.process_id,
            ):
                msg = "Activation projection differs from event"
                raise RecordingError(msg)
        elif isinstance(p, Terminal):
            if p.outcome is Outcome.COMPLETED and (
                lifecycle is not Lifecycle.RUNNING or stage is not None
            ):
                msg = "Completion requires activation and finished stage"
                raise RecordingError(msg)
            lifecycle = Lifecycle.STOPPED
            if activations[0].ended_at != event.occurred_at:
                msg = "Terminal projection timestamp differs"
                raise RecordingError(msg)
        elif isinstance(p, Diagnostic):
            if p.stage != stage:
                msg = "Diagnostic differs from active stage"
                raise RecordingError(msg)
        else:
            if lifecycle is not Lifecycle.RUNNING:
                msg = "Stage/progress requires active occurrence"
                raise RecordingError(msg)
            if isinstance(p, StageStarted):
                if stage is not None:
                    msg = "Unfinished stage before new stage"
                    raise RecordingError(msg)
                stage, progress = (p.stage, None)
            elif isinstance(p, StageFinished):
                if stage != p.stage:
                    msg = "Stage finish differs from active stage"
                    raise RecordingError(msg)
                stage = None
            elif isinstance(p, Progress):
                if stage != p.stage or (
                    progress is not None
                    and (
                        progress.unit != p.unit
                        or progress.total != p.total
                        or (
                            progress.completed is not None
                            and (
                                p.completed is None or p.completed < progress.completed
                            )
                        )
                    )
                ):
                    msg = "Invalid stage/progress transition"
                    raise RecordingError(msg)
                progress = p
    if projected_stage != stage:
        msg = "Active-stage projection conflicts with events"
        raise RecordingError(msg)


class SQLiteInspectionSession:
    """One private read-only transaction with once-per-snapshot structural checks.

    This is ephemeral inspection authority, never a persistent validation cache.
    A live WAL writer may commit while this session continues reading its original
    snapshot; rollback-journal writers may wait for the reader. No immutable=1,
    shared cache, dirty reads, public SQL interface or writer change is involved.
    """

    def __init__(self, database: Path) -> None:
        """Initialize the explicitly scoped scientific boundary."""
        if not isinstance(database, Path):
            msg = "inspection requires Path"
            raise TypeError(msg)
        self._database = database.resolve()
        self._connection: sqlite3.Connection | None = None
        self._entered = False
        self._owner = (os.getpid(), threading.get_ident())
        self._identity: tuple[int, int, int, int] | None = None
        self._children: dict[UUID | None, tuple[UUID, ...]] | None = None
        self._histories: dict[UUID, ExecutionHistory | None] = {}
        self._positions: dict[UUID, int] = {}

    @property
    def database(self) -> Path:
        """Exact bound source path, not a semantic empirical-state identity."""
        return self._database

    def _source_identity(self) -> tuple[int, int, int, int]:
        info = self._database.stat()
        if not stat.S_ISREG(info.st_mode) or not info.st_ino:
            msg = "Identifiable regular database file required"
            raise RecordingError(msg)
        return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)

    def __enter__(self) -> Self:
        """Apply the explicit   enter   contract within this owner."""
        if self._entered or self._owner != (os.getpid(), threading.get_ident()):
            msg = "Inspection session is single-use and owner-bound"
            raise RecordingError(msg)
        self._entered = True
        try:
            self._identity = self._source_identity()
            connection = sqlite3.connect(
                self._database.as_uri() + "?mode=ro&cache=private",
                uri=True,
                isolation_level=None,
                timeout=0.25,
            )
            self._connection = connection
            connection.execute("PRAGMA query_only=ON")
            connection.execute("BEGIN")
            connection.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
            mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
            if mode not in ("delete", "truncate", "persist", "wal"):
                raise RecordingError("Unsupported inspection journal mode: " + mode)
            _validate_schema(connection)
            if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
                msg = "Execution database foreign-key integrity failed"
                raise RecordingError(msg)
            self._checked()
            return self
        except (OSError, sqlite3.Error, ValueError, TypeError, RecordingError) as error:
            self.close()
            if isinstance(error, RecordingError):
                raise
            msg = f"Cannot open inspection snapshot: {error}"
            raise RecordingError(msg) from error

    def _checked(self) -> sqlite3.Connection:
        try:
            connection = self._connection
            if (
                connection is None
                or self._owner != (os.getpid(), threading.get_ident())
                or (not connection.in_transaction)
                or (self._identity != self._source_identity())
            ):
                msg = "Closed, expired, replaced or foreign inspection session"
                raise RecordingError(msg)
            return connection
        except (OSError, sqlite3.Error) as error:
            msg = f"Inspection snapshot is unavailable: {error}"
            raise RecordingError(msg) from error

    def require_database(self, database: Path) -> None:
        """Reject accidental cross-database use of shared inspection authority."""
        if not isinstance(database, Path):
            msg = "inspection requires Path"
            raise TypeError(msg)
        self._checked()
        if database.resolve() != self._database:
            msg = "Inspection session belongs to another database"
            raise RecordingError(msg)

    def close(self) -> None:
        """Release the transaction and all session-local relationship information."""
        if self._connection is not None and self._owner != (
            os.getpid(),
            threading.get_ident(),
        ):
            msg = "Only the owning process/thread may close a snapshot"
            raise RecordingError(msg)
        connection, self._connection = (self._connection, None)
        self._children = None
        self._histories.clear()
        self._positions.clear()
        if connection is not None:
            connection.close()

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        """Apply the explicit   exit   contract within this owner."""
        try:
            if error is None and self._connection is not None:
                self._checked()
        finally:
            self.close()

    def inspect_execution(self, execution_id: UUID) -> ExecutionHistory | None:
        """Read this snapshot's immutable history; callers retain semantic checks.

        Reuse is confined to this pinned transaction, including absent histories.
        Check the live session before every lookup, even an already decoded ID.
        """
        if not isinstance(execution_id, UUID):
            msg = "inspection requires UUID"
            raise TypeError(msg)
        try:
            connection = self._checked()
            if execution_id not in self._histories:
                self._histories[execution_id] = _read_history(connection, execution_id)
            return self._histories[execution_id]
        except (
            sqlite3.Error,
            ValueError,
            TypeError,
            KeyError,
            RecordingError,
        ) as error:
            self.close()
            if isinstance(error, RecordingError):
                raise
            msg = f"Cannot inspect execution history: {error}"
            raise RecordingError(msg) from error

    def execution_ids(self, *, operation: str | None = None) -> tuple[UUID, ...]:
        """Enumerate the exact snapshot's occurrence membership in admission order."""
        if operation is not None and (
            type(operation) is not str or not operation.strip()
        ):
            msg = "nonempty identified operation required"
            raise ValueError(msg)
        try:
            connection = self._checked()
            rows = connection.execute(
                "SELECT id FROM executions ORDER BY rowid"
                if operation is None
                else "SELECT id FROM executions WHERE operation=? ORDER BY rowid",
                () if operation is None else (operation,),
            )
            return tuple(UUID(row[0]) for row in rows)
        except (sqlite3.Error, ValueError, TypeError, RecordingError) as error:
            self.close()
            if isinstance(error, RecordingError):
                raise
            msg = f"Cannot inspect occurrence membership: {error}"
            raise RecordingError(msg) from error

    def recorded_before(self, first_event_id: UUID, second_event_id: UUID) -> bool:
        """Compare two acknowledged events in this snapshot's committed order.

        SQLite recording order, rather than wall-clock fields, establishes this
        source-local fact. Both identified records must exist and decode; missing
        evidence is an error, never an apparently valid reversed ordering.
        """
        if not isinstance(first_event_id, UUID) or not isinstance(
            second_event_id,
            UUID,
        ):
            msg = "recorded event ordering requires UUIDs"
            raise TypeError(msg)
        if first_event_id == second_event_id:
            msg = "recorded ordering requires two distinct events"
            raise ValueError(msg)
        try:
            connection = self._checked()
            missing = tuple(
                i for i in (first_event_id, second_event_id) if i not in self._positions
            )
            for identifier in missing:
                row = connection.execute(
                    (
                        "SELECT rowid,id,execution_id,activation_id,sequence,ki"
                        "nd,documen"
                        "t FROM events WHERE id=?"
                    ),
                    (str(identifier),),
                ).fetchone()
                if row is None:
                    msg = "Original acknowledged ordering events missing"
                    raise RecordingError(msg)
                event = _decode_record(row[1:])
                if event.observed_at is None:
                    msg = "Unacknowledged event has no recording order"
                    raise RecordingError(msg)
                if event.event_id != identifier:
                    msg = "Recorded ordering event identity differs"
                    raise RecordingError(msg)
                self._positions[identifier] = row[0]
            return bool(
                self._positions[first_event_id] < self._positions[second_event_id],
            )
        except (
            sqlite3.Error,
            ValueError,
            TypeError,
            KeyError,
            RecordingError,
        ) as error:
            self.close()
            if isinstance(error, RecordingError):
                raise
            msg = f"Cannot inspect recorded event order: {error}"
            raise RecordingError(msg) from error

    def child_execution_ids(self, parent_execution_id: UUID) -> tuple[UUID, ...]:
        """One validated snapshot-local admission index, no repeated global scans."""
        if not isinstance(parent_execution_id, UUID):
            msg = "inspection requires UUID"
            raise TypeError(msg)
        try:
            connection = self._checked()
            if self._children is None:
                children: dict[UUID | None, list[UUID]] = {}
                admitted: set[UUID] = set()
                active: set[UUID] = set()
                for row in connection.execute(
                    (
                        "SELECT id,execution_id,activation_id,sequence,kind,doc"
                        "ument FROM"
                        " events WHERE sequence=1 OR kind IN ('Admitted','Activ"
                        "ated','Ter"
                        "minal') ORDER BY rowid"
                    ),
                ):
                    event = _decode_record(row)
                    identity, payload = (event.execution_id, event.payload)
                    if event.observed_at is None:
                        msg = "Unacknowledged relationship event"
                        raise RecordingError(msg)
                    if isinstance(payload, Admitted):
                        if (
                            event.sequence != 1
                            or identity in admitted
                            or (
                                event.parent_execution_id is not None
                                and event.parent_execution_id not in active
                            )
                        ):
                            msg = "Invalid child admission/parent relationship"
                            raise RecordingError(msg)
                        admitted.add(identity)
                        children.setdefault(event.parent_execution_id, []).append(
                            identity,
                        )
                    elif isinstance(payload, Activated):
                        if identity not in admitted or identity in active:
                            msg = "Invalid activation relationship"
                            raise RecordingError(msg)
                        active.add(identity)
                    elif isinstance(payload, Terminal):
                        active.discard(identity)
                    else:
                        msg = "First occurrence record is not an admission"
                        raise RecordingError(msg)
                if admitted != set(self.execution_ids()):
                    msg = "Occurrence/admission membership differs"
                    raise RecordingError(msg)
                self._children = {k: tuple(v) for k, v in children.items()}
            return self._children.get(parent_execution_id, ())
        except (
            sqlite3.Error,
            ValueError,
            TypeError,
            KeyError,
            RecordingError,
        ) as error:
            self.close()
            if isinstance(error, RecordingError):
                raise
            msg = f"Cannot inspect child identities: {error}"
            raise RecordingError(msg) from error


def inspect_execution(
    database: Path,
    execution_id: UUID,
    *,
    session: SQLiteInspectionSession | None = None,
) -> ExecutionHistory | None:
    """One-off verified read, or the same semantic check in an explicit snapshot."""
    if not isinstance(database, Path) or not isinstance(execution_id, UUID):
        msg = "inspection requires Path and UUID"
        raise TypeError(msg)
    if session is not None:
        session.require_database(database)
        return session.inspect_execution(execution_id)
    with SQLiteInspectionSession(database) as opened:
        return opened.inspect_execution(execution_id)


def inspect_child_execution_ids(
    database: Path,
    parent_execution_id: UUID,
    *,
    session: SQLiteInspectionSession | None = None,
) -> tuple[UUID, ...]:
    """Direct children in committed admission order, including unexpected children."""
    if not isinstance(database, Path) or not isinstance(parent_execution_id, UUID):
        msg = "inspection requires Path and UUID"
        raise TypeError(msg)
    if session is not None:
        session.require_database(database)
        return session.child_execution_ids(parent_execution_id)
    with SQLiteInspectionSession(database) as opened:
        return opened.child_execution_ids(parent_execution_id)


def inspect_execution_ids(
    database: Path,
    *,
    operation: str | None = None,
    session: SQLiteInspectionSession | None = None,
) -> tuple[UUID, ...]:
    """Bounded typed membership read; callers cannot supply arbitrary SQL."""
    if not isinstance(database, Path):
        msg = "inspection requires Path"
        raise TypeError(msg)
    if session is not None:
        session.require_database(database)
        return session.execution_ids(operation=operation)
    with SQLiteInspectionSession(database) as opened:
        return opened.execution_ids(operation=operation)
