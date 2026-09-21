# Copyright (c) 2026
# ruff: noqa: E501, S101
# mypy: disable-error-code="arg-type,attr-defined,call-overload,misc,operator,unused-ignore,var-annotated"
"""Bounded lexical-seed repository-address structural expansion experiment."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from scripts.retrieval_bm25_baseline import run_benchmark

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class StructuralEvidence:
    """Explain one candidate's syntactic address relationship to one seed."""

    seed: RepositoryResourceAddress
    candidate: RepositoryResourceAddress
    seed_rank: int
    same_parent: bool
    shared_directory_depth: int
    directory_distance: int
    strategy: str


@dataclass(frozen=True, slots=True)
class StructuralExpansionCase:
    """Retain one fixed manual judgment for structural-expansion evaluation."""

    name: str
    query_text: str
    relevant_resource_addresses: tuple[RepositoryResourceAddress, ...]
    relevant_rationales: tuple[str, ...]
    negative_control_resource_addresses: tuple[RepositoryResourceAddress, ...] = ()
    negative_control_rationales: tuple[str, ...] = ()
    relationship_categories: frozenset[str] = frozenset()


_STRUCTURAL_EXPANSION_CASES = (
    StructuralExpansionCase(
        name="corpus-document-representation",
        query_text="selected observed corpus whole resource document representation",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/corpus.py"),
            RepositoryResourceAddress("src/devtools/context/repository/document.py"),
        ),
        relevant_rationales=(
            "Defines selected observed corpus membership and realization.",
            "Represents each realized corpus member as one whole-resource document.",
        ),
        negative_control_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/resource.py"),
        ),
        negative_control_rationales=(
            (
                "Defines shared resource values but not corpus realization or "
                "document representation."
            ),
        ),
        relationship_categories=frozenset({"implementation-siblings"}),
    ),
    StructuralExpansionCase(
        name="filename-bm25-fusion",
        query_text="combined content filename stem BM25 score contributions",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/retrieval/lexical/bm25.py"),
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/filename.py",
            ),
        ),
        relevant_rationales=(
            "Combines content and independently scored filename-stem BM25 evidence.",
            "Builds and scores the independent filename-stem lexical field.",
        ),
        negative_control_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/evaluation.py",
            ),
        ),
        negative_control_rationales=(
            (
                "Evaluates retained retrieval results but does not score or fuse "
                "filename evidence."
            ),
        ),
        relationship_categories=frozenset(
            {"implementation-siblings", "false-proximity"},
        ),
    ),
    StructuralExpansionCase(
        name="corpus-definition-validation-test",
        query_text="reject duplicate selected repository text corpus addresses",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/corpus.py"),
            RepositoryResourceAddress("tests/context/repository/test_corpus.py"),
        ),
        relevant_rationales=(
            "Rejects duplicate selected addresses when defining a corpus.",
            (
                "Exercises corpus-definition validation, including duplicate-address "
                "rejection."
            ),
        ),
        relationship_categories=frozenset({"implementation-test"}),
    ),
    StructuralExpansionCase(
        name="whole-resource-document-identity",
        query_text=(
            "whole resource document identity address content representation "
            "semantics"
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/document.py"),
        ),
        relevant_rationales=(
            (
                "Defines whole-resource document identity from repository, address, "
                "content, and representation semantics."
            ),
        ),
        negative_control_resource_addresses=(
            RepositoryResourceAddress("tests/context/repository/test_document.py"),
        ),
        negative_control_rationales=(
            "Verifies behavior but falls outside this implementation-focused need.",
        ),
        relationship_categories=frozenset({"nearby-test-control"}),
    ),
    StructuralExpansionCase(
        name="architecture-corpus-membership",
        query_text=(
            "repository text corpus membership boundary current architecture "
            "implementation"
        ),
        relevant_resource_addresses=(
            RepositoryResourceAddress("docs/architecture.md"),
            RepositoryResourceAddress("src/devtools/context/repository/corpus.py"),
        ),
        relevant_rationales=(
            (
                "States the architecture boundary for corpus definition, observation, "
                "and corpus realization."
            ),
            "Implements the defined corpus membership and realization boundary.",
        ),
        negative_control_resource_addresses=(
            RepositoryResourceAddress("docs/roadmap.md"),
        ),
        negative_control_rationales=(
            (
                "Shares the documentation directory but does not define the current "
                "corpus boundary."
            ),
        ),
        relationship_categories=frozenset(
            {"documentation-implementation", "false-proximity"},
        ),
    ),
    StructuralExpansionCase(
        name="discovery-observation-corpus-flow",
        query_text="discover selected observe repository text corpus pipeline",
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/repository/discovery.py",
            ),
            RepositoryResourceAddress(
                "src/devtools/context/repository/observation.py",
            ),
            RepositoryResourceAddress("src/devtools/context/repository/corpus.py"),
        ),
        relevant_rationales=(
            "Discovers bounded repository resource addresses without reading content.",
            "Observes explicitly addressed UTF-8 repository resources.",
            "Defines selection and realizes the observed resources as a text corpus.",
        ),
        relationship_categories=frozenset(
            {"implementation-siblings", "multiple-seeds"},
        ),
    ),
)


