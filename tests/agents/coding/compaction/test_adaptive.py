# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- literal independent adaptive boundaries
"""Actual neutral host selection, auxiliary entry and exact fallback controls."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.agents.coding.compaction import AdaptiveCompaction, SummaryAttempt
from devtools.agents.coding.projection import ProjectionCapacityError, ProjectionPolicy
from devtools.models.interaction import InteractionSource, ModelResponse
from tests.agents.coding.compaction.test_semantic import Summarizer, prepare, setup
from tests.agents.coding.test_repository import LIMITS

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_thresholds(value: int) -> None:
    with pytest.raises(ValueError, match="positive"):
        AdaptiveCompaction(value, 1024, lambda _: frozenset())
    with pytest.raises(ValueError, match="positive"):
        AdaptiveCompaction(1024, value, lambda _: frozenset())


def test_automatic_real_host_cache_and_history(tmp_path: Path) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        adaptive=AdaptiveCompaction(8000, 4096, lambda _: frozenset({2})),
    )
    original = tuple(host.messages)
    result = prepare(host)
    assert "hypothesis failed" in str(result)
    assert len(model.requests) == 1
    assert host.compaction is not None
    assert host.compaction.decisions == ["semantic-requested"]
    assert prepare(host) == result
    assert host.compaction.decisions[-1] == "cached-summary"
    assert len(model.requests) == 1
    assert tuple(host.messages) == original


@pytest.mark.parametrize(
    ("pressure", "reserve", "valuable", "decision"),
    [
        (10000, 1024, frozenset({2}), "no-pressure"),
        (8000, 10000, frozenset({2}), "insufficient-headroom"),
        (8000, 1024, frozenset(), "deterministic-sufficient"),
        (8000, 1024, frozenset({3}), "deterministic-sufficient"),
    ],
)
def test_avoids_unnecessary_inference(
    tmp_path: Path,
    pressure: int,
    reserve: int,
    valuable: frozenset[int],
    decision: str,
) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        adaptive=AdaptiveCompaction(pressure, reserve, lambda _: valuable),
    )
    prepare(host)
    assert not model.requests
    assert host.compaction is not None
    assert host.compaction.decisions == [decision]


@pytest.mark.parametrize("value", [{2}, frozenset({99}), frozenset({True})])
def test_invalid_host_value_preserves_fallback(
    tmp_path: Path,
    value: frozenset[int],
) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        adaptive=AdaptiveCompaction(8000, 1024, lambda _: value),
    )
    result = prepare(host)
    assert "Recent exact progress" in str(result)
    assert not model.requests
    assert host.compaction is not None
    assert host.compaction.decisions == ["policy-failed"]
    prepare(host)
    assert host.compaction.decisions[-1] == "prior-strategy-failure"


@pytest.mark.parametrize("fault", ["transport", "malformed", "timeout", "cancel"])
def test_failed_strategy_not_automatically_repeated(tmp_path: Path, fault: str) -> None:
    model = Summarizer(fault)
    host = setup(
        tmp_path,
        model,
        adaptive=AdaptiveCompaction(8000, 1024, lambda _: frozenset({2})),
    )
    if fault == "cancel":
        with pytest.raises(asyncio.CancelledError):
            prepare(host)
    else:
        prepare(host)
    assert len(model.requests) == 1
    prepare(host)
    assert len(model.requests) == 1
    assert host.compaction is not None
    assert host.compaction.decisions[-1] == "prior-strategy-failure"


def test_budget_and_protected_overflow(tmp_path: Path) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        adaptive=AdaptiveCompaction(8000, 1024, lambda _: frozenset({2})),
        maximum_calls=1,
    )
    assert host.compaction is not None
    host.compaction.attempts.append(SummaryAttempt(entered=True))
    prepare(host)
    assert host.compaction.decisions[-1] == "auxiliary-budget-exhausted"
    host.compaction.attempts.clear()
    host.objective = replace(host.objective, prompt_bytes=1000)
    host.projection = ProjectionPolicy(900, 800, frozenset({"list_repository"}))
    with pytest.raises(ProjectionCapacityError):
        prepare(host)
    assert host.compaction.decisions[-1] == "protected-context-unaffordable"
    assert not model.requests


def test_changed_prefix_reassessed_without_mutating_original(tmp_path: Path) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        adaptive=AdaptiveCompaction(8000, 1024, lambda _: frozenset({2})),
    )
    prepare(host)
    host.messages[1] = replace(host.messages[1], content="New qualified investigation")
    retained = tuple(host.messages)
    prepare(host)
    assert len(model.requests) == 2
    assert host.compaction is not None
    assert host.compaction.decisions == ["semantic-requested", "semantic-requested"]
    assert tuple(host.messages) == retained


def test_disabled_permission_and_unaffordable_input(tmp_path: Path) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        input_bytes=100,
        adaptive=AdaptiveCompaction(8000, 1024, lambda _: frozenset({2})),
    )
    result = prepare(host)
    assert "Recent exact progress" in str(result)
    assert not model.requests
    assert host.compaction is not None
    assert host.compaction.attempts[0].status == "failed"
    prepare(host)
    assert host.compaction.decisions[-1] == "prior-strategy-failure"


def test_independent_coding_process_consumes_automatic_notes(tmp_path: Path) -> None:
    class Acting:
        source = InteractionSource("independent-adaptive-consumer")
        calls = 0

        async def send(self, request: object) -> ModelResponse:
            assert "hypothesis failed" in str(request)
            assert "Recent exact progress" in str(request)
            self.calls += 1
            return ModelResponse("No candidate proposed", self.source)

    host = setup(
        tmp_path,
        adaptive=AdaptiveCompaction(8000, 1024, lambda _: frozenset({2})),
    )
    acting = Acting()
    result = asyncio.run(run_coding_agent(acting, host=host, limits=LIMITS))
    assert result.disposition == "stopped"
    assert not result.accepted
    assert result.progress.proposals == 0
    assert result.progress.effects == []
    assert acting.calls == 1
    assert host.compaction is not None
    assert host.compaction.attempts[0].adopted
