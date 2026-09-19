# Copyright (c) 2026
"""Exact-name retrieval over established Python declaration knowledge."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python_declarations import (
        PythonFunctionDeclarationKnowledge,
    )


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
