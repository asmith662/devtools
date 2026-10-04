# Copyright (c) 2026
"""Delegate exact task-anchor locators to existing repository intelligence."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from devtools.context.localization.grounding.contract import (
    AnchorGrounding,
    AnchorGroundingCandidate,
    AnchorGroundingDisposition,
    AnchorGroundingRequest,
    GroundingResolver,
    PythonDirectDeclarationLocator,
    PythonDirectMethodLocator,
    PythonModuleLocator,
    ResourceAddressLocator,
)
from devtools.context.python.classes import (
    PythonClassMethodAnalysisAggregate,
    PythonClassMethodParseError,
    build_python_class_method_containment_view,
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    PythonModuleParseError,
)
from devtools.context.python.modules import (
    PythonModuleInterpretationUniverse,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
    lookup_python_modules,
)
from devtools.context.python.modules.selection import (
    PythonSourceDeclarationKind,
    select_python_module_source_declarations,
)
from devtools.context.repository.resource import RepositoryResourceOccurrence

if TYPE_CHECKING:
    from devtools.context.localization.grounding.contract import (
        NativeGroundingEvidence,
        NativeGroundingReferent,
    )
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


def ground_task_anchor(
    *,
    task: LocalizationTaskInterpretation,
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    module_universe: PythonModuleInterpretationUniverse | None = None,
) -> AnchorGrounding:
    """Resolve only the supplied locator, without interpreting anchor text."""
    if request.task != task.identity or request.anchor not in {
        item.identity for item in task.anchors
    }:
        msg = "Grounding request names a foreign or unknown task anchor."
        raise ValueError(msg)
    if (
        request.repository_id != snapshot.repository_id
        or request.snapshot_id != snapshot.id
    ):
        msg = "Grounding request belongs to another repository snapshot."
        raise ValueError(msg)
    locator = request.locator
    if isinstance(locator, ResourceAddressLocator):
        return _ground_resource(snapshot, request, locator)
    if isinstance(locator, PythonDirectMethodLocator):
        return _ground_method(snapshot, request, locator)
    if module_universe is None:
        resolver = (
            GroundingResolver.PYTHON_MODULE_LOOKUP
            if isinstance(locator, PythonModuleLocator)
            else GroundingResolver.PYTHON_SOURCE_DECLARATION_SELECTION
        )
        return _account(
            request,
            resolver,
            (),
            (),
            None,
            AnchorGroundingDisposition.UNSUPPORTED,
            "An explicit native Python module universe is required.",
        )
    _validate_universe(snapshot, module_universe)
    if isinstance(locator, PythonModuleLocator):
        return _ground_module(request, locator, module_universe)
    return _ground_declaration(snapshot, request, locator, module_universe)


def _ground_resource(
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    locator: ResourceAddressLocator,
) -> AnchorGrounding:
    try:
        resource = snapshot.resource_at(locator.address)
    except ValueError:
        return _account(
            request,
            GroundingResolver.SNAPSHOT_RESOURCE_AT,
            (),
            (),
            None,
            AnchorGroundingDisposition.UNRESOLVED,
            "Exact address is absent from the supplied observed snapshot.",
        )
    return _account(
        request,
        GroundingResolver.SNAPSHOT_RESOURCE_AT,
        (AnchorGroundingCandidate(resource, resource),),
        (resource,),
        None,
        AnchorGroundingDisposition.RESOLVED,
        "Exact address identifies one observed resource occurrence.",
    )


def _ground_module(
    request: AnchorGroundingRequest,
    locator: PythonModuleLocator,
    universe: PythonModuleInterpretationUniverse,
) -> AnchorGrounding:
    matches = tuple(
        item
        for item in lookup_python_modules(universe, locator.dotted_name)
        if locator.kind is None or item.kind is locator.kind
    )
    candidates = tuple(AnchorGroundingCandidate(item, item) for item in matches)
    disposition = _candidate_disposition(candidates)
    return _account(
        request,
        GroundingResolver.PYTHON_MODULE_LOOKUP,
        candidates,
        matches,
        universe,
        disposition,
        "Exact dotted name matched within the supplied explicit-root universe."
        if matches
        else "No exact module interpretation matched in the supplied universe.",
    )


def _ground_declaration(
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    locator: PythonDirectDeclarationLocator,
    universe: PythonModuleInterpretationUniverse,
) -> AnchorGrounding:
    modules = tuple(
        item
        for item in lookup_python_modules(universe, locator.module.dotted_name)
        if locator.module.kind is None or item.kind is locator.module.kind
    )
    observations: list[NativeGroundingEvidence] = []
    candidates: list[AnchorGroundingCandidate] = []
    unsupported = False
    for module in modules:
        try:
            selection = select_python_module_source_declarations(
                snapshot,
                module=module,
                declared_name=locator.declared_name,
                kind=PythonSourceDeclarationKind(locator.kind.value),
            )
        except (PythonModuleParseError, PythonClassMethodParseError, SyntaxError):
            unsupported = True
            continue
        observations.append(selection)
        candidates.extend(
            AnchorGroundingCandidate(item, selection) for item in selection.declarations
        )
    disposition = (
        AnchorGroundingDisposition.AMBIGUOUS
        if len(candidates) > 1 or (unsupported and bool(candidates))
        else AnchorGroundingDisposition.UNSUPPORTED
        if unsupported
        else _candidate_disposition(tuple(candidates))
    )
    reason = {
        AnchorGroundingDisposition.RESOLVED: (
            "Exactly one native source declaration matches the exact locator; "
            "runtime binding identity is not established."
        ),
        AnchorGroundingDisposition.AMBIGUOUS: (
            "Multiple native declarations or incompletely interpreted modules prevent "
            "unique source declaration selection."
        ),
        AnchorGroundingDisposition.UNRESOLVED: (
            "No requested direct declaration was found in the supplied modules."
        ),
        AnchorGroundingDisposition.UNSUPPORTED: (
            "Relevant syntax cannot establish the requested direct declaration."
        ),
    }[disposition]
    return _account(
        request,
        GroundingResolver.PYTHON_SOURCE_DECLARATION_SELECTION,
        tuple(candidates),
        tuple(observations),
        universe,
        disposition,
        reason,
    )


def _ground_method(
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    locator: PythonDirectMethodLocator,
) -> AnchorGrounding:
    parent = locator.containing_class
    if (
        parent.subject.snapshot_id != snapshot.id
        or parent.support.snapshot_id != snapshot.id
    ):
        msg = "Direct method locator contains a foreign or stale class declaration."
        raise ValueError(msg)
    address = parent.support.resource_address
    try:
        analysis = derive_python_class_method_declarations(
            snapshot,
            resource_address=address,
        )
    except PythonClassMethodParseError:
        return _account(
            request,
            GroundingResolver.PYTHON_METHOD_CONTAINMENT,
            (),
            (),
            None,
            AnchorGroundingDisposition.UNSUPPORTED,
            "Observed Python source cannot be analyzed for direct methods.",
        )
    view = build_python_class_method_containment_view(
        snapshot,
        aggregate=PythonClassMethodAnalysisAggregate((analysis,)),
    )
    if parent not in analysis.classes:
        msg = "Direct method locator contains a stale or foreign class declaration."
        raise ValueError(msg)
    methods = tuple(
        item
        for item in view.direct_methods_of(parent)
        if item.declared_name == locator.declared_name
    )
    candidates = tuple(AnchorGroundingCandidate(item, analysis) for item in methods)
    return _account(
        request,
        GroundingResolver.PYTHON_METHOD_CONTAINMENT,
        candidates,
        (analysis,),
        None,
        _candidate_disposition(candidates),
        "Exact direct class-body method syntax matched in the observed class."
        if methods
        else "No exact direct method syntax matched in the observed class.",
    )


def _candidate_disposition(
    candidates: tuple[AnchorGroundingCandidate, ...],
) -> AnchorGroundingDisposition:
    return (
        AnchorGroundingDisposition.UNRESOLVED
        if not candidates
        else AnchorGroundingDisposition.RESOLVED
        if len(candidates) == 1
        else AnchorGroundingDisposition.AMBIGUOUS
    )


def _account(  # noqa: PLR0913, PLR0917
    request: AnchorGroundingRequest,
    resolver: GroundingResolver,
    candidates: tuple[AnchorGroundingCandidate, ...],
    evidence: tuple[NativeGroundingEvidence, ...],
    universe: PythonModuleInterpretationUniverse | None,
    disposition: AnchorGroundingDisposition,
    reason: str,
) -> AnchorGrounding:
    ordered = tuple(sorted(candidates, key=lambda item: _referent_key(item.referent)))
    return AnchorGrounding(
        request,
        disposition,
        resolver,
        ordered,
        evidence,
        universe,
        reason,
    )


def _referent_key(referent: NativeGroundingReferent) -> tuple[str, str]:
    if isinstance(referent, RepositoryResourceOccurrence):
        return (
            "resource",
            referent.address.value + ":" + referent.content_identity.value,
        )
    return (type(referent).__name__, referent.identity)


def _validate_universe(
    snapshot: RepositorySnapshot,
    universe: PythonModuleInterpretationUniverse,
) -> None:
    if universe.repository_id != snapshot.repository_id:
        msg = "Python module universe belongs to another repository."
        raise ValueError(msg)
    define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=universe.interpretations,
    )
    by_root: dict[PythonModuleRoot, list[PythonModuleInterpretation]] = defaultdict(
        list,
    )
    for item in universe.interpretations:
        if item.snapshot_id != snapshot.id:
            msg = "Python module interpretation belongs to another snapshot."
            raise ValueError(msg)
        by_root[item.module_root].append(item)
    for root, supplied in by_root.items():
        expected = interpret_python_module_resources(
            snapshot,
            module_root=root,
            resource_addresses=tuple(item.resource.address for item in supplied),
        )
        if sorted(item.identity for item in supplied) != sorted(
            item.identity for item in expected.interpretations
        ) or any(
            item.resource != snapshot.resource_at(item.resource.address)
            for item in supplied
        ):
            msg = "Python module interpretation differs from native snapshot analysis."
            raise ValueError(msg)
