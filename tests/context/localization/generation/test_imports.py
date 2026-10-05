# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Generic direct import projections preserve native truth and bounded branching."""

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
    PythonImportDependencyProjectionRequest,
    PythonImportDependencyResourceSupport,
    PythonImportDependencySourceInput,
    WitnessHypothesisFamilyIdentity,
)
from devtools.context.localization.association.imports import (
    validate_import_dependency_frame,
    validate_import_dependency_support,
)
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
from devtools.context.localization.generation import GenerationDisposition as G
from devtools.context.localization.grounding import (
    PythonDirectDeclarationKind,
    PythonDirectDeclarationLocator,
    PythonDirectMethodLocator,
    PythonModuleLocator,
    ResourceAddressLocator,
)
from devtools.context.python.classes import derive_python_class_method_declarations
from devtools.context.python.imports import (
    PythonImportResolutionOutcome,
    derive_python_import_declarations,
    resolve_python_import_declaration,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    interpret_python_module_resources,
)
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
    _snapshot,
    _universe,
)

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.localization.generation import WitnessGenerationView
    from devtools.context.localization.grounding.contract import AnchorLocator
    from devtools.context.repository.snapshot import RepositorySnapshot


def _request(snapshot: RepositorySnapshot) -> PythonImportDependencyProjectionRequest:
    universe = _universe(snapshot)
    sources = []
    for module in universe.interpretations:
        analysis = derive_python_import_declarations(
            snapshot,
            resource_address=module.resource.address,
        )
        sources.append(
            PythonImportDependencySourceInput(
                module,
                analysis,
                tuple(
                    resolve_python_import_declaration(
                        analysis,
                        declaration,
                        target_universe=universe,
                        source_interpretations=(module,),
                    )
                    for declaration in analysis.declarations
                ),
            ),
        )
    return PythonImportDependencyProjectionRequest(universe, tuple(sources), 1)


def _run(
    snapshot: RepositorySnapshot,
    *,
    request: PythonImportDependencyProjectionRequest | None = None,
    locator: AnchorLocator | None = None,
    fixed: bool = False,
    max_results: int = 10,
) -> WitnessGenerationView:
    task = _frame()[0]
    request = request or _request(snapshot)
    grounding = _ground(
        task,
        snapshot,
        locator or PythonModuleLocator("pkg.source"),
        universe=request.module_universe,
    )
    branch = BranchingGroundedMemberRecipe(
        "imports",
        grounding,
        ProjectionKind.DIRECT_IMPORT_DEPENDENCY_RESOURCE,
        "one caller-proposed direct dependency",
        TaskProvenance("generic-fixture"),
        max_results,
    )
    recipe = WitnessGenerationRecipe(
        WitnessHypothesisFamilyIdentity(task.obligations[0].identity, "import-family"),
        (_member(grounding, key="owner"), branch) if fixed else (branch,),
        TaskProvenance("generic-family"),
    )
    return generate_witness_hypotheses(
        WitnessGenerationPlan(
            task,
            snapshot,
            (recipe,),
            python_import_dependencies=request,
        ),
    )


def _fixture(tmp_path: Path, syntax: str = "import pkg.target\n") -> RepositorySnapshot:
    return _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "from .target import Name\n",
            "src/pkg/source.py": syntax
            + "def work(): pass\nclass Service:\n    def run(self): pass\n",
            "src/pkg/target.py": "import pkg.leaf\nclass Name: pass\n",
            "src/pkg/leaf.py": "Name = 42\n",
            "src/pkg/other.py": "class Name: pass\n",
        },
    )


def _support(view: WitnessGenerationView) -> PythonImportDependencyResourceSupport:
    support = view.generated[0].members[0].structural[0]
    assert isinstance(support, PythonImportDependencyResourceSupport)
    return support


@pytest.mark.parametrize(
    "syntax",
    [
        "import pkg.target\n",
        "import pkg.target as m\n",
        "from pkg.target import Name\n",
        "from .target import Name as alias\n",
        "from pkg.target import unknown\n",
        "from . import target\n",
    ],
)
def test_supported_module_portions(tmp_path: Path, syntax: str) -> None:
    view = _run(_fixture(tmp_path, syntax))
    target = (
        "src/pkg/__init__.py"
        if syntax == "from . import target\n"
        else "src/pkg/target.py"
    )
    assert len(view.generated) == 1
    support = _support(view)
    assert support.relations[0].target.resource.address == Address(target)
    assert support.relations[0].source == support.source.module
    assert (
        support.relations[0].resolution.outcome
        is PythonImportResolutionOutcome.RESOLVED
    )
    assert support.request.identity
    assert support.identity
    assert view.attempts[0].members[0].work_performed == 1
    assert all(
        member.target.address != Address("src/pkg/leaf.py")
        for child in view.generated
        for member in child.members
    )


