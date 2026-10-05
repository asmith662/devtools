# Copyright (c) 2026
"""Unresolved, snapshot-bound candidate witness hypotheses."""

from devtools.context.localization.association.hypothesis import (
    CandidateWitnessHypothesis,
    CandidateWitnessMember,
    CandidateWitnessView,
    GeneratedWitnessHypothesisIdentity,
    LexicalMatchSupport,
    RoutedMatchSupport,
    WitnessHypothesisFamilyIdentity,
    WitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.association.imports import (
    PythonImportDependencyProjectionRequest,
    PythonImportDependencyResourceSupport,
    PythonImportDependencySourceInput,
)
from devtools.context.localization.association.references import (
    PythonReferenceProjectionRequest,
    PythonReferenceResourceSupport,
    PythonReferenceSourceInput,
)
from devtools.context.localization.association.structural import (
    MirroredResourceSupport,
    OwnerResourceSupport,
)

__all__ = [
    "CandidateWitnessHypothesis",
    "CandidateWitnessMember",
    "CandidateWitnessView",
    "GeneratedWitnessHypothesisIdentity",
    "LexicalMatchSupport",
    "MirroredResourceSupport",
    "OwnerResourceSupport",
    "PythonImportDependencyProjectionRequest",
    "PythonImportDependencyResourceSupport",
    "PythonImportDependencySourceInput",
    "PythonReferenceProjectionRequest",
    "PythonReferenceResourceSupport",
    "PythonReferenceSourceInput",
    "RoutedMatchSupport",
    "WitnessHypothesisFamilyIdentity",
    "WitnessHypothesisIdentity",
    "build_candidate_witness_view",
]