def structural_expansion_cases() -> tuple[StructuralExpansionCase, ...]:
    """Return the fixed manual cases without retrieval, ranking, or inference."""
    return _STRUCTURAL_EXPANSION_CASES


def directory_parts(address: RepositoryResourceAddress) -> tuple[str, ...]:
    """Return address components excluding the final filename component."""
    return address.parts[:-1]


def shared_directory_depth(
    first: RepositoryResourceAddress,
    second: RepositoryResourceAddress,
) -> int:
    """Return the longest shared prefix length of two directory component tuples."""
    depth = 0
    for left, right in zip(
        directory_parts(first),
        directory_parts(second),
        strict=False,
    ):
        if left != right:
            break
        depth += 1
    return depth


def directory_distance(
    first: RepositoryResourceAddress,
    second: RepositoryResourceAddress,
) -> int:
    """Return tree-edge distance between two address parent directories."""
    shared = shared_directory_depth(first, second)
    return len(directory_parts(first)) + len(directory_parts(second)) - 2 * shared


def expand_addresses(
    *,
    addresses: tuple[RepositoryResourceAddress, ...],
    seeds: tuple[RepositoryResourceAddress, ...],
    maximum_candidates_per_seed: int,
    strategy: str,
) -> tuple[tuple[StructuralEvidence, ...], ...]:
    """Expand canonical seeds over one retained corpus address universe only."""
    if maximum_candidates_per_seed <= 0:
        msg = "Maximum structural candidates per seed must be positive."
        raise ValueError(msg)
    if strategy not in {"same-parent", "distance"}:
        msg = "Structural strategy must be same-parent or distance."
        raise ValueError(msg)
    positions = {address: position for position, address in enumerate(addresses)}
    evidence: dict[RepositoryResourceAddress, list[StructuralEvidence]] = {}
    for seed_rank, seed in enumerate(seeds, start=1):
        candidates = [address for address in addresses if address != seed]
        if strategy == "same-parent":
            candidates = [
                address
                for address in candidates
                if directory_parts(address) == directory_parts(seed)
            ]
        candidates.sort(
            key=lambda address: (
                directory_distance(seed, address),
                -shared_directory_depth(seed, address),
                positions[address],
            ),
        )
        for candidate in candidates[:maximum_candidates_per_seed]:
            evidence.setdefault(candidate, []).append(
                StructuralEvidence(
                    seed=seed,
                    candidate=candidate,
                    seed_rank=seed_rank,
                    same_parent=directory_parts(seed) == directory_parts(candidate),
                    shared_directory_depth=shared_directory_depth(seed, candidate),
                    directory_distance=directory_distance(seed, candidate),
                    strategy=strategy,
                ),
            )
    return tuple(
        tuple(items)
        for _candidate, items in sorted(
            evidence.items(),
            key=lambda item: (
                min(evidence.seed_rank for evidence in item[1]),
                min(evidence.directory_distance for evidence in item[1]),
                positions[item[0]],
            ),
        )
    )


_K = 5
_CANDIDATE_BOUND = 3


