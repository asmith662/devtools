# Copyright (c) 2026
"""Time value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class Duration:
    """Represent an immutable non-negative amount of elapsed time.

    :ivar value: Elapsed time represented as a timedelta.
    """

    value: timedelta

    def __post_init__(self) -> None:
        """Validate duration invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate the duration value.

        :raises ValueError: If the duration is negative.
        """
        if self.value < timedelta():
            msg = "Duration cannot be negative."
            raise ValueError(msg)

    @classmethod
    def nanoseconds(cls, value: int) -> Duration:
        """Create a duration from nanoseconds.

        :param value: Number of nanoseconds.
        :returns: Duration representing the supplied nanoseconds.
        """
        return cls(timedelta(microseconds=value / 1000))

    @classmethod
    def seconds(cls, value: float) -> Duration:
        """Create a duration from seconds.

        :param value: Number of seconds.
        :returns: Duration representing the supplied seconds.
        """
        return cls(timedelta(seconds=value))

    @classmethod
    def milliseconds(cls, value: float) -> Duration:
        """Create a duration from milliseconds.

        :param value: Number of milliseconds.
        :returns: Duration representing the supplied milliseconds.
        """
        return cls(timedelta(milliseconds=value))

    @classmethod
    def minutes(cls, value: float) -> Duration:
        """Create a duration from minutes.

        :param value: Number of minutes.
        :returns: Duration representing the supplied minutes.
        """
        return cls(timedelta(minutes=value))

    @classmethod
    def hours(cls, value: float) -> Duration:
        """Create a duration from hours.

        :param value: Number of hours.
        :returns: Duration representing the supplied hours.
        """
        return cls(timedelta(hours=value))

    @property
    def total_seconds(self) -> float:
        """Return the duration in seconds.

        :returns: Total number of seconds.
        """
        return self.value.total_seconds()

    @property
    def total_milliseconds(self) -> float:
        """Return the duration in milliseconds.

        :returns: Total number of milliseconds.
        """
        return self.total_seconds * 1000.0

    def __str__(self) -> str:
        """Return the standard timedelta representation.

        :returns: Human-readable duration representation.
        """
        return str(self.value)

    def __add__(self, other: Duration) -> Duration:
        """Add two durations.

        :param other: Duration to add.
        :returns: Combined duration.
        """
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(self.value + other.value)

    def __sub__(self, other: Duration) -> Duration:
        """Subtract one duration from another.

        :param other: Duration to subtract.
        :returns: Remaining duration.
        :raises ValueError: If the result would be negative.
        """
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(self.value - other.value)

    def __mul__(self, factor: float) -> Duration:
        """Scale the duration.

        :param factor: Multiplication factor.
        :returns: Scaled duration.
        """
        if not isinstance(factor, int | float):
            return NotImplemented

        return Duration(self.value * factor)

    def __rmul__(self, factor: float) -> Duration:
        """Scale the duration using reversed multiplication.

        :param factor: Multiplication factor.
        :returns: Scaled duration.
        """
        return self * factor

    def __truediv__(self, divisor: float) -> Duration:
        """Divide the duration by a numeric divisor.

        :param divisor: Divisor.
        :returns: Divided duration.
        """
        if not isinstance(divisor, int | float):
            return NotImplemented

        return Duration(self.value / divisor)
