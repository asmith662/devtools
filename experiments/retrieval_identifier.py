# Copyright (c) 2026
r"""Compare experimental identifier-aware lexical expansion with the BM25 baseline.

This module is deliberately experiment-owned.  Production lexical semantics remain
the Unicode ``\\w+`` plus ``casefold()`` baseline in ``devtools.context.retrieval``.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import iter_lexical_spans

if TYPE_CHECKING:
    from types import ModuleType

_ROOT = Path(__file__).resolve().parents[1]
_BASELINE_SCRIPT = _ROOT / "scripts" / "retrieval_bm25_baseline.py"
_K1 = 1.2
_B = 0.75
_MAXIMUM_RESULTS = 5
_REPORT_SCHEMA = "devtools-identifier-aware-bm25-comparison-v1"


@dataclass(frozen=True, slots=True)
class IdentifierExperimentDocument:
    """Retain one text unit and its native repository address for this experiment."""

    address: RepositoryResourceAddress
    text: str


@dataclass(frozen=True, slots=True)
class IdentifierExperimentObservation:
    """Record one original or derived term from an exact Unicode word span."""

    observed_text: str
    normalized_term: str
    start: int
    end: int
    origin: str


@dataclass(frozen=True, slots=True)
class IdentifierExperimentDocumentStatistics:
    """Retain expanded lexical length and term frequencies for one document."""

    document: IdentifierExperimentDocument
    observations: tuple[IdentifierExperimentObservation, ...]
    term_frequencies: tuple[tuple[str, int], ...]

    @property
    def document_length(self) -> int:
        """Return the number of original and derived lexical observations."""
        return len(self.observations)


@dataclass(frozen=True, slots=True)
class IdentifierExperimentIndex:
    """Retain deterministic experimental corpus statistics and postings."""

    document_statistics: tuple[IdentifierExperimentDocumentStatistics, ...]
    document_frequency: tuple[tuple[str, int], ...]
    postings: tuple[tuple[str, tuple[tuple[int, int], ...]], ...]
    average_document_length: float


@dataclass(frozen=True, slots=True)
class IdentifierExperimentMatch:
    """Retain one positive experimental BM25 document score."""

    document_statistics: IdentifierExperimentDocumentStatistics
    score: float


@dataclass(frozen=True, slots=True)
class IdentifierExperimentEvaluation:
    """Retain bounded binary-relevance evidence for one experimental query."""

    query_text: str
    relevant_addresses: tuple[RepositoryResourceAddress, ...]
    matches: tuple[IdentifierExperimentMatch, ...]
    retrieved_ranks: tuple[tuple[RepositoryResourceAddress, int], ...]
    missed_addresses: tuple[RepositoryResourceAddress, ...]
    hit_at_k: bool
    recall_at_k: float
    reciprocal_rank: float


@dataclass(frozen=True, slots=True)
class IdentifierExperimentComparison:
    """Retain unchanged-baseline and expanded-term evaluation evidence."""

    name: str
    baseline: Any
    experimental: IdentifierExperimentEvaluation
    newly_recovered: tuple[RepositoryResourceAddress, ...]
    lost: tuple[RepositoryResourceAddress, ...]


def parse_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    """Parse one explicit repository root and caller-selected comparison report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=Path.cwd(), type=Path)
    parser.add_argument("--report-path", required=True, type=Path)
    return parser.parse_args(arguments)


def expand_identifier_terms(*, observed_text: str) -> tuple[str, ...]:
    """Return original plus deterministic snake/camel/acronym/digit components.

    Leading/trailing and repeated underscores are ignored only while deriving
    components. The original casefolded span remains the first returned term.
    Camel boundaries are lower-to-upper and acronym-to-Capitalized transitions;
    alphabetic/digit transitions are boundaries. Components are casefolded and
    de-duplicated in encounter order.
    """
    original = observed_text.casefold()
    pieces = tuple(piece for piece in observed_text.strip("_").split("_") if piece)
    components = tuple(
        component.casefold()
        for piece in pieces
        for component in _split_identifier_piece(piece=piece)
    )
    return tuple(dict.fromkeys((original, *components)))


