# Copyright (c) 2026
"""Elapsed-time measurement primitives."""

from __future__ import annotations

import time as standard_time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self

from devtools.time.models.duration import Duration

if TYPE_CHECKING:
    from types import TracebackType

perf_counter_ns = standard_time.perf_counter_ns


@dataclass(slots=True)
class Stopwatch:
    """Measure elapsed time using a monotonic high-resolution clock.

    A stopwatch begins running immediately upon construction and may be used
    either explicitly or as a context manager.

    Examples
    --------
    Manual usage::

        stopwatch = Stopwatch()

        do_work()

        stopwatch.stop()

        print(stopwatch.elapsed)

    Context manager::

        with Stopwatch() as stopwatch:
            do_work()

        print(stopwatch.elapsed)

    """

    _started_ns: int = field(init=False, repr=False)
    _stopped_ns: int | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Start the stopwatch immediately after construction."""
        self._started_ns = perf_counter_ns()

    def __enter__(self) -> Self:
        """Enter the stopwatch context.

        :returns: This stopwatch instance.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop the stopwatch when leaving the context.

        Any exception is allowed to propagate normally.
        """
        self.stop()

    @property
    def is_running(self) -> bool:
        """Return whether the stopwatch is currently running.

        :returns: ``True`` while the stopwatch has not been stopped.
        """
        return self._stopped_ns is None

    @property
    def is_stopped(self) -> bool:
        """Return whether the stopwatch has been stopped.

        :returns: ``True`` after :meth:`stop` has been called.
        """
        return self._stopped_ns is not None

    @property
    def elapsed(self) -> Duration:
        """Return the elapsed duration.

        While running, the elapsed duration is calculated against the current
        monotonic clock. Once stopped, the duration remains constant.

        :returns: Elapsed duration.
        """
        end_ns = perf_counter_ns() if self._stopped_ns is None else self._stopped_ns

        return Duration.nanoseconds(end_ns - self._started_ns)

    def stop(self) -> Duration:
        """Stop the stopwatch.

        Calling this method multiple times is idempotent.

        :returns: Final elapsed duration.
        """
        if self._stopped_ns is None:
            self._stopped_ns = perf_counter_ns()

        return self.elapsed
