# Copyright (c) 2026
"""Bounded observation of explicitly addressed repository text resources.

Observation is complete for exactly the finite caller-requested collection of
UTF-8 text resources. Resources are acquired sequentially in canonical address
order; the operation makes no atomic, repository-wide, or discovery claim.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Collection

    from devtools.context.repository.identity import Repository

from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.core.paths import ResolvedPath, resolve_path
from devtools.resources.filesystem import FileFormat, TextFile, read

_CONTENT_IDENTITY_SEMANTICS = "decoded-utf8-text-sha256-v1"
_SNAPSHOT_IDENTITY_SEMANTICS = RepositorySnapshot.OBSERVATION_SEMANTICS


class RepositoryObservationError(Exception):
    """Reject an observation that cannot satisfy its declared boundary."""


def observe_repository_resource(
    *,
    repository: Repository,
    root: ResolvedPath,
    address: RepositoryResourceAddress,
    maximum_resource_bytes: int,
) -> RepositorySnapshot:
    """Observe one required UTF-8 text resource through one bounded read.

    Success means the exact requested address resolved beneath ``root`` and was
    read completely according to :func:`devtools.resources.filesystem.read`.
    The operation does not discover other resources or claim an atomic view of
    the containing filesystem.

    :raises RepositoryObservationError: If resolution escapes the supplied root.
    :raises FilesystemError: If the required resource cannot be read completely.
    """
    return observe_repository_resources(
        repository=repository,
        root=root,
        addresses=(address,),
        maximum_resource_bytes=maximum_resource_bytes,
    )


def observe_repository_resources(
    *,
    repository: Repository,
    root: ResolvedPath,
    addresses: Collection[RepositoryResourceAddress],
    maximum_resource_bytes: int,
) -> RepositorySnapshot:
    """Observe a finite explicit collection of required UTF-8 text resources.

    Addresses are canonicalized into repository-relative lexical order before
    sequential acquisition. Success means every distinct requested address was
    read completely. A failure raises without publishing a partial snapshot.
    Equivalent collections therefore produce equivalent state regardless of
    caller ordering or observation root, but no simultaneous filesystem view is
    claimed.

    :raises ValueError: If the byte bound is nonpositive or an address is repeated.
    :raises RepositoryObservationError: If resolution escapes the supplied root.
    :raises FilesystemError: If any required resource cannot be read completely.
    """
    requested_addresses = tuple(addresses)
    if maximum_resource_bytes <= 0:
        msg = "Repository observation maximum resource bytes must be positive."
        raise ValueError(msg)
    if len(set(requested_addresses)) != len(requested_addresses):
        msg = "Repository observation resource addresses must be distinct."
        raise ValueError(msg)

    ordered_addresses = tuple(
        sorted(requested_addresses, key=lambda requested: requested.value),
    )
    normalized_root = resolve_path(root.value)
    resources = tuple(
        _observe_resource(
            root=normalized_root,
            address=requested,
            maximum_resource_bytes=maximum_resource_bytes,
        )
        for requested in ordered_addresses
    )
    snapshot_id = RepositorySnapshotId(
        _semantic_digest(
            _SNAPSHOT_IDENTITY_SEMANTICS,
            str(repository.id),
            *(
                value
                for resource in resources
                for value in (
                    str(resource.address),
                    str(resource.content_identity),
                )
            ),
        ),
    )
    return RepositorySnapshot(
        id=snapshot_id,
        repository_id=repository.id,
        resources=resources,
    )


def _observe_resource(
    *,
    root: ResolvedPath,
    address: RepositoryResourceAddress,
    maximum_resource_bytes: int,
) -> RepositoryResourceOccurrence:
    """Acquire one required occurrence within a normalized observation root."""
    candidate = resolve_path(
        Path(*address.parts),
        base_directory=root.value,
    )
    if not candidate.value.is_relative_to(root.value):
        msg = f"Repository resource resolves outside the observation root: {address}."
        raise RepositoryObservationError(msg)

    file = cast(
        "TextFile",
        read(
            candidate,
            file_format=FileFormat.TEXT,
            max_bytes=maximum_resource_bytes,
        ),
    )
    content_identity = ContentIdentity(
        _semantic_digest(_CONTENT_IDENTITY_SEMANTICS, file.content),
    )
    return RepositoryResourceOccurrence(
        address=address,
        content_identity=content_identity,
        content=file.content,
        encoding=file.encoding,
        byte_size=file.byte_size,
    )


def _semantic_digest(semantics: str, *values: str) -> str:
    """Hash unambiguous length-framed semantic values for this module."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big"))
        digest.update(encoded)
    return digest.hexdigest()
