# Copyright (c) 2026
# ruff: noqa: D103
"""Exact task-anchor grounding preserves native identity and uncertainty."""

from __future__ import annotations

import hashlib
from dataclasses import replace
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import (
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    TaskProvenance,
)
from devtools.context.localization.grounding import (
    AnchorGrounding,
    AnchorGroundingCandidate,
    AnchorGroundingRequest,
    PythonDirectDeclarationKind,
    PythonDirectDeclarationLocator,
    PythonDirectMethodLocator,
    PythonModuleLocator,
    ResourceAddressLocator,
    build_anchor_grounding_view,
    ground_task_anchor,
)
from devtools.context.localization.grounding import (
    AnchorGroundingDisposition as D,
)
from devtools.context.localization.grounding.view import _locator_key
from devtools.context.python.classes import derive_python_class_method_declarations
from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonClassMethodParseError,
    PythonMethodDeclarationKnowledge,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
)
from devtools.context.python.modules import (
    PythonModuleInterpretation,
    PythonModuleInterpretationUniverse,
    PythonModuleKind,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.modules.declarations import PythonModuleDeclarationLookup
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import (
    ContentIdentity,
)
from devtools.context.repository.resource import (
    RepositoryResourceAddress as Address,
)
from devtools.context.repository.resource import (
    RepositoryResourceOccurrence as Occurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)

if TYPE_CHECKING:
    from devtools.context.localization.grounding.contract import AnchorLocator


def _frame() -> tuple[LocalizationTaskInterpretation, RepositorySnapshot]:
    task_id = LocalizationTaskIdentity("grounding-test")
    task = LocalizationTaskInterpretation(
        task_id,
        TaskProvenance("task"),
        tuple(
            LocalizationAnchor(LocalizationAnchorIdentity(task_id, name), name)
            for name in ("first", "second")
        ),
        (),
    )
    sources = (
        ("src/pkg/__init__.py", "class Thing:\n    def run(self): pass\n"),
        ("src/pkg.py", "def target(): pass\n"),
        ("src/duplicate.py", "def target(): pass\ndef target(): pass\n"),
        ("src/decorated.py", "@decorator\ndef target(): pass\n"),
        ("src/dynamic.py", "exec('def target(): pass')\n"),
        ("src/value.py", "target = 1\n"),
        ("src/broken.py", "def incomplete(\n"),
        ("scripts/validate.py", "print('ok')\n"),
    )
    resources = tuple(
        Occurrence(
            Address(address),
            ContentIdentity(hashlib.sha256(content.encode()).hexdigest()),
            content,
            "utf-8",
            len(content.encode()),
        )
        for address, content in sources
    )
    snapshot = RepositorySnapshot(
        RepositorySnapshotId("a" * 64),
        RepositoryId.parse("00000000-0000-0000-0000-000000000001"),
        resources,
    )
    return task, snapshot


def _universe(snapshot: RepositorySnapshot) -> PythonModuleInterpretationUniverse:
    analysis = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=tuple(
            item.address
            for item in snapshot.resources
            if item.address.value.endswith(".py")
            and item.address.value.startswith("src/")
        ),
    )
    return define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=analysis.interpretations,
    )


def _request(
    task: LocalizationTaskInterpretation,
    snapshot: RepositorySnapshot,
    locator: AnchorLocator,
    anchor: str = "first",
) -> AnchorGroundingRequest:
    return AnchorGroundingRequest(
        task.identity,
        LocalizationAnchorIdentity(task.identity, anchor),
        snapshot.repository_id,
        snapshot.id,
        locator,
        TaskProvenance("explicit-interpretation"),
    )


def test_resource_exact_miss_and_snapshot_safety() -> None:
    task, snapshot = _frame()
    locator = ResourceAddressLocator(Address("scripts/validate.py"))
    request = _request(task, snapshot, locator)
    found = ground_task_anchor(task=task, snapshot=snapshot, request=request)
    assert found.disposition is D.RESOLVED
    assert found.candidates[0].referent is snapshot.resource_at(locator.address)
    assert found.candidates[0].evidence is found.native_evidence[0]
    assert found.request.provenance.source_identity == "explicit-interpretation"
    assert (
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=_request(
                task,
                snapshot,
                ResourceAddressLocator(Address("missing.py")),
            ),
        ).disposition
        is D.UNRESOLVED
    )
    with pytest.raises(ValueError, match="another repository snapshot"):
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=replace(request, snapshot_id=RepositorySnapshotId("b" * 64)),
        )
    with pytest.raises(ValueError, match="another repository snapshot"):
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=replace(
                request,
                repository_id=RepositoryId.parse(
                    "00000000-0000-0000-0000-000000000002",
                ),
            ),
        )
    with pytest.raises(ValueError, match="unknown task anchor"):
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=_request(task, snapshot, locator, "unknown"),
        )


