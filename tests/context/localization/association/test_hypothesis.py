# Copyright (c) 2026
# ruff: noqa: COM812, D103
"""Unresolved hypothesis algebra and native-frame validation."""

from __future__ import annotations

from dataclasses import replace

import pytest

from devtools.context.localization import (
    Disposition,
    LocalizationAssessment,
    assess_localization_readiness,
)
from devtools.context.localization.association import (
    CandidateWitnessHypothesis,
    CandidateWitnessMember,
    CandidateWitnessView,
    LexicalMatchSupport,
    RoutedMatchSupport,
    WitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.identity import LocalizationObligationIdentity
from devtools.context.localization.lexical import LocalizationLexicalAcquisition
from devtools.context.localization.roles import (
    RepositoryRoleEvidenceView,
    RepositoryRoleKind,
    derive_repository_role_evidence,
)
from devtools.context.localization.routing import (
    LocalizationRoleRoutingView,
    ObligationRolePreference,
    route_localization_lexical_evidence,
)
from devtools.context.localization.task import LocalizationTaskInterpretation
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from tests.context.localization.test_lexical import _execute, _inputs, _query

type Frame = tuple[
    LocalizationTaskInterpretation,
    RepositorySnapshot,
    LocalizationLexicalAcquisition,
    RepositoryRoleEvidenceView,
    LocalizationRoleRoutingView,
]


def _frame() -> Frame:
    task, snapshot, index = _inputs()
    queries = (
        _query(task, "implementation", 0, "Obligation"),
        _query(task, "tests", 1, "Obligation"),
    )
    acquisition = _execute(
        task,
        snapshot,
        index,
        purpose="Locate task witnesses",
        full_query="Obligation",
        queries=queries,
    )
    roles = derive_repository_role_evidence(snapshot)
    routing = route_localization_lexical_evidence(
        acquisition,
        roles,
        tuple(
            ObligationRolePreference(
                query.identity, query.obligation, (RepositoryRoleKind.PYTHON_CODE,)
            )
            for query in queries
        ),
    )
    return task, snapshot, acquisition, roles, routing


def _member(
    frame: Frame,
    address: str = "src/alpha.py",
    *,
    query_index: int = 0,
    role: bool = False,
    routed: bool = False,
) -> CandidateWitnessMember:
    _task, snapshot, acquisition, roles, routing = frame
    target = snapshot.resource_at(RepositoryResourceAddress(address))
    lane = acquisition.obligation_retrievals[query_index]
    rank, match = next(
        (index, item)
        for index, item in enumerate(lane.retrieval.matches, 1)
        if item.document_statistics.analysis.document.resource == target
    )
    routed_lane = routing.obligation_lanes[query_index]
    candidate = next(item for item in routed_lane.candidates if item.match is match)
    return CandidateWitnessMember(
        target,
        "caller observes a plausible witness",
        (LexicalMatchSupport(lane.request.identity, rank, match),),
        roles.for_resource(target.address) if role else (),
        (RoutedMatchSupport(lane.request.identity, candidate),) if routed else (),
    )


def _hypothesis(
    frame: Frame,
    key: str = "a",
    *,
    obligation_index: int = 0,
    members: tuple[CandidateWitnessMember, ...] | None = None,
) -> CandidateWitnessHypothesis:
    task = frame[0]
    return CandidateWitnessHypothesis(
        WitnessHypothesisIdentity(task.obligations[obligation_index].identity, key),
        (_member(frame, query_index=obligation_index),) if members is None else members,
    )


def _view(
    frame: Frame, *hypotheses: CandidateWitnessHypothesis
) -> CandidateWitnessView:
    task, snapshot, acquisition, roles, routing = frame
    return build_candidate_witness_view(
        task=task,
        snapshot=snapshot,
        hypotheses=hypotheses,
        acquisition=acquisition,
        role_evidence=roles,
        routing=routing,
    )


def test_basic_native_support_and_unresolved_boundary() -> None:
    frame = _frame()
    hypothesis = _hypothesis(frame)
    view = _view(frame, hypothesis)
    support = view.hypotheses[0].members[0].lexical[0]
    assert view.for_obligation(hypothesis.identity.obligation) == (hypothesis,)
    assert (
        support.match
        is frame[2].obligation_retrievals[0].retrieval.matches[support.native_rank - 1]
    )
    assert view.acquisition is frame[2]
    assert view.role_evidence is frame[3]
    assert view.routing is frame[4]
    assert not hasattr(hypothesis, "disposition")
    assert not hasattr(hypothesis, "confidence")
    assert not hasattr(view, "accepted_witnesses")
    task, snapshot = frame[:2]
    assessments = tuple(
        LocalizationAssessment(
            item.identity, snapshot.repository_id, snapshot.id, Disposition.OPEN
        )
        for item in task.obligations
    )
    readiness = assess_localization_readiness(
        task=task,
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        assessments=assessments,
    )
    assert not readiness.is_ready
    assert readiness.unresolved_mandatory == tuple(
        item.identity for item in task.obligations
    )


def test_complementarity_competition_and_deterministic_order() -> None:
    frame = _frame()
    first = _member(frame)
    second = _member(frame, "docs/alpha.md")
    combined = _hypothesis(frame, "b", members=(first, second))
    competing = _hypothesis(frame, "a", members=(second,))
    view = _view(frame, combined, competing)
    assert view.hypotheses == (competing, combined)
    assert combined.members == (second, first)
    assert replace(combined, members=(second, first)) == combined
    assert _view(frame, competing, combined) == view
    assert _hypothesis(frame, "b", members=(first,)) != combined


def test_cross_obligation_target_and_obligation_specific_support() -> None:
    frame = _frame()
    first = _hypothesis(frame)
    second = _hypothesis(frame, "other", obligation_index=1)
    view = _view(frame, second, first)
    assert view.for_target(first.members[0].target) == (first, second)
    assert view.cross_obligation_targets == (first.members[0].target,)
    assert first.members[0].lexical[0].query != second.members[0].lexical[0].query


def test_role_and_routing_support_preserve_native_values_without_resolution() -> None:
    frame = _frame()
    member = _member(frame, role=True, routed=True)
    view = _view(frame, _hypothesis(frame, members=(member,)))
    retained = view.hypotheses[0].members[0]
    assert retained.roles == frame[3].for_resource(member.target.address)
    assert retained.routed[0].candidate is frame[4].obligation_lanes[0].candidates[0]
    assert retained.routed[0].candidate.native_rank == retained.lexical[0].native_rank
    assert retained.roles[0].supports
    assert not hasattr(retained, "score")
    assert not hasattr(view, "eliminated")


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ("repository", "Lexical acquisition differs"),
        ("snapshot", "Lexical acquisition differs"),
        ("target", "Candidate target differs"),
        ("unknown_obligation", "unknown obligation"),
        ("foreign_query", "foreign to its obligation"),
        ("stale_role", "Role support is stale"),
        ("foreign_routing", "Routed support is foreign"),
    ],
)
def test_reject_foreign_or_stale_inputs(change: str, message: str) -> None:
    frame = _frame()
    task, snapshot, acquisition, roles, routing = frame
    member = _member(frame, role=True, routed=True)
    hypothesis = _hypothesis(frame, members=(member,))
    if change == "repository":
        snapshot = replace(
            snapshot,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000002"),
        )
    elif change == "snapshot":
        snapshot = replace(snapshot, id=RepositorySnapshotId("b" * 64))
    elif change == "target":
        member = replace(member, target=replace(member.target, content="stale"))
    elif change == "unknown_obligation":
        hypothesis = replace(
            hypothesis,
            identity=WitnessHypothesisIdentity(
                LocalizationObligationIdentity(task.identity, "unknown"), "a"
            ),
        )
    elif change == "foreign_query":
        member = replace(
            member,
            lexical=(
                replace(
                    member.lexical[0],
                    query=acquisition.obligation_retrievals[1].request.identity,
                ),
            ),
        )
    elif change == "stale_role":
        member = replace(
            member,
            roles=(
                replace(member.roles[0], snapshot_id=RepositorySnapshotId("b" * 64)),
            ),
        )
    elif change == "foreign_routing":
        member = replace(
            member,
            routed=(
                replace(
                    member.routed[0],
                    query=acquisition.obligation_retrievals[1].request.identity,
                ),
            ),
        )
    if change in {"target", "foreign_query", "stale_role", "foreign_routing"}:
        hypothesis = replace(hypothesis, members=(member,))
    with pytest.raises(ValueError, match=message):
        build_candidate_witness_view(
            task=task,
            snapshot=snapshot,
            hypotheses=(hypothesis,),
            acquisition=acquisition,
            role_evidence=roles,
            routing=routing,
        )


