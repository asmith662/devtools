# Copyright (c) 2026
"""Instantiate caller recipes through two bounded native RI projections."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.localization.association import (
    CandidateWitnessHypothesis,
    CandidateWitnessMember,
    LexicalMatchSupport,
    MirroredResourceSupport,
    OwnerResourceSupport,
    RoutedMatchSupport,
    build_candidate_witness_view,
)
from devtools.context.localization.association.structural import owner_resource
from devtools.context.localization.generation.contract import (
    GenerationDisposition,
    HypothesisGenerationAttempt,
    MemberProjectionAttempt,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    WitnessGenerationView,
)
from devtools.context.localization.grounding import (
    AnchorGroundingDisposition,
    ground_task_anchor,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)

if TYPE_CHECKING:
    from devtools.context.localization.association.structural import (
        StructuralMemberSupport,
    )
    from devtools.context.localization.generation.contract import GroundedMemberRecipe
    from devtools.context.localization.identity import LocalizationObligationIdentity
    from devtools.context.python.mirrored_paths import PythonMirroredPathAnalysis
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalBm25Match


def generate_witness_hypotheses(plan: WitnessGenerationPlan) -> WitnessGenerationView:
    """Generate only caller-shaped unresolved hypotheses from exact RI relations."""
    _validate_recipes(plan)
    # Validate optional native frames even when every structural recipe abstains.
    build_candidate_witness_view(
        task=plan.task,
        snapshot=plan.snapshot,
        hypotheses=(),
        acquisition=plan.acquisition,
        role_evidence=plan.role_evidence,
        routing=plan.routing,
    )
    mirrors = (
        derive_python_mirrored_path_correspondences(plan.snapshot)
        if any(
            member.projection is ProjectionKind.MIRRORED_RESOURCE
            and member.grounding.disposition is AnchorGroundingDisposition.RESOLVED
            for recipe in plan.recipes
            for member in recipe.members
        )
        else None
    )
    obligation_order = {
        item.identity: index for index, item in enumerate(plan.task.obligations)
    }
    ordered_recipes = sorted(
        plan.recipes,
        key=lambda item: (
            obligation_order[item.identity.obligation],
            item.identity.value,
        ),
    )
    attempts = tuple(
        _attempt_recipe(plan, recipe, mirrors) for recipe in ordered_recipes
    )
    hypotheses = tuple(
        item.hypothesis for item in attempts if item.hypothesis is not None
    )
    association = build_candidate_witness_view(
        task=plan.task,
        snapshot=plan.snapshot,
        hypotheses=hypotheses,
        acquisition=plan.acquisition,
        role_evidence=plan.role_evidence,
        routing=plan.routing,
    )
    return WitnessGenerationView(plan, attempts, association)


def _validate_recipes(plan: WitnessGenerationPlan) -> None:
    obligations = {item.identity: item for item in plan.task.obligations}
    for recipe in plan.recipes:
        obligation = obligations.get(recipe.identity.obligation)
        if obligation is None:
            msg = "Generation recipe names an unknown task obligation."
            raise ValueError(msg)
        for member in recipe.members:
            grounding = member.grounding
            if grounding.request.anchor not in obligation.anchors:
                msg = "Generation member anchor is not linked to its obligation."
                raise ValueError(msg)
            replayed = ground_task_anchor(
                task=plan.task,
                snapshot=plan.snapshot,
                request=grounding.request,
                module_universe=grounding.module_universe,
            )
            if replayed != grounding:
                msg = "Generation member has stale or altered native grounding."
                raise ValueError(msg)


def _attempt_recipe(
    plan: WitnessGenerationPlan,
    recipe: WitnessGenerationRecipe,
    mirrors: PythonMirroredPathAnalysis | None,
) -> HypothesisGenerationAttempt:
    attempts = tuple(_project(plan, member, mirrors) for member in recipe.members)
    failure = next(
        (
            item.disposition
            for item in attempts
            if item.disposition is not GenerationDisposition.GENERATED
        ),
        None,
    )
    if failure is not None:
        return HypothesisGenerationAttempt(recipe, failure, attempts, None)
    targets = tuple(item.targets[0] for item in attempts)
    if len({item.address for item in targets}) != len(targets):
        return HypothesisGenerationAttempt(
            recipe,
            GenerationDisposition.DUPLICATE_TARGET,
            attempts,
            None,
        )
    members = tuple(
        _make_member(plan, recipe.identity.obligation, attempt) for attempt in attempts
    )
    hypothesis = CandidateWitnessHypothesis(recipe.identity, members)
    return HypothesisGenerationAttempt(
        recipe,
        GenerationDisposition.GENERATED,
        attempts,
        hypothesis,
    )


def _project(
    plan: WitnessGenerationPlan,
    member: GroundedMemberRecipe,
    mirrors: PythonMirroredPathAnalysis | None,
) -> MemberProjectionAttempt:
    grounding = member.grounding
    source_disposition = {
        AnchorGroundingDisposition.AMBIGUOUS: GenerationDisposition.AMBIGUOUS_SOURCE,
        AnchorGroundingDisposition.UNRESOLVED: GenerationDisposition.UNRESOLVED_SOURCE,
        AnchorGroundingDisposition.UNSUPPORTED: (
            GenerationDisposition.UNSUPPORTED_SOURCE
        ),
    }.get(grounding.disposition)
    if source_disposition is not None:
        return MemberProjectionAttempt(member, source_disposition, None, (), (), 0)
    source = grounding.candidates[0].referent
    owner = owner_resource(plan.snapshot, source)
    if member.projection is ProjectionKind.OWNER_RESOURCE:
        return MemberProjectionAttempt(
            member,
            GenerationDisposition.GENERATED,
            source,
            (owner,),
            (OwnerResourceSupport(grounding),),
            1,
        )
    if mirrors is None:
        msg = "Mirrored projection requires the native snapshot analysis."
        raise ValueError(msg)
    matches = tuple(
        item for item in mirrors.correspondences if owner in (item.source, item.test)
    )
    targets = tuple(
        item.test if item.source == owner else item.source for item in matches
    )
    supports: tuple[StructuralMemberSupport, ...] = tuple(
        MirroredResourceSupport(grounding, item) for item in matches
    )
    disposition = (
        GenerationDisposition.NO_TARGET
        if not targets
        else GenerationDisposition.GENERATED
        if len(targets) == 1
        else GenerationDisposition.MULTI_TARGET
    )
    return MemberProjectionAttempt(
        member,
        disposition,
        source,
        targets,
        supports,
        len(plan.snapshot.resources),
        mirror_analysis=mirrors,
    )


def _make_member(
    plan: WitnessGenerationPlan,
    obligation: LocalizationObligationIdentity,
    attempt: MemberProjectionAttempt,
) -> CandidateWitnessMember:
    target = attempt.targets[0]
    lexical: list[LexicalMatchSupport] = []
    if plan.acquisition is not None:
        lexical.extend(
            LexicalMatchSupport(None, rank, match)
            for rank, match in enumerate(
                plan.acquisition.full_task_retrieval.matches,
                1,
            )
            if _match_target(match) == target
        )
        lexical.extend(
            LexicalMatchSupport(lane.request.identity, rank, match)
            for lane in plan.acquisition.obligation_retrievals
            if lane.request.obligation == obligation
            for rank, match in enumerate(lane.retrieval.matches, 1)
            if _match_target(match) == target
        )
    roles = (
        plan.role_evidence.for_resource(target.address)
        if plan.role_evidence is not None
        else ()
    )
    routed = (
        tuple(
            RoutedMatchSupport(lane.preference.query, candidate)
            for lane in plan.routing.obligation_lanes
            if lane.preference.obligation == obligation
            for candidate in lane.candidates
            if _match_target(candidate.match) == target
        )
        if plan.routing is not None
        else ()
    )
    return CandidateWitnessMember(
        target=target,
        reason=attempt.recipe.reason,
        lexical=tuple(lexical),
        roles=roles,
        routed=routed,
        structural=attempt.structural,
    )


def _match_target(
    match: RepositoryTextLexicalBm25Match,
) -> RepositoryResourceOccurrence:
    # Native BM25 matches are deliberately retained; this helper only reads identity.
    return match.document_statistics.analysis.document.resource
