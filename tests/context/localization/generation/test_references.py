# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Exact Reference projection and integration with settled branching semantics."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import (
    Disposition,
    LocalizationAssessment,
    TaskProvenance,
    assess_localization_readiness,
)
from devtools.context.localization.association import (
    PythonReferenceProjectionRequest,
    PythonReferenceResourceSupport,
    PythonReferenceSourceInput,
    WitnessHypothesisFamilyIdentity,
)
from devtools.context.localization.association.references import reference_seed
from devtools.context.localization.association.structural import (
    validate_structural_support,
)
from devtools.context.localization.generation import (
    BranchingGroundedMemberRecipe,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    generate_witness_hypotheses,
)
from devtools.context.localization.generation import (
    GenerationDisposition as G,
)
from devtools.context.localization.grounding import (
    AnchorGroundingDisposition,
    PythonDirectDeclarationLocator,
    PythonDirectMethodLocator,
    PythonModuleLocator,
    ResourceAddressLocator,
)
from devtools.context.localization.grounding import (
    PythonDirectDeclarationKind as Kind,
)
from devtools.context.python.classes import derive_python_class_method_declarations
from devtools.context.python.references import PythonDeclarationReferenceRoute as Route
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import RepositoryResourceAddress as Address
from devtools.context.repository.snapshot import RepositorySnapshotId
from tests.context.localization.generation.test_generation import (
    _frame,
    _ground,
    _member,
    _recipe,
)
from tests.context.python.references.declarations.test_analysis import (
    _analysis,
    _snapshot,
    _universe,
)

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.localization.generation import WitnessGenerationView
    from devtools.context.localization.grounding.contract import AnchorLocator
    from devtools.context.repository.snapshot import RepositorySnapshot


def _request(
    snapshot: RepositorySnapshot,
    *,
    limit: int | None = None,
) -> PythonReferenceProjectionRequest:
    universe = _universe(snapshot)
    sources = tuple(
        PythonReferenceSourceInput(
            _analysis(snapshot, item.address.value),
            tuple(
                module for module in universe.interpretations if module.resource == item
            ),
        )
        for item in snapshot.resources
    )
    return PythonReferenceProjectionRequest(
        universe,
        sources,
        len(sources) if limit is None else limit,
    )


def _run(
    snapshot: RepositorySnapshot,
    *,
    locator: AnchorLocator | None = None,
    fixed: bool = False,
    max_results: int = 10,
    request: PythonReferenceProjectionRequest | None = None,
) -> WitnessGenerationView:
    task = _frame()[0]
    grounding = _ground(
        task,
        snapshot,
        locator
        or PythonDirectDeclarationLocator(
            PythonModuleLocator("pkg.impl"),
            "helper",
            Kind.FUNCTION,
        ),
        universe=_universe(snapshot),
    )
    branch = BranchingGroundedMemberRecipe(
        "references",
        grounding,
        ProjectionKind.REFERENCING_RESOURCE,
        "caller proposes one exact referencer",
        TaskProvenance("reference-shape"),
        max_results,
    )
    recipe = WitnessGenerationRecipe(
        WitnessHypothesisFamilyIdentity(
            task.obligations[0].identity,
            "reference-family",
        ),
        (_member(grounding, key="owner"), branch) if fixed else (branch,),
        TaskProvenance("caller-family"),
    )
    return generate_witness_hypotheses(
        WitnessGenerationPlan(
            task,
            snapshot,
            (recipe,),
            python_references=request or _request(snapshot),
        ),
    )


def _fixture(tmp_path: Path) -> RepositorySnapshot:
    return _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "from .impl import helper as exported\n",
            "src/pkg/impl.py": (
                "def helper(): pass\nclass Service:\n"
                "    def run(self): pass\nhelper()\n"
            ),
            "src/use.py": (
                "from pkg.impl import helper as named, Service\nimport pkg.impl as m\n"
                "from pkg import exported as public\nnamed()\nnamed\nm.helper()\n"
                "public()\nService()\nService.run()\nmissing\nobj.run()\n"
            ),
            "src/another.py": "from pkg.impl import helper\nhelper()\n",
            "src/method_only.py": "from pkg.impl import Service\nService.run()\n",
            "src/import_only.py": "from pkg.impl import helper\n",
            "src/other.py": "def helper(): pass\nhelper()\n",
            "src/uncertain.py": "from pkg.impl import helper\nhelper = 1\nhelper()\n",
        },
    )


def _support(view: WitnessGenerationView, path: str) -> PythonReferenceResourceSupport:
    target = view.plan.snapshot.resource_at(Address(path))
    member = next(
        item for item in view.for_target(target)[0].members if item.target == target
    )
    support = member.structural[0]
    assert isinstance(support, PythonReferenceResourceSupport)
    return support