def run_comparison(*, repository_root: Path) -> dict[str, object]:
    """Run one paired canonical-lexical and structural-expansion comparison."""
    benchmark = run_benchmark(repository_root=repository_root)
    addresses = tuple(item.resource.address for item in benchmark.documents.documents)
    original_cases = tuple(
        StructuralExpansionCase(
            name=case.name,
            query_text=case.query_text,
            relevant_resource_addresses=case.relevant_resource_addresses,
            relevant_rationales=(case.description,) * len(case.relevant_resource_addresses),
        )
        for case in benchmark.cases
    )
    case_sets = {
        "original": original_cases,
        "structural": structural_expansion_cases(),
        "combined": (*original_cases, *structural_expansion_cases()),
    }
    lexical_cases = tuple(
        _lexical_case(case=case, index=benchmark.index) for case in case_sets["combined"]
    )
    lexical_payload = [_case_payload(item) for item in lexical_cases]
    variants: dict[str, object] = {}
    for strategy in ("same-parent", "distance"):
        for seed_count in (1, 3):
            variant_cases = tuple(
                _variant_case(
                    lexical=item,
                    addresses=addresses,
                    strategy=strategy,
                    seed_count=seed_count,
                )
                for item in lexical_cases
            )
            variants[f"{strategy}-seed-{seed_count}"] = {
                "strategy": strategy,
                "seed_count": seed_count,
                "cases": [_case_payload(item) for item in variant_cases],
                "metrics": _all_metrics(variant_cases, case_sets),
            }
    return {
        "schema": "devtools-structural-expansion-v2",
        "semantics": "experiment-only bounded lexical-seed address expansion",
        "reproducibility": {
            "snapshot_id": str(benchmark.snapshot.id),
            "corpus_id": str(benchmark.corpus.id),
            "document_count": len(benchmark.documents.documents),
            "bounds": {
                "maximum_discovered_resources": 10_000,
                "maximum_traversal_entries": 20_000,
                "maximum_resource_bytes": 1_048_576,
            },
        },
        "lexical_configuration": {"canonical": "content-bm25 + 0.25 filename-stem-bm25", "k": _K},
        "structural_configuration": {"seed_counts": [1, 3], "candidate_bound_per_seed": _CANDIDATE_BOUND, "arithmetic": "filename-excluded parent-directory tree distance"},
        "original_cases": [_frozen_case(case) for case in original_cases],
        "structural_cases": [_frozen_case(case) for case in structural_expansion_cases()],
        "lexical_baseline": {"cases": lexical_payload, "metrics": _all_metrics(lexical_cases, case_sets)},
        "variants": variants,
    }


def _lexical_case(*, case: StructuralExpansionCase, index: object) -> dict[str, object]:
    query = analyze_repository_text_lexical_query(text=case.query_text)
    result = retrieve_repository_text_documents_by_bm25(query=query, index=index, maximum_results=_K)  # type: ignore[arg-type]
    lexical = tuple(match.document_statistics.analysis.document.resource.address for match in result.matches)
    return {"case": case, "lexical": lexical, "lexical_scores": [match.score for match in result.matches]}


def _variant_case(*, lexical: dict[str, object], addresses: tuple[RepositoryResourceAddress, ...], strategy: str, seed_count: int) -> dict[str, object]:
    ranked = lexical["lexical"]
    assert isinstance(ranked, tuple)
    seeds = ranked[:seed_count]
    groups = expand_addresses(addresses=addresses, seeds=seeds, maximum_candidates_per_seed=_CANDIDATE_BOUND, strategy=strategy)  # type: ignore[arg-type]
    additions = tuple(group[0].candidate for group in groups if group[0].candidate not in ranked)
    fixed = tuple(dict.fromkeys((*ranked[:1], *additions, *ranked)))[:_K]
    return {**lexical, "seeds": seeds, "groups": groups, "additions": additions, "fixed": fixed}


