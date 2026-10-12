# Copyright (c) 2026
# ruff: noqa: EM101, TRY003
"""Thin caller-literal adapter for the existing exact snapshot lookup."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True)
class ExactSeedResult:
    """Retain literal locators, native existing occurrences and explicit absence."""

    snapshot: RepositorySnapshot
    locators: tuple[RepositoryResourceAddress, ...]
    resources: tuple[RepositoryResourceOccurrence, ...]
    absent: tuple[RepositoryResourceAddress, ...]


def resolve_exact_seeds(
    snapshot: RepositorySnapshot,
    query: str,
    locators: tuple[RepositoryResourceAddress, ...],
) -> ExactSeedResult:
    """Resolve only frozen literal addresses; never extract or guess a hint."""
    unique = tuple(sorted(set(locators), key=str))
    if any(str(locator) not in query.split() for locator in unique):
        raise ValueError("Exact seed locator is not a frozen query literal")
    resources = []
    absent = []
    for locator in unique:
        try:
            resource = snapshot.resource_at(locator)
        except ValueError:
            absent.append(locator)
        else:
            resources.append(resource)
    return ExactSeedResult(snapshot, unique, tuple(resources), tuple(absent))
