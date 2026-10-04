# Copyright (c) 2026
"""Frozen Python Reference inputs and exact referencing-resource support."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
)
from devtools.context.python.references import derive_python_declaration_references

if TYPE_CHECKING:
    from devtools.context.localization.grounding import AnchorGrounding
    from devtools.context.python.modules import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.python.references import (
        PythonDeclarationReferenceAnalysis,
        PythonDeclarationReferenceKnowledge,
        PythonReferenceTarget,
    )
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True, slots=True)
class PythonReferenceSourceInput:
    """Retain one native analysis and its explicit source interpretations."""

    analysis: PythonDeclarationReferenceAnalysis
    source_interpretations: tuple[PythonModuleInterpretation, ...] = ()


@dataclass(frozen=True, slots=True)
class PythonReferenceProjectionRequest:
    """Supply a finite native frame and maximum source analyses to inspect."""

    module_universe: PythonModuleInterpretationUniverse
    sources: tuple[PythonReferenceSourceInput, ...]
    work_limit: int

    def __post_init__(self) -> None:
        """Require explicit nonnegative work and unambiguous native analysis keys."""
        if self.work_limit < 0:
            msg = "Reference projection work limit must be nonnegative."
            raise ValueError(msg)
        sources: dict[str, PythonReferenceSourceInput] = {}
        for source in self.sources:
            key = source.analysis.derivation.identity
            if key in sources and sources[key] != source:
                msg = "Reference source analysis identity collides."
                raise ValueError(msg)
            sources[key] = source
        object.__setattr__(
            self,
            "sources",
            tuple(sources[key] for key in sorted(sources)),
        )

    @property
    def identity(self) -> str:
        """Encode frozen projection inputs, not rank or execution order."""
        return json.dumps(
            (
                "python-referencing-resource-v1",
                self.module_universe.identity,
                self.work_limit,
                *(item.analysis.derivation.identity for item in self.sources),
            ),
            separators=(",", ":"),
        )


def reference_seed(grounding: AnchorGrounding) -> PythonReferenceTarget | None:
    """Accept only the exact native declaration kinds Reference RI can target."""
    seed = grounding.candidates[0].referent
    return (
        seed
        if isinstance(
            seed,
            (
                PythonFunctionDeclarationKnowledge,
                PythonClassDeclarationKnowledge,
                PythonMethodDeclarationKnowledge,
            ),
        )
        else None
    )


def validate_reference_frame(
    request: PythonReferenceProjectionRequest,
    snapshot: RepositorySnapshot,
) -> None:
    """Reject foreign/stale metadata before authorizing any native replay work."""
    universe = request.module_universe
    if universe.repository_id != snapshot.repository_id:
        msg = "Reference universe belongs to a foreign repository."
        raise ValueError(msg)
    for module in universe.interpretations:
        if (
            module.repository_id != snapshot.repository_id
            or module.snapshot_id != snapshot.id
            or module.resource != snapshot.resource_at(module.resource.address)
        ):
            msg = "Reference universe differs from the frozen snapshot."
            raise ValueError(msg)
    for source in request.sources:
        derivation = source.analysis.derivation
        dependency = derivation.dependency
        if (
            dependency.repository_id != snapshot.repository_id
            or dependency.snapshot_id != snapshot.id
            or dependency.resource != snapshot.resource_at(dependency.resource.address)
            or derivation.module_universe_identity != universe.identity
        ):
            msg = "Reference analysis differs from the frozen frame."
            raise ValueError(msg)
        source_ids = tuple(
            sorted(item.identity for item in source.source_interpretations),
        )
        if derivation.source_interpretation_identities != source_ids or any(
            item.repository_id != snapshot.repository_id
            or item.snapshot_id != snapshot.id
            or item.resource != dependency.resource
            for item in source.source_interpretations
        ):
            msg = "Reference source interpretations differ from native inputs."
            raise ValueError(msg)


def replay_reference_source(
    source: PythonReferenceSourceInput,
    request: PythonReferenceProjectionRequest,
    snapshot: RepositorySnapshot,
) -> None:
    """Verify supplied native truth against retained content; never replace it."""
    native = derive_python_declaration_references(
        snapshot,
        resource_address=source.analysis.derivation.dependency.resource.address,
        module_universe=request.module_universe,
        source_interpretations=source.source_interpretations,
    )
    if native != source.analysis:
        msg = "Reference analysis differs from canonical native replay."
        raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class PythonReferenceResourceSupport:
    """Retain exact native Reference facts supporting one referencing resource."""

    grounding: AnchorGrounding
    request: PythonReferenceProjectionRequest
    source: PythonReferenceSourceInput
    references: tuple[PythonDeclarationReferenceKnowledge, ...]

    def __post_init__(self) -> None:
        """Retain distinct native facts once, in canonical identity order."""
        references = set(self.references)
        if not references or len({item.identity for item in references}) != len(
            references,
        ):
            msg = "Reference support needs facts with unambiguous native identities."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "references",
            tuple(
                sorted(
                    references,
                    key=lambda item: item.identity,
                ),
            ),
        )

    @property
    def identity(self) -> str:
        """Retain operator/frame/analysis and exact native fact identity."""
        return json.dumps(
            (
                self.request.identity,
                self.source.analysis.derivation.identity,
                *(item.identity for item in self.references),
            ),
            separators=(",", ":"),
        )


def validate_reference_support(
    support: PythonReferenceResourceSupport,
    snapshot: RepositorySnapshot,
    target: RepositoryResourceOccurrence,
) -> None:
    """Verify positive fact membership, exact seed and referencing resource."""
    validate_reference_frame(support.request, snapshot)
    if (
        support.source not in support.request.sources
        or len(support.request.sources) > support.request.work_limit
    ):
        msg = "Reference support is outside its complete authorized native frame."
        raise ValueError(msg)
    replay_reference_source(support.source, support.request, snapshot)
    seed = reference_seed(support.grounding)
    if seed is None:
        msg = "Reference support requires a native declaration grounding."
        raise ValueError(msg)
    if support.source.analysis.derivation.dependency.resource != target or any(
        fact not in support.source.analysis.references
        or fact.target_subject != seed.subject
        or fact.target_declaration != seed
        or fact.occurrence.snapshot_id != snapshot.id
        or fact.occurrence.resource_address != target.address
        for fact in support.references
    ):
        msg = "Reference support differs from native fact, seed or source target."
        raise ValueError(msg)
