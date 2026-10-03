# Copyright (c) 2026
"""Derive soft role support independently of task, query, acquisition or ranking."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from devtools.context.localization.roles.configuration import configuration_supports
from devtools.context.localization.roles.inputs import validate_role_inputs
from devtools.context.localization.roles.models import (
    RepositoryRoleEvidenceInputs,
    RepositoryRoleEvidenceView,
    RepositoryRoleKind,
    RepositoryRoleSupport,
    ResourceRoleEvidence,
    RoleSupportKind,
    digest,
)
from devtools.context.python.modules import PythonModuleKind

if TYPE_CHECKING:
    from devtools.context.localization.roles.models import RoleObservation
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot

_R = RepositoryRoleKind
_K = RoleSupportKind
_EMPTY_INPUTS = RepositoryRoleEvidenceInputs()


def derive_repository_role_evidence(
    snapshot: RepositorySnapshot,
    *,
    inputs: RepositoryRoleEvidenceInputs = _EMPTY_INPUTS,
) -> RepositoryRoleEvidenceView:
    """Retain a complete observed frame and independently inspectable positive hints.

    Canonical inputs are validated/reproduced by their owners, not reinterpreted
    as relevance or witnesses. Repeated native presentation is deduplicated.
    """
    resources = tuple(sorted(snapshot.resources, key=lambda item: item.address.value))
    if len({item.address for item in resources}) != len(resources):
        msg = "Role-evidence snapshot repeats a resource address."
        raise ValueError(msg)
    canonical, dependencies = validate_role_inputs(snapshot, inputs)
    derivation = digest(
        RepositoryRoleEvidenceView.SEMANTICS,
        str(snapshot.repository_id),
        str(snapshot.id),
        tuple((item.address.value, item.content_identity.value) for item in resources),
        dependencies,
    )
    observations = list(_intrinsic_supports(resources))
    observations.extend(_structural_supports(canonical))
    configured, limitations = configuration_supports(canonical)
    observations.extend(configured)
    grouped: dict[
        tuple[RepositoryResourceAddress, RepositoryRoleKind],
        dict[str, RepositoryRoleSupport],
    ] = {}
    for address, role, support in observations:
        grouped.setdefault((address, role), {})[support.identity] = support
    evidence = []
    for (address, role), supports in sorted(
        grouped.items(),
        key=lambda item: (item[0][0].value, item[0][1].value),
    ):
        evidence.append(
            ResourceRoleEvidence(
                snapshot.repository_id,
                snapshot.id,
                derivation,
                snapshot.resource_at(address),
                role,
                tuple(supports[key] for key in sorted(supports)),
            ),
        )
    return RepositoryRoleEvidenceView(
        snapshot.repository_id,
        snapshot.id,
        derivation,
        resources,
        canonical,
        tuple(evidence),
        tuple(
            sorted(
                set(limitations),
                key=lambda item: (
                    item.source_address.value,
                    item.native_identity,
                    item.reason,
                    item.observation,
                ),
            ),
        ),
    )


def _intrinsic_supports(
    resources: tuple[RepositoryResourceOccurrence, ...],
) -> tuple[RoleObservation, ...]:
    observations: list[RoleObservation] = []
    for resource in resources:
        path = PurePosixPath(resource.address.value)
        rules = (
            (
                path.suffix == ".py",
                _R.PYTHON_CODE,
                _K.PYTHON_SUFFIX_CONVENTION,
                (path.suffix,),
            ),
            (
                path.suffix.casefold() == ".md",
                _R.DOCUMENTATION,
                _K.MARKDOWN_SUFFIX_CONVENTION,
                (path.suffix,),
            ),
            (
                "tests" in resource.address.parts[:-1],
                _R.TEST,
                _K.TEST_DIRECTORY_CONVENTION,
                ("tests",),
            ),
            (
                "docs" in resource.address.parts[:-1],
                _R.DOCUMENTATION,
                _K.DOCUMENTATION_DIRECTORY_CONVENTION,
                ("docs",),
            ),
            (
                path.name.casefold()
                in {"readme", "readme.md", "readme.rst", "readme.txt"},
                _R.DOCUMENTATION,
                _K.README_NAME_CONVENTION,
                (path.name,),
            ),
            (
                path.name == "pyproject.toml",
                _R.PROJECT_CONFIGURATION,
                _K.PYPROJECT_NAME_CONVENTION,
                (path.name,),
            ),
            (
                path.name == "__init__.py",
                _R.PACKAGE_SURFACE,
                _K.INITIALIZER_NAME_CONVENTION,
                (path.name,),
            ),
        )
        observations.extend(
            (
                resource.address,
                role,
                RepositoryRoleSupport(kind, resource.address, (), detail),
            )
            for matched, role, kind, detail in rules
            if matched
        )
    return tuple(observations)


def _structural_supports(
    inputs: RepositoryRoleEvidenceInputs,
) -> tuple[RoleObservation, ...]:
    observations: list[RoleObservation] = []
    for module_analysis in inputs.modules:
        for module in module_analysis.interpretations:
            support = RepositoryRoleSupport(
                _K.MODULE_INTERPRETATION,
                module.resource.address,
                (module.identity,),
                (module.module_root.value, module.dotted_name, module.kind.value),
            )
            observations.append((module.resource.address, _R.PYTHON_CODE, support))
            if module.kind == PythonModuleKind.PACKAGE:
                observations.append(
                    (
                        module.resource.address,
                        _R.PACKAGE_SURFACE,
                        RepositoryRoleSupport(
                            _K.PACKAGE_INTERPRETATION,
                            module.resource.address,
                            (module.identity,),
                            support.observation,
                        ),
                    ),
                )
    for membership_analysis in inputs.memberships:
        for fact in membership_analysis.memberships:
            support = RepositoryRoleSupport(
                _K.PACKAGE_MEMBERSHIP,
                fact.child.resource.address,
                (fact.identity,),
                (fact.package.resource.address.value,),
            )
            observations.append(
                (fact.child.resource.address, _R.PACKAGE_MEMBER, support),
            )
            observations.append(
                (fact.package.resource.address, _R.PACKAGE_SURFACE, support),
            )
    for mirror_analysis in inputs.mirrors:
        observations.extend(
            (
                pair.test.address,
                _R.TEST,
                RepositoryRoleSupport(
                    _K.MIRRORED_TEST_PATH,
                    pair.test.address,
                    (pair.identity,),
                    (pair.source.address.value,),
                ),
            )
            for pair in mirror_analysis.correspondences
        )
    return tuple(observations)