def analyze_identifier_text(
    *,
    text: str,
) -> tuple[IdentifierExperimentObservation, ...]:
    """Expand every baseline word span while retaining the original term first."""
    return tuple(
        IdentifierExperimentObservation(
            observed_text=observed_text,
            normalized_term=term,
            start=start,
            end=end,
            origin="original" if ordinal == 0 else "component",
        )
        for observed_text, _baseline_term, start, end in iter_lexical_spans(text=text)
        for ordinal, term in enumerate(
            expand_identifier_terms(observed_text=observed_text),
        )
    )


def analyze_identifier_query(
    *,
    text: str,
) -> tuple[IdentifierExperimentObservation, ...]:
    """Apply the identical experimental lexicalization to retrieval input."""
    return analyze_identifier_text(text=text)


def build_identifier_index(
    *,
    documents: tuple[IdentifierExperimentDocument, ...],
    identifier_aware: bool,
) -> IdentifierExperimentIndex:
    """Build one isolated baseline or identifier-expanded lexical BM25 input."""
    statistics = tuple(
        _document_statistics(document=document, identifier_aware=identifier_aware)
        for document in documents
    )
    frequency_by_term: dict[str, int] = {}
    postings_by_term: dict[str, list[tuple[int, int]]] = {}
    for document_position, statistic in enumerate(statistics):
        for term, frequency in statistic.term_frequencies:
            frequency_by_term[term] = frequency_by_term.get(term, 0) + 1
            postings_by_term.setdefault(term, []).append((document_position, frequency))
    return IdentifierExperimentIndex(
        document_statistics=statistics,
        document_frequency=tuple(frequency_by_term.items()),
        postings=tuple(
            (term, tuple(postings)) for term, postings in postings_by_term.items()
        ),
        average_document_length=(
            sum(statistic.document_length for statistic in statistics) / len(statistics)
            if statistics
            else 0.0
        ),
    )


def retrieve_identifier_bm25(
    *,
    query_text: str,
    index: IdentifierExperimentIndex,
    identifier_aware: bool,
    maximum_results: int = _MAXIMUM_RESULTS,
) -> tuple[IdentifierExperimentMatch, ...]:
    """Score distinct query terms with unchanged BM25 parameters and tie ordering."""
    if maximum_results <= 0:
        msg = "Maximum result count must be positive."
        raise ValueError(msg)
    query_terms = tuple(
        dict.fromkeys(
            observation.normalized_term
            for observation in _query_observations(
                text=query_text,
                identifier_aware=identifier_aware,
            )
        ),
    )
    frequency_by_term = dict(index.document_frequency)
    postings_by_term = dict(index.postings)
    scores: dict[int, float] = {}
    for term in query_terms:
        postings = postings_by_term.get(term)
        if postings is None:
            continue
        document_frequency = frequency_by_term[term]
        inverse_document_frequency = math.log(
            1
            + (len(index.document_statistics) - document_frequency + 0.5)
            / (document_frequency + 0.5),
        )
        for position, term_frequency in postings:
            document_length = index.document_statistics[position].document_length
            denominator = term_frequency + _K1 * (
                1 - _B + _B * document_length / index.average_document_length
            )
            scores[position] = scores.get(position, 0.0) + (
                inverse_document_frequency * term_frequency * (_K1 + 1) / denominator
            )
    return tuple(
        IdentifierExperimentMatch(
            document_statistics=index.document_statistics[position],
            score=score,
        )
        for position, score in sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0]),
        )[:maximum_results]
    )


def evaluate_identifier_retrieval(
    *,
    query_text: str,
    relevant_addresses: tuple[RepositoryResourceAddress, ...],
    matches: tuple[IdentifierExperimentMatch, ...],
) -> IdentifierExperimentEvaluation:
    """Evaluate retained experimental matches against explicit binary relevance."""
    relevant = set(relevant_addresses)
    recovered = tuple(
        (match.document_statistics.document.address, rank)
        for rank, match in enumerate(matches, start=1)
        if match.document_statistics.document.address in relevant
    )
    recovered_addresses = {address for address, _rank in recovered}
    missed = tuple(
        address for address in relevant_addresses if address not in recovered_addresses
    )
    first_rank = recovered[0][1] if recovered else None
    return IdentifierExperimentEvaluation(
        query_text=query_text,
        relevant_addresses=relevant_addresses,
        matches=matches,
        retrieved_ranks=recovered,
        missed_addresses=missed,
        hit_at_k=bool(recovered),
        recall_at_k=len(recovered) / len(relevant_addresses),
        reciprocal_rank=0.0 if first_rank is None else 1 / first_rank,
    )


