# Copyright (c) 2026
"""Explicit membership intent grounded in one completed repository discovery."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.repository.resource import _validate_sha256

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.discovery import RepositoryResourceDiscovery
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True, slots=True)
class RepositoryTextCorpusId:
    """Identify selected observed textual state under corpus realization semantics."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Repository text corpus identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value


@dataclass(frozen=True, slots=True)
class RepositoryTextCorpusDefinition:
    """Retain selected discovered addresses for one future textual corpus attempt."""

    discovery: RepositoryResourceDiscovery
    selected_addresses: tuple[RepositoryResourceAddress, ...]

    DEFINITION_SEMANTICS: ClassVar[str] = (
        "explicit-discovery-grounded-text-corpus-membership-v1"
    )

    @property
    def excluded_addresses(self) -> tuple[RepositoryResourceAddress, ...]:
        """Return discovered addresses not selected by this definition."""
        selected = set(self.selected_addresses)
        return tuple(
            address for address in self.discovery.addresses if address not in selected
        )


@dataclass(frozen=True, slots=True)
class RepositoryTextCorpus:
    """Retain selected observed UTF-8 resource state for one corpus definition."""

    id: RepositoryTextCorpusId
    definition: RepositoryTextCorpusDefinition
    resources: tuple[RepositoryResourceOccurrence, ...]

    REALIZATION_SEMANTICS: ClassVar[str] = (
        "selected-observed-utf8-resource-occurrences-sha256-v1"
    )


def define_repository_text_corpus(
    *,
    discovery: RepositoryResourceDiscovery,
    selected_addresses: Sequence[RepositoryResourceAddress],
) -> RepositoryTextCorpusDefinition:
    """Define explicit membership without reading, classifying, or parsing resources."""
    requested = tuple(selected_addresses)
    if len(set(requested)) != len(requested):
        msg = "Repository text corpus selected addresses must be distinct."
        raise ValueError(msg)
    discovered = set(discovery.addresses)
    missing = tuple(address for address in requested if address not in discovered)
    if missing:
        msg = f"Repository text corpus address was not discovered: {missing[0]}."
        raise ValueError(msg)
    selected = set(requested)
    return RepositoryTextCorpusDefinition(
        discovery=discovery,
        selected_addresses=tuple(
            address for address in discovery.addresses if address in selected
        ),
    )


def realize_repository_text_corpus(
    *,
    definition: RepositoryTextCorpusDefinition,
    snapshot: RepositorySnapshot | None = None,
) -> RepositoryTextCorpus:
    """Realize exactly a definition's selected resources from observed state.

    Nonempty membership requires a snapshot of the definition's logical
    repository. Empty membership has no resource-state dependency and can be
    realized without a snapshot.

    :raises ValueError: If required observed state is missing, mismatched, or
        lacks exactly one selected occurrence per address.
    """
    if not definition.selected_addresses:
        resources: tuple[RepositoryResourceOccurrence, ...] = ()
    else:
        if snapshot is None:
            msg = "A nonempty repository text corpus requires an observed snapshot."
            raise ValueError(msg)
        if snapshot.repository_id != definition.discovery.repository_id:
            msg = "Repository text corpus snapshot does not match its definition."
            raise ValueError(msg)
        resources = tuple(
            _selected_resource(snapshot=snapshot, address=address)
            for address in definition.selected_addresses
        )

    return RepositoryTextCorpus(
        id=RepositoryTextCorpusId(
            _semantic_digest(
                RepositoryTextCorpus.REALIZATION_SEMANTICS,
                str(definition.discovery.repository_id),
                *(
                    value
                    for resource in resources
                    for value in (
                        str(resource.address),
                        str(resource.content_identity),
                    )
                ),
            ),
        ),
        definition=definition,
        resources=resources,
    )


def _selected_resource(
    *,
    snapshot: RepositorySnapshot,
    address: RepositoryResourceAddress,
) -> RepositoryResourceOccurrence:
    """Return the one selected occurrence or reject malformed observed state."""
    matches = tuple(
        resource for resource in snapshot.resources if resource.address == address
    )
    if not matches:
        msg = f"Repository text corpus snapshot lacks selected address: {address}."
        raise ValueError(msg)
    if len(matches) != 1:
        msg = f"Repository text corpus snapshot repeats selected address: {address}."
        raise ValueError(msg)
    return matches[0]


def _semantic_digest(semantics: str, *values: str) -> str:
    """Hash unambiguous length-framed corpus identity inputs."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big"))
        digest.update(encoded)
    return digest.hexdigest()
