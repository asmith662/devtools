# Copyright (c) 2026
"""Explicit-root repository Python-module interpretation."""

from devtools.context.python.modules.interpretation import (
    PythonModuleInterpretation,
    PythonModuleInterpretationAnalysis,
    PythonModuleInterpretationExclusion,
    PythonModuleInterpretationExclusionReason,
    PythonModuleInterpretationUniverse,
    PythonModuleKind,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.modules.lookup import lookup_python_modules
from devtools.context.python.modules.membership import (
    PythonImmediatePackageMembership,
    PythonImmediatePackageMembershipAnalysis,
    PythonImmediatePackageMembershipAssessment,
    PythonImmediatePackageMembershipCoverage,
    PythonImmediatePackageMembershipDerivation,
    PythonImmediatePackageMembershipStatus,
    derive_python_immediate_package_memberships,
)

__all__ = [
    "PythonImmediatePackageMembership",
    "PythonImmediatePackageMembershipAnalysis",
    "PythonImmediatePackageMembershipAssessment",
    "PythonImmediatePackageMembershipCoverage",
    "PythonImmediatePackageMembershipDerivation",
    "PythonImmediatePackageMembershipStatus",
    "PythonModuleInterpretation",
    "PythonModuleInterpretationAnalysis",
    "PythonModuleInterpretationExclusion",
    "PythonModuleInterpretationExclusionReason",
    "PythonModuleInterpretationUniverse",
    "PythonModuleKind",
    "PythonModuleRoot",
    "define_python_module_interpretation_universe",
    "derive_python_immediate_package_memberships",
    "interpret_python_module_resources",
    "lookup_python_modules",
]
