# Copyright (c) 2026
# ruff: noqa: COM812, S101, D103, FBT003, PT011 -- controlled fixture assertions and positional boundary fixtures
"""Task-only policy, native safety composition and prospective gate arithmetic."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.codex_dogfood.acquisition.needs import InformationNeed
from experiments.exact_hint_routing.extraction import extract
from experiments.exact_hint_routing.models import HintAssociation
from experiments.exact_hint_routing.routing import resolve
from experiments.exact_hint_routing.serialization import encode
from experiments.exact_hint_routing.tests.conftest import make_frame
from experiments.mechanism_routing.composition import compose
from experiments.mechanism_routing.gates import GateEvidence, evaluate
from experiments.mechanism_routing.policy import (
    Arm,
    IntentRole,
    RoutingBasis,
    classify,
    decide,
    decisions,
)

if TYPE_CHECKING:
    from pathlib import Path


def basis(
    text: str, statement: str = "Inspect existing native fixture contract"
) -> RoutingBasis:
    hint = next(
        d.observation
        for d in extract(LocalizationTaskIdentity("u3-controlled-fixture"), text)
        if d.observation is not None
    )
    obligation = LocalizationObligationIdentity(hint.task, "owner")
    association = HintAssociation(
        hint.identity,
        obligation,
        "Controlled task-only fixture",
        hint.provenance,
    )
    need = InformationNeed(
        "fixture-intent",
        obligation,
        statement,
        "Explicit controlled fixture intent",
        hint.provenance,
    )
    return RoutingBasis(need, hint, association, hint.provenance)


@pytest.mark.parametrize(
    ("statement", "role"),
    [
        ("Inspect existing contract", IntentRole.INSPECT_EXISTING),
        ("Introduce new destination", IntentRole.INTRODUCE_NEW),
        ("Understand conceptual requirement", IntentRole.CONCEPTUAL),
    ],
)
def test_deterministic_classification(statement: str, role: IntentRole) -> None:
    assert classify(statement) is role
    assert classify(statement) is classify(statement)
    with pytest.raises(ValueError, match="grammar"):
        classify("guess relevance from prose")


@pytest.mark.parametrize(
    "text",
    [
        "file `src/pkg/native.py`",
        "module `pkg.native`",
        "function `pkg.native.build`",
        "class `pkg.native.Target`",
        "method `pkg.native.Target.run`",
    ],
)
def test_mechanism_admission_and_isolated_arm_choice(text: str) -> None:
    b = basis(text)
    a, c = decide(Arm.A, b), decide(Arm.C, b)
    assert a.request is None
    assert c.request is not None
    assert decide(Arm.B, b).request == c.request
    assert c.disposition == "EXACT_PLUS_LEXICAL"
    assert c.identity == decide(Arm.C, b).identity
    assert c.identity != decide(Arm.B, b).identity
    assert encode(c) == encode(decide(Arm.C, b))
    assert b.hint is not None
    assert c.basis.provenance == b.hint.provenance
    new = replace(
        b, need=replace(b.need, statement="Introduce new feature destination")
    )
    assert decide(Arm.C, new).request is None
    assert decide(Arm.B, new).request is not None
    conceptual = replace(
        b, need=replace(b.need, statement="Understand source behavior")
    )
    assert decide(Arm.C, conceptual).request is None
    with pytest.raises(ValueError, match="Duplicate"):
        decisions(Arm.C, (b, b))


def test_unsupported_and_unanchored_fallback() -> None:
    b = basis("class `Unqualified`")
    for arm in (Arm.B, Arm.C):
        result = decide(arm, b)
        assert result.request is None
        assert result.disposition == "UNSUPPORTED_WITH_LEXICAL_FALLBACK"
    conceptual = replace(b, hint=None, association=None)
    assert all(decide(arm, conceptual).disposition == "LEXICAL_ONLY" for arm in Arm)


def test_rank_gold_independence_and_foreign_intent_rejection() -> None:
    b = basis("class `pkg.native.Target`")
    before = encode(decide(Arm.C, b))
    # Policy has no result/gold inputs; contaminated inputs fail at the API boundary.
    for keyword in ("rank", "score", "gold", "repository_results"):
        with pytest.raises(TypeError):
            decide(Arm.C, b, **{keyword: 999})
    assert encode(decide(Arm.C, b)) == before
    with pytest.raises(ValueError, match="Foreign"):
        replace(b, provenance=replace(b.provenance, source_identity="foreign"))
    assert b.association is not None
    with pytest.raises(ValueError, match="mismatched"):
        replace(
            b,
            association=replace(
                b.association,
                lane=LocalizationObligationIdentity(b.need.obligation.task, "foreign"),
            ),
        )


@pytest.mark.parametrize("arm", list(Arm))
def test_native_composition_candidate_score_provenance_and_frame_safety(
    tmp_path: Path, arm: Arm
) -> None:
    frame, index = make_frame(tmp_path)
    lexical = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="noise target"),
        index=index,
        maximum_results=len(frame.snapshot.resources),
    )
    b = basis("class `pkg.native.Target`")
    plan = decisions(arm, (b,))
    results = tuple(resolve(frame, d.request) for d in plan if d.request is not None)
    original = encode(lexical)
    view = compose(
        frame, b.need.obligation, lexical, lexical, plan, results, b.provenance
    )
    assert view.original_lexical_acquisition is lexical
    assert view.global_lexical_safety_lane is lexical
    assert encode(lexical) == original
    assert {e.resource.address for e in view.exact_first} >= {
        m.document_statistics.analysis.document.resource.address
        for m in lexical.matches
    }
    assert len({e.resource.address for e in view.exact_first}) == len(view.exact_first)
    for e in view.exact_first:
        if e.lexical_result_reference is not None:
            assert e.native_lexical_rank is not None
            assert (
                e.lexical_result_reference is lexical.matches[e.native_lexical_rank - 1]
            )
    assert encode(view) == encode(view)
    if results:
        for changed in (
            replace(results[0], frame_identity="foreign"),
            replace(results[0], snapshot_id=RepositorySnapshotId("b" * 64)),
        ):
            with pytest.raises(ValueError, match=r"Foreign|Stale|frame"):
                compose(
                    frame,
                    b.need.obligation,
                    lexical,
                    lexical,
                    plan,
                    (changed,),
                    b.provenance,
                )
        with pytest.raises(ValueError, match="resolution"):
            compose(frame, b.need.obligation, lexical, lexical, plan, (), b.provenance)
        with pytest.raises(ValueError, match="resolution"):
            compose(
                frame,
                b.need.obligation,
                lexical,
                lexical,
                plan,
                (*results, *results),
                b.provenance,
            )
        with pytest.raises(ValueError, match="resolution"):
            compose(
                frame,
                b.need.obligation,
                lexical,
                lexical,
                decisions(Arm.A, (b,)),
                results,
                b.provenance,
            )
    with pytest.raises(ValueError, match="Mixed arm"):
        compose(
            frame,
            b.need.obligation,
            lexical,
            lexical,
            (decide(Arm.A, b), decide(Arm.B, b)),
            (),
            b.provenance,
        )
    for stale in (
        replace(frame, snapshot_id=RepositorySnapshotId("a" * 64)),
        replace(
            frame,
            repository_id=RepositoryId.parse("00000000-0000-0000-0000-000000000099"),
        ),
    ):
        with pytest.raises(ValueError):
            compose(
                stale, b.need.obligation, lexical, lexical, plan, results, b.provenance
            )


def test_new_destination_native_fallback_has_no_candidate_loss(tmp_path: Path) -> None:
    frame, index = make_frame(tmp_path)
    b = basis("file `src/new.py`", "Introduce new feature destination")
    lexical = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="target noise"),
        index=index,
        maximum_results=len(frame.snapshot.resources),
    )
    c = compose(
        frame,
        b.need.obligation,
        lexical,
        lexical,
        decisions(Arm.C, (b,)),
        (),
        b.provenance,
    )
    assert tuple(e.lexical_result_reference for e in c.exact_first) == lexical.matches
    selective = decide(Arm.C, b)
    always_on = decide(Arm.B, b)
    forged = replace(selective, request=always_on.request)
    with pytest.raises(ValueError, match="Forged"):
        compose(
            frame,
            b.need.obligation,
            lexical,
            lexical,
            (forged,),
            (),
            b.provenance,
        )
    unsupported = basis("class `Unknown`")
    u = compose(
        frame,
        unsupported.need.obligation,
        lexical,
        lexical,
        decisions(Arm.C, (unsupported,)),
        (),
        unsupported.provenance,
    )
    assert tuple(e.lexical_result_reference for e in u.exact_first) == lexical.matches


def evidence() -> GateEvidence:
    return GateEvidence(
        True,
        True,
        True,
        True,
        True,
        1,
        100,
        75,
        100,
        90,
        100,
        105,
        100,
        100,
        100,
        100,
        True,
    )


def test_frozen_gate_boundaries_precedence_and_equality() -> None:
    e = evidence()
    assert evaluate(e)["outcome"] == "SELECTIVE_MECHANISM_ROUTING_SUPPORTED"
    for changes in (
        {"invocations_c": 76},
        {"mechanism_ns_c": 91},
        {"charged_ns_c": 106},
        {"b_meaningful_gain_count": 0},
        {"preserves_b_gains": False},
    ):
        assert (
            evaluate(replace(e, **changes))["outcome"]
            == "COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER"
        )
    assert (
        evaluate(replace(e, contract_valid=False, router_sound=False))["outcome"]
        == "EXPERIMENTAL_CONTRACT_DEFECT"
    )
    for field in ("router_sound", "reach_safe", "obligation_safe"):
        assert evaluate(replace(e, **{field: False}))["outcome"] == "ROUTER_DEFECT"
    equal = replace(
        e,
        invocations_c=100,
        mechanism_ns_c=100,
        charged_ns_c=100,
        positive_selective_value=False,
    )
    assert evaluate(equal)["outcome"] == "NO_MATERIAL_VALUE"
    assert (
        evaluate(replace(equal, unique_c=90))["outcome"]
        == "SELECTIVE_MECHANISM_ROUTING_SUPPORTED"
    )
    assert evaluate(replace(equal, unique_c=91))["outcome"] == "NO_MATERIAL_VALUE"
    zero = replace(
        equal,
        invocations_b=0,
        invocations_c=0,
        mechanism_ns_b=0,
        mechanism_ns_c=0,
        charged_ns_b=0,
        charged_ns_c=0,
        unique_b=0,
        unique_c=0,
    )
    assert not evaluate(zero)["preserve_b_gains_and_reduce"]
    assert not evaluate(zero)["burden_10_percent_gain_without_cost_increase"]
    with pytest.raises(ValueError, match="negative"):
        replace(e, invocations_b=-1)
