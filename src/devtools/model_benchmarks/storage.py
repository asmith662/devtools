# Copyright (c) 2026
"""JSON artifact storage for completed experimental benchmark runs."""
# ruff: noqa: TRY004

from __future__ import annotations

import json
import math
import os
import re
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import cast

from devtools.model_benchmarks.models import (
    BenchmarkCase,
    ModelBenchmarkResult,
    VLLMBenchmarkServingSnapshot,
)
from devtools.paths import ResolvedPath
from devtools.time import Duration, Timestamp

_SCHEMA_VERSION = 4
_SAFE_FILENAME = re.compile(r"[^a-zA-Z0-9._-]+")


def save_benchmark_result(
    result: ModelBenchmarkResult,
    output_root: ResolvedPath,
) -> ResolvedPath:
    """Atomically save one self-describing benchmark JSON artifact."""
    output_root.value.mkdir(parents=True, exist_ok=True)
    filename = _result_filename(result)
    destination = output_root.value / filename
    serialized = json.dumps(_to_json(result), indent=2, sort_keys=True) + "\n"
    temporary: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_root.value,
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary = Path(file.name)
            file.write(serialized)
        os.replace(temporary, destination)  # noqa: PTH105
    except BaseException:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise
    return ResolvedPath(destination)


def load_benchmark_result(path: ResolvedPath) -> ModelBenchmarkResult:
    """Load a supported benchmark artifact into its immutable result value."""
    try:
        raw = json.loads(path.value.read_text(encoding="utf-8"))
        return _from_json(cast("object", raw))
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        msg = f"Invalid model benchmark artifact: {path}."
        raise ValueError(msg) from error


def _to_json(result: ModelBenchmarkResult) -> dict[str, object]:
    """Encode explicit current experimental-schema JSON values."""
    return {
        "schema_version": _SCHEMA_VERSION,
        "started_at": result.started_at.isoformat(),
        "case": {
            "name": result.case.name,
            "prompt": result.case.prompt,
            "max_tokens": result.case.max_tokens,
            "temperature": result.case.temperature,
            "expected_response": result.case.expected_response,
        },
        "serving": {
            "provider": "vllm",
            "model_repository": result.serving.model_repository,
            "model_revision": result.serving.model_revision,
            "served_model_name": result.serving.served_model_name,
            "image": result.serving.image,
            "max_model_len": result.serving.max_model_len,
            "gpu_memory_utilization": result.serving.gpu_memory_utilization,
            "max_num_seqs": result.serving.max_num_seqs,
            "trust_remote_code": result.serving.trust_remote_code,
            "cpu_offload_gb": result.serving.cpu_offload_gb,
            "offload_backend": result.serving.offload_backend,
            "offload_group_size": result.serving.offload_group_size,
            "offload_num_in_group": result.serving.offload_num_in_group,
            "offload_prefetch_step": result.serving.offload_prefetch_step,
            "wsl2_enable_pin_memory": result.serving.wsl2_enable_pin_memory,
        },
        "response_text": result.response_text,
        "ttft_seconds": _duration_seconds(result.ttft),
        "total_duration_seconds": result.total_duration.total_seconds,
        "prompt_tokens": result.prompt_tokens,
        "completion_tokens": result.completion_tokens,
        "completion_tokens_per_second": result.completion_tokens_per_second,
        "finish_reason": result.finish_reason,
        "expectation_met": result.expectation_met,
    }


