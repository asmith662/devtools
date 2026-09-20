# Copyright (c) 2026
"""Pre-analysis Python function resource candidates from observed source.

This bounded selector filters an explicit caller-ordered set of already
observed resources. A positive result means only that the requested exact name
occurred as a stdlib-tokenizer ``NAME`` token; declaration analysis remains a
separate AST-owned operation.
"""

from __future__ import annotations

import tokenize
from dataclasses import dataclass
from io import StringIO
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.function.retrieval import (
        PythonFunctionExactNameQuery,
    )
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


class PythonFunctionCandidateTokenizationError(Exception):
    """Report a required eligible resource that could not be tokenized."""

    snapshot_id: RepositorySnapshotId
    resource_address: RepositoryResourceAddress
    tokenizer_message: str

    def __init__(
        self,
        *,
        snapshot_id: RepositorySnapshotId,
        resource_address: RepositoryResourceAddress,
        error: tokenize.TokenError | IndentationError,
    ) -> None:
        """Capture the failed resource and narrow tokenizer diagnostic."""
        self.snapshot_id = snapshot_id
        self.resource_address = resource_address
        self.tokenizer_message = str(error)
        message = (
            "Could not tokenize observed Python candidate resource "
            f"{resource_address}: {error}"
        )
        super().__init__(message)


@dataclass(frozen=True, slots=True)
class PythonFunctionNameTokenCandidateEvidence:
    """Record one exact ``NAME`` token observation within one resource."""

    token_index: int
    token_string: str

    MECHANISM: ClassVar[str] = "stdlib-generate-tokens-name-exact-equality-v1"
    NATIVE_OBSERVATION: ClassVar[str] = "exact-python-name-token-match"


@dataclass(frozen=True, slots=True)
class PythonFunctionAnalysisCandidateResource:
    """Retain one selected observed resource and all supporting token matches."""

    resource: RepositoryResourceOccurrence
    supporting_matches: tuple[PythonFunctionNameTokenCandidateEvidence, ...]


@dataclass(frozen=True, slots=True)
class PythonFunctionAnalysisCandidateSelection:
    """Retain one bounded pre-analysis candidate-selection result."""

    snapshot_id: RepositorySnapshotId
    query: PythonFunctionExactNameQuery
    eligible_resources: tuple[RepositoryResourceOccurrence, ...]
    candidates: tuple[PythonFunctionAnalysisCandidateResource, ...]

    @property
    def eligible_resource_addresses(self) -> tuple[RepositoryResourceAddress, ...]:
        """Expose every considered resource in caller-supplied order."""
        return tuple(resource.address for resource in self.eligible_resources)

    @property
    def candidate_resource_addresses(self) -> tuple[RepositoryResourceAddress, ...]:
        """Expose selected candidates in caller-supplied eligible order."""
        return tuple(candidate.resource.address for candidate in self.candidates)


def select_python_function_analysis_candidates(
    snapshot: RepositorySnapshot,
    *,
    query: PythonFunctionExactNameQuery,
    resource_addresses: Sequence[RepositoryResourceAddress],
) -> PythonFunctionAnalysisCandidateSelection:
    """Select resources containing an exact matching Python ``NAME`` token.

    Every eligible address is validated against ``snapshot`` before any source
    is tokenized. Tokenization consumes only retained decoded text. Candidate
    order follows caller-supplied eligible order; multiple matching tokens
    select one resource while all token observations remain available.
    """
    eligible_addresses = tuple(resource_addresses)
    if not eligible_addresses:
        msg = "Python function candidate selection requires at least one resource."
        raise ValueError(msg)
    if len(set(eligible_addresses)) != len(eligible_addresses):
        msg = "Python function candidate resource addresses must be distinct."
        raise ValueError(msg)

    eligible_resources = tuple(
        snapshot.resource_at(address) for address in eligible_addresses
    )
    candidates: list[PythonFunctionAnalysisCandidateResource] = []
    for resource in eligible_resources:
        try:
            supporting_matches = tuple(
                PythonFunctionNameTokenCandidateEvidence(
                    token_index=token_index,
                    token_string=token_info.string,
                )
                for token_index, token_info in enumerate(
                    tokenize.generate_tokens(StringIO(resource.content).readline),
                )
                if token_info.type == tokenize.NAME
                and token_info.string == query.declared_name
            )
        except (tokenize.TokenError, IndentationError) as error:
            raise PythonFunctionCandidateTokenizationError(
                snapshot_id=snapshot.id,
                resource_address=resource.address,
                error=error,
            ) from error
        if supporting_matches:
            candidates.append(
                PythonFunctionAnalysisCandidateResource(
                    resource=resource,
                    supporting_matches=supporting_matches,
                ),
            )

    return PythonFunctionAnalysisCandidateSelection(
        snapshot_id=snapshot.id,
        query=query,
        eligible_resources=eligible_resources,
        candidates=tuple(candidates),
    )
