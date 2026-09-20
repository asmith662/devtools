# Copyright (c) 2026
"""Explicit membership intent grounded in one completed repository discovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.discovery import RepositoryResourceDiscovery
    from devtools.context.repository.resource import RepositoryResourceAddress


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
