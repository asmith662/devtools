# Copyright (c) 2026
"""Caller-directed bounded generation of unresolved witness hypotheses."""

from devtools.context.localization.generation.contract import (
    GenerationDisposition,
    GroundedMemberRecipe,
    HypothesisGenerationAttempt,
    MemberProjectionAttempt,
    ProjectionKind,
    WitnessGenerationPlan,
    WitnessGenerationRecipe,
    WitnessGenerationView,
)
from devtools.context.localization.generation.generate import (
    generate_witness_hypotheses,
)

__all__ = [
    "GenerationDisposition",
    "GroundedMemberRecipe",
    "HypothesisGenerationAttempt",
    "MemberProjectionAttempt",
    "ProjectionKind",
    "WitnessGenerationPlan",
    "WitnessGenerationRecipe",
    "WitnessGenerationView",
    "generate_witness_hypotheses",
]
