# Copyright (c) 2026
"""Declaration-grounded repository module-import relations."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.imports.resolution import PythonImportResolutionOutcome

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationAnalysis,
    )
    from devtools.context.python.imports.resolution import PythonImportResolution
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
    )

_SEMANTICS = "declaration-grounded-repository-module-import-relation-v1"


class PythonImportRelationSourceStatus(Enum):
    """Qualify availability of the importing module endpoint."""

    AVAILABLE = "available"
    MISSING = "missing"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True, slots=True)
class PythonResolvedModuleImportRelation:
    """One source declaration's uniquely resolved module-import relation."""

    source: PythonModuleInterpretation
    resolution: PythonImportResolution
    target: PythonModuleInterpretation

    SEMANTICS: ClassVar[str] = _SEMANTICS

    @property
    def declaration(self) -> object:
        """Expose the exact source declaration retained by resolution evidence."""
        return self.resolution.declaration

    @property
    def identity(self) -> str:
        """Identify one declaration-grounded relation without snapshot shortcuts."""
        return _digest(
            self.SEMANTICS,
            self.source.identity,
            self.resolution.identity,
            self.target.identity,
        )


@dataclass(frozen=True, slots=True)
class PythonResolvedModuleImportRelationAnalysis:
    """Retain relations derivable from supplied resolution evidence."""

    source_status: PythonImportRelationSourceStatus
    source: PythonModuleInterpretation | None
    relations: tuple[PythonResolvedModuleImportRelation, ...]


def derive_python_resolved_module_import_relations(
    analysis: PythonImportDeclarationAnalysis,
    *,
    resolutions: Sequence[PythonImportResolution],
    source_interpretations: Sequence[PythonModuleInterpretation],
) -> PythonResolvedModuleImportRelationAnalysis:
    """Derive relations only from resolved declarations and one source module."""
    source_candidates = tuple(source_interpretations)
    if any(
        item.repository_id != analysis.repository_id
        or item.resource.address != analysis.resource.address
        or item.resource.content_identity != analysis.resource.content_identity
        for item in source_candidates
    ):
        msg = "Relation source interpretation does not match declaration source."
        raise ValueError(msg)
    if not source_candidates:
        return PythonResolvedModuleImportRelationAnalysis(
            source_status=PythonImportRelationSourceStatus.MISSING,
            source=None,
            relations=(),
        )
    if len(source_candidates) != 1:
        return PythonResolvedModuleImportRelationAnalysis(
            source_status=PythonImportRelationSourceStatus.AMBIGUOUS,
            source=None,
            relations=(),
        )
    source = source_candidates[0]
    values = tuple(resolutions)
    if any(
        resolution.declaration not in analysis.declarations
        or resolution.target_universe.repository_id != analysis.repository_id
        for resolution in values
    ):
        msg = "Relation resolution does not belong to the supplied analysis."
        raise ValueError(msg)
    relations = tuple(
        PythonResolvedModuleImportRelation(
            source=source,
            resolution=resolution,
            target=resolution.matches[0],
        )
        for resolution in values
        if resolution.outcome is PythonImportResolutionOutcome.RESOLVED
    )
    return PythonResolvedModuleImportRelationAnalysis(
        source_status=PythonImportRelationSourceStatus.AVAILABLE,
        source=source,
        relations=relations,
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
