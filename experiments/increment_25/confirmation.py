# Copyright (c) 2026
# ruff: noqa: E501
"""Confirmation-only execution adapter for the frozen Increment-25 generator."""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Final, cast

from experiments.increment_25.development import (
    EXECUTION_SEMANTICS,
    LEXICAL_SEED_SIZE,
    _assert_judgment_artifact,
    _build_snapshot_corpus,
    _identity,
    _judgment_case,
    _materialize_git_snapshot,
    _task_card,
    generate_case,
)
from experiments.increment_25.task_population import TaskCard, validate_freeze

if TYPE_CHECKING:
    from collections.abc import Mapping

CONFIRMATION_SCHEMA: Final = "devtools-increment-25-confirmation-candidates-v1"
CONFIRMATION_JUDGMENT_SCHEMA: Final = (
    "devtools-increment-25-confirmation-judgment-input-v1"
)

__all__ = ["generate_case"]


class ConfirmationBoundaryError(ValueError):
    """Reject execution outside the frozen confirmation partition."""


@dataclass(frozen=True, slots=True)
class FrozenConfirmation:
    """Validated freeze metadata and its only executable task cards."""

    freeze_identity: str
    cards: tuple[TaskCard, ...]
    confirmation_case_ids: tuple[str, ...]
    development_case_ids: frozenset[str]
    reserve_case_ids: frozenset[str]

    def require_case(self, case_id: str) -> TaskCard:
        """Return a confirmation card or reject development/reserve/unknown work."""
        if case_id in self.development_case_ids:
            msg = f"Development case cannot execute in confirmation mode: {case_id}."
            raise ConfirmationBoundaryError(msg)
        if case_id in self.reserve_case_ids:
            msg = f"Reserve case cannot execute in confirmation mode: {case_id}."
            raise ConfirmationBoundaryError(msg)
        for card in self.cards:
            if card.case_id == case_id:
                return card
        msg = f"Case is not in the frozen confirmation partition: {case_id}."
        raise ConfirmationBoundaryError(msg)


def load_frozen_confirmation(path: Path) -> FrozenConfirmation:
    """Load the immutable freeze while exposing confirmation cards only."""
    envelope = cast(
        "dict[str, object]",
        json.loads(path.read_text(encoding="utf-8")),
    )
    if not validate_freeze(envelope):
        msg = "Increment-25 task-population freeze failed validation."
        raise ValueError(msg)
    payload = cast("dict[str, object]", envelope["payload"])
    split = cast("dict[str, list[str]]", payload["split"])
    confirmation_ids = tuple(split["confirmation_case_ids"])
    development_ids = frozenset(split["development_case_ids"])
    reserve_ids = frozenset(split["reserve_case_ids"])
    if (set(confirmation_ids) & development_ids) or (
        set(confirmation_ids) & reserve_ids
    ) or (development_ids & reserve_ids):
        msg = "Frozen Increment-25 partitions overlap."
        raise ValueError(msg)
    cards_by_id = {
        str(item["case_id"]): _task_card(item)
        for item in cast("list[dict[str, object]]", payload["task_cards"])
    }
    if any(case_id not in cards_by_id for case_id in confirmation_ids):
        msg = "Frozen confirmation partition references a missing task card."
        raise ValueError(msg)
    return FrozenConfirmation(
        freeze_identity=str(envelope["content_identity"]),
        cards=tuple(cards_by_id[case_id] for case_id in confirmation_ids),
        confirmation_case_ids=confirmation_ids,
        development_case_ids=development_ids,
        reserve_case_ids=reserve_ids,
    )


def run_confirmation(
    *, repository_root: Path, freeze_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    """Execute all and only frozen confirmation cases with the validated generator."""
    frozen = load_frozen_confirmation(freeze_path)
    case_payloads: list[dict[str, object]] = []
    judgment_cases: list[dict[str, object]] = []
    for case_id in frozen.confirmation_case_ids:
        card = frozen.require_case(case_id)
        with tempfile.TemporaryDirectory(prefix=f"devtools-i25-{case_id}-") as raw:
            snapshot_root = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=snapshot_root,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=snapshot_root,
                source_roots=card.corpus_source_roots,
            )
            case = generate_case(card=card, corpus=corpus)
            case_payloads.append(case)
            judgment_cases.append(
                _judgment_case(card=card, case=case, snapshot=corpus.snapshot),
            )
    evidence: dict[str, object] = {
        "schema": CONFIRMATION_SCHEMA,
        "execution": {
            "generator_semantics": EXECUTION_SEMANTICS,
            "freeze_identity": frozen.freeze_identity,
            "mode": "confirmation-only",
            "case_count": len(case_payloads),
            "canonical_lexical": "content BM25 + 0.25 * filename-stem BM25",
            "lexical_seed_size": LEXICAL_SEED_SIZE,
            "structural_rule": "outgoing resolved imported-member binding to defining resource; one facade; one hop",
        },
        "cases": case_payloads,
    }
    judgment: dict[str, object] = {
        "schema": CONFIRMATION_JUDGMENT_SCHEMA,
        "execution_identity": _identity(evidence),
        "scope": "neutral confirmation resources awaiting human judgment",
        "cases": judgment_cases,
    }
    _assert_confirmation_artifact(evidence, frozen=frozen)
    _assert_judgment_artifact(judgment)
    return evidence, judgment


def _assert_confirmation_artifact(
    artifact: Mapping[str, object], *, frozen: FrozenConfirmation,
) -> None:
    cases = cast("list[dict[str, object]]", artifact["cases"])
    case_ids = tuple(str(case["case_id"]) for case in cases)
    if case_ids != frozen.confirmation_case_ids:
        msg = "Confirmation artifact does not contain exactly the frozen confirmation cases."
        raise RuntimeError(msg)
    if set(case_ids) & (frozen.development_case_ids | frozen.reserve_case_ids):
        msg = "Development or reserve outcomes contaminated the confirmation artifact."
        raise RuntimeError(msg)