def test_duplicate_and_empty_semantics() -> None:
    frame = _frame()
    hypothesis = _hypothesis(frame)
    with pytest.raises(ValueError, match="duplicated"):
        _view(frame, hypothesis, hypothesis)
    with pytest.raises(ValueError, match="at least one member"):
        replace(hypothesis, members=())
    with pytest.raises(ValueError, match="repeats a resource"):
        replace(hypothesis, members=(hypothesis.members[0], hypothesis.members[0]))
    with pytest.raises(ValueError, match="reason and positive"):
        replace(hypothesis.members[0], reason="")
    with pytest.raises(ValueError, match="reason and positive"):
        replace(hypothesis.members[0], lexical=())


def test_identity_view_and_support_structure_errors() -> None:
    frame = _frame()
    member = _member(frame, role=True, routed=True)
    hypothesis = _hypothesis(frame, members=(member,))
    view = _view(frame, hypothesis)
    with pytest.raises(ValueError, match="identity must not be blank"):
        WitnessHypothesisIdentity(hypothesis.identity.obligation, " ")
    with pytest.raises(ValueError, match="no such obligation"):
        view.for_obligation(LocalizationObligationIdentity(frame[0].identity, "other"))
    with pytest.raises(ValueError, match="differs from the retained snapshot"):
        view.for_target(replace(member.target, content="changed"))
    with pytest.raises(ValueError, match="repeats a native match"):
        replace(member, lexical=member.lexical * 2)
    with pytest.raises(ValueError, match="repeats a native match"):
        replace(member, routed=member.routed * 2)
    with pytest.raises(ValueError, match="repeats role evidence"):
        replace(member, roles=member.roles * 2)


