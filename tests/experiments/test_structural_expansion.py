# Copyright (c) 2026
"""Tests for the bounded experiment-local address structural arithmetic."""

from pathlib import Path

import pytest

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.structural_expansion import (
    directory_distance,
    expand_addresses,
    shared_directory_depth,
    structural_expansion_cases,
)
from scripts.retrieval_bm25_baseline import run_benchmark

_GENERIC_ANCESTOR_DEPTH = 2
_GENERIC_ANCESTOR_DISTANCE = 5
_EXPECTED_STRUCTURAL_CASE_COUNT = 6
_REQUIRED_RELATIONSHIP_CATEGORIES = frozenset(
    {
        "implementation-siblings",
        "implementation-test",
        "nearby-test-control",
        "documentation-implementation",
        "false-proximity",
        "multiple-seeds",
    },
)


def _address(value: str) -> RepositoryResourceAddress:
    return RepositoryResourceAddress(value)


def _candidates(
    *,
    addresses: tuple[RepositoryResourceAddress, ...],
    seeds: tuple[RepositoryResourceAddress, ...],
    strategy: str,
    maximum_candidates_per_seed: int = 3,
) -> tuple[RepositoryResourceAddress, ...]:
    return tuple(
        group[0].candidate
        for group in expand_addresses(
            addresses=addresses,
            seeds=seeds,
            maximum_candidates_per_seed=maximum_candidates_per_seed,
            strategy=strategy,
        )
    )


def test_address_arithmetic_excludes_filenames_and_bounds_expansion() -> None:
    """Address arithmetic excludes names and expansion respects its bounds."""
    seed = _address("src/context/lexical/index.py")
    same = _address("src/context/lexical/statistics.py")
    nested = _address("src/context/other.py")
    distant = _address("docs/architecture.md")

    assert shared_directory_depth(seed, same) == len(("src", "context", "lexical"))
    assert directory_distance(seed, same) == 0
    assert shared_directory_depth(seed, nested) == len(("src", "context"))
    assert directory_distance(seed, nested) == 1
    assert directory_distance(seed, distant) > 1
    same_parent = expand_addresses(
        addresses=(seed, same, nested, distant),
        seeds=(seed,),
        maximum_candidates_per_seed=1,
        strategy="same-parent",
    )
    distance = expand_addresses(
        addresses=(seed, same, nested, distant),
        seeds=(seed,),
        maximum_candidates_per_seed=2,
        strategy="distance",
    )

    assert same_parent[0][0].candidate == same
    assert distance[0][0].candidate == same
    assert distance[1][0].candidate == nested
    with pytest.raises(ValueError, match="positive"):
        expand_addresses(
            addresses=(seed,),
            seeds=(),
            maximum_candidates_per_seed=0,
            strategy="distance",
        )
    with pytest.raises(ValueError, match="strategy"):
        expand_addresses(
            addresses=(seed,),
            seeds=(),
            maximum_candidates_per_seed=1,
            strategy="package",
        )


def test_same_directory_fixture_expands_a_related_sibling() -> None:
    """A same-directory sibling is available as a bounded structural candidate."""
    seed = _address("src/catalog/query.py")
    related = _address("src/catalog/filters.py")

    assert _candidates(
        addresses=(seed, related),
        seeds=(seed,),
        strategy="same-parent",
    ) == (related,)


def test_same_directory_fixture_also_expands_an_unrelated_sibling() -> None:
    """Same-directory placement alone does not establish a useful relationship."""
    seed = _address("src/catalog/query.py")
    unrelated = _address("src/catalog/release_notes.py")

    assert _candidates(
        addresses=(seed, unrelated),
        seeds=(seed,),
        strategy="same-parent",
    ) == (unrelated,)


def test_nested_directory_fixture_expands_a_related_ancestor_sibling() -> None:
    """Distance expansion can reach a useful file in an enclosing directory."""
    seed = _address("src/catalog/parsing/query.py")
    related = _address("src/catalog/schema.py")

    assert _candidates(
        addresses=(seed, related),
        seeds=(seed,),
        strategy="distance",
    ) == (related,)


def test_generic_ancestor_fixture_exposes_a_distant_unrelated_candidate() -> None:
    """A generic shared ancestor remains expansion evidence without suppression."""
    seed = _address("src/devtools/context/retrieval/lexical/bm25.py")
    unrelated = _address("src/devtools/models/lexical/adapter.py")

    candidates = _candidates(
        addresses=(seed, unrelated),
        seeds=(seed,),
        strategy="distance",
    )

    assert candidates == (unrelated,)
    assert shared_directory_depth(seed, unrelated) == _GENERIC_ANCESTOR_DEPTH
    assert directory_distance(seed, unrelated) == _GENERIC_ANCESTOR_DISTANCE


def test_source_fixture_expands_both_related_source_and_nearby_test() -> None:
    """Structural expansion treats nearby source and test files alike."""
    seed = _address("src/catalog/query.py")
    related_source = _address("src/catalog/filters.py")
    nearby_test = _address("src/catalog/test_query.py")

    assert _candidates(
        addresses=(seed, related_source, nearby_test),
        seeds=(seed,),
        strategy="same-parent",
    ) == (related_source, nearby_test)


def test_test_fixture_expands_a_related_test_sibling() -> None:
    """A useful relationship can also occur wholly within a test directory."""
    seed = _address("tests/catalog/test_query.py")
    related_test = _address("tests/catalog/test_filters.py")

    assert _candidates(
        addresses=(seed, related_test),
        seeds=(seed,),
        strategy="same-parent",
    ) == (related_test,)


