# Copyright (c) 2026
"""Tests for public timestamp and duration value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone

import pytest

from devtools.core.time import Duration, Timestamp


def test_timestamp_normalizes_aware_values_to_utc_and_is_immutable() -> None:
    """Aware datetimes represent the same instant after UTC normalization."""
    timestamp = Timestamp(
        datetime(2026, 1, 2, 8, 30, tzinfo=timezone(timedelta(hours=2))),
    )
    attribute = "value"

    assert timestamp.value == datetime(2026, 1, 2, 6, 30, tzinfo=UTC)
    assert timestamp.isoformat() == "2026-01-02T06:30:00+00:00"
    assert str(timestamp) == timestamp.isoformat()
    assert timestamp == Timestamp(datetime(2026, 1, 2, 6, 30, tzinfo=UTC))
    assert hash(timestamp) == hash(Timestamp(timestamp.value))

    with pytest.raises(FrozenInstanceError):
        setattr(timestamp, attribute, datetime(2026, 1, 1, tzinfo=UTC))


def test_timestamp_rejects_naive_datetimes() -> None:
    """Direct construction requires a timezone-aware datetime."""
    with pytest.raises(ValueError, match="timezone-aware"):
        Timestamp(datetime.fromisoformat("2026-01-02T03:04:00"))


def test_timestamp_now_returns_a_utc_timestamp() -> None:
    """The current-time factory returns an aware UTC value."""
    timestamp = Timestamp.now()

    assert timestamp.value.tzinfo is UTC


def test_timestamp_arithmetic_preserves_time_invariants() -> None:
    """Timestamps support duration arithmetic and ordered differences."""
    earlier = Timestamp(datetime(2026, 1, 2, tzinfo=UTC))
    duration = Duration.seconds(90)
    later = Timestamp(datetime(2026, 1, 2, 0, 1, 30, tzinfo=UTC))

    assert earlier + duration == later
    assert later - duration == earlier
    assert later - earlier == duration

    with pytest.raises(ValueError, match="negative Duration"):
        earlier - later

    with pytest.raises(TypeError):
        earlier + 1  # type: ignore[operator]

    with pytest.raises(TypeError):
        earlier - 1  # type: ignore[operator]


def test_duration_factories_create_expected_values() -> None:
    """Each public duration factory delegates to its documented unit."""
    assert Duration.nanoseconds(2_000).value == timedelta(microseconds=2)
    assert Duration.seconds(2.5).value == timedelta(seconds=2.5)
    assert Duration.milliseconds(2.5).value == timedelta(milliseconds=2.5)
    assert Duration.minutes(2.5).value == timedelta(minutes=2.5)
    assert Duration.hours(2.5).value == timedelta(hours=2.5)


def test_duration_accessors_string_and_value_semantics() -> None:
    """Duration representations expose the underlying elapsed amount."""
    expected_seconds = 1.25
    expected_milliseconds = 1250.0
    duration = Duration(timedelta(seconds=expected_seconds))

    assert duration.total_seconds == expected_seconds
    assert duration.total_milliseconds == expected_milliseconds
    assert str(duration) == "0:00:01.250000"
    assert duration == Duration.seconds(expected_seconds)
    assert hash(duration) == hash(Duration.seconds(expected_seconds))


def test_duration_rejects_negative_values_and_negative_results() -> None:
    """Durations remain non-negative after construction and arithmetic."""
    with pytest.raises(ValueError, match="cannot be negative"):
        Duration(timedelta(seconds=-1))

    with pytest.raises(ValueError, match="cannot be negative"):
        Duration.seconds(1) - Duration.seconds(2)

    with pytest.raises(ValueError, match="cannot be negative"):
        Duration.seconds(1) * -1

    with pytest.raises(ValueError, match="cannot be negative"):
        Duration.seconds(1) / -1


def test_duration_arithmetic_and_invalid_operands() -> None:
    """Supported numeric arithmetic returns durations and rejects other types."""
    duration = Duration.seconds(2)

    assert duration + Duration.seconds(3) == Duration.seconds(5)
    assert duration * 2.5 == Duration.seconds(5)
    assert 2 * duration == Duration.seconds(4)
    assert duration / 2 == Duration.seconds(1)

    with pytest.raises(TypeError):
        duration + 1  # type: ignore[operator]

    with pytest.raises(TypeError):
        duration - 1  # type: ignore[operator]

    with pytest.raises(TypeError):
        duration * "two"  # type: ignore[operator]

    with pytest.raises(TypeError):
        duration / "two"  # type: ignore[operator]

    with pytest.raises(ZeroDivisionError):
        duration / 0


def test_duration_nanoseconds_uses_timedelta_bounded_precision() -> None:
    """Sub-microsecond values follow timedelta's available precision."""
    assert Duration.nanoseconds(1).value == timedelta()
