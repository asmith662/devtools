# Copyright (c) 2026
"""Policy-free evidence-to-witness resolution recording and explicit promotion."""

from devtools.context.localization.resolution.contract import (
    CandidateHypothesisResolution,
    CandidateMemberResolution,
    HypothesisResolutionDisposition,
    MemberResolutionDisposition,
)
from devtools.context.localization.resolution.promotion import (
    PromotedWitnessHypothesis,
    promote_supported_hypothesis,
)
from devtools.context.localization.resolution.view import WitnessResolutionView

__all__ = [
    "CandidateHypothesisResolution",
    "CandidateMemberResolution",
    "HypothesisResolutionDisposition",
    "MemberResolutionDisposition",
    "PromotedWitnessHypothesis",
    "WitnessResolutionView",
    "promote_supported_hypothesis",
]
