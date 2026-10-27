# Copyright (c) 2026
"""Bounded trusted configuration, separate from the existing CodingTask schema."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from devtools.context.localization import RequirementStatus, SatisfactionCriterion
from devtools.context.localization.resolution import MemberResolutionDisposition
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
)
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import FileFormat, TextFile, read

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.tasks import CodingTask

MAX_FRAME_BYTES = 8192
MAX_COORDINATE = 131072
MAX_OBLIGATIONS = 8
MAX_ALTERNATIVES = 4
MAX_MEMBERS = 16
SHA256_LENGTH = 64


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict(pairs)
    if len(result) != len(pairs):
        msg = "Obligation frame contains duplicate JSON members"
        raise ValueError(msg)
    return result


def _fields(value: Any, names: str) -> dict[str, Any]:  # noqa: ANN401 -- JSON boundary
    if not isinstance(value, dict) or set(value) != set(names.split()):
        msg = "Unexpected obligation frame fields"
        raise ValueError(msg)
    return value


def _text(value: Any, limit: int = 512) -> str:  # noqa: ANN401 -- JSON boundary
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        msg = "Obligation frame requires bounded nonblank text"
        raise ValueError(msg)
    return value


@dataclass(frozen=True, slots=True)
class Witness:
    """A caller decision conditional on disclosure of exact current source."""

    path: RepositoryResourceAddress
    version: ContentIdentity
    start: int
    end: int
    decision: MemberResolutionDisposition
    claim: str
    reason: str

    @classmethod
    def parse(cls, value: Any) -> Witness:  # noqa: ANN401 -- JSON boundary
        """Admit source coordinates and a named caller judgment, never model data."""
        v = _fields(value, "path version start end decision claim reason")
        if (
            type(v["start"]) is not int
            or type(v["end"]) is not int
            or not 0 <= v["start"] < v["end"] <= MAX_COORDINATE
        ):
            msg = "Witness requires a bounded nonempty character range"
            raise ValueError(msg)
        return cls(
            RepositoryResourceAddress(_text(v["path"])),
            ContentIdentity(_text(v["version"], 64)),
            v["start"],
            v["end"],
            MemberResolutionDisposition(v["decision"]),
            _text(v["claim"]),
            _text(v["reason"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Preserve native address/version spelling in the application frame."""
        return {
            "path": self.path.value,
            "version": self.version.value,
            "start": self.start,
            "end": self.end,
            "decision": self.decision.value,
            "claim": self.claim,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class Alternative:
    """One explicit all-member witness set competing with other alternatives."""

    key: str
    members: tuple[Witness, ...]

    @classmethod
    def parse(cls, value: Any) -> Alternative:  # noqa: ANN401 -- JSON boundary
        """Keep one member per native resource, as required by association."""
        v = _fields(value, "key members")
        if (
            not isinstance(v["members"], list)
            or not 1 <= len(v["members"]) <= MAX_OBLIGATIONS
        ):
            msg = "Alternative requires one to eight witnesses"
            raise ValueError(msg)
        members = tuple(Witness.parse(m) for m in v["members"])
        if len({m.path for m in members}) != len(members):
            msg = "Alternative repeats a resource witness"
            raise ValueError(msg)
        return cls(_text(v["key"], 64), members)

    def to_dict(self) -> dict[str, Any]:
        """Retain explicit complements and alternatives without inference."""
        return {"key": self.key, "members": [m.to_dict() for m in self.members]}


@dataclass(frozen=True, slots=True)
class Obligation:
    """Application configuration for existing Localization obligation values."""

    key: str
    predicate: str
    query: str
    requirement: RequirementStatus
    criterion: SatisfactionCriterion
    alternatives: tuple[Alternative, ...]

    @classmethod
    def parse(cls, value: Any) -> Obligation:  # noqa: ANN401 -- JSON boundary
        """Require explicit queries and criteria; do not formulate needs."""
        v = _fields(value, "key predicate query requirement criterion alternatives")
        c = _fields(v["criterion"], "name statement")
        if (
            not isinstance(v["alternatives"], list)
            or len(v["alternatives"]) > MAX_ALTERNATIVES
        ):
            msg = "Obligation alternatives exceed the bounded frame"
            raise ValueError(msg)
        alternatives = tuple(Alternative.parse(a) for a in v["alternatives"])
        if len({a.key for a in alternatives}) != len(alternatives) or len(
            {frozenset(m.path for m in a.members) for a in alternatives},
        ) != len(alternatives):
            msg = "Obligation repeats an alternative identity"
            raise ValueError(msg)
        return cls(
            _text(v["key"], 64),
            _text(v["predicate"]),
            _text(v["query"]),
            RequirementStatus(v["requirement"]),
            SatisfactionCriterion(_text(c["name"], 64), _text(c["statement"])),
            alternatives,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize only the host's declared information contract."""
        return {
            "key": self.key,
            "predicate": self.predicate,
            "query": self.query,
            "requirement": self.requirement.value,
            "criterion": {
                "name": self.criterion.name,
                "statement": self.criterion.statement,
            },
            "alternatives": [a.to_dict() for a in self.alternatives],
        }


@dataclass(frozen=True, slots=True)
class ObligationFrame:
    """Trusted opt-in frame; its hash does not change legacy task identities."""

    task_definition_sha256: str
    caller: str
    obligations: tuple[Obligation, ...]

    @classmethod
    def from_dict(cls, value: Any) -> ObligationFrame:  # noqa: ANN401 -- host JSON boundary
        """Admit a small immutable host declaration, not semantic model approval."""
        v = _fields(value, "schema task_definition_sha256 caller obligations")
        if v["schema"] != "qwen-obligation-frame-v1":
            msg = "Unsupported obligation frame schema"
            raise ValueError(msg)
        if (
            not isinstance(v["obligations"], list)
            or not 1 <= len(v["obligations"]) <= MAX_OBLIGATIONS
        ):
            msg = "Frame requires one to eight obligations"
            raise ValueError(msg)
        digest = _text(v["task_definition_sha256"], 64)
        if len(digest) != SHA256_LENGTH or any(
            c not in "0123456789abcdef" for c in digest
        ):
            msg = "Frame requires an exact CodingTask digest"
            raise ValueError(msg)
        obligations = tuple(Obligation.parse(o) for o in v["obligations"])
        if (
            len({o.key for o in obligations}) != len(obligations)
            or sum(len(a.members) for o in obligations for a in o.alternatives)
            > MAX_MEMBERS
        ):
            msg = "Frame repeats obligations or exceeds sixteen witness members"
            raise ValueError(msg)
        frame = cls(digest, _text(v["caller"], 128), obligations)
        if (
            len(json.dumps(frame.to_dict(), ensure_ascii=False).encode())
            > MAX_FRAME_BYTES
        ):
            msg = "Obligation frame byte bound exceeded"
            raise ValueError(msg)
        return frame

    @classmethod
    def load(cls, path: Path) -> ObligationFrame:
        """Read bounded host JSON through Resources, refusing duplicate members."""
        file = read(
            resolve_path(path),
            file_format=FileFormat.TEXT,
            max_bytes=MAX_FRAME_BYTES,
        )
        if not isinstance(file, TextFile):
            msg = "Expected a text obligation frame"
            raise TypeError(msg)
        return cls.from_dict(json.loads(file.content, object_pairs_hook=_object))

    def validate(self, task: CodingTask) -> None:
        """Bind the frame to the exact native task and its unchanged read scope."""
        # Revalidate even direct dataclass construction at this trusted boundary.
        if self.from_dict(self.to_dict()) != self:
            msg = "Invalid obligation frame value"
            raise ValueError(msg)
        scope = {p for p, _ in task.baseline_hashes}
        if (
            self.task_definition_sha256 != task.definition_sha256
            or task.context_mode != "on-demand"
        ):
            msg = "Obligation frame requires its exact native CodingTask"
            raise ValueError(msg)
        if any(
            m.path.value not in scope
            for o in self.obligations
            for a in o.alternatives
            for m in a.members
        ):
            msg = "Obligation witness is outside the authorized existing read scope"
            raise ValueError(msg)

    def to_dict(self) -> dict[str, Any]:
        """Keep optional application configuration separate from CodingTask."""
        return {
            "schema": "qwen-obligation-frame-v1",
            "task_definition_sha256": self.task_definition_sha256,
            "caller": self.caller,
            "obligations": [o.to_dict() for o in self.obligations],
        }

    @property
    def sha256(self) -> str:
        """Identify the exact normalized host declaration, not a new RI identity."""
        return hashlib.sha256(
            json.dumps(self.to_dict(), sort_keys=True).encode(),
        ).hexdigest()


def validate_frame(frame: ObligationFrame | None, task: CodingTask) -> None:
    """Validate optional host configuration before service or source operations."""
    if frame is not None:
        frame.validate(task)
