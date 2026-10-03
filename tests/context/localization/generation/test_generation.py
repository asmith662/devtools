# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Caller-shaped, low-fanout generation retains native proof and open status."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import (
    Disposition,
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationAssessment,
    LocalizationObligationIdentity,
    TaskProvenance,
    assess_localization_readiness,
)
from devtools.context.localization.association import (
    CandidateWitnessMember,
    MirroredResourceSupport,
    OwnerResourceSupport,
    WitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.generation import (
    GenerationDisposition as G,
)
from devtools.context.localization.generation import (
    GroundedMemberRecipe,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    generate_witness_hypotheses,
)
from devtools.context.localization.generation.generate import _project
from devtools.context.localization.grounding import (
    AnchorGroundingDisposition,
    AnchorGroundingRequest,
    PythonDirectDeclarationKind,
    PythonDirectDeclarationLocator,
    PythonDirectMethodLocator,
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
from devtools.context.python.classes import derive_python_class_method_declarations
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import RepositoryResourceAddress as Address
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)
from tests.context.localization.test_lexical import _execute, _inputs, _query
from tests.context.retrieval.lexical._helpers import _collection, _document

if TYPE_CHECKING:
    from devtools.context.localization.grounding import AnchorGrounding
    from devtools.context.localization.grounding.contract import AnchorLocator
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.python.modules import PythonModuleInterpretationUniverse

type LocatorCase = tuple[AnchorLocator, PythonModuleInterpretationUniverse | None]


def _frame() -> tuple[LocalizationTaskInterpretation, RepositorySnapshot]:
    task, baseline, _index = _inputs()
    documents = _collection(
        (
            _document("src/devtools/__init__.py", "# package\n"),
            _document(
                "src/devtools/alpha.py",
                "class Thing:\n    def run(self): return 'alpha'\n"
                "def target(): return 'alpha'\n",
            ),
            _document("src/devtools/orphan.py", "def orphan(): pass\n"),
            _document("tests/test_alpha.py", "def test_alpha(): pass\n# alpha\n"),
            _document("docs/overview.md", "alpha documentation\n"),
        ),
    )
    return task, RepositorySnapshot(
        baseline.id,
        baseline.repository_id,
        tuple(item.resource for item in documents.documents),
    )


def _universe(snapshot: RepositorySnapshot) -> PythonModuleInterpretationUniverse:
    analysis = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=tuple(
            item.address
            for item in snapshot.resources
            if item.address.value.startswith("src/")
        ),
    )
    return define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=analysis.interpretations,
    )


def _ground(
    task: LocalizationTaskInterpretation,
    snapshot: RepositorySnapshot,
    locator: AnchorLocator,
    *,
    universe: PythonModuleInterpretationUniverse | None = None,
) -> AnchorGrounding:
    request = AnchorGroundingRequest(
        task.identity,
        task.anchors[0].identity,
        snapshot.repository_id,
        snapshot.id,
        locator,
        TaskProvenance("caller-locator"),
    )
    return ground_task_anchor(
        task=task,
        snapshot=snapshot,
        request=request,
        module_universe=universe,
    )


def _member(
    grounding: AnchorGrounding,
    projection: ProjectionKind = ProjectionKind.OWNER_RESOURCE,
    key: str = "one",
) -> GroundedMemberRecipe:
    return GroundedMemberRecipe(
        key,
        grounding,
        projection,
        "caller proposes this resource",
        TaskProvenance("recipe"),
    )


def _recipe(
    task: LocalizationTaskInterpretation,
    *members: GroundedMemberRecipe,
    obligation: int = 0,
    key: str = "alternative",
) -> WitnessGenerationRecipe:
    return WitnessGenerationRecipe(
        WitnessHypothesisIdentity(task.obligations[obligation].identity, key),
        tuple(members),
        TaskProvenance("shape"),
    )


