# Copyright (c) 2026
# ruff: noqa: INP001
"""Pinned research-backed configuration for the first Qwen3.8 worker run.

This is data only: it neither acquires the GGUF nor starts llama.cpp.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from devtools.model_serving.huggingface import HuggingFaceGGUFRef


@dataclass(frozen=True, slots=True)
class Qwen38LlamaCppExperimentalProfile:
    """Freeze the model and serving dimensions for the first worker experiment."""

    model: HuggingFaceGGUFRef
    expected_sha256: str
    quant: str
    context_size: int
    n_cpu_ffn: int
    gpu_layers: int | Literal["auto", "all"]
    flash_attention: Literal["auto", "on", "off"]
    cache_type_k: str
    cache_type_v: str
    parallel_sequences: int
    image_build_identity: str | None = None


QWEN38_27B_UD_IQ4_XS = Qwen38LlamaCppExperimentalProfile(
    model=HuggingFaceGGUFRef(
        repository="unsloth/Qwen3.8-27B-GGUF",
        revision="16b6ae91d7429915de9e9a1c859c604731c78088",
        filename="Qwen3.8-27B-UD-IQ4_XS.gguf",
    ),
    expected_sha256="40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199",
    quant="Unsloth Dynamic IQ4_XS",
    context_size=32768,
    n_cpu_ffn=4,
    gpu_layers="all",
    flash_attention="on",
    cache_type_k="q4_0",
    cache_type_v="q4_0",
    parallel_sequences=1,
)