def test_grouping_provenance_and_no_facade_traversal(tmp_path: Path) -> None:
    view = _run(
        _fixture(
            tmp_path,
            "import pkg.target\nimport pkg.target as m\n"
            "from .target import Name as N\nfrom pkg import Name\n",
        ),
    )
    assert len(view.generated) == 2
    target = next(
        child
        for child in view.generated
        if child.members[0].target.address == Address("src/pkg/target.py")
    )
    support = target.members[0].structural[0]
    assert isinstance(support, PythonImportDependencyResourceSupport)
    assert len(support.relations) == 3
    assert {item.resolution.declaration.local_alias for item in support.relations} == {
        None,
        "m",
        "N",
    }
    assert len(target.members[0].structural) == 1
    facade = next(
        child
        for child in view.generated
        if child.members[0].target.address == Address("src/pkg/__init__.py")
    )
    assert len(facade.members[0].structural) == 1
    for child in view.generated:
        member = child.members[0]
        child_support = member.structural[0]
        assert isinstance(child_support, PythonImportDependencyResourceSupport)
        assert all(
            item.target.resource == member.target for item in child_support.relations
        )
    assert (
        generate_witness_hypotheses(
            replace(
                view.plan,
                python_import_dependencies=replace(
                    support.request,
                    sources=tuple(reversed(support.request.sources)),
                ),
            ),
        )
        == view
    )


@pytest.mark.parametrize(
    "syntax",
    [
        "import missing\n",
        "from ..beyond import Name\n",
        "from pkg.target import *\n",
        "__import__('pkg.target')\n",
        "def load():\n    import pkg.target\n",
        "if True:\n    import pkg.target\n",
        "",
    ],
)
def test_nonpositive_or_excluded_syntax(tmp_path: Path, syntax: str) -> None:
    view = _run(_fixture(tmp_path, syntax))
    assert not view.generated
    assert view.attempts[0].disposition is G.NO_TARGET
    assert view.attempts[0].members[0].complete
    assert view.attempts[0].members[0].result_count == 0


def test_ambiguous_import_has_no_target(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/source.py": "import duplicate\n",
            "src/duplicate.py": "",
            "src/duplicate/__init__.py": "",
        },
    )
    view = _run(snapshot)
    assert not view.generated
    assert _request(snapshot).sources[0].module.repository_id == snapshot.repository_id


@pytest.mark.parametrize("seed", ["function", "class", "method", "resource", "missing"])
def test_exact_seed_kinds(tmp_path: Path, seed: str) -> None:
    snapshot = _fixture(tmp_path)
    locators: dict[str, AnchorLocator] = {
        "function": PythonDirectDeclarationLocator(
            PythonModuleLocator("pkg.source"),
            "work",
            PythonDirectDeclarationKind.FUNCTION,
        ),
        "class": PythonDirectDeclarationLocator(
            PythonModuleLocator("pkg.source"),
            "Service",
            PythonDirectDeclarationKind.CLASS,
        ),
        "method": PythonDirectMethodLocator(
            derive_python_class_method_declarations(
                snapshot,
                resource_address=Address("src/pkg/source.py"),
            ).classes[0],
            "run",
        ),
        "resource": ResourceAddressLocator(Address("src/pkg/source.py")),
        "missing": PythonModuleLocator("absent"),
    }
    view = _run(snapshot, locator=locators[seed])
    assert bool(view.generated) == (seed in {"function", "class", "method"})


def test_missing_native_source_analysis(tmp_path: Path) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    view = _run(snapshot, request=replace(request, sources=()))
    assert view.attempts[0].disposition is G.UNSUPPORTED_SOURCE
    assert view.attempts[0].members[0].failure_reason


