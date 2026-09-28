# Copyright (c) 2026
"""Qualified immediate membership of observed Python modules in packages.

This module derives one repository relationship from existing explicit-root
module interpretations. It does not inspect filesystem hierarchy, import
modules, infer module roots, or create retrieval candidates.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.modules.interpretation import (
    PythonModuleInterpretation,
    PythonModuleInterpretationAnalysis,
    PythonModuleInterpretationExclusion,
    PythonModuleKind,
    PythonModuleRoot,
)

if TYPE_CHECKING:
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

_SEMANTICS = "observed-immediate-python-package-membership-v1"


class PythonImmediatePackageMembershipStatus(Enum):
    """Classify one selected module interpretation's immediate-parent result."""

    ESTABLISHED = "established"
    NO_PARENT_COMPONENT = "no-parent-component"
    MISSING_OBSERVED_PACKAGE = "missing-observed-package"
    PARENT_NOT_PACKAGE = "parent-not-package"
    AMBIGUOUS_PACKAGE = "ambiguous-package"


@dataclass(frozen=True, slots=True)
class PythonImmediatePackageMembershipDerivation:
    """Bind versioned semantics to one snapshot and selected root analysis."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    module_root: PythonModuleRoot
    interpretation_identities: tuple[str, ...]
    exclusion_dependencies: tuple[tuple[str, str, str], ...]

    DEFINITION_SEMANTICS: ClassVar[str] = _SEMANTICS

    @property
    def identity(self) -> str:
        """Identify the exact bounded semantic input independent of input order."""
        return _digest(
            self.DEFINITION_SEMANTICS,
            str(self.repository_id),
            str(self.snapshot_id),
            self.module_root.value,
            *self.interpretation_identities,
            *(
                component
                for dependency in self.exclusion_dependencies
                for component in dependency
            ),
        )


@dataclass(frozen=True, slots=True)
class PythonImmediatePackageMembership:
    """Assert one observed child module's unique immediate package module.

    The existing interpretations retain their exact observed resources,
    content identities, snapshot, explicit root, dotted names, and kinds.
    """

    derivation_identity: str
    child: PythonModuleInterpretation
    package: PythonModuleInterpretation

    PROPOSITION: ClassVar[str] = (
        "observed-python-module-immediate-member-of-unique-observed-package"
    )

    @property
    def identity(self) -> str:
        """Identify this qualified relationship, not a retrieval projection."""
        return _digest(
            self.PROPOSITION,
            self.derivation_identity,
            self.child.identity,
            self.package.identity,
        )


@dataclass(frozen=True, slots=True)
class PythonImmediatePackageMembershipAssessment:
    """Retain a result for each interpreted child in the selected set."""

    child: PythonModuleInterpretation
    status: PythonImmediatePackageMembershipStatus
    requested_parent_name: str | None
    observed_name_matches: tuple[PythonModuleInterpretation, ...]
    membership: PythonImmediatePackageMembership | None


@dataclass(frozen=True, slots=True)
class PythonImmediatePackageMembershipCoverage:
    """Account for the exact selected interpretation set, not a whole repo."""

    derivation_identity: str
    interpreted_count: int
    excluded_count: int
    assessment_count: int
    established_count: int

    SCOPE: ClassVar[str] = "one-explicit-root-selected-observed-resource-set"
    IS_EXHAUSTIVE_FOR_SELECTION: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class PythonImmediatePackageMembershipAnalysis:
    """Group one derivation's relationships, assessments, and exclusions."""

    derivation: PythonImmediatePackageMembershipDerivation
    memberships: tuple[PythonImmediatePackageMembership, ...]
    assessments: tuple[PythonImmediatePackageMembershipAssessment, ...]
    exclusions: tuple[PythonModuleInterpretationExclusion, ...]
    coverage: PythonImmediatePackageMembershipCoverage

    def immediate_package_of(
        self,
        child: PythonModuleInterpretation,
    ) -> PythonImmediatePackageMembership | None:
        """Return this analysis's one qualified parent fact, if established."""
        return next(
            (item for item in self.memberships if item.child == child),
            None,
        )

    def immediate_members_of(
        self,
        package: PythonModuleInterpretation,
    ) -> tuple[PythonImmediatePackageMembership, ...]:
        """Return this analysis's direct children of one observed package."""
        return tuple(item for item in self.memberships if item.package == package)


