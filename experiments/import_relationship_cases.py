# Copyright (c) 2026
"""Frozen manual cases for the import-relationship retrieval experiment.

This module declares repository-specific relevance judgments only.  It does not
resolve imports, expand candidates, retrieve documents, or rank resources.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from devtools.context.repository.resource import RepositoryResourceAddress


class ImportRelationshipDirection(StrEnum):
    """Name the directed relationship projection a later experiment may evaluate."""

    OUTGOING = "outgoing"
    INCOMING = "incoming"


@dataclass(frozen=True, slots=True)
class ImportRelationshipCase:
    """Retain one fixed manual judgment without retrieval-derived evidence."""

    name: str
    query_text: str
    lexical_seed_resource_address: RepositoryResourceAddress
    relevant_resource_addresses: tuple[RepositoryResourceAddress, ...]
    relevant_rationales: tuple[str, ...]
    direction: ImportRelationshipDirection
    negative_control_resource_addresses: tuple[RepositoryResourceAddress, ...] = ()
    negative_control_rationales: tuple[str, ...] = ()
    coverage_categories: frozenset[str] = frozenset()


_CASES = (
    ImportRelationshipCase(
        name="observation-resource-snapshot-flow",
        query_text=(
            "How does bounded repository observation turn selected resource "
            "addresses into the snapshot's observed text resource occurrences?"
        ),
        lexical_seed_resource_address=RepositoryResourceAddress(
            "src/devtools/context/repository/observation.py",
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/observation.py"),
            RepositoryResourceAddress("src/devtools/context/repository/resource.py"),
            RepositoryResourceAddress("src/devtools/context/repository/snapshot.py"),
        ),
        relevant_rationales=(
            "Owns bounded UTF-8 observation of the caller-selected addresses.",
            "Defines the observed resource occurrence and its address/content facts.",
            "Defines the snapshot that retains the resulting observed occurrences.",
        ),
        direction=ImportRelationshipDirection.OUTGOING,
        coverage_categories=frozenset({"outgoing-positive", "multi-resource"}),
    ),
    ImportRelationshipCase(
        name="filename-field-fusion",
        query_text=(
            "How does canonical repository retrieval combine content BM25 with "
            "separately derived filename-stem evidence?"
        ),
        lexical_seed_resource_address=RepositoryResourceAddress(
            "src/devtools/context/retrieval/lexical/bm25.py",
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/bm25.py",
            ),
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/filename.py",
            ),
        ),
        relevant_rationales=(
            (
                "Combines content and filename-field scores at the fixed production "
                "weight."
            ),
            "Builds and scores the separate filename-stem lexical field.",
        ),
        direction=ImportRelationshipDirection.OUTGOING,
        negative_control_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/analysis.py",
            ),
        ),
        negative_control_rationales=(
            (
                "Supplies shared lexical spans but does not define filename-field "
                "scoring or fusion."
            ),
        ),
        coverage_categories=frozenset({"outgoing-positive", "outgoing-negative"}),
    ),
    ImportRelationshipCase(
        name="resolution-becomes-relation",
        query_text=(
            "When does a qualified repository Python import resolution become a "
            "declaration-grounded resolved module-import relation?"
        ),
        lexical_seed_resource_address=RepositoryResourceAddress(
            "src/devtools/context/python/imports/resolution.py",
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/python/imports/resolution.py",
            ),
            RepositoryResourceAddress(
                "src/devtools/context/python/imports/relations.py",
            ),
        ),
        relevant_rationales=(
            (
                "Defines the qualified RESOLVED, unresolved, ambiguous, and "
                "unsupported outcomes."
            ),
            (
                "Creates a relation only from a RESOLVED outcome and one source "
                "interpretation."
            ),
        ),
        direction=ImportRelationshipDirection.INCOMING,
        negative_control_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/python/imports/__init__.py"),
        ),
        negative_control_rationales=(
            (
                "Re-exports the public import-intelligence surface but does not "
                "establish the relation-derivation conditions."
            ),
        ),
        coverage_categories=frozenset({"incoming-positive", "incoming-negative"}),
    ),
    ImportRelationshipCase(
        name="lexical-span-semantics-without-expansion",
        query_text=(
            "What Unicode word-span and casefold semantics define terms for "
            "repository lexical queries?"
        ),
        lexical_seed_resource_address=RepositoryResourceAddress(
            "src/devtools/context/retrieval/lexical/analysis.py",
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/analysis.py",
            ),
        ),
        relevant_rationales=(
            (
                "Defines the baseline Unicode span extraction and normalized-term "
                "observations."
            ),
        ),
        direction=ImportRelationshipDirection.INCOMING,
        negative_control_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/bm25.py",
            ),
        ),
        negative_control_rationales=(
            (
                "Imports the span helper for retrieval, but does not define the span "
                "and casefold semantics themselves."
            ),
        ),
        coverage_categories=frozenset(
            {"incoming-negative", "relationship-independent-control"},
        ),
    ),
    ImportRelationshipCase(
        name="public-relation-tests",
        query_text=(
            "Which tests guard the public Python import-intelligence interface "
            "for declaration-grounded resolved relations?"
        ),
        lexical_seed_resource_address=RepositoryResourceAddress(
            "src/devtools/context/python/imports/__init__.py",
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/python/imports/__init__.py"),
            RepositoryResourceAddress("tests/context/python/imports/test_relations.py"),
        ),
        relevant_rationales=(
            "Exports the public relation derivation and its qualified result types.",
            (
                "Exercises resolved, self-import, ambiguous, unsupported, and "
                "multiple-root relation behavior through that interface."
            ),
        ),
        direction=ImportRelationshipDirection.INCOMING,
        negative_control_resource_addresses=(
            RepositoryResourceAddress(
                "tests/context/python/imports/test_declarations.py",
            ),
        ),
        negative_control_rationales=(
            (
                "Imports the same public package but tests declaration syntax rather "
                "than resolved relation behavior."
            ),
        ),
        coverage_categories=frozenset({"incoming-positive", "test-source"}),
    ),
    ImportRelationshipCase(
        name="filesystem-tool-error-translation",
        query_text=(
            "How does the repository file-reading tool translate filesystem read "
            "failures into ToolInputError?"
        ),
        lexical_seed_resource_address=RepositoryResourceAddress(
            "src/devtools/tools/filesystem.py",
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/tools/filesystem.py"),
            RepositoryResourceAddress("src/devtools/resources/filesystem/__init__.py"),
        ),
        relevant_rationales=(
            (
                "Adapts bounded filesystem reads and their failures into the Tool "
                "boundary."
            ),
            (
                "Exposes the filesystem read operation and typed errors consumed by "
                "the Tool."
            ),
        ),
        direction=ImportRelationshipDirection.OUTGOING,
        negative_control_resource_addresses=(
            RepositoryResourceAddress("src/devtools/core/paths/__init__.py"),
        ),
        negative_control_rationales=(
            (
                "Supplies path normalization but does not define the filesystem-error "
                "to ToolInputError translation."
            ),
        ),
        coverage_categories=frozenset({"outgoing-positive", "cross-package-module"}),
    ),
    ImportRelationshipCase(
        name="relation-source-availability",
        query_text=(
            "How is source-module availability reported when import relation "
            "derivation has missing or ambiguous source interpretations?"
        ),
        lexical_seed_resource_address=RepositoryResourceAddress(
            "src/devtools/context/python/imports/relations.py",
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/python/imports/relations.py",
            ),
        ),
        relevant_rationales=(
            (
                "Defines the AVAILABLE, MISSING, and AMBIGUOUS source-status "
                "qualification."
            ),
        ),
        direction=ImportRelationshipDirection.OUTGOING,
        negative_control_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/python/imports/resolution.py",
            ),
        ),
        negative_control_rationales=(
            (
                "Provides the imported target-resolution outcome enum, not the "
                "distinct source-interpretation availability rule."
            ),
        ),
        coverage_categories=frozenset({"outgoing-negative"}),
    ),
)


def import_relationship_cases() -> tuple[ImportRelationshipCase, ...]:
    """Return the fixed manual judgments without retrieval-derived work."""
    return _CASES
