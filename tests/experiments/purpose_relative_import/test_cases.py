# Copyright (c) 2026
# ruff: noqa: D103, E501, EM101, PLR2004, TRY003
"""Anti-leakage and integrity tests for frozen purpose-relative needs."""

from pathlib import Path

import pytest

from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.core.paths import resolve_path
from experiments.purpose_relative_import.cases import (
    UsefulnessJudgment,
    purpose_relative_needs,
)
from scripts.retrieval_bm25_baseline import select_benchmark_addresses


def test_needs_are_complete_explicit_and_preserve_paired_query_distinction() -> None:
    needs = purpose_relative_needs()

    assert len(needs) == 12
    assert len({need.name for need in needs}) == 12
    for need in needs:
        assert need.information_need.strip()
        assert need.query_text.strip()
        assert need.judgments
        assert len({item.address for item in need.judgments}) == len(need.judgments)
        assert all(item.rationale.strip() for item in need.judgments)
        assert any(item.judgment is UsefulnessJudgment.USEFUL for item in need.judgments)
        assert not any(item.judgment is UsefulnessJudgment.UNJUDGED for item in need.judgments)
        assert all(
            item.judgment is UsefulnessJudgment.NOT_USEFUL
            for item in need.judgments
            if item.is_control
        )
    architecture, implementation = needs[-2:]
    assert architecture.query_text == implementation.query_text
    assert architecture.information_need != implementation.information_need
    assert {
        item.address for item in architecture.judgments if item.judgment is UsefulnessJudgment.USEFUL
    }.isdisjoint(
        item.address for item in implementation.judgments if item.judgment is UsefulnessJudgment.USEFUL
    )


def test_judged_addresses_are_in_the_selected_benchmark_corpus() -> None:
    root = resolve_path(Path.cwd())
    discovery = discover_repository_resource_addresses(
        repository=Repository(RepositoryId.parse("d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8")),
        root=root,
        maximum_resource_count=10_000,
        maximum_traversal_entry_count=20_000,
    )
    selected = set(select_benchmark_addresses(discovery=discovery))
    for need in purpose_relative_needs():
        assert {item.address for item in need.judgments} <= selected


def test_loading_needs_performs_no_retrieval_expansion_or_oracle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("Frozen needs must not compute experimental outcomes.")

    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        fail,
    )
    monkeypatch.setattr(
        "experiments.import_relationship.comparison.expand_candidates",
        fail,
    )
    assert purpose_relative_needs()
