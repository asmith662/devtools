# Copyright (c) 2026
"""Tests for pinned Hugging Face model references."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from devtools.model_serving.huggingface import HuggingFaceModelRef


def test_model_ref_is_immutable_hashable_value() -> None:
    """A pinned repository reference has ordinary immutable value semantics."""
    reference = HuggingFaceModelRef("Qwen/Qwen3-8B", "a" * 40)

    assert reference == HuggingFaceModelRef("Qwen/Qwen3-8B", "a" * 40)
    assert hash(reference) == hash(HuggingFaceModelRef("Qwen/Qwen3-8B", "a" * 40))

    with pytest.raises(FrozenInstanceError):
        reference.repository = "other/model"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("repository", "revision", "match"),
    [
        ("", "a" * 40, "repository"),
        ("   ", "a" * 40, "repository"),
        ("Qwen/Qwen3-8B", "", "revision"),
        ("Qwen/Qwen3-8B", "latest", "pinned"),
        ("Qwen/Qwen3-8B", "main", "pinned"),
    ],
)
def test_model_ref_rejects_unusable_identity(
    repository: str,
    revision: str,
    match: str,
) -> None:
    """Unpinned or blank repository identity cannot reproduce a launch."""
    with pytest.raises(ValueError, match=match):
        HuggingFaceModelRef(repository, revision)
