# Copyright (c) 2026
# ruff: noqa: BLE001, INP001, T201
"""Experimental one-run local vLLM benchmark driver."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.commands import CommandExecutor
from devtools.model_benchmarks.models import BenchmarkCase, ModelBenchmarkResult
from devtools.model_benchmarks.runner import run_vllm_benchmark
from devtools.model_benchmarks.storage import save_benchmark_result
from devtools.model_serving.huggingface import HuggingFaceModelRef
from devtools.model_serving.vllm import (
    DEFAULT_READINESS_TIMEOUT,
    VLLMServer,
    VLLMServingConfig,
)
from devtools.paths import ResolvedPath, resolve_path
from devtools.time import Duration

if TYPE_CHECKING:
    from collections.abc import Sequence


_DEFAULT_PROMPT = "Reply with exactly: local model ready"
_DEFAULT_EXPECTED_RESPONSE = "local model ready"


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse explicit experimental vLLM serving and benchmark inputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        required=True,
        help="Pinned Hugging Face repository",
    )
    parser.add_argument(
        "--revision",
        required=True,
        help="40-character Hugging Face commit",
    )
    parser.add_argument("--image", required=True, help="Explicit vLLM image reference")
    parser.add_argument(
        "--cache-root",
        required=True,
        help="Visible model-cache directory",
    )
    parser.add_argument(
        "--output-root",
        required=True,
        help="Benchmark JSON output directory",
    )
    parser.add_argument(
        "--served-model-name",
        required=True,
        help="vLLM served model name",
    )
    parser.add_argument("--max-model-len", required=True, type=int)
    parser.add_argument("--gpu-memory-utilization", required=True, type=float)
    parser.add_argument(
        "--cpu-offload-gb",
        default=0.0,
        type=float,
        help="GiB of model weights per GPU that vLLM may offload to CPU memory.",
    )
    parser.add_argument(
        "--offload-backend",
        choices=("prefetch",),
        help="vLLM offload backend; prefetch copies selected layer weights to GPU.",
    )
    parser.add_argument(
        "--offload-group-size",
        default=0,
        type=int,
        help="Number of transformer layers in each vLLM prefetch offload group.",
    )
    parser.add_argument(
        "--offload-num-in-group",
        default=0,
        type=int,
        help="Number of layers offloaded in each vLLM prefetch group.",
    )
    parser.add_argument(
        "--offload-prefetch-step",
        default=0,
        type=int,
        help="Number of layers ahead vLLM prefetches selected offloaded weights.",
    )
    parser.add_argument("--max-num-seqs", required=True, type=int)
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--prompt", default=_DEFAULT_PROMPT)
    parser.add_argument("--expected-response")
    parser.add_argument("--max-tokens", default=32, type=int)
    parser.add_argument("--temperature", default=0.0, type=float)
    parser.add_argument(
        "--readiness-timeout-seconds",
        default=DEFAULT_READINESS_TIMEOUT.total_seconds,
        type=float,
        help="Maximum seconds to wait for vLLM model readiness after launch.",
    )
    parser.add_argument("--trust-remote-code", action="store_true")
    return parser.parse_args(arguments)


def build_configuration(
    arguments: argparse.Namespace,
    *,
    base_directory: Path,
) -> tuple[VLLMServingConfig, BenchmarkCase, ResolvedPath, Duration]:
    """Construct validated public library values from explicit driver arguments."""
    cache_root = resolve_path(arguments.cache_root, base_directory=base_directory)
    output_root = resolve_path(arguments.output_root, base_directory=base_directory)
    expected_response = arguments.expected_response
    if expected_response is None and arguments.prompt == _DEFAULT_PROMPT:
        expected_response = _DEFAULT_EXPECTED_RESPONSE

    return (
        VLLMServingConfig(
            model=HuggingFaceModelRef(arguments.model, arguments.revision),
            image=arguments.image,
            cache_root=cache_root,
            host_port=arguments.port,
            served_model_name=arguments.served_model_name,
            max_model_len=arguments.max_model_len,
            gpu_memory_utilization=arguments.gpu_memory_utilization,
            cpu_offload_gb=arguments.cpu_offload_gb,
            offload_backend=arguments.offload_backend,
            offload_group_size=arguments.offload_group_size,
            offload_num_in_group=arguments.offload_num_in_group,
            offload_prefetch_step=arguments.offload_prefetch_step,
            max_num_seqs=arguments.max_num_seqs,
            trust_remote_code=arguments.trust_remote_code,
        ),
        BenchmarkCase(
            name=arguments.served_model_name,
            prompt=arguments.prompt,
            max_tokens=arguments.max_tokens,
            temperature=arguments.temperature,
            expected_response=expected_response,
        ),
        output_root,
        Duration.seconds(arguments.readiness_timeout_seconds),
    )


async def run_experiment(
    *,
    config: VLLMServingConfig,
    case: BenchmarkCase,
    output_root: ResolvedPath,
    readiness_timeout: Duration,
) -> tuple[ModelBenchmarkResult, ResolvedPath]:
    """Start one owned server, benchmark it once, save the result, and stop it."""
    print(f"Cache root: {config.cache_root}")
    print("Starting vLLM...")
    server = await VLLMServer.start(
        config=config,
        executor=CommandExecutor(),
        readiness_timeout=readiness_timeout,
    )

    try:
        result = await run_vllm_benchmark(server=server, case=case)
        result_path = save_benchmark_result(result, output_root)
        _print_summary(
            result=result,
            result_path=result_path,
            cache_root=config.cache_root,
        )
    except BaseException:
        try:
            await server.stop()
        except Exception as error:
            print(f"Owned vLLM server cleanup failed: {error}", file=sys.stderr)
        raise
    else:
        await server.stop()
        return result, result_path


def _print_summary(
    *,
    result: ModelBenchmarkResult,
    result_path: ResolvedPath,
    cache_root: ResolvedPath,
) -> None:
    """Print a concise terminal summary while leaving JSON as the durable record."""
    print(f"Model repository: {result.serving.model_repository}")
    print(f"Model revision: {result.serving.model_revision}")
    print(f"Served model: {result.serving.served_model_name}")
    print(f"CPU weight offload: {result.serving.cpu_offload_gb} GiB")
    print(f"Offload backend: {result.serving.offload_backend or 'disabled'}")
    print(f"Prefetch group size: {result.serving.offload_group_size}")
    print(f"Prefetch layers per group: {result.serving.offload_num_in_group}")
    print(f"Prefetch step: {result.serving.offload_prefetch_step}")
    print(f"TTFT: {result.ttft}")
    print(f"Total duration: {result.total_duration}")
    print(f"Completion tokens: {result.completion_tokens}")
    print(f"Completion tokens/sec: {result.completion_tokens_per_second}")
    print(f"Expected response met: {result.expectation_met}")
    print(f"Benchmark JSON: {result_path}")
    print(f"Cache root: {cache_root}")


def main(arguments: Sequence[str] | None = None) -> None:
    """Run one experimental vLLM benchmark invocation."""
    parsed = parse_arguments(arguments)
    config, case, output_root, readiness_timeout = build_configuration(
        parsed,
        base_directory=Path.cwd(),
    )
    asyncio.run(
        run_experiment(
            config=config,
            case=case,
            output_root=output_root,
            readiness_timeout=readiness_timeout,
        ),
    )


if __name__ == "__main__":
    main()
