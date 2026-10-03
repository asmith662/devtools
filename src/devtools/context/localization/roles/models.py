# Copyright (c) 2026
"""Multi-label soft role supports, native references and immutable queries."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.python.mirrored_paths import PythonMirroredPathAnalysis
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretationAnalysis,
    )
    from devtools.context.python.modules.membership import (
        PythonImmediatePackageMembershipAnalysis,
    )
    from devtools.context.python.project_configuration.models import (
        PythonConfigurationDeclarationAnalysis,
        PythonConfigurationResolutionAnalysis,
    )
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import RepositorySnapshotId


class RepositoryRoleKind(Enum):
    """Name local Python/repository evidence families, never exclusive roles."""

    PYTHON_CODE = "python-code"
    TEST = "test"
    DOCUMENTATION = "documentation"
    PROJECT_CONFIGURATION = "project-configuration"
    TEST_CONFIGURATION = "test-configuration"
    BUILD_CONFIGURATION = "build-configuration"
    TOOL_CONFIGURATION = "tool-configuration"
    PACKAGE_SURFACE = "package-surface"
    PACKAGE_MEMBER = "package-member"


class RoleSupportKind(Enum):
    """Describe exact evidence bases without a strength or ordering policy."""

    PYTHON_SUFFIX_CONVENTION = "python-suffix-convention"
    MARKDOWN_SUFFIX_CONVENTION = "markdown-suffix-convention"
    TEST_DIRECTORY_CONVENTION = "test-directory-convention"
    DOCUMENTATION_DIRECTORY_CONVENTION = "documentation-directory-convention"
    README_NAME_CONVENTION = "readme-name-convention"
    PYPROJECT_NAME_CONVENTION = "pyproject-name-convention"
    INITIALIZER_NAME_CONVENTION = "initializer-name-convention"
    MODULE_INTERPRETATION = "module-interpretation"
    PACKAGE_INTERPRETATION = "package-interpretation"
    PACKAGE_MEMBERSHIP = "package-membership"
    MIRRORED_TEST_PATH = "mirrored-test-path"
    PROJECT_DECLARATION = "project-declaration"
    BUILD_DECLARATION = "build-declaration"
    PYTEST_DECLARATION = "pytest-declaration"
    TOOL_TABLE = "tool-table"
    TOOL_DECLARATION = "tool-declaration"
    PYTEST_TESTPATH_TARGET = "pytest-testpath-target"
    PYTEST_BASENAME_GLOB = "pytest-basename-glob"
    README_TARGET = "readme-target"


@dataclass(frozen=True, slots=True)
class RepositoryRoleEvidenceInputs:
    """Retain explicitly supplied native RI scopes, including nonpositive results."""

    modules: tuple[PythonModuleInterpretationAnalysis, ...] = ()
    memberships: tuple[PythonImmediatePackageMembershipAnalysis, ...] = ()
    mirrors: tuple[PythonMirroredPathAnalysis, ...] = ()
    configurations: tuple[PythonConfigurationDeclarationAnalysis, ...] = ()
    configuration_targets: tuple[PythonConfigurationResolutionAnalysis, ...] = ()


@dataclass(frozen=True, slots=True)
class RepositoryRoleSupport:
    """Reference one native observation or an explicitly named address convention."""

    kind: RoleSupportKind
    source_address: RepositoryResourceAddress
    native_identities: tuple[str, ...]
    observation: tuple[str, ...]

    @property
    def identity(self) -> str:
        """Identify support without duplicating a native fact or resource identity."""
        return digest(
            "repository-role-support-v1",
            self.kind.value,
            self.source_address.value,
            self.native_identities,
            self.observation,
        )


@dataclass(frozen=True, slots=True)
class RepositoryRoleLimitation:
    """Explain an unperformed pattern interpretation, never negative role evidence."""

    source_address: RepositoryResourceAddress
    native_identity: str
    reason: str
    observation: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ResourceRoleEvidence:
    """Group positive supports for one role-like interpretation of one resource."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    derivation_identity: str
    resource: RepositoryResourceOccurrence
    role: RepositoryRoleKind
    supports: tuple[RepositoryRoleSupport, ...]

    @property
    def identity(self) -> str:
        """Bind role evidence to snapshot and exact support membership."""
        return digest(
            "resource-role-evidence-v1",
            str(self.repository_id),
            str(self.snapshot_id),
            self.derivation_identity,
            self.resource.address.value,
            self.resource.content_identity.value,
            self.role.value,
            tuple(item.identity for item in self.supports),
        )


@dataclass(frozen=True, slots=True)
class RepositoryRoleEvidenceView:
    """Keep the entire frame and positive role inventory without candidate filtering."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    derivation_identity: str
    resources: tuple[RepositoryResourceOccurrence, ...]
    inputs: RepositoryRoleEvidenceInputs
    evidence: tuple[ResourceRoleEvidence, ...]
    limitations: tuple[RepositoryRoleLimitation, ...]

    SEMANTICS: ClassVar[str] = "positive-python-repository-role-support-v1"

    def for_resource(
        self,
        address: RepositoryResourceAddress,
    ) -> tuple[ResourceRoleEvidence, ...]:
        """Return all role evidence; empty for a known resource is not negative."""
        if not any(item.address == address for item in self.resources):
            msg = "Role-evidence resource is outside the retained frame."
            raise ValueError(msg)
        return tuple(item for item in self.evidence if item.resource.address == address)

    def for_role(self, role: RepositoryRoleKind) -> tuple[ResourceRoleEvidence, ...]:
        """Return positive supports without changing frame eligibility."""
        return tuple(item for item in self.evidence if item.role == role)

    def supports_for(
        self,
        address: RepositoryResourceAddress,
        role: RepositoryRoleKind,
    ) -> tuple[RepositoryRoleSupport, ...]:
        """Explain one role; missing support is not an exclusion or contradiction."""
        return tuple(
            support
            for item in self.for_resource(address)
            if item.role == role
            for support in item.supports
        )


def digest(*values: object) -> str:
    """Hash framed JSON values for this local evidence family, not RI identity."""
    return hashlib.sha256(
        json.dumps(values, ensure_ascii=True, separators=(",", ":")).encode("utf-8"),
    ).hexdigest()


type RoleObservation = tuple[
    RepositoryResourceAddress,
    RepositoryRoleKind,
    RepositoryRoleSupport,
]