def test_documentation_code_colocation_fixture_expands_related_code() -> None:
    """A colocated documentation and code pair can be structurally connected."""
    documentation = _address("docs/catalog/query.md")
    related_code = _address("docs/catalog/query_example.py")

    assert _candidates(
        addresses=(documentation, related_code),
        seeds=(documentation,),
        strategy="same-parent",
    ) == (related_code,)


def test_documentation_code_colocation_fixture_also_expands_unrelated_code() -> None:
    """Documentation/code colocation alone does not establish a useful relationship."""
    documentation = _address("docs/catalog/query.md")
    unrelated_code = _address("docs/catalog/release_tool.py")

    assert _candidates(
        addresses=(documentation, unrelated_code),
        seeds=(documentation,),
        strategy="same-parent",
    ) == (unrelated_code,)


def test_three_seeds_expose_a_related_candidate_missed_by_one_seed() -> None:
    """Later lexical seeds can expose a useful structural candidate."""
    first_seed = _address("src/query/lexical.py")
    first_seed_neighbor = _address("src/query/formatting.py")
    second_seed = _address("src/schema/lexical.py")
    related = _address("src/schema/validation.py")
    third_seed = _address("src/other/lexical.py")
    third_seed_neighbor = _address("src/other/maintenance.py")
    addresses = (
        first_seed,
        first_seed_neighbor,
        second_seed,
        related,
        third_seed,
        third_seed_neighbor,
    )

    one_seed = _candidates(
        addresses=addresses,
        seeds=(first_seed,),
        strategy="same-parent",
        maximum_candidates_per_seed=1,
    )
    three_seeds = _candidates(
        addresses=addresses,
        seeds=(first_seed, second_seed, third_seed),
        strategy="same-parent",
        maximum_candidates_per_seed=1,
    )

    assert related not in one_seed
    assert related in three_seeds


def test_three_seeds_also_add_additional_unrelated_candidates() -> None:
    """Increasing the lexical seed count increases unrelated expansion exposure."""
    first_seed = _address("src/query/lexical.py")
    first_seed_neighbor = _address("src/query/formatting.py")
    second_seed = _address("src/schema/lexical.py")
    second_seed_neighbor = _address("src/schema/migration.py")
    third_seed = _address("src/other/lexical.py")
    third_seed_neighbor = _address("src/other/maintenance.py")
    addresses = (
        first_seed,
        first_seed_neighbor,
        second_seed,
        second_seed_neighbor,
        third_seed,
        third_seed_neighbor,
    )

    one_seed = _candidates(
        addresses=addresses,
        seeds=(first_seed,),
        strategy="same-parent",
        maximum_candidates_per_seed=1,
    )
    three_seeds = _candidates(
        addresses=addresses,
        seeds=(first_seed, second_seed, third_seed),
        strategy="same-parent",
        maximum_candidates_per_seed=1,
    )

    assert one_seed == (first_seed_neighbor,)
    assert three_seeds == (
        first_seed_neighbor,
        second_seed_neighbor,
        third_seed_neighbor,
    )


def test_structural_cases_are_complete_manual_repository_judgments() -> None:
    """Fixed cases retain explicit, distinct addresses and matching rationales."""
    cases = structural_expansion_cases()

    assert len(cases) == _EXPECTED_STRUCTURAL_CASE_COUNT
    assert len({case.name for case in cases}) == len(cases)
    assert all(case.query_text for case in cases)
    assert all(case.relevant_resource_addresses for case in cases)
    assert all(
        len(set(case.relevant_resource_addresses))
        == len(case.relevant_resource_addresses)
        for case in cases
    )
    assert all(
        len(case.relevant_rationales) == len(case.relevant_resource_addresses)
        for case in cases
    )
    assert all(
        all(rationale for rationale in case.relevant_rationales) for case in cases
    )
    assert all(
        len(case.negative_control_rationales)
        == len(case.negative_control_resource_addresses)
        for case in cases
    )
    assert all(
        all(rationale for rationale in case.negative_control_rationales)
        for case in cases
    )
    assert all(
        not set(case.relevant_resource_addresses).intersection(
            case.negative_control_resource_addresses,
        )
        for case in cases
    )


def test_structural_case_addresses_are_in_the_benchmark_corpus_selection() -> None:
    """Manual judgments name only resources available to the benchmark corpus."""
    benchmark = run_benchmark(repository_root=Path.cwd())
    selected = set(benchmark.definition.selected_addresses)

    assert all(
        address in selected
        for case in structural_expansion_cases()
        for address in (
            *case.relevant_resource_addresses,
            *case.negative_control_resource_addresses,
        )
    )


def test_structural_cases_cover_the_required_relationship_categories() -> None:
    """The fixed set includes positive and falsification relationship situations."""
    categories = frozenset().union(
        *(case.relationship_categories for case in structural_expansion_cases()),
    )

    assert categories == _REQUIRED_RELATIONSHIP_CATEGORIES


def test_structural_case_construction_performs_no_ranking_or_inference(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Case construction returns fixed judgments without examining retrieval state."""

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Structural case construction must not invoke ranking or retrieval."
        raise AssertionError(msg)

    monkeypatch.setattr("experiments.structural_expansion.expand_addresses", fail)
    monkeypatch.setattr("experiments.structural_expansion.run_benchmark", fail)

    assert structural_expansion_cases() == structural_expansion_cases()