def test_owner_projection_native_referents() -> None:
    task, snapshot = _frame()
    universe = _universe(snapshot)
    module = PythonModuleLocator("devtools.alpha")
    parent = derive_python_class_method_declarations(
        snapshot,
        resource_address=Address("src/devtools/alpha.py"),
    ).classes[0]
    locators: tuple[LocatorCase, ...] = (
        (ResourceAddressLocator(Address("src/devtools/alpha.py")), None),
        (module, universe),
        (
            PythonDirectDeclarationLocator(
                module,
                "target",
                PythonDirectDeclarationKind.FUNCTION,
            ),
            universe,
        ),
        (
            PythonDirectDeclarationLocator(
                module,
                "Thing",
                PythonDirectDeclarationKind.CLASS,
            ),
            universe,
        ),
        (PythonDirectMethodLocator(parent, "run"), None),
    )
    for index, (locator, scope) in enumerate(locators):
        grounding = _ground(task, snapshot, locator, universe=scope)
        recipe = _recipe(task, _member(grounding, key=str(index)))
        view = generate_witness_hypotheses(
            WitnessGenerationPlan(task, snapshot, (recipe,)),
        )
        attempt = view.attempts[0].members[0]
        assert attempt.disposition is G.GENERATED
        assert attempt.result_count == 1
        assert attempt.result_limit == 1
        assert not attempt.truncated
        assert not attempt.uncovered_frontier
        assert attempt.examined_resources == 1
        assert attempt.targets == (
            snapshot.resource_at(Address("src/devtools/alpha.py")),
        )
        assert isinstance(attempt.structural[0], OwnerResourceSupport)
        assert attempt.structural[0].grounding == grounding
        assert view.generated[0].members[0].structural == attempt.structural
        assert not view.generated[0].members[0].lexical


def test_mirror_projection_and_no_target_are_bounded() -> None:
    task, snapshot = _frame()
    source = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    test = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("tests/test_alpha.py")),
    )
    orphan = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/orphan.py")),
    )
    recipes = (
        _recipe(task, _member(source, ProjectionKind.MIRRORED_RESOURCE), key="test"),
        _recipe(task, _member(test, ProjectionKind.MIRRORED_RESOURCE), key="source"),
        _recipe(task, _member(orphan, ProjectionKind.MIRRORED_RESOURCE), key="missing"),
    )
    view = generate_witness_hypotheses(WitnessGenerationPlan(task, snapshot, recipes))
    assert len(view.generated) == 2
    assert len(view.no_target) == 1
    assert view.no_target[0].source == orphan.candidates[0].referent
    assert view.no_target[0].examined_resources == len(snapshot.resources)
    assert view.no_target[0].mirror_analysis is not None
    assert view.no_target[0].mirror_analysis.coverage.IS_EXHAUSTIVE_FOR_SELECTION
    assert view.no_target[0].targets == ()
    test_attempt = next(
        item for item in view.attempts if item.recipe.identity.value == "test"
    )
    assert test_attempt.hypothesis is not None
    support = test_attempt.hypothesis.members[0].structural[0]
    assert isinstance(support, MirroredResourceSupport)
    assert support.correspondence.source == snapshot.resource_at(
        Address("src/devtools/alpha.py"),
    )
    assert support.correspondence.test == snapshot.resource_at(
        Address("tests/test_alpha.py"),
    )
    assert test_attempt.members[0].targets == (support.correspondence.test,)
    reverse = next(
        item for item in view.attempts if item.recipe.identity.value == "source"
    )
    assert reverse.members[0].targets == (support.correspondence.source,)


def test_caller_shape_complementarity_competition_and_cross_obligation() -> None:
    task, snapshot = _frame()
    ground = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    owner = _member(ground, key="owner")
    mirror = _member(ground, ProjectionKind.MIRRORED_RESOURCE, "test")
    combined = _recipe(task, owner, mirror, key="combined")
    competing = _recipe(task, owner, key="single")
    cross = _recipe(task, owner, obligation=1, key="other-obligation")
    forward = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (cross, combined, competing)),
    )
    reverse = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (competing, combined, cross)),
    )
    assert forward == reverse
    assert len(forward.generated) == 3
    assert len(forward.for_obligation(task.obligations[0].identity)) == 2
    assert len(forward.for_anchor(task.anchors[0].identity)) == 4
    assert len(forward.generated[0].members) == 2
    assert len(forward.generated[1].members) == 1
    target = snapshot.resource_at(Address("src/devtools/alpha.py"))
    assert len(forward.for_target(target)) == 3
    assert forward.cross_obligation_targets == (target,)
    duplicate = _recipe(
        task,
        owner,
        _member(ground, key="same-target"),
        key="duplicate",
    )
    refused = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (duplicate,)),
    )
    assert refused.attempts[0].disposition is G.DUPLICATE_TARGET
    assert not refused.generated