def test_exact_routes_grouping_and_call_tags(tmp_path: Path) -> None:
    view = _run(_fixture(tmp_path))
    assert {
        item.target.address.value for child in view.generated for item in child.members
    } == {
        "src/pkg/impl.py",
        "src/use.py",
        "src/another.py",
    }
    support = _support(view, "src/use.py")
    assert len(support.references) == 4
    assert {fact.route for fact in support.references} == {
        Route.IMPORTED_MEMBER,
        Route.MODULE_QUALIFIED,
        Route.ONE_FACADE,
    }
    assert {fact.direct_call for fact in support.references} == {True, False}
    assert _support(view, "src/pkg/impl.py").references[0].route is Route.SAME_MODULE
    assert support.identity
    seed = reference_seed(support.grounding)
    assert seed is not None
    assert all(fact.target_subject == seed.subject for fact in support.references)
    assert len(view.generated) == 3  # occurrences do not create extra branches
    assert not hasattr(view, "ranked")
    assert not hasattr(view, "accepted")


def test_class_and_method_subjects_remain_distinct(tmp_path: Path) -> None:
    snapshot = _fixture(tmp_path)
    locator = PythonDirectDeclarationLocator(
        PythonModuleLocator("pkg.impl"),
        "Service",
        Kind.CLASS,
    )
    classes = _run(snapshot, locator=locator)
    assert len(classes.generated) == 1
    assert classes.generated[0].members[0].target.address == Address("src/use.py")
    support = _support(classes, "src/use.py")
    assert len(support.references) == 1
    knowledge = derive_python_class_method_declarations(
        snapshot,
        resource_address=Address("src/pkg/impl.py"),
    ).classes[0]
    methods = _run(snapshot, locator=PythonDirectMethodLocator(knowledge, "run"))
    assert len(methods.generated) == 2
    assert {
        fact.route
        for child in methods.generated
        for member in child.members
        for item in member.structural
        if isinstance(item, PythonReferenceResourceSupport)
        for fact in item.references
    } == {
        Route.CLASS_QUALIFIED_METHOD,
    }


@pytest.mark.parametrize(
    ("syntax", "kind"),
    [
        ("def helper(): pass", Kind.FUNCTION),
        ("async def helper(): pass", Kind.FUNCTION),
        ("class helper: pass", Kind.CLASS),
    ],
)
def test_decorated_declaration_grounding_does_not_manufacture_references(
    tmp_path: Path,
    syntax: str,
    kind: Kind,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "# package\n",
            "src/pkg/impl.py": "@decorator\n" + syntax + "\nhelper()\n",
            "src/use.py": "from pkg.impl import helper\nhelper()\n",
        },
    )
    locator = PythonDirectDeclarationLocator(
        PythonModuleLocator("pkg.impl"),
        "helper",
        kind,
    )
    view = _run(snapshot, locator=locator)
    branch = view.attempts[0].members[0]
    assert branch.recipe.grounding.disposition is AnchorGroundingDisposition.RESOLVED
    assert branch.complete
    assert branch.result_count == 0
    assert view.attempts[0].disposition is G.NO_TARGET
    assert not view.generated


@pytest.mark.parametrize("source", ["resource", "module", "missing", "unsupported"])
def test_unsupported_and_unresolved_sources(tmp_path: Path, source: str) -> None:
    snapshot = _fixture(tmp_path)
    locators: dict[str, AnchorLocator] = {
        "resource": ResourceAddressLocator(Address("src/pkg/impl.py")),
        "module": PythonModuleLocator("pkg.impl"),
        "missing": PythonDirectDeclarationLocator(
            PythonModuleLocator("pkg.impl"),
            "missing",
            Kind.FUNCTION,
        ),
        "unsupported": PythonDirectDeclarationLocator(
            PythonModuleLocator("absent"),
            "helper",
            Kind.FUNCTION,
        ),
    }
    view = _run(snapshot, locator=locators[source])
    assert view.attempts[0].disposition in {G.UNSUPPORTED_SOURCE, G.UNRESOLVED_SOURCE}
    assert not view.generated


