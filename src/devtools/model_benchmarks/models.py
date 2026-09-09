# Copyright (c) 2026
"""Immutable values for experimental vLLM benchmark runs."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from devtools.model_serving.vllm import VLLMServer
    from devtools.time import Duration, Timestamp


@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    """Describe one small chat-completion workload."""

    name: str
    prompt: str
    max_tokens: int
    temperature: float = 0.0
    expected_response: str | None = None

    def __post_init__(self) -> None:
        """Validate structural benchmark-workload constraints."""
        if not self.name.strip():
            msg = "Benchmark case name cannot be empty."
            raise ValueError(msg)
        if not self.prompt.strip():
            msg = "Benchmark prompt cannot be empty."
            raise ValueError(msg)
        if self.max_tokens <= 0:
            msg = "Benchmark maximum tokens must be positive."
            raise ValueError(msg)
        if not math.isfinite(self.temperature) or self.temperature < 0:
            msg = "Benchmark temperature must be finite and non-negative."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class VLLMBenchmarkServingSnapshot:
    """Capture the vLLM launch facts needed to interpret one benchmark."""

    model_repository: str
    model_revision: str
    served_model_name: str
    image: str
    max_model_len: int
    gpu_memory_utilization: float
    max_num_seqs: int
    trust_remote_code: bool
    cpu_offload_gb: float = 0.0
    offload_backend: str | None = None
    offload_group_size: int = 0
    offload_num_in_group: int = 0
    offload_prefetch_step: int = 0
    wsl2_enable_pin_memory: bool = False
    estimate_cudagraph_memory: bool = True

    @classmethod
    def from_server(cls, server: VLLMServer) -> VLLMBenchmarkServingSnapshot:
        """Extract immutable serving facts through the public server config."""
        config = server.config
        return cls(
            model_repository=config.model.repository,
            model_revision=config.model.revision,
            served_model_name=config.served_model_name,
            image=config.image,
            max_model_len=config.max_model_len,
            gpu_memory_utilization=config.gpu_memory_utilization,
            max_num_seqs=config.max_num_seqs,
            trust_remote_code=config.trust_remote_code,
            cpu_offload_gb=config.cpu_offload_gb,
            offload_backend=config.offload_backend,
            offload_group_size=config.offload_group_size,
            offload_num_in_group=config.offload_num_in_group,
            offload_prefetch_step=config.offload_prefetch_step,
            wsl2_enable_pin_memory=config.wsl2_enable_pin_memory,
            estimate_cudagraph_memory=config.estimate_cudagraph_memory,
        )


@dataclass(frozen=True, slots=True)
class ModelBenchmarkResult:
    """Record one completed streamed vLLM benchmark request."""

    started_at: Timestamp
    case: BenchmarkCase
    serving: VLLMBenchmarkServingSnapshot
    response_text: str
    ttft: Duration | None
    total_duration: Duration
    prompt_tokens: int | None
    completion_tokens: int | None
    completion_tokens_per_second: float | None
    finish_reason: str | None
    expectation_met: bool | None

    def __post_init__(self) -> None:
        """Validate measurements that can be checked without provider inference."""
        if self.ttft is not None and self.ttft.value > self.total_duration.value:
            msg = "TTFT cannot exceed total benchmark duration."
            raise ValueError(msg)
        if self.prompt_tokens is not None and self.prompt_tokens < 0:
            msg = "Prompt token count cannot be negative."
            raise ValueError(msg)
        if self.completion_tokens is not None and self.completion_tokens < 0:
            msg = "Completion token count cannot be negative."
            raise ValueError(msg)
        if self.completion_tokens_per_second is not None and (
            not math.isfinite(self.completion_tokens_per_second)
            or self.completion_tokens_per_second < 0
        ):
            msg = "Completion throughput must be finite and non-negative."
            raise ValueError(msg)


SupervisorReviewOutcome = Literal[
    "accepted",
    "correction_requested",
    "rejected",
    "escalated",
]
_SUPERVISOR_REVIEW_OUTCOMES = frozenset(
    ("accepted", "correction_requested", "rejected", "escalated"),
)


@dataclass(frozen=True, slots=True)
class WorkerStoryResult:
    """Record acceptance telemetry for one completed experimental worker story."""

    story_name: str
    difficulty: int
    started_at: Timestamp
    duration: Duration
    gates_passed: bool
    review_outcome: SupervisorReviewOutcome
    local_repair_attempts: int
    supervisor_correction_turns: int
    supervisor_prompt_tokens: int | None
    supervisor_completion_tokens: int | None
    escalated: bool
    escalation_reason: str | None
    architecture_violation_count: int
    human_intervention: bool

    def __post_init__(self) -> None:  # noqa: C901
        """Validate bounded, independently observable worker telemetry."""
        if not self.story_name.strip():
            msg = "Story name cannot be empty."
            raise ValueError(msg)
        if (
            isinstance(self.difficulty, bool)
            or not isinstance(self.difficulty, int)
            or self.difficulty not in {1, 2, 3, 4, 5}
        ):
            msg = "Story difficulty must be an integer from 1 through 5."
            raise ValueError(msg)
        if self.review_outcome not in _SUPERVISOR_REVIEW_OUTCOMES:
            msg = "Supervisor review outcome is invalid."
            raise ValueError(msg)
        for value, label in (
            (self.local_repair_attempts, "Local repair attempts"),
            (self.supervisor_correction_turns, "Supervisor correction turns"),
            (self.architecture_violation_count, "Architecture violation count"),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                msg = f"{label} must be an integer."
                raise TypeError(msg)
            if value < 0:
                msg = f"{label} cannot be negative."
                raise ValueError(msg)
        for optional_value, label in (
            (self.supervisor_prompt_tokens, "Supervisor prompt tokens"),
            (self.supervisor_completion_tokens, "Supervisor completion tokens"),
        ):
            if optional_value is not None and (
                isinstance(optional_value, bool)
                or not isinstance(optional_value, int)
            ):
                msg = f"{label} must be an integer."
                raise TypeError(msg)
            if optional_value is not None and optional_value < 0:
                msg = f"{label} cannot be negative."
                raise ValueError(msg)
        if self.escalation_reason is not None and not self.escalation_reason.strip():
            msg = "Escalation reason cannot be blank when supplied."
            raise ValueError(msg)