def test_ambiguous_method_owner(tmp_path: Path) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    other = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=(Address("src/pkg/source.py"),),
    ).interpretations[0]
    request = replace(
        request,
        module_universe=replace(
            request.module_universe,
            interpretations=(*request.module_universe.interpretations, other),
        ),
        sources=(),
    )
    parent = derive_python_class_method_declarations(
        snapshot,
        resource_address=Address("src/pkg/source.py"),
    ).classes[0]
    view = _run(
        snapshot,
        request=request,
        locator=PythonDirectMethodLocator(parent, "run"),
    )
    assert view.attempts[0].disposition is G.AMBIGUOUS_SOURCE


@pytest.mark.parametrize("bound", ["work", "result", "exact"])
def test_complete_bound_and_fixed_branch_semantics(tmp_path: Path, bound: str) -> None:
    snapshot = _fixture(
        tmp_path,
        "import pkg.target\nimport pkg.other\nimport pkg.source\n",
    )
    request = _request(snapshot)
    view = _run(
        snapshot,
        request=replace(request, work_limit=0) if bound == "work" else request,
        max_results=2 if bound == "result" else 3,
        fixed=True,
    )
    attempt = view.attempts[0]
    branch = next(item for item in attempt.members if item.recipe.key == "imports")
    if bound == "exact":
        assert attempt.disposition is G.GENERATED_WITH_BRANCH_FAILURES
        assert len(view.generated) == 2
        assert len(attempt.failed_branches) == 1
        assert attempt.failed_branches[0].disposition is G.DUPLICATE_TARGET
        assert all(len(child.members) == 2 for child in view.generated)
    else:
        assert attempt.disposition is (
            G.WORK_BOUND_EXCEEDED if bound == "work" else G.RESULT_BOUND_EXCEEDED
        )
        assert not view.generated
        assert not attempt.branches
        assert branch.result_count == (None if bound == "work" else 3)
        assert branch.work_performed == (0 if bound == "work" else 1)
        assert branch.complete == (bound != "work")
        assert bool(branch.uncovered_frontier) == (bound == "work")


def test_work_preflight_does_not_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot = _fixture(tmp_path)
    request = replace(_request(snapshot), work_limit=0)

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "source replay exceeded work authorization"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.localization.generation.imports.replay_import_dependency_source",
        forbidden,
    )
    assert not _run(snapshot, request=request).generated


@pytest.mark.parametrize(
    "alteration",
    [
        "repository",
        "snapshot",
        "module",
        "duplicate-universe",
        "analysis",
        "missing-resolution",
        "universe",
        "forged-resolution",
        "coverage",
    ],
)
def test_foreign_and_forged_native_inputs(tmp_path: Path, alteration: str) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    source = next(
        item for item in request.sources if item.module.dotted_name == "pkg.source"
    )
    if alteration == "repository":
        request = replace(
            request,
            module_universe=replace(
                request.module_universe,
                repository_id=RepositoryId.parse(
                    "00000000-0000-4000-8000-000000000099",
                ),
            ),
        )
    elif alteration in {"snapshot", "module"}:
        bad = (
            replace(source.module, snapshot_id=RepositorySnapshotId("f" * 64))
            if alteration == "snapshot"
            else replace(source.module, dotted_name="wrong")
        )
        request = replace(
            request,
            module_universe=replace(request.module_universe, interpretations=(bad,)),
        )
    elif alteration == "duplicate-universe":
        request = replace(
            request,
            module_universe=replace(
                request.module_universe,
                interpretations=(source.module, source.module),
            ),
        )
    else:
        if alteration == "analysis":
            source = replace(
                source,
                analysis=replace(
                    source.analysis,
                    snapshot_id=RepositorySnapshotId("f" * 64),
                ),
            )
        elif alteration == "missing-resolution":
            source = replace(source, resolutions=())
        elif alteration == "universe":
            source = replace(
                source,
                resolutions=(
                    replace(
                        source.resolutions[0],
                        target_universe=replace(
                            request.module_universe,
                            interpretations=(),
                        ),
                    ),
                ),
            )
        elif alteration == "coverage":
            source = replace(
                source,
                analysis=replace(
                    source.analysis,
                    coverage=replace(source.analysis.coverage, declaration_count=99),
                ),
            )
        else:
            source = replace(
                source,
                resolutions=(replace(source.resolutions[0], matches=(source.module,)),),
            )
        request = replace(request, sources=(source,))
    with pytest.raises(ValueError, match=r"Import dependency|Python module"):
        _run(snapshot, request=request)


