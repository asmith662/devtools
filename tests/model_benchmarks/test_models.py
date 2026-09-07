# Copyright (c) 2026
"""Tests for immutable model benchmark values."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import TYPE_CHECKING

import pytest

from devtools.model_benchmarks.models import (
    BenchmarkCase,
    ModelBenchmarkResult,
    VLLMBenchmarkServingSnapshot,
)
from devtools.model_serving.huggingface import HuggingFaceModelRef
from devtools.model_serving.vllm import VLLMServer, VLLMServingConfig
from devtools.paths import ResolvedPath
from devtools.time import Duration, Timestamp

if TYPE_CHECKING:
    from pathlib import Path


_CPU_OFFLOAD_GB = 2.0
_PREFETCH_GROUP_SIZE = 24
_PREFETCH_NUM_IN_GROUP = 5
_PREFETCH_STEP = 1


def _case(**changes: object) -> BenchmarkCase:
    values: dict[str, object] = {
        "name": "ready",
        "prompt": "Reply with exactly: local model ready",
        "max_tokens": 16,
    }
    values.update(changes)
    return BenchmarkCase(**values)  # type: ignore[arg-type]


def _serving() -> VLLMBenchmarkServingSnapshot:
    return VLLMBenchmarkServingSnapshot(
        model_repository="Qwen/Qwen3-8B",
        model_revision="a" * 40,
        served_model_name="qwen-local",
        image="vllm/vllm-openai:v0.26.0",
        max_model_len=2048,
        gpu_memory_utilization=0.8,
        max_num_seqs=1,
        trust_remote_code=False,
    )


def _result(**changes: object) -> ModelBenchmarkResult:
    values: dict[str, object] = {
        "started_at": Timestamp.now(),
        "case": _case(),
        "serving": _serving(),
        "response_text": "local model ready",
        "ttft": Duration.milliseconds(2),
        "total_duration": Duration.milliseconds(10),
        "prompt_tokens": 8,
        "completion_tokens": 4,
        "completion_tokens_per_second": 500.0,
        "finish_reason": "stop",
        "expectation_met": True,
    }
    values.update(changes)
    return ModelBenchmarkResult(**values)  # type: ignore[arg-type]


def test_benchmark_case_is_immutable_hashable_and_preserves_expectation() -> None:
    """A workload is a stable reusable benchmark input value."""
    case = _case(expected_response="local model ready")

    assert case == _case(expected_response="local model ready")
    assert hash(case) == hash(_case(expected_response="local model ready"))
    with pytest.raises(FrozenInstanceError):
        case.name = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("changes", "match"),
    [
        ({"name": " "}, "name"),
        ({"prompt": " "}, "prompt"),
        ({"max_tokens": 0}, "tokens"),
        ({"temperature": -0.1}, "temperature"),
        ({"temperature": float("inf")}, "temperature"),
    ],
)
def test_benchmark_case_rejects_invalid_workload_values(
    changes: dict[str, object],
    match: str,
) -> None:
    """Only structurally usable one-run workloads are accepted."""
    with pytest.raises(ValueError, match=match):
        _case(**changes)


@pytest.mark.parametrize(
    ("changes", "match"),
    [
        ({"ttft": Duration.seconds(2), "total_duration": Duration.seconds(1)}, "TTFT"),
        ({"prompt_tokens": -1}, "Prompt"),
        ({"completion_tokens": -1}, "Completion"),
        ({"completion_tokens_per_second": float("nan")}, "throughput"),
        ({"completion_tokens_per_second": -1.0}, "throughput"),
    ],
)
def test_result_rejects_invalid_measurements(
    changes: dict[str, object],
    match: str,
) -> None:
    """Result values reject internally contradictory measurements."""
    with pytest.raises(ValueError, match=match):
        _result(**changes)


def test_result_is_immutable_hashable_and_supports_unknown_measurements() -> None:
    """Missing provider usage and absent content timing remain explicit optionals."""
    result = _result(
        ttft=None,
        prompt_tokens=None,
        completion_tokens=None,
        completion_tokens_per_second=None,
        expectation_met=None,
    )

    assert hash(result) == hash(result)
    with pytest.raises(FrozenInstanceError):
        result.response_text = "other"  # type: ignore[misc]


def test_serving_snapshot_reads_public_server_config(tmp_path: Path) -> None:
    """A benchmark captures serving facts without Docker handle internals."""
    config = VLLMServingConfig(
        model=HuggingFaceModelRef("Qwen/Qwen3-8B", "a" * 40),
        image="vllm/vllm-openai:v0.26.0",
        cache_root=ResolvedPath(tmp_path / "cache"),
        host_port=8123,
        served_model_name="qwen-local",
        max_model_len=2048,
        gpu_memory_utilization=0.8,
        max_num_seqs=1,
        cpu_offload_gb=0.0,
        offload_backend="prefetch",
        offload_group_size=_PREFETCH_GROUP_SIZE,
        offload_num_in_group=_PREFETCH_NUM_IN_GROUP,
        offload_prefetch_step=_PREFETCH_STEP,
        wsl2_enable_pin_memory=True,
    )
    server = VLLMServer(
        config=config,
        container_id="a" * 64,
        container_name="devtools-vllm-test",
        executor=object(),  # type: ignore[arg-type]
        started_at=Timestamp.now(),
    )

    snapshot = VLLMBenchmarkServingSnapshot.from_server(server)
    assert snapshot.cpu_offload_gb == 0.0
    assert snapshot.offload_backend == "prefetch"
    assert snapshot.offload_group_size == _PREFETCH_GROUP_SIZE
    assert snapshot.offload_num_in_group == _PREFETCH_NUM_IN_GROUP
    assert snapshot.offload_prefetch_step == _PREFETCH_STEP
    assert snapshot.wsl2_enable_pin_memory is True
    assert snapshot.model_repository == config.model.repository
