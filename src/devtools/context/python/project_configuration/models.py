# Copyright (c) 2026
"""Python project configuration syntax and qualified observed relationships."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
        PythonModuleRoot,
    )
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshotId


class PythonConfigurationSelector(Enum):
    """Name the six supported Python-project selectors."""

    README = "project.readme"
    HATCH_PACKAGES = "tool.hatch.build.targets.wheel.packages"
    PYTEST_TESTPATHS = "tool.pytest.ini_options.testpaths"
    COVERAGE_SOURCE = "tool.coverage.run.source"
    MYPY_FILES = "tool.mypy.files"
    MYPY_PATH = "tool.mypy.mypy_path"


class PythonConfigurationStatus(Enum):
    """Qualify resolution within retained resources and explicit assumptions."""

    RESOLVED = "resolved"
    MISSING_IN_FRAME = "missing-in-frame"
    AMBIGUOUS = "ambiguous"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class PythonConfigurationDeclaration:
    """Retain a semantic TOML key/item anchor, never a fabricated source span."""

    derivation_identity: str
    key: tuple[str, ...]
    item_ordinal: int | None
    selector: PythonConfigurationSelector | None
    value: str | None
    unsupported_reason: str | None

    @property
    def identity(self) -> str:
        """Version and distinguish key and duplicate array occurrences."""
        return digest(
            "python-project-config-occurrence-v1",
            self.derivation_identity,
            *self.key,
            str(self.item_ordinal),
            self.selector.value if self.selector else "",
            self.value or "",
            self.unsupported_reason or "",
        )


@dataclass(frozen=True, slots=True)
class PythonConfigurationDeclarationAnalysis:
    """Account for supported keys and explicitly assessed unsupported syntax."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    resource: RepositoryResourceOccurrence
    derivation_identity: str
    declarations: tuple[PythonConfigurationDeclaration, ...]
    absent_selectors: tuple[PythonConfigurationSelector, ...]
    parse_error: str | None

    SCOPE: ClassVar[str] = "six-selector-keys-and-project-entrypoint-presence"


@dataclass(frozen=True, slots=True)
class PythonConfigurationFrame:
    """Declare repository-relative tool frames without ambient cwd inference."""

    working_directory: PythonModuleRoot | None = None
    pytest_root: PythonModuleRoot | None = None


@dataclass(frozen=True, slots=True)
class PythonConfigurationAlternative:
    """Retain one selector interpretation and all its observed targets."""

    route: str
    requested: str | None
    status: PythonConfigurationStatus
    resources: tuple[RepositoryResourceOccurrence, ...] = ()
    modules: tuple[PythonModuleInterpretation, ...] = ()
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class PythonConfigurationAssessment:
    """Separate a declaration from its competing interpretations."""

    declaration: PythonConfigurationDeclaration
    status: PythonConfigurationStatus
    alternatives: tuple[PythonConfigurationAlternative, ...]
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class PythonConfigurationTargetFact:
    """Assert a qualified exact-resource, prefix-member, or module relationship."""

    derivation_identity: str
    declaration: PythonConfigurationDeclaration
    configuration: RepositoryResourceOccurrence
    route: str
    requested: str
    target: RepositoryResourceOccurrence
    module: PythonModuleInterpretation | None = None

    @property
    def identity(self) -> str:
        """Version relationship identity including source and target dependencies."""
        return digest(
            "python-project-config-target-fact-v1",
            self.derivation_identity,
            self.declaration.identity,
            self.route,
            self.requested,
            self.target.address.value,
            self.target.content_identity.value,
            self.module.identity if self.module else "",
        )


@dataclass(frozen=True, slots=True)
class PythonConfigurationResolutionAnalysis:
    """Retain every assessment, native fact and direct resolution dependency."""

    declarations: PythonConfigurationDeclarationAnalysis
    frame: PythonConfigurationFrame
    universe: PythonModuleInterpretationUniverse
    resource_dependencies: tuple[RepositoryResourceOccurrence, ...]
    derivation_identity: str
    assessments: tuple[PythonConfigurationAssessment, ...]
    facts: tuple[PythonConfigurationTargetFact, ...]

    SCOPE: ClassVar[str] = "all-declarations-in-explicit-observed-snapshot-and-universe"


def digest(*values: str) -> str:
    """Hash length-framed semantic values for this bounded family."""
    result = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        result.update(len(encoded).to_bytes(8, "big"))
        result.update(encoded)
    return result.hexdigest()
