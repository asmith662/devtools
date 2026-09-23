# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, SLF001
"""Tests for the frozen Increment-25 confirmation boundary."""

from __future__ import annotations

from pathlib import Path

import pytest

from experiments.increment_25 import confirmation, development
from experiments.increment_25.confirmation import (
    ConfirmationBoundaryError,
    load_frozen_confirmation,
)
from experiments.increment_25.run_confirmation import parse_arguments

_FREEZE = Path("experiments/increment_25/task_population_freeze.json")


def test_confirmation_partition_is_exact_and_uses_committed_generator() -> None:
    frozen = load_frozen_confirmation(_FREEZE)

    assert len(frozen.cards) == 16
    assert tuple(card.case_id for card in frozen.cards) == frozen.confirmation_case_ids
    assert confirmation.generate_case is development.generate_case


def test_development_reserve_and_unknown_confirmation_execution_are_rejected() -> None:
    frozen = load_frozen_confirmation(_FREEZE)

    with pytest.raises(ConfirmationBoundaryError, match="Development case"):
        frozen.require_case(next(iter(frozen.development_case_ids)))
    with pytest.raises(ConfirmationBoundaryError, match="Reserve case"):
        frozen.require_case(next(iter(frozen.reserve_case_ids)))
    with pytest.raises(ConfirmationBoundaryError, match="not in"):
        frozen.require_case("not-frozen")


def test_confirmation_cli_has_no_partition_selection() -> None:
    parsed = parse_arguments(
        [
            "--candidate-output",
            "candidate.json",
            "--judgment-output",
            "judgment.json",
        ],
    )
    assert vars(parsed).keys() == {
        "repository_root",
        "freeze",
        "candidate_output",
        "judgment_output",
    }


def test_confirmation_artifact_rejects_nonconfirmation_case() -> None:
    frozen = load_frozen_confirmation(_FREEZE)
    cases = [{"case_id": case_id} for case_id in frozen.confirmation_case_ids]
    cases[-1] = {"case_id": next(iter(frozen.reserve_case_ids))}

    with pytest.raises(RuntimeError, match="exactly"):
        confirmation._assert_confirmation_artifact({"cases": cases}, frozen=frozen)
