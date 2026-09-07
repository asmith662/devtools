# Copyright (c) 2026
# ruff: noqa: INP001
"""Tests for the experimental vLLM benchmark composition script."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import pytest

from devtools.model_benchmarks.models import (
    BenchmarkCase,
    ModelBenchmarkResult,
    VLLMBenchmarkServingSnapshot,
)
from devtools.model_serving.huggingface import HuggingFaceModelRef
from devtools.model_serving.vllm import VLLMServingConfig
from devtools.paths import ResolvedPath
from devtools.time import Duration, Timestamp

if TYPE_CHECKING:
    from types import ModuleType


_DRIVER_PATH = Path("scripts/model_benchmarks/vllm.py")
_DEFAULT_READINESS_TIMEOUT = Duration.minutes(10)
_CPU_OFFLOAD_GB = 2.0
_RESULT_CPU_OFFLOAD_GB = 2.5
_PREFETCH_BACKEND: Literal["prefetch"] = "prefetch"
_PREFETCH_GROUP_SIZE = 24
_PREFETCH_NUM_IN_GROUP = 5
_PREFETCH_STEP = 1
_RESULT_PREFETCH_GROUP_SIZE = 23
_RESULT_PREFETCH_NUM_IN_GROUP = 4
_RESULT_PREFETCH_STEP = 2


@pytest.fixture
def driver() -> ModuleType:
    """Load the tracked script without making scripts a library package."""
    specification = importlib.util.spec_from_file_location(
        "test_vllm_benchmark_driver",
        _DRIVER_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _config(tmp_path: Path) -> VLLMServingConfig:
    return VLLMServingConfig(
        model=HuggingFaceModelRef("org/model", "a" * 40),
        image="vllm/vllm-openai:v0.26.0",
        cache_root=ResolvedPath(tmp_path / "cache"),
        host_port=8123,
        served_model_name="local-model",
        max_model_len=2048,
        gpu_memory_utilization=0.8,
        max_num_seqs=1,
    )


def _case() -> BenchmarkCase:
    return BenchmarkCase("ready", "Reply with exactly: local model ready", 16)


def _result() -> ModelBenchmarkResult:
    return ModelBenchmarkResult(
        started_at=Timestamp.from_isoformat("2026-09-06T12:00:00+00:00"),
        case=_case(),
        serving=VLLMBenchmarkServingSnapshot(
            model_repository="org/model",
            model_revision="a" * 40,
            served_model_name="local-model",
            image="vllm/vllm-openai:v0.26.0",
            max_model_len=2048,
            gpu_memory_utilization=0.8,
            max_num_seqs=1,
            trust_remote_code=False,
        ),
        response_text="local model ready",
        ttft=Duration.milliseconds(2),
        total_duration=Duration.milliseconds(10),
        prompt_tokens=8,
        completion_tokens=4,
        completion_tokens_per_second=400.0,
        finish_reason="stop",
        expectation_met=True,
    )


class _Server:
    """Record stop calls without creating infrastructure."""

    def __init__(self, calls: list[str]) -> None:
        self._calls = calls

    async def stop(self) -> None:
        self._calls.append("stop")


def _patch_start(
    monkeypatch: pytest.MonkeyPatch,
    driver: ModuleType,
    server: _Server,
    calls: list[str],
    expected: tuple[
        Duration,
        float,
        Literal["prefetch"] | None,
        int,
        int,
        int,
        bool,
    ] = (
        _DEFAULT_READINESS_TIMEOUT,
        0.0,
        None,
        0,
        0,
        0,
        False,
    ),
) -> None:
    async def start(
        *,
        config: VLLMServingConfig,
        executor: object,
        readiness_timeout: Duration,
    ) -> _Server:
        (
            expected_readiness_timeout,
            expected_cpu_offload_gb,
            expected_offload_backend,
            expected_offload_group_size,
            expected_offload_num_in_group,
            expected_offload_prefetch_step,
            expected_wsl2_enable_pin_memory,
        ) = expected
        assert config == replace(
            _config(config.cache_root.value.parent),
            cpu_offload_gb=expected_cpu_offload_gb,
            offload_backend=expected_offload_backend,
            offload_group_size=expected_offload_group_size,
            offload_num_in_group=expected_offload_num_in_group,
            offload_prefetch_step=expected_offload_prefetch_step,
            wsl2_enable_pin_memory=expected_wsl2_enable_pin_memory,
        )
        assert executor is not None
        assert readiness_timeout == expected_readiness_timeout
        calls.append("start")
        return server

    monkeypatch.setattr(driver.VLLMServer, "start", start)


def test_driver_composes_start_benchmark_save_and_stop(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    driver: ModuleType,
) -> None:
    """The driver composes validated public APIs in their required order."""
    calls: list[str] = []
    server = _Server(calls)
    config = replace(
        _config(tmp_path),
        cpu_offload_gb=0.0,
        offload_backend=_PREFETCH_BACKEND,
        offload_group_size=_PREFETCH_GROUP_SIZE,
        offload_num_in_group=_PREFETCH_NUM_IN_GROUP,
        offload_prefetch_step=_PREFETCH_STEP,
    )
    case = _case()
    result = replace(
        _result(),
        serving=replace(
            _result().serving,
            cpu_offload_gb=_RESULT_CPU_OFFLOAD_GB,
            offload_backend=_PREFETCH_BACKEND,
            offload_group_size=_RESULT_PREFETCH_GROUP_SIZE,
            offload_num_in_group=_RESULT_PREFETCH_NUM_IN_GROUP,
            offload_prefetch_step=_RESULT_PREFETCH_STEP,
            wsl2_enable_pin_memory=True,
        ),
    )
    result_path = ResolvedPath(tmp_path / "results" / "run.json")
    _patch_start(
        monkeypatch,
        driver,
        server,
        calls,
        expected=(
            _DEFAULT_READINESS_TIMEOUT,
            0.0,
            _PREFETCH_BACKEND,
            _PREFETCH_GROUP_SIZE,
            _PREFETCH_NUM_IN_GROUP,
            _PREFETCH_STEP,
            False,
        ),
    )

    async def benchmark(
        *,
        server: _Server,
        case: BenchmarkCase,
    ) -> ModelBenchmarkResult:
        assert server is not None
        assert case == _case()
        calls.append("benchmark")
        return result

    def save(value: ModelBenchmarkResult, root: ResolvedPath) -> ResolvedPath:
        assert value == result
        assert root == ResolvedPath(tmp_path / "results")
        calls.append("save")
        return result_path

    monkeypatch.setattr(driver, "run_vllm_benchmark", benchmark)
    monkeypatch.setattr(driver, "save_benchmark_result", save)

    returned = asyncio.run(
        driver.run_experiment(
            config=config,
            case=case,
            output_root=ResolvedPath(tmp_path / "results"),
            readiness_timeout=Duration.minutes(10),
        ),
    )

    assert returned == (result, result_path)
    assert calls == ["start", "benchmark", "save", "stop"]
    output = capsys.readouterr().out
    assert str(config.cache_root) in output
    assert str(result_path) in output
    assert f"CPU weight offload: {_RESULT_CPU_OFFLOAD_GB} GiB" in output
    assert "Offload backend: prefetch" in output
    assert "Prefetch group size: 23" in output
    assert "Prefetch layers per group: 4" in output
    assert "Prefetch step: 2" in output
    assert "WSL2 pinned memory: enabled" in output
    assert "Prefetch group size: 24" not in output


@pytest.mark.parametrize("failure_site", ["benchmark", "save"])
def test_driver_preserves_primary_failure_and_stops_owned_server(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    driver: ModuleType,
    failure_site: str,
) -> None:
    """Benchmark and save failures still clean up only the created server."""
    calls: list[str] = []
    primary = RuntimeError(failure_site)
    _patch_start(monkeypatch, driver, _Server(calls), calls)

    async def benchmark(**_kwargs: object) -> ModelBenchmarkResult:
        calls.append("benchmark")
        if failure_site == "benchmark":
            raise primary
        return _result()

    def save(*_args: object) -> ResolvedPath:
        calls.append("save")
        raise primary

    monkeypatch.setattr(driver, "run_vllm_benchmark", benchmark)
    monkeypatch.setattr(driver, "save_benchmark_result", save)
    with pytest.raises(RuntimeError) as raised:
        asyncio.run(
            driver.run_experiment(
                config=_config(tmp_path),
                case=_case(),
                output_root=ResolvedPath(tmp_path / "results"),
                readiness_timeout=Duration.minutes(10),
            ),
        )

    assert raised.value is primary
    assert calls == (
        ["start", "benchmark", "stop"]
        if failure_site == "benchmark"
        else ["start", "benchmark", "save", "stop"]
    )


def test_driver_preserves_cancellation_and_stops_owned_server(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    driver: ModuleType,
) -> None:
    """Cancellation keeps its identity while owned-server cleanup is attempted."""
    calls: list[str] = []
    primary = asyncio.CancelledError("interrupted")
    _patch_start(monkeypatch, driver, _Server(calls), calls)

    async def benchmark(**_kwargs: object) -> ModelBenchmarkResult:
        calls.append("benchmark")
        raise primary

    monkeypatch.setattr(driver, "run_vllm_benchmark", benchmark)
    with pytest.raises(asyncio.CancelledError) as raised:
        asyncio.run(
            driver.run_experiment(
                config=_config(tmp_path),
                case=_case(),
                output_root=ResolvedPath(tmp_path / "results"),
                readiness_timeout=Duration.minutes(10),
            ),
        )

    assert raised.value is primary
    assert calls == ["start", "benchmark", "stop"]


def test_driver_does_not_clean_up_when_startup_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    driver: ModuleType,
) -> None:
    """A failed start never creates a handle that the driver could stop."""
    primary = RuntimeError("start")

    async def start(**_kwargs: object) -> _Server:
        raise primary

    monkeypatch.setattr(driver.VLLMServer, "start", start)
    with pytest.raises(RuntimeError) as raised:
        asyncio.run(
            driver.run_experiment(
                config=_config(tmp_path),
                case=_case(),
                output_root=ResolvedPath(tmp_path / "results"),
                readiness_timeout=Duration.minutes(10),
            ),
        )
    assert raised.value is primary


def test_driver_builds_public_configuration_from_explicit_arguments(
    tmp_path: Path,
    driver: ModuleType,
) -> None:
    """Argument parsing delegates domain validation to the public values."""
    arguments = driver.parse_arguments(
        [
            "--model",
            "org/model",
            "--revision",
            "a" * 40,
            "--image",
            "vllm/vllm-openai:v0.26.0",
            "--cache-root",
            "cache",
            "--output-root",
            "results",
            "--served-model-name",
            "local-model",
            "--max-model-len",
            "2048",
            "--gpu-memory-utilization",
            "0.8",
            "--max-num-seqs",
            "1",
        ],
    )

    config, case, output_root, readiness_timeout = driver.build_configuration(
        arguments,
        base_directory=tmp_path,
    )

    assert config.model.repository == "org/model"
    assert config.model.revision == "a" * 40
    assert config.cache_root == ResolvedPath(tmp_path / "cache")
    assert output_root == ResolvedPath(tmp_path / "results")
    assert case.expected_response == "local model ready"
    assert readiness_timeout == driver.DEFAULT_READINESS_TIMEOUT
    assert config.cpu_offload_gb == 0.0
    assert config.offload_backend is None
    assert config.offload_group_size == 0
    assert config.offload_num_in_group == 0
    assert config.offload_prefetch_step == 0
    assert config.wsl2_enable_pin_memory is False


def test_driver_maps_explicit_prefetch_configuration(
    tmp_path: Path,
    driver: ModuleType,
) -> None:
    """The tracked driver maps its prefetch arguments into public config only."""
    arguments = driver.parse_arguments(
        [
            "--model",
            "org/model",
            "--revision",
            "a" * 40,
            "--image",
            "vllm/vllm-openai:v0.26.0",
            "--cache-root",
            "cache",
            "--output-root",
            "results",
            "--served-model-name",
            "local-model",
            "--max-model-len",
            "2048",
            "--gpu-memory-utilization",
            "0.8",
            "--offload-backend",
            "prefetch",
            "--offload-group-size",
            "24",
            "--offload-num-in-group",
            "5",
            "--offload-prefetch-step",
            "1",
            "--wsl2-enable-pin-memory",
            "--max-num-seqs",
            "1",
        ],
    )

    config, _, _, _ = driver.build_configuration(arguments, base_directory=tmp_path)

    assert config.cpu_offload_gb == 0.0
    assert config.offload_backend == "prefetch"
    assert config.offload_group_size == _PREFETCH_GROUP_SIZE
    assert config.offload_num_in_group == _PREFETCH_NUM_IN_GROUP
    assert config.offload_prefetch_step == _PREFETCH_STEP
    assert config.wsl2_enable_pin_memory is True


def test_driver_maps_custom_readiness_timeout_to_server_start(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    driver: ModuleType,
) -> None:
    """A caller-selected readiness allowance reaches the lifecycle start call."""
    arguments = driver.parse_arguments(
        [
            "--model",
            "org/model",
            "--revision",
            "a" * 40,
            "--image",
            "vllm/vllm-openai:v0.26.0",
            "--cache-root",
            "cache",
            "--output-root",
            "results",
            "--served-model-name",
            "local-model",
            "--max-model-len",
            "2048",
            "--gpu-memory-utilization",
            "0.8",
            "--cpu-offload-gb",
            "2.0",
            "--max-num-seqs",
            "1",
            "--port",
            "8123",
            "--readiness-timeout-seconds",
            "1800",
        ],
    )
    config, case, output_root, readiness_timeout = driver.build_configuration(
        arguments,
        base_directory=tmp_path,
    )
    assert config.cpu_offload_gb == _CPU_OFFLOAD_GB
    calls: list[str] = []
    _patch_start(
        monkeypatch,
        driver,
        _Server(calls),
        calls,
        expected=(Duration.minutes(30), _CPU_OFFLOAD_GB, None, 0, 0, 0, False),
    )

    async def benchmark(**_kwargs: object) -> ModelBenchmarkResult:
        calls.append("benchmark")
        return _result()

    def save(*_args: object) -> ResolvedPath:
        calls.append("save")
        return ResolvedPath(tmp_path / "results" / "run.json")

    monkeypatch.setattr(driver, "run_vllm_benchmark", benchmark)
    monkeypatch.setattr(driver, "save_benchmark_result", save)

    asyncio.run(
        driver.run_experiment(
            config=config,
            case=case,
            output_root=output_root,
            readiness_timeout=readiness_timeout,
        ),
    )

    assert calls == ["start", "benchmark", "save", "stop"]