def test_same_owner_collision_and_target_specific_support(tmp_path: Path) -> None:
    view = _run(_fixture(tmp_path), fixed=True)
    family = view.attempts[0]
    assert family.disposition is G.GENERATED_WITH_BRANCH_FAILURES
    assert len(family.branches) == 3
    assert len(view.generated) == 2
    assert family.failed_branches[0].disposition is G.DUPLICATE_TARGET
    assert family.failed_branches[0].projection.target.address == Address(
        "src/pkg/impl.py",
    )
    for child in view.generated:
        assert len(child.members) == 2
        assert view.parent_family(child.identity) == family  # type: ignore[arg-type]
        branch = next(
            item
            for item in child.members
            if isinstance(
                item.structural[0],
                PythonReferenceResourceSupport,
            )
        )
        support = branch.structural[0]
        assert isinstance(support, PythonReferenceResourceSupport)
        assert all(
            fact.occurrence.resource_address == branch.target.address
            for fact in support.references
        )


def test_complete_result_bound_and_incomplete_work(tmp_path: Path) -> None:
    snapshot = _fixture(tmp_path)
    within = _run(snapshot, max_results=3)
    assert len(within.generated) == 3
    overflow = _run(snapshot, max_results=2)
    assert overflow.attempts[0].disposition is G.RESULT_BOUND_EXCEEDED
    assert overflow.attempts[0].members[0].result_count == 3
    assert not overflow.generated
    assert not overflow.attempts[0].branches
    incomplete = _run(snapshot, request=_request(snapshot, limit=1))
    member = incomplete.attempts[0].members[0]
    assert incomplete.attempts[0].disposition is G.WORK_BOUND_EXCEEDED
    assert not member.complete
    assert member.result_count is None
    assert member.work_performed == 0
    assert member.work_limit == 1
    assert len(member.uncovered_frontier) == len(snapshot.resources)
    assert not incomplete.generated
    assert not incomplete.attempts[0].branches


def test_empty_frame_and_single_referencer_identity(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "# package\n",
            "src/pkg/impl.py": "def helper(): pass\n",
            "src/use.py": "from pkg.impl import helper\nhelper()\n",
        },
    )
    view = _run(snapshot, max_results=1, fixed=True)
    assert len(view.generated) == 1
    assert len(view.generated[0].members) == 2
    assert view.generated[0].identity.family == view.plan.recipes[0].identity  # type: ignore[union-attr]
    request = replace(_request(snapshot), sources=(), work_limit=0)
    empty = _run(snapshot, request=request)
    assert empty.attempts[0].disposition is G.NO_TARGET
    assert empty.attempts[0].members[0].complete
    assert empty.attempts[0].members[0].result_count == 0


def test_ordering_and_duplicate_support(tmp_path: Path) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    view = _run(snapshot, request=request)
    reversed_request = replace(request, sources=tuple(reversed(request.sources)))
    assert request == reversed_request
    assert _run(snapshot, request=reversed_request) == view
    assert replace(request, sources=(*request.sources, request.sources[0])) == request
    support = _support(view, "src/use.py")
    assert (
        replace(
            support,
            references=(*reversed(support.references), support.references[0]),
        )
        == support
    )
    with pytest.raises(ValueError, match="needs facts"):
        replace(support, references=())
    with pytest.raises(ValueError, match="nonnegative"):
        replace(request, work_limit=-1)


def test_explicit_projection_inputs_and_branch_authorization(tmp_path: Path) -> None:
    view = _run(_fixture(tmp_path))
    with pytest.raises(ValueError, match="explicit native inputs"):
        generate_witness_hypotheses(replace(view.plan, python_references=None))
    branch = view.plan.recipes[0].members[0]
    fixed = _member(branch.grounding, ProjectionKind.REFERENCING_RESOURCE)
    with pytest.raises(ValueError, match="branching member"):
        generate_witness_hypotheses(
            replace(view.plan, recipes=(_recipe(view.plan.task, fixed),)),
        )


@pytest.mark.parametrize("change", ["repository", "snapshot", "content", "universe"])
def test_analysis_frame_rejected(tmp_path: Path, change: str) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    source = request.sources[0]
    dependency = source.analysis.derivation.dependency
    if change == "repository":
        dependency = replace(dependency, repository_id=RepositoryId.new())
    elif change == "snapshot":
        dependency = replace(dependency, snapshot_id=RepositorySnapshotId("f" * 64))
    elif change == "content":
        dependency = replace(
            dependency,
            resource=replace(dependency.resource, content="altered"),
        )
    derivation = (
        replace(source.analysis.derivation, module_universe_identity="wrong")
        if change == "universe"
        else replace(source.analysis.derivation, dependency=dependency)
    )
    changed = replace(source, analysis=replace(source.analysis, derivation=derivation))
    request = replace(request, sources=(changed,))
    with pytest.raises(ValueError, match="frozen frame"):
        _run(snapshot, request=request)


