# Copyright (c) 2026
"""Unresolved, snapshot-bound candidate witness hypotheses."""

from devtools.context.localization.association.hypothesis import (
    CandidateWitnessHypothesis,
    CandidateWitnessMember,
    CandidateWitnessView,
    LexicalMatchSupport,
    RoutedMatchSupport,
    WitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.association.structural import (
    MirroredResourceSupport,
    OwnerResourceSupport,
)

__all__ = [
    "CandidateWitnessHypothesis",
    "CandidateWitnessMember",
    "CandidateWitnessView",
    "LexicalMatchSupport",
    "MirroredResourceSupport",
    "OwnerResourceSupport",
    "RoutedMatchSupport",
    "WitnessHypothesisIdentity",
    "build_candidate_witness_view",
]
