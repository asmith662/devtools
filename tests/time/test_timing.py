# Copyright (c) 2026
"""Tests for public stopwatch behavior."""

from __future__ import annotations

import pytest

from devtools.time import Duration, Stopwatch


def test_stopwatch_measures_running_and_stopped_elapsed_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A stopwatch uses the monotonic clock until it is stopped."""
    readings = iter([1_000, 3_500, 5_000])
    monkeypatch.setattr(
        "devtools.time.models.stopwatch.perf_counter_ns",
        lambda: next(readings),
    )

    stopwatch = Stopwatch()

    assert stopwatch.is_running is True
    assert stopwatch.is_stopped is False
    assert stopwatch.elapsed == Duration.nanoseconds(2_500)
    assert stopwatch.stop() == Duration.nanoseconds(4_000)
    assert stopwatch.is_running is False
    assert stopwatch.is_stopped is True
    assert stopwatch.elapsed == Duration.nanoseconds(4_000)
    assert stopwatch.stop() == Duration.nanoseconds(4_000)


def test_stopwatch_context_stops_and_preserves_exceptions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Context exit stops the stopwatch without suppressing exceptions."""
    readings = iter([10, 110])
    monkeypatch.setattr(
        "devtools.time.models.stopwatch.perf_counter_ns",
        lambda: next(readings),
    )

    message = "expected"
    stopwatch = Stopwatch()
    with pytest.raises(RuntimeError, match=message), stopwatch:
        raise RuntimeError(message)

    assert stopwatch.is_stopped is True
    assert stopwatch.elapsed == Duration.nanoseconds(100)


def test_stopwatch_context_returns_the_same_instance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The context manager supplies its active stopwatch to callers."""
    readings = iter([10, 110])
    monkeypatch.setattr(
        "devtools.time.models.stopwatch.perf_counter_ns",
        lambda: next(readings),
    )

    stopwatch = Stopwatch()
    with stopwatch as entered:
        assert entered is stopwatch

    assert stopwatch.elapsed == Duration.nanoseconds(100)