def test_module_name_preserves_package_module_ambiguity_and_kind() -> None:
    task, snapshot = _frame()
    universe = _universe(snapshot)
    both = ground_task_anchor(
        task=task,
        snapshot=snapshot,
        request=_request(task, snapshot, PythonModuleLocator("pkg")),
        module_universe=universe,
    )
    assert both.disposition is D.AMBIGUOUS
    assert {
        item.referent.kind
        for item in both.candidates
        if isinstance(item.referent, PythonModuleInterpretation)
    } == {
        PythonModuleKind.ORDINARY,
        PythonModuleKind.PACKAGE,
    }
    package = ground_task_anchor(
        task=task,
        snapshot=snapshot,
        request=_request(
            task,
            snapshot,
            PythonModuleLocator("pkg", PythonModuleKind.PACKAGE),
        ),
        module_universe=universe,
    )
    assert package.disposition is D.RESOLVED
    package_referent = package.candidates[0].referent
    assert isinstance(package_referent, PythonModuleInterpretation)
    assert package_referent.kind is PythonModuleKind.PACKAGE
    assert (
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=_request(task, snapshot, PythonModuleLocator("absent")),
            module_universe=universe,
        ).disposition
        is D.UNRESOLVED
    )
    assert (
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=_request(task, snapshot, PythonModuleLocator("pkg")),
        ).disposition
        is D.UNSUPPORTED
    )


def test_direct_declarations_and_methods_retain_native_analysis() -> None:
    task, snapshot = _frame()
    universe = _universe(snapshot)

    def ground(
        module: str,
        name: str,
        kind: PythonDirectDeclarationKind,
    ) -> AnchorGrounding:
        return ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=_request(
                task,
                snapshot,
                PythonDirectDeclarationLocator(PythonModuleLocator(module), name, kind),
            ),
            module_universe=universe,
        )

    function = ground("pkg", "target", PythonDirectDeclarationKind.FUNCTION)
    assert function.disposition is D.RESOLVED
    function_referent = function.candidates[0].referent
    function_evidence = function.candidates[0].evidence
    assert isinstance(function_referent, PythonFunctionDeclarationKnowledge)
    assert isinstance(function_evidence, PythonModuleDeclarationLookup)
    assert function_referent.declared_name == "target"
    assert function_evidence.target == function_referent
    cls = ground("pkg", "Thing", PythonDirectDeclarationKind.CLASS)
    assert cls.disposition is D.RESOLVED
    class_referent = cls.candidates[0].referent
    assert isinstance(class_referent, PythonClassDeclarationKnowledge)
    assert class_referent.declared_name == "Thing"
    assert (
        ground("pkg", "absent", PythonDirectDeclarationKind.CLASS).disposition
        is D.UNRESOLVED
    )
    assert (
        ground("duplicate", "target", PythonDirectDeclarationKind.FUNCTION).disposition
        is D.AMBIGUOUS
    )
    assert (
        ground("decorated", "target", PythonDirectDeclarationKind.FUNCTION).disposition
        is D.UNSUPPORTED
    )
    assert (
        ground("broken", "target", PythonDirectDeclarationKind.FUNCTION).disposition
        is D.UNSUPPORTED
    )
    assert (
        ground("dynamic", "target", PythonDirectDeclarationKind.FUNCTION).disposition
        is D.AMBIGUOUS
    )
    assert (
        ground("pkg", "target", PythonDirectDeclarationKind.CLASS).disposition
        is D.UNRESOLVED
    )
    assert (
        ground("value", "target", PythonDirectDeclarationKind.FUNCTION).disposition
        is D.UNSUPPORTED
    )

    parent = derive_python_class_method_declarations(
        snapshot,
        resource_address=Address("src/pkg/__init__.py"),
    ).classes[0]
    method = ground_task_anchor(
        task=task,
        snapshot=snapshot,
        request=_request(task, snapshot, PythonDirectMethodLocator(parent, "run")),
    )
    assert method.disposition is D.RESOLVED
    method_referent = method.candidates[0].referent
    assert isinstance(method_referent, PythonMethodDeclarationKnowledge)
    assert method_referent.containing_class == parent
    repeated = snapshot.resource_at(Address("src/pkg/__init__.py"))
    duplicate_methods = replace(
        repeated,
        content="class Thing:\n    def run(self): pass\n    def run(self): pass\n",
    )
    ambiguous_snapshot = replace(
        snapshot,
        resources=(duplicate_methods, *snapshot.resources[1:]),
    )
    ambiguous_parent = derive_python_class_method_declarations(
        ambiguous_snapshot,
        resource_address=Address("src/pkg/__init__.py"),
    ).classes[0]
    ambiguous_method = ground_task_anchor(
        task=task,
        snapshot=ambiguous_snapshot,
        request=_request(
            task,
            ambiguous_snapshot,
            PythonDirectMethodLocator(ambiguous_parent, "run"),
        ),
    )
    assert ambiguous_method.disposition is D.AMBIGUOUS
    assert len(ambiguous_method.candidates) == len(task.anchors)
    assert (
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=_request(
                task,
                snapshot,
                PythonDirectMethodLocator(parent, "missing"),
            ),
        ).disposition
        is D.UNRESOLVED
    )
    with pytest.raises(ValueError, match="stale"):
        ground_task_anchor(
            task=task,
            snapshot=replace(snapshot, id=RepositorySnapshotId("b" * 64)),
            request=replace(
                _request(task, snapshot, PythonDirectMethodLocator(parent, "run")),
                snapshot_id=RepositorySnapshotId("b" * 64),
            ),
        )
    with pytest.raises(ValueError, match="stale"):
        ground_task_anchor(
            task=task,
            snapshot=ambiguous_snapshot,
            request=_request(
                task,
                ambiguous_snapshot,
                PythonDirectMethodLocator(parent, "run"),
            ),
        )


