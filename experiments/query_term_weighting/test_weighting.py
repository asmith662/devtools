# Copyright (c) 2026
# ruff: noqa: S101, PLR2004, COM812, PT011 -- varied mutation paths share one rejection contract
"""Synthetic contracts, never the prospective case's ranking or gold oracle."""

from __future__ import annotations

import json
from dataclasses import replace

import pytest

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
    TaskTextSpan,
)
from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25RetrievalResult,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from experiments.query_term_weighting.classification import (
    AnchorCopy,
    Arm,
    QueryPolicy,
    Role,
    classify,
)
from experiments.query_term_weighting.scoring import require_identical_candidates, score
from experiments.query_term_weighting.serialization import trace
from tests.context.retrieval.lexical._helpers import _collection, _document


def policy(text: str = "implement Anchor semantic implement") -> QueryPolicy:
    """Supply exact synthetic task/query-only source spans."""
    task_id = LocalizationTaskIdentity("synthetic-weighting")
    task = "implement `Anchor` semantic implement"
    start = task.index("Anchor")
    query_start = text.index("Anchor")
    return classify(
        identity=LocalizationQueryIdentity(task_id, "Q"),
        obligation=LocalizationObligationIdentity(task_id, "O"),
        query_text=text,
        task_text=task,
        source=TaskProvenance(task_id, TaskTextSpan(0, len(task))),
        anchors=(
            AnchorCopy(
                query_start,
                query_start + 6,
                TaskProvenance(task_id, TaskTextSpan(start, start + 6)),
            ),
        ),
    )


def native(p: QueryPolicy) -> RepositoryTextLexicalBm25RetrievalResult:
    """Build only a tiny synthetic native combined-channel fixture."""
    collection = _collection(
        (
            _document("a/Anchor.py", "Anchor semantic"),
            _document("b/implement.py", "implement implement semantic"),
            _document("c/tie.py", "semantic"),
            _document("d/tie.py", "semantic"),
            _document("e/absent.py", "unrelated"),
            _document("f/Anchor.py", ""),
        )
    )
    analysis = analyze_repository_text_document_collection(
        document_collection=collection
    )
    index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analysis
        )
    )
    return retrieve_repository_text_documents_by_bm25(
        query=p.native_query, index=index, maximum_results=6
    )


def test_task_only_classification_and_duplicate_semantics() -> None:
    """All three roles retain exact observations and one multiplier per term."""
    p = policy()
    p.validate()
    assert tuple(t.role for t in p.terms) == (
        Role.GENERIC_OPERATION,
        Role.EXPLICIT_ANCHOR,
        Role.SEMANTIC,
    )
    assert tuple(t.multipliers for t in p.terms) == ((1, 1, 0.5), (1, 2, 2), (1, 1, 1))
    assert len(p.terms[0].observations) == 2
    assert p == policy()
    assert not any(
        s in json.dumps(trace(score(native(p), p, Arm.C))["query_policy"])
        for s in ("document_frequency", "rank", "gold", "witness")
    )


@pytest.mark.parametrize("mutation", ["role", "analysis", "weight", "foreign"])
def test_policy_tamper_rejected(mutation: str) -> None:
    """Classifier replay rejects changed term identity, weights and task scope."""
    p = policy()
    if mutation == "role":
        p = replace(p, terms=(replace(p.terms[0], role=Role.SEMANTIC), *p.terms[1:]))
    elif mutation == "weight":
        p = replace(p, terms=(replace(p.terms[0], multipliers=(1, 1, 0)), *p.terms[1:]))
    elif mutation == "analysis":
        p = replace(
            p,
            native_query=replace(
                p.native_query, observations=p.native_query.observations[:-1]
            ),
        )
    else:
        p = replace(
            p,
            obligation=LocalizationObligationIdentity(
                LocalizationTaskIdentity("foreign"), "O"
            ),
        )
    with pytest.raises(ValueError):
        p.validate()


def test_ambiguous_partial_foreign_anchor_rejected() -> None:
    """Only complete exact task-marked query literals can establish anchors."""
    p = policy()
    for anchors in (
        (p.anchors[0], p.anchors[0]),
        (replace(p.anchors[0], query_end=p.anchors[0].query_end - 1),),
        (
            replace(
                p.anchors[0],
                task_provenance=TaskProvenance("foreign", TaskTextSpan(0, 1)),
            ),
        ),
    ):
        with pytest.raises(ValueError):
            classify(
                identity=p.identity,
                obligation=p.obligation,
                query_text=p.native_query.text,
                task_text=p.task_text,
                source=p.source,
                anchors=anchors,
            )