def run_comparison(
    *,
    repository_root: Path,
) -> tuple[Any, tuple[IdentifierExperimentComparison, ...]]:
    """Compare both lexicalizations over one exact baseline-run corpus state."""
    baseline = _load_baseline_runner()
    baseline_run = baseline.run_benchmark(repository_root=repository_root)
    documents = tuple(
        IdentifierExperimentDocument(
            address=document.resource.address,
            text=document.text,
        )
        for document in baseline_run.documents.documents
    )
    index = build_identifier_index(documents=documents, identifier_aware=True)
    comparisons = tuple(
        _compare_case(
            case=case,
            baseline_evaluation=baseline_evaluation,
            index=index,
        )
        for case, baseline_evaluation in zip(
            baseline_run.cases,
            baseline_run.evaluations,
            strict=True,
        )
    )
    return baseline_run, comparisons


def controlled_cases() -> tuple[IdentifierExperimentComparison, ...]:
    """Run focused identifier and non-identifier cases under both lexicalizations."""
    return tuple(
        _controlled_case(name=name, documents=documents, query=query, relevant=address)
        for name, documents, query, address in (
            (
                "pascal-case",
                (("target.py", "RepositoryTextCorpus"), ("noise.md", "quiet prose")),
                "repository text corpus",
                "target.py",
            ),
            (
                "snake-case",
                (("target.py", "repository_text_corpus"), ("noise.md", "quiet prose")),
                "repository text corpus",
                "target.py",
            ),
            (
                "camel-case",
                (
                    ("target.py", "loadRepositoryTextCorpus"),
                    ("noise.md", "quiet prose"),
                ),
                "repository text corpus",
                "target.py",
            ),
            (
                "acronym-and-digits",
                (
                    (
                        "target.py",
                        (
                            "HTTPClient parseHTTPResponse version2Parser BM25 "
                            "Qwen3 __init__"
                        ),
                    ),
                ),
                "http client parse http response version 2 parser bm 25 qwen 3 init",
                "target.py",
            ),
            (
                "prose-only",
                (("target.md", "repository text corpus"), ("noise.md", "quiet prose")),
                "repository text corpus",
                "target.md",
            ),
            (
                "lexical-distractor",
                (
                    ("target.py", "RepositoryTextCorpus"),
                    ("noise.md", "repository text corpus repository text corpus"),
                ),
                "repository text corpus",
                "target.py",
            ),
        )
    )


def report_payload(
    *,
    baseline_run: Any,  # noqa: ANN401 -- dynamic script boundary
    comparisons: tuple[IdentifierExperimentComparison, ...],
) -> dict[str, object]:
    """Serialize paired evidence without changing the preserved baseline report."""
    baseline_summary = baseline_run.summary
    experimental_metrics = _aggregate_metrics(comparisons=comparisons)
    return {
        "schema": _REPORT_SCHEMA,
        "scope": "experimental identifier-aware lexical expansion comparison",
        "identified_state": {
            "snapshot_id": str(baseline_run.snapshot.id),
            "corpus_id": str(baseline_run.corpus.id),
            "document_count": len(baseline_run.documents.documents),
        },
        "constant_configuration": {
            "evaluation_k": _MAXIMUM_RESULTS,
            "bm25": {"k1": _K1, "b": _B},
            "baseline_lexical_semantics": "unicode-word-span-casefold-v1",
            "experimental_lexical_semantics": "identifier-expansion-v1",
            "path_or_package_scoring": False,
        },
        "aggregate": {
            "baseline": _summary_payload(summary=baseline_summary),
            "experimental": experimental_metrics,
            "delta": {
                key: experimental_metrics[key]
                - _summary_payload(summary=baseline_summary)[key]
                for key in experimental_metrics
            },
        },
        "cases": [
            _comparison_payload(comparison=comparison) for comparison in comparisons
        ],
    }


