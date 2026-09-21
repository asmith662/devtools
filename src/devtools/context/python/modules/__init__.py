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

__all__ = [
    "PythonModuleInterpretation",
    "PythonModuleInterpretationAnalysis",
    "PythonModuleInterpretationExclusion",
    "PythonModuleInterpretationExclusionReason",
    "PythonModuleInterpretationUniverse",
    "PythonModuleKind",
    "PythonModuleRoot",
    "define_python_module_interpretation_universe",
    "interpret_python_module_resources",
]
