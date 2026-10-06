# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- bounded experimental capture validation
"""Immutable diagnostic input projections retaining native semantic identities."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Literal

from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalBm25Settings

if TYPE_CHECKING:
    from devtools.context.localization.identity import LocalizationObligationIdentity
    from devtools.context.repository.corpus import RepositoryTextCorpusId
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshotId

type Label = Literal["REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED"]
type Analyzer = Literal["canonical", "identifier"]


@dataclass(frozen=True, slots=True)
class Frame:
    """Retain the native repository, snapshot and selected corpus identities."""

    repository: RepositoryId
    snapshot: RepositorySnapshotId
    corpus: RepositoryTextCorpusId


@dataclass(frozen=True, slots=True)
class Configuration:
    """Identify externally named treatment/index and explicit scoring settings."""

    treatment: str
    index_identity: str
    analyzer: Analyzer
    k1: float
    b: float
    filename_weight: float

    def __post_init__(self) -> None:
        """Reject unnamed or unsupported configurations, without choosing values."""
        RepositoryTextLexicalBm25Settings(k1=self.k1, b=self.b)
        if (
            not self.treatment
            or not self.index_identity
            or self.analyzer not in {"canonical", "identifier"}
            or not math.isfinite(self.filename_weight)
            or self.filename_weight < 0
        ):
            raise ValueError("Invalid diagnostic configuration.")

    @property
    def identity(self) -> str:
        """Hash the full experimental configuration, never invent a framework ID."""
        return hashlib.sha256(
            json.dumps(asdict(self), sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()


@dataclass(frozen=True, slots=True)
class DiagnosticSubject:
    """Identify one exact lane/resource/treatment in a frozen frame."""

    frame: Frame
    lane: str
    resource: RepositoryResourceOccurrence
    configuration: Configuration
    query: str


@dataclass(frozen=True, slots=True)
class Judgment:
    """Attach caller-owned independent obligation relevance and information units."""

    frame: Frame
    resource: RepositoryResourceOccurrence
    obligation: LocalizationObligationIdentity
    label: Label
    units: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Keep unknown distinct from negative and unit references unique."""
        if self.label not in {
            "REQUIRED",
            "HELPFUL_ONLY",
            "UNNECESSARY",
            "UNRESOLVED",
        } or len(set(self.units)) != len(self.units):
            raise ValueError("Invalid independent judgment.")


@dataclass(frozen=True, slots=True)
class FieldStatistics:
    """Project preexisting field statistics and text for source-span replay."""

    name: str
    weight: float
    texts: tuple[str, ...]
    lengths: tuple[int, ...]
    average_length: float
    postings: tuple[tuple[str, tuple[tuple[int, int], ...]], ...]


@dataclass(frozen=True, slots=True)
class TermCapture:
    """Retain the already captured ranker evidence, without inferred importance."""

    field: str
    term: str
    tf: int
    df: int
    length: int
    average_length: float
    idf: float
    contribution: float


@dataclass(frozen=True, slots=True)
class RankedCapture:
    """Retain one observed positive score and rank from the actual ranker."""

    resource: RepositoryResourceOccurrence
    rank: int
    score: float
    terms: tuple[TermCapture, ...]


@dataclass(frozen=True, slots=True)
class Exclusion:
    """Retain an explicit caller eligibility reason, never infer it from a miss."""

    resource: RepositoryResourceOccurrence
    reason: Literal["UNSUPPORTED_RESOURCE_TYPE", "RESOURCE_NOT_IN_FRAME"]

    def __post_init__(self) -> None:
        """Reject unsupported caller exclusion reasons."""
        if self.reason not in {"UNSUPPORTED_RESOURCE_TYPE", "RESOURCE_NOT_IN_FRAME"}:
            raise ValueError("Invalid exclusion reason.")


@dataclass(frozen=True, slots=True)
class LaneCapture:
    """Consume one ranked capture and its exact representation/statistics frame."""

    frame: Frame
    lane: str
    query: str
    query_terms: tuple[str, ...]
    configuration: Configuration
    resources: tuple[RepositoryResourceOccurrence, ...]
    fields: tuple[FieldStatistics, ...]
    rows: tuple[RankedCapture, ...]
    complete_positive_universe: bool
    obligation: LocalizationObligationIdentity | None = None
    exclusions: tuple[Exclusion, ...] = ()


@dataclass(frozen=True, slots=True)
class SupportReference:
    """Attach an existing positive observation by identity, not semantic necessity."""

    frame: Frame
    resource: RepositoryResourceOccurrence
    kind: Literal["EXACT", "STRUCTURAL", "ROLE"]
    identity: str
    provenance: str

    def __post_init__(self) -> None:
        """Require a known positive evidence kind and explicit provenance."""
        if (
            self.kind not in {"EXACT", "STRUCTURAL", "ROLE"}
            or not self.identity
            or not self.provenance
        ):
            raise ValueError("Invalid positive support reference.")


@dataclass(frozen=True, slots=True)
class DiagnosticPolicy:
    """Name descriptive thresholds explicitly; never use them to rank or tune."""

    substantial_unnecessary_ahead: int = 20
    common_fraction: float = 0.25
    low_idf: float = 1.5
    overtaker_limit: int = 5

    def __post_init__(self) -> None:
        """Require finite, bounded inspection thresholds."""
        if (
            self.substantial_unnecessary_ahead < 1
            or self.overtaker_limit < 0
            or not 0 <= self.common_fraction <= 1
            or not math.isfinite(self.low_idf)
            or self.low_idf < 0
        ):
            raise ValueError("Invalid descriptive diagnostic policy.")
