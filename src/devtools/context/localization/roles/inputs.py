# Copyright (c) 2026
"""Validate native RI inputs against exact retained snapshot semantics."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from devtools.context.localization.roles.models import (
    RepositoryRoleEvidenceInputs,
    digest,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules import (
    PythonModuleInterpretationAnalysis,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.python.project_configuration import (
    analyze_python_project_configuration,
    resolve_python_project_configuration,
)

if TYPE_CHECKING:
    from devtools.context.python.modules.membership import (
        PythonImmediatePackageMembershipAnalysis,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


def validate_role_inputs(
    snapshot: RepositorySnapshot,
    inputs: RepositoryRoleEvidenceInputs,
) -> tuple[RepositoryRoleEvidenceInputs, tuple[str, ...]]:
    """Reject stale/forged inputs, normalize presentation and retain native scopes."""
    modules = {}
    memberships = {}
    mirrors = {}
    configurations = {}
    targets = {}
    for module_input in inputs.modules:
        canonical = _module_analysis(snapshot, module_input)
        identity = digest(
            "role-module-input-v1",
            canonical.module_root.value,
            tuple(module.identity for module in canonical.interpretations),
            tuple(
                (excluded.resource.address.value, excluded.reason.value)
                for excluded in canonical.exclusions
            ),
        )
        modules[identity] = canonical
    for membership_input in inputs.memberships:
        canonical_membership = _membership_analysis(snapshot, membership_input)
        memberships[canonical_membership.derivation.identity] = canonical_membership
    for mirror_input in inputs.mirrors:
        canonical_mirror = derive_python_mirrored_path_correspondences(snapshot)
        if mirror_input != canonical_mirror:
            msg = "Role mirror analysis differs from the retained snapshot."
            raise ValueError(msg)
        mirrors[mirror_input.derivation.identity] = mirror_input
    for configuration_input in (
        *inputs.configurations,
        *(target.declarations for target in inputs.configuration_targets),
    ):
        canonical_configuration = analyze_python_project_configuration(
            snapshot,
            address=configuration_input.resource.address,
        )
        if configuration_input != canonical_configuration:
            msg = "Role configuration analysis differs from the retained snapshot."
            raise ValueError(msg)
        configurations[configuration_input.derivation_identity] = configuration_input
    for target_input in inputs.configuration_targets:
        canonical_targets = resolve_python_project_configuration(
            snapshot,
            target_input.declarations,
            universe=target_input.universe,
            frame=target_input.frame,
        )
        if target_input != canonical_targets:
            msg = "Role configuration targets differ from the retained snapshot."
            raise ValueError(msg)
        targets[target_input.derivation_identity] = target_input
    return RepositoryRoleEvidenceInputs(
        tuple(modules[key] for key in sorted(modules)),
        tuple(memberships[key] for key in sorted(memberships)),
        tuple(mirrors[key] for key in sorted(mirrors)),
        tuple(configurations[key] for key in sorted(configurations)),
        tuple(targets[key] for key in sorted(targets)),
    ), tuple(
        digest(family, tuple(sorted(collection)))
        for family, collection in (
            ("modules", modules),
            ("memberships", memberships),
            ("mirrors", mirrors),
            ("configurations", configurations),
            ("targets", targets),
        )
    )


def _module_analysis(
    snapshot: RepositorySnapshot,
    analysis: PythonModuleInterpretationAnalysis,
) -> PythonModuleInterpretationAnalysis:
    selected = tuple(
        item.resource.address for item in analysis.interpretations
    ) + tuple(item.resource.address for item in analysis.exclusions)
    canonical = interpret_python_module_resources(
        snapshot,
        module_root=analysis.module_root,
        resource_addresses=selected,
    )
    if analysis != canonical:
        msg = "Role module analysis differs from the retained snapshot."
        raise ValueError(msg)
    return replace(
        canonical,
        interpretations=tuple(
            sorted(canonical.interpretations, key=lambda item: item.identity),
        ),
        exclusions=tuple(
            sorted(canonical.exclusions, key=lambda item: item.resource.address.value),
        ),
    )


def _membership_analysis(
    snapshot: RepositorySnapshot,
    analysis: PythonImmediatePackageMembershipAnalysis,
) -> PythonImmediatePackageMembershipAnalysis:
    module_analysis = PythonModuleInterpretationAnalysis(
        analysis.derivation.repository_id,
        analysis.derivation.snapshot_id,
        analysis.derivation.module_root,
        tuple(item.child for item in analysis.assessments),
        analysis.exclusions,
    )
    # Verify structural interpretations before trusting a supplied relationship.
    normalized = _module_analysis(snapshot, module_analysis)
    canonical = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=module_analysis,
    )
    if analysis != canonical:
        msg = "Role package membership differs from the retained snapshot."
        raise ValueError(msg)
    return derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=normalized,
    )
