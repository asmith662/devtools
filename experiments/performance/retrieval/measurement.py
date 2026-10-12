# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, T201, E501
"""Small auditable timing boundary; publication is always outside the sample."""

from __future__ import annotations

import gc
import math
import statistics
import time
import tracemalloc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

from devtools.core.time import Timestamp

CATEGORIES = frozenset(
    {
        "OFFLINE_SNAPSHOT_BUILD",
        "INCREMENTAL_UPDATE",
        "ONLINE_QUERY",
        "CONTEXT_MATERIALIZATION",
        "EXPERIMENT_ONLY",
    },
)
CEILING_NS = 1_000_000_000


def summary(samples: list[int]) -> dict[str, int | float]:
    """Use nearest-rank p95: sorted samples at ceil(0.95*n)-1; population SD."""
    if not samples or any(value < 0 for value in samples):
        raise ValueError("Nonempty nonnegative timing samples required")
    ordered = sorted(samples)
    return {
        "n": len(samples),
        "minimum_ns": ordered[0],
        "median_ns": statistics.median(samples),
        "mean_ns": statistics.mean(samples),
        "p95_ns": ordered[math.ceil(0.95 * len(samples)) - 1],
        "maximum_ns": ordered[-1],
        "standard_deviation_ns": statistics.pstdev(samples),
    }


def viability(stats: dict[str, Any], target_ns: int) -> str:
    """Apply engineering targets, independent of relevance or scientific gates."""
    if stats["median_ns"] > CEILING_NS or stats["p95_ns"] > CEILING_NS:
        return "TOO_SLOW"
    return "VIABLE" if stats["median_ns"] <= target_ns else "NEEDS_OPTIMIZATION"


def allocation(invoke: Callable[[], Any]) -> dict[str, int]:
    """Measure Python allocations separately; exclude existing retained state."""
    gc.collect()
    tracemalloc.start()
    try:
        value = invoke()
        retained, peak = tracemalloc.get_traced_memory()
        del value
        return {"retained_bytes": retained, "peak_bytes": peak}
    finally:
        tracemalloc.stop()


class Recorder:
    """Collect raw sequential samples with GC enabled and boundary progress."""

    def __init__(self, progress: Callable[[dict[str, Any]], None]) -> None:
        """Bind an out-of-timing progress sink."""
        self.started = time.perf_counter_ns()
        self.progress = progress
        self.measurements: dict[str, Any] = {}

    def emit(self, surface: str, started: int, **details: Any) -> None:
        """Persist and print concise timestamps outside every timed invocation."""
        row = {
            "timestamp": Timestamp.now().isoformat(),
            "surface": surface,
            "elapsed_ns": time.perf_counter_ns() - started,
            "total_elapsed_ns": time.perf_counter_ns() - self.started,
            **details,
        }
        self.progress(row)
        print(
            f"{row['timestamp']} {surface} {details} elapsed={row['elapsed_ns'] / 1e9:.3f}s total={row['total_elapsed_ns'] / 1e9:.3f}s",
            flush=True,
        )

    def measure(  # noqa: PLR0913 -- explicit timing configuration
        self,
        name: str,
        category: str,
        invoke: Callable[[], Any],
        *,
        warmup: int = 10,
        repetitions: int = 50,
        note: str = "",
    ) -> Any:
        """Time only invoke(); summaries, progress and output checks occur later."""
        if category not in CATEGORIES or warmup < 0 or repetitions < 1:
            raise ValueError("Invalid benchmark configuration")
        started = time.perf_counter_ns()
        self.emit(name, started, phase="START", warmup=warmup, repetitions=repetitions)
        value = None
        for _ in range(warmup):
            value = invoke()
        samples = []
        for number in range(repetitions):
            # Previous result release is outside timing, including large offline objects.
            value = None
            before = time.perf_counter_ns()
            value = invoke()
            samples.append(time.perf_counter_ns() - before)
            if category == "OFFLINE_SNAPSHOT_BUILD" and samples[-1] > CEILING_NS:
                self.emit(name, started, repetition=number + 1, total=repetitions)
        stats = summary(samples)
        self.measurements[name] = {
            "category": category,
            "warmup": warmup,
            "samples_ns": samples,
            "summary": stats,
            "note": note,
        }
        if category == "ONLINE_QUERY":
            self.measurements[name]["viability"] = viability(
                stats,
                50_000_000 if "bm25" in name else 250_000_000,
            )
        self.emit(
            name,
            started,
            phase="COMPLETE",
            median_ms=stats["median_ns"] / 1e6,
            p95_ms=stats["p95_ns"] / 1e6,
        )
        return value
