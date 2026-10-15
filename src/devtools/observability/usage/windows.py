# Copyright (c) 2026
"""Half-open historical query windows; changing a window changes no observation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from zoneinfo import ZoneInfo

from devtools.core.time import Duration, Timestamp


@dataclass(frozen=True, slots=True)
class UsageWindow:
    """An exact [start,end) UTC interval and the calendar timezone used."""

    start: Timestamp
    end: Timestamp
    timezone: str = "UTC"

    def __post_init__(self) -> None:
        """Reject an inverted interval and unknown timezone."""
        ZoneInfo(self.timezone)
        if self.start.value > self.end.value:
            message = "Usage window start exceeds end"
            raise ValueError(message)

    def contains(self, timestamp: Timestamp | None) -> bool:
        """Unknown times are unallocated, never assigned the import timestamp."""
        return (
            timestamp is not None
            and self.start.value <= timestamp.value < self.end.value
        )

    @classmethod
    def rolling(
        cls,
        at: Timestamp,
        days: int = 7,
        timezone: str = "UTC",
    ) -> UsageWindow:
        """Use elapsed 24-hour days, independent of local daylight saving."""
        if days <= 0:
            message = "Rolling usage days must be positive"
            raise ValueError(message)
        return cls(Timestamp(at.value - Duration.hours(days * 24).value), at, timezone)

    @classmethod
    def calendar_week(
        cls,
        at: Timestamp,
        timezone: str,
        *,
        previous: bool = False,
        week_start: int = 0,
    ) -> UsageWindow:
        """Use configurable weekday boundaries in an IANA timezone, including DST."""
        if week_start not in range(7):
            message = "Week start must be 0..6 (Monday..Sunday)"
            raise ValueError(message)
        local = at.value.astimezone(ZoneInfo(timezone))
        start = local.replace(hour=0, minute=0, second=0, microsecond=0)
        start -= timedelta(days=(local.weekday() - week_start) % 7)
        if previous:
            start -= timedelta(days=7)
        return cls(Timestamp(start), Timestamp(start + timedelta(days=7)), timezone)
