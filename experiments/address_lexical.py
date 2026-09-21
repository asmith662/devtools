# Copyright (c) 2026
"""Compare experimental filename and path lexical evidence with content BM25.

This experiment leaves production content-only lexical analysis and BM25 untouched.
It scores address evidence in a separate BM25 field, then adds that score to the
unchanged production content score. Address terms therefore never alter content
document length, TF, DF, or average document length.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)

if TYPE_CHECKING:
    from types import ModuleType

_ROOT = Path(__file__).resolve().parents[1]
_BASELINE_SCRIPT = _ROOT / "scripts" / "retrieval_bm25_baseline.py"
_K1 = 1.2
_B = 0.75
_K = 5
_REPORT_SCHEMA = "devtools-address-lexical-bm25-comparison-v1"


@dataclass(frozen=True, slots=True)
class AddressObservation:
    """Retain one independently scored filename or directory lexical observation."""

    normalized_term: str
    source: str


@dataclass(frozen=True, slots=True)
class AddressDocument:
    """Retain address-local lexical observations for one repository document."""

    address: RepositoryResourceAddress
    observations: tuple[AddressObservation, ...]
    extension: str

    @property
    def length(self) -> int:
        """Return the count of scored address observations only."""
        return len(self.observations)


@dataclass(frozen=True, slots=True)
class AddressIndex:
    """Retain local address-field TF/DF/postings without changing content state."""

    documents: tuple[AddressDocument, ...]
    term_frequencies: tuple[tuple[tuple[str, int], ...], ...]
    document_frequencies: tuple[tuple[str, int], ...]
    postings: tuple[tuple[str, tuple[tuple[int, int], ...]], ...]
    average_length: float


@dataclass(frozen=True, slots=True)
class AddressContribution:
    """Explain one address-field BM25 term contribution."""

    normalized_term: str
    sources: tuple[str, ...]
    term_frequency: int
    document_frequency: int
    inverse_document_frequency: float
    document_length: int
    average_document_length: float
    contribution: float


@dataclass(frozen=True, slots=True)
class AddressMatch:
    """Retain separately attributable content and address evidence for one result."""

    address: RepositoryResourceAddress
    content_score: float
    address_contributions: tuple[AddressContribution, ...]
    document_position: int

    @property
    def address_score(self) -> float:
        """Return the local filename/path BM25 contribution sum."""
        return sum(item.contribution for item in self.address_contributions)

    @property
    def score(self) -> float:
        """Return the explicit unweighted content-plus-address experiment score."""
        return self.content_score + self.address_score


@dataclass(frozen=True, slots=True)
class AddressEvaluation:
    """Retain bounded native-address relevance evidence for one variant/case."""

    matches: tuple[AddressMatch, ...]
    relevant_ranks: tuple[tuple[RepositoryResourceAddress, int], ...]
    missed: tuple[RepositoryResourceAddress, ...]
    hit_at_k: bool
    recall_at_k: float
    reciprocal_rank: float


@dataclass(frozen=True, slots=True)
class AddressComparison:
    """Retain three paired retrieval evaluations for a manually judged case."""

    name: str
    query_text: str
    relevant_addresses: tuple[RepositoryResourceAddress, ...]
    baseline: Any
    filename: AddressEvaluation
    full_path: AddressEvaluation


def parse_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    """Parse one root and a caller-selected address-comparison report path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=Path.cwd(), type=Path)
    parser.add_argument("--report-path", required=True, type=Path)
    return parser.parse_args(arguments)


def filename_observations(
    *,
    address: RepositoryResourceAddress,
) -> tuple[AddressObservation, ...]:
    r"""Tokenize only a filename stem with baseline span and casefold semantics.

    The extension is retained separately by :func:`address_document` and is never
    scored. Underscores remain inside a baseline ``\\w+`` span, while hyphens split
    spans; no identifier expansion is applied.
    """
    return tuple(
        AddressObservation(normalized_term=term, source="filename")
        for _observed, term, _start, _end in iter_lexical_spans(
            text=PurePosixPath(address.value).stem,
        )
    )