def test_unresolved_ambiguous_and_unsupported_grounding_never_guess() -> None:
    task, snapshot = _frame()
    unresolved = _ground(task, snapshot, ResourceAddressLocator(Address("missing.py")))
    unsupported = _ground(task, snapshot, PythonModuleLocator("devtools.alpha"))
    recipe = _recipe(task, _member(unresolved), _member(unsupported, key="two"))
    view = generate_witness_hypotheses(WitnessGenerationPlan(task, snapshot, (recipe,)))
    assert [item.disposition for item in view.attempts[0].members] == [
        G.UNRESOLVED_SOURCE,
        G.UNSUPPORTED_SOURCE,
    ]
    assert not view.generated
    assert view.attempts[0].members[0].source is None
    unvalidated = CandidateWitnessMember(
        snapshot.resources[0],
        "retained for validation",
        structural=(OwnerResourceSupport(unresolved),),
    )
    assert unvalidated.structural[0].grounding is unresolved


def test_native_evidence_is_supplemental_including_escape() -> None:
    task, snapshot = _frame()
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
    queries = (
        _query(task, "impl", 0, "alpha"),
        _query(task, "tests", 1, "alpha"),
    )
    acquisition = _execute(
        task,
        snapshot,
        index,
        purpose="locate",
        full_query="alpha",
        queries=queries,
    )
    roles = derive_repository_role_evidence(snapshot)
    routing = route_localization_lexical_evidence(
        acquisition,
        roles,
        tuple(
            ObligationRolePreference(
                q.identity,
                q.obligation,
                (RepositoryRoleKind.DOCUMENTATION,),
            )
            for q in queries
        ),
    )
    ground = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    recipe = _recipe(task, _member(ground, ProjectionKind.MIRRORED_RESOURCE))
    view = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (recipe,), acquisition, roles, routing),
    )
    member = view.generated[0].members[0]
    assert member.target.address == Address("tests/test_alpha.py")
    assert member.lexical
    assert member.roles
    assert member.routed
    assert member.routed[0].candidate.tier.value == "escape"
    assert member.structural
    assert not hasattr(member, "confidence")
    assert not hasattr(view, "accepted")
    assert not hasattr(view, "eliminated")
    assert not hasattr(view, "ranked")
    assert not generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (), acquisition, roles, routing),
    ).generated
    no_match_acquisition = _execute(
        task,
        snapshot,
        index,
        purpose="locate",
        full_query="unlikelyunmatchedtoken",
        queries=(),
    )
    no_match_view = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (recipe,), no_match_acquisition),
    )
    assert no_match_view.generated
    assert not no_match_view.generated[0].members[0].lexical
    assessments = tuple(
        LocalizationAssessment(
            item.identity,
            snapshot.repository_id,
            snapshot.id,
            Disposition.OPEN,
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
    assert task.obligations[0].witness_alternatives


def test_caller_contract_and_view_rejections() -> None:
    task, snapshot = _frame()
    ground = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    member = _member(ground)
    recipe = _recipe(task, member)
    with pytest.raises(ValueError, match="key and interpretation"):
        replace(member, key=" ")
    with pytest.raises(ValueError, match="key and interpretation"):
        replace(member, reason=" ")
    with pytest.raises(TypeError, match="unsupported projection"):
        replace(member, projection="neighbors")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least one member"):
        replace(recipe, members=())
    with pytest.raises(ValueError, match="repeats a member key"):
        replace(recipe, members=(member, member))
    with pytest.raises(ValueError, match="repeats a hypothesis"):
        WitnessGenerationPlan(task, snapshot, (recipe, recipe))
    view = generate_witness_hypotheses(WitnessGenerationPlan(task, snapshot, (recipe,)))
    with pytest.raises(ValueError, match="no such obligation"):
        view.for_obligation(LocalizationObligationIdentity(task.identity, "other"))
    with pytest.raises(ValueError, match="no such anchor"):
        view.for_anchor(LocalizationAnchorIdentity(task.identity, "other"))
    with pytest.raises(ValueError, match="unknown task obligation"):
        generate_witness_hypotheses(
            WitnessGenerationPlan(
                task,
                snapshot,
                (
                    replace(
                        recipe,
                        identity=WitnessHypothesisIdentity(
                            LocalizationObligationIdentity(task.identity, "other"),
                            "x",
                        ),
                    ),
                ),
            ),
        )
    stale = replace(ground, reason="altered")
    with pytest.raises(ValueError, match="stale or altered"):
        generate_witness_hypotheses(
            WitnessGenerationPlan(task, snapshot, (_recipe(task, _member(stale)),)),
        )
    other_anchor = LocalizationAnchorIdentity(task.identity, "other")
    expanded_task = replace(
        task,
        anchors=(*task.anchors, LocalizationAnchor(other_anchor, "other")),
    )
    other_ground = ground_task_anchor(
        task=expanded_task,
        snapshot=snapshot,
        request=replace(ground.request, anchor=other_anchor),
    )
    with pytest.raises(ValueError, match="not linked"):
        generate_witness_hypotheses(
            WitnessGenerationPlan(
                expanded_task,
                snapshot,
                (_recipe(expanded_task, _member(other_ground)),),
            ),
        )


def test_ambiguous_source_and_multi_target_abstain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    task, snapshot = _frame()
    alternate = _document("alt/devtools/alpha.py", "def target(): pass\n").resource
    expanded = replace(snapshot, resources=(*snapshot.resources, alternate))
    src_analysis = interpret_python_module_resources(
        expanded,
        module_root=PythonModuleRoot("src"),
        resource_addresses=(Address("src/devtools/alpha.py"),),
    )
    alt_analysis = interpret_python_module_resources(
        expanded,
        module_root=PythonModuleRoot("alt"),
        resource_addresses=(alternate.address,),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=expanded.repository_id,
        interpretations=(*src_analysis.interpretations, *alt_analysis.interpretations),
    )
    ambiguous = _ground(
        task,
        expanded,
        PythonModuleLocator("devtools.alpha"),
        universe=universe,
    )
    assert ambiguous.disposition is AnchorGroundingDisposition.AMBIGUOUS
    view = generate_witness_hypotheses(
        WitnessGenerationPlan(task, expanded, (_recipe(task, _member(ambiguous)),)),
    )
    assert view.attempts[0].disposition is G.AMBIGUOUS_SOURCE
    assert not view.generated

    def should_not_derive(_snapshot: RepositorySnapshot) -> None:
        msg = "mirror analysis ran for an unresolved source"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.localization.generation.generate.derive_python_mirrored_path_correspondences",
        should_not_derive,
    )
    unresolved_mirror = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("missing.py")),
    )
    mirror_member = _member(unresolved_mirror, ProjectionKind.MIRRORED_RESOURCE)
    mirror_recipe = _recipe(task, mirror_member)
    missed = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (mirror_recipe,)),
    )
    assert missed.attempts[0].disposition is G.UNRESOLVED_SOURCE

    owner = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    analysis = derive_python_mirrored_path_correspondences(snapshot)
    duplicate = replace(
        analysis.correspondences[0],
        test=snapshot.resource_at(Address("docs/overview.md")),
    )
    monkeypatch.setattr(
        "devtools.context.localization.generation.generate.derive_python_mirrored_path_correspondences",
        lambda _snapshot: replace(
            analysis,
            correspondences=(*analysis.correspondences, duplicate),
        ),
    )
    recipe = _recipe(task, _member(owner, ProjectionKind.MIRRORED_RESOURCE))
    result = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (recipe,)),
    )
    assert result.attempts[0].disposition is G.MULTI_TARGET
    assert result.attempts[0].members[0].result_count == 2
    assert not result.generated
    with pytest.raises(ValueError, match="requires the native"):
        _project(
            WitnessGenerationPlan(task, snapshot, (recipe,)),
            recipe.members[0],
            None,
        )


