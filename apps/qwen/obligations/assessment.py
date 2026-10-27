# Copyright (c) 2026
"""Compose native Localization judgments with actual active source disclosure."""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, Any

from devtools.context.localization import (
    Disposition,
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationAssessment,
    LocalizationEvidenceReference,
    LocalizationObligation,
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    TaskProvenance,
    WitnessSet,
    assess_localization_readiness,
)
from devtools.context.localization.association import (
    CandidateWitnessHypothesis,
    CandidateWitnessMember,
    LexicalMatchSupport,
    OwnerResourceSupport,
    WitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.grounding import (
    AnchorGroundingRequest,
    ResourceAddressLocator,
    ground_task_anchor,
)
from devtools.context.localization.resolution import (
    CandidateMemberResolution,
    MemberResolutionDisposition,
    WitnessResolutionView,
    promote_supported_hypothesis,
)

if TYPE_CHECKING:
    from apps.qwen.context_tools import ContextTools
    from apps.qwen.obligations.frame import ObligationFrame, Witness
    from devtools.context.localization import (
        LocalizationLexicalAcquisition,
        LocalizationReadiness,
    )
    from devtools.models.interaction import PromptMessage


def interpretation(
    frame: ObligationFrame,
    tools: ContextTools,
) -> LocalizationTaskInterpretation:
    """Translate only host declarations; use current native occurrence targets."""
    identity = LocalizationTaskIdentity(
        frame.task_definition_sha256 + ":" + frame.sha256,
    )
    provenance = TaskProvenance(
        (frame.task_definition_sha256, frame.sha256),
        explanation="Trusted host declaration by " + frame.caller,
    )
    paths = dict.fromkeys(
        m.path for o in frame.obligations for a in o.alternatives for m in a.members
    )
    anchors = tuple(
        LocalizationAnchor(
            LocalizationAnchorIdentity(identity, p.value),
            p.value,
            provenance,
        )
        for p in paths
    )
    obligations = tuple(
        LocalizationObligation(
            LocalizationObligationIdentity(identity, spec.key),
            spec.predicate,
            tuple(
                a.identity
                for a in anchors
                if any(
                    m.path.value == a.text
                    for alt in spec.alternatives
                    for m in alt.members
                )
            ),
            provenance,
            spec.requirement,
            spec.criterion,
            tuple(
                WitnessSet(
                    tuple(tools.snapshot.resource_at(m.path) for m in alt.members),
                )
                for alt in spec.alternatives
            ),
        )
        for spec in frame.obligations
    )
    return LocalizationTaskInterpretation(identity, provenance, anchors, obligations)


def _disclosures(
    messages: tuple[PromptMessage, ...],
    tools: ContextTools,
) -> list[dict[str, Any]]:
    """Authenticate selected exact text against retained native observations."""
    visible = []
    for message in messages:
        if message.role != "tool":
            continue
        try:
            value = json.loads(message.content)
        except ValueError:
            continue
        if not isinstance(value, dict):
            continue
        for item in (value, *value.get("source_observations", ())):
            if not isinstance(item, dict) or not isinstance(item.get("text"), str):
                continue
            keys = ("path", "version", "span", "text")
            if any(
                all(item.get(k) == observed.get(k) for k in keys)
                for observed in tools.observations
            ):
                visible.append(
                    {
                        **{k: item[k] for k in keys},
                        "tool_call_id": message.tool_call_id,
                    },
                )
    return visible


def _disposition(
    witness: Witness,
    member: CandidateWitnessMember,
    visible: list[dict[str, Any]],
) -> tuple[MemberResolutionDisposition, str, list[dict[str, Any]]]:
    """No lexical score or model claim is a criterion decision."""
    if witness.version != member.target.content_identity or witness.end > len(
        member.target.content,
    ):
        return (
            MemberResolutionDisposition.UNRESOLVED,
            "STALE_OR_FOREIGN_WITNESS_SOURCE",
            [],
        )
    cursor = witness.start
    used = []
    for item in sorted(visible, key=lambda o: o["span"]):
        if (
            item["path"] != witness.path.value
            or item["version"] != witness.version.value
        ):
            continue
        start, end = item["span"]
        if not start <= cursor < end:
            continue
        if item["text"] != member.target.content[start:end]:
            continue
        cursor = end
        used.append(
            {
                "tool_call_id": item["tool_call_id"],
                "span": [start, end],
                "text_sha256": hashlib.sha256(item["text"].encode()).hexdigest(),
            },
        )
        if cursor >= witness.end:
            return witness.decision, witness.reason, used
    return (
        MemberResolutionDisposition.UNRESOLVED,
        "REQUIRED_RANGE_NOT_IN_ACTIVE_CONTEXT",
        used,
    )


def assess(
    frame: ObligationFrame,
    tools: ContextTools,
    messages: tuple[PromptMessage, ...],
    acquisition: LocalizationLexicalAcquisition,
) -> tuple[LocalizationReadiness, dict[str, Any]]:
    """Ground, associate, explicitly resolve/promote, then assess readiness."""
    tools.check_current()
    task = acquisition.task
    snapshot = tools.snapshot
    hypotheses = []
    for spec, obligation in zip(frame.obligations, task.obligations, strict=True):
        for alternative in spec.alternatives:
            members = []
            for witness in alternative.members:
                grounding = ground_task_anchor(
                    task=task,
                    snapshot=snapshot,
                    request=AnchorGroundingRequest(
                        task.identity,
                        LocalizationAnchorIdentity(task.identity, witness.path.value),
                        snapshot.repository_id,
                        snapshot.id,
                        ResourceAddressLocator(witness.path),
                        task.provenance,
                    ),
                )
                target = snapshot.resource_at(witness.path)
                lexical = tuple(
                    LexicalMatchSupport(query, rank, match)
                    for query, result in [
                        (None, acquisition.full_task_retrieval),
                        *(
                            (lane.request.identity, lane.retrieval)
                            for lane in acquisition.obligation_retrievals
                            if lane.request.obligation == obligation.identity
                        ),
                    ]
                    for rank, match in enumerate(result.matches, 1)
                    if match.document_statistics.analysis.document.resource == target
                )
                members.append(
                    CandidateWitnessMember(
                        target,
                        witness.reason,
                        lexical=lexical,
                        structural=(OwnerResourceSupport(grounding),),
                    ),
                )
            hypotheses.append(
                CandidateWitnessHypothesis(
                    WitnessHypothesisIdentity(obligation.identity, alternative.key),
                    tuple(members),
                ),
            )
    candidates = build_candidate_witness_view(
        task=task,
        snapshot=snapshot,
        hypotheses=tuple(hypotheses),
        acquisition=acquisition,
    )
    visible = _disclosures(messages, tools)
    records = []
    details = []
    for hypothesis in candidates.hypotheses:
        spec = next(
            o
            for o in frame.obligations
            if o.key == hypothesis.identity.obligation.value
        )
        alternative = next(
            a for a in spec.alternatives if a.key == hypothesis.identity.value
        )
        rows = []
        for member in hypothesis.members:
            witness = next(
                m for m in alternative.members if m.path == member.target.address
            )
            disposition, reason, used = _disposition(witness, member, visible)
            records.append(
                CandidateMemberResolution(
                    candidates,
                    hypothesis,
                    member,
                    disposition,
                    spec.criterion,
                    witness.claim,
                    reason,
                    frame.caller,
                    task.provenance,
                    (
                        LocalizationEvidenceReference(
                            member.structural[0],
                            snapshot.repository_id,
                            snapshot.id,
                        ),
                    ),
                ),
            )
            rows.append(
                {
                    "path": witness.path.value,
                    "expected_version": witness.version.value,
                    "version": str(member.target.content_identity),
                    "span": [witness.start, witness.end],
                    "decision": disposition.value,
                    "host_decision": witness.decision.value,
                    "claim": witness.claim,
                    "grounding_resolver": member.structural[0].grounding.resolver.value,
                    "reason": reason,
                    "used_disclosures": used,
                    "lexical_ranks": [s.native_rank for s in member.lexical],
                },
            )
        details.append(
            {"obligation": spec.key, "alternative": alternative.key, "members": rows},
        )
    view = WitnessResolutionView(candidates, tuple(records)) if hypotheses else None
    assessments = []
    for obligation in task.obligations:
        supported = (
            next(
                (
                    r
                    for r in view.completely_supported
                    if r.hypothesis.identity.obligation == obligation.identity
                ),
                None,
            )
            if view
            else None
        )
        promotion = (
            promote_supported_hypothesis(view, supported.hypothesis.identity)
            if view and supported
            else None
        )
        assessments.append(
            LocalizationAssessment(
                obligation.identity,
                snapshot.repository_id,
                snapshot.id,
                Disposition.RESOLVED if promotion else Disposition.OPEN,
                supported_witnesses=promotion.supported_witnesses if promotion else (),
            ),
        )
    readiness = assess_localization_readiness(
        task=task,
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        assessments=assessments,
    )
    status = {
        "frame_sha256": frame.sha256,
        "task_definition_sha256": frame.task_definition_sha256,
        "repository": str(snapshot.repository_id),
        "snapshot": str(snapshot.id),
        "readiness": readiness.readiness.value,
        "purpose": "before-source-changing-action",
        "task_interpretation": task.identity.value,
        "caller": frame.caller,
        "identity_coverage_exact": readiness.identity_coverage.is_exact,
        "unresolved_mandatory": [i.value for i in readiness.unresolved_mandatory],
        "unresolved_helpful": [i.value for i in readiness.unresolved_helpful],
        "obligations": [
            {
                "key": o.key,
                "requirement": o.requirement.value,
                "predicate": o.predicate,
                "criterion": o.criterion.statement,
            }
            for o in frame.obligations
        ],
        "candidates": details,
        "lexical_lanes": [
            {
                "obligation": lane.request.obligation.value,
                "query": lane.request.text,
                "paths": [
                    m.document_statistics.analysis.document.resource.address.value
                    for m in lane.retrieval.matches
                ],
            }
            for lane in acquisition.obligation_retrievals
        ],
        "full_task_query": tools.task.objective,
        "full_task_paths": [
            m.document_statistics.analysis.document.resource.address.value
            for m in acquisition.full_task_retrieval.matches
        ],
        "qualification": (
            "Trusted criterion decisions plus exact current active source disclosure; "
            "not exhaustive task coverage, correctness, edit authority or publication."
        ),
    }
    status["assessment_sha256"] = hashlib.sha256(
        json.dumps(status, sort_keys=True).encode(),
    ).hexdigest()
    return readiness, status
