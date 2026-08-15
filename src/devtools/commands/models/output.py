# Copyright (c) 2026
"""Command output retention policy."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommandOutputPolicy:
    """Bound memory retained for one command execution.

    Output limits apply independently to standard output and standard error.
    Event buffering is best effort: any newly emitted event is dropped when the
    pending event limit is reached so process draining never waits for a
    consumer. No event type is privileged.

    :ivar max_stdout_bytes: Maximum stdout bytes retained in a result.
    :ivar max_stderr_bytes: Maximum stderr bytes retained in a result.
    :ivar max_pending_events: Maximum events awaiting the single consumer.
    """

    max_stdout_bytes: int = 1_048_576
    max_stderr_bytes: int = 1_048_576
    max_pending_events: int = 1_024

    def __post_init__(self) -> None:
        """Validate output-retention invariants."""
        if self.max_stdout_bytes < 0:
            msg = "Maximum stdout bytes cannot be negative."
            raise ValueError(msg)

        if self.max_stderr_bytes < 0:
            msg = "Maximum stderr bytes cannot be negative."
            raise ValueError(msg)

        if self.max_pending_events <= 0:
            msg = "Maximum pending events must be positive."
            raise ValueError(msg)
