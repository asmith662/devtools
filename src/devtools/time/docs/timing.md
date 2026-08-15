# Stopwatch timing

`Stopwatch` measures elapsed process-local time. It is not a wall-clock
timestamp source; see [timestamp semantics](timestamps.md) for timestamps and
durations.

## Clock source

`Stopwatch` uses `time.perf_counter_ns()`, a monotonic high-resolution clock.
Measurements are suitable for elapsed process-local timing, not persistence or
cross-process clock comparison.

## Lifecycle

```text
construction
    ↓
running
    ↓
stop()
    ↓
stopped
```

A stopwatch starts immediately when constructed. `is_running` and `is_stopped`
reflect its state. While running, `elapsed` reads the current clock. The first
`stop()` records the endpoint; repeated calls are idempotent, and `elapsed`
then remains fixed. Elapsed values and `stop()` results are `Duration` values.

## Context manager

```python
with Stopwatch() as stopwatch:
    do_work()
```

`__enter__()` returns the same stopwatch. Context exit stops it and does not
suppress exceptions.

## Limitations

There is no reset, restart, pause/resume, async context-manager behavior,
scheduling, or active timer callback. Stopwatch measurement is process-local
and monotonic only.
