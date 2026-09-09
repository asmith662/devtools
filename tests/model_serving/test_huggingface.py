# Copyright (c) 2026
"""Tests for pinned Hugging Face model references."""

from __future__ import annotations

import asyncio
from dataclasses import FrozenInstanceError
from typing import TYPE_CHECKING

import pytest
from huggingface_hub.errors import LocalEntryNotFoundError

from devtools.model_serving.huggingface import (
    AcquiredGGUF,
    HuggingFaceGGUFRef,
    HuggingFaceModelRef,
    acquire_huggingface_gguf,
)
from devtools.model_serving.llama_cpp import GGUFModel
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path


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


def test_gguf_ref_is_immutable_exact_artifact_identity() -> None:
    """A GGUF reference retains repository, revision, and artifact filename."""
    reference = HuggingFaceGGUFRef(
        "org/model",
        "a" * 40,
        "quant/model.Q4_K_M.gguf",
    )

    assert reference == HuggingFaceGGUFRef(
        "org/model",
        "a" * 40,
        "quant/model.Q4_K_M.gguf",
    )
    with pytest.raises(FrozenInstanceError):
        reference.filename = "other.gguf"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("repository", "revision", "filename"),
    [
        ("", "a" * 40, "model.gguf"),
        ("org/model", "main", "model.gguf"),
        ("org/model", "a" * 39, "model.gguf"),
        ("org/model", "g" * 40, "model.gguf"),
        ("org/model", "a" * 41, "model.gguf"),
        ("org/model", "a" * 40, "model.json"),
        ("org/model", "a" * 40, "/model.gguf"),
        ("org/model", "a" * 40, "/path/model.gguf"),
        ("org/model", "a" * 40, "C:/models/model.gguf"),
        ("org/model", "a" * 40, r"C:\models\model.gguf"),
        ("org/model", "a" * 40, r"\\server\share\model.gguf"),
        ("org/model", "a" * 40, "../model.gguf"),
        ("org/model", "a" * 40, r"foo\..\..\model.gguf"),
    ],
)
def test_gguf_ref_rejects_nonreproducible_or_unsafe_identity(
    repository: str,
    revision: str,
    filename: str,
) -> None:
    """Only a pinned relative GGUF artifact can enter acquisition."""
    with pytest.raises(ValueError, match="Hugging Face"):
        HuggingFaceGGUFRef(repository, revision, filename)


def test_acquire_gguf_maps_exact_identity_to_explicit_cache(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Acquisition delegates the exact request and exposes its cached file."""
    cache = tmp_path / "cache"
    artifact = (
        cache
        / "models--org--model"
        / "snapshots"
        / ("a" * 40)
        / "nested"
        / "model.gguf"
    )
    artifact.parent.mkdir(parents=True)
    artifact.write_bytes(b"GGUF")
    calls: list[dict[str, str]] = []

    def download(**kwargs: str) -> str:
        calls.append(kwargs)
        return str(artifact)

    monkeypatch.setattr("devtools.model_serving.huggingface.hf_hub_download", download)
    reference = HuggingFaceGGUFRef("org/model", "a" * 40, "nested/model.gguf")
    acquired = asyncio.run(
        acquire_huggingface_gguf(
            model=reference,
            cache_root=ResolvedPath(cache),
        ),
    )

    assert calls == [
        {
            "repo_id": "org/model",
            "filename": "nested/model.gguf",
            "revision": "a" * 40,
            "cache_dir": str(cache),
        },
    ]
    assert acquired == AcquiredGGUF(
        reference,
        ResolvedPath(cache),
        ResolvedPath(artifact.resolve()),
    )
    assert GGUFModel(acquired.path).path == ResolvedPath(artifact.resolve())


def test_acquire_gguf_retains_snapshot_gguf_path_for_suffixless_blob(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A Hub snapshot link may store a GGUF in a suffixless content blob."""
    cache = tmp_path / "cache"
    blob = cache / "blobs" / ("a" * 64)
    blob.parent.mkdir(parents=True)
    blob.write_bytes(b"GGUF")
    snapshot = cache / "snapshots" / ("a" * 40) / "model.gguf"
    snapshot.parent.mkdir(parents=True)
    snapshot.symlink_to(blob)
    monkeypatch.setattr(
        "devtools.model_serving.huggingface.hf_hub_download",
        lambda **_kwargs: str(snapshot),
    )

    acquired = asyncio.run(
        acquire_huggingface_gguf(
            model=HuggingFaceGGUFRef("org/model", "a" * 40, "model.gguf"),
            cache_root=ResolvedPath(cache),
        ),
    )

    assert acquired.path == ResolvedPath(snapshot.absolute())
    assert acquired.path.suffix == ".gguf"
    assert acquired.path.value.resolve() == blob.resolve()


@pytest.mark.parametrize(
    "kind",
    ["missing", "directory", "non_gguf", "outside_cache"],
)
def test_acquire_gguf_rejects_invalid_hub_result(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    kind: str,
) -> None:
    """A Hub result must name an existing GGUF file under the selected cache."""
    cache = tmp_path / "cache"
    returned = cache / "artifact.gguf"
    if kind == "directory":
        returned.mkdir(parents=True)
    elif kind == "non_gguf":
        returned = cache / "artifact.json"
        returned.parent.mkdir(parents=True)
        returned.write_text("{}")
    elif kind == "outside_cache":
        returned = tmp_path / "outside.gguf"
        returned.write_bytes(b"GGUF")
    monkeypatch.setattr(
        "devtools.model_serving.huggingface.hf_hub_download",
        lambda **_kwargs: str(returned),
    )

    with pytest.raises(ValueError, match="Hugging Face"):
        asyncio.run(
            acquire_huggingface_gguf(
                model=HuggingFaceGGUFRef("org/model", "a" * 40, "artifact.gguf"),
                cache_root=ResolvedPath(cache),
            ),
        )


def test_acquire_gguf_rejects_snapshot_resolving_outside_cache(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A cache-local snapshot link cannot escape its explicit cache root."""
    cache = tmp_path / "cache"
    outside = tmp_path / "outside-blob"
    outside.write_bytes(b"GGUF")
    snapshot = cache / "snapshots" / ("a" * 40) / "artifact.gguf"
    snapshot.parent.mkdir(parents=True)
    snapshot.symlink_to(outside)
    monkeypatch.setattr(
        "devtools.model_serving.huggingface.hf_hub_download",
        lambda **_kwargs: str(snapshot),
    )

    with pytest.raises(ValueError, match="outside"):
        asyncio.run(
            acquire_huggingface_gguf(
                model=HuggingFaceGGUFRef("org/model", "a" * 40, "artifact.gguf"),
                cache_root=ResolvedPath(cache),
            ),
        )


def test_acquire_gguf_preserves_hub_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Hub/provider failures remain available to callers unchanged."""
    error = LocalEntryNotFoundError("Hub cache entry unavailable")

    def download(**_kwargs: str) -> str:
        raise error

    monkeypatch.setattr("devtools.model_serving.huggingface.hf_hub_download", download)

    with pytest.raises(LocalEntryNotFoundError) as raised:
        asyncio.run(
            acquire_huggingface_gguf(
                model=HuggingFaceGGUFRef("org/model", "a" * 40, "artifact.gguf"),
                cache_root=ResolvedPath(tmp_path / "cache"),
            ),
        )

    assert raised.value is error
