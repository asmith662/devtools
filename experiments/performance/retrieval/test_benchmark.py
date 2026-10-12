# Copyright (c) 2026
# ruff: noqa: PLR2004, S101, D103, COM812
"""Focused engineering correctness; no scientific verifier, gold join or gates."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.resources.commands import Command

import pytest

from devtools.context.retrieval.fusion import _fused_resource_order
from devtools.context.retrieval.graph.walk import stationary_distribution
from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.performance.retrieval import computation as c
from experiments.performance.retrieval.benchmark import check_query, setup
from experiments.performance.retrieval.measurement import (
    CATEGORIES,
    Recorder,
    summary,
    viability,
)


@pytest.fixture(scope="module")
def workload() -> dict[str, Any]:
    return setup()


def test_summary_nearest_rank_and_population_deviation() -> None:
    result = summary(list(range(1, 51)))
    assert result["n"] == 50
    assert result["median_ns"] == 25.5
    assert result["p95_ns"] == 48
    assert result["mean_ns"] == 25.5
    assert result["minimum_ns"] == 1
    assert result["maximum_ns"] == 50
    assert result["standard_deviation_ns"] == pytest.approx(14.4308696897)
    with pytest.raises(ValueError, match="Nonempty"):
        summary([])


def test_recorder_sample_counts_and_outside_progress() -> None:
    calls = []
    progress: list[dict[str, Any]] = []
    recorder = Recorder(progress.append)

    def invoke() -> int:
        calls.append(1)
        return len(calls)

    assert recorder.measure("test", "ONLINE_QUERY", invoke) == 60
    assert len(calls) == 60
    assert len(progress) == 2
    row = recorder.measurements["test"]
    assert row["warmup"] == 10
    assert len(row["samples_ns"]) == 50
    assert row["summary"] == summary(row["samples_ns"])
    assert row["category"] in CATEGORIES


def test_engineering_ceiling_and_targets() -> None:
    assert viability(summary([50_000_000]), 50_000_000) == "VIABLE"
    assert viability(summary([50_000_001]), 50_000_000) == "NEEDS_OPTIMIZATION"
    assert viability(summary([1_000_000_001]), 250_000_000) == "TOO_SLOW"


def test_exact_production_implementation_bindings() -> None:
    assert c.kernel.__globals__["stationary_distribution"] is stationary_distribution
    assert c.rrf.__globals__["_fused_resource_order"] is _fused_resource_order
    assert (c.SETTINGS.k1, c.SETTINGS.b) == (1.2, 0.75)


def test_all_six_frozen_outputs_and_exact_frame(workload: dict[str, Any]) -> None:
    data = workload
    assert len(data["references"]) == 3954
    for obligation in data["design"]["requirement_matrix"]:
        q = obligation["query_id"]
        result = c.warm(
            data["frame"].snapshot,
            data["state"].content,
            data["view"],
            data["outgoing"],
            data["positions"],
            obligation["query"],
            data["design"]["seed_policy"]["exact_locators"][q],
        )
        checked = check_query(data, q, result)
        assert checked["A_order"] == checked["B_order"] == checked["C_order"] == "EXACT"
        assert checked["stationary_max_abs_error"] == 0.0


def test_result_summary_and_stable_json() -> None:
    from experiments.performance.retrieval.benchmark import PACKAGE  # noqa: PLC0415

    path = PACKAGE / "results.json"
    if not path.exists():
        pytest.skip("Run baseline to validate retained sample publication")
    raw = path.read_bytes()
    result = json.loads(raw)
    assert result["status"] == "COMPLETE"
    assert json_bytes(result) == raw
    for measurement in result["measurements"].values():
        assert measurement["summary"] == summary(measurement["samples_ns"])
        assert measurement["category"] in CATEGORIES
        if measurement["category"] == "ONLINE_QUERY":
            assert measurement["warmup"] >= 10
            assert len(measurement["samples_ns"]) >= 50
    assert result["configuration"]["ppr"]["maximum_iterations"] == 200
    assert result["scientific_state"]["gold_join"] == "NOT_PERFORMED"


def test_semantic_mismatch_stops_benchmark(workload: dict[str, Any]) -> None:
    data = workload
    obligation = data["design"]["requirement_matrix"][0]
    result = list(
        c.warm(
            data["frame"].snapshot,
            data["state"].content,
            data["view"],
            data["outgoing"],
            data["positions"],
            obligation["query"],
            data["design"]["seed_policy"]["exact_locators"]["Q1"],
        )
    )
    bad = result.copy()
    bad[0] = replace(result[0], matches=tuple(reversed(result[0].matches)))
    with pytest.raises(ValueError, match="canonical A ordering mismatch"):
        check_query(data, "Q1", bad)
    bad = result.copy()
    bad[1] = tuple(reversed(result[1]))
    with pytest.raises(ValueError, match="propagated B ordering mismatch"):
        check_query(data, "Q1", bad)
    bad = result.copy()
    bad[2] = tuple(reversed(result[2]))
    with pytest.raises(ValueError, match="production C ordering mismatch"):
        check_query(data, "Q1", bad)
    bad = result.copy()
    bad[3] = result[3].copy()
    bad[3][0] += 0.01
    with pytest.raises(ValueError, match="stationary vector mismatch"):
        check_query(data, "Q1", bad)


def test_profiler_timeout_is_stopped_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio  # noqa: PLC0415

    from devtools.resources.commands.errors import CommandTimeoutError  # noqa: PLC0415
    from experiments.performance.retrieval import profiler  # noqa: PLC0415

    calls = []

    class Executor:
        def __init__(self, **_kwargs: object) -> None:
            pass

        async def execute(self, command: Command) -> None:
            assert command.timeout is not None
            assert command.timeout.total_seconds == 120
            calls.append(command)
            message = "synthetic bounded timeout"
            raise CommandTimeoutError(message)

    monkeypatch.setattr(profiler, "CommandExecutor", Executor)
    monkeypatch.setattr(profiler, "PHASES", ("native_return_authentication",))
    result = asyncio.run(profiler.profile(tmp_path / "profile.json"))
    assert len(calls) == 1
    assert (
        result["phases"]["native_return_authentication"]["status"]
        == "TIME_LIMIT_STOPPED_NOT_REPEATED"
    )
    assert result["full_stage_d_verify"] == "NOT_RUN"