def test_scores_candidates_native_provenance_and_ties() -> None:
    """Both channels reconstruct; candidates and original statistics never change."""
    p = policy()
    n = native(p)
    before = repr(n.index)
    results = tuple(score(n, p, a) for a in Arm)
    require_identical_candidates(results)
    assert tuple(m.score for m in results[0].matches) == tuple(
        m.score for m in n.matches
    )
    for result in results:
        assert result.native_result is n
        for match in result.matches:
            assert any(match.native_match is original for original in n.matches)
            content = sum(
                v.weighted for v in match.contributions if v.channel == "content"
            )
            filename = sum(
                v.weighted for v in match.contributions if v.channel == "filename"
            )
            assert match.score == content + 0.25 * filename
            assert all(
                v.weighted == v.native * v.multiplier for v in match.contributions
            )
        tied = [
            m.collection_position
            for m in result.matches
            if str(
                m.native_match.document_statistics.analysis.document.resource.address
            ).endswith("tie.py")
        ]
        assert tied == [2, 3]
        assert trace(result) == trace(result)
        assert json.loads(json.dumps(trace(result), sort_keys=True)) == trace(result)
    assert repr(n.index) == before
    assert results[0].policy.native_query is p.native_query
    assert {m.collection_position for m in results[0].matches} == {0, 1, 2, 3, 5}
    assert tuple(
        t.multiplier
        for m in results[1].matches
        for t in m.contributions
        if t.role is Role.GENERIC_OPERATION
    ) == (1, 1)


def test_result_candidate_query_and_bound_tamper_rejected() -> None:
    """Recover positive candidates from postings and reject altered result traces."""
    p = policy()
    n = native(p)
    result = score(n, p, Arm.C)
    for damaged in (
        replace(result, matches=result.matches[:-1]),
        replace(
            result, matches=(replace(result.matches[0], score=0), *result.matches[1:])
        ),
    ):
        with pytest.raises(ValueError):
            damaged.validate()
    for damaged_native in (
        replace(n, matches=n.matches[:-1]),
        replace(n, matches=(*n.matches, n.matches[0])),
        replace(n, maximum_results=1),
        replace(n, query=policy("Anchor semantic").native_query),
    ):
        with pytest.raises(ValueError):
            score(damaged_native, p, Arm.C)
    with pytest.raises(ValueError):
        require_identical_candidates((result, score(native(p), p, Arm.B)))


def test_no_canonical_subtoken_expansion_or_query_frequency_weight() -> None:
    """Identifier underscores/case stay whole and duplicate terms do not boost A."""
    p = policy("Anchor semantic implement FooBar snake_case dotted.name")
    assert p.native_query.normalized_terms == (
        "anchor",
        "semantic",
        "implement",
        "foobar",
        "snake_case",
        "dotted",
        "name",
    )
    a = native(policy("Anchor semantic implement"))
    b = native(policy("Anchor semantic implement implement"))
    assert tuple(m.score for m in a.matches) == tuple(m.score for m in b.matches)


def test_native_term_statistics_tamper_and_arm_isolation() -> None:
    """Native DF/contributions must reconstruct from unchanged native statistics."""
    p = policy()
    n = native(p)
    first = next(m for m in n.matches if m.term_contributions)
    changed = replace(
        first,
        term_contributions=(
            replace(first.term_contributions[0], document_frequency=99),
            *first.term_contributions[1:],
        ),
    )
    damaged = replace(n, matches=tuple(changed if m is first else m for m in n.matches))
    with pytest.raises(ValueError, match="statistics tamper"):
        score(damaged, p, Arm.B)
    a, b, c = (score(n, p, arm) for arm in Arm)
    for result in (a, b, c):
        for match in result.matches:
            for term in match.contributions:
                if term.role is Role.SEMANTIC:
                    assert term.multiplier == 1
                elif term.role is Role.EXPLICIT_ANCHOR:
                    assert term.multiplier == (1 if result.arm is Arm.A else 2)
                else:
                    assert term.multiplier == (0.5 if result.arm is Arm.C else 1)