def test_structural_support_rejects_forgery_and_foreign_frames() -> None:
    task, snapshot = _frame()
    ground = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    owner = _recipe(task, _member(ground))
    generated = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (owner,)),
    )
    hypothesis = generated.generated[0]
    member = hypothesis.members[0]
    with pytest.raises(ValueError, match="repeats structural"):
        replace(member, structural=member.structural * 2)
    altered = replace(ground, reason="altered")
    with pytest.raises(ValueError, match="no current unique"):
        build_candidate_witness_view(
            task=task,
            snapshot=snapshot,
            hypotheses=(
                replace(
                    hypothesis,
                    members=(
                        replace(member, structural=(OwnerResourceSupport(altered),)),
                    ),
                ),
            ),
        )
    wrong_target = snapshot.resource_at(Address("docs/overview.md"))
    with pytest.raises(ValueError, match="Owner support target differs"):
        build_candidate_witness_view(
            task=task,
            snapshot=snapshot,
            hypotheses=(
                replace(hypothesis, members=(replace(member, target=wrong_target),)),
            ),
        )
    mirror_recipe = _recipe(task, _member(ground, ProjectionKind.MIRRORED_RESOURCE))
    mirrored = generate_witness_hypotheses(
        WitnessGenerationPlan(task, snapshot, (mirror_recipe,)),
    )
    mirror_member = mirrored.generated[0].members[0]
    support = mirror_member.structural[0]
    assert isinstance(support, MirroredResourceSupport)
    forged = replace(
        support,
        correspondence=replace(support.correspondence, test=wrong_target),
    )
    with pytest.raises(ValueError, match="Mirrored support differs"):
        build_candidate_witness_view(
            task=task,
            snapshot=snapshot,
            hypotheses=(
                replace(
                    mirrored.generated[0],
                    members=(replace(mirror_member, structural=(forged,)),),
                ),
            ),
        )
    foreign = replace(
        snapshot,
        repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000002"),
    )
    with pytest.raises(ValueError, match="another repository snapshot"):
        generate_witness_hypotheses(WitnessGenerationPlan(task, foreign, (owner,)))
    stale = replace(snapshot, id=RepositorySnapshotId("b" * 64))
    with pytest.raises(ValueError, match="another repository snapshot"):
        generate_witness_hypotheses(WitnessGenerationPlan(task, stale, (owner,)))


