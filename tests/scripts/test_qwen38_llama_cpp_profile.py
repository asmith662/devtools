# Copyright (c) 2026
# ruff: noqa: INP001
"""Tests for the single tracked Qwen3.8 worker profile."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType


_PROFILE_PATH = Path("scripts/model_benchmarks/qwen38_llama_cpp_profile.py")
_CONTEXT_SIZE = 32_768
_CPU_FFN_LAYERS = 0
_IMAGE_BUILD_IDENTITY = (
    "ghcr.io/ggml-org/llama.cpp:server-cuda-b10868@"
    "sha256:7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e"
)


@pytest.fixture
def profile_module() -> ModuleType:
    """Load the tracked profile without turning scripts into a package."""
    specification = importlib.util.spec_from_file_location(
        "test_qwen38_llama_cpp_profile",
        _PROFILE_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def test_profile_freezes_exact_research_backed_provenance(
    profile_module: ModuleType,
) -> None:
    """The profile is one immutable Qwen artifact and serving configuration."""
    profile = profile_module.QWEN38_27B_UD_IQ4_XS

    assert profile.model.repository == "unsloth/Qwen3.8-27B-GGUF"
    assert profile.model.revision == "16b6ae91d7429915de9e9a1c859c604731c78088"
    assert profile.model.filename == "Qwen3.8-27B-UD-IQ4_XS.gguf"
    assert (
        profile.expected_sha256
        == "40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199"
    )
    assert profile.context_size == _CONTEXT_SIZE
    assert profile.n_cpu_ffn == _CPU_FFN_LAYERS
    assert profile.flash_attention == "on"
    assert profile.cache_type_k == profile.cache_type_v == "q4_0"
    assert profile.parallel_sequences == 1
    assert profile.image_build_identity == _IMAGE_BUILD_IDENTITY
    with pytest.raises(FrozenInstanceError):
        profile.context_size = 1
