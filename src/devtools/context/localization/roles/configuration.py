# Copyright (c) 2026
"""Interpret declared configuration as positive soft supports, not tool behavior."""

from __future__ import annotations

from fnmatch import fnmatchcase
from typing import TYPE_CHECKING

from devtools.context.localization.roles.models import (
    RepositoryRoleKind,
    RepositoryRoleLimitation,
    RepositoryRoleSupport,
    RoleSupportKind,
)
from devtools.context.python.project_configuration.models import (
    PythonConfigurationSelector,
)

if TYPE_CHECKING:
    from devtools.context.localization.roles.models import (
        RepositoryRoleEvidenceInputs,
        RoleObservation,
    )
    from devtools.context.python.project_configuration.models import (
        PythonConfigurationDeclarationAnalysis,
        PythonConfigurationSetting,
        PythonConfigurationTargetFact,
    )

_R = RepositoryRoleKind
_K = RoleSupportKind
_PYTEST = ("tool", "pytest", "ini_options")
_HATCH_WHEEL = ("tool", "hatch", "build", "targets", "wheel")
_ASCII_PRINTABLE_START = 32
_ASCII_DELETE = 127
_PATTERN_SEMANTICS = "case-sensitive-posix-basename-glob-v1"


def configuration_supports(
    inputs: RepositoryRoleEvidenceInputs,
) -> tuple[tuple[RoleObservation, ...], tuple[RepositoryRoleLimitation, ...]]:
    """Keep declaration presence distinct from positive observed target matches."""
    observations: list[RoleObservation] = []
    limitations: list[RepositoryRoleLimitation] = []
    test_targets: dict[str, list[PythonConfigurationTargetFact]] = {}
    for resolution in inputs.configuration_targets:
        for fact in resolution.facts:
            if (
                fact.declaration.selector
                == PythonConfigurationSelector.PYTEST_TESTPATHS
            ):
                test_targets.setdefault(
                    resolution.declarations.derivation_identity,
                    [],
                ).append(fact)
                observations.append(
                    (
                        fact.target.address,
                        _R.TEST,
                        RepositoryRoleSupport(
                            _K.PYTEST_TESTPATH_TARGET,
                            fact.configuration.address,
                            (fact.identity,),
                            (fact.route, fact.requested),
                        ),
                    ),
                )
            elif fact.declaration.selector == PythonConfigurationSelector.README:
                observations.append(
                    (
                        fact.target.address,
                        _R.DOCUMENTATION,
                        RepositoryRoleSupport(
                            _K.README_TARGET,
                            fact.configuration.address,
                            (fact.identity,),
                            (fact.route, fact.requested),
                        ),
                    ),
                )
    for analysis in inputs.configurations:
        declared, omitted = _analysis_supports(
            analysis,
            tuple(test_targets.get(analysis.derivation_identity, ())),
        )
        observations.extend(declared)
        limitations.extend(omitted)
    return tuple(observations), tuple(limitations)


def _analysis_supports(
    analysis: PythonConfigurationDeclarationAnalysis,
    targets: tuple[PythonConfigurationTargetFact, ...],
) -> tuple[tuple[RoleObservation, ...], tuple[RepositoryRoleLimitation, ...]]:
    observations: list[RoleObservation] = []
    limitations: list[RepositoryRoleLimitation] = []
    for declaration in analysis.declarations:
        if declaration.unsupported_reason is None:
            roles, kind = _declaration_roles(declaration.key)
            support = RepositoryRoleSupport(
                kind,
                analysis.resource.address,
                (declaration.identity,),
                declaration.key,
            )
            observations.extend(
                (analysis.resource.address, role, support) for role in roles
            )
    settings = analysis.settings
    if settings is None:
        return tuple(observations), ()
    for setting in settings.declarations:
        if setting.unsupported_reason is None:
            roles, kind = _declaration_roles(setting.key)
            support = RepositoryRoleSupport(
                kind,
                analysis.resource.address,
                (setting.identity,),
                setting.key,
            )
            observations.extend(
                (analysis.resource.address, role, support) for role in roles
            )
        if setting.key == (*_PYTEST, "python_files"):
            matches, omitted = _pattern_supports(
                analysis,
                setting,
                targets,
            )
            observations.extend(matches)
            limitations.extend(omitted)
    for table in settings.recognized_tool_tables:
        roles, _ = _declaration_roles(table)
        support = RepositoryRoleSupport(
            _K.TOOL_TABLE,
            analysis.resource.address,
            (analysis.derivation_identity,),
            table,
        )
        observations.extend(
            (analysis.resource.address, role, support) for role in roles
        )

    return tuple(observations), tuple(limitations)


def _declaration_roles(
    key: tuple[str, ...],
) -> tuple[tuple[RepositoryRoleKind, ...], RoleSupportKind]:
    if key[0] == "project":
        return (_R.PROJECT_CONFIGURATION,), _K.PROJECT_DECLARATION
    if key[0] == "build-system":
        return (_R.PROJECT_CONFIGURATION, _R.BUILD_CONFIGURATION), _K.BUILD_DECLARATION
    if key[: len(_PYTEST)] == _PYTEST:
        return (
            _R.PROJECT_CONFIGURATION,
            _R.TOOL_CONFIGURATION,
            _R.TEST_CONFIGURATION,
        ), _K.PYTEST_DECLARATION
    if key[: len(_HATCH_WHEEL)] == _HATCH_WHEEL:
        return (
            _R.PROJECT_CONFIGURATION,
            _R.TOOL_CONFIGURATION,
            _R.BUILD_CONFIGURATION,
        ), _K.BUILD_DECLARATION
    return (_R.PROJECT_CONFIGURATION, _R.TOOL_CONFIGURATION), _K.TOOL_DECLARATION


def _pattern_supports(
    analysis: PythonConfigurationDeclarationAnalysis,
    setting: PythonConfigurationSetting,
    targets: tuple[PythonConfigurationTargetFact, ...],
) -> tuple[tuple[RoleObservation, ...], tuple[RepositoryRoleLimitation, ...]]:
    source = analysis.resource.address
    if setting.unsupported_reason is not None or not isinstance(setting.value, tuple):
        return (), (
            RepositoryRoleLimitation(
                source,
                setting.identity,
                setting.unsupported_reason or "scalar-pattern-syntax-not-interpreted",
            ),
        )
    if not targets:
        return (), (
            RepositoryRoleLimitation(
                source,
                setting.identity,
                "no-supplied-testpaths-targets",
            ),
        )
    observations: list[RoleObservation] = []
    limitations: list[RepositoryRoleLimitation] = []
    for ordinal, pattern in enumerate(setting.value):
        anchor = (str(ordinal), pattern)
        if (
            not pattern
            or any(character in pattern for character in "/\\")
            or any(
                ord(character) < _ASCII_PRINTABLE_START
                or ord(character) == _ASCII_DELETE
                for character in pattern
            )
        ):
            limitations.append(
                RepositoryRoleLimitation(
                    source,
                    setting.identity,
                    "outside-basename-pattern-scope",
                    anchor,
                ),
            )
            continue
        for fact in targets:
            basename = fact.target.address.parts[-1]
            if basename.endswith(".py") and fnmatchcase(basename, pattern):
                observations.append(
                    (
                        fact.target.address,
                        _R.TEST,
                        RepositoryRoleSupport(
                            _K.PYTEST_BASENAME_GLOB,
                            source,
                            (setting.identity, fact.identity),
                            (_PATTERN_SEMANTICS, *anchor),
                        ),
                    ),
                )
    return tuple(observations), tuple(limitations)