def test_locator_and_result_contract_rejects_invalid_structure() -> None:
    task, snapshot = _frame()
    request = _request(
        task,
        snapshot,
        ResourceAddressLocator(Address("scripts/validate.py")),
    )
    valid = ground_task_anchor(task=task, snapshot=snapshot, request=request)
    for name in ("", "a..b", "a/b"):
        with pytest.raises(ValueError, match="dotted identifier"):
            PythonModuleLocator(name)
    with pytest.raises(ValueError, match="module kind"):
        PythonModuleLocator("pkg", "package")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="identifier name"):
        PythonDirectDeclarationLocator(
            PythonModuleLocator("pkg"),
            "a.b",
            PythonDirectDeclarationKind.CLASS,
        )
    with pytest.raises(TypeError, match="unsupported kind"):
        PythonDirectDeclarationLocator(PythonModuleLocator("pkg"), "Thing", "class")  # type: ignore[arg-type]
    parent = derive_python_class_method_declarations(
        snapshot,
        resource_address=Address("src/pkg/__init__.py"),
    ).classes[0]
    with pytest.raises(ValueError, match="identifier name"):
        PythonDirectMethodLocator(parent, "a.b")
    with pytest.raises(ValueError, match="another task"):
        replace(
            request,
            anchor=LocalizationAnchorIdentity(
                LocalizationTaskIdentity("other"),
                "first",
            ),
        )
    with pytest.raises(TypeError, match="unsupported locator"):
        replace(request, locator="scripts/validate.py")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="reason"):
        replace(valid, reason=" ")
    with pytest.raises(ValueError, match="exactly one"):
        replace(valid, candidates=())
    for disposition in (D.UNRESOLVED, D.UNSUPPORTED):
        with pytest.raises(ValueError, match="cannot claim"):
            replace(valid, disposition=disposition)
    assert AnchorGroundingCandidate(
        valid.candidates[0].referent,
        valid.candidates[0].evidence,
    )