def full_path_observations(
    *,
    address: RepositoryResourceAddress,
) -> tuple[AddressObservation, ...]:
    """Tokenize directories plus filename stem; extensions remain unscored."""
    path = PurePosixPath(address.value)
    return tuple(
        AddressObservation(
            normalized_term=term,
            source="filename" if position == len(path.parts) - 1 else "directory",
        )
        for position, component in enumerate(path.parts)
        for _observed, term, _start, _end in iter_lexical_spans(
            text=PurePosixPath(component).stem
            if position == len(path.parts) - 1
            else component,
        )
    )


def address_document(
    *,
    address: RepositoryResourceAddress,
    variant: str,
) -> AddressDocument:
    """Create one filename-only or full-path experimental address field."""
    if variant == "filename":
        observations = filename_observations(address=address)
    elif variant == "full-path":
        observations = full_path_observations(address=address)
    else:
        msg = f"Unknown address lexicalization variant: {variant}."
        raise ValueError(msg)
    return AddressDocument(
        address=address,
        observations=observations,
        extension=PurePosixPath(address.value).suffix.casefold(),
    )


def build_address_index(
    *,
    addresses: tuple[RepositoryResourceAddress, ...],
    variant: str,
) -> AddressIndex:
    """Build a separate deterministic address BM25 field over document order."""
    documents = tuple(
        address_document(address=address, variant=variant) for address in addresses
    )
    frequencies: list[tuple[tuple[str, int], ...]] = []
    document_frequency: dict[str, int] = {}
    postings: dict[str, list[tuple[int, int]]] = {}
    for position, document in enumerate(documents):
        counts: dict[str, int] = {}
        for observation in document.observations:
            counts[observation.normalized_term] = (
                counts.get(observation.normalized_term, 0) + 1
            )
        frequency_items = tuple(counts.items())
        frequencies.append(frequency_items)
        for term, frequency in frequency_items:
            document_frequency[term] = document_frequency.get(term, 0) + 1
            postings.setdefault(term, []).append((position, frequency))
    return AddressIndex(
        documents=documents,
        term_frequencies=tuple(frequencies),
        document_frequencies=tuple(document_frequency.items()),
        postings=tuple((term, tuple(items)) for term, items in postings.items()),
        average_length=(
            sum(document.length for document in documents) / len(documents)
            if documents
            else 0.0
        ),
    )


def retrieve_with_address_evidence(
    *,
    query_text: str,
    content_index: Any,  # noqa: ANN401 -- dynamic production-script boundary
    address_index: AddressIndex,
    maximum_results: int = _K,
) -> tuple[AddressMatch, ...]:
    """Add separately normalized address BM25 evidence to unchanged content scores."""
    if maximum_results <= 0:
        msg = "Maximum result count must be positive."
        raise ValueError(msg)
    query = analyze_repository_text_lexical_query(text=query_text)
    content_result = retrieve_repository_text_documents_by_bm25(
        query=query,
        index=content_index,
        maximum_results=len(address_index.documents),
    )
    content_scores = {
        match.document_statistics.analysis.document.resource.address: match.score
        for match in content_result.matches
    }
    contributions = _address_contributions(
        query_terms=query.normalized_terms,
        index=address_index,
    )
    candidates = tuple(
        AddressMatch(
            address=document.address,
            content_score=content_scores.get(document.address, 0.0),
            address_contributions=contributions.get(position, ()),
            document_position=position,
        )
        for position, document in enumerate(address_index.documents)
        if content_scores.get(document.address, 0.0) > 0 or position in contributions
    )
    return tuple(
        sorted(candidates, key=lambda item: (-item.score, item.document_position))[
            :maximum_results
        ],
    )


def evaluate_address_matches(
    *,
    relevant_addresses: tuple[RepositoryResourceAddress, ...],
    matches: tuple[AddressMatch, ...],
) -> AddressEvaluation:
    """Evaluate local variant ranks against unchanged explicit ground truth."""
    relevant = set(relevant_addresses)
    ranks = tuple(
        (match.address, rank)
        for rank, match in enumerate(matches, start=1)
        if match.address in relevant
    )
    recovered = {address for address, _rank in ranks}
    missed = tuple(
        address for address in relevant_addresses if address not in recovered
    )
    return AddressEvaluation(
        matches=matches,
        relevant_ranks=ranks,
        missed=missed,
        hit_at_k=bool(ranks),
        recall_at_k=len(ranks) / len(relevant_addresses),
        reciprocal_rank=0.0 if not ranks else 1 / ranks[0][1],
    )