def write_report(*, path: Path, payload: dict[str, object]) -> None:
    """Write only an explicitly requested experimental JSON artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(arguments: list[str] | None = None) -> None:
    """Run one local paired comparison and persist a distinct report artifact."""
    parsed = parse_arguments(arguments)
    baseline_run, comparisons = run_comparison(
        repository_root=parsed.repository_root.resolve(),
    )
    write_report(
        path=parsed.report_path,
        payload=report_payload(baseline_run=baseline_run, comparisons=comparisons),
    )


def _split_identifier_piece(*, piece: str) -> tuple[str, ...]:
    """Split one underscore-free piece at camel, acronym, and digit boundaries."""
    parts: list[str] = []
    start = 0
    for position in range(1, len(piece)):
        previous = piece[position - 1]
        current = piece[position]
        following = piece[position + 1] if position + 1 < len(piece) else ""
        if (
            (previous.islower() and current.isupper())
            or (previous.isupper() and current.isupper() and following.islower())
            or (previous.isalpha() and current.isdigit())
            or (previous.isdigit() and current.isalpha())
        ):
            parts.append(piece[start:position])
            start = position
    parts.append(piece[start:])
    return tuple(part for part in parts if part)


def _document_statistics(
    *,
    document: IdentifierExperimentDocument,
    identifier_aware: bool,
) -> IdentifierExperimentDocumentStatistics:
    """Analyze one document and count terms in their first expanded encounter order."""
    observations = _query_observations(
        text=document.text,
        identifier_aware=identifier_aware,
    )
    counts: dict[str, int] = {}
    for observation in observations:
        counts[observation.normalized_term] = (
            counts.get(observation.normalized_term, 0) + 1
        )
    return IdentifierExperimentDocumentStatistics(
        document=document,
        observations=observations,
        term_frequencies=tuple(counts.items()),
    )


def _query_observations(
    *,
    text: str,
    identifier_aware: bool,
) -> tuple[IdentifierExperimentObservation, ...]:
    """Apply either exact baseline terms or the symmetric experimental expansion."""
    if identifier_aware:
        return analyze_identifier_query(text=text)
    return tuple(
        IdentifierExperimentObservation(
            observed_text=observed_text,
            normalized_term=normalized_term,
            start=start,
            end=end,
            origin="original",
        )
        for observed_text, normalized_term, start, end in iter_lexical_spans(text=text)
    )


def _compare_case(
    *,
    case: Any,  # noqa: ANN401 -- dynamic script boundary
    baseline_evaluation: Any,  # noqa: ANN401 -- dynamic script boundary
    index: IdentifierExperimentIndex,
) -> IdentifierExperimentComparison:
    """Compare one unchanged baseline evaluation with one expanded-term result."""
    matches = retrieve_identifier_bm25(
        query_text=case.query_text,
        index=index,
        identifier_aware=True,
    )
    experimental = evaluate_identifier_retrieval(
        query_text=case.query_text,
        relevant_addresses=case.relevant_resource_addresses,
        matches=matches,
    )
    baseline_recovered = {
        item.address for item in baseline_evaluation.retrieved_relevant_resources
    }
    experimental_recovered = {
        address for address, _rank in experimental.retrieved_ranks
    }
    return IdentifierExperimentComparison(
        name=case.name,
        baseline=baseline_evaluation,
        experimental=experimental,
        newly_recovered=tuple(
            address
            for address in experimental.relevant_addresses
            if address in experimental_recovered and address not in baseline_recovered
        ),
        lost=tuple(
            address
            for address in experimental.relevant_addresses
            if address in baseline_recovered and address not in experimental_recovered
        ),
    )


def _controlled_case(
    *,
    name: str,
    documents: tuple[tuple[str, str], ...],
    query: str,
    relevant: str,
) -> IdentifierExperimentComparison:
    """Build one fixture-local binary-relevance comparison without repository I/O."""
    experimental_documents = tuple(
        IdentifierExperimentDocument(RepositoryResourceAddress(address), text)
        for address, text in documents
    )
    relevant_address = RepositoryResourceAddress(relevant)
    baseline_index = build_identifier_index(
        documents=experimental_documents,
        identifier_aware=False,
    )
    experimental_index = build_identifier_index(
        documents=experimental_documents,
        identifier_aware=True,
    )
    baseline_matches = retrieve_identifier_bm25(
        query_text=query,
        index=baseline_index,
        identifier_aware=False,
    )
    baseline = evaluate_identifier_retrieval(
        query_text=query,
        relevant_addresses=(relevant_address,),
        matches=baseline_matches,
    )
    experimental_matches = retrieve_identifier_bm25(
        query_text=query,
        index=experimental_index,
        identifier_aware=True,
    )
    experimental = evaluate_identifier_retrieval(
        query_text=query,
        relevant_addresses=(relevant_address,),
        matches=experimental_matches,
    )
    baseline_recovered = {address for address, _rank in baseline.retrieved_ranks}
    experimental_recovered = {
        address for address, _rank in experimental.retrieved_ranks
    }
    return IdentifierExperimentComparison(
        name=name,
        baseline=baseline,
        experimental=experimental,
        newly_recovered=(relevant_address,)
        if relevant_address in experimental_recovered - baseline_recovered
        else (),
        lost=(relevant_address,)
        if relevant_address in baseline_recovered - experimental_recovered
        else (),
    )


def _aggregate_metrics(
    *,
    comparisons: tuple[IdentifierExperimentComparison, ...],
) -> dict[str, float]:
    """Calculate same-case experimental aggregates without significance inference."""
    count = len(comparisons)
    return {
        "hit_rate_at_k": sum(item.experimental.hit_at_k for item in comparisons)
        / count,
        "mean_recall_at_k": sum(item.experimental.recall_at_k for item in comparisons)
        / count,
        "mean_reciprocal_rank": sum(
            item.experimental.reciprocal_rank for item in comparisons
        )
        / count,
    }


def _summary_payload(*, summary: Any) -> dict[str, float]:  # noqa: ANN401
    """Project the existing baseline evaluator's aggregate metrics for comparison."""
    return {
        "hit_rate_at_k": summary.hit_rate_at_k,
        "mean_recall_at_k": summary.mean_recall_at_k,
        "mean_reciprocal_rank": summary.mean_reciprocal_rank,
    }


