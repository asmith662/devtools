# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Snapshot-bound correlation of native lexical and structural evidence."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import (
    RepositoryTextDocumentCollection,
    represent_repository_text_corpus,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.context.retrieval.composition import (
    LexicalStructuralResourceInventory,
    compose_lexical_structural_resource_evidence,
)
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    analyze_repository_text_lexical_query,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25RetrievalResult,
)
from devtools.context.retrieval.structural import (
    PythonDirectStructuralRetrievalRequest,
    PythonDirectStructuralRetrievalResult,
    retrieve_python_direct_structural_resources,
)
from devtools.core.paths import ResolvedPath

from .test_structural import _facts

_PURPOSE = "Locate implementation and its repository neighbors"


def _lexical(
    tmp_path: Path,
    snapshot: RepositorySnapshot,
    *,
    query_text: str = "target unrelated",
) -> RepositoryTextLexicalBm25RetrievalResult:
    discovery = discover_repository_resource_addresses(
        repository=Repository(snapshot.repository_id),
        root=ResolvedPath(tmp_path),
        maximum_resource_count=20,
        maximum_traversal_entry_count=30,
    )
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=tuple(item.address for item in snapshot.resources),
    )
    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)
    collection = represent_repository_text_corpus(corpus=corpus)
    index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=collection,
            ),
        ),
    )
    return retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text=query_text),
        index=index,
        maximum_results=10,
    )


def _inputs(
    tmp_path: Path,
) -> tuple[
    RepositorySnapshot,
    RepositoryTextLexicalBm25RetrievalResult,
    PythonDirectStructuralRetrievalResult,
]:
    snapshot, relation, references, membership = _facts(tmp_path)
    structural = retrieve_python_direct_structural_resources(
        snapshot,
        request=PythonDirectStructuralRetrievalRequest(
            _PURPOSE,
            (
                RepositoryResourceAddress("consumer.py"),
                RepositoryResourceAddress("pkg/target.py"),
            ),
        ),
        imports=(relation,),
        references=references,
        memberships=(membership,),
    )
    return snapshot, _lexical(tmp_path, snapshot), structural


def _compose(
    snapshot: RepositorySnapshot,
    lexical: RepositoryTextLexicalBm25RetrievalResult,
    structural: PythonDirectStructuralRetrievalResult,
    *,
    purpose: str = _PURPOSE,
) -> LexicalStructuralResourceInventory:
    return compose_lexical_structural_resource_evidence(
        snapshot,
        purpose=purpose,
        lexical_result=lexical,
        structural_result=structural,
    )


def test_inventory_correlates_native_evidence_without_ranking_or_parsing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot, lexical, structural = _inputs(tmp_path)
    assert lexical.query.text != _PURPOSE

    def forbid_parse(*_args: object, **_kwargs: object) -> None:
        msg = "Composition must not derive source semantics"
        raise AssertionError(msg)

    monkeypatch.setattr("ast.parse", forbid_parse)
    result = _compose(snapshot, lexical, structural)
    assert result == _compose(snapshot, lexical, structural)
    assert result.snapshot_id == snapshot.id
    assert result.purpose == _PURPOSE
    assert result.lexical_result is lexical
    assert result.structural_result is structural
    assert [item.resource.address.value for item in result.resources] == sorted(
        item.resource.address.value for item in result.resources
    )
    entries = {item.resource.address.value: item for item in result.resources}
    assert entries["unrelated.py"].lexical_match is not None
    assert entries["unrelated.py"].lexical_rank is not None
    assert entries["unrelated.py"].structural_supports == ()
    assert entries["pkg/__init__.py"].lexical_match is None
    assert entries["pkg/__init__.py"].lexical_rank is None
    assert entries["pkg/__init__.py"].structural_supports
    target = entries["pkg/target.py"]
    assert target.lexical_match is not None
    assert target.lexical_match in lexical.matches
    assert target.lexical_rank == lexical.matches.index(target.lexical_match) + 1
    assert len(target.structural_supports) == 4
    assert all(item.snapshot_id == snapshot.id for item in result.resources)


def test_duplicate_presentations_do_not_erase_independent_supports(
    tmp_path: Path,
) -> None:
    snapshot, lexical, structural = _inputs(tmp_path)
    target_candidate = next(
        item for item in structural.candidates
        if item.resource_address == RepositoryResourceAddress("pkg/target.py")
    )
    repeated_structural = replace(
        structural,
        candidates=(*structural.candidates, target_candidate),
    )
    repeated_lexical = replace(lexical, matches=(*lexical.matches, lexical.matches[0]))
    result = _compose(snapshot, repeated_lexical, repeated_structural)
    target = next(
        item for item in result.resources
        if item.resource.address == target_candidate.resource_address
    )
    assert len(target.structural_supports) == len(target_candidate.supports)
    assert [item.fact for item in target.structural_supports] == [
        item.fact for item in target_candidate.supports
    ]
    for item in result.resources:
        if item.lexical_match is not None:
            assert item.lexical_rank == lexical.matches.index(item.lexical_match) + 1
    assert len({item.resource.address for item in result.resources}) == len(
        result.resources,
    )