@pytest.mark.parametrize("change", ["repository", "snapshot", "content"])
def test_universe_frame_rejected(tmp_path: Path, change: str) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    module = request.module_universe.interpretations[0]
    if change == "repository":
        module = replace(module, repository_id=RepositoryId.new())
    elif change == "snapshot":
        module = replace(module, snapshot_id=RepositorySnapshotId("f" * 64))
    else:
        module = replace(module, resource=replace(module.resource, content="altered"))
    universe = replace(request.module_universe, interpretations=(module,))
    with pytest.raises(ValueError, match="frozen snapshot"):
        _run(snapshot, request=replace(request, module_universe=universe))
    with pytest.raises(ValueError, match="foreign repository"):
        _run(
            snapshot,
            request=replace(
                request,
                module_universe=replace(
                    request.module_universe,
                    repository_id=RepositoryId.new(),
                ),
            ),
        )


def test_native_replay_rejects_forged_or_incomplete_analysis(tmp_path: Path) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    source = next(item for item in request.sources if item.analysis.references)
    changed = replace(source, analysis=replace(source.analysis, references=()))
    with pytest.raises(ValueError, match="canonical native replay"):
        _run(snapshot, request=replace(request, sources=(changed,)))
    with pytest.raises(ValueError, match="identity collides"):
        replace(request, sources=(source, changed))


@pytest.mark.parametrize(
    "change",
    ["target", "source", "frame", "resource-seed", "foreign-fact"],
)
def test_reference_support_replayed_not_trusted(tmp_path: Path, change: str) -> None:
    view = _run(_fixture(tmp_path))
    support = _support(view, "src/use.py")
    target = view.plan.snapshot.resource_at(Address("src/use.py"))
    if change == "target":
        target = view.plan.snapshot.resource_at(Address("src/another.py"))
    elif change == "source":
        support = replace(support, request=replace(support.request, sources=()))
    elif change == "frame":
        support = replace(support, request=replace(support.request, work_limit=0))
    elif change == "resource-seed":
        support = replace(
            support,
            grounding=_ground(
                view.plan.task,
                view.plan.snapshot,
                ResourceAddressLocator(Address("src/pkg/impl.py")),
            ),
        )
    else:
        support = replace(
            support,
            references=(
                replace(
                    support.references[0],
                    direct_call=not support.references[0].direct_call,
                ),
            ),
        )
    with pytest.raises(ValueError, match="Reference support"):
        validate_structural_support(
            task=view.plan.task,
            snapshot=view.plan.snapshot,
            target=target,
            support=support,
        )


@pytest.mark.parametrize("change", ["missing", "repository", "snapshot", "resource"])
def test_source_interpretation_inputs_rejected(tmp_path: Path, change: str) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    source = request.sources[0]
    module = source.source_interpretations[0]
    if change == "missing":
        changed = replace(source, source_interpretations=())
    else:
        if change == "repository":
            module = replace(module, repository_id=RepositoryId.new())
        elif change == "snapshot":
            module = replace(module, snapshot_id=RepositorySnapshotId("f" * 64))
        else:
            module = replace(
                module,
                resource=replace(module.resource, encoding="foreign"),
            )
        changed = replace(source, source_interpretations=(module,))
    with pytest.raises(ValueError, match="source interpretations"):
        _run(snapshot, request=replace(request, sources=(changed,)))


def test_duplicate_fact_key_collision_rejected(tmp_path: Path) -> None:
    view = _run(_fixture(tmp_path))
    support = _support(view, "src/use.py")
    fact = support.references[0]
    forged = replace(
        fact,
        target_resource=replace(fact.target_resource, encoding="foreign"),
    )
    assert forged.identity == fact.identity
    with pytest.raises(ValueError, match="unambiguous native identities"):
        replace(support, references=(fact, forged))


def test_base_expression_is_only_reference_support(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "# package\n",
            "src/pkg/impl.py": "class Service: pass\n",
            "src/use.py": "from pkg.impl import Service\nclass Child(Service): pass\n",
        },
    )
    locator = PythonDirectDeclarationLocator(
        PythonModuleLocator("pkg.impl"),
        "Service",
        Kind.CLASS,
    )
    view = _run(snapshot, locator=locator)
    assert len(view.generated) == 1
    support = _support(view, "src/use.py")
    assert len(support.references) == 1
    fact = support.references[0]
    assert not fact.direct_call
    assert fact.PROPOSITION == "bounded-expression-references-python-declaration"
    assert not hasattr(support, "inheritance")
    assert not hasattr(support, "runtime_call")


