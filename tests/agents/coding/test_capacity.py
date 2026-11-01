# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, PT018, EM101, TRY003 -- literal independent controls
"""Independent byte/token admission and pressure over the existing coding host."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.agents.coding.capacity import ContextPressure, TokenCapacity
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.navigation import FIND
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionPolicy,
    request_bytes,
)
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.models.interaction import ModelSettings, PromptMessage
from tests.agents.coding.test_aggregate_reads import host
from tests.agents.coding.test_repository import LIMITS, Script, call, host_at

if TYPE_CHECKING:
    from devtools.models.interaction import ModelRequest


async def measure(_request: ModelRequest) -> int:
    return 1024


def configured(root: Path, **kwargs: Any) -> RepositoryCodingHost:  # noqa: ANN401 -- invalid configuration controls
    initial = host_at(root)
    return RepositoryCodingHost(
        initial.objective,
        corpus=initial.corpus,
        authorize=initial.authorize,
        apply_changes=initial.effect,
        archive=initial.archive,
        restore=initial.restore,
        settings=ModelSettings(maximum_output_tokens=128),
        **kwargs,
    )


@pytest.mark.parametrize(
    "values",
    [(0, 1, 1), (8, 8, 1), (True, 1, 1), (8, -1, 1), (8, 1, 1.5)],
)
def test_invalid_token_capacity(values: tuple[int, int, int]) -> None:
    with pytest.raises(ValueError, match="token capacity"):
        TokenCapacity(*values)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"measure_input": measure},
        {"token_capacity": TokenCapacity(2048, 1900, 128)},
        {"token_capacity": TokenCapacity(2048, 2000, 48), "measure_input": measure},
        {"warning_bytes": 0},
        {"warning_bytes": True},
        {"warning_bytes": 32769},
    ],
)
def test_incompatible_host_capacity(tmp_path: Path, kwargs: dict[str, Any]) -> None:
    with pytest.raises(ValueError, match="capacity"):
        configured(tmp_path, **kwargs)


@pytest.mark.parametrize("tokens", [0, 1024, 1900, 1901, -1, True, "invalid"])
def test_exact_independent_measurement(tmp_path: Path, tokens: int) -> None:
    calls = []

    async def counted(request: ModelRequest) -> int:
        calls.append(request)
        return tokens

    observed: list[ContextPressure] = []
    instance = configured(
        tmp_path,
        token_capacity=TokenCapacity(2048, 1900, 128),
        measure_input=counted,
        warning_bytes=1,
        observe_context=observed.append,
    )
    worker = Script([()])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=instance))
    assert result.disposition == (
        "stopped" if type(tokens) is int and 0 <= tokens <= 1900 else "failed"
    )
    assert len(calls) == 1
    fact = observed[0]
    assert fact == instance.context_pressure[0]
    expected = tokens if type(tokens) is int and tokens >= 0 else None
    assert fact.measured_input_tokens == expected and fact.warning
    assert fact.ceiling_bytes == 32768 and fact.request_bytes == request_bytes(calls[0])
    assert fact.token_capacity is not None
    assert fact.policy == "strict" and fact.token_capacity.reserved_output_tokens == 128
    assert fact.action == ("ready" if result.error is None else "refused")


@pytest.mark.parametrize("failure", ["tokenizer", "source", "history", "observer"])
def test_measurement_and_observer_failures_never_enter_or_retry(
    tmp_path: Path,
    failure: str,
) -> None:
    async def counted(_request: ModelRequest) -> int:
        if failure == "tokenizer":
            raise OSError("No tokenizer response")
        if failure == "source":
            (tmp_path / "module.py").write_text("changed", encoding="utf-8")
        if failure == "history":
            instance.messages.append(PromptMessage("user", "unexpected"))
        return 1024

    def observed(_fact: object) -> None:
        if failure == "observer":
            raise OSError("Capture unavailable")

    instance = configured(
        tmp_path,
        token_capacity=TokenCapacity(2048, 1900, 128),
        measure_input=counted,
        observe_context=observed,
    )
    worker = Script([()])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=instance))
    assert (
        result.disposition
        == ("reconciliation_required" if failure == "source" else "failed")
        and worker.entries == 0
    )
    assert len(instance.context_pressure) == 1


def test_automatic_reduction_retains_original_history(tmp_path: Path) -> None:
    instance = configured(
        tmp_path,
        navigation=True,
        projection=ProjectionPolicy(16000, 10000, frozenset({FIND.name})),
        warning_bytes=15000,
    )
    for i in range(12):
        instance.messages.extend(
            (
                PromptMessage("assistant", "", (call(FIND.name, {}, str(i)),)),
                PromptMessage(
                    "tool",
                    json.dumps({"metadata": "x" * 1700}),
                    tool_call_id=str(i),
                ),
            ),
        )
    original = tuple(instance.messages[2:])
    request = asyncio.run(instance.prepare(CodingProgress(LIMITS)))
    fact = instance.context_pressure[-1]
    assert fact.original_bytes > 16000 and fact.request_bytes <= 10000
    assert (
        fact.action == "reduced" and fact.warning and fact.measured_input_tokens is None
    )
    assert tuple(instance.messages[2:]) == original
    assert len(request.prompt.messages) < len(instance.messages)
    assert request.prompt.messages[-2:] == original[-2:]


@pytest.mark.parametrize("projection", [None, ProjectionPolicy(20000, 16000)])
def test_impossible_minimum_is_visible(
    tmp_path: Path,
    projection: ProjectionPolicy | None,
) -> None:
    instance = configured(tmp_path, projection=projection)
    instance.messages.append(PromptMessage("user", "mandatory" * 5000))
    with pytest.raises((ValueError, ProjectionCapacityError)):
        asyncio.run(instance.prepare(CodingProgress(LIMITS)))
    fact = instance.context_pressure[-1]
    assert fact.request_bytes > fact.ceiling_bytes and fact.action == "refused"


def test_higher_byte_profile_delivers_preserved_batch_without_duplicate_reads(
    tmp_path: Path,
) -> None:
    frozen = json.loads((Path(__file__).parent / "data/b0049.json").read_bytes())
    instance = host(
        tmp_path,
        frozen["contents"],
        source=frozen["source"],
        budget=131072,
        projection=ProjectionPolicy(114688, 98304),
    )
    instance.objective = replace(instance.objective, text=frozen["objective"])
    instance.messages[0] = PromptMessage("user", frozen["objective"])
    instance.settings = ModelSettings(**frozen["settings"])
    batches = [
        tuple(
            call(c["name"], json.loads(c["arguments_json"]), c["provider_call_id"])
            for c in batch
        )
        for batch in frozen["calls"]
    ]
    worker = Script([*batches, ()])
    result = asyncio.run(
        run_coding_agent(
            worker,
            limits=replace(LIMITS, model_calls=3, tool_actions=4),
            host=instance,
        ),
    )
    assert result.disposition == "stopped", result.error
    assert len(instance.source_results) == 4
    assert sum(len(o.text.encode()) for o in instance.disclosures) == 51544
    assert 65536 < request_bytes(instance.requests[-1]) < 98304
    assert all(
        json.loads(m.content).get("error") is None
        for m in instance.requests[-1].prompt.messages
        if m.role == "tool"
    )


def test_model_cannot_self_authorize_semantic_compaction(tmp_path: Path) -> None:
    instance = configured(tmp_path, projection=ProjectionPolicy(24000, 20000))
    worker = Script([(call("compact_context", {}, "unapproved"),)])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=instance))
    assert result.disposition == "failed"
    assert not result.progress.effects
    assert instance.compaction is None


def test_warning_includes_current_annotation_overhead_at_exact_boundary(
    tmp_path: Path,
) -> None:
    instance = configured(
        tmp_path,
        projection=ProjectionPolicy(24000, 20000, report_source_state=True),
    )
    first = asyncio.run(instance.prepare(CodingProgress(LIMITS)))
    instance.warning_bytes = request_bytes(first)
    asyncio.run(instance.prepare(CodingProgress(LIMITS)))
    fact = instance.context_pressure[-1]
    assert fact.original_bytes < fact.warning_bytes
    assert fact.request_bytes == fact.warning_bytes
    assert fact.warning
