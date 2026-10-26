# Copyright (c) 2026
"""Tests for public timestamp and duration value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest

from devtools.core.time import Duration, Timestamp

if TYPE_CHECKING:
    from collections.abc import Callable


_DURATION_FACTORIES = (
    Duration.nanoseconds,
    Duration.seconds,
    Duration.milliseconds,
    Duration.minutes,
    Duration.hours,
)


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


@pytest.mark.parametrize(
    ("factory", "value"),
    [
        (Duration.nanoseconds, -1),
        (Duration.nanoseconds, -499),
        (Duration.seconds, -1e-12),
        (Duration.milliseconds, -1e-9),
        (Duration.minutes, -1e-12),
        (Duration.hours, -1e-14),
    ],
)
def test_duration_factories_reject_negative_inputs_before_rounding(
    factory: Callable[..., Duration],
    value: float,
) -> None:
    """Negative source values must not become admitted zero durations."""
    with pytest.raises(ValueError, match="Duration cannot be negative"):
        factory(value)


@pytest.mark.parametrize("factory", _DURATION_FACTORIES)
def test_duration_factories_reject_ordinary_negative_inputs(
    factory: Callable[..., Duration],
) -> None:
    """Every factory retains ordinary finite negative-input refusal."""
    with pytest.raises(ValueError, match="Duration cannot be negative"):
        factory(-1_000)


@pytest.mark.parametrize("factory", _DURATION_FACTORIES)
@pytest.mark.parametrize("value", [0, -0.0])
def test_duration_factories_preserve_zero_inputs(
    factory: Callable[..., Duration],
    value: float,
) -> None:
    """Zero and negative floating zero retain their exact represented value."""
    assert factory(value).value == timedelta()


@pytest.mark.parametrize(
    ("factory", "value", "expected"),
    [
        (Duration.nanoseconds, 1, timedelta()),
        (Duration.nanoseconds, 499, timedelta()),
        (Duration.nanoseconds, 500, timedelta()),
        (Duration.nanoseconds, 501, timedelta(microseconds=1)),
        (Duration.nanoseconds, 1_500, timedelta(microseconds=2)),
        (Duration.nanoseconds, 2_500, timedelta(microseconds=2)),
        (Duration.seconds, 1e-12, timedelta()),
        (Duration.milliseconds, 1e-9, timedelta()),
        (Duration.minutes, 1e-12, timedelta()),
        (Duration.hours, 1e-14, timedelta()),
    ],
)
def test_duration_factories_preserve_literal_positive_rounding(
    factory: Callable[..., Duration],
    value: float,
    expected: timedelta,
) -> None:
    """Positive precision remains microsecond-bounded with half-even ties."""
    assert factory(value).value == expected


@pytest.mark.parametrize("factory", _DURATION_FACTORIES)
@pytest.mark.parametrize(
    ("value", "error"),
    [
        (float("nan"), ValueError),
        (float("inf"), OverflowError),
        (-float("inf"), OverflowError),
    ],
)
def test_duration_factories_preserve_nonfinite_conversion_errors(
    factory: Callable[..., Duration],
    value: float,
    error: type[Exception],
) -> None:
    """Nonfinite runtime inputs retain the existing conversion exception classes."""
    with pytest.raises(error):
        factory(value)


@pytest.mark.parametrize("factory", _DURATION_FACTORIES)
@pytest.mark.parametrize("value", ["1", None, object(), Decimal("-0.1")])
def test_duration_factories_preserve_unsupported_input_errors(
    factory: Callable[..., Duration],
    value: object,
) -> None:
    """Sign admission must not replace unsupported-value errors with ValueError."""
    with pytest.raises(TypeError):
        factory(value)


@pytest.mark.parametrize("factory", _DURATION_FACTORIES)
def test_duration_factories_preserve_range_overflow(
    factory: Callable[..., Duration],
) -> None:
    """An out-of-range nonnegative integer retains native overflow refusal."""
    with pytest.raises(OverflowError):
        factory(10**1000)


def test_duration_arithmetic_preserves_represented_result_policy() -> None:
    """Factory admission does not change arithmetic's rounded-result semantics."""
    tiny = Duration(timedelta(microseconds=1))
    zero = Duration(timedelta())

    assert (tiny * -0.1).value == timedelta()
    assert (-0.1 * tiny).value == timedelta()
    assert (tiny / -10).value == timedelta()
    assert (zero * -1).value == timedelta()
    assert (tiny * 2).value == timedelta(microseconds=2)
