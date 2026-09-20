# Copyright (c) 2026
"""Bounded Context disclosure for exact-name Python function retrieval."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKind,
        PythonSourceOccurrence,
    )
    from devtools.context.python.function.retrieval import (
        PythonFunctionExactNameRelevanceEvidence,
        PythonFunctionExactNameRetrievalResult,
    )

_DISCLOSURE_IDENTITY_SEMANTICS = "python-function-exact-name-context-disclosure-v1"


@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationDisclosureItem:
    """Project established declaration knowledge into a disclosure form."""

    selected_match: PythonFunctionExactNameRelevanceEvidence
    declared_name: str
    declaration_kind: PythonFunctionDeclarationKind
    source_occurrence: PythonSourceOccurrence
    proposition: str

    REPRESENTATION: ClassVar[str] = (
        "python-function-declaration-knowledge-projection-v1"
    )


@dataclass(frozen=True, slots=True)
class PythonFunctionExactNameContextDisclosure:
    """Retain fixed all-match selection and its realized representations."""

    retrieval: PythonFunctionExactNameRetrievalResult
    selected_matches: tuple[PythonFunctionExactNameRelevanceEvidence, ...]
    items: tuple[PythonFunctionDeclarationDisclosureItem, ...]

    SELECTION: ClassVar[str] = "all-exact-name-matches-in-retrieval-order-v1"

    @property
    def identity(self) -> str:
        """Identify the bounded selection and representation deterministically."""
        return _semantic_digest(
            _DISCLOSURE_IDENTITY_SEMANTICS,
            self.SELECTION,
            PythonFunctionDeclarationDisclosureItem.REPRESENTATION,
            self.retrieval.query.declared_name,
            *(match.knowledge.identity for match in self.selected_matches),
        )


def disclose_python_function_exact_name_retrieval(
    retrieval: PythonFunctionExactNameRetrievalResult,
) -> PythonFunctionExactNameContextDisclosure:
    """Select every match and faithfully project its established knowledge."""
    selected_matches = retrieval.matches
    items = tuple(
        PythonFunctionDeclarationDisclosureItem(
            selected_match=match,
            declared_name=match.knowledge.declared_name,
            declaration_kind=match.knowledge.declaration_kind,
            source_occurrence=match.knowledge.support,
            proposition=match.knowledge.PROPOSITION,
        )
        for match in selected_matches
    )
    return PythonFunctionExactNameContextDisclosure(
        retrieval=retrieval,
        selected_matches=selected_matches,
        items=items,
    )


def _semantic_digest(semantics: str, *values: str) -> str:
    """Hash length-framed values for this bounded disclosure representation."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big"))
        digest.update(encoded)
    return digest.hexdigest()
