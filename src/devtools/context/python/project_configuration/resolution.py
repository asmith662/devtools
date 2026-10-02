# Copyright (c) 2026
"""Resolve literal selectors only against retained resources and module knowledge."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.python.modules.lookup import lookup_python_modules
from devtools.context.python.project_configuration.declarations import (
    analyze_python_project_configuration,
)
from devtools.context.python.project_configuration.models import (
    PythonConfigurationAlternative,
    PythonConfigurationAssessment,
    PythonConfigurationFrame,
    PythonConfigurationResolutionAnalysis,
    PythonConfigurationSelector,
    PythonConfigurationStatus,
    PythonConfigurationTargetFact,
    digest,
)
from devtools.context.repository.resource import RepositoryResourceAddress

if TYPE_CHECKING:
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretationUniverse,
        PythonModuleRoot,
    )
    from devtools.context.python.project_configuration.models import (
        PythonConfigurationDeclaration,
        PythonConfigurationDeclarationAnalysis,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot

_S = PythonConfigurationStatus
_K = PythonConfigurationSelector
_EMPTY_FRAME = PythonConfigurationFrame()
_FIRST_PRINTABLE_ASCII = 32
_ASCII_DELETE = 127


def resolve_python_project_configuration(
    snapshot: RepositorySnapshot,
    declarations: PythonConfigurationDeclarationAnalysis,
    *,
    universe: PythonModuleInterpretationUniverse,
    frame: PythonConfigurationFrame = _EMPTY_FRAME,
) -> PythonConfigurationResolutionAnalysis:
    """Derive qualified observed target facts without acquisition or tool execution.

    Many members of one directory selection are not ambiguous. Coverage path
    and module alternatives and distinct module roots are competing readings.
    Only unambiguous supported readings publish facts. Missing means only no
    match in the retained frame, never filesystem absence or an external target.
    """
    _validate(snapshot, declarations, universe, frame)
    resources = tuple(sorted(snapshot.resources, key=lambda item: item.address.value))
    derivation = digest(
        "python-project-config-observed-resolution-v1",
        declarations.derivation_identity,
        universe.identity,
        frame.working_directory.value if frame.working_directory else "",
        frame.pytest_root.value if frame.pytest_root else "",
        *(
            value
            for item in resources
            for value in (
                item.address.value,
                item.content_identity.value,
                item.content,
            )
        ),
    )
    assessments: list[PythonConfigurationAssessment] = []
    facts: list[PythonConfigurationTargetFact] = []
    for declaration in declarations.declarations:
        alternatives = _alternatives(
            snapshot,
            declarations,
            declaration,
            universe,
            frame,
        )
        status = _status(declaration, alternatives)
        assessments.append(
            PythonConfigurationAssessment(
                declaration,
                status,
                alternatives,
                declaration.unsupported_reason,
            ),
        )
        if status != _S.RESOLVED:
            continue
        alternative = next(item for item in alternatives if item.status == _S.RESOLVED)
        facts.extend(
            PythonConfigurationTargetFact(
                derivation,
                declaration,
                declarations.resource,
                alternative.route,
                alternative.requested or "",
                target,
            )
            for target in alternative.resources
        )
        facts.extend(
            PythonConfigurationTargetFact(
                derivation,
                declaration,
                declarations.resource,
                alternative.route,
                alternative.requested or "",
                module.resource,
                module,
            )
            for module in alternative.modules
        )
    return PythonConfigurationResolutionAnalysis(
        declarations,
        frame,
        universe,
        resources,
        derivation,
        tuple(assessments),
        tuple(facts),
    )


def _validate(
    snapshot: RepositorySnapshot,
    declarations: PythonConfigurationDeclarationAnalysis,
    universe: PythonModuleInterpretationUniverse,
    frame: PythonConfigurationFrame,
) -> None:
    if (
        snapshot.repository_id != declarations.repository_id
        or snapshot.id != declarations.snapshot_id
        or snapshot.resource_at(declarations.resource.address) != declarations.resource
        or analyze_python_project_configuration(
            snapshot,
            address=declarations.resource.address,
        )
        != declarations
    ):
        msg = "Configuration declarations do not match exact retained snapshot content."
        raise ValueError(msg)
    if universe.repository_id != snapshot.repository_id:
        msg = "Configuration universe does not match repository."
        raise ValueError(msg)
    for module in universe.interpretations:
        if (
            module.repository_id != snapshot.repository_id
            or module.snapshot_id != snapshot.id
            or snapshot.resource_at(module.resource.address) != module.resource
        ):
            msg = "Configuration module interpretation has stale dependencies."
            raise ValueError(msg)
    for root in (frame.working_directory, frame.pytest_root):
        if root is not None and root.value != ".":
            RepositoryResourceAddress(root.value)


def _status(
    declaration: PythonConfigurationDeclaration,
    alternatives: tuple[PythonConfigurationAlternative, ...],
) -> PythonConfigurationStatus:
    supported = tuple(item for item in alternatives if item.status == _S.RESOLVED)
    if declaration.unsupported_reason:
        return _S.UNSUPPORTED
    if any(item.status == _S.AMBIGUOUS for item in alternatives) or len(supported) > 1:
        return _S.AMBIGUOUS
    if any(item.status == _S.UNSUPPORTED for item in alternatives):
        return _S.UNSUPPORTED
    return _S.RESOLVED if supported else _S.MISSING_IN_FRAME


def _alternatives(
    snapshot: RepositorySnapshot,
    analysis: PythonConfigurationDeclarationAnalysis,
    declaration: PythonConfigurationDeclaration,
    universe: PythonModuleInterpretationUniverse,
    frame: PythonConfigurationFrame,
) -> tuple[PythonConfigurationAlternative, ...]:
    if declaration.unsupported_reason:
        return ()
    value = declaration.value
    assert value is not None  # noqa: S101  # validated declaration analysis
    if any(character in value for character in "*?[]${}~") or any(
        ord(character) < _FIRST_PRINTABLE_ASCII or ord(character) == _ASCII_DELETE
        for character in value
    ):
        return (
            PythonConfigurationAlternative(
                "literal",
                value,
                _S.UNSUPPORTED,
                reason="glob-env-or-dynamic-value",
            ),
        )
    try:
        if value != ".":
            RepositoryResourceAddress(value)
    except ValueError:
        return (
            PythonConfigurationAlternative(
                "literal",
                value,
                _S.UNSUPPORTED,
                reason="noncanonical-relative-path",
            ),
        )
    selector = declaration.selector
    if selector in {_K.README, _K.HATCH_PACKAGES}:
        parent = analysis.resource.address.parts[:-1]
        path = _path(
            snapshot,
            value,
            parent,
            "configuration-relative",
            selector == _K.README,
        )
    elif selector == _K.PYTEST_TESTPATHS:
        path = _framed_path(snapshot, value, frame.pytest_root, "pytest-root-relative")
    else:
        path = _framed_path(
            snapshot,
            value,
            frame.working_directory,
            "command-cwd-relative",
        )
    if selector != _K.COVERAGE_SOURCE or not all(
        part.isidentifier() for part in value.split(".")
    ):
        return (path,)
    matches = tuple(
        sorted(lookup_python_modules(universe, value), key=lambda item: item.identity),
    )
    module = PythonConfigurationAlternative(
        "coverage-exact-module",
        value,
        _S.MISSING_IN_FRAME
        if not matches
        else _S.RESOLVED
        if len(matches) == 1
        else _S.AMBIGUOUS,
        modules=matches,
    )
    return path, module


def _framed_path(
    snapshot: RepositorySnapshot,
    value: str,
    root: PythonModuleRoot | None,
    route: str,
) -> PythonConfigurationAlternative:
    if root is None:
        return PythonConfigurationAlternative(
            route,
            None,
            _S.UNSUPPORTED,
            reason="explicit-tool-frame-required",
        )
    return _path(snapshot, value, root.parts, route, exact_only=False)


def _path(
    snapshot: RepositorySnapshot,
    value: str,
    parent: tuple[str, ...],
    route: str,
    exact_only: bool,  # noqa: FBT001
) -> PythonConfigurationAlternative:
    parts = (*parent, *(() if value == "." else RepositoryResourceAddress(value).parts))
    requested = "/".join(parts) or "."
    exact = tuple(item for item in snapshot.resources if item.address.parts == parts)
    members = (
        ()
        if exact_only
        else tuple(
            sorted(
                (
                    item
                    for item in snapshot.resources
                    if item.address.parts[: len(parts)] == parts
                    and len(item.address.parts) > len(parts)
                ),
                key=lambda item: item.address.value,
            ),
        )
    )
    if exact and members:
        return PythonConfigurationAlternative(
            route,
            requested,
            _S.AMBIGUOUS,
            exact + members,
            reason="competing-exact-resource-and-directory-prefix",
        )
    return PythonConfigurationAlternative(
        route + ("-exact-resource" if exact_only or exact else "-directory-prefix"),
        requested,
        _S.RESOLVED if exact or members else _S.MISSING_IN_FRAME,
        exact or members,
    )
