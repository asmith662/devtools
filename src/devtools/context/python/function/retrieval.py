# Copyright (c) 2026
"""Exact-name retrieval over established Python declaration knowledge."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKnowledge,
    )
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshotId


@dataclass(frozen=True, slots=True)
class PythonFunctionExactNameQuery:
    """Express a bounded purpose to find one exact established declared name."""

    declared_name: str

    def __post_init__(self) -> None:
        """Reject an empty purpose, which cannot match a Python declaration."""
        if not self.declared_name:
            msg = "Exact declared-name query cannot be empty."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class PythonFunctionExactNameRelevanceEvidence:
    """Record one purpose-relative exact-name retrieval observation."""

    query: PythonFunctionExactNameQuery
    knowledge: PythonFunctionDeclarationKnowledge

    MECHANISM: ClassVar[str] = "python-function-declared-name-exact-equality-v1"
    NATIVE_OBSERVATION: ClassVar[str] = "exact-declared-name-match"


@dataclass(frozen=True, slots=True)
class PythonFunctionExactNameRetrievalResult:
    """Retain one query and its ordered purpose-relative match evidence."""

    query: PythonFunctionExactNameQuery
    matches: tuple[PythonFunctionExactNameRelevanceEvidence, ...]


@dataclass(frozen=True, slots=True)
class PythonFunctionExactNameSelectedResource:
    """Retain one selected resource and the exact matches supporting it."""

    snapshot_id: RepositorySnapshotId
    resource_address: RepositoryResourceAddress
    supporting_matches: tuple[PythonFunctionExactNameRelevanceEvidence, ...]


@dataclass(frozen=True, slots=True)
class PythonFunctionExactNameResourceSelection:
    """Project distinct matching resources from one exact-name retrieval."""

    retrieval: PythonFunctionExactNameRetrievalResult
    selected_resources: tuple[PythonFunctionExactNameSelectedResource, ...]

    @property
    def resource_addresses(self) -> tuple[RepositoryResourceAddress, ...]:
        """Expose selected addresses in first retrieval-match order."""
        return tuple(selected.resource_address for selected in self.selected_resources)


def retrieve_python_functions_by_exact_name(
    *,
    declarations: Sequence[PythonFunctionDeclarationKnowledge],
    query: PythonFunctionExactNameQuery,
) -> PythonFunctionExactNameRetrievalResult:
    """Return exact declared-name matches in the supplied knowledge order.

    A result with no matches is a successful bounded retrieval over only the
    supplied declaration knowledge. It makes no repository-wide absence claim.
    """
    matches = tuple(
        PythonFunctionExactNameRelevanceEvidence(
            query=query,
            knowledge=knowledge,
        )
        for knowledge in declarations
        if knowledge.declared_name == query.declared_name
    )
    return PythonFunctionExactNameRetrievalResult(query=query, matches=matches)


def select_python_function_resources_from_exact_name_retrieval(
    retrieval: PythonFunctionExactNameRetrievalResult,
) -> PythonFunctionExactNameResourceSelection:
    """Select distinct resources supported by an existing retrieval result.

    Resources retain first-match order. Every original declaration-level match
    remains available as support, including multiple matches in one resource.
    A zero-match retrieval produces a successful zero-resource selection.
    """
    support_by_resource: dict[
        tuple[RepositorySnapshotId, RepositoryResourceAddress],
        list[PythonFunctionExactNameRelevanceEvidence],
    ] = {}
    for match in retrieval.matches:
        occurrence = match.knowledge.support
        key = (occurrence.snapshot_id, occurrence.resource_address)
        support_by_resource.setdefault(key, []).append(match)

    selected_resources = tuple(
        PythonFunctionExactNameSelectedResource(
            snapshot_id=snapshot_id,
            resource_address=resource_address,
            supporting_matches=tuple(supporting_matches),
        )
        for (snapshot_id, resource_address), supporting_matches in (
            support_by_resource.items()
        )
    )
    return PythonFunctionExactNameResourceSelection(
        retrieval=retrieval,
        selected_resources=selected_resources,
    )