def _case_payload(item: dict[str, object]) -> dict[str, object]:
    case = item["case"]
    assert isinstance(case, StructuralExpansionCase)
    lexical = item["lexical"]
    assert isinstance(lexical, tuple)
    relevant = case.relevant_resource_addresses
    controls = case.negative_control_resource_addresses
    additions = item.get("additions", ())
    fixed = item.get("fixed", lexical)
    groups = item.get("groups", ())
    assert isinstance(additions, tuple)
    assert isinstance(fixed, tuple)
    return {
        "name": case.name, "query": case.query_text,
        "relevant": [str(value) for value in relevant], "relevant_rationales": list(case.relevant_rationales),
        "controls": [str(value) for value in controls], "control_rationales": list(case.negative_control_rationales),
        "relationship_categories": sorted(case.relationship_categories),
        "lexical": [str(value) for value in lexical], "lexical_scores": item["lexical_scores"],
        "seeds": [str(value) for value in item.get("seeds", ())],
        "structural_candidates": [[_evidence(value) for value in group] for group in groups],
        "augmentation": [str(value) for value in (*lexical, *additions)],
        "augmentation_candidate_count": len(additions),
        "augmentation_recovered": [str(value) for value in relevant if value in additions],
        "augmentation_controls": [str(value) for value in controls if value in additions],
        "fixed_k": [str(value) for value in fixed],
        "fixed_k_recovered": [str(value) for value in relevant if value in fixed and value not in lexical],
        "relevant_losses": [str(value) for value in relevant if value in lexical and value not in fixed],
        "controls_in_fixed_k": [str(value) for value in controls if value in fixed and value not in lexical],
        "displacements": [
            {"lexical": str(old), "fixed_k": str(new)}
            for old, new in zip(lexical, fixed, strict=False) if old != new
        ],
    }


def _evidence(value: StructuralEvidence) -> dict[str, object]:
    return {"candidate": str(value.candidate), "seed": str(value.seed), "seed_rank": value.seed_rank, "relationship_kind": value.strategy, "same_parent": value.same_parent, "shared_directory_depth": value.shared_directory_depth, "directory_distance": value.directory_distance}


def _frozen_case(case: StructuralExpansionCase) -> dict[str, object]:
    return {"name": case.name, "query": case.query_text, "relevant": [str(value) for value in case.relevant_resource_addresses], "relevant_rationales": list(case.relevant_rationales), "controls": [str(value) for value in case.negative_control_resource_addresses], "control_rationales": list(case.negative_control_rationales), "relationship_categories": sorted(case.relationship_categories)}


def _all_metrics(items: tuple[dict[str, object], ...], case_sets: dict[str, tuple[StructuralExpansionCase, ...]]) -> dict[str, object]:
    payload: dict[str, object] = {}
    for name, cases in case_sets.items():
        selected = tuple(item for item in items if item["case"] in cases)
        payload[name] = _metrics(selected)
    return payload


def _metrics(items: tuple[dict[str, object], ...]) -> dict[str, object]:
    rows = [_case_payload(item) for item in items]
    hits = sum(bool(set(row["relevant"]).intersection(row["fixed_k"] if "fixed" in item else row["lexical"])) for row, item in zip(rows, items, strict=True))
    recalls = [len(set(row["relevant"]).intersection(row["fixed_k"] if "fixed" in item else row["lexical"])) / len(row["relevant"]) for row, item in zip(rows, items, strict=True)]
    rankings = [row["fixed_k"] if "fixed" in item else row["lexical"] for row, item in zip(rows, items, strict=True)]
    mrr = sum(next((1 / rank for rank, address in enumerate(ranking, 1) if address in row["relevant"]), 0.0) for row, ranking in zip(rows, rankings, strict=True)) / len(rows)
    additions = [row for row in rows if "fixed" in items[0]] if items else []
    return {"case_count": len(rows), "hit_at_5": hits / len(rows), "mean_recall_at_5": sum(recalls) / len(rows), "mrr": mrr, "augmentation_cases_with_new_relevant": sum(bool(row["augmentation_recovered"]) for row in additions), "augmentation_new_relevant": sum(len(row["augmentation_recovered"]) for row in additions), "augmentation_cases_with_controls": sum(bool(row["augmentation_controls"]) for row in additions), "augmentation_control_exposures": sum(len(row["augmentation_controls"]) for row in additions), "fixed_k_cases_with_recoveries": sum(bool(row["fixed_k_recovered"]) for row in additions), "fixed_k_recoveries": sum(len(row["fixed_k_recovered"]) for row in additions), "fixed_k_cases_with_losses": sum(bool(row["relevant_losses"]) for row in additions), "fixed_k_relevant_losses": sum(len(row["relevant_losses"]) for row in additions), "fixed_k_control_insertions": sum(len(row["controls_in_fixed_k"]) for row in additions)}


def write_report(*, path: Path, payload: dict[str, object]) -> None:
    """Write the caller-selected structural experiment artifact."""
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
