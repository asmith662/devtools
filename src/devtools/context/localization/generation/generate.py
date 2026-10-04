# Copyright (c) 2026
"""Instantiate caller recipes through explicit bounded native RI projections."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, cast

from devtools.context.localization.association import (
    CandidateWitnessHypothesis,
    CandidateWitnessMember,
    GeneratedWitnessHypothesisIdentity,
    LexicalMatchSupport,
    MirroredResourceSupport,
    OwnerResourceSupport,
    RoutedMatchSupport,
    WitnessHypothesisFamilyIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.association.references import (
    validate_reference_frame,
)
from devtools.context.localization.association.structural import (
    owner_resource,
    validate_structural_support,
)
from devtools.context.localization.generation.contract import (
    BranchGenerationAttempt,
    BranchingGroundedMemberRecipe,
    GenerationDisposition,
    HypothesisGenerationAttempt,
    MemberProjectionAttempt,
    ProjectedMemberTarget,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    WitnessGenerationView,
)
from devtools.context.localization.generation.references import (
    project_referencing_resources,
)
from devtools.context.localization.grounding import (
    AnchorGroundingDisposition,
    ground_task_anchor,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)

if TYPE_CHECKING:
    from devtools.context.localization.association.references import (
        PythonReferenceProjectionRequest,
    )
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
            type(item.identity).__name__,
            item.identity.value,
        ),
    )
    attempts = tuple(
        _attempt_recipe(plan, recipe, mirrors) for recipe in ordered_recipes
    )
    hypotheses = tuple(child for item in attempts for child in item.children)
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
    if plan.python_references is not None:
        validate_reference_frame(plan.python_references, plan.snapshot)
    obligations = {item.identity: item for item in plan.task.obligations}
    for recipe in plan.recipes:
        obligation = obligations.get(recipe.identity.obligation)
        if obligation is None:
            msg = "Generation recipe names an unknown task obligation."
            raise ValueError(msg)
        for member in recipe.members:
            if member.projection is ProjectionKind.REFERENCING_RESOURCE:
                if plan.python_references is None:
                    msg = "Reference projection requires explicit native inputs."
                    raise ValueError(msg)
                if not isinstance(member, BranchingGroundedMemberRecipe):
                    msg = "Reference projection requires a branching member."
                    raise ValueError(msg)
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
    if isinstance(recipe.identity, WitnessHypothesisFamilyIdentity):
        return _attempt_family(plan, recipe, attempts)
    failure = next(
        (
            _fixed_disposition(item)
            for item in attempts
            if _fixed_disposition(item) is not GenerationDisposition.GENERATED
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
    hypothesis = CandidateWitnessHypothesis(
        recipe.identity,
        members,
    )
    return HypothesisGenerationAttempt(
        recipe,
        GenerationDisposition.GENERATED,
        attempts,
        hypothesis,
    )


def _fixed_disposition(attempt: MemberProjectionAttempt) -> GenerationDisposition:
    if not attempt.complete:
        return GenerationDisposition.WORK_BOUND_EXCEEDED
    return attempt.disposition


def _attempt_family(
    plan: WitnessGenerationPlan,
    recipe: WitnessGenerationRecipe,
    attempts: tuple[MemberProjectionAttempt, ...],
) -> HypothesisGenerationAttempt:
    attempts = tuple(
        item
        if isinstance(item.recipe, BranchingGroundedMemberRecipe)
        else _admit_fixed_member(plan, recipe, item)
        for item in attempts
    )
    fixed = tuple(
        item
        for item in attempts
        if not isinstance(item.recipe, BranchingGroundedMemberRecipe)
    )
    if any(
        _fixed_disposition(item) is not GenerationDisposition.GENERATED
        for item in fixed
    ):
        return HypothesisGenerationAttempt(
            recipe,
            GenerationDisposition.FIXED_MEMBER_FAILED,
            attempts,
            None,
        )
    if len({item.targets[0].address for item in fixed}) != len(fixed):
        return HypothesisGenerationAttempt(
            recipe,
            GenerationDisposition.DUPLICATE_TARGET,
            attempts,
            None,
        )
    branch = next(
        item
        for item in attempts
        if isinstance(item.recipe, BranchingGroundedMemberRecipe)
    )
    failure = None
    if not branch.complete:
        failure = GenerationDisposition.WORK_BOUND_EXCEEDED
    elif branch.disposition not in (
        GenerationDisposition.GENERATED,
        GenerationDisposition.MULTI_TARGET,
        GenerationDisposition.NO_TARGET,
    ):
        failure = branch.disposition
    elif not branch.projections:
        failure = GenerationDisposition.NO_TARGET
    elif len(branch.projections) > branch.result_limit:
        failure = GenerationDisposition.RESULT_BOUND_EXCEEDED
    if failure is not None:
        return HypothesisGenerationAttempt(recipe, failure, attempts, None)
    # Enumeration is complete and admitted as a whole before any child is built.
    outcomes = tuple(
        _attempt_branch(plan, recipe, fixed, branch, target)
        for target in branch.projections
    )
    successful = sum(item.hypothesis is not None for item in outcomes)
    disposition = (
        GenerationDisposition.GENERATED
        if successful == len(outcomes)
        else GenerationDisposition.GENERATED_WITH_BRANCH_FAILURES
        if successful
        else GenerationDisposition.ABSTAINED
    )
    return HypothesisGenerationAttempt(recipe, disposition, attempts, None, outcomes)


def _admit_fixed_member(
    plan: WitnessGenerationPlan,
    recipe: WitnessGenerationRecipe,
    attempt: MemberProjectionAttempt,
) -> MemberProjectionAttempt:
    if _fixed_disposition(attempt) is not GenerationDisposition.GENERATED:
        return attempt
    try:
        member = _make_member(plan, recipe.identity.obligation, attempt)
        if plan.snapshot.resource_at(member.target.address) != member.target:
            msg = "Fixed member target differs from the generation snapshot."
            raise ValueError(msg)  # noqa: TRY301 - retained as member failure
        for support in member.structural:
            validate_structural_support(
                task=plan.task,
                snapshot=plan.snapshot,
                target=member.target,
                support=support,
            )
    except ValueError as error:
        return replace(
            attempt,
            disposition=GenerationDisposition.INVALID_MEMBER,
            failure_reason=str(error),
        )
    return attempt


def _attempt_branch(
    plan: WitnessGenerationPlan,
    recipe: WitnessGenerationRecipe,
    fixed: tuple[MemberProjectionAttempt, ...],
    branch: MemberProjectionAttempt,
    projection: ProjectedMemberTarget,
) -> BranchGenerationAttempt:
    identity = GeneratedWitnessHypothesisIdentity(
        cast("WitnessHypothesisFamilyIdentity", recipe.identity),
        branch.recipe.key,
        plan.snapshot.repository_id,
        plan.snapshot.id,
        projection.target,
    )
    targets = (*tuple(item.targets[0] for item in fixed), projection.target)
    if len({item.address for item in targets}) != len(targets):
        return BranchGenerationAttempt(
            identity,
            projection,
            GenerationDisposition.DUPLICATE_TARGET,
            None,
            "Branch combination repeats a complementary resource target.",
        )
    try:
        members = (
            *(_make_member(plan, recipe.identity.obligation, item) for item in fixed),
            _make_member(plan, recipe.identity.obligation, branch, projection),
        )
        hypothesis = CandidateWitnessHypothesis(identity, members)
        build_candidate_witness_view(
            task=plan.task,
            snapshot=plan.snapshot,
            hypotheses=(hypothesis,),
            acquisition=plan.acquisition,
            role_evidence=plan.role_evidence,
            routing=plan.routing,
        )
    except ValueError as error:
        # A fully enumerated target may fail exact frame/support validation.
        return BranchGenerationAttempt(
            identity,
            projection,
            GenerationDisposition.INVALID_BRANCH,
            None,
            str(error),
        )
    return BranchGenerationAttempt(
        identity,
        projection,
        GenerationDisposition.GENERATED,
        hypothesis,
        "Exact branch combination passed unresolved candidate association validation.",
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
        return MemberProjectionAttempt(member, source_disposition, None, (), 0)
    if member.projection is ProjectionKind.REFERENCING_RESOURCE:
        return project_referencing_resources(
            plan.snapshot,
            member,
            cast("PythonReferenceProjectionRequest", plan.python_references),
        )
    source = grounding.candidates[0].referent
    owner = owner_resource(plan.snapshot, source)
    if member.projection is ProjectionKind.OWNER_RESOURCE:
        return MemberProjectionAttempt(
            member,
            GenerationDisposition.GENERATED,
            source,
            (ProjectedMemberTarget(owner, (OwnerResourceSupport(grounding),)),),
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
        tuple(
            ProjectedMemberTarget(target, (support,))
            for target, support in zip(targets, supports, strict=True)
        ),
        len(plan.snapshot.resources),
        mirror_analysis=mirrors,
    )


def _make_member(
    plan: WitnessGenerationPlan,
    obligation: LocalizationObligationIdentity,
    attempt: MemberProjectionAttempt,
    projection: ProjectedMemberTarget | None = None,
) -> CandidateWitnessMember:
    selected = attempt.projections[0] if projection is None else projection
    target = selected.target
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
        structural=selected.structural,
    )


def _match_target(
    match: RepositoryTextLexicalBm25Match,
) -> RepositoryResourceOccurrence:
    # Native BM25 matches are deliberately retained; this helper only reads identity.
    return match.document_statistics.analysis.document.resource
