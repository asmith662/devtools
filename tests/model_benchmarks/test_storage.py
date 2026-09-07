# Copyright (c) 2026
"""Tests for JSON benchmark artifact storage."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.model_benchmarks import storage
from devtools.model_benchmarks.models import (
    BenchmarkCase,
    ModelBenchmarkResult,
    VLLMBenchmarkServingSnapshot,
)
from devtools.model_benchmarks.storage import (
    load_benchmark_result,
    save_benchmark_result,
)
from devtools.paths import ResolvedPath
from devtools.time import Duration, Timestamp

if TYPE_CHECKING:
    from pathlib import Path


_CPU_OFFLOAD_GB = 2.0
_SCHEMA_VERSION = 2


def _result(**changes: object) -> ModelBenchmarkResult:
    values: dict[str, object] = {
        "started_at": Timestamp.from_isoformat("2026-09-05T12:00:00+00:00"),
        "case": BenchmarkCase(
            "ready test",
            "Reply with exactly: local model ready",
            16,
        ),
        "serving": VLLMBenchmarkServingSnapshot(
            model_repository="Qwen/Qwen3-8B",
            model_revision="a" * 40,
            served_model_name="qwen-local",
            image="vllm/vllm-openai:v0.26.0",
            max_model_len=2048,
            gpu_memory_utilization=0.8,
            max_num_seqs=1,
            trust_remote_code=False,
        ),
        "response_text": "local model ready",
        "ttft": Duration.milliseconds(2),
        "total_duration": Duration.milliseconds(10),
        "prompt_tokens": 8,
        "completion_tokens": 4,
        "completion_tokens_per_second": 500.0,
        "finish_reason": "stop",
        "expectation_met": None,
    }
    values.update(changes)
    return ModelBenchmarkResult(**values)  # type: ignore[arg-type]


def test_save_and_load_round_trip_explicit_schema(tmp_path: Path) -> None:
    """Saved artifacts remain inspectable and reconstruct the immutable result."""
    output_root = ResolvedPath(tmp_path / "results")
    result = _result(
        serving=replace(_result().serving, cpu_offload_gb=_CPU_OFFLOAD_GB),
    )

    path = save_benchmark_result(result, output_root)
    raw = json.loads(path.value.read_text(encoding="utf-8"))

    assert path.value.parent == output_root.value
    assert path.suffix == ".json"
    assert raw["schema_version"] == _SCHEMA_VERSION
    assert raw["serving"]["provider"] == "vllm"
    assert raw["serving"]["model_revision"] == "a" * 40
    assert raw["serving"]["cpu_offload_gb"] == _CPU_OFFLOAD_GB
    assert raw["response_text"] == "local model ready"
    assert load_benchmark_result(path) == result


def test_save_explicitly_serializes_zero_cpu_offload_in_schema_two(
    tmp_path: Path,
) -> None:
    """Schema two distinguishes an explicit disabled setting from omission."""
    path = save_benchmark_result(_result(), ResolvedPath(tmp_path / "results"))
    raw = json.loads(path.value.read_text(encoding="utf-8"))

    assert raw["schema_version"] == _SCHEMA_VERSION
    assert raw["serving"]["cpu_offload_gb"] == 0.0


def test_loads_version_one_artifact_with_historical_zero_cpu_offload(
    tmp_path: Path,
) -> None:
    """Pre-offload artifacts reconstruct their historically fixed zero value."""
    raw = storage._to_json(_result())  # noqa: SLF001
    raw["schema_version"] = 1
    serving = raw["serving"]
    assert isinstance(serving, dict)
    del serving["cpu_offload_gb"]
    path = ResolvedPath(tmp_path / "version-one.json")
    path.value.write_text(json.dumps(raw), encoding="utf-8")

    assert load_benchmark_result(path) == _result()


def test_rejects_schema_two_artifact_missing_cpu_offload(tmp_path: Path) -> None:
    """Schema two requires explicit complete serving provenance."""
    raw = storage._to_json(_result())  # noqa: SLF001
    serving = raw["serving"]
    assert isinstance(serving, dict)
    del serving["cpu_offload_gb"]
    path = ResolvedPath(tmp_path / "missing-offload.json")
    path.value.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid"):
        load_benchmark_result(path)


def test_repeated_saves_are_independent(tmp_path: Path) -> None:
    """Independent runs never overwrite prior result artifacts."""
    root = ResolvedPath(tmp_path / "results")

    first = save_benchmark_result(_result(), root)
    second = save_benchmark_result(_result(), root)

    assert first != second
    assert first.value.is_file()
    assert second.value.is_file()


def test_benchmark_name_cannot_escape_the_explicit_output_root(tmp_path: Path) -> None:
    """A benchmark name influences only a safe final filename component."""
    root = ResolvedPath(tmp_path / "results")
    result = _result(case=BenchmarkCase("../../outside\\result", "prompt", 1))

    path = save_benchmark_result(result, root)

    assert path.value.parent == root.value
    assert path.value.is_file()
    assert "/" not in path.value.name
    assert "\\" not in path.value.name
    assert not (tmp_path / "outside").exists()


@pytest.mark.parametrize(
    "content",
    [
        "not json",
        json.dumps({"schema_version": 3}),
        json.dumps({"schema_version": 1}),
        json.dumps({"schema_version": 1, "case": {}, "serving": {"provider": "other"}}),
    ],
)
def test_load_rejects_malformed_or_unsupported_artifacts(
    tmp_path: Path,
    content: str,
) -> None:
    """Persisted experimental records fail clearly rather than guessing schema."""
    path = ResolvedPath(tmp_path / "invalid.json")
    path.value.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match=r"Invalid|Unsupported"):
        load_benchmark_result(path)


def test_save_removes_temporary_file_when_atomic_replace_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A storage failure does not leave a completed-looking final artifact."""
    root = ResolvedPath(tmp_path / "results")

    def deny_replace(_source: Path, _destination: Path) -> None:
        msg = "replace denied"
        raise OSError(msg)

    monkeypatch.setattr("devtools.model_benchmarks.storage.os.replace", deny_replace)
    with pytest.raises(OSError, match="denied"):
        save_benchmark_result(_result(), root)
    assert list(root.value.iterdir()) == []


def test_save_propagates_temporary_file_creation_failure(tmp_path: Path) -> None:
    """No cleanup is attempted when no temporary artifact was created."""
    root = ResolvedPath(tmp_path / "results")

    def deny_temporary_file(**_kwargs: object) -> None:
        msg = "temporary denied"
        raise OSError(msg)

    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(storage, "NamedTemporaryFile", deny_temporary_file)
        with pytest.raises(OSError, match="temporary denied"):
            save_benchmark_result(_result(), root)


@pytest.mark.parametrize(
    ("helper", "value"),
    [
        (storage._object, []),  # noqa: SLF001
        (storage._string, 1),  # noqa: SLF001
        (storage._integer, True),  # noqa: SLF001
        (storage._number, float("nan")),  # noqa: SLF001
        (storage._boolean, "false"),  # noqa: SLF001
    ],
)
def test_storage_schema_helpers_reject_wrong_runtime_types(
    helper: object,
    value: object,
) -> None:
    """Malformed JSON scalar shapes fail rather than being coerced."""
    with pytest.raises(ValueError, match="field"):
        helper(value)  # type: ignore[operator]
