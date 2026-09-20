# Copyright (c) 2026
"""Deterministic evaluation of bounded lexical retrieval evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
        RepositoryTextLexicalQuery,
    )


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalRetrievalEvaluationCase:
    """Retain fixture-designated relevant resources for one bounded query evaluation."""

    query: RepositoryTextLexicalQuery
    relevant_resource_addresses: tuple[RepositoryResourceAddress, ...]
    evaluation_k: int

    EVALUATION_SEMANTICS: ClassVar[str] = "binary-designated-relevance-at-k-v1"

    def __post_init__(self) -> None:
        """Require a positive cutoff and at least one distinct designated resource."""
        if self.evaluation_k <= 0:
            msg = "Retrieval evaluation K must be positive."
            raise ValueError(msg)
        if not self.relevant_resource_addresses:
            msg = "Retrieval evaluation requires at least one relevant resource."
            raise ValueError(msg)
        if len(set(self.relevant_resource_addresses)) != len(
            self.relevant_resource_addresses,
        ):
            msg = "Retrieval evaluation relevant resources must be distinct."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalRetrievedRelevantResource:
    """Retain one designated resource recovered at a concrete result rank."""

    address: RepositoryResourceAddress
    rank: int
    match: RepositoryTextLexicalBm25Match


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalRetrievalEvaluationResult:
    """Retain one evaluated ranked result and inspectable binary-relevance evidence."""

    case: RepositoryTextLexicalRetrievalEvaluationCase
    retrieval_result: RepositoryTextLexicalBm25RetrievalResult
    retrieved_relevant_resources: tuple[
        RepositoryTextLexicalRetrievedRelevantResource,
        ...,
    ]
    missed_relevant_resource_addresses: tuple[RepositoryResourceAddress, ...]
    hit_at_k: bool
    recall_at_k: float
    reciprocal_rank: float


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalRetrievalEvaluationSummary:
    """Retain same-cutoff aggregate retrieval metrics and their case results."""

    evaluations: tuple[RepositoryTextLexicalRetrievalEvaluationResult, ...]
    evaluation_k: int
    hit_rate_at_k: float
    mean_recall_at_k: float
    mean_reciprocal_rank: float


def evaluate_repository_text_lexical_bm25_retrieval(
    *,
    case: RepositoryTextLexicalRetrievalEvaluationCase,
    retrieval_result: RepositoryTextLexicalBm25RetrievalResult,
) -> RepositoryTextLexicalRetrievalEvaluationResult:
    """Evaluate one retained BM25 result without rescoring or reacquiring resources."""
    if case.query != retrieval_result.query:
        msg = "Retrieval evaluation case query must equal the retrieval query."
        raise ValueError(msg)
    if case.evaluation_k > retrieval_result.maximum_results:
        msg = "Retrieval evaluation K cannot exceed the retrieval result bound."
        raise ValueError(msg)

    indexed_document_statistics = (
        retrieval_result.index.corpus_statistics.document_statistics
    )
    available_addresses = {
        document_statistics.analysis.document.resource.address
        for document_statistics in indexed_document_statistics
    }
    unknown_addresses = tuple(
        address
        for address in case.relevant_resource_addresses
        if address not in available_addresses
    )
    if unknown_addresses:
        msg = (
            "Retrieval evaluation relevant resources must belong to the indexed "
            "collection."
        )
        raise ValueError(msg)

    relevant_addresses = set(case.relevant_resource_addresses)
    retrieved_relevant_resources = tuple(
        RepositoryTextLexicalRetrievedRelevantResource(
            address=match.document_statistics.analysis.document.resource.address,
            rank=rank,
            match=match,
        )
        for rank, match in enumerate(
            retrieval_result.matches[: case.evaluation_k],
            start=1,
        )
        if match.document_statistics.analysis.document.resource.address
        in relevant_addresses
    )
    retrieved_addresses = {
        retrieved.address for retrieved in retrieved_relevant_resources
    }
    missed_addresses = tuple(
        address
        for address in case.relevant_resource_addresses
        if address not in retrieved_addresses
    )
    first_relevant_rank = (
        retrieved_relevant_resources[0].rank if retrieved_relevant_resources else None
    )
    return RepositoryTextLexicalRetrievalEvaluationResult(
        case=case,
        retrieval_result=retrieval_result,
        retrieved_relevant_resources=retrieved_relevant_resources,
        missed_relevant_resource_addresses=missed_addresses,
        hit_at_k=bool(retrieved_relevant_resources),
        recall_at_k=len(retrieved_relevant_resources)
        / len(case.relevant_resource_addresses),
        reciprocal_rank=0.0 if first_relevant_rank is None else 1 / first_relevant_rank,
    )


def summarize_repository_text_lexical_retrieval_evaluations(
    *,
    evaluations: Sequence[RepositoryTextLexicalRetrievalEvaluationResult],
) -> RepositoryTextLexicalRetrievalEvaluationSummary:
    """Aggregate deterministic same-cutoff hit, recall, and reciprocal-rank metrics."""
    collected_evaluations = tuple(evaluations)
    if not collected_evaluations:
        msg = "Retrieval evaluation summary requires at least one evaluation."
        raise ValueError(msg)
    evaluation_k = collected_evaluations[0].case.evaluation_k
    if any(
        evaluation.case.evaluation_k != evaluation_k
        for evaluation in collected_evaluations
    ):
        msg = "Retrieval evaluation summary requires one shared evaluation K."
        raise ValueError(msg)
    evaluation_count = len(collected_evaluations)
    return RepositoryTextLexicalRetrievalEvaluationSummary(
        evaluations=collected_evaluations,
        evaluation_k=evaluation_k,
        hit_rate_at_k=sum(evaluation.hit_at_k for evaluation in collected_evaluations)
        / evaluation_count,
        mean_recall_at_k=sum(
            evaluation.recall_at_k for evaluation in collected_evaluations
        )
        / evaluation_count,
        mean_reciprocal_rank=sum(
            evaluation.reciprocal_rank for evaluation in collected_evaluations
        )
        / evaluation_count,
    )
