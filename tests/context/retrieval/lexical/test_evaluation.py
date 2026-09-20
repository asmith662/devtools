# Copyright (c) 2026
"""Tests for deterministic evaluation of bounded lexical retrieval results."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25RetrievalResult,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.evaluation import (
    RepositoryTextLexicalRetrievalEvaluationCase,
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

from ._helpers import _collection, _document

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalQuery


def _controlled_index() -> RepositoryTextLexicalInvertedIndex:
    """Build a heterogeneous fixture with deliberate baseline successes and gaps."""
    documents = (
        _document(
            "src/devtools/context/repository/corpus.py",
            "bounded lexical retrieval baseline",
        ),
        _document("docs/architecture.md", "architecture retrieval design"),
        _document("docs/corpus-guide.md", "markdown corpus guide"),
        _document("pyproject.toml", "project configuration tooling"),
        _document("config/context.yaml", "context maximum results"),
        _document("src/identifiers.py", "RepositoryTextCorpus"),
        _document("src/path_signal/repository_corpus.py", "opaque payload"),
        _document("src/cluster/relevant_a.py", "quiet one"),
        _document("src/cluster/relevant_b.py", "quiet two"),
        _document("other/package_noise.py", "package proximity package proximity"),
        _document("docs/intent.md", "uncommon signal"),
        _document(
            "unrelated/noise.py",
            "uncommon signal uncommon signal uncommon signal",
        ),
    )
    collection_analysis = analyze_repository_text_document_collection(
        document_collection=_collection(documents),
    )
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=collection_analysis,
        ),
    )


def _address(value: str) -> RepositoryResourceAddress:
    """Construct one native repository-relative evaluation address."""
    return RepositoryResourceAddress(value)


def _retrieve(
    text: str,
    *,
    index: RepositoryTextLexicalInvertedIndex,
    maximum_results: int = 10,
) -> RepositoryTextLexicalBm25RetrievalResult:
    """Run existing BM25 once so evaluation consumes retained ranked evidence."""
    return retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text=text),
        index=index,
        maximum_results=maximum_results,
    )


def _case(
    query: RepositoryTextLexicalQuery,
    *relevant_addresses: str,
    evaluation_k: int = 5,
) -> RepositoryTextLexicalRetrievalEvaluationCase:
    """Build one explicit binary-relevance case from native resource addresses."""
    return RepositoryTextLexicalRetrievalEvaluationCase(
        query=query,
        relevant_resource_addresses=tuple(
            _address(address) for address in relevant_addresses
        ),
        evaluation_k=evaluation_k,
    )


def test_evaluation_retains_native_relevance_rank_and_missed_resource_evidence() -> (
    None
):
    """A completed evaluation retains its exact result and resource-level outcome."""
    expected_recall = 0.5
    index = _controlled_index()
    retrieval_result = _retrieve("bounded lexical", index=index)
    case = _case(
        retrieval_result.query,
        "src/devtools/context/repository/corpus.py",
        "docs/architecture.md",
    )

    evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=case,
        retrieval_result=retrieval_result,
    )

    assert evaluation.retrieval_result is retrieval_result
    assert evaluation.retrieved_relevant_resources[0].address == _address(
        "src/devtools/context/repository/corpus.py",
    )
    assert evaluation.retrieved_relevant_resources[0].rank == 1
    assert (
        evaluation.retrieved_relevant_resources[0].match is retrieval_result.matches[0]
    )
    assert evaluation.missed_relevant_resource_addresses == (
        _address("docs/architecture.md"),
    )
    assert evaluation.hit_at_k is True
    assert evaluation.recall_at_k == expected_recall
    assert evaluation.reciprocal_rank == 1.0


def test_evaluation_metrics_handle_no_results_short_lists_and_multiple_relevant() -> (
    None
):
    """No retrieval evidence yields zero metrics without hiding designated resources."""
    index = _controlled_index()
    retrieval_result = _retrieve("nonexistent", index=index)
    case = _case(
        retrieval_result.query,
        "docs/corpus-guide.md",
        "pyproject.toml",
        evaluation_k=2,
    )

    evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=case,
        retrieval_result=retrieval_result,
    )

    assert retrieval_result.matches == ()
    assert evaluation.retrieved_relevant_resources == ()
    assert (
        evaluation.missed_relevant_resource_addresses
        == case.relevant_resource_addresses
    )
    assert evaluation.hit_at_k is False
    assert evaluation.recall_at_k == 0.0
    assert evaluation.reciprocal_rank == 0.0


def test_aggregate_metrics_preserve_case_results_and_compute_mrr() -> None:
    """Same-cutoff case results support direct hit-rate, recall, and MRR aggregation."""
    expected_evaluation_k = 2
    expected_aggregate_metric = 0.5
    index = _controlled_index()
    found_result = _retrieve("markdown guide", index=index)
    missed_result = _retrieve("nonexistent", index=index)
    found_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(
            found_result.query,
            "docs/corpus-guide.md",
            evaluation_k=2,
        ),
        retrieval_result=found_result,
    )
    missed_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(
            missed_result.query,
            "docs/corpus-guide.md",
            evaluation_k=2,
        ),
        retrieval_result=missed_result,
    )

    summary = summarize_repository_text_lexical_retrieval_evaluations(
        evaluations=(found_evaluation, missed_evaluation),
    )

    assert summary.evaluations == (found_evaluation, missed_evaluation)
    assert summary.evaluation_k == expected_evaluation_k
    assert summary.hit_rate_at_k == expected_aggregate_metric
    assert summary.mean_recall_at_k == expected_aggregate_metric
    assert summary.mean_reciprocal_rank == expected_aggregate_metric


def test_evaluation_rejects_invalid_cases_and_insufficient_result_evidence() -> None:
    """Impossible designated relevance and unavailable ranks fail explicitly."""
    index = _controlled_index()
    retrieval_result = _retrieve("markdown", index=index, maximum_results=1)
    with pytest.raises(ValueError, match="at least one relevant"):
        _case(retrieval_result.query)
    with pytest.raises(ValueError, match="must be distinct"):
        _case(retrieval_result.query, "docs/corpus-guide.md", "docs/corpus-guide.md")
    with pytest.raises(ValueError, match="K must be positive"):
        _case(retrieval_result.query, "docs/corpus-guide.md", evaluation_k=0)
    with pytest.raises(ValueError, match="must belong"):
        evaluate_repository_text_lexical_bm25_retrieval(
            case=_case(retrieval_result.query, "missing.txt", evaluation_k=1),
            retrieval_result=retrieval_result,
        )
    with pytest.raises(ValueError, match="cannot exceed"):
        evaluate_repository_text_lexical_bm25_retrieval(
            case=_case(
                retrieval_result.query,
                "docs/corpus-guide.md",
                evaluation_k=2,
            ),
            retrieval_result=retrieval_result,
        )
    with pytest.raises(ValueError, match="requires at least one evaluation"):
        summarize_repository_text_lexical_retrieval_evaluations(evaluations=())


def test_summary_rejects_mixed_cutoffs_and_case_query_mismatch() -> None:
    """Aggregate metrics retain a coherent cutoff and result/case query relationship."""
    index = _controlled_index()
    first_result = _retrieve("markdown", index=index)
    second_result = _retrieve("configuration", index=index)
    first_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(first_result.query, "docs/corpus-guide.md", evaluation_k=1),
        retrieval_result=first_result,
    )
    second_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(second_result.query, "pyproject.toml", evaluation_k=2),
        retrieval_result=second_result,
    )

    with pytest.raises(ValueError, match="one shared"):
        summarize_repository_text_lexical_retrieval_evaluations(
            evaluations=(first_evaluation, second_evaluation),
        )
    with pytest.raises(ValueError, match="must equal"):
        evaluate_repository_text_lexical_bm25_retrieval(
            case=_case(second_result.query, "docs/corpus-guide.md"),
            retrieval_result=first_result,
        )


def test_controlled_heterogeneous_cases_measure_strengths_and_known_gaps() -> None:
    """Fixture findings expose content strengths and excluded signals."""
    expected_distractor_rank = 2
    index = _controlled_index()
    strong_result = _retrieve("bounded lexical", index=index)
    markdown_result = _retrieve("markdown guide", index=index)
    configuration_result = _retrieve("PROJECT CONFIGURATION", index=index)
    identifier_result = _retrieve("repository text corpus", index=index)
    path_result = _retrieve("repository corpus", index=index)
    package_result = _retrieve("package proximity", index=index)
    distractor_result = _retrieve("uncommon signal", index=index)

    strong_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(
            strong_result.query,
            "src/devtools/context/repository/corpus.py",
        ),
        retrieval_result=strong_result,
    )
    markdown_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(markdown_result.query, "docs/corpus-guide.md"),
        retrieval_result=markdown_result,
    )
    configuration_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(configuration_result.query, "pyproject.toml"),
        retrieval_result=configuration_result,
    )
    identifier_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(identifier_result.query, "src/identifiers.py"),
        retrieval_result=identifier_result,
    )
    path_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(
            path_result.query,
            "src/path_signal/repository_corpus.py",
        ),
        retrieval_result=path_result,
    )
    package_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(
            package_result.query,
            "src/cluster/relevant_a.py",
            "src/cluster/relevant_b.py",
        ),
        retrieval_result=package_result,
    )
    distractor_evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=_case(distractor_result.query, "docs/intent.md"),
        retrieval_result=distractor_result,
    )

    assert strong_evaluation.hit_at_k is True
    assert markdown_evaluation.hit_at_k is True
    assert configuration_evaluation.hit_at_k is True
    assert identifier_evaluation.hit_at_k is False
    assert path_evaluation.hit_at_k is False
    assert package_evaluation.hit_at_k is False
    assert (
        distractor_evaluation.retrieved_relevant_resources[0].rank
        == expected_distractor_rank
    )


def test_evaluation_is_deterministic_and_performs_no_upstream_or_model_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evaluation only inspects retained result evidence and never reruns retrieval."""
    index = _controlled_index()
    retrieval_result = _retrieve("markdown guide", index=index)
    case = _case(retrieval_result.query, "docs/corpus-guide.md")

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Retrieval evaluation must not perform unrelated work."
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.analysis.analyze_repository_text_document",
        fail,
    )
    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.ast.parse",
        fail,
    )

    first = evaluate_repository_text_lexical_bm25_retrieval(
        case=case,
        retrieval_result=retrieval_result,
    )
    second = evaluate_repository_text_lexical_bm25_retrieval(
        case=case,
        retrieval_result=retrieval_result,
    )

    assert first == second
