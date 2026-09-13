# Timestamps, durations, and parsing

This document defines the value and parsing contract for `devtools.core.time`. See
the [package overview](overview.md) and [Stopwatch documentation](timing.md).

## Timestamp invariants

`Timestamp(value: datetime)` is a frozen, slotted value object. Stored values
are timezone-aware and normalized to `datetime.UTC`; equality and hashing use
that value. Direct construction rejects naive datetimes with `ValueError`.

## Construction

```python
Timestamp(aware_datetime)
Timestamp.now()
Timestamp.from_isoformat(text)
parse_timestamp(value)
```

Direct construction rehydrates an already-aware value. `now()` creates a
current UTC value. `from_isoformat()` accepts ISO timestamp text only.
`parse_timestamp()` is the broader representation parser.

## `Timestamp.from_isoformat()`

`Timestamp.from_isoformat(text)` uses standard-library ISO parsing. Aware ISO
values normalize to UTC; timezone-less ISO datetimes are interpreted as UTC.
Invalid ISO text raises `TimestampParsingError`. Alternate slash and locale-like
formats are not accepted by this constructor.

## `parse_timestamp()`

`parse_timestamp()` accepts `None`, `Timestamp`, `datetime`, `date`, and `str`.

- `None` creates a fresh current UTC timestamp.
- An existing `Timestamp` is returned unchanged.
- Aware datetimes normalize to UTC; naive datetimes mean UTC.
- Dates mean midnight UTC.
- Strings have outer whitespace removed before parsing.

It first uses `datetime.fromisoformat()`, then supports these fallback datetime
formats:

```text
%Y-%m-%d %H:%M:%S
%Y-%m-%d %H:%M
%Y/%m/%d %H:%M:%S
%Y/%m/%d %H:%M
%m/%d/%Y %H:%M:%S
%m/%d/%Y %H:%M
```

It also supports these date formats:

```text
%Y-%m-%d
%Y/%m/%d
%m/%d/%Y
```

Malformed, empty, and impossible string values raise `TimestampParsingError`.

## Naive versus aware values

Direct model construction is strict, while representation parsing interprets
timezone-less values as UTC. This keeps stored timestamp values unambiguous
while allowing explicit parsing of common external representations.

## Timestamp arithmetic

```text
Timestamp + Duration -> Timestamp
Timestamp - Duration -> Timestamp
Timestamp - Timestamp -> Duration
```

`Duration` cannot be negative, so subtracting a later timestamp from an earlier
one raises `ValueError` instead of returning a signed value.

## Duration

`Duration(value: timedelta)` is a frozen, slotted non-negative value. Factories
are `nanoseconds()`, `milliseconds()`, `seconds()`, `minutes()`, and `hours()`.
`total_seconds` and `total_milliseconds` expose numeric totals.

Durations support addition, non-negative subtraction, multiplication by an
`int` or `float`, reversed multiplication, and division by an `int` or `float`.
Unsupported operands raise normal `TypeError`; division by zero raises normal
`ZeroDivisionError`.

## Precision and errors

`Duration` stores `datetime.timedelta`, not true nanoseconds. Consequently,
`Duration.nanoseconds()` follows standard-library microsecond-bounded
conversion and rounding for sub-microsecond inputs.

`TimestampParsingError` is used for invalid external timestamp text. Direct
Timestamp/Duration invariant failures use `ValueError`; arithmetic preserves
normal Python protocol errors.