def _from_json(raw: object) -> ModelBenchmarkResult:
    """Decode the supported experimental artifact schemas."""
    root = _object(raw)
    schema_version = _integer(root["schema_version"])
    if schema_version not in {1, 2, 3, _SCHEMA_VERSION}:
        msg = "Unsupported model benchmark artifact schema version."
        raise ValueError(msg)
    case = _object(root["case"])
    serving = _object(root["serving"])
    if serving["provider"] != "vllm":
        msg = "Unsupported model benchmark serving provider."
        raise ValueError(msg)
    return ModelBenchmarkResult(
        started_at=Timestamp.from_isoformat(_string(root["started_at"])),
        case=BenchmarkCase(
            name=_string(case["name"]),
            prompt=_string(case["prompt"]),
            max_tokens=_integer(case["max_tokens"]),
            temperature=_number(case["temperature"]),
            expected_response=_optional_string(case["expected_response"]),
        ),
        serving=VLLMBenchmarkServingSnapshot(
            model_repository=_string(serving["model_repository"]),
            model_revision=_string(serving["model_revision"]),
            served_model_name=_string(serving["served_model_name"]),
            image=_string(serving["image"]),
            max_model_len=_integer(serving["max_model_len"]),
            gpu_memory_utilization=_number(serving["gpu_memory_utilization"]),
            max_num_seqs=_integer(serving["max_num_seqs"]),
            trust_remote_code=_boolean(serving["trust_remote_code"]),
            cpu_offload_gb=(
                0.0
                if schema_version == 1
                else _number(serving["cpu_offload_gb"])
            ),
            offload_backend=(
                None
                if schema_version in {1, 2}
                else _optional_string(serving["offload_backend"])
            ),
            offload_group_size=(
                0
                if schema_version in {1, 2}
                else _integer(serving["offload_group_size"])
            ),
            offload_num_in_group=(
                0
                if schema_version in {1, 2}
                else _integer(serving["offload_num_in_group"])
            ),
            offload_prefetch_step=(
                0
                if schema_version in {1, 2}
                else _integer(serving["offload_prefetch_step"])
            ),
            wsl2_enable_pin_memory=(
                False
                if schema_version in {1, 2, 3}
                else _boolean(serving["wsl2_enable_pin_memory"])
            ),
        ),
        response_text=_string(root["response_text"]),
        ttft=_optional_duration(root["ttft_seconds"]),
        total_duration=Duration.seconds(_number(root["total_duration_seconds"])),
        prompt_tokens=_optional_integer(root["prompt_tokens"]),
        completion_tokens=_optional_integer(root["completion_tokens"]),
        completion_tokens_per_second=_optional_number(
            root["completion_tokens_per_second"],
        ),
        finish_reason=_optional_string(root["finish_reason"]),
        expectation_met=_optional_boolean(root["expectation_met"]),
    )


def _result_filename(result: ModelBenchmarkResult) -> str:
    """Create a safe collision-resistant JSON filename without a benchmark ID."""
    timestamp = result.started_at.isoformat().replace(":", "-").replace("+", "_")
    name = _SAFE_FILENAME.sub("-", result.case.name).strip(".-") or "benchmark"
    return f"{timestamp}-{name}-{uuid.uuid4().hex[:8]}.json"


def _duration_seconds(value: Duration | None) -> float | None:
    """Encode an optional duration in explicit seconds."""
    return value.total_seconds if value is not None else None


def _object(value: object) -> dict[str, object]:
    """Require a JSON object with string keys."""
    if not isinstance(value, dict):
        msg = "Benchmark artifact field must be an object."
        raise ValueError(msg)
    return cast("dict[str, object]", value)


def _string(value: object) -> str:
    """Require a JSON string."""
    if not isinstance(value, str):
        msg = "Benchmark artifact field must be text."
        raise ValueError(msg)
    return value


def _optional_string(value: object) -> str | None:
    """Require optional JSON text."""
    return None if value is None else _string(value)


def _integer(value: object) -> int:
    """Require a JSON integer but exclude booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        msg = "Benchmark artifact field must be an integer."
        raise ValueError(msg)
    return value


def _optional_integer(value: object) -> int | None:
    """Require an optional JSON integer."""
    return None if value is None else _integer(value)


def _number(value: object) -> float:
    """Require a finite JSON number but exclude booleans."""
    if (
        isinstance(value, bool)
        or not isinstance(value, int | float)
        or not math.isfinite(value)
    ):
        msg = "Benchmark artifact field must be numeric."
        raise ValueError(msg)
    return float(value)


def _optional_number(value: object) -> float | None:
    """Require an optional JSON number."""
    return None if value is None else _number(value)


def _boolean(value: object) -> bool:
    """Require a JSON boolean."""
    if not isinstance(value, bool):
        msg = "Benchmark artifact field must be boolean."
        raise ValueError(msg)
    return value


def _optional_boolean(value: object) -> bool | None:
    """Require an optional JSON boolean."""
    return None if value is None else _boolean(value)


def _optional_duration(value: object) -> Duration | None:
    """Decode an optional duration encoded in seconds."""
    return None if value is None else Duration.seconds(_number(value))
