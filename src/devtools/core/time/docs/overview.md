# `devtools.core.time`

## Purpose

`devtools.core.time` provides foundational primitives for UTC timestamps,
non-negative durations, bounded timestamp parsing, and monotonic elapsed-time
measurement. It is not a scheduler or broad temporal framework.

## Public API

```python
from devtools.core.time import (
    Duration,
    Stopwatch,
    TimeError,
    Timestamp,
    TimestampParsingError,
    parse_timestamp,
)
```

## Package architecture

```text
Timestamp
    absolute UTC instant

Duration
    non-negative elapsed/span value

parse_timestamp()
    representation -> Timestamp

Stopwatch
    monotonic elapsed-time measurement
```

`Timestamp` and `Duration` are immutable values. `Stopwatch` is mutable
measurement state. See [timestamp and duration semantics](timestamps.md) and
[Stopwatch semantics](timing.md) for details.

## Dependencies and consumers

The package uses only Python standard-library `dataclasses`, `datetime`, and
`time` facilities. It does not depend on higher-level `devtools` domains.
Command execution consumes `Duration` for timeout/result values and `Stopwatch`
for elapsed-time measurement.

## Errors

```text
TimeError
└── TimestampParsingError
```

`TimestampParsingError` represents invalid external timestamp text. Model
invariants and normal arithmetic protocol failures retain established Python
errors such as `ValueError`, `TypeError`, and `ZeroDivisionError`.

## Boundaries

This package does not own scheduling, retries, cancellation, cron, sleep or
backoff policy, calendars, broad timezone management, or session/runtime
orchestration.

## Limitations

Timestamp parsing is deliberately bounded, `Duration` precision is limited by
`datetime.timedelta`, and `Stopwatch` is a process-local monotonic measurement
with no reset or restart. There is no deadline, scheduler, or active timer.

## Future evolution

Additional primitives require demonstrated demand from multiple concrete
consumers. A deadline or clock abstraction may be considered only under that
condition; neither is currently planned.
