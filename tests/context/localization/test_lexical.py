# Copyright (c) 2026
# ruff: noqa: D103, PLR0913, PLR2004
"""Production BM25 acquisition and obligation-association contract tests."""

from __future__ import annotations

from dataclasses import replace

import pytest

from devtools.context.localization import (
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationLexicalAcquisition,
    LocalizationLexicalAcquisitionRequest,
    LocalizationObligation,
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    ObligationLexicalQuery,
    RequirementStatus,
    SatisfactionCriterion,
    TaskProvenance,
    WitnessSet,
    acquire_localization_lexical_evidence,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.context.retrieval.lexical import (
    RepositoryTextLexicalBm25Settings,
    RepositoryTextLexicalInvertedIndex,
    analyze_repository_text_document_collection,
    analyze_repository_text_lexical_query,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
    retrieve_repository_text_documents_by_bm25,
)
from tests.context.retrieval.lexical._helpers import _collection, _document

_REPOSITORY = RepositoryId.parse("00000000-0000-4000-8000-000000000001")
_SNAPSHOT = RepositorySnapshotId("a" * 64)


def _inputs() -> tuple[
    LocalizationTaskInterpretation,
    RepositorySnapshot,
    RepositoryTextLexicalInvertedIndex,
]:
    documents = _collection(
        (
            _document("src/alpha.py", "Obligation implement interface"),
            _document("tests/test_alpha.py", "Obligation test behavior"),
            _document("docs/alpha.md", "Obligation public interface"),
        ),
    )
    snapshot = RepositorySnapshot(
        _SNAPSHOT,
        _REPOSITORY,
        tuple(document.resource for document in documents.documents),
    )
    index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=documents,
            ),
        ),
    )
    task_id = LocalizationTaskIdentity("task-1")
    anchor_id = LocalizationAnchorIdentity(task_id, "Obligation")
    provenance = TaskProvenance("prompt", None, "caller interpretation")
    obligations = tuple(
        LocalizationObligation(
            LocalizationObligationIdentity(task_id, name),
            predicate,
            (anchor_id,),
            provenance,
            RequirementStatus.MANDATORY,
            SatisfactionCriterion("caller-defined", "native evidence establishes it"),
            (WitnessSet((f"target:{name}",)),),
        )
        for name, predicate in (
            ("implementation", "locate implementation"),
            ("tests", "locate tests"),
        )
    )
    task = LocalizationTaskInterpretation(
        task_id,
        provenance,
        (LocalizationAnchor(anchor_id, "Obligation", provenance),),
        obligations,
    )
    return task, snapshot, index


def _query(
    task: LocalizationTaskInterpretation,
    key: str,
    obligation_index: int,
    text: str,
) -> ObligationLexicalQuery:
    return ObligationLexicalQuery(
        LocalizationQueryIdentity(task.identity, key),
        task.obligations[obligation_index].identity,
        text,
    )


def _acquire(
    *,
    full_query: str = "Implement Obligation across repository",
    queries: tuple[ObligationLexicalQuery, ...] = (),
) -> tuple[
    LocalizationTaskInterpretation,
    RepositorySnapshot,
    RepositoryTextLexicalInvertedIndex,
    LocalizationLexicalAcquisition,
]:
    task, snapshot, index = _inputs()
    result = _execute(
        task,
        snapshot,
        index,
        purpose="Complete the caller's task",
        full_query=full_query,
        queries=queries,
        maximum_results=10,
    )
    return task, snapshot, index, result


def _execute(
    task: LocalizationTaskInterpretation,
    snapshot: RepositorySnapshot,
    index: RepositoryTextLexicalInvertedIndex,
    *,
    purpose: str,
    full_query: str,
    queries: tuple[ObligationLexicalQuery, ...] = (),
    maximum_results: int = 10,
) -> LocalizationLexicalAcquisition:
    return acquire_localization_lexical_evidence(
        LocalizationLexicalAcquisitionRequest(
            task=task,
            purpose=purpose,
            full_task_query=full_query,
            obligation_queries=queries,
            snapshot=snapshot,
            index=index,
            maximum_results=maximum_results,
        ),
    )


