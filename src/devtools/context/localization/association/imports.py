# Copyright (c) 2026
"""Frozen native module-import relations supporting direct dependency candidates."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.python.classes.declarations import (
    PythonMethodDeclarationKnowledge,
)
from devtools.context.python.imports.declarations import (
    derive_python_import_declarations,
)
from devtools.context.python.imports.relations import (
    PythonResolvedModuleImportRelation,
    derive_python_resolved_module_import_relations,
)
from devtools.context.python.imports.resolution import resolve_python_import_declaration
from devtools.context.python.modules.interpretation import (
    PythonModuleInterpretation,
    interpret_python_module_resources,
)
from devtools.context.python.modules.selection import (
    PythonModuleSourceDeclarationSelection,
)

if TYPE_CHECKING:
    from devtools.context.localization.grounding import AnchorGrounding
    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationAnalysis,
    )
    from devtools.context.python.imports.resolution import PythonImportResolution
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True, slots=True)
class PythonImportDependencySourceInput:
    """Retain one interpreted module's exhaustive declarations and resolutions."""

    module: PythonModuleInterpretation
    analysis: PythonImportDeclarationAnalysis
    resolutions: tuple[PythonImportResolution, ...]


@dataclass(frozen=True, slots=True)
class PythonImportDependencyProjectionRequest:
    """Authorize frozen native inputs and a source-analysis replay work bound."""

    module_universe: PythonModuleInterpretationUniverse
    sources: tuple[PythonImportDependencySourceInput, ...]
    work_limit: int

    def __post_init__(self) -> None:
        """Canonicalize exact source inputs without selecting competing modules."""
        if self.work_limit < 0:
            msg = "Import dependency work limit must be nonnegative."
            raise ValueError(msg)
        sources: dict[str, PythonImportDependencySourceInput] = {}
        for source in self.sources:
            key = source.module.identity
            if key in sources and sources[key] != source:
                msg = "Import dependency source identity collides."
                raise ValueError(msg)
            sources[key] = source
        object.__setattr__(
            self,
            "sources",
            tuple(sources[key] for key in sorted(sources)),
        )

    @property
    def identity(self) -> str:
        """Identify the operator, universe, quota and exact supplied native inputs."""
        return json.dumps(
            (
                "direct-python-import-dependency-resource-v1",
                self.module_universe.identity,
                self.work_limit,
                *(
                    (
                        item.module.identity,
                        item.analysis.derivation_identity,
                        *(value.identity for value in item.resolutions),
                    )
                    for item in self.sources
                ),
            ),
            separators=(",", ":"),
        )


def import_dependency_modules(
    grounding: AnchorGrounding,
    request: PythonImportDependencyProjectionRequest,
) -> tuple[PythonModuleInterpretation, ...]:
    """Use native grounding evidence; only methods need an explicit owner lookup."""
    candidate = grounding.candidates[0]
    if isinstance(candidate.referent, PythonModuleInterpretation):
        return (candidate.referent,)
    if isinstance(candidate.evidence, PythonModuleSourceDeclarationSelection):
        return (candidate.evidence.module,)
    if isinstance(candidate.referent, PythonMethodDeclarationKnowledge):
        return tuple(
            item
            for item in request.module_universe.interpretations
            if item.resource.address == candidate.referent.support.resource_address
        )
    return ()


def validate_import_dependency_frame(
    request: PythonImportDependencyProjectionRequest,
    snapshot: RepositorySnapshot,
) -> None:
    """Check frame metadata and exhaustive input coverage before bounded replay."""
    universe = request.module_universe
    if universe.repository_id != snapshot.repository_id:
        msg = "Import dependency universe belongs to another repository."
        raise ValueError(msg)
    if len({item.identity for item in universe.interpretations}) != len(
        universe.interpretations,
    ):
        msg = "Import dependency universe repeats a module interpretation."
        raise ValueError(msg)
    for module in universe.interpretations:
        canonical = interpret_python_module_resources(
            snapshot,
            module_root=module.module_root,
            resource_addresses=(module.resource.address,),
        ).interpretations
        if canonical != (module,):
            msg = "Import dependency module differs from the frozen snapshot."
            raise ValueError(msg)
    for source in request.sources:
        analysis = source.analysis
        if (
            source.module not in universe.interpretations
            or analysis.repository_id != snapshot.repository_id
            or analysis.snapshot_id != snapshot.id
            or analysis.resource != source.module.resource
        ):
            msg = "Import dependency analysis differs from its native frame."
            raise ValueError(msg)
        if (
            tuple(value.declaration for value in source.resolutions)
            != analysis.declarations
        ):
            msg = "Import dependency resolutions must cover every declaration once."
            raise ValueError(msg)
        if any(value.target_universe != universe for value in source.resolutions):
            msg = "Import dependency resolution uses another universe."
            raise ValueError(msg)


def replay_import_dependency_source(
    source: PythonImportDependencySourceInput,
    request: PythonImportDependencyProjectionRequest,
    snapshot: RepositorySnapshot,
) -> tuple[PythonResolvedModuleImportRelation, ...]:
    """Validate native inputs and derive only canonical positive module relations."""
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=source.module.resource.address,
    )
    resolutions = tuple(
        resolve_python_import_declaration(
            analysis,
            declaration,
            target_universe=request.module_universe,
            source_interpretations=(source.module,),
        )
        for declaration in analysis.declarations
    )
    if analysis != source.analysis or resolutions != source.resolutions:
        msg = "Import dependency inputs differ from canonical native replay."
        raise ValueError(msg)
    relations = derive_python_resolved_module_import_relations(
        analysis,
        resolutions=resolutions,
        source_interpretations=(source.module,),
    ).relations
    # Module resolution interprets even a star import's module portion. The
    # adapter deliberately excludes that syntax rather than claiming star closure.
    return tuple(
        item for item in relations if item.resolution.declaration.imported_name != "*"
    )


@dataclass(frozen=True, slots=True)
class PythonImportDependencyResourceSupport:
    """Retain every exact direct module-import relation for one target resource."""

    grounding: AnchorGrounding
    request: PythonImportDependencyProjectionRequest
    source: PythonImportDependencySourceInput
    relations: tuple[PythonResolvedModuleImportRelation, ...]

    def __post_init__(self) -> None:
        """Canonicalize distinct facts and reject empty or colliding provenance."""
        relations = set(self.relations)
        if not relations or len({item.identity for item in relations}) != len(
            relations,
        ):
            msg = "Import dependency support needs unambiguous native relations."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "relations",
            tuple(sorted(relations, key=lambda item: item.identity)),
        )

    @property
    def identity(self) -> str:
        """Encode exact operator/frame/source and positive native relation keys."""
        return json.dumps(
            (
                self.request.identity,
                self.source.module.identity,
                *(item.identity for item in self.relations),
            ),
            separators=(",", ":"),
        )


def validate_import_dependency_support(
    support: PythonImportDependencyResourceSupport,
    snapshot: RepositorySnapshot,
    target: RepositoryResourceOccurrence,
) -> None:
    """Reject forged resolutions, source association and dependency targets."""
    validate_import_dependency_frame(support.request, snapshot)
    if (
        support.source not in support.request.sources
        or support.request.work_limit < 1
        or import_dependency_modules(support.grounding, support.request)
        != (support.source.module,)
    ):
        msg = "Import dependency support is outside its authorized source frame."
        raise ValueError(msg)
    relations = replay_import_dependency_source(
        support.source,
        support.request,
        snapshot,
    )
    if any(
        item not in relations or item.target.resource != target
        for item in support.relations
    ):
        msg = "Import dependency support differs from native relation or target."
        raise ValueError(msg)
