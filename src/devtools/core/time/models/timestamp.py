# Copyright (c) 2026
"""Time value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from devtools.core.time.errors import TimestampParsingError

from .duration import Duration


@dataclass(frozen=True, slots=True)
class Timestamp:
    """Represent an immutable UTC timestamp.

    All timestamp values must be timezone-aware. Aware values supplied in
    another timezone are normalized to UTC during construction.

    :ivar value: Timezone-aware datetime normalized to UTC.
    """

    value: datetime

    def __post_init__(self) -> None:
        """Normalize and validate the timestamp value."""
        self._validate()

        normalized = self.value.astimezone(UTC)
        object.__setattr__(self, "value", normalized)

    def _validate(self) -> None:
        """Validate timestamp invariants.

        :raises ValueError: If the timestamp is timezone-naive.
        """
        if self.value.tzinfo is None or self.value.utcoffset() is None:
            msg = "Timestamp requires a timezone-aware datetime."
            raise ValueError(msg)

    @classmethod
    def now(cls) -> Timestamp:
        """Create a timestamp representing the current UTC time.

        :returns: Current UTC timestamp.
        """
        return cls(datetime.now(UTC))

    def isoformat(self) -> str:
        """Return the timestamp in ISO 8601 format.

        :returns: ISO 8601 timestamp representation.
        """
        return self.value.isoformat()

    def __str__(self) -> str:
        """Return the ISO 8601 timestamp representation.

        :returns: ISO 8601 timestamp representation.
        """
        return self.isoformat()

    @classmethod
    def from_isoformat(cls, value: str) -> Timestamp:
        """Create a timestamp from an ISO 8601 representation.

        :param value: ISO 8601 timestamp representation.
        :returns: Parsed timestamp.
        :raises TimestampParsingError: If the value is not valid ISO timestamp
            text.
        """
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError as error:
            msg = f"Invalid ISO timestamp representation: {value!r}."
            raise TimestampParsingError(msg) from error

        if parsed.tzinfo is None or parsed.utcoffset() is None:
            parsed = parsed.replace(tzinfo=UTC)

        return cls(parsed)

    def __add__(self, duration: Duration) -> Timestamp:
        """Advance the timestamp by a duration.

        :param duration: Duration to add.
        :returns: Advanced timestamp.
        """
        if not isinstance(duration, Duration):
            return NotImplemented

        return Timestamp(self.value + duration.value)

    def __sub__(
        self,
        other: Timestamp | Duration,
    ) -> Timestamp | Duration:
        """Subtract a timestamp or duration.

        :param other: Timestamp or duration to subtract.
        :returns: A duration for timestamp differences or an earlier timestamp
            when subtracting a duration.
        """
        if isinstance(other, Duration):
            return Timestamp(self.value - other.value)

        if isinstance(other, Timestamp):
            difference = self.value - other.value

            if difference < timedelta():
                msg = "Timestamp difference cannot produce a negative Duration."
                raise ValueError(msg)

            return Duration(difference)

        return NotImplemented
