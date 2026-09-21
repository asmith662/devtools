# Copyright (c) 2026
"""Qualified resolution of import syntax within an explicit module universe."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, cast

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationAnalysis,
        PythonImportDeclarationKnowledge,
    )
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )

_RESOLUTION_SEMANTICS = "qualified-repository-python-import-resolution-v1"


class PythonImportResolutionOutcome(Enum):
    """Classify one qualified repository-scoped import resolution."""

    RESOLVED = "resolved"
    UNRESOLVED_IN_UNIVERSE = "unresolved-in-universe"
    AMBIGUOUS = "ambiguous"
    UNSUPPORTED = "unsupported"


class PythonImportResolutionUnsupportedReason(Enum):
    """Qualify a declaration that the bounded resolver cannot evaluate."""

    RELATIVE_SOURCE_MISSING = "relative-source-missing"
    RELATIVE_SOURCE_AMBIGUOUS = "relative-source-ambiguous"
    RELATIVE_BEYOND_PACKAGE = "relative-beyond-package"


@dataclass(frozen=True, slots=True)
class PythonImportResolution:
    """Retain one declaration's result within one explicit module universe."""

    declaration: PythonImportDeclarationKnowledge
    target_universe: PythonModuleInterpretationUniverse
    outcome: PythonImportResolutionOutcome
    requested_module: str | None
    source_interpretation: PythonModuleInterpretation | None
    matches: tuple[PythonModuleInterpretation, ...]
    unsupported_reason: PythonImportResolutionUnsupportedReason | None

    SEMANTICS: ClassVar[str] = _RESOLUTION_SEMANTICS

    @property
    def identity(self) -> str:
        """Identify the resolution from its semantic inputs and outcome."""
        return _digest(
            self.SEMANTICS,
            self.declaration.derivation_identity,
            str(self.declaration.declaration_ordinal),
            self.target_universe.identity,
            self.outcome.value,
            self.requested_module or "",
            self.source_interpretation.identity
            if self.source_interpretation is not None
            else "",
            *(item.identity for item in self.matches),
            self.unsupported_reason.value if self.unsupported_reason else "",
        )


def resolve_python_import_declaration(
    analysis: PythonImportDeclarationAnalysis,
    declaration: PythonImportDeclarationKnowledge,
    *,
    target_universe: PythonModuleInterpretationUniverse,
    source_interpretations: Sequence[PythonModuleInterpretation] = (),
) -> PythonImportResolution:
    """Resolve one declaration's eligible module portion in a supplied universe.

    This is repository-scoped syntax interpretation, not runtime importability,
    target discovery, member-to-submodule resolution, or a dependency assertion.
    """
    if declaration not in analysis.declarations:
        msg = "Import declaration does not belong to the supplied analysis."
        raise ValueError(msg)
    if target_universe.repository_id != analysis.repository_id:
        msg = "Import resolution universe does not match declaration repository."
        raise ValueError(msg)

    source = _source_interpretation(
        analysis=analysis,
        declaration=declaration,
        source_interpretations=source_interpretations,
    )
    if isinstance(source, PythonImportResolutionUnsupportedReason):
        return PythonImportResolution(
            declaration=declaration,
            target_universe=target_universe,
            outcome=PythonImportResolutionOutcome.UNSUPPORTED,
            requested_module=None,
            source_interpretation=None,
            matches=(),
            unsupported_reason=source,
        )

    requested_module = _requested_module(declaration=declaration, source=source)
    if isinstance(requested_module, PythonImportResolutionUnsupportedReason):
        return PythonImportResolution(
            declaration=declaration,
            target_universe=target_universe,
            outcome=PythonImportResolutionOutcome.UNSUPPORTED,
            requested_module=None,
            source_interpretation=source,
            matches=(),
            unsupported_reason=requested_module,
        )
    matches = tuple(
        item
        for item in target_universe.interpretations
        if item.dotted_name == requested_module
    )
    outcome = (
        PythonImportResolutionOutcome.UNRESOLVED_IN_UNIVERSE
        if not matches
        else PythonImportResolutionOutcome.RESOLVED
        if len(matches) == 1
        else PythonImportResolutionOutcome.AMBIGUOUS
    )
    return PythonImportResolution(
        declaration=declaration,
        target_universe=target_universe,
        outcome=outcome,
        requested_module=requested_module,
        source_interpretation=source,
        matches=matches,
        unsupported_reason=None,
    )


def _source_interpretation(
    *,
    analysis: PythonImportDeclarationAnalysis,
    declaration: PythonImportDeclarationKnowledge,
    source_interpretations: Sequence[PythonModuleInterpretation],
) -> PythonModuleInterpretation | PythonImportResolutionUnsupportedReason | None:
    if declaration.level == 0:
        return None
    candidates = tuple(source_interpretations)
    if any(
        item.repository_id != analysis.repository_id
        or item.resource.address != analysis.resource.address
        or item.resource.content_identity != analysis.resource.content_identity
        for item in candidates
    ):
        msg = "Relative import source interpretation does not match declaration source."
        raise ValueError(msg)
    if not candidates:
        return PythonImportResolutionUnsupportedReason.RELATIVE_SOURCE_MISSING
    if len(candidates) != 1:
        return PythonImportResolutionUnsupportedReason.RELATIVE_SOURCE_AMBIGUOUS
    return candidates[0]


def _requested_module(
    *,
    declaration: PythonImportDeclarationKnowledge,
    source: PythonModuleInterpretation | None,
) -> str | PythonImportResolutionUnsupportedReason:
    if declaration.level == 0:
        if declaration.module is None:
            msg = "Absolute import declaration lacks a module portion."
            raise ValueError(msg)
        return declaration.module
    relative_source = cast("PythonModuleInterpretation", source)
    package_parts = relative_source.dotted_name.split(".")
    if relative_source.kind.value == "ordinary-module":
        package_parts = package_parts[:-1]
    if declaration.level > len(package_parts):
        return PythonImportResolutionUnsupportedReason.RELATIVE_BEYOND_PACKAGE
    base_parts = package_parts[: len(package_parts) - declaration.level + 1]
    return ".".join((*base_parts, *(declaration.module or "").split("."))).rstrip(".")


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
