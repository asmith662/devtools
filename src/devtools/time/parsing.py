# Copyright (c) 2026
"""Timestamp parsing operations."""

from __future__ import annotations

from datetime import UTC, date, datetime

from devtools.time.errors import TimestampParsingError
from devtools.time.models import Timestamp

_DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M",
)

_DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%m/%d/%Y",
)


def parse_timestamp(
    value: str | date | datetime | Timestamp | None = None,
) -> Timestamp:
    """Parse a value into a normalized UTC timestamp.

    ``None`` produces the current UTC timestamp. Naive datetime values and
    parsed strings without timezone information are interpreted as UTC.

    Date-only values are interpreted as midnight UTC.

    :param value: Timestamp representation, or ``None`` for the current time.
    :returns: Normalized UTC timestamp.
    :raises TimestampParsingError: If a string representation cannot be parsed.
    """
    if value is None:
        return Timestamp.now()

    if isinstance(value, Timestamp):
        return value

    if isinstance(value, datetime):
        return Timestamp(_normalize_datetime(value))

    if isinstance(value, date):
        return Timestamp(
            datetime(
                value.year,
                value.month,
                value.day,
                tzinfo=UTC,
            ),
        )

    normalized = value.strip()

    if not normalized:
        msg = "Timestamp representation cannot be empty."
        raise TimestampParsingError(msg)

    parsed = _parse_datetime_string(normalized)

    if parsed is None:
        msg = f"Unsupported timestamp representation: {value!r}."
        raise TimestampParsingError(msg)

    return Timestamp(_normalize_datetime(parsed))


def _normalize_datetime(value: datetime) -> datetime:
    """Normalize a datetime to UTC.

    Naive datetime values are interpreted as UTC.

    :param value: Datetime to normalize.
    :returns: Timezone-aware UTC datetime.
    """
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)


def _parse_datetime_string(value: str) -> datetime | None:
    """Parse a supported string representation.

    :param value: Timestamp representation.
    :returns: Parsed datetime, or ``None`` when no format matches.
    """
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass

    for format_string in _DATETIME_FORMATS:
        try:
            return datetime.strptime(value, format_string).replace(tzinfo=UTC)
        except ValueError:
            continue

    for format_string in _DATE_FORMATS:
        try:
            parsed_date = (
                datetime.strptime(value, format_string)
                .replace(
                    tzinfo=UTC,
                )
                .date()
            )
        except ValueError:
            continue

        return datetime(
            parsed_date.year,
            parsed_date.month,
            parsed_date.day,
            tzinfo=UTC,
        )

    return None
