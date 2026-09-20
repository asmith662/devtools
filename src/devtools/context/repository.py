# Copyright (c) 2026
"""Bounded observation of explicitly addressed repository text resources.

Observation is complete for exactly the finite caller-requested collection of
UTF-8 text resources. Resources are acquired sequentially in canonical address
order; the operation makes no atomic, repository-wide, or discovery claim.
"""

from __future__ import annotations

import hashlib
import string
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import TYPE_CHECKING, ClassVar, cast

if TYPE_CHECKING:
    from collections.abc import Collection

from devtools.core.identity import Identity
from devtools.core.paths import ResolvedPath, resolve_path
from devtools.resources.filesystem import FileFormat, TextFile, read

_CONTENT_IDENTITY_SEMANTICS = "decoded-utf8-text-sha256-v1"
_SNAPSHOT_IDENTITY_SEMANTICS = "explicit-required-text-resources-sha256-v1"
_SHA256_HEX_LENGTH = 64


class RepositoryObservationError(Exception):
    """Reject an observation that cannot satisfy its declared boundary."""


@dataclass(frozen=True, slots=True)
class RepositoryId:
    """Identify one logical Repository independently of its location or state."""

    value: Identity

    @classmethod
    def new(cls) -> RepositoryId:
        """Generate a new nominal Repository identity."""
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> RepositoryId:
        """Parse a Repository identity from UUID text."""
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return canonical UUID text."""
        return str(self.value)


@dataclass(frozen=True, slots=True)
class Repository:
    """Represent a logical software repository across changing states."""

    id: RepositoryId

    @classmethod
    def new(cls) -> Repository:
        """Create a logical Repository with a new nominal identity."""
        return cls(RepositoryId.new())


@dataclass(frozen=True, slots=True)
class RepositoryResourceAddress:
    """Represent one canonical POSIX-style path relative to a repository root."""

    value: str

    def __post_init__(self) -> None:
        """Reject empty, absolute, noncanonical, or traversing addresses."""
        if not self.value:
            msg = "Repository resource address cannot be empty."
            raise ValueError(msg)
        if "\\" in self.value:
            msg = "Repository resource address must use forward slashes."
            raise ValueError(msg)

        posix_path = PurePosixPath(self.value)
        windows_path = PureWindowsPath(self.value)
        if posix_path.is_absolute() or windows_path.drive:
            msg = "Repository resource address must be relative."
            raise ValueError(msg)

        parts = self.value.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            msg = "Repository resource address must be canonical without traversal."
            raise ValueError(msg)

    @property
    def parts(self) -> tuple[str, ...]:
        """Return canonical repository-relative path components."""
        return tuple(self.value.split("/"))

    def __str__(self) -> str:
        """Return the canonical repository-relative address."""
        return self.value


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Identify decoded UTF-8 text independently of its repository address."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Content identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value


@dataclass(frozen=True, slots=True)
class RepositorySnapshotId:
    """Identify state observed under this module's bounded semantics."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Repository snapshot identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value


@dataclass(frozen=True, slots=True)
class RepositoryResourceOccurrence:
    """Retain one addressed text occurrence and its independent content identity."""

    address: RepositoryResourceAddress
    content_identity: ContentIdentity
    content: str
    encoding: str
    byte_size: int


@dataclass(frozen=True, slots=True)
class RepositorySnapshot:
    """Represent complete state for an explicit required resource collection."""

    OBSERVATION_SEMANTICS: ClassVar[str] = _SNAPSHOT_IDENTITY_SEMANTICS

    id: RepositorySnapshotId
    repository_id: RepositoryId
    resources: tuple[RepositoryResourceOccurrence, ...]

    @property
    def resource(self) -> RepositoryResourceOccurrence:
        """Return the sole occurrence for compatible single-resource consumers."""
        if len(self.resources) != 1:
            msg = "Repository snapshot does not contain exactly one resource."
            raise ValueError(msg)
        return self.resources[0]


def observe_repository_resource(
    *,
    repository: Repository,
    root: ResolvedPath,
    address: RepositoryResourceAddress,
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
    )


def observe_repository_resources(
    *,
    repository: Repository,
    root: ResolvedPath,
    addresses: Collection[RepositoryResourceAddress],
) -> RepositorySnapshot:
    """Observe a finite explicit collection of required UTF-8 text resources.

    Addresses are canonicalized into repository-relative lexical order before
    sequential acquisition. Success means every distinct requested address was
    read completely. A failure raises without publishing a partial snapshot.
    Equivalent collections therefore produce equivalent state regardless of
    caller ordering or observation root, but no simultaneous filesystem view is
    claimed.

    :raises ValueError: If no addresses are supplied or an address is repeated.
    :raises RepositoryObservationError: If resolution escapes the supplied root.
    :raises FilesystemError: If any required resource cannot be read completely.
    """
    requested_addresses = tuple(addresses)
    if not requested_addresses:
        msg = "Repository observation requires at least one resource address."
        raise ValueError(msg)
    if len(set(requested_addresses)) != len(requested_addresses):
        msg = "Repository observation resource addresses must be distinct."
        raise ValueError(msg)

    ordered_addresses = tuple(
        sorted(requested_addresses, key=lambda requested: requested.value),
    )
    normalized_root = resolve_path(root.value)
    resources = tuple(
        _observe_resource(root=normalized_root, address=requested)
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
) -> RepositoryResourceOccurrence:
    """Acquire one required occurrence within a normalized observation root."""
    candidate = resolve_path(
        Path(*address.parts),
        base_directory=root.value,
    )
    if not candidate.value.is_relative_to(root.value):
        msg = f"Repository resource resolves outside the observation root: {address}."
        raise RepositoryObservationError(msg)

    file = cast("TextFile", read(candidate, file_format=FileFormat.TEXT))
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


def _validate_sha256(value: str, *, label: str) -> None:
    """Validate one lowercase SHA-256 hexadecimal representation."""
    if len(value) != _SHA256_HEX_LENGTH or any(
        character not in string.hexdigits for character in value
    ):
        msg = f"{label} must be a 64-character hexadecimal SHA-256 value."
        raise ValueError(msg)
    if value != value.lower():
        msg = f"{label} must use lowercase hexadecimal."
        raise ValueError(msg)
