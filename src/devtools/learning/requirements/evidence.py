# Copyright (c) 2026
"""Immutable attributed findings; concrete operations own their truth conditions."""

from dataclasses import dataclass
from enum import Enum

from devtools.learning.measurement.contracts import EvidenceReference


class RequirementVerdict(Enum):
    """Knowledge of one condition, independently of preference or authorization."""

    SATISFIED = "satisfied"
    UNSATISFIED = "unsatisfied"
    UNKNOWN = "unknown"


class FindingBasis(Enum):
    """Attribution of support; a reference or declaration cannot verify itself."""

    INPUT_INSPECTION = "input_inspection"
    CALLER_DECLARATION = "caller_declaration"
    VALIDATED_RETAINED_EVIDENCE = "validated_retained_evidence"
    ABSENT = "absent"


class ConditionState(Enum):
    """Separate uncertainty, conflict, conditional claims and observed support."""

    MISSING = "unresolved_information"
    VIOLATED = "known_violation"
    CONDITIONAL = "conditional_declaration"
    INSPECTED = "directly_supported"
    RETAINED = "retained_evidence_supported"


def validate_references(values: tuple[EvidenceReference, ...]) -> None:
    """Validate immutable attributed references without inspecting their sources."""
    if type(values) is not tuple or any(
        not isinstance(value, EvidenceReference) for value in values
    ):
        msg = "references must be an immutable tuple of EvidenceReference"
        raise TypeError(msg)


def canonical_verdict(value: Enum) -> RequirementVerdict:
    """Read shared meaning while preserving established family enum identity."""
    if not isinstance(value, Enum):
        msg = "finding verdict must be a typed enum"
        raise TypeError(msg)
    try:
        result = RequirementVerdict(value.value)
    except (TypeError, ValueError) as error:
        msg = "finding verdict must use the three supported meanings"
        raise TypeError(msg) from error
    if value.name != result.name:
        msg = "finding verdict name and meaning disagree"
        raise TypeError(msg)
    return result


def canonical_basis(value: Enum) -> FindingBasis:
    """Read attribution without promoting an original family finding's authority."""
    if not isinstance(value, Enum):
        msg = "finding basis must be a typed enum"
        raise TypeError(msg)
    try:
        result = FindingBasis(value.value)
    except (TypeError, ValueError) as error:
        msg = "finding basis must use a supported attribution"
        raise TypeError(msg) from error
    if value.name != result.name:
        msg = "finding basis name and meaning disagree"
        raise TypeError(msg)
    return result


@dataclass(frozen=True, slots=True)
class RequirementFinding[R: Enum, V: Enum, B: Enum]:
    """A named fact with validated support, never an overall eligibility score.

    Verdict/basis parameters preserve existing distinct family enum identities.
    Families specialize this value and check their exact runtime enum classes.
    Direct users can use the shared RequirementVerdict and FindingBasis.
    """

    requirement: R
    verdict: V
    basis: B
    explanation: str
    references: tuple[EvidenceReference, ...] = ()
    coordinates: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (
            not isinstance(self.requirement, Enum)
            or type(self.requirement.value) is not str
            or (not self.requirement.value.strip())
        ):
            msg = "requirement must be an enum with a nonempty named identity"
            raise TypeError(msg)
        verdict = canonical_verdict(self.verdict)
        basis = canonical_basis(self.basis)
        if type(self.explanation) is not str or not self.explanation.strip():
            msg = "finding requires a nonempty explanation"
            raise ValueError(msg)
        validate_references(self.references)
        if (
            type(self.coordinates) is not tuple
            or any(
                type(name) is not str or not name.strip() for name in self.coordinates
            )
            or len(set(self.coordinates)) != len(self.coordinates)
        ):
            msg = "coordinate identities must be unique immutable names"
            raise ValueError(msg)
        if basis is FindingBasis.ABSENT and verdict is not RequirementVerdict.UNKNOWN:
            msg = "absent evidence cannot establish a verdict"
            raise ValueError(msg)
        if basis is FindingBasis.VALIDATED_RETAINED_EVIDENCE and (not self.references):
            msg = "retained-evidence findings require explicit references"
            raise ValueError(msg)

    def _validate_family(
        self, requirement: type[Enum], verdict: type[Enum], basis: type[Enum],
    ) -> None:
        """Enforce a concrete family's public boundary before common validation."""
        if (
            not isinstance(self.requirement, requirement)
            or not isinstance(self.verdict, verdict)
            or (not isinstance(self.basis, basis))
        ):
            msg = "finding requirement/verdict/basis must use its family types"
            raise TypeError(msg)
        RequirementFinding.__post_init__(self)

    @property
    def state(self) -> ConditionState:
        """Project knowledge without interpreting requirement codes or prose."""
        verdict = canonical_verdict(self.verdict)
        basis = canonical_basis(self.basis)
        if verdict is RequirementVerdict.UNKNOWN:
            return ConditionState.MISSING
        if verdict is RequirementVerdict.UNSATISFIED:
            return ConditionState.VIOLATED
        if basis is FindingBasis.CALLER_DECLARATION:
            return ConditionState.CONDITIONAL
        if basis is FindingBasis.VALIDATED_RETAINED_EVIDENCE:
            return ConditionState.RETAINED
        return ConditionState.INSPECTED
