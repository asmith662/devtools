# Copyright (c) 2026
# ruff: noqa: E402, INP001, T201
"""Run the bounded content-only BM25 baseline against this repository."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from devtools.context.repository.corpus import (
    RepositoryTextCorpus,
    RepositoryTextCorpusDefinition,
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import (
    RepositoryResourceDiscovery,
    discover_repository_resource_addresses,
)
from devtools.context.repository.document import (
    RepositoryTextDocumentCollection,
    represent_repository_text_corpus,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import (
    observe_repository_resources,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_content_bm25,
)
from devtools.context.retrieval.lexical.evaluation import (
    RepositoryTextLexicalRetrievalEvaluationCase,
    RepositoryTextLexicalRetrievalEvaluationResult,
    RepositoryTextLexicalRetrievalEvaluationSummary,
    evaluate_repository_text_lexical_bm25_retrieval,
    summarize_repository_text_lexical_retrieval_evaluations,
)
from devtools.context.retrieval.lexical.index import (
    RepositoryTextLexicalInvertedIndex,
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import ResolvedPath, resolve_path

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.snapshot import RepositorySnapshot

_BENCHMARK_REPOSITORY_ID = "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
_MAXIMUM_DISCOVERED_RESOURCES = 10_000
_MAXIMUM_TRAVERSAL_ENTRIES = 20_000
_MAXIMUM_RESOURCE_BYTES = 1_048_576
_MAXIMUM_RESULTS = 5
_INCLUDED_SUFFIXES = frozenset({".md", ".py", ".toml", ".yaml", ".yml"})
_EXCLUDED_TOP_LEVEL_DIRECTORIES = frozenset(
    {
        ".devtools",
        ".git",
        ".idea",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "htmlcov",
    },
)
_EXCLUDED_EXACT_ADDRESSES = frozenset(
    {
        "architecture-archaeology-dossier.md",
        "evaluation-architecture-investigation-dossier.md",
        "docs/implementation_ledger.md",
        "scripts/retrieval_bm25_baseline.py",
        "tests/scripts/test_retrieval_bm25_baseline.py",
    },
)
_REPORT_SCHEMA = "devtools-content-only-bm25-repository-benchmark-v1"


@dataclass(frozen=True, slots=True)
class RepositoryBm25BenchmarkCase:
    """Declare one manually judged, repository-specific retrieval case."""

    name: str
    description: str
    query_text: str
    relevant_resource_addresses: tuple[RepositoryResourceAddress, ...]


@dataclass(frozen=True, slots=True)
class RepositoryBm25BenchmarkRun:
    """Retain one exact pipeline realization and its evaluated case evidence."""

    root: ResolvedPath
    discovery: RepositoryResourceDiscovery
    definition: RepositoryTextCorpusDefinition
    snapshot: RepositorySnapshot
    corpus: RepositoryTextCorpus
    documents: RepositoryTextDocumentCollection
    index: RepositoryTextLexicalInvertedIndex
    cases: tuple[RepositoryBm25BenchmarkCase, ...]
    evaluations: tuple[RepositoryTextLexicalRetrievalEvaluationResult, ...]
    summary: RepositoryTextLexicalRetrievalEvaluationSummary


_CASES = (
    RepositoryBm25BenchmarkCase(
        name="corpus-realization",
        description="Locate the selected-observed repository text corpus realization.",
        query_text="repository text corpus realization",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/corpus.py"),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="repository-discovery",
        description="Locate bounded metadata-only repository resource discovery.",
        query_text="bounded repository resource discovery",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/discovery.py"),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="observation-bound",
        description="Locate the explicit UTF-8 per-resource observation byte bound.",
        query_text="maximum resource bytes utf8 observation",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/repository/observation.py"),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="lexical-analysis",
        description="Locate Unicode word-span and casefold lexical analysis semantics.",
        query_text="unicode lexical spans casefold",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/retrieval/lexical/analysis.py"),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="bm25-scoring",
        description="Locate Okapi BM25 inverse-document-frequency scoring behavior.",
        query_text="okapi bm25 inverse document frequency",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/retrieval/lexical/bm25.py"),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="retrieval-evaluation",
        description="Locate bounded retrieval evaluation and reciprocal-rank metrics.",
        query_text="recall reciprocal rank retrieval evaluation",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/retrieval/lexical/evaluation.py"),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="python-function-declarations",
        description="Locate direct module-body Python function declaration derivation.",
        query_text="direct module body python function declarations",
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/python/function/declarations.py",
            ),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="python-function-context-assembly",
        description=(
            "Locate exact source materialization, rendering, and request assembly."
        ),
        query_text="exact source materialization rendering model request assembly",
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/python/function/materialization.py",
            ),
            RepositoryResourceAddress(
                "src/devtools/context/python/function/rendering.py",
            ),
            RepositoryResourceAddress(
                "src/devtools/context/python/function/request_assembly.py",
            ),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="architecture-context-retrieval",
        description="Locate the current architecture account of Context and retrieval.",
        query_text="Context retrieval repository intelligence architecture",
        relevant_resource_addresses=(RepositoryResourceAddress("docs/architecture.md"),),
    ),
    RepositoryBm25BenchmarkCase(
        name="b0002-backlog",
        description="Locate the B-0002 coding Context substrate design record.",
        query_text="coding Context substrate repository intelligence",
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "docs/backlog/epics/B-0002-coding-context-substrate.md",
            ),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="project-configuration",
        description="Locate pytest coverage and project configuration settings.",
        query_text="pytest coverage branch threshold configuration",
        relevant_resource_addresses=(RepositoryResourceAddress("pyproject.toml"),),
    ),
    RepositoryBm25BenchmarkCase(
        name="lexical-index-cross-file",
        description=(
            "Locate both lexical corpus statistics and inverted index behavior."
        ),
        query_text="lexical corpus statistics inverted index",
        relevant_resource_addresses=(
            RepositoryResourceAddress(
                "src/devtools/context/retrieval/lexical/statistics.py",
            ),
            RepositoryResourceAddress("src/devtools/context/retrieval/lexical/index.py"),
        ),
    ),
    RepositoryBm25BenchmarkCase(
        name="identifier-boundary",
        description=(
            "Locate the RepositoryTextLexicalQueryObservation identifier concept."
        ),
        query_text="repository text lexical query observation",
        relevant_resource_addresses=(
            RepositoryResourceAddress("src/devtools/context/retrieval/lexical/bm25.py"),
        ),
    ),
)


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse one explicit root and caller-selected report output path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=Path.cwd(), type=Path)
    parser.add_argument("--report-path", required=True, type=Path)
    return parser.parse_args(arguments)


def benchmark_cases() -> tuple[RepositoryBm25BenchmarkCase, ...]:
    """Return the fixed manually judged cases for this repository checkpoint."""
    return _CASES


def select_benchmark_addresses(
    *,
    discovery: RepositoryResourceDiscovery,
) -> tuple[RepositoryResourceAddress, ...]:
    """Select the bounded benchmark's operationally eligible text addresses.

    This local inclusion policy is not repository classification or relevance.
    """
    return tuple(
        address
        for address in discovery.addresses
        if _is_benchmark_eligible(address=address)
    )


def run_benchmark(*, repository_root: Path) -> RepositoryBm25BenchmarkRun:
    """Run the established acquisition, lexical, BM25, and evaluation pipeline."""
    root = resolve_path(repository_root)
    repository = Repository(RepositoryId.parse(_BENCHMARK_REPOSITORY_ID))
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=root,
        maximum_resource_count=_MAXIMUM_DISCOVERED_RESOURCES,
        maximum_traversal_entry_count=_MAXIMUM_TRAVERSAL_ENTRIES,
    )
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=select_benchmark_addresses(discovery=discovery),
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=root,
        addresses=definition.selected_addresses,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )
    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)
    documents = represent_repository_text_corpus(corpus=corpus)
    analysis = analyze_repository_text_document_collection(
        document_collection=documents,
    )
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analysis,
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)
    cases = benchmark_cases()
    evaluations = tuple(_evaluate_case(case=case, index=index) for case in cases)
    return RepositoryBm25BenchmarkRun(
        root=root,
        discovery=discovery,
        definition=definition,
        snapshot=snapshot,
        corpus=corpus,
        documents=documents,
        index=index,
        cases=cases,
        evaluations=evaluations,
        summary=summarize_repository_text_lexical_retrieval_evaluations(
            evaluations=evaluations,
        ),
    )


def report_payload(*, run: RepositoryBm25BenchmarkRun) -> dict[str, object]:
    """Serialize inspectable baseline evidence without interpreting relevance."""
    return {
        "schema": _REPORT_SCHEMA,
        "scope": "bounded real-repository content-only BM25 baseline",
        "repository_root": str(run.root),
        "bounds": {
            "maximum_discovered_resources": _MAXIMUM_DISCOVERED_RESOURCES,
            "maximum_traversal_entries": _MAXIMUM_TRAVERSAL_ENTRIES,
            "maximum_resource_bytes": _MAXIMUM_RESOURCE_BYTES,
            "maximum_results": _MAXIMUM_RESULTS,
            "evaluation_k": run.summary.evaluation_k,
        },
        "membership": {
            "included_suffixes": sorted(_INCLUDED_SUFFIXES),
            "excluded_top_level_directories": sorted(_EXCLUDED_TOP_LEVEL_DIRECTORIES),
            "excluded_exact_addresses": sorted(_EXCLUDED_EXACT_ADDRESSES),
            "discovered_resource_count": len(run.discovery.addresses),
            "examined_entry_count": run.discovery.examined_entry_count,
            "selected_addresses": [
                str(address) for address in run.definition.selected_addresses
            ],
        },
        "identified_state": {
            "repository_id": str(run.definition.discovery.repository_id),
            "snapshot_id": str(run.snapshot.id),
            "corpus_id": str(run.corpus.id),
            "document_count": len(run.documents.documents),
        },
        "bm25": {
            "k1": 1.2,
            "b": 0.75,
            "content_only": True,
            "path_or_package_scoring": False,
        },
        "cases": [
            _evaluation_payload(case=case, evaluation=evaluation)
            for case, evaluation in zip(run.cases, run.evaluations, strict=True)
        ],
        "aggregate": {
            "hit_rate_at_k": run.summary.hit_rate_at_k,
            "mean_recall_at_k": run.summary.mean_recall_at_k,
            "mean_reciprocal_rank": run.summary.mean_reciprocal_rank,
        },
    }


def write_report(*, path: Path, payload: dict[str, object]) -> None:
    """Write one caller-selected JSON report outside normal test execution."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main(arguments: Sequence[str] | None = None) -> None:
    """Run one local benchmark and persist its inspectable baseline evidence."""
    parsed = parse_arguments(arguments)
    run = run_benchmark(repository_root=parsed.repository_root)
    write_report(path=parsed.report_path, payload=report_payload(run=run))
    print(f"benchmark cases: {len(run.cases)}")
    print(f"Hit@{run.summary.evaluation_k}: {run.summary.hit_rate_at_k:.3f}")
    print(f"mean Recall@{run.summary.evaluation_k}: {run.summary.mean_recall_at_k:.3f}")
    print(f"MRR: {run.summary.mean_reciprocal_rank:.3f}")