@pytest.mark.parametrize("alteration", ["target", "relation", "source", "work", "seed"])
def test_forged_support(tmp_path: Path, alteration: str) -> None:
    view = _run(_fixture(tmp_path))
    support = _support(view)
    snapshot = view.plan.snapshot
    target = view.generated[0].members[0].target
    if alteration == "target":
        target = snapshot.resource_at(
            Address("src/pkg/other.py"),
        )  # same Name, different module
    elif alteration == "relation":
        support = replace(
            support,
            relations=(replace(support.relations[0], target=support.source.module),),
        )
    elif alteration == "source":
        support = replace(support, request=replace(support.request, sources=()))
    elif alteration == "work":
        support = replace(support, request=replace(support.request, work_limit=0))
    else:
        support = replace(
            support,
            grounding=_ground(
                view.plan.task,
                snapshot,
                PythonModuleLocator("pkg.other"),
                universe=support.request.module_universe,
            ),
        )
    with pytest.raises(ValueError, match="Import dependency"):
        validate_import_dependency_support(support, snapshot, target)


def test_empty_duplicate_and_colliding_support(tmp_path: Path) -> None:
    support = _support(_run(_fixture(tmp_path)))
    assert (
        replace(support, relations=(*support.relations, *support.relations)) == support
    )
    with pytest.raises(ValueError, match="unambiguous native relations"):
        replace(support, relations=())
    relation = support.relations[0]
    collision = replace(
        relation,
        source=replace(relation.source, snapshot_id=RepositorySnapshotId("f" * 64)),
    )
    with pytest.raises(ValueError, match="unambiguous native relations"):
        replace(support, relations=(relation, collision))
    assert (
        replace(
            support.request,
            sources=(*support.request.sources, *support.request.sources),
        )
        == support.request
    )
    with pytest.raises(ValueError, match="source identity collides"):
        replace(
            support.request,
            sources=(support.source, replace(support.source, resolutions=())),
        )
    with pytest.raises(ValueError, match="nonnegative"):
        replace(support.request, work_limit=-1)


@pytest.mark.parametrize("alteration", ["repository", "duplicates", "interpretation"])
def test_frame_checks_before_any_recipe_replay(tmp_path: Path, alteration: str) -> None:
    snapshot = _fixture(tmp_path)
    request = _request(snapshot)
    universe = request.module_universe
    if alteration == "repository":
        universe = replace(
            universe,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000099"),
        )
    elif alteration == "duplicates":
        universe = replace(
            universe,
            interpretations=(*universe.interpretations, universe.interpretations[0]),
        )
    else:
        universe = replace(
            universe,
            interpretations=(
                replace(universe.interpretations[0], dotted_name="invented"),
            ),
        )
    with pytest.raises(ValueError, match="Import dependency"):
        validate_import_dependency_frame(
            replace(request, module_universe=universe),
            snapshot,
        )


def test_plan_requires_native_inputs_and_branching(tmp_path: Path) -> None:
    view = _run(_fixture(tmp_path))
    with pytest.raises(ValueError, match="explicit native inputs"):
        generate_witness_hypotheses(replace(view.plan, python_import_dependencies=None))
    grounding = view.plan.recipes[0].members[0].grounding
    recipe = _recipe(
        view.plan.task,
        _member(grounding, ProjectionKind.DIRECT_IMPORT_DEPENDENCY_RESOURCE),
    )
    with pytest.raises(ValueError, match="branching member"):
        generate_witness_hypotheses(replace(view.plan, recipes=(recipe,)))


def test_candidates_leave_readiness_and_all_nonclaims_open(tmp_path: Path) -> None:
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
    assert before == assess_localization_readiness(
        task=again.plan.task,
        repository_id=again.plan.snapshot.repository_id,
        snapshot_id=again.plan.snapshot.id,
        assessments=assessments,
    )
    assert all(not item.supported_witnesses for item in assessments)
    assert not any(
        hasattr(view, field)
        for field in (
            "exports",
            "public_api",
            "runtime_result",
            "references",
            "relevant",
            "ranked",
            "accepted",
            "scores",
        )
    )
    support = _support(view)
    validate_structural_support(
        task=view.plan.task,
        snapshot=view.plan.snapshot,
        target=view.generated[0].members[0].target,
        support=support,
    )
