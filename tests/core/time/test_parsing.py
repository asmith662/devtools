# Copyright (c) 2026
"""Tests for public timestamp parsing."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta, timezone

import pytest

from devtools.core.time import (
    TimeError,
    Timestamp,
    TimestampParsingError,
    parse_timestamp,
)


def test_parse_timestamp_accepts_existing_timestamp() -> None:
    """Existing timestamp values pass through unchanged."""
    timestamp = Timestamp(datetime(2026, 1, 2, tzinfo=UTC))

    assert parse_timestamp(timestamp) is timestamp


def test_parse_timestamp_accepts_and_normalizes_datetime_values() -> None:
    """Naive values are UTC and aware values normalize to equivalent UTC."""
    naive_datetime = datetime.fromisoformat("2026-01-02T03:04:00")

    assert parse_timestamp(naive_datetime).value == datetime(
        2026,
        1,
        2,
        3,
        4,
        tzinfo=UTC,
    )
    assert parse_timestamp(
        datetime(2026, 1, 2, 8, 4, tzinfo=timezone(timedelta(hours=5))),
    ).value == datetime(2026, 1, 2, 3, 4, tzinfo=UTC)


def test_parse_timestamp_accepts_date_values_at_utc_midnight() -> None:
    """Dates represent midnight at the start of their UTC calendar day."""
    assert parse_timestamp(date(2026, 1, 2)).value == datetime(2026, 1, 2, tzinfo=UTC)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-01-02T03:04:05+00:00", datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)),
        ("2026-01-02T08:04:05+05:00", datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)),
        ("2026-01-02 03:04:05", datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)),
        ("2026/01/02 03:04", datetime(2026, 1, 2, 3, 4, tzinfo=UTC)),
        ("01/02/2026 03:04:05", datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)),
        ("2026-01-02", datetime(2026, 1, 2, tzinfo=UTC)),
        ("2026/01/02", datetime(2026, 1, 2, tzinfo=UTC)),
        ("01/02/2026", datetime(2026, 1, 2, tzinfo=UTC)),
        ("  2026-01-02T03:04:05+00:00  ", datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)),
    ],
)
def test_parse_timestamp_accepts_supported_string_formats(
    value: str,
    expected: datetime,
) -> None:
    """Supported ISO, alternate datetime, and date strings parse to UTC."""
    assert parse_timestamp(value).value == expected


def test_parse_timestamp_none_returns_a_structurally_valid_current_time() -> None:
    """None delegates to the current UTC timestamp factory."""
    timestamp = parse_timestamp()

    assert timestamp.value.tzinfo is UTC


@pytest.mark.parametrize("value", ["", "  ", "not-a-date", "2026-02-30"])
def test_parse_timestamp_rejects_invalid_strings(value: str) -> None:
    """Empty, malformed, and impossible dates are rejected."""
    with pytest.raises(TimestampParsingError):
        parse_timestamp(value)


def test_timestamp_from_isoformat_accepts_only_iso_text() -> None:
    """The ISO constructor does not inherit the broad parser's fallbacks."""
    assert Timestamp.from_isoformat("2026-01-02T08:04:05+05:00") == Timestamp(
        datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
    )
    assert Timestamp.from_isoformat("2026-01-02T03:04:05") == Timestamp(
        datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
    )

    with pytest.raises(TimestampParsingError) as raised:
        Timestamp.from_isoformat("01/02/2026")

    assert isinstance(raised.value.__cause__, ValueError)


def test_time_errors_are_available_from_the_public_package() -> None:
    """The package-level error exports preserve their documented hierarchy."""
    assert issubclass(TimestampParsingError, TimeError)