def _is_benchmark_eligible(*, address: RepositoryResourceAddress) -> bool:
    """Apply only the benchmark's explicit operational membership restrictions."""
    return (
        address.parts[0] not in _EXCLUDED_TOP_LEVEL_DIRECTORIES
        and address.value not in _EXCLUDED_EXACT_ADDRESSES
        and Path(address.value).suffix.casefold() in _INCLUDED_SUFFIXES
    )


def _evaluate_case(
    *,
    case: RepositoryBm25BenchmarkCase,
    index: RepositoryTextLexicalInvertedIndex,
) -> RepositoryTextLexicalRetrievalEvaluationResult:
    """Run unchanged BM25 once and evaluate only its retained ranked evidence."""
    query = analyze_repository_text_lexical_query(text=case.query_text)
    retrieval_result = retrieve_repository_text_documents_by_content_bm25(
        query=query,
        index=index,
        maximum_results=_MAXIMUM_RESULTS,
    )
    return evaluate_repository_text_lexical_bm25_retrieval(
        case=RepositoryTextLexicalRetrievalEvaluationCase(
            query=query,
            relevant_resource_addresses=case.relevant_resource_addresses,
            evaluation_k=_MAXIMUM_RESULTS,
        ),
        retrieval_result=retrieval_result,
    )


def _evaluation_payload(
    *,
    case: RepositoryBm25BenchmarkCase,
    evaluation: RepositoryTextLexicalRetrievalEvaluationResult,
) -> dict[str, object]:
    """Serialize one case's designated relevance and retained ranked evidence."""
    return {
        "name": case.name,
        "description": case.description,
        "query": case.query_text,
        "designated_relevant_resources": [
            str(address) for address in case.relevant_resource_addresses
        ],
        "ranked_resources": [
            {
                "rank": rank,
                "address": str(
                    match.document_statistics.analysis.document.resource.address,
                ),
                "score": match.score,
            }
            for rank, match in enumerate(evaluation.retrieval_result.matches, start=1)
        ],
        "retrieved_relevant_resources": [
            {"address": str(retrieved.address), "rank": retrieved.rank}
            for retrieved in evaluation.retrieved_relevant_resources
        ],
        "missed_relevant_resources": [
            str(address) for address in evaluation.missed_relevant_resource_addresses
        ],
        "metrics": {
            "hit_at_k": evaluation.hit_at_k,
            "recall_at_k": evaluation.recall_at_k,
            "reciprocal_rank": evaluation.reciprocal_rank,
        },
    }


if __name__ == "__main__":
    main()