def _comparison_payload(
    *,
    comparison: IdentifierExperimentComparison,
) -> dict[str, object]:
    """Serialize paired ranks, recovery transitions, and metrics for one case."""
    baseline = comparison.baseline
    return {
        "name": comparison.name,
        "query": comparison.experimental.query_text,
        "designated_relevant_resources": [
            str(address) for address in comparison.experimental.relevant_addresses
        ],
        "baseline": {
            "ranked_resources": [
                str(match.document_statistics.analysis.document.resource.address)
                for match in baseline.retrieval_result.matches
            ],
            "retrieved_relevant_resources": [
                {"address": str(item.address), "rank": item.rank}
                for item in baseline.retrieved_relevant_resources
            ],
            "missed_relevant_resources": [
                str(address) for address in baseline.missed_relevant_resource_addresses
            ],
            "metrics": _evaluation_metrics(evaluation=baseline),
        },
        "experimental": {
            "ranked_resources": [
                str(match.document_statistics.document.address)
                for match in comparison.experimental.matches
            ],
            "retrieved_relevant_resources": [
                {"address": str(address), "rank": rank}
                for address, rank in comparison.experimental.retrieved_ranks
            ],
            "missed_relevant_resources": [
                str(address) for address in comparison.experimental.missed_addresses
            ],
            "metrics": _evaluation_metrics(evaluation=comparison.experimental),
        },
        "newly_recovered": [str(address) for address in comparison.newly_recovered],
        "lost": [str(address) for address in comparison.lost],
    }


def _evaluation_metrics(
    *,
    evaluation: Any,  # noqa: ANN401 -- dynamic script boundary
) -> dict[str, float | bool]:
    """Project native metric values without recalculation or normalization."""
    return {
        "hit_at_k": evaluation.hit_at_k,
        "recall_at_k": evaluation.recall_at_k,
        "reciprocal_rank": evaluation.reciprocal_rank,
    }


def _load_baseline_runner() -> ModuleType:
    """Load the one operational baseline script without promoting it to production."""
    specification = importlib.util.spec_from_file_location(
        "identifier_comparison_baseline",
        _BASELINE_SCRIPT,
    )
    if specification is None or specification.loader is None:
        msg = "Could not load the real-repository BM25 baseline script."
        raise RuntimeError(msg)
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


if __name__ == "__main__":
    main()