def test_universe_frame_checks_and_view_locator_ordering() -> None:
    task, snapshot = _frame()
    universe = _universe(snapshot)
    module_request = _request(task, snapshot, PythonModuleLocator("pkg"))
    for changed, match in (
        (
            replace(
                universe,
                repository_id=RepositoryId.parse(
                    "00000000-0000-0000-0000-000000000002",
                ),
            ),
            "another repository",
        ),
        (
            replace(
                universe,
                interpretations=(
                    replace(
                        universe.interpretations[0],
                        snapshot_id=RepositorySnapshotId("b" * 64),
                    ),
                    *universe.interpretations[1:],
                ),
            ),
            "another snapshot",
        ),
        (
            replace(
                universe,
                interpretations=(
                    replace(universe.interpretations[0], dotted_name="wrong"),
                    *universe.interpretations[1:],
                ),
            ),
            "differs from native",
        ),
    ):
        with pytest.raises(ValueError, match=match):
            ground_task_anchor(
                task=task,
                snapshot=snapshot,
                request=module_request,
                module_universe=changed,
            )
    parent = derive_python_class_method_declarations(
        snapshot,
        resource_address=Address("src/pkg/__init__.py"),
    ).classes[0]
    requests = (
        module_request,
        _request(task, snapshot, PythonModuleLocator("pkg", PythonModuleKind.PACKAGE)),
        _request(
            task,
            snapshot,
            PythonDirectDeclarationLocator(
                PythonModuleLocator("pkg"),
                "Thing",
                PythonDirectDeclarationKind.CLASS,
            ),
        ),
        _request(task, snapshot, PythonDirectMethodLocator(parent, "run")),
    )
    view = build_anchor_grounding_view(
        task=task,
        snapshot=snapshot,
        requests=tuple(reversed(requests)),
        module_universe=universe,
    )
    assert view == build_anchor_grounding_view(
        task=task,
        snapshot=snapshot,
        requests=requests,
        module_universe=universe,
    )
    assert len(view.ambiguous) == 1
    assert len(view.resolved) == len(requests) - 1
    ambiguous_only = build_anchor_grounding_view(
        task=task,
        snapshot=snapshot,
        requests=(module_request,),
        module_universe=universe,
    )
    assert ambiguous_only.anchors_without_resolved_locator == tuple(
        anchor.identity for anchor in task.anchors
    )
    with pytest.raises(ValueError, match="unsupported locator"):
        _locator_key(SimpleNamespace(locator="invalid"))  # type: ignore[arg-type]


def test_native_method_parse_abstention(monkeypatch: pytest.MonkeyPatch) -> None:
    task, snapshot = _frame()
    analysis = derive_python_class_method_declarations(
        snapshot,
        resource_address=Address("src/pkg/__init__.py"),
    )
    parent = analysis.classes[0]
    failure = PythonClassMethodParseError(analysis.derivation, SyntaxError("broken"))

    def fail(*_args: object, **_kwargs: object) -> None:
        raise failure

    monkeypatch.setattr(
        "devtools.context.localization.grounding.resolve.derive_python_class_method_declarations",
        fail,
    )
    result = ground_task_anchor(
        task=task,
        snapshot=snapshot,
        request=_request(task, snapshot, PythonDirectMethodLocator(parent, "run")),
    )
    assert result.disposition is D.UNSUPPORTED


def test_deterministic_view_many_to_many_without_witness_or_readiness() -> None:
    task, snapshot = _frame()
    locator = ResourceAddressLocator(Address("scripts/validate.py"))
    first = _request(task, snapshot, locator)
    second = _request(task, snapshot, locator, "second")
    forward = build_anchor_grounding_view(
        task=task,
        snapshot=snapshot,
        requests=(second, first),
    )
    reverse = build_anchor_grounding_view(
        task=task,
        snapshot=snapshot,
        requests=(first, second),
    )
    assert forward == reverse
    assert forward.anchors_for_referent(snapshot.resource_at(locator.address)) == (
        task.anchors[0].identity,
        task.anchors[1].identity,
    )
    assert len(forward.resolved) == len(task.anchors)
    assert not forward.ambiguous
    assert not forward.unresolved
    assert not forward.unsupported
    assert forward.anchors_without_resolved_locator == ()
    assert forward.for_anchor(task.anchors[0].identity)[0].request == first
    assert task.obligations == ()
    assert not hasattr(forward, "witness_alternatives")
    assert not hasattr(forward, "candidate_hypotheses")
    assert not hasattr(forward, "readiness")
    assert not hasattr(forward, "confidence")
    with pytest.raises(ValueError, match="repeats"):
        build_anchor_grounding_view(
            task=task,
            snapshot=snapshot,
            requests=(first, first),
        )
    with pytest.raises(ValueError, match="Unknown task anchor"):
        forward.for_anchor(LocalizationAnchorIdentity(task.identity, "missing"))
    partial = build_anchor_grounding_view(
        task=task,
        snapshot=snapshot,
        requests=(first,),
    )
    assert partial.anchors_without_resolved_locator == (task.anchors[1].identity,)
