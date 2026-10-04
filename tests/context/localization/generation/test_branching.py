# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Explicit single-slot branching, independent of any future relation adapter."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

import devtools.context.localization.generation.generate as execution
from devtools.context.localization import (
    Disposition,
    LocalizationAssessment,
    TaskProvenance,
    assess_localization_readiness,
)
from devtools.context.localization.association import (
    CandidateWitnessHypothesis,
    GeneratedWitnessHypothesisIdentity,
    OwnerResourceSupport,
    WitnessHypothesisFamilyIdentity,
    WitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.generation import (
    BranchingGroundedMemberRecipe,
    MemberProjectionAttempt,
    ProjectedMemberTarget,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    generate_witness_hypotheses,
)
from devtools.context.localization.generation import (
    GenerationDisposition as G,
)
from devtools.context.localization.grounding import (
    PythonModuleLocator,
    ResourceAddressLocator,
    ground_task_anchor,
)
from devtools.context.localization.roles import (
    RepositoryRoleKind,
    derive_repository_role_evidence,
)
from devtools.context.localization.routing import (
    ObligationRolePreference,
    route_localization_lexical_evidence,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import RepositoryResourceAddress as Address
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)
from tests.context.localization.generation.test_generation import (
    _frame,
    _ground,
    _member,
    _recipe,
    _universe,
)
from tests.context.localization.test_lexical import _execute, _query
from tests.context.retrieval.lexical._helpers import _collection, _document

if TYPE_CHECKING:
    from devtools.context.localization.generation import (
        GroundedMemberRecipe,
        WitnessGenerationView,
    )
    from devtools.context.python.mirrored_paths import PythonMirroredPathAnalysis


def _run(  # noqa: PLR0913
    monkeypatch: pytest.MonkeyPatch,
    paths: tuple[str, ...],
    *,
    limit: int = 4,
    complete: bool = True,
    fixed: bool = True,
    bad_support: bool = False,
    family: str = "family",
) -> WitnessGenerationView:
    task, snapshot = _frame()
    seed = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    branch = BranchingGroundedMemberRecipe(
        "branch",
        seed,
        ProjectionKind.OWNER_RESOURCE,
        "one proposed complement",
        TaskProvenance("explicit-branching"),
        limit,
    )
    projections = tuple(
        ProjectedMemberTarget(
            snapshot.resource_at(Address(path)),
            (
                OwnerResourceSupport(
                    seed
                    if bad_support and path == "docs/overview.md"
                    else _ground(task, snapshot, ResourceAddressLocator(Address(path))),
                ),
            ),
        )
        for path in paths
    )
    native_project = execution._project  # noqa: SLF001

    def project(
        plan: WitnessGenerationPlan,
        member: GroundedMemberRecipe,
        mirrors: PythonMirroredPathAnalysis | None,
    ) -> MemberProjectionAttempt:
        if not isinstance(member, BranchingGroundedMemberRecipe):
            return native_project(plan, member, mirrors)
        return MemberProjectionAttempt(
            member,
            G.MULTI_TARGET if len(paths) > 1 else G.GENERATED,
            seed.candidates[0].referent,
            projections,
            3,
            complete=complete,
            work_limit=3,
            uncovered_frontier=(snapshot.resources[-1],) if not complete else (),
        )

    monkeypatch.setattr(execution, "_project", project)
    members = (_member(seed, key="fixed"), branch) if fixed else (branch,)
    recipe = WitnessGenerationRecipe(
        WitnessHypothesisFamilyIdentity(task.obligations[0].identity, family),
        members,
        TaskProvenance("caller-family"),
    )
    return generate_witness_hypotheses(WitnessGenerationPlan(task, snapshot, (recipe,)))


@pytest.mark.parametrize(
    "paths",
    [(), ("tests/test_alpha.py",), ("tests/test_alpha.py", "docs/overview.md")],
)
def test_zero_one_many(monkeypatch: pytest.MonkeyPatch, paths: tuple[str, ...]) -> None:
    view = _run(monkeypatch, paths)
    family = view.attempts[0]
    assert len(view.generated) == len(paths)
    assert len(family.branches) == len(paths)
    assert family.hypothesis is None
    assert family.disposition is (G.GENERATED if paths else G.NO_TARGET)
    assert family.children == tuple(item.hypothesis for item in family.branches)
    assert family.failed_branches == ()
    assert view.for_family(family.recipe.identity) == family  # type: ignore[arg-type]
    assert view.for_obligation(view.plan.task.obligations[0].identity) == (family,)
    for child in view.generated:
        identity = child.identity
        assert isinstance(identity, GeneratedWitnessHypothesisIdentity)
        assert view.parent_family(identity) == family
        assert len(child.members) == 2
        assert {item.target.address.value for item in child.members} == {
            "src/devtools/alpha.py",
            identity.target.address.value,
        }
        for member in child.members:
            assert (
                member.structural[0].grounding.candidates[0].referent == member.target
            )
        assert view.for_target(identity.target) == (child,)
        assert not hasattr(child, "rank")
        assert not hasattr(child, "score")
    assert not view.cross_obligation_targets
    assert view.plan.task == _frame()[0]


def test_canonical_identity_and_order(monkeypatch: pytest.MonkeyPatch) -> None:
    first = _run(monkeypatch, ("tests/test_alpha.py", "docs/overview.md"))
    monkeypatch.undo()
    reverse = _run(monkeypatch, ("docs/overview.md", "tests/test_alpha.py"))
    assert first == reverse
    identities = tuple(item.identity for item in first.generated)
    assert len(set(identities)) == 2
    assert len({item.value for item in identities}) == 2
    monkeypatch.undo()
    other = _run(
        monkeypatch,
        ("tests/test_alpha.py", "docs/overview.md"),
        family="other",
    )
    assert set(identities).isdisjoint(item.identity for item in other.generated)
    assert tuple(item.stable_key for item in first.attempts[0].branches)


def test_result_and_work_bounds(monkeypatch: pytest.MonkeyPatch) -> None:
    paths = ("tests/test_alpha.py", "docs/overview.md")
    overflow = _run(monkeypatch, paths, limit=1)
    family = overflow.attempts[0]
    assert family.disposition is G.RESULT_BOUND_EXCEEDED
    assert not family.branches
    assert not overflow.generated
    branch = family.members[0]
    assert branch.result_count == 2
    assert branch.result_limit == 1
    assert branch.complete
    assert branch.work_performed == branch.work_limit == 3
    monkeypatch.undo()
    incomplete = _run(monkeypatch, paths, limit=1, complete=False)
    family = incomplete.attempts[0]
    assert family.disposition is G.WORK_BOUND_EXCEEDED
    assert not family.branches
    assert not incomplete.generated
    branch = family.members[0]
    assert branch.result_count is None
    assert branch.truncated
    assert branch.uncovered_frontier
    assert len(branch.targets) == 2  # diagnostic prefix is retained, never admitted
    monkeypatch.undo()
    empty = _run(monkeypatch, (), complete=False)
    assert empty.attempts[0].disposition is G.WORK_BOUND_EXCEEDED


def test_duplicate_targets_and_failed_siblings(monkeypatch: pytest.MonkeyPatch) -> None:
    view = _run(
        monkeypatch,
        (
            "tests/test_alpha.py",
            "tests/test_alpha.py",
            "src/devtools/alpha.py",
        ),
    )
    family = view.attempts[0]
    assert family.members[0].result_count == 2
    assert len(view.generated) == 1
    assert len(family.branches) == 2
    assert family.disposition is G.GENERATED_WITH_BRANCH_FAILURES
    assert family.failed_branches[0].disposition is G.DUPLICATE_TARGET
    assert family.failed_branches[0].reason
    assert len(view.generated[0].members[1].structural) == 1
    monkeypatch.undo()
    failed = _run(monkeypatch, ("src/devtools/alpha.py",))
    assert not failed.generated
    assert failed.attempts[0].disposition is G.ABSTAINED


def test_invalid_support_retained_with_valid_sibling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    view = _run(
        monkeypatch,
        ("tests/test_alpha.py", "docs/overview.md"),
        bad_support=True,
    )
    family = view.attempts[0]
    assert family.disposition is G.GENERATED_WITH_BRANCH_FAILURES
    assert len(view.generated) == 1
    assert family.failed_branches[0].disposition is G.INVALID_BRANCH
    assert "Owner support" in family.failed_branches[0].reason
    assert view.parent_family(family.failed_branches[0].identity) == family


def test_fixed_failure_blocks_every_child(monkeypatch: pytest.MonkeyPatch) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",))
    recipe = view.plan.recipes[0]
    fixed = recipe.members[1]
    missing = _ground(
        view.plan.task,
        view.plan.snapshot,
        ResourceAddressLocator(Address("missing.py")),
    )
    altered = replace(
        recipe,
        members=(recipe.members[0], replace(fixed, grounding=missing)),
    )
    result = generate_witness_hypotheses(replace(view.plan, recipes=(altered,)))
    assert result.attempts[0].disposition is G.FIXED_MEMBER_FAILED
    assert result.attempts[0].members[1].disposition is G.UNRESOLVED_SOURCE
    assert not result.generated
    assert not result.attempts[0].branches


def test_family_contract_and_view_rejections(monkeypatch: pytest.MonkeyPatch) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",))
    recipe = view.plan.recipes[0]
    branch = recipe.members[0]
    assert isinstance(branch, BranchingGroundedMemberRecipe)
    with pytest.raises(ValueError, match="positive result bound"):
        replace(branch, max_results=0)
    with pytest.raises(ValueError, match="at most one"):
        replace(recipe, members=(branch, replace(branch, key="second")))
    with pytest.raises(ValueError, match="family identity"):
        replace(
            recipe,
            identity=WitnessHypothesisIdentity(recipe.identity.obligation, "x"),
        )
    with pytest.raises(ValueError, match="family identity"):
        replace(recipe, members=(recipe.members[1],))
    with pytest.raises(ValueError, match="must not be blank"):
        replace(recipe.identity, value=" ")
    identity = view.generated[0].identity
    assert isinstance(identity, GeneratedWitnessHypothesisIdentity)
    with pytest.raises(ValueError, match="member key"):
        replace(identity, member_key=" ")
    with pytest.raises(ValueError, match="no such family"):
        view.for_family(replace(identity.family, value="unknown"))
    with pytest.raises(ValueError, match="no such branch child"):
        view.parent_family(replace(identity, member_key="unknown"))
    projection = view.attempts[0].members[0]
    with pytest.raises(ValueError, match="uncovered frontier"):
        replace(projection, uncovered_frontier=(view.plan.snapshot.resources[0],))
    for work, limit in ((-1, None), (2, 1), (0, -1)):
        with pytest.raises(ValueError, match="work bound"):
            replace(projection, work_performed=work, work_limit=limit)


def test_collision_validation_and_literal_namespace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",), fixed=False)
    child = view.generated[0]
    with pytest.raises(ValueError, match="identity is duplicated"):
        build_candidate_witness_view(
            task=view.plan.task,
            snapshot=view.plan.snapshot,
            hypotheses=(child, child),
        )
    literal = CandidateWitnessHypothesis(
        WitnessHypothesisIdentity(child.identity.obligation, child.identity.value),
        child.members,
    )
    combined = build_candidate_witness_view(
        task=view.plan.task,
        snapshot=view.plan.snapshot,
        hypotheses=(literal, child),
    )
    assert len(combined.hypotheses) == 2
    identity = child.identity
    assert isinstance(identity, GeneratedWitnessHypothesisIdentity)
    wrong = replace(
        identity,
        target=view.plan.snapshot.resource_at(Address("docs/overview.md")),
    )
    with pytest.raises(ValueError, match="frame or branch target"):
        build_candidate_witness_view(
            task=view.plan.task,
            snapshot=view.plan.snapshot,
            hypotheses=(replace(child, identity=wrong),),
        )


def test_existing_fixed_attempt_children() -> None:
    task, snapshot = _frame()
    seed = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    view = generate_witness_hypotheses(
        WitnessGenerationPlan(
            task,
            snapshot,
            (_recipe(task, _member(seed)),),
        ),
    )
    assert view.attempts[0].children == view.generated
    assert not view.attempts[0].branches


@pytest.mark.parametrize(
    "disposition",
    [G.UNRESOLVED_SOURCE, G.UNSUPPORTED_SOURCE, G.AMBIGUOUS_SOURCE],
)
def test_branch_source_failure_keeps_family(
    monkeypatch: pytest.MonkeyPatch,
    disposition: G,
) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",))
    branch = view.attempts[0].members[0]
    fixed = view.attempts[0].members[1]
    monkeypatch.setattr(
        execution,
        "_project",
        lambda _plan, member, _mirrors: (
            replace(branch, disposition=disposition, projections=())
            if isinstance(member, BranchingGroundedMemberRecipe)
            else fixed
        ),
    )
    failed = generate_witness_hypotheses(view.plan)
    assert failed.attempts[0].disposition is disposition
    assert not failed.generated
    assert not failed.attempts[0].branches


@pytest.mark.parametrize("failure", ["incomplete", "support", "foreign", "empty"])
def test_fixed_admission_failure(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",))
    branch, fixed = view.attempts[0].members
    if failure == "incomplete":
        fixed = replace(fixed, complete=False, work_limit=1)
    elif failure == "empty":
        fixed = replace(fixed, projections=())
    else:
        projection = fixed.projections[0]
        target = (
            replace(projection.target, encoding="foreign")
            if failure == "foreign"
            else view.plan.snapshot.resource_at(Address("docs/overview.md"))
        )
        fixed = replace(fixed, projections=(replace(projection, target=target),))
    monkeypatch.setattr(
        execution,
        "_project",
        lambda _plan, member, _mirrors: (
            branch if isinstance(member, BranchingGroundedMemberRecipe) else fixed
        ),
    )
    result = generate_witness_hypotheses(view.plan)
    family = result.attempts[0]
    assert family.disposition is G.FIXED_MEMBER_FAILED
    assert not result.generated
    assert not family.branches
    if failure in {"support", "foreign"}:
        assert family.members[1].disposition is G.INVALID_MEMBER
        assert family.members[1].failure_reason


def test_fixed_duplicates_block_family(monkeypatch: pytest.MonkeyPatch) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",))
    recipe = view.plan.recipes[0]
    duplicated = replace(
        recipe,
        members=(*recipe.members, replace(recipe.members[1], key="extra")),
    )
    result = generate_witness_hypotheses(replace(view.plan, recipes=(duplicated,)))
    assert result.attempts[0].disposition is G.DUPLICATE_TARGET
    assert not result.attempts[0].branches


def test_complete_target_group_retains_all_support(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    view = _run(monkeypatch, ("src/devtools/alpha.py",), fixed=False)
    branch = view.attempts[0].members[0]
    projection = branch.projections[0]
    other = _ground(
        view.plan.task,
        view.plan.snapshot,
        PythonModuleLocator("devtools.alpha"),
        universe=_universe(view.plan.snapshot),
    )
    duplicate = replace(projection, structural=(OwnerResourceSupport(other),))
    grouped = replace(branch, projections=(duplicate, projection, projection))
    assert grouped.result_count == 1
    assert len(grouped.projections[0].structural) == 2
    assert replace(branch, projections=(projection, duplicate)) == grouped
    monkeypatch.setattr(execution, "_project", lambda _plan, _member, _mirrors: grouped)
    result = generate_witness_hypotheses(view.plan)
    assert len(result.generated) == 1
    assert result.generated[0].members[0].structural == grouped.structural


def test_two_families_and_cross_obligation_children(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py", "docs/overview.md"))
    recipe = view.plan.recipes[0]
    first = recipe.identity
    assert isinstance(first, WitnessHypothesisFamilyIdentity)
    recipes = (
        recipe,
        replace(recipe, identity=replace(first, value="second")),
        replace(
            recipe,
            identity=replace(first, obligation=view.plan.task.obligations[1].identity),
        ),
    )
    before = tuple(
        LocalizationAssessment(
            item.identity,
            view.plan.snapshot.repository_id,
            view.plan.snapshot.id,
            Disposition.OPEN,
        )
        for item in view.plan.task.obligations
    )
    result = generate_witness_hypotheses(replace(view.plan, recipes=recipes))
    reverse = generate_witness_hypotheses(
        replace(view.plan, recipes=tuple(reversed(recipes))),
    )
    assert result == reverse
    assert len(result.attempts) == 3
    assert len(result.generated) == 6
    assert len(result.for_obligation(first.obligation)) == 2
    assert len(result.cross_obligation_targets) == 3
    assert (
        len(
            result.for_target(
                view.plan.snapshot.resource_at(Address("tests/test_alpha.py")),
            ),
        )
        == 3
    )
    readiness = assess_localization_readiness(
        task=view.plan.task,
        repository_id=view.plan.snapshot.repository_id,
        snapshot_id=view.plan.snapshot.id,
        assessments=before,
    )
    assert readiness == assess_localization_readiness(
        task=result.plan.task,
        repository_id=result.plan.snapshot.repository_id,
        snapshot_id=result.plan.snapshot.id,
        assessments=before,
    )
    assert all(not item.supported_witnesses for item in before)


def test_generated_identity_frame_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",), fixed=False)
    child = view.generated[0]
    identity = child.identity
    assert isinstance(identity, GeneratedWitnessHypothesisIdentity)
    wrongs = (
        replace(identity, repository_id=RepositoryId.new()),
        replace(identity, snapshot_id=RepositorySnapshotId("f" * 64)),
    )
    for wrong in wrongs:
        with pytest.raises(ValueError, match="frame or branch target"):
            build_candidate_witness_view(
                task=view.plan.task,
                snapshot=view.plan.snapshot,
                hypotheses=(replace(child, identity=wrong),),
            )


def test_fixed_incomplete_projection_abstains(monkeypatch: pytest.MonkeyPatch) -> None:
    task, snapshot = _frame()
    seed = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    member = _member(seed)
    recipe = _recipe(task, member)
    plan = WitnessGenerationPlan(task, snapshot, (recipe,))
    native = execution._project(plan, member, None)  # noqa: SLF001
    monkeypatch.setattr(
        execution,
        "_project",
        lambda _plan, _member, _mirrors: replace(native, complete=False, work_limit=1),
    )
    result = generate_witness_hypotheses(plan)
    assert result.attempts[0].disposition is G.WORK_BOUND_EXCEEDED
    assert not result.generated


def test_canonical_key_collisions_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py",), fixed=False)
    attempt = view.attempts[0].members[0]
    projection = attempt.projections[0]
    altered = replace(projection, target=replace(projection.target, encoding="foreign"))
    with pytest.raises(ValueError, match="target stable key collides"):
        replace(attempt, projections=(projection, altered))
    grounding = projection.structural[0].grounding
    other = ground_task_anchor(
        task=view.plan.task,
        snapshot=view.plan.snapshot,
        request=replace(grounding.request, provenance=TaskProvenance("second-proof")),
    )
    with pytest.raises(ValueError, match="support stable key collides"):
        replace(
            projection,
            structural=(*projection.structural, OwnerResourceSupport(other)),
        )
    identity = view.generated[0].identity
    assert isinstance(identity, GeneratedWitnessHypothesisIdentity)
    left = replace(
        identity,
        family=replace(identity.family, value="a/b"),
        member_key="c",
    )
    right = replace(
        identity,
        family=replace(identity.family, value="a"),
        member_key="b/c",
    )
    assert left != right
    assert left.value != right.value


@pytest.mark.parametrize("failure", ["foreign", "empty-support"])
def test_branch_validation_failures_are_target_specific(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py", "docs/overview.md"))
    branch, fixed = view.attempts[0].members
    bad, good = branch.projections
    bad = (
        replace(bad, structural=())
        if failure == "empty-support"
        else replace(bad, target=replace(bad.target, encoding="foreign"))
    )
    modified = replace(branch, projections=(bad, good))
    monkeypatch.setattr(
        execution,
        "_project",
        lambda _plan, member, _mirrors: (
            modified if isinstance(member, BranchingGroundedMemberRecipe) else fixed
        ),
    )
    result = generate_witness_hypotheses(view.plan)
    assert len(result.generated) == 1
    assert len(result.attempts[0].failed_branches) == 1
    assert result.attempts[0].failed_branches[0].disposition is G.INVALID_BRANCH


def test_branch_cardinality_independent_of_supplemental_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    view = _run(monkeypatch, ("tests/test_alpha.py", "docs/overview.md"))
    task, snapshot = view.plan.task, view.plan.snapshot
    documents = _collection(
        tuple(
            _document(item.address.value, item.content) for item in snapshot.resources
        ),
    )
    index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=documents,
            ),
        ),
    )
    query = _query(task, "branch-support", 0, "alpha")
    acquisition = _execute(
        task,
        snapshot,
        index,
        purpose="locate",
        full_query="alpha",
        queries=(query,),
    )
    roles = derive_repository_role_evidence(snapshot)
    routing = route_localization_lexical_evidence(
        acquisition,
        roles,
        (
            ObligationRolePreference(
                query.identity,
                query.obligation,
                (RepositoryRoleKind.DOCUMENTATION,),
            ),
        ),
    )
    supported = generate_witness_hypotheses(
        replace(
            view.plan,
            acquisition=acquisition,
            role_evidence=roles,
            routing=routing,
        ),
    )
    assert tuple(item.identity for item in supported.generated) == tuple(
        item.identity for item in view.generated
    )
    for child in supported.generated:
        assert all(
            member.lexical and member.roles and member.routed
            for member in child.members
        )
        assert all(member.structural for member in child.members)
    target = snapshot.resource_at(Address("tests/test_alpha.py"))
    child = supported.for_target(target)[0]
    member = next(item for item in child.members if item.target == target)
    assert member.routed[0].candidate.tier.value == "escape"
