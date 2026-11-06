# Copyright (c) 2026
"""Explicit managed empirical observation; no scheduler or implicit global state."""

from __future__ import annotations

import os
import platform
import socket
import time
import traceback
from dataclasses import replace
from typing import TYPE_CHECKING, Literal, Protocol, Self
from uuid import UUID, uuid4

from devtools.core.time import Timestamp
from devtools.learning.evidence.events import (
    Activated,
    Admitted,
    Diagnostic,
    ExceptionFact,
    ExecutionEvent,
    Fact,
    FailureCategory,
    Outcome,
    Payload,
    Progress,
    Severity,
    StageFinished,
    StageStarted,
    Terminal,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import TracebackType

_EXCEPTION_CHAIN_LIMIT = 8
_EXCEPTION_MESSAGE_LIMIT = 4000
_TRACEBACK_CHARACTER_LIMIT = 16000


class RecordingError(RuntimeError):
    """Required history is not acknowledged; computation may still have occurred."""

    def __init__(self, message: str) -> None:
        """Initialize the explicitly scoped scientific boundary."""
        super().__init__(message)
        self.execution_id: UUID | None = None
        self.last_acknowledged_sequence = 0
        self.computation_outcome: Outcome | None = None


class ExecutionRecorder(Protocol):
    """Acknowledge a validated event only after its required persistence commits."""

    def record(self, event: ExecutionEvent) -> ExecutionEvent:
        """Apply the explicit record contract within this owner."""
        ...


def exception_diagnostic(
    error: BaseException,
    category: FailureCategory,
    stage: str | None,
    severity: Severity = Severity.ERROR,
) -> Diagnostic:
    """Bound evidence without interpreting exception text as root cause."""
    chain: list[ExceptionFact] = []
    seen: set[int] = set()
    current: BaseException | None = error
    relation = "primary"
    truncated = False
    while (
        current is not None
        and id(current) not in seen
        and (len(chain) < _EXCEPTION_CHAIN_LIMIT)
    ):
        seen.add(id(current))
        message = str(current)
        truncated |= len(message) > _EXCEPTION_MESSAGE_LIMIT
        chain.append(
            ExceptionFact(
                f"{type(current).__module__}.{type(current).__qualname__}",
                message[:4000],
                relation,
            ),
        )
        if current.__cause__ is not None:
            current, relation = (current.__cause__, "cause")
        elif not current.__suppress_context__:
            current, relation = (current.__context__, "context")
        else:
            current = None
    trace = "".join(traceback.format_exception(error))
    truncated |= current is not None or len(trace) > _TRACEBACK_CHARACTER_LIMIT
    return Diagnostic(
        category,
        severity,
        str(error)[:4000] or type(error).__name__,
        stage,
        tuple(chain),
        trace[:16000],
        truncated,
    )


class ExecutionContext:
    """One admitted activation with synchronous required acknowledgments.

    Use within an explicit concrete operation. No automatic retry/resume is
    offered. Exceptions raised before entering this boundary are caller work.
    A remote producer may supply only its active parent's UUID; the required
    recorder, rather than a transferred runtime object, validates that lineage.
    """

    def __init__(
        self,
        recorder: ExecutionRecorder,
        request: Admitted,
        *,
        observer: Callable[[ExecutionEvent], None] | None = None,
        parent: ExecutionContext | None = None,
        parent_execution_id: UUID | None = None,
    ) -> None:
        """Initialize the explicitly scoped scientific boundary."""
        if not isinstance(request, Admitted):
            msg = "request must use Admitted"
            raise TypeError(msg)
        if parent_execution_id is not None and (
            not isinstance(parent_execution_id, UUID) or parent is not None
        ):
            msg = "remote parent requires a UUID and no live parent context"
            raise ValueError(msg)
        if parent is not None:
            parent.require_child_recorder(recorder)
        self.parent_execution_id = (
            parent.execution_id if parent else parent_execution_id
        )
        self.execution_id: UUID = uuid4()
        self.activation_id = uuid4()
        self._recorder: ExecutionRecorder = recorder
        self._request = request
        self._observer = observer
        self._producer = f"{socket.gethostname()}:{os.getpid()}"
        self._clock = time.perf_counter()
        self._sequence = 0
        self._started = False
        self._stopped = False
        self._stage: str | None = None
        self._stage_started = 0.0
        self._category = FailureCategory.INPUT
        self._output_facts: tuple[Fact, ...] = ()
        self._computed = False
        self._progress: Progress | None = None

    @property
    def active_stage(self) -> str | None:
        """Apply the explicit active stage contract within this owner."""
        return self._stage

    def __enter__(self) -> Self:
        """Apply the explicit   enter   contract within this owner."""
        if self._started or self._sequence:
            msg = "context cannot be entered twice"
            raise ValueError(msg)
        try:
            self._emit(self._request)
            self._emit(
                Activated(
                    os.getpid(),
                    socket.gethostname(),
                    platform.python_version(),
                    platform.platform(),
                ),
            )
        except BaseException as error:
            if self._sequence:
                self.__exit__(type(error), error, error.__traceback__)
            raise
        self._started = True
        return self

    def _emit(self, payload: Payload, *, notify: bool = True) -> ExecutionEvent:
        event = ExecutionEvent(
            event_id=uuid4(),
            execution_id=self.execution_id,
            activation_id=self.activation_id,
            producer=self._producer,
            sequence=self._sequence + 1,
            occurred_at=Timestamp.now().value,
            elapsed_seconds=time.perf_counter() - self._clock,
            payload=payload,
            parent_execution_id=self.parent_execution_id,
        )
        try:
            acknowledged = self._recorder.record(event)
            self._validate_acknowledgment(event, acknowledged)
        except Exception as error:
            failure = (
                error
                if isinstance(error, RecordingError)
                else RecordingError("Required recorder did not acknowledge the event")
            )
            failure.execution_id = self.execution_id
            failure.last_acknowledged_sequence = self._sequence
            failure.computation_outcome = Outcome.COMPLETED if self._computed else None
            if failure is error:
                raise
            raise failure from error
        self._sequence = event.sequence
        if notify and self._observer is not None:
            try:
                self._observer(acknowledged)
            except Exception as error:  # noqa: BLE001 -- arbitrary optional callback; recorded without altering computation
                self._observer = None
                self._emit(
                    exception_diagnostic(
                        error,
                        FailureCategory.OBSERVER,
                        self._stage,
                        Severity.WARNING,
                    ),
                    notify=False,
                )
        return acknowledged

    @staticmethod
    def _validate_acknowledgment(
        event: ExecutionEvent,
        acknowledged: ExecutionEvent,
    ) -> None:
        """Require the exact immutable event with an observed commit time."""
        if (
            not isinstance(acknowledged, ExecutionEvent)
            or acknowledged.observed_at is None
            or replace(acknowledged, observed_at=None) != event
        ):
            msg = "Recorder returned an invalid acknowledgment"
            raise RecordingError(msg)

    def _running(self) -> None:
        if not self._started or self._stopped:
            msg = "operation must be active and nonterminal"
            raise ValueError(msg)

    def require_child_recorder(self, recorder: ExecutionRecorder) -> None:
        """Require live parent custody and the same acknowledged history owner."""
        self._running()
        if recorder is not self._recorder:
            msg = "parent and child must share the required recorder"
            raise ValueError(msg)

    def stage(
        self,
        name: str,
        description: str,
        category: FailureCategory,
        *,
        facts: tuple[Fact, ...] = (),
    ) -> None:
        """Close a successful prior stage and observe the next actual boundary."""
        self._running()
        self._finish_stage()
        if not isinstance(category, FailureCategory):
            msg = "category must use FailureCategory"
            raise TypeError(msg)
        self._stage, self._category = (name, category)
        self._progress = None
        event = self._emit(StageStarted(name, description, facts))
        self._stage_started = event.elapsed_seconds

    def _finish_stage(self) -> None:
        if self._stage is not None:
            name = self._stage
            duration = time.perf_counter() - self._clock - self._stage_started
            self._stage = None
            self._emit(StageFinished(name, duration))

    def progress(
        self,
        unit: str,
        completed: int | None = None,
        total: int | None = None,
    ) -> None:
        """Apply the explicit progress contract within this owner."""
        self._running()
        if self._stage is None:
            msg = "progress requires an active stage"
            raise ValueError(msg)
        progress = Progress(self._stage, unit, completed, total)
        old = self._progress
        if old is not None and (
            old.unit != progress.unit
            or old.total != progress.total
            or (
                old.completed is not None
                and (progress.completed is None or progress.completed < old.completed)
            )
        ):
            msg = "progress must preserve unit, total and monotone count"
            raise ValueError(msg)
        self._emit(progress)
        self._progress = progress

    def diagnostic(self, diagnostic: Diagnostic) -> None:
        """Apply the explicit diagnostic contract within this owner."""
        self._running()
        self._emit(diagnostic)

    def completed(self, facts: tuple[Fact, ...] = ()) -> None:
        """Retain small validated output facts, not fitted/backend state."""
        self._running()
        Terminal(Outcome.COMPLETED, facts)
        self._output_facts = facts
        self._computed = True

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> Literal[False]:
        """Apply the explicit   exit   contract within this owner."""
        if self._stopped:
            msg = "operation is already terminal"
            raise ValueError(msg)
        if error is None:
            self._computed = True
            self._finish_stage()
            self._emit(Terminal(Outcome.COMPLETED, self._output_facts))
            self._stopped = True
            return False
        category = self._category
        outcome = Outcome.FAILED
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            category, outcome = (FailureCategory.INTERRUPTION, Outcome.INTERRUPTED)
        elif isinstance(error, RecordingError):
            category = FailureCategory.RECORDING
        try:
            self._emit(exception_diagnostic(error, category, self._stage))
            self._emit(Terminal(outcome))
            self._stopped = True
        except Exception as recording_error:  # noqa: BLE001 -- retain the primary failure and explicitly report incomplete recording
            error.add_note(
                f"Required recording incomplete for {self.execution_id}; "
                f"last acknowledged sequence={self._sequence}; "
                f"{type(recording_error).__name__}: {recording_error}",
            )
        return False