def run_comparison(
    *,
    repository_root: Path,
) -> tuple[Any, tuple[AddressComparison, ...]]:
    """Run all three variants over exactly one production benchmark realization."""
    baseline_script = _load_baseline_runner()
    baseline_run = baseline_script.run_benchmark(repository_root=repository_root)
    addresses = tuple(
        document.resource.address for document in baseline_run.documents.documents
    )
    filename_index = build_address_index(addresses=addresses, variant="filename")
    path_index = build_address_index(addresses=addresses, variant="full-path")
    return baseline_run, tuple(
        AddressComparison(
            name=case.name,
            query_text=case.query_text,
            relevant_addresses=case.relevant_resource_addresses,
            baseline=baseline_evaluation,
            filename=evaluate_address_matches(
                relevant_addresses=case.relevant_resource_addresses,
                matches=retrieve_with_address_evidence(
                    query_text=case.query_text,
                    content_index=baseline_run.index,
                    address_index=filename_index,
                ),
            ),
            full_path=evaluate_address_matches(
                relevant_addresses=case.relevant_resource_addresses,
                matches=retrieve_with_address_evidence(
                    query_text=case.query_text,
                    content_index=baseline_run.index,
                    address_index=path_index,
                ),
            ),
        )
        for case, baseline_evaluation in zip(
            baseline_run.cases,
            baseline_run.evaluations,
            strict=True,
        )
    )


def controlled_cases() -> dict[
    str,
    tuple[AddressEvaluation, AddressEvaluation, AddressEvaluation],
]:
    """Run filename, directory, distractor, extension, and stable-content fixtures."""
    fixtures = {
        "filename-only": (
            (("src/target-guide.md", "quiet prose"), ("docs/noise.md", "quiet prose")),
            "target guide",
            "src/target-guide.md",
        ),
        "directory-only": (
            (("context/opaque.md", "quiet prose"), ("docs/noise.md", "quiet prose")),
            "context",
            "context/opaque.md",
        ),
        "filename-distractor": (
            (
                ("src/target-guide.md", "quiet prose"),
                ("docs/noise.md", "target guide target guide"),
            ),
            "target guide",
            "src/target-guide.md",
        ),
        "directory-distractor": (
            (
                ("context/opaque.md", "quiet prose"),
                ("docs/noise.md", "context context"),
            ),
            "context",
            "context/opaque.md",
        ),
        "shared-extension": (
            (("src/first.py", "quiet prose"), ("src/second.py", "quiet prose")),
            "py",
            "src/first.py",
        ),
        "strong-content": (
            (
                ("src/target.md", "exact strong content"),
                ("docs/noise.md", "quiet prose"),
            ),
            "exact strong content",
            "src/target.md",
        ),
    }
    return {
        name: _controlled_case(documents=documents, query=query, relevant=relevant)
        for name, (documents, query, relevant) in fixtures.items()
    }


def report_payload(
    *,
    baseline_run: Any,  # noqa: ANN401 -- dynamic production-script boundary
    comparisons: tuple[AddressComparison, ...],
) -> dict[str, object]:
    """Serialize paired variant evidence without mutating either established report."""
    baseline_metrics = _baseline_metrics(comparisons=comparisons)
    filename_metrics = _variant_metrics(comparisons=comparisons, variant="filename")
    path_metrics = _variant_metrics(comparisons=comparisons, variant="full_path")
    return {
        "schema": _REPORT_SCHEMA,
        "identified_state": {
            "snapshot_id": str(baseline_run.snapshot.id),
            "corpus_id": str(baseline_run.corpus.id),
            "document_count": len(baseline_run.documents.documents),
        },
        "configuration": {
            "evaluation_k": _K,
            "bm25": {"k1": _K1, "b": _B},
            "content_semantics": "production-unicode-word-span-casefold-v1",
            "filename": (
                "stem unicode-word-span casefold; extension retained but unscored"
            ),
            "full_path": "directory components plus filename stem; extension unscored",
            "combination": (
                "content_bm25_score + separately_normalized_address_bm25_score"
            ),
        },
        "aggregate": {
            "baseline": baseline_metrics,
            "filename": filename_metrics,
            "full_path": path_metrics,
            "filename_delta": _metric_delta(
                left=filename_metrics,
                right=baseline_metrics,
            ),
            "full_path_delta": _metric_delta(left=path_metrics, right=baseline_metrics),
        },
        "cases": [_comparison_payload(comparison=item) for item in comparisons],
    }


