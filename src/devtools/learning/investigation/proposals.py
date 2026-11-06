# Copyright (c) 2026
"""Closed untrusted scientific proposals and sanitized original observations."""

from __future__ import annotations

import json
from dataclasses import dataclass

from devtools.learning.integrations.local._codec import array
from devtools.learning.integrations.local._codec import nonempty_text as text
from devtools.learning.integrations.local._codec import retained_object as obj

_MAXIMUM_PROPOSAL_BYTES = 16384
_MAXIMUM_RATIONALE_CHARACTERS = 1024
_MAXIMUM_EVIDENCE_REFERENCES = 5


@dataclass(frozen=True, slots=True)
class LearningProposal:
    """An effect-free request; it contains neither raw code nor fitting authority."""

    task_identity: str
    source_handle: str
    family: str
    metric: str
    schema_identity: str
    unit_identity: str
    role: str
    state_identity: str
    evidence: tuple[str, ...]
    action: str
    method: str | None
    rationale: str

    @classmethod
    def materialize(cls, serialized: str) -> LearningProposal:
        """Reject extra meanings, malformed values and excessive disclosure sizes."""
        if len(serialized.encode()) > _MAXIMUM_PROPOSAL_BYTES:
            msg = "learning proposal is too large"
            raise ValueError(msg)

        def unique_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
            result = dict(pairs)
            if len(result) != len(pairs):
                msg = "duplicate learning proposal fields are ambiguous"
                raise ValueError(msg)
            return result

        d = obj(json.loads(serialized, object_pairs_hook=unique_fields))
        if set(d) != set(cls.__dataclass_fields__):
            msg = "unsupported learning proposal fields"
            raise ValueError(msg)
        strings = {
            k: text(v)
            for k, v in d.items()
            if k not in {"evidence", "method", "rationale"}
        }
        rationale = d["rationale"]
        if (
            not isinstance(rationale, str)
            or len(rationale) > _MAXIMUM_RATIONALE_CHARACTERS
        ):
            msg = "bounded textual rationale required"
            raise ValueError(msg)
        evidence = tuple(text(v) for v in array(d["evidence"]))
        if len(evidence) > _MAXIMUM_EVIDENCE_REFERENCES or len(set(evidence)) != len(
            evidence,
        ):
            msg = "bounded unique admitted evidence required"
            raise ValueError(msg)
        return cls(
            **strings,
            evidence=evidence,
            method=None if d["method"] is None else text(d["method"]),
            rationale=rationale,
        )


@dataclass(frozen=True, slots=True)
class LearningFeedback:
    """Original inspected online information, without protected labels or grants."""

    action: str
    method: str | None
    metric: str
    value: float | None
    evidence_identity: str
    nonvalue_reason: str | None = None