def derive_python_immediate_package_memberships(
    snapshot: RepositorySnapshot,
    *,
    interpretation_analysis: PythonModuleInterpretationAnalysis,
) -> PythonImmediatePackageMembershipAnalysis:
    """Derive one-edge membership within one explicit-root observed selection.

    Missing means missing from the supplied interpreted selection; it is not
    evidence that no package exists elsewhere. Ambiguity retains all observed
    name matches and establishes no membership.
    """
    _validate_inputs(snapshot, interpretation_analysis)
    interpretations = interpretation_analysis.interpretations
    derivation = PythonImmediatePackageMembershipDerivation(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        module_root=interpretation_analysis.module_root,
        interpretation_identities=tuple(
            sorted(item.identity for item in interpretations),
        ),
        exclusion_dependencies=tuple(
            sorted(
                (
                    str(item.resource.address),
                    str(item.resource.content_identity),
                    item.reason.value,
                )
                for item in interpretation_analysis.exclusions
            ),
        ),
    )
    by_name: dict[str, list[PythonModuleInterpretation]] = {}
    for item in interpretations:
        by_name.setdefault(item.dotted_name, []).append(item)

    memberships: list[PythonImmediatePackageMembership] = []
    assessments: list[PythonImmediatePackageMembershipAssessment] = []
    for child in interpretations:
        if "." not in child.dotted_name:
            parent_name = None
            matches: tuple[PythonModuleInterpretation, ...] = ()
            packages: tuple[PythonModuleInterpretation, ...] = ()
            status = PythonImmediatePackageMembershipStatus.NO_PARENT_COMPONENT
        else:
            parent_name = child.dotted_name.rsplit(".", 1)[0]
            matches = tuple(by_name.get(parent_name, ()))
            packages = tuple(
                item for item in matches if item.kind is PythonModuleKind.PACKAGE
            )
            if not matches:
                status = PythonImmediatePackageMembershipStatus.MISSING_OBSERVED_PACKAGE
            elif not packages:
                status = PythonImmediatePackageMembershipStatus.PARENT_NOT_PACKAGE
            elif len(packages) > 1:
                status = PythonImmediatePackageMembershipStatus.AMBIGUOUS_PACKAGE
            else:
                status = PythonImmediatePackageMembershipStatus.ESTABLISHED
        membership = None
        if status is PythonImmediatePackageMembershipStatus.ESTABLISHED:
            package = packages[0]
            if package.resource.address == child.resource.address:
                msg = "A Python package cannot immediately contain itself."
                raise ValueError(msg)
            membership = PythonImmediatePackageMembership(
                derivation_identity=derivation.identity,
                child=child,
                package=package,
            )
            memberships.append(membership)
        assessments.append(
            PythonImmediatePackageMembershipAssessment(
                child=child,
                status=status,
                requested_parent_name=parent_name,
                observed_name_matches=matches,
                membership=membership,
            ),
        )
    return PythonImmediatePackageMembershipAnalysis(
        derivation=derivation,
        memberships=tuple(memberships),
        assessments=tuple(assessments),
        exclusions=interpretation_analysis.exclusions,
        coverage=PythonImmediatePackageMembershipCoverage(
            derivation_identity=derivation.identity,
            interpreted_count=len(interpretations),
            excluded_count=len(interpretation_analysis.exclusions),
            assessment_count=len(assessments),
            established_count=len(memberships),
        ),
    )


def _validate_inputs(
    snapshot: RepositorySnapshot,
    analysis: PythonModuleInterpretationAnalysis,
) -> None:
    if (
        analysis.repository_id != snapshot.repository_id
        or analysis.snapshot_id != snapshot.id
    ):
        msg = "Module interpretation analysis belongs to another snapshot."
        raise ValueError(msg)
    if len({item.identity for item in analysis.interpretations}) != len(
        analysis.interpretations,
    ):
        msg = "Module interpretation analysis repeats an interpretation."
        raise ValueError(msg)
    for item in analysis.interpretations:
        if (
            item.repository_id != snapshot.repository_id
            or item.snapshot_id != snapshot.id
            or item.module_root != analysis.module_root
            or item.resource != snapshot.resource_at(item.resource.address)
        ):
            msg = "Module interpretation differs from its snapshot or root."
            raise ValueError(msg)
    for exclusion in analysis.exclusions:
        if (
            exclusion.module_root != analysis.module_root
            or exclusion.resource != snapshot.resource_at(exclusion.resource.address)
        ):
            msg = "Module interpretation exclusion differs from its snapshot or root."
            raise ValueError(msg)


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