def test_foreign_native_supplemental_views_are_rejected() -> None:
    task, snapshot = _frame()
    ground = _ground(
        task,
        snapshot,
        ResourceAddressLocator(Address("src/devtools/alpha.py")),
    )
    recipe = _recipe(task, _member(ground))
    other_task, other_snapshot, index = _inputs()
    query = _query(other_task, "foreign", 0, "Obligation")
    foreign_acquisition = _execute(
        other_task,
        other_snapshot,
        index,
        purpose="foreign",
        full_query="Obligation",
        queries=(query,),
    )
    foreign_roles = derive_repository_role_evidence(other_snapshot)
    foreign_routing = route_localization_lexical_evidence(
        foreign_acquisition,
        foreign_roles,
        (ObligationRolePreference(query.identity, query.obligation, ()),),
    )
    with pytest.raises(ValueError, match="Lexical corpus resource is absent"):
        generate_witness_hypotheses(
            WitnessGenerationPlan(task, snapshot, (recipe,), foreign_acquisition),
        )
    with pytest.raises(ValueError, match="Role evidence differs"):
        generate_witness_hypotheses(
            WitnessGenerationPlan(
                task,
                snapshot,
                (recipe,),
                role_evidence=foreign_roles,
            ),
        )
    with pytest.raises(ValueError, match="Routing view differs"):
        generate_witness_hypotheses(
            WitnessGenerationPlan(task, snapshot, (recipe,), routing=foreign_routing),
        )
