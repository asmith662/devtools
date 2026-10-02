# Copyright (c) 2026
"""Caller-authored repository information obligations and scoped readiness."""

from devtools.context.localization.assessment import (
    ApplicabilityStatus,
    DeferredDiscovery,
    Disposition,
    LocalizationAssessment,
    LocalizationEvidenceReference,
    SupportedWitness,
)
from devtools.context.localization.identity import (
    LocalizationAnchorIdentity,
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
    TaskTextSpan,
)
from devtools.context.localization.lexical import (
    LocalizationLexicalAcquisition,
    LocalizationLexicalAcquisitionRequest,
    ObligationLexicalEvidence,
    ObligationLexicalQuery,
    acquire_localization_lexical_evidence,
)
from devtools.context.localization.obligation import (
    LocalizationObligation,
    RequirementStatus,
    SatisfactionCriterion,
    WitnessSet,
)
from devtools.context.localization.readiness import (
    AssessedObligation,
    HandoffReadiness,
    LocalizationReadiness,
    assess_localization_readiness,
)
from devtools.context.localization.task import (
    LocalizationAnchor,
    LocalizationTaskInterpretation,
)

__all__ = [
    "ApplicabilityStatus",
    "AssessedObligation",
    "DeferredDiscovery",
    "Disposition",
    "HandoffReadiness",
    "LocalizationAnchor",
    "LocalizationAnchorIdentity",
    "LocalizationAssessment",
    "LocalizationEvidenceReference",
    "LocalizationLexicalAcquisition",
    "LocalizationLexicalAcquisitionRequest",
    "LocalizationObligation",
    "LocalizationObligationIdentity",
    "LocalizationQueryIdentity",
    "LocalizationReadiness",
    "LocalizationTaskIdentity",
    "LocalizationTaskInterpretation",
    "ObligationLexicalEvidence",
    "ObligationLexicalQuery",
    "RequirementStatus",
    "SatisfactionCriterion",
    "SupportedWitness",
    "TaskProvenance",
    "TaskTextSpan",
    "WitnessSet",
    "acquire_localization_lexical_evidence",
    "assess_localization_readiness",
]
