# Copyright (c) 2026
"""Tests for frozen import-relationship experiment case judgments."""

from pathlib import Path

import pytest

from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.core.paths import resolve_path
from experiments.import_relationship_cases import (
    ImportRelationshipDirection,
    import_relationship_cases,
)
from scripts.retrieval_bm25_baseline import select_benchmark_addresses

_EXPECTED_CASE_COUNT = 7
_REQUIRED_COVERAGE_CATEGORIES = frozenset(
    {
        "outgoing-positive",
        "outgoing-negative",
        "incoming-positive",
        "incoming-negative",
        "multi-resource",
        "test-source",
        "cross-package-module",
        "relationship-independent-control",
    },
)


def test_cases_are_fixed_complete_and_manually_aligned() -> None:
    """Frozen definitions retain complete, non-overlapping manual judgments."""
    cases = import_relationship_cases()

    assert len(cases) == _EXPECTED_CASE_COUNT
    assert len({case.name for case in cases}) == len(cases)
    assert {case.direction for case in cases} == {
        ImportRelationshipDirection.OUTGOING,
        ImportRelationshipDirection.INCOMING,
    }
    for case in cases:
        assert case.query_text.strip()
        assert case.lexical_seed_resource_address in case.relevant_resource_addresses
        assert len(case.relevant_resource_addresses) == len(
            set(case.relevant_resource_addresses),
        )
        assert len(case.relevant_rationales) == len(case.relevant_resource_addresses)
        assert all(rationale.strip() for rationale in case.relevant_rationales)
        assert len(case.negative_control_resource_addresses) == len(
            set(case.negative_control_resource_addresses),
        )
        assert len(case.negative_control_rationales) == len(
            case.negative_control_resource_addresses,
        )
        assert all(rationale.strip() for rationale in case.negative_control_rationales)
        assert not (
            set(case.relevant_resource_addresses)
            & set(case.negative_control_resource_addresses)
        )


def test_cases_belong_to_the_selected_real_repository_benchmark_corpus() -> None:
    """Every designated resource is eligible in the benchmark corpus state."""
    root = resolve_path(Path.cwd())
    discovery = discover_repository_resource_addresses(
        repository=Repository(
            RepositoryId.parse("d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"),
        ),
        root=root,
        maximum_resource_count=10_000,
        maximum_traversal_entry_count=20_000,
    )
    selected_addresses = set(select_benchmark_addresses(discovery=discovery))

    for case in import_relationship_cases():
        assert set(case.relevant_resource_addresses) <= selected_addresses
        assert set(case.negative_control_resource_addresses) <= selected_addresses


def test_cases_cover_required_categories() -> None:
    """The fixed set includes positive, negative, and control evidence pressure."""
    coverage = frozenset(
        category
        for case in import_relationship_cases()
        for category in case.coverage_categories
    )

    assert coverage >= _REQUIRED_COVERAGE_CATEGORIES


def test_loading_cases_performs_no_relation_expansion_or_retrieval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Case loading is declaration-only and cannot inspect later candidate evidence."""
    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Frozen case loading must not derive relationship candidates."
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.python.imports.relations.derive_python_resolved_module_import_relations",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        fail,
    )
    assert import_relationship_cases()
