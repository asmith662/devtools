# Copyright (c) 2026
"""Pinned Hugging Face model references and GGUF artifact acquisition."""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import TYPE_CHECKING

from huggingface_hub import hf_hub_download

from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from collections.abc import Callable

_PINNED_REVISION = re.compile(r"^[0-9a-fA-F]{40}$")


@dataclass(frozen=True, slots=True)
class HuggingFaceModelRef:
    """Represent one exact Hugging Face model repository revision.

    vLLM's normal model-loading CLI consumes a repository plus revision; it
    does not consume an individual filename.  A future GGUF-oriented provider
    can pressure-test whether a distinct artifact-file value is warranted.

    :ivar repository: Hugging Face repository identifier.
    :ivar revision: Pinned commit revision to load.
    """

    repository: str
    revision: str

    def __post_init__(self) -> None:
        """Validate the local structural identity."""
        _validate_repository_and_revision(self.repository, self.revision)


@dataclass(frozen=True, slots=True)
class HuggingFaceGGUFRef:
    """Identify one exact GGUF artifact at an immutable Hub revision."""

    repository: str
    revision: str
    filename: str

    def __post_init__(self) -> None:
        """Validate the local structural identity."""
        _validate_repository_and_revision(self.repository, self.revision)
        posix_path = PurePosixPath(self.filename)
        windows_path = PureWindowsPath(self.filename)
        if (
            not self.filename
            or posix_path.is_absolute()
            or windows_path.is_absolute()
            or windows_path.drive
            or windows_path.root
        ):
            msg = "Hugging Face GGUF filename must be a relative artifact path."
            raise ValueError(msg)
        if ".." in posix_path.parts or ".." in windows_path.parts:
            msg = "Hugging Face GGUF filename cannot contain parent traversal."
            raise ValueError(msg)
        if posix_path.suffix.casefold() != ".gguf":
            msg = "Hugging Face GGUF filename must end with .gguf."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class AcquiredGGUF:
    """Expose an exact GGUF request and its persistent local cache result."""

    model: HuggingFaceGGUFRef
    cache_root: ResolvedPath
    path: ResolvedPath


async def acquire_huggingface_gguf(
    *,
    model: HuggingFaceGGUFRef,
    cache_root: ResolvedPath,
) -> AcquiredGGUF:
    """Acquire or reuse one pinned GGUF artifact in an explicit Hub cache."""
    return await asyncio.to_thread(_acquire, model, cache_root, hf_hub_download)


def _acquire(
    model: HuggingFaceGGUFRef,
    cache_root: ResolvedPath,
    download: Callable[..., str],
) -> AcquiredGGUF:
    """Run the synchronous Hub call and validate its local artifact result."""
    downloaded = download(
        repo_id=model.repository,
        filename=model.filename,
        revision=model.revision,
        cache_dir=str(cache_root.value),
    )
    path = Path(downloaded).absolute()
    storage_path = path.resolve()
    root = cache_root.value.resolve()
    if not path.is_relative_to(root) or not storage_path.is_relative_to(root):
        msg = "Hugging Face returned a path outside the configured cache root."
        raise ValueError(msg)
    if path.parts[-len(PurePosixPath(model.filename).parts) :] != tuple(
        PurePosixPath(model.filename).parts,
    ):
        msg = (
            "Hugging Face returned a path that does not retain the requested "
            "artifact identity."
        )
        raise ValueError(msg)
    if not storage_path.is_file():
        msg = "Hugging Face did not return an existing GGUF artifact file."
        raise ValueError(msg)
    return AcquiredGGUF(model, cache_root, ResolvedPath(path))


def _validate_repository_and_revision(repository: str, revision: str) -> None:
    """Validate the shared immutable Hub repository identity."""
    if not repository.strip():
        msg = "Hugging Face repository cannot be empty."
        raise ValueError(msg)
    if not revision.strip():
        msg = "Hugging Face revision cannot be empty."
        raise ValueError(msg)
    if _PINNED_REVISION.fullmatch(revision) is None:
        msg = "Hugging Face revision must be a pinned 40-character commit ID."
        raise ValueError(msg)
