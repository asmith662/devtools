# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Verify stable two-tier views, validation and retained native evidence."""

from dataclasses import replace
from typing import cast

import pytest

from devtools.context.localization import (
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
)
from devtools.context.localization.lexical import LocalizationLexicalAcquisition
from devtools.context.localization.roles import (
    RepositoryRoleKind,
    derive_repository_role_evidence,
)
from devtools.context.localization.routing import (
    ObligationRolePreference,
    RoutingTier,
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

_R = RepositoryRoleKind
_T = RoutingTier
_A = RepositoryResourceAddress


def _acquisition(
    *specifications: tuple[str, int, str],
) -> tuple[
    LocalizationTaskInterpretation,
    RepositorySnapshot,
    LocalizationLexicalAcquisition,
]:
    task, snapshot, index = _inputs()
    queries = tuple(
        _query(task, identity, obligation_index, text)
        for identity, obligation_index, text in specifications
    )
    acquisition = _execute(
        task,
        snapshot,
        index,
        purpose="Complete the caller's task",
        full_query="Obligation",
        queries=queries,
        maximum_results=10,
    )
    return task, snapshot, acquisition


def test_two_tiers_keep_every_native_match_and_explain_preferred_support() -> None:
    _task, snapshot, acquisition = _acquisition(("tests-query", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    request = acquisition.obligation_retrievals[0].request
    routed = route_localization_lexical_evidence(
        acquisition,
        role_view,
        (ObligationRolePreference(request.identity, request.obligation, (_R.TEST,)),),
    )
    lane = routed.obligation_lanes[0]
    native = acquisition.obligation_retrievals[0]
    native_addresses = tuple(
        match.document_statistics.analysis.document.resource.address
        for match in native.retrieval.matches
    )
    assert routed.acquisition is acquisition
    assert routed.global_retrieval is acquisition.full_task_retrieval
    assert routed.global_retrieval == acquisition.full_task_retrieval
    assert lane.native_lane is native
    assert (
        tuple(
            item.match
            for item in sorted(
                lane.candidates,
                key=lambda candidate: candidate.native_rank,
            )
        )
        == native.retrieval.matches
    )
    assert all(
        candidate.match is native.retrieval.matches[candidate.native_rank - 1]
        for candidate in lane.candidates
    )
    assert {
        item.match.document_statistics.analysis.document.resource.address
        for item in lane.preferred
    } == {
        _A("tests/test_alpha.py"),
    }
    assert all(item.tier is _T.PREFERRED_ROLE_SUPPORTED for item in lane.preferred)
    assert all(
        item.tier is _T.ESCAPE and not item.role_evidence for item in lane.escape
    )
    assert tuple(item.native_rank for item in lane.preferred) == tuple(
        sorted(item.native_rank for item in lane.preferred),
    )
    assert tuple(item.native_rank for item in lane.escape) == tuple(
        sorted(item.native_rank for item in lane.escape),
    )
    assert tuple(item.routed_position for item in lane.candidates) == tuple(
        range(1, len(native_addresses) + 1),
    )
    preferred = lane.preferred[0]
    assert preferred.match is native.retrieval.matches[preferred.native_rank - 1]
    assert (
        preferred.match.score
        == native.retrieval.matches[preferred.native_rank - 1].score
    )
    assert tuple(item.role for item in preferred.role_evidence) == (_R.TEST,)
    assert preferred.role_evidence[0].supports == role_view.supports_for(
        _A("tests/test_alpha.py"),
        _R.TEST,
    )


def test_role_union_has_no_evidence_count_priority_and_keeps_native_order() -> None:
    _task, snapshot, acquisition = _acquisition(("union-query", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    request = acquisition.obligation_retrievals[0].request
    routed = route_localization_lexical_evidence(
        acquisition,
        role_view,
        (
            ObligationRolePreference(
                request.identity,
                request.obligation,
                (_R.PYTHON_CODE, _R.TEST),
            ),
        ),
    )
    lane = routed.obligation_lanes[0]
    native = acquisition.obligation_retrievals[0].retrieval.matches
    assert len(lane.preferred) == 2
    assert tuple(item.native_rank for item in lane.preferred) == tuple(
        sorted(item.native_rank for item in lane.preferred),
    )
    test_candidate = next(
        item
        for item in lane.preferred
        if item.match.document_statistics.analysis.document.resource.address
        == _A("tests/test_alpha.py")
    )
    assert tuple(item.role for item in test_candidate.role_evidence) == (
        _R.PYTHON_CODE,
        _R.TEST,
    )
    assert test_candidate.routed_position == next(
        index
        for index, item in enumerate(lane.preferred, start=1)
        if item.native_rank == test_candidate.native_rank
    )
    assert tuple(item.match for item in lane.preferred) == tuple(
        match
        for match in native
        if match.document_statistics.analysis.document.resource.address
        in {_A("src/alpha.py"), _A("tests/test_alpha.py")}
    )
    assert _R.DOCUMENTATION not in {
        item.role for candidate in lane.preferred for item in candidate.role_evidence
    }
    assert not lane.escape[0].role_evidence
    assert lane.escape[
        0
    ].match.document_statistics.analysis.document.resource.address == _A(
        "docs/alpha.md",
    )


def test_empty_preference_is_native_order_in_complete_escape_tier() -> None:
    _task, snapshot, acquisition = _acquisition(("empty-preference", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    request = acquisition.obligation_retrievals[0].request
    routed = route_localization_lexical_evidence(
        acquisition,
        role_view,
        (ObligationRolePreference(request.identity, request.obligation, ()),),
    )
    lane = routed.obligation_lanes[0]
    assert not lane.preferred
    assert (
        tuple(item.match for item in lane.escape)
        == acquisition.obligation_retrievals[0].retrieval.matches
    )
    assert tuple(item.native_rank for item in lane.escape) == tuple(
        range(1, len(lane.escape) + 1),
    )
    assert all(item.tier is _T.ESCAPE for item in lane.escape)


def test_same_obligation_queries_route_independently_without_fusion() -> None:
    _task, snapshot, acquisition = _acquisition(
        ("lane-a", 1, "behavior"),
        ("lane-b", 1, "public interface"),
    )
    query_a, query_b = (item.request for item in acquisition.obligation_retrievals)
    role_view = derive_repository_role_evidence(snapshot)
    preferences = tuple(
        ObligationRolePreference(item.request.identity, item.request.obligation, roles)
        for item, roles in zip(
            acquisition.obligation_retrievals,
            ((_R.TEST,), (_R.DOCUMENTATION,)),
            strict=True,
        )
    )
    routed = route_localization_lexical_evidence(acquisition, role_view, preferences)
    assert tuple(
        item.native_lane.request.identity for item in routed.obligation_lanes
    ) == (
        query_a.identity,
        query_b.identity,
    )
    assert (
        routed.obligation_lanes[0].native_lane is acquisition.obligation_retrievals[0]
    )
    assert (
        routed.obligation_lanes[1].native_lane is acquisition.obligation_retrievals[1]
    )
    assert (
        routed.obligation_lanes[0].native_lane.retrieval
        is not routed.obligation_lanes[1].native_lane.retrieval
    )
    assert all(
        len(lane.candidates) == len(lane.native_lane.retrieval.matches)
        for lane in routed.obligation_lanes
    )


def test_rejects_foreign_stale_and_inconsistent_role_frames() -> None:
    _task, snapshot, acquisition = _acquisition(("frame-query", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    request = acquisition.obligation_retrievals[0].request
    preference = ObligationRolePreference(
        request.identity,
        request.obligation,
        (_R.TEST,),
    )
    with pytest.raises(ValueError, match="repository or snapshot"):
        route_localization_lexical_evidence(
            acquisition,
            replace(role_view, snapshot_id=RepositorySnapshotId("b" * 64)),
            (preference,),
        )
    with pytest.raises(ValueError, match="repository or snapshot"):
        route_localization_lexical_evidence(
            acquisition,
            replace(
                role_view,
                repository_id=RepositoryId.parse(
                    "00000000-0000-4000-8000-000000000099",
                ),
            ),
            (preference,),
        )
    bad_item = replace(
        role_view.evidence[0],
        snapshot_id=RepositorySnapshotId("c" * 64),
    )
    with pytest.raises(ValueError, match="stale, duplicate, or out-of-frame"):
        route_localization_lexical_evidence(
            acquisition,
            replace(role_view, evidence=(bad_item, *role_view.evidence[1:])),
            (preference,),
        )


def test_rejects_bad_preferences_and_query_lane_associations() -> None:
    task, snapshot, acquisition = _acquisition(("pref-query", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    request = acquisition.obligation_retrievals[0].request
    good = ObligationRolePreference(request.identity, request.obligation, (_R.TEST,))
    with pytest.raises(ValueError, match="cover exactly"):
        route_localization_lexical_evidence(acquisition, role_view, ())
    unknown = LocalizationQueryIdentity(task.identity, "unknown")
    with pytest.raises(ValueError, match="cover exactly"):
        route_localization_lexical_evidence(
            acquisition,
            role_view,
            (ObligationRolePreference(unknown, request.obligation, ()),),
        )
    with pytest.raises(ValueError, match="differs from its query lane"):
        route_localization_lexical_evidence(
            acquisition,
            role_view,
            (
                ObligationRolePreference(
                    request.identity,
                    LocalizationObligationIdentity(task.identity, "other"),
                    (),
                ),
            ),
        )
    with pytest.raises(ValueError, match="duplicated query lane"):
        route_localization_lexical_evidence(acquisition, role_view, (good, good))
    with pytest.raises(ValueError, match="unsupported repository role"):
        ObligationRolePreference(
            request.identity,
            request.obligation,
            (cast("RepositoryRoleKind", "TEST"),),
        )
    with pytest.raises(ValueError, match="repeats a preferred role"):
        ObligationRolePreference(
            request.identity,
            request.obligation,
            (_R.TEST, _R.TEST),
        )
    foreign_query = LocalizationQueryIdentity(
        type(task.identity)("foreign-task"),
        "foreign-query",
    )
    with pytest.raises(ValueError, match="share task scope"):
        ObligationRolePreference(foreign_query, request.obligation, ())


def test_rejects_unknown_candidates_duplicate_lane_ids_and_incompatible_results() -> (
    None
):
    task, snapshot, acquisition = _acquisition(("bad-result", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    lane = acquisition.obligation_retrievals[0]
    preference = ObligationRolePreference(
        lane.request.identity,
        lane.request.obligation,
        (_R.TEST,),
    )
    incomplete_view = replace(
        role_view,
        resources=tuple(
            item
            for item in role_view.resources
            if item.address != _A("tests/test_alpha.py")
        ),
        evidence=tuple(
            item
            for item in role_view.evidence
            if item.resource.address != _A("tests/test_alpha.py")
        ),
    )
    with pytest.raises(ValueError, match="absent from the supplied snapshot"):
        route_localization_lexical_evidence(acquisition, incomplete_view, (preference,))
    bad_lane = replace(
        lane,
        request=replace(
            lane.request,
            obligation=LocalizationObligationIdentity(task.identity, "unknown"),
        ),
    )
    with pytest.raises(ValueError, match="invalid query lane"):
        route_localization_lexical_evidence(
            replace(acquisition, obligation_retrievals=(bad_lane,)),
            role_view,
            (preference,),
        )
    duplicate_acquisition = replace(
        acquisition,
        obligation_retrievals=(lane, replace(lane, retrieval=lane.retrieval)),
    )
    with pytest.raises(ValueError, match="invalid query lane"):
        route_localization_lexical_evidence(
            duplicate_acquisition,
            role_view,
            (preference,),
        )
    mismatch = replace(lane, retrieval=replace(lane.retrieval, maximum_results=2))
    with pytest.raises(ValueError, match="do not share acquisition settings"):
        route_localization_lexical_evidence(
            replace(acquisition, obligation_retrievals=(mismatch,)),
            role_view,
            (preference,),
        )


def test_rejects_matches_outside_the_native_index_and_duplicate_resources() -> None:
    _task, snapshot, acquisition = _acquisition(("invalid-match", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    lane = acquisition.obligation_retrievals[0]
    preference = ObligationRolePreference(
        lane.request.identity,
        lane.request.obligation,
        (_R.TEST,),
    )
    original_statistics = lane.retrieval.matches[0].document_statistics
    changed_statistics = replace(
        original_statistics,
        document_length=original_statistics.document_length + 1,
    )
    foreign_match = replace(
        lane.retrieval.matches[0],
        document_statistics=changed_statistics,
    )
    outside_result = replace(
        lane.retrieval,
        matches=(foreign_match, *lane.retrieval.matches[1:]),
    )
    with pytest.raises(ValueError, match="absent from its native retrieval index"):
        route_localization_lexical_evidence(
            replace(
                acquisition,
                obligation_retrievals=(replace(lane, retrieval=outside_result),),
            ),
            role_view,
            (preference,),
        )
    duplicate_result = replace(
        lane.retrieval,
        matches=(lane.retrieval.matches[0], lane.retrieval.matches[0]),
    )
    with pytest.raises(ValueError, match="repeats a resource candidate"):
        route_localization_lexical_evidence(
            replace(
                acquisition,
                obligation_retrievals=(replace(lane, retrieval=duplicate_result),),
            ),
            role_view,
            (preference,),
        )


def test_rejects_duplicate_or_out_of_frame_role_support_data() -> None:
    _task, snapshot, acquisition = _acquisition(("bad-role", 1, "Obligation"))
    role_view = derive_repository_role_evidence(snapshot)
    lane = acquisition.obligation_retrievals[0]
    preference = ObligationRolePreference(
        lane.request.identity,
        lane.request.obligation,
        (_R.TEST,),
    )
    with pytest.raises(ValueError, match="repeats a resource address"):
        route_localization_lexical_evidence(
            acquisition,
            replace(role_view, resources=role_view.resources * 2),
            (preference,),
        )
    repeated = replace(
        role_view,
        evidence=(*role_view.evidence, role_view.evidence[0]),
    )
    with pytest.raises(ValueError, match="stale, duplicate, or out-of-frame"):
        route_localization_lexical_evidence(acquisition, repeated, (preference,))
    support = replace(role_view.evidence[0].supports[0], source_address=_A("ghost.py"))
    evidence = replace(role_view.evidence[0], supports=(support,))
    with pytest.raises(ValueError, match="source is outside the retained frame"):
        route_localization_lexical_evidence(
            acquisition,
            replace(role_view, evidence=(evidence, *role_view.evidence[1:])),
            (preference,),
        )