def test_rejects_stale_lexical_corpus_even_when_match_is_unchanged(
    tmp_path: Path,
) -> None:
    snapshot, _lexical_result, _structural_result = _inputs(tmp_path)
    lexical = _lexical(tmp_path, snapshot, query_text="unrelated")
    (tmp_path / "pkg" / "target.py").write_text(
        "def f():\n    return 1\n", encoding="utf-8",
    )
    newer = observe_repository_resources(
        repository=Repository(snapshot.repository_id),
        root=ResolvedPath(tmp_path),
        addresses=tuple(item.address for item in snapshot.resources),
        maximum_resource_bytes=1024,
    )
    assert newer.id != snapshot.id
    empty_structural = retrieve_python_direct_structural_resources(
        newer,
        request=PythonDirectStructuralRetrievalRequest(
            _PURPOSE,
            (RepositoryResourceAddress("consumer.py"),),
        ),
    )
    with pytest.raises(ValueError, match="Lexical corpus resource differs"):
        _compose(newer, lexical, empty_structural)


def test_rejects_structural_snapshot_and_purpose_mismatch(tmp_path: Path) -> None:
    snapshot, lexical, structural = _inputs(tmp_path)
    with pytest.raises(ValueError, match="snapshot or purpose"):
        _compose(
            snapshot,
            lexical,
            replace(structural, snapshot_id=replace(snapshot.id, value="0" * 64)),
        )
    with pytest.raises(ValueError, match="snapshot or purpose"):
        _compose(snapshot, lexical, structural, purpose="Another information purpose")
    with pytest.raises(ValueError, match="nonempty purpose"):
        _compose(snapshot, lexical, structural, purpose=" ")
    wrong_candidate = replace(
        structural.candidates[0],
        snapshot_id=replace(snapshot.id, value="0" * 64),
    )
    with pytest.raises(ValueError, match="candidate belongs to another snapshot"):
        _compose(
            snapshot,
            lexical,
            replace(
                structural,
                candidates=(wrong_candidate, *structural.candidates[1:]),
            ),
        )


def test_rejects_lexical_corpus_and_index_inconsistency(tmp_path: Path) -> None:
    snapshot, lexical, structural = _inputs(tmp_path)
    statistics = lexical.index.corpus_statistics
    analysis = statistics.collection_analysis
    collection = analysis.document_collection

    def with_collection(
        changed: RepositoryTextDocumentCollection,
    ) -> RepositoryTextLexicalBm25RetrievalResult:
        return replace(
            lexical,
            index=replace(
                lexical.index,
                corpus_statistics=replace(
                    statistics,
                    collection_analysis=replace(
                        analysis,
                        document_collection=changed,
                    ),
                ),
            ),
        )

    other_repository = RepositoryId.parse("00000000-0000-4000-8000-000000000032")
    other_discovery = replace(
        collection.corpus.definition.discovery,
        repository_id=other_repository,
    )
    other_corpus = replace(
        collection.corpus,
        definition=replace(
            collection.corpus.definition,
            discovery=other_discovery,
        ),
    )
    with pytest.raises(ValueError, match="another repository"):
        _compose(
            snapshot,
            with_collection(replace(collection, corpus=other_corpus)),
            structural,
        )
    with pytest.raises(ValueError, match="differ from their observed corpus"):
        _compose(
            snapshot,
            with_collection(replace(collection, documents=collection.documents[:-1])),
            structural,
        )
    wrong_document = replace(
        collection.documents[0],
        repository_id=other_repository,
    )
    with pytest.raises(ValueError, match="document belongs to another repository"):
        _compose(
            snapshot,
            with_collection(
                replace(
                    collection,
                    documents=(wrong_document, *collection.documents[1:]),
                ),
            ),
            structural,
        )
    missing_statistics = replace(
        lexical,
        index=replace(
            lexical.index,
            corpus_statistics=replace(
                statistics,
                document_statistics=statistics.document_statistics[:-1],
            ),
        ),
    )
    with pytest.raises(ValueError, match="statistics differ"):
        _compose(snapshot, missing_statistics, structural)
    foreign_match = replace(
        lexical.matches[0],
        document_statistics=replace(lexical.matches[0].document_statistics),
    )
    with pytest.raises(ValueError, match="absent from its retrieval index"):
        _compose(
            snapshot,
            replace(lexical, matches=(foreign_match,)),
            structural,
        )
    conflicting_match = replace(lexical.matches[0], score=lexical.matches[0].score + 1)
    with pytest.raises(ValueError, match="conflicting matches"):
        _compose(
            snapshot,
            replace(lexical, matches=(lexical.matches[0], conflicting_match)),
            structural,
        )


def test_rejects_lexical_resource_missing_from_snapshot(tmp_path: Path) -> None:
    snapshot, lexical, _structural = _inputs(tmp_path)
    missing_address = RepositoryResourceAddress("unrelated.py")
    reduced = replace(
        snapshot,
        id=replace(snapshot.id, value="0" * 64),
        resources=tuple(
            item for item in snapshot.resources if item.address != missing_address
        ),
    )
    empty_structural = retrieve_python_direct_structural_resources(
        reduced,
        request=PythonDirectStructuralRetrievalRequest(
            _PURPOSE,
            (RepositoryResourceAddress("consumer.py"),),
        ),
    )
    with pytest.raises(ValueError, match="absent from the supplied snapshot"):
        _compose(reduced, lexical, empty_structural)