def write_report(*, path: Path, payload: dict[str, object]) -> None:
    """Write only the explicitly selected address-evidence experiment artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(arguments: list[str] | None = None) -> None:
    """Run the paired address-evidence comparison once at a caller-selected path."""
    parsed = parse_arguments(arguments)
    baseline_run, comparisons = run_comparison(
        repository_root=parsed.repository_root.resolve(),
    )
    write_report(
        path=parsed.report_path,
        payload=report_payload(baseline_run=baseline_run, comparisons=comparisons),
    )


def _address_contributions(
    *,
    query_terms: tuple[str, ...],
    index: AddressIndex,
) -> dict[int, tuple[AddressContribution, ...]]:
    frequencies = dict(index.document_frequencies)
    postings = dict(index.postings)
    result: dict[int, list[AddressContribution]] = {}
    for term in query_terms:
        term_postings = postings.get(term)
        if term_postings is None:
            continue
        document_frequency = frequencies[term]
        inverse_document_frequency = math.log(
            1
            + (len(index.documents) - document_frequency + 0.5)
            / (document_frequency + 0.5),
        )
        for position, term_frequency in term_postings:
            document_length = index.documents[position].length
            contribution = (
                inverse_document_frequency
                * term_frequency
                * (_K1 + 1)
                / (
                    term_frequency
                    + _K1 * (1 - _B + _B * document_length / index.average_length)
                )
            )
            result.setdefault(position, []).append(
                AddressContribution(
                    normalized_term=term,
                    sources=tuple(
                        dict.fromkeys(
                            observation.source
                            for observation in index.documents[position].observations
                            if observation.normalized_term == term
                        ),
                    ),
                    term_frequency=term_frequency,
                    document_frequency=document_frequency,
                    inverse_document_frequency=inverse_document_frequency,
                    document_length=document_length,
                    average_document_length=index.average_length,
                    contribution=contribution,
                ),
            )
    return {position: tuple(items) for position, items in result.items()}


def _controlled_case(
    *,
    documents: tuple[tuple[str, str], ...],
    query: str,
    relevant: str,
) -> tuple[AddressEvaluation, AddressEvaluation, AddressEvaluation]:
    """Use a local content field to isolate address contributions without I/O."""
    relevant_address = RepositoryResourceAddress(relevant)
    baseline = evaluate_address_matches(
        relevant_addresses=(relevant_address,),
        matches=_controlled_matches(documents=documents, query=query, variant=None),
    )
    filename = evaluate_address_matches(
        relevant_addresses=(relevant_address,),
        matches=_controlled_matches(
            documents=documents,
            query=query,
            variant="filename",
        ),
    )
    path = evaluate_address_matches(
        relevant_addresses=(relevant_address,),
        matches=_controlled_matches(
            documents=documents,
            query=query,
            variant="full-path",
        ),
    )
    return baseline, filename, path


def _controlled_matches(
    *,
    documents: tuple[tuple[str, str], ...],
    query: str,
    variant: str | None,
) -> tuple[AddressMatch, ...]:
    """Rank a tiny fixture with baseline content counts plus optional address BM25.

    Controlled cases are diagnostic only. Real-repository comparisons above use
    the unchanged production BM25 index and score. This local scorer isolates the
    presence or absence of address terms without filesystem acquisition.
    """
    addresses = tuple(
        RepositoryResourceAddress(address) for address, _text in documents
    )
    query_terms = analyze_repository_text_lexical_query(text=query).normalized_terms
    content_scores = {
        RepositoryResourceAddress(address): sum(
            term == query_term
            for _observed, term, _start, _end in iter_lexical_spans(text=text)
            for query_term in query_terms
        )
        for address, text in documents
    }
    if variant is None:
        contributions: dict[int, tuple[AddressContribution, ...]] = {}
    else:
        contributions = _address_contributions(
            query_terms=query_terms,
            index=build_address_index(addresses=addresses, variant=variant),
        )
    return tuple(
        sorted(
            (
                AddressMatch(
                    address=address,
                    content_score=content_scores[address],
                    address_contributions=contributions.get(position, ()),
                    document_position=position,
                )
                for position, address in enumerate(addresses)
                if content_scores[address] > 0 or position in contributions
            ),
            key=lambda item: (-item.score, item.document_position),
        ),
    )


def _baseline_metrics(
    *,
    comparisons: tuple[AddressComparison, ...],
) -> dict[str, float]:
    return {
        "hit_rate_at_k": sum(item.baseline.hit_at_k for item in comparisons)
        / len(comparisons),
        "mean_recall_at_k": sum(item.baseline.recall_at_k for item in comparisons)
        / len(comparisons),
        "mean_reciprocal_rank": sum(
            item.baseline.reciprocal_rank for item in comparisons
        )
        / len(comparisons),
    }


def _variant_metrics(
    *,
    comparisons: tuple[AddressComparison, ...],
    variant: str,
) -> dict[str, float]:
    evaluations = tuple(getattr(item, variant) for item in comparisons)
    return {
        "hit_rate_at_k": sum(item.hit_at_k for item in evaluations) / len(evaluations),
        "mean_recall_at_k": sum(item.recall_at_k for item in evaluations)
        / len(evaluations),
        "mean_reciprocal_rank": sum(item.reciprocal_rank for item in evaluations)
        / len(evaluations),
    }


def _metric_delta(
    *,
    left: dict[str, float],
    right: dict[str, float],
) -> dict[str, float]:
    return {key: left[key] - right[key] for key in left}


def _comparison_payload(*, comparison: AddressComparison) -> dict[str, object]:
    return {
        "name": comparison.name,
        "query": comparison.query_text,
        "relevant_resources": [str(item) for item in comparison.relevant_addresses],
        "baseline": _baseline_payload(evaluation=comparison.baseline),
        "filename": _address_payload(
            evaluation=comparison.filename,
            baseline=comparison.baseline,
        ),
        "full_path": _address_payload(
            evaluation=comparison.full_path,
            baseline=comparison.baseline,
        ),
    }


def _baseline_payload(*, evaluation: Any) -> dict[str, object]:  # noqa: ANN401
    return {
        "ranked_resources": [
            str(item.document_statistics.analysis.document.resource.address)
            for item in evaluation.retrieval_result.matches
        ],
        "relevant_ranks": [
            {"address": str(item.address), "rank": item.rank}
            for item in evaluation.retrieved_relevant_resources
        ],
        "missed": [str(item) for item in evaluation.missed_relevant_resource_addresses],
        "metrics": {
            "hit_at_k": evaluation.hit_at_k,
            "recall_at_k": evaluation.recall_at_k,
            "reciprocal_rank": evaluation.reciprocal_rank,
        },
    }


def _address_payload(
    *,
    evaluation: AddressEvaluation,
    baseline: Any,  # noqa: ANN401 -- dynamic production-script boundary
) -> dict[str, object]:
    """Serialize address contributions and native relevance transitions."""
    baseline_recovered = {
        item.address for item in baseline.retrieved_relevant_resources
    }
    recovered = {address for address, _rank in evaluation.relevant_ranks}
    return {
        "ranked_resources": [
            {
                "address": str(item.address),
                "content_score": item.content_score,
                "address_score": item.address_score,
                "score": item.score,
                "address_contributions": [
                    {
                        "term": part.normalized_term,
                        "sources": list(part.sources),
                        "contribution": part.contribution,
                    }
                    for part in item.address_contributions
                ],
            }
            for item in evaluation.matches
        ],
        "relevant_ranks": [
            {"address": str(address), "rank": rank}
            for address, rank in evaluation.relevant_ranks
        ],
        "missed": [str(item) for item in evaluation.missed],
        "newly_recovered": [
            str(address)
            for address, _rank in evaluation.relevant_ranks
            if address not in baseline_recovered
        ],
        "lost": [
            str(address)
            for address in baseline.retrieved_relevant_resources
            if address.address not in recovered
        ],
        "metrics": {
            "hit_at_k": evaluation.hit_at_k,
            "recall_at_k": evaluation.recall_at_k,
            "reciprocal_rank": evaluation.reciprocal_rank,
        },
    }


def _load_baseline_runner() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "address_comparison_baseline",
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
