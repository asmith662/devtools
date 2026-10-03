# Copyright (c) 2026
"""Deterministically partition existing obligation lanes by caller preference."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.localization.roles.models import (
    RepositoryRoleKind,
    RoleSupportKind,
)
from devtools.context.localization.routing.models import (
    LocalizationRoleRoutingView,
    ObligationRolePreference,
    RoutedLexicalCandidate,
    RoutedObligationLane,
    RoutingTier,
)
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.context.retrieval.composition import require_lexical_result_snapshot

if TYPE_CHECKING:
    from devtools.context.localization.identity import LocalizationQueryIdentity
    from devtools.context.localization.lexical import (
        LocalizationLexicalAcquisition,
        ObligationLexicalEvidence,
    )
    from devtools.context.localization.roles.models import (
        RepositoryRoleEvidenceView,
    )
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
    )


def route_localization_lexical_evidence(
    acquisition: LocalizationLexicalAcquisition,
    role_evidence: RepositoryRoleEvidenceView,
    preferences: tuple[ObligationRolePreference, ...],
) -> LocalizationRoleRoutingView:
    """Create lossless per-query views; never acquire, fuse, satisfy or eliminate.

    A candidate is preferred when any caller-selected role has positive support.
    Both tiers preserve the native match order, and the complete full-task result
    remains untouched on the returned view.
    """
    _validate_frame(acquisition, role_evidence)
    snapshot = RepositorySnapshot(
        role_evidence.snapshot_id,
        role_evidence.repository_id,
        role_evidence.resources,
    )
    _validate_role_evidence(role_evidence)
    _validate_native_acquisition(acquisition, snapshot)
    preferences_by_query = _validate_preferences(acquisition, preferences)
    lanes = tuple(
        _route_lane(lane, preferences_by_query[lane.request.identity], role_evidence)
        for lane in acquisition.obligation_retrievals
    )
    return LocalizationRoleRoutingView(
        acquisition,
        acquisition.full_task_retrieval,
        role_evidence,
        lanes,
    )


def _validate_frame(
    acquisition: LocalizationLexicalAcquisition,
    role_evidence: RepositoryRoleEvidenceView,
) -> None:
    if (
        acquisition.repository_id != role_evidence.repository_id
        or acquisition.snapshot_id != role_evidence.snapshot_id
    ):
        msg = "Role evidence belongs to another repository or snapshot."
        raise ValueError(msg)


def _validate_role_evidence(role_evidence: RepositoryRoleEvidenceView) -> None:
    resources = {item.address: item for item in role_evidence.resources}
    if len(resources) != len(role_evidence.resources):
        msg = "Role evidence frame repeats a resource address."
        raise ValueError(msg)
    seen: set[tuple[RepositoryResourceAddress, RepositoryRoleKind]] = set()
    for evidence in role_evidence.evidence:
        key = (evidence.resource.address, evidence.role)
        if (
            evidence.repository_id != role_evidence.repository_id
            or evidence.snapshot_id != role_evidence.snapshot_id
            or evidence.derivation_identity != role_evidence.derivation_identity
            or evidence.resource != resources.get(evidence.resource.address)
            or not isinstance(evidence.role, RepositoryRoleKind)
            or key in seen
            or not evidence.supports
        ):
            msg = "Role evidence contains stale, duplicate, or out-of-frame data."
            raise ValueError(msg)
        seen.add(key)
        for support in evidence.supports:
            if (
                not isinstance(support.kind, RoleSupportKind)
                or support.source_address not in resources
            ):
                msg = "Role support kind or source is outside the retained frame."
                raise ValueError(msg)


def _validate_native_acquisition(
    acquisition: LocalizationLexicalAcquisition,
    snapshot: RepositorySnapshot,
) -> None:
    global_result = acquisition.full_task_retrieval
    require_lexical_result_snapshot(snapshot, global_result)
    _validate_result_matches(global_result)
    obligation_ids = {item.identity for item in acquisition.task.obligations}
    query_ids = set()
    for lane in acquisition.obligation_retrievals:
        if (
            lane.request.identity.task != acquisition.task.identity
            or lane.request.obligation not in obligation_ids
            or lane.request.identity in query_ids
        ):
            msg = "Localization acquisition contains an invalid query lane."
            raise ValueError(msg)
        query_ids.add(lane.request.identity)
        result = lane.retrieval
        if (
            result.index != global_result.index
            or result.filename_index != global_result.filename_index
            or result.settings != global_result.settings
            or result.maximum_results != global_result.maximum_results
        ):
            msg = "Localization query lanes do not share acquisition settings."
            raise ValueError(msg)
        require_lexical_result_snapshot(snapshot, result)
        _validate_result_matches(result)


def _validate_result_matches(
    result: RepositoryTextLexicalBm25RetrievalResult,
) -> None:
    statistics = result.index.corpus_statistics.document_statistics
    seen: set[RepositoryResourceAddress] = set()
    for match in result.matches:
        if not any(match.document_statistics is item for item in statistics):
            msg = "Lexical match is absent from its native retrieval index."
            raise ValueError(msg)
        address = match.document_statistics.analysis.document.resource.address
        if address in seen:
            msg = "Native lexical lane repeats a resource candidate."
            raise ValueError(msg)
        seen.add(address)


def _validate_preferences(
    acquisition: LocalizationLexicalAcquisition,
    preferences: tuple[ObligationRolePreference, ...],
) -> dict[LocalizationQueryIdentity, ObligationRolePreference]:
    expected = {item.request.identity for item in acquisition.obligation_retrievals}
    indexed = {item.query: item for item in preferences}
    if len(indexed) != len(preferences):
        msg = "Routing preferences contain a duplicated query lane."
        raise ValueError(msg)
    if set(indexed) != expected:
        msg = "Routing preferences must cover exactly the acquired query lanes."
        raise ValueError(msg)
    lane_by_query = {
        item.request.identity: item for item in acquisition.obligation_retrievals
    }
    for query, preference in indexed.items():
        if preference.obligation != lane_by_query[query].request.obligation:
            msg = "Routing preference obligation differs from its query lane."
            raise ValueError(msg)
    return indexed


def _route_lane(
    lane: ObligationLexicalEvidence,
    preference: ObligationRolePreference,
    role_evidence: RepositoryRoleEvidenceView,
) -> RoutedObligationLane:
    preferred: list[RoutedLexicalCandidate] = []
    escape: list[tuple[int, RepositoryTextLexicalBm25Match]] = []
    for native_rank, match in enumerate(lane.retrieval.matches, start=1):
        address = match.document_statistics.analysis.document.resource.address
        available = role_evidence.for_resource(address)
        selected = tuple(
            item
            for role in preference.preferred_roles
            for item in available
            if item.role == role
        )
        if selected:
            preferred.append(
                RoutedLexicalCandidate(
                    native_rank,
                    len(preferred) + 1,
                    RoutingTier.PREFERRED_ROLE_SUPPORTED,
                    match,
                    selected,
                ),
            )
        else:
            escape.append((native_rank, match))
    return RoutedObligationLane(
        lane,
        preference,
        tuple(preferred),
        tuple(
            RoutedLexicalCandidate(
                native_rank,
                len(preferred) + index,
                RoutingTier.ESCAPE,
                match,
                (),
            )
            for index, (native_rank, match) in enumerate(escape, start=1)
        ),
    )