def test_full_task_query_is_verbatim_and_native_bm25_is_retained() -> None:
    text = "\n Implement Obligation across repository \t"
    task, snapshot, index, result = _acquire(full_query=text)
    expected_native = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text=text),
        index=index,
        maximum_results=10,
        settings=RepositoryTextLexicalBm25Settings(),
    )

    assert result.task is task
    assert result.purpose == "Complete the caller's task"
    assert result.repository_id == snapshot.repository_id
    assert result.snapshot_id == snapshot.id
    assert result.full_task_retrieval == expected_native
    assert result.full_task_retrieval.query.text == text
    assert result.full_task_retrieval.index is index
    assert result.full_task_retrieval.settings == RepositoryTextLexicalBm25Settings()
    assert result.full_task_retrieval.maximum_results == 10
    assert result.obligation_retrievals == ()


def test_native_rank_order_and_tie_order_are_preserved() -> None:
    _task, _snapshot, index, result = _acquire(full_query="Obligation")
    expected = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="Obligation"),
        index=index,
        maximum_results=10,
    )

    assert result.full_task_retrieval.matches == expected.matches
    assert tuple(
        (rank, match.document_statistics.analysis.document.resource.address.value)
        for rank, match in enumerate(result.full_task_retrieval.matches, start=1)
    ) == tuple(
        (rank, match.document_statistics.analysis.document.resource.address.value)
        for rank, match in enumerate(expected.matches, start=1)
    )
    assert all(match.term_contributions for match in expected.matches)


def test_native_filename_evidence_is_retained_without_reinterpretation() -> None:
    _task, _snapshot, _index, result = _acquire(full_query="alpha")
    native = result.full_task_retrieval

    assert native.filename_index is not None
    assert native.matches
    assert all(match.filename_term_contributions for match in native.matches)
    assert all(match.filename_weight == 0.25 for match in native.matches)
    assert all(
        match.score == match.content_score + match.weighted_filename_score
        for match in native.matches
    )


def test_explicit_obligation_lanes_retain_identity_text_order_and_native_results() -> (
    None
):
    task, _snapshot, index = _inputs()
    requests = (
        _query(task, "implementation-query", 0, "Obligation implement"),
        _query(task, "test-query", 1, "Obligation test"),
        _query(task, "implementation-followup", 0, "interface"),
    )
    _same_task, snapshot, _same_index = _inputs()
    result = _execute(
        task,
        snapshot,
        index=index,
        purpose="Implement and validate Obligation",
        full_query="Full original task text remains intact.",
        queries=requests,
        maximum_results=5,
    )

    assert tuple(item.request for item in result.obligation_retrievals) == requests
    assert tuple(
        item.request.identity.value for item in result.obligation_retrievals
    ) == (
        "implementation-query",
        "test-query",
        "implementation-followup",
    )
    assert tuple(
        item.retrieval.query.text for item in result.obligation_retrievals
    ) == (
        "Obligation implement",
        "Obligation test",
        "interface",
    )
    assert all(item.retrieval.index is index for item in result.obligation_retrievals)
    assert all(
        item.retrieval.maximum_results == 5 for item in result.obligation_retrievals
    )
    assert (
        result.obligation_retrievals[0].request.obligation
        == task.obligations[0].identity
    )
    assert (
        result.obligation_retrievals[1].request.obligation
        == task.obligations[1].identity
    )


def test_same_resource_remains_independent_across_lanes_without_fusion() -> None:
    task_for_query, _snapshot, _index = _inputs()
    request = _query(task_for_query, "obligation-query", 0, "Obligation")
    task, _snapshot, _index, result = _acquire(
        full_query="Obligation",
        queries=(request,),
    )
    global_matches = result.full_task_retrieval.matches
    obligation_matches = result.obligation_retrievals[0].retrieval.matches
    global_top = global_matches[0]
    obligation_top = obligation_matches[0]

    assert global_top.document_statistics.analysis.document.resource.address == (
        obligation_top.document_statistics.analysis.document.resource.address
    )
    assert result.full_task_retrieval is not result.obligation_retrievals[0].retrieval
    assert result.full_task_retrieval.matches == obligation_matches
    assert not hasattr(result, "fused_matches")
    assert not hasattr(result.obligation_retrievals[0], "agreement_bonus")
    assert not hasattr(result.obligation_retrievals[0], "satisfied")
    assert result.task.obligations[0].identity == task.obligations[0].identity