def test_optional_native_inputs_and_global_lane() -> None:
    task, snapshot, acquisition, roles, routing = _frame()
    empty = build_candidate_witness_view(task=task, snapshot=snapshot, hypotheses=())
    assert empty.hypotheses == ()
    assert empty.cross_obligation_targets == ()
    member = _member((task, snapshot, acquisition, roles, routing), role=True)
    global_match = next(
        (rank, match)
        for rank, match in enumerate(acquisition.full_task_retrieval.matches, 1)
        if match.document_statistics.analysis.document.resource == member.target
    )
    member = replace(member, lexical=(LexicalMatchSupport(None, *global_match),))
    assert build_candidate_witness_view(
        task=task,
        snapshot=snapshot,
        hypotheses=(_hypothesis(_frame(), members=(member,)),),
        acquisition=acquisition,
        role_evidence=roles,
    ).hypotheses
    role_only = replace(member, lexical=())
    assert build_candidate_witness_view(
        task=task,
        snapshot=snapshot,
        hypotheses=(_hypothesis(_frame(), members=(role_only,)),),
        role_evidence=roles,
    ).hypotheses
    routed_only = replace(
        _member((task, snapshot, acquisition, roles, routing), routed=True),
        lexical=(),
    )
    assert build_candidate_witness_view(
        task=task,
        snapshot=snapshot,
        hypotheses=(_hypothesis(_frame(), members=(routed_only,)),),
        acquisition=acquisition,
        role_evidence=roles,
        routing=routing,
    ).hypotheses


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ("no_acquisition", "requires its native acquisition"),
        ("no_roles", "Role support is stale"),
        ("no_routing", "requires its native routing"),
        ("wrong_rank", "foreign to its obligation"),
        ("wrong_match", "foreign to its obligation"),
        ("wrong_lexical_target", "foreign to its obligation"),
        ("wrong_role_target", "Role support is stale"),
        ("detached_role", "Role support is stale"),
        ("wrong_routed_target", "Routed support is foreign"),
        ("missing_target", "does not contain resource address"),
        ("role_frame", "Role evidence differs"),
        ("routing_frame", "Routing view differs"),
    ],
)
def test_support_membership_guards(  # noqa: C901
    change: str, message: str
) -> None:
    frame = _frame()
    task, snapshot, acquisition, roles, routing = frame
    acquisition_input: LocalizationLexicalAcquisition | None = acquisition
    roles_input: RepositoryRoleEvidenceView | None = roles
    routing_input: LocalizationRoleRoutingView | None = routing
    member = _member(frame, role=True, routed=True)
    if change == "no_acquisition":
        acquisition_input = None
        routing_input = None
        member = replace(member, roles=(), routed=())
    elif change == "no_roles":
        roles_input = None
        routing_input = None
        member = replace(member, routed=())
    elif change == "no_routing":
        routing_input = None
    elif change == "wrong_rank":
        member = replace(member, lexical=(replace(member.lexical[0], native_rank=100),))
    elif change == "wrong_match":
        matches = acquisition.obligation_retrievals[0].retrieval.matches
        wrong = matches[0 if member.lexical[0].native_rank != 1 else 1]
        member = replace(member, lexical=(replace(member.lexical[0], match=wrong),))
    elif change == "wrong_lexical_target":
        other = _member(frame, "docs/alpha.md")
        member = replace(member, lexical=other.lexical)
    elif change == "wrong_role_target":
        other = _member(frame, "docs/alpha.md", role=True)
        member = replace(member, roles=other.roles)
    elif change == "detached_role":
        member = replace(member, roles=(replace(member.roles[0]),))
    elif change == "wrong_routed_target":
        other = _member(frame, "docs/alpha.md", routed=True)
        member = replace(member, routed=other.routed)
    elif change == "missing_target":
        member = replace(
            member,
            target=replace(
                member.target, address=RepositoryResourceAddress("missing.py")
            ),
        )
    elif change == "role_frame":
        roles_input = replace(roles, snapshot_id=RepositorySnapshotId("b" * 64))
        routing_input = None
    elif change == "routing_frame":
        routing_input = replace(
            routing,
            global_retrieval=acquisition.obligation_retrievals[0].retrieval,
        )
    with pytest.raises(ValueError, match=message):
        build_candidate_witness_view(
            task=task,
            snapshot=snapshot,
            hypotheses=(_hypothesis(frame, members=(member,)),),
            acquisition=acquisition_input,
            role_evidence=roles_input,
            routing=routing_input,
        )