def test_ambiguous_grounding_abstains(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "# package\n",
            "src/pkg/impl.py": "def helper(): pass\ndef helper(): pass\nhelper()\n",
        },
    )
    view = _run(snapshot)
    assert view.attempts[0].disposition is G.AMBIGUOUS_SOURCE
    assert not view.generated


def test_universe_permutation_and_valid_support_replay(tmp_path: Path) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    reversed_request = replace(
        request,
        module_universe=replace(
            request.module_universe,
            interpretations=tuple(reversed(request.module_universe.interpretations)),
        ),
    )
    with pytest.raises(ValueError, match="canonical native replay"):
        _run(snapshot, request=reversed_request)
    view = _run(snapshot, request=request)
    for child in view.generated:
        member = child.members[0]
        validate_structural_support(
            task=view.plan.task,
            snapshot=snapshot,
            target=member.target,
            support=member.structural[0],
        )


@pytest.mark.parametrize(
    "change",
    ["declaration", "occurrence", "coverage", "assessment"],
)
def test_fact_and_coverage_integrity(tmp_path: Path, change: str) -> None:
    view = _run(_fixture(tmp_path))
    support = _support(view, "src/use.py")
    snapshot = view.plan.snapshot
    if change == "declaration":
        changed = replace(
            support,
            grounding=_ground(
                view.plan.task,
                snapshot,
                PythonDirectDeclarationLocator(
                    PythonModuleLocator("pkg.impl"),
                    "Service",
                    Kind.CLASS,
                ),
                universe=_universe(snapshot),
            ),
        )
        with pytest.raises(ValueError, match="seed or source target"):
            validate_structural_support(
                task=view.plan.task,
                snapshot=snapshot,
                target=snapshot.resource_at(Address("src/use.py")),
                support=changed,
            )
    else:
        analysis = support.source.analysis
        if change == "coverage":
            analysis = replace(
                analysis,
                coverage=replace(analysis.coverage, assessed_count=0),
            )
        elif change == "assessment":
            analysis = replace(analysis, assessments=())
        else:
            fact = analysis.references[0]
            foreign = replace(
                fact,
                occurrence=replace(
                    fact.occurrence,
                    resource_address=Address("src/another.py"),
                ),
            )
            analysis = replace(analysis, references=(foreign, *analysis.references[1:]))
        source = replace(support.source, analysis=analysis)
        with pytest.raises(ValueError, match="canonical native replay"):
            _run(snapshot, request=replace(support.request, sources=(source,)))


@pytest.mark.parametrize("bound", ["work", "result", "exact"])
def test_fixed_owner_branch_bounds(tmp_path: Path, bound: str) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot, limit=1) if bound == "work" else _request(snapshot)
    view = _run(
        snapshot,
        fixed=True,
        request=request,
        max_results=2 if bound == "result" else 3,
    )
    family = view.attempts[0]
    if bound == "exact":
        assert family.disposition is G.GENERATED_WITH_BRANCH_FAILURES
        assert len(view.generated) == 2
        assert len(family.failed_branches) == 1
    else:
        assert family.disposition is (
            G.WORK_BOUND_EXCEEDED if bound == "work" else G.RESULT_BOUND_EXCEEDED
        )
        assert not view.generated
        assert not family.branches


def test_work_preflight_performs_no_native_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot, limit=0)

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "oversized Reference frame was replayed"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.localization.association.references.derive_python_declaration_references",
        forbidden,
    )
    view = _run(snapshot, request=request)
    assert view.attempts[0].disposition is G.WORK_BOUND_EXCEEDED
    assert view.attempts[0].members[0].work_performed == 0


def test_reference_candidates_leave_readiness_open(tmp_path: Path) -> None:
    view = _run(_fixture(tmp_path))
    assessments = tuple(
        LocalizationAssessment(
            item.identity,
            view.plan.snapshot.repository_id,
            view.plan.snapshot.id,
            Disposition.OPEN,
        )
        for item in view.plan.task.obligations
    )
    before = assess_localization_readiness(
        task=view.plan.task,
        repository_id=view.plan.snapshot.repository_id,
        snapshot_id=view.plan.snapshot.id,
        assessments=assessments,
    )
    again = generate_witness_hypotheses(view.plan)
    assert again == view
    assert all(not item.supported_witnesses for item in assessments)
    assert before == assess_localization_readiness(
        task=again.plan.task,
        repository_id=again.plan.snapshot.repository_id,
        snapshot_id=again.plan.snapshot.id,
        assessments=assessments,
    )
    assert not hasattr(view, "relevant")
    assert not hasattr(view, "ranked")
    assert not hasattr(view, "scores")
    assert not hasattr(view, "accepted")
    assert not hasattr(view, "resolved")