def test_empty_query_and_zero_hit_query_remain_positive_acquisition_records() -> None:
    task, _snapshot, _index = _inputs()
    empty_result = _acquire(full_query="")[3]
    zero_request = _query(task, "zero", 1, "zz-no-such-term-zz")
    _task, _snapshot, _index, zero_result = _acquire(
        full_query="Original task",
        queries=(zero_request,),
    )

    assert empty_result.full_task_retrieval.query.text == ""
    assert empty_result.full_task_retrieval.matches == ()
    assert len(zero_result.obligation_retrievals) == 1
    assert zero_result.obligation_retrievals[0].retrieval.matches == ()
    assert zero_result.obligation_retrievals[0].request is zero_request
    assert not hasattr(zero_result.obligation_retrievals[0], "non_applicable")


def test_obligation_without_query_is_unchanged_in_supplied_frame() -> None:
    request = _query(_inputs()[0], "one", 0, "implement")
    task, _snapshot, _index, result = _acquire(queries=(request,))

    assert result.task.obligations[1].identity == task.obligations[1].identity
    assert all(
        item.request.obligation != task.obligations[1].identity
        for item in result.obligation_retrievals
    )
    assert not hasattr(result, "readiness")


def test_invalid_task_or_obligation_query_associations_are_rejected() -> None:
    task, snapshot, index = _inputs()
    unknown = ObligationLexicalQuery(
        LocalizationQueryIdentity(task.identity, "unknown-obligation-query"),
        LocalizationObligationIdentity(task.identity, "unknown"),
        "unknown",
    )
    foreign = ObligationLexicalQuery(
        LocalizationQueryIdentity(LocalizationTaskIdentity("other"), "foreign"),
        LocalizationObligationIdentity(LocalizationTaskIdentity("other"), "other"),
        "foreign",
    )
    duplicate = _query(task, "duplicate", 0, "one")
    with pytest.raises(ValueError, match="unknown obligation"):
        _execute(
            task,
            snapshot,
            index,
            purpose="purpose",
            full_query="task",
            queries=(unknown,),
            maximum_results=5,
        )
    with pytest.raises(ValueError, match="foreign task"):
        _execute(
            task,
            snapshot,
            index,
            purpose="purpose",
            full_query="task",
            queries=(foreign,),
            maximum_results=5,
        )
    with pytest.raises(ValueError, match="duplicated"):
        _execute(
            task,
            snapshot,
            index,
            purpose="purpose",
            full_query="task",
            queries=(duplicate, replace(duplicate, text="second query")),
            maximum_results=5,
        )
    with pytest.raises(ValueError, match="task scope"):
        ObligationLexicalQuery(
            LocalizationQueryIdentity(task.identity, "mismatched"),
            LocalizationObligationIdentity(LocalizationTaskIdentity("other"), "x"),
            "query",
        )
    with pytest.raises(ValueError, match="query key"):
        LocalizationQueryIdentity(task.identity, " ")


def test_empty_obligation_lanes_are_allowed_but_purpose_must_be_present() -> None:
    task, snapshot, index = _inputs()
    result = _execute(
        task,
        snapshot,
        index=index,
        purpose="purpose",
        full_query="whole task",
        queries=(),
        maximum_results=2,
    )
    with pytest.raises(ValueError, match="task purpose"):
        _execute(
            task,
            snapshot,
            index,
            purpose=" ",
            full_query="whole task",
            queries=(),
            maximum_results=2,
        )

    assert result.obligation_retrievals == ()


def test_snapshot_and_repository_mismatch_are_rejected() -> None:
    task, snapshot, index = _inputs()
    absent_snapshot = replace(snapshot, resources=())
    other_repository = RepositoryId.parse("00000000-0000-4000-8000-000000000002")
    foreign_snapshot = replace(snapshot, repository_id=other_repository)
    for supplied_snapshot, message in (
        (absent_snapshot, "absent from the supplied snapshot"),
        (foreign_snapshot, "another repository"),
    ):
        with pytest.raises(ValueError, match=message):
            _execute(
                task,
                supplied_snapshot,
                index,
                purpose="purpose",
                full_query="task",
                queries=(),
                maximum_results=3,
            )


def test_task_purpose_is_not_replaced_by_query_text() -> None:
    _task, _snapshot, _index, result = _acquire(
        full_query="Complete different original prompt text",
    )

    assert result.purpose == "Complete the caller's task"
    assert result.full_task_retrieval.query.text != result.purpose
