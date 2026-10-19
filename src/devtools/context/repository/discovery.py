# Copyright (c) 2026
"""Bounded discovery of repository-relative regular-file addresses.

Discovery inspects filesystem metadata beneath one explicit root. It does not
read file content, publish resource occurrences, or construct repository
snapshot state. Symbolic links and Windows junctions are skipped rather than
followed. Traversal is sequential and makes no atomic or race-free filesystem
claim.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath, resolve_path

if TYPE_CHECKING:
    from collections.abc import Collection

    from devtools.context.repository.identity import Repository, RepositoryId


class RepositoryResourceDiscoveryError(Exception):
    """Report failure to complete one bounded repository resource discovery."""

    root: ResolvedPath
    discovery_message: str

    def __init__(self, *, root: ResolvedPath, message: str) -> None:
        """Capture the discovery root and narrow failure diagnostic."""
        self.root = root
        self.discovery_message = message
        super().__init__(
            f"Could not discover repository resources beneath {root}: {message}",
        )


@dataclass(frozen=True, slots=True)
class RepositoryResourceDiscovery:
    """Retain one bounded regular-file address discovery result."""

    repository_id: RepositoryId
    root: ResolvedPath
    maximum_resource_count: int
    maximum_traversal_entry_count: int
    examined_entry_count: int
    addresses: tuple[RepositoryResourceAddress, ...]
    requested_addresses: tuple[RepositoryResourceAddress, ...] | None = None

    DISCOVERY_SEMANTICS: ClassVar[str] = (
        "recursive-entry-bounded-regular-files-skip-links-lexical-address-order-v2"
    )

    @property
    def semantics(self) -> str:
        """Distinguish explicit component probes from recursive enumeration."""
        if self.requested_addresses is not None:
            return "explicit-address-component-bounded-regular-files-v1"
        return self.DISCOVERY_SEMANTICS


@dataclass(slots=True)
class _DiscoveryState:
    """Track the two local finite bounds during one discovery operation."""

    root: ResolvedPath
    maximum_resource_count: int
    maximum_traversal_entry_count: int
    examined_entry_count: int = 0
    discovered: list[RepositoryResourceAddress] = field(default_factory=list)

    def examine_entry(self) -> None:
        """Account for one enumerated filesystem entry before classification."""
        self.examined_entry_count += 1
        if self.examined_entry_count > self.maximum_traversal_entry_count:
            msg = (
                "Examined filesystem entry count exceeds maximum "
                f"{self.maximum_traversal_entry_count}."
            )
            raise RepositoryResourceDiscoveryError(root=self.root, message=msg)

    def add_resource(self, address: RepositoryResourceAddress) -> None:
        """Account for one discovered regular resource before publication."""
        self.discovered.append(address)
        if len(self.discovered) > self.maximum_resource_count:
            msg = (
                "Discovered resource count exceeds maximum "
                f"{self.maximum_resource_count}."
            )
            raise RepositoryResourceDiscoveryError(root=self.root, message=msg)


def discover_repository_resource_addresses(
    *,
    repository: Repository,
    root: ResolvedPath,
    maximum_resource_count: int,
    maximum_traversal_entry_count: int,
    requested_addresses: Collection[RepositoryResourceAddress] | None = None,
) -> RepositoryResourceDiscovery:
    """Discover regular-file addresses recursively beneath an explicit root.

    Traversal uses metadata only, skips symbolic links and Windows junctions,
    and returns canonical addresses in lexical order. Independent positive
    limits bound examined filesystem entries and discovered regular resources.
    Exceeding either limit or encountering a required traversal failure raises
    without publishing a partial discovery result.

    With ``requested_addresses``, probe only those canonical paths without
    directory enumeration. Each component probe counts against the traversal
    limit, including repeated parents. Missing/nonregular/link-like required
    paths refuse. ``requested_addresses`` and ``semantics`` retain this scope;
    it is never a claim to have discovered the entire repository.
    """
    if maximum_resource_count <= 0:
        msg = "Maximum discovered resource count must be positive."
        raise ValueError(msg)
    if maximum_traversal_entry_count <= 0:
        msg = "Maximum traversal entry count must be positive."
        raise ValueError(msg)

    normalized_root = resolve_path(root.value)
    state = _DiscoveryState(
        root=normalized_root,
        maximum_resource_count=maximum_resource_count,
        maximum_traversal_entry_count=maximum_traversal_entry_count,
    )
    requested = None
    if requested_addresses is None:
        _discover_regular_files(state=state, directory=normalized_root.value)
    else:
        requested = tuple(sorted(requested_addresses, key=lambda a: a.value))
        if len(set(requested)) != len(requested):
            msg = "Requested discovery addresses must be distinct."
            raise ValueError(msg)
        _discover_requested_files(state, requested)
    return RepositoryResourceDiscovery(
        repository_id=repository.id,
        root=normalized_root,
        maximum_resource_count=maximum_resource_count,
        maximum_traversal_entry_count=maximum_traversal_entry_count,
        examined_entry_count=state.examined_entry_count,
        addresses=tuple(
            sorted(state.discovered, key=lambda address: address.value),
        ),
        requested_addresses=requested,
    )


def _discover_requested_files(
    state: _DiscoveryState,
    addresses: tuple[RepositoryResourceAddress, ...],
) -> None:
    """Probe only required paths; count each component probe against the bound.

    Link-like required components refuse rather than silently returning partial
    membership. This is metadata discovery, not content acquisition or an atomic
    filesystem claim. Unrequested directories are never enumerated.
    """
    for address in addresses:
        candidate = state.root.value
        try:
            for part in address.parts:
                state.examine_entry()
                candidate = candidate / part
                if candidate.is_symlink() or candidate.is_junction():
                    msg = f"Requested discovery path contains a link: {address}."
                    raise RepositoryResourceDiscoveryError(root=state.root, message=msg)
            if not candidate.is_file():
                msg = f"Requested discovery path is not a regular file: {address}."
                raise RepositoryResourceDiscoveryError(root=state.root, message=msg)
        except OSError as error:
            raise RepositoryResourceDiscoveryError(
                root=state.root,
                message=str(error),
            ) from error
        state.add_resource(address)


def _discover_regular_files(
    *,
    state: _DiscoveryState,
    directory: Path,
) -> None:
    """Traverse one directory without following link-like entries."""
    try:
        with os.scandir(directory) as iterator:
            entries = []
            for entry in iterator:
                state.examine_entry()
                entries.append(entry)
            entries.sort(key=lambda entry: entry.name)
    except OSError as error:
        raise RepositoryResourceDiscoveryError(
            root=state.root,
            message=str(error),
        ) from error

    for entry in entries:
        try:
            is_symlink = entry.is_symlink()
            is_junction = entry.is_junction()
            if is_symlink or is_junction:
                continue
            if entry.is_dir(follow_symlinks=False):
                child = resolve_path(entry.path)
                if not child.value.is_relative_to(state.root.value):
                    msg = f"Resolved directory escapes discovery root: {entry.path}."
                    raise RepositoryResourceDiscoveryError(
                        root=state.root,
                        message=msg,
                    )
                _discover_regular_files(
                    state=state,
                    directory=child.value,
                )
            if not entry.is_file(follow_symlinks=False):
                continue
        except OSError as error:
            raise RepositoryResourceDiscoveryError(
                root=state.root,
                message=str(error),
            ) from error

        relative_path = Path(entry.path).relative_to(state.root.value)
        state.add_resource(RepositoryResourceAddress(relative_path.as_posix()))
